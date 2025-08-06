from operator import mod
from sqlite3 import Date
from django.core.serializers.json import DjangoJSONEncoder
import json
from datatableview import Datatable
from django.db import connections
from datatableview.views import MultipleDatatableView
from datatableview.views.legacy import LegacyDatatableView
from datatableview import helpers
from django.middleware.gzip import GZipMiddleware
import random
import pytz
from BaseProject.CustomBaseObject.base_views.CustomView import CustomUpdateView
from BaseProject.tools import DateTools
from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
from BaseApp.library.cust_views.SWCreateView import SWCreateView
from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from BaseApp.library.cust_views.SWDeleteView import SWDeleteView
from django.core.cache import cache
from django.conf import settings
from DataBase_MPMS import models
import time
import datetime
import copy
import re
import base64
from base64 import b64encode
from django.db import transaction
from django.db.models import Count,Q,F,Case,Sum,When,IntegerField,Max
from django.http import JsonResponse,HttpResponse,HttpRequest
from time import sleep


#獲取會議詳細信息
def get_metting_item(request:HttpRequest):
    '''
    功能描述：獲取一個metting的metting_item
    '''
    #
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        strid = request.GET.get('id')
        subject = request.GET.get('subject')
        status  = request.GET.get('status')
        if (strid and subject) or (status and strid):
            if status == 'Browse' and strid:
                meeting_items = models.Task.objects.filter(docpath=strid,editionid='1').order_by('editionid','rank').values()
            else:
                meeting_items = models.Task.objects.filter(docpath=strid,editionid='1',inc_id=subject).order_by('editionid','rank').values()
            for item in meeting_items:
                data = {}
                data.setdefault('subjects', []).append(item)
                relationid = item['pid']+'-'+str(int(item['tid']))+'-'+str(int(item['taskid']))
                other_meeting_items = models.Task.objects.filter(docpath=strid,relationid=relationid).order_by('editionid','rank').values()
                for other_item in other_meeting_items:
                    if other_item['editionid']=='3':
                        data.setdefault('conclusions', []).append(other_item)
                    elif other_item['editionid']=='4':
                        data.setdefault('arranges', []).append(other_item)
                result['data'].append(data)
            result['status'] = True  
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   

#獲取會議樹狀圖
def get_metting_tree(request:HttpRequest):
    '''
    功能描述：獲取metting的樹狀圖
    '''
    #
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        strdate = request.GET.get('date')
        if (not strdate) or (not strdate.isdigit()):
            strdate = time.strftime("%Y%m%d", time.localtime())[2:]
        TreeList = [] 
        mettings = models.Mettingmaster.objects.filter(id__contains=strdate).values()
        for metting in mettings:
            if metting['topic']=='' or metting['topic']==None:
                metting['topic'] = '未命名會議主題'
            meeting_items = models.Task.objects.filter(docpath=metting['id'])
            childrenlist = Getmettingchildren(metting,meeting_items)
            #獲取對應會議的結論數量
            meeting_items_finish = meeting_items.filter(progress__in=['C','F']).values()
            meeting_items = meeting_items.filter(editionid='3').values()
            analysis ='({0}/{1})'.format(len(meeting_items_finish),len(meeting_items))
            TreeList.append({'icon': "",'name': metting['id']+analysis,'children': childrenlist,'inc_id':metting['inc_id'],'strid':metting['id'].replace(' ',''),'sub_inc_id':'','tier':'0'})   
        result['data'] = TreeList
        result['status'] = True  
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   

#獲取會議的會議信息、議題、附件內容 
def Getmettingchildren(metting_item,metting_sub_items):
    TreeList = []
    metting_mes_list = []
    metting_sub_list = []
    metting_acc_list = []

    #會議議題
    metting_sub_items = metting_sub_items.filter(editionid='1').order_by('editionid','taskid').values()
    for metting_sub_item in metting_sub_items:
        if metting_sub_item['task']=='' or metting_sub_item['task']==None:
            metting_sub_item['task'] = '未命名議題'
        metting_sub_list.append({'icon': "",'name': metting_sub_item['task'],'children': [],'inc_id':metting_item['inc_id'],'strid':metting_item['id'].replace(' ',''),'sub_inc_id':metting_sub_item['inc_id'],'tier':'2'})

    
    # TreeList.append({'icon': "",'name': '會議信息','children': metting_mes_list,'inc_id':metting_item['inc_id'],'strid':metting_item['id'].replace(' ',''),'sub_inc_id':'','tier':'1'})
    # TreeList.append({'icon': "",'name': '會議議題','children': metting_sub_list,'inc_id':metting_item['inc_id'],'strid':metting_item['id'].replace(' ',''),'sub_inc_id':'','tier':'1'})
    # TreeList.append({'icon': "",'name': '會議附件','children': metting_acc_list,'inc_id':metting_item['inc_id'],'strid':metting_item['id'].replace(' ',''),'sub_inc_id':'','tier':'1'})
    return metting_sub_list


#獲取會議未完成的結論
def get_metting_undone(request:HttpRequest):
    '''
    功能描述：獲取前八天未完成的結論
    '''
    #
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        search_dec = request.GET.get('search_dec')
        search_metid = request.GET.get('search_metid')
        search_pro = request.GET.get('search_pro')
        search_dis = request.GET.get('search_dis')
        search_con = request.GET.get('search_con')
        search_hop = request.GET.get('search_hop')
        
        resultData = {'master':[],'detail':[]}
        
        if search_dis==None or search_dis=='':
           search_dis='3' 
        strf_time = ((datetime.datetime.now())+datetime.timedelta(days= -8)).strftime("%Y%m%d")[-6:]
        #過去八天所有會議記錄
        if search_dis=='5' and (search_hop==None or search_hop=='') and (search_metid==None or search_metid=='') and (search_dec==None or search_dec=='') and (search_pro==None or search_pro=='') and (search_con==None or search_con==''):
            q = Q()
            q.connector = "and"
            q.children.append(("docpath__gte",strf_time))
            q.children.append(("editionid",'3'))
            meeting_items = models.Task.objects.filter(q).values()
            resultData['detail']=list(meeting_items)
            for meeting_item in resultData['detail']:
                meeting_item['planbdate'] = meeting_item['planbdate'].strftime('%Y-%m-%d')
                meeting_item['planedate'] = meeting_item['planedate'].strftime('%Y-%m-%d')
            meetingData = models.Mettingmaster.objects.filter(id__gte=strf_time).values()
            for meeting in meetingData:
                analysisData = analysis_meeting_data(meeting['id'])
                if meeting['participants']:
                    meeting['participants'] = meeting['participants'].split(",")
                resultData['master'].append({'analysisData':analysisData,'meetingData':meeting}) 
        else:    
            if search_dis=='5':
                search_dis='3'   
            #會議結論條件
            meetingid_list = []
            q2 = Q()
            q2.connector = "and"    
            q2.children.append(("editionid",'3'))
            #結論內容
            if search_dec!=None and search_dec!='':
                q2.children.append(("task__contains",search_dec))
            #已完成
            if search_pro!=None and search_pro=='1':
                q2.children.append(('process__in','CF'))
            #聯繫人
            if search_con!=None and search_con!='':  
                q2.children.append(("contact",search_con))  
            if search_hop!=None and search_hop!='':
                q2.children.append(("hoperation",search_hop))  
            if search_metid==None or search_metid=='':
                q2.children.append(("docpath__gte",strf_time))
            else:
                q2.children.append(("docpath__contains",search_metid))
            met_q = copy.deepcopy(q2)
            meeting_items = models.Task.objects.filter(q2).values()
            for metting_item in meeting_items:
                session_id = metting_item['pid']+'-'+str(int(metting_item['tid']))+'-'+str(int(metting_item['taskid']))
                metting_relationtask = models.Task.objects.filter(Q(relationid=session_id) & ~Q(editionid__in =['1','2','3'])).values()
                #已分配任務未完成的會議 
                if metting_relationtask.exists() and search_dis == '1':
                    if metting_relationtask[0]['progress'] not in ['C','F']:
                        metting_item['planbdate'] = metting_item['planbdate'].strftime('%Y-%m-%d')
                        metting_item['planedate'] = metting_item['planedate'].strftime('%Y-%m-%d')
                        resultData['detail'].append(metting_item)
                        if metting_item['docpath'] not in meetingid_list:
                            meetingid_list.append(metting_item['docpath'])
                    #已分配已完成的會議
                    elif (search_dis == '1') and (search_pro=='1'):
                        metting_item['planbdate'] = metting_item['planbdate'].strftime('%Y-%m-%d')
                        metting_item['planedate'] = metting_item['planedate'].strftime('%Y-%m-%d')
                        resultData['detail'].append(metting_item)
                        if metting_item['docpath'] not in meetingid_list:
                            meetingid_list.append(metting_item['docpath'])
                #未分配任務的會議 
                elif (not metting_relationtask.exists() ) and (search_dis == '0') and metting_item['progress'] not in ['C','F']:
                    metting_item['planbdate'] = metting_item['planbdate'].strftime('%Y-%m-%d')
                    metting_item['planedate'] = metting_item['planedate'].strftime('%Y-%m-%d')
                    resultData['detail'].append(metting_item)
                    if metting_item['docpath'] not in meetingid_list:
                        meetingid_list.append(metting_item['docpath'])
                #未分配任務或未完成的會議 
                elif search_dis == '3':
                    if (metting_item['progress'] not in ['C','F']) and ((not metting_relationtask.exists() ) or (metting_relationtask[0]['progress'] not in ['C','F'])):
                        metting_item['planbdate'] = metting_item['planbdate'].strftime('%Y-%m-%d')
                        metting_item['planedate'] = metting_item['planedate'].strftime('%Y-%m-%d')
                        resultData['detail'].append(metting_item) 
                    if metting_item['docpath'] not in meetingid_list:
                        meetingid_list.append(metting_item['docpath'])
                #未完成的優先處理任務
                elif search_dis == '4':
                    if (metting_item['progress'] not in ['C','F']) and (metting_item['hoperation'] == 'P') and ((not metting_relationtask.exists() ) or (metting_relationtask[0]['progress'] not in ['C','F'])):
                        metting_item['planbdate'] = metting_item['planbdate'].strftime('%Y-%m-%d')
                        metting_item['planedate'] = metting_item['planedate'].strftime('%Y-%m-%d')
                        resultData['detail'].append(metting_item) 
                        if metting_item['docpath'] not in meetingid_list:
                            meetingid_list.append(metting_item['docpath'])
            meetingData = models.Mettingmaster.objects.filter(id__in=meetingid_list).values()
            for meeting in meetingData:
                analysisData = analysis_meeting_data(meeting['id'])
                if meeting['participants']:
                    meeting['participants'] = meeting['participants'].split(",")
                resultData['master'].append({'analysisData':analysisData,'meetingData':meeting})                 
        result['data'].append(resultData)                 
        result['status'] = True  
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   



#保存會議文件
def save_met_file(request:HttpRequest):
    '''
    功能描述：保存會議文件
    '''
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        parentid = 120
        folderid = 1
        task_inc_id = request.POST.get('task_inc_id')
        filesize = request.POST.get('filesize')
        filename = request.POST.get('filename')
        filetype = filename.split('.')
        filetype = filetype[len(filetype)-1]
        file = request.POST.get('file')
        file=base64.b64decode(file.split(',')[1])    
        task = models.Task.objects.filter(inc_id=task_inc_id).values()
        if len(task) > 0:
            parentid = int(task[0]['tid'])
        documentdata = models.Document.objects.filter(parentid=parentid).values('folderid').aggregate(Max('folderid'))['folderid__max'] 
        if not (documentdata == None):   
            folderid = documentdata+1

        document = models.Document()
        document.parentid = parentid
        document.folderid = folderid
        document.foldername = task[0]['pid']+'-'+str(int(task[0]['tid']))+'-'+str(int(task[0]['taskid']))
        document.docid = task[0]['pid']+str(int(task[0]['tid']))+str(int(task[0]['taskid']))
        document.docname = filename
        document.docsize = filesize
        document.mediatype = filetype
        document.revisedby = task[0]['contact']
        document.t_stamp = datetime.datetime.now()
        document.save()
        docdetail = models.Docdetail()
        docdetail.parentid = parentid
        docdetail.folderid = folderid
        docdetail.revisedby = task[0]['contact']
        docdetail.t_stamp = datetime.datetime.now()
        docdetail.content = file
        docdetail.save()
        result['status'] = True  
        
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   

#統計會議信息
def analysis_meeting(request:HttpRequest):
    '''
    功能描述：統計會議信息
    '''
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        strid = request.GET.get('id')
        analysisData = analysis_meeting_data(strid)
        result['data'].append(analysisData) 
        result['status'] = True  
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   


def analysis_meeting_data(meetingID):
    #對相應的會議進行統計
    analysisData = {
        'conclusion_con':0,'finish_con':0,'assigning_con':0,'undistributed_con':0,'finish_task_con':0,'unfinish_task_con':0,
        'assigning_ratio':0,'undistributed_ratio':0,'finish_task_ratio':0,'unfinish_task_ratio':0,
    }
    #會議結論條件
    q2 = Q()
    q2.connector = "and"    
    q2.children.append(("editionid",'3'))
    q2.children.append(("docpath__contains",meetingID.strip()))
    num = 0
    met_q = copy.deepcopy(q2)
    meeting_items = models.Task.objects.filter(met_q).values()
    #當前會議的結論總數 
    analysisData['conclusion_con'] = len(meeting_items)
    for metting_item in meeting_items:
        #已完成的會議 
        if metting_item['progress'] =='C' or metting_item['progress']=='F':
            analysisData['finish_con']+=1
        session_id = metting_item['pid']+'-'+str(int(metting_item['tid']))+'-'+str(int(metting_item['taskid']))
        metting_relationtask = models.Task.objects.filter(Q(relationid=session_id) & ~Q(editionid__in =['1','2','3'])).values()
        #已分配任務的會議 
        if metting_relationtask.exists():
            analysisData['assigning_con']+=1
            #已分配任務並完成的會議 
            for metting_relation in metting_relationtask:
                if metting_relation['progress']=='C' or metting_relation['progress']=='F':
                    analysisData['finish_task_con']+=1
                else:
                    analysisData['unfinish_task_con']+=1
        #未分配任務的會議 
        else:
            analysisData['undistributed_con']+=1
    if analysisData['conclusion_con']>0:
        analysisData['assigning_ratio'] = int(analysisData['assigning_con']/analysisData['conclusion_con']*100)
        analysisData['undistributed_ratio'] = int(analysisData['undistributed_con']/analysisData['conclusion_con']*100)
        analysisData['finish_task_ratio'] = int(analysisData['finish_task_con']/analysisData['conclusion_con']*100)
        analysisData['unfinish_task_ratio'] = int(analysisData['unfinish_task_con']/analysisData['conclusion_con']*100)
    return analysisData


#獲取會議信息和統計信息
def search_meeting(request:HttpRequest):
    '''
    功能描述：獲取會議信息和統計信息
    '''
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        strid = request.GET.get('id')
        search_dec = request.GET.get('search_dec')
        strf_time = ((datetime.datetime.now())+datetime.timedelta(days= -8)).strftime("%Y%m%d")[-6:]
        con = Q()
        q = Q()
        q2 = Q()
        q.connector = "and"
        if not strid:
            q.children.append(("id__gte",strf_time))
        else:   
            q.children.append(("id__contains",strid))
        if search_dec:
            q2.connector = "or"
            q2.children.append(("summary__contains",search_dec))
            q2.children.append(("discussprocess__contains",search_dec))
            con.add(q2,'and')
        con.add(q,'and')
        meetingData = models.Mettingmaster.objects.filter(con).values()
        for meeting in meetingData:
            analysisData = analysis_meeting_data(meeting['id'])
            if meeting['participants']:
                meeting['participants'] = meeting['participants'].split(",")
            result['data'].append({'analysisData':analysisData,'meetingData':meeting}) 
        result['status'] = True  
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   






















class MettingmasterView(DatatablesServerSideView):
    model = models.Mettingmaster
    columns = "__all__"
    searchable_columns = ['id','topic','participants','mustread','inc_id']

class MettingmasterCreateView(SWCreateView):
    model = models.Mettingmaster        

    def get_initial(self, instance):
        '''
        功能描述：Http Get 訪問時初始化model新增時的數據
        參數說明:
            instance:該model的實例
        '''
        self.set_max_seqno(instance)
    
    def set_max_seqno(self, instance):
        '''
        功能描述：獲取最大單號
        參數說明:
            instance:需要保存或初始化的model實例
        '''
        strf_time = time.strftime("%Y%m%d", time.localtime())[2:]
        strid = models.Mettingmaster.objects.filter(id__startswith=strf_time).values('id').aggregate(Max('id'))['id__max'] 
        if strid == None:   
            instance.id = strf_time+'01'
        else:
            instance.id = str(int(strid)+1)

    def save_other(self, instance):
        '''
        功能描述：保存與該model相關的其他model數據
        參數說明:
            instance:本model實例
        '''
        modaldata = self.model.objects.get(inc_id = instance.inc_id)
        instance.summary = modaldata.summary
        instance.discussprocess = modaldata.discussprocess
        if self.request.POST.get("details"):
            details = json.loads(self.request.POST.get("details"))[0]
            strkeys = list(details.keys())
            session_id = None
            #優先保存議題內容
            if not details['subjects'][0]['inc_id']:    
                strkeys.remove('subjects')
                details['subjects'] = createTask(details['subjects'],None)  
            
            if details['subjects'][0]['inc_id']:    
                session_id = details['subjects'][0]['pid']+'-'+str(int(details['subjects'][0]['tid']))+'-'+str(int(details['subjects'][0]['taskid']))

            #保存或修改其他內容
            for strkey in strkeys:
                details[strkey] = batchUpdateTask(details[strkey],session_id)
            for strkey in strkeys:
                details[strkey] = createTask(details[strkey],session_id)
            return details

class MettingmasterUpdateView(SWUpdateView):
    model = models.Mettingmaster   

    def save_other(self, instance):
        '''
        功能描述：保存與該model相關的其他model數據
        參數說明:
            instance:本model實例
        '''
        
        modaldata = self.model.objects.get(inc_id = instance.inc_id)
        instance.summary = modaldata.summary
        instance.discussprocess = modaldata.discussprocess
        if self.request.POST.get("details"):
            details = json.loads(self.request.POST.get("details"))[0]
            strkeys = list(details.keys())
            session_id = None
            #優先保存議題內容
            if not details['subjects'][0]['inc_id']:    
                strkeys.remove('subjects')
                details['subjects'] = createTask(details['subjects'],None)  
            
            if details['subjects'][0]['inc_id']:    
                session_id = details['subjects'][0]['pid']+'-'+str(int(details['subjects'][0]['tid']))+'-'+str(int(details['subjects'][0]['taskid']))

            #保存或修改其他內容
            for strkey in strkeys:
                details[strkey] = batchUpdateTask(details[strkey],session_id)
            for strkey in strkeys:
                details[strkey] = createTask(details[strkey],session_id)
            return details


def batchUpdateTask(details,session_id):
    '''
    功能描述：批量修改會議記錄數據
    '''
    mettingUpdatedata = []
    # removelists = []
    for detail in details:
        mettingdetail = models.Task()
        mettingdata = None
        if detail['inc_id']:
            mettingdata = models.Task.objects.filter(inc_id = detail['inc_id'])
        if  mettingdata:  
            mettingdetail.inc_id = detail['inc_id']
            mettingdetail.task = detail['task']
            mettingdetail.relationid = session_id
            mettingdetail.contact = detail['contact']
            mettingdetail.docpath = detail['docpath']
            mettingdetail.editionid = detail['editionid']
            mettingdetail.rank = detail['rank']
            mettingdetail.pid = detail['pid']
            mettingdetail.tid = detail['tid']
            mettingdetail.taskid = detail['taskid']
            
            detail['relationid'] = session_id
            mettingUpdatedata.append(mettingdetail)
            # removelists.append(detail)
    with transaction.atomic(using='MPMS'):
        models.Task.objects.bulk_update(mettingUpdatedata, fields=['task','relationid','contact','docpath','rank','editionid'], batch_size=100)
    # for removedetail in removelists:
    #     details.remove(removedetail)    
    return details  

def createTask(details,session_id):
    '''
    功能描述：批量修改會議記錄數據
    '''
    mettingCreatedata = []
    for detail in details:
        mettingdata = None
        if detail['inc_id']:
            mettingdata = models.Task.objects.filter(inc_id = detail['inc_id'])
        if  not mettingdata:  
            mettingdetail = models.Task()
            mettingdetail.task = detail['task']
            mettingdetail.relationid = session_id
            mettingdetail.contact = detail['contact']
            mettingdetail.docpath = detail['docpath']
            mettingdetail.editionid = detail['editionid']
            mettingdetail.rank = detail['rank']
            mettingdetail.pid = detail['pid']
            mettingdetail.tid = detail['tid']
            mettingdetail.progress = detail['progress']
            mettingdetail.planbdate = detail['planbdate']
            mettingdetail.planedate = detail['planedate']
            mettingdetail=max_seqno(mettingdetail)
            with transaction.atomic(using='MPMS'):
                mettingdetail.save()
            mettingdata = models.Task.objects.filter(inc_id=mettingdetail.inc_id)
        mettingCreatedata.append(list(mettingdata.values())[0])
    return mettingCreatedata
 
def max_seqno(instance):
    '''
    功能描述：獲取最大單號
    參數說明:
        instance:需要保存或初始化的model實例
    '''
    maxtaskid = models.Task.objects.filter(pid=instance.pid,tid =instance.tid).values('taskid').aggregate(Max('taskid'))['taskid__max'] 
    if maxtaskid == None:   
        instance.taskid = 10
    else:
        instance.taskid = maxtaskid+10
    return instance    


def delete_met_project(request:HttpRequest):
    '''
    功能描述：刪除會議議題及相關內容
    '''
    #
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        inc_id = request.GET.get('id')
        deletemetting =  models.Task.objects.filter(inc_id=inc_id).values()
        for delmetting in deletemetting:
            session_id = delmetting['pid']+'-'+str(int(delmetting['tid']))+'-'+str(int(delmetting['taskid']))
            relationtask = models.Task.objects.filter(relationid=session_id)
            relationtask.delete()
        deletemetting.delete()    
        result['status'] = True  
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   



class MettingmasterDeleteView(SWDeleteView):
    model = models.Mettingmaster    

    def delete_other(self, instance):
        '''
        功能描述：刪除時，更新與該model相關的其他model數據
        參數說明:
            instance:本model實例
        '''
        detail = models.Task.objects.filter(docpath=instance.id)
        detail.delete()
        return True

class MettingdetailView(DatatablesServerSideView):
    model = models.Mettingdetail
    columns = "__all__"
    searchable_columns = ['id','itemno','subject','discussprocess','conclusion','arrange','inc_id']

class MettingdetailCreateView(SWCreateView):
    model = models.Mettingdetail        

    def get_initial(self, instance):
        '''
        功能描述：Http Get 訪問時初始化model新增時的數據
        參數說明:
            instance:該model的實例
        '''
        self.set_max_seqno(instance)
    
    def set_max_seqno(self, instance):
        '''
        功能描述：獲取最大單號
        參數說明:
            instance:需要保存或初始化的model實例
        '''
        strf_time = time.strftime("%Y%m%d", time.localtime())
        strid = models.Mettingmaster.objects.filter().values('id').aggregate(Max('id'))['id__max'] 
        if strid == None:   
            instance.id = strf_time+'001'
        else:
            instance.id = str(int(strid)+1)

class MettingdetailDeleteView(SWDeleteView):
    model = models.Mettingdetail















