from django.shortcuts import render

from DataBase_MPMS import models
from django.forms.models import model_to_dict
from django.db.models import Count,Q,Case,Sum,When,IntegerField,Max
import json
import datetime
from django.http import JsonResponse,HttpResponse,HttpRequest
from BaseApp.library.cust_views.SWCreateView import SWCreateView
from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from BaseApp.library.tools import DateTools
from PMISLooper.Services.ProjectManagementService import ProjectManagementService
from PMIS.Services.UserService import UserService
import logging
import math

LOGGER = logging.getLogger(__name__)

class ProjectGoalCreateView(SWCreateView):
    model = models.MpGoals

    def get_initial(self, instance:models.MpGoals):
        instance.quarterly = self.request.GET.get('quarterly', ProjectManagementService.get_cur_quarterly())
        instance.contact = self.request.GET.get("contact", UserService.GetLoginUserName(self.request))
        instance.progress = 'N' #默認為N

class ProjectGoalUpdateView(SWUpdateView):
    model = models.MpGoals

def analysis_goal_simulation(Request:HttpRequest):
    '''
    功能描述：分析Goal Simulation
    '''
    def get_query(pk):
        query = Q()
        query.conditional = Q.OR
        goal = models.Goalmanagement.objects.get(pk=pk)
        sessions = getattr(goal, "sessions","")
        sessions_arr = sessions.split(',')
        for session in sessions_arr:
            session = session.strip()
            arr = session.split('-')
            if len(arr) == 2:
                query.add(Q(pid=arr[0], tid=arr[1]), Q.OR)
        return query
    def analysis(tasks):
        data = {'total_qty':0, 'finish_qty':0, 'unfinish_qty':0, 'left_days':0, 'expected_date':DateTools.formatf(DateTools.now(), '%Y-%m-%d'),'ratio':0,
        'total_qty_simu':0, 'finish_qty_simu':0, 'unfinish_qty_simu':0, 'left_days_simu':0, 'expected_date_simu':DateTools.formatf(DateTools.now(), '%Y-%m-%d'), 'ratio_simu':0}
        if len(tasks) == 0:
            return data
        data['total_qty'] = len(tasks)
        est_finish_qty = 0
        finish_qty_simu = 0
        left_tasks  = []
        right_tasks = []
        for task in tasks:
            if task.planedate and DateTools.format(task.planedate) <= DateTools.format(DateTools.now()):
                est_finish_qty += 1
                left_tasks.append(task)
            else:
                right_tasks.append(task)
            if task.progress in ['C','F']:
                finish_qty_simu += 1
        data['finish_qty'] = est_finish_qty
        data['unfinish_qty'] = data['total_qty'] - data['finish_qty']
        left_days = 0
        ##如果當天時間小於計畫最後一天,才有剩餘天數
        if DateTools.format(tasks[data['total_qty'] - 1].planedate) >= DateTools.format(DateTools.now()):
            left_days = DateTools.dateBetweenHasSelf(tasks[data['total_qty'] - 1].planedate, DateTools.now()) 
        data['left_days'] = left_days
        data['expected_date'] = DateTools.formatf(tasks[data['total_qty'] - 1].planedate, '%Y-%m-%d')
        data['ratio'] = data['finish_qty']/data['total_qty']

        data['total_qty_simu'] = len(tasks)
        data['finish_qty_simu'] = finish_qty_simu
        data['unfinish_qty_simu'] = data['total_qty_simu'] - data['finish_qty_simu']
        data['ratio_simu'] = data['finish_qty_simu']/data['total_qty_simu']
        ##如果所有任務都已經完成
        if data['unfinish_qty_simu'] == 0:
            data['left_days_simu'] = 0
            data['expected_date_simu'] = DateTools.formatf(tasks[len(tasks)-1].planedate, '%Y-%m-%d')
        else:
            start_date = tasks[0].planbdate
            end_date = tasks[len(tasks)-1].planedate
            ##如果左邊的任務都已經完成
            if len([task for task in left_tasks if not task.progress in ['C','F']]) == 0:
                ##如果右邊的任務的任務都沒有完成
                if len([task for task in right_tasks if task.progress in ['C','F']]) == 0:
                    start_date = DateTools.now()
                    end_date = right_tasks[len(right_tasks)-1].planedate
                ##右邊有任務沒有完成
                else:
                    #找出右邊連續完成的最後一個任務
                    right_finish_task = right_tasks[0]
                    for task in right_tasks:
                        if task.progress in ['C','F']:
                            right_finish_task = task
                        else:
                            break
                    start_date = right_finish_task.planedate
                    end_date = right_tasks[len(right_tasks) -1].planedate
            else:
                ##取左邊第一個沒有完成的任務的結束日期，如果是第一個任務取開始日期
                if not left_tasks[0].progress in ['C','F']:
                    start_date = left_tasks[0].planbdate
                else:
                    start_date = [task for task in left_tasks if not task.progress in ['C','F']][0].planedate
                end_date = tasks[len(tasks)-1].planedate
            data['left_days_simu'] = DateTools.dateBetween(start_date, end_date)+1
            data['expected_date_simu'] = DateTools.formatf(DateTools.addDay(DateTools.now(), data['left_days_simu']), '%Y-%m-%d')
        return data
    result = {'status':False, 'msg':'', 'data':{}}
    try:
        pk = Request.GET.get("pk","")
        query = get_query(pk)
        qs = models.Task.objects.filter(process='C').filter(query).order_by("planbdate")
        data = analysis(qs)
        result['data'] = data
        result['status'] = True
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)

def analysis_goal_simulation_test(Request:HttpRequest):
    '''
    功能描述：分析Goal Simulation
    '''
    result = {'status':False, 'msg':'', 'data':{}}

    try:
        pk = Request.GET.get("pk","")
        goal = models.Goalmanagement.objects.get(pk=pk)
        param = models.Syspara.objects.filter(ftype="GoalSimulation", nfield="TechnicalQtyAvg")[:1]
        tech_avg = int(param[0].fvalue if param else "5")
        allocateuser = goal.allocateuser if goal.allocateuser else 1
        sessions = getattr(goal, "sessions","")
        sessions_arr = sessions.split(',')
        str_sql = '''SELECT 1 INC_ID,COUNT_BIG([Task].[Pid]) AS [total_qty], SUM(CASE WHEN [Task].[Progress] IN ('C', 'F') THEN 1 ELSE 0 END) AS [finish_qty],
                    SUM(CASE WHEN [Task].[Progress] IN ('C', 'F') THEN 1 ELSE 0 END) AS [active_qty],
                    Max(Case WHEN [Task].[Progress] IN ('C', 'F') then NULL else PlanEDate END) as expected_date,
                    ISNULL(SUM(ManDay),0) total_qty_simu,
                    SUM(CASE WHEN [Task].[Progress] IN ('C', 'F') THEN ManDay ELSE 0 END) AS [finish_qty_simu],
                    SUM(CASE WHEN [Task].[Progress] IN ('T', 'I') THEN ManDay Else 0 END) As active_qty_simu
                    FROM [Task] WHERE [Task].[Process] = 'C'
                '''
        session_filter = ''
        params = []
        for session in sessions_arr:
            session = session.strip()
            arr = session.split('-')
            if len(arr) == 2:
                if session_filter == '':
                    session_filter = "(Pid=%s and tid=%s)"
                else:
                    session_filter = session_filter + " or (Pid=%s and tid=%s)"
                params.append(arr[0])
                params.append(arr[1])
        str_sql = str_sql + " and (" + session_filter + ")"
        queryset = models.Task.objects.raw(str_sql, params)
        data = {key:value for key,value in queryset[0].__dict__.items() if key in ['total_qty','finish_qty','active_qty','expected_date','total_qty_simu','finish_qty_simu','active_qty_simu']}

        for key,value in data.items():
            if value == None:
                data[key] = 0
        data['unfinish_qty'] = data['total_qty'] - data['finish_qty']
        data['qty_ratio'] = 0
        if (data['finish_qty'] > 0):
            data['qty_ratio'] = data['finish_qty']/data['total_qty']
        if data['expected_date']:
            data['expected_date'] = DateTools.formatf(data['expected_date'], '%Y-%m-%d')
        else:
            data['expected_date'] = DateTools.formatf(DateTools.now(), '%Y-%m-%d')

        data['total_qty_simu'] =  round(data['total_qty_simu']/(allocateuser * tech_avg),2)
        data['finish_qty_simu'] = round(data['finish_qty_simu']/(allocateuser * tech_avg),2)
        data['active_qty_simu'] = round(data['active_qty_simu']/(allocateuser * tech_avg),2)
        data['unfinish_qty_simu'] = data['total_qty_simu'] - data['finish_qty_simu']
        data['expected_date_simu'] = DateTools.formatf(DateTools.addDay(DateTools.now(), math.ceil(data['unfinish_qty_simu'])), '%Y-%m-%d')
        if data['finish_qty_simu'] > 0:
            data['qty_ratio_simu'] = round(data['finish_qty_simu']/data['total_qty_simu'],2)
        else:
            data['qty_ratio_simu'] = 0
        result['status'] = True
        result['data'] = data
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)


def analysis_goal_simulation_bak(Request:HttpRequest):
    '''
    功能描述：分析Goal Simulation
    '''
    result = {'status':False, 'msg':'', 'data':{}}
    try:
        sessions = Request.GET.get("sessions","")
        sessions_arr = sessions.split(',')
        str_sql = '''SELECT 1 INC_ID, COUNT_BIG([Pid]) AS [total_qty], SUM(CASE WHEN [Progress] IN ('C', 'F') THEN 1 ELSE 0 END) AS [finish_qty],
                    SUM(CASE WHEN [Progress] IN ('C', 'F') THEN 1 ELSE 0 END) AS [active_qty],
                    SUM(CASE WHEN ISNULL(DATEDIFF(DAY, PlanBDate, PlanEDate),0) <= 0 THEN 1 ELSE ISNULL(DATEDIFF(DAY, PlanBDate, PlanEDate),0) + 1 END) total_day,
                    SUM(CASE WHEN [Progress] NOT IN ('C', 'F') THEN 
                    CASE WHEN ISNULL(DATEDIFF(DAY, PlanBDate, PlanEDate),0) <= 0 THEN 1 ELSE ISNULL(DATEDIFF(DAY, PlanBDate, PlanEDate),0) + 1 END
                    ELSE 0 END) lave_day,
                    SUM(CASE WHEN [Progress] IN ('T', 'I') THEN 
                    CASE WHEN ISNULL(DATEDIFF(DAY, PlanBDate, PlanEDate),0) <= 0 THEN 1 ELSE ISNULL(DATEDIFF(DAY, PlanBDate, PlanEDate),0) + 1 END
                    ELSE 0 END) actived_day
                    FROM [Task] WHERE [Process] = 'C'
                '''
        session_filter = ''
        params = []
        for session in sessions_arr:
            session = session.strip()
            arr = session.split('-')
            if len(arr) == 2:
                if session_filter == '':
                    session_filter = "(Pid=%s and tid=%s)"
                else:
                    session_filter = session_filter + " or (Pid=%s and tid=%s)"
                params.append(arr[0])
                params.append(arr[1])
        str_sql = str_sql + " and (" + session_filter + ")"
        queryset = models.Task.objects.raw(str_sql, params)
        '''
        queryset = models.Task.objects.filter(process='C')
        query = Q()
        query.conditional = Q.OR
        for session in sessions_arr:
            session = session.strip()
            arr = session.split('-')
            if len(arr) == 2:
                query.add(Q(pid=arr[0], tid=arr[1]), Q.OR)
        queryset = queryset.filter(query)
        queryset = queryset.extra(select={'total_day':"CASE WHEN ISNULL(DATEDIFF(DAY, PlanBDate, PlanEDate),0) <= 0 THEN 1 ELSE ISNULL(DATEDIFF(DAY, PlanBDate, PlanEDate),0) + 1 END",
            'lave_day':"CASE WHEN [Task].[Progress] NOT IN ('C', 'F') THEN \
                    CASE WHEN ISNULL(DATEDIFF(DAY, PlanBDate, PlanEDate),0) <= 0 THEN 1 ELSE ISNULL(DATEDIFF(DAY, PlanBDate, PlanEDate),0) + 1 END \
                    ELSE 0 END",
            'active_day':"CASE WHEN [Task].[Progress] IN ('T', 'I') THEN \
                    CASE WHEN ISNULL(DATEDIFF(DAY, PlanBDate, PlanEDate),0) <= 0 THEN 1 ELSE ISNULL(DATEDIFF(DAY, PlanBDate, PlanEDate),0) + 1 END \
                    ELSE 0 END"})
        queryset = queryset.annotate(total_qty= Count('pid'), 
            finish_qty=Sum(Case(When(progress__in='CF', then=1),
                    default=0,
                    output_field=IntegerField()
            )),
            active_qty=Sum(Case(When(progress__in='TI', then=1),
                    default=0,
                    output_field=IntegerField()
            )),
            total_day=Sum('total_day'),
            lave_day = Sum('lave_day'),
            active_day=Sum('active_day')
        )'''
        data = {key:value for key,value in queryset[0].__dict__.items() if key in ['total_qty','finish_qty','active_qty','total_day','lave_day','actived_day']}

        for key,value in data.items():
            if value == None:
                data[key] = 0
        data['unfinish_qty'] = data['total_qty'] - data['finish_qty']
        data['qty_ratio'] = 0
        if (data['finish_qty'] > 0):
            data['qty_ratio'] = data['finish_qty']/data['total_qty']
        finish_date = data['total_day'] - data['lave_day']
        if finish_date > 0:
            data['day_ratio'] = finish_date/data['total_day']
        else:
            data['day_ratio'] = 0
        if data['lave_day'] > 0:
            data['expected_date'] = DateTools.formatf(DateTools.addDay(DateTools.now(), data['lave_day']), '%Y-%m-%d')
        else:
            data['expected_date'] = DateTools.formatf(DateTools.now(), '%Y-%m-%d')
        result['status'] = True
        result['data'] = data
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)

def get_project_goal(request:HttpRequest):
    result = {'status':False, 'msg':'', 'data':None}
    try:
        contact = request.GET.get('contact')
        period = request.GET.get("period")
        goals = models.Goalmanagement.objects.filter(period=period, contact=contact, goaltype='Q')
        data = {'quarterly':[], 'sessions':[]}
        sessions = []
        for goal in goals:
            data['quarterly'].append(model_to_dict(goal))
            if goal.sessions:
                arr = goal.sessions.split(",")
                for session in arr:
                    sessions.append(session);
        sessions = models.VTasklist.objects.filter(sessionid__in = sessions)
        data['sessions'] = [model_to_dict(session) for session in sessions]
        result['status'] = True
        result['data'] = data
    except Exception as e:
        LOGGER.error(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)
