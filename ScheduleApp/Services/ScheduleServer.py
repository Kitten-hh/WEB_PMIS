from PMIS.Services.UserService import UserService
from django.conf import settings
from DataBase_MPMS import models
from BaseApp.library.tools import DateTools,ModelTools
from django.db import connections
from BaseApp.library.tools import AsyncioTools
from django.core.serializers.json import DjangoJSONEncoder
from . import ScheduleConstant as Constant
import re
from django import dispatch
import json
from django.dispatch import receiver
import threading

session_schedule_with_task_signal = dispatch.Signal()

@receiver(session_schedule_with_task_signal)
def session_schedule_with_task_signal_callback(sender, **kwargs):
    task = kwargs.get('task')
    original_task = kwargs.get("original_task", None)
    if task:
        thread = threading.Thread(target=handle_session_schedule_with_task_signal, args=(task,original_task,))
        thread.start()

def handle_session_schedule_with_task_signal(task, original_task):
    service = ScheduleServer()
    service.globalScheduleWithTask(task, original_task)

class ScheduleServer:
    def getUserScheduleSession(self, contact):
        """
        功能描述：获取用户排期的Project和Session信息
        """
        result = {}
        qs = models.VSubporjectSessionUser.objects.values('method','projectid','recordid').filter(isglobal="N", contactc=contact).order_by("-userscore")[:1]
        if len(qs) > 0:
            recordid = qs[0]['recordid']
            projectid = qs[0]['projectid']
            method = qs[0]['method']
            if method == "B" and projectid:
                sqs = models.VTasklistSchUser.objects.values("pid","tid", "sessionid").filter(pid=projectid, recordid=recordid,isglobal="N", contactc=contact).order_by("-userweight")[:1]
            else:
                sqs = models.VTasklistSchUser.objects.values("pid","tid","sessionid").filter(recordid=recordid,isglobal="N", contactc=contact).order_by("-userweight")[:1]
            if len(sqs) > 0:
                session = sqs[0]
                result[recordid] = [session]
        return result

    def callScenarioScheduleServiceBak(self, modifier):
        """
        功能描述：調用Scenario - One Person One Project One Session
        """
        partUsers = UserService.GetPartUserNames();
        url = "{0}{1}".format(settings.PMIS_REST_API_SERVER, settings.PMIS_RESTAPI_ENDPOINT['scenarioSchedule']['url'])
        methodType = settings.PMIS_RESTAPI_ENDPOINT['scenarioSchedule']['method']
        authUserName = settings.PMIS_REST_API_USERNAME
        authPasswrod = settings.PMIS_REST_API_PASSWORD
        startDate = DateTools.formatf(DateTools.now(), '%Y-%m-%d')
        params = {}
        for contact in partUsers:       
            qs = models.VSubporjectSessionUser.objects.values('method','projectid','recordid').filter(isglobal="N", contactc=contact).order_by("-userscore")[:1]
            if len(qs) > 0:
                recordid = qs[0]['recordid']
                projectid = qs[0]['projectid']
                method = qs[0]['method']
                if method == "B" and projectid:
                    sqs = models.VTasklistSchUser.objects.values("sessionid").filter(pid=projectid, recordid=recordid,isglobal="N", contactc=contact).order_by("-userweight")[:1]
                else:
                    sqs = models.VTasklistSchUser.objects.values("sessionid").filter(recordid=recordid,isglobal="N", contactc=contact).order_by("-userweight")[:1]
                if len(sqs) > 0:
                    sessionid = sqs[0]['sessionid']
                    params[contact] = {"recordId":recordid, "sessionId":sessionid, "startDate":startDate,"modifier":modifier}
        http_methods = {contact:{"url":url, "method":methodType,"basic_auth_user":authUserName, "basic_auth_password":authPasswrod, "params":{"contact":contact,**param}} for contact,param in params.items()}        
        for contact, http_method in http_methods.items():
            results = AsyncioTools.async_fetch_http_json({contact:http_method})
            for lcontact,value in results.items():
                if not value['status']:
                    result['msg'] = lcontact
                    raise Exception("對聯繫人:{0} Session:{1}排期失敗".format(lcontact, sessionId))


    def callScenarioScheduleService(self,schType,contact, modifier, exportExcel=False,returnResults=False):
        """
        功能描述：調用Scenario - One Person One Project One Session
        """
        url = "{0}{1}".format(settings.PMIS_REST_API_SERVER, settings.PMIS_RESTAPI_ENDPOINT['scenarioSchedule']['url'])
        methodType = settings.PMIS_RESTAPI_ENDPOINT['scenarioSchedule']['method']
        authUserName = settings.PMIS_REST_API_USERNAME
        authPasswrod = settings.PMIS_REST_API_PASSWORD
        params = {"scenario":schType,"contact":contact, "exportExcel":str(exportExcel).lower(),"returnResults":str(returnResults).lower()}
        http_methods = {'data':{"url":url, "method":methodType,"basic_auth_user":authUserName, "basic_auth_password":authPasswrod, "params":params}}
        response = AsyncioTools.async_fetch_http_json(http_methods)['data']
        return response
    
    def globalScheduleWithTask(self, task, original_task=None):
        """
        功能描述：任務變化時調用這個任務的Session排期
        """
        url = "{0}{1}".format(settings.PMIS_REST_API_SERVER, settings.PMIS_RESTAPI_ENDPOINT['globalScheduleWithTask']['url'])
        methodType = settings.PMIS_RESTAPI_ENDPOINT['globalScheduleWithTask']['method']
        authUserName = settings.PMIS_REST_API_USERNAME
        authPasswrod = settings.PMIS_REST_API_PASSWORD
        if task:
            task = json.loads(json.dumps(task, cls=DjangoJSONEncoder))
        if original_task:
            original_task = json.loads(json.dumps(original_task, cls=DjangoJSONEncoder))

        params = {"task":task, "original_task":original_task}
        http_methods = {'data':{"url":url, "method":methodType,"basic_auth_user":authUserName, "basic_auth_password":authPasswrod, "params":params}}
        response = AsyncioTools.async_fetch_http_json(http_methods)['data']
        return response

    def getScheduleSessionFilter(self, contact):
        """
        功能描述：獲取聯繫人的Single Session的查詢條件
        """
        strSQL = """Select top 1 A.Method,A.ProjectId,A.RecordId from SubProject A with(nolock)
                    left join SCHMM C with(nolock)
                    on C.MM001 = '{0}' and C.MM002='P' and A.RecordId = C.MM003
                    order by case when C.MM001 is null then A.Score else C.MM004 end desc""".format(contact)
        projects = []
        with connections[ModelTools.get_database(models.Task)].cursor() as cursor:
            cursor.execute(strSQL)            
            columns = [column[0].lower() for column in cursor.description]
            for row in cursor.fetchall():
                obj = dict(zip(columns, row))
                projects.append(obj)                
        result = {"recordId":"","sessionId":"","filter":"1<>1"}
        if len(projects) > 0:
            recordid = projects[0]['recordid']
            result['recordId'] = recordid
            qs = models.Syspara.objects.values('fvalue').filter(nfield="Scenario", ftype="ScheduleParams")[:1]
            topQty = 1
            if len(qs) > 0 and int(qs[0]['fvalue']) == 2:
                topQty = 2
            strSQL = """Select  top {0} A.Pid+'-'+CONVERT(VARCHAR(20), CONVERT(DECIMAL(18, 0), A.Tid)) SessionId from TaskList A with(nolock)
                CROSS APPLY (Select TOP 1 RecordId from SubProject with(nolock) where RecordId='{1}' and ProjectId like A.Pid and dbo.ValidateTid(A.Tid,Filter) = 1) B
                left join SCHMM C with(nolock)
                on C.MM001 = '{2}' and C.MM002='S' and C.MM003 = A.Pid+'-'+CONVERT(VARCHAR(20), CONVERT(DECIMAL(18, 0), A.Tid))
                order by case when C.MM001 is null then A.Weight else C.MM004 end DESC""".format(topQty,  recordid, contact)
            with connections[ModelTools.get_database(models.Task)].cursor() as cursor:
                cursor.execute(strSQL)            
                columns = [column[0].lower() for column in cursor.description]
                sessions = []
                for row in cursor.fetchall():
                    obj = dict(zip(columns, row))
                    sessions.append(obj)
                filterArr = []                
                for session in sessions:
                    sessionid = session['sessionid']
                    if not result['sessionId']:
                        result['sessionId'] = sessionid
                    sessionArr = sessionid.split("-")
                    filterArr.append(f"(Pid='{sessionArr[0]}' and Tid = '{sessionArr[1]}')")
                if len(filterArr) > 0:
                    result['filter'] =  "(" + " or ".join(filterArr) + ")"
        return result

    def getScheduleTaskQuery(self, contact):
        """
        功能描述：獲取Schedule Task的查詢條件
        """
        taskQuery = self.getScheduleSessionFilter(contact)['filter']
        filterQuerys = []
        filterQuerys.append("(" + taskQuery + ")")
        filterQuerys.append("(ISNULL(UDF09,'') = 'robert')") ##Raise by Robert
        filterQuerys.append("(ISNULL(UDF09,'') = 'sing')") ##Raise by sing
        filterQuerys.append("(ISNULL(RelationId,'') like '11580-12%%' and ISNULL(HOperation,'') = 'P')") ##Meeting P
        filterQuerys.append("(ISNULL(PARSENAME(REPLACE(relationId, '-', '.'), 2),'') like '%%7[0-9][0-9]')") ##External Request
        filterQuerys.append("(ISNULL(HOperation,'')='F')")
        return "(" + " or ".join(filterQuerys) + ")"

    def getScheduleCategoryFilterMap(self, contact):
        taskQuery = self.getScheduleSessionFilter(contact)['filter']
        filterMap = {
            Constant.SCHEDULE_SESSION:"(" + taskQuery + ")",
        }
        qs = models.Syspara.objects.filter(ftype='ScheduleParams', nfield__in=[Constant.SCHEDULE_RAISED_BY_ROBERT,Constant.SCHEDULE_RAISED_BY_SING,Constant.SCHEDULE_MEETING_P,Constant.SCHEDULE_EXTERNAL_REQUEST,Constant.SCHEDULE_FIXED_DAY]).values()
        qs = sorted(list(qs), key=lambda x:int(x['fvalue']), reverse=True)
        ##已經按優先級從大到小的順序排序好的參數列表
        for param in qs:
            if param['nfield'] == Constant.SCHEDULE_RAISED_BY_ROBERT:
                filterMap[Constant.SCHEDULE_RAISED_BY_ROBERT] = "(UDF09 = 'robert')"
            elif param['nfield'] == Constant.SCHEDULE_RAISED_BY_SING:
                filterMap[Constant.SCHEDULE_RAISED_BY_SING] = "(UDF09 = 'sing')"
            elif param['nfield'] == Constant.SCHEDULE_MEETING_P:
                filterMap[Constant.SCHEDULE_MEETING_P] = "(RelationId like '11580-12%%' and HOperation = 'P')"
            elif param['nfield'] == Constant.SCHEDULE_EXTERNAL_REQUEST:
                filterMap[Constant.SCHEDULE_EXTERNAL_REQUEST] = "(PARSENAME(REPLACE(relationId, '-', '.'), 2) like '%%7[0-9][0-9]')"
            elif param['nfield'] == Constant.SCHEDULE_FIXED_DAY:
                filterMap[Constant.SCHEDULE_FIXED_DAY] = "(ISNULL(HOperation,'')='F')"
        return filterMap              
    
    def getScheduleTaskRangeFilter(self, queryset):
        """
        功能描述：獲取排期任務範圍，去掉狀態限制
        """
        rs = models.Syspara.objects.filter(ftype='ScheduleParams', nfield='NormalTaskRangeFilter');
        if len(rs) > 0:
            filter = rs[0].fvalue.replace('%', '%%');
            pattern = re.compile(r"CHARINDEX\(ISNULL\(Progress[^=]+", re.IGNORECASE)
            match = pattern.match(filter)
            if match:
                filter = filter.replace(match.group(0),"CHARINDEX(ISNULL(Progress,'N'), '')")
            return queryset.extra(where=[filter])
        return queryset        
    