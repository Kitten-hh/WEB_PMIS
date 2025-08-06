from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,JsonResponse
from DataBase_VCAsia_db import models
from .. import forms
from DataBase_MPMS import forms_base
from django.core.serializers.json import DjangoJSONEncoder
import json
import re
from BaseProject.CustomBaseObject.mixins.CustomMixin import AjaxableResponseMixin
from BaseProject.tools import DateTools
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db import connections,transaction
from datatableview import helpers
from django.db.models import IntegerField,CharField, Value as V
from django.db.models.functions import Cast, Substr
from django.db.models import Sum,Count,Max,Min,Avg,Q
from ..Services.TaskService import TaskService

default_result = {'code':1, 'data':[]}

def genJsonData(rs):
    result = default_result.copy()
    result['code'] = 0
    result['data'] = list(rs)
    return JsonResponse(result)

def getCompletionTasks(request):
    try:
        start=None
        end = None
        contact = None
        if 'start' in request.GET:
            start = DateTools.parse(request.GET.get('start'))
        if 'end' in request.GET:
            end = DateTools.parse(request.GET.get('end'))
        if 'contact' in request.GET:
            contact = request.GET.get('contact')
        rs = TaskService.analysisFinishTasks(contact, start, end)
        return genJsonData(rs)
    except Exception as e:
        print(e)
        return JsonResponse(default_result)