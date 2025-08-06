from django.conf.urls import url
from PMIS.ViewsFolder import views_user
from django.urls import path
from . import views
from .ViewsFolder import SystemBugRptView

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.shortcuts import render
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
    url(r'^$', auth_page("SystemBugRpt_app/SystemBugRpt.html"), name="systembugrpt"),
    url(r'^admrp_table$',SystemBugRptView.get_admrpTable, name="admrp_table"),
    url(r'^cmsme_table$',SystemBugRptView.get_cmsmeArray, name="cmsme_table"),
    url(r'^get_admrpno$',SystemBugRptView.getAdmrpNo, name="get_admrpno"),
    url(r'^admrp/create$',SystemBugRptView.admrpCreate, name="admrp_create"),
    url(r'^admrp/delete$',SystemBugRptView.admrpDelete, name="admrp_delete"),
    url(r'^admrp/update$',SystemBugRptView.admrpUpdate, name="admrp_update"),
    url(r'^admrp/get$',SystemBugRptView.getMasterInfo, name="admrp_get"),
    url(r'^subproject$',SystemBugRptView.get_subprojectTable, name="subproject"),
    url(r'^module_array$',SystemBugRptView.get_moduleArray, name="module_array"),
    url(r'^moduleobject_array$',SystemBugRptView.get_moduleObjectArray, name="moduleobject_array"),
    url(r'^admrq/create$',SystemBugRptView.admrqCreate, name="admrq_create"),
    url(r'^get_admrqno$',SystemBugRptView.getAdmrqNo, name="get_admrqno"),
    url(r'^get_admrqimg$',SystemBugRptView.getAdmrqImg, name="get_admrqimg"),
    url(r'^admrqimg_save$',SystemBugRptView.admrqImgSave, name="admrqimg_save"),
    url(r'^upload_imgarray$',SystemBugRptView.uploadImgArray, name="upload_imgarray"),
    url(r'^get_imgarray$',SystemBugRptView.getImgArray, name="get_imgarray"),
    url(r'^admrf_table$',SystemBugRptView.get_admrfTable, name="admrf_table"),
    url(r'^get_admrfno$',SystemBugRptView.getAdmrfNo, name="get_admrfno"),
    url(r'^admrf/create$',SystemBugRptView.admrfCreate, name="admrf_create"),
    url(r'^admrf/update$',SystemBugRptView.admrfUpdate, name="admrf_update"),
    url(r'^admrf/delete$',SystemBugRptView.admrfDelete, name="admrf_delete"),
    url(r'^task_table$',SystemBugRptView.get_taskTable, name="systembugrpt_task_table"),
    url(r'^project_table$',SystemBugRptView.get_projectTable, name="systembugrpt_project_table"),
    url(r'^tasklist_table$',SystemBugRptView.get_taskListTable, name="systembugrpt_tasklist_table"),
    url(r'^get_userdefaultproject$',SystemBugRptView.getUserDefaultProject, name="get_userdefaultproject"),
    url(r'^checkpidexist$',SystemBugRptView.checkPidExist, name="checkpidexist"),
    url(r'^checktidexist$',SystemBugRptView.checkTidExist, name="checktidexist"),
    url(r'^gettaskno$',SystemBugRptView.getTaskNo, name="gettaskno"),
    url(r'^pmsut_save$',SystemBugRptView.pmsutSave, name="pmsut_save"),
    url(r'^get_defaultpro$',SystemBugRptView.getDefaultPro, name="get_defaultpro"),
    url(r'^user_table$',SystemBugRptView.get_userTable, name="user_table"),
    url(r'^task/create$',SystemBugRptView.taskCreate, name="task_create"),
    url(r'^vtask_table$',SystemBugRptView.get_vtaskTable, name="vtask_table"),
    url(r'^taskitem_table$',SystemBugRptView.get_taskItemTable, name="taskitem_table"),
    url(r'^get_systembugfile$',SystemBugRptView.get_systemBugFile, name="get_systembugfile"),
    url(r'^download_file$',SystemBugRptView.download_file, name="download_file"),
    url(r'^get_taskrelation$',SystemBugRptView.get_taskRelation, name="get_taskrelation"),
    url(r'^preview_file$',SystemBugRptView.preview_file, name="preview_file"),
    url(r'^get_solutiontype_table$',SystemBugRptView.get_solutiontypeTable, name="get_solutiontype_table"),
    url(r'^get_problemcategory$',SystemBugRptView.get_problemCategory, name="get_problemcategory"),
    url(r'^get_flowchart$',SystemBugRptView.get_flowChart, name="get_flowchart"),
    url(r'^get_flowChartInfo$',SystemBugRptView.get_flowChartInfo, name="get_flowChartInfo"),
    url(r'^flowchart/create$',SystemBugRptView.flowchart_create, name="flowchart_create"),
    url(r'^flowchart/update$',SystemBugRptView.flowchart_update, name="flowchart_update"),
    url(r'^flowchart/delete$',SystemBugRptView.flowchart_delete, name="flowchart_delete"),
    url(r'^get_docmhTable$',SystemBugRptView.get_docmhTable, name="get_docmhTable"),
    url(r'^fetch_sysbug_table$',SystemBugRptView.fetchSysBugTable, name="fetch_sysbug_table"),
    url(r'^execute_sql$',SystemBugRptView.execute_sql, name="execute_sql"),
    url(r'^get_vtasklist$',SystemBugRptView.get_vtasklist, name="get_vtasklist"),
    # url(r'^admrq/delete$',SystemBugRptView.admrqDelete, name="admrq_delete"),

    url(r'^refresh_csrf$',SystemBugRptView.refresh_csrf, name="refresh_csrf"),

]

urlpatterns += staticfiles_urlpatterns()    