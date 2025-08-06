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

def sales_dashboard(request):
    return render(request, 'PMIS/keen/sales_dashboard.html')

default_result = {'code':1, 'data':[]}

def genJsonData(rs):
    result = default_result.copy()
    result['code'] = 0
    result['data'] = list(rs.values())
    return JsonResponse(result)

def getPastYearSales(request):
    '''
    功能描述：獲取過去一年的銷售
    '''
    try:
        rs = models.VSalesPastyear.objects.all()
        return genJsonData(rs)
    except Exception as e:
        print(str(e))
        return JsonResponse(default_result)

def getQuarterSales(request):
    '''
    功能描述：獲取本季度新訂單
    '''
    try:
        rs = models.VSalesQuarter.objects.all()
        return genJsonData(rs)
    except Exception as e:
        print(str(e))
        return JsonResponse(default_result)
def getWeeklyShipment(request):
    ''''
    功能描述：獲取本周出貨
    '''
    try:
        rs = models.VSalesWeeklyShipment.objects.all()
        return genJsonData(rs)
    except:
        return JsonResponse(default_result)

def getSalesCustAnalysis(request):
    '''
    功能描述：客戶這兩年對比增長
    '''
    try:
        rs = models.VSalesCustAnalysis.objects.all()
        return genJsonData(rs)
    except:
        return JsonResponse(default_result)
def getOrderState(request):
    '''
    功能描述：獲取過去一年銷售數據
    '''
    try:
        rs = models.VSalesPastyear.objects.all()
        return genJsonData(rs)
    except:
        return JsonResponse(default_result)

def getSaleOrderList(request):
    '''
    功能描述：獲取最後的訂單信息
    '''
    try:
        rs = models.VSalesOrderlist.objects.all()
        return genJsonData(rs)
    except:
        return JsonResponse(default_result)

def product_search(request):
    '''
    功能描述：獲取top Product
    '''
    try:
        rs = models.VSalesTopProduct.objects.all()
        return genJsonData(rs)
    except:
        return JsonResponse(default_result)

def getNewProduct(request):
    '''
    功能描述：獲取新產品
    '''
    end_date = DateTools.datetime.datetime.now()
    start_date = DateTools.addMonth(end_date, -12)
    try:
        rs = models.VSalesNewproduct.objects.annotate(new_date=Cast(Left('create_date', 6), output_field=CharField())).\
                     filter(new_date__gte=DateTools.formatf(start_date, '%Y%m'), \
                     new_date__lte=DateTools.formatf(end_date, '%Y%m'))
        return genJsonData(rs)
    except:
        return JsonResponse(default_result)

