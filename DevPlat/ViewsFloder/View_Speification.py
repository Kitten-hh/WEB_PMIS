from math import fabs
from django.db.models.base import ModelBase
from django.db.models.expressions import F
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse, response, HttpResponse
from BaseApp.library.tools import DateTools, ModelTools
from PMIS.Services.SessionService import SessionService
from DataBase_MPMS import models
from DataBase_PMSDSCSYS.models import System
import json
from django.db.models import Sum, Count, Max, Min, Avg, Q
from django.db.models.functions import Concat
from django.db.models import Value
from django.core.serializers.json import DjangoJSONEncoder
from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
from BaseApp.library.cust_views.SWCreateView import SWCreateView
from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from BaseApp.library.cust_views.SWDeleteView import SWDeleteView
from ..Services.SpecificationService import SpecificationService
from PMIS.Services.UserService import UserService
import timeago
import datetime
import re
import logging
from django.forms.models import model_to_dict
from BaseApp.library.tools import ImageTools
from BaseApp.library.decorators.customer_dec import cust_login_required
from django.utils.decorators import method_decorator
from django.db import connections
from SystemBugRpt_app.ViewsFolder.SystemBugRptView import get_admrpTable


LOGGER = logging.Logger(__name__)


class SpecTableView(DatatablesServerSideView):
    model = models.VDocma
    columns = ['ma001', 'ma002', 'ma003', 'ma018',
               'ma010', 'ma011', 'ma004c', 'ma026c']

    def get_initial_queryset(self):
        sessionid = self.request.GET.get("sessionid")
        qs = self.model.objects.all()
        if sessionid:
            arr = sessionid.split("-")
            pid = arr[0]
            tid = arr[1]
            qs = self.model.objects.extra(
                where=["exists (Select * from Task where Pid=%s and tid = %s and UDF04 = V_DOCMA.MA001)"], params=[pid, tid])
        qs = qs.extra(
            where=["MA002 = (Select Max(MA002) from DOCMA A where A.MA001 = V_DOCMA.MA001)"])
        return qs


def show_spec_pdfdoc(request: HttpRequest):
    spec_id = request.GET.get("spec_id")
    spec_seq = request.GET.get("spec_seq")
    qs = models.Docmg.objects.values("mg003").filter(
        mg001=spec_id, mg002=spec_seq)
    if len(qs) > 0:
        response = HttpResponse(qs[0]['mg003'], content_type="application/pdf")
        response.__setitem__("Content-Disposition",
                             "inline;filename="+"{0}.pdf".format(spec_id))
    else:
        response = HttpResponse(status=404)
    return response

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class SpecCreateView(SWCreateView):
    model = models.Docma

    def get_initial(self, instance: models.Docma):
        '''
        功能描述：Http Get 訪問時初始化model新增時的數據
        參數說明:
            instance:該model的實例
        '''
        instance.ma008 = UserService.GetLoginUserName(self.request)  # 創建人員
        instance.ma009 = DateTools.format(DateTools.now())  # 創建日期
        instance.ma010 = UserService.GetLoginUserName(self.request)  # 修改人
        instance.ma011 = DateTools.format(DateTools.now())  # 修改日期

    def set_max_seqno(self, instance: models.Docma):
        if instance.ma001:
            instance.ma002 = SpecificationService.get_max_verno(instance.ma001)
        else:
            instance.ma002 = None

    def save_check(self, instance: models.Docma):
        '''
        功能描述:保存前检查数据
        參數說明:
            instance:需要保存的model實例
        返回值:
            1) boolean 数据是否合法
            2) msg 数据不合法的原因
        '''
        return True, ''


def get_max_verno(request: HttpRequest):
    result = {'status': False, 'msg': '', 'data': None}
    try:
        spec_no = request.GET.get('sepc_no')
        if spec_no:
            ver_no = SpecificationService.get_max_verno(spec_no)
            result['data'] = ver_no
            result['status'] = True
        else:
            result['status'] = False
            result['msg'] = "get max version no fail"
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)


def get_system(request: HttpRequest):
    result = {'status': False, 'msg': '', 'data': None}
    try:
        qs = System.objects.all()
        result['status'] = True
        result['data'] = [model_to_dict(sys) for sys in qs]
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class SpecUpdateView(SWUpdateView):
    model = models.Docma

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class SpecDeleteView(SWDeleteView):
    model = models.Docma


class DocmbTableView(DatatablesServerSideView):
    model = models.Docmb
    columns = ['company', 'creator', 'usr_group', 'create_date', 'modifier', 'modi_date', 'flag', 'mb001', 'mb002', 'mb003',
               'mb004', 'mb005', 'mb006', 'mb007', 'mb008', 'mb009', 'mb010', 'mb011', 'mb013', 'mb015', 'mb016', 'mb017', 'inc_id']

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class DocmbCreateView(SWCreateView):
    model = models.Docmb

    def get_initial(self, instance: models.Docmb):
        '''
        功能描述：Http Get 訪問時初始化model新增時的數據
        參數說明:
            instance:該model的實例
        '''
        instance.mb001 = self.request.GET.get("mb001")
        instance.mb002 = self.request.GET.get("mb002")
        self.set_max_seqno(instance)

    def set_max_seqno(self, instance: models.Docmb):
        if instance.mb001 and instance.mb002:
            qs = models.Docmb.objects.values('mb003').filter(
                mb001=instance.mb001, mb002=instance.mb002).order_by('-mb003')[:1]
        if len(qs) > 0:
            instance.mb003 = str(int(qs[0]['mb003']) + 1).rjust(5, '0')
        else:
            instance.mb003 = '00001'

    def save_supplement(self, instance: models.Docmb):
        '''
        功能描述:保存時設置默認值
        參數說明:
            instance:需要保存的model實例
        '''
        instance.create_date = DateTools.format(DateTools.now())
        instance.modi_date = DateTools.formatf(DateTools.now(), "%Y%m%d%H%M%S")
        instance.creator = UserService.GetLoginUserName(self.request)
        instance.modifier = UserService.GetLoginUserName(self.request)

    def convert_file_format(self, key, file):
        '''
        功能描述:轉換上傳的文件的格式,如:png to jpg
        '''
        jpg = ImageTools.PngToJpg(file)
        if jpg:
            return jpg
        else:
            file.read()    

def getDocmbImage(request:HttpRequest):
    pk = request.GET.get("pk");
    try:
        qs = models.Docmb.objects.values('mb001','mb002','mb003','mb012').filter(inc_id=pk)
        if len(qs):
            image = qs[0]['mb012']
            if image is None:
                return HttpResponse(status=404)
            else:
                IMAGE_TYPE = ["image/jpeg", "image/png", "image/jpg", "image/gif", "image/bmp"]
                response = HttpResponse(image, content_type=IMAGE_TYPE)
                response.__setitem__("Content-Disposition", "inline;filename="+\
                    "{0}-{1}-{2}".format(qs[0]['mb001'], qs[0]['mb002'], qs[0]['mb003']));
                return response 
    except Exception as e:    
        LOGGER.error(str(e));
    return HttpResponse(status=404)

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class DocmbUpdateView(SWUpdateView):
    model = models.Docmb

    def convert_file_format(self, key, file):
        '''
        功能描述:轉換上傳的文件的格式,如:png to jpg
        '''
        jpg = ImageTools.PngToJpg(file)
        if jpg:
            return jpg
        else:
            file.read()    

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class DocmbDeleteView(SWDeleteView):
    model = models.Docmb


class DocmhTableView(DatatablesServerSideView):
    model = models.VDocmhTr

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class DocmhCreateView(SWCreateView):
    model = models.Docmh

    def get_initial(self, instance: models.Docmh):
        '''
        功能描述：Http Get 訪問時初始化model新增時的數據
        參數說明:
            instance:該model的實例
        '''
        instance.mh001 = self.request.GET.get("mh001")
        instance.mh002 = self.request.GET.get("mh002")
        self.set_max_seqno(instance)

    def set_max_seqno(self, instance: models.Docmh):
        if instance.mh001 and instance.mh002:
            qs = models.Docmh.objects.values('mh003').filter(
                mh001=instance.mh001, mh002=instance.mh002).order_by('-mh003')[:1]
        if len(qs) > 0:
            instance.mh003 = str(int(qs[0]['mh003']) + 1).rjust(5, '0')
        else:
            instance.mh003 = '00001'

    def save_supplement(self, instance: models.Docmh):
        '''
        功能描述:保存時設置默認值
        參數說明:
            instance:需要保存的model實例
        '''
        instance.create_date = DateTools.format(DateTools.now())
        instance.modi_date = DateTools.formatf(DateTools.now(), "%Y%m%d%H%M%S")
        instance.creator = UserService.GetLoginUserName(self.request)
        instance.modifier = UserService.GetLoginUserName(self.request)

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class DocmhUpdateView(SWUpdateView):
    model = models.Docmh

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class DocmhDeleteView(SWDeleteView):
    model = models.Docmh


class DocmiTableView(DatatablesServerSideView):
    model = models.Docmi
    columns = ['company','creator','usr_group','create_date','modifier','modi_date','flag','mi001','mi002','mi003','mi004','mi005','mi006','mi007','mi008','mi009','mi011','mi012','mi013','mi014','mi015','inc_id']    
    
@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")    
class DocmiCreateView(SWCreateView):
    model = models.Docmi

    def get_initial(self, instance: models.Docmi):
        '''
        功能描述：Http Get 訪問時初始化model新增時的數據
        參數說明:
            instance:該model的實例
        '''
        instance.mi001 = self.request.GET.get("mi001")
        instance.mi002 = self.request.GET.get("mi002")
        self.set_max_seqno(instance)

    def set_max_seqno(self, instance: models.Docmi):
        if instance.mi001 and instance.mi002:
            qs = models.Docmi.objects.values('mi003').filter(
                mi001=instance.mi001, mi002=instance.mi002).order_by('-mi003')[:1]
        if len(qs) > 0:
            instance.mi003 = str(int(qs[0]['mi003']) + 1).rjust(5, '0')
        else:
            instance.mi003 = '00001'

    def save_supplement(self, instance: models.Docmi):
        '''
        功能描述:保存時設置默認值
        參數說明:
            instance:需要保存的model實例
        '''
        instance.create_date = DateTools.format(DateTools.now())
        instance.modi_date = DateTools.formatf(DateTools.now(), "%Y%m%d%H%M%S")
        instance.creator = UserService.GetLoginUserName(self.request)
        instance.modifier = UserService.GetLoginUserName(self.request)

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class DocmiUpdateView(SWUpdateView):
    model = models.Docmi

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class DocmiDeleteView(SWDeleteView):
    model = models.Docmi


class DocmjTableView(DatatablesServerSideView):
    model = models.Docmj

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class DocmjCreateView(SWCreateView):
    model = models.Docmj

    def get_initial(self, instance: models.Docmj):
        '''
        功能描述：Http Get 訪問時初始化model新增時的數據
        參數說明:
            instance:該model的實例
        '''
        instance.mj001 = self.request.GET.get("mj001")
        instance.mj002 = self.request.GET.get("mj002")
        self.set_max_seqno(instance)

    def set_max_seqno(self, instance: models.Docmj):
        if instance.mj001 and instance.mj002:
            qs = models.Docmj.objects.values('mj003').filter(
                mj001=instance.mj001, mj002=instance.mj002).order_by('-mj003')[:1]
        if len(qs) > 0:
            instance.mj003 = str(int(qs[0]['mj003']) + 1).rjust(5, '0')
        else:
            instance.mj003 = '00001'

    def save_supplement(self, instance: models.Docmj):
        '''
        功能描述:保存時設置默認值
        參數說明:
            instance:需要保存的model實例
        '''
        instance.create_date = DateTools.format(DateTools.now())
        instance.modi_date = DateTools.formatf(DateTools.now(), "%Y%m%d%H%M%S")
        instance.creator = UserService.GetLoginUserName(self.request)
        instance.modifier = UserService.GetLoginUserName(self.request)

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class DocmjUpdateView(SWUpdateView):
    model = models.Docmj

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class DocmjDeleteView(SWDeleteView):
    model = models.Docmj

# Docmc CRUD Views #############################################################
class DocmcTableView(DatatablesServerSideView):
    model = models.Docmc
    columns = ['company', 'creator', 'usr_group', 'create_date', 'modifier', 'modi_date', 'flag', 'mc001', 'mc002', 'mc003',
               'mc004', 'mc005', 'mc006', 'mc007', 'mc008', 'mc009', 'mc010', 'mc011', 'mc013','inc_id']

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class DocmcCreateView(SWCreateView):
    model = models.Docmc

    def get_initial(self, instance: models.Docmc):
        instance.mc001 = self.request.GET.get("mc001")
        instance.mc002 = self.request.GET.get("mc002")
        self.set_max_seqno(instance)

    def set_max_seqno(self, instance: models.Docmc):
        if instance.mc001 and instance.mc002:
            qs = models.Docmc.objects.values('mc003').filter(
                mc001=instance.mc001, mc002=instance.mc002).order_by('-mc003')[:1]
            if len(qs) > 0:
                instance.mc003 = str(int(qs[0]['mc003']) + 1).rjust(5, '0')
            else:
                instance.mc003 = '00001'

    def save_supplement(self, instance: models.Docmc):
        instance.create_date = DateTools.format(DateTools.now())
        instance.modi_date = DateTools.formatf(DateTools.now(), "%Y%m%d%H%M%S")
        instance.creator = UserService.GetLoginUserName(self.request)
        instance.modifier = UserService.GetLoginUserName(self.request)

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class DocmcUpdateView(SWUpdateView):
    model = models.Docmc

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class DocmcDeleteView(SWDeleteView):
    model = models.Docmc

# Docme CRUD Views #############################################################    
class DocmeTableView(DatatablesServerSideView):
    model = models.Docme
    columns = ['company', 'creator', 'usr_group', 'create_date', 'modifier', 'modi_date', 'flag', 'me001', 'me002', 'me003',
               'me004', 'me005', 'me006', 'me007', 'me008', 'me009', 'me010', 'me011', 'me013', 'me015','inc_id']

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class DocmeCreateView(SWCreateView):
    model = models.Docme

    def get_initial(self, instance: models.Docme):
        instance.me001 = self.request.GET.get("me001")
        instance.me002 = self.request.GET.get("me002")
        self.set_max_seqno(instance)

    def set_max_seqno(self, instance: models.Docme):
        if instance.me001 and instance.me002:
            qs = models.Docme.objects.values('me003').filter(
                me001=instance.me001, me002=instance.me002).order_by('-me003')[:1]
            if len(qs) > 0:
                instance.me003 = str(int(qs[0]['me003']) + 1).rjust(5, '0')
            else:
                instance.me003 = '00001'

    def save_supplement(self, instance: models.Docme):
        instance.create_date = DateTools.format(DateTools.now())
        instance.modi_date = DateTools.formatf(DateTools.now(), "%Y%m%d%H%M%S")
        instance.creator = UserService.GetLoginUserName(self.request)
        instance.modifier = UserService.GetLoginUserName(self.request)

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class DocmeUpdateView(SWUpdateView):
    model = models.Docme

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class DocmeDeleteView(SWDeleteView):
    model = models.Docme


class TaskIDTableView(DatatablesServerSideView):
    model = models.Task

    def get_initial_queryset(self):
        pid = self.request.GET.get("pid")
        tid = self.request.GET.get("tid")
        return self.model.objects.filter(pid=pid, tid=tid)

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class TaskSaveDocwin(SWUpdateView):
    model = models.Task

    def post(self, request, *args, **kwargs):
        result = {'status':False, 'msg':'', 'data':None}
        try:
            pid = request.POST.get("pid")
            tid = request.POST.get("tid")
            taskid = request.POST.get("taskid")
            udf04 = request.POST.get("udf04")
            old_model = self.model.objects.filter(pid=pid,tid=tid,taskid=taskid)
            old_model.update(udf04=udf04)
            result['status'] = True
            result['msg'] = "保存成功"
        except Exception as e:
            result['status'] = False
            result['msg'] = {"error":"{0} is not exist".format(self.model.__name__)}
            return JsonResponse(result, safe=False)
        return JsonResponse(result, safe=False)  

def get_external_problems(request: HttpRequest):
    """获取窗口文档关联的外部系统问题单"""
    result = {"draw": 1, "recordsTotal": 0, "recordsFiltered": 0, "data": []}
    try:
        # 获取基础参数
        ma001 = request.GET.get("ma001")
        ma002 = request.GET.get("ma002")
        

        # 执行原始SQL查询
        with connections[ModelTools.get_database(models.Docma)].cursor() as cursor:
            cursor.execute("""
                WITH RequestExternalProblem AS (
				Select                 
				PARSENAME(REPLACE(MI005, '-', '.'), 3) Pid,
                TRY_CAST(PARSENAME(REPLACE(MI005, '-', '.'), 2) AS float) Tid,
                TRY_CAST(PARSENAME(REPLACE(MI005, '-', '.'), 1) AS float) TaskId,
				B.relationID
				from DOCMI A
				inner join Task B
				on B.Pid = PARSENAME(REPLACE(MI005, '-', '.'), 3)  and B.Tid = TRY_CAST(PARSENAME(REPLACE(MI005, '-', '.'), 2) AS float) 
				and B.TaskId = TRY_CAST(PARSENAME(REPLACE(MI005, '-', '.'), 1) AS float)
				where MI001=%s and MI002=%s
            ),
            SessionExternalProblem As (
                Select A.Pid,A.Tid,A.TaskId,A.relationID from Task A
                inner join RequestExternalProblem B
				on
                PARSENAME(REPLACE(B.relationId, '-', '.'), 3) = A.Pid and
                TRY_CAST(PARSENAME(REPLACE(B.relationId, '-', '.'), 2) AS float) = A.Tid and
                TRY_CAST(PARSENAME(REPLACE(B.relationId, '-', '.'), 1) AS float) = A.TaskId
            ),
			ProjectExternalProblem As (
                Select A.Pid,A.Tid,A.TaskId,A.relationID from Task A
                inner join SessionExternalProblem B
				on
                PARSENAME(REPLACE(B.relationId, '-', '.'), 3) = A.Pid and
                TRY_CAST(PARSENAME(REPLACE(B.relationId, '-', '.'), 2) AS float) = A.Tid and
                TRY_CAST(PARSENAME(REPLACE(B.relationId, '-', '.'), 1) AS float) = A.TaskId
			),
            AllExternalProblem As (
                 Select A.Pid,A.Tid,A.TaskId,A.relationID from Task A
                inner join ProjectExternalProblem B
				on
                PARSENAME(REPLACE(B.relationId, '-', '.'), 3) = A.Pid and
                TRY_CAST(PARSENAME(REPLACE(B.relationId, '-', '.'), 2) AS float) = A.Tid and
                TRY_CAST(PARSENAME(REPLACE(B.relationId, '-', '.'), 1) AS float) = A.TaskId
            )
			Select distinct B.UDF01 from (
            Select * from RequestExternalProblem
            union
            Select * from SessionExternalProblem
            union
            Select * from ProjectExternalProblem
			union
			Select * from AllExternalProblem
			) A
			inner join Task B
			on A.Pid=B.Pid and A.Tid = B.Tid and A.TaskId = B.TaskId 
			where ISNULL(B.UDF01,'') <> ''
            """, [ma001, ma002])
            udf_list = [row[0] for row in cursor.fetchall()]

        # 调用SystemBugRptView获取详细数据
        bug_request = HttpRequest()
        bug_request.GET = request.GET.copy()
        bug_request.method = "GET"
        attach_query = {
            "condition": "AND",
            "rules": [{"id": "me001", "field": "rp017", "type": "string", "input": "text", "operator": "in", "value": udf_list}],
            "not": False,
            "valid": True
        }
        bug_request.GET['attach_query'] = json.dumps(attach_query)        
        bug_request.GET['draw'] = 1
        bug_request.GET['start'] = 0
        bug_request.GET['length'] = -1
        response = get_admrpTable(bug_request)
        
        # 合并结果
        if response.status_code == 200:
            result.update(json.loads(response.content))
            result["draw"] = 1
        
    except Exception as e:
        LOGGER.error(f"获取外部问题单失败: {str(e)}")
        result["error"] = str(e)
    
    return JsonResponse(result)
