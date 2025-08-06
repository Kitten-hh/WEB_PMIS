import atexit
import fcntl
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import apps
from django.forms import ModelForm
from django_apscheduler.jobstores import DjangoJobStore,register_events,register_job
from django.db.models import Count,Q,Case,Sum,When,IntegerField,Max
from django.db import transaction
from django.core.cache import cache
from PMIS.Services.TaskService import TaskService
from PMISLooper.Services.NotificationService import NotificationService
from DataBase_MPMS import models
import dateutil.relativedelta
import datetime
import re
from django.http import JsonResponse,HttpResponse,HttpRequest

LOGGER = logging.getLogger(__name__)
f = open("scheduler.lock", "wb")
try:
    fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)   # 加锁
    scheduler = BackgroundScheduler() # 建一個調度器對象
    scheduler.add_jobstore(DjangoJobStore(), "default") # 添加一個作業

    # 定時執行：每小時執行一次
    @register_job(scheduler, 'cron',id='sync_PMS_task',hour='0/1', replace_existing=True)
    def sync_PMS_task():
        LOGGER.info("-->開始同步PMS任務數據")
        with transaction.atomic(using='MPMS'):
            save_id = transaction.savepoint(using='MPMS')
            try:
                now = datetime.datetime.now()
                monthago = now + dateutil.relativedelta.relativedelta(months=-1)#一個月前
                monthago.strftime('%Y-%m')
                #同步最近一個月的TecDailyPlanner表
                update_TecDailyPlanner = models.Tecdailyplanner.objects.all().extra(
                    select={'modi_date_task':'Task.modi_date'},
                    tables=['Task'],
                    where=["TRIM(Pid)+'-'+TRIM(STR(Tid))+'-'+TRIM(STR(TaskID)) = TRIM(TaskNo)", 
                    "TecDailyPlanner.modi_date<Task.modi_date" , "inputdate>%s"],
                    params=[monthago.strftime('%Y%m')]
                )
                if update_TecDailyPlanner.exists():
                    for TecDailyPlanner in update_TecDailyPlanner:
                        taskno = re.findall(r"\d+\.?\d*",TecDailyPlanner.taskno)
                        TaskData = models.Task.objects.filter(pid=taskno[0],tid=taskno[1],taskid=taskno[2])
                        if TaskData.exists():
                            for theTask in TaskData:
                                
                                tasktype = theTask.tasktype
                                subtasktype = theTask.subtasktype
                                diff = 'difficulties1'
                                if theTask.diff != None:
                                    diff = 'difficulties'+str(theTask.diff)
                                if tasktype != None and subtasktype != None and diff != None and tasktype != '' and subtasktype != '' and diff != '' :            
                                    theType = list(models.Tasktypelist.objects.filter(tasktype=tasktype).values('description'))
                                    thesubType = list(models.Tasktypelist.objects.filter(tasktype=subtasktype).values('description'))
                                    score = list(models.Tasktypelist.objects.filter(tasktype=subtasktype,parenttype=tasktype).values(diff))
                                    if len(theType)>0:
                                        theTask.tasktype = theType[0]['description']
                                    if len(thesubType)>0:
                                        theTask.subtasktype = thesubType[0]['description']
                                    if len(score)>0:
                                        theTask.diff = score[0][diff]
                                update_TecDailyPlanner.update(modi_date=theTask.modi_date,taskdescription=theTask.task,
                                framespecification=theTask.udf04,status=theTask.progress,tasktype=theTask.tasktype + '-->' + str(theTask.subtasktype))
                                #print(theTask.modi_date)
                    LOGGER.info("Timing tasks - SyncPMSUsers - SynchronousTecDailyPlanner | rows %s", len(update_TecDailyPlanner))

                #同步最近一個月的Task表
                update_Task = models.Task.objects.all().extra(
                    select={'modi_date_TecDailyPlanner':'TecDailyPlanner.modi_date'},
                    tables=['TecDailyPlanner'],
                    where=["TRIM(Pid)+'-'+TRIM(STR(Tid))+'-'+TRIM(STR(TaskID)) = TRIM(TaskNo)", 
                    "TecDailyPlanner.modi_date>Task.modi_date" , "inputdate>%s"],
                    params=[monthago.strftime('%Y%m')]
                )
                if update_Task.exists():
                    for task in update_Task:
                        TecdailyplannerData = models.Tecdailyplanner.objects.filter(taskno=task.pid+'-'+str(int(task.tid))+'-'+str(int(task.taskid)))
                        if TecdailyplannerData.exists():
                            for TecdailyData in TecdailyplannerData:
                                update_Task.update(modi_date=TecdailyData.modi_date,task=TecdailyData.taskdescription,udf04=TecdailyData.framespecification,progress=TecdailyData.status)
                                #print(TecdailyData.modi_date)
                    LOGGER.info("Timing tasks - SyncPMSUsers - SynchronousTask | rows %s", len(update_Task))
                transaction.savepoint_commit(save_id, using='MPMS')#?提交事務
            except Exception as e:
                transaction.savepoint_rollback(save_id,using='MPMS')#?事務回滾
                LOGGER.error(e)


    # 定時執行：每天6點半執行
    @register_job(scheduler, 'cron',id='CheckTechnical_AddTask',hour=6,minute=30, replace_existing=True)
    def CheckTechnical_AddTask():
        LOGGER.info("-->檢驗技術文檔")
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
                            taskdes = '未Confirmed技術文檔：http://183.63.205.83:8000/PMIS/opportunity/Technical_Material?param='+tecmb.mb023
                            remark = ''
                            for techinc in techniclist:
                                if techinc['inc_id']==tecmb.inc_id:
                                    if remark!='':
                                        remark = remark+'\nhttp://183.63.205.83:8000/looper/technic/selectdailyplanner?inc_id='+str(techinc["inc_id"])+'&contact='+techinc["contact"]+'&inputdate='+techinc["inputdate"]    
                                    else:
                                        remark = 'http://183.63.205.83:8000/looper/technic/selectdailyplanner?inc_id='+str(techinc["inc_id"])+'&contact='+techinc["contact"]+'&inputdate='+techinc["inputdate"]                           
                            checkData = models.Task.objects.filter(task__contains=taskdes,create_date=now_date.strftime('%Y%m%d'))
                            if not checkData.exists():
                                task = models.Task()
                                task.pid = '00500'
                                task.tid = 9
                                task.taskid = TaskService.get_max_taskid(task.pid, task.tid)
                                task.contact = 'sing'
                                task.progress = 'N'
                                task.task = taskdes
                                task.hoperation = 'F'
                                task.dayjob = 'Y'
                                task.remark = remark
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
                    LOGGER.info("Timing tasks - SyncPMSTechnical - AddTask | rows %s", len(TecmbData))


                transaction.savepoint_commit(save_id, using='MPMS')#?提交事務
            except Exception as e:
                transaction.savepoint_rollback(save_id,using='MPMS')#?事務回滾
                LOGGER.error(e)


    # 定時執行：每半小時執行一次
    @register_job(scheduler, 'interval',id='sync_PMS_meeting', minutes=30, replace_existing=True)
    def sync_PMS_meeting():
        LOGGER.info("-->開始同步PMS任務數據")
        sync_PMS_meeting = []
        sync_PMS_task = []
        #無需同步字段
        not_up_fields = ['inc_id','pid','tid','taskid','relationid','schpriority','schedulestate','editionid','creator',
                        'company','usr_group','create_date','modifier','flag']
        up_fields = [field.name for field in models.Task._meta.fields if(field.name not in not_up_fields)]
        #獲取議題結論修改日期大於分配任務修改時間的數據
        update_Task = models.Task.objects.all().extra(
            select={'parent_inc_id':'V_Task_Meeting.inc_id'},
            tables=['V_Task_Meeting'],
            where=["TRIM(Task.Pid)+'-'+TRIM(STR(Task.Tid))+'-'+TRIM(STR(Task.TaskID)) = TRIM(V_Task_Meeting.relationID)", 
            "ISNUMERIC (Task.DocPath) = 1" , "Task.modi_date>V_Task_Meeting.modi_date"],
            params=[]
        ).values()
        #若存在數據，將差異數據同步
        print(update_Task)
        if update_Task.exists():
            for detail in update_Task:
                taskdetail = models.Task()
                taskdetail.inc_id = detail['parent_inc_id']
                for field in up_fields:
                    setattr(taskdetail, field, detail[field])
                sync_PMS_meeting.append(taskdetail)

        #獲取操作存在差異的議題結論
        update_Meeting = models.VTaskMeeting.objects.all().extra(
            select={'parent_inc_id':'Task.inc_id'},
            tables=['Task'],
            where=["TRIM(Task.Pid)+'-'+TRIM(STR(Task.Tid))+'-'+TRIM(STR(Task.TaskID)) = TRIM(V_Task_Meeting.relationID)", 
            "ISNUMERIC (Task.DocPath) = 1" , "Task.modi_date<V_Task_Meeting.modi_date"],
            params=[]
        ).values()
        print(update_Meeting)
        #若存在數據，將差異數據同步
        if update_Meeting.exists():
            for detail in update_Meeting:
                taskdetail = models.Task()
                taskdetail.inc_id = detail['parent_inc_id']
                for field in up_fields:
                    setattr(taskdetail, field, detail[field])
                sync_PMS_meeting.append(taskdetail)

        with transaction.atomic(using='MPMS'):
            save_id = transaction.savepoint(using='MPMS')
            try:
                if len(sync_PMS_meeting)>0:    
                    models.Task.objects.bulk_update(sync_PMS_meeting, fields=up_fields, batch_size=500)
                    LOGGER.info("Timing tasks - SyncPMSUsers - SynchronousTask | rows %s", len(sync_PMS_meeting))
                if len(sync_PMS_task)>0:    
                    models.Task.objects.bulk_update(sync_PMS_task, fields=up_fields, batch_size=500)
                    LOGGER.info("Timing tasks - SyncPMSUsers - SynchronousTask | rows %s", len(sync_PMS_task))
                transaction.savepoint_commit(save_id, using='MPMS')#?提交事務
            except Exception as e:
                transaction.savepoint_rollback(save_id,using='MPMS')#?事務回滾
                LOGGER.error(e)


    # 定時執行：每1小時執行一次
    #@register_job(scheduler, 'cron',id='send_todayt_tasks',hour='8-17/1', replace_existing=True)
    #@register_job(scheduler, 'cron',id='send_todayt_tasks',hour="8-17/1", replace_existing=True)
    @register_job(scheduler, 'cron',id='send_todayt_tasks',minute="0/30", replace_existing=True)
    def send_todayt_tasks():
        print("{0}-->============開始發送Today Task=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        qs = models.Syspara.objects.values("nfield").filter(ftype="NotificationId")
        if len(qs) > 0:
            users = [item['nfield'] for item in qs]
            service = NotificationService()
            service.send_todayt_tasks(",".join(users))
        print("{0}-->============結束發送Today Task=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
    try:
        register_events(scheduler)
        scheduler.start()
        LOGGER.info("Start Apschedule!!!!!!!!!")
    except Exception as e:
        LOGGER.error(e)
        if scheduler.running:
            scheduler.shutdown()
except:
    LOGGER.info("Start Apschedule Fail !!!!!!!!!")
def unlock():
    fcntl.flock(f, fcntl.LOCK_UN)   
    f.close()
atexit.register(unlock)     # 释放锁


            
    