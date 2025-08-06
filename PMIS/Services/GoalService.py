from DataBase_MPMS import models
from . BaseService import BaseService
from django.db.models import Count,Q,Case,Sum,When,IntegerField,Max
from django.db.models import F, ExpressionWrapper, fields
import json
import random
import math
import datetime
import timeago
from BaseProject.tools import DateTools
import re
from django.db import connections
from BaseApp.library.tools import DateTools,ModelTools
from . import QueryFilterService

class GoalService(BaseService):

    @staticmethod
    def get_goal_treelist(appraisal_pk):
        master = models.Goalmaster.objects.get(pk=appraisal_pk)
        results = []
        with connections['MPMS'].cursor() as cursor:
            goal_filter = "contact = '{}' and period = '{}' and recordId = '{}' and itemno = '{}'".format(master.contact, master.period,
                master.recordid, master.itemno)
            param = ['TaskNo','RelationGoalId', 1, 0, '', '', goal_filter]
            cursor.execute('SET NOCOUNT ON {CALL dbo.LoadTreeList (%s,%s,%s,%s,%s,%s,%s)}', param)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                obj = dict(zip(columns, row))
                reGoalId = obj.get('RelationGoalId')
                if reGoalId:
                    obj['RelationGoalId'] = reGoalId.strip()
                results.append(obj)
        return results;

    @staticmethod
    def get_overall_monthly_goal(contact, period): 
        '''
        功能描述：根據月份獲取聯繫人所有Monthly Goal
        參數說明:
            1) content 聯繫人
            2) period 季度 格式:2021-1
        '''
        goals = models.VGoalmanagementM.objects.values('inc_id','taskno','task','relationid','schpriority','planbdate','planedate').filter(contact=contact, period=period, class_field=1).order_by("-schpriority")
        tasklist_nos = []
        for goal in goals:
            relationid = goal['relationid']
            if relationid:
                tasklist_nos.extend(goal['relationid'].split(";"))
        qs = models.VTasklist.objects.values('sessionid','sdesp').filter(sessionid__in=tasklist_nos)
        tasklist_map = {m['sessionid']:m for m in qs}
        for goal in goals:
            relationid = goal['relationid']
            if relationid:
                tasklist_sub = [value for key,value in tasklist_map.items() if key in relationid.split(";")]
                if tasklist_sub:
                    session_desc = ""
                    for item in tasklist_sub:
                        session_desc += "{0} {1} ".format(item['sessionid'], item['sdesp']);
                    goal['session_desc'] = session_desc
        return goals

    @staticmethod
    def get_overall_monthly_goal_bak(contact, period, is_major=False): 
        '''
        功能描述：根據月份獲取聯繫人所有Monthly Goal
        參數說明:
            1) content 聯繫人
            2) period 季度 格式:2021-1
            3) is_major 是否重要project
        '''
        master = models.VGoalmaster.objects.values('inc_id').filter(contact=contact, period=period).order_by("-score")[:5]
        
        where_str = "GoalMaster.INC_ID in {0} and \
            GoalMaster.period = V_GoalDetail.period and \
            GoalMaster.contact = V_GoalDetail.contact and GoalMaster.recordid = V_GoalDetail.recordid and \
            GoalMaster.gtype = V_GoalDetail.gtype and GoalMaster.itemno = V_GoalDetail.itemno"
        where_str = where_str.format("('" + "','".join([str(m['inc_id']) for m in master]) + "')")
        qs = models.VGoaldetail.objects.values('taskno').extra(tables=['GoalMaster'], where=[where_str])
        monthly_qs = models.VTask.objects.filter(relationgoalid__in=[m['taskno'] for m in qs])
        return list(monthly_qs)

    @staticmethod
    def get_overall_weekly_goal_bak(contact, period, is_magor=False):
        '''
        功能描述：根據月份獲取聯繫人所有Weekly Goal
        參數說明:
            1) content 聯繫人
            2) period 月份 格式:2021-1
            3) is_major 是否重要project
        '''
        monthlys = GoalService.get_overall_monthly_goal_bak(contact, period, is_magor)
        weekly_qs = models.VTask.objects.filter(relationgoalid__in=[m.taskno for m in monthlys])
        return list(weekly_qs)
        
    def get_overall_weekly_goal(contact, period):
        '''
        功能描述：根據月份獲取聯繫人所有Weekly Goal
        參數說明:
            1) content 聯繫人
            2) period 月份 格式:2021-1
        '''
        goals = models.VGoalmanagementW.objects.values('inc_id','taskno','task','relationid','schpriority','planbdate','planedate').filter(contact=contact, period=period, class_field=1).order_by("-schpriority")
        return list(goals)

    @staticmethod
    def get_goal_management(contact, period):
        '''
        功能描述：根據季度獲取管理人員給聯繫人寫的季度goal,所有月度goal
        '''
        rs = models.Goalmanagement.objects.filter(period=period, contact=contact)
        return list(rs);

    def set_important_goal_with_goalmaster(goal_master_pk, goal_type):
        '''
        功能描述：根據goal master獲取
        '''
    @staticmethod
    def search_goal_progress(filter_str, progress):
        data = []
        tasks = []
        with connections[ModelTools.get_database(models.Goalmanagement)].cursor() as cursor:
            cursor.execute('SET NOCOUNT ON {CALL SearchGoalManagementProgress (%s,%s)}', [filter_str, progress])
            local_fields = {a.column:a.attname for a in models.Goalmanagement._meta.get_fields()}
            columns = [(lambda m:local_fields[m] if m in local_fields.keys() else m)(column[0]) for column in cursor.description]
            for row in cursor.fetchall():
                obj = dict(zip(columns,row))
                data.append(obj)
            ##讀取Tasks內容
            cursor.nextset()
            columns = [column[0].lower() for column in cursor.description]
            for row in cursor.fetchall():
                obj = dict(zip(columns,row))
                tasks.append(obj)
        return data,tasks

    @staticmethod
    def search_goal_progress_single(filter_str, progress):
        data = []
        tasks = []
        with connections[ModelTools.get_database(models.VGoalmanagementdetail)].cursor() as cursor:
            cursor.execute('SET NOCOUNT ON {CALL SearchGoalManagementProgress_single (%s,%s)}', [filter_str, progress])
            local_fields = {a.column:a.attname for a in models.VGoalmanagementdetail._meta.get_fields()}
            columns = [(lambda m:local_fields[m] if m in local_fields.keys() else m)(column[0]) for column in cursor.description]
            for row in cursor.fetchall():
                obj = dict(zip(columns,row))
                data.append(obj)
            '''
            ##讀取Tasks內容
            cursor.nextset()
            columns = [column[0].lower() for column in cursor.description]
            for row in cursor.fetchall():
                obj = dict(zip(columns,row))
                tasks.append(obj)
            '''
        return data,tasks
