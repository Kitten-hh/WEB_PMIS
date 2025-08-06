from math import fabs
from django.db import models
from django.shortcuts import render
from django.http import HttpRequest,JsonResponse
from BaseApp.library.cust_views.SWCreateView import SWCreateView
from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from BaseApp.library.cust_views.SWDeleteView import SWDeleteView
from DataBase_MPMS.models import Requirement, Syspara, VTask, Subproject, Tasklist, Tecrequiremnt
from django.db.models import Sum,Count,Max,Min,Avg,Q, query
from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
from BaseApp.library.tools import DateTools
from PMIS.Services.UserService import UserService
import logging
from BaseApp.library.decorators.customer_dec import cust_login_required
from django.utils.decorators import method_decorator

LOGGER = logging.Logger(__name__)

class RequirementCreateView(SWCreateView):
    model = Requirement

    def get_initial(self, instance):
        '''
        功能描述：Http Get 訪問時初始化model新增時的數據
        參數說明:
            instance:該model的實例
        '''
        if self.get_initial_with_session(instance) or self.get_initial_with_recordid(instance):
            pass

    def get_initial_with_session(self, instance:Requirement):
        sessionid = self.request.GET.get("sessionid")
        if sessionid:
            session_arr = sessionid.split("-");
            pid = session_arr[0]
            tid = session_arr[1]
            qs = Tasklist.objects.values('pid').filter(pid=pid, tid=tid)
            if len(qs) > 0:
                instance.rid = sessionid
                instance.session_id = sessionid
                instance.rt = 'S'; ##sesson的默認類型為S
                return True
            else:
                raise Exception("沒有sessionid:{0}的session".format(sessionid));
        else:
            return False    

    def get_initial_with_recordid(self, instance:Requirement):
        recordid = self.request.GET.get("recordid")
        if recordid:
            qs = Subproject.objects.values("recordid").filter(recordid=recordid)
            if len(qs) > 0:
                instance.rid = recordid
                instance.rt = 'P'; ##sesson的默認類型為S
            else:
                raise Exception("沒有recordid:{0}的子工程".format(recordid));
        else:
            return False    

class RequirementUpdateView(SWUpdateView):
    model = Requirement

    def get_object_with_params(self, request_data):
        rid = request_data.get("rid")
        return Requirement.objects.filter(rid=rid)[:1][0]    

class RequirementDeleteView(SWDeleteView):
    model = Requirement


class RequirementTableView(DatatablesServerSideView):
    model = Requirement

def get_requirement_type(request:HttpRequest):
    
    result = {'status':False, 'msg':'', 'data':None}
    data = []
    try:
        qs = Syspara.objects.values('fvalue').filter(nfield='ReqType', ftype='DevelopmentCycle')
        if len(qs):
            value = qs[0]['fvalue']
            value_arr = value.split(";")
            for v in value_arr:
                v_arr = v.split(":")
                data.append({"value":v_arr[0], 'label':v_arr[1]})
        result['status'] = True
        result['data'] = data
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)
    
def get_requirement_task(request:HttpRequest):
    result = {'status':False, 'msg':'', 'data':None}
    sessionid = request.GET.get("sessionid");
    data = []
    try:
        session = sessionid.split("-")
        pid = session[0]
        tid = session[1];
        qs = VTask.objects.filter(pid=pid, tid=tid, taskcategory__isnull=False).order_by("taskid");
        data = [{task.category:task for task in qs}]
        result['data'] = data
        result['status'] = True
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False);

class TecRequirementTableView(DatatablesServerSideView):
    model=Tecrequiremnt

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class TecRequirementCreateView(SWCreateView):
    model=Tecrequiremnt
    def get_initial(self, instance:Tecrequiremnt):
        '''
        功能描述：Http Get 訪問時初始化model新增時的數據
        參數說明:
            instance:該model的實例
        '''
        instance.specname = self.request.GET.get("specname")
        instance.verno = self.request.GET.get("verno")
        instance.funcitemno = self.request.GET.get("funcitemno")
        self.set_max_seqno(instance)

    def set_max_seqno(self, instance:Tecrequiremnt):
        '''
        功能描述：獲取最大單號
        參數說明:
            instance:需要保存或初始化的model實例
        '''
        if instance.specname and instance.verno and instance.funcitemno:
            qs = Tecrequiremnt.objects.values("itemno").filter(specname=instance.specname, \
                verno=instance.verno, funcitemno=instance.funcitemno).order_by("-itemno")[:1]
            if len(qs) > 0:
                instance.itemno = str(int(qs[0]['itemno']) + 10).rjust(5, "0")
            else:
                instance.itemno = "00001";

    def save_supplement(self, instance):
        '''
        功能描述:保存時設置默認值
        參數說明:
            instance:需要保存的model實例
        '''
        instance.create_date = DateTools.format(DateTools.now());
        instance.modi_date = DateTools.formatf(DateTools.now(), "%Y%m%d%H%M%S")
        instance.creator = UserService.GetLoginUserName(self.request)
        instance.modifier = UserService.GetLoginUserName(self.request)            

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class TecRequirementUpdateView(SWUpdateView):
    model=Tecrequiremnt

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class TecRequirementDeleteView(SWDeleteView):
    model=Tecrequiremnt