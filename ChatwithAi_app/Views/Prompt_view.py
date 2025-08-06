from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from DataBase_MPMS.models import Task
from django.utils import timezone
from ..Services.SubprojectServices import SubprojectService
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
import json
from django.db import transaction
from BaseApp.library.tools import ModelTools,DateTools
from PMIS.Services.TaskService import TaskService

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def save_prompt(request):
    result = {"status":False, 'msg':"","data":[]}
    data = request.POST
    try:
        promptStr = data.get('prompts', "[]")
        prompts = json.loads(promptStr)
        sessionid = data.get("sessionid", "")
        if sessionid and len(sessionid.split("-")) == 2:
            arr = sessionid.split("-")
            old_tasks = Task.objects.values('inc_id').filter(pid=arr[0], tid = arr[1])
            old_inc_ids = [item['inc_id'] for item in old_tasks]
            cur_inc_ids = [item['inc_id'] for item in prompts]
            updateTasks = []
            deleteTasks = []
            createTasks = []
            for prompt in prompts:
                inc_id = prompt['inc_id']
                task = prompt['task']
                if inc_id:
                    task = Task(inc_id=inc_id, task=task)
                    updateTasks.append(task)
                else:
                    task = Task(pid=arr[0], tid=arr[1], contact='sing',task=task, 
                        planbdate=DateTools.now(), planedate=DateTools.now(), progress='N')
                    createTasks.append(task)
            
            deleteTasks = list(filter(lambda x: x not in cur_inc_ids, old_inc_ids))
            with transaction.atomic(ModelTools.get_database(Task)):
                Task.objects.filter(inc_id__in = deleteTasks).delete()
                Task.objects.bulk_update(updateTasks, fields=['task'], batch_size=50)
                for task in createTasks:
                    task.taskid = TaskService.get_max_taskid(arr[0], arr[1])
                    task.save()
            result['status'] = True
    except Exception as e:
        print(str(e))
    return JsonResponse(result, safe=False)
