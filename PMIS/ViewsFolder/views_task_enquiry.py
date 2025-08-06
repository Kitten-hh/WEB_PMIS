from django.shortcuts import render
from django.forms.models import model_to_dict
from django.template import loader
from django.http import HttpResponse,JsonResponse,HttpRequest
from django.db.models import Sum,Count,Max,Min,Avg,Q
from DataBase_MPMS import models
from .. import forms
from ..Services import QueryFilterService
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from datatableview import Datatable
from django.db import connections
from datatableview.views import MultipleDatatableView
from datatableview.views.legacy import LegacyDatatableView
from datatableview import helpers
from PMIS.Services.MindmapService import MindmapService
from django.contrib.auth.decorators import login_required



class DisplayView(MultipleDatatableView):
    class datatable_task(Datatable):
        class Meta:
            model = forms.TaskR_S_Form.Meta.model
            columns = forms.TaskR_S_Form.Meta.fields
            labels = forms.TaskR_S_Form.Meta.labels
    datatable_classes = {
        'task': datatable_task
    }    

    def get_task_datatable_queryset(self):
        search_val = self.request.GET.get('search[value]')
        if search_val == '':
            return models.Task.objects.all()
        else:
            #QueryFilterService.get_query_filter_queryset(search_val)
            return models.Task.objects.all()
    '''
    def get_datatables(self, only=None):
        datatables = super(MultipleDatatableView, self).get_datatables(only)
        if only in (None, 'demo2'):
            demo2 = datatables['demo2']
            del demo2.columns['pid']
        return datatables
    '''
    def getAllUsers(self):
        rs = models.Users.objects.values('username').all()
        return json.dumps(list(rs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = self.getAllUsers()
        return context

    paginate_by = 30    
    template_name = 'PMIS/task_enquiry.html'

def display_task_enquiry(request):
    if 'query_filter_id' in request.GET:
        id = request.GET.get('query_filter_id')
        str_filter = QueryFilterService.get_query_filter(id)
        print(str_filter)
        rs = models.VTask.objects.raw('select * from V_Task where ' + str_filter);
        results = []
        for task in rs:
            results.append(model_to_dict(task))
        return JsonResponse(results, safe=False)
    else: #默認查詢top twenty
        str_sql = '''Select top 20 * from V_Task where ((((TidStr LIKE '%%0[0-9][0-9]') OR (Tid BETWEEN 0 AND 99)) OR ((Pid = '00500') AND 
                    (Tid BETWEEN 100 AND 199)) OR ((Pid = '888') AND (Tid = 100)) OR ((TaskIDStr LIKE '%%5[0-9][0-9]'))) 
                    AND ((Contact = 'sing') AND (Progress NOT IN ('C', 'F')) AND (SchPriority > 0))) '''
        rs = models.VTask.objects.raw(str_sql)
        data = list(rs)
        return render(request, 'PMIS/task_enquiry.html', {'datas': data})

def searchRecordFilter(request):
    result = {}
    if 'filter' in request.GET:
        str_filter = request.GET.get("filter")
        is_daily = request.GET.get("is_dialy")
        qf003_filter = Q()
        qf003_filter.connector = 'AND'
        qf008_filter = Q()
        qf008_filter.connector = 'AND'
        filter_arr = str_filter.split('+')
        for filter in filter_arr:
            filter = filter.strip()
            qf003_filter.children.append(('qf003__contains',filter))
            qf008_filter.children.append(('qf008__contains',filter))
        rs = models.VQueryfilter.objects.values('qf001','qf002','qf003','qf012','qf025').filter(Q(qf006='sing',qf009='PMS',qf010='TaskEnquiry_Frm') & (qf003_filter | qf008_filter))
        if 'Y' == is_daily:
            rs = rs.filter(qt002__contains='Daily Goal')
        rs = rs.order_by('qf012')
        result['data'] = list(rs)
    return JsonResponse(result)
##############################################################################################
##以上為原來Demo的代碼
##############################################################################################
def search_task_with_query_filter(request:HttpRequest, queryid):
    result = {'status':False, 'msg':'', 'data':[]}
    if queryid:
        try:
            str_filter,top = QueryFilterService.get_query_filter_advanced(queryid)
        except Exception as e:
            print(str(e))
            result['status'] = False
            result['msg'] = '沒有這個查詢條件 {0}，或查詢條件錯誤'.format(queryid)
            return result
        try:
            if not top:
                rs = models.VTask.objects.raw('select * from V_Task where ' + str_filter + ' order by PlanBDate asc')
            else:
                rs = models.VTask.objects.raw(f'select top {top} * from V_Task where ' + str_filter + ' order by SchPriority Desc')
            result['status'] = True
            result['data'] = [model_to_dict(task) for task in rs]
        except Exception as ee:
            print(str(ee))
            result['status'] = False
            result['msg'] = '使用查詢條件查詢失敗'
    return JsonResponse(result, safe=False)

@login_required()
def dynamicMindmap(request:HttpRequest):
    try:
        server = MindmapService()
        requestMethod = request.GET;
        if request.method == "POST":
            requestMethod = request.POST
        queryFilterId = requestMethod.get('queryFilterId')
        queryFilterKeyStr = requestMethod.get('queryFilterKey')
        queryFilterKey = None
        if queryFilterKeyStr:
            queryFilterKey = json.loads(queryFilterKeyStr)
        condition = requestMethod.get('condition');
        mindmap_json = server.generateMindmap(queryFilterId, queryFilterKey, condition)
        return render(request, "PMISLooper/mindmap/mindmap.html", {'hideMenu':'Y',"dynamic_mindmap_json":mindmap_json})
    except Exception as e:
        print(str(e))
        return HttpResponse(status=404)