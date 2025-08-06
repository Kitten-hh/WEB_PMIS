from DataBase_MPMS import models
import logging
from django.db import connections
from django.db.models import Sum,Count,Max,Min,Avg,Q
from BaseApp.library.tools import DateTools
LOGGER = logging.Logger(__name__)
from django.core.cache import cache

class TemplateService:
    def getTodayFollowupUser(self):
        '''
        功能描述：獲取當天需要跟進的人
        '''
        cache_name = "{0}:{1}".format(__name__, self.getTodayFollowupUser.__name__)
        contacts = cache.get(cache_name)
        if contacts:
            return contacts
        else:
            try:
                contacts = []
                qs = models.Tpparam.objects.filter(pname='SingCheckStaff')
                if len(qs) > 0 and qs[0].ptype=='2':
                    strsql = qs[0].psql
                    with connections['MPMS'].cursor() as cursor:
                        cursor.execute(strsql)
                        row = cursor.fetchone()
                        if row and row[0]:
                            contacts = row[0].strip().split(',')
                            cache.set(cache_name, contacts, 60 * 60 *24)
            except Exception as e:        
                return contacts
            return contacts
