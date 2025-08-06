from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,JsonResponse,HttpRequest
from ..Services.TypeListService import TypeListService
import logging


LOGGING = logging.Logger(__name__)

def get_type_list(request:HttpRequest):
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        type_name = request.GET.get("type_name")
        if type_name:
            data = TypeListService.get_typelist(type_name)
            result['data'] = data
        result['status'] = True
    except Exception as e:
        LOGGING.error(e)
    return JsonResponse(result, safe=False)