# views.py

from django.shortcuts import render
from django.http import JsonResponse
from DataBase_MPMS.models import VTasklistS, Task,Subproject,Goalmanagement,VTask, VTaskRecordid
from ChatwithAi_app.models import Aisummaryrecord
from BaseApp.library.tools import AsyncioTools,DateTools,ModelTools
import logging
from django.db.models import Sum,Count,Max,Min,Avg,Q
import json
from django.forms.models import model_to_dict
from django.conf import settings

LOGGER = logging.Logger(__name__)


def calSessionProgresss(pid,tid):
    tasks_stats = Task.objects.filter(pid=pid, tid=tid).aggregate(
        total_tasks=Count('pid'),
        completed_tasks=Count('pid', filter=Q(progress__in=['C', 'F']))
    )
    total_tasks_count = tasks_stats['total_tasks']
    completed_tasks_count = tasks_stats['completed_tasks']    
    progress = 0
    if total_tasks_count > 0:
        progress = round(completed_tasks_count/total_tasks_count * 100)
    return progress


def get_sessions_and_tasks(request):
    result = {'status':False, 'msg':'', 'data':[]}
    record_id = request.GET.get("record_id")
    session_id = request.GET.get("session_id")
    if record_id:
        try:
            qs = Subproject.objects.filter(recordid=record_id)[:1]
            subProject = qs[0]
            subproject_data = {
                    'task_description': subProject.projectname,
                    'task_number': subProject.recordid,
                    'contact': subProject.contact,
                    'plan_start': subProject.planbdate,
                    'plan_end': subProject.planedate,
                    'bdate':subProject.bdate,
                    'edate':subProject.edate,
                    'priority':None,
                    'class_field':None,
                    'status': subProject.progress,
                    'inc_id': subProject.inc_id,
                    'progress':0,
                    'show_all_task':False,
                    'data_type':1,
                    'parent': None
            }
            session_data = []
            q = Q(recordid=record_id)
            if session_id: 
                q = q & Q(sessionid=session_id)
            else:
                session_data.append(subproject_data)
            sessions = VTasklistS.objects.filter(q).order_by("planbdate")
            periodStartDate = DateTools.getBeginOfQuarter(DateTools.now())
            periodEndDate = DateTools.getEndOfQuarter(DateTools.now())
            for session in sessions:
                session_info = {
                    'task_description': session.sdesp,
                    'task_number': "{0}-{1}".format(session.pid,int(session.tid)),
                    'contact': session.contact,
                    'plan_start': session.planbdate,
                    'plan_end': session.planedate,
                    'bdate':session.bdate,
                    'edate':session.edate,
                    'priority':None,
                    'class_field':None,
                    'status': session.progress,
                    'inc_id': session.inc_id,
                    'progress':0,
                    'show_all_task':False,
                    'data_type':2,
                    'parent': subProject.recordid if not session.parent else session.parent
                }
                if session_id:
                    session_info['parent'] = None
                #只顯示未完成的Class1和計畫結束日期>=本季度開始日期
                tasks = list(Task.objects.filter(pid=session.pid, tid=session.tid).filter(
                    ((Q(class_field=1) & ~Q(progress__in=['C','F'])) | \
                    (Q(taskcategory='MF', planedate__date__gte=periodStartDate)))).order_by("planbdate"))
                """
                tasks = Task.objects.filter(pid=session.pid, tid=session.tid).filter(
                    (Q(class_field=1) & ~Q(progress__in=['C','F'])) | \
                    (Q(taskcategory__in=['MF'],edate__date__gte=periodStartDate, edate__date__lte=periodEndDate))).order_by("planbdate")
                """
                ##計算Session的進度
                progress = calSessionProgresss(session.pid, session.tid)
                session_info['progress'] = progress
                session_data.append(session_info)
                for task in tasks:
                    task_info = {
                        'task_description': task.task,
                        'task_number': "{0}-{1}-{2}".format(task.pid,int(task.tid),int(task.taskid)),
                        'contact': task.contact,
                        'plan_start': task.planbdate,
                        'plan_end': task.planedate,
                        'bdate':task.bdate,
                        'edate':task.edate,                        
                        'priority':task.priority,
                        'class_field':task.class_field,
                        'status': task.progress,
                        'inc_id': task.inc_id,
                        'progress':0,
                        'show_all_task':False,
                        'data_type':3,
                        'parent': "{0}-{1}".format(session.pid,int(session.tid))
                    }
                    session_data.append(task_info)
            session_data.sort(key=lambda x:(x['data_type'], DateTools.now() if not x['plan_start'] else x['plan_start'],x['task_number']))
            result['status'] = True
            result['data'] = session_data
        except Exception as e:
            LOGGER.error(e)
    else:
        result['status'] = True
    return JsonResponse(result, safe=False)

def getTaskWithSession(request):
    result = {'status':False, 'msg':"", 'data':[]}
    try:
        sessionids = request.POST.get("sessionids");
        isall = request.POST.get("show_all_task", "false") == "true"
        periodStartDate = DateTools.getBeginOfQuarter(DateTools.now())
        periodEndDate = DateTools.getEndOfQuarter(DateTools.now())        
        session_data = []
        sessionProgress = {}
        if sessionids:
            sessions = sessionids.split(",")
            for sessionid in sessions:
                arr = sessionid.split("-")
                if isall:
                    tasks = Task.objects.filter(pid=arr[0], tid=arr[1]).order_by("planbdate")
                else:
                    #只顯示未完成的Class1和計畫結束日期>=本季度開始日期
                    tasks = Task.objects.filter(pid=arr[0], tid=arr[1]).filter(
                        ((Q(class_field=1) & ~Q(progress__in=['C','F'])) | \
                        (Q(taskcategory='MF', planedate__date__gte=periodStartDate)))).order_by("planbdate")                
                tasks = list(tasks)
                progress = calSessionProgresss(arr[0], arr[1])
                sessionProgress[sessionid] = progress
                for task in tasks:
                    task_info = {
                        'task_description': task.task,
                        'task_number': "{0}-{1}-{2}".format(task.pid,int(task.tid),int(task.taskid)),
                        'contact': task.contact,
                        'plan_start': task.planbdate,
                        'plan_end': task.planedate,
                        'bdate':task.bdate,
                        'edate':task.edate,                        
                        'priority':task.priority,
                        'class_field':task.class_field,
                        'status': task.progress,
                        'inc_id': task.inc_id,
                        'progress':0,
                        'show_all_task':isall,
                        'data_type':3,
                        'parent': sessionid
                    }
                    session_data.append(task_info)        
            session_data.sort(key=lambda x:(x['data_type'], DateTools.now() if not x['plan_start'] else x['plan_start'],x['task_number']))
        result['status'] = True
        result['data'] = session_data
        result['sessionProgress'] = sessionProgress
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)

def getMilestoneInfo(request):
    result = {'status':False, 'msg':"", 'data':[]}
    try:
        task_number = request.GET.get("task_number")
        numberArr = task_number.split("-")
        if len(numberArr) == 1:
            recordid = numberArr[0]
        else:
            pid = numberArr[0]
            tid = numberArr[1]
            qs = VTasklistS.objects.values("recordid").filter(pid=pid, tid=tid)[:1]
            if len(qs) > 0:
                recordid = qs[0]['recordid']              
        period = "{0}-{1}".format(DateTools.formatf(DateTools.now(), '%Y'), DateTools.getQuarter(DateTools.now()))
        qs = Goalmanagement.objects.values('contact').filter(period=period, goaltype='Q', recordid=recordid)
        milestone_contact = [item['contact'] for item in qs][0]
        result['status'] = True
        result['data'] = {'recordid':recordid, 'contact':milestone_contact}
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)

def getProjectSummaryId(request):
    result = {'status':False, 'msg':"", 'data':[]}
    try:
        task_number = request.GET.get("task_number")
        qs = Aisummaryrecord.objects.extra(where=["convert(varchar(max),sessionids)=%s"], params=[task_number]).order_by("-createdat")[:1]
        if len(qs) > 0:
            result['status'] = True
            result['data'] = qs[0].inc_id
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)

def getTasks(request):
    result = {'status':False, 'msg':"", 'data':[]}
    try:
        sessions =  json.loads(request.POST.get("sessions","[]"))
        isClassOne = request.POST.get("class1","false") == "true"
        if len(sessions) == 0:
            result['status'] = True
        else:
            qs = VTask.objects.filter(tasklistno__in=sessions)
            if isClassOne:
                qs = qs.filter(class_field=1)
            result['data'] = [model_to_dict(item) for item in qs]
            result['status'] = True
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)

def translate(request):
    result = {'status':False, 'msg':"", 'data':[]}
    try:
        data = json.loads(request.POST.get('data', '[]'))
        fields = json.loads(request.POST.get('fields', '[]'))
        target_language = request.POST.get('target_language', 'English')        
        if not data:
            result['msg']  = 'No data or fields provided'
            return JsonResponse(result, safe=False)
        url = "{0}{1}".format(settings.PMIS_REST_API_SERVER_NEW, settings.PMIS_RESTAPI_ENDPOINT['translate']['url'])
        methodType = settings.PMIS_RESTAPI_ENDPOINT['translate']['method']
        authUserName = settings.PMIS_REST_API_USERNAME
        authPasswrod = settings.PMIS_REST_API_PASSWORD
        params = {"data":data,"fields":fields, "target_language":target_language}
        http_methods = {'data':{"url":url, "method":methodType,"basic_auth_user":authUserName, "basic_auth_password":authPasswrod, "params":params}}
        result = AsyncioTools.async_fetch_http_json(http_methods)['data']
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)
