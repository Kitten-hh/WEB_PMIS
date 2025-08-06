from django.http import JsonResponse,HttpRequest,FileResponse
from datetime import tzinfo,timedelta
from BaseApp.library.tools import DateTools
from WEB_PMIS.tools import RestApiUtils #引入工具類
from django.conf import settings #引入settings文件配置信息
import base64
from BaseApp.library.serializer.json import DjangoJSONBinaryEncoder
import json
from django.http import HttpResponse
from django.utils.encoding import escape_uri_path
from BaseApp.library.tools.PdfTools import convert_to_pdf
import base64
import io
from zhconv import convert
from django import dispatch
from django.conf import settings
from BaseApp.library.tools import AsyncioTools
import concurrent.futures
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie

# Define a custom signal
sync_system_bug_signal = dispatch.Signal(providing_args=["rp017"])

# Receiver function for the signal
@dispatch.receiver(sync_system_bug_signal)
def sync_system_bug_receiver(sender, **kwargs):
    rp017 = kwargs.get('rp017')
    url = "{0}{1}".format(settings.PMIS_REST_API_SERVER_NEW, settings.PMIS_RESTAPI_ENDPOINT['synctaskissuedata']['url'])
    methodType = settings.PMIS_RESTAPI_ENDPOINT['synctaskissuedata']['method']
    authUserName = settings.PMIS_REST_API_USERNAME
    authPasswrod = settings.PMIS_REST_API_PASSWORD

    http_methods = {
        'data': {
            "url": url,
            "method": methodType,
            "basic_auth_user": authUserName,
            "basic_auth_password": authPasswrod,
            "params": {'rp017': rp017}
        }
    }

    def async_request():
        try:
            response = AsyncioTools.async_fetch_http_json(http_methods)['data']
            print("Sync successful:", response)
        except Exception as e:
            print("Sync failed:", str(e))

    # Run the request in a separate thread to ensure non-blocking behavior
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(async_request)

class UTC(tzinfo):
    def __init__(self, offset=0):
        self._offset = offset
    def utcoffset(self, dt):
        return timedelta(hours=self._offset)
    def tzname(self, dt):
        return "UTC + %s" % self._offset
    def dst(self, dt):
        return timedelta(hours=self._offset)

#獲取系統問題上報關聯任務信息
def get_taskRelation(request):
    rp024 = get_param_value(request, 'rp024')
    url = '/pms/get_taskrelation'
    args = {'rp024':rp024}
    result = get_restapi_data(url,args,'GET').get('get_data')
    return JsonResponse(result, safe=False)

#下載系統問題上報附件
def download_file(request):
    inc_id = get_param_value(request, 'inc_id')
    url = '/pms/download_file'
    args = {'inc_id':inc_id}
    result = get_restapi_data(url,args,'GET').get('get_data')
    if not result['rq006']:
        return HttpResponse(status=404) #當不存在對應文件時返回404
    # 創建相應對象，並設置內容類型和內容
    response = HttpResponse(base64.b64decode(result['rq006']), content_type=result['rq007']) #文件,文件類型
    # 若不是圖片或要求下載則直接下載文件
    response.__setitem__("Content-Disposition", "rq006;filename="+escape_uri_path(result['rq005'])) #文件名字
    return response

#預覽系統問題上報附件
def preview_file(request):
    def file_type(file_name: str) -> str:
        """ 根据文件名获取文件的扩展名 """
        parts = file_name.rsplit('.', 1)   # 在最後一個點處分割文件名。
        if len(parts) > 1:
            return parts[-1].lower()   # 如果存在擴展名，則返回小寫的擴展名。
        return None  # 如果沒有擴展名，則返回 None。

    inc_id = request.GET.get('inc_id')
    url = '/pms/download_file'
    args = {'inc_id': inc_id}
    result = get_restapi_data(url, args, 'GET').get('get_data')  # 調用 RestApi 並獲取數據。

    if not result or not result.get('rq006'):
        # 如果沒有找到數據或缺少 'rq006' 鍵，返回 404 響應。
        return HttpResponse("No file found or invalid request.", status=404)

    file_data = base64.b64decode(result['rq006'])  # 解碼 base64 編碼的文件數據。
    file_name = result['rq005']  # 從結果中檢索文件名。
    extension = file_type(file_name)  # 獲取文件擴展名。

    file_stream = io.BytesIO(file_data)  # 從文件數據創建一個字節流。

    # 根據文件擴展名確定響應。
    if extension in ['pdf']: # 如果文件是PDF,則直接返回到頁面預覽
        return HttpResponse(file_stream, content_type='application/pdf')
    elif extension in ['doc', 'docx', 'xls', 'xlsx']: # 如果文件是這幾種類型,則直接下載
        return FileResponse(file_stream, as_attachment=True, filename=file_name)
    elif extension in ['png', 'jpg', 'jpeg', 'gif', 'bmp']: # 如果文件是圖片,則直接返回到頁面預覽
        return HttpResponse(file_stream, content_type=f'image/{extension}')
    else:
        # 如果文件類型不支持，返回 400 響應。
        return HttpResponse('Unsupported file type', status=400)

#刪除系統問題上報附件信息
# def admrqDelete(request):
#     jsonData = json.loads(request.body.decode('utf-8'))
#     args = jsonData['pk']
#     url = '/pms/admrq/{0}/'.format(args)
#     result = get_restapi_data(url,args,'DELETE').get('get_data')
#     return JsonResponse(result, safe=False)

#查詢系統問題上報附件信息列表
def get_systemBugFile(request):
    rq002 = get_param_value(request, 'rq002')
    rq007 = get_param_value(request, 'rq007')
    url = '/pms/get_systembugfile'
    args = {'rq002':rq002,'rq007':rq007}
    result = get_restapi_data(url,args,'GET').get('get_data')
    return JsonResponse(result, safe=False)

#查詢問題跟進狀態列表信息
def get_taskItemTable(request):
    url = '/pms/taskitem_table/'
    method = 'GET'
    result = get_datatable(request,url,method)
    return JsonResponse(result,safe=False)

#查詢關聯任務進度
def get_vtaskTable(request):
    url = '/pms/vtask_table/'
    method = 'GET'
    result = get_datatable(request,url,method)
    return JsonResponse(result,safe=False)

#新增任务信息
def taskCreate(request):
    url = '/pms/task/'
    args = {key: request.POST[key] for key in request.POST.keys()}
    set_basic_field_info(request,args)
    # args['rp002'] = DateTools.formatf(DateTools.now().astimezone(UTC(8)), '%Y-%m-%d %H:%M:%S')
    args['create_date'] = DateTools.formatf(DateTools.now().astimezone(UTC(8)), '%Y%m%d')
    args['modi_date'] = DateTools.formatf(DateTools.now().astimezone(UTC(8)), '%Y%m%d%H%M')
    result = get_restapi_data(url,args,'POST').get('get_data')

    return JsonResponse(result, safe=False)

#获取用户列表
def get_userTable(request):
    url = '/pms/users/'
    method = 'GET'
    result = get_datatable(request,url,method)
    return JsonResponse(result,safe=False)

#查詢窗體所屬工程
def getDefaultPro(request):
    result = {'status':True,'msg':'','sc005':'','sc008':''}
    formname = get_param_value(request, 'formname')
    url = '/pms/get_defaultpro'
    args = {'formname':formname}
    result = get_restapi_data(url,args,'GET').get('get_data')
    return JsonResponse(result, safe=False)

#設置默認工程(已存在數據則執行修改操作,不存在則執行新增操作)
def pmsutSave(request):
    result = {'status':True,'msg':'','data':''}
    ut001 = get_param_value(request, 'ut001')
    ut002 = get_param_value(request, 'ut002')
    ut003 = get_param_value(request, 'ut003')
    url = '/pms/pmsut_save'
    args = {'ut001':ut001,'ut002':ut002,'ut003':ut003}
    result = get_restapi_data(url,args,'POST').get('get_data')
    return JsonResponse(result, safe=False)

#獲取任務編號
def getTaskNo(request):
    pid = get_param_value(request, 'pid')
    tid = get_param_value(request, 'tid')
    url = '/pms/gettaskno'
    args = {'pid':pid,'tid':tid}
    result = get_restapi_data(url,args,'GET').get('get_data')
    return JsonResponse(result, safe=False)

#檢驗tid合法性
def checkTidExist(request):
    pid = get_param_value(request, 'pid')
    tid = get_param_value(request, 'tid')
    url = '/pms/checktidexist'
    args = {'pid':pid,'tid':tid}
    result = get_restapi_data(url,args,'GET').get('get_data')
    return JsonResponse(result, safe=False)

#檢驗pid合法性
def checkPidExist(request):
    pid = get_param_value(request, 'pid')
    url = '/pms/checkpidexist'
    args = {'pid':pid}
    result = get_restapi_data(url,args,'GET').get('get_data')
    return JsonResponse(result, safe=False)

#讀取用戶默認工程
def getUserDefaultProject(request):
    ut001 = get_param_value(request, 'ut001')
    url = '/pms/get_userdefaultproject'
    args = {'ut001':ut001}
    result = get_restapi_data(url,args,'GET').get('get_data')
    return JsonResponse(result, safe=False)

#獲取工程編號列表
def get_taskListTable(request:HttpRequest):
    url = '/pms/tasklist/'
    method = 'GET'
    result = get_datatable(request,url,method)
    return JsonResponse(result,safe=False)

#獲取工程列表
def get_projectTable(request:HttpRequest):
    url = '/pms/project/'
    method = 'GET'
    result = get_datatable(request,url,method)
    return JsonResponse(result,safe=False)

#查看問題記錄列表
def get_taskTable(request:HttpRequest):
    url = '/pms/task/'
    method = 'GET'
    result = get_datatable(request,url,method)
    return JsonResponse(result,safe=False)

#新增系統問題上報功能列表數據
def admrfCreate(request):
    url = '/pms/admrf/'
    args = {key: request.POST[key] for key in request.POST.keys()}
    result = get_restapi_data(url,args,'POST').get('get_data')
    return JsonResponse(result, safe=False)

#修改系統問題上報功能列表數據
def admrfUpdate(request):
    args = {key:request.POST[key] for key in request.POST.keys()}
    url = '/pms/admrf/{0}/'.format(args['inc_id'])
    result = get_restapi_data(url,args,'PUT').get('get_data')
    return JsonResponse(result, safe=False)

#刪除系統問題上報功能列表數據
def admrfDelete(request):
    args = {'pk':request.POST['inc_id']}
    url = '/pms/admrf/{0}/'.format(request.POST['inc_id'])
    result = get_restapi_data(url,args,'DELETE').get('get_data')
    return JsonResponse(result, safe=False)

#新增系統問題上報功能時獲取序號
def getAdmrfNo(request):
    result = {'status':True,'msg':None,'data':None}
    rf002 = get_param_value(request, 'rf002')
    url = '/pms/get_admrfno'
    args = {'rf002':rf002}
    try:
        result['data'] = get_restapi_data(url,args,'GET').get('get_data')
    except Exception as e:
        result['status'] = False
        print(str(e))
    return JsonResponse(result, safe=False)

#獲取系統問題上報table數據源
def get_admrfTable(request:HttpRequest):
    url = '/pms/admrf/'
    method = 'GET'
    result = get_datatable(request,url,method)
    return JsonResponse(result,safe=False)

#查詢圖片(多張)
def getImgArray(request):
    try:
        rq002 = get_param_value(request, 'rq002')
        rq007 = get_param_value(request, 'rq007')
        url = '/pms/get_imgarray'
        args = {'rq002':rq002,'rq007':rq007}
        result = get_restapi_data(url,args,'GET').get('get_data')
    except Exception as e:
        print(str(e))
    return JsonResponse(result,encoder=DjangoJSONBinaryEncoder, safe=False)

#上傳圖片(多張上傳)
def uploadImgArray(request):
    '''
    批量上傳用戶界面圖片,上傳時覆蓋已有記錄
    '''
    url = '/pms/upload_imgarray'
    args = {key: request.POST[key] for key in request.POST.keys()}
    for item in request.FILES:
        args[item] = base64.b64encode(request.FILES[item].read()).decode()
    result = get_restapi_data(url,args,'POST').get('get_data')
    return JsonResponse(result, safe=False)

#獲取系統問題上報圖片信息
def getAdmrqImg(request):
    try:
        rq002 = get_param_value(request, 'rq002')
        url = '/pms/get_admrqimg'
        args = {'rq002':rq002}
        result = get_restapi_data(url,args,'GET').get('get_data')
    except Exception as e:
        print(str(e))
    return JsonResponse(result, safe=False)

#獲取附件ID
def getAdmrqNo(request):
    try:
        rq002 = get_param_value(request, 'rq002')
        url = '/pms/get_admrqno'
        args = {'rq002':rq002}
        result = get_restapi_data(url,args,'GET').get('get_data')
    except Exception as e:
        print(str(e))
    return JsonResponse(result, safe=False)

#保存系統問題上報圖片信息
def admrqImgSave(request):
    url = '/pms/get_imgid'
    args = {"rq002":request.POST["rq002"]}
    data = get_restapi_data(url,args,'GET').get('get_data')
    args = {key: request.POST[key] for key in request.POST.keys()}
    file = request.FILES['rq003']
    args['rq003'] = base64.b64encode(file.read()).decode()
    args['rq004'] = data['rq004']
    type = "POST" #請求類型
    if data['inc_id']: #已存在數據則執行修改
        url = '/pms/admrq/{0}/'.format(data['inc_id'])
        type = "PUT"
    else: #不存在數據執行新增
        url = '/pms/admrq/'
    result = get_restapi_data(url,args,type).get('get_data')

    return JsonResponse(result, safe=False)

#新增附件信息
def admrqCreate(request):
    url = '/pms/admrq/'
    args = {key: request.POST[key] for key in request.POST.keys()}
    file = request.FILES['rq006']
    args['rq006'] = base64.b64encode(file.read()).decode()
    result = get_restapi_data(url,args,'POST').get('get_data')

    return JsonResponse(result, safe=False)

#獲取功能依賴對象列表
def get_moduleObjectArray(request):
    result = {'status':True,'msg':None,'data':None}
    moduleid = get_param_value(request, 'moduleid')
    url = '/pms/moduleobject_array'
    args = {}
    if moduleid:
        args = {"moduleid":moduleid}
    try:    
        result['data'] = get_restapi_data(url,args,'GET').get('get_data')
    except Exception as e:
        result['status'] = False
        print(str(e))
    return JsonResponse(result, safe=False)

#獲取窗體列表
def get_moduleArray(request):
    result = {'status':True,'msg':None,'data':None}
    parentid = get_param_value(request, 'parentid')
    url = '/pms/module_array'
    args = {}
    if parentid:
        args = {"parentid":parentid}
    try:    
        result['data'] = get_restapi_data(url,args,'GET').get('get_data')
    except Exception as e:
        result['status'] = False
        print(str(e))
    return JsonResponse(result, safe=False)

#獲取子工程項目table數據源
def get_subprojectTable(request):
    url = '/pms/subproject/'
    method = 'GET'
    result = get_datatable(request,url,method)
    return JsonResponse(result,safe=False)

#修改系統問題上報信息
def admrpUpdate(request):
    args = {key:request.POST[key] for key in request.POST.keys()}
    for file_key in request.FILES:
        args[file_key] = base64.b64encode(request.FILES[file_key].read()).decode()
    del args['rp002'] 
    args['modifier'] = request.user.username
    args['modi_date'] = DateTools.formatf(DateTools.now().astimezone(UTC(8)), '%Y%m%d%H%M')
    url = '/pms/admrp/{0}/'.format(args['inc_id'])
    result = get_restapi_data(url,args,'PUT').get('get_data')

    return JsonResponse(result, safe=False)

#獲取系統問題上報信息
def getMasterInfo(request):
    try:
        id = get_param_value(request, 'id')
        rp017 = get_param_value(request, 'rp017')
        url = '/pms/admrp/get'
        args = {'id':id,'rp017':rp017}
        result = get_restapi_data(url,args,'GET').get('get_data')
    except Exception as e:
        print(str(e))
    return JsonResponse(result, safe=False)

#刪除系統問題上報數據
def admrpDelete(request):
    args = {'pk':request.POST['inc_id']}
    url = '/pms/admrp/{0}/'.format(request.POST['inc_id'])
    result = get_restapi_data(url,args,'DELETE').get('get_data')

    return JsonResponse(result, safe=False)

#新增系統問題上報信息
def admrpCreate(request):
    url = '/pms/admrp/'
    args = {key: request.POST[key] for key in request.POST.keys()}
    for file_key in request.FILES:
        args[file_key] = base64.b64encode(request.FILES[file_key].read()).decode()
    set_basic_field_info(request,args)
    args['rp002'] = DateTools.formatf(DateTools.now().astimezone(UTC(8)), '%Y-%m-%d %H:%M:%S')
    args['create_date'] = DateTools.formatf(DateTools.now().astimezone(UTC(8)), '%Y%m%d')
    args['modi_date'] = DateTools.formatf(DateTools.now().astimezone(UTC(8)), '%Y%m%d%H%M')
    result = get_restapi_data(url,args,'POST').get('get_data')

    return JsonResponse(result, safe=False)

#新增時獲取系統問題上報單號
def getAdmrpNo(request):
    result = {'status':True,'msg':None,'data':None}
    id = get_param_value(request, 'id')
    url = '/pms/get_admrpno'
    args = {'id':id}
    try:
        result['data'] = get_restapi_data(url,args,'GET').get('get_data')
    except Exception as e:
        result['status'] = False
        print(str(e))
    return JsonResponse(result, safe=False)

#獲取部門信息
def get_cmsmeArray(request):
    result = {'status':True,'msg':None,'data':None}
    url = '/pms/cmsme_array'
    args = {}
    try:    
        result['data'] = get_restapi_data(url,args,'GET').get('get_data')
    except Exception as e:
        result['status'] = False
        print(str(e))
    return JsonResponse(result, safe=False)

def get_restapi_data(url, params,method):
    data = RestApiUtils.async_fetch_http_json({"get_data":{"url":settings.VC220_REST_API_SERVER + url, "params":params, "basic_auth_user":settings.VC220_REST_API_USERNAME, "basic_auth_password":settings.VC220_REST_API_PASSWORD,'method':method}})
    return data

def set_basic_field_info(request:HttpRequest, instance):
    basic_fields = ['COMPANY','USR_GROUP','CREATOR','CREATE_DATE','MODIFIER','MODI_DATE','FLAG']
    for field in basic_fields:
        name = field.lower();
        upper_name = field.upper()
        if upper_name == "USR_GROUP":
            if (request.user.is_active):
                instance[name] = request.user.username;
        elif upper_name == "CREATOR" and (not name in instance or not instance[name]):
            if (request.user.is_active):
                instance[name] = request.user.username
        elif upper_name == "CREATE_DATE" and (not name in instance or not instance[name]):
            instance[name] = DateTools.formatf(DateTools.now().astimezone(UTC(8)), '%Y-%m-%d %H:%M:%S')
        elif upper_name == "MODIFIER":
            if (request.user.is_active):
                instance[name] = request.user.username;
        elif upper_name == "MODI_DATE":
            instance[name] = DateTools.formatf(DateTools.now().astimezone(UTC(8)), '%Y-%m-%d %H:%M:%S')
        elif upper_name == "FLAG":
            old_flag = None
            if name in instance and instance[name]:
                old_flag = int(instance[name])
            if old_flag:
                if old_flag >= 999:
                    instance[name] = 1
                else:
                    instance[name] = old_flag + 1;
            else:
                instance[name] = 1

#通過RestApi獲取datatable數據源
def get_datatable(request,url,method):
    result = {'draw': 1, 'recordsTotal': 0, 'recordsFiltered': 0, 'data': []}
    try:    
        params = RestApiUtils.get_params(request,[])
        params.update(request.GET.dict())
        del params['location']
        data = get_restapi_data(url,  params,method)
        if "recordsTotal" in data['get_data']:
            result = data['get_data']
        else:
            result['data'] = data["get_data"].get('data',None) or data["get_data"].get('results', None)
            result['recordsFiltered'] = len(result['data'])
            result['draw'] = request.GET.get('draw')    
    except Exception as e:
        print(str(e))
    return result  


#獲取系統問題上報table數據源
def get_admrpTable(request:HttpRequest):
    url = '/pms/admrp/'
    method = 'GET'
    result = get_datatable(request,url,method)
    return JsonResponse(result,safe=False)

def get_param_value(request, param_name):
    value = None
    if param_name in request.GET:
        value = request.GET.get(param_name)
    return value

def get_solutiontypeTable(request:HttpRequest):
    url = '/pms/solutiontype/'
    method = 'GET'
    result = get_datatable(request,url,method)

    # 遍歷 result.data 中的每個項目並轉換 remark 字段為繁體
    if 'data' in result:
        for item in result['data']:
            if 'remark' in item and item['remark']:
                item['remark'] = convert(item['remark'], 'zh-hant')  # 將簡體轉為繁體 zh-hant
    
    return JsonResponse(result,safe=False)

def get_problemCategory(request:HttpRequest):
    """
    功能描述: 獲取問題類別(Problem Category)數據源
    """
    result = {'status':True,'msg':None,'data':[]}
    url = '/pms/get_problemcategory'
    args = {}
    try:    
        result['data'] = get_restapi_data(url,args,'GET').get('get_data')
    except Exception as e:
        result['status'] = False
        print(str(e))
    return JsonResponse(result, safe=False)

def get_flowChart(request:HttpRequest):
    """
    功能描述: 獲取系統問題上報流程圖數據源
    """
    result = {'status':True,'msg':None,'data':[]}
    url = '/pms/get_flowchart'
    admrpid = get_param_value(request, 'admrpid')
    args = {'admrpid':admrpid}
    try:    
        result['data'] = get_restapi_data(url,args,'GET').get('get_data')
    except Exception as e:
        result['status'] = False
        print(str(e))
    return JsonResponse(result, safe=False)

def get_flowChartInfo(request:HttpRequest):
    """
    功能描述: 根據流程圖編號獲取流程圖標題
    """
    result = {'status':True,'msg':None,'data':[]}
    url = '/pms/get_flowchartinfo'
    id = get_param_value(request, 'id')
    args = {'id':id}
    try:    
        result['data'] = get_restapi_data(url,args,'GET').get('get_data')
    except Exception as e:
        result['status'] = False
        print(str(e))
    return JsonResponse(result, safe=False)

def flowchart_create(request:HttpRequest):
    """
    功能描述: 新增上報流程圖
    """
    url = '/pms/salcflowchart/'
    args = {key: request.POST[key] for key in request.POST.keys()}
    result = get_restapi_data(url,args,'POST').get('get_data')
    return JsonResponse(result, safe=False)

def flowchart_update(request:HttpRequest):
    """
    功能描述: 修改上報流程圖
    """
    args = {key:request.POST[key] for key in request.POST.keys()}
    url = '/pms/salcflowchart/{0}/'.format(args['inc_id'])
    result = get_restapi_data(url,args,'PUT').get('get_data')
    return JsonResponse(result, safe=False)

def flowchart_delete(request:HttpRequest):
    """
    功能描述: 刪除上報流程圖
    """
    args = {'pk':request.POST['inc_id']}
    url = '/pms/salcflowchart/{0}/'.format(request.POST['inc_id'])
    result = get_restapi_data(url,args,'DELETE').get('get_data')
    return JsonResponse(result, safe=False)

def get_docmhTable(request):
    """
    功能描述: 獲取窗口文檔功能列表數據源
    """
    url = '/pms/docmh/'
    method = 'GET'
    result = get_datatable(request,url,method)
    return JsonResponse(result,safe=False)

def fetchSysBugTable(request):
    """
    功能描述: 根據用戶錄入的自然語言用AI查詢
    """
    result = {}
    url = '/pms/get_sysbugtable'
    question = get_param_value(request, 'question')
    condition = get_param_value(request, 'condition')
    args = {'question':question,'inc_id':condition}
    try:    
        result = get_restapi_data(url,args,'GET').get('get_data')
    except Exception as e:
        print(str(e))
    return JsonResponse(result, safe=False)

def execute_sql(request):
    """
    功能描述: 檢驗sql是否能執行
    """
    result = {}
    url = '/pms/execute_sql'
    data = json.loads(request.body)
    sql_query = data.get('sql', '')
    args = {'sql':sql_query}
    try:    
        result = get_restapi_data(url,args,'GET').get('get_data')
    except Exception as e:
        print(str(e))
    return JsonResponse(result, safe=False)

#獲取Session模塊table數據源
def get_flowChart(request:HttpRequest):
    """
    功能描述: 獲取系統問題上報流程圖數據源
    """
    result = {'status':True,'msg':None,'data':[]}
    url = '/pms/get_flowchart'
    admrpid = get_param_value(request, 'admrpid')
    args = {'admrpid':admrpid}
    try:    
        result['data'] = get_restapi_data(url,args,'GET').get('get_data')
    except Exception as e:
        result['status'] = False
        print(str(e))
    return JsonResponse(result, safe=False)


def get_vtasklist(request):
    """
    功能描述: 獲取Session列表數據源
    """
    result = {'status':True,'msg':None,'data':[]}
    url = '/pms/get_vtasklist'
    recordid = get_param_value(request, 'recordid')
    args = {'recordid':recordid}
    try:    
        result['data'] = get_restapi_data(url,args,'GET').get('get_data')
    except Exception as e:
        result['status'] = False
        print(str(e))
    return JsonResponse(result, safe=False)


@ensure_csrf_cookie
def refresh_csrf(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})



