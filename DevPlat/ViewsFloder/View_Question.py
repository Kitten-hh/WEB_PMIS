from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,JsonResponse,HttpRequest
from DataBase_MPMS import models,forms_base
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
from PMIS.Services.TaskService import TaskService
from PMIS.Services.UserService import UserService
from BaseApp.library.tools import DateTools
from BaseProject.CustomBaseObject.base_views.CustomView import CustomUpdateView
from BaseProject.CustomBaseObject.mixins.CustomMixin import AjaxableResponseMixin
from django.forms.models import model_to_dict
from BaseApp.library.cust_views.SWCreateView import SWCreateView
from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from django.forms import ModelForm
from BaseApp.library.tools import ModelTools
from ..Services.ForumService import ForumService
from django.conf import settings
from BaseApp.library.decorators.customer_dec import cust_login_required
from django.utils.decorators import method_decorator
from PMISLooper.Services.NtfyNotificationServer import NtfyNotificationService
from PMIS.Services.ElasticService import ElasticService


@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class CreateTaskView(SWCreateView):
    '''
    功能描述：添加任務
    '''
    model = models.Task
    forum_service = ForumService()
    def post(self, request, *args, **kwargs):
        '''
        功能描述:標準django http function view
        當http post 方式訪問該SWCreateView類或它的子類時，調用此方法處理請求
        '''
        result = {'status':False, 'msg':'', 'data':None}
        class Dynamic_Form(ModelForm):
            def validate_unique(self):
                pass
            class Meta:
                model = self.model
                fields = '__all__'
        if self.get_initial_with_session() or self.get_initial_with_default():
            pass
        def mutil_post_data():
            try:
                with transaction.atomic(ModelTools.get_database(self.model)):
                    instance.save()
                    self.save_other(instance)
                return True
            except Exception as e:
                print(str(e))
            return False
        ##複製一份Task內容，處理Task內容超過500個字符時，截取後再保存
        local = request.POST.copy()
        local['task_bak'] = local['task']
        if len(local['task']) > 500:
            local['task'] = local['task'][0:500]
        request.POST = local
        form = Dynamic_Form(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            check_status, check_msg = self.save_check(instance)
            if check_status:            
                self.save_supplement(instance)
                save_qty = 0
                while save_qty < 3:
                    if mutil_post_data() == True:
                        break
                    self.set_max_seqno(instance)
                    save_qty += 1
                ##如果保存3次都沒有成功，則返回保存失敗
                result['status'] = save_qty <= 3
                result['data'] = {'pk':instance.pk, 'instance':model_to_dict(instance)}
            else:
                result['status'] = False
                result['msg'] = {'fail':check_msg}
        else:
            result['status'] = False
            result['msg'] = form.errors
        return JsonResponse(result, safe=False) 
        
    def set_max_seqno(self, instance):
        if instance.pid and instance.tid:
            instance.taskid = TaskService.get_max_taskid(instance.pid, instance.tid)
        else:
            instance.taskid = None
    
    def save_other(self, instance):
        all_task = self.request.POST.get('task_bak')  ##所有提問內容
        instance.task = all_task
        topic_id =  self.forum_service.post_task(instance)
        if topic_id:
            #service  = NtfyNotificationService()
            #service.send_question(model_to_dict(instance), settings.FORUM_SHOW_TOPIC.format(topic_id))
            instance.task = instance.task + '\n' + settings.FORUM_SHOW_TOPIC.format(topic_id)
            if len(instance.task) > 1000:
                instance.task = instance.task[0:1000]
            instance.save()


    def save_supplement(self, instance):
            instance.contact = self.request.POST.get('contact', UserService.GetLoginUserName(self.request))
            instance.progress = 'N'
            if not instance.planbdate:
                instance.planbdate = datetime.date.today()
            if not instance.planedate:
                instance.planedate = datetime.date.today()
            instance.requestdate = datetime.date.today()
            instance.create_date = DateTools.format(DateTools.now());
            instance.modi_date = DateTools.formatf(DateTools.now(), "%Y%m%d%H%M%S")
            instance.creator = UserService.GetLoginUserName(self.request)
            instance.modifier = UserService.GetLoginUserName(self.request)
            instance.udf09 = UserService.GetLoginUserName(self.request)        

    def get_initial_with_default(self):
        qs = models.Syspara.objects.values('fvalue').filter(nfield='QuestionSession', ftype='DevelopmentCycle')
        if len(qs) > 0:
            session_arr = qs[0]['fvalue'].split('-')
            local = self.request.POST.copy()
            local['pid'] = session_arr[0]
            local['tid'] = session_arr[1]
            local['taskid'] = TaskService.get_max_taskid(session_arr[0], session_arr[1])
            self.request.POST = local
            return True;
        else:
            raise Exception("沒有設置Question對應的默認Session")

    def get_initial_with_session(self):
        sessionid = self.request.POST.get("sessionid")
        if sessionid:
            session_arr =  sessionid.split("-")
            local = self.request.POST.copy()
            local['pid'] = session_arr[0]
            local['tid'] = session_arr[1]
            local['taskid'] = TaskService.get_max_taskid(session_arr[0], session_arr[1])
            self.request.POST = local            
            return True
        else:
            return False

def content_search(request):
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        searchValue = request.POST.get("searchValue")
        if searchValue:
            service = ElasticService()
            data = service.fullTextSearchDoc(searchValue)
            if data['hits']['total'] > 0:
                for item in data['hits']['hits']:
                    source = item['_source']
                    result['data'].append({
                        "inc_id":source['IndexId'], 
                        "mb023":source['TechNo'], 
                        "mb004":source['Topic'],
                        "parentid":source['PMindId'],
                        "mb001":"",
                        "mb015c":source['Category'],
                        "mb016":source['Area'],
                        "mb005":source['Contact'],
                        "mb006":source['date'],
                        "mb008":source['Usage']
                        })
            result['status'] = True
    except Exception as e:
        result['status'] = False
        print(str(e))
    return JsonResponse(result, safe=False)