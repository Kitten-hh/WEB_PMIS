from django.conf.urls import url,include
from django.urls import path
from BaseApp.library.tools import UrlTools
from .ViewsFolder import ScheduleView,ScheduleDashboardView
from rest_framework import routers
from .ViewsFolder.RestApi import TaskForAIView
from WEB_PMIS.tools import UrlTools as LocaleUrlTools

router = routers.DefaultRouter()

router.register(r'chattopic', TaskForAIView.ChattopictblViewSet)
router.register(r'prompt', TaskForAIView.PrompttblViewSet)
router.register(r'promptsql', TaskForAIView.PromtsqlViewSet)

urlpatterns = [
    url(r'^set_sch_priority$', LocaleUrlTools.protected_auth_page("ScheduleApp/SchedulePriority.html", None,"ProjectSession_Prioirty", 4), name="set_sch_priority"),
    url(r'^subproject_table$', ScheduleView.SubProjectSchView.as_view(), name="subproject_table"),
    url(r'^session_table$', ScheduleView.SessionSchView.as_view(), name="session_table"),
    url(r'^batch_update_priority$', ScheduleView.batch_update_priority, name="batch_update_priority"),
    url(r'^schedule_distribution$', UrlTools.auth_page("ScheduleApp/ScheduleDistrMap.html"), name="display_schedule_distribution"),
    url(r'^schedule_dashboard$', UrlTools.auth_page("ScheduleApp/ScheduleDashboard.html"), name="sch_schedule_dashboard_page"),   
    url(r'^get_schedule_dashboard_data$', ScheduleDashboardView.getData, name="get_data_sch_schedule_dashboard"),   
    url(r'^call_service$', ScheduleView.callScheduleService, name="schedule_call_service"),   
    url(r'^get_schedule_prarms$', ScheduleView.getSchedulePrarms, name="get_schedule_prarms"),   
    url(r'^update_schedule_prarms$', ScheduleView.updateScheduleParams, name="update_schedule_prarms"),   
    url(r'^save_params_history$', ScheduleView.saveScheduleParamsHistory, name="save_params_history"),   
    url(r'^get_params_history_list$', ScheduleView.getScheduleParamsHistoryList, name="get_params_history_list"),
    url(r'^load_params_history$', ScheduleView.loadScheduleParamsFromHistory, name="load_params_history"),
    url(r'^del_params_history$', ScheduleView.delScheduleParamsFromHistory, name="del_params_history"),
    path('api/', include(router.urls)),
    url(r"^promptsql/get_data", TaskForAIView.getDataWithPromtSql, name="promptsql_get_data"),
    url(r"^promptsql/expand_prompt_data", TaskForAIView.expandPromptData, name="promptsql_expand_prompt_data"),
    url(r"^api/generate_task", TaskForAIView.generateTaskWithAiResult, name="api_generate_task"),
    url(r"^api/save_to_db", TaskForAIView.saveToDB, name="save_to_db"),
    url(r"^api/get_prompt_answer_data", TaskForAIView.getPromptAnswerData, name="get_prompt_answer_data"),
    url(r"^api/get_action_page", TaskForAIView.getActionPage, name="get_action_page"),
    url(r'^api/generate_prompts$', TaskForAIView.generatePrompt, name='generate_prompts'),
    url(r'^api/get_task_category$', TaskForAIView.getTaskCategory, name='get_task_category'),
    
    #url(r'^get_project_dashboard_data$', ScheduleDashboardView.ScheduleDashboardTableView.as_view(), name="get_project_dashboard_data"),   
]