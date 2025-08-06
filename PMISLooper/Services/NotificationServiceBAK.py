from BaseApp.library.tools import SWTools,DateTools
from PMIS.Services.ActiveTaskService import ActiveTaskService
from PMIS.Services.UserService import UserService
from django.forms.models import model_to_dict
from DataBase_MPMS.models import Syspara
from django.core.cache import cache
import time

class NotificationService(object):
    def send_todayt_tasks(self,receives):
        """
        功能描述：發送用戶當前T的任務
        """
        def get_tasks(username):
            service = ActiveTaskService()
            cycle_fixed_tasks = [model_to_dict(task) for task in service.get_today_cycle_fixed(username) if task.progress == 'T']
            today_fixed_tasks = [model_to_dict(task) for task in service.get_today_fixed_tasks(username) if task.progress == 'T']
            today_normal_tasks = [model_to_dict(task) for task in service.get_today_normal_task(username) if task.progress == 'T']
            today_cycle_tasks = [model_to_dict(task) for task in service.get_today_cycle_task(username) if task.progress == 'T']
            today_tasks = []
            service.meger_task_dict(cycle_fixed_tasks, today_tasks)
            service.meger_task_dict(today_fixed_tasks, today_tasks)
            service.meger_task_dict(today_normal_tasks, today_tasks)
            service.meger_task_dict(today_cycle_tasks, today_tasks)
            return today_tasks
        def get_send_tasks():
            cache_key = "required_sent_todayt_tasks_{0}".format(DateTools.format(DateTools.now()))
            send_tasks = cache.get(cache_key)            
            if send_tasks:
                return send_tasks
            else:
                all_tasks = {}
                users = [user for user in UserService.GetPartUserNames() if user != 'sing']
                for user in users:
                    tasks = get_tasks(user)
                    all_tasks[user] = tasks
                    time.sleep(5)
                send_tasks = []
                for user in users:
                    if len(all_tasks[user]) > 0:
                        send_tasks.append(all_tasks[user][0])
                        all_tasks[user].pop(0)
                cache.set(cache_key, send_tasks, timeout=60 * 60 * 24) #過期時間為1天
                return send_tasks

        #users = [user for user in UserService.GetPartUserNames() if user in ['hb','qfq','lsy']]
        cache_key = "sented_todayt_tasks_{0}".format(DateTools.format(DateTools.now()))
        exists_send_tasks = cache.get(cache_key)
        if not exists_send_tasks:
            exists_send_tasks = []
        send_tasks = get_send_tasks()
        current_send_tasks = [item for item in send_tasks if not item['taskno'] in exists_send_tasks]
        if len(current_send_tasks) > 0:
            task = current_send_tasks[0] #每只發一條，為了測試FCM多少時間發一條可以收到
            ##for task in [item for item in tasks if not item['taskno'] in exists_send_tasks]:
            contact = task['contact'].strip()
            url = "http://183.63.205.83:8000/looper/staff_dashboard?username={0}&bdate={1}&edate={2}&dp=3".format(contact, 
            DateTools.formatf(DateTools.getBeginOfWeek(DateTools.now()), '%Y-%m-%d'),
            DateTools.formatf(DateTools.getEndOfWeek(DateTools.now()), '%Y-%m-%d'))
            SWTools.pushMessage(receives, {"text":task['task'], "title":"{0}'s today tasks".format(contact), "ctype":"text", "url":url})
            #SWTools.pushMessage(receives, {"text":task['task'], "title":"{0}'s today tasks".format(contact), "ctype":"text"})
            exists_send_tasks.append(task['taskno'])
            cache.set(cache_key, exists_send_tasks, timeout=60 * 60 * 24) #過期時間為1天
    
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