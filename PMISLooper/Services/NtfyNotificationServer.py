from BaseApp.library.tools import SWTools,DateTools
from PMIS.Services.ActiveTaskService import ActiveTaskService
from PMIS.Services.UserService import UserService
from django.forms.models import model_to_dict
from django.db.models import Count,Q
from DataBase_MPMS.models import Syspara,VTask,Task,VTaskRecordid,VTasklist,VDocument,Goalmanagement,TasklistRelation
from django.core.cache import cache
import time
import logging
from PMIS.Services.TemplateService import TemplateService
from PMIS.Services.UserService import UserService
from django.test import RequestFactory
from operator import itemgetter
from BaseApp.library.tools import AsyncioTools,DateTools,ModelTools
from BaseApp.library.middleware import LogPortMiddleware
from django.urls import reverse
from django import dispatch
from django.dispatch import receiver
from django.db import connections
import threading
from time import sleep
from django.utils.dateparse import parse_datetime
from DataBase_MPMS.models import Pmstr
from django.conf import settings
import copy
import json
import os
from ChatwithAi_app.Services.ProjectManagementService import ProjectManagementService
from ChatwithAi_app.Services.AiManagementService import AiManagementService
from Notification_app.models import Ntfymessage
from django.db.models import Sum,Count,Max,Min,Avg,Q
from Authorization_app.permissions.decorators_pmis import has_permission_message, get_users_with_permission_message

send_finish_task_signal = dispatch.Signal()
send_remind_task_signal = dispatch.Signal()
clear_remind_task_signal = dispatch.Signal()
send_intray_task_signal = dispatch.Signal()
send_new_task_instant_signal = dispatch.Signal()

LOGGER = logging.getLogger(__name__)
NOTIFICATION_FLAG_FIELD_NAME = "notification_falg"
NOTIFICATION_KNOW_FIELD_NAME = "know_flag"
NOTIFICATION_OUTSTAINDING_GOAL_FLAG = "outstanding goal" #Outstanding
NOTIFICATION_TODAY_CYCLE_FIXED_TASK_FLAG = "today cycle fixed task" #Fixed Day
NOTIFICATION_HIGHEST_TASK = "highest task" #High Priority
NOTIFICATION_COMPLETE_TASK = "complete task" #Completion 
NOTIFICATION_REMIND_TASK = "remind task" #Reminder
NOTIFICATION_TODO_TASK = "To-Do" #To-Do, 
NOTIFICATION_ISSUE_TASK = "issue task" #New Request
NOTIFICATION_CONVERT_TASK = "convert issue task"
NOTIFICATION_ASSIGN_ISSUE_TASK = 'assign issue task' #Allocation
NOTIFICATION_NEW_TASK = "new task" #Allocation
NOTIFICATION_QUESTION_TASK = "question" #Forum
NOTIFICATION_DELAY_RESEND_TASK = "DelayResend"
NOTIFICATION_PROJECT_STATUS = "Project Status" #Project Status
NOTIFICATION_PROJECT_MILESTONE = "Milestone"
NOTIFICATION_MEETING = "Meeting"
NOTIFICATION_IN_TRAY_TASK = "In Tray Task"
NOTIFICATION_HELP_DESK = "Help Desk"
DEBUG_SEND_USER = "lsy"


@receiver(send_finish_task_signal)
def send_finish_task_signal_callback(sender, **kwargs):
    contact = kwargs.get('users')
    task = kwargs.get("task")
    if contact and task:
        thread = threading.Thread(target=handle_send_finish_task_signal, args=(contact,task,))
        thread.start()

def handle_send_finish_task_signal(users, task):
    service = NtfyNotificationService()
    #測試使用
    service.send_finish_task(users,task)
    #檢查是否這個任務的session是否有關聯session如果有，需要同步這個任務後再發一個新任務消息
    response = service.sync_task_with_relation_session(task)
    if response['status'] and response['data']:
        target_task = response['data']
        service.send_finish_task(users, target_task, False)    

@receiver(send_intray_task_signal)
def send_intray_task_signal_callback(sender, **kwargs):
    task = kwargs.get("task")
    if task:
        thread = threading.Thread(target=handle_send_intray_task_signal, args=(task,))
        thread.start()

def handle_send_intray_task_signal(task):
    service = NtfyNotificationService()
    #測試使用
    service.send_intray_task(task)

@receiver(send_remind_task_signal)
def send_remind_task_signal_callback(sender, **kwargs):
    remindInfos = kwargs.get("remindInfos")
    if remindInfos:
        thread = threading.Thread(target=handle_send_remind_task_signal, args=(remindInfos, ))
        thread.start()

def handle_send_remind_task_signal(remindInfos):
    service = NtfyNotificationService()
    #測試使用
    service.sendNotificationWithRemind(remindInfos)

@receiver(send_new_task_instant_signal)
def send_new_task_instant_signal_callback(sender, **kwargs):
    task = kwargs.get("task")
    if task:
        thread = threading.Thread(target=handle_send_new_task_instant_signal, args=(task, ))
        thread.start()

def handle_send_new_task_instant_signal(task):
    service = NtfyNotificationService()
    #調用限時發送new任務
    service.send_new_task_instant(task)
    #檢查是否這個任務的session是否有關聯session如果有，需要同步這個任務後再發一個新任務消息
    response = service.sync_task_with_relation_session(task)
    if response['status'] and response['data']:
        target_task = response['data']
        service.send_new_task_instant(target_task)



@receiver(clear_remind_task_signal)
def clear_remind_task_signal_callback(sender, **kwarg):
    reminds = kwarg.get("reminds")
    if reminds:
        thread = threading.Thread(target=handle_clear_remind_task_signal, args=(reminds, ))
        thread.start()    
def handle_clear_remind_task_signal(reminds):
    service = NtfyNotificationService()
    #測試使用
    service.clear_remind(reminds)    

class NtfyNotificationService(object):

    def getManagers(self):
        """
        功能描述：獲取消息發送到哪些管理人員
        """
        cache_name = "{0}:{1}".format(__name__, self.getManagers.__name__)
        managers = cache.get(cache_name)
        if managers:
            return managers
        else:
            managers = []          
            try:
                qs = Syspara.objects.values("fvalue").filter(ftype="Notification", nfield="Managers")
                if len(qs) > 0:
                    managers = qs[0]['fvalue'].strip().split(",")
                    cache.set(cache_name, managers, timeout=60 * 60 * 24) #過期時間為1天    
            except Exception as e:
                LOGGER.error("獲取發送消息到哪些管理人員失敗，請檢查系統參數，ftype:Notification nfield:Managers")
            return managers

    def getAllUsers(self):
        allUsers = UserService.GetPartUserNames()
        return allUsers

    def getNotificationUserSetting(self):
        """
        功能描述：獲取設置的哪些用戶可以收到哪些消息的信息
        """
        cache_name = "{0}:{1}".format(__name__, self.getNotificationUserSetting.__name__)
        userSettings = cache.get(cache_name)
        if userSettings:
            return userSettings
        else:
            userSettings = {}
            try:
                qs = Syspara.objects.values("nfield","ftype","fvalue").filter(ftype__startswith="NotificationSetting").order_by("nfield")
                if len(qs) > 0:
                    for item in qs:
                        username = item['nfield'].strip()
                        value = item['fvalue'].strip()
                        topic = item['ftype'].strip().replace("NotificationSetting_","")
                        if username in userSettings:
                            if topic in userSettings[username]:
                                userSettings[username][topic].extend(value.split(","))
                            else:
                                userSettings[username][topic] = value.split(",")
                        else:
                            userSettings[username] = {topic:value.split(",")}
                    #cache.set(cache_name, userSettings, timeout=60 * 60) #過期時間為1天    
            except Exception as e:
                LOGGER.error("獲取聯繫人應該接收哪些消息的設置信息失敗，請檢查系統參數，ftype:NotificationSetting_*")
            return userSettings

    def has_intersection(self, arr1, arr2):
        set1 = set(arr1)
        set2 = set(arr2)
        return bool(set1 & set2)            

    def getReceiverWithUserSetting(self, recordids, sessions):
        userSettings = self.getNotificationUserSetting()
        users = []
        if recordids:
            users.extend([k for k,v in userSettings.items() if "Project" in v and self.has_intersection(recordids, v['Project'])])
        if sessions:
            users.extend([k for k,v in userSettings.items() if "Session" in v and self.has_intersection(sessions, v['Session'])])
        return list(set(users))
        

    def getNotifcationTimeZone(self):
        """
        功能描述：獲取設置的消息時區
        """
        cache_name = "{0}:{1}".format(__name__, self.getNotifcationTimeZone.__name__)
        notifTimeZone = cache.get(cache_name)
        if notifTimeZone:
            return notifTimeZone
        else:
            notifTimeZone = {}
            try:
                qs = Syspara.objects.values("nfield","fvalue").filter(ftype="NotificationTimeZone")
                if len(qs) > 0:
                    notifTimeZone = {item["nfield"]:{'minuteDiff':int(item['fvalue']),'users':[]} for item in qs}
                    qs = Syspara.objects.values("nfield","fvalue").filter(ftype="NotificationTimeZoneUsers")
                    if len(qs) > 0:
                        for row in qs:
                            timeZone = row['nfield']
                            if timeZone in notifTimeZone:
                                notifTimeZone[timeZone]['users'].extend(row['fvalue'].split(","))
                    cache.set(cache_name, notifTimeZone, timeout=60 * 60 * 24) #過期時間為1天    
            except Exception as e:
                LOGGER.error("獲取獲取設置的消息時區，請檢查系統參數，ftype:NotificationTimeZone")
            return notifTimeZone

    def getUserDelay(self):
        cache_name = "{0}:{1}".format(__name__, self.getUserDelay.__name__)        
        userDelay = cache.get(cache_name)
        if userDelay != None:
            return userDelay
        else:
            userDelay = {}
            try:
                notifTimeZone = self.getNotifcationTimeZone()        
                for area, notifTimeZoneInfo in notifTimeZone.items():
                    users = notifTimeZoneInfo['users']
                    minuteDiff = notifTimeZoneInfo['minuteDiff']
                    userDelay.update({user:int(minuteDiff) for user in users})
                cache.set(cache_name, userDelay, timeout=60 * 60 * 24)
            except Exception as e:
                LOGGER.error("獲取獲取用戶延遲發送失敗，請檢查系統參數，ftype:NotificationTimeZone")
            return userDelay



    def getNotifcationNoTimeZoneUsers(self):
        notifTimeZone = self.getNotifcationTimeZone()
        users = UserService.GetPartUserNames()
        hasZoneUsers = []
        for zoneInfo in notifTimeZone.values():
            hasZoneUsers.extend(zoneInfo['users'])
        hasZoneUsers = list(set(hasZoneUsers))
        return [user for user in users if user not in hasZoneUsers]


    def send_finish_task(self,users,taskObj, is_send_higest_task=True):
        task = copy.deepcopy(taskObj)
        task = dict(task) if type(task) != dict else task
        task[NOTIFICATION_FLAG_FIELD_NAME] = NOTIFICATION_COMPLETE_TASK
        taskContact = task['contact'].strip()
        title = "{0}'s Completed Tasks".format(taskContact)
        tags = ['white_check_mark']
        recordid, sessionid = self.get_recordid_sessionid(task)
        send_users = get_users_with_permission_message("Receive_Completion", 4, recordid, sessionid)
        if settings.DEBUG == True:
            send_users = [DEBUG_SEND_USER]
        self.send_task(send_users, title, task, tags)        
        sleep(1)
        if is_send_higest_task:
            self.send_schedule_higest_task([taskContact])

    def send_intray_task(self,taskObj):
        task = copy.deepcopy(taskObj)
        task = dict(task) if type(task) != dict else task
        task[NOTIFICATION_FLAG_FIELD_NAME] = NOTIFICATION_IN_TRAY_TASK
        taskContact = task['contact'].strip()
        title = "{0}'s In Tray Tasks".format(taskContact)
        tags = ['memo']
        recordid, sessionid = self.get_recordid_sessionid(task)
        has_permission_users = get_users_with_permission_message("Receive_InTray", 4, recordid, sessionid)
        if taskContact in has_permission_users:
            send_users = [taskContact]
        else:
            send_users = []        
        if settings.DEBUG == True:
            send_users = [DEBUG_SEND_USER]
        self.send_task(send_users, title, task, tags)        
    

    def send_assign_task(self,sender, taskObj):
        task = copy.deepcopy(taskObj)
        task = dict(task) if type(task) != dict else task
        task[NOTIFICATION_FLAG_FIELD_NAME] = NOTIFICATION_ASSIGN_ISSUE_TASK
        taskContact = task['contact'].strip()
        
        title = "Issue reported assigned by {0}".format(sender)
        tags = ['rotating_light']
        recordid, sessionid = self.get_recordid_sessionid(task)
        has_permission_users = get_users_with_permission_message("Receive_Allocation", 4, recordid, sessionid)
        if taskContact in has_permission_users:
            send_users = [taskContact]
        else:
            send_users = []
        if settings.DEBUG == True:
            send_users = [DEBUG_SEND_USER]
        self.send_task(send_users, title, task, tags)        

    def getDateStr(self, dateObj):
        if not dateObj:
            return ""
        if type(dateObj) == str:
            try:
                dateObj = parse_datetime(dateObj)
            except Exception as e:
                return ""
        return  DateTools.formatf(dateObj,'%Y-%m-%d')

    def send_remind_task(self,sender, taskObj):
        task = copy.deepcopy(taskObj)
        task = dict(task) if type(task) != dict else task
        task[NOTIFICATION_FLAG_FIELD_NAME] = NOTIFICATION_TODO_TASK
        taskContact = task['contact'].strip()
        title = "{0}'s task sent by {1}".format(taskContact, sender)
        tags = ['loudspeaker']
        recordid, sessionid = self.get_recordid_sessionid(task)
        has_permission_users = get_users_with_permission_message("Receive_ToDo", 4, recordid, sessionid)
        if taskContact in has_permission_users:
            send_users = [taskContact]
        else:
            send_users = []
        if settings.DEBUG == True:
            send_users = [DEBUG_SEND_USER]
        self.send_task(send_users, title, task, tags)       

    def set_notification_action(self,message, task):
        taskContact = '' if not task['contact'] else task['contact'].strip()
        actionUrl = "{0}/looper/staff_dashboard?username={1}&bdate={2}&edate={3}&dp=3&dp_task_pk={4}".format(settings.WEBPMIS_SERVER_OUT, taskContact, 
        DateTools.formatf(DateTools.getBeginOfWeek(DateTools.now()), '%Y-%m-%d'),
        DateTools.formatf(DateTools.getEndOfWeek(DateTools.now()), '%Y-%m-%d'),
        task['inc_id'])
        defaultAction =  {
                "action": "view",
                "label": "View Task",
                "url": actionUrl,
            }
        actions = []        
        if NOTIFICATION_FLAG_FIELD_NAME in task:
            if task[NOTIFICATION_FLAG_FIELD_NAME] == NOTIFICATION_OUTSTAINDING_GOAL_FLAG: ##outstanding goal
                pid = task['pid']
                tid = task['tid']
                qs = VTaskRecordid.objects.values("recordid").filter(pid=pid, tid=tid)[:1]
                if len(qs) > 0:
                    recordid = qs[0]['recordid']
                    actionUrl = "{0}/looper/goal/goal_management?contact={1}&recordid={2}".format(settings.WEBPMIS_SERVER_OUT, taskContact, recordid)
                    defaultAction['label'] = "Outstanding"
                    defaultAction['url'] = actionUrl
            elif task[NOTIFICATION_FLAG_FIELD_NAME] == NOTIFICATION_HIGHEST_TASK:
                defaultAction['label'] = "Highest Priority"
            elif task[NOTIFICATION_FLAG_FIELD_NAME] == NOTIFICATION_TODAY_CYCLE_FIXED_TASK_FLAG:
                defaultAction['label'] = "Fixed Day"
            elif task[NOTIFICATION_FLAG_FIELD_NAME] == NOTIFICATION_TODO_TASK:
                defaultAction['label'] = "To-Do"            
            elif task[NOTIFICATION_FLAG_FIELD_NAME] == NOTIFICATION_COMPLETE_TASK:
                defaultAction['label'] = "Completion"            
            elif task[NOTIFICATION_FLAG_FIELD_NAME] == NOTIFICATION_IN_TRAY_TASK:
                defaultAction['label'] = "In Tray"
            elif task[NOTIFICATION_FLAG_FIELD_NAME] == NOTIFICATION_REMIND_TASK:
                defaultAction['label'] = "Reminder"        
            elif task[NOTIFICATION_FLAG_FIELD_NAME] == NOTIFICATION_NEW_TASK:
                defaultAction['label'] = "New Task"        
            elif task[NOTIFICATION_FLAG_FIELD_NAME] == NOTIFICATION_QUESTION_TASK:
                defaultAction['label'] = "Forum"
                defaultAction['url'] = task['question_url']
            elif task[NOTIFICATION_FLAG_FIELD_NAME] == NOTIFICATION_ISSUE_TASK: #系統問題上報
                assignTaskUrl = "{0}/looper/notif/assign_task?taskno={1}-{2}-{3}".format(settings.WEBPMIS_SERVER_OUT, task['pid'], int(task['tid']), int(task['taskid']))                
                defaultAction['label'] = "Allocation"
                defaultAction['url'] = assignTaskUrl
            elif task[NOTIFICATION_FLAG_FIELD_NAME] == NOTIFICATION_PROJECT_STATUS: ##Project Status
                url = "{0}/chatwithai/project_status?id={1}".format(settings.WEBPMIS_SERVER_OUT, task['project_status_id'])                
                defaultAction['label'] = "Project Status"
                defaultAction['url'] = url
            elif task[NOTIFICATION_FLAG_FIELD_NAME] == NOTIFICATION_PROJECT_MILESTONE: ##Milestone
                url = "{0}/looper/user/top5_projects?contact={1}&recordid={2}&sessions={3}&shrink=true".format(settings.WEBPMIS_SERVER_OUT,task['milestone_contact'], task['milestone_recordid'], task['milestone_sessionid'])                
                defaultAction['label'] = "Milestone"
                defaultAction['url'] = url                

        actions.append(defaultAction)
        message['actions'] = actions

    def setClickUrl(self, message, task):
        if NOTIFICATION_KNOW_FIELD_NAME in task and task[NOTIFICATION_KNOW_FIELD_NAME]: #需要添加一個知道了的按鈕            
            knowUrl = "{0}/looper/notif/user_know?taskno={1}-{2}-{3}".format(settings.WEBPMIS_SERVER_OUT, task['pid'], int(task['tid']), int(task['taskid']))
            message['click'] = knowUrl        

    def ellipsis_filename(self, filename, max_length=20):
        if len(filename) <= max_length:
            return filename

        # 分割文件名和扩展名
        name_part, extension_part = os.path.splitext(filename)

        # 在保留扩展名的同时减去三个点的长度
        max_name_length = max_length - len(extension_part) - 3
        part_length = max_name_length // 2  # 分为两部分
        start_part = name_part[:part_length]
        end_part = name_part[-part_length:]

        return f"{start_part}...{end_part}{extension_part}"

    def setAttachWithTask(self, message, task):
        docid='{0}{1}{2}'.format(task['pid'],int(task['tid']),int(task['taskid']))
        taskid='{0}-{1}-{2}'.format(task['pid'],int(task['tid']),int(task['taskid']))
        taskfolder = VDocument.objects.filter(docid=docid,foldername=taskid)\
            .extra(where=["T_Stamp = (SELECT MAX(T_Stamp) FROM Document WHERE DocId=%s and FolderName=%s AND V_Document.DocName = DocName)"], params=[docid,taskid]).order_by('folderid')
        attachActions = []
        if taskfolder.exists():
            uploadList = list(taskfolder.values())
            for file in uploadList:
                try:
                    filename=self.ellipsis_filename(file['docname'], 12)
                    url="{0}/looper/metting/browse_task_image?inc_id={1}".format(settings.WEBPMIS_SERVER_OUT, file['inc_id'])
                    attachActions.append({
                        "action": "view",
                        "label": filename,
                        "url": url,                    
                    })
                except Exception as e:
                    LOGGER.info(e)
        if len(attachActions) > 0:
            if 'actions' in message:
                message['actions'].extend(attachActions)
            else:
                message['actions'] = attachActions

    def get_recordid_sessionid(self, task):
        qs = VTasklist.objects.values("recordid","sessionid").filter(pid=task['pid'], tid=task['tid'])[:1]
        recordId = ""
        sessionId = f"{task['pid']}-{task['tid']}"
        if len(qs) > 0:
            recordId = qs[0]['recordid']        
            sessionId = qs[0]['sessionid']        
        return recordId, sessionId

    def send_task(self,users,title, task, tags=None):
        topic = 'PMIS'
        task = dict(task) if type(task) != dict else task
        dateStr = "EDate"        
        dateValue = DateTools.formatf(DateTools.now(),'%Y-%m-%d')
        recordId = ""
        sessionId = ""
        qs = VTasklist.objects.values("recordid","sessionid").filter(pid=task['pid'], tid=task['tid'])[:1]
        if len(qs) > 0:
            recordId = qs[0]['recordid']        
            sessionId = qs[0]['sessionid']
        planbdate = self.getDateStr(task['planbdate'])
        planedate = self.getDateStr(task['planedate'])
        currentDate = DateTools.formatf(DateTools.now(), '%m-%d %H:%M')
        if NOTIFICATION_FLAG_FIELD_NAME in task and (task[NOTIFICATION_FLAG_FIELD_NAME] == NOTIFICATION_HIGHEST_TASK or task[NOTIFICATION_FLAG_FIELD_NAME] == NOTIFICATION_OUTSTAINDING_GOAL_FLAG or \
            task[NOTIFICATION_FLAG_FIELD_NAME] == NOTIFICATION_TODAY_CYCLE_FIXED_TASK_FLAG or task[NOTIFICATION_FLAG_FIELD_NAME] == NOTIFICATION_NEW_TASK or 
            task[NOTIFICATION_FLAG_FIELD_NAME] == NOTIFICATION_QUESTION_TASK): #highest task
            dateStr = "PEDate"
            dateValue = planedate
        message = {"title":title, 'message':"""{0}

Date:{1}    
RID:{2}    SID:{3}
{4}:{5}    Sch Priority:{6}""".format(task['task'],currentDate, recordId, sessionId, dateStr, dateValue, 0 if not task['schpriority'] else int(task['schpriority']))
        }
        if tags:
            message['tags'] = tags
        self.set_notification_action(message, task)
        self.setClickUrl(message, task)
        SWTools.pushNtfyMessage(users,topic,message)
        self.saveNtfyMessageRecord(users, topic, message, task)
        if NOTIFICATION_DELAY_RESEND_TASK in task and task[NOTIFICATION_DELAY_RESEND_TASK]: #需要根據設置delay再次發送消息
            userDelay = self.getUserDelay()
            for user, delay in {key:value for key,value in userDelay.items() if key in users}.items():
                tempMessage = copy.deepcopy(message)
                tempMessage['delay'] = f"{delay}min"
                print({'delay':True, 'users':users, 'topic':topic, 'message':tempMessage})
                SWTools.pushNtfyMessage([user],topic,tempMessage)

    def send_schedule_higest_task(self, users, data=None):
        """
        功能描述：發送Today's task中未完成任務的優先級最高的任務
        參數說明:
            users：用戶數組
            data:要發送消息的 用戶名:任務字典, 如果有值則不必調用today's task讀取數據
        """
        if not data:
            data = self.get_all_highest_tasks(users)
        managerUsers = self.getManagers()
        for user, task in data.items():
            task = dict(task) if type(task) != dict else task
            taskContact = task['contact'].strip()
            recordid, sessionid = self.get_recordid_sessionid(task)
            send_users = get_users_with_permission_message("Receive_HighPriority", 4, recordid, sessionid)
            if settings.DEBUG == True: #測試時只發給hb alarm_clock
                send_users = [DEBUG_SEND_USER]            
            self.send_task(send_users, f"{taskContact}'s Tasks that should be done", task, ['date'])
            sleep(1)
            if settings.DEBUG == True: #測試時只發送一條信息
                return            

    def get_all_highest_tasks(self, users):
        factory = RequestFactory()    
        cache_name = LogPortMiddleware.__name__
        port = cache.get(cache_name)
        if not port:
            return {}
        url = 'http://127.0.0.1:{0}{1}'.format(port, reverse("today_fixed_tasks"))
        http_methods = {user:{"url":url + f"?contact={user}"} for user in users}
        responses = AsyncioTools.async_fetch_http_json(http_methods)
        result = {}
        for user, response in responses.items():
            today_tasks = response['data']
            if len(today_tasks) > 0:
                key=lambda x:records.index(x['recordid'])
                today_tasks = list(filter(lambda x:x['progress'] not in ['C','F','R'], today_tasks))
                if len(today_tasks) > 0:
                    today_tasks.sort(key=lambda x:0 if not x['schpriority'] else x['schpriority'], reverse=True)
                    task = today_tasks[0]
                    task[NOTIFICATION_FLAG_FIELD_NAME] = NOTIFICATION_HIGHEST_TASK
                    result[user] = task
        return result;

    
    def get_today_task_data(self, users):
        factory = RequestFactory()    
        cache_name = LogPortMiddleware.__name__
        port = cache.get(cache_name)
        if not port:
            return {}
        #url = 'http://222.118.20.236:{0}{1}'.format(port, reverse("today_fixed_tasks"))  #測試使用
        url = 'http://127.0.0.1:{0}{1}'.format(port, reverse("today_fixed_tasks"))
        http_methods = {user:{"url":url + f"?contact={user}"} for user in users}
        responses = AsyncioTools.async_fetch_http_json(http_methods)
        result = {'highest_tasks':{}, 'outstanding_goals':{}, 'user_fixed_day_tasks':{}}
        managers = self.getManagers()
        for user, response in responses.items():
            today_tasks = response['data']
            if len(today_tasks) > 0:
                ##分析出highest task
                unfinish_tasks = list(filter(lambda x:x['progress'] not in ['C','F','R'], today_tasks))
                if len(unfinish_tasks) > 0:
                    unfinish_tasks.sort(key=lambda x:0 if not x['schpriority'] else x['schpriority'], reverse=True)
                    task = unfinish_tasks[0]
                    task[NOTIFICATION_FLAG_FIELD_NAME] = NOTIFICATION_HIGHEST_TASK
                    result['highest_tasks'][user] = task
                ##分析出最早的一個Goal, 當前只發送管理人員的Goal
                if user in managers:
                    outstanding_goals = list(filter(lambda x:NOTIFICATION_FLAG_FIELD_NAME in x and x[NOTIFICATION_FLAG_FIELD_NAME] == NOTIFICATION_OUTSTAINDING_GOAL_FLAG and x['planedate'], today_tasks))
                    if len(outstanding_goals) > 0:
                        outstanding_goals.sort(key=lambda x:DateTools.format(parse_datetime(x['planedate'])))
                        result['outstanding_goals'][user] = [outstanding_goals[0]]
                ##分析出用戶當前天循環任務生成的fixed task
                cycleFixedTasks = list(filter(lambda x:NOTIFICATION_FLAG_FIELD_NAME in x and x[NOTIFICATION_FLAG_FIELD_NAME] == NOTIFICATION_TODAY_CYCLE_FIXED_TASK_FLAG and x['planedate'], today_tasks))
                if len(cycleFixedTasks) > 0:
                    cycleFixedTasks.sort(key=lambda x:DateTools.format(parse_datetime(x['planedate'])))
                    result['user_fixed_day_tasks'][user] = cycleFixedTasks
        return result;    

    def send_outstanding_goals(self, data):
        """
        功能描述：發送Today's task中Outstanding Goal中最早的一個Goal
        參數說明:
            data:要發送的消息 用戶名:任務字典
        """
        managerUsers = self.getManagers()
        for user, tasks in data.items():
            for task in tasks:
                task = dict(task) if type(task) != dict else task
                taskContact = task['contact'].strip()
                recordid, sessionid = self.get_recordid_sessionid(task)
                send_users = get_users_with_permission_message("Recevie_Outstanding", 4, recordid, sessionid)
                if settings.DEBUG == True: #測試時只發給hb alarm_clock
                    send_users = [DEBUG_SEND_USER]
                self.send_task(send_users, f"{taskContact}'s Oustanding Goal", task, ['rainbow_flag'])
                sleep(1)        
                if settings.DEBUG == True: #測試時只發送一條信息
                    return
                
    
    def send_cycle_fixed_tasks(self, data):
        """
        功能描述：發送Today's task中當天User Fixed Day Tasks中的循環任務
        參數說明:
            data:要發送的消息 用戶名:任務字典
        """
        for user, tasks in data.items():
            for task in tasks:
                task = dict(task) if type(task) != dict else task
                taskContact = task['contact'].strip()
                if type(task['planedate']) == str:
                    fixedDate = DateTools.formatf(parse_datetime(task['planedate']), '%y-%m-%d')
                else:
                    fixedDate = DateTools.formatf(task['planedate'], '%y-%m-%d')
                recordid, sessionid = self.get_recordid_sessionid(task)
                send_users = get_users_with_permission_message("Receive_FixedDay", 4, recordid, sessionid)                
                if settings.DEBUG == True: #測試時只發給hb alarm_clock
                    send_users = [DEBUG_SEND_USER]
                self.send_task(send_users, f"{taskContact}'s Fixed Day({fixedDate})", task, ['alarm_clock'])
                sleep(1)   
                if settings.DEBUG == True: #測試時只發送一條信息
                    return

    def send_new_task_instant(self,taskObj):        
        task = copy.deepcopy(taskObj)
        task = dict(task) if type(task) != dict else task
        task[NOTIFICATION_FLAG_FIELD_NAME] = NOTIFICATION_NEW_TASK
        taskContact = task['contact'].strip()
        recordid, sessionid = self.get_recordid_sessionid(task)
        send_users = get_users_with_permission_message("Receive_NewTask", 4, recordid, sessionid)
        if settings.DEBUG == True: 
            send_users = [DEBUG_SEND_USER]
        self.send_task(send_users, f"{taskContact}'s New Task", task, ['new'])

    def send_new_tasks(self, data):
        """
        功能描述：發送New Task
        參數說明:
            data:要發送的消息 用戶名:任務字典
        """
        for user, tasks in data.items():
            for task in tasks:
                task = dict(task) if type(task) != dict else task
                task[NOTIFICATION_FLAG_FIELD_NAME] = NOTIFICATION_NEW_TASK
                taskContact = task['contact'].strip()
                recordid, sessionid = self.get_recordid_sessionid(task)
                send_users = get_users_with_permission_message("Receive_NewTask", 4, recordid, sessionid)
                if settings.DEBUG == True: 
                    send_users = [DEBUG_SEND_USER]
                self.send_task(send_users, f"{taskContact}'s New Task", task, ['new'])
                sleep(1)   
                if settings.DEBUG == True: #測試時只發送一條信息
                    return

    def send_remind_task_with_pmstr(self,data):
        for user, tasks in data.items():
            for task in tasks:
                task = dict(task) if type(task) != dict else task
                task[NOTIFICATION_FLAG_FIELD_NAME] = NOTIFICATION_REMIND_TASK
                taskContact = task['contact'].strip()
                recordid, sessionid = self.get_recordid_sessionid(task)
                has_permission_users = get_users_with_permission_message("Receive_Reminder", 4, recordid, sessionid)
                if taskContact in has_permission_users:
                    send_users = [taskContact]
                else:
                    send_users = []
                if settings.DEBUG == True: 
                    send_users = [DEBUG_SEND_USER]
                self.send_task(send_users, f"{taskContact}'s Reminder Task", task, ['loudspeaker'])
                sleep(1)   
                if settings.DEBUG == True: #測試時只發送一條信息
                    return

    def sendTimelyNotificationsForPriorityTasksGoalsAndFixedDay(self, users):
        """
        功能描述：定時發送所有用戶highest priority task, Outstanding Goal, Fixed Day Task
        """
        todayTaskDatas = self.get_today_task_data(users)
        highest_tasks = todayTaskDatas['highest_tasks']
        outstanding_goals = todayTaskDatas['outstanding_goals']
        user_fixed_day_tasks = todayTaskDatas['user_fixed_day_tasks']
        ##發送highest_tasks, 如果出現異常接著執行
        try:
            self.send_schedule_higest_task(users, highest_tasks)
        except Exception as e:
            LOGGER.error(e)
            print(str(e))
        ##發送outstainding goals, 如果出現異常接著執行
        try:
            self.send_outstanding_goals(outstanding_goals)
        except Exception as e:
            print(str(e))
            LOGGER.error(e)
        ##發送用戶Fixed Day Tasks
        self.send_cycle_fixed_tasks(user_fixed_day_tasks)

    def sendAllTaskRemind(self):
        """
        功能描述：定時根據任務的提醒信息發送消息
        """
        def checkDate(remind):
            tr024 = 0 if not remind['tr024'] else remind['tr024'] #循環周期
            if tr024 == 0: #只發送一次
                if remind['starttime'].hour == currentDate.hour and remind['starttime'].minute == currentDate.minute: #當前小時分鐘==提醒開始時間才發送
                    return True
            else: #發送多次
                currentTimeMinute = currentDate.hour * 60  + currentDate.minute
                startTimeMinute = remind['starttime'].hour * 60 + remind['starttime'].minute
                if (currentTimeMinute - startTimeMinute) % tr024 == 0:
                    return True
            return False
        def checkOutstandingDate(remind):
            currentTimeMinute = currentDate.hour * 60  + currentDate.minute
            startTimeMinute = remind['starttime'].hour * 60 + remind['starttime'].minute
            if (currentTimeMinute - startTimeMinute) % 60 == 0:  #每60分鐘發送一次
                if remind['tr031'] and DateTools.format(remind['tr031']) == DateTools.format(DateTools.now()): #如果用戶當前點擊了I Know則今天不再發送
                    return False
                else:
                    return True
            return False

        currentDate = DateTools.now().replace(second=0, microsecond=0)
        ##讀取數據
        reminds = []
        try:
            with connections[ModelTools.get_database(Pmstr)].cursor() as cursor:
                strsql = '''
                    Select 
                    A.INC_ID,TR002,B.Contact TaskContact,
                    cast(case when TR028 = 1 then TR021 else dateadd(day,TR029,B.PlanBDate) end as Date) StartDate,
                    cast(TR004 as time) StartTime,cast(TR005 as time) EndTime,ISNULL(TR024,0) TR024,tr026,tr030,tr031,
                    case when TR030 <> 3 and B.PlanBDate is not null and cast(B.PlanEDate as date) < cast(getdate() as date) then 'Y' else 'N' end isout,
                    case TR030  when 1 then case when cast(getdate() as date) > cast(TR022 as date) then 'Y' else 'N' end
                    when 2 then case when B.Progress = 'C' or B.Progress = 'F' then 'Y' else 'N' end else 'N' end isFinish
                    from PMSTR A with(nolock)
                    inner join Task B with(nolock)
                    on A.TR002 = B.Pid + '-' + CONVERT(Varchar(20), CONVERT(Decimal(18, 0), B.Tid)) + '-' + CONVERT(Varchar(10), CONVERT(Decimal(18, 0), B.TaskID))
                    where TR007 <> 'F' and ISNULL(TR027,'Y') = 'Y' and ISNULL(B.contact,'') <> '' and 
                    cast(getdate() as time) >= cast(TR004 as time) and cast(getdate() as time) <= cast(TR005 as time) and 
                    cast(case when TR028 = 1 then TR021 else dateadd(day,TR029,B.PlanBDate) end as Date) is not null and 
                    cast(case when TR028 = 1 then TR021 else dateadd(day,TR029,B.PlanBDate) end as Date) <= cast(getdate() as Date)
                '''
                cursor.execute(strsql)
                columns = [column[0].lower() for column in cursor.description]
                for row in cursor.fetchall():
                    obj = dict(zip(columns, row))
                    reminds.append(obj)                        
        except Exception as e:
            LOGGER.error(e)
            print(str(e))
        send_reminds = filter(lambda x: x['isfinish'] == "N", reminds)
        clear_reminds = list(filter(lambda x:x['isfinish'] == "Y", reminds))
        if clear_reminds:
            clear_remind_task_signal.send(sender=self.__class__, reminds=clear_reminds)
        current_send_reminds = []
        for remind in send_reminds:
            try:
                remind[NOTIFICATION_KNOW_FIELD_NAME] = False #默認不添加I Know
                if remind['isout'] == "N": #沒有脫期時，只發送給任務的聯繫人
                    remind['remind_contacts'] = [remind['taskcontact']]
                    if checkDate(remind):
                        if remind['tr030'] == '3':
                            remind[NOTIFICATION_KNOW_FIELD_NAME] = True #需要用戶點擊I Know才能完成的提醒
                        current_send_reminds.append(remind)
                else: ##脫期時，按正常發送給脫期人聯繫人, 按一個小時一次發送給任務聯繫人
                    if remind['tr026'] and checkDate(remind): #按正常發送給脫期人聯繫人, 不需要添加I Know
                        temp_remind = copy.deepcopy(remind)
                        temp_remind['remind_contacts'] = remind['tr026'].split(",")
                        current_send_reminds.append(temp_remind)
                    if checkOutstandingDate(remind): #按一個小時一次發送給任務聯繫人
                        temp_remind = copy.deepcopy(remind)
                        temp_remind['remind_contacts'] = [remind['taskcontact']]
                        temp_remind[NOTIFICATION_KNOW_FIELD_NAME] = True #需要用戶點擊I Know才能完成的提醒
                        current_send_reminds.append(temp_remind)
            except Exception as e:
                LOGGER.error(e)
                print(str(e))
        if current_send_reminds:
            send_remind_task_signal.send(sender=self.__class__, remindInfos=current_send_reminds)

    def sendNotificationWithRemind(self, remindInfos):
        tasknos = list(set([item['tr002'] for item in remindInfos]))
        inc_ids = list(set([item['inc_id'] for item in remindInfos]))
        Pmstr.objects.filter(tr007="N",inc_id__in = inc_ids).update(tr007="I")
        qs = Task.objects.extra(where=["Pid + '-' + CONVERT(Varchar(20), CONVERT(Decimal(18, 0), Tid)) + '-' + CONVERT(Varchar(10), CONVERT(Decimal(18, 0), TaskID)) in ('{0}')".format("','".join(tasknos))]).values()
        taskMap = {"{0}-{1}-{2}".format(item['pid'], int(item['tid']), int(item['taskid'])):item for item in qs}
        reminds = []
        for remind in remindInfos:
            if remind['tr002'] in taskMap:
                remind['task'] = taskMap[remind['tr002']]
                remind['task'][NOTIFICATION_KNOW_FIELD_NAME] = remind[NOTIFICATION_KNOW_FIELD_NAME]
                reminds.append(remind)
        for remind in reminds:
            try: #如果有一條發送不出去，不要影響其他消息的發送
                if remind['task']['hoperation'] == 'F': #如果是Fixed Day任務
                    remind['task'][NOTIFICATION_FLAG_FIELD_NAME] = NOTIFICATION_TODAY_CYCLE_FIXED_TASK_FLAG
                    self.send_cycle_fixed_tasks({contact:[remind['task']] for contact in remind['remind_contacts']})
                elif remind['tr030'] == '3': #表示新任務需要用戶點擊知道了才能取消
                    self.send_new_tasks({contact:[remind['task']] for contact in remind['remind_contacts']})
                else:
                    self.send_remind_task_with_pmstr({contact:[remind['task']] for contact in remind['remind_contacts']})
            except Exception as e:
                print(str(e))
            print("*******正在發送任務的消息:{0}".format(remind['tr002']))

    def clear_remind(self, reminds):
        """
        功能描述：對於任務已經完成或已經到提醒結束時間的remind，更新remind的狀態
        """
        inc_ids = [item['inc_id'] for item in reminds]
        Pmstr.objects.filter(inc_id__in = inc_ids).update(tr007="F")
        Pmstr.objects.filter(tr027='Y').extra(where=["not exists (Select PId from Task where Pid=PARSENAME(REPLACE(TR002, '-', '.'), 3) and Tid = TRY_CAST(PARSENAME(REPLACE(TR002, '-', '.'), 2) AS float) and TaskId = TRY_CAST(PARSENAME(REPLACE(TR002, '-', '.'), 1) AS float))"]).delete()

    def send_question(self, taskObj, url):
        """
        功能描述：發送問題給所有人
        """
        task = copy.deepcopy(taskObj)
        task = dict(task) if type(task) != dict else task
        task[NOTIFICATION_FLAG_FIELD_NAME] = NOTIFICATION_QUESTION_TASK
        task['question_url'] = url
        taskContact = task['contact'].strip()
        title = "{0} raised a question on the forum".format(taskContact)
        tags = ['rotating_light']
        send_users = self.getAllUsers()
        if settings.DEBUG == True:
            send_users = [DEBUG_SEND_USER]
        self.send_task(send_users, title, task, tags)            

    def send_project_status(self):
        qs = Syspara.objects.values("fvalue").filter(ftype="ProjectStatus")
        
        if len(qs) > 0:
            for item in qs:
                try:
                    fvalue = item['fvalue']
                    fvalueArr = fvalue.split(":")
                    recordId = fvalueArr[0]
                    sessions = fvalueArr[1]
                    sessionids = sessions.split(",")
                    #IP - SZ Warehouse Implementation AI分析結果
                    sessionid = sessionids[0]
                    sessArr = sessionid.split("-")
                    qs = VTasklist.objects.values("sdesp","contact").filter(pid=sessArr[0], tid=sessArr[1])[:1]
                    if len(qs) > 0:
                        sessionDesc = qs[0]['sdesp']
                        taskDesc = '''Providing "{0}" AI Analysis Results'''.format(sessionDesc)
                        task = {"pid":sessArr[0], "tid":sessArr[1], "task":taskDesc,"planbdate":DateTools.now(),"planedate":DateTools.now(),"progress":"N","schpriority":None,"contact":None,"inc_id":""}
                        task[NOTIFICATION_FLAG_FIELD_NAME] = NOTIFICATION_PROJECT_STATUS
                        server = ProjectManagementService()
                        project_status_id = server.getProjectStatus(recordId, sessionids)
                        task['project_status_id'] = project_status_id
                        #task['project_status_id'] = 4
                        title = "Project Status with {0}".format(recordId)
                        tags = ['spiral_notepad']
                        send_users = get_users_with_permission_message("Show_Project_Status", 4, recordId, sessionid)
                        #send_users = list(set(self.getManagers()+self.getReceiverWithUserSetting([recordId],sessionids)))
                        if settings.DEBUG == True:
                            send_users = [DEBUG_SEND_USER]
                        self.send_task(send_users, title, task, tags)                           
                        if settings.DEBUG == True:
                            return
                except Exception as e:
                    LOGGER.error(e)

    def send_summary_project_status(self):
        qs = Syspara.objects.values("fvalue",'desp').filter(ftype="SummaryProjectStatus").filter(~Q(nfield='SystemRole'))
        if len(qs) > 0:
            for item in qs:
                try:
                    fvalue = item['fvalue']
                    fvalueArr = fvalue.split(":")
                    recordId = fvalueArr[0]
                    sessions = fvalueArr[1]
                    sessionids = sessions.split(",")
                    title_desc = item['desp']
                    taskDesc = '''Providing "{0}" AI Analysis Results'''.format(title_desc)
                    sessionid = sessionids[0]
                    sessArr = sessionid.split("-")
                    task = {"pid":sessArr[0], "tid":sessArr[1], "task":taskDesc,"planbdate":DateTools.now(),"planedate":DateTools.now(),"progress":"N","schpriority":None,"contact":None,"inc_id":""}
                    task[NOTIFICATION_FLAG_FIELD_NAME] = NOTIFICATION_PROJECT_STATUS
                    server = ProjectManagementService()
                    project_status_id = server.summaryProjectStatus(recordId, sessionids)
                    task['project_status_id'] = project_status_id
                    #task['project_status_id'] = 4
                    title = "Project Status with {0}".format(recordId)
                    tags = ['spiral_notepad']
                    send_users = get_users_with_permission_message("Show_Project_Status", 4, recordId)
                    if settings.DEBUG == True:
                        send_users = [DEBUG_SEND_USER]
                    self.send_task(send_users, title, task, tags)                           
                    if settings.DEBUG == True:
                        return
                except Exception as e:
                    LOGGER.error(e)



    def saveNtfyMessageRecord(self,users,topic,message, task=None):
        categoryMap = {
            NOTIFICATION_ISSUE_TASK:10, #New Request
            NOTIFICATION_ASSIGN_ISSUE_TASK:20, #Allocation
            NOTIFICATION_NEW_TASK:150, #New Task
            NOTIFICATION_HIGHEST_TASK:30, #High Priority
            NOTIFICATION_OUTSTAINDING_GOAL_FLAG:40, #Outstanding
            NOTIFICATION_TODAY_CYCLE_FIXED_TASK_FLAG:50, #Fixed Day
            NOTIFICATION_TODO_TASK:60, #To-Do
            NOTIFICATION_QUESTION_TASK:70, #Forum
            NOTIFICATION_COMPLETE_TASK:80, #Completion 
            NOTIFICATION_REMIND_TASK:90, #Reminder
            NOTIFICATION_PROJECT_STATUS:100,#Project Status
            NOTIFICATION_MEETING:110, #Meeting
            NOTIFICATION_IN_TRAY_TASK:120, #In Tray
            NOTIFICATION_PROJECT_MILESTONE:130, #Milestone
            NOTIFICATION_HELP_DESK:140, #Help Desk
        }
        """
        功能描述：保存所發消息的記錄
        """
        def getCategoryId():
            if not task:
                return None
            if NOTIFICATION_FLAG_FIELD_NAME in task and task[NOTIFICATION_FLAG_FIELD_NAME] in categoryMap:
                return categoryMap[task[NOTIFICATION_FLAG_FIELD_NAME]]
            else:
                return None
        try:
            fieldMap = {"click":"click_url","attch":"attch_url","markdown":"is_markdown","icon":"icon_url","call":"call_info"}
            ntfyMessages = []
            for user in users:
                tempTopic = "{0}_{1}".format(user.strip().upper(), topic.strip().upper())
                tempMessage = copy.deepcopy(message)
                tempMessage['topic'] = tempTopic
                ntfyMessage = Ntfymessage()
                ntfyMessage.category_id = getCategoryId()
                ntfyMessage.receiver = user
                ntfyMessage.sent_time = DateTools.now()
                ntfyMessage.is_markdown = False #默認為False
                ntfyMessage
                for field,value in tempMessage.items():
                    if field in fieldMap:
                        field = fieldMap[field]
                    if type(value) == list:
                        value = json.dumps(value)
                    setattr(ntfyMessage, field, value)
                ntfyMessages.append(ntfyMessage)
            save_qty = 0
            while save_qty < 5:
                maxId = Ntfymessage.objects.aggregate(Max('id'))['id__max']
                maxId = (maxId or 0) + 1
                try:
                    for m in ntfyMessages:
                        m.id = maxId
                        maxId += 1
                    Ntfymessage.objects.bulk_create(ntfyMessages, batch_size=50)
                    break
                except Exception as ex:
                    save_qty += 1
                    LOGGER.error(ex)
                    sleep(0.09)
        except Exception as e:
            LOGGER.error(e)
            
    def send_message_summary(self):
        users = self.getAllUsers()
        userSettings = self.getNotificationUserSetting()
        otherUsers = [key for key, value in userSettings.items()]
        users = list(set(users+otherUsers))
        topic = "PMIS"
        for user in users:
            title = "Your Message Summary"
            dateStr = "Date"
            dateValue = self.getDateStr(DateTools.now())
            actionUrl = "{0}/ntfy/message_summary?contact={1}&date={2}".format(settings.WEBPMIS_SERVER_OUT, user, DateTools.formatf(DateTools.now(),'%Y-%m-%d'))
            message = {"title":title, 'message':"""{0}

{1}:{2}    """.format("Message Summary of Today", dateStr, dateValue), 
            "tags":['bar_chart'],
            "actions": [
                {
                    "action": "view",
                    "label": "Summary",
                    "url": actionUrl,
                }]
            }        
            has_permission_users = get_users_with_permission_message("Receive_MessageSummary", 4)
            if user in has_permission_users:
                send_users = [user]
            else:
                send_users = []        
            if settings.DEBUG == True:
                send_users = [DEBUG_SEND_USER]
            SWTools.pushNtfyMessage(send_users,topic,message)       
            sleep(1)
            if settings.DEBUG == True: #測試時只發送一條信息
                return            
            ##self.saveNtfyMessageRecord(send_users,ntfy_topic,message)                 

    def send_milestone(self):
        qs = Syspara.objects.values("fvalue").filter(ftype="ProjectStatus")
        if len(qs) > 0:
            for item in qs:
                try:
                    fvalue = item['fvalue']
                    fvalueArr = fvalue.split(":")
                    recordId = fvalueArr[0]
                    sessions = fvalueArr[1]
                    sessionids = sessions.split(",")
                    sessionid = sessionids[0]
                    sessArr = sessionid.split("-")
                    qs = VTasklist.objects.values("sdesp","contact").filter(pid=sessArr[0], tid=sessArr[1])[:1]
                    if len(qs) > 0:
                        sessionDesc = qs[0]['sdesp']
                        taskDesc = '''Milestone for "{0}"'''.format(sessionDesc)
                        task = {"pid":sessArr[0], "tid":sessArr[1], "task":taskDesc,"planbdate":DateTools.now(),"planedate":DateTools.now(),"progress":"N","schpriority":None,"contact":None,"inc_id":""}
                        task[NOTIFICATION_FLAG_FIELD_NAME] = NOTIFICATION_PROJECT_MILESTONE
                        task['milestone_recordid'] = recordId
                        task['milestone_sessionid'] = sessionid
                        title = "{0}'s Milestone".format(recordId)
                        tags = ['spiral_calendar']
                        send_users = get_users_with_permission_message("Receive_Milestone", 4, recordId, sessionid)                        
                        ##獲取有這個Milestone的聯繫人，隨便取一個
                        period = "{0}-{1}".format(DateTools.formatf(DateTools.now(), '%Y'), DateTools.getQuarter(DateTools.now()))
                        qs = Goalmanagement.objects.values('contact').filter(period=period, goaltype='Q', recordid=recordId)
                        milestone_contacts = [item['contact'] for item in qs]
                        milestone_in_send_users = [item for item in send_users if item in milestone_contacts]
                        if len(milestone_in_send_users) > 0:
                            task['milestone_contact'] = milestone_in_send_users[0]
                        elif len(milestone_contacts) > 0:
                            task['milestone_contact'] = milestone_contacts[0]
                        else:
                            task['milestone_contact'] = ''
                        if settings.DEBUG == True:
                            send_users = [DEBUG_SEND_USER]
                        self.send_task(send_users, title, task, tags)                           
                        if settings.DEBUG == True:
                            return
                except Exception as e:
                    LOGGER.error(e)    

    def send_meeting_aisummary(self):
        try:
            topic = "PMIS"
            title = "Meeting's AI Summary"
            dateStr = "Date"
            dateValue = self.getDateStr(DateTools.now())
            server = AiManagementService()
            inc_id = server.getAiSummary("Meeting")
            url = "{0}/chatwithai/project_status?id={1}".format(settings.WEBPMIS_SERVER_OUT, inc_id)                
            message = {"title":title, 'message':"""{0}

{1}:{2}    """.format('Providing "Meeting" AI Analysis Results', dateStr, dateValue), 
            "tags":['bar_chart'],
            "actions": [
                {
                    "action": "view",
                    "label": "Meeting",
                    "url": url,
                }]
            }        
            send_users = get_users_with_permission_message("Receive_Meeting", 4)
            if settings.DEBUG == True:
                send_users = [DEBUG_SEND_USER]
            SWTools.pushNtfyMessage(send_users,topic,message)    
            self.saveNtfyMessageRecord(send_users, topic, message, {NOTIFICATION_FLAG_FIELD_NAME:NOTIFICATION_MEETING})
        except Exception as e:
            LOGGER.error(e)

    def send_help_desk_aisummary(self):
        try:
            topic = "PMIS"
            title = "Help Desk's AI Summary"
            dateStr = "Date"
            dateValue = self.getDateStr(DateTools.now())
            server = AiManagementService()
            inc_id = server.getAiSummary("Help Desk")
            url = "{0}/chatwithai/project_status?id={1}".format(settings.WEBPMIS_SERVER_OUT, inc_id)                
            message = {"title":title, 'message':"""{0}

{1}:{2}    """.format('Providing "Help Desk" AI Analysis Results', dateStr, dateValue), 
            "tags":['bar_chart'],
            "actions": [
                {
                    "action": "view",
                    "label": "Help Desk",
                    "url": url,
                }]
            }        
            send_users = get_users_with_permission_message("Receive_HelpDesk", 4)
            if settings.DEBUG == True:
                send_users = [DEBUG_SEND_USER]
            SWTools.pushNtfyMessage(send_users,topic,message)    
            self.saveNtfyMessageRecord(send_users, topic, message, {NOTIFICATION_FLAG_FIELD_NAME:NOTIFICATION_HELP_DESK})
        except Exception as e:
            print(str(e))
            LOGGER.error(e)            
    
    def sync_task_with_relation_session(self, task):
        response_data = {'status': False, 'msg': '', 'data': {}}
        try:
            relations = TasklistRelation.objects.filter(status='I', relationtype='S', relationsessionid=f"{task['pid']}-{int(task['tid'])}")
            check_qty = 0
            if len(relations) > 0:
                #檢查這個源任務是否存在, 可能會因為事務的原因導致源任務不存在
                source_task_isexists = False
                while check_qty < 3:
                    if Task.objects.filter(pid=task['pid'], tid=task['tid'], taskid=task['taskid']).exists():
                        source_task_isexists = True
                        break
                    sleep(2)
                    check_qty += 1
                #調用PMIS_RestApi同步這個任務
                taskno = f"{task['pid']}-{int(task['tid'])}-{int(task['taskid'])}"
                url = f"{settings.PMIS_REST_API_SERVER_NEW}/project/sync_one_task/"
                params = {"taskno":taskno}
                http_methods = {'data':{"url":url, "method":"POST","basic_auth_user":settings.PMIS_REST_API_USERNAME, "basic_auth_password":settings.PMIS_REST_API_PASSWORD, "params":params}}
                response_data = AsyncioTools.async_fetch_http_json(http_methods)['data']            
        except Exception as e:
            LOGGER.error(e)
        return response_data
            
