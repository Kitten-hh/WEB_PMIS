from django.shortcuts import render
from django.forms.models import model_to_dict
from django.template import loader
from django.http import HttpResponse,JsonResponse,HttpRequest
from django.db.models import Sum,Count,Max,Min,Avg,Q
from DataBase_MPMS import models
from PMIS import forms
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
from BaseProject.views_folder.base_crud.SimpleView import SimpleView
from BaseProject.decorators.customer_dec import URL
from PMIS.Services.ScheduleService import ScheduleParam
from BaseProject.CustomBaseObject.base_views.CustomView import CustomUpdateView,ViewInfo
from BaseProject.tools.QueryBuilderUtils import QueryBuildUtils

class ScheduleParamsViews(SimpleView):
    

    def init_view(self):
        self.view_template_name = 'PMIS/schedule/params.html'
        self.form = forms.SchPeriod_main_form
        self.schTypeForm = forms.SchType_main_form

    def get_view_cls(self):
        outerClassSelf = self
        base = super().get_view_cls()        
        class ScheduleParamsMasterView(base):
            class datatable_type(Datatable):
                class Meta:
                    id = "SchType"
                    model = outerClassSelf.schTypeForm.Meta.model
                    columns = outerClassSelf.get_fields_from_form(outerClassSelf.schTypeForm)
                    labels = outerClassSelf.schTypeForm.Meta.labels
                    page_length = -1
            base.datatable_classes['SchType'] = datatable_type
            def get_SchType_datatable_queryset(self):
                return outerClassSelf.schTypeForm.Meta.model.objects.all()
        return ScheduleParamsMasterView

    def get_context_data_display(self, displayView, context, **kwargs):        
        user = displayView.request.GET.get('user')
        if not user:
            user = 'sing'
        sys_params = ScheduleParam.read_sys_params()
        context['sys_params'] = json.dumps(sys_params)
        periods,curr_user_params,next_user_params = ScheduleParam.read_user_params(user)
        context['curr_user_params'] = json.dumps(curr_user_params)
        context['next_user_params'] = json.dumps(next_user_params)
        context['user_list'] = ScheduleParam.get_user_list()
        context['user'] = user
        context['periods'] = [key for key in periods.keys()]

        type_dict = ScheduleParam.get_type_list()
        context['type_list'] = json.dumps(type_dict)
    
    def get_initial_create(self, createView, initial):
        view_id = createView.request.GET.get('view_id')
        if view_id == 'SchType':
            max_no = ScheduleParam.get_max_sch_type_no()
            initial['typeno'] = max_no
            initial['udf02'] = max_no
        return initial

    @URL(url="params")
    def params_manager(self, request:HttpRequest):
        return render(request, "")

    @URL(url="save_params")
    def save_params(self, request:HttpRequest):
        sys_params = request.POST.get('sys_params')
        cur_user_parasm = request.POST.get('curr_user_params')
        user = request.POST.get('user')
        if not user:
            user = 'sing'
        if sys_params:
            sys_params = json.loads(sys_params)
        if cur_user_parasm:
            cur_user_parasm = json.loads(cur_user_parasm)
        status = ScheduleParam.save_params(user,sys_params, cur_user_parasm)
        return JsonResponse({'status':status})