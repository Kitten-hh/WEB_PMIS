from sqlite3 import DatabaseError
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,JsonResponse
from DataBase_MPMS import models,forms_base
from .. import forms
from django.core.serializers.json import DjangoJSONEncoder
import json
import re
from BaseProject.CustomBaseObject.mixins.CustomMixin import AjaxableResponseMixin
from BaseProject.tools import DateTools
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db import connections,transaction
from datatableview import helpers
from django.db.models import IntegerField,CharField, Value as V
from django.db.models.functions import Cast, Substr
from django.db.models import Sum,Count,Max,Min,Avg,Q
from ..Services.TaskService import TaskService
from ..Services.ProjectService import ProjectService
from ..Services.UserService import UserService
from django.http import HttpRequest,JsonResponse,HttpResponse
from django.conf import settings
import logging
from django.contrib import auth
from django.shortcuts import redirect
from django.forms.models import model_to_dict
auth.signals.user_logged_in.disconnect(auth.models.update_last_login, dispatch_uid='update_last_login')
from django.views.decorators.csrf import csrf_exempt

LOGGER = logging.getLogger(__name__)

def profile(request):
    username = request.GET.get('username')
    result = {
        'teams':UserService.getLocalPartUserCount(),
        'projects':ProjectService.getFixdProjects(username),
        'active_tasks':TaskService.getActiveTaskCount(username),
        'ongoing_tasks':TaskService.getOngoingTaskCount(username),
        'time_spent_projects':TaskService.getProjectsSpent(username),
        'task_spent':TaskService.getTaskSpent(username)
    }    
    return render(request, 'PMIS/looper/user/profile.html', result)



def getAchievement(request):
    try:
        username = request.GET.get('username')
        cur_date = DateTools.datetime.datetime.now()
        start = DateTools.parse(str(cur_date.year) + '0101')
        end = cur_date
        month_str = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        achievement = TaskService.getAchievement(username, start, end)
        for row in achievement:
            month = row['date']
            month = month[4:]
            row['date'] = month_str[int(month)]
        return JsonResponse({'code':0, 'data':achievement})
    except:
        return JsonResponse({'code':1, 'data':[]})
def getUserActivites(reqeust):
    template_name = "PMIS/looper/user/activities.html"
    if reqeust.is_ajax():
        contact = reqeust.GET.get("contact")
        endDate = reqeust.GET.get('endDate')
        ##如果沒有用戶，默認使用sing
        if not contact:
            contact = 'sing'
        if endDate:
            end_date = DateTools.parse(endDate)
        ##第一頁時讀取當前時間以前最後一個日期
        else:
            rs = models.Task.objects.values('planbdate').filter(contact = contact, planbdate__lte =  DateTools.datetime.datetime.now()).order_by('-planbdate')[:1]
            end_date = rs[0]['planbdate']
        start_date = DateTools.addDay(end_date, -3)
        ##查詢數據
        rs = models.VTaskRecordid.objects.filter(contact=contact, planbdate__gte = start_date, planbdate__lte = end_date).\
             extra(where=["tid not like '%%5[257]' and tid not like '%%7[0-4][0-9]' and tid not like '%%3[0-4][0-9]' and \
            tid not like '%%9[0-4][0-9]' and not (Pid = '11580' and (tid ='28' or tid='21'))"]).\
             extra(select={'sessionDesc':'SubProject.ProjectName'}, tables=['SubProject'], where=["V_Task_RecordId.recordid=SubProject.recordid"]).\
             values('contact','task','sessionDesc','planbdate').order_by('-planbdate')
        result = {'code':0}
        result['endDate'] = DateTools.format(start_date)
        result['data'] = list(rs)
        return JsonResponse(result)
    else:
        return render(reqeust, template_name)

def getUserProject(request):
    template_name = 'PMIS/looper/user/projects.html'
    contact = request.GET.get('contact')
    ##如果沒有用戶，默認使用sing
    if not contact:
        contact = 'sing'
    result = UserService.getUserProjects(contact)
    return render(request, template_name, {'data':result})

##############################################################################################
##以上為原來Demo的代碼
##############################################################################################    
def get_all_user_name_list(request):
    '''
    功能描述：獲取用戶名列表
    '''
    result = UserService.GetAllUserNames()
    return JsonResponse({'data':result}, safe=False)

def get_part_user_name_list(request):
    '''
    功能描述：獲取電腦部在職人員列表
    '''
    result = UserService.GetPartUserNames()
    return JsonResponse({'data':result}, safe=False)    

@csrf_exempt
def login(request:HttpRequest):
    '''
    功能描述：用戶登錄
    '''
    result = {'status':False, 'msg':'', 'data':None}
    username = request.POST.get('username')
    password = request.POST.get('password')
    nxt = request.POST.get('next')
    
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        result['status'] = True
        result['data'] = model_to_dict(user)
        result['csrftoken'] = request.META['CSRF_COOKIE']
    if request.is_ajax():
        return JsonResponse(result, safe=False)
    else:
        if result['status']:
            if not nxt:
                return redirect("/looper")
            else:
                return redirect(nxt)
        else:
            if not nxt:
                return redirect("/looper/login_page")
            else:
                return redirect("/looper/login_page?next={0}".format(nxt));
            

def is_login(request:HttpRequest):
    result = {'status':False, 'msg':'', 'data':None}
    try:
        result['status'] = request.user.is_authenticated
    except Exception as e:
        LOGGER.error(e)        
    return JsonResponse(result, safe=False)

def logout(request:HttpRequest):
    '''
    功能描述：用戶登出
    '''
    result = {'status':False, 'msg':'', 'data':None}
    try:
        auth.logout(request)
        result['status'] = True
    except Exception as e:
        LOGGER.error(e)        
    return JsonResponse(result, safe=False)
