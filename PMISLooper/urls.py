from django.conf.urls import url
from PMIS.ViewsFolder import views_user
from django.urls import path
from . import views
from .ViewsFolder import (AIConditionManagerView, AnalyseProjects, AnalyseSolutionView,TecdailyplannerView,SolutionTypeView,
TecdailyPlannerImageView,ApscheduleView,MettingView,TestingView,TechnicalUseRecordView,FrameUpdateView,top_projectView,DashboardView, TaskDashboardView,
NotificationView,PmsSessionManager)
from PMIS.ViewsFolder import (views_active_tasks)

from .ViewsFolder.ProjectManagement import View_ProjectGoals
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .ViewsFolder import GoalManagement_View
from BaseApp.library.tools.UrlTools import auth_page,page
from PMIS.ViewsFolder import views_task_enquiry


    
urlpatterns = [
    url(r'^$', views.staff_dashboard, name="looper_index"),
    url(r'^login$', views_user.login, name="login"),
    url(r'^login_page$', page("PMISLooper/user/login.html"), name="login_page"),
    url(r'^logout$', views_user.logout, name="logout"),
    url(r'^is_login$', views_user.is_login, name="is_login"),
    url(r'^team_dashboard$', views.index, name="team_dashboard"),
    url(r'^team_dashboard/get_followup_sessions$', DashboardView.getFlowupActiveSession, name="get_followup_sessions"),
    
    url(r'^staff_dashboard$', views.staff_dashboard, name="staff_dashboard"),

    url(r'^staff_dashboard_color$', views.staff_dashboard_color, name="staff_dashboard_color"),
    
    url(r'^get_dashboard_data_part$', views.get_dashboard_data_part, name='get_dashboard_data_part'),    
    url(r'^dashboard/analysis_task_type$', views.analysis_task_type, name='dashboard_analysis_task_type'),    
    url(r'^dashboard/analysis_solution_type$', views.analysis_solution_type, name='dashboard_analysis_solution_type'),    
    url(r'^dashboard/analysis_new_task$', views.analysis_new_task, name='dashboard_analysis_new_task'),    
    url(r'^get_staff_planner_task$', views.get_staff_planner_task, name="get_staff_planner_task"),
    url(r'^user/activites$', auth_page("PMISLooper/user/activities.html"), name="user_activites"),
    url(r'^user/activites/arrage_tasks$', views_active_tasks.get_arrage_tasks, name="get_arrage_tasks"),
    url(r'^user/teams$', auth_page("PMISLooper/user/teams.html"), name="user_teams"),
    url(r'^user/sessions$', auth_page("PMISLooper/user/sessions.html"), name="user_sessions"),

    url(r'^user/top5_projects$', auth_page("PMISLooper/user/top5_projects.html"), name="user_top5_projects"),

    url(r'^task/enquiry$', auth_page("PMISLooper/task/task-enquiry.html"), name="task-enquiry"),
    url(r'^task/today_task$', auth_page("PMISLooper/task/today_task.html"), name="today_tasks"),
    url(r'^goal/goal_master$', auth_page("PMISLooper/goal/goal_master_form.html"), name="goal_master"),
    url(r'^technic/createdailyplanner$',auth_page("PMISLooper/technic/technic.html"), name="createdailyplanner"),
    url(r'^technic/selectdailyplanner$',auth_page("PMISLooper/technic/TreeMenu.html"), name="selectdailyplanner"),
    url(r'^technic/createUI$',auth_page("PMISLooper/technic/createUI.html"), name="createUI"),
    url(r'^technic/tasktypeTable$',auth_page("PMISLooper/technic/tasktypeTable.html"), name="tasktypeTable"),
    url(r'^technic/solutiontypeTable$',auth_page("PMISLooper/technic/solutiontypeTable.html"), name="solutiontypeTable"),

    url(r'^technic/edit-daily-planner$',auth_page("PMISLooper/technic/edit-daily-planner.html"), name="edit-daily-planner"),

    url(r'^solutiontype/technique_involved$',auth_page("PMISLooper/solutiontype/technique_involved.html"), name="technique_involved"),
    url(r'^technic/technical_statement$', auth_page("PMISLooper/technic/technical_dailyPlanner_statement.html")),
    url(r'^technic/AnomalyDailyPlannerTable$',auth_page("PMISLooper/technic/AnomalyDailyPlannerTable.html"), name="AnomalyDailyPlannerTable"),

    url(r'^technic/SALCFollowUp$',auth_page("PMISLooper/technic/SALCFollowUp.html"), name="SALCFollowUp"),
    
    url(r'^frame/FrameUpdate$',auth_page("PMISLooper/technic/FrameUpdate.html"), name="FrameUpdate"),

    
    url(r'^DailyPlanner/create$', views.DailyPlannerCreateView.as_view(), name="DailyPlanner_create"),
    url(r'^DailyPlanner/update$', views.DailyPlannerUpdateView.as_view(), name="DailyPlanner_update"),
    url(r'^DailyPlanner/solutiontypecreate$', views.DailyPlannerSolutionCreateView.as_view(), name="DailyPlannerSolutionType_create"),
    url(r'^DailyPlanner/solutiontypeupdate$', views.DailyPlannerSolutionUpdateView.as_view(), name="SolutionType_update"),

    url(r'^SolutionType/create$', views.SolutionTypeCreateView.as_view(), name="SolutionType_create"),

    url(r'^search_demo$',views.search_demo,name="search_demo"),

    # url(r'^sync_PMS_meeting$', ApscheduleView.CheckTechnical_AddTask, name="sync_PMS_meeting"),
    
    url(r'^technic/get_task$', views.getTask, name="get_task"),
    url(r'^DailyPlanner/selectTreeMenu$', views.getTreemenu, name="get_Treemenu"),
    url(r'^DailyPlanner/createImage$', views.createImage, name="create_Image"),
    url(r'^DailyPlanner/get_Image', views.gettecdailyplannerimage, name="get_Image"),
    url(r'^DailyPlanner/selectImagees', views.selectImagees, name="select_Imagees"),
    url(r'^DailyPlanner/getTecMindMap', views.getTecMindMap, name="get_TecMindMap"),
    url(r'^DailyPlanner/getTecMindDetail', views.getTecMindMapDetail, name="get_TecMindMapDetail"),
    url(r'^DailyPlanner/TecmindmapDatatable$', views.Tecmindmap_Datatable.as_view(), name="Tecmindmap_Datatable"),
    url(r'^DailyPlanner/TechnicDatatable$', views.Technic_Datatable.as_view(), name="Technic_Datatable"),
    url(r'^DailyPlanner/displaysolutionType', views.displaysolutionType, name="display_solutionType"),
    url(r'^DailyPlanner/AnalyseTaskType', views.AnalyseTaskType, name="Analyse_TaskType"),
    url(r'^DailyPlanner/getRecentlyinMarchu', views.getRecentlyinMarchu, name="get_Recently_in_Marchu"),
    url(r'^DailyPlanner/AnalyseSolutionType', AnalyseSolutionView.AnalyseSolutionType, name="Analyse_SolutionType"),
    url(r'^DailyPlanner/AllContactSolution', AnalyseSolutionView.AllContactSolution, name="All_Contact_Solution"),
    url(r'^DailyPlanner/Alldistictsolution', AnalyseSolutionView.Alldistictsolution, name="All_distict_solution"),
    # url(r'^DailyPlanner/TEST', views.test, name="All_distict_solution"),

    url(r'^goal/treelist$', auth_page("PMISLooper/goal/goal_master_treelist.html"), name="goal_master_treelist"),
    url(r'^goal/calendar$', auth_page("PMISLooper/goal/goal_calendar.html"), name="goal_calendar"),
    url(r'^goal/overall/quarterly_goal$', auth_page("PMISLooper/goal/overall/quarterly_goal.html"), name="overall_quarterly_goal"),
    #url(r'^goal/overall/quarterly_goal_bak$', auth_page("PMISLooper/goal/overall/quarterly_goal_bak.html"), name="overall_quarterly_goal"),
    #url(r'^goal/project_goal$', auth_page("PMISLooper/goal/overall/project_goal.html"), name="mindmap_modal"),
    url(r'^goal/project_goal/analysis_simulation$', View_ProjectGoals.analysis_goal_simulation, name="analysis_simulation"),
    url(r'^goal/project_goal/get_project_goal$', View_ProjectGoals.get_project_goal, name="get_project_goal"),
    url(r'^mindmap$', views.mindmapPage, name="mindmap"),
    url(r'^dynamic_mindmap', views_task_enquiry.dynamicMindmap, name="dynamic_mindmap"),
    url(r'^mindmap_modal$', auth_page("PMISLooper/mindmap/mindmap_modal.html"), name="mindmap_modal"),
    url(r'^goal/project_goal$', auth_page("PMISLooper/goal/project_goal.html"), name="project_goal"),
    
    url(r'^DailyPlanner/TaskDelete', TecdailyplannerView.TaskDeleteView.as_view(), name="Task_Delete"),
    url(r'^DailyPlanner/TaskCodeDelete', TecdailyplannerView.TaskCodeDeleteView, name="Task_Code_Delete"),
    url(r'^DailyPlanner/SolutionDelete', TecdailyplannerView.SolutionDeleteView.as_view(), name="Solution_Delete"),
    url(r'^DailyPlanner/DeletemoreDailyPlanner', TecdailyplannerView.DeletemoreDailyPlanner, name="Delete_more_DailyPlanner"),
    url(r'^DailyPlanner/AnalyseDailyPlanner', TecdailyplannerView.AnalyseDailyPlanner, name="Analyse_DailyPlanner"),
    url(r'^DailyPlanner/get_development', TecdailyplannerView.get_development, name="get_development"),

    url(r'^DailyPlanner/getTechnicid', SolutionTypeView.getTechnicid, name="get_Technicid"),
    
    url(r'^DailyPlanner/GetTecdailyplannerImageContent', TecdailyPlannerImageView.GetTecdailyplannerImageContent, name="Get_TecdailyplannerImageContent"),
    url(r'^DailyPlanner/TecdailyplannerImageController', TecdailyPlannerImageView.TecdailyplannerImageController, name="TecdailyplannerImage_Controller"),
    
    url(r'^user/AnalyseProjects', AnalyseProjects.AnalyseProjects, name="AnalyseProjects"),
    url(r'^user/get_goaldesc', AnalyseProjects.getGoaldesc, name="get_goaldesc"),

    url(r'^modal_add$',auth_page("PMISLooper/mindmap/modal_add.html"),name="testmind"),
    url(r'^solutionType$',auth_page("PMISLooper/mindmap/solutionType_mindmap.html"),name="solutionType_mindmap"),

    url(r'^metting/MettingDataTable$', auth_page("PMISLooper/metting/MettingDataTable.html"), name="MettingDataTable"),    
    url(r'^metting/MettingMaster_Add$', auth_page("PMISLooper/metting/MettingMaster_Add.html"), name="MettingMaster_Add"),   
    url(r'^metting/MettingmasterView', MettingView.MettingmasterView.as_view(), name="MettingmasterView"),
    url(r'^metting/MettingmasterCreateView', MettingView.MettingmasterCreateView.as_view(), name="MettingmasterCreateView"),
    url(r'^metting/MettingmasterUpdateView$', MettingView.MettingmasterUpdateView.as_view(), name="MettingmasterUpdateView"),
    url(r'^metting/MettingmasterDeleteView/(?P<pk>[^/]+)$$', MettingView.MettingmasterDeleteView.as_view(), name="MettingmasterDeleteView"),
    url(r'^metting/MettingdetailView', MettingView.MettingdetailView.as_view(), name="MettingdetailView"),
    url(r'^metting/MettingdetailCreateView', MettingView.MettingdetailCreateView.as_view(), name="MettingdetailCreateView"),
    url(r'^metting/MettingdetailDeleteView/(?P<pk>[^/]+)$$', MettingView.MettingdetailDeleteView.as_view(), name="MettingdetailDeleteView"),
    url(r'^metting/get_metting_item', MettingView.get_metting_item, name="get_metting_item"),
    url(r'^metting/get_metting_tree', MettingView.get_metting_tree, name="get_metting_tree"),
    url(r'^metting/get_metting_undone', MettingView.get_metting_undone, name="get_metting_undone"),
    url(r'^metting/delete_met_project', MettingView.delete_met_project, name="delete_met_project"),
    url(r'^metting/save_met_file', MettingView.save_met_file, name="save_met_file"),
    url(r'^metting/analysis_meeting', MettingView.analysis_meeting, name="analysis_meeting"),
    url(r'^metting/browse_task_image', MettingView.browse_task_image, name="browse_task_image"),
    url(r'^metting/DocumentDeleteView/(?P<pk>[^/]+)$$', MettingView.DocumentDeleteView.as_view(), name="DocumentDeleteView"),
    url(r'^metting/get_combobox_topic', MettingView.get_combobox_topic, name="get_combobox_topic"),
    url(r'^metting/get_combobox_mettopic', MettingView.get_combobox_mettopic, name="get_combobox_mettopic"),
    url(r'^metting/MeetingmanagerMastView$', MettingView.MeetingmanagerMastView.as_view(), name="MeetingmanagerMastView"),    
    url(r'^metting/MeetingmanagerDetailView$', MettingView.MeetingmanagerDetailView.as_view(), name="MeetingmanagerDetailView"),    
    url(r'^metting/topic_get_metting$', MettingView.topic_get_metting, name="topic_get_metting"),    
    url(r'^metting/update_meetingid$', MettingView.update_meetingid, name="update_meetingid"),    
    url(r'^metting/create_met_item$', MettingView.create_met_item, name="create_met_item"),    
    url(r'^metting/check_met_topic$', MettingView.check_met_topic, name="check_met_topic"),    
    url(r'^metting/TpdetailView$', MettingView.TpdetailView, name="TpdetailView"),    
    url(r'^metting/get_Improvement$', MettingView.get_Improvement, name="get_Improvement"),
    url(r'^metting/get_Improvement_item$', MettingView.get_Improvement_item, name="get_Improvement_item"),
    url(r'^metting/get_credits$', MettingView.get_credits, name="get_credits"),
    url(r'^metting/get_Mettingma$', MettingView.get_Mettingma, name="get_Mettingma"),
    
    url(r'^metting/MeetingTopicView$', MettingView.MeetingTopicView.as_view(), name="MeetingTopicView"),
    

    url(r'^task/get_task_file$', MettingView.get_task_file, name="get_task_file"),    
    url(r'^task/get_requirement_task$', MettingView.get_requirement_task, name="get_requirement_task"),    
    


    url(r'^metting/newMeeting$', auth_page("PMISLooper/metting/newMeeting.html"), name="newMeeting"), 
    url(r'^goal/goal_management_old$', auth_page("PMISLooper/goal/goalManagementOld.html"), name="goalManagementOld"), 
    url(r'^goal/goal_management$', auth_page("PMISLooper/goal/goalManagement.html"), name="goalManagement"), 
    url(r'^goal/search_goal$', GoalManagement_View.search_goal, name="search_goal"),    

    url(r'^testing$', auth_page("PMISLooper/testing/testing.html"), name="testing"), 
    url(r'^testing/get_sys_tree$',TestingView.get_system_tree, name="get_sys_tree"), 
    url(r'^testing/get_sys_frm$',TestingView.get_sys_frm, name="get_sys_frm"), 
    url(r'^testing/get_template_excel$',TestingView.get_template_excel, name="get_template_excel"), 
    url(r'^testing/upload_excel$',TestingView.upload_excel, name="upload_excel"), 
    url(r'^testing/note_tab$',TestingView.TestingNotesTable.as_view(), name="note_tab"), 
    url(r'^testing/add$',TestingView.TestingNotesCreate.as_view(), name="tseting_add"), 
    url(r'^testing/update$',TestingView.TestingNotesUpdate.as_view(), name="tseting_update"), 
    url(r'^testing/delete/(?P<pk>[^/]+)$',TestingView.TestingNotesDelete.as_view(), name="tseting_delete"), 

    url(r'^technicalUseRecord$', auth_page("PMISLooper/technic/TechnicalUseRecord.html"), name="technicalUseRecord"), 
    url(r'^technicalUseRecord/table$',TechnicalUseRecordView.TechnicaluserecordTable.as_view(), name="technicalUseRecord_table"), 
    url(r'^technicalUseRecord/add$',TechnicalUseRecordView.TechnicaluserecordCreate.as_view(), name="technicalUseRecord_add"), 
    url(r'^technicalUseRecord/update$',TechnicalUseRecordView.TechnicaluserecordUpdate.as_view(), name="technicalUseRecord_update"), 
    url(r'^technicalUseRecord/delete/(?P<pk>[^/]+)$',TechnicalUseRecordView.TechnicaluserecordDelete.as_view(), name="technicalUseRecord_delete"), 
    url(r'^technicalUseRecord/technical$',TechnicalUseRecordView.getTechnicalInfo, name="getTechnicalInfo"), 

    url(r'^top_porject/batch_set_MHTask$',top_projectView.batch_set_MHTask, name="batch_set_MHTask"), 

    
    url(r'^frame/search_frames_list$',FrameUpdateView.search_frames_list, name="search_frames_list"), 

    url(r'^task/faqAnalysisTask$', auth_page("PMISLooper/task/FaqAnalysisTask.html"), name="faqAnalysisTask"), 
    url(r'^task_dashboard$', auth_page("PMISLooper/dashboard/TaskDashboard.html"), name="TaskDashboard"), 
    url(r'^projectFollowUp$', auth_page("PMISLooper/temp/projectFollowUp.html"), name="projectFollowUp"), 
    url(r'^task_dashboard/get_data', TaskDashboardView.getData, name="task_dashboard_get_data"),
    url(r'^documentManagement$', auth_page("PMISLooper/temp/documentManagement.html"), name="documentManagement"), 
    url(r'^notif/create', NotificationView.CreatePmstrView.as_view(), name="create_notif"),
    url(r'^notif/update/(?P<pk>[^/]+)$', NotificationView.UpdatePmstrView.as_view(), name="update_notif"),
    url(r'^notif/delete/(?P<pk>[^/]+)$', NotificationView.DeletePmstrView.as_view(), name="delete_notif"),
    url(r'^notif/get_pmstr_with_task$', NotificationView.getPmstrWithTask, name="get_pmstr_with_task"),
    url(r'^notif/user_know$', NotificationView.userKnow, name="notif_user_know"),
    url(r'^notif/assign_task$', NotificationView.assignTask, name="notif_user_assign_task"),

    # 模組及場景管理PMSSessionFrm
    url(r'^session_manager$', auth_page("PMISLooper/session/PmsSessionManager.html"), name="session_manager"), 
    url(r'^session_manager/get_vtask_list_tree$', PmsSessionManager.get_vtask_list_tree, name="get_vtask_list_tree"), 
    url(r'^session_manager/get_filtered_tasks$', PmsSessionManager.get_filtered_tasks, name="get_filtered_tasks"), 
    url(r'^session_manager/get_tasks$', PmsSessionManager.GetTasksView.as_view(), name='get_tasks'),
    url(r'^session_manager/get_conditon_data$', PmsSessionManager.get_sqlscript_data, name='get_conditon_data'),
    url(r'^session_manager/get_category_data$', PmsSessionManager.get_category_data, name='get_category_data'),
    url(r'^session_manager/approve_condition$', PmsSessionManager.approve_condition, name='approve_condition'),
    url(r'^session_manager/promtsql', PmsSessionManager.get_promtsql_by_inc_id, name='get_promtsql_by_inc_id'),
    url(r'^session_manager/get_user_prompt_approve', PmsSessionManager.get_user_prompt_approve, name='get_user_prompt_approve'),
    url(r'^session_manager/session_group_task$', PmsSessionManager.session_group_task, name='session_group_task'),
    url(r'^session_manager/get_session_list$', PmsSessionManager.get_session_list, name='get_session_list'),
    url(r'^session_manager/execute_sql$', PmsSessionManager.execute_sql, name='execute_sql'),
    url(r'^session_manager/get_sysbugno$', PmsSessionManager.get_sysbugno, name='get_sysbugno'),

    #session manager的meeting相關
    url(r'^session_manager/get_meeting_master$', PmsSessionManager.get_meeting_master, name="get_meeting_master"), 
    url(r'^session_manager/get_meeting_detail$', PmsSessionManager.get_meeting_detail, name="get_meeting_detail"), 

    #session manager的goal相關
    url(r'^session_manager/get_Goal_master$', PmsSessionManager.get_Goal_master, name="get_Goal_master"), 

    # session manage的 technical相關
    url(r'^session_manager/get_technical$', PmsSessionManager.get_technical, name="get_technical"), 

    # 查詢參數管理
    url(r'^aicondition_manager$', auth_page("PMISLooper/session/AIConditionManager.html"), name="aicondition_manager"),
    url(r'^promtsql/table$',AIConditionManagerView.PromtsqlTableView.as_view(), name="promtsql_table"), 
    url(r'^promtsql/insert$', AIConditionManagerView.PromtsqlCreateView.as_view(), name="promtsql_insert"),
    url(r'^promtsql/update$', AIConditionManagerView.PromtsqlUpdateView.as_view(), name="promtsql_update"),
    # url(r'^promtsql/delete/(?P<pk>[^/]+)$', AIConditionManager.PromtsqlDeleteView.as_view(), name="promtsql_delete"),
    url(r'^promtsql/batch_delete$', AIConditionManagerView.batch_delete, name="batch_delete"),
    url(r'^promptcategorytbl/table$',AIConditionManagerView.PromptcategoryTblTableView.as_view(), name="promptcategorytbl_table"), 
    url(r'^category/insert$',AIConditionManagerView.PromptcategoryTblCreateView.as_view(), name="category_insert"),
    url(r'^category/update$',AIConditionManagerView.PromptcategoryTblUpdateView.as_view(), name="category_update"),
    url(r'^category/batch_delete$', AIConditionManagerView.category_batch_delete, name="category_batch_delete"),
    url(r'^category/array$', AIConditionManagerView.get_category_array, name="category_array"),
    
    url(r'^chatbot_question_manager$', auth_page("PMISLooper/session/ChatbotQuestionManagementOverview.html"), name="chatbot_question_manager"),
]

urlpatterns += staticfiles_urlpatterns()    