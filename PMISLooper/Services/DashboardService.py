from DataBase_MPMS import models
from PMIS.Services.BaseService import BaseService
from PMIS.Services.UserService import UserService
from PMIS.Services import QueryFilterService
from PMIS.Services.TemplateService import TemplateService
from BaseApp.library.tools import AsyncioTools
from django.db.models import Count,Q,Case,Sum,When,IntegerField,Max
from django.db.models import F, ExpressionWrapper, fields
import json
import aiohttp
import asyncio
import random
import math
import datetime
import timeago
from BaseApp.library.tools import DateTools
import re
from django.db import connections,transaction
from PMIS import Public as Pub
from django.conf import settings
from django.db import connections
import logging
import dateutil

LOGGING = logging.Logger(__name__)

SYS_DASHBOARD_TYPE = settings.SYS_DASHBOARD_TYPE
SYS_DASHBOARD_STAFF_PAST_QUERY_ID = settings.SYS_DASHBOARD_STAFF_PAST_QUERY_ID

class DashboardService(BaseService):

    def __init__(self, *args, **kwargs):
        self.tempService = TemplateService()


    def __get_staff_past_query_filter(self):
        try:
            qs = models.Syspara.objects.values('fvalue').filter(ftype=SYS_DASHBOARD_TYPE, nfield=SYS_DASHBOARD_STAFF_PAST_QUERY_ID)
            query_id = qs[0]['fvalue']
            filter = QueryFilterService.get_query_filter(query_id)
            return filter
        except Exception as e:
            LOGGING.error(str(e))
        return None

    def __get_staff_past_actual_filter(self,filter, users):
        users_filter = "contact in ('{0}')".format("','".join(users))
        return re.sub(r"contact\s*[^']*'[^']+'", users_filter, filter, flags=re.I)


    def __get_date_from_filter(self,filter:str):
        bdate = None
        edate = None
        regex_bdate = r"((PLANBDATE)|(PLANEDATE)|(BDATE)|(EDATE))+\s*([>]={0,1})\s*'([^']+)'"
        regex_edate = r"((PLANBDATE)|(PLANEDATE)|(BDATE)|(EDATE))+\s*([<]={0,1})\s*'([^']+)'"
        matched = re.search(regex_bdate, filter, re.IGNORECASE)
        if matched:
            bdate = matched.group(7)
            bdate = dateutil.parser.parse(bdate)
        matched = re.search(regex_edate, filter, re.IGNORECASE)
        if matched:
            edate = matched.group(7)
            edate = dateutil.parser.parse(edate)
        return bdate, edate

    def __handle_date_with_fiter(self, filter:str, bdate, edate):
        regex_bdate = r"((PLANBDATE)|(PLANEDATE)|(BDATE)|(EDATE))+\s*([>]={0,1})\s*'([^']+)'"
        regex_edate = r"((PLANBDATE)|(PLANEDATE)|(BDATE)|(EDATE))+\s*([<]={0,1})\s*'([^']+)'"
        matched = re.search(regex_bdate, filter, re.IGNORECASE)
        if matched:
            filter = re.sub(regex_bdate, matched.group(1) + matched.group(6) + "'"+DateTools.format(dateutil.parser.parse(bdate)) + "'", filter, flags=re.I)
        matched = re.search(regex_edate, filter, re.IGNORECASE)
        if matched:
            filter = re.sub(regex_edate, matched.group(1) + matched.group(6) + "'"+DateTools.format(dateutil.parser.parse(edate)) + "'", filter, flags=re.I)            
        return filter
    
    def get_staff_arragemnt_ratio(self, url, username=None, bdate=None, edate=None):
        filter = self.__get_staff_past_query_filter()
        if bdate and edate:
            filter = self.__handle_date_with_fiter(filter, bdate, edate);
        users = [username]
        if not username:
            users = UserService.GetPartUserNames()
        result = {user.lower().strip():{'contact':user.lower(), 'assign':0, 'complete':0, 'actualuncomplete':0, 'unassigncomplete':0, \
            'ratio':0, 'totalcomplete':0, 'actual_tasks':[]} for user in users}

        task_filter = self.__get_staff_past_actual_filter(filter, users)
        qs = models.VTask.objects.raw('select INC_ID, taskno, contact from V_Task where ' + task_filter)
        for task in qs:
            result[task.contact.lower().strip()]['actual_tasks'].append(task.taskno)

        bdate, edate = self.__get_date_from_filter(filter)
        http_methods = {user:{'url':url, 'params':{'user':user, 'bdate':DateTools.format(bdate), 
            'edate':DateTools.format(edate)}} for user in result.keys()}
        all_plan_tasks = self.__async_fetch_http_json(http_methods)
        for user in result.keys():
            plan_tasks = all_plan_tasks[user];
            plan_tasks = set(['{0}-{1}-{2}'.format(task['pid'], int(task['tid']), int(task['taskid'])) for task in plan_tasks])
            actual_tasks = result[user.lower()]['actual_tasks']
            result[user]['assign'] = len(plan_tasks)
            result[user]['complete'] = len([taskno for taskno in actual_tasks if taskno in plan_tasks])
            result[user]['unassigncomplete'] = len([taskno for taskno in actual_tasks if taskno not in plan_tasks])
            result[user]['actualuncomplete'] = result[user]['assign'] - result[user]['complete']
            if result[user]['assign'] != 0 and result[user]['complete'] != 0:
                result[user]['ratio'] = round(result[user]['complete']/result[user]['assign'] * 100, 2)
            result[user]['totalcomplete']  = result[user]['complete'] + result[user]['unassigncomplete']
            del result[user]['actual_tasks']
        return result        

    def get_staff_arragemnt_ratio_with_plandate(self, username=None, bdate=None, edate=None):
        """
        功能描述：以任務計畫日期為Assign任務，分析Completion Rate
        """
        str_sql = '''SELECT 1 INC_ID,ISNULL(SUM(CASE WHEN (Cast(PlanEDate as Date) >= %s and Cast(PlanEDate as Date) <= %s) THEN 1 ELSE 0 end),0) assign,
                ISNULL(SUM(CASE WHEN (Cast(PlanEDate as Date) >= %s and Cast(PlanEDate as Date) <= %s) AND Progress IN ('C','F') THEN 1 ELSE 0 END),0) completed,
				ISNULL(SUM(CASE WHEN Progress IN ('C','F') THEN 1 ELSE 0 END),0) allcompleted
                FROM V_Task WHERE Contact = %s AND  ((Cast(PlanEDate as Date) >= %s and Cast(PlanEDate as Date) <= %s) OR 
                (Cast(EDate as Date) >= %s AND Cast(EDate as Date) <= %s AND Progress IN ('C','F'))) {0}'''

        rs = models.Syspara.objects.filter(ftype='Query', nfield='TaskQuery')
        attach_filter = "" if not len(rs) > 0 else "and (" + rs[0].fvalue.replace('%', '%%') + ")";        
        str_sql = str_sql.format(attach_filter)
        start_date = DateTools.format(dateutil.parser.parse(bdate))
        end_date = DateTools.format(dateutil.parser.parse(edate))
        params = []
        for i in range(2):
            params.append(start_date)
            params.append(end_date)
        params.append(username)
        for i in range(2):
            params.append(start_date)
            params.append(end_date)
        rs = models.VTask.objects.raw(str_sql, params)
        data =  {username:{'contact':username, 'assign':0, 'complete':0, 'actualuncomplete':0, 'unassigncomplete':0, \
            'ratio':0, 'totalcomplete':0}}        
        data[username]['assign'] = rs[0].assign
        data[username]['complete'] = rs[0].completed
        data[username]['actualuncomplete'] = rs[0].assign - rs[0].completed
        data[username]['unassigncomplete'] = rs[0].allcompleted - rs[0].completed
        data[username]['totalcomplete'] = rs[0].allcompleted
        if data[username]['assign'] != 0 and data[username]['complete'] != 0:
                data[username]['ratio'] = round(data[username]['complete']/data[username]['assign'] * 100, 2)        
        return data
        

    def __async_fetch_http_json(self,http_methods):
        '''
        功能描述:異步獲取數據
        '''
        async def fetch(method):
            url = method.get('url')
            method_type = method.get('method')
            if not method_type:
                method_type = 'GET'
            method_type = method_type.upper()
            params = method.get('params')
            if not params:
                params = {}
            basic_auth_user = method.get('basic_auth_user')
            basic_auth_password = method.get('basic_auth_password')
            headers={'Content-Type': 'application/json'}
            auth = None
            if basic_auth_user and basic_auth_password:
                auth = aiohttp.BasicAuth(basic_auth_user, basic_auth_password)
            async with aiohttp.ClientSession(headers=headers, auth=auth) as client:
                if method_type == 'POST':
                    async with client.post(url,data=json.dumps(params)) as resp:
                        assert resp.status == 200
                        return await resp.json()
                else:
                    async with client.get(url,params=params) as resp:
                        assert resp.status == 200
                        return await resp.json()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop) 
        tasks = []
        keys = []
        if type(http_methods) == dict:
            for key,method in http_methods.items():
                task = asyncio.ensure_future(fetch(method))
                keys.append(key)
                tasks.append(task)
        elif type(http_methods) == list:
            for method in http_methods:
                task = asyncio.ensure_future(fetch(method))
                tasks.append(task)
        result = loop.run_until_complete(asyncio.gather(*tasks))        
        if len(keys) > 0:
            result = {keys[idx]:value for idx,value in enumerate(result)}
        return result
        
    def get_plann_arragement_task(self, contact, bdate:datetime.date, edate:datetime.date):
        '''
        '''
        results = []
        with transaction.atomic(using='MPMS'):
            with connections['MPMS'].cursor() as cursor:
                sql_str = "exec GetTaskPlanner %s, %s, %s"
                cursor.execute('SET NOCOUNT ON {CALL dbo.GetTaskPlanner (%s,%s,%s)}', [contact, DateTools.format(bdate), DateTools.format(edate)])
                columns = [column[0].lower() for column in cursor.description]
                results = []
                for row in cursor.fetchall():
                    obj = dict(zip(columns, row))
                    results.append(obj)           
            return results

    def getSessionOfDate(self, url):
        """
        功能描述：獲取陳生當天跟進人，每人前三個Session
        """
        
        followUpUsers = self.tempService.getTodayFollowupUser()
        if followUpUsers:
            rs = models.Syspara.objects.filter(nfield='Dashboard_ShowActiveSessionNum', ftype='WEBPMIS')
            firstNum = 3
            if len(rs) > 0:
                firstNum = int(rs[0].fvalue)
            http_methods = {user:{'url':url, 'params':{'allcontact':user, 'period':Pub.getCurPeriod()}} for user in followUpUsers}        
            response = AsyncioTools.async_fetch_http_json(http_methods)
            session_map = {}
            for user in followUpUsers:
                for session in response[user]['data'][:firstNum]:
                    sessionid = session['sessionid']
                    if sessionid in session_map:
                        session_map[sessionid]['owner'] = "{0},{1}".format(session_map[sessionid]['owner'], user)
                    else:
                        session['owner'] = user
                        session_map[sessionid] = session
            return list(session_map.values())
        else:
            return []