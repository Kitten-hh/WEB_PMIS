from django.shortcuts import render
from django.forms.models import model_to_dict
from django.template import loader
from django.http import HttpResponse
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


def display_simple_template(request):
    return render(request, 'PMIS/my_main_page.html')

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
        return models.Task.objects.all()
    '''
    def get_datatables(self, only=None):
        datatables = super(MultipleDatatableView, self).get_datatables(only)
        if only in (None, 'demo2'):
            demo2 = datatables['demo2']
            del demo2.columns['pid']
        return datatables
    '''
    paginate_by = 30    
    template_name = 'PMIS/simple_template.html'
