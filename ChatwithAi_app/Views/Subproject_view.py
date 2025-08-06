from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from DataBase_MPMS.models import Subproject,Project
from django.utils import timezone
from ..Services.SubprojectServices import SubprojectService
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_project(request):
    data = request.POST
    try:
        pid = data.get('pid', "")
        name = data.get("name","")

        if pid and name:
            qs = Project.objects.filter(pid=pid)
            if len(qs):
                service = SubprojectService()
                result = service.create_project(pid, name)
                return JsonResponse({'status':True,"data": result})
            else:
                return JsonResponse({'status':False,'msg':"The parameters passed in are incorrect!",'data':{}})
        else:
            return JsonResponse({'status':False, 'msg':"The parameters passed in are incorrect!",'data':{}})
    except Exception as e:
        print(str(e))
    return JsonResponse({'status':False, 'msg':"create project fail!",'data':{}})
