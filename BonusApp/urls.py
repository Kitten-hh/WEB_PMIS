"""Gallery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

from .view import views_tasktype, views_bonusparam
from django.shortcuts import render
from . import views
from django.contrib.auth.decorators import login_required

def page(url:str):
    def dynamic_template(request):
        return render(request, url)
    return dynamic_template

def auth_page(url:str):
    @login_required()
    def dynamic_template(request):
        return render(request, url)
    return dynamic_template   

urlpatterns = [
    url(r'^$',page("BonusApp/bonus_analysis.html"), name='index'),
    url(r'^task_search$',views.Task_Management, name='task_search'),
    
    # Task_Management
    path('Task_Management/',views.Task_Management),  
    path('get_Tasts/',views.get_Task),                     
    path('get_Task_Details/',views.get_Task_Details,name='get_Task_Details'),  
    path('get_TaskTypeList/',views.get_TaskTypeList),              
    path('get_Contact_Details/',views.get_Contact_Details),   
    path('get_Task_List/',views.get_Task_List),              
    path('get_Task_Modif_Page/',views.get_Task_Modif_Page),   
    path('Modif_Task/',views.Modif_Task),                 
    path('task_enquiry/', views.display_task_enquiry),    
    path('query/search/', views.searchRecordFilter),
    path('query/searchdate/',views.get_searchdate),# 通过日期范围搜索数据
    path('Task_Add/',views.Task_Add), # Bouns/ 页面的“+”号按钮
    path('Task_Del/',views.Task_Del), # Task_Details 页面删除按钮
    path('get_bonus_stats/',page("BonusApp/bonusS.html")), 

    # 看板
    path('spectaculars/', views.get_Spectaculars), 
    path('spectaculars/technicalDoc_Details/', views.technicalDoc_Details), 

    # TaskType_Management  
    path('tasktype/',views_tasktype.get_TaskType_Management),
    path('tasktype/datatable/',views_tasktype.TaskTypeDataTable.as_view(),name="get_TaskType_List"),   
    path('tasktype/detail/',views_tasktype.get_TaskType_Details), # 添加error.html
    path('tasktype/edit/',views_tasktype.get_TaskType_Modif_Page), # 添加error.html   
    #path('tasktype/update/save/',views_tasktype.Modif_TaskType), 
    path('tasktype/update/save',views_tasktype.TaskTypeUpdateView.as_view(),name="update_tasktype"),    
    path('tasktype/add/',views_tasktype.get_TaskType_Add_Page), 
    path('tasktype/add/save/',views_tasktype.TaskTypeCreativeView.as_view(),name="add_tasktype"),    
    url(r'^tasktype/delete/(?P<pk>[^/]+)$',views_tasktype.TaskTypeDeleteView.as_view(),name="delete_tasktype"), 
    url(r'^tasktype/import$', views_tasktype.import_tasktype_excel,name="import_tasktype_excel"),
    url(r'^tasktype/download$', views_tasktype.download_tasktype_excel,name="download_tasktype_excel"),

    url(r'^lstasktype/treelist$', views_tasktype.searchTasktype,name="searchTasktype"),
    url(r'^lstasktype/add$',views_tasktype.TaskTypelistCreativeView.as_view(), name="lstasktype_add"), 
    url(r'^lstasktype/update$',views_tasktype.TaskTypelistUpdateView.as_view(), name="lstasktype_update"), 
    url(r'^lstasktype/delete/(?P<pk>[^/]+)$',views_tasktype.TaskTypelistDeleteView.as_view(), name="lstasktype_delete"),
    url(r'^lstasktype/maxtasktype$', views_tasktype.getMaxTaskType,name="getMaxTaskType"), 

    #系统参数
    path('user_bonusparams_index/',page("BonusApp/Parameters/user_bonusparam.html")),
    #path('get_systemParameters_List/',views_system.get_systemParameters_List), # .as_view()    
    url(r'^get_systemParameters_List$', views_bonusparam.SysparaView.as_view(), name="get_systemParameters_List"),
    url(r'^user_bonusparams$', views_bonusparam.UserBonusParamView.as_view(), name="user_bonusparams"),
    path('get_Syspara_Add_Page/',page("BonusApp/Parameters/Syspara_Add.html")),
    path('get_Syspara_Details/',views_bonusparam.get_Syspara_Details), # page("BonusApp/SystemParameters/Syspara_Details.html")
    
    path('Add_Syspara/',views_bonusparam.CreateSyspara.as_view()),
    url('update_Syspara/(?P<pk>[^/]+)',views_bonusparam.UpdateSyspara.as_view()),
    url('delete_Syspara/(?P<pk>[^/]+)',views_bonusparam.DeleteSyspara.as_view()),
    #path('bonus_analysis_page/',page("BonusApp/bonus_analysis.html")), 
    url(r'^bonus_analysis$', views.bonus_analysis_new, name="bonus_analysis"),
    url(r'^bonus_analysis_part$', views.bonus_analysis_part, name="bonus_analysis_part"),
    path('test_json/',page("BonusApp/Parameters/json_test.html")), 
    url(r'^json_to_model$', views.json_to_model, name="json_to_model"),
    url(r'^audit_source$', views.auditScore, name="audit_source"),
    url('bonus/update/(?P<pk>[^/]+)',views_bonusparam.UpdateBonusParam.as_view()),
    path('analyse_bar/',views.get_bonusStatistics),
    url(r'^bonus_recalculate$', views.bonus_recalculate, name="bonus_recalculate"),
    url(r'^get_tasktype_sl$', views.getTaskTypeSL, name="get_tasktype_sl"),
    url(r'^update_tasktype_sl$', views.updateTaskTypeSL, name="update_tasktype_sl"),
    url(r'^get_tasktype_sl_history_maxver$', views.getSimulationTaskTypeHistoryMaxVerNo, name="get_tasktype_sl_history_maxver"),
    url(r'^reset_tasktype_sl$', views.resetSimulationTaskType, name="reset_tasktype_sl"),
    #url(r'^bonus_analysis_page$', page('BonusApp/bonus_analysis.html')),
    #url('search_Syspara',views_system.searchData),    
    url(r'^main_page$', auth_page("BonusApp/bonus/bonus_analysis.html"), name="main_page"),   
    url(r'^mobile_page$', auth_page("BonusApp/bonus/bonus_analysis_mobile.html"), name="mobile_page"), 
    url(r'^tasktype_page$', auth_page("BonusApp/bonus/tasktype.html"), name="tasktype_page"),  
    url(r'^userdeduction_page$', auth_page("BonusApp/bonus/userdeduction.html"), name="userdeduction_page"),  
    url(r'^improvearea_page$', auth_page("BonusApp/bonus/improvearea.html"), name="improvearea_page"), 
    url(r'^bonuscredit_page$', auth_page("BonusApp/bonus/bonus_credit.html"), name="bonuscredit_page"),  

    path('deductionitem/datatable',views.DeductionItemDataTable.as_view(),name="deductionitem_table"),  
    path('userdeduction/datatable',views.UserDeductionDataTable.as_view(),name="userdeduction_table"), 
    url(r'^userdeduction/add$',views.UserDeductionCreativeView.as_view(), name="userdeduction_add"), 
    url(r'^userdeduction/update$',views.UserDeductionUpdateView.as_view(), name="userdeduction_update"), 
    url(r'^userdeduction/chart$',views.getDeductionChartData, name="getDeductionChartData"), 
    url(r'^userdeduction/delete/(?P<pk>[^/]+)$',views.UserDeductionDeleteView.as_view(), name="userdeduction_delete"),
    url(r'^userdeduction/get_position$',views.getPositionByContact, name="getPositionByContact"),
    url(r'^userdeduction/get_duction_category$',views.getDuctionCategory, name="getDuctionCategory"),

    path('improvearea/datatable',views.ImproveareaDataTable.as_view(),name="improvearea_table"), 
    url(r'^improvearea/add$',views.ImproveareaCreativeView.as_view(), name="improvearea_add"), 
    url(r'^improvearea/update$',views.ImproveareaUpdateView.as_view(), name="improvearea_update"), 
    url(r'^improvearea/delete/(?P<pk>[^/]+)$',views.ImproveareaDeleteView.as_view(), name="improvearea_delete"),
]
