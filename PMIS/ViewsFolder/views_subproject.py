from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,JsonResponse,HttpRequest
from DataBase_MPMS import models,forms_base
from .. import forms
from django.core.serializers.json import DjangoJSONEncoder
import json
import re
import datetime
from django.db.models.functions import Cast, Substr
from django.db.models import Sum,Count,Max,Min,Avg,Q
from django.db.models.functions import Left,StrIndex
from BaseProject.tools import DateTools
from django.forms.models import model_to_dict
from django.conf import settings
from django.core.cache import cache
from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView

def get_all_recordid_list(request):
    '''
    功能描述：獲取用戶名列表
    '''
    result = {'status':False, 'msg':'', 'data':None}
    try:
        all_recordid = cache.get(settings.CACHES_NAME_ALLRRECORDID)
        if all_recordid:
            result['status'] = True
            result['data'] = all_recordid
        else:
            queryset = models.Subproject.objects.values('recordid','projectname').all().order_by('recordid');
            all_recordid = [{'recordid':t['recordid'], 'projectname':t['projectname'], 'CompDesc':'{0}({1})'.format(t['recordid'], t['projectname'])} for t in queryset]
            result['status'] = True
            result['data'] = all_recordid
            cache.set(settings.CACHES_NAME_ALLRRECORDID, all_recordid, timeout=3600)
    except Exception as e:
        print(str(e));
        result['status'] = False
    return JsonResponse(result, safe=False)



def get_recordid_list(request):
    '''
    功能描述：獲取項目信息
    '''
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        recordid = request.GET.get('recordid')
        pid = request.GET.get('pid')
        tid = request.GET.get('tid')
        queryset = {'subproject':[],'tasklist':[]}
        if recordid:
            subproject = models.Subproject.objects.filter(recordid=recordid).values()
            queryset['subproject'] = list(subproject)
        if pid and tid:   
            tasklist = models.Tasklist.objects.filter(pid=pid,tid=tid).values()
            queryset['tasklist'] = list(tasklist)
        result['status'] = True
        result['data'].append(queryset)
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)
