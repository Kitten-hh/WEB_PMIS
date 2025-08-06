from django.shortcuts import render
from PMIS.Services.UserService import UserService
from PMIS.Services.TaskService import TaskService
from PMIS.Services.ProjectService import ProjectService
from PMIS.Services.FrameService import FrameService
import itertools

from DataBase_MPMS import models
from django.core.serializers.json import DjangoJSONEncoder 
from django.forms.models import model_to_dict
from django.db.models import Count,Q,Case,Sum,When,IntegerField,Max
import json
import datetime
import calendar
import dateutil.relativedelta
import decimal
from django.http import JsonResponse,HttpResponse,HttpRequest
from BaseApp.library.cust_views.SWCreateView import SWCreateView
from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from BaseApp.library.cust_views.SWDeleteView import SWDeleteView
from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
from BaseApp.library.tools import DateTools
import re
from django.shortcuts import render
from datatableview import Datatable
from BaseApp.library.tools.QueryBuilderUtils import QueryBuilderUtils
from querybuilder.rules import Rule
from .Services.DashboardService import LOGGING, DashboardService
from django.urls import reverse
from BaseApp.library.tools import  AsyncioTools
from DataBase_MPMS.models import Mindmap, VMindmapMenu,Tecfa,Goalmanagement
from django.contrib.auth.decorators import login_required


# Create your views here.
class TemplateIterator(itertools.count):
    def current(self):
        return int(repr(self)[17:-1])
    def next(self):
        next(self)
        return int(repr(self)[17:-1])        

def get_dashboard_data_part(request):
    username = request.GET.get("username")
    bdate = request.GET.get("bdate")
    edate = request.GET.get("edate")
    type = request.GET.get("type")
    result = {'data':None}
    if type == 'projects':
        result['data'] = ProjectService.getFixdProjects(username, bdate, edate)
    elif type == 'active_tasks':
        result['data'] = TaskService.getActiveTaskCount(username, bdate, edate)
    elif type == 'ongoing_tasks':
        result['data'] = TaskService.getOngoingTaskCount(username, bdate, edate)
    elif type == 'task_performance':
        result['data'] = TaskService.analysisTaskPercent(username, bdate, edate)
    elif type == 'leader_board':
        result['data'] = TaskService.analysisUserProjectPercent(username, bdate, edate)
    elif type == 'active_project':
        result['data'] = TaskService.getSessionPercent(username, bdate, edate)
    elif type== 'to_dos':
        result['data'] = TaskService.getToDos(username)
    return  JsonResponse(result, safe=False)

def get_dashbarod_data_new(request, default_user=None, isteam=False):
    scheme = request.is_secure() and "https" or "http"
    host_name = f'{scheme}://{request.get_host()}'
    url = host_name + reverse("get_dashboard_data_part")
    iterator = TemplateIterator()
    username = request.GET.get("username")
    if not username and default_user:
        username = default_user

    bdate = request.GET.get("bdate")
    edate = request.GET.get("edate")
    if not bdate or not edate:
        bdate = DateTools.formatf(DateTools.getBeginOfWeek(DateTools.now()), '%Y-%m-%d')
        edate = DateTools.formatf(DateTools.getEndOfWeek(DateTools.now()), '%Y-%m-%d')
    params = {'bdate':bdate, 'edate':edate}
    if username:
        params['username'] = username
    keys = ['projects','active_tasks','ongoing_tasks','task_performance','leader_board']
    if isteam:
        keys.append('active_project')
        keys.append('to_dos')
    http_methods = {key:{'url':url+'?type=' + key, 'params':params} for key in keys}
    result = AsyncioTools.async_fetch_http_json(http_methods)        
    result = {key:item['data'] for key, item in result.items()}
    result['teams'] = 1
    result['iterator'] = iterator;
    return result

def get_dashbarod_data(request, default_user=None):
    iterator = TemplateIterator()
    username = request.GET.get("username")
    if not username and default_user:
        username = default_user

    bdate = request.GET.get("bdate")
    edate = request.GET.get("edate")
    if not bdate or not edate:
        bdate = DateTools.getBeginOfWeek(DateTools.now())
        edate = DateTools.getEndOfWeek(DateTools.now())
    result = {
        'teams':1,#UserService.getLocalPartUserCount()
        'projects':ProjectService.getFixdProjects(username, bdate, edate),
        'active_tasks':TaskService.getActiveTaskCount(username, bdate, edate),
        'ongoing_tasks':TaskService.getOngoingTaskCount(username, bdate, edate),
        'task_performance':TaskService.analysisTaskPercent(username, bdate, edate),
        ##'leader_board':TaskService.analysisUserTaskPercent(username, bdate, edate),
        'leader_board':TaskService.analysisUserProjectPercent(username, bdate, edate),
        ##'active_project':TaskService.getActiveProjects(username, bdate, edate),
        'active_project':TaskService.getSessionPercent(username, bdate, edate),
        'to_dos':TaskService.getToDos(username),
        'iterator':iterator
    }
    return result

@login_required()
def index(request):
    result = get_dashbarod_data_new(request, None, True)
    service = DashboardService()
    scheme = request.is_secure() and "https" or "http"
    host_name = f'{scheme}://{request.get_host()}'
    url = host_name + reverse("get_staff_planner_task")
    bdate = request.GET.get("bdate")
    edate = request.GET.get("edate")
    if not bdate or not edate:
        bdate = DateTools.formatf(DateTools.getBeginOfWeek(DateTools.now()), '%Y-%m-%d')
        edate = DateTools.formatf(DateTools.getEndOfWeek(DateTools.now()), '%Y-%m-%d')    
    complete_rate = service.get_staff_arragemnt_ratio(url,None, bdate,edate).values()
    for item in complete_rate:
        assign = item['assign']
        if assign == 0:
            item['actualuncomplete_ratio'] = 0
            item['unassigncomplete_ratio'] = 0
        else:
            item['actualuncomplete_ratio'] = item['actualuncomplete']/assign * 100
            item['unassigncomplete_ratio'] = item['unassigncomplete']/assign * 100
    result['completion_rate'] = complete_rate
    
    topics = Tecfa.objects.all()
    result['unsolved_topics'] = topics.filter(fa008='N').count()
    result['unclassified_topics'] = topics.filter(Q(fa002='') | Q(fa002__exact=None)).count()
    return render(request, 'PMISLooper/dashboard/dashboard.html', result)

def staff_dashboard_bak(request):
    default_user = UserService.GetLoginUserName(request)
    service = DashboardService()
    result = get_dashbarod_data_new(request, default_user)
    url = AsyncioTools.get_url(request,"get_staff_planner_task", True)
    username = request.GET.get("username")
    if not username and default_user:
        username = default_user    
    complete_rate = service.get_staff_arragemnt_ratio(url, username).values()
    for item in complete_rate:
        assign = item['assign']
        if assign == 0:
            item['actualuncomplete_ratio'] = 0
            item['unassigncomplete_ratio'] = 0
        else:
            item['actualuncomplete_ratio'] = item['actualuncomplete']/assign * 100
            item['unassigncomplete_ratio'] = item['unassigncomplete']/assign * 100    
    result['completion_rate'] = complete_rate
    ##獲取當前用戶的Mindmap Id
    qs = VMindmapMenu.objects.values('inc_id').filter(menu_type=1, \
        sdesc__istartswith="{0}-{1} {2}".format(DateTools.formatf(DateTools.now(),'%Y'), \
        DateTools.getQuarter(DateTools.now()),username))[:1]
    if len(qs):
        result['mindmap_id'] = qs[0]['inc_id']
    else:
        result['mindmap_id'] = ''
    return render(request, 'PMISLooper/dashboard/staff_dashboard.html', result)



@login_required()
def staff_dashboard(request):
    username = request.GET.get("username", UserService.GetLoginUserName(request))
    bdate = request.GET.get("bdate")
    edate = request.GET.get("edate")
    if not bdate or not edate:
        bdate = DateTools.formatf(DateTools.getBeginOfWeek(DateTools.now()), '%Y-%m-%d')
        edate = DateTools.formatf(DateTools.getEndOfWeek(DateTools.now()), '%Y-%m-%d')
    service = DashboardService()
    result = TaskService.analysis_dashboard(username, bdate, edate)
    result['teams'] = 1
    #url = AsyncioTools.get_url(request,"get_staff_planner_task", True)
    #complete_rate = service.get_staff_arragemnt_ratio(url, username, bdate,edate).values()
    complete_rate = service.get_staff_arragemnt_ratio_with_plandate(username, bdate,edate).values()
    for item in complete_rate:
        assign = item['assign']
        if assign == 0:
            item['actualuncomplete_ratio'] = 0
            item['unassigncomplete_ratio'] = 0
        else:
            item['actualuncomplete_ratio'] = item['actualuncomplete']/assign * 100
            item['unassigncomplete_ratio'] = item['unassigncomplete']/assign * 100    
    result['completion_rate'] = complete_rate
    ##獲取當前用戶的Mindmap Id
    qs = VMindmapMenu.objects.values('inc_id').filter(menu_type=1, \
        sdesc__istartswith="{0}-{1} {2}".format(DateTools.formatf(DateTools.now(),'%Y'), \
        DateTools.getQuarter(DateTools.now()),username))[:1]
    if len(qs):
        result['mindmap_id'] = qs[0]['inc_id']
    else:
        result['mindmap_id'] = ''
    ##獲取當前用戶創建的Mindmap數量
    result['mindmap_count'] = Mindmap.objects.filter(sdesc__iendswith=username, map_type=3).values('inc_id').count()
    quarterly_str = '{0}-{1}'.format(DateTools.formatf(DateTools.now(),"%Y"), DateTools.getQuarter(DateTools.now()))
    result['goal_count'] = Goalmanagement.objects.filter(contact=username, period=quarterly_str, goaltype='Q').values('goalid').count()
    ##獲取當前用戶本季度的session數量
    strplanbdate = DateTools.formatf(DateTools.getBeginOfQuarter(DateTools.now()), '%Y-%m-%d')
    strplanedate = DateTools.formatf(DateTools.getEndOfQuarter(DateTools.now()), '%Y-%m-%d')
    result['session_count'] = models.VTasklistSub.objects.filter(
        Q(contact=username) & 
        Q(
            Q(Q(planbdate__gte=strplanbdate) & Q(planedate__lte=strplanedate)) |
            Q(Q(planedate__gte=strplanbdate) & Q(planedate__lte=strplanedate)) |
            Q(Q(planbdate__lte=strplanbdate) & Q(planedate__gte=strplanedate))
        )
    ).count()
    bdate = bdate.replace('-','')
    edate = edate.replace('-','')
    #topics = Tecfa.objects.all()
    result['unsolved_topics'] = Tecfa.objects.filter(create_date__range=(bdate, edate),fa008='N',fa015='N').count()
    result['new_technicals'] = models.Tecmb.objects.filter(create_date__range=(bdate, edate)).count()
    result['active_tasks'] = result['all_tasks']
    frames = FrameService.analysis_frames_qty(username, bdate, edate)
    result['func_qty'] = frames['func_num']
    result['frame_qty'] = frames['frame_num']
    result['username'] = username
    return render(request, 'PMISLooper/dashboard/staff_dashboard.html', result)

def staff_dashboard_color(request):
    username = request.GET.get("username", UserService.GetLoginUserName(request))
    bdate = request.GET.get("bdate")
    edate = request.GET.get("edate")
    if not bdate or not edate:
        bdate = DateTools.formatf(DateTools.getBeginOfWeek(DateTools.now()), '%Y-%m-%d')
        edate = DateTools.formatf(DateTools.getEndOfWeek(DateTools.now()), '%Y-%m-%d')
    service = DashboardService()
    result = TaskService.analysis_dashboard(username, bdate, edate)
    result['teams'] = 1
    url = AsyncioTools.get_url(request,"get_staff_planner_task", True)
    complete_rate = service.get_staff_arragemnt_ratio(url, username, bdate,edate).values()
    for item in complete_rate:
        assign = item['assign']
        if assign == 0:
            item['actualuncomplete_ratio'] = 0
            item['unassigncomplete_ratio'] = 0
        else:
            item['actualuncomplete_ratio'] = item['actualuncomplete']/assign * 100
            item['unassigncomplete_ratio'] = item['unassigncomplete']/assign * 100    
    result['completion_rate'] = complete_rate
    ##獲取當前用戶的Mindmap Id
    qs = VMindmapMenu.objects.values('inc_id').filter(menu_type=1, \
        sdesc__istartswith="{0}-{1} {2}".format(DateTools.formatf(DateTools.now(),'%Y'), \
        DateTools.getQuarter(DateTools.now()),username))[:1]
    if len(qs):
        result['mindmap_id'] = qs[0]['inc_id']
    else:
        result['mindmap_id'] = ''
    ##獲取當前用戶創建的Mindmap數量
    result['mindmap_count'] = Mindmap.objects.filter(sdesc__iendswith=username, map_type=3).values('inc_id').count()
    result['active_tasks'] = result['all_tasks']
    frames = FrameService.analysis_frames_qty(username, DateTools.addDay(DateTools.now().date(), -7), DateTools.now().date())
    result['func_qty'] = frames['func_num']
    result['frame_qty'] = frames['frame_num']
    return render(request, 'PMISLooper/dashboard/staff_dashboard_color.html', result)
def analysis_new_task(request):
    result = {'status':False, 'msg':'', 'data':None}
    try:
        username = request.GET.get("username", UserService.GetLoginUserName(request))
        bdate = request.GET.get("bdate")
        edate = request.GET.get("edate")
        if not bdate or not edate:
            bdate = DateTools.formatf(DateTools.getBeginOfWeek(DateTools.now()), '%Y-%m-%d')
            edate = DateTools.formatf(DateTools.getEndOfWeek(DateTools.now()), '%Y-%m-%d')
        data = TaskService.analysis_new_task(username, bdate, edate)
        result['status'] = True
        result['data'] = data
    except Exception as e:
        LOGGING.error(e)
    return JsonResponse(result, safe=False)

def analysis_task_type(request):
    result = {'status':False, 'msg':'', 'data':None}
    try:
        username = request.GET.get("username", UserService.GetLoginUserName(request))
        bdate = request.GET.get("bdate")
        edate = request.GET.get("edate")
        if not bdate or not edate:
            bdate = DateTools.formatf(DateTools.getBeginOfWeek(DateTools.now()), '%Y-%m-%d')
            edate = DateTools.formatf(DateTools.getEndOfWeek(DateTools.now()), '%Y-%m-%d')
        data = TaskService.analysis_tasktype(username, bdate, edate, True)
        result['status'] = True
        result['data'] = data
    except Exception as e:
        LOGGING.error(e)
    return JsonResponse(result, safe=False)

def analysis_solution_type(request):
    result = {'status':False, 'msg':'', 'data':None}
    try:
        username = request.GET.get("username", UserService.GetLoginUserName(request))
        bdate = request.GET.get("bdate")
        edate = request.GET.get("edate")
        if not bdate or not edate:
            bdate = DateTools.formatf(DateTools.getBeginOfWeek(DateTools.now()), '%Y-%m-%d')
            edate = DateTools.formatf(DateTools.getEndOfWeek(DateTools.now()), '%Y-%m-%d')
        data = TaskService.analysis_solutiontype(username, bdate, edate)
        result['status'] = True
        result['data'] = data
    except Exception as e:
        LOGGING.error(e)
    return JsonResponse(result, safe=False)

def analysis_new_task(request):
    result = {'status':False, 'msg':'', 'data':None}
    try:
        username = request.GET.get("username", UserService.GetLoginUserName(request))
        bdate = request.GET.get("bdate")
        edate = request.GET.get("edate")
        if not bdate or not edate:
            bdate = DateTools.formatf(DateTools.getBeginOfWeek(DateTools.now()), '%Y-%m-%d')
            edate = DateTools.formatf(DateTools.getEndOfWeek(DateTools.now()), '%Y-%m-%d')
        search_task = request.GET.get("search_task")
        data = TaskService.analysis_new_task(username, bdate, edate, bool(search_task))
        result['status'] = True
        result['data'] = data
    except Exception as e:
        LOGGING.error(e)
    return JsonResponse(result, safe=False)

def get_staff_planner_task(request):
    service = DashboardService()
    user = request.GET.get("user")
    bdate = request.GET.get("bdate")
    edate = request.GET.get("edate")
    planner_task = service.get_plann_arragement_task(user, DateTools.parse(bdate), DateTools.parse(edate))
    return JsonResponse(planner_task, safe=False)

## Json數據轉換的處理類
class DataEncoder(json.JSONEncoder):
    def default(self, obj):
        ## 處理日期數據
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        ## 處理Decimal類型的數據
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self,obj)

def search_demo(request): 
    # 獲得頁面的條件   
    conStr = request.GET.get('taskno') 
    arr = conStr.split("-")
    # 根據Q 定義的條件查詢Cust信息   
    tasklist = models.Task.objects.filter(pid=arr[0], tid=arr[1], taskid=arr[2]) 
    return JsonResponse(list(tasklist.values()),safe=False)




# 查詢Tecdailyplanner的所有數據
class Tecdailyplanner_Datatable(DatatablesServerSideView):
    model = models.Tecdailyplanner
    columns =['inc_id','contact','inputdate','itemno','taskno','startdate','enddate','taskdescription','goalachieve','platformused','tasktype','score','framespecification','designdoc','flowchart','questions','newtechnicalneed','comment','status']
    searchable_columns = columns

class DailyPlannerCreateView(SWCreateView):
    model = models.Tecdailyplanner

    def get_initial(self, instance):
        '''
        功能描述：Http Get 訪問時初始化model新增時的數據
        參數說明:
            instance:該model的實例
        '''
        instance.contact = UserService.GetLoginUserName(self.request)
        instance.inputdate = DateTools.format(datetime.datetime.now())
        instance.startdate = datetime.datetime.now()
        instance.enddate = datetime.datetime.now()
        self.set_max_seqno(instance)

    def set_max_seqno(self, instance):
        '''
        功能描述：獲取最大單號
        參數說明:
            instance:需要保存或初始化的model實例
        '''
        rs = self.model.objects.values('itemno').filter(contact=instance.contact, inputdate=instance.inputdate).order_by('-itemno')[:1]
        if len(rs) > 0:
            max_seq_no = '00000{0}'.format(int(rs[0]['itemno']) + 10)[-5:]
        else:
            max_seq_no = '00010'
        instance.itemno = max_seq_no


    def save_other(self, instance):
        contact = instance.contact
        inputdate = instance.inputdate
        itemno = instance.itemno
        #獲取下標值，將值轉為int類型並排序
        indexlist = set([re.match('solution\[(\d+)\]', key).group(1) for key in self.request.POST.keys() if re.match('solution\[\d+\][.]', key)])
        indexlist = [int(i) for i in indexlist]
        indexlist.sort()
        #獲取前端傳入的參數
        postData = self.request.POST
        for i in indexlist:
            saveSolutionData(i,postData,contact,inputdate,itemno)
        synchronousTask(postData)     
            
    def save_check(self, instance):
        check_status, check_msg = True, ''
        instance.modi_date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        indexlist = set([re.match('solution\[(\d+)\]', key).group(1) for key in self.request.POST.keys() if re.match('solution\[\d+\][.]', key)])
        indexlist = [int(i) for i in indexlist]
        indexlist.sort()
        #獲取前端傳入的參數
        postData = self.request.POST
        #檢驗數據是否正確
        ispass,check_msg,check_status = CheckDetailDailyplanner(indexlist,postData,instance)
        #根據檢驗結果設置字段值
        if ispass == False:
            instance.statusdesc, instance.dailyplannerstatus = check_msg,'I'
        else:    
            instance.statusdesc, instance.dailyplannerstatus = '','C'
        return check_status, check_msg        


def saveSolutionData(indexnum:int,postData:object,contact,inputdate,itemno:str):
    '''
    功能描述：新增TecDailyPlannerSolution表數據
    '''
    #獲取字段值
    technicid = postData.get('solution['+str(indexnum)+'].technicid')
    ftime = postData.get('solution['+str(indexnum)+'].ftime')
    etime = postData.get('solution['+str(indexnum)+'].etime')
    remark = postData.get('solution['+str(indexnum)+'].remark')
    mindmapid = postData.get('solution['+str(indexnum)+'].mindmapid')
    tis = postData.get('solution['+str(indexnum)+'].tis')
    if not tis:
        tis = None
    condition = ''
    if (postData.get('solution['+str(indexnum)+'].satisfactory')=='') or (postData.get('solution['+str(indexnum)+'].satisfactory')=='on'):
        condition = 'S'
    if (postData.get('solution['+str(indexnum)+'].refinement')=='') or (postData.get('solution['+str(indexnum)+'].refinement')=='on'):
        condition = 'R'
    if (postData.get('solution['+str(indexnum)+'].ambiguous')=='') or (postData.get('solution['+str(indexnum)+'].ambiguous')=='on'):
        condition = 'A'
    mindmaplabel = postData.get('solution['+str(indexnum)+'].mindmaplabel')
    stitemno = set_max_solution(contact,inputdate,itemno)
    #當結束時間或閱讀時間沒設時自定義為0
    if ftime=='':
        ftime='0'
    if etime=='':   
        etime='0'
    try:
        solutionData = models.Tecdailyplannersolution(contact=contact,inputdate=inputdate,itemno=itemno,stitemno=stitemno,mindmapid=mindmapid,mindmaplabel=mindmaplabel,technicid=technicid,condition=condition,etime=etime,ftime=ftime,remark=remark, tis=tis)
        solutionData.save()
    except Exception as e:
        print(str(e))    

class DailyPlannerUpdateView(SWUpdateView):
    model = models.Tecdailyplanner  
    
    def save_other(self, instance):
        contact = instance.contact
        inputdate = instance.inputdate
        itemno = instance.itemno
        #獲取下標值，將值轉為int類型並排序
        indexlist = set([re.match('solution\[(\d+)\]', key).group(1) for key in self.request.POST.keys() if re.match('solution\[\d+\][.]', key)])
        indexlist = [int(i) for i in indexlist]
        indexlist.sort()
        #獲取前端傳入的參數
        postData = self.request.POST
        for i in indexlist:
            stitemno = postData.get('solution['+str(i)+'].stitemno')
            stTable = models.Tecdailyplannersolution.objects.filter(contact=contact,inputdate=inputdate,itemno=itemno,stitemno=stitemno)
            if stTable:
                updateSolutionData(i,postData,stTable)   
            else:  
                saveSolutionData(i,postData,contact,inputdate,itemno)
        synchronousTask(postData)        


    def save_check(self, instance):
        check_status, check_msg = True, ''
        instance.modi_date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        indexlist = set([re.match('solution\[(\d+)\]', key).group(1) for key in self.request.POST.keys() if re.match('solution\[\d+\][.]', key)])
        indexlist = [int(i) for i in indexlist]
        indexlist.sort()
        #獲取前端傳入的參數
        postData = self.request.POST
        #檢驗數據是否正確
        ispass,check_msg,check_status = CheckDetailDailyplanner(indexlist,postData,instance)
        #根據檢驗結果設置字段值
        if ispass == False:
            instance.statusdesc, instance.dailyplannerstatus = check_msg,'I'
        else:    
            instance.statusdesc, instance.dailyplannerstatus = '','C'
        return check_status, check_msg  



def updateSolutionData(indexnum:int,postData,stTable:object):
    '''
    功能描述：新增TecDailyPlannerSolution表數據
    '''
    #獲取字段值
    technicid = postData.get('solution['+str(indexnum)+'].technicid')
    ftime = postData.get('solution['+str(indexnum)+'].ftime')
    etime = postData.get('solution['+str(indexnum)+'].etime')
    remark = postData.get('solution['+str(indexnum)+'].remark')
    mindmapid = postData.get('solution['+str(indexnum)+'].mindmapid')
    tis = postData.get('solution['+str(indexnum)+'].tis')
    if not tis:
        tis = None
    condition = ''
    if (postData.get('solution['+str(indexnum)+'].satisfactory')=='') or (postData.get('solution['+str(indexnum)+'].satisfactory')=='on'):
        condition = 'S'
    if (postData.get('solution['+str(indexnum)+'].refinement')=='') or (postData.get('solution['+str(indexnum)+'].refinement')=='on'):
        condition = 'R'
    if (postData.get('solution['+str(indexnum)+'].ambiguous')=='') or (postData.get('solution['+str(indexnum)+'].ambiguous')=='on'):
        condition = 'A'
    mindmaplabel = postData.get('solution['+str(indexnum)+'].mindmaplabel')
    #當結束時間或閱讀時間沒設時自定義為0
    if ftime=='':
        ftime='0'
    if etime=='':   
        etime='0'
    try:
        if technicid != '':
            stTable.update(mindmapid=mindmapid,mindmaplabel=mindmaplabel,technicid=technicid,condition=condition,etime=etime,ftime=ftime,remark=remark, tis=tis)    
    except Exception as e:
        print(str(e))         

def set_max_solution(contact,inputdate,itemno:str):
    '''
    功能描述：獲取SolutionType最大單號
    '''
    stTable = models.Tecdailyplannersolution.objects.filter(contact=contact,inputdate=inputdate,itemno=itemno).order_by('-stitemno')[:1].values('stitemno')
    if len(stTable) > 0:
        max_seq_no = '00000{0}'.format(int(stTable[0]['stitemno']) + 10)[-5:]
    else:
        max_seq_no = '00010'
    return max_seq_no


def synchronousTask(postData:object):
    taskno = re.findall(r"\d+\.?\d*",postData['taskno'])
    pid = taskno[0]
    tid = taskno[1]
    taskid = taskno[2]
    tastData = models.Task.objects.filter(pid=pid,tid=tid,taskid=taskid)
    tastData.update(modi_date=datetime.datetime.now().strftime("%Y%m%d%H%M%S"),task=postData['taskdescription'],udf04=postData['framespecification'],progress=postData['status'])


# class DailyPlannerUpdateView(SWUpdateView):
#     model = so.Tecdailyplanner

# class DailyPlannerDeleteView(SWDeleteView):
#     model = so.Tecdailyplanner


# 查詢Tecsolutiontype的所有數據
class Tecsolutiontype_Datatable(DatatablesServerSideView):
    model = models.Tecsolutiontype
    columns =['inc_id','solutiontype','technical','condition','time','remark']
    searchable_columns = columns

class SolutionTypeCreateView(SWCreateView):
    model = models.Tecsolutiontype

def getTask(request:HttpRequest):
    #獲取TaskType翻譯
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        taskno = request.GET.get('taskno')
        inputdate = datetime.datetime.strptime(request.GET.get('inputdate'),"%Y-%m-%d").date().strftime('%Y%m%d')
        taskno = re.findall(r"\d+\.?\d*",taskno)
        pid = taskno[0]
        tid = taskno[1]
        taskid = taskno[2]
        tastData = models.Task.objects.filter(pid=pid,tid=tid,taskid=taskid).values()
        for task in tastData:
            tasktype = task['tasktype']
            Subtasktype = task['subtasktype']
            diff = 'difficulties1'
            if task['diff'] != None:
                diff = 'difficulties'+str(task['diff'])
            if tasktype != None and Subtasktype != None and diff != None and tasktype != '' and Subtasktype != '' and diff != '' :            
                theType = list(models.Tasktypelist.objects.filter(tasktype=tasktype).values('description'))
                thesubType = list(models.Tasktypelist.objects.filter(tasktype=Subtasktype).values('description'))
                score = list(models.Tasktypelist.objects.filter(tasktype=Subtasktype,parenttype=tasktype).values(diff))
                task['tasktype'] = theType[0]['description']
                task['subtasktype'] = thesubType[0]['description']
                task['diff'] = score[0][diff]
            dpdata = models.Tecdailyplanner.objects.values('itemno').filter(contact=task['contact'], inputdate=inputdate).order_by('-itemno')[:1]
        
        thedata = list(tastData)   
        #獲取用戶detailplanner的itemno最大值
        if len(dpdata) > 0:
            max_seq_no = '00000{0}'.format(int(dpdata[0]['itemno']) + 10)[-5:]
        else:
            max_seq_no = '00010'
        thedata.append(max_seq_no) 
        result['status'] = True
        result['data'] =  thedata
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   

class DailyPlannerSolutionCreateView(SWCreateView):
    model = models.Tecdailyplannersolution

    def get_initial(self, instance):
        '''
        功能描述：Http Get 訪問時初始化model新增時的數據
        參數說明:
            instance:該model的實例
        '''
        ##set contact, inputdate
        instance.contact = UserService.GetLoginUserName(self.request)
        instance.inputdate = DateTools.format(datetime.datetime.now())
        self.set_max_seqno(instance)

    def set_max_seqno(self, instance):
        '''
        功能描述：獲取最大單號
        參數說明:
            instance:需要保存或初始化的model實例
        '''
        rs = self.model.objects.values('itemno').filter(contact=instance.contact, inputdate=instance.inputdate).order_by('-itemno')[:1]
        if len(rs) > 0:
            max_seq_no = '00000{0}'.format(int(rs[0]['itemno']) + 10)[-5:]
        else:
            max_seq_no = '00010'
        instance.itemno = max_seq_no

class DailyPlannerSolutionUpdateView(SWUpdateView):
    model = models.Tecdailyplannersolution  

def getRecentlyinMarchu(request:HttpRequest):
    '''
    功能描述：獲取最近三個月的日期
    '''
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        TimeData = []
        now = datetime.datetime.now()
        monthago = now + dateutil.relativedelta.relativedelta(months=-1)#一個月前
        twomonthago = now + dateutil.relativedelta.relativedelta(months=-2)#兩個个月前
        threemonthago = now + dateutil.relativedelta.relativedelta(months=-3)#三個个月前
        fourmonthago = now + dateutil.relativedelta.relativedelta(months=-4)#四個个月前
        fivemonthago = now + dateutil.relativedelta.relativedelta(months=-5)#四個个月前
        datalist = {"MonthTime":now.strftime('%Y-%m')}
        TimeData.append(datalist)
        datalist = {"MonthTime":monthago.strftime('%Y-%m')}
        TimeData.append(datalist)
        datalist = {"MonthTime":twomonthago.strftime('%Y-%m')}
        TimeData.append(datalist)
        datalist = {"MonthTime":threemonthago.strftime('%Y-%m')}
        TimeData.append(datalist)
        datalist = {"MonthTime":fourmonthago.strftime('%Y-%m')}
        TimeData.append(datalist)
        datalist = {"MonthTime":fivemonthago.strftime('%Y-%m')}
        TimeData.append(datalist)

        result['status'] = True
        result['data'] = TimeData
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)     
    

def getMonthDay(MonthTime:str):
    '''
    功能描述：獲取某年某月的第一天和最後一天日期
    '''
    #獲取參數的具體值
    MonthTime = re.findall(r"\d+\.?\d*",MonthTime)
    # 获取当月第一天的星期和当月的总天数
    firstDayWeekDay, monthRange = calendar.monthrange(int(MonthTime[0]), int(MonthTime[1]))
    # 获取当月的第一天
    firstDay = datetime.date(year=int(MonthTime[0]), month=int(MonthTime[1]), day=1)
    lastDay = datetime.date(year=int(MonthTime[0]), month=int(MonthTime[1]), day=monthRange)
    print(firstDay, lastDay)
    return firstDay.strftime('%Y%m%d'), lastDay.strftime('%Y%m%d')

def getTreemenu(request:HttpRequest):
    '''
    功能描述：獲取某員工某月的dailyplanner樹狀圖
    '''
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        contact = request.GET.get('contact')
        monthday = request.GET.get('monthday')
        if not contact:
            contact = 'zyl'
        if not monthday:
            monthday = datetime.datetime.now().strftime('%Y-%m') 
        startTime ,endTime = getMonthDay(monthday)
        folderdata = []
        #第一層，某員工某月的寫過dailyplanner的日期
        dateList = models.Tecdailyplanner.objects.filter(contact=contact,inputdate__range=(startTime,endTime)).values('inputdate','contact').annotate(dcount=Count('inc_id')).order_by('-inputdate')
        for datefolder in dateList:
            theTime = DateTools.parse(datefolder['inputdate']).strftime('%Y-%m-%d')
            folderlist = {'FolderID':datefolder['contact']+datefolder['inputdate'],'FolderName':theTime,'ParentID':0,'statusdesc':'','dailyplannerstatus':'','inc_id':''}
            folderdata.append(folderlist)
        #第二層，每天具體的dailyplanner
        dateList2 = models.Tecdailyplanner.objects.filter(contact=contact,inputdate__range=(startTime,endTime)).values('inputdate','contact','startdate','itemno','inc_id','statusdesc','dailyplannerstatus','framespecification','flowchart').order_by('-inputdate')
        for datefolder in dateList2:
            foldername2 = 'Task'+datefolder['itemno'][-2]
            folderid2 = datefolder['inputdate']+datefolder['itemno']+'inc_id'+str(datefolder['inc_id'])
            folderlist = {'FolderID':folderid2,'FolderName':foldername2,'ParentID':datefolder['contact']+datefolder['inputdate'],'statusdesc':datefolder['statusdesc'],'dailyplannerstatus':datefolder['dailyplannerstatus'],'inc_id':datefolder['inc_id']}
            folderdata.append(folderlist)  
            #第三層，每個dailyplanner下的page

            dateList4 = models.Tecdailyplannerimage.objects.filter(contact=datefolder['contact'],inputdate=datefolder['inputdate'],itemno=datefolder['itemno']).values()
            for thedateList4 in dateList4:
                foldername4 = thedateList4['text']
                folderid4 = thedateList4['inputdate']+'ThePage'+str(thedateList4['imageno'])+str(thedateList4['inc_id'])
                folderlist = {'FolderID':folderid4,'FolderName':foldername4,'ParentID':folderid2,'statusdesc':'','dailyplannerstatus':'','inc_id':thedateList4['inc_id']}
                folderdata.append(folderlist)  


            # dateList4 = models.Tecdailyplannerimage.objects.filter(contact=datefolder['contact'],inputdate=datefolder['inputdate'],itemno=datefolder['itemno'],classify='U')
            # dateList4 = dateList4.values('inputdate','classify','inc_id').order_by('-inputdate')[:1]  
            # if len(dateList4) > 0:
            #     foldername4 = 'UI'
            #     folderid4 = dateList4[0]['inputdate']+dateList4[0]['classify'].strip( ' ' )+str(dateList4[0]['inc_id'])
            #     folderlist = {'FolderID':folderid4,'FolderName':foldername4,'ParentID':folderid2,'statusdesc':'','dailyplannerstatus':''}
            #     folderdata.append(folderlist)  
            # #第三層，每個dailyplanner下的Code     
            # dateList4 = models.Tecdailyplannerimage.objects.filter(contact=datefolder['contact'],inputdate=datefolder['inputdate'],itemno=datefolder['itemno'],classify='C')
            # dateList4 = dateList4.values('inputdate','classify','inc_id').order_by('-inputdate')[:1]  
            # if len(dateList4) > 0:
            #     foldername4 = 'Code'
            #     folderid4 = dateList4[0]['inputdate']+dateList4[0]['classify'].strip( ' ' )+str(dateList4[0]['inc_id'])
            #     folderlist = {'FolderID':folderid4,'FolderName':foldername4,'ParentID':folderid2,'statusdesc':'','dailyplannerstatus':''}
            #     folderdata.append(folderlist)  
              
            #窗口文檔模塊
            if datefolder['framespecification']!='' and datefolder['framespecification']!=None:  
                folderlist = {'FolderID':datefolder['framespecification']+folderid2+"Frm",'FolderName':datefolder['framespecification'],'ParentID':folderid2,'statusdesc':'','dailyplannerstatus':'','inc_id':''}
                folderdata.append(folderlist)  
            #流程圖
            if datefolder['flowchart']!='' and datefolder['flowchart']!=None:  
                folderlist = {'FolderID':'Flowchart'+datefolder['flowchart'],'FolderName':'Flowchart','ParentID':folderid2,'statusdesc':'','dailyplannerstatus':'','inc_id':''}
                folderdata.append(folderlist)       
            #第三層，每個dailyplanner下的技術文檔
            dateList3 = models.Tecdailyplannersolution.objects.filter(contact=datefolder['contact'],inputdate=datefolder['inputdate'],itemno=datefolder['itemno'])
            dateList3 = dateList3.values('inputdate','technicid','itemno','inc_id').order_by('-inputdate')
            for datefolder3 in dateList3:
                #獲取技術文檔詳情
                if datefolder3['technicid']:
                    foldername3 = models.Tecmb.objects.filter(inc_id=datefolder3['technicid']).values('mb023','mb004','inc_id')
                    if foldername3:
                        foldername3 = foldername3[0]
                        mb023 = foldername3['mb023']
                        mb004 = foldername3['mb004']
                        TecInc_id = foldername3['inc_id']
                        inc_id = datefolder3['inc_id']
                        if foldername3['mb023'] == None:
                            mb023 = ''
                        if foldername3['mb004'] == None:
                            mb004 = ''
                        foldername3 = mb023+'('+mb004+')'
                        folderid3 = 'Technical_'+str(TecInc_id)+'_'+str(inc_id)
                        folderlist = {'FolderID':folderid3,'FolderName':foldername3,'ParentID':folderid2,'statusdesc':'','dailyplannerstatus':'','inc_id':inc_id}
                        folderdata.append(folderlist)       
        #print(folderdata)
        
        result['status'] = True
        result['data'] =  folderdata
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   

def createImage(request:HttpRequest):
    #創建圖片信息
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        image = request.FILES.get('file')
        #判斷是否存在圖片
        if image != None:
            imagefile = request.FILES.get('file')
            image = imagefile.file.read()
            imagetype = imagefile.content_type
        contact = request.POST.get('contact')
        inputdate = request.POST.get('inputdate')
        itemno = request.POST.get('itemno')
        classify = request.POST.get('Classify')
        description = request.POST.get('Description')
        text = request.POST.get('Text')
        imageno = getMaxImageno(contact,inputdate,itemno,classify)
        #分為有圖片和沒有圖片的新增
        if not image:
            tecdailyplannerimage = models.Tecdailyplannerimage(contact=contact,inputdate=inputdate,itemno=itemno,classify=classify,
            description=description,text=text,imageno=imageno) 
        else:
            tecdailyplannerimage = models.Tecdailyplannerimage(contact=contact,inputdate=inputdate,itemno=itemno,classify=classify,
                description=description,text=text,imageno=imageno,image=image,imagetype=imagetype) 
        tecdailyplannerimage.save() 
        result['status'] = True
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   

def getMaxImageno(contact,inputdate,itemno,classify):
    #獲取圖片序號最大值
    rs = models.Tecdailyplannerimage.objects.values('imageno').filter(contact=contact,inputdate=inputdate,itemno=itemno,classify=classify).order_by('-imageno')[:1]
    if len(rs) > 0:
        max_seq_no = '00000{0}'.format(int(rs[0]['imageno']) + 10)[-5:]
    else:
        max_seq_no = '00010'
    return max_seq_no    

def gettecdailyplannerimage(request:HttpRequest):
    #查看圖片
    inc_id = request.GET.get('inc_id')
    dailyplannerimage = models.Tecdailyplannerimage.objects.filter(inc_id=inc_id).order_by('imageno')
    if not dailyplannerimage.exists():
        return HttpResponse(status=404) #不存在的文件，返回404
    dailyplannerimage = dailyplannerimage.values()[0]
    response = HttpResponse(dailyplannerimage['image'], content_type=dailyplannerimage['imagetype'])
    #根據文件的類型設置響應頭
    IMAGE_TYPE = ["image/jpeg", "image/png", "image/jpg", "image/gif", "image/bmp"]

    # 是圖片直接顯示
    response.__setitem__("Content-Disposition", "inline;filename="+dailyplannerimage['inputdate'])
    return response    

def selectImagees(request:HttpRequest):
    #查詢圖片信息表
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        contact = request.GET.get('contact')
        inputdate = request.GET.get('inputdate')
        itemno = request.GET.get('itemno')
        classify = request.GET.get('classify')
        Tecdailyplannerimages = models.Tecdailyplannerimage.objects.filter(contact=contact,inputdate=inputdate,itemno=itemno,classify=classify)
        Tecdailyplannerimages = Tecdailyplannerimages.values('contact','inputdate','itemno','classify','description','text','imageno','imagetype','inc_id')
        result['data'] = list(Tecdailyplannerimages)
        result['status'] = True
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   


def getTecMindMap(request:HttpRequest):
    #獲取所有MindMap數據
    result = {'status':False, 'msg':'', 'data':[]}
    thedata = []
    try:
        Tecmindmaps = models.Tecmindmap.objects.all().values('inc_id','parentid','sdesc')
        for tecmindmap in Tecmindmaps:
            mindmaplist = {"inc_id":tecmindmap['inc_id'],"parentid":tecmindmap['parentid'],"sdesc":tecmindmap['sdesc']}
            thedata.append(mindmaplist)
        result['data'] = thedata
        result['status'] = True    
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)       

def getTecMindMapDetail(request:HttpRequest):
    #獲取MindMap下技術文檔
    result = {'status':False, 'msg':'', 'data':[]}
    resultdata = []
    try:
        mindmapid = request.GET.get('mindmapid')
        Tecmindmapdetailes = models.Tecmindmapdetail.objects.filter(mindmapid=mindmapid).values('mindmapid','technicid')
        for Tecmindmapdetail in Tecmindmapdetailes:
            Tecmbdata =  models.Tecmb.objects.filter(inc_id=Tecmindmapdetail['technicid']).values('mb023','mb004','inc_id') 
            if Tecmbdata:
                Tecmbdata = Tecmbdata[0]
                mb023 = Tecmbdata['mb023']
                mb004 = Tecmbdata['mb004']
                if Tecmbdata['mb023'] == None:
                    mb023 = ''
                if Tecmbdata['mb004'] == None:
                    mb004 = ''
                Technicalcode = mb023.strip(" ")+'('+mb004+')'
                Tecmblist = {"Technicalcode":Technicalcode,"inc_id":Tecmbdata['inc_id']}
                resultdata.append(Tecmblist)
        result['data'] = resultdata
        result['status'] = True
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   

class Tecmindmap_Datatable(DatatablesServerSideView):
    model = models.Tecmindmap
    columns =['inc_id','parentid','sdesc']
    searchable_columns = columns

class Technic_Datatable(DatatablesServerSideView):
    model = models.Tecmb
    columns =['inc_id','mb023','mb004','mb008','mb005']
    searchable_columns = columns

def displaysolutionType(request:HttpRequest):
    #獲取Task的Solution
    result = {'status':False, 'msg':'', 'data':[]}
    thedata = []
    try:
        contact = request.GET.get('contact')
        inputdate = request.GET.get('inputdate')
        itemno = request.GET.get('itemno')
        solutionTypelist = models.Tecdailyplannersolution.objects.filter(contact=contact,inputdate=inputdate,itemno=itemno).values('technicid','inc_id',
        'mindmapid','mindmaplabel','condition','ftime','etime','remark','stitemno','tis').order_by('mindmaplabel')
        for solutionType in solutionTypelist:
            if solutionType['technicid']:
                Tecmbdata =  models.Tecmb.objects.filter(inc_id=solutionType['technicid']).values('mb023','mb004','inc_id') 
                #Tecmindmaplist =  models.Tecmindmap.objects.filter(inc_id=solutionType['mindmapid']).values('parentid','sdesc','inc_id') 
                if Tecmbdata :
                    Tecmbdata = Tecmbdata[0]
                    mb023 = Tecmbdata['mb023']
                    mb004 = Tecmbdata['mb004'] 
                    if Tecmbdata['mb023'] == None:
                        mb023 = ''
                    if Tecmbdata['mb004'] == None:
                        mb004 = ''
                    Technicalcode = mb023.strip(" ")+'('+mb004+')'
                    Tecmblist = {"Technicalcode":Technicalcode,"inc_id":solutionType['technicid'],"mindmapid":solutionType['mindmapid'],
                        "mindmapsdesc":solutionType['mindmaplabel'],"condition":solutionType['condition'],"ftime":solutionType['ftime'],
                        "etime":solutionType['etime'],"remark":solutionType['remark'],"stitemno":solutionType['stitemno'],"tis":solutionType['tis'],'solution_inc_id':solutionType['inc_id']}
            else:
                Tecmblist = {"Technicalcode":'',"inc_id":solutionType['technicid'],"mindmapid":solutionType['mindmapid'],
                    "mindmapsdesc":solutionType['mindmaplabel'],"condition":solutionType['condition'],"ftime":solutionType['ftime'],
                    "etime":solutionType['etime'],"remark":solutionType['remark'],"stitemno":solutionType['stitemno'],"tis":solutionType['tis'],'solution_inc_id':solutionType['inc_id']}
            thedata.append(Tecmblist)
        result['data'] = thedata
        result['status'] = True    
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)     


def AnalyseTaskType(request:HttpRequest):
    #分析用戶一段時間的TaskType
    result = {'status':False, 'msg':'', 'data':[]}
    TaskTypedata = []
    try:
        search_obj = QueryBuilderUtils.getQueryFromRequest(request,'search[value]', 'form-search:')
        if search_obj:
            search_obj['rules'][1]['type'] = 'string'
            search_obj['rules'][2]['type'] = 'string'
            a = search_obj['rules'][1]['value'].split("-")
            sdate = a[0]+a[1]+a[2]
            search_obj['rules'][1]['value'] = sdate
            a = search_obj['rules'][2]['value'].split("-")
            edate = a[0]+a[1]+a[2]
            search_obj['rules'][2]['value'] = edate
            query = QueryBuilderUtils.json_to_query(json.dumps(search_obj))
        else:    
            query = Q()
            query.connector = "and"
            query.children.append(('contact', 'lsy'))
            query.children.append(('inputdate__range', ('20210130', '20210206')))
        Tecdailyplannerlist = models.Tecdailyplanner.objects.filter(query).extra(
            select = {'subtasktypedesc':'V_Task.subtasktypedesc','realtasktype':'V_Task.realtasktype'},
            tables = ["V_Task"],
            where = ["TecDailyPlanner.taskno=V_Task.taskno"]
        ).values('subtasktypedesc',"realtasktype").annotate(Total=Count('inc_id'))
        for Tecdailyplanner in Tecdailyplannerlist:
            TaskTypedata.append(Tecdailyplanner)
        result['data'] = TaskTypedata
        result['status'] = True
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   



def CheckDetailDailyplanner(indexlist:int,postData,instance:object):  
    #功能描述：檢驗數據是否合法
    ispass,check_msg,check_status = True, '',True 
    sumcondition = 0
    if instance.framespecification =='' or instance.framespecification == None:
        ispass,check_msg,check_status = False,'未填寫Frame Specification',True   
        return  ispass,check_msg,check_status
    if instance.tasktype =='' or instance.tasktype == None:
        ispass,check_msg,check_status = False,'未填寫Task Type',False    
        return  ispass,check_msg,check_status  
    if instance.status =='' or instance.status == None:
        ispass,check_msg,check_status = False,'未填寫Status',False    
        return  ispass,check_msg,check_status  
    if instance.goalachieve =='' or instance.goalachieve == None:
        ispass,check_msg,check_status = False,'未填寫Goal Achieve',False    
        return  ispass,check_msg,check_status  
    for i in indexlist:
        if postData.get('solution['+str(i)+'].mindmaplabel')=='':
            ispass,check_msg,check_status = False,'未填寫Solution Type',True  
            break
        if postData.get('solution['+str(i)+'].ftime')=='' and instance.status !='C':
            ispass,check_msg,check_status = False,'未填寫FTime',True  
            break
        if postData.get('solution['+str(i)+'].etime')=='':
            ispass,check_msg,check_status = False,'未填寫ETime',True  
            break
        if postData.get('solution['+str(i)+'].satisfactory')=='':
            sumcondition = sumcondition + 1
        if postData.get('solution['+str(i)+'].refinement')=='':
            sumcondition = sumcondition + 1
        if postData.get('solution['+str(i)+'].ambiguous')=='':
            sumcondition = sumcondition + 1
        if sumcondition > 1:
            ispass,check_msg,check_status = False,'Condition填寫錯誤',True  
            break         
    return  ispass,check_msg,check_status

@login_required()
def mindmapPage(request):
    hideMenu = request.GET.get("hideMenu", "N") == "Y"
    return render(request, "PMISLooper/mindmap/mindmap.html", {'hideMenu':hideMenu})