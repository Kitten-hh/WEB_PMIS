import sys
from enum import Enum
import os
import django

from django.db.models import Sum,Count,Max,Min,Avg,Q
import unittest
import hashlib
import pip, os, time
import json

# 這兩行很重要，用來尋找專案根目錄，os.path.dirname要寫多少個根據要運行的python檔到根目錄的層數決定
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WEB_PMIS.settings')
django.setup()


from DataBase_MPMS import models
from DataBase_PMSDSCSYS import models as sys_models
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.test import TestCase
import datetime
from PMIS.Services.UserService import UserService
from ScheduleApp.Services.PromptSqlService import PromptSqlService,PromptSqlName
from ScheduleApp.Services.TaskForAIService import TaskForAIService
from ScheduleApp.models import Promtsql
from PMIS.Services.ActiveTaskService import ActiveTaskService
from PMIS.Services.TaskService import TaskService
from PMIS.Services import QueryFilterService
from PMIS.Services.SessionService import SessionService
from PMIS.Services.GoalService import GoalService
from PMISLooper.Services.DashboardService import DashboardService
from PMISLooper.Services.TaskDashboardService import TaskDashboardService
import re
from DevPlat.Services.ForumService import ForumService
from PMIS.Services.FrameService import FrameService
from BaseApp.library.tools import DateTools
from BaseApp.library.tools import SWTools
from BaseApp.library.tools import AsyncioTools, ModelTools
from PMISLooper.Services.NotificationService import NotificationService
from PMIS.Services.GoalManageService import GoalManagementService
from django.forms.models import model_to_dict
import pyodbc
from PMIS.Services.ElasticService import ElasticService
from DataBase_MPMS.models import Tecma,Tecmb
from django.db import transaction
from django.db import models as djmodels
from PMIS.Services.MindmapService import MindmapService
from ScheduleApp.Services.ScheduleServer import ScheduleServer
import requests
from requests.auth import HTTPBasicAuth
from PMISLooper.Services.NtfyNotificationServer import NtfyNotificationService
from PMISLooper.Services.NtfyNotificationServer import NtfyNotificationService,NOTIFICATION_DELAY_RESEND_TASK,NOTIFICATION_KNOW_FIELD_NAME
from ChatwithAi_app.Services.ChatTopicsServices import ChatTopicsServices
from ChatwithAi_app.Services.ProjectManagementService import ProjectManagementService
from ChatwithAi_app.Services.AiManagementService import AiManagementService
from django.conf import settings
import redis
import json
import pickle
from Authorization_app.permissions.decorators_pmis import get_users_with_permission,has_permission_message
from DataBase_MPMS.models import Users
from ChatwithAi_app.Services.AiSentencesService import AiSentencesService
from ChatwithAi_app.models import MainQuestions, SubQuestions,AiSentences,AiPageurls
from DataBase_MPMS.models import Mindmap
from ChatwithAi_app.Services.ConversationServices import ConversationService
from ChatwithAi_app.models import TopicCategories

'''from django.db import models
from django.db import connections
import DataBase_MPMS.forms_base as fb
from BaseProject.tools.QueryBuilderUtils import QueryBuildUtils
from BaseProject.tools import utils
from PMIS.Services.ScheduleService import QuarterlyScheduleLogic,FixedDateScheduleLogic
import datetime'''

'''class TestSchedule(unittest.TestCase):
    def test_Schedule(self):
        print(datetime.datetime.now())
        schedule = QuarterlyScheduleLogic('2020-3',('hb',))
        schedule.big_schedule()
        print(datetime.datetime.now())
        ##in_session_logic.calculate_task_type_priority()
    def test_fixed_date_schedule(self):
        print(datetime.datetime.now())
        schedule = FixedDateScheduleLogic('2020-3',('hb',))
        print(datetime.datetime.now())'''
class TestTodayTask(TestCase):
    def test_get_today_normal_task(self):
        service = ActiveTaskService()
        tasks = service.get_today_normal_task('hb')
        print(tasks)
class TestTask(TestCase):
    databases = ['MPMS']
    def test_add_quick_task(self):
        r = self.client.post("/PMIS/task/add_task", data={
            'pid':'888',
            'tid':100,
            'taskid':136003,
            'task':'hb test add task',
            'contact':'hb'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, 200) # this is OK.
        print(r.content)
class TestSession(TestCase):
    databases = ['MPMS']
    def test_search_sessioni(self):
        data = SessionService.search_sessioni(contact='sing', period='2020-4')
        print(len(data))
        print(data)
class TestGoal(TestCase):
    databases = ['MPMS']
    def test_get_overall_monthly_goal(self):
        try:
            ##data = GoalService.get_overall_monthly_goal('hb','2021-1')
            data = GoalService.get_overall_weekly_goal('hb','2021-1')
            print(data)
        except Exception as e:
            print(str(e))

class TestMatch(TestCase):
    def test_test(self):
        content = "dict_keys(['datatable', 'draw', 'columns[0][data]', 'columns[0][name]', 'columns[0][searchable]', 'columns[0][orderable]', 'columns[0][search][value]', 'columns[0][search][regex]', 'columns[1][data]', 'columns[1][name]', 'columns[1][searchable]', 'columns[1][orderable]', 'columns[1][search][value]', 'columns[1][search][regex]', 'columns[2][data]', 'columns[2][name]', 'columns[2][searchable]', 'columns[2][orderable]', 'columns[2][search][value]', 'columns[2][search][regex]', 'columns[3][data]', 'columns[3][name]', 'columns[3][searchable]', 'columns[3][orderable]', 'columns[3][search][value]', 'columns[3][search][regex]', 'columns[4][data]', 'columns[4][name]', 'columns[4][searchable]', 'columns[4][orderable]', 'columns[4][search][value]', 'columns[4][search][regex]', 'columns[5][data]', 'columns[5][name]', 'columns[5][searchable]', 'columns[5][orderable]', 'columns[5][search][value]', 'columns[5][search][regex]', 'columns[6][data]', 'columns[6][name]', 'columns[6][searchable]', 'columns[6][orderable]', 'columns[6][search][value]', 'columns[6][search][regex]', 'columns[7][data]', 'columns[7][name]', 'columns[7][searchable]', 'columns[7][orderable]', 'columns[7][search][value]', 'columns[7][search][regex]', 'columns[8][data]', 'columns[8][name]', 'columns[8][searchable]', 'columns[8][orderable]', 'columns[8][search][value]', 'columns[8][search][regex]', 'columns[9][data]', 'columns[9][name]', 'columns[9][searchable]', 'columns[9][orderable]', 'columns[9][search][value]', 'columns[9][search][regex]', 'columns[10][data]', 'columns[10][name]', 'columns[10][searchable]', 'columns[10][orderable]', 'columns[10][search][value]', 'columns[10][search][regex]', 'columns[11][data]', 'columns[11][name]', 'columns[11][searchable]', 'columns[11][orderable]', 'columns[11][search][value]', 'columns[11][search][regex]', 'columns[12][data]', 'columns[12][name]', 'columns[12][searchable]', 'columns[12][orderable]', 'columns[12][search][value]', 'columns[12][search][regex]', 'order[0][column]', 'order[0][dir]', 'start', 'length', 'search[value]', 'search[regex]', '_', 'order[1][column]', 'order[1][dir]'])"
        match = re.search(r'order\[(\d+)\]\[column\]', content)
        if match:
            print(match.group(1))
            print(match.group())

class TestDashboard(TestCase):
    databases = ['MPMS']    
    def test_test(self):
        ##service = DashboardService()
        ##result = service.get_staff_arragemnt_ratio()
        ##print(result)
        ##for r in result.values():
          ##  print(r)
        ##service = TaskService()
        #service.analysis_dashboard(None,DateTools.parse('20211018'), DateTools.parse('20211024'))
        ##service.analysis_solutiontype("hb",DateTools.parse('20211208'), DateTools.parse('20211215'))
        ##qs = service.analysis_new_task("hb",'20211208', '20211226')
        print(" abasdasdf ".center(4, "_"))
    def test_sessonOfDate(self):
        service = DashboardService()
        AsyncioTools.get_url()
        service.getSessionOfDate(url)
    def test_amf(self):
        service = TaskDashboardService()
        response = service.getInitSyspara("sing")
        print(response)

class TestForumService(TestCase):
    databases = ['MPMS']    
    def test_test(self):
        qs = models.Goalmanagement.objects.filter(goaltype='W', sessions__isnull=False)
        for item in qs:
            tasks = []
            sessions = item.sessions
            if not sessions:
                sessions = '{}'
            sessions = json.loads(sessions);
            for sessionid, taskids in sessions.items():
                task_list = ["{0}-{1}".format(sessionid, taskid) for taskid in taskids.split(",")]
                tasks.extend(task_list)
            item.relationtasks = ",".join(tasks)
            item.save()
        print(len(qs))

class TestExportToExcel(TestCase):
    databases = ['MPMS']
    def test_export_to_excel(self):
        ##qs = models.VTecmb.objects.all()
        result = AsyncioTools.async_fetch_http_json({'data':{'url':'http://222.118.20.236:8009/PMIS/TechnicalDatatable', 
            'params':{'draw':0,'length':-1,'start':0}, 'headers':{'x-requested-with': 'XMLHttpRequest'}}});
        '''
        status,excel = SWTools.exportToExcel(result['data'], [
            {'field':'pid','label':'工程編號','width':10},
            {'field':'tid', 'label':'類別編號','width':10},
            {'field':'taskid','label':'任務編號','width':12},
            {'field':'task','label':'任務描述','width':50},
            {'field':'planbdate','label':'計畫開始','width':12},
            {'field':'planedate','label':'計畫結束','width':12},
            {'field':'contact','label':'聯繫人','width':10},
            {'field':'bdate','label':'實際開始','width':12},
            {'field':'edate','label':'實際結束','width':12}])
        '''
        status,excel = SWTools.exportToExcel(result['data'])
        if status == 0:
            with open('test.xlsx','wb') as f:
                f.write(excel)
        elif status == 1:
          print("沒有數據不導出Excel")  
class TestSystem(TestCase):
    databases = ['PMSDSCSYS']
    def test_system(self):
        def check_root_func(data):
            if data[parent_field]:
                return False
            else:
                return True
        def convert_func(data):
            return {'icon': "",'name': data['sysremark'],'children': [],'sysid':data['sysid']}
        qs = sys_models.System.objects.all().values()
        id_field = 'sysid'
        parent_field = 'parentid'
        children_property_name = 'children'
        tree = SWTools.convert_list_tree(qs, id_field, parent_field, check_root_func, convert_func)
        print(tree)

class TestGoalMangaement(TestCase):
    databases = ['MPMS']
    def test_goal_management(self):
        qs = models.Goalmanagement.objects.filter(goalid=3720)
        self.save_split_week_goal(qs[0])
        
    def save_split_week_goal(self,weekly_doal):
        if weekly_doal.goaltype != 'W':
            return
        goaldesc = weekly_doal.goaldesc
        sessions = weekly_doal.sessions
        if not goaldesc:
            models.Goalmanagementdetail.objects.filter(goalid=weekly_doal.goalid).delete()
            return
        goals = goaldesc.replace("\r\n", "\r").replace("\n", "\r").split("\r")
        if not sessions:
            sessions = '{}'
        sessions = json.loads(sessions)
        goal_management_details = []
        for index,goal in enumerate(goals):
            goal_detail = models.Goalmanagementdetail()
            goal_detail.goalid = weekly_doal.goalid
            goal_detail.itemno = (index + 1) * 10
            goal_detail.goaldesc = goal
            match = re.search(r"\(((\w+-\d+,?)+)\)$", goal, re.IGNORECASE)
            relation_tasks = []
            if match:
                relation_sessions = match.group(1).split(",")
                for sessionid in relation_sessions:
                    if sessionid in sessions and sessions[sessionid]:
                        temp_taskno = ["{0}-{1}".format(sessionid, taskid) for taskid in sessions[sessionid].split(",")]
                        relation_tasks.extend(temp_taskno)
                goal_detail.relationtasks = ",".join(relation_tasks)
            goal_management_details.append(goal_detail)
        models.Goalmanagementdetail.objects.filter(goalid=weekly_doal.goalid).delete()
        models.Goalmanagementdetail.objects.bulk_create(goal_management_details,batch_size=50)
        print(goaldesc)

class TestNotificationService(TestCase):
    databases = ['MPMS']
    def test_send_today_task(self):
        qs = models.Syspara.objects.values("nfield").filter(ftype="NotificationId")
        if len(qs) > 0:
            users = [item['nfield'] for item in qs]            
            service = NotificationService()
            service.send_todayt_tasks(",".join(users))
            service.send_first_last_class1("sing", "sing")
            for i in range(100):
                service.schedule_send_message()
    def test_send_message(self):
        msg = '通知{0}'.format(datetime.datetime.now().strftime('%H:%M:%S'))
        SWTools.pushMessage('hb', {"text":msg, "title":msg, "ctype":"text"})

class TestNewTask(TestCase):
    databases=['MPMS']
    def test_new_task(self):
        count = self.get_new_tasks_count("hb")
        print("新任務數量:{0}".format(count))
    def get_new_tasks(self, usernam):
        qs = self.get_new_tasks_query(username)
        return qs
    def get_new_tasks_count(self, username):
        qs = self.get_new_tasks_query(username)
        return qs.count()
    def get_new_tasks_query(self, username):
        qs = models.Task.objects.filter(contact='hb').filter(~Q(r_flag=1))
        qs = TaskService.getRequestQuerySetWithSysparam(qs)
        qs = qs.extra(where=['not exists (Select * from TECMB where Pid = Task.Pid and Tid = Task.Tid and TaskId=Task.Taskid)'])
        return qs
    def test_get_notification_tasks(self):
        try:
            print("{0}-->============開始收集需要發送消息的任務=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
            qs = models.Syspara.objects.values("nfield").filter(ftype="NotificationId")
            if len(qs) > 0:
                users = [item['nfield'] for item in qs]
                service = NotificationService()
                service.send_todayt_tasks(",".join(users))
                #service.send_first_last_class1("sing", "sing")
            print("{0}-->============開始收集需要發送消息的任務=============".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        except Exception as e:
            print(str(e))

class TestApscheduler(TestCase):
    databases = ['MPMS']
    def test_apscheduler(self):
        scheduler = BackgroundScheduler() # 建一個調度器對象
        for job in scheduler.get_jobs():
            print(job)
class TestGoalManagement(TestCase):
    databases = ['MPMS']
    def test_goalmanagement(self):
        service = GoalManagementService()
        contacts = service.getTodayFollowupUser()
        service.searchGoalManagement(contacts)
    def test_topOutstandingGoal(self):
        service = GoalManagementService()
        tasks = service.getTopOutstandingGoal("hb", 5)
        for task in tasks:
            print("{0}-{1}-{2} {3}".format(task.pid, task.tid, task.taskid, task.task))

class TestOverallGoal(TestCase):
    databases = ['MPMS']
    def test_Goal(self):
        a = ['a','b','c']
        for a,index in enumerate(a):
            print(a)
            print(index)
    def test_bonus(self):          
        qs = models.LSTasktypelist.objects.all()
        parents = {item.tasktype:model_to_dict(item) for item in qs if not item.parenttype}
        detail = [model_to_dict(item) for item in qs if item.parenttype]
        result = []
        for tasktype in detail:
            if tasktype['parenttype'] in parents.keys():
                parent = parents[tasktype['parenttype']]
                description = "{0}-->{1}".format(parent['description'], tasktype['description'])
                tasktype_str = "{0}-{1}-".format(parent['tasktype'], tasktype['displaytype'])
                result.append({'tasktype':tasktype_str+"1", "description":description, "score":tasktype['difficulties1']})
                result.append({'tasktype':tasktype_str+"2", "description":description, "score":tasktype['difficulties2']})
                result.append({'tasktype':tasktype_str+"3", "description":description, "score":tasktype['difficulties3']})
        print(result)
class TestPyodbc(TestCase):
    def test_pool(self):
        #conn_str = 'DRIVER={0};SERVER={1};PORT=1433;DATABASE={2};UID={3};PWD={4};TDS_Version={5};'.format('FreeTDS','192.168.2.253','pubs','dbname','access','7.1')
        conn_str = 'DRIVER={0};SERVER={1};PORT=1433;DATABASE={2};UID={3};PWD={4};'.format('ODBC Driver 17 for SQL Server','192.168.2.83','PMIS','dbname','access')
        
        ##創建數據庫連接對象
        conn = pyodbc.connect(connstr, ansi=True)
        with conn.cursor() as cursor:
            sql = "select top 10 Task from Task"
            for row in cursor.execute(sql):
                print(row)
        conn.close()

        conn = pyodbc.connect(connstr, ansi=True)
        with conn.cursor() as cursor:
            sql = "select top 10 Pid,Tid,TaskId from Task"
            for row in cursor.execute(sql):
                print(row)
        conn.close()        

class TestElasticService(TestCase):
    def test_fullTextSearchDoc(self):
        service = ElasticService()
        service.fullTextSearchDoc("批量 事務")

class TestCategory(TestCase):
    databases = ['MPMS']
    def set_max_seqno(self, instance):
        '''
        功能描述：獲取最大單號
        參數說明:
            instance:需要保存或初始化的model實例
        '''
        todaydate = datetime.datetime.now().strftime("%Y%m%d")
        rs = Tecma.objects.filter(ma001__startswith = todaydate).aggregate(Max('ma001'))
        if rs and rs['ma001__max']:
            max_seq_no = str(int(rs['ma001__max']) + 1)
        else:
            max_seq_no = todaydate+'001'
        instance.ma001 = max_seq_no

    def set_basic_field_info(self,instance):
        model = Tecma
        username = 'hb'
        basic_fields = [f for f in model._meta.get_fields() if f.column and f.column.upper() in ['COMPANY','USR_GROUP','CREATOR','CREATE_DATE','MODIFIER','MODI_DATE','T_STAMP', 'REVISEDBY','FLAG']]
        for field in basic_fields:
            name = field.name
            upper_name = field.column.upper()
            if upper_name == 'T_STAMP' and type(field) in [djmodels.DateField,  djmodels.DateTimeField]:
                setattr(instance, name, DateTools.now())
            elif upper_name == 'REVISEDBY':
                setattr(instance, name, username)
            elif upper_name == "COMPANY":
                pass
            elif upper_name == "USR_GROUP":
                setattr(instance, name, username)
            elif upper_name == "CREATOR" and not getattr(instance, name):
                setattr(instance, name, username)            
            elif upper_name == "CREATE_DATE" and not getattr(instance, name) and type(field) in [ djmodels.CharField]:
                setattr(instance, name, DateTools.formatf(DateTools.now(), '%Y%m%d'))
            elif upper_name == "MODIFIER":
                setattr(instance, name, username)            
            elif upper_name == "MODI_DATE":
                setattr(instance, name, DateTools.formatf(DateTools.now(), '%Y%m%d%H%M%S'))
            elif upper_name == "FLAG" and type(field) in [ djmodels.DecimalField,  djmodels.IntegerField,  djmodels.BigIntegerField]:
                old_flag = getattr(instance, name)
                if old_flag:
                    if old_flag >= 999:
                        setattr(instance, name, 1)
                    else:
                        setattr(instance, name, old_flag + 1)
                else:
                    setattr(instance, name, 1)

    def saveCategory(self, category, data):
        categoryTecma = Tecma.objects.filter(ma003 = category).extra(where=["ISNULL(MA002,'') = ''"])
        with transaction.atomic(ModelTools.get_database(Tecma())):
            categoryNo = ''
            if len(categoryTecma) == 0:
                categoryTecma = Tecma()
                self.set_max_seqno(categoryTecma)
                self.set_basic_field_info(categoryTecma)
                categoryTecma.ma003 = category
                categoryTecma.save()
            else:
                categoryTecma = categoryTecma[0]
            categoryNo = categoryTecma.ma001
            for area, subareas in data.items():
                areaTecma = Tecma.objects.filter(ma002=categoryNo, ma003 = area)
                areaNo = ''
                if len(areaTecma) == 0:
                    areaTecma = Tecma()
                    self.set_max_seqno(areaTecma)
                    self.set_basic_field_info(areaTecma)
                    areaTecma.ma002 = categoryNo
                    areaTecma.ma003 = area
                    areaTecma.ma007 = categoryNo
                    areaTecma.save()
                else:
                    areaTecma = areaTecma[0]
                areaNo = areaTecma.ma001
                for subarea in subareas:
                    subAreaTecma = Tecma.objects.filter(ma002=areaNo, ma003 = area)
                    subAreaNo = ''
                    if len(subAreaTecma) == 0:
                        subAreaTecma = Tecma()
                        self.set_max_seqno(subAreaTecma)
                        self.set_basic_field_info(subAreaTecma)
                        subAreaTecma.ma002 = areaNo
                        subAreaTecma.ma003 = subarea
                        subAreaTecma.ma007 = categoryNo
                        subAreaTecma.save()
                
    def test_technical_category(self):
        result = {}
        category = "Vue"
        currentArea = ""
        currentSubArea = ""
        with open("category.txt", 'r') as file:
             for line in file:
                    if line.strip():
                        match1 = re.search(r'^\s*\d+', line)
                        match2 = re.search(r'^\s[*]+', line)
                        match3 = re.search(r'[*]+([^*]+)', line)
                        if match1 or match2 or match3: ##表示是Category
                            currentArea = match3.group(1).replace(":", "")
                            result[currentArea] = []
                        elif line:
                            currentSubArea = re.sub(r'\s*-\s*','', line).strip()
                            currentSubArea = re.sub(r'[.]*\n*$','', currentSubArea)
                            print("{0} - {1}".format(currentArea, currentSubArea))
                            result[currentArea].append(currentSubArea)
        self.saveCategory(category, result)

class TestNewMeeting(TestCase):
    databases = ['MPMS','default']
    def test_add_quick_task(self):
        resp = self.client.post("/en/looper/login", data={'username':"hb",'password':"hb11"},HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        if not resp.json()['status']:
            raise Exception("登錄不成功")
        else:
            for i in range(0, 100):
                resp = self.client.get("/en/looper/metting/newMeeting")
                if resp.status_code != 200:
                    raise Exception('===========訪問不成功=============')
                else:
                    print("================訪問成功============")

class TestGenerateMindmap(TestCase):
    databases = ['MPMS','default']
    def test_generate_mindmap(self):
        service = MindmapService()
        service.generateMindmap("19838", None, None)

class TestPromptSqlService(TestCase):
    databases = ['MPMS']
    def test_getData(self):
        service = PromptSqlService()
        data = service.getData(PromptSqlName.GetURSessionWithName.value, {"RecordId":"00259", "SDesp":"%%WJ MES%%"})
        print(data)
        if len(data) > 0:
            sessionid = data[0]['sessionid']
            data = service.getData(PromptSqlName.UserRequirementForSession.value, {"RID":sessionid})
            print(data)

class TestTaskForAiService(TestCase):
    databases = ['MPMS']
    def test_getData(self):
        service = TaskForAIService()
        data = service.expandPromptData("10","20","30")
        print(data)

class TestScheduleService(TestCase):
    databases = ['MPMS']
    def test_callScenarioScheduleService(self):
        service = ScheduleServer()
        service.callScenarioScheduleService("sing");

class TestSpecialDataTableService(TestCase):
    databases = ['MPMS']
    def test_specialDataTable(self):
        users = ['hb','lmy']
        topic = 'PMIS'
        actionUrl = "http://183.63.205.83:8000/looper/staff_dashboard?username={0}&bdate={1}&edate={2}&dp=3".format('hb', 
        DateTools.formatf(DateTools.getBeginOfWeek(DateTools.now()), '%Y-%m-%d'),
        DateTools.formatf(DateTools.getEndOfWeek(DateTools.now()), '%Y-%m-%d'))        
        message = {"title":"hb's Finish Tasks", 'message':"""Try out the messaging previously given to lsy(使用ntfy測試实现將C的任務發消息給陳生，hb,lmy的功能)
EDate:2024-1-20 14:31 Sch Priority:1980""", 'tags':['white_check_mark'], 
        "actions": []
        }
        SWTools.pushNtfyMessage(users,topic,message)
class TestSendScheduleServer(TestCase):
    databases = ['MPMS']     
    def test_goal(self):
        server = NtfyNotificationService()
        todayTaskDatas = server.get_today_task_data(['hb','sing','lmy','lsy'])
        outstanding_goals = todayTaskDatas['outstanding_goals']
        server.send_outstanding_goals(outstanding_goals)        
    def test_hight_task(self):
        server = NtfyNotificationService()
        users = ['xmm']
        todayTaskDatas = server.get_today_task_data(users)
        highest_tasks = todayTaskDatas['highest_tasks']
        server.send_schedule_higest_task(users, highest_tasks)
    def test_cycle_task(self):
        server = NtfyNotificationService()
        users = ['lsy']
        todayTaskDatas = server.get_today_task_data(users)
        user_fixed_day_tasks = todayTaskDatas['user_fixed_day_tasks']
        server.send_cycle_fixed_tasks(user_fixed_day_tasks)           
    def test_send_assign_task(self):
        server  = NtfyNotificationService()
        qs = models.Task.objects.filter(pid='11580',tid='3738', taskid='207210').values()
        server.send_assign_task('hb', qs[0])

    def test_send_new_task(self):
        server  = NtfyNotificationService()
        qs = models.Task.objects.filter(pid='11580',tid='3738', taskid='207210').values()
        server.send_new_tasks({'hb':qs,'czz':qs})
    def test_send_new_task_with_click_cancel(self):
        server  = NtfyNotificationService()
        qs = models.Task.objects.filter(pid='11580',tid='3738', taskid='207210').values()
        task = qs[0]
        task[NOTIFICATION_KNOW_FIELD_NAME] = True
        server.send_new_tasks({'hb':[task]})

    def test_send_todo_task(self):
        server  = NtfyNotificationService()
        #qs = models.Task.objects.filter(pid='11580',tid='3738', taskid='207210').values()
        ##qs = models.Task.objects.filter(pid='00900',tid='51910', taskid='10').values() #這個任務有附件
        qs = models.Task.objects.filter(pid='01000',tid='1080', taskid='10').values() #這個任務有附件
        server.send_remind_task('hb', qs[0])

    def test_send_finished_task(self):
        server  = NtfyNotificationService()
        #qs = models.Task.objects.filter(pid='11580',tid='3738', taskid='207210').values()
        ##qs = models.Task.objects.filter(pid='00900',tid='51910', taskid='10').values() #這個任務有附件
        qs = models.Task.objects.filter(pid='01000',tid='1080', taskid='10').values() #這個任務有附件
        server.send_finish_task(['hb'], qs[0])
    
    def test_send_remind_task(self):
        server  = NtfyNotificationService()
        #qs = models.Task.objects.filter(pid='11580',tid='3738', taskid='207210').values()
        ##qs = models.Task.objects.filter(pid='00900',tid='51910', taskid='10').values() #這個任務有附件
        qs = models.Task.objects.filter(pid='01000',tid='1080', taskid='10').values() #這個任務有附件
        server.send_remind_task_with_pmstr({'hb':qs})

    def test_send_remind_task_with_click_cancel(self):
        server  = NtfyNotificationService()
        qs = models.Task.objects.filter(pid='11580',tid='3738', taskid='207210').values()
        task = qs[0]
        task[NOTIFICATION_KNOW_FIELD_NAME] = True
        server.send_remind_task_with_pmstr({'hb':[task]})
    
    def test_send_message_summary(self):
        server  = NtfyNotificationService()
        server.send_message_summary()

    def test_send_ai_summary(self):        
        server = NtfyNotificationService()
        server.send_meeting_aisummary()

    def test_send_help_desk_summary(self):        
        server = NtfyNotificationService()
        server.send_help_desk_aisummary()


    def test_getNotificationUserSetting(self):
        server = NtfyNotificationService()
        data = server.getReceiverWithUserSetting(['00510'],['00300-21020'])
        print(data)
    
    def test_send_milestone(self):
        server = NtfyNotificationService()
        server.send_milestone()


    def test_get_message_from_ntfy(self):
        try:
            url = "{0}HB_PMIS".format(settings.NTFY_SERVER)
            basicHttpMethod = {'data':{'method':"GET", 'url':url, 'basic_auth_user':settings.NTFY_USERNAME, 'basic_auth_password':settings.NTFY_PASSWORD}}
            response = AsyncioTools.async_fetch_http_json(basicHttpMethod)
            print(response)
        except Exception as e:
            print("An error occurred:", str(e))        
class TestAi(TestCase):
    databases = ['MPMS']
    def test_get_project_status(self):
        server = ProjectManagementService()
        server.getProjectStatus('00286', ["00300-21500"])
    def test_summary_project_status(self):
        server = ProjectManagementService()
        sessions = "00900-51062,00900-51013,00900-51017,00900-51011,00900-51069".split(",")
        summary = server.summaryProjectStatus("00399",sessions)
        print(summary)

    def test_generate_pdf(self):
        server = ProjectManagementService()
        server.generatePdf(None)
    def test_send_project_status(self):
        server = NtfyNotificationService()
        #qs = models.Syspara.objects.values("fvalue").filter(ftype="ProjectStatus", nfield="Test")
        server.send_project_status()
    def test_send_summary_project_status(self):
        server = NtfyNotificationService()
        #qs = models.Syspara.objects.values("fvalue").filter(ftype="ProjectStatus", nfield="Test")
        server.send_summary_project_status()
    def test_send_ai_summary(self):
        server = AiManagementService()
        server.getAiSummary("Meeting")

class TestChatTopicsServices(TestCase):
    databases = ['MPMS']
    def test_get_topics(self):
        ##server = ChatTopicsServices()
        ##data = server.get_mindmap_data_text("Chat with ai topics",0)
        print("a")

class TestRedisCache(TestCase):
    databases=['MPMS']
    def test_getCache(self):
        # 连接到 Redis 服务器
        r = redis.Redis(host='localhost', port=6379, db=0)

        # 获取特定键的值
        binary_data = r.get('WEBPMIS_:1:PMIS.ViewsFolder.views_opportunity:TechnicalQuestion')
        python_obj = pickle.loads(binary_data)
        for obj in python_obj:
            #if not obj['contact']:
            if not obj['contact'] or DateTools.format(obj['Date']) != DateTools.format(DateTools.now()):
                continue
            print("{0}\t{1}\t{2}".format(obj['contact'], DateTools.formatf(obj['Date'], '%Y-%m-%d %H:%M:%S'), obj['Question']))

        binary_data = r.get('WEBPMIS_:1:PMIS.ViewsFolder.views_opportunity:ViewTechnical')
        

        # 将 JSON 字符串反序列化为 Python 对象
        python_obj = pickle.loads(binary_data)
        for obj in python_obj:
            #if not obj['contact']:
            if not obj['contact'] or DateTools.format(obj['Date']) != DateTools.format(DateTools.now()):
                continue
            qs = Tecmb.objects.filter(mb023=obj['TechnicalId'])[:1]
            technicalName = ""
            if len(qs) > 0:
                technicalName = qs[0].mb004
            print("{0}\t{1}\t{2}\t({3})".format(obj['contact'], DateTools.formatf(obj['Date'], '%Y-%m-%d %H:%M:%S'), obj['TechnicalId'],technicalName))

class TestPermission(TestCase):
    databases=['MPMS']
    def test_permission(self):
        user = Users.objects.filter(username='hb')
        data = has_permission_message(user[0], "Show_Project_Status", 2, "00513", "18000-35")
        print(data)
        data = get_users_with_permission_message("Show_Project_Status", 4, "00513", "18000-35")
        print(data)

def generateAiSentences():
    service = AiSentencesService()
    """
    qs = Promtsql.objects.filter(isapproved=1)
    data = [{"reference_id":row.inc_id, 'sentence':row.sname} for row in qs]
    service.generate_sentences('pre-condition', data, gpt_model="gpt4", append=False, generate_embedding=True)
    """
    #sentences_for_embedding = list(AiSentences.objects.filter(reference_type='page', embedding_vector=None).values('reference_id', 'sentence'))
    sentences_for_embedding = list(AiSentences.objects.filter(reference_type='pre-condition', embedding_vector=None).values('reference_id', 'sentence'))
    service.generate_embeddings("pre-condition", sentences_for_embedding, model="text-embedding-ada-002")    

def generatePreConditionSentences():
    service = AiSentencesService()
    qs = Promtsql.objects.filter(isapproved=1).extra(where=["""(not exists  (Select * from ai_sentences where reference_type = 'pre-condition' and PromtSQL.INC_ID = reference_id) or 
        exists  (Select * from ai_sentences where reference_type = 'pre-condition' and PromtSQL.INC_ID = reference_id and PromtSQL.SName <> sentence and language is null))"""])
    data = [{"reference_id":row.inc_id, 'sentence':row.sname} for row in qs]
    service.generate_sentences('pre-condition', data, gpt_model="gpt4", append=False, generate_embedding=True)    


class TechnicalMindmap(TestCase):
    databases=['MPMS']
    def test_get_django_technical(self):
        qs = Mindmap.objects.filter(inc_id=1168)
        data = json.loads(qs[0].data)   
        pattern = r'[A-Za-z]{1,3}-[A-Za-z]{1,3}-\d{5}'
        for node in data['nodeDataArray']:
            text = node['text']
            # 提取匹配的內容
            matches = re.findall(pattern, text)
            if matches:
                doc_id = matches[0]
                doc_topic = text.replace(doc_id, "").replace("Doc:","").replace("\r\n","")
                doc_topic = re.sub(r"doc:", "", doc_topic, flags=re.IGNORECASE)
                print(f"{doc_id}: {doc_topic}")


    def test_get_react_technical(self):
        qs = Mindmap.objects.filter(inc_id=2435)
        data = json.loads(qs[0].data)        
        pattern = r'[A-Za-z]{1,3}-[A-Za-z]{1,3}-\d{5}'
        for node in data['nodeDataArray']:
            text = node['text']
            # 提取匹配的內容
            matches = re.findall(pattern, text)
            if matches:
                doc_id = matches[0]
                doc_topic = text.replace(doc_id, "").replace("Doc:","").replace("\r\n","")
                doc_topic = re.sub(r"doc:", "", doc_topic, flags=re.IGNORECASE)
                print(f"{doc_id}: {doc_topic}")

        qs = Mindmap.objects.filter(inc_id=2435)
        data = json.loads(qs[0].data)


    def test_modify_django_course_mindmap(self):
        color = "#f4fc0d"
        default_color = "#adc2ff"
        doc_ids = ['Dja-Mod-00060','Dja-Mod-00005','Dja-mod-00004','Dja-Vie-00003','Dja-RES-00038','Dja-RES-00041','Dja-RES-00043','Dja-Lis-00003','Dja-Jso-00002']
        qs = Mindmap.objects.filter(inc_id=1168)
        data = json.load(qs[0].data)
        pattern = r'[A-Za-z]{1,3}-[A-Za-z]{1,3}-\d{5}'
        for node in data['nodeDataArray']:
            text = node['text']
            #還原顏色
            if node['brush'] == color:
                node['brush'] = default_color
            if "color" in node and node['color'] == color:
                node['color'] = default_color
            # 提取匹配的內容
            matches = re.findall(pattern, text)
            if matches:
                doc_id = matches[0]
                if doc_id in doc_ids:
                    node['brush'] = color
                    node['color'] = color
        with open('output.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        Mindmap.objects.filter(inc_id=1168).update(data=json.dumps(data))


    def test_modify_react_course_mindmap(self):
        color = "#f4fc0d"
        default_color = "#adc2ff"
        doc_ids = ['Rea-Sty-00010','Rea-Sty-00016','Rea-Sty-00032','Rea-Sty-00021','Rea-Sty-00014','Rea-Sty-00011','Rea-Com-00021','Rea-Com-00022','Rea-Sty-00038','Rea-Dat-00010','Rea-Fet-00001','Rea-Dat-00011','Rea-Com-00034','Rea-Com-00039','Rea-Com-00024','Rea-Dat-00021',
        'Rea-Get-00014']
        qs = Mindmap.objects.filter(inc_id=2435)
        data = json.loads(qs[0].data)
        pattern = r'[A-Za-z]{1,3}-[A-Za-z]{1,3}-\d{5}'
        for node in data['nodeDataArray']:
            text = node['text']
            #還原顏色
            if node['brush'] == color:
                node['brush'] = default_color
            if "color" in node and node['color'] == color:
                node['color'] = default_color
            # 提取匹配的內容
            matches = re.findall(pattern, text)
            if matches:
                doc_id = matches[0]
                if doc_id in doc_ids:
                    node['brush'] = color
                    node['color'] = color
        with open('output.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        Mindmap.objects.filter(inc_id=2435).update(data=json.dumps(data))


    def test_confirm_django_product_course(self):
        contacts = ['hw','lxb']
        color = "#f4fc0d"  #需要確認的顏色
        default_color = "#adc2ff" #默認的顏色
        confirm_data = []
        with open('confirm_technical.json', 'r', encoding='utf-8') as file:
            confirm_data = json.load(file)
        qs = Mindmap.objects.filter(inc_id=1168)
        data = json.loads(qs[0].data)
        exists_technical = set()
        for contact in contacts:
            contact_confirm_data = filter(lambda x: contact in x['people'], confirm_data)
            doc_ids = [row['tecno'].strip() for row in contact_confirm_data]
            pattern = r'[A-Za-z]{1,3}-[A-Za-z]{1,3}-\d{5}'
            for node in data['nodeDataArray']:
                text = node['text']
                # 提取匹配的內容
                matches = re.findall(pattern, text)
                if matches:
                    doc_id = matches[0]
                    if doc_id in doc_ids:
                        exists_technical.add(doc_id)
                        if len(text) > 15:
                            last_str = text[len(text)-15:].strip()
                            if bool(re.search(r'\d$', last_str)):
                                node['text'] = text + " " + contact
                            elif last_str.find(contact) ==  -1:
                                node['text'] = text + "," + contact                                
                        node['brush'] = color
                        node['color'] = color
        Mindmap.objects.filter(inc_id=1168).update(data=json.dumps(data))
        #打印出哪些Technical不存在
        all_confirm_technical_ids = [row['tecno'].strip() for row in confirm_data]
        notexists_technical = [tecno for tecno in all_confirm_technical_ids if tecno not in exists_technical]
        print("不存在的Technical有:")
        print("'"+"','".join(notexists_technical) + "'")


    def test_confirm_react_product_course(self):
        contacts = ['hw','lxb']
        color = "#f4fc0d"  #需要確認的顏色
        default_color = "#adc2ff" #默認的顏色
        confirm_data = []
        with open('confirm_technical.json', 'r', encoding='utf-8') as file:
            confirm_data = json.load(file)
        qs = Mindmap.objects.filter(inc_id=2435)
        data = json.loads(qs[0].data)
        exists_technical = set()
        for contact in contacts:
            contact_confirm_data = filter(lambda x: contact in x['people'], confirm_data)
            doc_ids = [row['tecno'].strip() for row in contact_confirm_data]
            pattern = r'[A-Za-z]{1,3}-[A-Za-z]{1,3}-\d{5}'
            for node in data['nodeDataArray']:
                text = node['text']
                # 提取匹配的內容
                matches = re.findall(pattern, text)
                if matches:
                    doc_id = matches[0]
                    if doc_id in doc_ids:
                        exists_technical.add(doc_id)
                        if len(text) > 15:
                            last_str = text[len(text)-15:].strip()
                            if bool(re.search(r'\d$', last_str)):
                                node['text'] = text + " " + contact
                            elif last_str.find(contact) ==  -1:
                                node['text'] = text + "," + contact                                
                        node['brush'] = color
                        node['color'] = color
        Mindmap.objects.filter(inc_id=2435).update(data=json.dumps(data))
        #打印出哪些Technical不存在
        all_confirm_technical_ids = [row['tecno'].strip() for row in confirm_data]
        notexists_technical = [tecno for tecno in all_confirm_technical_ids if tecno not in exists_technical]
        print("不存在的Technical有:")
        print("'"+"','".join(notexists_technical) + "'")

        """
        用于處理不存在的Technical的Sql
        Select B.MA003,MB016,MB026,MB023, Convert(varchar(500),MB004) + CHAR(13) + CHAR(10) + 'Doc:'+rtrim(MB023) Desp from TECMB A
        inner join TECMA B
        on A.MB015 = B.MA001
        where MB023 in ('Dja-RES-00038','Dja-Mod-00060','Dja-RES-00041','Dja-RES-00053','Dja-RES-00039','Dja-RES-00042','Dja-RES-00043','Vue-Com-00016','Dja-Exp-00001','Dja-Res-00010','Vue-Com-00045','Dja-Com-00038','Dja-Lis-00001','Dja-Gen-00006','Dja-Adm-00002','Dja-Res-00055','Del-del-00028','Pyt-Mod-00006','Dja-bin-00001')
        and MA003 in ('Django')
        """

class TestConversationService(TestCase):
    databases=['MPMS']
    def test_get_chart_data(self):
        service = ConversationService()
        topic = TopicCategories()
        topic.id = 58
        service.load_topic_data(topic, None)

if __name__ == "__main__": 
    ##unittest.main()
    ##content = "dict_keys(['datatable', 'draw', 'columns[0][data]', 'columns[0][name]', 'columns[0][searchable]', 'columns[0][orderable]', 'columns[0][search][value]', 'columns[0][search][regex]', 'columns[1][data]', 'columns[1][name]', 'columns[1][searchable]', 'columns[1][orderable]', 'columns[1][search][value]', 'columns[1][search][regex]', 'columns[2][data]', 'columns[2][name]', 'columns[2][searchable]', 'columns[2][orderable]', 'columns[2][search][value]', 'columns[2][search][regex]', 'columns[3][data]', 'columns[3][name]', 'columns[3][searchable]', 'columns[3][orderable]', 'columns[3][search][value]', 'columns[3][search][regex]', 'columns[4][data]', 'columns[4][name]', 'columns[4][searchable]', 'columns[4][orderable]', 'columns[4][search][value]', 'columns[4][search][regex]', 'columns[5][data]', 'columns[5][name]', 'columns[5][searchable]', 'columns[5][orderable]', 'columns[5][search][value]', 'columns[5][search][regex]', 'columns[6][data]', 'columns[6][name]', 'columns[6][searchable]', 'columns[6][orderable]', 'columns[6][search][value]', 'columns[6][search][regex]', 'columns[7][data]', 'columns[7][name]', 'columns[7][searchable]', 'columns[7][orderable]', 'columns[7][search][value]', 'columns[7][search][regex]', 'columns[8][data]', 'columns[8][name]', 'columns[8][searchable]', 'columns[8][orderable]', 'columns[8][search][value]', 'columns[8][search][regex]', 'columns[9][data]', 'columns[9][name]', 'columns[9][searchable]', 'columns[9][orderable]', 'columns[9][search][value]', 'columns[9][search][regex]', 'columns[10][data]', 'columns[10][name]', 'columns[10][searchable]', 'columns[10][orderable]', 'columns[10][search][value]', 'columns[10][search][regex]', 'columns[11][data]', 'columns[11][name]', 'columns[11][searchable]', 'columns[11][orderable]', 'columns[11][search][value]', 'columns[11][search][regex]', 'columns[12][data]', 'columns[12][name]', 'columns[12][searchable]', 'columns[12][orderable]', 'columns[12][search][value]', 'columns[12][search][regex]', 'order[0][column]', 'order[0][dir]', 'start', 'length', 'search[value]', 'search[regex]', '_', 'order[1][column]', 'order[1][dir]'])"
    ##SessionService.search_task_with_session('00001', '14005')
    ##match = re.match(r'order\[\d+\]\[column\]', content)
    ##if match:
    ##  print(match.group())
    #test = TestCategory()
    #test.test_technical_category()
    ##print(SWTools.encrypt('marcus11'))
    '''
    regex = "User\\s+Requirement\\s+for\\s+(.*?)\\s+to"
    match = re.search(regex, "For the Project (00298) schedule the User Requirement for WJ MES to be goal and complete within 2 month and list tasks with prefix in this format pid-tid-xxx where (00390-1000-xxx)  xxx is a running number incremented by 10", re.IGNORECASE)
    if match:
        print(match.group(1))
    else:
        print("未匹配到")
    print('asdfsd')
    '''
    #password = SWTools.encrypt("Admin@123")        
    #print(password)
    #test = TechnicalMindmap()
    #test.test_confirm_django_product_course()
    #test.test_confirm_react_product_course()
    ##test.test_modify_react_course_mindmap()
    #server = NtfyNotificationService()
    #server.send_project_status()
    #server.send_help_desk_aisummary()
    #server = NtfyNotificationService()
    #server.send_summary_project_status()    
    #generatePreConditionSentences()
    #server = NtfyNotificationService()
    #qs = models.Syspara.objects.values("fvalue").filter(ftype="ProjectStatus", nfield="Test")
    #server.send_summary_project_status()
    ##测试获取目录产品可用库存
    """
    auth_endpoint = "http://203.198.152.189:8010/auth/"
    auth_response = requests.post(auth_endpoint, json={'username': 'test', 'password': 'test123456'}) 
    print(auth_response)
    if auth_response.status_code == 200:
        api_key = auth_response.json()['token']
        headers = {'Authorization': f'Api-Key {api_key}'}
        #response = requests.get('http://203.198.152.189:8010/stock_availability', headers=headers)
        #帶參數的調用
        response = requests.get('http://203.198.152.189:8010/stock_availability?warehouse=china', headers=headers)
        # response = requests.get('http://203.198.152.189:8010/stock_availability?itemcode=KS 1220SB-L-EU,RL 2969PN/Q-EU,TOB 2740PN-L-EU', headers=headers)
        if response.status_code == 200:
            print(response.json())
    """
    ##测试OC Stock Report
    auth_endpoint = "http://203.198.152.189:8010/auth/"
    auth_response = requests.post(auth_endpoint, json={'username': "test", 'password': "test123456"}) 
    print(auth_response)
    if auth_response.status_code == 200:
        api_key = auth_response.json()['token']
        headers = {'Authorization': f'Api-Key {api_key}'}
        response = requests.get('http://203.198.152.189:8010/oc_stock_report/', headers=headers)
        #帶參數的調用
        # response = requests.get('http://203.198.152.189:8010/oc_stock_report?cat=Wall,Celling,Table&flag=GISP,NON-GISP ', headers=headers)
        print(response)
        if response.status_code == 200:
            print(response.json())
