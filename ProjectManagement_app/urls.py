from django.conf.urls import url,include
from django.urls import path
from BaseApp.library.tools.UrlTools import auth_page
from rest_framework import routers
from .Views import ProjectMilestoneView,SessionView

#router = routers.DefaultRouter()

#router.register(r'chat_history', ChatHistory_view.ChatHistoryViewSet)
#router.register(r'chattopic', TaskForAIView.ChattopictblViewSet)

urlpatterns = [
    url(r"^project_milestone$", auth_page("ProjectManagement_app/ProjectMilestone.html"), name="project_milestone"),
    url(r"^project_gantt_modal$", auth_page("ProjectManagement_app/ProjectGanttModal.html"), name="project_gantt_modal"),
    url(r"project_milestone/get_session_and_task", ProjectMilestoneView.get_sessions_and_tasks, name="get_session_and_task"),
    url(r"project_milestone/get_milestone_info", ProjectMilestoneView.getMilestoneInfo, name="get_milestone_info"),
    url(r"project_milestone/get_project_summary_id", ProjectMilestoneView.getProjectSummaryId, name="get_project_summary_id"),
    url(r"project_milestone/get_tasks", ProjectMilestoneView.getTasks, name="project_milestone_get_tasks"),
    url(r"project_milestone/get_session_tasks", ProjectMilestoneView.getTaskWithSession, name="project_milestone_get_session_tasks"),
    url(r"session/delete", SessionView.TaskListDeleteView.as_view(), name="session_delete"),
    url(r"session/get_relation_info", SessionView.getSessionRelationInfo, name="session_get_relation_info"),
    url(r"translate", ProjectMilestoneView.translate, name="ai_translate")
    #path('api/', include(router.urls)),
]