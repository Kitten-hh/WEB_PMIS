from ..Services.DashboardService import DashboardService
from django.http import HttpRequest, JsonResponse
from BaseApp.library.tools import AsyncioTools
import logging

LOGGING = logging.Logger(__name__)

def getFlowupActiveSession(request:HttpRequest):
    """
    功能描述:獲取陳生每天需要跟進的人前3個Session
    """
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        url = AsyncioTools.get_url(request, "session_list", True)
        service = DashboardService()
        data = service.getSessionOfDate(url)
        result['status'] = True
        result['data'] = data
    except Exception as e:
        LOGGING.error(e)
    return JsonResponse(result, safe=False)