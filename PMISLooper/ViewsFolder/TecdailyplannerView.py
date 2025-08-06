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




class TaskDeleteView(SWDeleteView):
    model = models.Tecdailyplanner

class SolutionDeleteView(SWDeleteView):
    model = models.Tecdailyplannersolution


    
def TaskCodeDeleteView(request:HttpRequest):
    #刪除Code或UI
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        inc_id = request.GET.get("inc_id")
        if inc_id!='' :
            query = Q()
            query.connector = "and"
            query.children.append(('inc_id',inc_id))
            Tecdailyplannerimage = models.Tecdailyplannerimage.objects.filter(query)
            Tecdailyplannerimage.delete()
            result['status'] = True
        else:
            result['status'] = False
            result['msg'] = {"error":"Parameter not found"}
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   


    



def DeletemoreDailyPlanner(request:HttpRequest):
    #一次刪除多條
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        inputdate = request.GET.get("inputdate")
        contact = request.GET.get("contact")
        itemno = request.GET.get("itemno")
        if inputdate!='' and contact!='':
            query = Q()
            query.connector = "and"
            query.children.append(('inputdate',inputdate))
            query.children.append(('contact',contact))
            if itemno != '':
                query.children.append(('itemno', itemno))
            Tecdailyplanner = models.Tecdailyplanner.objects.filter(query)
            Tecdailyplanner.delete()
            Tecdailyplannersolutionlist = models.Tecdailyplannersolution.objects.filter(query)
            Tecdailyplannersolutionlist.delete()
            Tecdailyplannerimage = models.Tecdailyplannerimage.objects.filter(query)
            Tecdailyplannerimage.delete()
            result['status'] = True
        else:
            result['status'] = False
            result['msg'] = {"error":"Parameter not found"}
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   





def AnalyseDailyPlanner(request:HttpRequest):
    #分析用戶的DailyPlanner
    result = {'status':False, 'msg':'', 'data':[]}
    DailyPlannerdata = []
    try:
        now = datetime.datetime.now()
        now = now + dateutil.relativedelta.relativedelta(months=-1)
        now = now.strftime('%Y%m')+'01'
        Tecdailyplannerlist = models.Tecdailyplanner.objects.filter(Q(inputdate__gte=now) & ~Q(abnormal__exact='') & ~Q(abnormal__exact=None)).order_by('-inputdate')
        result['data'] = list(Tecdailyplannerlist.values())
        result['status'] = True
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   


def get_development(request:HttpRequest):
    #分析用戶的DailyPlanner
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        pk = request.GET.get("pk")
        dailyplanner = models.Tecdailyplanner.objects.get(pk=pk)
        taskno = dailyplanner.taskno
        if taskno:
            arr = taskno.split("-")
            if len(arr) == 3:
                sessionid = "{0}-{1}".format(arr[0], arr[1])
                qs = models.VTasklistS.objects.filter(sessionid=sessionid)
                if len(qs) > 0:
                    result['status'] = True
                    result['data'] = {"recordid":qs[0].recordid, "sessionid":sessionid}
    except Exception as e:
        print(str(e))
    return JsonResponse(result, safe=False)
