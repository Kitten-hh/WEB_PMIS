from django.conf.urls import url
from . import views
from .ViewsFolder import views_goalmaster,views_task, views_simple_template, views_report, views_task_enquiry, \
    views_sale, views_looper, views_user, views_tasktype, views_active_tasks, views_session, views_opportunity, \
        views_subproject, views_goaloverall,views_mindmap,views_typelist,views_goalmanagement,views_public
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from BaseProject.tools.UrlUtils import dynamic_view_url
from .ViewsFolder.Schedule.views_sch_params import ScheduleParamsViews
from .ViewsFolder.Schedule import views_display 
from .ViewsFolder.views_datatable import Task_Datatable_Demo
from django.shortcuts import render

scheduleParamsViews = ScheduleParamsViews()
opportunity_view = views_opportunity.OpportunityView()
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

    #url(r'^$',views.index,name='index'),
    url(r'^$', views.looper_index, name="looper_index"),
    ##url(r'^$',views.index, name='index'),
    #path('',views.PMIS,name='PMIS'),
    url('todo_task',views.todo_task, name='todo_task'),
    url('Starter_page',views.Starter_page, name='Starter_page'),
    url('PMIS_bak',views.PMIS_bak, name='PMIS_bak'),
    url('Adminux_base',views.Adminux_base, name='Adminux_base'),
    url('Trial',views.Trial, name='Trial'),
    url('contextmenu',views.contextmenu, name='contextmenu'),
    url('Test_Appearance',views.Test_Appearance, name='Test_Appearance'),
    url('PMS_Staff_Dashboard',views.Staff_Dashboard, name='PMS_Staff_Dashboard'),
    url('TaskForm',views.task_create, name='TaskForm'),
    url('task_create',views.task_create, name='task_create'),
    url('task_search',views.task_create, name='task_search'),
    url('systembug_create', views.system_bug_create, name="systembug_create"),
    url('display_systembug', views.display_system_bug, name="display_system_bug"),
    url('test_customer_filter', views.test_customer_filter, name="test_customer_filter"),
    url('create_goal_master', views.create_goal_master, name="create_goal_master"),
    url('task_datatable', views.TaskTableView.as_view(), name="Task_list"),
    url('multi_datatable', views.MultiTableView.as_view(), name="mulit_datatable"),
    url(r'^goal_master_form$', views_goalmaster.GoalMasterView.as_view(), name="goal_master_form"),
    url(r'^goal_master_form/edit/(?P<pk>[^/]+)$', views_goalmaster.GoalMasterEditView.as_view(), name="goal_master_edit"),
    url(r'^goal_master_form/treelist/(?P<pk>[^/]+)$', views_goalmaster.display_goal, name="goal_master_treelist"),
    url(r'^goal_master_form/update_goal/(?P<pk>[^/]+)$', views_goalmaster.update_goal, name="update_goal"),
    url(r'^goal_master_form/report$', views_goalmaster.report, name="goal_master_report"),
    url(r'^task_detail_from/create$', views_task.TaskDetailCreateView.as_view(), name='task_detail_create'),
    url(r'^task_detail_from/edit/(?P<pk>[^/]+)$', views_task.TaskDetailUpdateView.as_view(), name='task_detail_edit'),
    url(r'^task_detail_from/del/(?P<pk>[^/]+)$', views_task.del_task, name='task_detail_del'),
    url("simple_template", views_simple_template.DisplayView.as_view(), name="simple_template"),
    url('task_enquiry', views_task_enquiry.display_task_enquiry, name="task_enquiry_frm"),
    url('query/search', views_task_enquiry.searchRecordFilter, name="query_search"),
    url('active_reports', views_report.display_report, name="active_reports"),
    url(r'^report/api/themes/list$', views_report.get_themes_list, name="report_themes_list"),
    url(r"^report/api/reports/(?P<report_name>[^/]+)/content$", views_report.get_report_content, name="get_report_content"),
    url(r"^report/api/reports/content$", views_report.save_report_content, name="save_report_content"),
    url(r"^report/api/datasets/list$", views_report.get_datasets_list, name="get_datasets_list"),
    url(r"^report/api/datasets/(?P<dataset_name>[^/]+)/content$", views_report.get_dataset_content, name="get_dataset_content"),
    url(r"^preview/(?P<report_name>[^/]+)$", views_report.preview_report, name="preview_report"),
    url(r"^report/api/reports/(?P<report_name>[^/]+)/info$", views_report.get_report_info, name="get_report_info"),
    url(r"^report/appraisal", views_report.get_appraisal, name="get_apraisal"),
    url(r"^looper_calendar$", views.looper_calendar, name="looper_calendar"),
    url(r"^looper_calendar/events$", views.looper_events, name="looper_calendar_events"),
    url(r"^looper_gantt$", views.looper_gantt, name="looper_gantt"),
    url(r"^looper_gantt_data$", views.looper_gantt_data, name="looper_gantt_data"),
    url(r"^looper_dashboard/getCompletionTasks$", views_looper.getCompletionTasks, name="getCompletionTasks"),
    url(r"^project/template_task$", views_task.template_task, name="template_task"),
    url(r"^sale/sales_dashboard$", views_sale.sales_dashboard, name="sales_dashboard"),
    url(r"^sale/sales_dashboard/getPastYearSales$", views_sale.getPastYearSales, name="getPastYearSales"),
    url(r"^sale/sales_dashboard/getQuarterSales$", views_sale.getQuarterSales, name="getQuarterSales"),
    url(r"^sale/sales_dashboard/getWeeklyShipment$", views_sale.getWeeklyShipment, name="getWeeklyShipment"),
    url(r"^sale/sales_dashboard/getSalesCustAnalysis$", views_sale.getSalesCustAnalysis, name="getSalesCustAnalysis"),
    url(r"^sale/sales_dashboard/getOrderState$", views_sale.getOrderState, name="getOrderState"),
    url(r"^sale/sales_dashboard/getSaleOrderList$", views_sale.getSaleOrderList, name="getSaleOrderList"),
    url(r"^sale/sales_dashboard/product_search$", views_sale.product_search, name="product_search"),
    url(r"^sale/sales_dashboard/getNewProduct$", views_sale.getNewProduct, name="getNewProduct"),
    ##url(r"^schedule/simulation$", ScheduleView.display_simulation_page, name="display_simulation_page"),
    ##url(r"^schedule/upload$", ScheduleView.upload, name="schedule_upload"),
    url(r'^schedule/display$', views_display.display_logic, name="display_logic"),
    url(r'^schedule/display_bar$', views_display.display_logic_bar, name="display_logic_bar"),
    url(r'^test$', views.test, name="test"),
    url('srh', views.srh, name="srh"),
    #####與任務相關的URL##############
    ##常用任務URL######
    url('task/progresses', views_task.get_task_progresses, name="progresses"),
    ##url('task/add_task', views_task.add_task, name="add_task"),
    url('task/t_list', views_task.TaskTableView.as_view(), name="task_t_list"),
    url('task/t_doc_list', views_task.sessionTaskDocList, name="task_doc_list"),
    url('task/get_t_doc', views_task.downloadDocument, name="task_get_t_doc"),
    url('task/preview_t_doc', views_task.previewDocument, name="task_preview_t_doc"),
    url('task/add_task', views_task.CreateTaskView.as_view(), name="add_task"),
    url('task/send_instant_notif', views_task.sendIntantNotif, name="task_send_instant_notif"),
    ##url('task/update_task', views_task.update_task, name="update_task"),
    url('task/update_task', views_task.UpdateTaskView.as_view(), name="update_task"),
    url(r'task/delete_task/(?P<pk>[^/]+)$$', views_task.DeleteTaskView.as_view(), name="delete_task"),
    url(r'^task/add_otheruser_relation_task/$', views_task.add_otheruser_relation_task, name="add_otheruser_relation_task"), # syl 20240807
    url("task/today_tasks/(?P<username>[^/]+)", views_active_tasks.get_user_today_tasks, name="today_tasks"),
    url(r"^task/get_today_fixed_tasks$", views_active_tasks.get_today_fixed_tasks, name="today_fixed_tasks"),
    url(r"^task/get_today_fixed_tasks_part$", views_active_tasks.get_today_fixed_tasks_part, name="today_tasks_part"),
    url("task/schedule_priority/(?P<username>[^/]+)", views_active_tasks.get_user_schedule_tasks, name="user_schedule_tasks"),
    url("task/classone_tasks/(?P<username>[^/]+)", views_active_tasks.get_user_class1_tasks, name="classone_tasks"),
    url("task/group_tasks", views_active_tasks.get_group_tasks, name="group_tasks"),
    url("task/default_dialy_pattern/(?P<username>[^/]+)", views_active_tasks.get_user_def_daily_pattern, name="default_dialy_pattern"),
    url("task/search_with_queryid/(?P<queryid>[^/]+)", views_task_enquiry.search_task_with_query_filter, name="search_with_queryid"),
    url("task/approve_request", views_task.approveRequest, name="task_approve_request"),
    
    
    #####與任務相關的URL##############

    #####與用戶有關的URL########
    url(r"^user/profile$", views_user.profile, name="profile"),
    url(r"^user/profile/get_chievement", views_user.getAchievement, name="getAchievement"),
    url(r"^user/getUserActivites$", views_user.getUserActivites, name="getUserActivites"),
    url(r"^user/project$", views_user.getUserProject, name="getUserProject"),
    url("user/get_user_names", views_user.get_all_user_name_list, name="get_user_names"),
    url("user/get_part_user_names", views_user.get_part_user_name_list, name="get_part_user_names"),
    #####與用戶有關的URL########

    ###與TaskType有關的URL#######
    url("tasktype/tasktype_list", views_tasktype.get_tasktype_list, name="tasktype_list"),
    url("tasktype/subtasktype_list/(?P<tasktype>[^/]+)", views_tasktype.get_subtasktype_list, name="subtasktype_list"),
    url("tasktype/subtasktype_score", views_tasktype.get_subtasktype_score, name="subtasktype_score"),

    ###與TaskType有關的URL#######

    ###與Session有關的URL#######
    url("^session/session_list$", views_session.session_list, name="session_list"),
    url("^session/session_list_all$", views_session.SessionListView.as_view(), name="session_list_all"),
    url("^session/task_list$", views_session.SessionTableView.as_view(), name="task_list"),
    url("session/search_task", views_session.search_task_with_session, name="session_search_task"),
    url("session/create", views_session.CreateSessionView.as_view(), name="session_create"),
    url("session/update", views_session.UpdateSessionView.as_view(), name="session_update"),
    url("session/session_sessionList", views_session.session_sessionList, name="session_sessionList"),
    ###與Session有關的URL#######

    ###與goalmaster有關的URL#######
    url("goalmaster/get_all_period", views_goalmaster.get_all_period_list, name="get_all_period"),
    url("goalmaster/update", views_goalmaster.UpdateMasterView.as_view(), name="update_goalmaster"),
    url('goalmaster/show_treelist/(?P<pk>[^/]+)$', views_goalmaster.show_goal_treelist, name="show_goal_treelist"),    
    url('goal/overall/monthly$', views_goaloverall.get_overall_monthly_goal, name="overall_monthly_goal"),    
    url('goal/overall/weekly$', views_goaloverall.get_overall_weekly_goal, name="overall_weekly_goal"),    
    url('goal/overall/weekly_bak$', views_goaloverall.get_overall_weekly_goal_bak, name="overall_weekly_goal_bak"),    
    url('goal/overall/goal_management$', views_goaloverall.get_goal_management, name="goal_management"),
    url('goal/overall/create_goal_management$', views_goaloverall.CreateGoalManagementView.as_view(), name="create_goal_management"),
    url('goal/overall/update_goal_management/(?P<pk>[^/]+)$', views_goaloverall.UpdateGoalManagementView.as_view(), name="update_goal_management"),
    url('goal/overall/del_goal_management/(?P<pk>[^/]+)$', views_goaloverall.DeleteGoalManagementView.as_view(), name="del_goal_management"),
    url('goal/overall/list_goal_management', views_goaloverall.GoalManagementTableView.as_view(), name="list_goal_management"),
    url('goal/overall/save_text_quarterly_goal', views_goaloverall.saveTextQuarterlyGoal, name="save_text_quarterly_goal"),
    url('goal/overall/get_week_goal', views_goaloverall.get_week_goal, name="get_week_goal"),
    url('goal/overall/select_appraisal_view', views_goaloverall.SelectAppraisalView.as_view(), name="select_appraisal_view"),
    url('goal/overall/select_weekly_view', views_goaloverall.SelectWeeklyView.as_view(), name="select_weekly_view"),
    url('goal/overall/del_overall_goal', views_goaloverall.del_overall_goal, name="del_overall_goal"),
    url('goal/overall/add_overall_goal', views_goaloverall.add_overall_goal, name="add_overall_goal"),

    ###與goalmaster有關的URL#######

    ###與subproject有關的URL#######
    url("subproject/get_all_recordid", views_subproject.get_all_recordid_list, name="get_all_recordid"),
    url("subproject/get_recordid_list", views_subproject.get_recordid_list, name="get_recordid_list"),
    ###與subproject有關的URL#######

    ##與goal有關的url###########
    url("goal/search", views_goalmaster.NewGoalMasterView.as_view(), name="goal_search"),
    
    ##與goal management有關的URL##########
    url("goal/management/table", views_goalmanagement.GoalManagementView.as_view(), name="goal_management_table"),
    url("goal/management/search", views_goalmanagement.searchGoalManagement, name="goal_management_search"),
    ##與goal有關的url###########
    #url('PMIS',views.PMIS, name='PMIS'),

    #url(r'^(?P<Knowledge_id>[0-9]+)/$',views.detail, name='detail'),
    #url('JoTech',views.JoTech, name='JoTech'),
    #url('PMIS',views.PMIS, name='PMIS'),
    #url('adminux',views.adminux, name='adminux'),
    
    url(r'^newOpportunity$',auth_page("PMIS/newOpportunity.html"), name="new_Opportunity"),
    url(r'^Technical_Material_update$', auth_page("PMIS/Technical_Material_update.html"), name="Technical_Material_update"),
    url(r'^Technical_Material_create$', auth_page("PMIS/Technical_Material_create.html"), name="Technical_Material_create"),
    url(r'^Technical_Material_update_show$', auth_page("PMIS/Technical_Material_update_show.html"), name="Technical_Material_update_show"),
    url(r'^Technical_Material_create_show$', auth_page("PMIS/Technical_Material_create_show.html"), name="Technical_Material_create_show"),
    url(r'^TechnicalDatatable$', views_opportunity.Technical_Datatable.as_view(), name="Technic_Datatable"),
    url(r'^technical/get_paraphrase$', views_opportunity.get_technical_paraphrase, name="get_technical_paraphrase"),
    url(r'^technical/update_embeddings$', views_opportunity.update_technical_embeddings, name="update_technical_embeddings"),
    url(r'^CatalogueDatatable$', views_opportunity.Catalogue_Datatable.as_view(), name="Catalogue_Datatable"),
    url(r'^TechnicalUpdate$', views_opportunity.TechnicalUpdateView.as_view(), name="Technical_Update"),
    url(r'^TechnicalCreate$', views_opportunity.TechnicalCreateView.as_view(), name="Technical_Create"),
    url(r'^TecmaCreateView$', views_opportunity.TecmaCreateView.as_view(), name="Tecma_Create"),
    url(r'^TecmaUpdateView$', views_opportunity.TecmaUpdateView.as_view(), name="Tecma_Update"),
    url(r'^TecmfCreateView$', views_opportunity.TecmfCreateView.as_view(), name="Tecmf_Create"),
    url(r'^TecmfUpdateView$', views_opportunity.TecmfUpdateView.as_view(), name="Tecmf_Update"),
    url(r'^download_tecnical_word$', views_opportunity.downloadTecnicalWord, name="download_tecnical_word"),

    ##與mindmap有關的url###########
    url(r'^mindmap/get_menu$', views_mindmap.get_mindmap_menu, name="mindmap_get_menu"),
    url(r'^mindmap/type_create$', views_mindmap.MindMapTypeCreateView.as_view(), name="mindmap_type_create"),
    url(r'^mindmap/type_update$', views_mindmap.MindMapTypeUpdateView.as_view(), name="mindmap_type_update"),
    url(r'^mindmap/type_del$', views_mindmap.MindMapTypeDelView.as_view(), name="mindmap_type_del"),
    url(r'^mindmap/create$', views_mindmap.MindMapCreateView.as_view(), name="mindmap_create"),
    url(r'^mindmap/update$', views_mindmap.MindMapUpdateView.as_view(), name="mindmap_update"),
    url(r'^mindmap/del$', views_mindmap.MindMapDelView.as_view(), name="mindmap_del"),
    url(r'^mindmap/active_session$', views_mindmap.get_week_active_session, name="active_session"),
    url(r'^mindmap/get_data/(?P<pk>[^/]+)$', views_mindmap.get_mindmap_data, name="mindmap_get_data"),
    url(r'^mindmap/copy_mindmap$', views_mindmap.copy_mindmap, name="copy_mindmap"),
    url(r'^mindmap/(?P<inc_id>[^/]+)$', views_mindmap.get_mindmap_incId_data, name="mindmap_incId_data"),
    url(r'^mindmap_project$', views_mindmap.get_mindmap_recordid_data, name="project_mindmap_incId_data"),
    
    url(r'^global/get_typelist$', views_typelist.get_type_list, name="get_type_list"),

    

    url(r'^technical/categorytree$', views_opportunity.get_categorytree, name="get_categorytree"),    

    
    url(r'^public/get_syspara$', views_public.get_syspara, name="get_syspara"),    


    
]

urlpatterns += dynamic_view_url(scheduleParamsViews,'schparams')
urlpatterns += dynamic_view_url(opportunity_view, 'opportunity')
urlpatterns += staticfiles_urlpatterns()