from enum import Enum
from .. import models
from django.db import connections,transaction
from BaseApp.library.tools import ModelTools,DateTools,AsyncioTools
from DataBase_MPMS import models as pmsModels
from django.conf import settings
import json
class PromptSqlName(Enum):
    UserRequirementForSession = "Check out project requirements" #根據Pid, Tid獲取該Session的Functional Requirement
    GetURSessionWithName = "Display Session Content" #根據RecordId, SDesp獲取Session Info
    WhatAreTheCriticalProjects = "What are the critical projects?"

class PromptSqlService:
    """
    功能描述：Promt SQL 服務，可以傳入參數獲取對應的數據
    """
    def getData(self, sqlName, params, id=None):
        """
        功能描述：根據Sql的名稱和參數獲取數據，此方法為通用方法
        """
        sqlObj = self._getSQL(sqlName, id)
        if not sqlObj.isai and not sqlObj.isapproved:
            sqlStr = sqlObj.ssql
            sqlParamNames = sqlObj.params
            sqlParams = []
            if sqlParamNames:
                for pn in sqlParamNames.split(","):
                    if pn.find("==") != -1:
                        pnAttr = pn.split("==")
                        pnName = pnAttr[0]
                        if pnName in params:
                            sqlParams.append(params[pnName])
                    else:
                        if pn in params:
                            sqlParams.append(params[pn])
            with connections[ModelTools.get_database(models.Promtsql)].cursor() as cursor:
                cursor.execute(sqlStr, sqlParams)
                columns = [column[0].lower() for column in cursor.description]
                results = []
                for row in cursor.fetchall():
                    obj = dict(zip(columns, row))
                    results.append(obj)        
                return results
        else:            
            url = "{0}/looper/session_manager/get_tasks".format(settings.WEBPMIS_SERVER)
            http_methods = {'url':url,'method':'GET', 'params':{'condition':sqlObj.inc_id,'question':sqlObj.sname}}
            response = AsyncioTools.async_fetch_http_json({"data":http_methods})
            result = response['data']
            if result['status']:
                return result['data']
            else:
                return []
            

    def getDataWithError(self, sqlName, params):
        """
        功能描述：根據Sql的名稱和參數獲取數據，此方法為通用方法
        """
        try:
            sqlObj = self._getSQL(sqlName)
            sqlStr = sqlObj.ssql
            sqlParamNames = sqlObj.params
            sqlParams = []
            notExistParamNames = []
            if sqlParamNames:
                for pn in sqlParamNames.split(","):
                    if pn.find("==") != -1:
                        pnAttr = pn.split("==")
                        pnName = pnAttr[0]
                        if pnName in params:
                            sqlParams.append(params[pnName])
                        else:
                            notExistParamNames.append(pnName)
                    else:
                        if pn in params:
                            sqlParams.append(params[pn])
                        else:
                            notExistParamNames.append(pn)
            with connections[ModelTools.get_database(models.Promtsql)].cursor() as cursor:
                cursor.execute(sqlStr, sqlParams)
                columns = [column[0].lower() for column in cursor.description]
                results = []
                for row in cursor.fetchall():
                    obj = dict(zip(columns, row))
                    results.append(obj)        
                return True,results,[]
        except Exception as e:
            print(str(e))
            return False,[],notExistParamNames

    def _getSQL(self, sqlName, id=None):
        """
        功能描述：根據Sql名稱獲取SQL, 沒有則拋出沒有該Sql的異常
        """
        ##qs = models.Promtsql.objects.get(sname=sqlName)
        if id:
            qs = models.Promtsql.objects.filter(inc_id=id)[:1]
        else:
            qs = models.Promtsql.objects.filter(sname=sqlName)[:1]
        return qs[0]