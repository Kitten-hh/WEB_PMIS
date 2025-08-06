from django.conf.urls import url,include
from django.urls import path
from BaseApp.library.tools import UrlTools
from rest_framework import routers
from .ViewsFolder import (NotificationView)

urlpatterns = [
    url(r'^message_summary$', UrlTools.auth_page("Notification_app/MessageSummary.html"), name="message_summary"),    
    url(r'^get_mesg_summary', NotificationView.mesg_summary, name="get_mesg_summary"),
    url(r'^get_message_list', NotificationView.get_message_list, name="get_message_list"),
    url(r'^detail_messageTable_view', NotificationView.DetailMessageTableView.as_view(), name="detail_messageTable_view"),
    url(r'^notification_setting$', UrlTools.auth_page("Notification_app/NotificationSetting.html"), name="Notification_settting_page"),    
]