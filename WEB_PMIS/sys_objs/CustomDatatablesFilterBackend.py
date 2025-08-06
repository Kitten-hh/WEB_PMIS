from rest_framework_datatables.filters import DatatablesFilterBackend
from BaseApp.library.tools.QueryBuilderUtils import QueryBuilderUtils
import json
class CustomDatatablesFilterBackend(DatatablesFilterBackend):
    def filter_queryset(self, request, queryset, view):
        queryset = self.attach_query(request, queryset)
        return super().filter_queryset(request, queryset, view)

    def attach_query(self, request, queryset):
        '''
        描述描述：處理用戶傳入附加查詢條件,以attach_query:{"condition":"and","rules":[{...}]}為格式
        即使用querybuilder通用查詢框和SWAdvancedSearch控件生成的查詢條件
        '''
        search_obj = QueryBuilderUtils.getQueryFromRequest(request,'attach_query')
        if search_obj:
            query = QueryBuilderUtils.json_to_query(json.dumps(search_obj))
            return queryset.filter(query)
        else:
            return queryset
