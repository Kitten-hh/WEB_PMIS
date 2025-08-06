from django.shortcuts import render,redirect
from django.forms.models import model_to_dict
from django.template import loader
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.db.models import Sum, Count, Max, Min, Avg, Q, Case,When,IntegerField,Max
from DataBase_MPMS import models
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.db import connections
from datatableview import helpers
from django.middleware.gzip import GZipMiddleware
import random
import pytz
from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from ..Services.GoalService import GoalService
from ..Services.SessionService import SessionService
from BaseApp.library.tools import DateTools
from BaseApp.library.cust_views.SWCreateView import SWCreateView
from BaseApp.library.cust_views.SWDeleteView import SWDeleteView
from PMIS.Services.TaskService import TaskService
import logging
from django.db import transaction
from BaseApp.library.decorators.customer_dec import cust_login_required
from django.utils.decorators import method_decorator

LOGGER = logging.Logger(__name__)


def get_mindmap_menu(request: HttpRequest):
    '''
    功能描述:獲取MindMap的分類菜單
    '''
    result = {'status': False, 'msg': '', 'data': []}
    try:
        type = request.GET.get("type")
        
        menus = models.VMindmapMenu.objects.all()
        if type:
            menus = menus.filter(menu_type=type)
        else:
            menus = menus.filter(menu_type__isnull=True)
        menus = menus.order_by('order')
        menu = [model_to_dict(menu) for menu in menus]
        result['status'] = True
        result['data'] = menu

    except Exception as e:
        LOGGER.error(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)


def get_mindmap_incId_data(request, inc_id):
    return render(request, "PMISLooper/mindmap/mindmap.html",{"inc_id":inc_id})

def get_mindmap_recordid_data(request):
    try:
        inc_id = ""
        recordid = request.GET.get("recordid","")
        if recordid:
            qs = models.Mindmap.objects.values("inc_id").filter(data__contains=f"({recordid.strip()})").extra(tables=["MindMapType"], \
                where=["MindMap.TypeId = MindMapType.INC_ID and JSON_VALUE(CAST(Data AS NVARCHAR(max)), '$.nodeDataArray[0].text') LIKE %s"], params=[f"%({recordid.strip()})%"])
            if len(qs) > 0:
                inc_id = qs[0]['inc_id']
    except Exception as e:
        LOGGER.error(str(e))

    return redirect(f"/looper/mindmap?pk={inc_id}")


def get_mindmap_data(request: HttpRequest, pk):
    '''
    功能描述:獲取MindMap的數據
    '''
    result = {'status': False, 'msg': '', 'data': []}
    try:
        rs = models.Mindmap.objects.values('data').filter(pk=pk)
        result['status'] = True
        result['data'] = rs[0]['data']
    except Exception as e:
        LOGGER.error(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class MindMapTypeCreateView(SWCreateView):
    model = models.Mindmaptype

    def get_initial(self, instance):
        '''
        功能描述：Http Get 訪問時初始化model新增時的數據
        參數說明:
            instance:該model的實例
        '''
        parentid = self.request.GET.get("parentid")
        if parentid:
            instance.parentid = parentid

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class MindMapTypeUpdateView(SWUpdateView):
    model = models.Mindmaptype

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class MindMapTypeDelView(SWDeleteView):
    model = models.Mindmaptype
    model_data = models.Mindmap

    def post(self, request, *args, **kwargs):
        result = {'status': False, 'msg': '', 'data': None}
        try:
            cids = []  # 存儲文件夾inc_id
            M_cids = []  # 存儲文件的INC_ID
            pk = request.GET.get("pk")
            all_childid = request.POST.getlist('all_childid[]')
            for cid in all_childid:
                if "M_" in cid:
                    cid = int(cid.lstrip("M_"))
                    M_cids.append(cid)
                else:
                    cid = int(cid)
                    cids.append(cid)
            if not pk:
                pk = kwargs['pk']
            old_model = self.model.objects.get(pk=pk)
            inc_old_model = self.model.objects.filter(inc_id__in=cids)
            M_inc_old_model = self.model_data.objects.filter(inc_id__in=M_cids)
            with transaction.atomic(using="MPMS"):  # 開啓事務
                save_id = transaction.savepoint(using="MPMS")  # 事務保存點
                try:
                    old_model.delete()
                    inc_old_model.delete()
                    M_inc_old_model.delete()
                    result['status'] = True
                    transaction.savepoint_commit(save_id, using="MPMS")  # 事務提交
                except Exception as k:
                    print(str(k))
                    transaction.savepoint_rollback(
                        save_id, using="MPMS")  # 事務回滾
                    result['status'] = False
                    result['msg'] = {"error": "delete fail"}
        except Exception as e:
            print(str(e))
            result['status'] = False
            result['msg'] = {
                "error": "{0} is not exist".format(self.model.__name__)}
            return JsonResponse(result, safe=False)
        return JsonResponse(result, safe=False)

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class MindMapCreateView(SWCreateView):
    model = models.Mindmap

    def get_initial(self, instance):
        '''
        功能描述：Http Get 訪問時初始化model新增時的數據
        參數說明:
            instance:該model的實例
        '''
        typeid = self.request.GET.get("typeid")
        map_type = self.request.GET.get("map_type")
        if typeid:
            instance.typeid = typeid
        if map_type:
            instance.map_type = map_type
            
@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class MindMapUpdateView(SWUpdateView):
    model = models.Mindmap

@method_decorator([cust_login_required(req_methods=["POST"])], name="dispatch")
class MindMapDelView(SWDeleteView):
    model = models.Mindmap

    def post(self, request, *args, **kwargs):
        result = {'status': False, 'msg': '', 'data': None}
        try:
            pk = request.GET.get("pk")
            if not pk:
                pk = kwargs['pk']
            old_model = self.model.objects.get(pk=pk)
            try:
                old_model.delete()
                result['status'] = True
            except Exception as k:
                print(str(k))
                result['status'] = False
                result['msg'] = {"error": "delete fail"}
        except Exception as e:
            print(str(e))
            result['status'] = False
            result['msg'] = {
                "error": "{0} is not exist".format(self.model.__name__)}
            return JsonResponse(result, safe=False)
        return JsonResponse(result, safe=False)

def get_week_active_session(request):
    username = request.GET.get('username')
    bdate = DateTools.getBeginOfWeek(DateTools.now().date())
    edate = DateTools.getEndOfWeek(DateTools.now().date())
    def get_query():
        q = Q()
        q.conditional = 'AND'
        n_q = Q()
        n_q.conditional = 'OR'
        n1_q = Q()
        n1_q.conditional = "AND"
        n2_q = Q()
        n2_q.conditional = "AND"
        n2_q.children.append(('progress__in', ['C','F']))
        n3_q = Q()
        n3_q.conditional = "AND"
        n3_q.children.append(('hoperation','F'))
        n3_q.add(~Q(progress__in=['C','F']), Q.AND)
        if username:
            q.children.append(('contact', username))
        if bdate:
            n1_q.children.append(('planbdate__gte', bdate))
            n2_q.children.append(('edate__gte', bdate))
            n3_q.children.append(('edate__lte', bdate))
        if edate:
            n1_q.children.append(('planedate__lte', edate))
            n2_q.children.append(('edate__lte', edate))
        return q & (n1_q | n2_q | n3_q)                   
    def search_active_session():
        rs = models.VTaskRecordid.objects.values('pid','tid').filter(get_query())
        rs = TaskService.getRequestQuerySetWithSysparam(rs).annotate(today_qty=Sum(
            Case(
                When(progress__in='T', then=1),
                default=0,
                output_field=IntegerField()
            ))
        ).distinct()
        return list(rs)    
    try:
        result = {'status':False, 'msg':'', 'data':None}
        if username:
            data = search_active_session()
            result['status'] = True
            result['data'] = data
    except Exception as e:
        print(str(e))
    return JsonResponse(result, safe=False)

def copy_mindmap(request):
    res = {'status': False, 'msg': '', 'data': None}
    id = request.GET.get('id','')
    target_id = request.POST.get('target_id','')
    file_name = request.POST.get('file_name','')
    try:
        qs = models.Mindmap.objects.get(pk=id)
        copy_qs = qs
        copy_qs.pk = None
        copy_qs.typeid = target_id
        if file_name != '':
            copy_qs.sdesc = file_name
        copy_qs.save()
        res['status'] = True
        res['msg'] = "複製成功"
        res['data'] = model_to_dict(copy_qs)
    except Exception as e:
        print(e)
        res['msg'] = '複製失敗'
    return JsonResponse(res,safe=False)
