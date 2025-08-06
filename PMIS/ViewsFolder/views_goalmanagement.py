from typing import Set
from django.db.models.fields import CharField
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.template import loader
from django.http import HttpResponse,JsonResponse,HttpRequest
from django.db.models import Sum,Count,Max,Min,Avg,Q,Case,When,IntegerField,Value,ExpressionWrapper
from BaseApp.library.cust_views.SWDeleteView import SWDeleteView
from DataBase_MPMS import models
from .. import forms
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from datatableview import Datatable
from django.db import connections
from datatableview.views import MultipleDatatableView
from datatableview.views.legacy import LegacyDatatableView
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
from DataBase_MPMS import models
import logging
from django.db import transaction
from PMIS.Services.GoalManageService import GoalManagementService
from PMIS.Services.TemplateService import TemplateService
from django.core.paginator import Paginator
import re
from django.utils.translation import ugettext_lazy as _

LOGGER = logging.Logger(__name__)

class GoalManagementView(DatatablesServerSideView):
    model=models.VTaskRecordid
    service = GoalManagementService()
    tempSservice = TemplateService()
    columns = ['recordid','pid','tid','taskid','task','contact','planedate','progress']
    searchable_columns = columns

    def get_initial_queryset(self):
        return self.generateQuery()
    
    def generateQuery(self):
        '''
        功能描述：生成查詢條件
        查詢該聯繫人當前Quarterly Goal中關聯的Project中沒有完成的Must Finish和Must Have的Goal
        '''
        #是否顯示默認跟進人員
        read_detail = self.request.GET.get("read_detail",'false') == 'true'
        if read_detail:
            taskno = self.request.GET.get('master_taskno')
            recordid = self.request.GET.get('master_recordid')
            return models.VTaskRecordid.objects.filter(taskcategory='MH', planedate__date__lte=DateTools.now(), relationgoalid=taskno, recordid=recordid)\
                .filter(~Q(progress='C') & ~Q(progress='F')).extra(select={'taskno':"CONVERT(Varchar(10), Pid) + '-' + CONVERT(Varchar(20), CONVERT(Decimal(18, 0), Tid)) + '-' + CONVERT(Varchar(10), CONVERT(Decimal(18, 0), TaskID))"})
        else:
            contact = self.request.GET.get('contact')
            goaldesc = self.request.GET.get("goaldesc")
            contacts = [] if not contact else [contact]
            if not contact:
                isDefault = self.request.GET.get('default',"false") == "true"
                if isDefault:
                    contacts = self.tempSservice.getTodayFollowupUser()
            quarterly_str = '{0}-{1}'.format(DateTools.formatf(DateTools.now(),"%Y"), DateTools.getQuarter(DateTools.now()))
            params = [quarterly_str]
            whereStr = "recordid in (Select recordid from GoalManagement where GoalType='Q' and Period=%s {0})"
            if contacts:
                whereStr = whereStr.format(" and Contact in ({0})")
                inStr = ""
                for contact in contacts:
                    inStr += "%s,"
                    params.append(contact)
                inStr = inStr[:len(inStr)-1]
                whereStr = whereStr.format(inStr)
            else:
                whereStr = whereStr.format("")
            qs = models.VTaskRecordid.objects.filter(taskcategory='MF', planedate__date__lte=DateTools.now())\
                .filter(~Q(progress='C') & ~Q(progress='F')).extra(select={'taskno':"CONVERT(Varchar(10), Pid) + '-' + CONVERT(Varchar(20), CONVERT(Decimal(18, 0), Tid)) + '-' + CONVERT(Varchar(10), CONVERT(Decimal(18, 0), TaskID))"}, where=[whereStr], params=params)
            if contacts:
                qs = qs.filter(contact__in=contacts)
            if goaldesc:
                qs = qs.filter(task__icontains=goaldesc)
            return qs
            

    def prepare_results(self, qs):
        '''
        功能描述：將查詢返回的model數據解析出來
        '''
        json_data = []

        for cur_object in qs:
            retdict = {fieldname: self.render_column(cur_object, fieldname)
                       for fieldname in self.columns}
            retdict['taskno'] = getattr(cur_object,'taskno')
            retdict['DT_RowId'] = cur_object.pk
            self.customize_row(retdict, cur_object)
            json_data.append(retdict)
        return json_data

def searchGoalManagement(request:HttpRequest):
    ##檢查傳入參數是否正確
    def check_params():
        if not str_search_filter and not str_filter:
            return False, _("Please pass search_filter or filter in parameters"),        
        return True,""
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        str_search_filter = request.GET.get("search_filter")
        str_filter = request.GET.get('filter')
        check_status,msg = check_params()
        if check_status:
            #獲取員工優先級前五的項目和該項目下的任務數量
            result['data'] = analysisGoalManagement(str_search_filter, str_filter)
            result['status'] = True
        else:
            result['msg'] = msg
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   



def analysisGoalManagement(str_search_filter=None, str_filter=None):
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
        if filter_obj.get('taskCategory') == 'all' or (not status):
            status = ['MF','MH']
        if filter_obj.get('user') == 'all':
            user = []
        return recordids, status, user,sessions
    def analysis_search_filter():
        if not str_search_filter:
            return None,None
        filter_obj = json.loads(str_search_filter)
        recordids = list(filter(None, (filter_obj.get('recordids') or '').split(",")))
        contacts = list(filter(None, (filter_obj.get('contacts') or '').split(",")))
        return contacts, recordids

    def get_filter_query(qs, str_filter, user_filter, sessions_filter):
        if str_filter:
            if user_filter:
                qs = qs.filter(contact__in = user_filter)
            if sessions_filter:
                sessions_query = Q()
                sessions_query.connector = Q.OR
                for sessionid in sessions_filter:
                    arr = sessionid.split("-")
                    sessions_query.add(Q(pid=arr[0], tid=arr[1]), Q.OR)
                qs = qs.filter(sessions_query)
        return qs

    ##獲取數據
    def search_data():
        filter_recordids, filter_status, user_filter,sessions_filter = analysis_filter()
        contacts,search_recordids = analysis_search_filter()
        projects = models.Subproject.objects.values('recordid','score','projectname').all()
        if str_filter:
            projects = projects.filter(recordid__in = filter_recordids).order_by("-score")
        else:
            quarterly_str = '{0}-{1}'.format(DateTools.formatf(DateTools.now(),"%Y"), DateTools.getQuarter(DateTools.now()))
            whereStr = '''Subproject.recordid=GoalManagement.recordid and \
                            GoalManagement.GoalType='Q' and GoalManagement.period=%s{0}'''
            params = [quarterly_str]
            if contacts:
                whereStr = whereStr.format(" and GoalManagement.Contact in ({0})")
                inStr = ""
                for contact in contacts:
                    inStr += "%s,"
                    params.append(contact)
                inStr = inStr[:len(inStr)-1]
                whereStr = whereStr.format(inStr)
            else:
                whereStr = whereStr.format("")
            whereStr += "{0}"
            if search_recordids:
                whereStr = whereStr.format(" and Subproject.recordid in ({0})")
                inStr = ""
                for recordid in search_recordids:
                    inStr += "%s,"
                    params.append(recordid)
                inStr = inStr[:len(inStr)-1]
                whereStr = whereStr.format(inStr)
            else:
                whereStr = whereStr.format("")
            projects = models.Subproject.objects.all().extra(select={'goalid':'GoalId','goaldesc':'GoalDesc'}, tables=['GoalManagement'], 
                        where=[whereStr],
                        params=params).values('recordid','score','projectname','goalid','goaldesc').order_by('goalid')
            
        recordids = [project['recordid'] for project in projects]

        #先查詢Must Finish
        qs = models.VTaskRecordid.objects.filter(recordid__in = recordids, taskcategory='MF', planedate__date__lte=DateTools.now())\
        .filter(~Q(progress='C') & ~Q(progress='F'))\
        .extra(select={'inc_id':"U0.INC_ID",'taskno':"CONVERT(Varchar(10), U0.Pid) + '-' + CONVERT(Varchar(20), CONVERT(Decimal(18, 0), U0.Tid)) + '-' + CONVERT(Varchar(10), CONVERT(Decimal(18, 0), U0.TaskID))"})
        if contacts: #如果有聯繫人查詢條件，只查詢聯繫人的Must Finish和Must Finish的下級有聯繫人沒有完成的Must Have
            qs = qs.extra(where=["contact=%s"], params=[contacts[0]])
            #qs = qs.extra(where=["(contact = %s or exists (Select * from Task where relationgoalid=CONVERT(Varchar(10), U0.Pid) + '-' + CONVERT(Varchar(20), CONVERT(Decimal(18, 0), U0.Tid)) + '-' + CONVERT(Varchar(10), CONVERT(Decimal(18, 0), U0.TaskID))\
            #    and taskcategory='MH' and CAST([PlanEDate] AS date) <= %s and progress not in ('C','F') and contact=%s))"], 
            #    params=[contacts[0],DateTools.now(), contacts[0]])
        qs = qs.values('taskno')
        #qs = get_filter_query(qs, str_filter, user_filter, sessions_filter)

        #根據Must Finish的TaskNo和ID查詢Must Finish和它下級Must Have任務
        fields = list([a.attname for a in models.VTaskRecordid._meta.get_fields() if a.attname not in ['emaildesp']])
        fields.extend(['sessionid','sdesp','sparent'])
        rs = models.VTaskRecordid.objects.extra(select={'sessionid':"V_Task_RecordId.Pid + '-' + CONVERT(Varchar(20), CONVERT(Decimal(18, 0), V_Task_RecordId.Tid))", \
        'sdesp':'tasklist.SDesp','sparent':'tasklist.Parent'}, 
        tables=['tasklist'],
        where=["V_Task_RecordId.Pid = tasklist.Pid and V_Task_RecordId.Tid = tasklist.Tid"])\
        .filter(planedate__date__lte=DateTools.now()).filter(~Q(progress='C') & ~Q(progress='F'))
        rs = get_filter_query(rs, str_filter, user_filter, sessions_filter)
        must_have_rs = rs.filter(recordid__in = recordids, taskcategory='MH',relationgoalid__in=qs.values("taskno")).values(*fields)
        if str_filter:
            if len(filter_status) == 2: #表示查詢must finish和must have
                rs = rs.filter(inc_id__in=qs.values("inc_id")).values(*fields).union(must_have_rs)
            elif "MH" in filter_status: #查詢must have
                rs = must_have_rs
            else: #查詢must finish
                rs = rs.filter(inc_id__in=qs.values("inc_id")).values(*fields)
        else:
            rs = rs.filter(inc_id__in=qs.values("inc_id")).values(*fields).union(must_have_rs)
        return projects, rs

    ##分析數據
    def analysis_data(projects,tasks):
        result = {project['recordid']:{
                "project":project, 
                "tasks":[], 
                "summary":{"All_Qty":0, "Completed":0,"Completed_Qty":0, "Complete_on_time":0, "Complete_on_time_Qty":0, "Overdue_Completed":0, "Overdue_Completed_Qty":0,
                "Uncompleted":0,"Uncompleted_Qty":0, "Active":0, "Active_Qty":0, "Overdue":0, "Overdue_Qty":0, "Unoverdue":0, "Unoverdue_Qty":0,
                "planedate":''}} 
        for project in projects}
        #統計Summary信息
        for task in tasks:
            recordid = task['recordid']
            result[recordid]["tasks"].append(task)
            summary = result[recordid]['summary']
            summary['All_Qty'] += 1
            if task['progress']:
                if task['progress'] in 'CF':
                    summary['Completed_Qty'] += 1
                    if task['edate'] and DateTools.format(task['edate']) <= DateTools.format(task['planedate']):
                        summary['Complete_on_time_Qty'] += 1
                    else:
                        summary['Overdue_Completed_Qty'] += 1
                else:
                    summary["Uncompleted_Qty"] += 1
                    if task['progress'] in 'TI':
                        summary['Active_Qty'] += 1
                    if DateTools.format(task['planedate']) < DateTools.format(DateTools.now()):
                        summary['Overdue_Qty'] += 1
            if task['planedate'] and DateTools.formatf(task['planedate'],'%Y-%m-%d') > summary['planedate']:
                summary['planedate'] = DateTools.formatf(task['planedate'], '%Y-%m-%d')
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
        return result
    
    projects, tasks = search_data()
    return analysis_data(projects, tasks)        