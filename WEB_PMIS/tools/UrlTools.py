from Authorization_app.permissions.decorators_pmis import permission_required
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.context_processors import PermWrapper
import importlib
from django.conf import settings
from django.urls import URLPattern, URLResolver
from BaseApp.library.tools import UrlTools

def protected_auth_page(url: str, main_page=None, permission_name=None, required_rwx=0):
    @permission_required(permission_name, required_rwx=required_rwx)
    @login_required
    def dynamic_template(request):
        return render(request, url, {"main_page": main_page, "Design": UrlTools.getDesignFlag(request)})
    
    return dynamic_template
