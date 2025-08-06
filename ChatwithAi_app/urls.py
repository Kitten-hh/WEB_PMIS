from django.conf.urls import url,include
from django.urls import path
from BaseApp.library.tools import UrlTools
from rest_framework import routers
from .Views import ChatTopics_view, Subproject_view,Prompt_view,ChatHistory_view,ProjectStatus_view,DocumentView
from .Views.ConversationServiceView import ConversationServiceView,ConversationServiceViewOld
from .Views.SystemOperationView import GetSimilarPagesView
from .Views.ActionsView import GetSimilarActionsView, GetActionView

router = routers.DefaultRouter()

router.register(r'chat_history', ChatHistory_view.ChatHistoryViewSet)
router.register(r'document', DocumentView.DocumentViewSet)

#router.register(r'chattopic', TaskForAIView.ChattopictblViewSet)

urlpatterns = [
    url(r"^get_chat_topics", ChatTopics_view.get_chat_topics, name="get_chat_topics"),
    url(r"^create_project", Subproject_view.create_project, name="create_project_api"),
    url(r"^save_prompt", Prompt_view.save_prompt, name="chatwithai_save_prompt"),
    url(r"project_status/update", ProjectStatus_view.UpdateAiSummaryRecordView.as_view(), name="update_project_status_page"),
    url(r'^project_status$', UrlTools.auth_page("ChatwithAi_app/ProjectStatus.html"), name="project_status_page"),    
    # url(r"^save_chat", ChatHistory_view.save_chat, name="save_chat"),
    path("api/similar-pages/", GetSimilarPagesView.as_view(), name="get_similar_pages"),    
    path('api/get-similar-actions/', GetSimilarActionsView.as_view(), name='get_similar_actions'),
    path('api/identify-action/', GetActionView.as_view(), name='identify_actions'),
    path('api/conversation/', ConversationServiceView.as_view(), name='conversation_service'),
    path('api/conversationold/', ConversationServiceViewOld.as_view(), name='conversation_service_old'),
    path('api/', include(router.urls)),
]