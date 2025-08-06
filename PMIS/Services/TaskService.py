from typing import Set

from timeago.parser import date_to_datetime
from DataBase_MPMS import models
from . BaseService import BaseService
from . import QueryFilterService
from django.db.models import Count,Q,Case,Sum,When,IntegerField,Max
from django.db.models import F, ExpressionWrapper, fields
import json
import random
import math
import datetime
import timeago
from BaseApp.library.tools import DateTools
import re
import dateutil
from django.forms.models import model_to_dict

class TaskService(BaseService):
    @staticmethod        
    def getRequestQuerySetWithSysparam(queryset):
        rs = models.Syspara.objects.filter(ftype='Query', nfield='TaskQuery');
        if len(rs) > 0:
            filter = rs[0].fvalue.replace('%', '%%');
            return queryset.extra(where=[filter])
        return queryset

    @staticmethod
    def analysis_new_task(username=None, bdate=None, edate=None,search_task=False):
        if search_task:
            qs = models.VTask.objects.filter(~Q(r_flag=1))
            if username:
                qs = qs.filter(contact=username)
            qs = TaskService.getRequestQuerySetWithSysparam(qs)
            qs = qs.extra(where=['not exists (Select * from TECMB where Pid = V_Task.Pid and Tid = V_Task.Tid and TaskId=V_Task.Taskid)'])
            return [model_to_dict(item) for item in qs]
        else:
            qs = models.Task.objects.filter(~Q(r_flag=1))
            if username:
                qs = qs.filter(contact=username)            
            qs = TaskService.getRequestQuerySetWithSysparam(qs)
            qs = qs.extra(where=['not exists (Select * from TECMB where Pid = Task.Pid and Tid = Task.Tid and TaskId=Task.Taskid)'])    
            return qs.count()

    @staticmethod
    def analysis_tasktype(username=None,bdate=None, edate=None, excludeZeroScore=False):
        q = Q()
        q.conditional = 'AND'
        if username:
            q.children.append(('contact', username))
        if bdate:
            q.children.append(('edate__date__gte', bdate))
        if edate:
            q.children.append(('edate__date__lte', edate))
        rs = models.VTask.objects.filter(q).filter(progress__in=['C','F'], realtasktype__isnull=False).\
            filter(~Q(realtasktype__exact=''))
        if excludeZeroScore:
            rs = rs.filter(score__isnull=False).filter(~Q(score__exact=0))
        rs = TaskService.getRequestQuerySetWithSysparam(rs)
        rs = rs.values('realtasktype','tasktypedesc','subtasktypedesc').annotate(qty=Count('*')).order_by("-qty")
        #rs = rs.values('realtasktype','tasktypedesc','subtasktypedesc').annotate(qty=Count('*')).order_by("-qty")[:10]
        return list(rs)

    @staticmethod
    def analysis_solutiontype(username=None,bdate=None, edate=None):
        str_sql = '''Select 1 INC_ID, A.Contact contact,B.MindMapLabel mindMaplabel, Count(*) as qty from TecDailyPlanner A
            inner join (Select distinct Contact, InputDate,ItemNo,MindMapLabel from TecDailyPlannerSolution) B
            on A.Contact = B.Contact and A.InputDate = B.InputDate and A.ItemNo = B.ItemNo
            where ISNULL(B.MindMapLabel,'') <> '' AND 
			TaskNo IN (SELECT TaskNo FROM V_Task WHERE {0} CAST(EDate AS DATE) >= %s AND Cast(EDate AS DATE) <= %s AND Progress IN ('C','F')
			AND ISNULL(RealTaskType,'') <> '' AND ISNULL(Score,0) <> 0 {1})
            group by A.Contact, B.MindMapLabel
            order by A.Contact, qty DESC
        '''
        rs = models.Syspara.objects.filter(ftype='Query', nfield='TaskQuery');
        user_filter = "" if not username else "Contact=%s AND"
        attach_filter = "" if not len(rs) > 0 else "and (" + rs[0].fvalue.replace('%', '%%') + ")";
        str_sql = str_sql.format(user_filter, attach_filter)
        rs = models.Tecdailyplanner.objects.raw(str_sql, [username,DateTools.format(dateutil.parser.parse(bdate)), DateTools.format(dateutil.parser.parse(edate))])
        data = []
        for item in rs:
            data.append({key:value for key,value in item.__dict__.items() if key in ['contact', 'mindMaplabel','qty']})
        return data

    @staticmethod
    def analysis_dashboard(username=None,bdate=None, edate=None):
        '''
        功能描述：dashboard分析數據
        '''
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
                #n3_q.children.append(('edate__lte', bdate))
                n3_q.children.append(('planedate__lte', bdate))
            if edate:
                n1_q.children.append(('planedate__lte', edate))
                n2_q.children.append(('edate__lte', edate))
            return q & (n1_q | n2_q | n3_q)
        def calculate_task_performance(result):
            ##設置complete百分比，固定為60        
            assigned_percent = 60
            assigned_qty = result['all_tasks']
            if assigned_qty == 0:
                completed_percent = 0
                completed_percent_r = 0
                active_percent = 0
                active_percent_r = 0
            else:
                completed_percent = math.ceil((result['completed_taks'] / assigned_qty) * 60)
                completed_percent_r = math.ceil((result['completed_taks'] / assigned_qty) * 100)
                active_percent = math.ceil((result['active_tasks'] / assigned_qty) * 60)
                active_percent_r = math.ceil((result['active_tasks'] / assigned_qty) * 100)
            result['task_performance'] = {'assigned_percent':assigned_percent, 'completed_percent': completed_percent, 'active_percent': active_percent, \
                        'completed_percent_r':completed_percent_r, 'active_percent_r':active_percent_r}                      
        def search_task():
            fields = ('inc_id','pid','tid','taskid','contact','planbdate','planedate','bdate','edate','progress','schpriority','recordid',)
            rs = models.VTaskRecordid.objects.values(*fields).filter(get_query())
            rs = TaskService.getRequestQuerySetWithSysparam(rs)
            return list(rs)
        result = {'projects':0, 'all_tasks':0, 'active_tasks':0, 'ongoing_tasks':0, \
            'completed_taks':0, 'task_performance':{},'leader_board':[], \
            'completion_tasks':[]}
        def calculate_project_process(pro_progress):
            rs = models.Subproject.objects.values('recordid','projectname','score').filter(recordid__in=pro_progress.keys())
            for subproject in rs:
                pro_progress[subproject['recordid']]['desc'] = subproject['projectname']
                if subproject['score']:
                    pro_progress[subproject['recordid']]['score'] = subproject['score']
                else:
                    pro_progress[subproject['recordid']]['score'] = 0
            pro_progress = {key:pro_progress[key] for key in sorted(pro_progress.keys(), key=lambda recordid: pro_progress[recordid]['score'], reverse=True)}
            for key,pro in pro_progress.items():
                if pro['All_Qty'] == 0:
                    pro['Completed'] = 0
                    pro['Active'] = 0
                    pro['Overdue'] = 0
                else:
                    pro['Completed'] = pro['Completed_Qty']/pro['All_Qty'] * 100
                    pro['Active'] = pro['Active_Qty']/pro['All_Qty'] * 100
                    pro['Overdue'] = pro['Overdue_Qty']/pro['All_Qty'] * 100
            return pro_progress
        def calculate_project_process_top_project(pro_progress):
            quarterly_str = '{0}-{1}'.format(DateTools.formatf(DateTools.now(),"%Y"), DateTools.getQuarter(DateTools.now()))
            rs = models.Subproject.objects.all().extra(tables=['GoalManagement'], 
                    where=["Subproject.recordid=GoalManagement.recordid and GoalManagement.contact=%s and \
                        GoalManagement.GoalType='Q' and GoalManagement.period=%s"],
                    params=[username, quarterly_str]).values('recordid','score','projectname').order_by('-score').distinct()
            topprojects = {item['recordid']:{'desc':item['projectname'],'All_Qty':0, 'Completed':0,'Completed_Qty':0, 'Active': '0',\
                    'Active_Qty':0, 'Overdue':0, 'Overdue_Qty':0,'score':0 if not item['score'] else item['score']} for item in rs}
            qs_schmm = models.Schmm.objects.values('mm003','mm004').filter(mm001=username, mm002='P')
            user_prioritys = {row['mm003']:0 if not row['mm004'] else row['mm004'] for row in qs_schmm}
            for recordid,value in topprojects.items():
                if recordid in pro_progress:
                    value.update({key:value for key, value in pro_progress[recordid].items() if key != 'desc' and key != 'score'})
                if recordid in user_prioritys:
                    value['score'] = 0 if not user_prioritys[recordid] else user_prioritys[recordid]
            pro_progress = topprojects
            for key,pro in pro_progress.items():
                if pro['All_Qty'] == 0:
                    pro['Completed'] = 0
                    pro['Active'] = 0
                    pro['Overdue'] = 0
                else:
                    pro['Completed'] = pro['Completed_Qty']/pro['All_Qty'] * 100
                    pro['Active'] = pro['Active_Qty']/pro['All_Qty'] * 100
                    pro['Overdue'] = pro['Overdue_Qty']/pro['All_Qty'] * 100
            pro_progress = dict(sorted(pro_progress.items(), key=lambda x:0 if not x[1]['score'] else x[1]['score'], reverse=True))
            return pro_progress            
        try:
            tasks = search_task()
            result['all_tasks'] = len(tasks)
            completion = {}
            pro_progress = {}
            current_date = DateTools.format(DateTools.now())
            for task in tasks:
                ##分析project
                recordid = task['recordid']
                if not recordid:
                    recordid = 'unknow'
                if not recordid in pro_progress.keys():
                    pro_progress[recordid] = {'desc':'','All_Qty':0, 'Completed':0,'Completed_Qty':0, 'Active': '0',\
                    'Active_Qty':0, 'Overdue':0, 'Overdue_Qty':0,'score':0}
                pro_progress[recordid]['All_Qty'] += 1
                if task['progress'] in ['T','I']:
                    result['active_tasks'] += 1
                    pro_progress[recordid]['Active_Qty'] += 1
                if task['progress'] == 'T':
                    result['ongoing_tasks'] += 1  
                if task['progress'] in ['C','F']:
                    result['completed_taks'] +=1    
                    pro_progress[recordid]['Completed_Qty'] += 1
                    if task['edate']:
                        edatestr = DateTools.format(task['edate'])
                        if not edatestr in completion.keys():
                            completion[edatestr] = 0
                        completion[edatestr] += 1
                else:
                    if task['planedate'] and DateTools.format(task['planedate']) < current_date:
                        pro_progress[recordid]['Overdue_Qty'] += 1
            result['projects'] = len(pro_progress.keys())
            result['projects_recorids'] = list(pro_progress.keys())
            leader_board = calculate_project_process_top_project(pro_progress) if username else calculate_project_process(pro_progress)
            result['leader_board'] = leader_board
            result['completion_tasks'] = [{'edatestr':key, 'task_qty':value} for key, value in sorted(completion.items())]
            calculate_task_performance(result)
        except Exception as e:
            print(str(e))
        return result

    @staticmethod
    def getActiveTaskCount(username=None,bdate=None,edate=None):
        '''
        功能描述：獲取用戶或所有用戶在指定時間段內未完成的任務數據
        '''
        q = Q()
        q.conditional = 'AND'
        if username:
            q.children.append(('contact', username))
        if bdate:
            q.children.append(('planbdate__gte', bdate))
        if edate:
            q.children.append(('planedate__lte', edate))
        #rs = models.VTaskRecordid.objects.filter(~Q(progress__in='CF') & (Q(hoperation='F')) & q).aggregate(Count('pid'))
        rs = models.VTaskRecordid.objects.filter(~Q(progress__in='CF') & q)
        rs = TaskService.getRequestQuerySetWithSysparam(rs).aggregate(Count('pid'))
        print(rs)
        return rs['pid__count']

    @staticmethod
    def getOngoingTaskCount(username=None,bdate=None,edate=None):
        '''
        功能描述：獲取用戶或所有用戶在指定時間段內狀態為T的任務數據
        '''
        q = Q()
        q.conditional = 'AND'
        if username:
            q.children.append(('contact', username))
        if bdate:
            q.children.append(('planbdate__gte', bdate))
        if edate:
            q.children.append(('planedate__lte', edate))        
        #rs = models.VTaskRecordid.objects.filter(Q(progress__in='T') & (Q(hoperation='F')) & q).aggregate(Count('pid'))
        rs = models.VTaskRecordid.objects.filter(Q(progress__in='T') & q).aggregate(Count('pid'))
        print(rs)
        return rs['pid__count']    

    @staticmethod
    def analysisFinishTasks(username=None, bdate=None, edate=None):
        '''
        功能描述：獲取用戶在一個時間段完成Fixed Day類型任務的數量
        '''
        q = Q()
        q.conditional = 'AND'
        if username:
            q.children.append(('contact', username))
        if bdate:
            q.children.append(('bdate__gte', bdate))
        if edate:
            q.children.append(('edate__lte', edate))
        ##rs = models.Task.objects.filter(Q(progress__in='CF') & (Q(hoperation='F')) & q) \
        rs = models.Task.objects.filter(Q(progress__in='CF') & q)
        rs = TaskService.getRequestQuerySetWithSysparam(rs)
        rs = rs.extra(select={'edatestr':"Convert(varchar(10), edate,120)"}).values('edatestr') \
                .annotate(task_qty=Count("pid"))
        return rs
    @staticmethod
    def analysisTaskPercent(username=None, bdate=None, edate=None):
        '''
        功能描述：統計用戶在一段時間內容總任務數量，已經完成的任務數據，正在做的任務數據
        '''
        q = Q()
        q.conditional = 'AND'
        if username:
            q.children.append(('contact', username))
        if bdate:
            q.children.append(('bdate__gte', bdate))
        if edate:
            q.children.append(('edate__lte', edate))
        #rs = models.Task.objects.filter(Q(progress__in='CF') & (Q(hoperation='F')) & q).aggregate(Count('pid'))
        rs = models.Task.objects.filter(Q(progress__in='CF') & q)
        rs = TaskService.getRequestQuerySetWithSysparam(rs).aggregate(Count('pid'))
        complete_qty = rs['pid__count']

        q = Q()
        q.conditional = 'AND'
        if username:
            q.children.append(('contact', username))
        if bdate:
            q.children.append(('planbdate__gte', bdate))
        if edate:
            q.children.append(('planedate__lte', edate))
        #rs = models.Task.objects.filter((Q(hoperation='F')) & q).aggregate(Count('pid'))
        rs = models.Task.objects.filter(q)
        rs = TaskService.getRequestQuerySetWithSysparam(rs).aggregate(Count('pid'))
        assigned_qty = rs['pid__count']

        #rs = models.Task.objects.filter(Q(progress__in='TI') & (Q(hoperation='F')) & q).aggregate(Count('pid'))
        rs = models.Task.objects.filter(Q(progress__in='TI') & q)
        rs = TaskService.getRequestQuerySetWithSysparam(rs).aggregate(Count('pid'))
        active_qty = rs['pid__count']

        ##設置complete百分比，固定為60        
        assigned_percent = 60
        if assigned_qty == 0:
            completed_percent = 0
            completed_percent_r = 0
            active_percent = 0
            active_percent_r = 0
        else:
            completed_percent = math.ceil((complete_qty / assigned_qty) * 60)
            completed_percent_r = math.ceil((complete_qty / assigned_qty) * 100)
            active_percent = math.ceil((active_qty / assigned_qty) * 60)
            active_percent_r = math.ceil((active_qty / assigned_qty) * 100)
        return {'assigned_percent':assigned_percent, 'completed_percent': completed_percent, 'active_percent': active_percent, \
                       'completed_percent_r':completed_percent_r, 'active_percent_r':active_percent_r}
    @staticmethod
    def analysisUserProjectPercent(username=None, bdate=None, edate=None):
        '''
        功能描述：統計過去一段時間員工的Project進度
        '''
        q = Q()
        q.conditional = 'AND'
        if username:
            q.children.append(('contact', username))
        if bdate:
            q.children.append(('planbdate__gte', bdate))
        if edate:
            q.children.append(('planedate__lte', edate))        
        #rs = models.Task.objects.filter((Q(hoperation='F')) & q).values('contact').annotate(Count('pid'))
        rs = models.VTaskRecordid.objects.filter(q)
        rs = TaskService.getRequestQuerySetWithSysparam(rs)
        rs = rs.extra(select={'desc':'SubProject.ProjectName'}, tables=['SubProject'], where=["V_Task_RecordId.recordid=SubProject.recordid"]).\
             values('recordid','desc').annotate(Count('pid'))
        all_tasks = {}
        result = {}
        for row in rs:
            all_tasks[row['recordid']] = row['pid__count']
            result[row['recordid']] = {'desc':row['desc'],'All_Qty':row['pid__count'], 'Completed':0,'Completed_Qty':0, 'Active': '0','Active_Qty':0, 'Overdue':0, 'Overdue_Qty':0}
        q.children.clear()
        if username:
            q.children.append(('contact', username))
        if bdate:
            q.children.append(('bdate__gte', bdate))
        if edate:
            q.children.append(('edate__lte', edate))
        #rs = models.Task.objects.filter(Q(progress__in='CF') & (Q(hoperation='F')) & q).values('contact').annotate(Count('pid'))
        rs = models.VTaskRecordid.objects.filter(Q(progress__in='CF') & q)
        rs = TaskService.getRequestQuerySetWithSysparam(rs)
        rs = rs.values('recordid').annotate(Count('pid'))
        for row in rs:
            l_recordid = row['recordid']
            qty = row['pid__count']
            if l_recordid in all_tasks:
                all_qty = all_tasks[l_recordid]
                result[l_recordid]['Completed'] = qty/all_qty * 100
                result[l_recordid]['Completed_Qty'] = qty
        q.children.clear()
        if username:
            q.children.append(('contact', username))        
        if bdate:
            q.children.append(('planbdate__gte', bdate))
        if edate:
            q.children.append(('planedate__lte', edate))        
        #rs = models.Task.objects.filter(Q(progress__in='TI') & (Q(hoperation='F')) & q).values('contact').annotate(Count('pid'))
        rs = models.VTaskRecordid.objects.filter(Q(progress__in='TI') & q)
        rs = TaskService.getRequestQuerySetWithSysparam(rs)
        rs = rs.values('recordid').annotate(Count('pid'))
        for row in rs:
            l_recordid = row['recordid']
            qty = row['pid__count']
            if l_recordid in all_tasks:
                all_qty = all_tasks[l_recordid]
                result[row['recordid']]['Active'] = qty/all_qty * 100
                result[row['recordid']]['Active_Qty'] = qty
        now = datetime.datetime.now()
        #rs = models.Task.objects.filter(~Q(progress__in='CF') & (Q(hoperation='F')) & q & Q(planedate__lt=now)).values('contact').annotate(Count('pid'))
        rs = models.VTaskRecordid.objects.filter(~Q(progress__in='CF')  & q & Q(planedate__lt=now))
        rs = TaskService.getRequestQuerySetWithSysparam(rs)
        rs = rs.values('recordid').annotate(Count('pid'))
        for row in rs:
            l_recordid = row['recordid']
            qty = row['pid__count']
            if l_recordid in all_tasks:
                all_qty = all_tasks[l_recordid]
                result[row['recordid']]['Overdue'] = qty/all_qty * 100
                result[row['recordid']]['Overdue_Qty'] = qty
        ##按完成數量從大到小排序
        result = {key:result[key] for key in sorted(result.keys(), key=lambda recordid: result[recordid]['Completed'], reverse=True)}
        return result

    @staticmethod
    def getActiveProjects(username=None,bdate=None, edate=None):
        q = Q()
        q.conditional = 'AND'
        if username:
            q.children.append(('contact', username))
        if bdate:
            q.children.append(('planbdate__gte', bdate))
        if edate:
            q.children.append(('planedate__lte', edate))
        #rs = models.VTaskRecordid.objects.filter(~Q(progress__in='CF') & (Q(hoperation='F')) & q).\
        rs = models.VTaskRecordid.objects.filter(~Q(progress__in='CF') & q)
        rs = TaskService.getRequestQuerySetWithSysparam(rs)
        rs = rs.extra(select={'desc':'SubProject.ProjectName'}, tables=['SubProject'], where=["V_Task_RecordId.recordid=SubProject.recordid"]).\
             values('recordid','desc').distinct()
        result = {}
        recordids = []
        for row in rs:
            recordid = row['recordid']
            title = row['desc']
            simple_title = ''
            if re.search('[a-zA-z]+', title):
                simple_title = re.search('[a-zA-z]+', title).group(0).upper()
                if len(simple_title) > 2:
                    simple_title = simple_title[:2]
            result[recordid] = {'title':row['desc'],'s_title':simple_title, 'progress':0, 'last_update':''}
            recordids.append(recordid)
        ##分析子工程的進度
        #sub_rs = models.VTaskRecordid.objects.filter(Q(recordid__in=recordids) &(Q(hoperation='F')) & q).values('recordid').annotate(completed_qty=Sum(
        sub_rs = models.VTaskRecordid.objects.filter(Q(recordid__in=recordids) & q).values('recordid').annotate(completed_qty=Sum(
            Case(
                When(progress__in='CF', then=1),
                default=0,
                output_field=IntegerField()
            )),
            task_qty=Count('pid'),
            last_update = Max('create_date')
        )
        for row in sub_rs:
            recordid = row['recordid']
            completed_qty = row['completed_qty']
            task_qty = row['task_qty']
            last_update = row['last_update']
            percent = math.ceil(completed_qty/task_qty * 100)
            try:
                last_update = last_update[:8]
                last_update = timeago.format(DateTools.parse(last_update), datetime.datetime.now())
            except:
                last_update = ''
            result[recordid]['progress'] = percent
            result[recordid]['last_update'] = last_update
        return result

    @staticmethod
    def getSessionPercent(username=None,bdate=None, edate=None):
        q = Q()
        q.conditional = 'AND'
        if username:
            q.children.append(('contact', username))
        if bdate:
            q.children.append(('planbdate__gte', bdate))
        if edate:
            q.children.append(('planedate__lte', edate))
        #rs = models.VTaskRecordid.objects.filter(~Q(progress__in='CF') & (Q(hoperation='F')) & q).\
        rs = models.VTask.objects.filter(~Q(progress__in='CF') & q)
        rs = TaskService.getRequestQuerySetWithSysparam(rs)
        rs = rs.values('tasklistno','tiddesc').distinct()
        result = {}
        sessions = []
        for row in rs:
            session = row['tasklistno']
            title = row['tiddesc']
            simple_title = ''
            if re.search('[a-zA-z]+', title):
                simple_title = re.search('[a-zA-z]+', title).group(0).upper()
                if len(simple_title) > 2:
                    simple_title = simple_title[:2]
            result[session] = {'title':"{0} {1}".format(session,row['tiddesc']),'s_title':simple_title, 'progress':0, 'last_update':''}
            sessions.append(session)

        ##分析Session的進度
        #sub_rs = models.VTaskRecordid.objects.filter(Q(recordid__in=recordids) &(Q(hoperation='F')) & q).values('recordid').annotate(completed_qty=Sum(
        sub_rs = models.VTask.objects.filter(Q(tasklistno__in=sessions) & q).values('tasklistno').annotate(completed_qty=Sum(
            Case(
                When(progress__in='CF', then=1),
                default=0,
                output_field=IntegerField()
            )),
            task_qty=Count('pid'),
            last_update = Max('create_date')
        )
        for row in sub_rs:
            sessionid = row['tasklistno']
            completed_qty = row['completed_qty']
            task_qty = row['task_qty']
            last_update = row['last_update']
            percent = math.ceil(completed_qty/task_qty * 100)
            try:
                last_update = last_update[:8]
                last_update = timeago.format(DateTools.parse(last_update), datetime.datetime.now())
            except:
                last_update = ''
            result[sessionid]['progress'] = percent
            result[sessionid]['last_update'] = last_update
        ##按完成數量從大到小排序
        result = {key:result[key] for key in sorted(result.keys(), key=lambda sessionid: result[sessionid]['progress'], reverse=True)}
        return result

    @staticmethod
    def getToDos(username=None,bdate=None,edate=None):
        '''
        功能描述：獲取用戶在這個時間段內的ToDos
        '''
        q = Q()
        q.conditional = 'AND'
        if username:
            q.children.append(('contact', username))
        if bdate:
            q.children.append(('planbdate__gte', bdate))
        if edate:
            q.children.append(('planedate__lte', edate))
        #rs = models.VTaskRecordid.objects.filter(Q(progress__in='T') & (Q(hoperation='F')) & q).
        rs = models.VTaskRecordid.objects.filter(Q(progress__in='T') & q).\
             extra(select={'project_desc':'SubProject.ProjectName'}, tables=['SubProject'], where=["V_Task_RecordId.recordid=SubProject.recordid"]).\
             values('recordid','project_desc','inc_id','task', 'planedate').order_by('recordid')
        result = {}
        index = 1
        for row in rs:
            recordid = row['recordid']
            if not recordid in result:
                result[recordid] = []
            result[recordid].append(row)
        return result

    @staticmethod
    def getAchievement(username=None, bdate=None, edate=None,group='M'):
        '''
        功能描述：獲取用戶這一年的任務完成情況
        '''
        result = {}
        q = Q()
        q.conditional = 'AND'
        if username:
            q.children.append(('contact', username))
        if bdate:
            q.children.append(('edate__gte', bdate))
        if edate:
            q.children.append(('edate__lte', edate))
        rs = models.Task.objects.filter(Q(progress__in='CF') & q)
        rs = TaskService.getRequestQuerySetWithSysparam(rs)        
        if group == 'Y':
            rs = rs.extra(select={'edatestr':"left(Convert(varchar(8), edate,112),4)"}).values('edatestr')
        elif group == 'M':
            rs = rs.extra(select={'edatestr':"left(Convert(varchar(8), edate,112),6)"}).values('edatestr')
        else:
            rs = rs.extra(select={'edatestr':"Convert(varchar(8), edate,112)"}).values('edatestr')
        rs = rs.annotate(task_qty=Count("pid"))

        for row in rs:
            edatestr = row['edatestr']
            count = row['task_qty']
            result[edatestr] = {'date':edatestr,'completed':count, 'assigned':0}
        q.children.clear()
        if username:
            q.children.append(('contact', username))
        if bdate:
            q.children.append(('planbdate__gte', bdate))
        if edate:
            q.children.append(('planbdate__lte', edate))
        rs = models.Task.objects.filter(q)
        rs = TaskService.getRequestQuerySetWithSysparam(rs)     
        if group == 'Y':
            rs = rs.extra(select={'edatestr':"left(Convert(varchar(8), planbdate,112),4)"}).values('edatestr')
        elif group == 'M':
            rs = rs.extra(select={'edatestr':"left(Convert(varchar(8), planbdate,112),6)"}).values('edatestr')
        else:
            rs = rs.extra(select={'edatestr':"Convert(varchar(8), planbdate,112)"}).values('edatestr')
        rs = rs.annotate(task_qty=Count("pid"))
        for row in rs:
            edatestr = row['edatestr']
            count = row['task_qty']            
            if edatestr in result:
                result[edatestr]['assigned'] = count
            else:
                result[edatestr] = {'date':edatestr,'completed':0, 'assigned':count}
        result_arr = []
        for key,value in result.items():
            result_arr.append(value)
        return result_arr

    @staticmethod
    def getProjectsSpent(username=None,bdate=None, edate=None):
        '''
        功能描述：獲取用戶過去一段時間工程所共的時間
        '''
        q = Q()
        q.conditional = 'AND'
        if username:
            q.children.append(('contact', username))
        if bdate:
            q.children.append(('planbdate__gte', bdate))
        if edate:
            q.children.append(('planedate__lte', edate))
        rs = models.VTaskRecordid.objects.filter(Q(hoperation='F') & q).\
             extra(select={'desc':'SubProject.ProjectName'}, tables=['SubProject'], where=["V_Task_RecordId.recordid=SubProject.recordid"]).\
             values('recordid','desc').distinct()
        result = {}
        recordids = []
        for row in rs:
            recordid = row['recordid']
            title = row['desc']
            simple_title = ''
            if re.search('[a-zA-z]+', title):
                simple_title = re.search('[a-zA-z]+', title).group(0).upper()
                if len(simple_title) > 2:
                    simple_title = simple_title[:2]
            result[recordid] = {'title':row['desc'],'s_title':simple_title, 'progress':0, 'hours_spent':''}
            recordids.append(recordid)        
        ##分析子工程的進度
        sub_rs = models.VTaskRecordid.objects.filter(Q(recordid__in=recordids) & Q(hoperation='F') & q).values('recordid').\
        annotate(duration=ExpressionWrapper(F('edate') - F('bdate'), output_field=fields.DurationField())).values('recordid').\
        annotate(completed_qty=Sum(
            Case(
                When(progress__in='CF', then=1),
                default=0,
                output_field=IntegerField()
            )),
            task_qty=Count('pid'),
            hours_spent = Sum(
                Case(
                    When(Q(progress__in='CF',bdate__isnull=False, edate__isnull=False), then='duration'),
                    default=0,
                    output_field=IntegerField()
            ))
        )
        for row in sub_rs:
            recordid = row['recordid']
            completed_qty = row['completed_qty']
            task_qty = row['task_qty']
            hours_spent = row['hours_spent']
            percent = math.ceil(completed_qty/task_qty * 100)
            result[recordid]['progress'] = percent            
            date_diff = datetime.timedelta(microseconds=hours_spent)
            result[recordid]['hours_spent'] = '{0}:{1}'.format(math.ceil(date_diff.total_seconds()//3600 - date_diff.days * 16), math.ceil(date_diff.total_seconds()%3600//60))
        result_arr = []
        for key,value in result.items():
            result_arr.append(value)
        return result_arr            

    @staticmethod
    def getTaskSpent(username=None,bdate=None,edate=None):
        '''
        功能描述：獲取用戶在這個時間段內的ToDos
        '''
        q = Q()
        q.conditional = 'AND'
        if username:
            q.children.append(('contact', username))
        if bdate:
            q.children.append(('planbdate__gte', bdate))
        if edate:
            q.children.append(('planedate__lte', edate))
        rs = models.VTaskRecordid.objects.filter(Q(progress__in='T') & Q(hoperation='F') & q).\
             extra(select={'project_desc':'SubProject.ProjectName'}, tables=['SubProject'], where=["V_Task_RecordId.recordid=SubProject.recordid"]).\
             values('recordid','project_desc','task', 'planedate','bdate').order_by('planedate')
        result = []
        index = 1
        for row in rs:
            title = row['project_desc']
            bdate = row['bdate']
            planedate = row['planedate']
            simple_title = ''
            if re.search('[a-zA-z]+', title):
                simple_title = re.search('[a-zA-z]+', title).group(0).upper()
                if len(simple_title) > 2:
                    simple_title = simple_title[:2]            
            worked = 0
            estimate = 0
            try:
                now = datetime.datetime.now(tz=bdate.tzinfo)
                interval = now - bdate
                hour = math.ceil(interval.total_seconds()//3600 - interval.days * 16)
                minutes = math.ceil(interval.total_seconds()%3600//60)
                worked = '{0}:{1}'.format(hour, minutes)
                estimate = '{0}:{1}'.format(random.randint(8, 24), random.randint(1, 36))
            except Exception as e:
                print(str(e))
            due_date = ''
            try:
                due_date = timeago.format(planedate, datetime.datetime.now(tz=planedate.tzinfo))
            except:
                pass
            result.append({'s_title':simple_title, 'task':row['task'], 'due_date':due_date, 'estimate':estimate, 'worked': worked})
        return result

##############################################################################################
##以上為原來Demo的代碼
##############################################################################################
    @staticmethod
    def get_max_taskid(pid, tid):
        qs = models.Task.objects.values('taskid').filter(Q(pid=pid) & Q(tid=tid)).order_by('-taskid')[:1]
        max_task_id = 10
        if len(qs) > 0:
            max_task_id = qs[0]['taskid']
            max_task_id = int(max_task_id/10) * 10 + 10
        return max_task_id        
    
    @staticmethod
    def get_progress_list():
        '''
        功能描述：獲取任務的進度
        '''
        return ['N','I','T','H','S','C','F','R','NF']

    @staticmethod
    def get_default_session(username):
        '''
        功能描述：獲取用戶默認工程
        '''
        queryset = models.Pmsut.objects.filter(ut001=username)
        if len(queryset) > 0:
            return queryset[0]
        else:
            return None