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
from django.db import transaction





def GetTecdailyplannerImageContent(request:HttpRequest):
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        contact = request.GET.get('contact')
        inputdate = request.GET.get('inputdate')
        itemno = request.GET.get('itemno')
        imageno = request.GET.get('imageno')
        inc_id = request.GET.get('inc_id')
        # isrichtext = request.GET.get('isrichtext')
        if inc_id:
            datamodel = models.Tecdailyplannerimage.objects.filter(inc_id=inc_id).values()
        else:    
            datamodel = models.Tecdailyplannerimage.objects.filter(contact=contact,inputdate=inputdate,itemno=itemno,imageno=imageno).values()
        if datamodel:
            # if str(isrichtext)=='1':
            #     result['data'] = list(datamodel.values('detailtext'))
            # else:
            result['data'] = list(datamodel)
            result['status'] = True
        else:
            result['msg'] = {"error":"Tecdailyplannerimage not found"}
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result,safe=False)

def TecdailyplannerImageController(request:HttpRequest):
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        contact = request.POST.get('contact')
        inputdate = request.POST.get('inputdate')
        itemno = request.POST.get('itemno')
        imageno = request.POST.get('imageno')
        datamodel = models.Tecdailyplannerimage.objects.filter(contact=contact,inputdate=inputdate,itemno=itemno,imageno=imageno)
        if datamodel:
            UpdateTecdailyplannerImage(request.POST,datamodel)   
        else:  
            imageno = CreateTecdailyplannerImage(request.POST,contact,inputdate,itemno) 
            datamodel = models.Tecdailyplannerimage.objects.filter(contact=contact,inputdate=inputdate,itemno=itemno,imageno=imageno)   
        result['data'] = list(datamodel.values())
        result['status'] = True
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result,safe=False)    

def CreateTecdailyplannerImage(postData:object,contact,inputdate,itemno:str):
    '''
    功能描述：新增TecdailyplannerImage表數據
    '''
    #獲取字段值
    text = postData.get('text')
    DetailText = postData.get('DetailText')
    imageno = set_max_Image(contact,inputdate,itemno)
    if not DetailText:
       DetailText='' 
    solutionData = models.Tecdailyplannerimage(contact=contact,inputdate=inputdate,itemno=itemno,imageno=imageno,text=text,detailtext=DetailText)
    solutionData.save()
    return imageno

def UpdateTecdailyplannerImage(postData,datamodel:object):
    '''
    功能描述：修改TecdailyplannerImage表數據
    '''
    #獲取字段值
    text = postData.get('text')
    DetailText = postData.get('DetailText')
    if not DetailText:
       DetailText='' 
    datamodel.update(text=text,detailtext=DetailText)        

def set_max_Image(contact,inputdate,itemno:str):
    '''
    功能描述：獲取TecdailyplannerImage最大單號
    '''
    stTable = models.Tecdailyplannerimage.objects.filter(contact=contact,inputdate=inputdate,itemno=itemno).order_by('-imageno')[:1].values('imageno')
    if len(stTable) > 0:
        max_seq_no = '00000{0}'.format(int(stTable[0]['imageno']) + 10)[-5:]
    else:
        max_seq_no = '00010'
    return max_seq_no



