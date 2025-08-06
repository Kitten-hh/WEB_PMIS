from typing import Set

from timeago.parser import date_to_datetime
from DataBase_MPMS import models
from . BaseService import BaseService
from django.db.models import Count,Q,Case,Sum,When,IntegerField,Max
from django.db.models import F, ExpressionWrapper, fields
import json
import random
import math
import datetime
import timeago
from BaseApp.library.tools import DateTools
import re
import dateutil

class FrameService(BaseService):

    @staticmethod        
    def analysis_frames_qty(username, bdate, edate):
        bdate = DateTools.format(dateutil.parser.parse(bdate))
        edate = DateTools.format(dateutil.parser.parse(edate))
        qs = models.VDocmhMi.objects.values('mh001','mh003').filter(Q(modifier=username, modi_date__range=(bdate,edate)) | Q(creator=username, create_date__range=(bdate,edate))).distinct()\
            .aggregate(func_num=Count('*'), frame_num=Count('mh001',distinct=True))
        return qs


    
    @staticmethod        
    def search_frames_list(username, bdate, edate):
        str_sql = '''Select A.*,MH004 from ( 
                     SELECT MH003,MH001 FROM V_DOCMH_MI 
                    WHERE  ((MODIFIER = '%s' and MODI_DATE BETWEEN '%s' and '%s') OR (CREATOR = '%s' and CREATE_DATE  BETWEEN '%s' and '%s')) group by MH003,MH001) A 
                    inner join DOCMH B
                    on A.MH001 = B.MH001 and A.MH003 = B.MH003
                    inner join (Select * from DOCMA D where exists (Select Max(MA002) from DOCMA where MA001 = D.MA001)) F
                    on B.MH001=F.MA001 and B.MH002 = F.MA002'''
        if bdate:
            bdate = DateTools.format(dateutil.parser.parse(bdate))
        else:
            bdate = DateTools.addWeek(DateTools.now(), - 1)
        if edate:
            edate = DateTools.format(dateutil.parser.parse(edate))
        else:
            edate = DateTools.format(DateTools.now())
        str_sql = str_sql % (username, bdate, edate, username, bdate, edate)
        qs = models.VDocmhMi.objects.raw(str_sql)
        results = []
        for i in list(qs):
            results.append({key:value for key,value in i.__dict__.items() if key != '_state'})
        return results
    
    