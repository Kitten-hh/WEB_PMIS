import json
from lib2to3.pytree import Node
from DataBase_MPMS import models
from django.forms.models import model_to_dict
from django.db.models import Count,Q,Case,Sum,When,IntegerField,Max
from django.http import JsonResponse,HttpResponse,HttpRequest
from BaseApp.library.tools import DateTools
from django.utils.translation import ugettext_lazy as _



def AnalyseProjects(request:HttpRequest):
    ##檢查傳入參數是否正確
    def check_params():
        if not username and not str_filter:
            return False, _("Please pass contact or filter in parameters"),        
        return True,""
    result = {'status':False, 'msg':'', 'data':[], 'recordids': []}
    try:
        username = request.GET.get('contact')
        recordid = request.GET.get('recordid')
        str_filter = request.GET.get('filter')
        check_status,msg = check_params()
        if check_status:
            #獲取員工優先級前五的項目和該項目下的任務數量
            result['data'], result['recordids'] = analysisUserProjectPercent(username, str_filter, recordid)
            result['status'] = True
        else:
            result['msg'] = msg
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   



def analysisUserProjectPercent(username=None, str_filter=None, recordid=None):
    '''
    功能描述：統計員工優先級前五的項目和該項目下的任務數量
    '''
    def analysis_filter():
        if not str_filter:
            return None, None, None,None
        filter_obj = json.loads(str_filter)
        recordids = list(filter(None, (filter_obj.get('recordid') or '').split(",")))
        status = list(filter(None, (filter_obj.get('taskCategory') or '').split(",")))
        user = list(filter(None, (filter_obj.get('user') or '').split(",")))
        sessions = list(filter(None, (filter_obj.get('sessions') or '').split(",")))
        if filter_obj.get('taskCategory') == 'all' or \
            (not status and user):
            status = ['MF','MH']
        if filter_obj.get('user') == 'all':
            user = []
        return recordids, status, user,sessions

    ##獲取數據
    def search_data():
        ##獲取員工Top 5 Projects
        filter_recordids, filter_status, user_filter,sessions_filter = analysis_filter()
        projects = models.Subproject.objects.values('recordid','score','projectname').all()
        if username:
            quarterly_str = '{0}-{1}'.format(DateTools.formatf(DateTools.now(),"%Y"), DateTools.getQuarter(DateTools.now()))
            projects = models.Subproject.objects.all().extra(select={'goalid':'GoalId','goaldesc':'GoalDesc'}, tables=['GoalManagement'], 
                        where=["Subproject.recordid=GoalManagement.recordid and GoalManagement.contact=%s and \
                            GoalManagement.GoalType='Q' and GoalManagement.period=%s"],
                        params=[username, quarterly_str]).values('recordid','score','projectname','goalid','goaldesc').order_by('goalid')
        else:
            projects = projects.filter(recordid__in = filter_recordids).order_by("-score")
        recordids = [project['recordid'] for project in projects]
        #讀取project對應的Must Have Task
        rs = models.VTaskRecordid.objects.extra(select={'SessionId':"V_Task_RecordId.Pid + '-' + CONVERT(Varchar(20), CONVERT(Decimal(18, 0), V_Task_RecordId.Tid))",'SDesp':'tasklist.SDesp','SParent':'tasklist.Parent'}, 
        tables=['tasklist'],
        where=['V_Task_RecordId.Pid = tasklist.Pid and V_Task_RecordId.Tid = tasklist.Tid'])
        if recordid: # 過濾傳入的recordid
            rs = rs.filter(recordid=recordid)
            projects = projects.filter(recordid=recordid)
        else:
            rs = rs.filter(recordid__in=recordids)
        if username:
            rs = rs.filter(taskcategory__in=['MF','MH'])
        else:
            if filter_status:
                rs = rs.filter(taskcategory__in=filter_status)
            if user_filter:
                rs = rs.filter(contact__in = user_filter)
            if sessions_filter:
                sessions_query = Q()
                sessions_query.connector = Q.OR
                for sessionid in sessions_filter:
                    arr = sessionid.split("-")
                    sessions_query.add(Q(pid=arr[0], tid=arr[1]), Q.OR)
                rs = rs.filter(sessions_query)
        return projects, rs, recordids

    ##分析數據
    def analysis_data(projects,tasks):
        result = {project['recordid']:{
                "project":project, 
                "tasks":[], 
                "summary":{"All_Qty":0, "Completed":0,"Completed_Qty":0, "Complete_on_time":0, "Complete_on_time_Qty":0, "Overdue_Completed":0, "Overdue_Completed_Qty":0,
                "Uncompleted":0,"Uncompleted_Qty":0, "Active":0, "Active_Qty":0, "Overdue":0, "Overdue_Qty":0, "Unoverdue":0, "Unoverdue_Qty":0,
                "planedate":''}} 
        for project in projects}
        if len(tasks) == 0: # 沒有任務時就不用計算了
            return result
        #統計Summary信息
        for task in tasks:
            recordid = task.recordid
            temp_task = model_to_dict(task);
            for field in ['SessionId','SDesp','SParent']:
                temp_task[field.lower()] = getattr(task, field)
            result[recordid]["tasks"].append(temp_task)
            summary = result[recordid]['summary']
            summary['All_Qty'] += 1
            if task.progress:
                if task.progress in 'CF':
                    summary['Completed_Qty'] += 1
                    if task.edate and DateTools.format(task.edate) <= DateTools.format(task.planedate):
                        summary['Complete_on_time_Qty'] += 1
                    else:
                        summary['Overdue_Completed_Qty'] += 1
                else:
                    summary["Uncompleted_Qty"] += 1
                    if task.progress in 'TI':
                        summary['Active_Qty'] += 1
                    if DateTools.format(task.planedate) < DateTools.format(DateTools.now()):
                        summary['Overdue_Qty'] += 1
            if task.planedate and DateTools.formatf(task.planedate,'%Y-%m-%d') > summary['planedate']:
                summary['planedate'] = DateTools.formatf(task.planedate, '%Y-%m-%d')
        summary['Unoverdue_Qty'] = summary['Uncompleted'] - summary['Overdue']
        #計算百分比
        for key,value in result.items():
            summary = value['summary']
            if summary['All_Qty'] == 0:
                continue
            summary['Completed'] = summary['Completed_Qty']/summary['All_Qty'] * 100
            summary['Complete_on_time'] = summary['Complete_on_time_Qty']/summary['All_Qty'] * 100
            summary['Overdue_Completed'] = summary['Overdue_Completed_Qty']/summary['All_Qty'] * 100
            summary['Uncompleted'] = summary['Uncompleted_Qty']/summary['All_Qty'] * 100
            summary['Active'] = summary['Active_Qty']/summary['All_Qty'] * 100
            summary['Overdue'] = summary['Overdue_Qty']/summary['All_Qty'] * 100
            summary['Unoverdue'] = summary['Unoverdue_Qty']/summary['All_Qty'] * 100
        result = dict(sorted(result.items(), key=lambda x:0 if not x[1]['project']['score'] else x[1]['project']['score'], reverse=True))
        return result
    
    projects, tasks, recordids = search_data()
    return analysis_data(projects, tasks), recordids
    
def getGoaldesc(request):
    result = {'status':False, 'msg':'', 'data':None}
    try:
        username = request.GET.get('contact')
        recordid = request.GET.get('recordid')
        if recordid:
            quarterly_str = '{0}-{1}'.format(DateTools.formatf(DateTools.now(),"%Y"), DateTools.getQuarter(DateTools.now()))
            q = Q()
            q.children.append(('recordid',recordid)) 
            q.children.append(('goaltype',"Q"))
            q.children.append(('period',quarterly_str))
            if username:
                q.children.append(('contact',username))
            goaldesc = models.Goalmanagement.objects.filter(q).values('goaldesc')
            result['data'] = [desc['goaldesc'] + '\n' for desc in goaldesc][0] 
            result['status'] = True
        else:
            result['msg'] = "no recordid"
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)  