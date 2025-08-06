from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..Services.SystemOperationService import SystemOperationService  
from rest_framework.permissions import AllowAny
import logging

LOGGER = logging.Logger(__name__)

class GetSimilarPagesView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        获取与用户问题相似的页面。
        """
        result = {"status":False, 'msg':"", "data":[]}
        try:
            user_question = request.data.get("user_question")
            similarity_threshold = float(request.data.get("similarity_threshold", 0.8))
            recordid = request.data.get("recordid", "")
            system_name = request.data.get("app_name", "")

            if not user_question:
                result['msg'] = "user question is required"
                return Response(result)
        
            # 调用服务方法
            service = SystemOperationService()
            similar_pages = service.get_similar_pages(user_question,recordid,system_name, similarity_threshold=similarity_threshold)
            result['status'] = True
            result['data'] = similar_pages
        except Exception as e:
            LOGGER.error(e)
        return Response(result)
