from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..Services.AiEmbeddingService import AiEmbeddingService
from ..Services.ActionService import ActionService
from rest_framework.permissions import AllowAny
import logging

class GetSimilarActionsView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        """
        REST API 用于获取相似的 actions。
        """
        result = {"status":False, 'msg':"", "data":{}}
        try:
            user_question = request.data.get("question")
            similarity_threshold = float(request.data.get("similarity_threshold", 0.8))
            if not user_question:
                result['msg'] = "user question is required"
                return Response(result)
            
            ai_service = AiEmbeddingService()
            similar_actions = ai_service.get_similar_actions(user_question, similarity_threshold)
            result['status'] = True
            result['data'] = similar_actions
        except Exception as e:
            result['msg'] = str(e)
        return Response(result)


class GetActionView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        """
        REST API 用于获取相似的 actions。
        """
        result = {"status":False, 'msg':"", "data":{}}
        try:
            user_question = request.data.get("question")
            context_params = request.data.get("context_params", "empty")
            similarity_threshold = float(request.data.get("similarity_threshold", 0.8))
            if not user_question:
                result['msg'] = "user question is required"
                return Response(result)
            
            ai_service = ActionService()
            similar_actions = ai_service.ai_identify_action(user_question,context_params, similarity_threshold)
            result['status'] = True
            result['data'] = similar_actions
        except Exception as e:
            result['msg'] = str(e)
        return Response(result)
