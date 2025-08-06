from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,JsonResponse,HttpRequest
from django.db.models import Sum,Count,Max,Min,Avg,Q
from django.forms.models import model_to_dict
from BaseApp.library.cust_views.SWDeleteView import SWDeleteView
from DataBase_MPMS.models import Tasklist,Task,VTasklistS
from ..models import TasklistRelation
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from BaseApp.library.decorators.customer_dec import cust_login_required
import json
import logging
from django.utils.translation import ugettext_lazy as _

LOGGER = logging.Logger(__name__)


@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class TaskListDeleteView(SWDeleteView):
    model = Tasklist

    def delete_check(self, instance):
        '''
        功能描述:刪除前检查数据
        參數說明:
            instance:需要刪除的model實例
        返回值:
            1) boolean 数据是否合法
            2) msg 数据不合法的原因
        '''
        existsTask = Task.objects.filter(pid=instance.pid, tid=instance.tid).exists()
        if existsTask:
            return False, _('This session contains tasks and cannot be deleted!')
        else:
            return True, ''


def getSessionRelationInfo(request):
    result = {'status':False, 'msg':"", 'data':[]}
    try:
        sessionid = request.GET.get("sessionid")
        if sessionid:
            arr = sessionid.split("-")
            pid = arr[0]
            tid = arr[1]
            qs = TasklistRelation.objects.values("relationsessionid").filter(pid=pid, tid=tid)[:1]
            recordid = None
            relationsessionid = None
            if len(qs) > 0:
                relationsessionid = qs[0]['relationsessionid']
                if relationsessionid:
                    rarr = relationsessionid.split("-")
                    rpid = rarr[0]
                    rtid = rarr[1]
                    qs = VTasklistS.objects.values("recordid").filter(pid=rpid, tid=rtid)[:1]
                    if len(qs) > 0:
                        recordid = qs[0]['recordid']              
        result['status'] = True
        result['data'] = {'recordid':recordid, 'relationsessionid':relationsessionid}
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)
