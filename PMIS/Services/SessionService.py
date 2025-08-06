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
from BaseApp.library.tools import DateTools
from . import QueryFilterService

class SessionService(BaseService):
    @staticmethod
    def search_sessioni(contact=None, recordid=None, period=None, allcontact=None, stype=None, desc=None):
        '''
        功能描述：查詢用戶SessionI
        '''
        results = []
        filter_str = '1<>1'
        filter_period = ''
        filter_arr = []
        if recordid:
            filter_arr.append("RecordId = '{0}'".format(recordid))
        if contact:
            filter_arr.append("Contact = '{0}'".format(contact))
        if stype:
            filter_arr.append("ISNULL(Type,1) = '{0}'".format(stype))
        if desc:
            filter_arr.append("SDesp like '%%{0}%%".format(desc))
        if len(filter_arr) > 0:
            filter_str = "({0}) and Progress='I'".format(') and ('.join(filter_arr))
        else:
            filter_str = "Progress='I'"            
        if period:
            start_date, end_date = SessionService.get_quarterly_date(period)
            start_str = DateTools.format(start_date)
            end_str = DateTools.format(end_date)
            filter_str = "({0}) and ((PlanBDate >= '{1}' and PlanBDate <= '{2}') or \
                (PlanEDate >= '{3}' and PlanEDate <= '{4}') or \
                (PlanBDate <= '{5}' and PlanEDate >= '{6}'))".format(filter_str, start_str, end_str,start_str, end_str,start_str, end_str)
            filter_period = "((PlanBDate >= '{0}' and PlanBDate <= '{1}') or \
                (PlanEDate >= '{2}' and PlanEDate <= '{3}') or \
                (PlanBDate <= '{4}' and PlanEDate >= '{5}'))".format(start_str, end_str,start_str, end_str,start_str, end_str)
        if allcontact:
            filter_str = "({0}) and {1}".format(filter_str, "',' + ISNULL(AllContact,' ') + ',' like '%%,{0},%%'".format(allcontact))        
        ##filter_str = filter_str.replace("'","''")
        ##filter_period = filter_period.replace("'", "''")
        with connections['MPMS'].cursor() as cursor:
            try:
                cursor.execute('SET NOCOUNT ON {CALL dbo.GetSessionTrees_Test (%s,%s,%s)}', [contact, filter_str, filter_period])
            except Exception as e:
                print(str(e))
            columns = [column[0].lower() for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                obj = dict(zip(columns, row))
                obj['pspriority'] = (0 if not obj['projectpriority'] else obj['projectpriority']) + (0 if not obj['sessionpriority'] else obj['sessionpriority'])
                results.append(obj)        
            results.sort(key=lambda x:x['pspriority'], reverse=True)
        return results

    
    @staticmethod
    def get_session_list(contact=None, pid=None, recordid=None, desc=None):
        '''
        功能描述：查詢用戶Session
        '''
        results = []
        with connections['MPMS'].cursor() as cursor:
            try:
                cursor.execute('SET NOCOUNT ON {CALL dbo.GetSessionList (%s,%s,%s,%s,%s)}', [contact, contact, pid, recordid, desc])
            except Exception as e:
                print(str(e))
            columns = [column[0].lower() for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                obj = dict(zip(columns, row))
                results.append(obj)        
        return results
  
    @staticmethod
    def get_quarterly_date(period):
        arr = period.split("-")
        year = arr[0]
        month = 1 + 3 * (int(arr[1]) - 1)
        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)
        first_date = DateTools.parsef("{0}-{1}".format(year, month), "%Y-%m")
        start_date = DateTools.getBeginOfQuarter(first_date)
        end_date = DateTools.getEndOfQuarter(first_date)
        return start_date, end_date

    @staticmethod
    def search_task_with_session(pid,tid,contact=None,params={}):
        '''
        功能描述：查詢Session的任務列表
        '''
        queryset = models.Tasklist.objects.filter(pid=pid, tid=tid);
        session = queryset[0]
        planbdate = session.planbdate
        planedate = session.planedate
        filter = Q()
        filter.connector = "and"
        if planbdate:
            filter.children.append(("planbdate__gte",planbdate))
        if planedate:
            filter.children.append(("planedate__lte",planedate))
        qs = models.VTask.objects.filter(Q(pid=pid, tid=tid))
        if contact:
            qs = qs.filter(contact=contact)
        if not ('session_filter' in params and params['session_filter'] == False):
            qs = qs.filter(filter | ~Q(progress__in=['C','F']))
        if 'progress_or' in params and params['progress_or']:
            progress_or = params['progress_or']
            progress_filter = Q()
            progress_filter.connector = "or"
            arr = progress_or.split(",")
            for item in arr:
                progress_filter.children.append(("progress", item))
            qs = qs.filter(progress_filter)
        if 'taskcategory_or' in params and params['taskcategory_or']:
            taskcategory_or = params['taskcategory_or']
            taskcategory_filter = Q()
            taskcategory_filter.connector = "or"
            arr = taskcategory_or.split(",")       
            for item in arr:
                taskcategory_filter.children.append(("taskcategory", item))
            qs = qs.filter(taskcategory_filter)
        if 'class_one' in params and params['class_one']:
            qs = qs.filter(class_field=1)
        if 'progress_nf' in params and params['progress_nf']:
            qs = qs.filter(~Q(progress='F'))
        if 'progress_ncf' in params and params['progress_ncf']:
                qs = qs.filter(~Q(progress__in=['C','F']))
        qs = qs.order_by("-schpriority")            
        return list(qs)       

    @staticmethod
    def get_max_tid(pid, min_tid, max_tid, type):
        def get_max_tid_with_step(qs, step=10):
            if len(qs) > 0:
                tid_array = [tasklist['tid'] for tasklist in qs]
                for i in range(math.floor((min_tid+step)/step) * step, max_tid-1, step):
                    if not i in tid_array:
                        return i;
                return None
            else:
                return min_tid + step

        range_num = max_tid - min_tid
        if type == '1': ##use requement
            if range_num > 1100:
                max_tid = min_tid + 1000
            else:
                max_tid = min_tid + 100
        qs = models.Tasklist.objects.values('tid').filter(pid=pid, tid__gt=min_tid, tid__lt=max_tid).order_by('tid')
        result = get_max_tid_with_step(qs, 10)
        if not result:
            result = get_max_tid_with_step(qs, 1)
        return result

    @staticmethod
    def get_session_range(recordid:str):
        '''
        功能描述:根據RecordId獲取Session的範圍
        '''
        qs = models.Subproject.objects.filter(recordid=recordid)
        if len(qs) > 0:
            filter = qs[0].filter
            pid = qs[0].projectid
            regex_str = r"tid\s*>={0,1}\s*'{0,1}([0-9]+)'{0,1}\s*and\s*tid\s*<={0,1}\s*'{0,1}([0-9]+)'{0,1}"
            matched = re.search(regex_str, filter, re.IGNORECASE)
            if not bool(matched):
                return None,None,None
            if int(matched.group(1)) < int(matched.group(2)):
                min_tid = int(matched.group(1))
                max_tid = int(matched.group(2))
            else:
                max_tid = int(matched.group(1))
                min_tid = int(matched.group(2))
            return pid,min_tid,max_tid
