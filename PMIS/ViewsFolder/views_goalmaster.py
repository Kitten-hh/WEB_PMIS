from django.shortcuts import render
from django.forms.models import model_to_dict
from django.template import loader
from django.http import HttpResponse,JsonResponse
from django.db.models import Sum,Count,Max,Min,Avg,Q
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
from BaseProject.CustomBaseObject.base_views.CustomView import CustomUpdateView
from BaseProject.tools import DateTools
from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from ..Services.GoalService import GoalService
from django.core.cache import cache
from django.conf import settings


gzip_middleware = GZipMiddleware()

class GZipMixin(object):
    def dispatch(self, request, *args, **kwargs):
        response = super(GZipMixin, self).dispatch(request, *args, **kwargs)
        return gzip_middleware.process_response(request, response)

class GoalMasterView(MultipleDatatableView):
    class datatable_master(Datatable):
        class Meta:
            model = forms.VGoalmaster_main_form.Meta.model
            columns = forms.VGoalmaster_main_form.Meta.fields
            labels = forms.VGoalmaster_main_form.Meta.labels
            hidden_columns = ['score','gtype','itemno','inc_id']
            page_length = -1
            processors = {
                "bdate": helpers.format_date("%Y-%m-%d"),
                'edate': helpers.format_date("%Y-%m-%d"),
                'pschedule': helpers.format("{0:.2f}"),
                'aschedule': helpers.format("{0:.2f}")                
            }
    datatable_classes = {
        'master': datatable_master
    }    

    def get_master_datatable_queryset(self):
        if 'draw' in self.request.GET:
            local_GET = self.request.GET.copy()
            for key in self.request.GET.keys():
                value = self.request.GET.get(key)
                if key.startswith('order['):
                    num_str = key[6:key.find(']')]
                    new_key = 'order[' + str(int(num_str) + 1) + key[6 + len(num_str):]
                    local_GET[new_key] = value
            local_GET['order[0][column]'] = '8'
            local_GET['order[0][dir]'] = 'desc'
            self.request.GET = local_GET
        return forms.VGoalmaster_main_form.Meta.model.objects.all()
    #paginate_by = 0
    template_name = 'PMIS/goal_master_form.html'
class GoalMasterEditView(CustomUpdateView):
    model = models.Goalmaster    
    fields = ["objective",'bdate','edate']
    def get_success_url(self):
        # Assuming there is a ForeignKey from Comment to Post in your model
        obj = self.object 
        return '/PMIS/goal_master_form'

def update_goal(request, pk):
    '''
    功能描述：更新任務信息
    '''
    result = {}
    model = models.Task.objects.get(pk=pk)
    if model and 'task' in request.POST:
        model.task = request.POST.get('task')
        model.save(update_fields=['task'])
        result['status'] = True
    else:
        result['status'] = False
    return JsonResponse(result)
        

def display_goal(request, pk):
    master = models.Goalmaster.objects.get(pk=pk)
    with connections['MPMS'].cursor() as cursor:
        goal_filter = "contact = '{}' and period = '{}' and recordId = '{}' and itemno = '{}'".format(master.contact, master.period,
            master.recordid, master.itemno)
        param = ['TaskNo','RelationGoalId', 1, 0, '', '', goal_filter]
        cursor.execute('SET NOCOUNT ON {CALL dbo.LoadTreeList (%s,%s,%s,%s,%s,%s,%s)}', param)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            obj = dict(zip(columns, row))
            reGoalId = obj.get('RelationGoalId')
            if reGoalId:
                obj['RelationGoalId'] = reGoalId.strip()
            results.append(obj)
    obj = model_to_dict(master)
    print(json.dumps(obj, cls=DjangoJSONEncoder))
    return render(request, 'PMIS/goal_master_treelist.html', {'data':json.dumps(results, cls=DjangoJSONEncoder),'appraisal_id':pk})

def get_doal_calendar(pk, start, end):
    results = []
    start_date = pytz.UTC.localize(DateTools.parsef(start, '%Y-%m-%d'))
    end_date = pytz.UTC.localize(DateTools.parsef(end, '%Y-%m-%d'))
    master = models.Goalmaster.objects.get(pk=pk)
    with connections['MPMS'].cursor() as cursor:
        goal_filter = "contact = '{}' and period = '{}' and recordId = '{}' and itemno = '{}'".format(master.contact, master.period,
            master.recordid, master.itemno)
        param = ['TaskNo','RelationGoalId', 1, 0, '', '', goal_filter]
        cursor.execute('SET NOCOUNT ON {CALL dbo.LoadTreeList (%s,%s,%s,%s,%s,%s,%s)}', param)
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            obj = dict(zip(columns, row))
            planbdate =  pytz.UTC.localize(obj.get('PlanBDate'))
            planedate =  pytz.UTC.localize(obj.get('PlanEDate'))
            if (planbdate >= start_date and planbdate <= end_date) or (planedate  >= start_date and planedate <= end_date):
                event = {"title": obj.get('Task'), "start": DateTools.formatf(obj.get('PlanBDate'), '%Y-%m-%d'),
                    "end":DateTools.formatf(obj.get('PlanEDate'), '%Y-%m-%d'), "textColor": "rgb(294, 172, 47)", 
                    "backgroundColor": "rgba(294, 172, 47, .12)",
                    "borderColor": "rgb(294, 172, 47)"}
                level = obj.get('LevelNum')
                if level == 1:
                    event['textColor'] = 'rgb(65, 105, 225)'
                    event['backgroundColor'] = 'rgba(65, 105, 225, .12)'
                    event['borderColor'] =  'rgb(65, 105, 225)'
                elif level == 2:
                    event['textColor'] = 'rgb(100,149,237)'
                    event['backgroundColor'] = 'rgba(100,149,237, .12)'
                    event['borderColor'] =  'rgb(100,149,237)'
                elif level == 3:
                    event['textColor'] = 'rgb(135, 206, 250)'
                    event['backgroundColor'] = 'rgba(135, 206, 250, .12)'
                    event['borderColor'] =  'rgb(135, 206, 250)'
                results.append(event)
    return results
def get_goal_gantt(pk, show_level):
    results = []
    pks = pk.split(';')
    masters = models.Goalmaster.objects.filter(pk__in=pks)
    goal_filter = ''
    for master in masters:
        if goal_filter != "":
            goal_filter += " or "
        goal_filter += "(contact = '{}' and period = '{}' and recordId = '{}' and itemno = '{}')".format(master.contact, master.period,
                master.recordid, master.itemno)
    if goal_filter == '':
        return results
    goal_filter = "(" + goal_filter + ")"
    with connections['MPMS'].cursor() as cursor:
        param = ['TaskNo','RelationGoalId', 1, 0, '', '', goal_filter]
        cursor.execute('SET NOCOUNT ON {CALL dbo.LoadTreeList (%s,%s,%s,%s,%s,%s,%s)}', param)
        columns = [column[0] for column in cursor.description]
        quarter_task = None
        monthly_task = None
        weekly_task = None
        task = None
        for row in cursor.fetchall():        
            obj = dict(zip(columns, row))
            level = obj.get('LevelNum')            
            if show_level and show_level.find(str(level)) == -1:
                continue
            event = {"name": obj.get('Task'), "start": DateTools.formatf(obj.get('PlanBDate'), '%Y-%m-%d'),
                    "end":DateTools.formatf(obj.get('PlanEDate'), '%Y-%m-%d'), 
                    "id":obj.get('TaskNo'),
                    "progress":random.randint(1,100)}
            reGoalId = obj.get('RelationGoalId')
            
            if not show_level or show_level == '1234':
                if level == 1:
                    quarter_task = obj
                elif level == 2:
                    if task.get('LevelNum') == 1:
                        event['dependencies'] = quarter_task.get('TaskNo').strip()
                    else:
                        event['dependencies'] = monthly_task.get('TaskNo').strip()
                    monthly_task = obj
                elif level == 3:
                    if task.get('LevelNum') == 2:
                        event['dependencies'] = monthly_task.get('TaskNo').strip()
                    else:
                        event['dependencies'] = weekly_task.get('TaskNo').strip()
                    weekly_task = obj
                elif level == 4:
                    if task.get('LevelNum') == 3:
                        event['dependencies'] = weekly_task.get('TaskNo').strip()
                    else:
                        event['dependencies'] = task.get('TaskNo').strip()
                task = obj
            results.append(event)
    return results
            
def report(request):
    dc = request.GET.get('dc')
    if not dc == "false":
        return JsonResponse({})
    id = request.GET.get('id')
    master = models.Goalmaster.objects.get(inc_id=id)
    with connections['MPMS'].cursor() as cursor:
        goal_filter = "contact = '{}' and period = '{}' and recordId = '{}' and itemno = '{}'".format(master.contact, master.period,
            master.recordid, master.itemno)
        param = ['TaskNo','RelationGoalId', 1, 0, '', '', goal_filter]
        cursor.execute('SET NOCOUNT ON {CALL dbo.LoadTreeList (%s,%s,%s,%s,%s,%s,%s)}', param)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            obj = dict(zip(columns, row))
            reGoalId = obj.get('RelationGoalId')
            if reGoalId:
                obj['RelationGoalId'] = reGoalId.strip()
            results.append(obj)
    obj = model_to_dict(master)
    data = {}
    data['master'] = obj
    data['details'] = results
    return JsonResponse(data)
##############################################################################################
##以上為原來Demo的代碼
##############################################################################################
def get_all_period_list(request):
    result = {'status':False, 'msg':'', 'data':None}
    try:
        periods = cache.get(settings.CACHES_NAME_GOALPERIODS)
        if periods:
            result['status'] = True
            result['data'] = periods
        else:
            queryset = models.Goalmaster.objects.values('period').distinct().order_by('-period')[:4];
            periods = [instance['period'] for instance in queryset]
            result['status'] = True
            result['data'] = periods
            cache.set(settings.CACHES_NAME_GOALPERIODS, periods)
    except Exception as e:
        print(str(e));
        result['status'] = False
    return JsonResponse(result, safe=False)

class NewGoalMasterView(DatatablesServerSideView):
    model = models.VGoalmaster
    def get_initial_queryset(self):
        return self.model.objects.all().order_by("-score")

class UpdateMasterView(SWUpdateView):
    model = models.Goalmaster

def show_goal_treelist(request, pk):
    result = {'status':False, 'msg':'', 'data':None}
    try:
        goals = GoalService.get_goal_treelist(pk)
        result['status'] = True
        result['data'] = goals
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)