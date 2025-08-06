from math import fabs
from django.shortcuts import render
from django.http import HttpRequest,JsonResponse
from BaseApp.library.cust_views.SWCreateView import SWCreateView
from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from BaseApp.library.cust_views.SWDeleteView import SWDeleteView
from DataBase_MPMS.models import Ruledoc
from django.db.models import Sum,Count,Max,Min,Avg,Q, query
from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
import logging
from BaseApp.library.tools import DateTools
from PMIS.Services.UserService import UserService

LOGGER = logging.Logger(__name__)


class RuledocCreateView(SWCreateView):
    model = Ruledoc
    def get_initial(self, instance:Ruledoc):
        '''
        功能描述：Http Get 訪問時初始化model新增時的數據
        參數說明:
            instance:該model的實例
        '''
        instance.recordid = self.request.GET.get("recordid");
        self.set_max_seqno(instance)
        instance.sstatus = 'N'

    def set_max_seqno(self, instance:Ruledoc):
        '''
        功能描述：獲取最大單號
        參數說明:
            instance:需要保存或初始化的model實例
        '''
        qs = Ruledoc.objects.values("itemno").filter(recordid=instance.recordid).order_by('-itemno')[:1]
        if len(qs) > 0 :
            instance.itemno = qs[0]['itemno'] + 10
        else:
            instance.itemno = 10

class RuledocUpdateView(SWUpdateView):
    model = Ruledoc

class RuledocDeleteView(SWDeleteView):
    model = Ruledoc


class RuledocTableView(DatatablesServerSideView):
    model = Ruledoc
    searchable_columns = ['recordid','itemno','topic','sdescription','content','sortno']
