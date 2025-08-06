from DataBase_MPMS import models
from . BaseService import BaseService
from django.db.models import Count,Q,Case,Sum,When,IntegerField,Max
from django.db.models import F, ExpressionWrapper, fields
import json
import random
import math
import datetime
import timeago
from BaseProject.tools import DateTools
import re
from django.db import connections
from BaseApp.library.tools import DateTools
from . import QueryFilterService
from django.utils import timezone
from django.forms.models import model_to_dict
from PMIS.Services.TaskService import TaskService
from ScheduleApp.Services import ScheduleConstant as Constant
import pytz
from ScheduleApp.Services.ScheduleServer import ScheduleServer
from ..Services.SessionService import SessionService


class ActiveTaskService(BaseService):
    top_twenty_task_filter =  "(((TidStr LIKE '%%0[0-9][0-9]') OR (Tid BETWEEN 0 AND 99)) OR ((Pid = '00500') AND \
            (Tid BETWEEN 100 AND 199)) OR ((Pid = '888') AND (Tid = 100)) OR ((TaskIDStr LIKE '%%5[0-9][0-9]')))"
    @staticmethod
    def get_today_tasks(username):
        '''
        功能描述：獲取用戶Today's Task-->Schedule Priority
        '''
        today_tasks = []
        queryfilters = QueryFilterService.get_daily_goal_filter(username, order_num=20)
        qf025 = queryfilters[0].qf025
        if len(queryfilters) > 1:
            for qf in queryfilters:
                if re.search('^'+username, qf.qt002, re.IGNORECASE):
                    qf025 = qf.qf025
        str_filter = QueryFilterService.get_query_filter(qf025)
        queryset = models.VTask.objects.raw('select top 20 * from V_Task where ' + str_filter + " order by SchPriority desc")        
        none_time = datetime.datetime.strptime(str(datetime.datetime.now().date())+'00:00', '%Y-%m-%d%H:%M')
        cur_date_str = DateTools.format(datetime.datetime.now())
        for task in queryset:
            planbdate = task.planbdate
            planedate = task.planedate
            if planbdate and planedate and \
                planbdate.time() != none_time.time() and planedate.time() != none_time.time() and \
                planbdate.time() != planedate.time():
                task.planbdate = DateTools.parsef(cur_date_str + DateTools.formatf(task.planbdate, '%H:%M'), '%Y%m%d%H:%M');
                task.planedate = DateTools.parsef(cur_date_str + DateTools.formatf(task.planedate, '%H:%M',), '%Y%m%d%H:%M');
                today_tasks.append(task)

        ##查詢當天之前未完成的Fixed Date任務
        queryset_fixed = models.VTask.objects.filter(contact=username, hoperation='F', planbdate__date__lte=timezone.now()).\
            filter(~Q(progress__in=['C','F'])).order_by('-planbdate')[:10]
        taskno_array = [task.taskno for task in today_tasks]
        today_tasks.extend([task for task in list(queryset_fixed) if not task.taskno in taskno_array])
        return today_tasks
    
    @staticmethod
    def get_today_tasks2(username):
        today_tasks = []
        service = ActiveTaskService()
        cycle_tasks = service.get_today_cycle_fixed(username)
        user_fixed_tasks = service.get_today_fixed_tasks(username)
        today_normal_task = service.get_today_normal_task(username)
        service.merge_task_arry(cycle_tasks, today_tasks)
        service.merge_task_arry(user_fixed_tasks, today_tasks)
        service.merge_task_arry(today_normal_task, today_tasks)
        return today_tasks

                
    def merge_task_arry(self,source, dest):
        taskno_array = [task.taskno for task in dest]
        dest.extend([task for task in list(source) if not task.taskno in taskno_array])
    def meger_task_dict(self, source, dest):
        taskno_array = [task['taskno'] for task in dest if 'taskno' in task]
        dest.extend([task for task in list(source) if not task['taskno'] in taskno_array])

    def get_today_fixed_tasks(self,username):
        '''
        功能描述：獲取用戶today's fixed day task     
        '''
        fields = fields = list([a.attname for a in models.VTask._meta.get_fields() if a.attname not in ['emaildesp']])
        queryset_fixed = models.VTask.objects.values(*fields).filter(contact=username, hoperation='F',schedulestate='Y', planbdate__date__lte=timezone.now()).\
        filter(~Q(progress__in=['C','F'])).filter(~Q(cycletask='Y'))
        finish_fixed = models.VTask.objects.values(*fields).filter(contact=username, hoperation='F',schedulestate='Y', edate__date=timezone.now(), progress__in=['C','F']).filter(~Q(cycletask='Y'))
        qs = queryset_fixed.union(finish_fixed)
        return list(qs)


    def get_today_cycle_fixed(self,username):
        '''
        功能描述：查詢用戶當天的循環任務
        '''

        queryset = models.VTask.objects.filter(planbdate__date__lte=timezone.now(), planedate__date__gte=timezone.now(),
                contact=username, cycletask='Y', hoperation='F')
        return list(queryset)
    
    def get_today_scheduled_task_bak(self, username):
        """
        功能描述：獲取用戶當天的排期的任務
        """
        server = ScheduleServer()
        strFilter = server.getScheduleTaskQuery(username)
        categoryFilterMap = server.getScheduleCategoryFilterMap(username)
        upcommingTaskDay = 3
        qs = models.Syspara.objects.values('fvalue').filter(nfield='UpcommingTaskDay', ftype='ScheduleDisplay')
        if len(qs) > 0:
            upcommingTaskDay = int(qs[0]['fvalue'])
        endDate = DateTools.addDay(DateTools.now(), upcommingTaskDay)
        selectStrArr = ["When ({0}) then '{1}'".format(strFilter, category) for category, strFilter in categoryFilterMap.items()]
        selectStr = "(case " + " ".join(selectStrArr) + " else '' end )"
        selectSeqNoStrArr = ["When ({0}) then {1}".format(strFilter, index) for index,(category, strFilter) in enumerate(categoryFilterMap.items())]
        selectSeqNoStr = "(case " + " ".join(selectSeqNoStrArr) + " else " + str(len(categoryFilterMap.keys()) + 1) + " end )"
        fields = [field.name for field in models.VTask._meta.fields] + ['schcategory','schcategory_seqno']
        qs = models.VTask.objects.filter(contact=username).filter(Q(schedulestate='Y') | (~Q(schedulestate='Y') & Q(hoperation='F')))\
            .filter(Q(progress__in=['C','F'],edate__date=DateTools.now()) | (Q(planedate__date__lte=endDate) & ~Q(progress__in=['C','F'])))\
            .extra(select={"schcategory":selectStr,'schcategory_seqno':selectSeqNoStr}, where=[strFilter])\
            .values(*fields)
            ##.order_by('-schpriority')
        qs = server.getScheduleTaskRangeFilter(qs)
        tasks = list(qs)
        today_fixed_tasks = []
        today_scheduled_tasks = []
        today_upcomming_fixed_tasks = []
        today_upcomming_schedule_tasks = []
        outstanding_fixed_tasks = []
        outstanding_schedule_tasks  = []
        for task in tasks:
            if not task['planbdate'] or not task['planedate']:
                continue
            if task['hoperation'] == "F":
                del task['schcategory']
                del task['schcategory_seqno']                            
            if DateTools.format(task['planbdate']) > DateTools.format(DateTools.now()): ##upcomming
                if task['hoperation'] == "F":
                    today_upcomming_fixed_tasks.append(task)
                else:
                    today_upcomming_schedule_tasks.append(task)
            elif DateTools.format(task['planedate']) < DateTools.format(timezone.now()): ##outstanding
                if task['hoperation'] == "F":
                    outstanding_fixed_tasks.append(task)
                else:
                    outstanding_schedule_tasks.append(task)
            elif task['hoperation'] == "F":
                today_fixed_tasks.append(task)
            else:
                today_scheduled_tasks.append(task)
        return today_fixed_tasks, today_scheduled_tasks, today_upcomming_fixed_tasks,today_upcomming_schedule_tasks,outstanding_fixed_tasks,outstanding_schedule_tasks

    #def get_today_scheduled_task_with_schpriority(self, username):
    def get_today_scheduled_task(self, username):
        """
        功能描述：獲取用戶當天的排期的任務，根據排期優先級來
        """
        queryfilters = QueryFilterService.get_daily_goal_filter("top+twenty", order_num=20, owner='xxx')
        defaultTopTwentyFilter = None
        topTwentyFilter = None
        if len(queryfilters) > 0:
            qf = queryfilters[0]
            topTwentyFilter = QueryFilterService.get_query_filter(qf.qf025)                    
            topTwentyFilter = topTwentyFilter.replace("xxx", username);
            
        qs = models.Syspara.objects.values('fvalue').filter(nfield='Top Twenty Query', ftype="TaskEnquiryTop")[:1]
        if len(qs) > 0:
            defaultTopTwentyFilter = qs[0]['fvalue']
            defaultTopTwentyFilter = defaultTopTwentyFilter.replace("%","%%")
        if not topTwentyFilter:
            topTwentyFilter = "1<>1"
        topNum = 20
        qs = models.Syspara.objects.values('fvalue').filter(nfield='Top Twenty', ftype="TaskEnquiryTop")[:1]
        if len(qs) > 0:
            topNum = int(qs[0]['fvalue'])
        server = ScheduleServer()
        categoryFilterMap = server.getScheduleCategoryFilterMap(username)
        del categoryFilterMap[Constant.SCHEDULE_SESSION]
        upcommingTaskDay = 3
        qs = models.Syspara.objects.values('fvalue').filter(nfield='UpcommingTaskDay', ftype='ScheduleDisplay')
        if len(qs) > 0:
            upcommingTaskDay = int(qs[0]['fvalue'])
        endDate = DateTools.addDay(DateTools.now(), upcommingTaskDay)
        selectStrArr = ["When ({0}) then '{1}'".format(strFilter, category) for category, strFilter in categoryFilterMap.items()]
        selectStr = "(case {0} else '{1}' end)".format(" ".join(selectStrArr), Constant.SCHEDULE_SESSION)
        selectSeqNoStrArr = ["When ({0}) then {1}".format(strFilter, index+1) for index,(category, strFilter) in enumerate(categoryFilterMap.items())]
        selectSeqNoStr = "(case " + " ".join(selectSeqNoStrArr) + " else 1 end )"
        fields = [field.name for field in models.VTask._meta.fields if field.name not in ['emaildesp']] + ['schcategory','schcategory_seqno']
        ##查詢Top Twenty的任務
        topTwentyQuerySet = models.VTask.objects.filter(contact=username).extra(select={"schcategory":selectStr,'schcategory_seqno':selectSeqNoStr}, where=[topTwentyFilter])\
            .values(*fields).order_by("-schpriority")[:topNum]
        ##查詢Fixed Day的任務
        fixedDayQuerySet = models.VTask.objects.filter(contact=username).filter(hoperation='F')\
            .filter(Q(progress__in=['C','F'],edate__date=DateTools.now()) | (Q(planedate__date__lte=endDate) & ~Q(progress__in=['C','F'])))\
            .extra(select={"schcategory":selectStr,'schcategory_seqno':selectSeqNoStr}, where=[defaultTopTwentyFilter])\
            .values(*fields)
            ##.order_by('-schpriority')
        tasks = list(topTwentyQuerySet)  #因為top twenty有limit不能使用union合併結果集，需要手動合併
        fixedDayTasks = list(fixedDayQuerySet)
        existsTaskNos = [item['taskno'] for item in tasks]
        tasks.extend([item for item in fixedDayTasks if item['taskno'] not in existsTaskNos])
        today_fixed_tasks = []
        today_scheduled_tasks = []
        today_upcomming_fixed_tasks = []
        today_upcomming_schedule_tasks = []
        outstanding_fixed_tasks = []
        outstanding_schedule_tasks  = []
        for task in tasks:
            if not task['planbdate'] or not task['planedate']:
                continue
            if task['hoperation'] == "F":
                del task['schcategory']
                del task['schcategory_seqno']                            
            if DateTools.format(task['planbdate']) > DateTools.format(DateTools.now()): ##upcomming
                if task['hoperation'] == "F":
                    today_upcomming_fixed_tasks.append(task)
                else:
                    today_upcomming_schedule_tasks.append(task)
            elif DateTools.format(task['planedate']) < DateTools.format(timezone.now()): ##outstanding
                if task['hoperation'] == "F":
                    outstanding_fixed_tasks.append(task)
                else:
                    outstanding_schedule_tasks.append(task)
            elif task['hoperation'] == "F":
                today_fixed_tasks.append(task)
            else:
                today_scheduled_tasks.append(task)
        return today_fixed_tasks, today_scheduled_tasks, today_upcomming_fixed_tasks,today_upcomming_schedule_tasks,outstanding_fixed_tasks,outstanding_schedule_tasks

    def get_today_intray_task(self, username):
        queryset = models.VTask.objects.filter(contact=username, progress="R")
        queryset = TaskService.getRequestQuerySetWithSysparam(queryset)
        return list(queryset)

    def get_today_cycle_task(self, username):
        queryset = models.VTask.objects.filter(planbdate__date__lte=timezone.now(), planedate__date__gte=timezone.now(), \
        contact=username, cycletask='Y').extra(tables=['TpDetail'], \
                where=["V_Task.MastNo =  Convert(varchar(20),Cast(TpDetail.TpMastId as int)) + '-' + Convert(varchar(20), Cast(TpDetail.TpDetailId as int)) and \
                (TpDetail.CycleDayOfMonth = '*' and TpDetail.CycleMonths = '*' and (TpDetail.CycleDayOfWeek = '*' or rtrim(TpDetail.CycleDayOfWeek) = '1-6' or rtrim(TpDetail.CycleDayOfWeek) = '1-7' or TpDetail.CycleDayOfWeek = '1,2,3,4,5,6' or TpDetail.CycleDayOfWeek = '1,2,3,4,5,6,7'))"])
        return list(queryset)         

    def get_today_daily_pallner(self, username):
        today_tasks = []
        queryfilters = QueryFilterService.get_daily_goal_filter(username, order_num=20)
        qf025 = queryfilters[0].qf025
        if len(queryfilters) > 1:
            for qf in queryfilters:
                if re.search('^'+username, qf.qt002, re.IGNORECASE):
                    qf025 = qf.qf025
        str_filter = QueryFilterService.get_query_filter(qf025)
        queryset = models.VTask.objects.raw('select top 20 * from V_Task where ' + str_filter + " order by SchPriority desc")        
        none_time = datetime.datetime.strptime(str(datetime.datetime.now().date())+'00:00', '%Y-%m-%d%H:%M')
        cur_date_str = DateTools.format(datetime.datetime.now())
        for task in queryset:
            planbdate = task.planbdate
            planedate = task.planedate
            if planbdate and planedate and \
                planbdate.time() != none_time.time() and planedate.time() != none_time.time() and \
                planbdate.time() != planedate.time() and (timezone.now() - planbdate).days >= 0:
                today_tasks.append(task)        
        return today_tasks

    @staticmethod
    def get_schedule_task(username):
        '''
        功能描述：獲取用戶Today's Task-->Schedule Priority
        '''
        sch_tasks = []
        queryset = models.VTask.objects.filter(contact=username, schpriority__gt=0).\
            filter(~Q(progress__in=['C','F'])).extra(where=[ActiveTaskService.top_twenty_task_filter]).\
            order_by('-schpriority')[:20]
        start_time = datetime.datetime.strptime(str(datetime.datetime.now().date())+'6:00', '%Y-%m-%d%H:%M')
        end_time =  datetime.datetime.strptime(str(datetime.datetime.now().date())+'22:00', '%Y-%m-%d%H:%M')
        for task in queryset:
            planbdate = task.planbdate
            planedate = task.planedate
            if planbdate and planedate and \
                planbdate.time() >= start_time.time() and planbdate.time() <= end_time.time() and \
                planedate.time() >= start_time.time() and planedate.time() <= end_time.time():
                pass
            else:
                sch_tasks.append(task)
        return sch_tasks
    @staticmethod
    def get_past_eight_day_arragemnt_task(username):
        '''
        功能描述：獲取用戶past 8 day arragement task
        '''
        start_date = DateTools.addDay(datetime.datetime.now(), -8)
        end_date = DateTools.addDay(datetime.datetime.now(), 1)
        with connections['MPMS'].cursor() as cursor:
            sql_str = "exec GetTaskPlanner %s, %s, %s"
            cursor.execute('SET NOCOUNT ON {CALL dbo.GetTaskPlanner (%s,%s,%s)}', [username,DateTools.format(start_date), DateTools.format(end_date)])
            columns = [column[0].lower() for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                obj = dict(zip(columns, row))
                results.append(obj)        

        start = datetime.datetime(start_date.year, start_date.month, start_date.day)
        end = datetime.datetime(end_date.year, end_date.month, end_date.day)
        queryset = models.VTask.objects.filter(bdate__gte=start, edate__lte=end, progress__in=['C','F'], contact='hb'). \
        extra(where=["(tid between 0 and 99 or TidStr like '%%0[0-9][0-9]' or pid = '00500')"])
        return results, list(queryset)



    @staticmethod
    def get_class1_tasks(username):
        '''
        功能描述：獲取用戶Class1 未完成任務列表
        '''
        queryfilters = QueryFilterService.get_daily_goal_filter("{0}+out+class".format(username))
        qf025 = queryfilters[0].qf025
        if len(queryfilters) > 1:
            for qf in queryfilters:
                if re.search('^'+username, qf.qt002, re.IGNORECASE):
                    qf025 = qf.qf025
        str_filter = QueryFilterService.get_query_filter(qf025)
        queryset_last = models.VTask.objects.raw('select * from V_Task where ' + str_filter + " order by CREATE_DATE desc")
        data = list(queryset_last)
        ##只有最近的class1任務有5條數據，才讀取最早的5條數據,
        # if len(data) == 5:
            # taskno_array = [task.taskno for task in data]
            # queryset_first = models.VTask.objects.raw('select * from V_Task where ' + str_filter + " order by CREATE_DATE asc")             
            # data.extend([task for task in list(queryset_first) if not task.taskno in taskno_array])
        return (data)

    @staticmethod
    def get_group_tasks():
        queryfilters = QueryFilterService.get_daily_goal_filter("all+staff+today", order_num=1150)
        qf025 = queryfilters[0].qf025
        str_filter = QueryFilterService.get_query_filter(qf025)
        queryset = models.VTask.objects.raw('select * from V_Task where ' + str_filter)             
        return (list(queryset))

    @staticmethod
    def get_user_defalut_daily_pattern_tasks(username):
        result = None
        master = models.Tpmast.objects.filter(category="DefDP").extra(where=["exists (select * from TpDetail where TpMast.TpMastId = TpMastId and contact = %s)"], params=[username])[:1]
        if len(master) == 1:
            tpmastid = master[0].tpmastid
            queryset = models.VTask.objects.filter(mastno__startswith="{0}-".format(tpmastid), planbdate=timezone.now().date())
            result = list(queryset)
        return result

    @staticmethod
    def get_arrage_tasks(username, startdate, enddate):
        result = None
        qs = models.VTaskArrage.objects.filter(contact=username, arrangedate__date__range=[startdate, enddate])\
            .filter(~Q(taskcategory='MF')).order_by('arrangedate')
        qs = TaskService.getRequestQuerySetWithSysparam(qs)
        return list(qs)

    @staticmethod
    def get_higest_session_today_tasks(username):
        period = "{0}-{1}".format(DateTools.formatf(DateTools.now(), '%Y'), DateTools.getQuarter(DateTools.now()))
        sessions = SessionService.search_sessioni(period=period, allcontact=username, stype=None, desc=None)               
        result = []
        if sessions and len(sessions) > 0:
            higest_session = sessions[0]
            pid = higest_session['pid']
            tid = higest_session['tid']
            queryset = models.VTask.objects.filter(pid=pid, tid=tid) \
            .filter(Q(progress__in=['C','F'],edate__date=DateTools.now()) | (~Q(progress__in=['C','F'])))
            if username:
                queryset = queryset.filter(contact=username)
            result = [model_to_dict(row) for row in queryset]
        return result