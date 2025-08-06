from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,JsonResponse
from django.db.models import Sum,Count,Max,Min,Avg,Q
from DataBase_MPMS.models import Task,ADMRP,Goalmaster,VGoalmaster,Task,VTask
from . import forms
from . forms import TaskForm,SystemBugForm,GoalmasterForm,VGoalmaster_d1_Form
from .ViewsFolder import views_goalmaster
from django.db import connection
from datatableview import Datatable
from datatableview.datatables import DatatableOptions
from datatableview.views import MultipleDatatableView
from datatableview.views.legacy import LegacyDatatableView
from datatableview import helpers
from BaseProject.tools import DateTools
from .Services.TaskService import TaskService
from .Services.ProjectService import ProjectService
from .Services.UserService import UserService
import json
import random
import itertools
# Create your views here.

class TemplateIterator(itertools.count):
    def current(self):
        return int(repr(self)[17:-1])
    def next(self):
        next(self)
        return int(repr(self)[17:-1])        


def index(request): 
    template = loader.get_template('PMIS/index.html')
    context = None
    return HttpResponse(template.render(context,request))

def PMIS(request): 
    template = loader.get_template('PMIS/PMIS.html')
    context = None
    return HttpResponse(template.render(context,request))
    #return HttpResponse("<h2>This is nice</h2>")
    #return HttpResponse(html)

def todo_task(request): 
    all_Task = Task.objects.all()
    template = loader.get_template('PMIS/todo_task.html')
    #context = None
    context = {
        'all_Task': all_Task,
    }
    return HttpResponse(template.render(context,request))


def Starter_page(request): 
    template = loader.get_template('PMIS/Starter_page.html')
    context = None
    return HttpResponse(template.render(context,request))

def Adminux_base(request): 
    all_Task = Task.objects.all()
    template = loader.get_template('PMIS/Adminux_base.html')
    context = {
        'all_Task': all_Task,
    }
    return HttpResponse(template.render(context,request))

def PMIS_bak(request): 
    template = loader.get_template('PMIS/PMIS_bak.html')
    context = None
    return HttpResponse(template.render(context,request))

def Trial(request): 
    template = loader.get_template('PMIS/Trial.html')
    context = None
    return HttpResponse(template.render(context,request))

def contextmenu(request): 
    template = loader.get_template('PMIS/contextmenu.html')
    context = None
    return HttpResponse(template.render(context,request))

def Test_Appearance(request): 
    template = loader.get_template('PMIS/Test_Appearance.html')
    context = None
    return HttpResponse(template.render(context,request))

def Staff_Dashboard(request): 
    template = loader.get_template('PMIS/Staff_Dashboard.html')
    context = None
    return HttpResponse(template.render(context,request))

'''
#@login_required(login_url="/PMIS/login/")
def task_create(request): 
    if request.method == 'POST':
        form = forms.CreateTask(request.POST)  #(request.POST,request.FILES) if we have upload file
        if form.is_valid():
            #save task to db
            print('Saving')
            #return redirect('PMIS:task_create.html')
            return HttpResponse(html)
    else:
        form = forms.CreateTask()
    return render(request,'PMIS/task_create.html',{'form':form})
'''


def task_create(request): 
    if request.method == 'POST': 
        form = forms.TaskForm(request.POST)
        if form.is_valid():
            print('Valid')
            Pid = form.cleaned_data['Pid']
            Tid = form.cleaned_data['Tid']
            TaskID = form.cleaned_data['TaskID']
            Taskdesp = form.cleaned_data['Task']
            Contact = form.cleaned_data['contact']
            PlanBDate = form.cleaned_data['PlanBDate']
            Class = form.cleaned_data['Class']
            Remark = form.cleaned_data['Remark']
            Progress = form.cleaned_data['Progress']

            print (Pid + ' - ' + Taskdesp)
            a = Task(Pid=Pid,Tid=Tid,TaskID=TaskID,Task=Taskdesp,contact=Contact,PlanBDate=PlanBDate,Class=Class,Remark=Remark,Progress=Progress)
            #a = Task(Pid=Pid,Tid=Tid,TaskID=TaskID,Task=Taskdesp,contact=Contact,PlanBDate=PlanBDate,Progress='N')
            #a = Task(Pid=Pid,Tid=Tid,TaskID=TaskID,Task=Taskdesp,Progress='N')
            a.save() 
        else:
            print('Something wrong with the form')
    form = forms.TaskForm()
    return render(request,'PMIS/task_create.html',{'form':form})

def task_search():
    print('This is call by pressing the search button in task page')


def srh(request):
    #sh
    search_context = request.GET['srh_txt']
    print("The search is " + search_context)
    '''
    Task.objects.all()
    Desp = Task.objects.filter(Task__startswith='Check').first()
    Desp = Task.objects.filter(Task__startswith='Check')
    Desp = Task.objects.filter(Task__icontains='Check').first()
    Desp = Task.objects.filter(Task__icontains='Check')
    template = loader.get_template('PMIS/Multi_task.html')
    '''
    All_Task = Task.objects.filter(Task__icontains=search_context)
    No = Task.objects.filter(Task__icontains=search_context).count()
    if No == 0 :
        print('Not Found The count is ' + str(No))
    if No == 1 :
        template = loader.get_template('PMIS/Single_task.html')
        print('Only one record found ' + str(No))
        context = {
            'All_Task': All_Task,
        }
        return HttpResponse(template.render(context,request))
        '''
        res=All_Task.first().Task
        print(All_Task.first().Task)
        return render(request,"PMIS/Single_task.html",{'result':res})    
        '''
    else:
        template = loader.get_template('PMIS/Multi_task.html')
        print('The count is ' + str(No))
        context = {
            'All_Task': All_Task,
        }
        return HttpResponse(template.render(context,request))

    return render(request,"PMIS/Single_task.html",{'result':res})    
def system_bug_create(request): 
    if request.method == 'POST': 
        form = forms.SystemBugForm(request.POST)
        if form.is_valid():
            print('Valid')
            RP001 = form.cleaned_data['RP001']
            RP002 = form.cleaned_data['RP002']
            RP003 = form.cleaned_data['RP003']
            RP004 = form.cleaned_data['RP004']
            RP005 = form.cleaned_data['RP005']
            RP006 = form.cleaned_data['RP006']
            RP007 = form.cleaned_data['RP007']
            RP008 = form.cleaned_data['RP008']
            RP009 = form.cleaned_data['RP009']
            RP010 = form.cleaned_data['RP010']
            RP011 = form.cleaned_data['RP011']
            RP012 = form.cleaned_data['RP012']
            RP013 = form.cleaned_data['RP013']
            RP014 = form.cleaned_data['RP014']
            RP015 = form.cleaned_data['RP015']
            RP016 = form.cleaned_data['RP016']
            RP017 = form.cleaned_data['RP017']
            RP018 = form.cleaned_data['RP018']
            RP019 = form.cleaned_data['RP019']
            RP020 = form.cleaned_data['RP020']
            RP021 = form.cleaned_data['RP021']
            RP022 = form.cleaned_data['RP022']
            RP023 = form.cleaned_data['RP023']
            RP024 = form.cleaned_data['RP024']
            RP025 = form.cleaned_data['RP025']
            RP026 = form.cleaned_data['RP026']
            RP027 = form.cleaned_data['RP027']
            RP028 = form.cleaned_data['RP028']
            RP029 = form.cleaned_data['RP029']
            RP030 = form.cleaned_data['RP030']
            RP031 = form.cleaned_data['RP031']
            RP032 = form.cleaned_data['RP032']
            RP033 = form.cleaned_data['RP033']
            RP034 = form.cleaned_data['RP034']
            RP035 = form.cleaned_data['RP035']
            RP036 = form.cleaned_data['RP036']
            RP037 = form.cleaned_data['RP037']
            RP038 = form.cleaned_data['RP038']
            RP039 = form.cleaned_data['RP039']
            RP040 = form.cleaned_data['RP040']
            RP041 = form.cleaned_data['RP041']

            print (RP016 + ' - ' + RP017 + '-' + RP005)
            a = ADMRP(RP001=RP001,RP002=RP002,RP003=RP003,RP004=RP004,RP005=RP005,RP006=RP006,RP007=RP007,RP008=RP008,RP009=RP009,RP010=RP010,
                      RP011=RP011,RP012=RP012,RP013=RP013,RP014=RP014,RP015=RP015,RP016=RP016,RP017=RP017,RP018=RP018,RP019=RP019,RP020=RP020,
                      RP021=RP021,RP022=RP022,RP023=RP023,RP024=RP024,RP025=RP025,RP026=RP026,RP027=RP027,RP028=RP028,RP029=RP029,RP030=RP030,
                      RP031=RP031,RP032=RP032,RP033=RP033,RP034=RP034,RP035=RP035,RP036=RP036,RP037=RP037,RP038=RP038,RP039=RP039,RP040=RP040,
                      RP041=RP041)
            a.save()
        else:
            print('Something wrong with the form')
            print(form.errors)
    form = forms.SystemBugForm()
    form.fields['RP016'].initial = 'XY'
    #form.RP016 = 'XY'
    qs = ADMRP.objects.values('RP017').filter(RP016 = 'XY').order_by('-RP017')[:1]
    if qs.count() > 0:
        form.RP017 = qs[0]['RP017']
    return render(request,'PMIS/system_bug_create.html',{'form':form})
def display_system_bug(request): 
    #查看所有數據
    allSystemBug = ADMRP.objects.all()
    form = forms.SystemBugForm()
    return render(request, "PMIS/display_system_bug.html",{'datas':allSystemBug,'form':form})

def test_customer_filter(request):
    class User:
        name = 'test'
    user = User()
    return render(request, 'PMIS/test_customer_filter.html', {'user':user})

def create_goal_master(request):
    if request.method == 'POST':
        form = GoalmasterForm(request.POST)
        if form.is_valid():
            print('valid')
            company = form.cleaned_data['company']
            creator = form.cleaned_data['creator']
            usr_group = form.cleaned_data['usr_group']
            create_date = form.cleaned_data['create_date']
            modifier = form.cleaned_data['modifier']
            modi_date = form.cleaned_data['modi_date']
            flag = form.cleaned_data['flag']
            period = form.cleaned_data['period']
            contact = form.cleaned_data['contact']
            recordid = form.cleaned_data['recordid']
            gtype = form.cleaned_data['gtype']
            itemno = form.cleaned_data['itemno']
            objective = form.cleaned_data['objective']
            bdate = form.cleaned_data['bdate']
            edate = form.cleaned_data['edate']
            project = form.cleaned_data['project']
            desp = form.cleaned_data['desp']
            escore = form.cleaned_data['escore']
            ascore = form.cleaned_data['ascore']
            management = form.cleaned_data['management']
            performance = form.cleaned_data['performance']
            comment = form.cleaned_data['comment']
            manday = form.cleaned_data['manday']
            difficulty = form.cleaned_data['difficulty']
            a = Goalmaster(company=company,creator=creator,usr_group=usr_group,create_date=create_date,modifier=modifier,modi_date=modi_date,flag=flag,
            period=period,contact=contact,recordid=recordid,gtype=gtype,itemno=itemno,objective=objective,bdate=bdate,edate=edate,project=project,desp=desp,
            escore=escore,ascore=ascore,management=management,performance=performance,comment=comment,manday=manday,difficulty=difficulty)
            a.save()
        else:
            print('this is some error')
            print(form.errors)
    form = GoalmasterForm()
    return render(request, 'PMIS/create_goal_master.html', {'form':form})

def goal_master_form(request):
    form = VGoalmaster_d1_Form()
    qs = VGoalmaster.objects.values(*(form._meta.fields)).filter(Q(period = '2020-1') & Q(contact = 'sing'))
    print(qs.query)
    taskform = TaskTForm()
    return render(request, 'PMIS/goal_master_form.html', {'datas':list(qs),'form':form}) 

class TaskTableView(LegacyDatatableView):
    model = Task
    datatable_options = {
        'structure_template': "datatableview/bootstrap_structure.html",
        'columns': [
            ('工程編號', 'pid'),
            ('類別編號', 'tid'),
            ('任務編號', 'taskid'),
            ('任務描述', 'task'),
            ('聯繫人', 'contact'),
            ('進度', 'progress'),
            ('計畫開始', 'planbdate', helpers.format_date("%Y-%m-%d")),
            ('計畫結束', 'planedate', helpers.format_date("%Y-%m-%d")),
            ('實際開始', 'bdate', helpers.format_date("%Y-%m-%d")),
            ('實際結束', 'edate', helpers.format_date("%Y-%m-%d")),
            ('備註', 'remark'),
        ],
    }
    paginate_by = 25
    template_name = 'PMIS/task_list.html'

class MultiTableView(MultipleDatatableView):
    class datatable_task(Datatable):
        class Meta:
            model = forms.TaskR_S_Form.Meta.model
            columns = forms.TaskR_S_Form.Meta.fields
            labels = forms.TaskR_S_Form.Meta.labels
    class datatable_goal_master(Datatable):
        class Meta:
            model = forms.VGoalmaster_d1_Form.Meta.model
            columns = forms.VGoalmaster_d1_Form.Meta.fields
            labels = forms.VGoalmaster_d1_Form.Meta.labels
            processors = {
                "bdate": helpers.format_date("%Y-%m-%d"),
                'edate': helpers.format_date("%Y-%m-%d"),
                'pschedule': helpers.format("{0:.2f}"),
                'aschedule': helpers.format("{0:.2f}")
            }
    datatable_classes = {
        'demo1': datatable_task,
        'demo2': datatable_task,
        'demo3': datatable_goal_master,
    }    

    def get_demo1_datatable_queryset(self):
        return Task.objects.all()

    def get_demo2_datatable_queryset(self):
        return Task.objects.all()

    def get_demo3_datatable_queryset(self):
        return Goalmaster.objects.all()

    def get_datatables(self, only=None):
        datatables = super(MultipleDatatableView, self).get_datatables(only)
        if only in (None, 'demo2'):
            demo2 = datatables['demo2']
            del demo2.columns['pid']
        return datatables
    paginate_by = 25    
    template_name = 'PMIS/multi_table.html'


class AjaxableResponseMixin(object):
    """ Ajax類型的請求及返回值ajax
    """

    def render_to_json_response(self, context, **response_kwargs):
        """Render a json response of the context."""

        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)
    
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)

        return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            # Request is ajax, send a json response
            data = {
                'pk': self.object.pk,
            }
            return self.render_to_json_response(data)

        return response  # Request isn't ajax, send normal response
def looper_index(request):
    iterator = TemplateIterator()
    result = {
        'teams':UserService.getLocalPartUserCount(),
        'projects':ProjectService.getFixdProjects(),
        'active_tasks':TaskService.getActiveTaskCount(),
        'ongoing_tasks':TaskService.getOngoingTaskCount(),
        'task_performance':TaskService.analysisTaskPercent(),
        'leader_board':TaskService.analysisUserTaskPercent(),
        'active_project':TaskService.getActiveProjects(),
        'to_dos':TaskService.getToDos(),
        'iterator':iterator
    }
    return render(request, 'PMIS/looper/index.html', result)

def looper_calendar(request):
    if 'type' in request.GET:
        type = request.GET.get('type')
        id = request.GET.get('id')
        return render(request, 'PMIS/looper/calendar.html', {'type':type, 'id':id})
    else:
        return render(request, 'PMIS/looper/calendar.html')

def looper_events(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    results = []
    if not ('type' in request.GET):
        str_sql = '''Select * from V_Task where ((((TidStr LIKE '%%0[0-9][0-9]') OR (Tid BETWEEN 0 AND 99)) OR ((Pid = '00500') AND 
                    (Tid BETWEEN 100 AND 199)) OR ((Pid = '888') AND (Tid = 100)) OR ((TaskIDStr LIKE '%%5[0-9][0-9]'))) 
                    AND ((Contact = 'hb') AND (Progress NOT IN ('C', 'F')) AND (SchPriority > 0))) '''
        str_sql += " and PlanBDate >= '{}' and PlanEDate <= '{}'".format(start,end)
        rs = VTask.objects.raw(str_sql)
        for task in rs:
            event = {"title": task.task, "start": DateTools.formatf(task.planbdate, '%Y-%m-%d'),
                "end":DateTools.formatf(task.planedate, '%Y-%m-%d'), "textColor": "rgb(0, 162, 138)", 
                "backgroundColor": "rgba(0, 162, 138, .12)",
                "borderColor": "rgb(0, 162, 138)"}
            results.append(event)
    else:
        type = request.GET.get('type')
        id = request.GET.get('id')
        if type == 'goal': #goalmaster 的日曆
            results = views_goalmaster.get_doal_calendar(id, start, end)
    return JsonResponse(results, safe=False)
def looper_gantt(request):
    if 'type' in request.GET:
        type = request.GET.get('type')
        id = request.GET.get('id')
        params = {'type':type, 'id':id}
        if type == 'goal':
            show_level = ''
            if 'show_q' in request.GET:
                show_level += '1'
            if 'show_m' in request.GET:
                show_level += '2'
            if 'show_w' in request.GET:
                show_level += '3'
            if 'show_t' in request.GET:
                show_level += '4'            
            params['show_level'] = show_level;
        return render(request, 'PMIS/looper/gantt.html', params)
    else:
        return render(request, 'PMIS/looper/gantt.html')

def looper_gantt_data(request):
    results = []
    if not ('type' in request.GET):
        str_sql = '''SELECT D.TaskNo taskno,D.Pid Pid, D.Task task,D.PlanBDate planbdate,D.PlanEDate planedate,D.inc_id FROM GoalDetail A
                INNER JOIN GoalMaster B
                ON A.Period = B.Period AND A.Contact = B.Contact AND A.RecordId = B.RecordId AND A.GType = B.GType AND A.ItemNo = B.ItemNo
                INNER JOIN Task C
                ON A.Pid = C.Pid AND A.Tid = C.Tid AND A.TaskId = C.TaskId
                INNER JOIN V_Task D
                ON D.RelationGoalId = CONVERT(Varchar(10),C.Pid) + '-' + CONVERT(Varchar(20), CONVERT(Decimal(18, 0), C.Tid)) + '-' + CONVERT(Varchar(10), CONVERT(Decimal(18, 0), C.TaskID)) 
                LEFT JOIN SubProject S
                ON S.RecordId = B.RecordId
                WHERE A.contact = 'hb' AND A.Period IN ('2019-4','2020-1') AND D.Task NOT LIKE '%%' + S.ProjectName '''
        rs = VTask.objects.raw(str_sql)
        for task in rs:
            event = {"name": task.task, "start": DateTools.formatf(task.planbdate, '%Y-%m-%d'),
                "end":DateTools.formatf(task.planedate, '%Y-%m-%d'), 
                "id":task.taskno,
                "progress":random.randint(1,100)}
            results.append(event)
    else:
        type = request.GET.get('type')
        id = request.GET.get('id') 
        if type == 'goal': #goalmaster 的gantt
            show_level = request.GET.get('show_level')
            results = views_goalmaster.get_goal_gantt(id, show_level)
    return JsonResponse(results, safe=False)
def test(request):
    return render(request, "PMIS/test.html")