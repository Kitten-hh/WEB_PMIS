from django import forms
from . import models
from django.forms.models import ModelFormMetaclass,ModelFormOptions
from . models import Task,Goalmaster,Goaldetail, Task
from django.utils.translation import gettext as _, gettext_lazy as __

class Task_Form(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        labels = {
            'adjustscore':__('adjustscore'),
            'appraisalid':__('appraisalid'),
            'bdate':__('實際開始時間'),
            'company':__('公司名稱'),
            'create_date':__('創建日期'),
            'creator':__('創建人'),
            'calpriority':__('計算的優先順序'),
            'categoryid':__('categoryid'),
            'charge':__('收費'),
            'class_field':__('class'),
            'classify':__('classify'),
            'comment':__('comment'),
            'companyid':__('companyid'),
            'contact':__('聯繫人'),
            'correctness':__('correctness'),
            'cycletask':__('是否迴圈任務'),
            'dayjob':__('dayjob'),
            'delayday':__('脫期天數'),
            'diff':__('diff'),
            'difficulty':__('difficulty'),
            'dispose':__('任務處理標記'),
            'docpath':__('文檔路徑'),
            'edate':__('實際結束時間'),
            'escore':__('預計績效分'),
            'editionid':__('版本號'),
            'emaildesp':__('郵件內容'),
            'environmentid':__('environmentid'),
            'etime':__('計畫天數'),
            'flag':__('修改次數'),
            'flowchartno':__('流程圖編號'),
            'generateddoc':__('generateddoc'),
            'hoperation':__('操作'),
            'isschedule':__('是否排期'),
            'modifier':__('修改人'),
            'modi_date':__('修改日期'),
            'manday':__('manday'),
            'mastno':__('範本編號'),
            'oldprogress':__('原進度'),
            'pid':__('項目編號'),
            'planbdate':__('計畫開始時間'),
            'planedate':__('計畫結束時間'),
            'priority':__('優先順序'),
            'process':__('處理'),
            'progress':__('進度'),
            'progressprocent':__('progressprocent'),
            'quantity':__('數量'),
            'questionno':__('questionno'),
            'r_flag':__('已讀'),
            'rank':__('rank'),
            'reference':__('三考'),
            'relationgoalid':__('上級goal編號'),
            'remark':__('備註'),
            'reply_taskno':__('reply_taskno'),
            'req_date':__('req_date'),
            'requestdate':__('需求日期'),
            'revisedby':__('修改人'),
            'saday':__('saday'),
            'smsreceiver':__('短信接收人'),
            'spaday':__('spaday'),
            'spday':__('計畫天數'),
            'schpriority':__('排期優先順序'),
            'schprioritysp':__('調整排期優先順序'),
            'schedulestate':__('排期狀態'),
            'score':__('績效分'),
            'sendctlemail':__('sendctlemail'),
            'setting':__('setting'),
            'sortno':__('sortno'),
            'special':__('特製'),
            'subprojectid':__('subprojectid'),
            'subtasktype':__('子分類編號'),
            't_stamp':__('更新時間'),
            'task':__('任務描述'),
            'taskid':__('任務編號'),
            'tasktype':__('任務類別'),
            'taskoption':__('taskoption'),
            'tid':__('工作編號'),
            'totalscore':__('totalscore'),
            'udf01':__('樣板號'),
            'udf02':__('關聯任務狀態'),
            'udf03':__('自訂欄位'),
            'udf04':__('窗口名稱'),
            'udf05':__('自訂欄位'),
            'udf06':__('udf06'),
            'udf07':__('udf07'),
            'udf08':__('udf08'),
            'udf09':__('上報人'),
            'udf10':__('樣板單別'),
            'udf11':__('人報部門'),
            'udf51':__('自訂欄位'),
            'udf52':__('自訂欄位'),
            'usr_group':__('用戶組'),
            'atime':__('實際天數'),
            'relationid':__('關聯任務')
        }

class Task_Form_NoValidate_Unique(Task_Form):
    def validate_unique(self):
        pass

class VGoalMaster_Form(forms.ModelForm):
    class Meta:
        model = models.VGoalmaster
        fields = '__all__'
        labels = {
            'period':__('季度'),
            'contact':__('聯繫人'),
            'recordid':__('子工程編號'),
            'gtype':__('目標類型'),
            'objective':__('季度工程'),
            'bdate':__('開始日期'),
            'edate':__('結束日期'),
            'project':__('工程編號'),
            'desp':__('描述'),
            'escore':__('預計績效分'),
            'ascore':__('實際績效分'),
            'management':__('管理分'),
            'performance':__('跟進分'),
            'comment':__('備註'),
            'company':__('company'),
            'creator':__('creator'),
            'usr_group':__('usr_group'),
            'create_date':__('create_date'),
            'modifier':__('modifier'),
            'modi_date':__('modi_date'),
            'flag':__('flag'),
            'itemno':__('序號'),
            'manday':__('manday'),
            'difficulty':__('difficulty'),
            'sortno':__('sortno'),
            'pschedule':__('計畫進度'),
            'aschedule':__('實際進度')
        }
class Schperiod_Form(forms.ModelForm):
    class Meta:
        model = models.Schperiod
        fields = '__all__'
        labels = {        
            'company':__('COMPANY'),
            'creator':__('CREATOR'),
            'usr_group':__('USR_GROUP'),
            'create_date':__('CREATE_DATE'),
            'modifier':__('MODIFIER'),
            'modi_date':__('MODI_DATE'),
            'flag':__('FLAG'),
            'period':__('Period'),
            'from_field':__('From'),
            'to':__('To'),
            'hour':__('Hour'),
            'logic':__('Logic'),
            'prefix':__('Prefix'),
            'completion':__('Completion'),
            'udf01':__('备用字段'),
            'udf02':__('备用字段'),
            'udf03':__('备用字段'),
            'udf04':__('备用字段'),
            'udf05':__('备用字段')
        }
class SchType_Form(forms.ModelForm):
    class Meta:
        model = models.Schtype
        fields = '__all__'
        labels = {
            'company':__('COMPANY'),
            'creator':__('CREATOR'),
            'usr_group':__('USR_GROUP'),
            'create_date':__('CREATE_DATE'),
            'modifier':__('MODIFIER'),
            'modi_date':__('MODI_DATE'),
            'flag':__('FLAG'),
            'typeno':__('TypeNo'),
            'typename':__('Name'),
            'logic':__('Logic'),
            'formula':__('Formula'),
            'remark':__('Remark'),
            'udf01':__('备用字段'),
            'udf02':__('order'),
            'udf03':__('备用字段'),
            'udf04':__('备用字段'),
            'udf05':__('备用字段'),            
        }

class Opportunity_Form(forms.ModelForm):
    class Meta:
        model = models.Tecmb
        # 當前為Model的所有字段"""  """
        fields = '__all__'
        labels = {
            'mb001': __('分類編號'),
            'mb002': __('序號'),
            'mb003': __('父級分類'),
            'mb004': __('Topoc'),
            'mb005': __('Contact'),
            'mb006': __('Date'),
            'mb007': __('Concept/Theory'),
            'mb008': __('Usage'),
            'mb009': __('Dependancy'),
            'mb010': __('備用字段'),
            'mb011': __('備用字段'),
            'mb012': __('備用字段'),
            'mb013': __('Qiestions'),
            'mb015': __('Categpry'),
            'mb016': __('Area'),
            'mb017': __('Reference'),
            'mb018': __('Video'),
            'mb019': __('Compulsory'),
            'mb020': __('Status'),
            'mb021': __('Script'),
            'mb022': __('Code Snippet'),
            'mb023': __('技術編號'),
            'mb024': __('Properties'),
            'mb025': __('Control'),
            'udf01': __('備用字段'),
            'udf02': __('備用字段'),
            'udf03': __('備用字段'),
            'udf04': __('備用字段'),
            'udf05': __('備用字段'),
            'pid': __('項目編號'),
            'tid': __('工作編號'),
            'taskid': __('任務編號'),
            'company': __('company'),
            'creator': __('creator'),
            'usr_group': __('usrGroup'),
            'create_date': __('createDate'),
            'modl_date': __('modlDate'),
            'flag': __('flag')
        }

class TaskType_Form(forms.ModelForm):
    class Meta:
        model = models.Tasktype
        fields = '__all__'
        labels = {
            'tasktype': __('任务类型'),
            'description': __('任务描述'),
            'Score': __('分数'),
            'id': __('id'),
        }