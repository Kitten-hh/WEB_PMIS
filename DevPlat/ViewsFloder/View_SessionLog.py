from DataBase_MPMS.models import Sessionlog, Syspara, VTasklistSub
from django.http.response import JsonResponse
from django.utils import timezone
from django.db.models import Case, When, Value, IntegerField

def get(request):
    res = {'status': False, 'msg':'', 'data':None, 'type_list': [], 'total': 0}
    # contact = request.GET.get('contact', '')
    sessionid = request.GET.get('sessionid', '')
    # if contact == '' or sessionid == '':
    if sessionid == '':
        res['msg'] = '沒有傳入必要的數據Session ID!'
        return JsonResponse(res)
    pid, tid = sessionid.split('-')
    # qs = Sessionlog.objects.filter(pid = pid, tid = tid, username = contact)
    qs = Sessionlog.objects.filter(pid = pid, tid = tid).annotate(
            custom_order=Case(
                When(username='sing', then=Value(0)),
                default=Value(1),
                output_field=IntegerField()
            )
        ).order_by('custom_order', 'username', 'exetime')
    syspara = Syspara.objects.filter(nfield='type_list', ftype='SeesionLog')
    if syspara.exists():
        res['type_list'] = str(syspara.first().fvalue or '').split(';')
    if qs.exists():
        res['status'] = True
        res['total'] = len(qs)
        # res['data'] = list(qs.values())[0]['action']
        res['data'] = list(qs.values())
    return JsonResponse(res)

def save(request):
    res = {'status': False, 'msg':'', 'data':None}
    contact = request.POST.get('contact', '')
    sessionid = request.POST.get('sessionid', '')
    log = request.POST.get('log', '')
    actiontype = request.POST.get('type', '')
    exetime = request.POST.get('exeTime', '')
    if contact == '' or sessionid == '':
        res['msg'] = '沒有傳入必要的數據!'
        return JsonResponse(res)
    pid, tid = sessionid.split('-')
    # qs = Sessionlog.objects.filter(pid = pid, tid = tid, username = contact)
    # if log == '': # 用戶清空了錄入的記錄則刪除創建的數據
    #    qs.delete()
    # else: 
    #     if qs.exists(): # 存在則修改
    #         qs = qs.first()
    #         qs.action = log
    #         qs.updatelogtime = timezone.now()
    #         qs.save()
    #     else:
    inst = Sessionlog() # 不存在則新增
    inst.pid = pid
    inst.tid = tid
    inst.username = contact
    inst.createlogtime = timezone.now()
    inst.action = log
    inst.actiontype = actiontype
    inst.exetime = exetime
    inst.save()
    qs = Syspara.objects.filter(nfield='type_list', ftype='SeesionLog')
    if qs.exists():
        syspara = qs.first()
        type_list = syspara.fvalue.split(';')
        if actiontype not in type_list:
            syspara.fvalue += ';' + actiontype  # 更新fvalue的值
            syspara.save()  # 保存修改
    else:
        Syspara.objects.create(nfield='type_list', ftype='SeesionLog', fvalue=actiontype)
    res['status'] = True
    return JsonResponse(res)

# ===================================上面的是原版本的代碼====================================

from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
from BaseApp.library.cust_views.SWCreateView import SWCreateView
from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from BaseApp.library.cust_views.SWDeleteView import SWDeleteView
from django.core.paginator import Paginator
from django.db.models.functions import Concat
from django.db.models import Q, F, CharField
from datetime import datetime

class SessionLogTableView(DatatablesServerSideView):
    model = Sessionlog
    columns = '__all__'

    def get_initial_queryset(self):
        sessionid = self.request.GET.get('sessionid', '-')
        username = self.request.GET.get('username', '')
        exetimeb = self.request.GET.get('exetimeb', '')
        exetimes = self.request.GET.get('exetimes', '')
        actiontype = self.request.GET.get('actiontype', '')
        action = self.request.GET.get('action', '')
        all_session = self.request.GET.get('all_session', '')
        inc_id = self.request.GET.get('inc_id', '')

        if sessionid == '':
            return self.model.objects.none()
        q = Q()
        if all_session == 'false':
            pid, tid = sessionid.split('-')
            q = Q(pid=pid, tid=tid)

        if username:
            q &= Q(username=username)

        if actiontype:
            q &= Q(actiontype=actiontype)

        if action:
            # q &= Q(action__icontains=action)
            q &= Q(action__contains=action)

        if inc_id:
            q &= Q(inc_id=inc_id)

        # 處理起始時間和結束時間的查詢條件
        if exetimeb and exetimes:
            exetime_end = datetime.strptime(exetimes, '%Y-%m-%d')
            exetime_end = exetime_end.replace(hour=23, minute=59, second=59)
            q &= Q(exetime__range=[exetimeb, exetime_end])
        elif exetimeb:  # 只有起始時間
            exetime_begin = datetime.strptime(exetimeb, '%Y-%m-%d')
            q &= Q(exetime__gte=exetime_begin)
        elif exetimes:  # 只有結束時間
            exetime_end = datetime.strptime(exetimes, '%Y-%m-%d')
            exetime_end = exetime_end.replace(hour=23, minute=59, second=59)
            q &= Q(exetime__lte=exetime_end)

        return self.model.objects.filter(q).order_by('-exetime', 'username')
    
    def customize_row(self, row, obj):
        row['sessionid'] = f'{obj.pid}-{int(obj.tid)}'
    
    def get_response_dict(self, paginator, draw_idx, start_pos):
        if isinstance(paginator,Paginator):
            page_id = (start_pos // paginator.per_page) + 1
            if page_id > paginator.num_pages:
                page_id = paginator.num_pages
            elif page_id < 1:
                page_id = 1

            objects = self.prepare_results(paginator.page(page_id))
            total_num = paginator.count
        else:
            objects = self.prepare_results(paginator)
            total_num = len(objects)
        res_json = {"draw": draw_idx, "recordsTotal": total_num, "recordsFiltered": total_num, "data": objects}
        if total_num == 0:
            sessionid = self.request.GET.get('sessionid', '-')
            username = self.request.GET.get('username', '')
            exetimeb = self.request.GET.get('exetimeb', '')
            exetimes = self.request.GET.get('exetimes', '')
            actiontype = self.request.GET.get('actiontype', '')
            action = self.request.GET.get('action', '')
            all_session = self.request.GET.get('all_session', '')
            filter_params = {}
            if all_session == 'false':
                pid, tid = sessionid.split('-')
                filter_params['pid'] = [pid, '這個模塊沒有日志'] # Session is no log
                filter_params['tid'] = [tid, '這個模塊沒有日志'] # Session is no log
            if username:
                filter_params['username'] = [username, '這個聯繫人沒有日誌'] # Contact is no log
            if exetimeb:
                filter_params['exetime__gte'] = [exetimeb, '這個起始時間沒有沒有日誌'] 
            if exetimes:
                exetime_end = datetime.strptime(exetimes, '%Y-%m-%d')
                exetime_end = exetime_end.replace(hour=23, minute=59, second=59)
                filter_params['exetime__lte'] = [exetime_end, '這個結束時間沒有沒有日誌'] #
            if actiontype:
                filter_params['actiontype'] = [actiontype, '這個類型沒有日誌']
            if action:
                filter_params['action__contains'] = [action, '這個Log詳情沒有日誌']
            query = self.model.objects.all()
            conditions = Q()
            empty_condition = None
            for key, value in filter_params.items():
                new_condition = Q(**{key: value[0]})
                new_query = query.filter(conditions & new_condition)
                if not new_query.exists():
                    empty_condition = value[1]
                    break
                conditions &= new_condition 
            if empty_condition is not None:
              res_json['empty_condition'] = empty_condition
        return res_json
                
                
                
                

class SessionLogCreateView(SWCreateView):
    model = Sessionlog

    def save_other(self, instance):
        actiontype = instance.actiontype
        qs = Syspara.objects.filter(nfield='type_list', ftype='SeesionLog')
        if qs.exists():
            syspara = qs.first()
            type_list = syspara.fvalue.split(';')
            if actiontype not in type_list:
                syspara.fvalue += ';' + actiontype  # 更新fvalue的值
                syspara.save()  # 保存修改
        else:
            Syspara.objects.create(nfield='type_list', ftype='SeesionLog', fvalue=actiontype)

class SessionLogUpdateView(SWUpdateView):
    model = Sessionlog

    def save_other(self, instance):
        actiontype = instance.actiontype
        qs = Syspara.objects.filter(nfield='type_list', ftype='SeesionLog')
        if qs.exists():
            syspara = qs.first()
            type_list = syspara.fvalue.split(';')
            if actiontype not in type_list:
                syspara.fvalue += ';' + actiontype  # 更新fvalue的值
                syspara.save()  # 保存修改
        else:
            Syspara.objects.create(nfield='type_list', ftype='SeesionLog', fvalue=actiontype)

class SessionLogDeleteView(SWDeleteView):
    model = Sessionlog

def getSessionTypeData(request):
    res = {'status': False, 'msg':'', 'data': []}
    syspara = Syspara.objects.filter(nfield='type_list', ftype='SeesionLog')
    if syspara.exists():
        res['data'] = str(syspara.first().fvalue or '').split(';')
        res['status'] = True
    return JsonResponse(res)


def getSessionName(request):
    res = {'status': False, 'name': ''}
    sessionid = request.GET.get('sessionid')
    if sessionid == '':
        return JsonResponse(res)
    qs = VTasklistSub.objects.filter(sessionid=sessionid).values('sdesp')
    if not qs.exists():
        return JsonResponse(res)
    res['name'] = qs[0]
    res['status'] = True
    return JsonResponse(res)