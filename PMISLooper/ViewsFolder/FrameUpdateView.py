
from django.shortcuts import render
from PMIS.Services.UserService import UserService
from PMIS.Services.FrameService import FrameService
import itertools

from DataBase_MPMS import models
from django.core.serializers.json import DjangoJSONEncoder 
from django.forms.models import model_to_dict
from django.db.models import Count,Q,Case,Sum,When,IntegerField,Max
import json
from django.http import JsonResponse,HttpResponse,HttpRequest
from BaseApp.library.tools import DateTools



#獲取修改窗口文檔列表
def search_frames_list(request):
    # 定義要返回的對象
    try:
        result = {'status':False, 'msg':'', 'data':[]}
        username = request.GET.get("username", UserService.GetLoginUserName(request))
        bdate = request.GET.get("bdate")
        edate = request.GET.get("edate")
        frames = FrameService.search_frames_list(username, bdate, edate)
        result['data'] = frames
        result['status'] = True
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)


