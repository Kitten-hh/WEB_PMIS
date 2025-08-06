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
from PMIS.Services.ScheduleService import QuarterlyScheduleLogic
import  decimal
from django.core.serializers.json import DjangoJSONEncoder

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)

def display_logic(request):
    user = request.GET.get('username')
    schedule = QuarterlyScheduleLogic('2020-3',(user,))
    schedule.big_schedule()    
    data = {
        'sessions':json.dumps([{key:value for key,value in a.__dict__.items() if key != '_state'} for a in schedule.source[user]['sessions']], cls=DjangoJSONEncoder),
        'tasks':json.dumps([{key:value for key, value in a.__dict__.items() if key != '_state'} for a in schedule.source[user]['tasks']], cls=DjangoJSONEncoder)
    }
    return render(request, 'PMIS/schedule/display_logic.html', data)

def display_logic_bar(request):
    user = request.GET.get('username')
    schedule = QuarterlyScheduleLogic('2020-3',(user,))
    schedule.big_schedule()    
    data = {
        'sessions':json.dumps([{key:value for key,value in a.__dict__.items() if key != '_state'} for a in schedule.source[user]['sessions']], cls=DjangoJSONEncoder),
        'tasks':json.dumps([{key:value for key, value in a.__dict__.items() if key != '_state'} for a in schedule.source[user]['tasks']], cls=DjangoJSONEncoder)
    }
    return render(request, 'PMIS/schedule/display_bar.html', data)


