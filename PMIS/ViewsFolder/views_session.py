from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,JsonResponse,HttpRequest, request
from DataBase_MPMS import models,forms_base
from .. import forms
from django.core.serializers.json import DjangoJSONEncoder
import json
import re
import datetime
from django.db.models.functions import Cast, Substr
from django.db.models import Sum,Count,Max,Min,Avg,Q, query
from django.db.models import IntegerField
from django.db.models.functions import Left,StrIndex,Right
from BaseProject.tools import DateTools
from django.forms.models import model_to_dict
from DataBase_MPMS import models
from ..Services.SessionService import SessionService
from BaseApp.library.cust_views.SWCreateView import SWCreateView
from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ProjectManagement_app.models import TasklistRelation


def session_list(request:HttpRequest):
    '''
    功能描述：獲取用戶Default Dialy Pattern
    '''
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        contact=request.GET.get("contact")
        recordid=request.GET.get("recordid")
        period=request.GET.get('period')
        allcontact=request.GET.get("allcontact")
        stype=request.GET.get("stype")
        desc=request.GET.get("desc")
        list = SessionService.search_sessioni(contact=contact, recordid=recordid, period=period, allcontact=allcontact, stype=stype, desc=desc)
        result['status'] = True
        result['data'] =  list
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)    

def search_task_with_session(request:HttpRequest):
    '''
    功能描述：根據Session查詢任務，要求
    '''
    result = {'status':False, 'msg':'', 'data':None}    
    try:
        pid = request.GET.get("pid")
        tid = request.GET.get("tid")
        count = request.GET.get("count")
        params = {'progress_or':request.GET.get("progress_or" ,""), \
                  'taskcategory_or':request.GET.get("taskcategory_or" ,""),\
                  'class_one':request.GET.get("class_one","false") == "true",
                  'progress_nf':request.GET.get("progress_nf", "false") == "true",
                  'progress_ncf':request.GET.get("progress_ncf", "false") == "true",
                  'session_filter':request.GET.get("session_filter","true") == "true"}
        if not pid or not tid:
            result['status'] = False
            result['msg'] = "沒有這個Session"
        else:
            
            if count:
                contact = request.GET.get("contact")
                tasks = SessionService.search_task_with_session(pid,tid,contact, params=params)
                result['data'] = [model_to_dict(task) for task in tasks[:int(count)]]    
            else:
                tasks = SessionService.search_task_with_session(pid,tid, params=params)
                result['data'] = [model_to_dict(task) for task in tasks]
            result['status'] = True
    except Exception as e:
        print(str(e))
        result['status'] = False
        result['msg'] = '服務器錯誤'
    return JsonResponse(result, safe=False)

def session_sessionList(request:HttpRequest):
    '''
    功能描述：獲取SessionList
    '''
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        contact=request.GET.get("contact")
        pid=request.GET.get('pid')
        recordid=request.GET.get("recordid")
        desc=request.GET.get("desc")
        list = SessionService.get_session_list(contact=contact, pid=pid, recordid=recordid, desc=desc)
        result['status'] = True
        result['data'] =  list
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)    



@method_decorator(csrf_exempt, name="dispatch")
class CreateSessionView(SWCreateView):
    
    '''
    功能描述:添加Session
    '''
    model = models.Tasklist
    def get_initial(self, instance):        
        self.set_max_seqno(instance)

    def set_max_seqno(self, instance):
        request = self.request.GET
        if self.request.method == 'POST':
            request = self.request.POST
        recordid = request.get("recordid")
        type = request.get("type")
        pid,min_tid,max_tid = SessionService.get_session_range(recordid)
        if pid and (min_tid or min_tid == 0) and max_tid:
            if self.request.method == 'GET':
                instance.pid = pid
            tid = SessionService.get_max_tid(pid, min_tid, max_tid, type)
            if tid:
                instance.tid = tid
            else:
                raise Exception("Session已經使用完，不能再添加")
        else:
            raise Exception("recordid 不正確")

class UpdateSessionView(SWUpdateView):
    '''
    功能描述:更新session
    '''
    model = models.Tasklist

    def get_object_with_params(self, request_data):
        pid = request_data.get("pid")
        tid = request_data.get("tid")
        return models.Tasklist.objects.filter(pid=pid, tid=tid)[:1][0] 

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        result = json.loads(response.content)
        try:
            if result['status']:
                instance = result['data']
                #如果任務的聯繫人更改了則修改tr006
                pid = instance['pid']
                tid = instance['tid']
                qs = TasklistRelation.objects.values("relationsessionid",'relationtype','status').filter(pid=pid, tid=tid)[:1]
                instance['relationsessionid'] = None if len(qs) == 0 else qs[0]['relationsessionid']
                instance['relationtype'] = None if len(qs) == 0 else qs[0]['relationtype']
                instance['relationstatus'] = None if len(qs) == 0 else qs[0]['status']
        except Exception as e:
            pass
        return JsonResponse(result, safe=False)            
    
    def save_other(self, instance):
        '''
        功能描述：保存與該model相關的其他model數據
        參數說明:
            instance:本model實例
        '''
        if 'relationsessionid' in self.request.POST:
            relationsessionid = self.request.POST.get("relationsessionid")
            relationstatus = self.request.POST.get("relationstatus","I")
            if relationsessionid: #有值就更新或新增
                TasklistRelation.objects.update_or_create(pid=instance.pid, tid = instance.tid, 
                defaults={"relationsessionid":relationsessionid, "status":relationstatus, "relationtype":"S"})
            else: #沒值則刪除
                TasklistRelation.objects.filter(pid=instance.pid, tid=instance.tid).delete()
    
class SessionListView(DatatablesServerSideView):
    model = models.VTasklistS
    columns = ['recordid','sessionid','sdesp']
    searchable_columns = columns
    def get_initial_queryset(self):
        recordid = self.request.GET.get("recordid");
        session_category = self.request.GET.get("category")
        queryset = self.model.objects.all()
        if recordid:
            queryset = queryset.filter(recordid = recordid)
        if session_category:
            if session_category == '1':
                # queryset = queryset.annotate(right_tid=Right(Cast('tid', output_field=IntegerField()), 3)).\
                #     filter((~Q(pid='00500') & Q(right_tid__lt=100)) | (Q(pid='00500') & Q(right_tid__lt=200)))
                queryset = queryset.filter(progress='I')
        return queryset

class SessionTableView(DatatablesServerSideView):
    model = models.VTasklist
    columns = "__all__"
    searchable_columns = columns










