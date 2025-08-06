from asyncio import tasks
from operator import mod
from sqlite3 import Date
from click import edit
from django.core.serializers.json import DjangoJSONEncoder
import json
from datatableview import Datatable
from django.db import connections
from datatableview.views import MultipleDatatableView
from datatableview.views.legacy import LegacyDatatableView
from datatableview import helpers
from django.middleware.gzip import GZipMiddleware
from BaseProject.CustomBaseObject.base_views.CustomView import CustomUpdateView
from BaseProject.tools import DateTools
from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
from BaseApp.library.cust_views.SWCreateView import SWCreateView
from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from BaseApp.library.cust_views.SWDeleteView import SWDeleteView
from django.core.cache import cache
from django.conf import settings
from DataBase_MPMS import models
from BaseApp.library.tools import ModelTools
import time
import datetime
import copy
import re
import io
import base64
from base64 import b64encode
from django.db import transaction
from django.db.models import Count,Q,F,Case,Sum,When,IntegerField,Max,ExpressionWrapper,CharField,Func,Value
from django.db.models.functions import Coalesce
from django.http import JsonResponse,HttpResponse,HttpRequest
from time import sleep
from django.utils.encoding import escape_uri_path
from BaseApp.library.tools import  AsyncioTools
from PMIS.Services.UserService import UserService
import math
import logging
from pdf2image import convert_from_bytes

IMAGE_TYPE = ["image/jpeg", "image/png", "image/jpg", "image/gif", "image/bmp"]
PDF_TYPE = ['application/pdf',"pdf",".pdf"]
        
batch_size = 100
LOGGER = logging.Logger(__name__)

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
            forldnamelist = []
            docidlist = []
            #獲取會議所有議題和議題相關信息
            if status == 'Browse' and strid:
                meeting_items = models.Task.objects.filter(docpath=strid,editionid__in=['1','2','3','4']).order_by('editionid','rank').values()
            #獲取會議對弈議題和議題相關信息
            else:
                meeting_items = list(models.Task.objects.filter(docpath=strid,inc_id=subject).order_by('editionid','rank').values())
                relationid = f"{meeting_items[0]['pid']}-{int(meeting_items[0]['tid'])}-{int(meeting_items[0]['taskid'])}"
                other_meeting_items = list(models.Task.objects.filter(docpath=strid,relationid=relationid).order_by('editionid','rank').values())
                meeting_items.extend(other_meeting_items)
                for meeting_item in meeting_items:
                    forldnamelist.append(f"{meeting_item['pid']}-{int(meeting_item['tid'])}-{int(meeting_item['taskid'])}")
                    docidlist.append(f"{meeting_item['pid']}{int(meeting_item['tid'])}{int(meeting_item['taskid'])}")
            data = {}
            meeting_items = batch_get_task_file(meeting_items,docidlist,forldnamelist)
            for item in meeting_items:
                relationid = item['relationid']
                if item['editionid']!='1':
                    relationid = relationid.strip()
                #議題
                if item['editionid']=='1':
                    relationid = f"{item['pid']}-{int(item['tid'])}-{int(item['taskid'])}"
                    data[relationid] = {'subjects':[item],'conclusions':[],'arranges':[]}
                #結論
                elif item['editionid']=='3':
                    if relationid in data:
                        data[relationid]['conclusions'].append(item)
                    else:
                        data[relationid] = {'subjects':[],'conclusions':[item],'arranges':[]}
                #後續安排
                elif item['editionid']=='4':
                    if relationid in data:
                        data[relationid]['arranges'].append(item)
                    else:
                        data[relationid] = {'subjects':[],'conclusions':[],'arranges':[item]}
            datakeys = data.keys()
            for datakey in datakeys:
                result['data'].append(data[datakey])
            result['status'] = True  
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)  


def get_task_file(request:HttpRequest):
    '''
    功能描述:獲取指定任務的文件信息
    '''
    result = {'status':True, 'msg':'', 'data':[]}
    try:
        taskid = request.GET.get('taskid')
        taskno = taskid.split('-')
        docid=''
        if len(taskno)==3:
            docid = '{0}{1}{2}'.format(taskno[0],taskno[1],taskno[2])
        taskfolder = models.VDocument.objects.filter(docid=docid,foldername=taskid).order_by('folderid')
        if taskfolder.exists():
            uploadList = list(taskfolder.values())
            for file in uploadList:
                file['fileurl'] = f"/looper/metting/browse_task_image?inc_id={file['inc_id']}"
            result['data'] = uploadList
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   


def batch_get_task_file(items,docidlist=[],foldernamelist=[],pid='pid',tid='tid',taskid='taskid'):
    '''
    功能描述：批量獲取文件
    參數說明：
        itmes:要獲取文件信息的數據集
        docidlist:主鍵值列表若該列表為空則itmes類型要是QuerySet)
        pid:主鍵Pid別名
        tid:主鍵tid別名
        taskid:主鍵taskid別名
    '''
    if len(docidlist)==0:
        # foldernamelist = list(items.annotate(
        #                 session_id=ExpressionWrapper(
        #                     F(pid)+'-'+
        #                     Func(Func(F(tid), function='Str'),function='Trim')+'-'+
        #                     Func(Func(F(taskid), function='Str'),function='Trim'), 
        #                     output_field=CharField()
        #                 )
        #             ).values_list('session_id',flat=True))
        # docidlist = list(items.annotate(
        #                 session_id=ExpressionWrapper(
        #                     F(pid)+
        #                     Func(Func(F(tid), function='Str'),function='Trim')+
        #                     Func(Func(F(taskid), function='Str'),function='Trim'), 
        #                     output_field=CharField()
        #                 )
        #             ).values_list('session_id',flat=True))
        foldernamelist = ['{}-{}-{}'.format(i['pid'],str(int(i['tid'])),str(int(i['taskid']))) for i in items]
        docidlist = ['{}{}{}'.format(i['pid'],str(int(i['tid'])),str(int(i['taskid']))) for i in items]
    taskfolders = getVDocument(docidlist,foldernamelist)
    if len(taskfolders)>0:
        taskfolder_list = [item['docid'] for item in taskfolders if item['docid']]
        # taskfolders = list(taskfolders.values())
        for item in items:
            item_taskid = f"{item[pid]}-{int(item[tid])}-{int(item[taskid])}"
            item_taskiddocid = f"{item[pid]}{int(item[tid])}{int(item[taskid])}"
            itemkeylist = list(item.keys())
            if itemkeylist.count('uploadList') == 0:
                item['uploadList']=[]
            if taskfolder_list.count(item_taskiddocid)>0:
                for taskfolder in taskfolders:
                    if item_taskiddocid == taskfolder['docid'] and item_taskid == taskfolder['foldername']:
                        taskfolder['fileurl'] = f"/looper/metting/browse_task_image?inc_id={taskfolder['inc_id']}"
                        item['uploadList'].append(taskfolder)
    else:
        for item in items:
            itemkeylist = list(item.keys())
            if itemkeylist.count('uploadList') == 0:
                item['uploadList']=[]
    return items

def getVDocument(docidlist,foldernamelist):
    # batch_size = 100
    num_batches = math.ceil(len(docidlist) / batch_size)
    results = []
    for i in range(num_batches):
        start = i * batch_size
        end = start + batch_size
        batch_docidlist = docidlist[start:end]
        batch_foldernamelist = foldernamelist[start:end]
        batch_results = models.VDocument.objects.filter(docid__in=batch_docidlist, foldername__in=batch_foldernamelist).order_by('folderid').values()
        results.extend(batch_results)
    return results


#獲取會議樹狀圖
def get_metting_tree(request:HttpRequest):
    '''
    功能描述：獲取metting的樹狀圖
    '''
    #
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        strdate = request.GET.get('date')
        isModal = request.GET.get('isModal')
        if ((not strdate) or (not strdate.isdigit())) and (strdate!='-8'):
            strdate = time.strftime("%Y%m%d", time.localtime())[2:]
        TreeList = [] 
        if strdate=='-8':
            strf_time = ((datetime.datetime.now())+datetime.timedelta(days= -8)).strftime("%Y%m%d")[-6:]
            mettings = models.Mettingmaster.objects.filter(id__gte=strf_time).values()
        else:
            mettings = models.Mettingmaster.objects.filter(id__contains=strdate).values()
        for metting in mettings:
            meeting_items = models.Task.objects.filter(docpath=metting['id'])
            childrenlist = Getmettingchildren(metting,meeting_items)
            name = metting['id']
            if isModal!='Y':
                #獲取對應會議的結論數量
                meeting_items =  meeting_items.filter(editionid='3').values().aggregate(
                            task_qty=Count('taskid'), 
                            completed_qty=Sum( 
                            Case(  
                                When(progress__in='CF', then=1),
                                default=0,
                                output_field=IntegerField()
                            )),
                        )
                if not meeting_items['completed_qty']: 
                    meeting_items['completed_qty'] = 0 
                if not meeting_items['task_qty']: 
                    meeting_items['task_qty'] = 0 
                name ='{0}({1}/{2})'.format(name,meeting_items['completed_qty'],meeting_items['task_qty'])
            TreeList.append({
                'icon': "",'name': name,'children': childrenlist,'inc_id':metting['inc_id'],'strid':metting['id'].replace(' ',''),
                'sub_inc_id':'','tier':'0','session_id':''
            })   
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
        metting_sub_list.append({
            'icon': "",'name': metting_sub_item['task'],'children': [],'inc_id':metting_item['inc_id'],'strid':metting_item['id'].replace(' ',''),
            'sub_inc_id':metting_sub_item['inc_id'],'tier':'2','session_id':f"{metting_sub_item['pid']}-{int(metting_sub_item['tid'])}-{int(metting_sub_item['taskid'])}"
        })

    
    # TreeList.append({'icon': "",'name': '會議信息','children': metting_mes_list,'inc_id':metting_item['inc_id'],'strid':metting_item['id'].replace(' ',''),'sub_inc_id':'','tier':'1'})
    # TreeList.append({'icon': "",'name': '會議議題','children': metting_sub_list,'inc_id':metting_item['inc_id'],'strid':metting_item['id'].replace(' ',''),'sub_inc_id':'','tier':'1'})
    # TreeList.append({'icon': "",'name': '會議附件','children': metting_acc_list,'inc_id':metting_item['inc_id'],'strid':metting_item['id'].replace(' ',''),'sub_inc_id':'','tier':'1'})
    return metting_sub_list

#檢驗會議主表查詢條件是否不為空
def check_meetingMaster_filter(meetingMaster_filter):
    Result = False
    keyList = meetingMaster_filter.keys()
    for key in keyList:
        if meetingMaster_filter[key]!='':
            Result = True
            break
    return Result

#獲取會議未完成的結論
def get_metting_undone(request:HttpRequest):
    '''
    功能描述：獲取前八天未完成的結論
    '''
    #
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        description = request.GET.get('description')#結論內容
        meetingid = request.GET.get('meetingid')#會議id
        progress = request.GET.get('progress')#進度
        allocation = request.GET.get('allocation')#是否分配任務
        contact = request.GET.get('contact')#聯繫人
        hoperation = request.GET.get('hoperation')#操作字段
        planbs = request.GET.get('planbs')#計劃開始日期字段
        planbe = request.GET.get('planbe')#計劃開始日期字段
        planes = request.GET.get('planes')#計劃結束日期字段
        planee = request.GET.get('planee')#計劃結束日期字段
        bdatebs = request.GET.get('bdatebs')#實際開始日期字段
        bdatebe = request.GET.get('bdatebe')#實際開始日期字段
        edatees = request.GET.get('edatees')#實際結束日期字段
        edateee = request.GET.get('edateee')#實際結束日期字段
        topic = request.GET.get('topic')#議題
        classif = request.GET.get('classif')#類型
        createdates = request.GET.get('createdates')#需求日期
        createdatee = request.GET.get('createdatee')#需求日期

        discussprocess = request.GET.get('discussprocess','')#討論過程
        summary = request.GET.get('summary','')#會議摘要
        meetingtopic = request.GET.get('meetingtopic','')#會議主題
        participants = request.GET.get('participants','')#參會人員
        plandates = request.GET.get('plandates','')#計劃日期開始
        plandatee = request.GET.get('plandatee','')#計劃日期結束
        meetingstate = request.GET.get('meetingstate','')#會議狀態
        meetingMaster_filter={'discussprocess':discussprocess,'summary':summary,'topic':meetingtopic,'participants':participants,
                              'plandates':plandates,'plandatee':plandatee,'state':meetingstate,'id':meetingid}
        resultData = {'master':[],'detail':[],'summary':[],'summary_topic':[]}
        if not (allocation=='null'):
            meetingData=[]
            meetingid_list=[]
            strf_time = ((datetime.datetime.now())+datetime.timedelta(days= -8)).strftime("%Y%m%d")[-6:]
            metting_relationtask=None
            #會議結論條件
            q2 = Q()
            q2.connector = "and"    
            if len(meetingid_list)>0:
                q2.children.append(("docpath__in",meetingid_list))
            #結論內容
            if description!=None and description!='':
                q2.children.append(("task__contains",description))
            #聯繫人
            if contact!=None and contact!='':  
                q2.children.append(("contact",contact))  
            #操作    
            if hoperation!=None and hoperation!='' and hoperation!='empty' and allocation != '4':
                q2.children.append(("hoperation",hoperation))  
            if hoperation=='empty':
                q2.children.append(Q(hoperation='') | Q(hoperation__isnull=True))  
            #會議id
            if meetingid!=None and meetingid!='':
                q2.children.append(("docpath__contains",meetingid))
            else:
                if allocation=='5':
                    q2.children.append(("docpath__gte",strf_time))
            if allocation == '4':
                q2.children.append(("hoperation",'P'))
            #已分配已完成的會議
            if (allocation != '0') and (progress=='1'):
                q2.children.append(("progress__in",['C','F']))
            elif (progress!=None) and (progress!='') and (progress.isdigit()==False):
                q2.children.append(("progress",progress))
            #計劃開始日期   
            if (planbs!=None and planbs!=''):
                q2.children.append(("planbdates__gte",planbs))   
            if (planbe!=None and planbe!=''):
                q2.children.append(("planbdates__lte",planbe))      
            #計劃結束日期    
            if (planes!=None and planes!=''):
                q2.children.append(("planedates__gte",planes))  
            if (planee!=None and planee!=''):
                q2.children.append(("planedates__lte",planee))  
            #實際開始日期    
            if (bdatebs!=None and bdatebs!=''):
                q2.children.append(("bdates__gte",bdatebs))   
            if (bdatebe!=None and bdatebe!=''):
                q2.children.append(("bdates__lte",bdatebe))    
            #實際結束日期      
            if (edatees!=None and edatees!=''):
                q2.children.append(("edates__gte",edatees))  
            if (edateee!=None and edateee!=''):
                q2.children.append(("edates__lte",edateee))  
            #創建日期      
            if (createdates!=None and createdates!=''):
                q2.children.append(("create_date__gte",createdates.replace('-','')))  
            if (createdatee!=None and createdatee!=''):
                q2.children.append(("create_date__lte",createdatee.replace('-','')))  
            #過去八天所有會議記錄
            if allocation=='5':
                meetingData = models.Mettingmaster.objects.filter(id__gte=strf_time).values()
                meetingid_list = [item['id'].replace(' ','') for item in meetingData if item['id']]
                meetingid_list =list(set(meetingid_list))
                if (len(meetingid_list)>0): 
                    #查詢過去八天分配任務和相關文件信息
                    meeting_items = models.VTaskMeeting.objects.filter(q2 & Q(docpath__in=meetingid_list)).order_by('pid','tid','taskid').values()
                    detail_list = meeting_items.values()
                    detail_list = batch_get_task_file(detail_list,[],[],'parent_pid','parent_tid','parent_taskid')
                    detail_list = batch_get_task_file(detail_list)
                    resultData['detail'] = list(detail_list)
                    #查詢過去八天議題結論
                    metting_relationtask = models.VTask.objects.filter(Q(docpath__in=meetingid_list) & Q(editionid='3')).order_by('pid','tid','taskid','docpath')
                    resultData['summary'],resultData['summary_topic']=summary_meeting_data(q2,metting_relationtask,classif,allocation)  
            else:    
                if allocation==None:
                    allocation='1'   
                #若會議主表查詢條件不為空則先查詢會議主表信息
                if check_meetingMaster_filter(meetingMaster_filter):
                    meetingData = getMeetingMaster(meetingMaster_filter)
                    meetingid_list = [item['id'].replace(' ','') for item in meetingData if item['id']]
                    meetingid_list =list(set(meetingid_list))
                
                if (not (check_meetingMaster_filter(meetingMaster_filter))) or (len(meetingData)>0): 
                    q1 = copy.deepcopy(q2)
                    q1.children.append(("editionid",'3'))
                    if len(meetingid_list)>0:
                        q1.children.append(("docpath__in",meetingid_list))
                    #當議題不為空時，先查詢議題信息，在將議題的pid-tid-taskid值作為條件寫入議題查詢條件中
                    if topic!=None and topic!='':
                        #按條件查詢相關議題
                        meeting_topic = models.Task.objects.filter(task__contains=topic,editionid='1').order_by('pid','tid','taskid')
                        #獲取結論的pid-tid-taskid拼接字段列表
                        session_id_list = [f'{item.pid}-{int(item.tid)}-{int(item.taskid)}' for item in meeting_topic  if item]
                        q1.children.append(("relationid__in",session_id_list)) 
                    
                    if meetingMaster_filter['plandates']=='-8':
                        q1.children.append(("udf09",'sing')) 
                    session_id_list=[]
                    #未分配任務
                    unallocation_task = models.VTaskMeetingUnd.objects.filter(q1)
                    if allocation=='0':
                        if classif!='0':
                            meeting_items = unallocation_task
                            meeting_items = meeting_items.exclude(hoperation__in=['L','O','R']).order_by('pid','tid','taskid')
                            detail_list = meeting_items.values()
                            detail_list = batch_get_task_file(detail_list)
                            #查詢到符合條件的數據
                            resultData['detail'] = list(detail_list)
                            meetingid_list = [item.docpath for item in meeting_items  if item.docpath]
                    #已分配任務
                    else:
                        #按條件查詢相關結論
                        meeting_items = models.VTask.objects.filter(q1).order_by('pid','tid','taskid','docpath')
                        #若為已分配則過濾掉未分配的數據
                        if allocation=='1':
                            tasknolist = [f'{item.pid}-{int(item.tid)}-{int(item.taskid)}' for item in unallocation_task if item] 
                            meeting_items = meeting_items.exclude(taskno__in=tasknolist)
                        if meeting_items.exists():
                            #是否完成任務
                            if  (allocation != '0') and (progress=='0'):
                                meeting_items = meeting_items.exclude(progress__in=['C','F'])
                            elif (progress!=None) and (progress!='') and (progress.isdigit()==False):
                                meeting_items = meeting_items.filter(progress=progress)
                            #獲取結論的pid-tid-taskid拼接字段列表
                            session_id_list = [item.taskno for item in meeting_items if item.taskno]
                        #議題結論
                        if classif=='1':
                            metting_relationtask = meeting_items
                        #轉後任務
                        elif classif=='0':
                            metting_relationtask = models.VTaskMeeting.objects.filter(Q(relationid__in=session_id_list) & q2).order_by('pid','tid','taskid')
                        #議題結論+轉後任務
                        else:
                            metting_relationtask = models.VTaskMeeting.objects.filter(Q(relationid__in=session_id_list) & q2).order_by('pid','tid','taskid')
                            if metting_relationtask!=None and metting_relationtask.exists():
                                if (allocation != '0') and (progress=='0'):
                                    metting_relationtask = metting_relationtask.exclude(progress__in=['C','F'])
                                elif (progress!=None) and (progress!='') and (progress.isdigit()==False):
                                    metting_relationtask = metting_relationtask.filter(progress=progress)
                                detail_list = metting_relationtask.values()
                                #獲取分配任務的文件信息
                                detail_list = batch_get_task_file(detail_list,[],[],'parent_pid','parent_tid','parent_taskid')
                                detail_list = batch_get_task_file(detail_list)
                                resultData['detail'] = list(detail_list)
                            #議題結論
                            metting_relationtask = copy.deepcopy(meeting_items)
                    #對議題結論數據進行處理
                    if metting_relationtask!=None and metting_relationtask.exists():
                        #已分配任務未完成的會議 
                        if (allocation != '0') and (progress=='0') and (classif!='0' and classif!='1'):
                            metting_relationtask = metting_relationtask.exclude(progress__in=['C','F'])
                        elif (progress!=None) and (progress!='') and (progress.isdigit()==False):
                            metting_relationtask = metting_relationtask.filter(progress=progress)
                        detail_list = metting_relationtask.values()
                        #獲取議題結論和分配任務的文件信息
                        if classif=='0':
                            #分配任務同時獲取分配任務文件和對弈議題結論的文件信息
                            detail_list = batch_get_task_file(detail_list,[],[],'parent_pid','parent_tid','parent_taskid')
                            detail_list = batch_get_task_file(detail_list)
                        else:
                            detail_list = batch_get_task_file(detail_list)
                        #查詢到符合條件的數據
                        if len(resultData['detail'])>0:
                            for detail in list(detail_list):
                                resultData['detail'].append(detail)
                        else:
                            resultData['detail'] = list(detail_list)
                        if classif=='0':
                            meetingid_list = [item.meetingid for item in metting_relationtask if item.meetingid]
                        else:
                            meetingid_list = [item.docpath for item in metting_relationtask if item.docpath]
                    resultData['summary'],resultData['summary_topic']=summary_meeting_data(q2,metting_relationtask,classif,allocation)  
                    meetingid_list = list(set(meetingid_list))  
                    if not(len(meetingData)>0):
                        #分批查詢數據
                        num_batches = math.ceil(len(meetingid_list) / batch_size)
                        meetingData = []
                        for i in range(num_batches):
                            start = i * batch_size
                            end = start + batch_size
                            batch_meetingid_list = meetingid_list[start:end]
                            batch_results = models.Mettingmaster.objects.filter(id__in=batch_meetingid_list).values()
                            meetingData.extend(batch_results)
            #會議分析數據
            analysisData = analysis_meeting_data(meetingid_list)
            for meeting in meetingData:
                #將參會人員字段轉換成列表格式
                if meeting['participants']:
                    meeting['participants'] = meeting['participants'].split(",")
                masterdata = {'analysisData':{},'meetingData':meeting}
                #將分析數據寫入對應的會議
                if meeting['id'].strip() in analysisData:
                    masterdata['analysisData'] = analysisData[meeting['id'].strip()]
                resultData['master'].append(masterdata)                 
        result['data'].append(resultData)                 
        result['status'] = True  
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   

def summary_meeting_data(q2,detail_list,classif,allocation):
    summary = []
    summary_topic = []
    detailList=copy.deepcopy(detail_list)
    if classif=='0' and allocation!='0':
        detailList = models.VTask.objects.filter(q2 & Q(editionid='3')).order_by('pid','tid','taskid','docpath')
    if allocation=='0' and  classif!='0':
        detailList = models.VTaskMeetingUnd.objects.filter(q2 & Q(editionid='3')).exclude(hoperation__in=['L','O','R']).order_by('pid','tid','taskid')
    #獲取議題結論的relationid並去重
    relationid_list = [item.relationid for item in detailList if item.relationid]
    relationid_list = list(set(relationid_list))
    #獲取所有議題的taskid
    taskidlist =[item.split('-')[2] for item in relationid_list if item]
    #查詢所有會議議題
    topicsData = models.VTask.objects.filter(taskid__in = taskidlist,pid='11580',tid=12,editionid='1').order_by('task')
    #獲取會議議題名稱並去重
    topics_list = [item.task for item in topicsData if item.task]
    topics_list = list(set(topics_list))
    summary.append({'title':'會議議題','statistical':len(topics_list)})
    #獲取所有會議主題的pid-tid-taskid
    TempDic = {}
    for topic in topics_list:
        topic = topic.replace(' ','')
        TempDic[topic]=[]
        for item in  topicsData:
            if item.task!=None and topic==item.task.replace(' ',''):
                TempDic[topic].append(item.taskno)
    #統計個任務數量
    taskqty=taskqty_f=p_taskqty=p_taskqty_f = 0
    for item in detailList:
        if item.editionid=='3':
           taskqty=taskqty+1 
        if item.editionid=='3' and item.progress in ['C','F']:
            taskqty_f=taskqty_f+1
        if item.editionid=='3' and item.hoperation=='P':
            p_taskqty=p_taskqty+1
        if item.editionid=='3' and item.progress in ['C','F'] and item.hoperation=='P':
            p_taskqty_f=p_taskqty_f+1
    #查詢總未分配任務數量
    unallocation_task = models.VTaskMeetingUnd.objects.filter(Q(relationid__in = relationid_list,pid='11580',tid=12,editionid='3') & q2)
    summary.append({'title':'議題結論總','statistical':taskqty})
    summary.append({'title':'完成議題結論總','statistical':taskqty_f})
    summary.append({'title':'議題結論總未分配','statistical':len(unallocation_task)})
    summary.append({'title':'馬上處理總任務','statistical':p_taskqty})
    summary.append({'title':'完成馬上處理總','statistical':p_taskqty_f})
    for i in topics_list:
        topic_i = {'topic':'','taskqty':0,'p_taskqty':0,'taskqty_f':0,'p_taskqty_f':0,'un_taskqty':0}
        topic_i['topic']=i
        for item in detailList:
            TempArray = TempDic[i.replace(' ','')]
            if item.relationid in TempArray:
                if item.editionid=='3':
                    topic_i['taskqty']=topic_i['taskqty']+1
                if item.editionid=='3' and  item.progress in ['C','F']:
                    topic_i['taskqty_f']=topic_i['taskqty_f']+1
                if item.editionid=='3' and  item.hoperation=='P':
                    topic_i['p_taskqty']=topic_i['p_taskqty']+1
                if item.editionid=='3' and  item.progress in ['C','F'] and item.hoperation=='P':
                    topic_i['p_taskqty_f']=topic_i['p_taskqty_f']+1
        untopic_task = models.VTaskMeetingUnd.objects.filter(Q(relationid__in = TempArray,pid='11580',tid=12,editionid='3') & q2)
        topic_i['un_taskqty']=len(untopic_task)
        summary_topic.append(topic_i)
    return summary,summary_topic

#根據會議主表條件查詢會議主表信息
def getMeetingMaster(filter):
    fkeys = filter.keys()
    qm = Q()
    qm.connector = "and"   
    for key in fkeys:
        if filter[key]  !='':
            if key in ['plandates','plandatee','meetingstate','participants']:
                if key =='plandates':
                    if filter[key]=='-8':
                        strf_time = ((datetime.datetime.now())+datetime.timedelta(days= -8)).strftime("%Y%m%d")[-6:]
                        qm.children.append(("id__gte",strf_time))  
                    else:
                        #創建日期      
                        qm.children.append(("plandate__gte",filter[key]))  
                if key =='plandatee':
                    qm.children.append(("plandate__lte",filter[key]))  
                if key =='meetingstate':
                    qm.children.append(("meetingstate__contains",filter[key]))  
                if key == 'participants':
                    parlist = filter[key].split('+')
                    for par in parlist:
                        qm.children.append((key+"__contains",par))   
            else:
                qm.children.append((key+"__contains",filter[key]))   
    return models.Mettingmaster.objects.filter(qm).values()
    

#保存會議文件
def save_met_file(request:HttpRequest):
    '''
    功能描述：保存會議文件
    '''
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        task_inc_id = request.POST.get('task_inc_id')
        file = request.FILES.get('file')
        if file and task_inc_id:
            task = models.Task.objects.filter(inc_id=task_inc_id).values()
            parentid,folderid = get_document_folder(task[0]['pid'])
            document = models.Document()
            document.parentid = parentid
            document.folderid = folderid
            document.foldername = f"{task[0]['pid']}-{int(task[0]['tid'])}-{int(task[0]['taskid'])}"
            document.docid = f"{task[0]['pid']}{int(task[0]['tid'])}{int(task[0]['taskid'])}"
            document.revisedby = task[0]['contact']
            document.t_stamp = datetime.datetime.now()
            docdetail = models.Docdetail()
            docdetail.parentid = parentid
            docdetail.folderid = folderid
            docdetail.revisedby = task[0]['contact']
            docdetail.t_stamp = datetime.datetime.now()
            document.docname = file.name
            document.docsize = f"{file.size}"
            document.mediatype = f"{file.content_type}"
            docdetail.content = file.read()
            file.close()
            with transaction.atomic(ModelTools.get_database(models.Document)):  
                document.save()
                docdetail.save()
            result['status'] = True  
        else:
            result['msg'] = '參數異常！'
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   

#獲取工程文件夾和最大文件序號
def get_document_folder(pid):
    parentid = 1
    folderid = models.Document.objects.aggregate(FolderMax_ID=Max('folderid'))
    if folderid:
        folderid = folderid['FolderMax_ID']
        folderid += 1
    else:
        folderid = 1
    #獲取對應工程文件夾
    FolderName = models.Document.objects.filter(docid=pid).values('parentid')
    if FolderName.exists():
        parentid = list(FolderName)[0]['parentid']
    else:
        #若不存在則獲取默認文件夾
        FolderName = models.Document.objects.filter(docid='taskDocument').values('parentid')
        if FolderName.exists():
            parentid = list(FolderName)[0]['parentid']
        else:
            #若不存在默認文件夾則創建默認文件夾
            create_document(0,folderid,0,'TaskDocument','taskDocument','F','','')
            parentid = folderid
            folderid = folderid+1
        #創建對應工廠的文件夾
        create_document(parentid,folderid,0,pid,pid,'F','','')
        parentid = folderid
        folderid = folderid+1
    return parentid,folderid

#創建工程文件夾
def create_document(ParentID,FolderID,FileType:int,FolderName,DocID,State,FName,MediaType:str):
    document = models.Document()
    document.parentid = ParentID
    document.folderid = FolderID
    document.type = FileType
    document.foldername = FolderName
    document.state = State
    document.docid = DocID
    document.docname = FName
    document.mediatype = MediaType
    document.t_stamp = datetime.datetime.now()
    document.save()

#統計會議信息並獲取當前會議所有附件
def analysis_meeting(request:HttpRequest):
    '''
    功能描述：統計會議信息並獲取當前會議所有附件
    '''
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        strid = request.GET.get('id')
        if strid:
            data = {'analysisData_hastask':{},'analysisData_nottask':{},'accessoryList':[]}
            analysisData_hastask = analysis_meeting_data([strid.strip()],'Y')
            analysisData_nottask = analysis_meeting_data([strid.strip()],'N')
            if strid.strip() in analysisData_hastask:
                data['analysisData_hastask']=analysisData_hastask[strid.strip()]
            if strid.strip() in analysisData_nottask:
                data['analysisData_nottask']=analysisData_nottask[strid.strip()]
            session_id_list = [f'{item.pid}-{int(item.tid)}-{int(item.taskid)}' for item in models.Task.objects.filter(docpath=strid,editionid__in='3') if item]
            taskfolder = models.VDocument.objects.filter(docid__in=session_id_list,foldername__in=session_id_list).order_by('folderid')
            if taskfolder.exists():
                uploadList = list(taskfolder.values())
                for file in uploadList:
                    file['fileurl'] = f"/looper/metting/browse_task_image?inc_id={file['inc_id']}"
                data['accessoryList']=uploadList
            result['data'].append(data) 
        result['status'] = True  
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   

#批量統計議題結論信息
def analysis_meeting_data(meetingID_list,classif=None):
    #對相應的會議進行統計
    resultData = {}
    meetingID_list = list(set(meetingID_list))
    if meetingID_list.count(None)>0:
        while meetingID_list.count(None)>0:
            meetingID_list.remove(None)
    if len(meetingID_list)>0:
        #初始化所有會議分析數據
        for item in meetingID_list:
            item = item.replace(' ','')
            resultData[item] = {
                #會議結論總數，完成結論總數，未完成結論總數，分配任務結論總數
                'conclusion_con':0,'finish_con':0,'unfinish_con':0,'assigning_con':0,
                #未分配任務結論總數，完成任務總數，未完成任務總數
                'undistributed_con':0,'finish_task_con':0,'unfinish_task_con':0,
                #P結論總數，完成P結論總數，未完成P結論總數，無需分配結論數量
                'conclusionP_con':0,'finishP_con':0,'unfinishP_con':0,'no_distribution_con':0,
                #各數所佔比例
                'assigning_ratio':0,'undistributed_ratio':0,'finish_task_ratio':0,'unfinish_task_ratio':0
            }
        #會議結論條件
        qs = models.Syspara.objects.filter(nfield='default_session', ftype='metting')
        if len(qs) > 0:
            fvalue = qs[0].fvalue
            fvalue_arr = fvalue.split('-')
        q2 = Q()
        q2.connector = "and"    
        q2.children.append(("editionid",'3'))
        q2.children.append(("docpath__in",meetingID_list))
        if len(fvalue_arr)==2:
            q2.children.append(("pid",fvalue_arr[0]))
            q2.children.append(("tid",fvalue_arr[1]))
        if classif=='N':
            q2.children.append(("hoperation__in",['O','U','L']))
        meeting_items = models.Task.objects.filter(q2)
        if classif=='Y':
            meeting_items = meeting_items.exclude(hoperation__in=['O','U','L'])
        if not meeting_items.exists():
            return resultData
        #統計當前會議的結論總數和已完成的會議 
        count_meetings = meeting_items.values()
        #統計當前會議的結論總數和已完成的會議 
        for count_meet in count_meetings:
            docpath= count_meet['docpath'].strip()
            #會議結論數量
            resultData[docpath]['conclusion_con'] = resultData[docpath]['conclusion_con']+1
            #無需分配結論數量
            if count_meet['hoperation'] in ['O','U','L']:
                resultData[docpath]['no_distribution_con'] = resultData[docpath]['no_distribution_con']+1
            #會議結論完成數量
            if count_meet['progress'] in ['C','F'] or count_meet['hoperation'] in ['O','U','L']:
                resultData[docpath]['finish_con'] = resultData[docpath]['finish_con']+1
            else:
                resultData[docpath]['unfinish_con'] = resultData[docpath]['unfinish_con']+1
            #會議結論P數量
            if count_meet['hoperation']=='P':
                resultData[docpath]['conclusionP_con'] = resultData[docpath]['conclusionP_con']+1
            #會議結論完成P數量
            if count_meet['progress'] in ['C','F'] and count_meet['hoperation']=='P':
                resultData[docpath]['finishP_con'] = resultData[docpath]['finishP_con']+1
            #外完成P任務數量
            resultData[docpath]['unfinishP_con'] = resultData[docpath]['conclusionP_con']-resultData[docpath]['finishP_con']

        #獲取結論的pid-tid-taskid拼接字段列表
        session_id_list = [f'{item.pid}-{int(item.tid)}-{int(item.taskid)}' for item in meeting_items if item]
        metting_relationtask = models.VTaskMeeting.objects.filter(
                                Q(relationid__in=session_id_list) & ~Q(editionid__in =['1','2','3'])
                            ).values()
                            # .values('docpath')
                            #     .annotate(
                            #     #已分配任務並完成的會議 
                            #     finish_task_con=Sum(
                            #         Case(
                            #             When(progress__in='CF', then=1),
                            #             default=0,
                            #             output_field=IntegerField()
                            #         )
                            #     ),
                            #     #已分配任務並未完成的會議 
                            #     unfinish_task_con=Sum(
                            #         Case(
                            #             When(~Q(progress__in='CF'), then=1),
                            #             default=0,
                            #             output_field=IntegerField()
                            #         )
                            #     ),
                            #     #已分配任務的會議 
                            #     assigning_con=Count('docpath')
                            # )
        num_batches = math.ceil(len(session_id_list) / batch_size)
        metting_relationtask = []
        for i in range(num_batches):
            start = i * batch_size
            end = start + batch_size
            batch_meetingid_list = session_id_list[start:end]
            batch_results = models.VTaskMeeting.objects.filter(
                                Q(relationid__in=batch_meetingid_list) & ~Q(editionid__in =['1','2','3'])
                            ).values()
            metting_relationtask.extend(batch_results)
        #滾動任務統計已完成任務和未完成任務數量
        for count_meet in metting_relationtask:
            docpath = count_meet['docpath'].strip()
            #完成任務數量
            if count_meet['progress'] in ['C','F'] or count_meet['hoperation'] in ['O','U','L']:
                resultData[docpath]['finish_task_con'] = resultData[docpath]['finish_task_con']+1
            #完成任務數量
            if count_meet['progress'] not in ['C','F']:
                resultData[docpath]['unfinish_task_con'] = resultData[docpath]['unfinish_task_con']+1
        #獲取所有任務的關聯任務編號，去重後就是已分配任務的議題結論數量
        for item in meetingID_list:
            docpath = item.replace(' ','')
            assigning_list = ['{}-{}-{}'.format(metting['parent_pid'],int(metting['parent_tid']),int(metting['parent_taskid'])) for metting in metting_relationtask if metting and metting['docpath']==docpath]
            assigning_list = list(set(assigning_list))
            #已分配任務數量    
            resultData[docpath]['assigning_con'] = len(assigning_list)
            #未分配結論 = 結論總數-分配任務數量-無需分配任務數量
            resultData[docpath]['undistributed_con'] = resultData[docpath]['conclusion_con']-resultData[docpath]['assigning_con']-resultData[docpath]['no_distribution_con']

        resultkeys = resultData.keys()
        for resultkey in resultkeys:
            resultkey = resultkey.strip()
            if resultData[resultkey]['conclusion_con']>0:
                resultData[resultkey]['assigning_ratio'] = int(resultData[resultkey]['assigning_con']/resultData[resultkey]['conclusion_con']*100)
                resultData[resultkey]['undistributed_ratio'] = int(resultData[resultkey]['undistributed_con']/resultData[resultkey]['conclusion_con']*100)
                resultData[resultkey]['finish_task_ratio'] = int(resultData[resultkey]['finish_con']/resultData[resultkey]['conclusion_con']*100)
                resultData[resultkey]['unfinish_task_ratio'] = int(resultData[resultkey]['unfinish_con']/resultData[resultkey]['conclusion_con']*100)
    return resultData


def browse_task_image(request:HttpRequest):
    #查看圖片
    inc_id = request.GET.get('inc_id')
    state = request.GET.get('state')
    taskfolder = models.VDocument.objects.filter(inc_id=inc_id).order_by('folderid')
    if not taskfolder.exists():
        return HttpResponse(status=404) #不存在的文件，返回404

    taskfolder = taskfolder.values()[0]
    taskimage =  models.Docdetail.objects.filter(parentid=taskfolder['parentid'],folderid=taskfolder['folderid']).order_by('folderid').values()[0]
    response = HttpResponse(taskimage['content'], content_type=taskfolder['mediatype'])
    # 判斷文件類型
    if (IMAGE_TYPE.count(taskfolder['mediatype']) != 0) and (not(state == 'download')):
        # 是圖片直接顯示
        response.__setitem__("Content-Disposition", "inline; filename="+escape_uri_path(taskfolder['docname']))
    elif (PDF_TYPE.count(taskfolder['mediatype']) != 0) and (state == "convert_pdf"): ##如果是pdf且需要轉為圖片
        try:
            images = convert_from_bytes(taskimage['content'], dpi=500, first_page=1, last_page=1)
            output = io.BytesIO()
            images[0].save(output,"PNG")
            response = HttpResponse(output.getvalue(), content_type="image/png")
        except Exception as e:
            response.__setitem__("Content-Disposition", "attachment; filename="+escape_uri_path(taskfolder['docname']))
    else:
        # 是文件直接下載
        response.__setitem__("Content-Disposition", "attachment; filename="+escape_uri_path(taskfolder['docname']))
    return response  


#獲取議題下拉框值
def get_combobox_topic(request):
    # 定義要返回的對象
    result = {'status':False, 'msg':'', 'data':[]}
    # 獲得下拉控件的valueField指定的字段
    searchfield = request.GET.get('field')
    # 獲得下拉控件輸入框輸入的值
    searchvalue = request.GET.get('searchvalue')
    # 獲得下拉控件明細的顯示記錄數
    count = int(request.GET.get('count'))
    # 獲得下拉控件的過濾條件
    filter = request.GET.get('filter')
    
    if filter==None or filter=='':   
        filter="ISNUMERIC (DocPath) = 1 AND EditionID='1'"
    try:
        topics=None
        # 當輸入框的值不為空時，根據輸入框的值進行查詢
        if searchvalue:  
            sqlWhere=['{0} and {1} like %s'.format(filter, searchfield)]            
            param=['%%{0}%%'.format(searchvalue)]
            topics = models.Task.objects.annotate(
                    topic=ExpressionWrapper(F('task'),output_field=CharField())
                ).values('topic').extra(where=sqlWhere,params=param).distinct()[:count]
        else:
            topics = models.Task.objects.annotate(
                    topic=ExpressionWrapper(F('task'),output_field=CharField())
                ).values('topic').extra(where=[filter]).distinct()[:count]      
        result['status'] = True
        result['data'] =  list(topics)  # 把查詢出來的內容轉成list返回給控件
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)


#獲取Meeting議題下拉框值
def get_combobox_mettopic(request):
    # 定義要返回的對象
    result = {'status':False, 'msg':'', 'data':[]}
    # 獲得下拉控件的valueField指定的字段
    searchfield = request.GET.get('field')
    # 獲得下拉控件輸入框輸入的值
    searchvalue = request.GET.get('searchvalue')
    # 獲得下拉控件明細的顯示記錄數
    count = int(request.GET.get('count'))
    # 獲得下拉控件的過濾條件
    filter = request.GET.get('filter')
    
    if filter==None or filter=='':   
        filter="1=1"
    try:
        topics=None
        # 當輸入框的值不為空時，根據輸入框的值進行查詢
        if searchvalue:  
            sqlWhere=['{0} and {1} like %s'.format(filter, searchfield)]            
            param=['%%{0}%%'.format(searchvalue)]
            topics = models.Mettingmaster.objects.values('topic').extra(where=sqlWhere,params=param).distinct()[:count]
        else:
            topics = models.Mettingmaster.objects.values('topic').extra(where=[filter]).distinct()[:count]      
        result['status'] = True
        result['data'] =  list(topics)  # 把查詢出來的內容轉成list返回給控件
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)


#刪除文件
class DocumentDeleteView(SWDeleteView):
    model = models.Document    

    def delete_other(self, instance):
        '''
        功能描述：刪除時，更新與該model相關的其他model數據
        參數說明:
            instance:本model實例
        '''
        taskimage = models.Docdetail.objects.filter(parentid=instance.parentid,folderid=instance.folderid)
        taskimage.delete()
        return True




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
        instance.state='N'
        instance.plandate=DateTools.formatf(datetime.datetime.now(),'%Y-%m-%d')
    
    def set_max_seqno(self, instance):
        '''
        功能描述：獲取最大單號
        參數說明:
            instance:需要保存或初始化的model實例
        '''
        strf_time = DateTools.formatf(datetime.datetime.now(),'%Y%m%d')[2:]
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
            if (not details['subjects'][0]['inc_id']):    
                strkeys.remove('subjects')
                details['subjects'] = createTask(details['subjects'],None,self.request,instance.id)  
            
            if details['subjects'][0]['inc_id']:    
                session_id = f"{details['subjects'][0]['pid']}-{int(details['subjects'][0]['tid'])}-{int(details['subjects'][0]['taskid'])}"
            #保存或修改其他內容
            for strkey in strkeys:
                details[strkey] = batchUpdateTask(details[strkey],session_id,self.request,instance.id)
            for strkey in strkeys:
                details[strkey] = createTask(details[strkey],session_id,self.request,instance.id)
            return details



def get_Mettingma(request):
    # 定義要返回的對象
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        metid = request.GET.get('metid','')
        if metid!='':   
            metdata = models.Mettingmaster.objects.filter(id=metid).values()    
            result['data'] =  list(metdata)  # 把查詢出來的內容轉成list返回
        result['status'] = True
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)

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
                details['subjects'] = createTask(details['subjects'],None,self.request,instance.id)  
            
            if details['subjects'][0]['inc_id']:    
                session_id = f"{details['subjects'][0]['pid']}-{int(details['subjects'][0]['tid'])}-{int(details['subjects'][0]['taskid'])}"

            #保存或修改其他內容
            for strkey in strkeys:
                details[strkey] = batchUpdateTask(details[strkey],session_id,self.request,instance.id)
            for strkey in strkeys:
                details[strkey] = createTask(details[strkey],session_id,self.request,instance.id)
            return details


def batchUpdateTask(details,session_id,request,meetingid):
    '''
    功能描述：批量修改會議記錄數據
    '''
    mettingUpdatedata = []
    # removelists = []
    for detail in details:
        mettingdetail = models.Task()
        ModelTools.set_basic_field_info(request, models.Task, mettingdetail)
        mettingdata = None
        if detail['inc_id']:
            mettingdata = models.Task.objects.filter(inc_id = detail['inc_id'])
        if  mettingdata:  
            mettingdetail.inc_id = detail['inc_id']
            mettingdetail.task = detail['task']
            mettingdetail.relationid = session_id
            mettingdetail.contact = detail['contact']
            mettingdetail.docpath = meetingid
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

def createTask(details,session_id,request,meetingid):
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
            ModelTools.set_basic_field_info(request, models.Task, mettingdetail)
            mettingdetail.task = detail['task']
            mettingdetail.relationid = session_id
            mettingdetail.contact = detail['contact']
            mettingdetail.docpath = meetingid
            mettingdetail.editionid = detail['editionid']
            mettingdetail.rank = detail['rank']
            mettingdetail.pid = detail['pid']
            mettingdetail.tid = detail['tid']
            mettingdetail.progress = detail['progress']
            mettingdetail.planbdate = detail['planbdate']
            mettingdetail.planedate = detail['planedate']
            mettingdetail.udf09 = detail['udf09']
            mettingdetail.requestdate = datetime.datetime.now()
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
        deletemetting =  models.Task.objects.filter(inc_id=inc_id)
        if deletemetting.exists():
            for delmetting in deletemetting:
                session_id =f"{delmetting.pid}-{int(delmetting.tid)}-{int(delmetting.taskid)}"
                relationtasks = models.Task.objects.filter(relationid=session_id)
                if relationtasks.exists():
                    #刪除圖片
                    for relationtask in relationtasks:
                        delete_task_file(relationtask.inc_id)
                relationtasks.delete()
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
        topics = models.Task.objects.filter(docpath=instance.id,editionid='1')
        if topics.exists():
            for topic in topics:
                session_id =f"{topic.pid}-{int(topic.tid)}-{int(topic.taskid)}"
                conclusions = models.Task.objects.filter(relationid=session_id)
                if conclusions.exists():
                    #刪除圖片
                    for conclusion in conclusions:
                        delete_task_file(conclusion.inc_id)
            topics.delete()
        return True

#刪除文件
def delete_task_file(inc_id):
    taskfolder = models.Document.objects.filter(inc_id=inc_id).order_by('folderid')
    if taskfolder.exists():
        folder = taskfolder.values()[0]
        taskimage =  models.Docdetail.objects.filter(parentid=folder['parentid'],folderid=folder['folderid']).order_by('folderid')
        with transaction.atomic(ModelTools.get_database(models.Document)):  
            taskimage.delete()
            taskfolder.delete()
        


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








#meeting的Management單頭數據
class MeetingmanagerMastView(DatatablesServerSideView):
    model = models.Tpmast
    columns = '__all__'
    searchable_columns = ['tpmastid','deptid','deptname','tpno','tpname','category','tpdesc','sessionid','revisedby','t_stamp','inc_id','manager']

    def get_initial_queryset(self):
        # manager_list = list(models.Syspara.objects.filter(ftype='Show_Template_Type').values('fvalue'))
        # manager_list = manager_list[0]['fvalue'].split(';')
        # result = self.model.objects.filter(tpname__in=manager_list).order_by('tpmastid')
        manager = self.request.GET.get("manager")
        result = self.model.objects.all().order_by('tpmastid')
        if manager:
            result = result.filter(manager=manager).order_by('tpmastid')
        return result
    

#獲取改進模板下拉框值
def get_Improvement(request):
    '''
    try:
        # 定義要返回的對象
        result = {'status':False, 'msg':'', 'data':[]}
        manager = request.GET.get("manager",'')
        tpdesc = request.GET.get("tpdesc",'')
        if manager!='':
            datas = models.Tpmast.objects.filter(manager=manager)
            if tpdesc=='AreasofImprovementfor':
                tpdesc='Areas of Improvement for'
                datas = datas.filter(manager=manager,tpdesc__startswith=tpdesc)
            result['data'] =  list(datas.values())  # 把查詢出來的內容轉成list返回給控件
        result['status'] = True
    except Exception as e:
        print(str(e))
        result['status'] = False
    '''
    # 定義要返回的對象
    result = {'status':False, 'msg':'', 'data':[]}
    # 獲得下拉控件的valueField指定的字段
    searchfield = request.GET.get('field')
    # 獲得下拉控件輸入框輸入的值
    searchvalue = request.GET.get('searchvalue')
    # 獲得下拉控件明細的顯示記錄數
    count = int(request.GET.get('count'))
    # 獲得下拉控件的過濾條件
    filter = request.GET.get('filter')
    if filter==None or filter=='':   
        filter="TpDesc like 'Areas of Improvement for%%'"
    else:
        filter="1=1"
    try:
        datas=None
        # 當輸入框的值不為空時，根據輸入框的值進行查詢
        if searchvalue:  
            sqlWhere=['{0} and {1} like %s'.format(filter, searchfield)]            
            param=['%%{0}%%'.format(searchvalue)]
            datas = models.Tpmast.objects.extra(where=sqlWhere,params=param)[:count]
        else:
            datas = models.Tpmast.objects.extra(where=[filter])[:count]      
        result['status'] = True
        result['data'] =  list(datas.values())  # 把查詢出來的內容轉成list返回給控件
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)

#獲取議題下拉框值
def get_Improvement_item(request):
    # 定義要返回的對象
    result = {'status':False, 'msg':'', 'data':[]}
    # 獲得下拉控件的valueField指定的字段
    searchfield = request.GET.get('field')
    # 獲得下拉控件輸入框輸入的值
    searchvalue = request.GET.get('searchvalue')
    # 獲得下拉控件明細的顯示記錄數
    count = int(request.GET.get('count'))
    # 獲得下拉控件的過濾條件
    filter = request.GET.get('filter')
    if filter==None or filter=='':   
        filter="1<>1"
    try:
        datas=None
        # 當輸入框的值不為空時，根據輸入框的值進行查詢
        if searchvalue:  
            sqlWhere=['{0} and {1} like %s'.format(filter, searchfield)]            
            param=['%%{0}%%'.format(searchvalue)]
            datas = models.Tpdetail.objects.extra(where=sqlWhere,params=param).distinct()[:count]
        else:
            datas = models.Tpdetail.objects.extra(where=[filter]).distinct()[:count]      
        result['status'] = True
        result['data'] =  list(datas.values())  # 把查詢出來的內容轉成list返回給控件
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)

#獲取加分模板下拉框值
def get_credits(request):
    # 定義要返回的對象
    result = {'status':False, 'msg':'', 'data':[]}
    # 獲得下拉控件的valueField指定的字段
    searchfield = request.GET.get('field')
    # 獲得下拉控件輸入框輸入的值
    searchvalue = request.GET.get('searchvalue')
    # 獲得下拉控件明細的顯示記錄數
    count = int(request.GET.get('count'))
    # 獲得下拉控件的過濾條件
    filter = request.GET.get('filter','')
    if filter==None or filter=='':   
        filter="TpDesc like 'Areas of Credit for%%'"
    try:
        datas=None
        # 當輸入框的值不為空時，根據輸入框的值進行查詢
        if searchvalue:  
            sqlWhere=['{0} and {1} like %s'.format(filter, searchfield)]            
            param=['%%{0}%%'.format(searchvalue)]
            datas = models.Tpmast.objects.extra(where=sqlWhere,params=param)[:count]
        else:
            datas = models.Tpmast.objects.extra(where=[filter])[:count]      
        result['status'] = True
        result['data'] =  list(datas.values())  # 把查詢出來的內容轉成list返回給控件
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)


#meeting的Management單身數據
class MeetingmanagerDetailView(DatatablesServerSideView):
    model = models.Tpdetail
    columns = '__all__'
    searchable_columns = ['tpdetailid','tpmastid','tptname','contact','priority','status',
    'remark','revisedby','t_stamp','operate','cycletime','cycleperiod','day','invalid',
    'sessionid','tasktype','subtasktype','diff','inc_id']

    def get_initial_queryset(self):
        tpmastid = self.request.GET.get("tpmastid")
        # result = self.model.objects.filter(Q(tpmastid=tpmastid)&~Q(invalid='Y')).order_by('tpdetailid')
        result = self.model.objects.filter(tpmastid=tpmastid).order_by('tpdetailid')
        return result

#Tpdetail表SWUpdateView
def TpdetailView(request:HttpRequest):
    result = {'status':True, 'msg':'', 'data':[]}
    try:
        tpmastid = request.GET.get('tpmastid')#議題
        if not (tpmastid==None or tpmastid=='') :
            #按條件查詢相關議題
            meeting_items = models.Tpdetail.objects.filter(tpmastid=tpmastid)
            if meeting_items.exists():
                result['data'] = list(meeting_items.values())           
            else:       
                result['status'] = False  
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   



#根據議題獲取會議結論
def topic_get_metting(request:HttpRequest):
    '''
    功能描述：根據議題獲取會議結論
    '''
    #
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        topic = request.GET.get('topic')#議題
        if not (topic==None or topic=='') :
            #按條件查詢相關議題
            meeting_items = models.Task.objects.filter(task=topic,editionid='1').order_by('pid','tid','taskid')
            #獲取結論的pid-tid-taskid拼接字段列表
            session_id_list = [f'{item.pid}-{int(item.tid)}-{int(item.taskid)}' for item in meeting_items if item]
            #獲取所有議題下的結論
            metting_relationtask = models.Task.objects.filter(relationid__in=session_id_list,editionid='3').order_by('pid','tid','taskid','docpath')
            if metting_relationtask.exists():
                result['data'] = list(metting_relationtask.values())                  
                result['status'] = True  
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   


#修改會議ID
def update_meetingid(request:HttpRequest):
    '''
    功能描述：修改會議ID
    '''
    #
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        old_meetingid = request.POST.get('old_meetingid')#原會議ID
        new_meetingid = request.POST.get('new_meetingid')#新會議ID
        inc_id = request.POST.get('inc_id')#inc_id
        checked = request.POST.get('checked')#inc_id
        status,msg = update_meetingid_check(inc_id,new_meetingid,old_meetingid)
        if status==False:            
            result['status'] = status  
            result['msg'] = msg  
        else:
            if checked == 'false':
                meetingMaster = []
                meetingDetail = []
                #查詢關聯議題結論及轉後任務
                meetingD = models.Task.objects.filter(docpath=old_meetingid).values()
                for item in meetingD:
                    meetingDModel = models.Task()
                    ModelTools.set_basic_field_info(request, models.Task, meetingDModel)
                    meetingDModel.inc_id = item['inc_id']
                    meetingDModel.docpath = new_meetingid
                    meetingDetail.append(meetingDModel)
                #修改會議單頭單
                meetingM = models.Mettingmaster.objects.filter(inc_id=inc_id).values()
                for item in meetingM:
                    meetingMModel = models.Mettingmaster()
                    ModelTools.set_basic_field_info(request, models.Task, meetingMModel)
                    meetingMModel.inc_id = item['inc_id']
                    meetingMModel.id = new_meetingid
                    meetingMaster.append(meetingMModel)
                with transaction.atomic(using='MPMS'):
                    models.Task.objects.bulk_update(meetingDetail, fields=['docpath','modifier','modi_date'], batch_size=500)
                    models.Mettingmaster.objects.bulk_update(meetingMaster, fields=['id','modifier','modi_date'], batch_size=500)
            result['status'] = True  
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   



#檢驗修改會議ID是否合法
def update_meetingid_check(inc_id,new_meetingid,old_meetingid):
    result,msg = True,''
    if new_meetingid.strip( ' ' ) == old_meetingid.strip( ' ' ):
        result,msg = False,'新ID和舊ID相同'
    hasRecord = models.Mettingmaster.objects.filter(id=new_meetingid).exclude(inc_id=inc_id).exists()
    if hasRecord:
        result,msg = False,'已存在會議ID{0}'.format(new_meetingid)
    return result,msg




#將數據生成新議題和議題結論
def create_met_item(request:HttpRequest):
    def mutil_post_data(instance):
        try:
            with transaction.atomic(ModelTools.get_database(models.Task)):
                instance.save()
            return True
        except Exception as e:
            print(str(e))
        return False

    def save_data(request,instance):
        ModelTools.set_basic_field_info(request, models.Task, taskData)
        result = False
        save_qty = 0
        while save_qty < 5:
            if mutil_post_data(instance) == True:
                result = True
                break
            sleep(0.09)
            instance.taskid = instance.taskid + 10
            save_qty += 1
        return result
    '''
    功能描述：將數據生成新議題和議題結論
    '''
    #
    result = {'status':True, 'msg':'', 'data':[]}
    try:
        met_items = json.loads(request.POST.get('met_items'))#會議明細
        topic = request.POST.get('topic')#會議主題
        docpath = request.POST.get('docpath')#會議ID
        #獲取下標值，將值轉為int類型並排序
        indexlist = set([re.findall("\d+",key)[0] for key in met_items.keys() if len(re.findall("\d+",key))>0 ])
        indexlist = [int(i) for i in indexlist]
        indexlist.sort()
        indexlist = [str(i) for i in indexlist]
        Temple = models.Task.objects.filter(docpath=docpath,task=topic)
        url = AsyncioTools.get_url(request,"add_task", True)
        params = {"username":UserService.GetLoginUserName(request) }
        http_methods = [{'url':url+'?sessionid=11580-12', 'params':params}]
        datas = AsyncioTools.async_fetch_http_json(http_methods)   
        datas = datas[0]['data']
        relationid = ''
        taskid = None
        taskData = models.Task()
        if not Temple.exists():
            taskData.task =topic
            taskData.docpath = docpath
            taskData.editionid = '1'

            taskData.pid = datas['pid']
            taskData.tid = datas['tid']
            taskData.taskid = datas['taskid']
            taskData.contact = datas['contact']
            taskData.planbdate = datas['planbdate']
            taskData.planedate = datas['planedate']
            taskData.progress = datas['progress']
            taskData.requestdate = datas['requestdate']
            save_result = save_data(request,taskData)
            if not save_result:
                result['status'] = False  
                result['msg'] = '新增議題失敗！'  
        else:
            taskData = Temple.first()
        relationid = f"{taskData.pid}-{int(taskData.tid)}-{int(taskData.taskid)}"
        taskid = datas['taskid']
        if result['status']:
            for i  in indexlist:
                if 'ischeck_'+i in met_items.keys() and met_items['ischeck_'+i]=='on':
                    taskData = models.Task()
                    taskData.task = met_items['task_'+i]
                    if met_items['tasktype_'+i]!='':
                        taskData.tasktype = met_items['tasktype_'+i]
                    if met_items['tasktype_'+i]!='':
                        taskData.subtasktype = met_items['subtasktype_'+i]
                    if met_items['tasktype_'+i]!='':
                        taskData.diff = met_items['diff_'+i]

                    taskData.rank = i
                    taskData.docpath = docpath
                    taskData.editionid = '3'
                    taskData.relationid = relationid
                    taskData.pid = datas['pid']
                    taskData.tid = datas['tid']
                    taskData.taskid = taskid
                    taskData.contact = datas['contact']
                    taskData.planbdate = datas['planbdate']
                    taskData.planedate = datas['planedate']
                    taskData.progress = datas['progress']
                    taskData.requestdate = datas['requestdate']
                    taskid+=10
                    save_result = save_data(request,taskData)
                    if not save_result:
                        result['status'] = False  
                        result['msg'] = '新增議題結論失敗！'  
                        break
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   

def hasTopic(docpath,topic):
    Temple = models.Task.objects.filter(docpath=docpath,task=topic).exists()





            # datas['docpath'] = docpath
            # datas['editionid'] = '1'
            # datas['task'] = topic
            # http_methods = [{'url':url, 'params':datas,'method':'POST'}]
            # datas = AsyncioTools.async_fetch_http_json(http_methods)   


#檢驗某會議是否存在對應議題
def check_met_topic(request:HttpRequest):
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        topic = request.GET.get('topic')
        met_inc_id = request.GET.get('met_inc_id')
        Temple = models.Mettingmaster.objects.filter(inc_id=met_inc_id)
        if Temple.exists():
            Temple = Temple.first()
            TempleB = models.Task.objects.filter(docpath=Temple.id,task=topic,editionid='1')
            if TempleB.exists():
                result['data'] = list(TempleB.values())
                result['status'] = True
    except Exception as e:
        print(str(e))
        result['status'] = False
    return JsonResponse(result, safe=False)   







#meeting的會議議題
class MeetingTopicView(DatatablesServerSideView):
    model = models.Task
    columns = '__all__'
    searchable_columns = '__all__'
    
    def get_initial_queryset(self):
        modal = self.request.GET.get('modal','')
        if modal == 'dis_topic':
            #去重的議題結論
            queryset = models.Task.objects.filter(editionid='1').exclude(docpath='',docpath__isnull=False)
        else:
            queryset = models.Task.objects.all()
        return queryset




def get_requirement_task(request:HttpRequest):
    result = {'status':False, 'msg':'', 'data':None}
    sessionid = request.GET.get("sessionid")
    data = []
    try:
        session = sessionid.split("-")
        pid = session[0]
        tid = session[1]
        qs = models.VTask.objects.filter(pid=pid, tid=tid).order_by("taskid")
        data = list(qs.values())
        result['data'] = data
        result['status'] = True
    except Exception as e:
        LOGGER.error(e)
    return JsonResponse(result, safe=False)