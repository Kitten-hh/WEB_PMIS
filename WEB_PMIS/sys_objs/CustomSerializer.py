from rest_framework import serializers
from rest_framework.exceptions import ValidationError
##from django_filters import rest_framework as filters
import rest_framework_filters  as filters
import django_filters as d_filters
from django.db import models
import base64

class BinaryField(serializers.Field):
    def to_representation(self, value):
        return base64.b64encode(value)

    def to_internal_value(self, value):
        if (value.find("base64") != -1):
            value = value.split('base64,')[1] # remove text before encoded data
        return base64.b64decode(value)

class BlobDataSerializerMetaClass(type(serializers.ModelSerializer)):
    def __new__(cls, clsname, bases, attrs):
        # Call the __new__ method from the ModelSerializer metaclass
        super_new = super().__new__(cls, clsname, bases, attrs)
        # Modify class variable "serializer_field_mapping"
        # serializer_field_mapping: model field -> serializer field
        super_new.serializer_field_mapping[models.BinaryField] = BinaryField
        return super_new

class CustomFloatField(serializers.FloatField):
    def to_representation(self, value):
        return round(float(value), 5)

class NumberDataSerializerMetaClass(type(serializers.ModelSerializer)):
    def __new__(cls, clsname, bases, attrs):
        # Call the __new__ method from the ModelSerializer metaclass
        super_new = super().__new__(cls, clsname, bases, attrs)
        # Modify class variable "serializer_field_mapping"
        # serializer_field_mapping: model field -> serializer field
        super_new.serializer_field_mapping[models.FloatField] = CustomFloatField
        return super_new


class ReadOnlyModelSerializer(serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        for field in fields:
            fields[field].read_only = True
        return fields