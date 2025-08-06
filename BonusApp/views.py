from django.shortcuts import render
from DataBase_MPMS.models import Tpdetail, VTask,VTaskbonussl, VUsers, Tasktype, Task, VTasktypetreelist, VQueryfilter, Tecmb, Tasktypelist,Syspara,TasktypeSl,TasktypeSlHistory, Deductionitem,Userdeduction,LSTasktypelist,Improvearea,Bonuscredit
from django.http import JsonResponse, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from BaseProject.views_folder.base_crud.SimpleView import SimpleView
from BaseApp.library.cust_views.SWCreateView import SWCreateView
from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from BaseApp.library.cust_views.SWDeleteView import SWDeleteView
from .forms import TaskType_main_form
from django.forms.models import model_to_dict  # Model转换字典
from django.shortcuts import redirect  # 重定向
import json
from django.db.models import Q,Count,Max,F,Sum
from . import hint, QueryFilterService
from django.db import transaction  # 事务
from chinese_calendar import is_workday, is_holiday
from datetime import datetime,timedelta
import dateutil
import calendar
import time
from django.core.paginator import Paginator
import pyodbc
import suds.client
from WEB_PMIS import settings
import requests
import aiohttp
import asyncio
from BaseApp.library.tools import ModelTools
from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
from django.db import connections
from BaseApp.library.tools import  AsyncioTools
from asgiref.sync import sync_to_async
import asyncio
from BonusApp.tools import RestApiUtils
import logging
LOGGER = logging.Logger(__name__)

# Create your views here.


def index(request):
    return render(request, 'BonusApp/App.html')


def Task_Management(request):
    '''
    Task管理页面
    '''
    return render(request, 'BonusApp/old_bonus_page.html')

# get_Tasks/ index.html 数据显示方法
def get_Task(request):
    '''
    获取本月的Task
    '''
    result = {} # { state : 200, data:[ ] }
    results = []
    sysresults = []
    sort = request.GET.get("sort")
    sql = "select * from V_Task where DATEDIFF(mm, EDate, GETDATE())=1 and Progress = 'C' and TaskTypeScore>0 order by %s desc " % (sort)
    v_tasks = VTask.objects.raw(sql) #通过参数SQL语句查询数据库
    for v in list(v_tasks):
        results.append({key:value for key,value in v.__dict__.items() if key != '_state'})
    
    syspara = Syspara.objects.filter(desp='BonusApp',ftype='qfq')
    for t in syspara:
        sysresults.append(model_to_dict(t))

    result['state'] = 200
    result['data'] = results
    result['paraData'] = sysresults
    return JsonResponse(result)

# url query/search/
def searchRecordFilter(request):
    def sort_by_qf012(queryfilter):
        qf012 = queryfilter.get('qf012')
        if qf012 is None:
            return float('inf')  # 将空值置于排序的末尾
        return qf012
    '''
    查询预定义的条件，填充到下拉框
    '''
    result = {}
    if 'filter' in request.GET:
        str_filter = request.GET.get("filter")
        is_daily = request.GET.get("is_dialy")
        qf003_filter = Q() 
        qf003_filter.connector = 'AND'
        qf008_filter = Q()
        qf008_filter.connector = 'AND'
        filter_arr = str_filter.split('+')
        for filter in filter_arr:
            filter = filter.strip()
            qf003_filter.children.append(('qf003__contains', filter))
            qf008_filter.children.append(('qf008__contains', filter))
        rs = VQueryfilter.objects.values('qf001', 'qf002', 'qf003', 'qf012', 'qf025').filter(
            Q(qf006='sing', qf009='PMS', qf010='TaskEnquiry_Frm') & (qf003_filter | qf008_filter))
        if 'Y' == is_daily:
            rs = rs.filter(qt002__contains='Daily Goal')
        result['state'] = "OK"
        result['data'] = sorted(list(rs), key=sort_by_qf012)
    return JsonResponse(result)

# url task_enquiry/
def display_task_enquiry(request):
    '''
    使用预定义条件进行查询
    '''
    result = {}
    if 'query_filter_id' in request.GET:
        sort = request.GET.get("sort")
        id = request.GET.get('query_filter_id')
        str_filter = QueryFilterService.get_query_filter(id) # 解析该查询条件
        str_filter += 'order by '+sort + ' desc' 
        v_tasks = VTask.objects.raw('select * from V_Task where ' + str_filter) # raw()通过参数SQL语句查询数据库        
        results = []
        '''
        result = {}
        for task in rs: # 若task 在列表rs中
            task.bdate = str(task.bdate)[0:10]
            results.append(model_to_dict(task))
        '''
        for v in list(v_tasks):
            results.append({key:value for key,value in v.__dict__.items() if key != '_state'})
        result['state'] = "OK"
        result['data'] = list(results)
        return JsonResponse(result)

# 按照计划时间范围搜索
def get_searchdate(request):
    contact = request.GET.get('contact')
    edateOne = request.GET.get('edateOne')
    edateTwo = request.GET.get('edateTwo')
    
    if(contact == ''):
        datalist = VTask.objects.filter(edate__range=(edateOne,edateTwo)).order_by('contact','-edate')
    else:    
        datalist = VTask.objects.filter(edate__range=(edateOne,edateTwo),contact=contact).order_by('-edate')

    # syspara = Syspara.objects.filter(ftype='BonusApp') 
    # for t in syspara:
    #     sysresults.append(model_to_dict(t))

    return JsonResponse(list(datalist.values()),safe=False)
    
# url get_Task_Details/
def get_Task_Details(request):
    '''
    查询Task信息
    '''
    result = {}
    if request.is_ajax():
        try:
            inc_id = request.GET.get("inc_id") # 获取url inc_id
            vtask = VTask.objects.filter(inc_id=inc_id) # 通过inc_id 进行筛选，并返回列表
            result['state'] = 200
            result['data'] = list(vtask.values())[0]
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse(hint.get_result(hint.HintMsg.not_found_Task))
    else:
        return render(request, 'BonusApp/Task_Details.html')

# Task_Details页面删除按钮
def Task_Del(request):
    inc_id = request.GET.get("inc_id")
    vTask = VTask.objects.get(inc_id=inc_id)
    vTask = delete()
    result = {}
    result['state'] = 200 
    result['flg'] = True
    result['message'] = "删除成功"

# url Modif_Task/  数据表Task Task_Details页面保存按钮
def Modif_Task(request):
    '''
    修改Task
    '''
    if request.is_ajax and request.method == "POST":
        result = {}
        # 開啟事務
        with transaction.atomic(using='MPMS'): 
            # 創建事務保存點
            save_id = transaction.savepoint(using='MPMS')
            try:  
                inc_id = request.POST.get("inc_id") # 获取的当前id
                tasktype = request.POST.get("tasktype")   # 获取的当前任务类型
                subtasktype = request.POST.get("subtasktype") # 获取的当前子任务类型
                diff = request.POST.get("diff") # 获取的当前难度
                task = request.POST.get("task") # 任务描述
                remark = request.POST.get("remark") # 备注
                progress = request.POST.get("progress") # 进度
                score = request.POST.get("score") # 实际绩效分
                class_field = request.POST.get("class_field") # class
                priority = request.POST.get("priority") # 优先级  
                planbdate = request.POST.get("planbdate") # 计划开始时间
                planedate = request.POST.get("planedate") # 计划结束时间
                bdate = request.POST.get("bdate") # 获取实际开始时间
                edate = request.POST.get("edate") # 获取实际结束时间 
                delayday = request.POST.get("delayday") # 获取拖期时间
                requestdate = request.POST.get("requestdate") # 获取需求时间

                taskDic = Task.objects.get(inc_id=inc_id) # 根据id匹配，返回字典对象
                taskDic.tasktype = tasktype  # 修改后的任务类型
                taskDic.subtasktype = subtasktype # 修改后的子任务类型
                taskDic.diff = diff # 修改后的难度
                taskDic.progress = progress # 进度
                taskDic.task = task # 任务描述
                taskDic.remark = remark # 备注
                taskDic.score = score # 实际绩效分
                taskDic.class_field = class_field # 修改后的class
                taskDic.priority = priority # 优先级
                taskDic.bdate = bdate # 实际开始时间
                taskDic.edate = edate # 实际结束时间
                taskDic.delayday = delayday # 修改后的拖期时间
                taskDic.requestdate = requestdate # 修改后的需求时间

                taskDic.save() # 提交修改后的数据
                
                transaction.savepoint_commit(save_id, using='MPMS')  # 提交事務
                result['state'] = 200
                result['data'] = taskDic.inc_id
                return JsonResponse(result)
            except Exception as e:
                print(e)
                transaction.savepoint_rollback(save_id, using='MPMS')  # 事務回滾
                return JsonResponse(hint.get_result(hint.HintMsg.database_error))

# url get_TaskTypeList/ 数据表 Tasktypelist
def get_TaskTypeList(request):
    result = {}
    tasktypelists = list(Tasktypelist.objects.all().values())
    result['state'] = 200
    result['data'] = tasktypelists
    return JsonResponse(result) 

# url get_Contact_Details/ 
def get_Contact_Details(request):
    '''
    通過聯繫人查詢當月的Task
    '''
    result = {}
    if request.is_ajax():
        contactName = request.GET.get("contact_name")
        users = list(VUsers.objects.filter(username=contactName).values())
        if len(users) == 0:
            return JsonResponse(hint.get_result(hint.HintMsg.not_found_user))
        else:
            users = users[0]
            result['state'] = 200
            result['data'] = users
            return JsonResponse(result)
    else:
        return render(request, 'BonusApp/Contact_Details.html')

# url get_Task_List/
def get_Task_List(request):
    '''
    通过联系人查询当月的Task
    '''
    id = request.GET.get('query_filter_id')
    contactName = request.GET.get("contact_name")
    result = {}
    results = []
    if request.is_ajax():
        if id == None:  # 等於None就通過聯繫人查詢前一個月的Task信息，否則使用預定義條件查詢Task
            sql = "select * from V_Task where Contact = '%s' and DATEDIFF(mm, EDate, GETDATE())=1 and Progress = 'C' and TaskTypeScore>0 order by EDate" % (
                contactName)
            v_tasks = VTask.objects.raw(sql) # 通过sql语句查询数据库
            for v in v_tasks:
                results.append(model_to_dict(v))
            result['state'] = 200
            result['data'] = results
            return JsonResponse(result)
        else:
            str_filter = QueryFilterService.get_query_filter(id)
            str_filter += 'order by bdate desc'
            rs = VTask.objects.raw(
                "select * from V_Task where Contact='"+contactName+"' AND " + str_filter)
            for task in rs:
                results.append(model_to_dict(task))
            result['state'] = 200
            result['data'] = results
            return JsonResponse(result)
    else:
        return render(request, 'BonusApp/Task_List.html')

# url get_Task_Modif_Page/
def get_Task_Modif_Page(request):
    '''
    跳轉到Task的修改頁面,並使用ajax讀取要修改的數據
    '''
    if request.is_ajax():
        try:
            result = {}
            inc_id = request.GET.get("inc_id")
            vtask = VTask.objects.filter(inc_id=inc_id)
            if not vtask.exists():
                return JsonResponse(hint.get_result(hint.HintMsg.not_found_Task))
            result['state'] = 200
            result['data'] = list(vtask.values())[0]
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse(hint.get_result(hint.HintMsg.not_found_Task))

    else:
        return render(request, 'BonusApp/Task_Modif.html')

# url spectaculars/
def get_Spectaculars(request):
    
    if request.is_ajax():
        result = {}
        sql = ""
        identifying = request.GET.get("identifying")
        if identifying == "question":
            sql = "Select * from V_Task where TaskListNo = '00500-95' AND DateDiff(dd,CreateDate,getdate())<=60 order by Contact ASC,CREATE_DATE DESC"
            tasks = VTask.objects.raw(sql)
            results = []
            for t in tasks:
                results.append(model_to_dict(t))
            result["state"] = 200
            result["data"] = results
            return JsonResponse(result)

        if identifying == "technicalDoc":
            sql = "Select * from TECMB WHERE DateDiff(dd,CREATE_DATE,getdate())<=60 order by MB005 ASC,CREATE_DATE DESC"
            tecmbs = Tecmb.objects.raw(sql)
            results = []
            for t in tecmbs:
                # 借用字段来显示拼接好的id
                t.mb010 = '%s-%s-%s' % (t.pid, t.tid, t.taskid) 
                results.append(model_to_dict(t))

            result["state"] = 200
            result["data"] = results
            return JsonResponse(result)
    else:
        return render(request, 'BonusApp/Spectaculars.html')

# url spectaculars/technicalDoc_Details/ 
def technicalDoc_Details(request):
    if request.is_ajax():
        result = {}
        results = []
        technicalDoc_id = request.GET.get("technicalDoc_id")
        # 判断是否获取到id
        if technicalDoc_id != None:
            # 分割进行数据查询
            tdNo = technicalDoc_id.split("-")
            # %s：占位符
            sql = "select * from TECMB where Pid = '%s' and Tid='%s' and TaskID = '%s'" % (
                tdNo[0], tdNo[1], tdNo[2])
            # 执行原生态sql
            tecmb = Tecmb.objects.raw(sql)
            # 遍历转换成字典型
            for t in tecmb:
                results.append(model_to_dict(t))
            # 等于0就是没有查到
            if len(results) == 0:
                return JsonResponse(hint.get_result(hint.HintMsg.not_found_TenicalDoc))
            else:
                result["state"] = 200
                result["data"] = results[0]
                return JsonResponse(result)
        else:
            return JsonResponse(hint.get_result(hint.HintMsg.not_found_TenicalDoc))
    else:
        return render(request, 'BonusApp/technicalDoc_Details.html')

# bouns/ 首页“+”号按钮 增加操作
def Task_Add(request):
    return render(request,'BonusApp/Task_Add.html')

def Add_Task(request):
    t = request.POST.get("tasktype")
    description = request.POST.get("description")
    score = request.POST.get("score")
    tasktype = Tasktype()
    tasktype.tasktype = t
    tasktype.description = description
    tasktype.score = score
    tasktype.save()

    result = {}
    result['state'] = 200
    result['message'] = "添加成功！"
    return JsonResponse(result)

def bonus_analysis_part(request):
    taskQuery = list(Syspara.objects.filter(ftype='Query', nfield='TaskQuery'))
    def getRequestQuerySetWithSysparam(queryset):
            if len(taskQuery) > 0:
                filter = taskQuery[0].fvalue.replace('%', '%%')
                return queryset.extra(where=[filter])
            return queryset    
    result = {}
    contact = request.GET.get('contact')
    edateOne = request.GET.get('edatefrom')
    edateTwo = request.GET.get('edateto')
    quarterBegin = request.GET.get('quarterbegin')
    quarterEnd = request.GET.get('quarterend')
    projectid = request.GET.get('projectid')
    recordid = request.GET.get('recordid')
    s_type = request.GET.get("s_type") ##查詢類型
    isSL = request.GET.get('isSL') == "true" #是否是模擬TaskType    
    if isSL:
        datalist = VTaskbonussl.objects.filter(contact=contact, edate__date__range=[quarterBegin, quarterEnd], progress__in=['C','F'])
        periodlist = VTaskbonussl.objects.filter(contact=contact, edate__date__range=[edateOne, edateTwo], progress__in=['C','F'])
    else:    
        datalist = VTask.objects.filter(contact=contact, edate__date__range=[quarterBegin, quarterEnd], progress__in=['C','F'])
        periodlist = VTask.objects.filter(contact=contact, edate__date__range=[edateOne, edateTwo], progress__in=['C','F'])
        if projectid:
            datalist = datalist.filter(pid=projectid)
            periodlist = periodlist.filter(pid=projectid)
        if recordid:
            datalist = datalist.filter(recordid=recordid)  
            periodlist = periodlist.filter(recordid=recordid)


    result = {'data':None}
    if s_type == "datalist":
        data = getRequestQuerySetWithSysparam(datalist).order_by('edate')
        result['data'] = [model_to_dict(row) for row in data]
    elif s_type == "workingday":
        result['data'] = getRequestQuerySetWithSysparam(datalist).values('edate__date').annotate(count=Count('edate__date')).count()
    elif s_type == "periodlist":
        data = getRequestQuerySetWithSysparam(periodlist).order_by('edate')
        result['data'] = [model_to_dict(row) for row in data]
    elif s_type == "periodworkingday":
        result['data'] = getRequestQuerySetWithSysparam(periodlist).values('edate__date').annotate(count=Count('edate__date')).count()    
    return JsonResponse(result, safe=False)

def bonus_analysis(request):
    '''
    功能描述：根據設定的查詢條件計算聯繫人的獎金
    '''
    def getRequestQuerySetWithSysparam(queryset):
        rs = Syspara.objects.filter(ftype='Query', nfield='TaskQuery')
        if len(rs) > 0:
            filter = rs[0].fvalue.replace('%', '%%')
            return queryset.extra(where=[filter])
        return queryset    
    result = {}
    contact = request.GET.get('contact')
    edateOne = request.GET.get('edatefrom')
    edateTwo = request.GET.get('edateto')
    quarterBegin = request.GET.get('quarterbegin')
    quarterEnd = request.GET.get('quarterend')
    calSat = request.GET.get('calSat') == "true" #是否計算周六上班
    isSL = request.GET.get('isSL') == "true" #是否是模擬TaskType
    if(contact==""):     
        # 如果聯繫人為空的時候，只需要查詢日期範圍內的任務（Goal除外）
        # 並且不計算獎金
        #datalist = VTask.objects.values('contact','taskno','task','edate','score','progress','lookupscore','realtasktype','tasktypedc','inc_id','pid','tid','taskid') \
        #Q(edate__range=(edateOne,edateTwo)) &
        #Q(edate__get=edateOne) & Q(edate__lt=newdate) &
     
        #enddate = datetime.strptime(edateTwo, "%Y/%m/%d") #把字符中轉成日期類型
        #newdate = enddate + timedelta(days=1) #得到+1天的日期
        #edate =datetime.strftime(newdate, "%Y/%m/%d") #把日期轉成字符串
  
        datalist = VTask.objects.filter(Q(edate__date__range=(edateOne,edateTwo)) &
                                       ~Q(tasklistno__endswith='57') & ~Q(tasklistno__endswith='55') & 
                                       ~Q(tasklistno__endswith='52')) \
                                       .order_by('contact','-edate')
        result['state'] = 200
        result['errorMessage'] = ''
        result['data'] = list(datalist.values()) # 任務列表數據
        return JsonResponse(result)

    # 得到用戶設置的Bonus參數
    bonusPara = Syspara.objects.filter((Q(desp='BonusApp',ftype=contact) & ~Q(nfield='BudgetAllowance')) | \
            Q(desp='BonusApp', nfield='BudgetAllowance', ftype='Bonus') | \
            Q(desp='BonusApp', nfield='UnitPrice', ftype='Bonus')).values('nfield','fvalue') 
    if len(bonusPara)!=8:
        result['errorMessage'] = '當前用戶（{}）設置的獎金參數不完整'.format(contact)
        return JsonResponse(result)
    
    #users = VUsers.objects.filter(username=contact) 
    # 獲得扣分信息
    '''
    deductions = Userdeduction.objects.filter(username=contact,deductiondate__range=(edateOne, edateTwo))
    deductionScore = 0
    for deduction in deductions:
        deductionScore = deductionScore - deduction.score
    '''
    #修改了上班天數的獲取方式
    '''
    WorkingDay = workdays(quarterBegin,quarterEnd,calSat) # 默認上班天數
    periodWorkingDay = workdays(edateOne,edateTwo,calSat) # 默認查詢條件上班天數
    date = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now()+timedelta(days=-1)).strftime('%Y-%m-%d')
    isToday = edateOne==edateTwo==date
    isYesterday = edateOne==edateTwo==yesterday
    # 得到用戶的實際上班天數
    if users.exists():
        workno = users[0].workno
        if (workno!='') and (workno!=None):
            connstr = 'DRIVER={0};SERVER={1};PORT=1433;DATABASE={2};UID={3};PWD={4};TDS_Version={5};'.format('FreeTDS',settings.EMP_SERVER,settings.EMPDB_NAME,settings.EMPDB_USER,settings.EMPDB_PASSWORD,'7.1')
            ##創建數據庫連接對象
            conn = pyodbc.connect(connstr)
            with conn.cursor() as cursor:     
                # 從每日考勤表中統計上班天數           
                sql = "select sum(Days) as WorkingDay from T_AR where WorkNo='{0}' and RQ between '{1}' and '{2}'".format(workno,quarterBegin,quarterEnd)
                for row in cursor.execute(sql):
                    if row.WorkingDay==None:
                        WorkingDay=0
                    else:   
                        WorkingDay = row.WorkingDay 
            # 獲得查詢條件的上班天數 
            if not isToday and not isYesterday:
                with conn.cursor() as cursor:     
                    # 從每日考勤表中統計上班天數           
                    sql = "select sum(Days) as WorkingDay from T_AR where WorkNo='{0}' and RQ between '{1}' and '{2}'".format(workno,edateOne,edateTwo)
                    for row in cursor.execute(sql):
                        if row.WorkingDay:                             
                            periodWorkingDay = row.WorkingDay 

            conn.close()  
    if WorkingDay==0:
        result['errorMessage'] = '當前用戶（{}）在查詢的時間範圍內上班天數為零，不可計算獎金'.format(contact)
        return JsonResponse(result)  
    '''      
    # 結合查詢條件
    #condition = '''EDate between '{0}' and '{1}' and contact='{2}' and Progress='C' and 
    #            LookUpScore>0 and CAST(RIGHT(TID,3) AS INT)<200 and RIGHT(TID,2) not in ('52','55','57')'''.format(edateOne,edateTwo,contact)  
    #datalist = VTask.objects.filter(edate__range=(edateOne,edateTwo),contact=contact,tasktypescore__gt=0).order_by('-edate')
    #datalist = VTask.objects.values('contact','taskno','task','edate','score','progress','lookupscore','realtasktype','tasktypedc','inc_id') \
    #        .extra(where=[condition]).order_by('edate')
    if isSL:
        datalist = VTaskbonussl.objects.filter(contact=contact, edate__date__range=[quarterBegin, quarterEnd], progress__in=['C','F'])
        periodlist = VTaskbonussl.objects.filter(contact=contact, edate__date__range=[edateOne, edateTwo], progress__in=['C','F'])
    else:    
        datalist = VTask.objects.filter(contact=contact, edate__date__range=[quarterBegin, quarterEnd], progress__in=['C','F'])
        periodlist = VTask.objects.filter(contact=contact, edate__date__range=[edateOne, edateTwo], progress__in=['C','F'])

    datalist = getRequestQuerySetWithSysparam(datalist).order_by('edate')
    WorkingDay = getRequestQuerySetWithSysparam(datalist).values('edate__date').annotate(count=Count('edate__date')).count()

    periodlist = getRequestQuerySetWithSysparam(periodlist).order_by('edate')
    periodWorkingDay = getRequestQuerySetWithSysparam(periodlist).values('edate__date').annotate(count=Count('edate__date')).count()

    # 總任務績效分
    totalScore = 0
    # 總任務Lookup績效分
    totalLookupScore = 0
    # 總管理任務績效分
    totalManagementScore = 0
    # 總管理任務Lookup績效分
    totalManagementLookupScore = 0
    # 查詢條件的任務管理分
    totalPeriodManagementScore = 0
    managementTaskType = '130'
    tmpSyspara = Syspara.objects.filter(nfield='ManagementTaskType',ftype='Bonus')
    if tmpSyspara:
       managementTaskType = tmpSyspara.first().fvalue

    tasktypedata = []
    mapObj = {} #定義一個用於存放Tasktype列表的集合   
    for task in datalist: 
        #if task.score==None:
            #continue           
        totalScore = totalScore + (task.score or 0)
        # 計算管理績效分
        if task.realtasktype and task.realtasktype[:len(managementTaskType)]==managementTaskType:
            totalManagementScore = totalManagementScore + (task.score or 0)
            #if not task.lookupscore is None:
            totalManagementLookupScore = totalManagementLookupScore + (task.lookupscore or 0)
        #if not task.lookupscore is None:
        totalLookupScore = totalLookupScore + (task.lookupscore or 0)
        
        
    periodScore = 0
    periodLookupScore = 0
    for task in periodlist: 
        #if (task.score==None) or (task.score==0):
            #continue  
        tasktype = {}   #定義一個TaskType的dict對象 
        
        #if not task.lookupscore is None:                    
        periodLookupScore = periodLookupScore + (task.lookupscore or 0)
        #if not task.score is None:
        periodScore = periodScore + (task.score or 0)
            
        # 計算管理績效分
        if task.realtasktype and task.realtasktype[:len(managementTaskType)]==managementTaskType:
            #if not task.score is None: 
            totalPeriodManagementScore = totalPeriodManagementScore + (task.score or 0)
        # 當TaskType在集合中不存在時，則定義一個新的
        if task.realtasktype not in mapObj:  
            tasktype["tasktype"] = task.realtasktype
            tasktype["description"] = task.tasktypedc
            tasktype["count"] = 1
            tasktype["score"] = (task.score or 0)
            tasktype["lookupscore"] = (task.lookupscore or 0)
        else:
            # 存在時，先在集合中獲得Tasktype信息
            tasktype = mapObj[task.realtasktype]        
            tasktype["count"] = tasktype["count"] + 1 # 累加數量
 
        tasktype["totalscore"] = tasktype["score"] * tasktype["count"]
        tasktype["totallookupscore"] = tasktype["lookupscore"] * tasktype["count"]
        mapObj[task.realtasktype] = tasktype

    # 把集合轉成List對象    
    for tasktype in mapObj.keys():
        tasktypedata.append(mapObj[tasktype]) 


    paraObj= {m['nfield']:float(m['fvalue']) for m in bonusPara} 
    
    paraObj["QuarterWorkingDay"] = workdays(get_quarter_begin(edateOne),get_quarter_end(edateOne),calSat) # 當前查詢季度的工用天數
    paraObj["WorkingDay"] = WorkingDay # 工作天數
    paraObj["Score"] = totalScore # Total Tasks Score    
    paraObj["LookupScore"] = totalLookupScore # Total Tasks Lookup Score
    paraObj["ManagementScore"] = totalManagementScore # Total Management Score
    paraObj["ManagementLookupScore"] = totalManagementLookupScore # Total Management Lookup Score
    paraObj["PeriodScore"] = periodScore # Total Task on the period
    paraObj["PeriodLookupScore"] = periodLookupScore # Total Task on the period
    paraObj["PeriodWorkingDay"] = periodWorkingDay # 當前查詢條件的工作天數
    paraObj["PeriodManagementScore"] = totalPeriodManagementScore # 查詢條件的管理分

    bonusResult = calculate_bonus(paraObj)  # 根據總分和Bonus參數計算獎金 
    # 定義返回結果對象    
    result['state'] = 200
    result['errorMessage'] = ''
    result['data'] = list(periodlist.values()) # 任務列表數據    
    result['bonusResult'] = bonusResult # 計算結果
    result['tasktypedata'] = tasktypedata
    result['contact'] = contact
    return JsonResponse(result)


def bonus_analysis_new(request):
    '''
    功能描述：根據設定的查詢條件計算聯繫人的獎金
    '''
    def getRequestQuerySetWithSysparam(queryset):
        rs = Syspara.objects.filter(ftype='Query', nfield='TaskQuery')
        if len(rs) > 0:
            filter = rs[0].fvalue.replace('%', '%%')
            return queryset.extra(where=[filter])
        return queryset    
    result = {}
    contact = request.GET.get('contact')
    edateOne = request.GET.get('edatefrom')
    edateTwo = request.GET.get('edateto')
    projectid = request.GET.get('projectid')
    recordid = request.GET.get('recordid')
    quarterBegin = request.GET.get('quarterbegin')
    quarterEnd = request.GET.get('quarterend')
    calSat = request.GET.get('calSat') == "true" #是否計算周六上班
    isSL = request.GET.get('isSL') == "true" #是否是模擬TaskType
    if(contact==""):     
        # 如果聯繫人為空的時候，只需要查詢日期範圍內的任務（Goal除外）
        # 並且不計算獎金
        #datalist = VTask.objects.values('contact','taskno','task','edate','score','progress','lookupscore','realtasktype','tasktypedc','inc_id','pid','tid','taskid') \
        #Q(edate__range=(edateOne,edateTwo)) &
        #Q(edate__get=edateOne) & Q(edate__lt=newdate) &
     
        #enddate = datetime.strptime(edateTwo, "%Y/%m/%d") #把字符中轉成日期類型
        #newdate = enddate + timedelta(days=1) #得到+1天的日期
        #edate =datetime.strftime(newdate, "%Y/%m/%d") #把日期轉成字符串
  
        datalist = VTask.objects.filter(Q(edate__date__range=(edateOne,edateTwo)) &
                                       ~Q(tasklistno__endswith='57') & ~Q(tasklistno__endswith='55') & 
                                       ~Q(tasklistno__endswith='52'))
        if projectid:
            datalist = datalist.filter(pid=projectid)
        if recordid:
            datalist = datalist.filter(recordid=recordid)    

        datalist.order_by('contact','-edate')
        result['state'] = 200
        result['errorMessage'] = ''
        result['data'] = list(datalist.values()) # 任務列表數據
        return JsonResponse(result)

    # 得到用戶設置的Bonus參數
    bonusPara = Syspara.objects.filter((Q(desp='BonusApp',ftype=contact) & ~Q(nfield='BudgetAllowance')) | \
            Q(desp='BonusApp', nfield='BudgetAllowance', ftype='Bonus') | \
            Q(desp='BonusApp', nfield='UnitPrice', ftype='Bonus')).values('nfield','fvalue') 
    if len(bonusPara)!=8:
        result['errorMessage'] = '當前用戶（{}）設置的獎金參數不完整'.format(contact)
        return JsonResponse(result)
    
    #users = VUsers.objects.filter(username=contact) 
    # 獲得扣分信息
    '''
    deductions = Userdeduction.objects.filter(username=contact,deductiondate__range=(edateOne, edateTwo))
    deductionScore = 0
    for deduction in deductions:
        deductionScore = deductionScore - deduction.score
    '''
    #修改了上班天數的獲取方式
    '''
    WorkingDay = workdays(quarterBegin,quarterEnd,calSat) # 默認上班天數
    periodWorkingDay = workdays(edateOne,edateTwo,calSat) # 默認查詢條件上班天數
    date = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now()+timedelta(days=-1)).strftime('%Y-%m-%d')
    isToday = edateOne==edateTwo==date
    isYesterday = edateOne==edateTwo==yesterday
    # 得到用戶的實際上班天數
    if users.exists():
        workno = users[0].workno
        if (workno!='') and (workno!=None):
            connstr = 'DRIVER={0};SERVER={1};PORT=1433;DATABASE={2};UID={3};PWD={4};TDS_Version={5};'.format('FreeTDS',settings.EMP_SERVER,settings.EMPDB_NAME,settings.EMPDB_USER,settings.EMPDB_PASSWORD,'7.1')
            ##創建數據庫連接對象
            conn = pyodbc.connect(connstr)
            with conn.cursor() as cursor:     
                # 從每日考勤表中統計上班天數           
                sql = "select sum(Days) as WorkingDay from T_AR where WorkNo='{0}' and RQ between '{1}' and '{2}'".format(workno,quarterBegin,quarterEnd)
                for row in cursor.execute(sql):
                    if row.WorkingDay==None:
                        WorkingDay=0
                    else:   
                        WorkingDay = row.WorkingDay 
            # 獲得查詢條件的上班天數 
            if not isToday and not isYesterday:
                with conn.cursor() as cursor:     
                    # 從每日考勤表中統計上班天數           
                    sql = "select sum(Days) as WorkingDay from T_AR where WorkNo='{0}' and RQ between '{1}' and '{2}'".format(workno,edateOne,edateTwo)
                    for row in cursor.execute(sql):
                        if row.WorkingDay:                             
                            periodWorkingDay = row.WorkingDay 

            conn.close()  
    if WorkingDay==0:
        result['errorMessage'] = '當前用戶（{}）在查詢的時間範圍內上班天數為零，不可計算獎金'.format(contact)
        return JsonResponse(result)  
    '''      
    # 結合查詢條件
    #condition = '''EDate between '{0}' and '{1}' and contact='{2}' and Progress='C' and 
    #            LookUpScore>0 and CAST(RIGHT(TID,3) AS INT)<200 and RIGHT(TID,2) not in ('52','55','57')'''.format(edateOne,edateTwo,contact)  
    #datalist = VTask.objects.filter(edate__range=(edateOne,edateTwo),contact=contact,tasktypescore__gt=0).order_by('-edate')
    #datalist = VTask.objects.values('contact','taskno','task','edate','score','progress','lookupscore','realtasktype','tasktypedc','inc_id') \
    #        .extra(where=[condition]).order_by('edate')
    params = {}
    params.update(request.GET.dict())
    url = AsyncioTools.get_url(request,"bonus_analysis_part",True)
    http_methods = {key:{'url':url+'?s_type='+key, 'params':params} for key in ['datalist','workingday','periodlist','periodworkingday']}
    datas = AsyncioTools.async_fetch_http_json(http_methods)
    if isSL:
        datalist = [VTaskbonussl(**row) for row in datas['datalist']['data']]
        periodlist = [VTaskbonussl(**row) for row in datas['periodlist']['data']]
    else:
        datalist = [VTask(**row) for row in datas['datalist']['data']]
        periodlist = [VTask(**row) for row in datas['periodlist']['data']]
    WorkingDay = datas['workingday']['data']
    
    periodWorkingDay = datas['periodworkingday']['data']

    userdeduction = Userdeduction.objects.filter(deductiondate__range=(edateOne, edateTwo),username=contact).values('username').annotate(sum_score=Sum('score'))
    deductionScore = 0
    if userdeduction:
        deductionScore = userdeduction[0]['sum_score']

    totalScore = 0
    # 總任務Lookup績效分
    totalLookupScore = 0
    # 總管理任務績效分
    totalManagementScore = 0
    # 總管理任務Lookup績效分
    totalManagementLookupScore = 0
    # 查詢條件的任務管理分
    totalPeriodManagementScore = 0
    managementTaskType = '130'
    tmpSyspara = Syspara.objects.filter(nfield='ManagementTaskType',ftype='Bonus')
    if tmpSyspara:
       managementTaskType = tmpSyspara.first().fvalue

    tasktypedata = []
    mapObj = {} #定義一個用於存放Tasktype列表的集合   
    for task in datalist: 
        #if task.score==None:
            #continue           
        totalScore = totalScore + (task.score or 0)
        # 計算管理績效分
        if task.realtasktype and task.realtasktype[:len(managementTaskType)]==managementTaskType:
            totalManagementScore = totalManagementScore + (task.score or 0)
            #if not task.lookupscore is None:
            totalManagementLookupScore = totalManagementLookupScore + (task.lookupscore or 0)
        #if not task.lookupscore is None:
        totalLookupScore = totalLookupScore + (task.lookupscore or 0)
        
        
    periodScore = 0
    periodLookupScore = 0
    for task in periodlist: 
        #if (task.score==None) or (task.score==0):
            #continue  
        tasktype = {}   #定義一個TaskType的dict對象 
        
        #if not task.lookupscore is None:                    
        periodLookupScore = periodLookupScore + (task.lookupscore or 0)
        #if not task.score is None:
        periodScore = periodScore + (task.score or 0)
            
        # 計算管理績效分
        if task.realtasktype and task.realtasktype[:len(managementTaskType)]==managementTaskType:
            #if not task.score is None: 
            totalPeriodManagementScore = totalPeriodManagementScore + (task.score or 0)
        # 當TaskType在集合中不存在時，則定義一個新的
        if task.realtasktype not in mapObj:  
            tasktype["tasktype"] = task.realtasktype
            tasktype["description"] = task.tasktypedc
            tasktype["count"] = 1
            tasktype["score"] = (task.score or 0)
            tasktype["lookupscore"] = (task.lookupscore or 0)
        else:
            # 存在時，先在集合中獲得Tasktype信息
            tasktype = mapObj[task.realtasktype]        
            tasktype["count"] = tasktype["count"] + 1 # 累加數量
 
        tasktype["totalscore"] = tasktype["score"] * tasktype["count"]
        tasktype["totallookupscore"] = tasktype["lookupscore"] * tasktype["count"]
        mapObj[task.realtasktype] = tasktype

    # 把集合轉成List對象    
    for tasktype in mapObj.keys():
        tasktypedata.append(mapObj[tasktype]) 


    paraObj= {m['nfield']:float(m['fvalue']) for m in bonusPara} 
    
    paraObj["QuarterWorkingDay"] = workdays(get_quarter_begin(edateOne),get_quarter_end(edateOne),calSat) # 當前查詢季度的工用天數
    paraObj["WorkingDay"] = WorkingDay # 工作天數
    paraObj["Score"] = totalScore # Total Tasks Score    
    paraObj["LookupScore"] = totalLookupScore # Total Tasks Lookup Score
    paraObj["ManagementScore"] = totalManagementScore # Total Management Score
    paraObj["ManagementLookupScore"] = totalManagementLookupScore # Total Management Lookup Score
    paraObj["PeriodScore"] = periodScore # Total Task on the period
    paraObj["PeriodLookupScore"] = periodLookupScore # Total Task on the period
    paraObj["PeriodWorkingDay"] = periodWorkingDay # 當前查詢條件的工作天數
    paraObj["PeriodManagementScore"] = totalPeriodManagementScore # 查詢條件的管理分
    paraObj["DeductionScore"] = deductionScore

    bonusResult = calculate_bonus(paraObj)  # 根據總分和Bonus參數計算獎金 
    # 定義返回結果對象    
    result['state'] = 200
    result['errorMessage'] = ''
    result['data'] = [model_to_dict(row) for row in periodlist] # 任務列表數據    
    result['bonusResult'] = bonusResult # 計算結果
    result['tasktypedata'] = tasktypedata
    result['contact'] = contact
    return JsonResponse(result)


def bonus_recalculate(request):
    result = {}
    para = request.GET.get("bonusPara")  
    bonusPara = json.loads(para)
    #totalScore = bonusPara["TotalScore"]
    #totalLookupScore = bonusPara["TotalLookupScore"]
    bonusResult = calculate_bonus(bonusPara)
    
    result['state'] = "OK"
    result['data'] = bonusResult # 計算結果
    return JsonResponse(result)

def calculate_bonus(bonusPara):
    '''
    功能描述：根據總分和設定的Bonus參數計算獎金
    '''
    totalScore = bonusPara["Score"]
    totalLookupScore = bonusPara["LookupScore"]
    totalManagementScore = bonusPara["ManagementScore"]
    totalManagementLookupScore = bonusPara["ManagementLookupScore"]
    totalPeriodManagementScore = bonusPara["PeriodManagementScore"]
    totalPeriodScore = bonusPara["PeriodScore"]
    deductionScore = bonusPara["DeductionScore"]

    # 模擬計算
    # 季度理想得分
    PerfectScoring = bonusPara["Salary"] * (1 + bonusPara["BudgetAllowance"]/100) * 3/bonusPara['UnitPrice']
    # 季度管理分
    ManagementS = PerfectScoring * bonusPara["RatioOFM"]/100
    # 季度跟進分
    PerformanceS = PerfectScoring * bonusPara["RatioOFP"]/100
    # 理想每日平均分
    #SuggAvg = (PerfectScoring - ManagementS - PerformanceS) / bonusPara["QuarterWorkingDay"]
    SuggAvg = PerfectScoring / bonusPara["QuarterWorkingDay"]
    # 模擬季度總分
    #SimulateScore = SuggAvg * bonusPara["QuarterWorkingDay"] + ManagementS + PerformanceS
    SimulateScore = PerfectScoring
    # 模擬每月得到的總金額（包括獎金+工資）
    #SimulatePerMth = SimulateScore * bonusPara['UnitPrice']/3

    # 實際計算
    # 每日平均Score
    #ScoreAvg = totalScore / bonusPara["WorkingDay"]
    if not bonusPara["PeriodWorkingDay"]==0:
        ScoreAvg = (totalPeriodScore + totalPeriodManagementScore*bonusPara["ManagementRatio"]/100 + totalPeriodScore*bonusPara["PerformanaceRatio"]/100 - deductionScore) / bonusPara["PeriodWorkingDay"]
    else:
        ScoreAvg = 0
    # 每日平均Lookup Score
    #LookupScoreAvg = totalLookupScore / bonusPara["WorkingDay"]
    #LookupScoreAvg = (totalLookupScore + totalManagementLookupScore*bonusPara["ManagementRatio"]/100 + totalLookupScore*bonusPara["PerformanaceRatio"]/100) / paraObj["PeriodWorkingDay"]
    # 季度總分
    #QuarterScore = ScoreAvg * bonusPara["QuarterWorkingDay"] + ManagementS * bonusPara["ManagementRatio"]/100 + PerformanceS * bonusPara["PerformanaceRatio"]/100   
    #QuarterScore = totalManagementScore * bonusPara["RatioOFM"]/100 * bonusPara["ManagementRatio"]/100 + (totalScore - totalManagementScore) + (totalScore - totalManagementScore) * bonusPara["RatioOFP"]/100 * bonusPara["PerformanaceRatio"]/100
    if not bonusPara["WorkingDay"]==0:
        QuarterScore = totalScore + (totalManagementScore*bonusPara["ManagementRatio"]/100 + totalScore*bonusPara["PerformanaceRatio"]/100) / bonusPara["WorkingDay"] - deductionScore
        QuarterLookupScore = totalLookupScore + (totalManagementLookupScore*bonusPara["ManagementRatio"]/100 + totalLookupScore*bonusPara["PerformanaceRatio"]/100) / bonusPara["WorkingDay"] - deductionScore
    else:
        QuarterScore = 0
        QuarterLookupScore = 0
    # 季度總Lookup分
    #QuarterLookupScore = LookupScoreAvg * bonusPara["QuarterWorkingDay"] + ManagementS * bonusPara["ManagementRatio"]/100 + PerformanceS * bonusPara["PerformanaceRatio"]/100
    #QuarterLookupScore = totalManagementLookupScore * bonusPara["RatioOFM"]/100 * bonusPara["ManagementRatio"]/100 + (totalLookupScore-totalManagementLookupScore) + (totalLookupScore-totalManagementLookupScore) * bonusPara["RatioOFP"]/100 * bonusPara["PerformanaceRatio"]/100
    

    # 模擬每月得到的總金額
    SimulatePerMth = (ScoreAvg * bonusPara["QuarterWorkingDay"])*bonusPara['UnitPrice']/3
    # 季度獎金得分
    #ScoreBonus = QuarterScore - bonusPara["Salary"]*3/bonusPara['UnitPrice']
    ScoreBonus = QuarterScore - bonusPara["Salary"]*bonusPara["WorkingDay"]/bonusPara["QuarterWorkingDay"]
    # 季度獎金Lookup得分
    #LookupScoreBonus = QuarterLookupScore - bonusPara["Salary"]*3/bonusPara['UnitPrice']
    LookupScoreBonus = QuarterLookupScore - bonusPara["Salary"]*bonusPara["WorkingDay"]/bonusPara["QuarterWorkingDay"]
    # 季度總分
    ScoreActualQuarter = bonusPara["Salary"]*3/bonusPara['UnitPrice'] + ScoreBonus
    # 季度總Lookup分
    LookupScoreActualQuarter = bonusPara["Salary"]*3/bonusPara['UnitPrice'] + LookupScoreBonus
    # 每月實得金額（含獎金+工資）
    #ActInPerMth = ScoreActualQuarter/3*bonusPara['UnitPrice']
    ActInPerMth = (SimulatePerMth-bonusPara["Salary"])*3
    # 季度實得獎金
    #ActQuarterBonusAmount = round(ScoreBonus,2) * bonusPara['UnitPrice']
    #ActQuarterLookupBonusAmount = round(LookupScoreBonus,2) * bonusPara['UnitPrice']
    ActQuarterBonusAmount = QuarterScore - bonusPara["Salary"] * 3 
    ActQuarterLookupBonusAmount = QuarterLookupScore - bonusPara["Salary"] * 3 

    bonusPara["TotalScore"] = totalScore
    bonusPara["TotalLookupScore"] = totalLookupScore

    bonusPara["PerfectScoring"] = round(PerfectScoring,2) # Perfect Scoring
    bonusPara["ManagementS"] = round(ManagementS,2) # Management S
    bonusPara["PerformanceS"] = round(PerformanceS,2) # Performance. S
    bonusPara["ScoreAvg"] = round(ScoreAvg,2) # Avg Daily on a period
    #bonusPara["LookupScoreAvg"] = round(LookupScoreAvg,2) # Avg Daily on a period
    bonusPara["SuggAvg"] = round(SuggAvg,2)  # Sugg.Avg
    bonusPara["QuarterScore"] = round(QuarterScore,2) # Final Score For The Quarter
    bonusPara["QuarterLookupScore"] = round(QuarterLookupScore,2) # Final Score For The Quarter
    bonusPara["SimulateScore"] = round(SimulateScore,2) # Simulate Score Base On Budget
    bonusPara["ScoreBonus"] = round(ScoreBonus,2) # Bonus Score
    bonusPara["LookupScoreBonus"] = round(LookupScoreBonus,2) # Bonus Score
    bonusPara["SimulatePerMth"] = round(SimulatePerMth,2) # Simulate Total Take In $Per Mth
    bonusPara["ScoreActualQuarter"] = round(ScoreActualQuarter,2) # S Actual Quarter
    bonusPara["LookupScoreActualQuarter"] = round(LookupScoreActualQuarter,2) # S Actual Quarter
    bonusPara["ActInPerMth"] = round(ActInPerMth,2) # Simulated bonus for the quarter
    bonusPara["ActQuarterBonusAmount"] = round(ActQuarterBonusAmount,2) # Actual Bonus $ for the quarter
    bonusPara["ActQuarterLookupBonusAmount"] = round(ActQuarterLookupBonusAmount,2) # Actual Bonus $ for the quarter
    
    return bonusPara

def get_quarter_begin(date):
    '''
    功能描述：根據日期得到季度的開始日期
    '''
    if type(date) == str:
        date = datetime.strptime(date,'%Y-%m-%d').date()
    quarter = (date.month-1)/3+1
    if quarter == 1:
        return datetime(date.year,1,1)
    elif quarter == 2:
        return datetime(date.year,4,1)
    elif quarter == 3:
        return datetime(date.year,7,1)
    else:
        return datetime(date.year,10,1)

def get_quarter_end(date):
    '''
    功能描述：根據日期得到季度的結束日期
    '''
    if type(date) == str:
        date = datetime.strptime(date,'%Y-%m-%d').date()
    quarter = (date.month-1)/3+1
    if quarter == 1:
        return datetime(date.year,3,31)
    elif quarter == 2:
        return datetime(date.year,6,30)
    elif quarter == 3:
        return datetime(date.year,9,30)
    else:
        return datetime(date.year,12,31)

def workdays(start,end,calSat):
    '''
    计算两个日期间的工作日
    start:开始时间
    end:结束时间
    calSat:是否計算周六
    ''' 
    # 字符串格式日期的处理
    if type(start) == str:
        start = datetime.strptime(start,'%Y-%m-%d').date()
    if type(end) == str:
        end = datetime.strptime(end,'%Y-%m-%d').date()
    # 开始日期大，颠倒开始日期和结束日期
    if start > end:
        start,end = end,start
    '''
    counts = 0
    while True:
        if start > end:
            break
        #if is_workday(start,calSat):
        if is_workday(start):
            counts += 1
        start += timedelta(days=1)
    return counts
    '''
    day_count = 0
    # Loop through each day in the range
    current_date = start
    while current_date <= end:
        if current_date.weekday() != 6:  # Check if the day is not a Sunday (Python counts Monday as 0 and Sunday as 6)
            day_count += 1
        current_date += timedelta(days=1)

    return day_count

def json_to_model(request):
    result = {}
    jsonString = request.POST.get("jsonObj")    
    obj = json.loads(jsonString)
    syspara = Syspara()
    syspara.nfield = obj["nfield"]
    syspara.ftype = obj["ftype"]
    syspara.fvalue = obj["fvalue"]
    syspara.save()
    result["state"] = "OK"
    return JsonResponse(result)

def auditScore(request):
    result = {'status': False, 'msg': ''}
    tasks = request.POST.get("tasks")
    audit = request.POST.get("audit")
    url = settings.BONUS_SERVICE_URL #已发布的接口
    client=suds.client.Client(url)
    service = client.service
    if audit=='Y':
        msg = service.autitScore('json',tasks)
    else:
        msg = service.unAuditWeeklyScore('json',tasks)
    msg_json = json.loads(str(msg))
    if msg_json['status'] == True:
        result['status'] = True
        result["msg"] = msg_json['msg']   
    else:
        result["msg"] = '訪問WebService失敗'     
    return JsonResponse(result)


# 看板图形显示汇总Bonus 
def get_bonusStatistics(request):
    edatefrom = request.GET.get('edatefrom')
    edateto = request.GET.get('edateto')
    calSat = request.GET.get('calSat')
    isSL = request.GET.get('isSL')
    result = analyse(edatefrom, edateto, calSat, isSL)    
    return JsonResponse(result)
    
def analyse(edatefrom,edateto,calSat,isSL):    
    # 創建異步對象
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop) 
    tasks=[]    
    users = list(VUsers.objects.filter(groupname='電腦部',dept='Mis').values())
    tasks=loop.run_until_complete(async_main(users,edatefrom,edateto,calSat,isSL))
    result = {'bonusResult':{}, 'taskTypeList':[]}
    mapObj = {} #定義一個用於存放Tasktype列表的集合   
    for item in tasks:
        if(item._result) and ('contact' in item._result.keys()):
            result['bonusResult'][item._result['contact']] = item._result['bonusResult']
            for tasktype in item._result['tasktypedata']:
                if not tasktype['tasktype']:
                    continue
                if tasktype['tasktype'] not in mapObj:
                    mapObj[tasktype['tasktype']] = tasktype
                else:
                    mapObj[tasktype['tasktype']]['count'] += tasktype['count']
            for key, value in mapObj.items():
                value['score'] = value['lookupscore'] if value['lookupscore'] else 0
                value['totalscore'] = value['score'] * value['count']
                value['totallookupscore'] = value['totalscore']
    # 把集合轉成List對象    
    for tasktype in mapObj.keys():
        result['taskTypeList'].append(mapObj[tasktype])
    result['taskTypeList'] = sorted(result['taskTypeList'], key=lambda t:t['tasktype'])
    #result = {item._result['contact']:item._result['bonusResult'] for item in tasks if(item._result) and ('contact' in item._result.keys())} 

    return result    

async def async_main(users,edatefrom,edateto,calSat,isSL):
    '''處理異步動作'''
    start = datetime.now() 
    headers={'Content-Type': 'application/json'}    
    #url='http://222.118.20.236:8011/bonus/bonus_analysis' 
    async with aiohttp.ClientSession(headers=headers) as client:
        tasks = []   
        for user in users:
            # 讀取用戶的獎金信息
            tasks.append(asyncio.create_task(fetch(client,settings.BONUS_ANALYSIS_URL,user['username'],edatefrom,edateto,calSat,isSL)))                      
        await asyncio.wait(tasks) # 等待所有異步操作的返回結果
    end = datetime.now()
    print("總花费时间为：")
    print(end - start)
    return tasks  

async def fetch(client,url,contact,edatefrom,edateto,calSat,isSL): 
    '''異步調用接口'''   
    params={'contact':contact,'edatefrom':edatefrom,'edateto':edateto,'calSat':calSat,'isSL':isSL, 'quarterbegin':edatefrom,'quarterend':edateto}
    async with client.get(url,params=params) as resp:
        assert resp.status == 200
        return await resp.json()

def getTaskTypeSL(request):
    result = {'status':False, 'msg':'', 'data':[]}
    def get_LSTasktype():
        qs = LSTasktypelist.objects.all()
        parents = {item.tasktype:model_to_dict(item) for item in qs if not item.parenttype}
        detail = [model_to_dict(item) for item in qs if item.parenttype]
        result = []
        for tasktype in detail:
            if tasktype['parenttype'] in parents.keys():
                parent = parents[tasktype['parenttype']]
                description = "{0}-{1}".format(parent['description'], tasktype['description'])
                tasktype_str = "{0}-{1}-".format(parent['tasktype'], tasktype['tasktype'])
                dtasktype_str = "{0}-{1}-".format(parent['tasktype'], tasktype['displaytype'])
                result.append({'tasktype':tasktype_str+"1",'dtasktype':dtasktype_str+"1", "description":description, "score":tasktype['difficulties1']})
                result.append({'tasktype':tasktype_str+"2", 'dtasktype':dtasktype_str+"2", "description":description, "score":tasktype['difficulties2']})
                result.append({'tasktype':tasktype_str+"3", 'dtasktype':dtasktype_str+"3", "description":description, "score":tasktype['difficulties3']})
        return result
    try:
        tasktype_list = get_LSTasktype()
        tasktypesl_list = TasktypeSl.objects.all()
        tasktype_list_map = {item['tasktype']:item for item in tasktype_list}
        tasktypesl_list_map = {item.tasktype:item for item in tasktypesl_list}
        update_list = []
        create_list = []
        for item in tasktype_list:
            if item['tasktype'] in tasktypesl_list_map: #已經存在
                tasktype = tasktypesl_list_map[item['tasktype']]
                if item['description'] != tasktype.description or item['score'] != tasktype.oldscore or item['dtasktype'] != tasktype.dtasktype: #如果描述原Score不同則更新
                    tasktype.description = item['description']
                    tasktype.oldscore = item['score']
                    tasktype.dtasktype = item['dtasktype']
                    if tasktype.score == None: #如果當前模擬Score為Null, 則使用原Score替換
                        tasktype.score = item['score']
                    update_list.append(tasktype)
            else: #不存在則創建
                new_takstype = TasktypeSl(tasktype=item['tasktype'], dtasktype=item['dtasktype'], description=item['description'], oldscore=item['score'], score=item['score'])
                create_list.append(new_takstype)
        delete_keys = [key for key in tasktypesl_list_map.keys() if key not in tasktype_list_map.keys()]
        with transaction.atomic(ModelTools.get_database(TasktypeSl)):            
            if len(delete_keys) > 0:
                TasktypeSl.objects.filter(tasktype__in=delete_keys).delete()
            if len(update_list) > 0:
                TasktypeSl.objects.bulk_update(update_list, fields=['description','oldscore','score','dtasktype'], batch_size=50)
            if len(create_list) > 0:
                TasktypeSl.objects.bulk_create(create_list, batch_size=50)
        qs = TasktypeSl.objects.all()
        result['status'] = True
        result['data'] = [model_to_dict(item) for item in qs]
        return JsonResponse(result, safe=False)
    except Exception as e:
        print(str(e))
        return JsonResponse(result, safe=False)

def updateTaskTypeSL(request):
    def saveTaskType():
        """
        功能描述：將模擬修改後的Task Type更新到真實的Task Type和SL Task Type中
        """
        StrSQL = """UPDATE A SET 
            Difficulties1=CASE WHEN B.Diff1 IS NOT NULL THEN B.Diff1 ELSE A.Difficulties1 END,
            Difficulties2=CASE WHEN B.Diff2 IS NOT NULL THEN B.Diff2 ELSE A.Difficulties2 END,
            Difficulties3=CASE WHEN B.Diff3 IS NOT NULL THEN B.Diff3 ELSE A.Difficulties3 END
            FROM {0} A
            INNER JOIN (SELECT T.ParentType,T.TaskType,
            SUM(CASE when DiffNum='1' THEN Score ELSE NULL END) Diff1,
            SUM(CASE when DiffNum='2' THEN Score ELSE NULL END) Diff2,
            SUM(CASE when DiffNum='3' THEN Score ELSE NULL END) Diff3
            FROM (
            SELECT PARSENAME(REPLACE(TaskType, '-', '.'), 3) ParentType,PARSENAME(REPLACE(TaskType, '-', '.'), 2) TaskType,PARSENAME(REPLACE(TaskType, '-', '.'), 1) DiffNum,Score
            FROM dbo.TaskType_SL WHERE Score <> OldScore) T
            GROUP BY T.ParentType, T.TaskType) B
            ON A.ParentType = B.ParentType AND A.TaskType = B.TaskType
            """
        try:
            with transaction.atomic(ModelTools.get_database(TasktypeSl)):
                with connections[ModelTools.get_database(TasktypeSl)].cursor() as cursor:
                    cursor.execute(StrSQL.format("TaskTypeList"))
                    cursor.execute(StrSQL.format("LSTaskTypeList"))       
            return True
        except Exception as e:
            print(str(e))
            return False
    def getSimulationTaskTypeHistory(updateTaskTypeSLList):
        create_list = []
        try:
            source = TasktypeSl.objects.filter(inc_id__in=[item.inc_id for item in updateTaskTypeSLList])
            qs = TasktypeSlHistory.objects.aggregate(max_verno=Max('verno'))
            updateTaskTypeSLList_map = {item.inc_id:item for item in updateTaskTypeSLList}
            max_verno = 1
            if qs['max_verno']:
                max_verno = qs['max_verno'] + 1
            for item in source:
                history = TasktypeSlHistory(**model_to_dict(item))
                history.pk = None
                history.inc_id = None
                history.verno = max_verno
                history.oldscore = item.score  #將Tasktype的原score保存了old score
                tasktypesl = updateTaskTypeSLList_map[str(item.inc_id)]
                if source:
                    history.score = tasktypesl.score #將Tasktype當前Score保存到score
                create_list.append(history)
        except Exception as e:
            print(str(e))
        return create_list

    result = {'status':False, 'msg':'', 'data':None}
    try:
        updateListStr = request.POST.get("updateList")
        updateList = json.loads(updateListStr)
        updateTaskTypeSLList = []
        for item in updateList:
            tsl = TasktypeSl(inc_id=item['inc_id'], score=item['score'])
            tsl.pk = item['inc_id']
            updateTaskTypeSLList.append(tsl)
        history_create_list =  getSimulationTaskTypeHistory(updateTaskTypeSLList)
        with transaction.atomic(ModelTools.get_database(TasktypeSl)):
            TasktypeSlHistory.objects.bulk_create(history_create_list, batch_size=50)
            TasktypeSl.objects.bulk_update(updateTaskTypeSLList, fields=['score'])
            if len(updateTaskTypeSLList) > 0:
                Syspara.objects.filter(nfield='TaskTypeSl_CurVerNo',ftype='BonusSimulation').update(fvalue="-1:0")
        result['status'] = True
        qs = TasktypeSlHistory.objects.aggregate(max_verno=Max('verno'))
        if qs['max_verno']:
            result['max_verno'] = qs['max_verno']
        else:
            result['max_verno'] = 0            
        save = request.GET.get("save","")
        if save:
            result['status'] = result['status'] and saveTaskType()
    except Exception as e:
        print(str(e))
    return JsonResponse(result, safe=False)

def resetSimulationTaskType(request):
    """
    功能描述:還原Simulaton Task Type上一次更改
    """
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        verno = request.POST.get('verno')
        action = request.POST.get('action')
        if verno:
            exist_history = TasktypeSlHistory.objects.filter(verno=verno)
            if len(exist_history) > 0:
                tasktypesl_list = TasktypeSl.objects.filter(tasktype__in=exist_history.values('tasktype'))
                exist_history_map = {item.tasktype:item for item in exist_history}
                for tasktypesl in tasktypesl_list:
                    history = exist_history_map[tasktypesl.tasktype]
                    if action == 'undo':
                        tasktypesl.score = history.oldscore
                    else:
                        tasktypesl.score = history.score
                TasktypeSl.objects.bulk_update(tasktypesl_list, fields=['score'])
                #設置當前有版本和方向
                qs = TasktypeSlHistory.objects.aggregate(max_verno=Max('verno'))
                max_verno = 0 if not qs['max_verno'] else qs['max_verno']
                TaskTypeSl_CurVerNo = int(verno)
                TaskTypeSl_CurDirection = "1" if action == 'redo' else "-1"
                if (int(verno) == max_verno and action == "redo"):
                    TaskTypeSl_CurVerNo = int(verno) + 1
                if (int(verno) == 1 and action == "undo"):
                    TaskTypeSl_CurVerNo = 0;         
                result['TaskTypeSl_CurVerNo'] = TaskTypeSl_CurVerNo
                result['TaskTypeSl_CurDirection'] = TaskTypeSl_CurDirection
                Syspara.objects.filter(nfield='TaskTypeSl_CurVerNo',ftype='BonusSimulation').update(fvalue="{0}:{1}".format(TaskTypeSl_CurVerNo,TaskTypeSl_CurDirection))
        qs = TasktypeSl.objects.all()
        result['status'] = True
        result['data'] = [model_to_dict(item) for item in qs]
    except Exception as e:
        print(str(e))
    return JsonResponse(result, safe=False)

def getSimulationTaskTypeHistoryMaxVerNo(request):
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        qs = TasktypeSlHistory.objects.aggregate(max_verno=Max('verno'))
        if qs['max_verno']:
            result['max_verno'] = qs['max_verno']
        else:
            result['max_verno'] = 0
        qs = Syspara.objects.filter(nfield='TaskTypeSl_CurVerNo',ftype='BonusSimulation')
        if len(qs) > 0:
            array = qs[0].fvalue.split(":")
            result['TaskTypeSl_CurVerNo'] = int(array[0])
            result['TaskTypeSl_CurDirection'] = int(array[1])
        result['status'] = True
    except Exception as e:
        print(str(e))
    return JsonResponse(result, safe=False)

class DeductionItemDataTable(DatatablesServerSideView):
    model = Deductionitem
    columns = "__all__"
    searchable_columns = ['description']

class UserDeductionDataTable(DatatablesServerSideView):
    model = Userdeduction
    columns = "__all__"
    searchable_columns = ['username','description','deductiondate']

class UserDeductionCreativeView(SWCreateView):
    model = Userdeduction

class UserDeductionDeleteView(SWDeleteView):
    model = Userdeduction

class UserDeductionUpdateView(SWUpdateView):
    model = Userdeduction

class BonusCreditDataTable(DatatablesServerSideView):
    model = Bonuscredit
    columns = "__all__"
    searchable_columns = ['username','description','creditdate']

class BonuscreditCreativeView(SWCreateView):
    model = Bonuscredit

class BonuscreditDeleteView(SWDeleteView):
    model = Bonuscredit

class BonuscreditUpdateView(SWUpdateView):
    model = Bonuscredit

def getDeductionChartData(request):
    def getImproveID():
        id = '611'
        syspara = Syspara.objects.filter(nfield='ImproveID',ftype='Deduction').first()
        if syspara:
            id = syspara.fvalue
        return id
    # 查詢用戶的扣分匯總
    result = {'status':False, 'msg':'', 'data':{}}
    datefrom  = request.GET.get('datefrom','')
    dateto  = request.GET.get('dateto','')
    contact = request.GET.get('contact','')
    try:
        filter="TpDetailId=PenaltyID and TpMastId={0}".format(getImproveID())
        params=[]
        userDeduction = Userdeduction.objects.all()
        if datefrom:            
            userDeduction = userDeduction.filter(deductiondate__gte=datefrom)
            filter = "{0} and DeductionDate>=%s".format(filter)
            params.append(datefrom)
        if dateto:
            userDeduction = userDeduction.filter(deductiondate__lte=dateto)
            filter = "{0} and DeductionDate<=%s".format(filter)
            params.append(dateto)
        if contact:
            userDeduction = userDeduction.filter(username=contact)
            filter = "{0} and UserName=%s".format(filter)
            params.append(contact)
        #按用戶進行匯總
        userDeductionScore = userDeduction.values('username','penaltyid').annotate(sum_record=Count('penaltyid')).order_by('username','penaltyid')  
        area = Tpdetail.objects.extra(tables=['UserDeduction'],where=[filter],params=params).values('tpdetailid','tptname').distinct()
        labels=[]
        datas=[]
        #把結果集轉成Chart的Data
        for deduction in userDeductionScore:
            if deduction['penaltyid']:
                labels.append('{0}-{1}'.format(deduction['username'],int(deduction['penaltyid'])))
            else:
                labels.append(deduction['username'])
            datas.append(deduction['sum_record'])
        result['data']={'labels':labels,'datas':datas}  
        result['areadata']=list(area)
        result['status'] = True 
    except Exception as e:
        print(str(e))
        result['msg']="分析用戶的扣分失敗"
    return JsonResponse(result, safe=False) 

class ImproveareaDataTable(DatatablesServerSideView):
    model = Improvearea
    columns = "__all__"
    searchable_columns = ['description','category','position']

class ImproveareaCreativeView(SWCreateView):
    model = Improvearea

class ImproveareaDeleteView(SWDeleteView):
    model = Improvearea

class ImproveareaUpdateView(SWUpdateView):
    model = Improvearea    

def getPositionByContact(request):
    result = {'status':False, 'msg':'', 'data':''}
    contact  = request.GET.get('contact','')
    users = VUsers.objects.filter(username=contact) 
    if users.exists():
        workno = users.first().workno
        if workno:
            try:
                params = {'location':'HC,YM,JF','workno':workno}
                res = RestApiUtils.get_restapi_data('get_allman', params)
                print(res)
                for k, item in res.items():
                    if item['data']:
                        result['data']=item['data'][0]['zhuwei']                        
                        break
                result['status']=True
            except Exception as e:
                LOGGER.error(e)
    return JsonResponse(result, safe=False) 

def getDuctionCategory(request):
    result = {'status':False, 'msg':'', 'data':[]}
    field = request.GET.get('field','')
    searchvalue = request.GET.get('searchvalue','')
    count = int(request.GET.get('count','5'))
    filter = request.GET.get('filter','')
    
    if filter==None or filter=='':   
        filter="Category<>''"
    try:
        data=None
        if searchvalue:  
            sqlWhere=['{0} and {1} like %s'.format(filter,field)]            
            param=['%%{0}%%'.format(searchvalue)]
            data = Userdeduction.objects.extra(where=sqlWhere,params=param).values('category').distinct()[:count]
        else:
            data = Userdeduction.objects.extra(where=[filter]).values('category').distinct()[:count]        
       
        result['status'] = True
        result['data'] =  list(data)
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)