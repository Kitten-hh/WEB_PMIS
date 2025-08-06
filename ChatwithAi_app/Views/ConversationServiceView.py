from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.permissions import AllowAny
from ..Services.ConversationServices import ConversationService
from ..Services.ConversationServicesOld import ConversationService as ConversationServiceOld

class ConversationServiceView(APIView):
    permission_classes = [AllowAny]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 实例化 ConversationService
        self.conversation_service = ConversationService()

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        user_input = request.data.get('user_input')

        if not user_id or not user_input:
            return Response({'error': 'Missing user ID or user input'}, status=status.HTTP_400_BAD_REQUEST)

        response = self.conversation_service.handle_conversation(user_id, user_input)
        return Response({'response': response}, status=status.HTTP_200_OK)
    

class ConversationServiceViewOld(APIView):
    permission_classes = [AllowAny]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 实例化 ConversationService
        self.conversation_service = ConversationServiceOld()

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        user_input = request.data.get('user_input')

        if not user_id or not user_input:
            return Response({'error': 'Missing user ID or user input'}, status=status.HTTP_400_BAD_REQUEST)

        response = self.conversation_service.handle_conversation(user_id, user_input)
        return Response({'response': response}, status=status.HTTP_200_OK)    