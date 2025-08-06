from DataBase_MPMS import models
from PMIS.Services.BaseService import BaseService
from django.db.models import Count,Q,Case,Sum,When,IntegerField,Max
from django.db.models import F, ExpressionWrapper, fields
import json
import random
import math
import datetime
import timeago
from BaseApp.library.tools import DateTools
import re
from django.db import connections
from BaseApp.library.tools import DateTools

class ProjectManagementService(BaseService):
    
    @staticmethod
    def get_quarterly_list():
        '''
        功能描述:獲取當前季度及前兩個季度和後兩個季度
        '''
        step_array = [-2,-1,0,1,2]
        quarterlies = []
        cur_quarterly = None
        for step in step_array:
            quarter_date = DateTools.getSeasonFirstTime(step)
            quarterly_str = '{0}-{1}'.format(DateTools.formatf("%y"), DateTools.getQuarter(quarter_date))
            if step == 0:
                cur_quarterly = quarterly_str
            quarterlies.append(quarterly_str)
        return cur_quarterly, quarterlies

    @staticmethod
    def get_cur_quarterly():
        quarter_date = DateTools.getSeasonFirstTime(0)
        quarterly_str = '{0}-{1}'.format(DateTools.formatf("%y"), DateTools.getQuarter(quarter_date))
        return quarterly_str
