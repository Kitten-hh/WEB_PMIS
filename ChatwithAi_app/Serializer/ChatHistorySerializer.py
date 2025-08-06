from rest_framework import viewsets
from ..models import Chathistory
from rest_framework import serializers
from WEB_PMIS.sys_objs.CustomFilterSet import CustomFilterSet,virtual_field_filter_mthod


class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Chathistory
        fields = '__all__'    
    def to_representation(self, instance):
        # 调用原始的 to_representation 获取常规数据
        ret = super().to_representation(instance)
        # 检查请求中是否有特定的查询参数，例如 `include_full_conversation`
        request = self.context.get('request')
        if request and request.query_params.get('include_full_conversation') == 'true':
            ret['fullconversation'] = instance.fullconversation
            ret['fulldisplayconversation'] = instance.fulldisplayconversation
        else:
            ret['fullconversation'] = None
            ret['fulldisplayconversation'] = None
        return ret        

class ChatHistoryFilterSet(CustomFilterSet):    
    class Meta:
        model = Chathistory
        fields = '__all__'
