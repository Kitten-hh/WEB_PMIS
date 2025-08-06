from BaseApp.library.cust_views.SWCreateView import SWCreateView
from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from BaseApp.library.cust_views.SWDeleteView import SWDeleteView
from DataBase_MPMS import models
from BaseApp.library.decorators.customer_dec import cust_login_required
from django.utils.decorators import method_decorator
from BaseApp.library.tools import DateTools,ModelTools
import logging
from django.http import JsonResponse,HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum,Count,Max,Min,Avg,Q
from django.db import transaction
import json
from django.shortcuts import render,redirect
from PMIS.Services.UserService import UserService
from PMISLooper.Services.NtfyNotificationServer import NtfyNotificationService
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.conf import settings

LOGGER = logging.getLogger(__name__)

def pmstr_save_check(self, instance):
    istr024 = self.request.POST.get("istr024", "false") == "true"
    tr024h = self.request.POST.get("tr024h", "0")
    tr024m = self.request.POST.get("tr024m","0")
    instance.tr024 = 0
    if istr024:
        if int(tr024h) == 0 and  int(tr024m) == 0:
            #If repeat is true, setting the repeat cycle is necessary.
            return False, _("repeat cycle valid.")
        if tr024m:
            instance.tr024 += int(tr024m)
        if tr024h:
            instance.tr024 += int(tr024h) * 60
    if instance.tr028 == "1" and not instance.tr021:
        return False, _("Please set the reminder start date.")
    if instance.tr030 == "1" and not instance.tr022:
        return False, _("Please set the reminder end date.")
    if not instance.tr004:
        return False, _("The reminder start time cannot be empty.")
    if not instance.tr005:
        return False, _("The reminder end time cannot be empty.")
    if  DateTools.formatf(instance.tr004,'%H:%M') >= DateTools.formatf(instance.tr005,'%H:%M'):
        return False, _("The reminder start time must less end time.")
    if instance.tr028 == "1" and instance.tr030 == "1" and DateTools.format(instance.tr021) > DateTools.format(instance.tr022):
        #The reminder start date must less than or equal to end date.
        return False, _("reminder date valid.")
    return True,""

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class CreatePmstrView(SWCreateView):
    model = models.Pmstr

    def get_initial(self, instance):
        self.set_max_seqno(instance)
        taskno = self.request.GET.get("taskno")
        if taskno:
            tasknoArr = taskno.split("-")
            qs = models.Task.objects.filter(pid=tasknoArr[0], tid = tasknoArr[1], taskid = tasknoArr[2])
            if len(qs) > 0:
                task = qs[0]
                instance.tr003 = task.progress
                instance.tr004 = DateTools.now().replace(hour=8, minute=0)
                instance.tr005 = DateTools.now().replace(hour=17, minute=0)
                instance.tr006 = task.contact
                instance.tr007 = 'N' #默認為等待發送
                instance.tr011 = '1,2,3,4,5,6' #星期設置
                instance.tr024 = 0 #循環周期數， 按分鐘記
                instance.tr027 = 'Y' #發送消息
                instance.tr028 = "2" #提醒開始，默認為：開始於計畫開始前
                instance.tr029 = 0 #默認為0天前
                instance.tr030 = "2" #提醒結束，默認為:結束於任務C和F
            instance.tr002 = taskno
        else:
            raise Exception("parameter is fail")

    def set_max_seqno(self, instance):
        qs = models.Pmstr.objects.all().order_by('-tr001')[:1]
        if len(qs) > 0:
            instance.tr001 = qs[0].tr001 + 1
        else:
            instance.tr001 = 1

    def save_check(self, instance):
        return pmstr_save_check(self, instance)

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class UpdatePmstrView(SWUpdateView):
    model = models.Pmstr
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        result = json.loads(response.content)
        try:
            if result['status']:
                instance = result['data']
                #如果任務的聯繫人更改了則修改tr006
                tasknoArr = instance['tr002'].split("-")
                qs = models.Task.objects.values("contact").filter(pid=tasknoArr[0], tid=tasknoArr[1], taskid = tasknoArr[2])
                if len(qs) > 0 and instance['tr006'] != qs[0]['contact']:
                    instance['tr006'] = qs[0]['contact']
        except Exception as e:
            pass
        return JsonResponse(result, safe=False)    
    def save_check(self, instance):
        return pmstr_save_check(self, instance)


@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class DeletePmstrView(SWDeleteView):
    model = models.Pmstr

def getPmstrWithTask(request):
    result = {'status':False, 'msg':"", 'data':''}
    try:
        taskno = request.GET.get("taskno","")
        if taskno:
            qs = models.Pmstr.objects.filter(tr002=taskno)[:1]
            if len(qs) > 0:
                result['data'] = qs[0].inc_id
            result['status'] = True
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)


@csrf_exempt
def userKnow(request):
    message = _("Setup Successful!")
    try:
        taskno = request.GET.get('taskno')
        if request.method == "POST":
            taskno = request.POST.get('taskno')
        if taskno:
            with transaction.atomic(ModelTools.get_database(models.Pmstr)):            
                models.Pmstr.objects.filter(tr002=taskno, tr030="3").update(tr007="F",tr031=DateTools.now())  #用戶點擊I Konw就結束提醒的任務
                models.Pmstr.objects.filter(tr002=taskno).filter(~Q(tr030="3")).update(tr031=DateTools.now())  #脫期的任務用戶點擊I Know後當天再發送給用戶,這裏記錄用戶點擊的日期
    except Exception as e:
        message = _("Setup failed")
        print(str(e))
    return render(request, 'PMISLooper/user/ntfy_know.html', {'message':message})

@csrf_exempt
@login_required()
def assignTask(request):
    pageUrl = 'PMISLooper/user/assignTask.html'
    
    default_values = {
        'users': [],
        'contact': '',
        'priority': '',
        'class_field': '',
        'task': '',
        'taskno': '',
        'message': '',
        'has_error': False
    }
    
    users = UserService.GetPartUserNames()
    if request.method == "GET":
        try:
            taskno = request.GET.get('taskno')
            tasknoArr = taskno.split("-")
            qs = models.Task.objects.filter(pid=tasknoArr[0], tid=tasknoArr[1], taskid=tasknoArr[2])
            if len(qs) > 0:
                if qs[0].contact and qs[0].contact in users:
                    return render(request, pageUrl, {**default_values, 'message':_('The task has been assigned to ') + qs[0].contact, 'users': users, 'contact': qs[0].contact, 'priority': qs[0].priority, 'class_field': qs[0].class_field, 'task': qs[0].task, 'taskno': taskno})
                return render(request, pageUrl, {**default_values, 'users': users, 'task': qs[0].task, 'taskno': taskno})
            else:
                return render(request, pageUrl, {**default_values, 'message': _("This task does not exist"), 'has_error': True})
        except Exception as e:
            LOGGER.error(e)
            return render(request, pageUrl, {**default_values, 'message': _("Search data fail!"), 'has_error': True})
    elif request.method == "POST":
        try:
            taskno = request.POST.get("taskno")
            contact = request.POST.get("contact")
            priority = None if not request.POST.get("priority") else int(request.POST.get("priority"))
            class_field = None if not request.POST.get("class_field") else int(request.POST.get("class_field"))
            tasknoArr = taskno.split("-")
            qs = models.Task.objects.filter(pid=tasknoArr[0], tid=tasknoArr[1], taskid=tasknoArr[2])
            if len(qs) > 0:
                task = qs[0]
                task.contact = contact
                task.priority = priority
                task.class_field = class_field
                server = NtfyNotificationService()
                server.send_assign_task(request.user.username, model_to_dict(task))
                models.Task.objects.filter(pid=tasknoArr[0], tid=tasknoArr[1], taskid=tasknoArr[2]).update(contact=contact, priority=priority, class_field=class_field)
                return render(request, pageUrl, {**default_values, 'message': _("Assign Successful!"), 'users': users, 'contact': contact, 'priority': task.priority, 'class_field': task.class_field, 'task': task.task, 'taskno': taskno})
            else:
                return render(request, pageUrl, {**default_values, 'message': _("This task does not exist"), 'users': users, 'has_error': True})
        except Exception as e:
            LOGGER.error(e)
            if task:
                return render(request, pageUrl, {**default_values, 'message': _("Assign failed"), 'users': users, 'contact': contact, 'priority': task.priority, 'class_field': task.class_field, 'task': task.task, 'taskno': taskno})
            else:
                return render(request, pageUrl, {**default_values, 'message': _("Assign failed"), 'users': users, 'has_error': True})
    else:
        return render(request, pageUrl, {**default_values, 'message': _("Illegal access"), 'users': users, 'has_error': True})
