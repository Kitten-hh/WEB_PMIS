from django.shortcuts import render
from PMIS.Services.UserService import UserService
from PMIS.Services.TaskService import TaskService
from PMIS.Services.ProjectService import ProjectService
import itertools

from DataBase_MPMS import models
from django.core.serializers.json import DjangoJSONEncoder 
from django.forms.models import model_to_dict
from django.db.models import Count,Q,Case,Sum,When,IntegerField,Max
import json
import datetime
import calendar
import dateutil.relativedelta
import decimal
from django.http import JsonResponse,HttpResponse,HttpRequest
from BaseApp.library.cust_views.SWCreateView import SWCreateView
from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from BaseApp.library.cust_views.SWDeleteView import SWDeleteView
from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
from BaseApp.library.tools import DateTools
import re
from django.shortcuts import render
from datatableview import Datatable
from BaseApp.library.tools.QueryBuilderUtils import QueryBuilderUtils
from querybuilder.rules import Rule




def getTechnicid(request:HttpRequest):
    #獲取技術文檔INC_ID
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        strmb023 = request.GET.get('mb023')
        if strmb023:
            Technicdata = models.Tecmb.objects.filter(mb023=strmb023).values('mb023','mb004','inc_id')
            if Technicdata:
                Technicdata = Technicdata[0]
                mb023 = Technicdata['mb023']
                mb004 = Technicdata['mb004']
                if Technicdata['mb023'] == None:
                    mb023 = ''
                if Technicdata['mb004'] == None:
                    mb004 = ''
                Technicalcode = mb023.strip(" ")+'('+mb004+')'
                Tecmblist = {"Technicalcode":Technicalcode,"inc_id":Technicdata['inc_id']}
                result['data'].append(Tecmblist)
            result['status'] = True
        else:
           result['msg'] = {"error":"Parameter not found"}
           result['status'] = False     
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   





