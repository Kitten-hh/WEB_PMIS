from rest_framework import viewsets
from rest_framework import permissions
from django.http import HttpRequest
from ...Serializers import TaskForAI_Serializer as TS
from ... import models
from DataBase_MPMS.models import Tasklist
from rest_framework import generics, mixins, views
from rest_framework.response import Response
from datetime import datetime
from rest_framework.decorators import api_view,permission_classes
from django.conf import settings
from BaseApp.library.tools import AsyncioTools
from django.db import transaction
from itertools import groupby
from operator import itemgetter
from django.forms.models import model_to_dict
import logging
from ...Services.PromptSqlService import PromptSqlService,PromptSqlName
from ...Services.TaskForAIService import TaskForAIService
from urllib.parse import urlparse
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from django.db.models import Sum,Count,Max,Min,Avg,Q
import json

LOGGER = logging.Logger(__name__)

class ChattopictblViewSet(viewsets.ModelViewSet):
    """
    API端點， 允許有權限的情況下, 操作Chat Topic， 支持http 
    Options:查看返回值的類型及描述信息
    """
    queryset = models.Chattopictbl.objects.all()
    serializer_class = TS.ChattopictblSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = TS.ChattopictblFilterSet

class PrompttblViewSet(viewsets.ModelViewSet):
    """
    API端點， 允許有權限的情況下, 操作Chat Prompt， 支持http 
    Options:查看返回值的類型及描述信息
    """
    queryset = models.Prompttbl.objects.all()
    serializer_class = TS.PrompttblSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = TS.PrompttblFilterSet

class PromtsqlViewSet(viewsets.ModelViewSet):
    """
    API端點， 允許有權限的情況下, 操作Chat Topic， 支持http 
    Options:查看返回值的類型及描述信息
    """
    queryset = models.Promtsql.objects.all()
    serializer_class = TS.PromtsqlSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = TS.PromtsqlFilterSet        

@api_view(['GET'])      
@permission_classes([permissions.IsAuthenticated])
def getDataWithPromtSql(request):
    result = {"status":False, "msg":"", "data":[]}
    try:
        name = request.GET.get("name", "")
        params = request.GET.get("params", "{}")
        params = json.loads(params)
        if name:
            service = PromptSqlService();
            data = service.getData(name, params)
            result['data'] = data
            result['status'] = True
    except Exception as e:
        LOGGER.error(e)
    return Response(result)

@api_view(['POST'])      
@permission_classes([permissions.IsAuthenticated])
def expandPromptData(request):
    result = {"status":False, "msg":"", "data":""}
    try:
        promptText = request.POST.get("promptText", "")
        if promptText:
            service = TaskForAIService()
            data,sessionid = service.expandPromptData(promptText)
            result['data'] = data
            result['sessionId'] = sessionid
            result['status'] = True
    except Exception as e:
        LOGGER.error(e)
    return Response(result)

@api_view(['POST'])      
@permission_classes([permissions.IsAuthenticated])
def generateTaskWithAiResult(request):
    result = {"status":False, "msg":"", "data":""}
    try:
        resultStr = request.POST.get("resultStr", "")
        sessionId = request.POST.get("sessionId", "")
        parentSessionId = request.POST.get("parentSessionId", "")
        service = TaskForAIService()
        if resultStr:
            if sessionId:
                arr = sessionId.split('-')
                pid = arr[0]
                tid = arr[1]
                session = Tasklist.objects.filter(pid=pid, tid=tid)
                if len(session) == 0:
                    result['msg'] = "Session is not exists!"
                    return Responst(result)
            service.generateTaskWithAiResult(resultStr, parentSessionId, sessionId, request)
            result['status'] = True
    except Exception as e:
        LOGGER.error(e)
    return Response(result)

@api_view(['POST'])      
@permission_classes([permissions.IsAuthenticated])
def getPromptAnswerData(request):
    result = {"status":False, "msg":"", "data":[]}
    try:
        promptName = request.data.get("promptName", "")
        id = request.data.get("id","")
        params = request.data.get("params","{}")
        params = json.loads(params)
        service = PromptSqlService()
        data = service.getData(promptName, params, id)
        result['data'] = data
        result['status'] = True
    except Exception as e:
        LOGGER.error(e)
    return Response(result)    

@api_view(['GET'])      
@permission_classes([permissions.IsAuthenticated])
def generatePrompt(request):
    result = {'status':False, 'msg':"", 'data':[]}
    try:
        topicid = int(request.GET.get("topicid", "10"))
        cid = int(request.GET.get("cid", "100"))
        con_category = request.GET.get("categoryno", "")
        # 查找最大PID
        max_pid = models.Prompttbl.objects.filter(topicid=topicid, cid=cid).aggregate(Max('pid'))['pid__max']
        if max_pid is None:
            max_pid = 0  # 如果沒有找到則設置為0

        # 查找已存在的Topic和Category
        existing_prompt = models.Prompttbl.objects.filter(topicid=topicid, cid=cid).first()
        if existing_prompt:
            topic = existing_prompt.topic
            category = existing_prompt.category
        else:
            topic = 'Management'
            category = 'Task Managements'

        # 查詢PromtSQL中IsAi=True的記錄
        sql_records = models.Promtsql.objects.filter(isapproved=True)
        if category:
            sql_records = sql_records.extra(where=["rtrim(ltrim(category))=%s"], params=[con_category])
        records = []
        for record in sql_records:
            new_prompt = models.Prompttbl(
                topicid=10,
                cid=40,
                pid=max_pid + 1,
                topic=topic,
                category=category,
                prompt=record.sname,
                post_bool='Y',
                predefined_questions=record.sname
            )
            max_pid += 1  # 更新PID以便下次使用
            records.append(new_prompt)
        result['status'] = True
        result['data'] = [model_to_dict(item) for item in records]
    except Exception as e:
        LOGGER.error(e)
    return Response(result)

@api_view(['GET'])      
@permission_classes([permissions.IsAuthenticated])
def getTaskCategory(request):
    result = {'status':False, 'msg':"", 'data':[]}
    try:
        # qs = models.Promtsql.objects.values('category').filter(isapproved=True).extra(where=["isnull(category,'')<>''"]).distinct()
        qs = models.PromptcategoryTbl.objects.all().values('categoryno','category')
        result['status'] = True
        result['data'] = [{'categoryno': item['categoryno'], 'category': item['category'].strip()} for item in qs]
    except Exception as e:
        LOGGER.error(e)
    return Response(result)


@api_view(['GET'])      
@permission_classes([permissions.IsAuthenticated])
def getActionPage(request):
    def is_valid_url(url):
        try:
            result = urlparse(url)
            if result.scheme and result.netloc:
                return True
            else:
                return False
        except ValueError:
            return False    
    result = {"status":False, "msg":"", "data":[]}
    try:
        topicid = request.GET.get("topicid", "")
        cid = request.GET.get("cid", "")
        pid = request.GET.get("pid", "")
        params = request.POST.get("params","{}")
        params = json.loads(params)
        service = TaskForAIService()
        url = service.getActionPage(topicid, cid, pid, params)
        if is_valid_url(url):
            result['data'] = url
            result['status'] = True
        else:
            result['status'] = False
    except Exception as e:
        LOGGER.error(e)
    return Response(result)        

@api_view(['POST'])      
@permission_classes([permissions.IsAuthenticated])
def saveToDB(request):
    result = {"status":False, "msg":"", "data":""}
    try:
        topicid = request.POST.get("topicid", "")
        cid = request.POST.get("cid", "")
        pid = request.POST.get("pid", "")
        dataStr = request.POST.get("datas", "{}")
        data = json.loads(dataStr)
        if data:
            service = TaskForAIService()
            service.saveContentToDB(topicid, cid, pid, [data])
            result['status'] = True
    except Exception as e:
        LOGGER.error(e)
    return Response(result)    
