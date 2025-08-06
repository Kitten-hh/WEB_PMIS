from DataBase_MPMS import models
from . BaseService import BaseService
from . TaskService import TaskService
from django.db.models import Count,Q
class ProjectService(BaseService):

    @staticmethod
    def getFixdProjects(username=None,bdate=None,edate=None):
        '''
        功能描述：獲取用戶或所有用戶的重要工程，及工程中含有Fixed Day類型的任務
        '''
        q = Q()
        q.conditional = 'AND'
        if username:
            q.children.append(('contact', username))
        if bdate:
            q.children.append(('planbdate__gte', bdate))
        if edate:
            q.children.append(('planedate__lte', edate))
        #rs = models.VTaskRecordid.objects.filter(~Q(progress__in='CF') &  Q(hoperation='F') & q).values('recordid').distinct().aggregate(Count('recordid'))
      
        rs = models.VTaskRecordid.objects.filter(~Q(progress__in='CF')  & q)
        rs = TaskService.getRequestQuerySetWithSysparam(rs)
        rs = rs.values('recordid').distinct().aggregate(Count('recordid'))
        print(rs)
        return rs['recordid__count']