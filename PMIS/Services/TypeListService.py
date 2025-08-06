from DataBase_MPMS import models
from . BaseService import BaseService
from django.core.cache import cache
from django.conf import settings

class TypeListService(BaseService):
    def _get_typelist_from_syspara(self,type_name):
        rs = models.Syspara.objects.filter(ftype=type_name)
        if len(rs) > 0:
            return [{"label":param.fvalue, "value":param.nfield} for param in rs]
        else: 
            return []
    def _get_taskcategory_from_syspara(self):
        '''
        功能描述：從系統中獲取TaskCategory
        '''
        rs = models.Syspara.objects.filter(ftype='DevelopmentCycle', nfield='TaskCategoryType')
        if len(rs) > 0:
            value = rs[0].fvalue
            arr = value.split(";")
            return [{"label":param.split(':')[0] + ':' + param.split(':')[1], "value":param.split(':')[0]} for param in arr]
        else: 
            return []

    
    def _get_mettingsession_from_syspara(self):
        '''
        功能描述：從系統中獲取MettingSession
        '''
        rs = models.Syspara.objects.filter(nfield='default_session', ftype='metting')
        if len(rs) > 0:
            value = rs[0].fvalue
            return [{"label":value, "value":value}]
        else: 
            return []        

    @staticmethod
    def get_typelist(type_name):
        cache_name = "{0}_{1}".format(settings.CACHES_NAME_GLOBAL_TYPELIST, type_name)
        data = cache.get(cache_name)
        if data:
            return data;
        #默認從syspara中取得
        Service = TypeListService()
        if type_name == 'taskcategory':
            data = Service._get_taskcategory_from_syspara()
        elif type_name == 'mettingsession':
            data = Service._get_mettingsession_from_syspara()
        else:
            data = Service._get_typelist_from_syspara(type_name)
        cache.set(cache_name, data, timeout=60)
        return data