from django.conf.urls import url
from PMIS.ViewsFolder import views_user
from django.urls import path
from . import views
from .ViewsFolder import ViewFlowChart

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.shortcuts import render
from BaseApp.library.tools.UrlTools import page
    
urlpatterns = [
    url(r'^$', page("FlowChartApp/Diagram.html"), name="index"),
    url(r'^test$', page("FlowChartApp/DiagramTest.html"), name="test"),
    url(r'^preview$', page("FlowChartApp/Preview.html"), name="flowchart_preview"),
    url(r'^preview_diagram$', page("FlowChartApp/PreviewDiagram.html"), name="test"),
    url(r'^dialy$', page("FlowChartApp/DialyPage.html"), name="index"),
    url(r'^get_old_flowchart_data$', ViewFlowChart.get_source_flowchart, name="get_source_flowchart"),
    url(r'^get_flowchart_data$', ViewFlowChart.get_flowchart_data, name="get_flowchart_data"),
    url(r'^get_flowchart_desc$', ViewFlowChart.get_source_flowchart_desc, name="get_flowchart_desc"),
    url(r'^list_docdesign$', ViewFlowChart.DocdesignTableView.as_view(), name="list_docdesign"),
    url(r'^convert$', ViewFlowChart.convertFlashToGojs, name="convert"),
]
urlpatterns += staticfiles_urlpatterns()    