from BaseApp.library.tools import SWTools,DateTools
from PMIS.Services.ActiveTaskService import ActiveTaskService
from PMIS.Services.UserService import UserService
from django.forms.models import model_to_dict
from django.db.models import Count,Q
from DataBase_MPMS.models import Syspara,VTask
from django.core.cache import cache
import time
import logging
from PMIS.Services.TemplateService import TemplateService

LOGGER = logging.getLogger(__name__)

class NotificationService(object):
    #當天需要發送的信息的緩存Key
    schedule_send_todayt_tasks_key="schedule_send_todayt_tasks_{0}".format(DateTools.format(DateTools.now()))
    schedule_send_class1_tasks_key="schedule_send_class1_tasks_{0}".format(DateTools.format(DateTools.now()))
    def send_todayt_tasks(self,receives):
        """
        功能描述：發送用戶當前T的任務
        """
        def get_tasks(username):
            service = ActiveTaskService()
            cycle_fixed_tasks = [model_to_dict(task) for task in service.get_today_cycle_fixed(username) if task.progress == 'T']
            today_fixed_tasks = [task for task in service.get_today_fixed_tasks(username) if task['progress'] == 'T']
            today_normal_tasks = []
            for i in range(3):
                try:
                    today_normal_tasks = [model_to_dict(task) for task in service.get_today_normal_task(username) if task.progress == 'T']
                    break
                except Exception as e:
                    time.sleep(5)
                    LOGGER.error(e)
            today_cycle_tasks = [model_to_dict(task) for task in service.get_today_cycle_task(username) if task.progress == 'T']
            today_tasks = []
            service.meger_task_dict(cycle_fixed_tasks, today_tasks)
            service.meger_task_dict(today_fixed_tasks, today_tasks)
            service.meger_task_dict(today_normal_tasks, today_tasks)
            service.meger_task_dict(today_cycle_tasks, today_tasks)
            return today_tasks
        def get_send_tasks():
            all_tasks = {}
            users = [user for user in UserService.GetPartUserNames() if user != 'sing']
            for user in users:
                tasks = get_tasks(user)
                all_tasks[user] = tasks
                time.sleep(5)
            send_tasks = []
            for user in users:
                if len(all_tasks[user]) > 0:
                    task = all_tasks[user][0]
                    task['send_receives'] = receives
                    task['send_flag'] = 'N'
                    send_tasks.append(task)
                    all_tasks[user].pop(0)
            return send_tasks
        tasks = get_send_tasks()
        cache.set(self.schedule_send_todayt_tasks_key, tasks, timeout=60 * 60 * 24) #過期時間為1天

    def schedule_send_message(self):
        def get_send_tasks():
            send_todayt_tasks = cache.get(self.schedule_send_todayt_tasks_key)
            if send_todayt_tasks:
                tasks = [item for item in send_todayt_tasks if item['send_flag'] == 'N']
                if len(tasks) > 0:
                    return {'todayt':tasks[0]}  #每次只發一條 
            send_class1_tasks = cache.get(self.schedule_send_class1_tasks_key)
            if send_class1_tasks:
                tasks = [item for item in send_class1_tasks if item['send_flag'] == 'N']
                if len(tasks) > 0:
                    return {'class1':tasks[0]}  #每次只發一條                                 
            return None
        send_task = get_send_tasks()
        if send_task:
            send_type = list(send_task.keys())[0]
            task = send_task[send_type]
            print("當前發送的任務是：{0}-{1} {2}".format(send_type, task['taskno'], task['task']))
            receives = task['send_receives']
            contact = task['contact'].strip()
            url = "http://183.63.205.83:8000/looper/staff_dashboard?username={0}&bdate={1}&edate={2}&dp=3".format(contact, 
            DateTools.formatf(DateTools.getBeginOfWeek(DateTools.now()), '%Y-%m-%d'),
            DateTools.formatf(DateTools.getEndOfWeek(DateTools.now()), '%Y-%m-%d'))
            if send_type == 'todayt':            
                title = "{0}'s today tasks".format(contact)
                cache_key = self.schedule_send_todayt_tasks_key
            elif send_type == 'class1':
                title = "{0}'s class1 tasks".format(contact)
                cache_key = self.schedule_send_class1_tasks_key
            else:
                title = "{0}'s tasks".format(contact)
                cache_key = None
            SWTools.pushMessage(receives, {"text":task['task'], "title":title, "ctype":"text", "url":url})
            if cache_key:
                data = cache.get(cache_key)
                for item in data:
                    if item['taskno'] == task['taskno']:
                        item['send_flag'] = 'Y'
                        break
                cache.set(cache_key, data, timeout=60 * 60 * 24) #過期時間為1天

    def send_first_last_class1(self, contact, receives):
        first_tasks = VTask.objects.filter(contact=contact,class_field=1).filter(~Q(progress='C') | ~Q(progress='F')).order_by('create_date')[:3]
        last_tasks = VTask.objects.filter(contact=contact,class_field=1).filter(~Q(progress='C') | ~Q(progress='F')).order_by('-create_date')[:3]
        tasks = list(set(first_tasks) | set(last_tasks))
        send_tasks = []
        for task in tasks:
            temp_task = model_to_dict(task)
            temp_task['send_receives'] = receives
            temp_task['send_flag'] = 'N'
            send_tasks.append(temp_task)
        cache.set(self.schedule_send_class1_tasks_key, send_tasks, timeout=60 * 60 * 24) #過期時間為1天

    def send_sing_today_flowup_contact(self, receives):
        tempService = TemplateService();
        users = tempService.getTodayFollowupUser()
        if users:
            url = "http://183.63.205.83:8000/looper/staff_dashboard?username={0}&bdate={1}&edate={2}&dp=3".format("sing", 
            DateTools.formatf(DateTools.getBeginOfWeek(DateTools.now()), '%Y-%m-%d'),
            DateTools.formatf(DateTools.getEndOfWeek(DateTools.now()), '%Y-%m-%d'))            
            SWTools.pushMessage(receives, {"text":"跟進"+",".join(users)+"的工程", "title":"Follow up the staff's project", "ctype":"text", "url":url})
    
    def send_todayt_tasks_now(self, task):
        cache_key = "sented_todayt_tasks_{0}".format(DateTools.format(DateTools.now()))
        exists_send_tasks = cache.get(cache_key)
        if not exists_send_tasks:
            exists_send_tasks = []        
        qs = Syspara.objects.values("nfield").filter(ftype="NotificationId")
        if len(qs) > 0:
            users = [item['nfield'] for item in qs]
            taskno =  '{0}-{1}-{2}'.format(task['pid'], int(task['tid']), int(task['taskid']))            
            if not taskno in exists_send_tasks:
                contact = task['contact'].strip()
                url = "http://183.63.205.83:8000/looper/staff_dashboard?username={0}&bdate={1}&edate={2}&dp=3".format(contact, 
                DateTools.formatf(DateTools.getBeginOfWeek(DateTools.now()), '%Y-%m-%d'),
                DateTools.formatf(DateTools.getEndOfWeek(DateTools.now()), '%Y-%m-%d'))
                SWTools.pushMessage(",".join(users), {"text":task['task'], "title":"{0}'s today tasks".format(contact), "ctype":"text", "url":url})
                exists_send_tasks.append(taskno)
        cache.set(cache_key, exists_send_tasks, timeout=60 * 60 * 24) #過期時間為1天
    
    def send_question(self, task, url):
        """
        功能描述：發送問題給所有人
        """
        qs = Syspara.objects.values("nfield").filter(ftype="NotificationId")
        if len(qs) > 0:
            users = [item['nfield'] for item in qs]
            SWTools.pushMessage(",".join(users), {"text":task['task'], "title":"{0}'s question".format(task['contact']), "ctype":"text", "url":url})
            #SWTools.pushMessage('hb', {"text":task['task'], "title":"{0}'s question".format(task['contact']), "ctype":"text", "url":url})