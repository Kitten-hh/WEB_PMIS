from rest_framework import viewsets
from rest_framework import permissions
from django.http import JsonResponse
from DataBase_MPMS.models import Tasklist
from rest_framework import generics, mixins, views
from rest_framework.response import Response
from datetime import datetime
from rest_framework.decorators import api_view,permission_classes
from django.conf import settings
import logging
from ..Services.ChatTopicsServices import ChatTopicsServices
from urllib.parse import urlparse
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ValidationError
import json

LOGGER = logging.Logger(__name__)



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_chat_topics(request):
    data = request.GET
    try:
        number = data.get('number', 0)
        topic = data.get('topic', '')
        if topic:
            service = ChatTopicsServices()
            datas,text = service.get_chat_topic_data_text()
            return JsonResponse({'status':True,"result": {"text":text, "datas":datas}})
        else:
            return JsonResponse({'status':False, 'result':[]})
    except Exception as e:
        print(str(e))