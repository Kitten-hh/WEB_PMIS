from rest_framework import viewsets
from ..models import Chathistory
from rest_framework import permissions
from ..Serializer.ChatHistorySerializer import ChatHistorySerializer,ChatHistoryFilterSet
# from rest_framework.decorators import api_view, permission_classes
# from django.http import JsonResponse
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas

class ChatHistoryViewSet(viewsets.ModelViewSet):
    queryset = Chathistory.objects.all()
    serializer_class = ChatHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = ChatHistoryFilterSet

# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
# def save_chat(request):
#     """
#     功能描述: 用來保存用戶的AI聊天對話記錄 syl20250211
#     """
#     chatText=request.data['chatText'] #AI聊天記錄
#     username=request.data['username'] #用戶
#     pass

    # data = request.GET
    # try:
    #     number = data.get('number', 0)
    #     topic = data.get('topic', '')
    #     if topic:
    #         service = ChatTopicsServices()
    #         datas,text = service.get_chat_topic_data_text()
    #         return JsonResponse({'status':True,"result": {"text":text, "datas":datas}})
    #     else:
    #         return JsonResponse({'status':False, 'result':[]})
    # except Exception as e:
    #     print(str(e))

