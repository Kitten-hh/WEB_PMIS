from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
from django.http import JsonResponse,HttpRequest
from DataBase_MPMS import models
from DataBase_PMSDSCSYS import models as sysModels
from django.db.models import Q
from django.db.models import F
from django.db import connections,transaction
from BaseApp.library.tools import ModelTools,DateTools
import json
import logging
import suds.client
from django.conf import settings
from django.forms.models import model_to_dict
from PMIS.Services.TaskService import TaskService
from PMIS.Services.UserService import UserService
from BaseApp.library.tools import AsyncioTools
from django.db.models import ExpressionWrapper, CharField, Value
from ScheduleApp.Services.ScheduleServer import ScheduleServer
from django.utils.translation import ugettext_lazy as _
from Authorization_app.permissions.decorators_pmis import permission_required

LOGGER = logging.Logger(__name__)

class SubProjectSchView(DatatablesServerSideView):
    model = models.VSubporjectSessionUser
    columns = ['recordid','projectname','projectid','method','contactc','sqty','score','inc_id', 'userscore','contact','useronlyscore']
    searchable_columns = columns

    def get_initial_queryset(self):
        sea_contact = self.request.GET.get("sea_contact", "")
        if sea_contact:
            return self.model.objects.all().filter(isglobal="N", contactc=sea_contact)
        else:
            return self.model.objects.all().filter(isglobal="Y")

class SessionSchView(DatatablesServerSideView):
    model = models.VTasklistSchUser
    columns = ['sessionid','inc_id','sdesp','weight','contactc','userweight','allcontact','progress','progress','planbdate','planedate','taskqty','tid','udf04','capacity','contact','useronlyweight']
    searchable_columns = []
    def get_initial_queryset(self):
        queryset = self.model.objects.all()
        recordid = self.request.GET.get("recordid", "")
        if recordid:
            qs = models.Subproject.objects.values("projectid","method").filter(recordid=recordid)
            if len(qs) > 0 and qs[0]['method'] == "B" and qs[0]['projectid']:
                queryset = queryset.filter(pid=qs[0]['projectid'],recordid=recordid)
            else:
                queryset = queryset.filter(recordid=recordid)
        sea_contact = self.request.GET.get("sea_contact", "")
        if sea_contact:
            return queryset.filter(isglobal="N", contactc=sea_contact)
        else:
            return queryset.filter(isglobal="Y")
    """
    def search(self, queryset):
        ##模糊查詢
        if 'search_value' in self.config:
            if self.is_plus_search:
                queryset = self.filter_queryset_multi(self.config['search_value'], queryset)
            else:
                queryset = self.filter_queryset(self.config['search_value'], queryset)
        
        # Add per-column searches where necessary
        filter = Q()
        filter.connector = "and"
        for name, searches in self.config['column_searches'].items():
            search_value = searches['search_value']
            if searches['regex']:
                filter.children.append(('{0}__icontains'.format(name), search_value))
            else:
                filter.children.append((name, search_value))
        queryset = queryset.filter(filter)
        ##排序
        if self.config['ordering']:
            for i in  range(len(self.config['ordering'])) :
                ord = self.config['ordering'][i]
                field = ord
                if ord.startswith("-"):
                    field = ord[1:]
                if field == 'weight':
                    if ord.startswith("-"):
                        self.config['ordering'][i] = F(field).desc(nulls_last=True)        
                    else:
                        self.config['ordering'][i] = F(field).asc(nulls_last=True)
            queryset = queryset.order_by(*(self.config['ordering']));
            
        return queryset    
    """

@permission_required("ProjectSession_Prioirty", 2)
def batch_update_priority(request):
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        projectsInfo = json.loads(request.POST.get("projects", "{'priority':[],'upriority':[]}"))
        projects = projectsInfo['priority']
        user_projects = projectsInfo['upriority']
        sessionsInfo = json.loads(request.POST.get("sessions","{'weight':[], 'uweight':[]}"))
        sessions = sessionsInfo['weight']
        user_sessions = sessionsInfo['uweight']
        update_projects = []
        update_sessions = []
        for p in projects:
            project = models.Subproject()
            project.inc_id = p['inc_id']
            project.score = None if p['score'] == '' else p['score']
            update_projects.append(project)
        for s in sessions:
            sessions = models.Tasklist();
            sessions.inc_id = s['inc_id']
            sessions.weight = None if s['weight'] == '' else s['weight']
            sessions.udf04 = s['fifo']
            sessions.capacity = None if s['capacity'] == '' else s['capacity']
            update_sessions.append(sessions)   
        with transaction.atomic(ModelTools.get_database(models.Subproject)):
            models.Subproject.objects.bulk_update(update_projects, fields=['score'], batch_size=50)
            models.Tasklist.objects.bulk_update(update_sessions, fields=['weight','udf04','capacity'], batch_size=50)
            for up in user_projects:
                if up['score']:
                    models.Schmm.objects.update_or_create(mm001=up['contact'],mm002='P', mm003=up['recordid'], defaults={"mm004":up['score']})
                else:
                    models.Schmm.objects.filter(mm001=up['contact'],mm002='P', mm003=up['recordid']).delete()
            for us in user_sessions:
                if us['weight']:
                    models.Schmm.objects.update_or_create(mm001=us['contact'],mm002='S', mm003=us['sessionid'], defaults={"mm004":us['weight']})
                else:
                    models.Schmm.objects.filter(mm001=us['contact'],mm002='S', mm003=us['sessionid']).delete()

        result['status'] = True
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)

def callScheduleServiceBak(request):
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        recordId = request.GET.get("recordId")
        sessionId = request.GET.get("sessionId")
        if recordId and sessionId and len(sessionId.split("-")) == 2:
            url = "{0}/xfire/services/ScenariosScheduleService?wsdl".format(settings.SCHEDULE_SERVER)
            client=suds.client.Client(url)
            service = client.service
            startDate = DateTools.format(DateTools.now())
            arr = sessionId.split("-")
            qs = models.Task.objects.filter(pid=arr[0], tid=arr[1], progress='N').values('contact').distinct()
            sessionUsers = [item['contact'].strip().lower() for item in qs if item['contact']]
            partUsers = UserService.GetPartUserNames();
            contacts = list(filter(lambda x : x.strip().lower() in sessionUsers, partUsers))
            for contact in contacts:
                msg = service.scenariosOneSchedule(recordId, sessionId, contact, startDate)
                if msg == "N":
                    result['status'] = False
                    result['msg'] = contact
                    break
            result['status'] = True
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)

def callScheduleService(request):
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        schType = request.GET.get("schType")
        loginUserName = request.user.username
        exportExcel = request.GET.get("exportExcel", "false") == "true"
        returnResults = request.GET.get("returnResults", "false") == "true"
        contact = request.GET.get("contact","")
        server = ScheduleServer()
        if not contact:
            result['msg'] = _("The 'contact' parameter must be passed.")
        elif schType == "1" or schType == "2":
            response = server.callScenarioScheduleService(schType,contact,loginUserName, exportExcel, returnResults)
            result.update(response)
            if returnResults: #返回排期結果數據
                result['resultTasks'] = dict(sorted(result['resultTasks'].items(), key=lambda x:'0' if x[0]==loginUserName else x[0]))
            if result['status'] and not returnResults:
                singleSession = server.getScheduleSessionFilter(loginUserName)
                result.update({"recordId":singleSession['recordId'], "sessionId":singleSession['sessionId']})
        else:
            result['status'] = True                
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)    

def getSchedulePrarms(request):
    """
    功能描述：獲取排期參數
    """ 
    result = {'status':False, 'msg':'', 'data':{}}
    try:
        qs = models.Syspara.objects.filter(ftype="ScheduleParams")
        scheduleParams = [model_to_dict(row) for row in qs]
        result['data'] = scheduleParams
        result['status'] = True
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)

def updateScheduleParams(request:HttpRequest):
    """
    功能描述：更新排期參數
    """
    result = {'status':False, 'msg':"", "data":{}}
    try:
        updateData = json.loads(request.POST.get("updateData","[]"))
        with transaction.atomic(ModelTools.get_database(models.Syspara)):
            ##處理Session Params更新數據
            for row in updateData:
                models.Syspara.objects.update_or_create(ftype="ScheduleParams",nfield=row['nfield'], defaults={"fvalue":row['fvalue']})
        result['status'] = True
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)

    
def saveScheduleParamsHistory(request):
    """
    功能描述：保存排期參數歴史記錄
    """
    result = {'status': False, 'msg': '', 'data': {}}
    try:
        data = json.loads(request.POST.get("paramsData","[]"))
        name = request.POST.get("name")
        nfield = request.POST.get("nfield")
        # 保存歴史記錄到 Syspara 錶的 fvalue 字段
        if not nfield: #新增歷史記錄
            qs = models.Syspara.objects.values('nfield').filter(ftype="ScheduleParamsHistory").order_by('-nfield')[:1]
            if len(qs) > 0:
                nfield = str(int(qs[0]['nfield']) + 10).rjust(4,'0')
            else:
                nfield = '0010'
            models.Syspara.objects.create(nfield=nfield, ftype="ScheduleParamsHistory",desp=name.strip(), fvalue=json.dumps(data))
        else:
            history_record = models.Syspara.objects.update_or_create(ftype="ScheduleParamsHistory",nfield=nfield, defaults={'fvalue':json.dumps(data)})
        result['status'] = True
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)

def loadScheduleParamsFromHistory(request):
    """
    功能描述：加載排期參數歴史記錄
    """
    result = {'status': False, 'msg': '', 'data': {}}
    try:
        nfield = request.GET.get("nfield")
        # 從歴史記錄中加載到當前排期參數
        if nfield: 
            qs = models.Syspara.objects.values('fvalue').filter(ftype="ScheduleParamsHistory", nfield=nfield)[:1]
            if len(qs) > 0:
                updateData = json.loads(qs[0]['fvalue'])
                with transaction.atomic(ModelTools.get_database(models.Syspara)):
                    ##處理Session Params更新數據
                    for row in updateData:
                        models.Syspara.objects.update_or_create(ftype="ScheduleParams",nfield=row['nfield'], defaults={"fvalue":row['fvalue']})
                result['status'] = True
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)    

def delScheduleParamsFromHistory(request):
    """
    功能描述：刪除排期參數歴史記錄
    """
    result = {'status': False, 'msg': '', 'data': {}}
    try:
        nfield = request.POST.get("nfield")
        # 從歴史記錄中加載到當前排期參數
        if nfield: 
            models.Syspara.objects.filter(ftype="ScheduleParamsHistory", nfield=nfield).delete()
            result['status'] = True
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)    

def getScheduleParamsHistoryList(request):
    """
    功能描述：獲取排期參數歴史記錄列錶
    """
    result = {'status': False, 'msg': '', 'data': {}}
    try:
        qs = models.Syspara.objects.values('nfield','desp').filter(ftype="ScheduleParamsHistory")
        result['data'] = list(qs)
        result['status'] = True
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)