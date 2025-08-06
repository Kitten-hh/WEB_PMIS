from math import fabs
from django.db.models.expressions import F
from django.shortcuts import render,redirect
from django.http import HttpRequest,JsonResponse,HttpResponse
from BaseApp.library.tools import DateTools,SWTools
from PMIS.Services.SessionService import SessionService
from DataBase_MPMS import models
import json
from django.db.models import Sum,Count,Max,Min,Avg,Q
from django.db.models.functions import Concat
from django.db.models import Value
from django.core.serializers.json import DjangoJSONEncoder
import timeago
import datetime
import re
import base64

def session_list(request:HttpRequest):
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        recordid = request.GET.get("recordid")
        period = "{0}-{1}".format(DateTools.formatf(DateTools.now(), '%Y'), DateTools.getQuarter(DateTools.now()))
        start_date, end_date = SessionService.get_quarterly_date(period)        
        sessions = SessionService.search_sessioni(contact=None, recordid=recordid, period=period, allcontact=None, stype=None, desc=None)            
        data = []
        for session in sessions:
            data.append({"sessionid":session['sessionid'], "sdesp":session['sdesp'], 'planbdate':session['planbdate'], 'planedate':session['planedate']})
        result['data'] = data;
        result['status'] = True
    except Exception as e:
        print(str(e))
    return JsonResponse(result, safe=False)
    
def questionDocWithChatgpt(request:HttpRequest):
    ids = request.GET.get("ids")
    if ids:
        ids = ids.split(",")
        taskfolder = models.Document.objects.filter(inc_id__in=[ids[0]])
        if len(taskfolder) > 0:
            taskfolder = taskfolder.values()[0]
            doc = models.Docdetail.objects.filter(parentid=taskfolder['parentid'], folderid=taskfolder['folderid']).order_by('folderid').values()[0]
            docInfo = {'name':taskfolder['docname'], 'type':taskfolder['mediatype'], 'content':base64.b64encode(doc['content']).decode('utf-8')}
            return SWTools.redirectLangChain(docInfo)
    else:
        return HttpResponse(status=404)

def get_frame_data(request):
    result = {'status': False, 'msg': '', 'data': {'framedata': [], 'framedictionary': {}}}
    try:
        frame_name = request.GET.get('frameName', None)
        # frame_version = request.GET.get('frameVersion', None)

        if frame_name :
             # 获取 DOCMC 表中 MC002 最大的那一条记录作为 frame_version
            latest_docmc_record = models.Docmc.objects.filter(mc001=frame_name).order_by('-mc002').first()
            if latest_docmc_record:
                frame_version = latest_docmc_record.mc002  # 使用获取到的 mc002 作为 frame_version

                # 查询 DOCMA 表
                docma_records = models.Docma.objects.filter(ma001=frame_name, ma002=frame_version).values()
                docma_data = list(docma_records) if docma_records.exists() else []

                # 查询 DOCMB 表
                # docmb_records = models.Docmb.objects.filter(mb001=frame_name, mb002=frame_version).values(
                #     'company', 'creator', 'usr_group', 'create_date', 'modifier', 'modi_date', 'flag',
                #     'mb001', 'mb002', 'mb003', 'mb004', 'mb005', 'mb006', 'mb007', 'mb008', 'mb009',
                #     'mb010', 'mb011', 'mb013', 'mb015', 'mb016', 'mb017', 'inc_id'
                # )

                docmb_records = models.Docmb.objects.filter(mb001=frame_name, mb002=frame_version).values(
                    'mb007','mb015'
                )

                docmb_data =[
                            {
                                '对应的功能序号': mb_record['mb015'] if mb_record['mb015'] else "未定义",
                                '操作说明': mb_record['mb007']
                            } for mb_record in docmb_records
                        ]

                # 查询 DOCMC 表
                # docmc_records = models.Docmc.objects.filter(mc001=frame_name, mc002=frame_version).values()
                # docmc_data = list(docmc_records) if docmc_records.exists() else []

                # 查询 DOCMD 表
                # docmd_records = models.Docmd.objects.filter(md001=frame_name, md002=frame_version).values()
                # docmd_data = list(docmd_records) if docmd_records.exists() else []

                # 查询 DOCME 表
                # docme_records = models.Docme.objects.filter(me001=frame_name, me002=frame_version).values()
                # docme_data = list(docme_records) if docme_records.exists() else []

                # 查询 DOCMH 表
                # docmh_records = models.Docmh.objects.filter(mh001=frame_name, mh002=frame_version).values()
                docmh_records = models.Docmh.objects.filter(mh001=frame_name, mh002=frame_version).values('mh003','mh004','mh005')
                docmh_data =  [
                                {
                                    '序号': mh_record['mh003'],
                                    '描述': mh_record['mh004'],
                                    '类别': mh_record['mh005']
                                } for mh_record in docmh_records
                            ]

                # 查询 DOCMI 表
                # docmi_records = models.Docmi.objects.filter(mi001=frame_name, mi002=frame_version).values()
                # docmi_data = list(docmi_records) if docmi_records.exists() else []

                # 将查询到的所有数据平级放入 framedata 中
                result['data']['framedata'] = {
                    'DOCMA': docma_data,
                    '操作': docmb_data,
                    # 'DOCMC': docmc_data,
                    # 'DOCMD': docmd_data,
                    # 'DOCME': docme_data,
                    '功能': docmh_data,
                    # 'DOCMI': docmi_data
                }

                # 调用 get_frame_dictionary 函数，获取 framedictionary 数据
                frame_dictionary_response = get_frame_dictionary(request)
                frame_dictionary_data = frame_dictionary_response.content.decode('utf-8')  # 获取并解析 JSON 数据
                frame_dictionary_json = json.loads(frame_dictionary_data)

                # 将字典数据放入 framedictionary 中
                result['data']['framedictionary'] = frame_dictionary_json.get('data', {})

                result['status'] = True
            else:
                result['msg'] = "No records found for the given frameName in DOCMC"
        else:
            result['msg'] = "Missing frameName parameter"

    except Exception as e:
        result['msg'] = str(e)

    return JsonResponse(result, safe=False)


def get_frame_dictionary(request):
    result = {'status': False, 'msg': '', 'data': {}}
    try:
        # 初始化返回的數據結構
        frame_data = {
            "ADMMC": {
            },
            "ADMMD": {
            }
        }
        # 查詢 ADMMD 表
        field=['ADMMC','ADMMD','DOCMA', 'DOCMC']
        admmd_records = models.Admmd.objects.using('DataDictionaryDSCSYS').filter(md001__in=field).values()
        if admmd_records.exists():
            for record in admmd_records:
                frame_data['ADMMD'][record['md001']] = record

        # 查詢 ADMMC 表
        admmc_records = models.Admmc.objects.using('DataDictionaryDSCSYS').filter(mc001__in=field).values()
        if admmc_records.exists():
            for record in admmc_records:
                frame_data['ADMMC'][record['mc001']] = record

        # 設置返回結果
        result['data'] = frame_data
        result['status'] = True

    except Exception as e:
        result['msg'] = str(e)

    return JsonResponse(result, safe=False)

