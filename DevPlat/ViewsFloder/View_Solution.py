from math import fabs
from django.shortcuts import render
from django.http import HttpRequest,JsonResponse
from BaseApp.library.cust_views.SWCreateView import SWCreateView
from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from BaseApp.library.cust_views.SWDeleteView import SWDeleteView
from DataBase_MPMS.models import Solutiontype
from django.db.models import Sum,Count,Max,Min,Avg,Q, query
from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
import logging
from BaseApp.library.tools import DateTools
from PMIS.Services.UserService import UserService
from django.db.models.functions import Cast, Substr
from django.db.models import IntegerField

LOGGER = logging.Logger(__name__)


class SolutionTypeCreateView(SWCreateView):
    model = Solutiontype
    def get_initial(self, instance:Solutiontype):
        '''
        功能描述：Http Get 訪問時初始化model新增時的數據
        參數說明:
            instance:該model的實例
        '''
        self.set_max_seqno(instance)
        instance.sstatus = 'N'

    def set_max_seqno(self, instance:Solutiontype):
        '''
        功能描述：獲取最大單號
        參數說明:
            instance:需要保存或初始化的model實例
        '''
        qs = Solutiontype.objects.annotate(istid=Cast('stid', output_field=IntegerField())).values("istid").all().order_by('-istid')[:1]
        if len(qs) > 0 :
            instance.stid = str(int(qs[0]['istid']) + 10)
        else:
            instance.stid = '10'

    def save_supplement(self, instance:Solutiontype):
        '''
        功能描述:保存時設置默認值
        參數說明:
            instance:需要保存的model實例
        '''
        instance.create_date = DateTools.format(DateTools.now())
        instance.creator = UserService.GetLoginUserName(self.request)
        instance.contact = self.request.POST.get("contact", UserService.GetLoginUserName(self.request))

class SolutionTypeUpdateView(SWUpdateView):
    model = Solutiontype

class SolutionTypeDeleteView(SWDeleteView):
    model = Solutiontype


class SolutionTypeTableView(DatatablesServerSideView):
    model = Solutiontype