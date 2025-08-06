from django.shortcuts import render

from DataBase_MPMS import models
from django.forms.models import model_to_dict
from django.db.models import Count,Q,Case,Sum,When,IntegerField,Max
import json
import datetime
from django.http import JsonResponse,HttpResponse,HttpRequest
from BaseApp.library.tools import DateTools
from django.shortcuts import render
from BaseApp.library.tools.QueryBuilderUtils import QueryBuilderUtils
from django.urls import reverse
from DataBase_MPMS.models import Task
from django.db import transaction
import logging


LOGGER = logging.getLogger(__name__)

def batch_set_MHTask(request:HttpRequest):
    def checkDatas(Datas):
        result, msg = True, ''
        if len(Datas)==0:
            result, msg = False, '未選擇任務!'
        return result, msg
    #批量設置任務為MH
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        jsondata = json.loads(request.body)
        sessiontask = jsondata['sessiontask']
        taskList = jsondata['data']['datas']
        sync_PMS_task = []
        up_fields = ['taskcategory','udf08']
        cke_status, result['msg'] = checkDatas(taskList)
        if cke_status==False:
            return JsonResponse(result, safe=False)  
        #若存在數據，將差異數據同步
        for detail in taskList:
            taskdetail = models.Task()
            taskdetail.inc_id = detail['inc_id']
            taskdetail.taskcategory = 'MH'
            taskdetail.udf08 = sessiontask
            sync_PMS_task.append(taskdetail)

        with transaction.atomic(using='MPMS'):
            save_id = transaction.savepoint(using='MPMS')
            try:
                if len(sync_PMS_task)>0:    
                    models.Task.objects.bulk_update(sync_PMS_task, fields=up_fields, batch_size=500)
                    LOGGER.info("批量設置MH任務成功: %s", len(sync_PMS_task))
                transaction.savepoint_commit(save_id, using='MPMS')#?提交事務
            except Exception as e:
                transaction.savepoint_rollback(save_id,using='MPMS')#?事務回滾
                LOGGER.error(e)
        
        result['status'] = True
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   