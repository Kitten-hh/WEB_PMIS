from typing import cast

from django.forms.models import model_to_dict
from DataBase_MPMS import models
from . BaseService import BaseService
from django.db.models import Count,Q,Case,Sum,When,IntegerField,Max
from django.db.models.functions import Lower
import json
import random
import re
import math
from  BaseProject.tools import DateTools
import timeago
import datetime
from django.http import HttpRequest,JsonResponse,HttpResponse
from django.core.cache import cache
from django.conf import settings
from BaseApp.library.tools import SWTools
from django.utils.translation import ugettext_lazy as _

class UserService(BaseService):
    group_name = '電腦部'
    local_dept = 'MIS'
    @staticmethod
    def getLocalPartUserCount(hasManager=False):
        rs = models.Users.objects.filter(groupname=UserService.group_name, dept=UserService.local_dept).aggregate(Count('username'))
        result = rs['username__count']
        if not hasManager and result > 2:
            result -= 2
        return result

    @staticmethod
    def getUserProjects(username=None):       
        q = Q()
        q.conditional = 'AND'
        if username:
            q.children.append(('contact', username))
        q.children.append(('planbdate__gte', datetime.date(datetime.datetime.now().year, 1, 1)))
        rs = models.VTaskRecordid.objects.filter(~Q(progress__in='CF') & ~Q(recordid__startswith='C') & q).\
            extra(where=["tid not like '%%5[257]' and tid not like '%%7[0-4][0-9]' and tid not like '%%3[0-4][0-9]' and \
            tid not like '%%9[0-4][0-9]' and not (Pid = '11580' and (tid ='28' or tid='21'))"]).\
             extra(select={'desc':'SubProject.ProjectName','deadline':'SubProject.PlanEDate'}, tables=['SubProject'], where=["V_Task_RecordId.recordid=SubProject.recordid"]).\
             values('recordid','desc', 'deadline').distinct()

        result = {}
        recordids = []
        for row in rs:
            recordid = row['recordid']
            title = row['desc']
            simple_title = ''
            if re.search('[a-zA-z]+', title):
                simple_title = re.search('[a-zA-z]+', title).group(0).upper()
                if len(simple_title) > 2:
                    simple_title = simple_title[:2]
            result[recordid] = {'title':row['desc'],'s_title':simple_title, 'progress':0, 'last_update':'','contacts':[], 'deadline':row['deadline'], 'no_complate':0}
            recordids.append(recordid)
        ##分析子工程的進度
        sub_rs = models.VTaskRecordid.objects.filter(Q(recordid__in=recordids)).\
        extra(where=["tid not like '%%5[257]' and tid not like '%%7[0-4][0-9]' and tid not like '%%3[0-4][0-9]' and \
            tid not like '%%9[0-4][0-9]' and not (Pid = '11580' and (tid ='28' or tid='21'))"]).\
        values('recordid').annotate(completed_qty=Sum(
            Case(
                When(progress__in='CF', then=1),
                default=0,
                output_field=IntegerField()
            )),
            task_qty=Count('pid'),
            last_update = Max('create_date')
        )
        for row in sub_rs:
            recordid = row['recordid']
            completed_qty = row['completed_qty']
            task_qty = row['task_qty']
            last_update = row['last_update']
            percent = math.ceil(completed_qty/task_qty * 100)
            try:
                last_update = last_update[:8]
                last_update = timeago.format(DateTools.parse(last_update), datetime.datetime.now())
            except Exception as e:
                print(str(e))
                last_update = ''
            result[recordid]['progress'] = percent
            result[recordid]['last_update'] = last_update
            result[recordid]['no_complate'] = task_qty - completed_qty
        ##分析參與子工程的聯繫人
        contacts_rs = models.VTaskRecordid.objects.filter(Q(recordid__in=recordids)).\
        extra(where=["tid not like '%%5[257]' and tid not like '%%7[0-4][0-9]' and tid not like '%%3[0-4][0-9]' and \
            tid not like '%%9[0-4][0-9]' and not (Pid = '11580' and (tid ='28' or tid='21'))"]).\
        values('recordid').annotate(contact_lower=Lower('contact')).distinct()
        for row in contacts_rs:
            recordid = row['recordid']
            contact = row['contact_lower']
            result[recordid]['contacts'].append(contact)
        return result

    @staticmethod    
    def GetAllUserNames():
        return [a['username'] for a in list(models.Users.objects.values('username'))]

    @staticmethod
    def GetLoginUserName(request:HttpRequest):
        username = request.user.username
        if username:
            return username
        else:
            return "sing"
            
    @staticmethod
    def GetPartUserNames():
        users = cache.get(settings.CACHES_NAME_PARTUSERNAME)
        if users:
            return users;
        rs = models.Users.objects.values('username').filter(groupname=UserService.group_name, dept=UserService.local_dept)
        users = [a['username'] for a in list(rs)]
        cache.set(settings.CACHES_NAME_PARTUSERNAME, users)
        return users

    @staticmethod
    def check_user(username:str, password:str):
        result = {'status':False, 'msg':'', 'data':None}
        try:
            qs =  models.Users.objects.filter(username=username)[:1]
            user = qs[0]
            if not password:
                password = ""
            if not user.password:
                user.password = ""
            password = SWTools.encrypt(password.strip())
            if user.password.strip() != password:
                result['msg'] = "密碼錯誤"
            else:
                result['status'] = True
                result['data'] = model_to_dict(user)
        except:
            result['msg'] = _("username is not exists")
        return result
