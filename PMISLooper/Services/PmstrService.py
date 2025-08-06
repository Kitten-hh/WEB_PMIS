from BaseApp.library.tools import SWTools,DateTools
from django.forms.models import model_to_dict
from django.db.models import Count,Q
from DataBase_MPMS.models import Syspara,VTask,Task,Pmstr
from django.core.cache import cache
import time
import logging
from operator import itemgetter
from BaseApp.library.tools import AsyncioTools,DateTools,ModelTools
from django.urls import reverse
from django import dispatch
from django.dispatch import receiver
from django.db import connections,transaction
import threading
from time import sleep
from django.utils.dateparse import parse_datetime
from django.conf import settings
import copy
import json

add_new_task_remind_singal = dispatch.Signal()

@receiver(add_new_task_remind_singal)
def add_new_task_remind_singal_callback(sender, **kwargs):
    task = kwargs.get("task")
    if task:
        taskObj = copy.deepcopy(task)
        taskObj = dict(taskObj) if type(taskObj) != dict else taskObj
        thread = threading.Thread(target=handel_add_new_task_remind_singal, args=(taskObj,))
        thread.start()    

def handel_add_new_task_remind_singal(task):
    service = PmstrService()
    service.add_new_task_remind(task)

class PmstrService:
    def getNewTaskSenders(self):
        """
        功能描述：獲取哪些聯繫人給其他人添加新任務時要添加提醒信息
        """
        cache_name = "{0}:{1}".format(__name__, self.getNewTaskSenders.__name__)
        senders = cache.get(cache_name)
        if senders:
            return senders
        else:
            senders = []          
            try:
                qs = Syspara.objects.values("fvalue").filter(ftype="Notification", nfield="NewTaskSenders")
                if len(qs) > 0:
                    senders = qs[0]['fvalue'].strip().split(",")
                    cache.set(cache_name, senders, timeout=60 * 60 * 24) #過期時間為1天    
            except Exception as e:
                LOGGER.error("獲取哪些聯繫人給其他人添加新任務時要添加提醒信息的人員失敗，請檢查系統參數，ftype:Notification nfield:NewTaskSenders")
            return senders
    def add_new_task_remind(self, task):
        maxTr001 = 1
        qs = Pmstr.objects.all().order_by('-tr001')[:1]
        if len(qs) > 0:
            maxTr001 = qs[0].tr001 + 1
        tr001 = maxTr001
        tr002 = "{0}-{1}-{2}".format(task['pid'], int(task['tid']), int(task['taskid']))
        tr003 = task['progress']
        tr004 = DateTools.now().replace(hour=8, minute=0,second=0,microsecond=0)
        tr005 = DateTools.now().replace(hour=17, minute=0, second=0, microsecond=0)
        tr006 = task['contact']
        tr007 = 'N' #默認為等待發送
        tr011 = '1,2,3,4,5,6' #星期設置
        tr024 = 60 #循環周期數， 按分鐘記
        tr027 = 'Y' #發送消息
        tr028 = "2" #提醒開始，默認為：開始於計畫開始前
        tr029 = 0 #默認為0天前
        tr030 = "3" #提醒結束，默認為:用戶點擊I Know結束
        with transaction.atomic(ModelTools.get_database(Pmstr)):            
            Pmstr.objects.filter(tr002=tr002).delete()
            Pmstr.objects.update_or_create(tr002=tr002, tr006=tr006, 
                defaults={'tr001':tr001,'tr003':tr003, 'tr004':tr004, 'tr005':tr005,'tr006':tr006,'tr007':tr007,'tr011':tr011,
                'tr024':tr024, 'tr027':tr027, 'tr028':tr028, 'tr029':tr029, 'tr030':tr030})