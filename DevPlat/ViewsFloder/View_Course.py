from math import fabs
from django.shortcuts import render
from django.http import HttpRequest,JsonResponse
from BaseApp.library.cust_views.SWCreateView import SWCreateView
from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from BaseApp.library.cust_views.SWDeleteView import SWDeleteView
from DataBase_MPMS.models import Course, Mindmap
from django.db.models import Sum,Count,Max,Min,Avg,Q, query
from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
import logging
from BaseApp.library.tools import DateTools
from PMIS.Services.UserService import UserService

LOGGER = logging.Logger(__name__)


class CourseCreateView(SWCreateView):
    model = Course
    def get_initial(self, instance:Course):
        '''
        功能描述：Http Get 訪問時初始化model新增時的數據
        參數說明:
            instance:該model的實例
        '''
        self.set_max_seqno(instance)
        instance.sstatus = 'N'

    def set_max_seqno(self, instance:Course):
        '''
        功能描述：獲取最大單號
        參數說明:
            instance:需要保存或初始化的model實例
        '''
        qs = Course.objects.values("courseid").all().order_by('-courseid')[:1]
        if len(qs) > 0 :
            instance.courseid = qs[0]['courseid'] + 10
        else:
            instance.courseid = 10

    def save_supplement(self, instance:Course):
        '''
        功能描述:保存時設置默認值
        參數說明:
            instance:需要保存的model實例
        '''
        instance.create_date = DateTools.format(DateTools.now())
        instance.creator = UserService.GetLoginUserName(self.request)

class CourseUpdateView(SWUpdateView):
    model = Course

class CourseDeleteView(SWDeleteView):
    model = Course


class CourseTableView(DatatablesServerSideView):
    model = Course
    searchable_columns = ['subscription','category','sdescription','videolink','contact','remark']


    def get_initial_queryset(self): # xmm 2024-05-20加的可以根據文檔編號查詢對應的Course
        import re
        val = self.request.GET.get('search[value]')
        pattern = r'^[A-Za-z]{3}-[A-Za-z]{3}-\d{5}$'
        if re.match(pattern, val):
            local = self.request.GET.copy()
            if 'search[value]' in local:
                del local['search[value]']
            self.request.GET = local
            return Course.objects.filter(mindmapid__in=Mindmap.objects.filter(data__contains=val).values_list('inc_id'))
        return super().get_initial_queryset()