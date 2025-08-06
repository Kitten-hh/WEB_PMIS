"""WEB_PMIS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static,serve
from django.conf import settings 
from django.urls import path, include,re_path
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import JavaScriptCatalog
from BaseApp.library.tools.UrlTools import auth_page,page
from BaseApp.library.tools import UrlTools

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path("locale/", include('LocaleApp.urls'))
]
urlpatterns += i18n_patterns(
    url(r'^admin/', admin.site.urls),
    url(r'^PMIS/', include('PMIS.urls')),
    url(r'^looper/', include('PMISLooper.urls')),
    url(r'^BaseApp/', include('BaseApp.urls')),
    url(r'^devplat/', include('DevPlat.urls')),
    url(r'^schedule/', include('ScheduleApp.urls')),
    url(r'^ntfy/', include('Notification_app.urls')),
    url(r'^chatwithai/', include('ChatwithAi_app.urls')),
    url(r'^flowchart/', include('FlowChartApp.urls')),
    url(r'^bonus/', include('BonusApp.urls')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    re_path(r'^rosetta/', include('rosetta.urls')),
    url(r'^base_report/', include('BaseReportApp.urls')),
    url(r'^systembugrpt/', include('SystemBugRpt_app.urls')),
    url(r'^project/', include('ProjectManagement_app.urls')),
    url(r'^auth/users$',auth_page("WEB_PMIS/auth/Users.html"), name="auth-users"),    
    url(r'^auth/roles$',auth_page("WEB_PMIS/auth/Roles.html"), name="auth-roles"),    
    url(r'^auth/permissions$',auth_page("WEB_PMIS/auth/Permissions.html"), name="auth-users"),    
    url(r'^auth/role_permissions_pmis$',auth_page("WEB_PMIS/auth/RolePermission.html"), name="auth-users"),    
)

if not settings.DEBUG:
    urlpatterns += url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
else:
    urlpatterns += staticfiles_urlpatterns()

#UrlTools.check_duplicate_url_names(urlpatterns)