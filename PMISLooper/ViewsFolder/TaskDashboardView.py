from ..Services.TaskDashboardService import TaskDashboardService
from django.http import HttpRequest, JsonResponse
import logging
import json

LOGGER = logging.Logger(__name__)


def getData(request:HttpRequest):
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        method = request.GET.get("method","")
        service = TaskDashboardService()
        if method == "initSyspara":
            data = service.getInitSyspara(request.user.username)
            result['data'] = data
        elif method == "getAllUsers":
            data = service.getCurrentPMSUserDailyQueryAllUser()
            result['data'] = data
        elif method == "getDashBoardPara":
            dashBoardModel = request.GET.get("dashBoardModel")
            category = request.GET.get("category","")
            data = service.getDashBoardPara(dashBoardModel, category)
            result['data'] = data
        elif method == "queryFilterGetDataWithParam":
            params = json.loads(request.GET.get("params","[]"))
            data = service.queryFilterGetDataWithParam(params)
            result['data'] = data
        result['status'] = True
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)


