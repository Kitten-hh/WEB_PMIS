from django.shortcuts import render
from DataBase_MPMS.models import Tasktype,Tasktypelist,LSTasktypelist
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.shortcuts import redirect
from django.db.models import Count, Q, Case, Sum, When, IntegerField, Max, F, Avg, Min
from django.db import transaction
import pandas as pd
from pandas import DataFrame
from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
import os
from django.conf import settings
from BaseApp.library.cust_views.SWCreateView import SWCreateView
from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from BaseApp.library.cust_views.SWDeleteView import SWDeleteView

# Create your views here.
# TaskType_Management管理頁面
# url get_TaskType_Management/
def get_TaskType_Management(request):
    return render(request, 'BonusApp/TaskType_Management/TaskType_List.html')

# url get_TaskType_List/
def get_TaskType_List(request):
    taskTypes = Tasktype.objects.all().order_by('-id')
    taskTypes = list(taskTypes.values())
    result = {}
    result['state'] = 200
    result['data'] = taskTypes
    return JsonResponse(result)

def searchTasktype(request):
    tasktype = get_param_value(request,'tasktype')
    description = get_param_value(request,'description')    
    customFilter = Q(tasktype__isnull=False)       
    if tasktype: 
        customFilter = customFilter & (Q(tasktype=tasktype)|Q(parenttype=tasktype))
    if description:
        customFilter = customFilter & Q(description__icontains=description)
    tasktypelist = LSTasktypelist.objects.filter(customFilter).order_by('tasktype')
    datalist = list(tasktypelist.values())
    result = {}
    result['status'] = True
    result['data'] = datalist
    return JsonResponse(result, safe=False)

class TaskTypeDataTable(DatatablesServerSideView):
    model = Tasktype
    columns = "__all__"
    searchable_columns = ['id','tasktype','description']

# url get_TaskType_Details/
def get_TaskType_Details(request):
    taskType_Id = request.GET.get("taskType_Id")
    taskType = Tasktype.objects.filter(id=taskType_Id)
    taskType = list(taskType)
    context = {}
    if(len(taskType) > 0):
        t = list(taskType)[0]
        context['taskType'] = t
        return render(request, 'BonusApp/TaskType_Management/TaskType_Details.html', context)
    else:
        return render(request, "BonusApp/error.html")
    

# url get_TaskType_Modif_Page/ 
def get_TaskType_Modif_Page(request):
    taskType_Id = request.GET.get("taskType_Id")
    taskType = Tasktype.objects.filter(id=taskType_Id)
    taskType = list(taskType)
    context = {}
    if(len(taskType) > 0):
        t = list(taskType)[0]
        context['taskType'] = t
        return render(request, 'BonusApp/TaskType_Management/TaskType_Modif.html', context)
    else:
        return render(request, "BonusApp/error.html")

class TaskTypeUpdateView(SWUpdateView):
    model = Tasktype



def get_TaskType_Add_Page(request):
    return render(request, "BonusApp/TaskType_Management/TaskType_Add.html")

class TaskTypeCreativeView(SWCreateView):
    model = Tasktype


class TaskTypeDeleteView(SWDeleteView):
    model = Tasktype

class TaskTypelistCreativeView(SWCreateView):
    model = LSTasktypelist


class TaskTypelistDeleteView(SWDeleteView):
    model = LSTasktypelist

class TaskTypelistUpdateView(SWUpdateView):
    model = LSTasktypelist

# 獲得最大的TaskType
def getMaxTaskType(request):
    max_tasktype = LSTasktypelist.objects.all().aggregate(Max("tasktype"))["tasktype__max"]
    max_tasktype = int(max_tasktype or 0)+10
    result = {}
    result['status'] = True
    result['data'] = max_tasktype
    return JsonResponse(result, safe=False)


def download_tasktype_excel(request):
    path = os.path.join(settings.BASE_DIR, "BonusApp/excel")
    out_file = open(os.path.join(path, 'TaskTypeTemp.xls'), 'rb')
    response =StreamingHttpResponse(out_file)
    response['Content-Type'] = 'application/octet-stream' #设置头信息，告诉浏览器这是个文件
    response['Content-Disposition'] = 'attachment;filename="TaskTypeTemp.xls"'  
    out_file.close  
    return response

def import_tasktype_excel(request):    
    result = {'status':False, 'msg':'', 'data':[]}
    file = request.FILES.get('excelFile')   
    if not file:
        result['msg']='Excel文件不能為空'
    else:
        try:
            excelData:DataFrame = pd.read_excel(file.file.read())
            tasktypeList = Tasktype.objects.all()
            mapObj = {item.tasktype:item.tasktype for item in tasktypeList} 
            #newdf = dfStock.loc[dfStock["mf004"]==partno] 
            #if newdf.empty == False:  
            print(excelData.index)
            new_list = []
            for i in excelData.index:#获取行号的索引，并对其进行遍历：
                #從Excel中得到TaskType信息
                id = excelData["TaskType"].at[i]
                description = excelData["Description"].at[i]
                score = excelData["Score"].at[i]
                if not(id in mapObj.keys()):
                    tasktype = Tasktype()
                    tasktype.tasktype = id
                    tasktype.description = description
                    tasktype.score = score
                    new_list.append(tasktype)
            
            print(new_list)    
            Tasktype.objects.bulk_create(new_list)         
            result['status']=True
            result['msg']='成功導入{0}條數據'.format(len(new_list))
        except Exception as e:
            print(str(e))
            result['msg']='導入Excel失敗'
    return JsonResponse(result, safe=False) 

def get_param_value(request, param_name):
    value = None
    if param_name in request.GET:
        value = request.GET.get(param_name)
    return value
