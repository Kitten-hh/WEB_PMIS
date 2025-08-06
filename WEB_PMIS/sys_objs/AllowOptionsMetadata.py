from rest_framework.metadata import SimpleMetadata
from collections import OrderedDict

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.encoding import force_str

from rest_framework import exceptions, serializers
from rest_framework.request import clone_request
from rest_framework.utils.field_mapping import ClassLookupDict


class AllowOptionsMetadata(SimpleMetadata):
    '''
    功能描述：修改基類只有在POST, PUT的情況下才可以在OPTIONS中顯示字段信息
    '''
    def determine_actions(self, request, view):
        """
        For generic class based views we return information about
        the fields that are accepted for 'PUT' and 'POST' methods.
        """
        actions = {}
        for method in {'PUT', 'POST', 'GET'} & set(view.allowed_methods):
            view.request = clone_request(request, method)
            try:
                # Test global permissions
                if hasattr(view, 'check_permissions'):
                    view.check_permissions(view.request)
                # Test object permissions
                if method == 'PUT' and hasattr(view, 'get_object'):
                    view.get_object()
            except (exceptions.APIException, PermissionDenied, Http404):
                pass
            else:
                # If user has appropriate permissions for the view, include
                # appropriate metadata about the fields that should be supplied.
                serializer = view.get_serializer()
                if method == 'GET':
                    actions[method] = {'results':self.get_serializer_info(serializer)}
                else:
                    actions[method] = self.get_serializer_info(serializer)
            finally:
                view.request = request

        return actions    