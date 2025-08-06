from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,JsonResponse,HttpRequest, FileResponse
from DataBase_MPMS import models,forms_base
from .. import forms
from django.core.serializers.json import DjangoJSONEncoder
import json
import re, io
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
from BaseProject.tools import DateTools
from BaseProject.CustomBaseObject.base_views.CustomView import CustomUpdateView
from BaseProject.CustomBaseObject.mixins.CustomMixin import AjaxableResponseMixin
from django.forms.models import model_to_dict
from BaseApp.library.cust_views.SWCreateView import SWCreateView
from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from BaseApp.library.cust_views.SWDeleteView import SWDeleteView
from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
from BaseApp.library.decorators.customer_dec import cust_login_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from BaseApp.library.tools import SWTools,AsyncioTools,DateTools as DateToolsUtils
from PMISLooper.Services.NotificationService import NotificationService
from PMISLooper.Services.PmstrService import PmstrService,add_new_task_remind_singal
from PMISLooper.Services.NtfyNotificationServer import send_finish_task_signal,NtfyNotificationService,send_intray_task_signal,send_new_task_instant_signal
from ScheduleApp.Services.ScheduleServer import session_schedule_with_task_signal
from BaseApp.library.tools.PdfTools import convert_to_pdf
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from Authorization_app.permissions.decorators_pmis import has_permission_message, get_users_with_permission_message,has_permission
from SystemBugRpt_app.ViewsFolder.SystemBugRptView import sync_system_bug_signal
from django.conf import settings


class TaskDetailUpdateView(AjaxableResponseMixin, CustomUpdateView):
    model = models.Task
    form_class = forms.TaskR_Simple_Form
    template_name = "PMIS/task_detail.html"
    success_url = 'task/list'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs);
        context['form'].fields['pid'].widget.attrs['readonly'] = True
        context['form'].fields['tid'].widget.attrs['readonly'] = True
        context['form'].fields['taskid'].widget.attrs['readonly'] = True
        return context;
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        response =  CustomUpdateView.get(self,request, *args, **kwargs)
        return response        
    '''
    def dispatch(self, request, *args, **kwargs):
        # Check permissions for the request.user here
        if request.method == 'POST':
            cur_fields = []
            for field in request.POST.keys():
                if getattr(models.Task,field,False):
                    cur_fields.append(field)
            if len(cur_fields) > 0:
                self.fields = cur_fields
            else:
                self.fields = None
        return super().dispatch(request, *args, **kwargs)        
    '''

class TaskDetailCreateView(AjaxableResponseMixin, CreateView):
    '''
        功能描述：添加目標或任務
    '''
    model = models.Task
    form_class = forms_base.Task_Form
    template_name = 'PMIS/task_detail.html'
    success_url = 'task/list'
    def get_max_taskid(self,pid, tid):
        qs = models.Task.objects.values('taskid').filter(Q(pid=pid) & Q(tid=tid)).order_by('-taskid')[:1]
        max_task_id = 10
        if len(qs) > 0:
            max_task_id = qs[0]['taskid']
            max_task_id = max_task_id + 10
        return max_task_id
    def get_initial_with_recordid(self, loc_initial):
        '''
            功能描述：根據appraisal初始化需要新增Quarterly Goal的Pid Tid Taskid
        '''
        #獲取Appraisal
        appraisal_id = self.request.GET.get('appraisal_id')
        goalmaster = models.Goalmaster.objects.values('recordid').filter(pk=appraisal_id)[:1]
        if goalmaster.count() == 0:
            return
        #根據recordid 獲取子工程的查詢條件，並從查詢條件中分析出最小tid和最大tid,用於計算quarterly 的tid
        record_id = goalmaster[0]['recordid']
        subproject = models.Subproject.objects.values('projectid','filter').filter(pk=record_id)[:1]
        if subproject.count() == 0:
            return
        pid = subproject[0]['projectid']
        pfilter = subproject[0]['filter']
        regex_str = r"tid\s*>={0,1}\s*'{0,1}([0-9]+)'{0,1}\s*and\s*tid\s*<={0,1}\s*'{0,1}([0-9]+)'{0,1}"
        matched = re.search(regex_str, pfilter, re.IGNORECASE)        
        if not bool(matched):
            return
        min_tid = matched.group(1)
        max_tid = matched.group(2)
        tid = int(int(min_tid) / 1000) * 1000 + 52
        max_task_id = self.get_max_taskid(pid, tid)
        loc_initial['pid'] = pid
        loc_initial['tid'] = tid
        loc_initial['taskid'] = max_task_id

    def get_initial_with_goal(self, loc_initial):
        '''
            功能描述：根據上級Goal 獲取它下組Goal的初始化pid tid taskid
        '''
        parent_goal  = self.request.GET.get('parent_goal')
        loc_initial['relationgoalid'] = parent_goal
        nos = parent_goal.split('-')
        if len(nos) == 3:
            pid = nos[0]
            tid = nos[1]
            matched = re.search('5[25]$', tid)
            if bool(matched):
                tid = re.sub('55$','57', tid)
                tid = re.sub('52$','55', tid)
                max_task_id = self.get_max_taskid(pid,tid)
                loc_initial['pid'] = pid
                loc_initial['tid'] = tid
                loc_initial['taskid'] = max_task_id
    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        if self.request.method == "GET":
            loc_initial = self.initial.copy()
            if 'parent_goal' in self.request.GET:
                self.get_initial_with_goal(loc_initial)
            if 'appraisal_id' in self.request.GET:
                self.get_initial_with_recordid(loc_initial)
            if "pid" in self.request.GET and 'tid' in self.request.GET:
                pid = self.request.GET.get("pid")
                tid = self.request.GET.get("tid")
                max_task_id = self.get_max_taskid(pid,tid)
                loc_initial['pid'] = pid
                loc_initial['tid'] = tid
                loc_initial['taskid'] = max_task_id
            loc_initial['progress'] = 'N'
            loc_initial['contact'] = 'hb'
            return loc_initial
        else:
            return super().get_initial()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            if 'appraisal_id' in self.request.GET:
                context['appraisal_id'] = self.request.GET.get('appraisal_id')
        return context
    def save_goal_detail(self):
        if 'appraisal_id' in self.request.POST:
            appraisal_id = self.request.POST.get('appraisal_id')
            master = models.Goalmaster.objects.get(pk=appraisal_id)
            if not master and not self.object:
                return
            period = master.period
            contact = master.contact
            recordid = master.recordid
            gtype = master.gtype
            itemno = master.itemno
            max_subitemno = 10
            qs = models.Goaldetail.objects.values('subitemno').filter(Q(period=period) & Q(contact=contact) & Q(recordid=recordid)
                & Q(gtype=gtype) & Q(itemno = itemno)).order_by('-subitemno')[:1]
            if qs.count() > 0:
                max_subitemno = int(qs[0]['subitemno']) + 10
            subitemno = str(max_subitemno).zfill(5)
            pid = self.object.pid            
            tid = self.object.tid
            taskid = self.object.taskid
            desp = self.object.task
            bdate = self.object.planbdate
            edate = self.object.planedate
            goal_detail = models.Goaldetail(period=period, contact=contact,recordid=recordid,gtype=gtype,itemno=itemno,
                subitemno=subitemno, pid=pid,tid=tid,taskid=taskid,desp=desp,bdate=bdate,edate=edate);
            goal_detail.save();

    def form_valid(self, form):
        if 'appraisal_id' in self.request.POST:
            #添加Quarterly Goal時需要添加goal detail，所以需要事務支持
            try:
                #以事務的方式保存數據
                with transaction.atomic('MPMS'):
                    result = super().form_valid(form)
                    self.save_goal_detail()
                    return result
            except Exception as e:
                print(e)
                return super().form_invalid(form)
        else:
            return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        response =  CreateView.get(self,request, *args, **kwargs)
        return response                 

def template_task(request):
    template_name = "PMIS/looper/project/template_task.html"
    contact = request.GET.get("contact")
    if not contact:
        contact = 'sing'
    ##查詢有哪些Template Type時，以當前日期到前一月
    end_date = DateTools.datetime.datetime.now()
    start_date = DateTools.addMonth(end_date, -2)
    mast_ids = []
    result = []
    rs = models.Task.objects.filter(cycletask='Y', contact=contact, planbdate__gte = start_date, planedate__lte = end_date, mastno__isnull=False).annotate(master_id=Cast(Left('mastno', StrIndex('mastno', V('-')) - 1), output_field=CharField())).values('master_id').distinct()
    for row in rs:
        mast_ids.append(row['master_id'])
    if len(mast_ids) == 0:
        return render(request, template_name, {'data':[]})
    else:
        TemplateCategorys = models.Tpmast.objects.filter(tpmastid__in = mast_ids)
        #查詢第一個Category的任務列表
        id = TemplateCategorys[0].tpmastid
        for i, category in  enumerate(TemplateCategorys):
            if i == 0:
                ##查詢單個Template Type以最後一個日期到前三天
                rs = models.Task.objects.filter(cycletask='Y', contact=contact, mastno__isnull=False).annotate(master_id=Cast(Left('mastno', StrIndex('mastno', V('-')) - 1), output_field=CharField())).filter(master_id=id).order_by('-planbdate')[:1]
                end_date = rs[0].planbdate
                start_date = DateTools.addDay(end_date, -3)
                rs = models.Task.objects.filter(cycletask='Y', contact=contact, planbdate__gte = start_date, planedate__lte = end_date, mastno__isnull=False).annotate(master_id=Cast(Left('mastno', StrIndex('mastno', V('-')) - 1), output_field=CharField())).filter(master_id=id)
                result.append({'category':category,'tasks':list(rs)})
            else:
                result.append({'category':category,'task':[]})
    return render(request, template_name, {'data':result})

def template_task_data(request):
    return JsonResponse({})


def general_pk_query(pk):
    q = Q()
    q.connector = "and"
    values = pk.split("-")
    q.children.append(("pid", values[0]))
    q.children.append(("tid", values[1]))
    q.children.append(('taskid', values[2]))
    return q

def del_task(request,pk):
    obj = models.Task.objects.get(pk=pk)
    obj.delete()
    return JsonResponse({})
    
##############################################################################################
##以上為原來Demo的代碼
##############################################################################################
@method_decorator(csrf_exempt, name="dispatch")
#@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class CreateTaskView(SWCreateView):
    '''
    功能描述：添加任務
    '''
    model = models.Task
    def get_initial(self, instance):    
        if self.get_initial_with_session(instance) or \
            self.get_initial_with_appraisal(instance) or \
                self.get_initial_with_default(instance):
            self.set_max_seqno(instance)
            instance.contact = self.request.GET.get('contact', UserService.GetLoginUserName(self.request))
            instance.progress = 'N'
            instance.udf09 = self.request.GET.get('contact', UserService.GetLoginUserName(self.request))
            now_date = datetime.datetime.now()
            instance.planbdate = datetime.datetime(now_date.year, now_date.month, now_date.day)
            instance.planedate = datetime.datetime(now_date.year, now_date.month, now_date.day)
            instance.requestdate = DateToolsUtils.now()
            initTaskCategory = self.request.GET.get("initTaskCategory", "")
            if initTaskCategory:
                instance.taskcategory = initTaskCategory

    def set_max_seqno(self, instance):
        if instance.pid and instance.tid:
            instance.taskid = TaskService.get_max_taskid(instance.pid, instance.tid)
        else:
            instance.taskid = None
    
    def save_other(self, instance):
        appraisal_id = self.request.GET.get("appraisal_id")
        parent_goal = self.request.GET.get("parent_goal")
        ##只有在添加Quarterly goal時，才需要生成對應的goal detail
        if appraisal_id and not parent_goal:
            master = models.Goalmaster.objects.get(pk=appraisal_id)
            period = master.period
            contact = master.contact
            recordid = master.recordid
            gtype = master.gtype
            itemno = master.itemno
            max_subitemno = 10
            qs = models.Goaldetail.objects.values('subitemno').filter(Q(period=period) & Q(contact=contact) & Q(recordid=recordid)
                & Q(gtype=gtype) & Q(itemno = itemno)).order_by('-subitemno')[:1]
            if qs.count() > 0:
                max_subitemno = int(qs[0]['subitemno']) + 10
            subitemno = str(max_subitemno).zfill(5)
            pid = instance.pid            
            tid = instance.tid
            taskid = instance.taskid
            desp = instance.task
            bdate = instance.planbdate
            edate = instance.planedate
            goal_detail = models.Goaldetail(period=period, contact=contact,recordid=recordid,gtype=gtype,itemno=itemno,
                subitemno=subitemno, pid=pid,tid=tid,taskid=taskid,desp=desp,bdate=bdate,edate=edate)
            goal_detail.save()

    def save_check(self, instance):
        #检查是否变更了排期优先级
        if instance.schpriority:
            if not has_permission(self.request.user, "Modify_SchedulePriority", 2):
                return False, "Modify Schedule Priority: {}".format(_("You do not have permission to perform this action."))
        return True,""

    def save_supplement(self, instance):
            if not instance.planbdate:
                instance.planbdate = datetime.date.today()
            if not instance.planedate:
                instance.planedate = datetime.date.today()
            instance.requestdate = DateToolsUtils.now()
            instance.udf09 = UserService.GetLoginUserName(self.request)   

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        try:
            result = json.loads(response.content)
            if result['status']:
                instance = result['data']['instance']
                if instance['progress'] == 'T':
                    service = NotificationService()
                    service.send_todayt_tasks_now(instance)
                if instance['progress'] == 'C':
                    service = NtfyNotificationService()
                    send_finish_task_signal.send(sender=self.__class__, users=service.getManagers(), task=instance)
                if instance['progress'] == 'R':
                    service = NtfyNotificationService()
                    recordid,sessionid = service.get_recordid_sessionid(instance)
                    if has_permission_message(request.user, 'Send_InTray', 1, recordid, sessionid):
                        send_intray_task_signal.send(sender=self.__class__, task=instance)
                service = PmstrService()
                #if instance['contact'] != request.user.username:
                service = NtfyNotificationService()
                recordid,sessionid = service.get_recordid_sessionid(instance)
                if has_permission_message(request.user, 'Send_NewTask', 1, recordid, sessionid):
                    send_new_task_instant_signal.send(sender=self.__class__, task=instance)
                session_schedule_with_task_signal.send(sender=self.__class__, task=instance)
        except Exception as e:
            print(str(e))
        return response

    def get_initial_with_default(self, instance):
        contact = self.request.GET.get('contact', UserService.GetLoginUserName(self.request)) ##登錄人
        default_session = TaskService.get_default_session(contact)
        if default_session:
            instance.pid = default_session.ut002
            instance.tid = default_session.ut003            
            return True
        else:
            return False

    def get_initial_with_session(self, instance):
        sessionid = self.request.GET.get("sessionid")
        if sessionid:
            session_arr =  sessionid.split("-")
            instance.pid = session_arr[0]
            instance.tid = session_arr[1]
            return True
        else:
            return False

    def get_initial_with_appraisal(self, instance:models.Task):
        appraisal_id = self.request.GET.get("appraisal_id")
        parent_goal = self.request.GET.get("parent_goal")
        if appraisal_id:
            ##如果有parent_goal表示添加monthly goal, weekly goal或Task
            if parent_goal:
                nos = parent_goal.split('-')
                if len(nos) == 3:
                    pid = nos[0]
                    tid = nos[1]
                    matched = re.search('5[25]$', tid)
                    if bool(matched):
                        tid = re.sub('55$','57', tid)
                        tid = re.sub('52$','55', tid)
                    else:
                        raise Exception("parent_goal error")
                    instance.pid = pid
                    instance.tid = tid
                    instance.relationgoalid = parent_goal.strip()
                else:
                    raise Exception("parent_goal error")
            ##如果沒有parent_goal表示添加的是quarterly
            else:
                goalmaster = models.Goalmaster.objects.get(pk=appraisal_id)
                #根據recordid 獲取子工程的查詢條件，並從查詢條件中分析出最小tid和最大tid,用於計算quarterly 的tid
                subproject = models.Subproject.objects.filter(recordid=goalmaster.recordid)[:1]
                if len(subproject) == 0:
                    raise Exception("沒有子工程：{0}".format(goalmaster.recordid))
                pid = subproject[0].projectid
                pfilter = subproject[0].filter
                regex_str = r"tid\s*>={0,1}\s*'{0,1}([0-9]+)'{0,1}\s*and\s*tid\s*<={0,1}\s*'{0,1}([0-9]+)'{0,1}"
                matched = re.search(regex_str, pfilter, re.IGNORECASE)        
                if not bool(matched):
                    raise Exception("子工程: {0} 不是標準子工程".format(goalmaster.recordid))
                min_tid = matched.group(1)
                tid = int(int(min_tid) / 1000) * 1000 + 52            
                instance.pid = pid
                instance.tid = tid
            return True
        else:
            return False
@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class UpdateTaskView(SWUpdateView):
    model = models.Task

    def get(self, request, *args, **kwargs):
        response = super().get(request, args, kwargs)
        result = json.loads(response.content)
        try:
            if result['status']:
                instance = result['data']
                #只有登錄人點擊自己的新任務且新任務才更新已讀標記，
                #是否加一個時間判斷是用戶剛加任務時發現描述不對重新修改
                if not instance['r_flag'] and request.user.username == instance['contact']:
                    models.Task.objects.filter(pid=instance['pid'], tid=instance['tid'], taskid=instance['taskid']).update(r_flag=True)
        except Exception as e:
            result['status'] = False
            result['msg'] = "更新已讀標記失敗!"
        return JsonResponse(result, safe=False)
        
    def save_check(self, instance):
        #检查是否变更了排期优先级
        if self.old_instance.schpriority != instance.schpriority:
            if not has_permission(self.request.user, "Modify_SchedulePriority", 2):
                return False, "Modify Schedule Priority: {}".format(_("You do not have permission to perform this action."))
        return True,""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        try:
            result = json.loads(response.content)
            if result['status']:
                instance = result['data']['instance']
                if instance['progress'] == 'T' and getattr(self.old_instance, 'progress') != 'T':
                    service = NotificationService()
                    service.send_todayt_tasks_now(instance)
                if instance['progress'] == 'C' and getattr(self.old_instance, 'progress') != 'C':
                    service = NtfyNotificationService()
                    send_finish_task_signal.send(sender=self.__class__, users=service.getManagers(), task=instance)
                    if self.old_instance.udf01: #有上報單號，則同步任務與上報信息
                        sync_system_bug_signal.send(sender=self.__class__, rp017=self.old_instance.udf01)
                if instance['progress'] == 'R' and getattr(self.old_instance, 'progress') != 'R':
                    service = NtfyNotificationService()
                    recordid,sessionid = service.get_recordid_sessionid(instance)
                    if has_permission_message(request.user, 'Send_InTray', 1, recordid, sessionid):
                        send_intray_task_signal.send(sender=self.__class__, task=instance)
                session_schedule_with_task_signal.send(sender=self.__class__, task=instance, original_task=model_to_dict(self.old_instance))
        except Exception as e:
            print(str(e))
        return response

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class DeleteTaskView(SWDeleteView):
    model = models.Task
    def post(self, request, *args, **kwargs):
        pk = request.GET.get("pk")
        if not pk:
            pk = kwargs['pk']            
        qs = list(self.model.objects.filter(pk=pk))
        response = super().post(request, *args, **kwargs)
        try:
            result = json.loads(response.content)
            if result['status']:
                instance = qs[0]
                session_schedule_with_task_signal.send(sender=self.__class__, task=model_to_dict(instance))
        except Exception as e:
            print(str(e))
        return response    

def add_task(request:HttpRequest):
    '''
    功能描述：添加任務
    '''
    ##當以http get請求時，表示獲取任務默認數據
    result = {'status':False, 'msg':'', 'data':None}
    if request.method == "GET":
        sessionid = request.GET.get("sessionid");
        contact = UserService.GetLoginUserName(request) ##登錄人
        ##初始化Task默認字段
        task = models.Task()
        default_session = TaskService.get_default_session(contact)
        pid = None
        tid = None
        if sessionid and len(sessionid.split("-")) == 2:
            session_arr = sessionid.split("-")
            pid = session_arr[0]
            tid = session_arr[1]
        else:
            default_session = TaskService.get_default_session(contact)
            if default_session:
                pid = default_session.ut002
                tid = default_session.ut003
        if pid:
            task.pid = pid
            task.tid = tid
            task.taskid = TaskService.get_max_taskid(task.pid, task.tid)
            task.contact = contact
            task.progress = 'N'
            now_date = datetime.datetime.now()
            task.planbdate = datetime.datetime(now_date.year, now_date.month, now_date.day)
            task.planedate = datetime.datetime(now_date.year, now_date.month, now_date.day)
            result['data'] = model_to_dict(task)
            result['status'] = True
        else:
            result['status'] = False
            result['msg'] = "用戶{0}沒有默認session".format(contact)
        return JsonResponse(result, safe=False)
    ##保存任務
    else:
        form = forms_base.Task_Form_NoValidate_Unique(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            if not task.planbdate:
                task.planbdate = datetime.date.today()
            if not task.planedate:
                task.planedate = datetime.date.today()
            task.requestdate = datetime.date.today()
            task.udf09 = UserService.GetLoginUserName(request)
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
            
            ##如果保存3次都沒有成功，則返回保存失敗
            result['status'] = save_qty <= 3
            result['data'] = model_to_dict(task)
        else:
            result['status'] = False
            result['msg'] = form.errors
        return JsonResponse(result, safe=False)


def update_task(request:HttpRequest):
    '''
    功能描述：添加任務
    '''
    ##當以http get請求時，表示獲取任務默認數據
    result = {'status':False, 'msg':'', 'data':None}
    if request.method == "GET":
        try:
            old_task = models.Task.objects.get(pk=request.GET.get("pk"))
            result['data'] = model_to_dict(old_task)
            result['status'] = True
        except Exception as e:
            print(str(e))
            result['status'] = False
            result['msg'] = {"error":"task is not exist"}
        return JsonResponse(result, safe=False)
    elif request.method == "POST":
        try:
            old_task = models.Task.objects.get(pid=request.POST.get('pid'),\
                 tid=request.POST.get('tid'),\
                taskid=request.POST.get('taskid'))
        except Exception as e:
            result['status'] = False
            result['msg'] = {"error":"task is not exist"}
            return JsonResponse(result, safe=False)
        form = forms_base.Task_Form(data=request.POST, instance=old_task)
        if form.is_valid():
            try:
                task = form.save(commit=False)
                task.save(update_fields=[key for key,value in form.cleaned_data.items() if value is not None])
                result['status'] = True
                result['data'] = model_to_dict(task)
            except Exception as e:
                print(str(e))
                result['status'] = False
        else:
            result['status'] = False
            result['msg'] = form.errors
        return JsonResponse(result, safe=False)        

def get_task_progresses(request:HttpRequest):
    '''
    功能描述：獲取任務進度列表
    '''
    result = TaskService.get_progress_list()
    return JsonResponse({'data':result}, safe=False)

class TaskTableView(DatatablesServerSideView):
    model = models.VTask
    columns =['taskno','taskid','contact','task','schpriority',
              'pid','tid','planedate','etime','bdate','atime','remark',
              'planbdate','edate','progress','createdate','priority',
              'class_field','process','hoperation','docflag','taskcategory','inc_id','sessionpriority']
    searchable_columns = columns
    def search(self, queryset):
        ##模糊查詢
        if 'search_value' in self.config:
            if self.is_plus_search:
                queryset = self.filter_queryset_multi(self.config['search_value'], queryset)
            else:
                queryset = self.filter_queryset(self.config['search_value'], queryset)
        
        # Add per-column searches where necessary
        filter = Q()
        filter.connector = "and"
        for name, searches in self.config['column_searches'].items():
            search_value = searches['search_value']
            if name == 'progress' and search_value == 'NF':
                queryset = queryset.filter(~Q(progress='NF'))
            else:
                if searches['regex']:
                    filter.children.append(('{0}__icontains'.format(name), search_value))
                else:
                    filter.children.append((name, search_value))

        queryset = queryset.filter(filter)
        ##排序
        if self.config['ordering']:
            queryset = queryset.order_by(*(self.config['ordering']))
        return queryset
    
def sessionTaskDocList(request):
    res = {'status': False, 'msg': '', 'data': []}
    pid = request.GET.get('pid')
    tid = request.GET.get('tid')
    attach = json.loads(request.GET.get('attach', '[]'))
    q = Q()
    q.connector = 'OR'
    q1 = Q()
    docid = str(pid) + str(tid)
    folder_name = str(pid) + '-' + str(tid) + '-'
    q1.children.append(('docid__contains', docid))
    q1.children.append(('foldername__contains', folder_name))
    q.children.append(q1)
    if len(attach) > 0: # 獲取附屬要顯示的session
        for sessionid in attach: 
            q2 = Q()
            d_docid = str(sessionid.split('-')[0]) + str(sessionid.split('-')[1])
            d_folder_name = sessionid + '-'
            q2.children.append(('docid__contains', d_docid))
            q2.children.append(('foldername__contains', d_folder_name))
            q.children.append(q2)

    # 每個任務相同名稱的文件只會取最新上傳的文檔-xmm
    max_folder_ids = models.Document.objects.filter(q).values('foldername', 'docname').annotate(max_date = Max('t_stamp'))
    filter = Q()
    filter.connector = 'OR'
    for folder in max_folder_ids:
        filter_and = Q()
        filter_and.children.append(('foldername', folder.get('foldername')))
        filter_and.children.append(('t_stamp', folder.get('max_date')))
        filter.children.append(filter_and)
    # ------
        
    if filter:
        doc = models.Document.objects.filter(filter)
        res['data'] = list(doc.values())
        res['status'] = True
    return JsonResponse(res, safe=False)

def downloadDocument(request):
    from urllib.parse import quote
    
    inc_id = request.GET.get('inc_id')
    taskfolder = models.Document.objects.filter(inc_id=inc_id)
    if not taskfolder.exists():
        return HttpResponse(status=404)
    taskfolder = taskfolder.values()[0]
    taskimage = models.Docdetail.objects.filter(parentid=taskfolder['parentid'], folderid=taskfolder['folderid']).order_by('folderid').values()[0]

    response = HttpResponse(taskimage['content'], content_type=taskfolder['mediatype'])
    filename = quote(taskfolder['docname'])  # 编码文件名
    response['Content-Disposition'] = f"attachment; filename*=UTF-8''{filename}"
    return response

def previewDocument(request):

    def file_type(file_name: str) -> str:
        parts = file_name.rsplit('.', 1)
        if len(parts) > 1:
            return parts[-1].lower()
        return None

    inc_id = request.GET.get('inc_id')
    taskfolder = models.Document.objects.filter(inc_id=inc_id).first()
    if not taskfolder:
        return HttpResponse(status=404)

    document = models.Docdetail.objects.filter(parentid=taskfolder.parentid, folderid=taskfolder.folderid).first()
    if not document:
        return HttpResponse(status=404)

    file_stream = io.BytesIO(document.content)
    extension = file_type(taskfolder.docname)

    if extension in ['docx', 'xlsx', 'png', 'jpg', 'jpeg', 'gif', 'bmp']:
        pdf_content = convert_to_pdf(file_stream, '.' + extension)
        return HttpResponse(pdf_content, content_type='application/pdf')
    elif extension in ['doc', 'xls']:
        response = FileResponse(file_stream, as_attachment=True, filename=taskfolder.docname)
        return response
    elif extension == 'pdf':
        return HttpResponse(file_stream, content_type='application/pdf')
    else:
        return HttpResponse('Unsupported file type', status=400)

@login_required()
def sendIntantNotif(request):
    result = {"status":False, 'msg':"", 'data':{}}
    taskNo = request.GET.get("taskNo","")
    if taskNo:
        try:
            taskNoArr = taskNo.split("-")
            qs = models.Task.objects.filter(pid=taskNoArr[0], tid=taskNoArr[1], taskid=taskNoArr[2])
            if len(qs) == 0:
                result['msg'] = _("The task {0} does not exist".format(taskNo))
                return JsonResponse(result, safe=False)
            else:
                service = NtfyNotificationService()
                instance = model_to_dict(qs[0])
                taskContact = instance['contact'].strip()
                recordid,sessionid = service.get_recordid_sessionid(instance)
                if has_permission_message(request.user, 'Send_ToDo', 1, recordid, sessionid):
                    service.send_remind_task(request.user.username, instance)
                    result['status'] = True
                else:
                    result['status'] = False
                    result['msg'] = _("You do not have permission to perform this action.")
        except Exception as e:
            print(str(e))    
    else:
        result['msg'] = _("The input parameter is incorrect!")
    return JsonResponse(result, safe=False)

def add_otheruser_relation_task(requset):
    """
    功能描述: 將原有Task的信息複製一份出來生成一個新Task(除了聯繫人不同),這兩個任務互相關聯
    參數: 
        taskno: 要生成關聯任務的taskno
        relation_user: 新任務的聯繫人
    注意: 必須是已存在的任務才能生成新任務
    """
    try:
        taskno = requset.POST.get('taskno', '')
        relation_user = requset.POST.get('relation_user', '')
        pid, tid, taskid = taskno.split('-')
        task_qs = models.Task.objects.filter(pid=pid, tid=tid, taskid=taskid) # 查出原Task
        taskid_max = models.Task.objects.filter(pid=pid, tid=tid).aggregate(taskid_max = Max('taskid'))['taskid_max'] + 10
        if task_qs.exists():
            relation_task = task_qs.first() # 將任務信息複製一份
            relation_task.inc_id = None
            relation_task.contact = relation_user # 聯繫人
            relation_task.relationid = taskno # 關聯任務
            relation_task.taskid = taskid_max # 任務編號
            relation_task.save()
        update_dict = {'relationid' : f'{relation_task.pid}-{int(relation_task.tid)}-{int(relation_task.taskid)}'} # 拼接關聯任務編號
        models.Task.objects.filter(pid=pid, tid=tid, taskid=taskid).update(**update_dict) # 更新原任務的關聯任務
    except Exception as e:
        print(e)
        return JsonResponse({'status': False, 'data' : ''})
    return JsonResponse({'status': True, 'data' : f'{relation_task.pid}-{int(relation_task.tid)}-{int(relation_task.taskid)}'}) # 返回關聯任務
    

@login_required()
def approveRequest(request):
    result = {"status":False, 'msg':"", 'data':{}}
    inc_id = request.POST.get("task_inc_id")
    approver = request.POST.get("approver")
    approveContent = request.POST.get("approveContent")
    if inc_id and approver and approveContent:
        try:
            params = {"approver":approver, "taskdescription":approveContent}
            url = settings.PMIS_RESTAPI_ENDPOINT['task_request_approve']['url']
            url = url.format(inc_id)
            url = "{0}{1}".format(settings.PMIS_REST_API_SERVER_NEW, url)
            methodType = settings.PMIS_RESTAPI_ENDPOINT['task_request_approve']['method']
            authUserName = settings.PMIS_REST_API_USERNAME
            authPasswrod = settings.PMIS_REST_API_PASSWORD
            http_methods = {'data':{"url":url, "method":methodType,"basic_auth_user":authUserName, "basic_auth_password":authPasswrod, "params":params}}
            result = AsyncioTools.async_fetch_http_json(http_methods)['data']
        except Exception as e:
            print(str(e))    
    return JsonResponse(result, safe=False)
