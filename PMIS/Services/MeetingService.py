from django.db.models import Count,Q,Case,Sum,When,IntegerField,Max
from DataBase_MPMS import models
from django.core.cache import cache
from django.forms.models import model_to_dict
from BaseApp.library.tools import DateTools
from PMIS.Services.TaskService import TaskService
import logging
LOGGER = logging.Logger(__name__)

class MeetingService(object):
    """
    功能描述：提供Meeting相關的一些服務
    """
    def getOutstandingPMeeting(self,contact):
        """
        功能描述：獲取用戶脫期的優先級P的Meeting
        """
        session = self.getMeetingDefaultSession()
        meeting_qs = models.Task.objects.all()
        if session:
            meeting_qs = meeting_qs.filter(pid=session['pid'], tid = session['tid'])
        meeting_qs = meeting_qs.filter(contact = contact, hoperation='P', editionid=3).filter(~Q(progress='C') & ~Q(progress='F'))
        meeting_qs = meeting_qs.extra(select={'taskno':"CONVERT(Varchar(10), Pid) + '-' + CONVERT(Varchar(20), CONVERT(Decimal(18, 0), Tid)) + '-' + CONVERT(Varchar(10), CONVERT(Decimal(18, 0), TaskID))"})
        qs = models.VTaskMeeting.objects.filter(relationid__in=meeting_qs.values('taskno')).filter(contact=contact).filter(~Q(progress='C') & ~Q(progress='F')).values()
        finish_qs = models.Task.objects.filter(contact=contact, edate__date=DateTools.now(), hoperation='P')
        finish_qs = TaskService.getRequestQuerySetWithSysparam(finish_qs)
        ##取得未分配的meeting
        result = list(qs)
        result.extend([model_to_dict(task) for task in finish_qs])
        tasknos = [task['relationid'] for task in result]
        meeting = [task for task in meeting_qs.values() if not task['taskno'] in tasknos]
        result.extend(meeting)
        result.sort(key=lambda x:(x['create_date']))
        for task in result:
            task['task'] = "【{0}】{1}".format('' if not task['udf04'] else task['udf04'],task['task'])
            task['taskno'] = "{0}-{1}-{2}".format(task['pid'],int(task['tid']), int(task['taskid']))
        return result

    def getMeetingDefaultSession(self):
        cache_name = "{0}:{1}".format(__name__, self.getMeetingDefaultSession.__name__)
        session = cache.get(cache_name)
        if session:
            return session
        else:
            session = {}
            try:
                qs = models.Syspara.objects.filter(nfield='default_session', ftype='metting')
                if len(qs) > 0:
                    fvalue = qs[0].fvalue
                    fvalue_arr = fvalue.split('-')
                    session = {'pid':fvalue_arr[0], 'tid':fvalue_arr[1]}
                    cache.set(cache_name, session, timeout=60*60*24) #緩存一天
            except Exception as e:
                LOGGER.error("請設置Meeting的系統，ftype:meeting nfield:default_session")
            return session
        
                



        