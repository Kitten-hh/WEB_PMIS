from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpRequest
from DataBase_MPMS.models import Tasktypelist
from django.conf import settings
from django.core.cache import cache

def get_tasktype_list(request:HttpRequest):
    '''
    功能描述：獲取TaskType 列表
    '''
    
    try:
        tasktype_list = cache.get(settings.CACHES_NAME_TASKTYPELIST)
        if tasktype_list:
            return JsonResponse({'data':tasktype_list}, safe=False)
        else:
            queryset = Tasktypelist.objects.values('tasktype','description').filter(parenttype__isnull=True)
            for data in queryset:
                data['description'] = '{0}.{1}'.format(data['tasktype'],data['description'])
            tasktype_list = list(queryset)
            cache.set(settings.CACHES_NAME_TASKTYPELIST,  tasktype_list)
            return JsonResponse({'data':tasktype_list}, safe=False)
    except Exception as e:
        print(str(e))
        return JsonResponse({'data':[]}, safe=False)

def get_subtasktype_list(request:HttpRequest, tasktype):
    '''
    功能描述：獲取Sub TaskType列表
    '''
    try:
        queryset = Tasktypelist.objects.values('tasktype','displaytype','description').filter(parenttype=tasktype)
        for data in queryset:
            data['description'] = '{0}.{1}'.format(data['displaytype'],data['description'])
        return JsonResponse({'data':list(queryset)}, safe=False)
    except Exception as e:
        print(str(e))
        return JsonResponse({'data':[]}, safe=False)

def get_subtasktype_score(request:HttpRequest):
    '''
    功能描述：獲取TaskType分數
    '''
    try:
        tasktype = request.GET.get('tasktype')
        subtasktype = request.GET.get('subtasktype')
        queryset = Tasktypelist.objects.values('tasktype','displaytype','description','score','difficulties1','difficulties2','difficulties3')\
        .filter(parenttype=tasktype,tasktype=subtasktype)
        return JsonResponse({'data':list(queryset),'status':True}, safe=False)
    except Exception as e:
        print(str(e))
        return JsonResponse({'data':[],'status':False}, safe=False)

