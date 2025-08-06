from typing import Set
from django.db.models.fields import CharField
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.template import loader
from django.http import HttpResponse,JsonResponse,HttpRequest
from django.db.models import Sum,Count,Max,Min,Avg,Q,Case,When,IntegerField,Value,ExpressionWrapper
from BaseApp.library.cust_views.SWDeleteView import SWDeleteView
from DataBase_MPMS import models
from .. import forms
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from datatableview import Datatable
from django.db import connections
from datatableview.views import MultipleDatatableView
from datatableview.views.legacy import LegacyDatatableView
from datatableview import helpers
from django.middleware.gzip import GZipMiddleware
import random
import pytz
from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from ..Services.GoalService import GoalService
from ..Services.SessionService import SessionService
from BaseApp.library.tools import DateTools, ModelTools
from BaseApp.library.cust_views.SWCreateView import SWCreateView
import logging
from django.db import transaction
import re
from django.contrib.auth.decorators import login_required

LOGGER = logging.Logger(__name__)


def get_overall_monthly_goal(request:HttpRequest):
    result = {'status':False, 'msg':'', 'data':None}
    try:
        contact = request.GET.get('contact')
        period = request.GET.get('period')
        first_date,_ = SessionService.get_quarterly_date(period)
        group_monthly = {}
        group_monthly[DateTools.formatf(first_date, '%Y-%m')] = []
        group_monthly[DateTools.formatf(DateTools.addMonth(first_date,1), '%Y-%m')] = []
        group_monthly[DateTools.formatf(DateTools.addMonth(first_date,2), '%Y-%m')] = []

        goals = GoalService.get_overall_monthly_goal(contact, period)
        for goal in goals:
            planbdate = goal['planbdate']
            if planbdate:
                key = DateTools.formatf(planbdate, '%Y-%m')
                if key in group_monthly:
                    group_monthly[key].append(goal)
        result['status'] = True
        result['data'] = group_monthly

    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)    

def get_overall_monthly_goal_bak(request:HttpRequest):
    result = {'status':False, 'msg':'', 'data':None}
    try:
        contact = request.GET.get('contact')
        period = request.GET.get('period')
        first_date,_ = SessionService.get_quarterly_date(period)
        group_monthly = {}
        group_monthly[DateTools.formatf(first_date, '%Y-%m')] = []
        group_monthly[DateTools.formatf(DateTools.addMonth(first_date,1), '%Y-%m')] = []
        group_monthly[DateTools.formatf(DateTools.addMonth(first_date,2), '%Y-%m')] = []

        goals = GoalService.get_overall_monthly_goal_bak(contact, period, True)
        for goal in goals:
            planbdate = goal.planbdate
            if planbdate:
                key = DateTools.formatf(planbdate, '%Y-%m')
                if key in group_monthly:
                    group_monthly[key].append(model_to_dict(goal))
        result['status'] = True
        result['data'] = group_monthly

    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)  

def del_overall_goal(request:HttpRequest):
    result = {'status':False, 'msg':'', 'data':None}
    try:
        pk = request.GET.get("pk")
        with transaction.atomic(using='MPMS'):
            parent_task_no = models.VTask.objects.values('taskno').get(pk=pk)['taskno']
            models.Task.objects.filter(pk=pk).update(class_field=None)
            models.Task.objects.filter(relationgoalid=parent_task_no).update(class_field=None)
        result['status'] = True
    except Exception as e:
        LOGGER.error(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)

def add_overall_goal(request:HttpRequest):
    result = {'status':False, 'msg':'', 'data':None}
    try:
        pk = request.GET.get("pk")
        with transaction.atomic(using='MPMS'):
            parent_task_no = models.VTask.objects.values('taskno').get(pk=pk)['taskno']
            models.Task.objects.filter(pk=pk).update(class_field=1)
            models.Task.objects.filter(relationgoalid=parent_task_no).update(class_field=1)
        result['status'] = True
    except Exception as e:
        LOGGER.error(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)

def get_overall_weekly_goal_bak(request:HttpRequest):
    result = {'status':False, 'msg':'', 'data':None}
    try:
        contact = request.GET.get('contact')
        period = request.GET.get("period")
        first_date,_ = SessionService.get_quarterly_date(period)
        group_weekly = {}
        group_weekly[DateTools.formatf(first_date, '%Y-%m')] = {'weekly1':[], 'weekly2':[], 'weekly3':[], 'weekly4':[], 'weekly5':[]}
        group_weekly[DateTools.formatf(DateTools.addMonth(first_date,1), '%Y-%m')] = {'weekly1':[], 'weekly2':[], 'weekly3':[], 'weekly4':[], 'weekly5':[]}
        group_weekly[DateTools.formatf(DateTools.addMonth(first_date,2), '%Y-%m')] = {'weekly1':[], 'weekly2':[], 'weekly3':[], 'weekly4':[], 'weekly5':[]}

        goals = GoalService.get_overall_weekly_goal_bak(contact, period, True)
        for goal in goals:
            planbdate = goal.planbdate
            if planbdate:
                key = DateTools.formatf(planbdate, '%Y-%m')
                if key in group_weekly:
                    weekly_str = 'weekly{0}'.format(DateTools.get_week_of_month(planbdate))
                    if weekly_str in group_weekly[key]:
                        group_weekly[key][weekly_str].append(model_to_dict(goal))
        result['status'] = True
        result['data'] = group_weekly
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)

def get_overall_weekly_goal(request:HttpRequest):
    result = {'status':False, 'msg':'', 'data':None}
    try:
        contact = request.GET.get('contact')
        period = request.GET.get("period")
        first_date,_ = SessionService.get_quarterly_date(period)
        group_weekly = {}
        group_weekly[DateTools.formatf(first_date, '%Y-%m')] = {'weekly1':[], 'weekly2':[], 'weekly3':[], 'weekly4':[], 'weekly5':[]}
        group_weekly[DateTools.formatf(DateTools.addMonth(first_date,1), '%Y-%m')] = {'weekly1':[], 'weekly2':[], 'weekly3':[], 'weekly4':[], 'weekly5':[]}
        group_weekly[DateTools.formatf(DateTools.addMonth(first_date,2), '%Y-%m')] = {'weekly1':[], 'weekly2':[], 'weekly3':[], 'weekly4':[], 'weekly5':[]}

        goals = GoalService.get_overall_weekly_goal(contact, period)
        for goal in goals:
            planbdate = goal['planbdate']
            if planbdate:
                key = DateTools.formatf(planbdate, '%Y-%m')
                if key in group_weekly:
                    weekly_str = 'weekly{0}'.format(DateTools.get_week_of_month(planbdate))
                    if weekly_str in group_weekly[key]:
                        group_weekly[key][weekly_str].append(goal)
        result['status'] = True
        result['data'] = group_weekly
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)

def get_goal_management(request:HttpRequest):
    result = {'status':False, 'msg':'', 'data':None}
    try:
        contact = request.GET.get('contact')
        period = request.GET.get("period")
        goals = GoalService.get_goal_management(contact, period)
        data = {}
        for goal in goals:
            if goal.goaltype == "Q":
                if 'quarterly' not in data:
                    data['quarterly'] = []
                data['quarterly'].append(model_to_dict(goal))
            elif goal.goaltype == "M":
                if 'monthly-{0}'.format(goal.month) not in data:
                    data['monthly-{0}'.format(goal.month)] = {}
                data['monthly-{0}'.format(goal.month)]["data"] = model_to_dict(goal)
            else:
                if 'monthly-{0}'.format(goal.month) not in data:
                    data['monthly-{0}'.format(goal.month)] = {}
                data['monthly-{0}'.format(goal.month)]['weekly-{0}'.format(goal.week)] = model_to_dict(goal)
        result['status'] = True
        result['data'] = data
    except Exception as e:
        LOGGER.error(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)

class CreateGoalManagementView(SWCreateView):
    model = models.Goalmanagement

    def get_initial(self, instance:models.Goalmanagement):
        '''
        功能描述：Http Get 訪問時初始化model新增時的數據
        參數說明:
            instance:該model的實例
        '''
        self.set_max_seqno(instance)

    def set_max_seqno(self, instance:models.Goalmanagement):
        '''
        功能描述：獲取最大單號
        參數說明:
            instance:需要保存或初始化的model實例
        '''
        qs = models.Goalmanagement.objects.values('goalid').all().order_by('-goalid')[:1]
        if len(qs) > 0 :
            instance.goalid = qs[0]['goalid'] + 10
        else:
            instance.goalid = 10
    def save_other(self, instance):
        if instance.goaltype == 'W':
            details = split_week_goal(instance)
            models.Goalmanagementdetail.objects.filter(goalid=instance.goalid).delete()
            models.Goalmanagementdetail.objects.bulk_create(details,batch_size=50)            

class UpdateGoalManagementView(SWUpdateView):
    model = models.Goalmanagement
    def save_other(self, instance):
        inst = models.Goalmanagement.objects.get(pk=instance.inc_id)
        if instance.sessions != inst.sessions:
            instance.sessions = inst.sessions
        if instance.goaldesc != inst.goaldesc:
            instance.goaldesc = inst.goaldesc
        if instance.goaltype == 'W':
            self.update_week_goal(inst)
            details = split_week_goal(instance)
            models.Goalmanagementdetail.objects.filter(goalid=instance.goalid).delete()
            models.Goalmanagementdetail.objects.bulk_create(details,batch_size=50)

    def update_week_goal(self, instance):
        tasks = []
        sessions = instance.sessions
        if not sessions:
            sessions = '{}'
        sessions = json.loads(sessions);
        del_sessions = []
        goaldesc = "" if not instance.goaldesc else instance.goaldesc
        for sessionid, taskids in sessions.items():
            if goaldesc.find(sessionid) != -1:
                task_list = ["{0}-{1}".format(sessionid, taskid) for taskid in taskids.split(",")]
                tasks.extend(task_list)
            else:
                del_sessions.append(sessionid)
        for sessionid in del_sessions:
            del sessions[sessionid]
        relationtasks = ",".join(tasks)
        if relationtasks != instance.relationtasks:
            instance.sessions = json.dumps(sessions)
            instance.relationtasks = relationtasks
            instance.save(update_fields=['relationtasks','sessions'])

def split_week_goal(weekly_goal):
    goaldesc = weekly_goal.goaldesc
    sessions = weekly_goal.sessions
    #如果該Weekly Goal的描述為內，則刪除details
    if not goaldesc:
        return []
    #將Goal內容以回車換行符拆分成多個Goal
    goals = goaldesc.replace("\r\n", "\r").replace("\n", "\r").split("\r")
    if not sessions:
        sessions = '{}'
    sessions = json.loads(sessions)
    goal_management_details = []
    #根據Goal內容和weekly_goal構造details
    for index,goal in enumerate(goals):
        goal_detail = models.Goalmanagementdetail()
        goal_detail.goalid = weekly_goal.goalid
        goal_detail.itemno = (index + 1) * 10
        goal_detail.goaldesc = goal
        match = re.search(r"\(((\w+-\d+,?)+)\)$", goal, re.IGNORECASE)
        relation_tasks = []
        if match:
            relation_sessions = match.group(1).split(",")
            for sessionid in relation_sessions:
                if sessionid in sessions and sessions[sessionid]:
                    temp_taskno = ["{0}-{1}".format(sessionid, taskid) for taskid in sessions[sessionid].split(",")]
                    relation_tasks.extend(temp_taskno)
            goal_detail.relationtasks = ",".join(relation_tasks)
        goal_management_details.append(goal_detail)
    return goal_management_details
    

class DeleteGoalManagementView(SWDeleteView):
    model = models.Goalmanagement    

class GoalManagementTableView(DatatablesServerSideView):
    model = models.Goalmanagement
    columns = '__all__'
    searchable_columns = '__all__'

@login_required()
def saveTextQuarterlyGoal(request:HttpRequest):
    def convert(content):
        if not content:
            return []
        lines = content.strip().replace("\r\n", "\r").replace("\n", "\r").split("\r")
        goals = []
        current = ""
        for row in lines:
            if re.search("^\s*G\d+", row): #以G數字開頭表示一個Goal開始
                if current:
                    goals.append(current.strip()) #將分析出的前一個Goal添加到結果數組中
                    current = "" #清除當前goal
            current += row + "\r"
        if current:
            goals.append(current)
        return goals

    def get_max_seqno():
        '''
        功能描述：獲取最大單號
        參數說明:
            instance:需要保存或初始化的model實例
        '''
        qs = models.Goalmanagement.objects.values('goalid').all().order_by('-goalid')[:1]
        if len(qs) > 0 :
            return qs[0]['goalid'] + 10
        else:
            return 10    

    result = {'status':False, 'msg':'', 'data':[]}
    try:
        contact = request.POST.get('contact')
        period = request.POST.get('period')
        content = request.POST.get('content', '')
        goals = convert(content)
        ##有Goal才處理，沒有則不處理
        if goals:
            qs = models.Goalmanagement.objects.filter(contact=contact, period=period, goaltype='Q').order_by('goalid')
            create_list = []
            exists_index = len(qs)
            for index, goal in enumerate(goals):
                if index < exists_index: #已經存在對應的Goal, 只根據順序對應
                    qs[index].goaldesc = goal
                else:
                    quarterly_goal = models.Goalmanagement(contact=contact, period=period, goaltype='Q', goaldesc=goal)
                    create_list.append(quarterly_goal)
            ##保存數據
            if len(create_list) > 0:
                max_seqno = get_max_seqno()
                for index, goal in enumerate(create_list):
                    goal.goalid = max_seqno + index * 10
            with transaction.atomic(ModelTools.get_database(models.Goalmanagement)):
                if len(qs) > 0:
                    models.Goalmanagement.objects.bulk_update(qs[:len(goals)], fields=['goaldesc'])
                if len(qs) > len(goals):
                    for i in range(len(goals), len(qs)):
                        qs[i].delete()
                if len(create_list) > 0:
                    models.Goalmanagement.objects.bulk_create(create_list)

        #從新讀取Quarterly Goal
        qs = models.Goalmanagement.objects.filter(period=period, contact=contact, goaltype='Q')
        data = {'quarterly':[model_to_dict(goal) for goal in qs]}
        result['status'] = True
        result['data'] = data
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)

class SelectAppraisalView(DatatablesServerSideView):
    model = models.VGoalmanagementM
    columns = ['recordid','objective','task', 'inc_id']
    searchable_columns = ['recordid','objective', 'task']

    def get_initial_queryset(self):
        contact = self.request.GET.get("contact")
        period = self.request.GET.get("period")
        month = self.request.GET.get("month");
        filter = Q()
        filter.connector = "and"
        if contact:
            filter.children.append(("contact", contact))
        if period:
            filter.children.append(("period", period))
        if month:
            month_date = DateTools.parsef(month, "%Y-%m")
            start_date = DateTools.getBeginOfMonth(month_date)
            end_date = DateTools.getEndofMonth(month_date)
            filter.children.append(('planbdate__gte', start_date))
            filter.children.append(('planedate__lte', end_date))
        return self.model.objects.filter(~Q(class_field=1)).filter(filter)
class SelectWeeklyView(DatatablesServerSideView):
    model = models.VGoalmanagementW
    columns = ['recordid','objective','task', 'inc_id']
    searchable_columns = ['recordid','objective', 'task']

    def get_initial_queryset(self):
        contact = self.request.GET.get("contact")
        period = self.request.GET.get("period")
        month = self.request.GET.get("month")
        weekly = self.request.GET.get("weekly")
        filter = Q()
        filter.connector = "and"
        if contact:
            filter.children.append(("contact", contact))
        if period:
            filter.children.append(("period", period))
        if month:
            month_date = DateTools.parsef(month, "%Y-%m")
            month_start_date = DateTools.getBeginOfMonth(month_date)
            month_end_date = DateTools.getEndofMonth(month_date)
            if weekly:
                start_date = DateTools.addWeek(month_start_date, int(weekly) - 1)
                start_date = DateTools.getBeginOfWeek(start_date)
                end_date = DateTools.getEndOfWeek(start_date)
                ##如果開始日期比這個月最後日期都大
                if DateTools.format(start_date) > DateTools.format(month_end_date):
                    start_date = month_end_date
                elif DateTools.format(end_date) > DateTools.format(month_end_date):
                    end_date  = month_end_date
            else:
                start_date = month_start_date
                end_date = month_end_date
            filter.children.append(('planbdate__gte', start_date))
            filter.children.append(('planedate__lte', end_date))
        return self.model.objects.filter(~Q(class_field=1)).filter(filter)

def get_week_goal(request:HttpRequest):
    def analysis_progress(data):
        goal_task_keys = {}
        queryFilter = Q()
        queryFilter.conditional = 'OR'
        for item in data:
            goal_desc = item['goaldesc']
            sessions = item['sessions']
            if not sessions:
                sessions = '{}'
            sessions = json.loads(sessions);
            if not item['inc_id'] in goal_task_keys:
                goal_task_keys[item['inc_id']] = []
            for sessionid, taskids in sessions.items():
                query = Q()
                query.conditional = "AND"
                if len(sessionid.split("-")) == 2 and taskids:
                    task_list = ["{0}-{1}".format(sessionid, taskid) for taskid in taskids.split(",")]
                    query.children.append(('pid', sessionid.split("-")[0]))
                    query.children.append(('tid', sessionid.split("-")[1]))
                    query.children.append(('taskid__in', taskids.split(",")))
                    queryFilter.add(query, Q.OR)
                    goal_task_keys[item['inc_id']].extend(task_list)
        if queryFilter:
            qs = list(models.VTask.objects.filter(queryFilter))
        else:
            qs = []
        for item in data:
            if item['inc_id'] in goal_task_keys:
                tasks_array = [model_to_dict(task) for task in qs if task.taskno in goal_task_keys[item['inc_id']]]
                item['finish_qty'] = len([task for task in tasks_array if task['progress'] in ['C','F']])
                item['total_qty'] = len(tasks_array)
                item['tasks_array'] = tasks_array
            else:
                item['finish_qty'] = 0
                item['total_qty'] = 0
                item['tasks_array'] = []
        return data
            
    result = {'status':False, 'msg':'', 'data':None}
    try:
        contact = request.GET.get("contact")
        weeks = '-1,0,1'
        weeks_date = []
        for week in weeks.split(","):
            week_date = DateTools.addWeek(DateTools.now(), int(week))
            if week == '-1':
                week_date = DateTools.getEndOfWeek(week_date)
            elif week == '1':
                week_date = DateTools.getBeginOfWeek(week_date)
            weeks_date.append(week_date)
        query = Q()
        query.conditional = Q.OR
        week_params = {}
        for idx,w_date in enumerate(weeks_date):
            period = '{0}-{1}'.format(DateTools.formatf(w_date, '%Y'), DateTools.getQuarter(w_date))
            month = DateTools.formatf(w_date, '%Y-%m')
            week = DateTools.get_week_of_month(w_date)
            query.add(Q(period=period, goaltype='W', month=month, week=week), Q.OR)
            week_params[idx] = [period, month, week]
        qs = models.Goalmanagement.objects.all()
        if contact:
            qs = qs.filter(contact=contact)
        qs = qs.filter(query).order_by('contact','period','month','week')
        data = []
        for item in qs:
            local_item = model_to_dict(item)
            for key, value in week_params.items():
                if item.period == value[0] and item.month == value[1] \
                    and item.week == value[2]:
                    local_item['week_num'] = key
            data.append(local_item)
        data = analysis_progress(data)
        result['data'] = data
        result['status'] = True
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)    