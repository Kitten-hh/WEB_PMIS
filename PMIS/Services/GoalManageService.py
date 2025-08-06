from DataBase_MPMS import models
import logging
from django.db import connections
from django.db.models import Sum,Count,Max,Min,Avg,Q
from BaseApp.library.tools import DateTools
LOGGER = logging.Logger(__name__)
from django.core.cache import cache

class GoalManagementService(object):

    def searchGoalManagement(self, contacts):
        '''
        功能描述：查詢Goal Management
        查詢該聯繫人當前Quarterly Goal中關聯的Project中沒有完成的Must Finish和Must Have的Goal
        '''
        quarterly_str = '{0}-{1}'.format(DateTools.formatf(DateTools.now(),"%Y"), DateTools.getQuarter(DateTools.now()))
        qs = models.Goalmanagement.objects.filter(contact__in=contacts, goaltype='Q', period=quarterly_str)
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
            .filter(~Q(progress='C') & ~Q(progress='F')).extra(where=[whereStr], params=params)
        for task in qs:
            print("{0}-{1}-{2} {3} {4}".format(task.pid, task.tid, task.taskid, task.task, task.contact, task.planedate))
        sub_qs = models.VTaskRecordid.objects.filter(taskcategory='MF', planedate__date__lte=DateTools.now())\
            .filter(~Q(progress='C') & ~Q(progress='F')).extra(
                select={'taskno':"CONVERT(Varchar(10), Pid) + '-' + CONVERT(Varchar(20), CONVERT(Decimal(18, 0), Tid)) + '-' + CONVERT(Varchar(10), CONVERT(Decimal(18, 0), TaskID))"}, 
                where=[whereStr], params=params).values('taskno')
        qs = models.Task.objects.filter(taskcategory='MF',relationgoalid__in=sub_qs)
        for task in qs:
            print("{0}-{1}-{2} {3} {4}".format(task.pid, task.tid, task.taskid, task.task, task.contact, task.planedate))        

    def getTopOutstandingGoal(self, username, top):
        '''
        功能描述：獲取前多少個脫期的Goal
        '''
        quarterly_str = '{0}-{1}'.format(DateTools.formatf(DateTools.now(),"%Y"), DateTools.getQuarter(DateTools.now()))
        project_qs =  models.Goalmanagement.objects.values('recordid').filter(contact=username, period=quarterly_str, goaltype='Q')
        #先查詢前top個脫期的Must Finish
        finish_qs = models.VTaskRecordid.objects.filter(contact=username,recordid__in = project_qs, taskcategory='MF', planedate__date__lte=DateTools.now())\
        .extra(select={'taskno':"CONVERT(Varchar(10), Pid) + '-' + CONVERT(Varchar(20), CONVERT(Decimal(18, 0), Tid)) + '-' + CONVERT(Varchar(10), CONVERT(Decimal(18, 0), TaskID))"})\
        .filter(~Q(progress='C') & ~Q(progress='F'))[:top]

        #一般查詢的數據不多，可以先取出Must Finish的TaskNo再根據TaskNo查询Must Have
        task_nos = [task.taskno for task in finish_qs]
        have_qs = models.VTaskRecordid.objects.filter(contact=username,recordid__in = project_qs, relationgoalid__in=task_nos, taskcategory='MH', planedate__date__lte=DateTools.now())\
        .filter(~Q(progress='C') & ~Q(progress='F'))[:top]

        #合並Must Finish和Must Have以PlanEDate排序取top
        result = list(finish_qs) + list(have_qs)
        result.sort(key=lambda x:(x.planedate))
        return result[:top]
        
        
