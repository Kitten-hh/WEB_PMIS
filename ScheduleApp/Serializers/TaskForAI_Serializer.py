from .. import models
from rest_framework import serializers
from django.utils.translation import gettext as _, gettext_lazy as __
import rest_framework_filters  as filters
import django_filters as d_filters
from WEB_PMIS.sys_objs.CustomFilterSet import CustomFilterSet,virtual_field_filter_mthod
from ..Services.TaskForAIService import TaskForAIService
from django.db.models import Sum,Count,Max,Min,Avg,Q
import decimal
from django.forms.models import model_to_dict


class ChattopictblSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chattopictbl
        fields = "__all__"

class ChattopictblFilterSet(CustomFilterSet):    
    class Meta:
        model = models.Chattopictbl
        fields = '__all__'

class IteratedPromptQuestion(serializers.Serializer):
    question = serializers.CharField()  

class PrompttblSerializer(serializers.ModelSerializer):
    iterated_prompt_questions = serializers.SerializerMethodField()  #生產可用庫存    
    def get_iterated_prompt_questions(self, instance):
        prompt = model_to_dict(instance)
        service = TaskForAIService()
        if prompt['post_bool'] == "Y" and prompt['relation'] and not prompt['predefined_prompt']:
            service.getIteratedPromptWithRelation(prompt)
            if 'iterated_prompt_questions' in prompt:
                return prompt['iterated_prompt_questions']
        return None
    class Meta:
        model = models.Prompttbl
        fields = [item.name for item in models.Prompttbl._meta.get_fields()] + ['iterated_prompt_questions']

    def to_representation(self, instance):
        prompt = super().to_representation(instance)
        service = TaskForAIService()
        if prompt['post_bool'] == "Y" and prompt['relation'] and not prompt['predefined_prompt']:
            service.getIteratedPromptWithRelation(prompt)
        return prompt 


class PrompttblFilterSet(CustomFilterSet):    
    class Meta:
        model = models.Prompttbl
        fields = '__all__'

class PromtsqlSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Promtsql
        fields = "__all__"

class PromtsqlFilterSet(CustomFilterSet):    
    class Meta:
        model = models.Promtsql
        fields = '__all__'        