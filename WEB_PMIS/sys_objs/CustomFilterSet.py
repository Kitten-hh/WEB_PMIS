from rest_framework import serializers
from rest_framework.exceptions import ValidationError
##from django_filters import rest_framework as filters
import rest_framework_filters  as filters
import django_filters as d_filters
from django.db import models


def virtual_field_filter_mthod(queryset, name, value):
    return queryset

class CustomFilterSet(filters.FilterSet):
    EMPTY_VALUES = ([], (), {}, '', None)
    real_filters = {}

    def filter_queryset(self, queryset):
        """
        Filter the queryset with the underlying form's `cleaned_data`. You must
        call `is_valid()` or `errors` before calling this method.

        This method should be overridden if additional filtering needs to be
        applied to the queryset before it is cached.
        """
        for name, value in self.form.cleaned_data.items():
            if name in self.real_filters:
                queryset = self.custom_filter_queryset(queryset, name, value)
            else:
                queryset = self.filters[name].filter(queryset, value)
            assert isinstance(queryset, models.QuerySet), \
                "Expected '%s.%s' to return a QuerySet, but got a %s instead." \
                % (type(self).__name__, name, type(queryset).__name__)
        queryset = self.filter_related_filtersets(queryset)
        return queryset    
    def custom_filter_queryset(self, queryset, name, value):
        if value in self.EMPTY_VALUES:
            return queryset
        lookup_expr = self.real_filters[name].lookup_expr
        if lookup_expr == 'in' or lookup_expr == 'range':
            value = value.split(',')
            if len(value)==1:
                value.append(value[0])
            try:
                queryset = self.real_filters[name].filter(queryset, value)
            except Exception as exc:
                raise ValidationError({name:[exc]})
        else:
            queryset = self.real_filters[name].filter(queryset, value)
        return queryset

    @property
    def qs(self):
        try:
            qs = super().qs
            self.custom_validate_field()
        except Exception as e:
            raise ValidationError(e)
        else:
            return qs        

    def custom_validate_field(self):
        for name, value in self.form.cleaned_data.items():
            filter_validate_method = getattr(self, "validate_" + name, None)
            if filter_validate_method != None:
                if not filter_validate_method(value, self.form.cleaned_data.items()):
                    raise ValidationError({name:['invaild value']})