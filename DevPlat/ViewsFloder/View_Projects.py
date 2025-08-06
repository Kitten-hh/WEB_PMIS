from math import fabs
from django.db.models.expressions import F
from django.shortcuts import render
from django.http import HttpRequest,JsonResponse
from BaseApp.library.tools import DateTools
from PMIS.Services.SessionService import SessionService
from django.forms.models import model_to_dict
from DataBase_MPMS import models
import json
from django.db.models import Sum,Count,Max,Min,Avg,Q,Case,When,IntegerField
from django.db.models.functions import Concat
from django.db.models import Value
from django.core.serializers.json import DjangoJSONEncoder
import timeago
import datetime
import re

def search_project(request:HttpRequest):
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        user = request.GET.get("contact","")
        recordids = request.GET.get("recordids")
        projectname = request.GET.get("projectname","")
        period = "{0}-{1}".format(DateTools.formatf(DateTools.now(), '%Y'), DateTools.getQuarter(DateTools.now()))
        start_date, end_date = SessionService.get_quarterly_date(period)
        sessioni_filter = Q(progress='I') & ((Q(planbdate__gte=start_date) & Q(planbdate__lte=end_date)) |\
                (Q(planedate__gte=start_date) & Q(planedate__lte=end_date)) |\
                (Q(planbdate__lte=start_date) & Q(planedate__gte=end_date)))
        projects = models.VTasklistP.objects.values('recordid','projectscore','projectname','projectenddate').all()
        projects_recordid = models.VTasklistP.objects.values('recordid')
        if user:
            projects_recordid = projects_recordid.filter(allcontact__contains = '{0},'.format(user))        
        if recordids:
            recordids = recordids.split(",")
            projects_recordid = projects_recordid.filter(Q(recordid__in=recordids))
        else:
            projects_recordid = projects_recordid.filter(sessioni_filter)
        if projectname:
            projects_recordid = projects_recordid.filter(projectname__icontains=projectname)
        projects_recordid = projects_recordid.distinct()
        recordids = [item['recordid'] for item in projects_recordid]
        projects = projects.filter(Q(recordid__in=recordids))
        #projects = projects.filter(sessioni_filter)

        projects = projects.annotate(weight=Min('weight'),
                    task_qty=Sum('taskqty'),
                    complteed_qty=Sum('completedqty'),
                    last_update = Max('maxcreatedate')
                ).order_by('-projectscore','weight')
        
        data = []            
        for project in projects:
            if project['task_qty'] == 0:
                project['progress'] = 0
            else:
                project['progress'] = round(project['complteed_qty']/project['task_qty'] * 100,2)
            try:
                last_update = timeago.format(project['last_update'], datetime.datetime.now())
            except Exception as e:
                print(str(e))
                last_update = ''            
            project['last_update'] = last_update
            simple_title = ''
            title = project['projectname']
            if title == None:
                title = ''
            if re.search('[a-zA-z]+', title):
                simple_title = re.search('[a-zA-z]+', title).group(0).upper()
                if len(simple_title) > 2:
                    simple_title = simple_title[:2]
            project['s_title'] = simple_title
            if re.search(r'^\s*[^0-9]+', title):
                project['projectname'] = project['recordid'] +' ' + title
            project['username'] = user                
            data.append(project)
        '''
        if user:
            sessions = SessionService.search_sessioni(contact=None, recordid=None, period=period, allcontact=user, stype=None, desc=None)            
            records = list(dict.fromkeys([session['recordid'] for session in sessions]))
            data.sort(key=lambda x:records.index(x['recordid']))
        '''
        result['data'] = data
        result['status'] = True
    except Exception as e:
        print(str(e))
    return JsonResponse(result, safe=False)
    


def search_mustTasks(request:HttpRequest):
    '''
    功能描述：獲取對應Session的必做任務
    '''
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        recordid = request.GET.get('recordid')
        q = Q()
        q.conditional = 'AND'
        q.children.append(('taskcategory__in',['MF','MH']))
        q.children.append(('recordid',recordid))
        must_tasks = models.VTaskRecordid.objects.filter(q).order_by('planedate')

        AnalysisData = models.VTaskRecordid.objects.filter(q).values('recordid').annotate(
                    completed_qty=Sum(  
                    Case(    
                        When(progress__in='CF', then=1),
                        default=0,
                        output_field=IntegerField()
                    )),
                    task_qty=Count('pid'), 
                )
        result['status'] = True
        result['data'].append({'MustTasks':[model_to_dict(task) for task in must_tasks],'AnalysisData':list(AnalysisData)})
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)

def getProjectMindmap(request:HttpRequest):
    result = {'status':False, 'msg':'', 'data':""}
    try:
        recordid = request.GET.get('recordid',"")
        if recordid:
            qs = models.Mindmap.objects.values("inc_id").filter(data__contains=f"({recordid.strip()})").extra(tables=["MindMapType"], \
                where=["MindMap.TypeId = MindMapType.INC_ID and JSON_VALUE(CAST(Data AS NVARCHAR(max)), '$.nodeDataArray[0].text') LIKE %s"], params=[f"%({recordid.strip()})%"])
            if len(qs) > 0:
                result['data'] = qs[0]['inc_id']
                result['status'] = True;
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)

