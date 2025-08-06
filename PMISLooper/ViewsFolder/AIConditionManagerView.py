from ScheduleApp.models import Promtsql,PromptcategoryTbl
from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
from BaseApp.library.cust_views.SWCreateView import SWCreateView
from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from BaseApp.library.cust_views.SWDeleteView import SWDeleteView
from django.db.models import Count, Q, Case, Sum, When, IntegerField, Max, F, Avg, Min
from datetime import datetime
import json
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _



class PromtsqlTableView(DatatablesServerSideView):
    model = Promtsql  # 綁定的 Model
    columns = "__all__"   # 顯示的字段
    searchable_columns = ['ssid', 'sname', 'ssql', 'category','promptbyai']  # 可查詢的字段

    def prepare_results(self, qs):
        json_data = []
        # 將 categoryno 和 category 的映射存儲到字典中
        mapping = {str(item['categoryno']): item['category'] for item in PromptcategoryTbl.objects.all().values('categoryno', 'category')}
        
        # 遍歷 queryset，處理每個對象
        for cur_object in qs:
            # 生成包含字段名和對應數據的字典
            retdict = {fieldname: self.render_column(cur_object, fieldname) for fieldname in self.columns}
            
            # 確保 category 不為 None 並在映射中有對應的值，將 category 轉換為字符串進行查找
            if cur_object.category is not None and str(cur_object.category) in mapping:
                retdict['categoryname'] = mapping[str(cur_object.category)]
            else:
                retdict['categoryname'] = None  # 或者使用默認值

            # 將結果添加到 json_data 列表中
            json_data.append(retdict)
        
        return json_data

class PromtsqlCreateView(SWCreateView):
    model = Promtsql

    def get_initial(self, instance):
        '''
        功能描述：Http Get 訪問時初始化model新增時的數據
        參數說明:
            instance:該model的實例
        '''
        instance.isai = ''
        instance.isapproved = ''
        instance.isdatabasesql = ''
        instance.category = ''
        instance.sname = ''
        instance.promptbyai = ''
        instance.ssid = self.set_max_seqno()

    def save_supplement(self, instance):
        '''
        功能描述:保存時設置默認值
        參數說明:
            instance:需要保存的model實例
        '''
        instance.ssid = self.set_max_seqno()
        instance.timestamp = datetime.now()
    
    def set_max_seqno(self):
        max_ssid = Promtsql.objects.aggregate(Max('ssid'))['ssid__max']
        pk = 10
        if max_ssid:
            pk = int(max_ssid) + 10
        return pk

class PromtsqlUpdateView(SWUpdateView):
    model = Promtsql

    def before_save(self, instance):
        '''
        功能描述：保存前的操作
        參數說明:
            instance:本model實例
        '''
        instance.timestamp = datetime.now()

# class PromtsqlDeleteView(SWDeleteView):
#     model = Promtsql

def batch_delete(request):
    """
    功能描述: 批量刪除AI條件
    """
    try:
        # 解析前台發來的JSON數據
        jsonData = json.loads(request.body.decode('utf-8'))
        details_Array = jsonData.get('details', [])
        # 提取inc_id屬性列表
        inc_ids = [item['inc_id'] for item in details_Array if 'inc_id' in item]
        # 批量刪除符合inc_id的數據
        deleted_count, rows = Promtsql.objects.filter(inc_id__in=inc_ids).delete()
        message_template = _('Successfully deleted {deleted_count} records')
        message = str(message_template).format(deleted_count=deleted_count)
        return JsonResponse({'status': True, 'msg':message}, safe=False) # 成功刪除了{deleted_count}條記錄
    except Exception as e:
        return JsonResponse({'status': False, 'msg': _('Error occurred during deletion: ') + str(e)}, safe=False) # 刪除過程中出錯
    
class PromptcategoryTblTableView(DatatablesServerSideView):
    model = PromptcategoryTbl  # 綁定的 Model
    columns = "__all__"   # 顯示的字段
    searchable_columns = ['categoryno', 'category', 'remark']  # 可查詢的字段


class PromptcategoryTblCreateView(SWCreateView):
    model = PromptcategoryTbl

    def get_initial(self, instance):
        '''
        功能描述：Http Get 訪問時初始化model新增時的數據
        參數說明:
            instance:該model的實例
        '''
        instance.categoryno = self.set_max_seqno()
        instance.category = ''
        instance.remark = ''

    def save_supplement(self, instance):
        '''
        功能描述:保存時設置默認值
        參數說明:
            instance:需要保存的model實例
        '''
        instance.categoryno = self.set_max_seqno()
    
    def set_max_seqno(self):
        max_categoryno = PromptcategoryTbl.objects.aggregate(Max('categoryno'))['categoryno__max']
        pk = 10
        if max_categoryno:
            pk = int(max_categoryno) + 10
        return pk

class PromptcategoryTblUpdateView(SWUpdateView):
    model = PromptcategoryTbl


def category_batch_delete(request):
    """
    功能描述: 批量刪除類別信息
    """
    try:
        # 解析前台發來的JSON數據
        jsonData = json.loads(request.body.decode('utf-8'))
        details_Array = jsonData.get('details', [])
        # 提取inc_id屬性列表
        inc_ids = [item['inc_id'] for item in details_Array if 'inc_id' in item]
        # 批量刪除符合inc_id的數據
        deleted_count, rows = PromptcategoryTbl.objects.filter(inc_id__in=inc_ids).delete()
        message_template = _('Successfully deleted {deleted_count} records')
        message = str(message_template).format(deleted_count=deleted_count)
        return JsonResponse({'status': True, 'msg':message}, safe=False) # 成功刪除了{deleted_count}條記錄
    except Exception as e:
        return JsonResponse({'status': False, 'msg': _('Error occurred during deletion: ') + str(e)}, safe=False) # 刪除過程中出錯


def get_category_array(request):
    """
    功能描述: 獲取類別信息
    """
    try:
        result = {'status':True,'msg':'','data':[]}
        result['data'] = list(PromptcategoryTbl.objects.all().values('categoryno','category'))
    except Exception as e:
        print(str(e))
        result['status'] = False
        result['msg'] = _('Error occurred while fetching category info: ') + str(e) # result['msg'] = f"獲取類別信息時出錯:  {str(e)}"
    return JsonResponse(result, safe=False)