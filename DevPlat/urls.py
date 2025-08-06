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
from django.urls import path, include
from . import views
#from BaseApp.library.tools.UrlTools import page
from .ViewsFloder import (View_Projects, View_Session, 
    View_Requement, View_Speification,View_Question,View_Course,
        View_Solution, View_RuleDoc,View_controlCenter,View_SessionLog,View_Design)
from .ViewsFloder.View_Speification import (DocmcTableView, DocmcCreateView, DocmcUpdateView, DocmcDeleteView,
                                          DocmeTableView, DocmeCreateView, DocmeUpdateView, DocmeDeleteView)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def auth_page(url:str):
    @login_required()
    def dynamic_template(request):
        return render(request, url)
    return dynamic_template

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.index, name="DevPlat"),
    url(r'^project/overview$', auth_page("DevPlat/projects.html"), name="project_index"),
    url(r'^project/list$', View_Projects.search_project, name="project_list"),
    url(r'^project/get_mindmap_id$', View_Projects.getProjectMindmap, name="getProjectMindmap"),
    url(r'^project/search_mustTasks$', View_Projects.search_mustTasks, name="search_mustTasks"),
    url(r'^sessions$', auth_page("DevPlat/dev_sessions.html"), name="dev_session"),
    url(r'^select_TaskID$', View_Speification.TaskIDTableView.as_view(), name="select_TaskID"),
    url(r'^save_docwin$', View_Speification.TaskSaveDocwin.as_view(), name="save_docwin"),
    url(r'^course$', auth_page("DevPlat/course.html"), name="dev_course"),
    url(r'^session/question$', auth_page("DevPlat/question.html"), name="dev_session_question"),
    url(r'^ruledoc$', auth_page("DevPlat/ruledoc.html"), name="ruledoc"),
    url(r'^sessions_list$', View_Session.session_list, name="devplat_session_list"),
    url(r'^session/question_doc', View_Session.questionDocWithChatgpt, name="question_doc_with_chatgpt"),
    url(r'^session/get_frame_dictionary', View_Session.get_frame_dictionary, name="get_frame_dictionary"),
    url(r'^session/get_frame_data', View_Session.get_frame_data, name="get_frame_data"),
    url(r'^requement/create$', View_Requement.RequirementCreateView.as_view(), name="requement_create"),
    url(r'^requement/update', View_Requement.RequirementUpdateView.as_view(), name="requement_update"),
    url(r'^requement/delete/(?P<pk>[^/]+)$$', View_Requement.RequirementDeleteView.as_view(), name="requement_delete"),
    url(r'^requement/list$', View_Requement.RequirementTableView.as_view(), name="requement_list"),
    url(r'^requement/req_task_list$', View_Requement.get_requirement_task, name="req_task_list"),
    url(r'^course/create$', View_Course.CourseCreateView.as_view(), name="course_create"),
    url(r'^course/update', View_Course.CourseUpdateView.as_view(), name="course_update"),
    url(r'^course/delete/(?P<pk>[^/]+)$$', View_Course.CourseDeleteView.as_view(), name="course_delete"),
    url(r'^course/list$', View_Course.CourseTableView.as_view(), name="course_list"),
    url(r'^solution/create$', View_Solution.SolutionTypeCreateView.as_view(), name="solution_create"),
    url(r'^solution/update', View_Solution.SolutionTypeUpdateView.as_view(), name="solution_update"),
    url(r'^solution/delete/(?P<pk>[^/]+)$$', View_Solution.SolutionTypeDeleteView.as_view(), name="solution_delete"),
    url(r'^solution/list$', View_Solution.SolutionTypeTableView.as_view(), name="solution_list"),
    url(r'^requement/gettypes$', View_Requement.get_requirement_type, name="requement_gettypes"),
    url(r'^question/post$', View_Question.CreateTaskView.as_view(), name="question_post"),
    url(r'^question/content_search$', View_Question.content_search, name="content_search"),
    url(r'^spec/list$', View_Speification.SpecTableView.as_view(), name="spec_list"),
    url(r'^spec/show_pdf$', View_Speification.show_spec_pdfdoc, name="spec_show_pdf"),
    url(r'^spec/create$',View_Speification.SpecCreateView.as_view(),name="technical_create"),
    url(r'^spec/update$', View_Speification.SpecUpdateView.as_view(),name="technical_update"),
    url(r'^spec/edit/get_max_verno$', View_Speification.get_max_verno, name="get_max_verno"),
    url(r'^spec/get_system$', View_Speification.get_system, name="get_system"),
    url(r'^spec/edit/docmb_list$', View_Speification.DocmbTableView.as_view(), name="docmb_list"),
    url(r'^spec/docmb/create$', View_Speification.DocmbCreateView.as_view(), name="docmb_create"),
    url(r'^spec/docmb/update$', View_Speification.DocmbUpdateView.as_view(), name="docmb_update"),
    url(r'^spec/docmb/delete/(?P<pk>[^/]+)$', View_Speification.DocmbDeleteView.as_view(), name="docmb_delete"),
    url(r'^spec/edit/docmh_list$', View_Speification.DocmhTableView.as_view(), name="docmh_list"),
    url(r'^spec/docmh/create$', View_Speification.DocmhCreateView.as_view(), name="docmh_create"),
    url(r'^spec/docmh/update$', View_Speification.DocmhUpdateView.as_view(), name="docmh_update"),
    url(r'^spec/docmh/delete/(?P<pk>[^/]+)$', View_Speification.DocmhDeleteView.as_view(), name="docmh_delete"),
    url(r'^spec/edit/docmi_list$', View_Speification.DocmiTableView.as_view(), name="docmi_list"),
    url(r'^spec/docmi/create$', View_Speification.DocmiCreateView.as_view(), name="docmi_create"),
    url(r'^spec/docmi/update$', View_Speification.DocmiUpdateView.as_view(), name="docmi_update"),
    url(r'^spec/docmi/delete/(?P<pk>[^/]+)$', View_Speification.DocmiDeleteView.as_view(), name="docmi_delete"),
    url(r'^spec/edit/docmj_list$', View_Speification.DocmjTableView.as_view(), name="docmj_list"),
    url(r'^spec/docmj/create$', View_Speification.DocmjCreateView.as_view(), name="docmj_create"),
    url(r'^spec/docmj/update$', View_Speification.DocmjUpdateView.as_view(), name="docmj_update"),
    url(r'^spec/docmj/delete/(?P<pk>[^/]+)$', View_Speification.DocmjDeleteView.as_view(), name="docmj_delete"),
    # Docmc URLs
    url(r'^spec/edit/docmc_list$', View_Speification.DocmcTableView.as_view(), name="docmc_list"),
    url(r'^spec/docmc/create$', View_Speification.DocmcCreateView.as_view(), name="docmc_create"),
    url(r'^spec/docmc/update$', View_Speification.DocmcUpdateView.as_view(), name="docmc_update"),
    url(r'^spec/docmc/delete/(?P<pk>[^/]+)$', View_Speification.DocmcDeleteView.as_view(), name="docmc_delete"),
    # Docme URLs
    url(r'^spec/edit/docme_list$', View_Speification.DocmeTableView.as_view(), name="docme_list"),
    url(r'^spec/docme/create$', View_Speification.DocmeCreateView.as_view(), name="docme_create"),
    url(r'^spec/docme/update$', View_Speification.DocmeUpdateView.as_view(), name="docme_update"),
    url(r'^spec/docme/delete/(?P<pk>[^/]+)$', View_Speification.DocmeDeleteView.as_view(), name="docme_delete"),
    url(r'^spec/get_external_problems$', View_Speification.get_external_problems, name="get_external_problems"),
    url(r'^tecreq/list$', View_Requement.TecRequirementTableView.as_view(), name="tecreq_list"),
    url(r'^tecreq/create$', View_Requement.TecRequirementCreateView.as_view(), name="tecreq_create"),
    url(r'^tecreq/update$', View_Requement.TecRequirementUpdateView.as_view(), name="tecreq_update"),
    url(r'^tecreq/delete/(?P<pk>[^/]+)$', View_Requement.TecRequirementDeleteView.as_view(), name="tecreq_delete"),
    url(r'^spec/docmb/show_image$', View_Speification.getDocmbImage, name="docmb_image"),
    url(r'^ruledoc/list$', View_RuleDoc.RuledocTableView.as_view(), name="ruledoc_list"),
    url(r'^ruledoc/create$', View_RuleDoc.RuledocCreateView.as_view(), name="ruledoc_create"),
    url(r'^ruledoc/update$', View_RuleDoc.RuledocUpdateView.as_view(), name="ruledoc_update"),
    url(r'^ruledoc/delete/(?P<pk>[^/]+)$', View_RuleDoc.RuledocDeleteView.as_view(), name="ruledoc_delete"),
    url(r'^ccenter/search_ControlCentre$', View_controlCenter.search_ControlCentre, name="search_ControlCentre"),
    url(r'^log/get$', View_SessionLog.get, name="session_log_get"),
    url(r'^log/save$', View_SessionLog.save, name="session_log_save"),
    url(r'^design/get_projects_design_doc$', View_Design.getDesignDOC, name="get_projects_design_doc"),

    url(r'^session/log_page$', auth_page("DevPlat/SessionLog.html")),
    url(r'^session/log_table$', View_SessionLog.SessionLogTableView.as_view(), name="SessionLogTableView"),
    url(r'^session/log_add$', View_SessionLog.SessionLogCreateView.as_view(), name="SessionLogCreateView"),
    url(r'^session/log_update$', View_SessionLog.SessionLogUpdateView.as_view(), name="SessionLogUpdateView"),
    url(r'^session/log_delete/(?P<pk>[^/]+)$', View_SessionLog.SessionLogDeleteView.as_view(), name="SessionLogDeleteView"),
    url(r'^session/get_type$', View_SessionLog.getSessionTypeData, name="getSessionTypeData"),
    url(r'^session/get_session_name$', View_SessionLog.getSessionName, name="get_session_name"),
    
    url(r'^test$', auth_page("DevPlat/test.html"))

]
