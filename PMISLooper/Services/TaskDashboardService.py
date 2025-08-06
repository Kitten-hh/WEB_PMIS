from BaseApp.library.tools import AsyncioTools
import requests
import pyamf
from pyamf import remoting,AMF3,TypedObject,register_class
from pyamf.flex import messaging,ObjectProxy
from django.conf import settings
from pyamf.remoting import Response as AmfResponse
import uuid
import logging
import json
LOGGER = logging.Logger(__name__)

class QueryfilterKey:
    def __init__(self, dictValue):
        self.qf001 = None if not dictValue else int(dictValue['qf001'])
        self.qf002 = None if not dictValue else int(dictValue['qf002'])
        self.qf006 = None if not dictValue else dictValue['qf006']
        self.qf009 = None if not dictValue else dictValue['qf009']
        self.qf010 = None if not dictValue else dictValue['qf010']
register_class(QueryfilterKey, "com.shingwai.webpms.bean.QueryfilterKey")

class DashBoardPara:
    def __init__(self, dictValue):
        self.db001 = dictValue['db001']
        self.db002 = dictValue['db002']
        self.db003 = dictValue['db003']
        self.db004 = dictValue['db004']
        self.db005 = dictValue['db005']
        self.db006 = dictValue['db006']
        self.db007 = dictValue['db007']
        self.db008 = int(dictValue['db008'])
        self.db009 = dictValue['db009']
        self.db010 = dictValue['db010']
        self.db011 = dictValue['db011']
        self.db012 = dictValue['db012']
        self.db013 = dictValue['db013']
register_class(DashBoardPara, "com.shingwai.webpms.bean.DashBoardPara")        

class RemoteObjectTools:
    def __init__(self, serverUrl, serverName, globalParams=None):
        self.serverUrl = serverUrl
        self.serverName = serverName
        self.globalParams = globalParams
    
    def getObj(self,id):
        """
        功能描述:使用id獲取對象
        """
        java_object = ObjectProxy(id)
        response = self.call_remote_server("getObj", id)
        return response

    def find(self,dictValue):
        """
        功能描述：依map條件得數據,eg map["tc001"]="wang",得tcoo1='wang'的記錄
        """
        response = self.call_remote_server("find", dictValue)
        return response

    def call_remote_server(self, operation, params):
        localParams = []
        if params:
            if type(params) == list:
                localParams.extend(params)
            else:
                localParams.append(params)
        if self.globalParams:
            localParams.extend(self.globalParams)
        msg = messaging.RemotingMessage(operation=operation,
                                   destination=self.serverName,
                                   messageId=self.serverName,
                                   body=localParams)
        req = remoting.Request(target=self.serverUrl, body=[msg])
        ev = remoting.Envelope(AMF3)
        ev['/0'] = req

        # Encode request
        bin_msg = remoting.encode(ev)        

        resp = requests.get(self.serverUrl,
                        data=bin_msg.getvalue(),
                        headers={'Content-Type': 'application/x-amf'})

        # Decode response
        resp_msg = remoting.decode(resp.content)
        return self.handle_respnose(resp_msg)

    def handle_respnose(self, response):
        response = AmfResponse(response.items()[0][1])
        if response.body:
            if type(response.body.body) == messaging.ErrorMessage:
                LOGGER.error(response.body.body)
                raise Exception("{0}-{1}".format(response.body.body.faultString, response.body.body.faultDetail))
            else:
                if type(response.body.body.body) == TypedObject:
                    return dict(response.body.body.body)
                else:
                    return list(response.body.body.body)
        else:
            return None

class TaskDashboardService:
    """
    功能描述：實現CRM任務看板相關業務邏輯
    """
    def __init__(self, *args, **kwargs):
        self.endpoint = "/messagebroker/amf"
        self.server_url = "{0}{1}".format(settings.SIMPLE_ERP_URL, self.endpoint)
        self.pms_server_url = "{0}{1}".format(settings.WEBPMS_URL, self.endpoint)
        self.sysParamService = RemoteObjectTools(self.server_url, "sysParamService", ["Mainland"])
        self.pmsUserService = RemoteObjectTools(self.pms_server_url, "pmsUserService")
        self.dashBoardParaService = RemoteObjectTools(self.pms_server_url, "dashBoardParaService")
        self.queryFilterWEBPMSService = RemoteObjectTools(self.pms_server_url, "queryFilterService")
        self.DASHBOARD_SYSPARA_TYPE = "DashBoardModel"
        self.DASHBOARD_SYSPARA_DATA = "DashBoardData"
        self.DASHBOARD_SYSPARA_STYLE = "DashBoardStyle"
        self.DASHBOARD_SYSPARA_PROJECT = "DashBoardPro" ##DashBoardPro Project
        self.DASHBOARD_SYSPARA_TASK = "DashBoardTask" ##DashBoardTask Task
        self.DASHBOARD_SYSPARA_SESSION = "DashBoardSe" ##DashBoardSe//Session
        self.DASHBOARD_GENERAL_QUERYpFILTER_CONTACT = "XXX"
        self.DASHBOARD_TIMER_INTERVAL ="DashBoInterval"
        self.PO_SYSPARA_PRICECONTROL ="poprice.control"
        self.TASKMANAGE_QUERY_INIT_SELECTED ="TaskMgs_"
        self.DASHBOARD_EXTERNAL_MODELNAME  = "dbExternalName" ##看板外部需求Model參數名稱 
        self.USER_SYSPARA_TYPE  = "User_"
        self.SESSIONPATTERM_SYSPARA = "SesPtn"
        self.APP_LOCATION_SYSPARA_NAME  = "AppLocation"
    
    def getDashboardSyspara(self):
        response = self.sysParamService.find({'CONDITION': "(ftype = 'DashBoardData')"})
        return response

    def getDashBoardPara(self, dashBoardModel, category):
        if category:
            params = f"(DB002 = '{dashBoardModel}' and DB001 = '{category}') ORDER BY DB003"
        else:
            params = f"(DB002 = '{dashBoardModel}') ORDER BY DB003"
        response = self.dashBoardParaService.call_remote_server("getDashBoardPara", params)
        return [row.__dict__ for row in response]

    def getInitSyspara(self, username):
        query = f"""(ftype='{self.DASHBOARD_SYSPARA_TYPE}') OR (nfield='{self.APP_LOCATION_SYSPARA_NAME}')
				 OR (nfield='{self.SESSIONPATTERM_SYSPARA}{username}')
				 OR (nfield='{self.DASHBOARD_TIMER_INTERVAL}') OR (ftype = '{self.DASHBOARD_SYSPARA_DATA}')
				 OR (ftype = '{self.USER_SYSPARA_TYPE}{username}') OR (nfield = '{self.DASHBOARD_EXTERNAL_MODELNAME}')
				 OR (nfield = '{self.DASHBOARD_SYSPARA_SESSION}') OR (nfield = '{self.TASKMANAGE_QUERY_INIT_SELECTED}{username}')"""    
        response = self.sysParamService.find({'CONDITION':query})
        dashBoardParas = {'dashboarTypes':[], 'interval':0, 'queryFitlerTypes':[]}
        for row in response:
            if row['ftype'] == self.DASHBOARD_SYSPARA_TYPE:
                dashBoardParas['dashboarTypes'].append(row)
            elif row['nfield'] == self.DASHBOARD_TIMER_INTERVAL:
                dashBoardParas['interval'] = int(row['fvalue'])
            elif row['nfield'] == self.DASHBOARD_SYSPARA_SESSION:
                dashBoardParas['dashboarSessionModelName'] = row['fvalue']
            elif row['ftype'] == self.DASHBOARD_SYSPARA_DATA and row['fvalue']: ##取到看板參數
                typeObj = json.loads(row['fvalue'])
                if typeObj and 'type' in typeObj:
                    item = {}
                    item['type'] = typeObj['type']
                    if 'set' in typeObj:
                        item['set'] = typeObj['set']
                    dashBoardParas['queryFitlerTypes'].append(item)
            elif row['nfield'] == self.TASKMANAGE_QUERY_INIT_SELECTED + username:
                dashBoardParas['initSyspara'] = row['fvalue']
            elif row['nfield'] == self.DASHBOARD_EXTERNAL_MODELNAME:
                dashBoardParas['externalName'] = row['fvalue']
            elif self.USER_SYSPARA_TYPE in row['ftype']:
                dashBoardParas['userSysparas'] = row['fvalue']
        return dashBoardParas
    def getCurrentPMSUserDailyQueryAllUser(self):
        """
        功能描述：獲取Task看板聯系人
        """
        response = self.pmsUserService.call_remote_server("getSameGroupUserByName", "sing")
        return response

    """
    功能描述：根據查詢條件獲取數據
    """
    def queryFilterGetDataWithParam(self, params):
        dashBoardPara = params[0];
        itemCode = -1; #看板編號
        if len(params) > 3:
            itemCode = params[3]
        if params[1]:
            key = QueryfilterKey(params[1])
        else:
            key = QueryfilterKey(None)
        params[1] = key
        params[0] = DashBoardPara(params[0])
        response = self.queryFilterWEBPMSService.call_remote_server("getQueryFilterDataWithDashBoardPara", params)
        return response