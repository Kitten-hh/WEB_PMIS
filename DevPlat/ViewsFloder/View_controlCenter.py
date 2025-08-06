
from django.conf import settings
from django.db import connections
import pyodbc
from django.http import JsonResponse, HttpResponse


def search_ControlCentre(request):
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        SessionId = request.GET.get('SessionId','')
        RecordID = request.GET.get('RecordID','')
        if SessionId!='':
            param=[SessionId]
            data=[]
            connstr = 'DRIVER={0};SERVER={1};PORT=1433;DATABASE={2};UID={3};PWD={4};TDS_Version={5};'.format('FreeTDS','192.168.2.200','hxp','dbname','sqlsinghc','7.1')
            ##創建數據庫連接對象
            conn = pyodbc.connect(connstr)
            with conn.cursor() as cursor:     
                # 從每日考勤表中統計上班天數           
                sql = "SELECT * FROM V_ControlCentre WHERE SessionId=?"
                cursor.execute(sql,param)
                fields = [field[0] for field in cursor.description]
                for item in cursor.fetchall():  
                    data.append(dict(list(zip(fields, item))))
            result['data'] = data
            result['status'] = True
        else:
            result['msg'] = 'data'
    except Exception as e:
        print(str(e))
    return JsonResponse(result, safe=False)
    