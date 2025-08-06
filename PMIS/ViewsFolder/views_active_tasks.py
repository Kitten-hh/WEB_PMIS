from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,JsonResponse,HttpRequest
from DataBase_MPMS import models,forms_base
from .. import forms
from django.core.serializers.json import DjangoJSONEncoder
import json
import re
import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db import connections,transaction
from datatableview import helpers
from django.db.models import IntegerField,CharField, Value as V
from django.db.models.functions import Cast, Substr
from django.db.models import Sum,Count,Max,Min,Avg,Q
from django.db.models.functions import Left,StrIndex
from ..Services.TaskService import TaskService
from ..Services.UserService import UserService
from BaseApp.library.tools import DateTools
from BaseProject.CustomBaseObject.base_views.CustomView import CustomUpdateView
from BaseProject.CustomBaseObject.mixins.CustomMixin import AjaxableResponseMixin
from django.forms.models import model_to_dict
from ..Services.ActiveTaskService import ActiveTaskService
from django.utils import timezone
from BaseApp.library.tools import  AsyncioTools
from django.utils.dateparse import parse_datetime
from PMIS.Services.MeetingService import MeetingService
from PMIS.Services.GoalManageService import GoalManagementService
from PMISLooper.Services.NtfyNotificationServer import NOTIFICATION_FLAG_FIELD_NAME,NOTIFICATION_TODAY_CYCLE_FIXED_TASK_FLAG,NOTIFICATION_OUTSTAINDING_GOAL_FLAG


def get_user_today_tasks(request:HttpRequest, username):
    '''
    功能描述：處理獲取用戶Schedule_priority
    '''
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        today_tasks = ActiveTaskService.get_today_tasks(username)
        result['status'] = True
        result['data'] = [model_to_dict(task) for task in today_tasks]
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)

def get_today_fixed_tasks_part(request:HttpRequest):
    username = request.GET.get('username');
    type = request.GET.get('type')
    service = ActiveTaskService()
    goalManagementService = GoalManagementService()
    meetingService = MeetingService()
    result = {'data':[]}
    try:
        if type == "1":
            result['data'] = [model_to_dict(task) for task in service.get_today_cycle_fixed(username)]
        elif type == "2":
            today_fixed_tasks, today_scheduled_tasks, today_upcomming_fixed_tasks,today_upcomming_schedule_tasks,outstanding_fixed_tasks,outstanding_schedule_tasks = service.get_today_scheduled_task(username)
            for task in today_fixed_tasks:
                task[NOTIFICATION_FLAG_FIELD_NAME] = NOTIFICATION_TODAY_CYCLE_FIXED_TASK_FLAG
            result['today_fixed_tasks'] = today_fixed_tasks
            result['today_scheduled_tasks'] = today_scheduled_tasks
            result['today_upcomming_fixed_tasks'] = today_upcomming_fixed_tasks
            result['today_upcomming_schedule_tasks'] = today_upcomming_schedule_tasks
            result['outstanding_fixed_tasks'] = outstanding_fixed_tasks
            result['outstanding_schedule_tasks'] = outstanding_schedule_tasks
        elif type == "3":
            result['data'] = [model_to_dict(task) for task in service.get_today_cycle_task(username)]
        elif type == "4":
            result['data'] = [model_to_dict(task) for task in service.get_today_intray_task(username)]
        elif type == "5":
            outstandingGoals = [model_to_dict(task) for task in goalManagementService.getTopOutstandingGoal(username, 5)]
            for goal in outstandingGoals:
                goal[NOTIFICATION_FLAG_FIELD_NAME] = NOTIFICATION_OUTSTAINDING_GOAL_FLAG
            result['data'] = outstandingGoals
        elif type == "6":
            result['data'] = meetingService.getOutstandingPMeeting(username)            
    except Exception as e:
        print(str(e))
    return  JsonResponse(result, safe=False)

def get_today_fixed_tasks(request:HttpRequest):
    '''
    功能描述：處理用戶today's Tasks的http請求
    '''
    def setGroupInfo():
        for index, (name,tasks) in enumerate(allCategoryTasks.items()):
            for task in tasks:
                if style == "list" and 'schcategory' in task:
                    del task['schcategory']
                    del task['schcategory_seqno']
                    
                task['group_type'] = name if name.find("--") == -1 else name.split("--")[1]
                task['parent_group_type'] = name if name.find("--") == -1 else name.split("--")[0]
                task['group_order'] = index+1
                if task['planedate'] and DateTools.format(timezone.now()) > DateTools.format(parse_datetime(task['planedate'])):
                    task['outstanding'] = 'Y'
                else:
                    task['outstanding'] = 'N'
                if task['progress'] == 'T' and task['planedate'] and task['planbdate'] and DateTools.format(timezone.now()) >= DateTools.format(parse_datetime(task['planbdate'])) and \
                    DateTools.format(timezone.now()) <= DateTools.format(parse_datetime(task['planedate'])):
                    task['todayt'] = 'Y'
                else:
                    task['todayt'] = 'N'     
    def calOrderNum(maxCount):
        #找到優先級最高的前10個任務,並標記
        hasSchPriorityTasks = {}
        for i in range(len(today_tasks)):
            task = today_tasks[i]
            if task['schpriority'] and task['schpriority'] > 0:
                hasSchPriorityTasks[i] = task['schpriority']
        hasSchPriorityTasks = {k: v for k, v in sorted(hasSchPriorityTasks.items(), key=lambda item: item[1], reverse=True)}
        for index, (taskIndex, schPriority) in enumerate(hasSchPriorityTasks.items()):
            today_tasks[taskIndex]['task_order_num'] = index + 1
            if index + 1 >= maxCount:
                break;
    
    def calSessionPriorityOrderNumAndStatus(maxCount):
        #找到優先級最高的前10個任務,並標記
        today_tasks.sort(key=lambda x:(x['sessionpriority'] *(-1) if x['sessionpriority'] else 0))
        for i in range(len(today_tasks)):
            task = today_tasks[i]
            if task['planedate'] and DateTools.format(timezone.now()) > DateTools.format(task['planedate']):
                task['outstanding'] = 'Y'
            else:
                task['outstanding'] = 'N'
            if task['progress'] == 'T' and task['planedate'] and task['planbdate'] and DateTools.format(timezone.now()) >= DateTools.format(task['planbdate']) and \
                DateTools.format(timezone.now()) <= DateTools.format(task['planedate']):
                task['todayt'] = 'Y'
            else:
                task['todayt'] = 'N'                   
        for index, task in enumerate(today_tasks):
            task['task_order_num'] = index + 1
            if index + 1 >= maxCount:
                break;    
    
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        today_tasks = []
        username = request.GET.get("contact")
        style = request.GET.get("style","group")
        service = ActiveTaskService()        
        if style == 'single':
            today_tasks = service.get_higest_session_today_tasks(username)
            #查找前10個優先級最高的任務，並標記
            calSessionPriorityOrderNumAndStatus(20)
        else:
            url = AsyncioTools.get_url(request,"today_tasks_part",True)
            
            params = {"username":username}
            http_methods = {str(key):{'url':url+'?type='+str(key), 'params':params} for key in range(1,7)}
            datas = AsyncioTools.async_fetch_http_json(http_methods)        
            if style == "group" or style == "top":
                allCategoryTasks = {
                    "Today's Tasks--User Fixed Day Tasks":datas["2"]["today_fixed_tasks"],
                    "Today's Tasks--Scheduled Tasks":datas["2"]["today_scheduled_tasks"],
                    'Outstanding Tasks--User Fixed Day Tasks':datas["2"]["outstanding_fixed_tasks"],
                    'Outstanding Tasks--Scheduled Tasks':datas["2"]["outstanding_schedule_tasks"],
                    'Meeting Important Outstanding Tasks':datas["6"]["data"],
                    'Outstainding Goals':datas["5"]["data"],
                    'Upcoming Tasks--User Fixed Day Tasks':datas["2"]["today_upcomming_fixed_tasks"],
                    'Upcoming Tasks--Scheduled Tasks':datas["2"]["today_upcomming_schedule_tasks"],
                    'In Tray Tasks':datas["4"]["data"],
                    'Cycle Tasks':datas["3"]["data"]
                }
            else:
                allCategoryTasks = {
                    "Today's Tasks":datas["2"]["today_fixed_tasks"] + datas["2"]["today_scheduled_tasks"],
                    'Outstanding Tasks':datas["2"]["outstanding_fixed_tasks"] + datas["2"]["outstanding_schedule_tasks"],
                    'Meeting Important Outstanding Tasks':datas["6"]["data"],
                    'Outstainding Goals':datas["5"]["data"],
                    'Upcoming Tasks':datas["2"]["today_upcomming_fixed_tasks"] + datas["2"]["today_upcomming_schedule_tasks"],
                    'In Tray Tasks':datas["4"]["data"],
                    'Cycle Tasks':datas["3"]["data"]
                }            
            setGroupInfo() 
            ##處理循環任務的分組
            tpmasts = set([task['mastno'][:task['mastno'].find('-')] for task in allCategoryTasks['Cycle Tasks'] if task['mastno']])
            tpmast_qs = models.Tpmast.objects.values('tpmastid','tpdesc').filter(tpmastid__in = tpmasts).order_by('-tpmastid')
            tp_map = {str(tpmaster['tpmastid']):{'desc':tpmaster['tpdesc'],'order':i} for i,tpmaster in enumerate(tpmast_qs)}
            for task in allCategoryTasks['Cycle Tasks']:
                if task['mastno']:
                    tpmast_id = task['mastno'][:task['mastno'].find('-')]
                    if tpmast_id in tp_map.keys():
                        task['parent_group_type'] = 'Working Pattern'
                        task['group_order'] = task['group_order'] + tp_map[tpmast_id]['order']
                        task['group_type'] = "{0} - {1}".format(task['group_type'], tp_map[tpmast_id]['desc'])

            service.meger_task_dict(allCategoryTasks['In Tray Tasks'], today_tasks)                    
            for name,tasks in allCategoryTasks.items():
                if name in ["Outstainding Goals"]:
                    today_tasks = today_tasks + tasks
                elif name not in ["In Tray Tasks","Meeting Important Outstanding Tasks"]:
                    service.meger_task_dict(tasks, today_tasks)                    
            service.meger_task_dict(allCategoryTasks["Meeting Important Outstanding Tasks"], today_tasks)                    
            
            #排序
            today_tasks.sort(key=lambda x:(x['group_order'], 0 if 'schcategory_seqno' not in x else x['schcategory_seqno'], x['schpriority'] *(-1) if x['schpriority'] else 0))
            #查找前10個優先級最高的任務，並標記
            calOrderNum(20)
            if style == "top" or style == "list": ##如果是top視圖，則只返回前優先級最高的前10個任務
                today_tasks = list(filter(lambda x:'task_order_num' in x, today_tasks))
            if style == "list": ##如果是list視圖，不要分組
                for task in today_tasks:
                    del task['group_order']
                    del task['parent_group_type']
                    del task['group_type']
                today_tasks.sort(key=lambda x:(x['schpriority'] *(-1) if x['schpriority'] else 0))            
        result['status'] = True
        result['data'] = today_tasks
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)
    

def get_user_schedule_tasks(request:HttpRequest, username):
    '''
    功能描述：處理獲取用戶Schedule_priority
    '''
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        schedule_tasks,_ = ActiveTaskService.get_past_eight_day_arragemnt_task(username)
        result['status'] = True
        result['data'] = schedule_tasks
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)    

def get_user_class1_tasks(request:HttpRequest, username):
    '''
    功能描述：處理獲取用戶未完成Class1 Task    
    '''
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        class1_tasks = ActiveTaskService.get_class1_tasks(username)
        result['status'] = True
        result['data'] =  [model_to_dict(task) for task in class1_tasks]
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)    

def get_group_tasks(request:HttpRequest):
    '''
    功能描述：處理Group Task    
    '''
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        group_tasks = ActiveTaskService.get_group_tasks()
        result['status'] = True
        result['data'] =  [model_to_dict(task) for task in group_tasks]
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)    

def get_user_def_daily_pattern(request:HttpRequest,username):
    '''
    功能描述：獲取用戶Default Dialy Pattern
    '''
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        default_daily_patterns = ActiveTaskService.get_user_defalut_daily_pattern_tasks(username)
        result['status'] = True
        result['data'] =  [model_to_dict(template) for template in default_daily_patterns]
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)    

def get_arrage_tasks(request:HttpRequest):
    '''
    功能描述：
    '''
    result = {'status':False, 'msg':'', 'data':[]}
    def getPastDayParams():
        try:
            rs = models.Syspara.objects.filter(nfield='PastArrageTaskDay', ftype='ActivityPage')
            return StrToInt(rs[0].fvalue)
        except Exception as e:
            return 1 #默認為1
    def getCommingDayParams():
        try:
            rs = models.Syspara.objects.filter(nfield='CommingArrageTaskDay', ftype='ActivityPage')
            return StrToInt(rs[0].fvalue)
        except Exception as e:
            return 7 #默認為7
    try:
        contact = request.GET.get("contact")
        query_type = request.GET.get("type", "T")
        if query_type == "P":
            pastDay = getPastDayParams()
            data = ActiveTaskService.get_arrage_tasks(contact, DateTools.addDay(DateTools.now(), pastDay * -1), DateTools.addDay(DateTools.now(), pastDay * -1));
        elif query_type == "C":
            futureDay = getCommingDayParams()
            data = ActiveTaskService.get_arrage_tasks(contact, DateTools.addDay(DateTools.now(), 1), DateTools.addDay(DateTools.now(), futureDay+1));
        elif query_type == "T":
            data = ActiveTaskService.get_arrage_tasks(contact, DateTools.now(), DateTools.now());
        else:
            raise Exception("參數不正確")
        result['data'] = [{**model_to_dict(item),**{'planbdate2':DateTools.formatf(item.planbdate, '%Y-%m-%d %H:%M')}} for item in data]
        result['status'] = True
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)