
from DataBase_MPMS import models
from django.http import JsonResponse
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

def get_syspara(request):
    result = {'msg': '', 'data': [], 'status': False}
    try:
        nfield = request.GET.get('nfield', '')
        ftype = request.GET.get('ftype', '')
        queries = []
        if nfield:
            queries.append(Q(nfield=nfield))
        if ftype:
            queries.append(Q(ftype=ftype))
        query = Q(*queries) if queries else Q()
        data = models.Syspara.objects.filter(query)
        result.update({'status': True, 'data': list(data.values())})
    except Exception as e:
        error_msg = f'獲取數據失敗: {repr(e)}'
        logger.error(error_msg)
        result['msg'] = error_msg
    return JsonResponse(result)




