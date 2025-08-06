import atexit
import fcntl
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import apps
from django.forms import ModelForm
from django_apscheduler.jobstores import DjangoJobStore,register_events,register_job,MemoryJobStore
from django.db.models import Count,Q,Case,Sum,When,IntegerField,Max
from django.db import transaction
from django.core.cache import cache
from PMIS.Services.TaskService import TaskService
from PMIS.Services.UserService import UserService
from PMISLooper.Services.NotificationService import NotificationService
from DataBase_MPMS import models
import dateutil.relativedelta
import datetime
import re
from django.http import JsonResponse,HttpResponse,HttpRequest
from django.conf import settings
from django.db import connections
from ScheduleApp.Services.ScheduleServer import ScheduleServer
from PMISLooper.Services.NtfyNotificationServer import NtfyNotificationService,NOTIFICATION_DELAY_RESEND_TASK
from django.db.models import Q,F
from datetime import date
from django.utils import timezone
from django.db import models as model_db
from BaseApp.library.tools import ModelTools
import os
from time import sleep

LOGGER = logging.getLogger(__name__)
f = open("scheduler.lock", "wb")
try:
    fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)   # 加锁
    scheduler = BackgroundScheduler() # 建一個調度器對象
    #scheduler.add_jobstore(DjangoJobStore(), "default") # 添加一個作業
    scheduler.add_jobstore(MemoryJobStore(), "default") # 添加一個作業

    #同步DetailPlanner和對應任務
    def sync_PMS_task():
        print("-->開始獲取PMS任務差異數據")
        now = datetime.datetime.now()
        monthago = now + dateutil.relativedelta.relativedelta(months=-1)#一個月前
        monthago.strftime('%Y-%m')
        DailyPlannerlist = []
        Tasklist = []
        #同步最近一個月的TecDailyPlanner表
        DailyPlanner_sql = """SELECT TecDailyPlanner.*,Task.TaskType,Task.SubTaskType,
                            Task.Diff,Task.Task,Task.MODI_DATE T_MODI_DATE,Task.UDF04 T_UDF04,Task.Progress FROM TecDailyPlanner
                            LEFT JOIN Task ON TRIM(Pid)+'-'+TRIM(STR(Tid))+'-'+TRIM(STR(TaskID)) = TRIM(TaskNo)
                            WHERE TecDailyPlanner.MODI_DATE<Task.MODI_DATE AND InputDate>'{}'""".format(monthago.strftime('%Y%m'))
        update_TecDailyPlanner = list()
        with connections['MPMS'].cursor() as cursor: 
            cursor.execute(DailyPlanner_sql,[])
            fields = [field[0] for field in cursor.description]
            for item in cursor.fetchall():  
                update_TecDailyPlanner.append(dict(list(zip(fields, item))))
        for DailyPlanner in update_TecDailyPlanner:
            tasktype = DailyPlanner['TaskType']
            subtasktype = DailyPlanner['SubTaskType']
            diff = 'difficulties1'
            if DailyPlanner['Diff'] != None:
                diff = 'difficulties'+str(DailyPlanner['Diff'])
            if tasktype != None and subtasktype != None and diff != None and tasktype != '' and subtasktype != '' and diff != '' :            
                theType = list(models.Tasktypelist.objects.filter(tasktype=tasktype).values('description'))
                thesubType = list(models.Tasktypelist.objects.filter(tasktype=subtasktype).values('description'))
                score = list(models.Tasktypelist.objects.filter(tasktype=subtasktype,parenttype=tasktype).values(diff))
                if len(theType)>0:
                    DailyPlanner['TaskType'] = theType[0]['description']
                if len(thesubType)>0:
                    DailyPlanner['SubTaskType'] = thesubType[0]['description']
                if len(score)>0:
                    DailyPlanner['Diff'] = score[0][diff]
            M_TecDailyPlanner = models.Tecdailyplanner()
            M_TecDailyPlanner.inc_id = DailyPlanner['INC_ID']
            M_TecDailyPlanner.modi_date = DailyPlanner['T_MODI_DATE']
            M_TecDailyPlanner.taskdescription = DailyPlanner['Task']
            M_TecDailyPlanner.framespecification = DailyPlanner['T_UDF04']
            M_TecDailyPlanner.status = DailyPlanner['Progress']
            M_TecDailyPlanner.tasktype = f"{DailyPlanner['TaskType']}-->{DailyPlanner['SubTaskType']}"
            DailyPlannerlist.append(M_TecDailyPlanner)

        #同步最近一個月的Task表
        Task_sql = """SELECT Task.*,TecDailyPlanner.MODI_DATE D_MODI_DATE,TecDailyPlanner.TaskDescription,
                    TecDailyPlanner.FrameSpecification,TecDailyPlanner.Status FROM Task
                    LEFT JOIN TecDailyPlanner ON TRIM(Pid)+'-'+TRIM(STR(Tid))+'-'+TRIM(STR(TaskID)) = TRIM(TaskNo)
                    WHERE TecDailyPlanner.MODI_DATE>Task.MODI_DATE AND InputDate>'{}'""".format(monthago.strftime('%Y%m'))
        update_Task = list()
        with connections['MPMS'].cursor() as cursor: 
            cursor.execute(Task_sql,[])
            fields = [field[0] for field in cursor.description]
            for item in cursor.fetchall():  
                update_Task.append(dict(list(zip(fields, item))))
            for task in update_Task:
                M_Task = models.Tecdailyplanner()
                M_Task.inc_id = task['INC_ID']
                M_Task.modi_date = task['D_MODI_DATE']
                M_Task.task = task['TaskDescription']
                M_Task.udf04 = task['FrameSpecification']
                M_Task.progress = task['Status']
                Tasklist.append(M_Task)
        print("-->開始同步PMS任務數據")
        with transaction.atomic(using='MPMS'):
            save_id = transaction.savepoint(using='MPMS')
            try:
                if len(DailyPlannerlist)>0:    
                    Dup_fields=['modi_date','taskdescription','status','tasktype']
                    models.Tecdailyplanner.objects.bulk_update(DailyPlannerlist, fields=Dup_fields, batch_size=500)
                    print("Timing tasks - SyncPMSUsers - SynchronousTecDailyPlanner | rows %s", len(DailyPlannerlist))
                if len(Tasklist)>0:    
                    Tup_fields=['modi_date','task','udf04','progress']
                    models.Task.objects.bulk_update(Tasklist, fields=Tup_fields, batch_size=500)
                    print("Timing tasks - SyncPMSUsers - SynchronousTask | rows %s", len(Tasklist))
                transaction.savepoint_commit(save_id, using='MPMS')#?提交事務
            except Exception as e:
                transaction.savepoint_rollback(save_id,using='MPMS')#?事務回滾
                print(str(e))


    def CheckTechnical_AddTask():
        print("-->檢驗技術文檔")
        with transaction.atomic(using='MPMS'):
            save_id = transaction.savepoint(using='MPMS')
            try:
                now = datetime.datetime.now()
                now = now + dateutil.relativedelta.relativedelta(days=-1)
                now = now.strftime('%Y%m%d')
                mb020 = ['S','A','N','T','I']
                TechnicDataList = models.Tecdailyplannersolution.objects.all().extra(
                    select={'startdate':'TecDailyPlanner.StartDate','enddate':'TecDailyPlanner.StartDate','status':'TecDailyPlanner.Status','tec_inc_id':'TecDailyPlanner.INC_ID'},
                    tables=['TecDailyPlanner'],
                    where=["TecDailyPlanner.Contact = TecDailyPlannerSolution.Contact", "TecDailyPlanner.InputDate = TecDailyPlannerSolution.InputDate", 
                    "TecDailyPlanner.ItemNo = TecDailyPlannerSolution.ItemNo", 
                    "TecDailyPlannerSolution.TechnicId<>''","TecDailyPlanner.StartDate=%s"],
                    params=[now]
                )
            
                if TechnicDataList.exists():
                    technicidlist = []
                    techniclist = []
                    for TechnicData in TechnicDataList:
                        technicidlist.append(int(TechnicData.technicid))
                        techniclist.append({'inc_id':int(TechnicData.technicid),'tec_inc_id':TechnicData.tec_inc_id,'contact':TechnicData.contact,'inputdate':TechnicData.inputdate})
                    TecmbData = models.Tecmb.objects.filter(inc_id__in=technicidlist,mb020__in=mb020)    
                    if TecmbData.exists():
                        for tecmb in TecmbData:
                            now_date = datetime.datetime.now()
                            taskdes = '{}'.format(tecmb.mb004)
                            urls = 'http://183.63.205.83:8000/PMIS/opportunity/Technical_Material?param={0}'.format(tecmb.mb023)
                            Contacts = ''
                            remark = ''
                            for techinc in techniclist:
                                if techinc['inc_id']==tecmb.inc_id:
                                    Contacts = '{}({})'.format(Contacts,techinc["contact"])
                                    if remark!='':
                                        remark = remark+';http://183.63.205.83:8000/looper/technic/selectdailyplanner?inc_id='+str(techinc["tec_inc_id"])+'&contact='+techinc["contact"]+'&inputdate='+techinc["inputdate"]    
                                    else:
                                        remark = 'http://183.63.205.83:8000/looper/technic/selectdailyplanner?inc_id='+str(techinc["tec_inc_id"])+'&contact='+techinc["contact"]+'&inputdate='+techinc["inputdate"]                           
                            checkData = models.Task.objects.filter(task__contains=taskdes,create_date=now_date.strftime('%Y%m%d'))
                            taskdes = '{}{}\n{}'.format(taskdes,Contacts,urls)
                            if not checkData.exists() and remark!='':
                                task = models.Task()
                                task.pid = '00500'
                                task.tid = 9
                                task.taskid = TaskService.get_max_taskid(task.pid, task.tid)
                                task.contact = 'sing'
                                task.progress = 'N'
                                task.task = taskdes[0:500]
                                task.hoperation = 'F'
                                task.dayjob = 'Y'
                                task.remark = remark[0:255]
                                task.planbdate = datetime.datetime(now_date.year, now_date.month, now_date.day)
                                task.planedate = datetime.datetime(now_date.year, now_date.month, now_date.day)
                                task.create_date = now_date.strftime('%Y%m%d')
                                save_qty = 0
                                while save_qty < 3:
                                    try:
                                        task.save()
                                        break
                                    except Exception as e:
                                        print(str(e))    
                                        pass
                                    task.taskid = TaskService.get_max_taskid(task.pid, task.tid)
                                    save_qty += 1
                    print("Timing tasks - SyncPMSTechnical - AddTask | rows %s", len(TecmbData))


                transaction.savepoint_commit(save_id, using='MPMS')#?提交事務
            except Exception as e:
                transaction.savepoint_rollback(save_id,using='MPMS')#?事務回滾
                print(str(e))

    #同步會議議題結論和對應任務
    # def sync_PMS_meeting():    
    #     print("-->開始同步PMS任務數據")
    #     sync_PMS_meeting = []
    #     sync_PMS_task = []
    #     #無需同步字段
    #     not_up_fields = ['inc_id','pid','tid','taskid','relationid','schpriority','schedulestate','editionid','creator',
    #                     'company','usr_group','create_date','modifier','flag','docpath','relationgoalid']
    #     up_fields = [field.name for field in models.Task._meta.fields if(field.name not in not_up_fields)]
    #     #獲取議題結論修改日期大於分配任務修改時間的數據
    #     update_Task = models.Task.objects.all().extra(
    #         select={'parent_inc_id':'V_Task_Meeting.inc_id'},
    #         tables=['V_Task_Meeting'],
    #         where=["TRIM(Task.Pid)+'-'+TRIM(STR(Task.Tid))+'-'+TRIM(STR(Task.TaskID)) = TRIM(V_Task_Meeting.relationID)", 
    #         "ISNUMERIC (Task.DocPath) = 1" , "Task.modi_date>V_Task_Meeting.modi_date"],
    #         params=[]
    #     ).values()
    #     #若存在數據，將差異數據同步
    #     # print(update_Task)
    #     for detail in update_Task:
    #         taskdetail = models.Task()
    #         taskdetail.inc_id = detail['parent_inc_id']
    #         for field in up_fields:
    #             setattr(taskdetail, field, detail[field])
    #         sync_PMS_meeting.append(taskdetail)

    #     #獲取操作存在差異的議題結論
    #     update_Meeting = models.VTaskMeeting.objects.all().extra(
    #         select={'parent_inc_id':'Task.inc_id'},
    #         tables=['Task'],
    #         where=["TRIM(Task.Pid)+'-'+TRIM(STR(Task.Tid))+'-'+TRIM(STR(Task.TaskID)) = TRIM(V_Task_Meeting.relationID)", 
    #         "ISNUMERIC (Task.DocPath) = 1" , "Task.modi_date<V_Task_Meeting.modi_date"],
    #         params=[]
    #     ).values()
    #     # print(update_Meeting)
    #     #若存在數據，將差異數據同步
    #     for detail in update_Meeting:
    #         metdetail = models.Task()
    #         metdetail.inc_id = detail['parent_inc_id']
    #         for field in up_fields:
    #             setattr(metdetail, field, detail[field])
    #         sync_PMS_task.append(metdetail)

    #     with transaction.atomic(using='MPMS'):
    #         save_id = transaction.savepoint(using='MPMS')
    #         try:
    #             if len(sync_PMS_meeting)>0:    
    #                 models.Task.objects.bulk_update(sync_PMS_meeting, fields=up_fields, batch_size=500)
    #                 print("Timing tasks - SyncPMSUsers - SynchronousTask | rows %s", len(sync_PMS_meeting))
    #             if len(sync_PMS_task)>0:    
    #                 models.Task.objects.bulk_update(sync_PMS_task, fields=up_fields, batch_size=500)
    #                 print("Timing tasks - SyncPMSUsers - SynchronousTask | rows %s", len(sync_PMS_task))
    #             transaction.savepoint_commit(save_id, using='MPMS')#?提交事務
    #         except Exception as e:
    #             transaction.savepoint_rollback(save_id,using='MPMS')#?事務回滾
    #             print(str(e))
    
    
    def sync_PMS_meeting():   
        def get_default_for_field(field):
            if isinstance(field, model_db.CharField) or isinstance(field, model_db.TextField):
                return ''
            elif isinstance(field, model_db.IntegerField):
                return 0
            elif isinstance(field, model_db.BooleanField):
                return False
            elif isinstance(field, model_db.DateTimeField):
                return timezone.now()
            elif isinstance(field, model_db.FloatField):
                return 0.0
            elif isinstance(field, model_db.DateField):
                return date.today() 
            elif isinstance(field, model_db.DecimalField):
                return 0.0
            else:
                return ''  # 默认返回空字符串，以确保不会为 None
        
        def get_sync_data(up_fields):
            sync_PMS_meeting = []
            sync_PMS_task = []

            # 獲取議題結論修改日期大於分配任務修改時間的數據
            update_Task = models.Task.objects.all().extra(
                select={'parent_inc_id':'V_Task_Meeting.inc_id'},
                tables=['V_Task_Meeting'],
                where=["TRIM(Task.Pid)+'-'+TRIM(STR(Task.Tid))+'-'+TRIM(STR(Task.TaskID)) = TRIM(V_Task_Meeting.relationID)", 
                "ISNUMERIC (Task.DocPath) = 1" , "Task.modi_date>V_Task_Meeting.modi_date"],
                params=[]
            ).values()

            for detail in update_Task:
                taskdetail = models.Task()
                taskdetail.inc_id = detail['parent_inc_id']
                for field in models.Task._meta.fields:
                    name = field.name
                    if name in up_fields:
                        if detail.get(name):
                            setattr(taskdetail, name, detail.get(name))
                        else:
                            setattr(taskdetail, name,get_default_for_field(field))
                sync_PMS_meeting.append(taskdetail)

            # 獲取操作存在差異的議題結論
            update_Meeting = models.VTaskMeeting.objects.all().extra(
                select={'parent_inc_id':'Task.inc_id'},
                tables=['Task'],
                where=["TRIM(Task.Pid)+'-'+TRIM(STR(Task.Tid))+'-'+TRIM(STR(Task.TaskID)) = TRIM(V_Task_Meeting.relationID)", 
                "ISNUMERIC (Task.DocPath) = 1" , "Task.modi_date<V_Task_Meeting.modi_date"],
                params=[]
            ).values()

            for detail in update_Meeting:
                metdetail = models.Task()
                if not detail.get('parent_inc_id'):
                    print(detail)
                metdetail.inc_id = detail['parent_inc_id']
                for field in models.Task._meta.fields:
                    name = field.name
                    if name in up_fields:
                        if detail.get(name):
                            setattr(metdetail, name, detail.get(name))
                        else:
                            setattr(metdetail, name,get_default_for_field(field))
                    
                sync_PMS_task.append(metdetail)

            return sync_PMS_meeting, sync_PMS_task


        def bulk_update_data(sync_PMS_meeting, sync_PMS_task, up_fields):
            with transaction.atomic(using='MPMS'):
                save_id = transaction.savepoint(using='MPMS')
                try:
                    if len(sync_PMS_meeting) > 0:    
                        models.Task.objects.bulk_update(sync_PMS_meeting, fields=up_fields, batch_size=5000)
                        print(f"Timing tasks - SyncPMSUsers - SynchronousTask | rows {len(sync_PMS_meeting)}")
                    if len(sync_PMS_task) > 0:    
                        models.Task.objects.bulk_update(sync_PMS_task, fields=up_fields, batch_size=500)
                        print(f"Timing tasks - SyncPMSUsers - SynchronousTask | rows {len(sync_PMS_task)}")
                    transaction.savepoint_commit(save_id, using='MPMS')
                except Exception as e:
                    transaction.savepoint_rollback(save_id, using='MPMS')
                    print(f"Error occurred during synchronization: {str(e)}")


        print("-->開始同步PMS任務數據")
        
        # 無需同步字段
        not_up_fields = ['inc_id','pid','tid','taskid','relationid', 'schpriority', 'schedulestate', 'editionid', 'creator',
                         'company', 'usr_group', 'create_date', 'modifier', 'flag', 'docpath', 'relationgoalid']
        up_fields = [field.name for field in models.Task._meta.fields if field.name not in not_up_fields]
        # 獲取需要同步的Task數據
        sync_PMS_meeting, sync_PMS_task = get_sync_data(up_fields)

        # 批量更新同步數據
        bulk_update_data(sync_PMS_meeting, sync_PMS_task, up_fields)


    #同步Forum帖子任務
    def sync_PMS_forum():    
        print("-->開始Forum帖子PMS任務數據")
        sync_PMS_task = []
        #無需同步字段
        up_fields = ['progress']
        now = datetime.datetime.now()
        now = now + dateutil.relativedelta.relativedelta(months=-6)
        create_date = now.strftime('%Y%m')+'01'
        #獲取議題結論修改日期大於分配任務修改時間的數據
        update_forum = models.Tecfa.objects.filter(create_date__gte=create_date,fa008='Y').extra(
            select={'Tinc_id':'Task.inc_id'},
            tables=['Task'],
            where=["(right(Task,len(Task)- CHARINDEX('topicsNo=',Task)-8)=trim(str(FA001)) OR Task=FA003) AND Pid='00500' AND Tid=95"],
            params=[]
        ).values()
        #若存在數據，將差異數據同步
        for detail in update_forum:
            taskdetail = models.Task()
            taskdetail.inc_id = detail['Tinc_id']
            taskdetail.progress = 'C'
            sync_PMS_task.append(taskdetail)

        # print(sync_PMS_task)
        with transaction.atomic(using='MPMS'):
            save_id = transaction.savepoint(using='MPMS')
            try:
                if len(sync_PMS_task)>0:    
                    models.Task.objects.bulk_update(sync_PMS_task, fields=up_fields, batch_size=500)
                    print("Timing tasks - SyncPMSUsers - SynchronousTask | rows %s", len(sync_PMS_task))
                transaction.savepoint_commit(save_id, using='MPMS')#?提交事務
            except Exception as e:
                transaction.savepoint_rollback(save_id,using='MPMS')#?事務回滾
                print(str(e))

    #定時刷新任務的SubProjectID
    def refreshSubProjectId():
        try:
            with connections[ModelTools.get_database(models.Task)].cursor() as cursor:
                strsql = "UPDATE dbo.V_Task_RecordId SET SubProjectID = RecordId WHERE ISNULL(RecordId,'') <> ISNULL(SubProjectID,'')"
                cursor.execute(strsql)
        except Exception as e:
            LOGGER.error(e)
            print(str(e))

    
    # 定時執行：每半小時執行一次
    @register_job(scheduler, 'interval',id='run_refresh_task_recordid', minutes=32, replace_existing=True)
    def run_refresh_task_recordid():
        try:
            print("{0}-->============開始執行刷新任務recordid=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
            refreshSubProjectId()
            print("{0}-->============結束執行刷新任務recordid=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        except Exception as e:
            print(str(e))

    # 定時執行：每半小時執行一次
    @register_job(scheduler, 'interval',id='sync_PMS_meeting', minutes=31, replace_existing=True)
    def run_sync_PMS_meeting():
        try:
            sync_PMS_meeting()
        except Exception as e:
            print(str(e))

        
    # 定時執行：每半小時執行一次
    @register_job(scheduler, 'interval',id='sync_PMS_forum', minutes=31, replace_existing=True)
    def run_sync_PMS_forum():
        try:
            sync_PMS_forum()
        except Exception as e:
            print(str(e))
            
    
    @register_job(scheduler, 'cron',id='CheckTechnical_AddTask',hour=6,minute=30, replace_existing=True)
    def run_CheckTechnical_AddTask():
        try:
            CheckTechnical_AddTask()
        except Exception as e:
            print(str(e))


    @register_job(scheduler, 'cron',id='sync_PMS_task',hour='0/1', minute=5, replace_existing=True)
    def run_sync_PMS_task():
        try:
            sync_PMS_task()
        except Exception as e:
            print(str(e))

    @register_job(scheduler, 'cron',id='get_notification_tasks', hour=7,  replace_existing=True)
    #@register_job(scheduler, 'cron',id='get_notification_tasks', hour=15, minute=40,  replace_existing=True)
    def get_notification_tasks():
        try:
            print("{0}-->============開始收集需要發送消息的任務=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
            qs = models.Syspara.objects.values("nfield").filter(ftype="NotificationId")
            if len(qs) > 0:
                users = [item['nfield'] for item in qs]
                service = NotificationService()
                service.send_todayt_tasks(",".join(users))
                #service.send_first_last_class1("sing", "sing")
            print("{0}-->============開始收集需要發送消息的任務=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        except Exception as e:
            print(str(e))
        

    @register_job(scheduler, 'cron',id='send_notification_sing_today_followup', hour=8,  replace_existing=True)
    def send_notification_sing_today_followup():
        try:
            print("{0}-->============開始發送陳生每天應該跟進的人的工程的消息=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
            service = NotificationService()
            service.send_sing_today_flowup_contact("sing,hb,lmy")
            print("{0}-->============結束發送陳生每天應該跟進的人的工程的消息=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        except Exception as e:
            print(str(e))



    # 定時執行：每20分鐘執行一次
    @register_job(scheduler, 'cron',id='send_notification',hour="8-17", minute="0/20", replace_existing=True)
    def send_notification():
        try:
            print("{0}-->============開始發送消息=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
            service = NotificationService()
            service.schedule_send_message()
            print("{0}-->============結束發送消息=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        except Exception as e:
            print(str(e))
    
    # 定時執行：每天8:30執行一次
    @register_job(scheduler, 'cron',id='auto_send_schedule_highest_task', hour=8, minute=5,  replace_existing=True)
    def run_autoSendScheduleHighestTask():
        try:
            print("{0}-->============開始Auto Send Schedule Highest Task=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
            server = NtfyNotificationService()
            users = UserService.GetPartUserNames()
            todayTaskDatas = server.get_today_task_data(users)
            highest_tasks = todayTaskDatas['highest_tasks']
            for contact,task in highest_tasks.items():
                task[NOTIFICATION_DELAY_RESEND_TASK] = True
            server.send_schedule_higest_task(users, highest_tasks)
            print("{0}-->============結束Auto Send Schedule Highest Task=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        except Exception as e:
            print(str(e))


    #定時執行:每天8:10分執行一次
    @register_job(scheduler, 'cron',id='auto_send_outstanding_goal', hour=8, minute=10,  replace_existing=True)
    def run_autoSendOutstandingGoal():
        try:
            print("{0}-->============開始Auto Send Outstanding Goal=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
            server = NtfyNotificationService()
            users = UserService.GetPartUserNames()
            todayTaskDatas = server.get_today_task_data(users)
            outstanding_goals = todayTaskDatas['outstanding_goals']
            for contact,tasks in outstanding_goals.items():
                for task in tasks:
                    task[NOTIFICATION_DELAY_RESEND_TASK] = True
            server.send_outstanding_goals(outstanding_goals)
            print("{0}-->============結束Auto Send Outstanding Goal=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        except Exception as e:
            print(str(e))

    #定時執行:每天8:15分執行一次
    @register_job(scheduler, 'cron',id='auto_send_fixed_day_task', hour=8, minute=15,  replace_existing=True)
    def run_autoSendCycleFixedDayTask():
        try:
            print("{0}-->============開始Auto Send Cycle Fixed Task=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
            server = NtfyNotificationService()
            users = UserService.GetPartUserNames()
            todayTaskDatas = server.get_today_task_data(users)
            user_fixed_day_tasks = todayTaskDatas['user_fixed_day_tasks']
            for contact,tasks in user_fixed_day_tasks.items():
                for task in tasks:
                    task[NOTIFICATION_DELAY_RESEND_TASK] = True
            server.send_cycle_fixed_tasks(user_fixed_day_tasks)
            print("{0}-->============結束Auto Send Cycle Fixed Task=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        except Exception as e:
            print(str(e))
    
    
    @register_job(scheduler, 'interval',id='auto_send_task_remind', minutes=1, replace_existing=True)
    def run_sendTaskRemind():
        try:
            print("{0}-->============開始Send Task Remind=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
            server = NtfyNotificationService()
            server.sendAllTaskRemind()
            print("{0}-->============結束Send Task Remind=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        except Exception as e:
            print(str(e))  


    @register_job(scheduler, 'cron',id='auto_send_project_status1', hour=8, minute=20,  replace_existing=True)
    def run_sendProjectStatus1():
        try:
            print("{0}-->============開始auto_send_project_status=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
            server = NtfyNotificationService()
            server.send_project_status() 
            server.send_summary_project_status()
            server.send_milestone()
            server.send_meeting_aisummary()
            server.send_help_desk_aisummary()
            print("{0}-->============結束auto_send_project_status=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        except Exception as e:
            print(str(e))

    @register_job(scheduler, 'cron',id='auto_send_project_status2', hour=13, minute=0,  replace_existing=True)
    def run_sendProjectStatus2():
        try:
            print("{0}-->============開始auto_send_project_status=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
            server = NtfyNotificationService()
            server.send_project_status() 
            server.send_summary_project_status()
            server.send_meeting_aisummary()
            server.send_help_desk_aisummary()
            print("{0}-->============結束auto_send_project_status=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        except Exception as e:
            print(str(e))
            
    @register_job(scheduler, 'cron',id='auto_send_project_status3', hour=17, minute=30,  replace_existing=True)
    def run_sendProjectStatus3():
        try:
            print("{0}-->============開始auto_send_project_status=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
            server = NtfyNotificationService()
            server.send_project_status() 
            server.send_summary_project_status()
            server.send_meeting_aisummary()
            server.send_help_desk_aisummary()
            print("{0}-->============結束auto_send_project_status=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        except Exception as e:
            print(str(e))
    
    @register_job(scheduler, 'cron',id='auto_send_message_summary1', hour="8-16/2", replace_existing=True)
    def run_sendMessageSummarys():
        try:
            print("{0}-->============開始auto_send_message_summary=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
            server = NtfyNotificationService()
            server.send_message_summary()
            print("{0}-->============結束auto_send_message_summary=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        except Exception as e:
            print(str(e))
    
    @register_job(scheduler, 'cron',id='auto_send_message_summary2', hour=17, minute=30, replace_existing=True)
    def run_sendMessageSummary2():
        try:
            print("{0}-->============開始auto_send_message_summary=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
            server = NtfyNotificationService()
            server.send_message_summary()
            print("{0}-->============結束auto_send_message_summary=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        except Exception as e:
            print(str(e))
    

    @register_job(scheduler, 'interval',id='auto_schedule', minutes=30, replace_existing=True)
    def auto_schedule():
        try:
            print("{0}-->============開始auto_schedule自動排期=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
            schType = "1"
            exportExcel = False
            returnResults = False
            
            server = ScheduleServer()
            loginUserName = ""
            users = UserService.GetPartUserNames()            
            for user in users:
                contact = user #表示對聯繫人的任務進行排期
                response = server.callScenarioScheduleService(schType,contact,loginUserName, exportExcel, returnResults)            
                sleep(0.2)
            print("{0}-->============結束auto_schedule自動排期=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        except Exception as e:
            print(str(e))

    # 檢查是否為主進程
    if os.getenv("UWSGI_ORIGINAL_PROC_NAME") == "uwsgi" and settings.DEBUG == False:
        try:
            register_events(scheduler)
            scheduler.start()
            print("Start Apschedule!!!!!!!!!")
        except Exception as e:
            print(str(e))
            if scheduler.running:
                scheduler.shutdown()    
    
except:
    print("Start Apschedule Fail !!!!!!!!!")
def unlock():
    fcntl.flock(f, fcntl.LOCK_UN)   
    f.close()
atexit.register(unlock)     # 释放锁





