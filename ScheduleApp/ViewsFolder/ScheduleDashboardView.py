from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
from django.http import JsonResponse,HttpRequest
from DataBase_MPMS import models
from django.db.models import Q
from django.db.models import F
from django.db import connections,transaction
from BaseApp.library.tools import ModelTools
import json
import logging

LOGGER = logging.Logger(__name__)

class ScheduleDashboardTableView(DatatablesServerSideView):
    model = models.VSubprojectSch
    columns = [field.name for field in models.VSubprojectSch._meta.fields]
    searchable_columns = columns
    
def getData(request:HttpRequest):
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        taskFilter = ""
        rs = models.Syspara.objects.filter(ftype='Query', nfield='TaskQuery');
        if len(rs) > 0:
            taskFilter = "and " +rs[0].fvalue.replace('%', '%%')
        strSql = '''SELECT A.RecordId,A.ProjectName,A.Score,A.Progress,B.GoalDesc Goal,C.* FROM V_SubProject_Expand A
            OUTER APPLY (SELECT TOP 1 GoalDesc FROM dbo.GoalManagement 
            WHERE Contact=%s AND GoalType='Q' AND RecordId=A.RecordId and Period = dbo.GetQuarterlyStr(CONVERT(VARCHAR(8),GETDATE(),112))) B
            OUTER APPLY (SELECT COUNT(*) TaskQty, SUM(CASE WHEN Progress NOT IN ('C','F') THEN 1 ELSE 0 end) OutTaskQty,
            Max(CASE WHEN Progress NOT IN ('C','F') AND ScheduleState = 'Y' THEN PlanBDate ELSE NULL END) SchFinishDate
            FROM dbo.Task WHERE 
            A.ProjectId like Pid and Tid >= A.MinTid and Tid <= A.MaxTid {0}
            ) C
            ORDER BY Score DESC'''.format(taskFilter)
        
        with connections['MPMS'].cursor() as cursor:
            cursor.execute(strSql, [request.user.username])
            columns = [column[0].lower() for column in cursor.description]
            for row in cursor.fetchall():
                obj = dict(zip(columns, row))
                result['data'].append(obj)        
        result['status'] = True;
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)