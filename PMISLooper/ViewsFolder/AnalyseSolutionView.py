from django.shortcuts import render

from DataBase_MPMS import models
from django.forms.models import model_to_dict
from django.db.models import Count,Q,Case,Sum,When,IntegerField,Max
import json
import datetime
from django.http import JsonResponse,HttpResponse,HttpRequest
from datatableview import Datatable
from BaseApp.library.tools.QueryBuilderUtils import QueryBuilderUtils


def AnalyseSolutionType(request:HttpRequest):
    #分析用戶一段時間的SolutionType
    result = {'status':False, 'msg':'', 'data':[]}
    SolutionTypedata = []
    try:
        query = Buildingcondition(request)
        contcat = request.GET.get('columns[0][search][value]')
        if contcat != '':
            query.children.append(('contact', contcat))
        else:
            query.children.append(('contact', 'zyl'))
        Tecdailyplannersolutionlist = models.Tecdailyplanner.objects.filter(query).extra(
            select = {'mindMaplabel':'TecDailyPlannerSolution.mindMaplabel'},
            tables = ["TecDailyPlannerSolution"],
            where = ["TecDailyPlannerSolution.contact=TecDailyPlanner.contact and TecDailyPlannerSolution.inputdate=TecDailyPlanner.inputdate and TecDailyPlannerSolution.itemno=TecDailyPlanner.itemno"]
        ).values('contact',"mindMaplabel").annotate(Total=Count('taskno'))
        for Tecdailyplannersolution in Tecdailyplannersolutionlist:
            SolutionTypedata.append(Tecdailyplannersolution)
        result['data'] = SolutionTypedata
        result['status'] = True
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   



def AllContactSolution(request:HttpRequest):
    #獲取每個人的SolutionType數量
    result = {'status':False, 'msg':'', 'data':[]}
    SolutionTypedata = []
    try:
        query = Buildingcondition(request)
        Contactstable = models.Tecdailyplanner.objects.filter(query).values('contact').annotate(cContact=Count('contact'))
        contactquery = query
        for contacttable in Contactstable:
            contactquery.children.append(('contact', contacttable['contact']))
            taskcount = models.Tecdailyplanner.objects.filter(contactquery).values('taskno').annotate(ctaskno=Count('taskno'))
            mindmaplabelcount = models.Tecdailyplannersolution.objects.filter(contactquery).values(
                'contact','inputdate','itemno').annotate(cmindmaplabel=Count('mindmaplabel'))
            distictsolution = models.Tecdailyplannersolution.objects.filter(contactquery).values('mindmaplabel').annotate(ccontact=Count('contact'))
            solutiondata = {'contact':contacttable['contact'],'taskcount':len(taskcount),'solutioncount':len(mindmaplabelcount),'distictsolution':len(distictsolution)}
            SolutionTypedata.append(solutiondata)
            contactquery.children.remove(('contact', contacttable['contact']))
        result['data'] = SolutionTypedata
        result['status'] = True
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   


def Alldistictsolution(request:HttpRequest):
    #獲取所有人的去重的SolutionType數量
    result = {'status':False, 'msg':'', 'data':[]}
    SolutionTypedata = []
    try:
        query = Buildingcondition(request)
        alldistictsolution = models.Tecdailyplannersolution.objects.filter(query).values('mindmaplabel').annotate(ccontact=Count('contact'))
        solutiondata = {'alldistictsolution':len(alldistictsolution)}
        SolutionTypedata.append(solutiondata)
        result['data'] = SolutionTypedata
        result['status'] = True
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   



def Buildingcondition(request:object):
    search_obj = QueryBuilderUtils.getQueryFromRequest(request,'search[value]', 'form-search:')
    if search_obj:
        query = QueryBuilderUtils.json_to_query(json.dumps(search_obj))
        return query
    else:    
        query = Q()
        query.connector = "and"
        query.children.append(('inputdate__range', (datetime.datetime.now().strftime('%Y%m')+'01', datetime.datetime.now().strftime('%Y%m%d'))))
        return query

    




