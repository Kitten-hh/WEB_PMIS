from rest_framework import viewsets
from DataBase_MPMS.models import Document
from rest_framework import serializers
from WEB_PMIS.sys_objs.CustomFilterSet import CustomFilterSet,virtual_field_filter_mthod
from django_filters import rest_framework as filters


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'    

class DocumentFilterSet(CustomFilterSet):    
    inc_id = filters.CharFilter(method='filter_inc_id')  # 使用自定义方法支持逗号分隔的数字 in 查询

    def filter_inc_id(self, queryset, name, value):
        # 解析逗号分隔的值，并转换为整数列表
        try:
            numbers = [int(v) for v in value.split(',')]
        except ValueError:
            # 如果解析失败，返回空的查询集
            return queryset.none()
        
        # 应用 in 查询过滤器
        return queryset.filter(**{f"{name}__in": numbers})    

    class Meta:
        model = Document
        fields = {
            'inc_id':['exact'],
            'docid': ['exact'],
            'docname': ['exact', 'contains'],
        }
