from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from DataBase_PMSDSCSYS.models import System
from DataBase_MPMS.models import Testingnotes, Docma, Docmh
from BaseApp.library.tools.SWTools import convert_list_tree
from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
from BaseApp.library.cust_views.SpecialDatatablesServerSideView import SpecialDatatablesServerSideView
from BaseApp.library.cust_views.SWCreateView import SWCreateView
from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from BaseApp.library.cust_views.SWDeleteView import SWDeleteView
from BaseApp.library.tools import ModelTools
from django.db.models import Max, F, IntegerField
from django.db.models.functions import Cast
import pandas as pd
import xlwt
from openpyxl import Workbook

def get_system_tree(request):
    '''
    功能描述: 獲取system的樹狀圖
    '''
    result = {'status': False, 'msg': '', 'data': []}
    try:
        qs = list(System.objects.all().values())
        result['data'] = convert_list_tree(
            qs, 'sysid', "parentid", check_root, convert_func)
    except Exception as e:
        print(e)
        result['msg'] = e
    return JsonResponse(result, safe=False)


def check_root(data):
    if data['parentid'] == "":
        return True
    else:
        return False


def convert_func(data):
    data['icon'] = ""
    data['name'] = data['sysremark']
    return data


class TestingNotesTable(SpecialDatatablesServerSideView):
    str_sql = """Select A.*,B.MA003 from TestingNotes A
        left join DOCMA B
        on A.FrmNo = B.MA001 and B.MA002 = (Select Max(MA002) from DOCMA where MA001 = B.MA001)
    """
    database = ModelTools.get_database(Testingnotes)
    columns = '__all__'
    searchable_columns = ['frmno', 'funcdesc', 'state',
                          'question', 'testdata', 'testresult', 'creator']

    def get_initial_queryset(self):
        if 'sysid' in self.request.GET:
            sysid = self.request.GET.get('sysid')
            self.str_sql += ' where sysid = \'%s\'' % sysid
        return super().get_initial_queryset()


class TestingNotesCreate(SWCreateView):
    model = Testingnotes

    def get_initial(self, instance):
        self.set_max_seqno(instance)

    def set_max_seqno(self, instance):
        sysid = self.request.GET.get('sysid')
        frmno = self.request.GET.get('frmno')
        if frmno == "":
            return
        itemno__max = Testingnotes.objects.filter(sysid=sysid, frmno=frmno).annotate( 
            itemno_field=Cast(F('itemno'), IntegerField())).aggregate(Max("itemno_field"))[
            "itemno_field__max"]
        instance.itemno = int(itemno__max or 0) + 1

    def save_check(self, instance):
        check_data = Testingnotes.objects.filter(
            sysid=instance.sysid, frmno=instance.frmno, funcitemno=instance.funcitemno)
        if check_data.exists():
            return False, f"當前系統{instance.sysid}中的窗口{instance.frmno}功能序號{instance.funcitemno}已存在"
        else:
            return True, ""

class TestingNotesUpdate(SWUpdateView):
    model = Testingnotes

class TestingNotesDelete(SWDeleteView):
    model = Testingnotes


def get_sys_frm(request):
    res = {'status': False, 'msg':'', 'data': None}
    sysid = request.GET.get('sysid')
    ma003_list = Docma.objects.filter(ma004=sysid).values('ma003', 'ma001').distinct()
    res['data'] = list(ma003_list)
    res['status'] = True
    return JsonResponse(res)

def get_template_excel(request):
    ma001 = request.GET.get('ma001')
    ma002 = Docma.objects.filter(ma001=ma001).aggregate(ma002_max=Max('ma002'))['ma002_max']
    rows = list(Docmh.objects.filter(mh001=ma001, mh002=ma002).values('mh001','mh003','mh004','mh005'))

    # 创建Workbook
    wb = Workbook()
    ws = wb.active  # 激活默认工作表

    # 定义表头，假设前面的字段是从模型中获取的，后面的字段留空
    head_fields = ['窗口', '功能序号', '功能描述', '功能类别', '是否测试', '测试数据', '测试操作与结果', '问题']
    
    # 写入表头
    ws.append(head_fields)
    
    # 填充数据并为特定字段留白
    for row in rows:
        # 这里构造一个新的行列表，后面4个字段留白
        row_data = list(row.values()) + [''] * 4  # 假设前面4个字段是模型数据，后面4个留空
        ws.append(row_data)

    # 设置HTTP响应
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="export.xlsx"'

    # 保存Workbook到响应中
    wb.save(response)

    return response

def upload_excel(request):
    res = {'status': False, 'data': "", 'msg': ''}
    file = request.FILES.get('excelFile')
    sysid = request.POST.get('sysid')
    if not file:
        res['msg'] = '沒有傳入Excel文件'
        return JsonResponse(res)
    try:
        excel_data = pd.read_excel(file.file.read())
    except:
        res['msg'] = '傳入Excel文件格式存在問題,請下載標準模板'
        return JsonResponse(res)
    excel_data = excel_data.fillna('')
    excel_list = excel_data.values.tolist()
    first_status = all(sublist[0] == excel_list[0][0] for sublist in excel_list)
    if not first_status:
        res['msg'] = '文件中導入的不是同一個窗口的測試數據'
        return JsonResponse(res)
    # 檢查上傳的Excel文檔的窗口編號是否在此系統中
    docma = Docma.objects.filter(ma004=sysid, ma001=excel_list[0][0])
    if not docma.exists():
        res['msg'] = '文件中的窗口不屬於選中的系統.'
        return JsonResponse(res)
    ''' 
        sysid, itemno, frmno, funcitemno, funcdesc, functype, state, testdata, testresult, question 
        系統名稱, 序號, 文檔編號, 功能序號, 功能描述, 功能類別, 是否測試, 測數數據, 測試操作與結果,問題
    '''
    fields = ['frmno', 'funcitemno', 'funcdesc', 'functype', 'state', 'testdata', 'testresult', 'question'] 
    excel = [dict(zip(fields,d)) for d in excel_list]
    max_itemno = Testingnotes.objects.filter(sysid=sysid, frmno=excel_list[0][0]).annotate(
        itemno_as_int=Cast('itemno', output_field=IntegerField())
    ).aggregate(max_itemno=Max('itemno_as_int')).get('max_itemno')
    itemno = int(max_itemno or 0) + 1
    notes = []
    for row in excel:
        note = Testingnotes()
        note.sysid = sysid
        note.itemno = itemno
        note.frmno = row['frmno']
        note.funcitemno = row['funcitemno']
        note.funcdesc = row['funcdesc']
        note.functype = row['functype']
        note.state = row['state']
        note.testdata = row['testdata']
        note.testresult = row['testresult']
        note.question = row['question']
        itemno += 1
        notes.append(note)
    try:
        Testingnotes.objects.bulk_create(notes)
    except:
        res['msg'] = 'Excel上傳失敗'
    res['status'] = True
    return JsonResponse(res)