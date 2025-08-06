from DataBase_MPMS.models import Document, Docdetail
from django.http import HttpRequest, JsonResponse
from .View_Session import session_list
from django.db.models import Q, Max
import json

def getDesignDOC(request):
    res = {'status': False, 'msg': '', 'data': []}
    recordid = request.GET.get('recordid', '')
    if recordid == '':
        res['msg'] = '沒有傳入recordid'
        return JsonResponse(res)
    session_list_request = HttpRequest()
    session_list_request.GET['recordid'] = recordid 
    session_list_response = session_list(session_list_request)
    session_list_data = json.loads(session_list_response.content.decode('utf-8')).get('data', [])
    if len(session_list_data) == 0:
        res['msg'] = 'recordid沒有查詢到對應的session'
        return JsonResponse(res)
    design_session = []
    for session in session_list_data:
        if str(session['sdesp'] or '') == '': continue
        if 'design' not in str(session['sdesp']).lower(): continue
        design_session.append(session['sessionid'])
    q = Q()
    q.connector = 'OR'
    for ds in design_session:
        if type(ds) != str: continue
        if str(ds or '') == '': continue
        if '-' not in str(ds or ''): continue
        pid, tid = ds.split('-')
        q1 = Q()
        docid = str(pid) + str(tid)
        folder_name = str(pid) + '-' + str(tid)
        q1.children.append(('docid__contains', docid))
        q1.children.append(('foldername__contains', folder_name))
        q.children.append(q1)
    # 每個任務相同名稱的文件只會取最新上傳的文檔-xmm
    max_folder_ids = Document.objects.filter(q).values('foldername', 'docname').annotate(max_date = Max('t_stamp'))
    filter = Q()
    filter.connector = 'OR'
    for folder in max_folder_ids:
        filter_and = Q()
        filter_and.children.append(('foldername', folder.get('foldername')))
        filter_and.children.append(('t_stamp', folder.get('max_date')))
        filter.children.append(filter_and)
    # ------
        
    if filter:
        doc = Document.objects.filter(filter)
        res['data'] = list(doc.values())
        res['status'] = True
    return JsonResponse(res, safe=False)