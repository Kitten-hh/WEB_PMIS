from django import forms
from DataBase_MPMS import models
from DataBase_MPMS.models import Task,Goalmaster,Goaldetail, Task
from DataBase_MPMS import forms_base as fb
import BaseProject.tools.utils as utils

#The number and order of the fill must match the corresponding display form
class TaskForm(forms.Form):
    Pid = forms.CharField(max_length=16)
    Tid = forms.FloatField()
    TaskID = forms.FloatField()
    Task = forms.CharField(widget=forms.Textarea)
    contact = forms.CharField(max_length=30)
    PlanBDate = forms.DateTimeField()
    Class = forms.IntegerField()
    Remark = forms.CharField(max_length=300)
    Progress = forms.CharField(max_length=1, required=False)

class SystemBugForm(forms.Form):
    RP001 = forms.CharField(max_length=50,required=False, label='版本號') #版本號
    RP002 = forms.DateTimeField(required=False, label='提出日期') #提出日期
    RP003 = forms.CharField(max_length=50,required=False, label='提出部門') #提出部門
    RP004 = forms.CharField(max_length=20,required=False, label='提出人員') #提出人員
    RP005 = forms.CharField(widget=forms.Textarea, label='問題描述') #問題描述
    RP006 = forms.CharField(max_length=50 , required=False, label='附件') #附件
    RP007 = forms.CharField(max_length=255, required=False, label='處理方式結果') #處理方式結果
    RP008 = forms.CharField(max_length=255,required=False, label='發生問題原因') #發生問題原因
    RP009 = forms.CharField(max_length=50,required=False, label='跟進部門') #跟進部門
    RP010 = forms.CharField(max_length=20,required=False, label='跟進人') #跟進人
    RP011 = forms.CharField(max_length=2,required=False, label='狀態') #狀態
    RP012 = forms.DateTimeField(required=False, label='處理開始日期') #處理開始日期
    RP013 = forms.DateTimeField(required=False, label='處理結束日期') #處理結束日期
    RP014 = forms.CharField(widget=forms.Textarea, required=False, label='備註') #備註
    RP015 = forms.CharField(max_length=1, required=False, label='轉電腦部處理') #轉電腦部處理
    RP016 = forms.CharField(max_length=10, label='單別') #單別
    RP017 = forms.CharField(max_length=11, label='單號') #單號
    RP018 = forms.FloatField(required=False, label='自訂') #自訂
    RP019 = forms.FloatField(required=False, label='自訂') #自訂
    RP020 = forms.CharField(max_length=30,required=False, label='系統名稱') #系統名稱
    RP021 = forms.CharField(max_length=30,required=False, label='問題類型') #問題類型
    RP022 = forms.CharField(max_length=50, required=False, label='表單名稱') #表單名稱
    RP023 = forms.CharField(max_length=50, required=False, label='問題所屬專案') #問題所屬專案
    RP024 = forms.CharField(max_length=100, required=False, label='關聯Task') #關聯Task
    RP025 = forms.CharField(max_length=1, required=False, label='更新穩定版本') #更新穩定版本
    RP026 = forms.CharField(max_length=1, required=False, label='更新開發版本') #更新開發版本
    RP027 = forms.CharField(max_length=30, required=False, label='功能名稱') #功能名稱
    RP028 = forms.CharField(max_length=30, required=False, label='功能依賴物件') #功能依賴物件
    RP029 = forms.CharField(max_length=1,required=False, label='問題級別') #問題級別
    RP030 = forms.CharField(max_length=1,required=False, label='是否重要視窗') #是否重要視窗
    RP031 = forms.DateTimeField(required=False, label='計畫開始日期') #計畫開始日期
    RP032 = forms.DateTimeField(required=False, label='計畫結束日期') #計畫結束日期
    RP033 = forms.IntegerField(required=False, label='優先順序') #優先順序
    RP034 = forms.IntegerField(required=False, label='備用欄位') #備用欄位
    RP035 = forms.CharField(max_length=30, required=False, label='匯出標記') #匯出標記
    RP036 = forms.CharField(max_length=30, required=False, label='備用欄位') #備用欄位
    RP037 = forms.CharField(max_length=60, required=False, label='處理分類') #處理分類
    RP038 = forms.CharField(max_length=60, required=False, label='處理方式') #處理方式
    RP039 = forms.DateTimeField(required=False, label='上報時間') #上報時間
    RP040 = forms.CharField(max_length=20,required=False, label='設備編號') #設備編號
    RP041 = forms.CharField(max_length=20,required=False, label='固定資產編號') #固定資產編號

class GoalmasterForm(forms.ModelForm):
    class Meta:
        model = Goalmaster
        fields = '__all__'
class VGoalmaster_d1_Form(forms.ModelForm):
    class Meta:
        model = models.VGoalmaster
        fields = ['period', 'contact', 'recordid','objective','bdate','edate','pschedule','aschedule']
        labels = {
            'period':'季度', 
            'contact':'聯繫人',
            'recordid':'子工程編號', 
            'objective':'季度工程',
            'bdate':'開始時間',
            'edate':'結束時間',
            'pschedule':'計畫進度',
            'aschedule':"實際進度"
        }
class TaskR_S_Form(fb.Task_Form):
    class Meta(fb.Task_Form.Meta):
        fields = ['pid','tid','taskid','task','contact','progress']
        labels = utils.subDict(fb.Task_Form.Meta.labels, ['pid','tid','taskid','task','contact','progress'])


class TaskR_D_Form(fb.Task_Form):
    class Meta(fb.Task_Form.Meta):
        fields = ['pid','tid','taskid','task','contact','progress','planbdate','planedate']
        labels = utils.subDict(fb.Task_Form.Meta.labels, ['pid','tid','taskid','task','contact','progress','planbdate','planedate'])
        
class TaskR_Simple_Form(fb.Task_Form):
    class Meta(fb.Task_Form.Meta):
        fields = ['pid','tid','taskid','task','contact','progress','relationgoalid','tasktype','class_field','planbdate','planedate']
        labels = utils.subDict(fb.Task_Form.Meta.labels, ['pid','tid','taskid','task','contact','progress','relationgoalid','tasktype','class_field','planbdate','planedate'])

class VGoalmaster_main_form(fb.VGoalMaster_Form):
    class Meta(fb.VGoalMaster_Form.Meta):
        fields = ['recordid','period', 'contact','objective','bdate','edate','pschedule','aschedule','score', 'gtype','itemno','inc_id']
        labels = utils.subDict(fb.VGoalMaster_Form.Meta.labels, ['recordid','period', 'contact','objective','bdate','edate','pschedule','aschedule','score','gtype','itemno','inc_id'])
class SchPeriod_main_form(fb.Schperiod_Form):
    class Meta(fb.Schperiod_Form.Meta):
        fields = ['period','from_field','to','hour','logic','prefix','completion']
        labels = utils.subDict(fb.Schperiod_Form.Meta.labels, ['period','from_field','to','hour','logic','prefix','completion'])
class SchType_main_form(fb.SchType_Form):
    class Meta(fb.SchType_Form.Meta):
        fields = ['typeno','typename','logic','formula','udf02','remark']
        labels = utils.subDict(fb.SchType_Form.Meta.labels, ['typeno','typename','logic','formula','udf02','remark'])
class Opportunity_main_from(fb.Opportunity_Form):
    class Meta(fb.Opportunity_Form.Meta):
        fields = ['mb023', 'mb004','mb003', 'mb001',  'mb005',
                  'mb006', 'mb008']
        labels = utils.subDict(fb.Opportunity_Form.Meta.labels, ['mb023', 'tid', 'pid', 'mb001', 'mb002', 'mb003',
                                                                 'mb004', 'mb005', 'mb006', 'mb008'])