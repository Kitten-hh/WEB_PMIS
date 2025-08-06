from django.db import models
from BaseProject.CustomBaseObject.base_models.MultipleKeyBaseModel import MultipleKeyBaseModel
from Authorization_app.models import Roles,AbstractUser
# Create your models here.
models.options.DEFAULT_NAMES += ('target_model',)

class ADMRP(models.Model):
    RP001 = models.CharField(max_length=50,null=True,blank=True)
    RP002 = models.DateTimeField(null=True,blank=True)
    RP003 = models.CharField(max_length=50,null=True,blank=True)
    RP004 = models.CharField(max_length=20,null=True,blank=True)
    RP005 = models.TextField(null=True,blank=True)
    RP006 = models.CharField(max_length=50,null=True,blank=True)
    RP007 = models.CharField(max_length=255,null=True,blank=True)
    RP008 = models.CharField(max_length=255,null=True,blank=True)
    RP009 = models.CharField(max_length=50,null=True,blank=True)
    RP010 = models.CharField(max_length=20,null=True,blank=True)
    RP011 = models.CharField(max_length=2,null=True,blank=True)
    RP012 = models.DateTimeField(null=True,blank=True)
    RP013 = models.DateTimeField(null=True,blank=True)
    RP014 = models.TextField(null=True,blank=True)
    RP015 = models.CharField(max_length=1,null=True,blank=True)
    RP016 = models.CharField(max_length=10,null=False,blank=False)
    RP017 = models.CharField(max_length=11,null=False,blank=False)
    RP018 = models.FloatField(null=True,blank=True)
    RP019 = models.FloatField(null=True,blank=True)
    RP020 = models.CharField(max_length=30,null=True,blank=True)
    RP021 = models.CharField(max_length=30,null=True,blank=True)
    RP022 = models.CharField(max_length=50,null=True,blank=True)
    RP023 = models.CharField(max_length=50,null=True,blank=True)
    RP024 = models.CharField(max_length=100,null=True,blank=True)
    RP025 = models.CharField(max_length=1,null=True,blank=True)
    RP026 = models.CharField(max_length=1,null=True,blank=True)
    RP027 = models.CharField(max_length=30,null=True,blank=True)
    RP028 = models.CharField(max_length=30,null=True,blank=True)
    RP029 = models.CharField(max_length=1,null=True,blank=True)
    RP030 = models.CharField(max_length=1,null=True,blank=True)
    RP031 = models.DateTimeField(null=True,blank=True)
    RP032 = models.DateTimeField(null=True,blank=True)
    RP033 = models.IntegerField(null=True,blank=True)
    RP034 = models.IntegerField(null=True,blank=True)
    RP035 = models.CharField(max_length=30,null=True,blank=True)
    RP036 = models.CharField(max_length=30,null=True,blank=True)
    RP037 = models.CharField(max_length=60,null=True,blank=True)
    RP038 = models.CharField(max_length=60,null=True,blank=True)
    RP039 = models.DateTimeField(null=True,blank=True)
    RP040 = models.CharField(max_length=20,null=True,blank=True)
    RP041 = models.CharField(max_length=20,null=True,blank=True)    
    def __str__(self):
        return self.RP016 + '-' + self.RP017

class Goalmaster(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    period = models.CharField(db_column='Period', max_length=10)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=15)  # Field name made lowercase.
    recordid = models.CharField(db_column='RecordID', max_length=6)  # Field name made lowercase.
    gtype = models.CharField(db_column='GType', max_length=1)  # Field name made lowercase.
    itemno = models.CharField(db_column='ItemNo', max_length=6)  # Field name made lowercase.
    objective = models.TextField(db_column='Objective', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    bdate = models.DateTimeField(db_column='BDate', blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='EDate', blank=True, null=True)  # Field name made lowercase.
    project = models.CharField(db_column='Project', max_length=500, blank=True, null=True)  # Field name made lowercase.
    desp = models.CharField(db_column='Desp', max_length=500, blank=True, null=True)  # Field name made lowercase.
    escore = models.FloatField(db_column='EScore', blank=True, null=True)  # Field name made lowercase.
    ascore = models.FloatField(db_column='AScore', blank=True, null=True)  # Field name made lowercase.
    management = models.FloatField(db_column='Management', blank=True, null=True)  # Field name made lowercase.
    performance = models.FloatField(db_column='Performance', blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=500, blank=True, null=True)  # Field name made lowercase.
    manday = models.IntegerField(db_column='ManDay', blank=True, null=True)  # Field name made lowercase.
    difficulty = models.CharField(db_column='Difficulty', max_length=1, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID',  primary_key=True)  # Field name made lowercase.    

    class Meta:
        managed = False
        db_table = 'GoalMaster'
        app_label = 'DataBase_MPMS'
        unique_together = (('period', 'contact', 'recordid', 'gtype', 'itemno'),)

class VGoalmaster(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    period = models.CharField(db_column='Period', max_length=10)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=15)  # Field name made lowercase.
    recordid = models.CharField(db_column='RecordID', max_length=6)  # Field name made lowercase.
    gtype = models.CharField(db_column='GType', max_length=1)  # Field name made lowercase.
    itemno = models.CharField(db_column='ItemNo', max_length=6)  # Field name made lowercase.
    objective = models.TextField(db_column='Objective', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    bdate = models.DateTimeField(db_column='BDate', blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='EDate', blank=True, null=True)  # Field name made lowercase.
    project = models.CharField(db_column='Project', max_length=500, blank=True, null=True)  # Field name made lowercase.
    desp = models.CharField(db_column='Desp', max_length=500, blank=True, null=True)  # Field name made lowercase.
    escore = models.FloatField(db_column='EScore', blank=True, null=True)  # Field name made lowercase.
    ascore = models.FloatField(db_column='AScore', blank=True, null=True)  # Field name made lowercase.
    management = models.FloatField(db_column='Management', blank=True, null=True)  # Field name made lowercase.
    performance = models.FloatField(db_column='Performance', blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=500, blank=True, null=True)  # Field name made lowercase.
    manday = models.IntegerField(db_column='ManDay', blank=True, null=True)  # Field name made lowercase.
    difficulty = models.CharField(db_column='Difficulty', max_length=1, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.IntegerField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    pschedule = models.FloatField(db_column='PSchedule', blank=True, null=True)  # Field name made lowercase.
    aschedule = models.FloatField(db_column='ASchedule', blank=True, null=True)  # Field name made lowercase.
    totalscore = models.DecimalField(db_column='TotalScore', max_digits=38, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    weeklyescore = models.DecimalField(db_column='WeeklyEScore', max_digits=22, decimal_places=6)  # Field name made lowercase.
    prescore = models.DecimalField(db_column='PreScore', max_digits=18, decimal_places=2)  # Field name made lowercase.
    weeklyascore = models.DecimalField(db_column='WeeklyAScore', max_digits=38, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    framecount = models.IntegerField(db_column='FrameCount', blank=True, null=True)  # Field name made lowercase.
    funccount = models.IntegerField(db_column='FuncCount', blank=True, null=True)  # Field name made lowercase.
    score = models.IntegerField(db_column='Score')  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_GoalMaster'

class Goaldetail(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    period = models.CharField(db_column='Period', max_length=10)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=15)  # Field name made lowercase.
    recordid = models.CharField(db_column='RecordID', max_length=6)  # Field name made lowercase.
    gtype = models.CharField(db_column='GType', max_length=1)  # Field name made lowercase.
    itemno = models.CharField(db_column='ItemNo', max_length=10)  # Field name made lowercase.
    subitemno = models.CharField(db_column='SubItemNo', max_length=6)  # Field name made lowercase.
    pid = models.CharField(db_column='PID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    tid = models.FloatField(db_column='TID', blank=True, null=True)  # Field name made lowercase.
    taskid = models.FloatField(db_column='TaskId', blank=True, null=True)  # Field name made lowercase.
    desp = models.CharField(db_column='Desp', max_length=500, blank=True, null=True)  # Field name made lowercase.
    bdate = models.DateTimeField(db_column='BDate', blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='EDate', blank=True, null=True)  # Field name made lowercase.
    escore = models.FloatField(db_column='EScore', blank=True, null=True)  # Field name made lowercase.
    ascore = models.FloatField(db_column='AScore', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=1, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=500, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GoalDetail'
        app_label = 'DataBase_MPMS'
        unique_together = (('period', 'contact', 'recordid', 'gtype', 'itemno', 'subitemno'),)

class VGoaldetail(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    period = models.CharField(db_column='Period', max_length=10)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=15)  # Field name made lowercase.
    recordid = models.CharField(db_column='RecordID', max_length=6)  # Field name made lowercase.
    gtype = models.CharField(db_column='GType', max_length=1)  # Field name made lowercase.
    itemno = models.CharField(db_column='ItemNo', max_length=10)  # Field name made lowercase.
    subitemno = models.CharField(db_column='SubItemNo', max_length=6)  # Field name made lowercase.
    pid = models.CharField(db_column='PID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    tid = models.FloatField(db_column='TID', blank=True, null=True)  # Field name made lowercase.
    taskid = models.FloatField(db_column='TaskId', blank=True, null=True)  # Field name made lowercase.
    desp = models.CharField(db_column='Desp', max_length=500, blank=True, null=True)  # Field name made lowercase.
    bdate = models.DateTimeField(db_column='BDate', blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='EDate', blank=True, null=True)  # Field name made lowercase.
    escore = models.FloatField(db_column='EScore', blank=True, null=True)  # Field name made lowercase.
    ascore = models.FloatField(db_column='AScore', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=1, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=500, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.IntegerField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    taskno = models.CharField(db_column='TaskNo', max_length=38, blank=True, null=True)  # Field name made lowercase.
    task = models.CharField(db_column='Task', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    planbdate = models.DateTimeField(db_column='PlanBDate', blank=True, null=True)  # Field name made lowercase.
    planedate = models.DateTimeField(db_column='PlanEDate', blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    progressprocent = models.IntegerField(db_column='ProgressProcent', blank=True, null=True)  # Field name made lowercase.
    relcontact = models.CharField(db_column='RelContact', max_length=25, blank=True, null=True)  # Field name made lowercase.
    relremark = models.CharField(db_column='RelRemark', max_length=255, blank=True, null=True)  # Field name made lowercase.
    spaday = models.FloatField(db_column='SPADay', blank=True, null=True)  # Field name made lowercase.
    spday = models.FloatField(db_column='SPDay', blank=True, null=True)  # Field name made lowercase.
    saday = models.FloatField(db_column='SADay', blank=True, null=True)  # Field name made lowercase.
    pschedule = models.FloatField(db_column='PSchedule', blank=True, null=True)  # Field name made lowercase.
    aschedule = models.FloatField(db_column='ASchedule', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_GoalDetail'

class Task(models.Model):
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pid = models.CharField(db_column='Pid', max_length=16)  # Field name made lowercase.
    tid = models.FloatField(db_column='Tid')  # Field name made lowercase.
    taskid = models.FloatField(db_column='TaskID')  # Field name made lowercase.
    task = models.CharField(db_column='Task', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=25, blank=True, null=True)  # Field name made lowercase.
    planbdate = models.DateTimeField(db_column='PlanBDate', blank=True, null=True)  # Field name made lowercase.
    etime = models.FloatField(db_column='Etime', blank=True, null=True)  # Field name made lowercase.
    planedate = models.DateTimeField(db_column='PlanEDate', blank=True, null=True)  # Field name made lowercase.
    atime = models.FloatField(blank=True, null=True)
    bdate = models.DateTimeField(db_column='BDate', blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='EDate', blank=True, null=True)  # Field name made lowercase.
    priority = models.IntegerField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=255, blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    revisedby = models.CharField(db_column='RevisedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    tasktype = models.IntegerField(db_column='TaskType', blank=True, null=True)  # Field name made lowercase.
    subtasktype = models.IntegerField(db_column='SubTaskType', blank=True, null=True)  # Field name made lowercase.
    diff = models.IntegerField(db_column='Diff', blank=True, null=True)  # Field name made lowercase.
    taskoption = models.IntegerField(db_column='Taskoption', blank=True, null=True)  # Field name made lowercase.
    relationid = models.CharField(db_column='relationID', max_length=200, blank=True, null=True)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
    docpath = models.CharField(db_column='DocPath', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emaildesp = models.TextField(db_column='EmailDesp', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf51 = models.CharField(db_column='UDF51', max_length=10, blank=True, null=True)  # Field name made lowercase.
    udf52 = models.DecimalField(db_column='UDF52', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    smsreceiver = models.CharField(db_column='SMSReceiver', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dispose = models.CharField(db_column='Dispose', max_length=2, blank=True, null=True)  # Field name made lowercase.
    editionid = models.CharField(db_column='EditionID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    oldprogress = models.CharField(db_column='OldProgress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    delayday = models.IntegerField(db_column='DelayDay', blank=True, null=True)  # Field name made lowercase.
    companyid = models.CharField(db_column='CompanyID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    subprojectid = models.CharField(db_column='SubProjectID', max_length=6, blank=True, null=True)  # Field name made lowercase.
    class_field = models.IntegerField(db_column='Class', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    sendctlemail = models.IntegerField(db_column='SendCTLEmail', blank=True, null=True)  # Field name made lowercase.
    generateddoc = models.CharField(db_column='GeneratedDoc', max_length=300, blank=True, null=True)  # Field name made lowercase.
    relationgoalid = models.CharField(db_column='RelationGoalId', max_length=200, blank=True, null=True)  # Field name made lowercase.
    escore = models.FloatField(db_column='EScore', blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    totalscore = models.FloatField(db_column='TotalScore', blank=True, null=True)  # Field name made lowercase.
    setting = models.CharField(db_column='Setting', max_length=1, blank=True, null=True)  # Field name made lowercase.
    questionno = models.CharField(db_column='QuestionNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    req_date = models.DateTimeField(db_column='Req_Date', blank=True, null=True)  # Field name made lowercase.
    reply_taskno = models.CharField(db_column='Reply_TaskNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    isschedule = models.CharField(db_column='IsSchedule', max_length=1, blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=500, blank=True, null=True)  # Field name made lowercase.
    environmentid = models.CharField(db_column='EnvironmentID', max_length=6, blank=True, null=True)  # Field name made lowercase.
    categoryid = models.FloatField(db_column='CategoryID', blank=True, null=True)  # Field name made lowercase.
    rank = models.IntegerField(db_column='Rank', blank=True, null=True)  # Field name made lowercase.
    correctness = models.CharField(db_column='Correctness', max_length=1, blank=True, null=True)  # Field name made lowercase.
    appraisalid = models.CharField(db_column='AppraisalId', max_length=20, blank=True, null=True)  # Field name made lowercase.
    progressprocent = models.IntegerField(db_column='ProgressProcent', blank=True, null=True)  # Field name made lowercase.
    classify = models.CharField(db_column='Classify', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flowchartno = models.CharField(db_column='FlowChartNo', max_length=200, blank=True, null=True)  # Field name made lowercase.
    spday = models.FloatField(db_column='SPDay', blank=True, null=True)  # Field name made lowercase.
    spaday = models.FloatField(db_column='SPADay', blank=True, null=True)  # Field name made lowercase.
    saday = models.FloatField(db_column='SADay', blank=True, null=True)  # Field name made lowercase.
    manday = models.IntegerField(db_column='ManDay', blank=True, null=True)  # Field name made lowercase.
    difficulty = models.CharField(db_column='Difficulty', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf06 = models.CharField(db_column='UDF06', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf07 = models.DateTimeField(db_column='UDF07', blank=True, null=True)  # Field name made lowercase.
    udf08 = models.CharField(db_column='UDF08', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf09 = models.CharField(db_column='UDF09', max_length=20, blank=True, null=True)  # Field name made lowercase.
    udf10 = models.CharField(db_column='UDF10', max_length=20, blank=True, null=True)  # Field name made lowercase.
    calpriority = models.IntegerField(db_column='CalPriority', blank=True, null=True)  # Field name made lowercase.
    schpriority = models.FloatField(db_column='SchPriority', blank=True, null=True)  # Field name made lowercase.
    schedulestate = models.CharField(db_column='ScheduleState', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dayjob = models.CharField(db_column='DayJob', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mastno = models.CharField(db_column='MastNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cycletask = models.CharField(db_column='CycleTask', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf11 = models.CharField(db_column='UDF11', max_length=20, blank=True, null=True)  # Field name made lowercase.
    reference = models.CharField(db_column='Reference', max_length=30, blank=True, null=True)  # Field name made lowercase.
    hoperation = models.CharField(db_column='HOperation', max_length=1, blank=True, null=True)  # Field name made lowercase.
    charge = models.CharField(db_column='Charge', max_length=1, blank=True, null=True)  # Field name made lowercase.
    special = models.CharField(db_column='Special', max_length=1, blank=True, null=True)  # Field name made lowercase.
    process = models.CharField(db_column='Process', max_length=1, blank=True, null=True)  # Field name made lowercase.
    requestdate = models.DateTimeField(db_column='RequestDate', blank=True, null=True)  # Field name made lowercase.
    schprioritysp = models.FloatField(db_column='SchPrioritySP', blank=True, null=True)  # Field name made lowercase.
    r_flag = models.NullBooleanField(db_column='R_Flag', blank=True, null=True)  # Field name made lowercase.
    taskcategory = models.CharField(db_column='TaskCategory', max_length=5, blank=True, null=True)  # Field name made lowercase.
    sessionpriority = models.DecimalField(db_column='SessionPriority', max_digits=11, decimal_places=2, blank=True, null=True)  # Field name made lowercase.        
    inc_id = models.AutoField(db_column='INC_ID',  primary_key=True)  # Field name made lowercase.    

    class Meta:
        managed = False
        db_table = 'Task'
        app_label = 'DataBase_MPMS'        
        unique_together = (('pid', 'tid', 'taskid'),)


class Tasklist(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pid = models.CharField(db_column='Pid', max_length=16)  # Field name made lowercase.
    tid = models.FloatField(db_column='Tid')  # Field name made lowercase.
    desp = models.BinaryField(db_column='Desp', blank=True, null=True)  # Field name made lowercase.
    priority = models.FloatField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    planbdate = models.DateTimeField(db_column='PlanBDate', blank=True, null=True)  # Field name made lowercase.
    etime = models.FloatField(db_column='Etime', blank=True, null=True)  # Field name made lowercase.
    planedate = models.DateTimeField(db_column='PlanEDate', blank=True, null=True)  # Field name made lowercase.
    bdate = models.DateTimeField(db_column='Bdate', blank=True, null=True)  # Field name made lowercase.
    atime = models.FloatField(db_column='Atime', blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='Edate', blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    sdesp = models.CharField(db_column='SDesp', max_length=3000, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=20, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=256, blank=True, null=True)  # Field name made lowercase.
    revisedby = models.CharField(db_column='RevisedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    msgflag = models.CharField(db_column='MsgFlag', max_length=1, blank=True, null=True)  # Field name made lowercase.
    recerver = models.CharField(db_column='Recerver', max_length=50, blank=True, null=True)  # Field name made lowercase.
    flowchartno = models.CharField(db_column='FlowChartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    parent = models.CharField(db_column='Parent', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=50, blank=True, null=True)  # Field name made lowercase.
    class_field = models.IntegerField(db_column='Class', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    weight = models.FloatField(db_column='Weight', blank=True, null=True)  # Field name made lowercase.
    goaltype = models.CharField(db_column='GoalType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    capacity = models.IntegerField(db_column='Capacity', blank=True, null=True)  # Field name made lowercase.
    djcapacity = models.IntegerField(db_column='DJCapacity', blank=True, null=True)  # Field name made lowercase.
    cycleno = models.CharField(db_column='CycleNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    schrate = models.IntegerField(db_column='SchRate', blank=True, null=True)  # Field name made lowercase.
    estimate = models.IntegerField(db_column='Estimate', blank=True, null=True)  # Field name made lowercase.
    handletype = models.CharField(db_column='HandleType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tasklist'
        unique_together = (('pid', 'tid'),)

class Users(AbstractUser):
    username = models.CharField(db_column='UserName', max_length=15)  # Field name made lowercase.
    workno = models.CharField(db_column='Workno', max_length=10, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='PassWord', max_length=20, blank=True, null=True)  # Field name made lowercase.
    level = models.IntegerField(db_column='Level', blank=True, null=True)  # Field name made lowercase.
    groupname = models.CharField(db_column='GroupName', max_length=20, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=100, blank=True, null=True)  # Field name made lowercase.
    telno = models.CharField(db_column='telNo', max_length=15, blank=True, null=True)  # Field name made lowercase.
    lanflag = models.CharField(db_column='lanFlag', max_length=10, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(blank=True, null=True)
    shorttelno = models.CharField(db_column='shortTelNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    receiveflag = models.CharField(db_column='receiveFlag', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dept = models.CharField(db_column='Dept', max_length=30, blank=True, null=True)  # Field name made lowercase.
    companyid = models.CharField(db_column='CompanyID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    goalflag = models.CharField(db_column='GoalFlag', max_length=1, blank=True, null=True)  # Field name made lowercase.
    issuper = models.NullBooleanField(db_column='IsSuper', blank=True, null=True)  # Field name made lowercase.
    isremind = models.NullBooleanField(db_column='IsRemind', blank=True, null=True)  # Field name made lowercase.
    salesremind = models.NullBooleanField(db_column='SalesRemind', blank=True, null=True)  # Field name made lowercase.
    isautologin = models.NullBooleanField(db_column='IsAutoLogin', blank=True, null=True)  # Field name made lowercase.
    roleid = models.ForeignKey(Roles, models.CASCADE, db_column='RoleId', null=True, blank=True)  # 权限的外键    
    inc_id = models.AutoField(db_column='INC_ID',  primary_key=True)  # Field name made lowercase

    class Meta:
        managed = False
        db_table = 'Users'
        app_label = 'DataBase_MPMS'

class Subproject(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    recordid = models.CharField(db_column='RecordID', max_length=6)  # Field name made lowercase.
    projectid = models.CharField(db_column='ProjectID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    projectname = models.CharField(db_column='ProjectName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    filter = models.TextField(db_column='Filter', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    contact = models.CharField(db_column='Contact', max_length=12, blank=True, null=True)  # Field name made lowercase.
    planbdate = models.DateTimeField(db_column='PlanBDate', blank=True, null=True)  # Field name made lowercase.
    planedate = models.DateTimeField(db_column='PlanEDate', blank=True, null=True)  # Field name made lowercase.
    etime = models.FloatField(db_column='Etime', blank=True, null=True)  # Field name made lowercase.
    bdate = models.DateTimeField(db_column='BDate', blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='EDate', blank=True, null=True)  # Field name made lowercase.
    atime = models.FloatField(db_column='ATime', blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=255, blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    score = models.IntegerField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    resource = models.CharField(db_column='Resource', max_length=200, blank=True, null=True)  # Field name made lowercase.
    revisedby = models.CharField(db_column='RevisedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    searchtypeid = models.IntegerField(db_column='SearchTypeID', blank=True, null=True)  # Field name made lowercase.
    searchid = models.IntegerField(db_column='SearchID', blank=True, null=True)  # Field name made lowercase.
    method = models.CharField(db_column='Method', max_length=1, blank=True, null=True)  # Field name made lowercase.
    priority = models.FloatField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    udf03 = models.FloatField(db_column='UDF03', blank=True, null=True)  # Field name made lowercase.
    searchcreator = models.CharField(db_column='SearchCreator', max_length=30, blank=True, null=True)  # Field name made lowercase.
    relationdoc = models.CharField(db_column='RelationDoc', max_length=30, blank=True, null=True)  # Field name made lowercase.
    complete = models.CharField(db_column='Complete', max_length=8, blank=True, null=True)  # Field name made lowercase.
    fullcomplete = models.CharField(db_column='FullComplete', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mainflowchar = models.CharField(db_column='MainFlowChar', max_length=100, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SubProject'

class Queryfilter(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    qf001 = models.IntegerField(db_column='QF001')  # Field name made lowercase.
    qf002 = models.IntegerField(db_column='QF002')  # Field name made lowercase.
    qf003 = models.CharField(db_column='QF003', max_length=60, blank=True, null=True)  # Field name made lowercase.
    qf004 = models.BinaryField(db_column='QF004', blank=True, null=True)  # Field name made lowercase.
    qf005 = models.BinaryField(db_column='QF005', blank=True, null=True)  # Field name made lowercase.
    qf006 = models.CharField(db_column='QF006', max_length=10)  # Field name made lowercase.
    qf007 = models.CharField(db_column='QF007', max_length=10, blank=True, null=True)  # Field name made lowercase.
    qf008 = models.CharField(db_column='QF008', max_length=30, blank=True, null=True)  # Field name made lowercase.
    qf009 = models.CharField(db_column='QF009', max_length=30)  # Field name made lowercase.
    qf010 = models.CharField(db_column='QF010', max_length=60)  # Field name made lowercase.
    qf011 = models.CharField(db_column='QF011', max_length=60, blank=True, null=True)  # Field name made lowercase.
    qf012 = models.DecimalField(db_column='QF012', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    qf013 = models.TextField(db_column='QF013', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    qf014 = models.TextField(db_column='QF014', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    qf015 = models.CharField(db_column='QF015', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qf016 = models.IntegerField(db_column='QF016', blank=True, null=True)  # Field name made lowercase.
    qf017 = models.DateTimeField(db_column='QF017', blank=True, null=True)  # Field name made lowercase.
    qf018 = models.DateTimeField(db_column='QF018', blank=True, null=True)  # Field name made lowercase.
    qf019 = models.CharField(db_column='QF019', max_length=50, blank=True, null=True)  # Field name made lowercase.
    qf020 = models.CharField(db_column='QF020', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qf021 = models.CharField(db_column='QF021', max_length=200, blank=True, null=True)  # Field name made lowercase.
    qf022 = models.CharField(db_column='QF022', max_length=200, blank=True, null=True)  # Field name made lowercase.
    qf023 = models.CharField(db_column='QF023', max_length=20, blank=True, null=True)  # Field name made lowercase.
    qf024 = models.IntegerField(db_column='QF024', blank=True, null=True)  # Field name made lowercase.
    qf025 = models.AutoField(db_column='QF025',  primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QueryFilter'
        unique_together = (('qf001', 'qf002', 'qf006', 'qf009', 'qf010'),)
        app_label = 'DataBase_MPMS'


class VQueryfilter(models.Model):
    selectflag = models.CharField(db_column='SelectFlag', max_length=1)  # Field name made lowercase.
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    qf001 = models.IntegerField(db_column='QF001')  # Field name made lowercase.
    qf002 = models.IntegerField(db_column='QF002')  # Field name made lowercase.
    qf003 = models.CharField(db_column='QF003', max_length=60, blank=True, null=True)  # Field name made lowercase.
    qf004 = models.BinaryField(db_column='QF004', blank=True, null=True)  # Field name made lowercase.
    qf005 = models.BinaryField(db_column='QF005', blank=True, null=True)  # Field name made lowercase.
    qf006 = models.CharField(db_column='QF006', max_length=10)  # Field name made lowercase.
    qf007 = models.CharField(db_column='QF007', max_length=10, blank=True, null=True)  # Field name made lowercase.
    qf008 = models.CharField(db_column='QF008', max_length=30, blank=True, null=True)  # Field name made lowercase.
    qf009 = models.CharField(db_column='QF009', max_length=30)  # Field name made lowercase.
    qf010 = models.CharField(db_column='QF010', max_length=60)  # Field name made lowercase.
    qf011 = models.CharField(db_column='QF011', max_length=60, blank=True, null=True)  # Field name made lowercase.
    qf012 = models.DecimalField(db_column='QF012', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    qf013 = models.TextField(db_column='QF013', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    qf014 = models.TextField(db_column='QF014', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    qf015 = models.CharField(db_column='QF015', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qf016 = models.IntegerField(db_column='QF016', blank=True, null=True)  # Field name made lowercase.
    qf017 = models.DateTimeField(db_column='QF017', blank=True, null=True)  # Field name made lowercase.
    qf018 = models.DateTimeField(db_column='QF018', blank=True, null=True)  # Field name made lowercase.
    qf019 = models.CharField(db_column='QF019', max_length=50, blank=True, null=True)  # Field name made lowercase.
    qf020 = models.CharField(db_column='QF020', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qf021 = models.CharField(db_column='QF021', max_length=200, blank=True, null=True)  # Field name made lowercase.
    qf022 = models.CharField(db_column='QF022', max_length=200, blank=True, null=True)  # Field name made lowercase.
    qf023 = models.CharField(db_column='QF023', max_length=20, blank=True, null=True)  # Field name made lowercase.
    qf024 = models.IntegerField(db_column='QF024', blank=True, null=True)  # Field name made lowercase.
    qf025 = models.IntegerField(db_column='QF025',  primary_key=True)  # Field name made lowercase.
    qt002 = models.CharField(db_column='QT002', max_length=30)  # Field name made lowercase.
    searchid = models.CharField(db_column='SearchID', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_QueryFilter'        
        app_label = 'DataBase_MPMS'

class VTask(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    selectflag = models.CharField(db_column='SelectFlag', max_length=1)  # Field name made lowercase.
    levelnum_1 = models.IntegerField(db_column='LevelNum_1', blank=True, null=True)  # Field name made lowercase.
    docflag = models.CharField(db_column='DocFlag', max_length=1)  # Field name made lowercase.
    tcontact = models.CharField(db_column='TContact', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tplanedate = models.DateTimeField(db_column='TPlanEDate', blank=True, null=True)  # Field name made lowercase.
    taskno = models.CharField(db_column='TaskNo',  max_length=42, blank=True, null=True)  # Field name made lowercase.
    tasklistno = models.CharField(db_column='TaskListNo', max_length=31, blank=True, null=True)  # Field name made lowercase.
    pschedule = models.FloatField(db_column='PSchedule', blank=True, null=True)  # Field name made lowercase.
    aschedule = models.FloatField(db_column='ASchedule', blank=True, null=True)  # Field name made lowercase.
    tasktypecaption = models.IntegerField(db_column='TaskTypeCaption')  # Field name made lowercase.
    tidstr = models.CharField(db_column='TidStr', max_length=20, blank=True, null=True)  # Field name made lowercase.
    taskidstr = models.CharField(db_column='TaskIDStr', max_length=10, blank=True, null=True)  # Field name made lowercase.
    taskcaption = models.CharField(db_column='TaskCaption', max_length=546, blank=True, null=True)  # Field name made lowercase.
    taskcaption2 = models.CharField(db_column='TaskCaption2', max_length=599, blank=True, null=True)  # Field name made lowercase.
    docid = models.CharField(db_column='DocId', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pid = models.CharField(db_column='Pid', max_length=16)  # Field name made lowercase.
    tid = models.FloatField(db_column='Tid')  # Field name made lowercase.
    taskid = models.FloatField(db_column='TaskID')  # Field name made lowercase.
    task = models.CharField(db_column='Task', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=25, blank=True, null=True)  # Field name made lowercase.
    planbdate = models.DateTimeField(db_column='PlanBDate', blank=True, null=True)  # Field name made lowercase.
    etime = models.FloatField(db_column='Etime', blank=True, null=True)  # Field name made lowercase.
    planedate = models.DateTimeField(db_column='PlanEDate', blank=True, null=True)  # Field name made lowercase.
    atime = models.FloatField(blank=True, null=True)
    bdate = models.DateTimeField(db_column='BDate', blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='EDate', blank=True, null=True)  # Field name made lowercase.
    priority = models.IntegerField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=255, blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    revisedby = models.CharField(db_column='RevisedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    tasktype = models.IntegerField(db_column='TaskType', blank=True, null=True)  # Field name made lowercase.
    taskoption = models.IntegerField(db_column='Taskoption', blank=True, null=True)  # Field name made lowercase.
    relationid = models.CharField(db_column='relationID', max_length=200, blank=True, null=True)  # Field name made lowercase.
    relationprogress = models.CharField(db_column='relationProgress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
    docpath = models.CharField(db_column='DocPath', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emaildesp = models.TextField(db_column='EmailDesp', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf51 = models.CharField(db_column='UDF51', max_length=10, blank=True, null=True)  # Field name made lowercase.
    udf52 = models.DecimalField(db_column='UDF52', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    udf09 = models.CharField(db_column='UDF09', max_length=20, blank=True, null=True)  # Field name made lowercase.
    udf10 = models.CharField(db_column='UDF10', max_length=20, blank=True, null=True)  # Field name made lowercase.
    smsreceiver = models.CharField(db_column='SMSReceiver', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dispose = models.CharField(db_column='Dispose', max_length=2, blank=True, null=True)  # Field name made lowercase.
    editionid = models.CharField(db_column='EditionID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    oldprogress = models.CharField(db_column='OldProgress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    delayday = models.IntegerField(db_column='DelayDay', blank=True, null=True)  # Field name made lowercase.
    companyid = models.CharField(db_column='CompanyID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    subprojectid = models.CharField(db_column='SubProjectID', max_length=6, blank=True, null=True)  # Field name made lowercase.
    class_field = models.IntegerField(db_column='Class', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    sendctlemail = models.IntegerField(db_column='SendCTLEmail', blank=True, null=True)  # Field name made lowercase.
    generateddoc = models.CharField(db_column='GeneratedDoc', max_length=300, blank=True, null=True)  # Field name made lowercase.
    relationgoalid = models.CharField(db_column='RelationGoalId', max_length=200, blank=True, null=True)  # Field name made lowercase.
    escore = models.FloatField(db_column='EScore', blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    totalscore = models.FloatField(db_column='TotalScore', blank=True, null=True)  # Field name made lowercase.
    setting = models.CharField(db_column='Setting', max_length=1, blank=True, null=True)  # Field name made lowercase.
    questionno = models.CharField(db_column='QuestionNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    req_date = models.DateTimeField(db_column='Req_Date', blank=True, null=True)  # Field name made lowercase.
    reply_taskno = models.CharField(db_column='Reply_TaskNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    isschedule = models.CharField(db_column='IsSchedule', max_length=1, blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=500, blank=True, null=True)  # Field name made lowercase.
    environmentid = models.CharField(db_column='EnvironmentID', max_length=6, blank=True, null=True)  # Field name made lowercase.
    categoryid = models.FloatField(db_column='CategoryID', blank=True, null=True)  # Field name made lowercase.
    rank = models.IntegerField(db_column='Rank', blank=True, null=True)  # Field name made lowercase.
    correctness = models.CharField(db_column='Correctness', max_length=1, blank=True, null=True)  # Field name made lowercase.
    appraisalid = models.CharField(db_column='AppraisalId', max_length=20, blank=True, null=True)  # Field name made lowercase.
    progressprocent = models.IntegerField(db_column='ProgressProcent', blank=True, null=True)  # Field name made lowercase.
    classify = models.CharField(db_column='Classify', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flowchartno = models.CharField(db_column='FlowChartNo', max_length=200, blank=True, null=True)  # Field name made lowercase.
    spday = models.FloatField(db_column='SPDay', blank=True, null=True)  # Field name made lowercase.
    spaday = models.FloatField(db_column='SPADay', blank=True, null=True)  # Field name made lowercase.
    saday = models.FloatField(db_column='SADay', blank=True, null=True)  # Field name made lowercase.
    manday = models.IntegerField(db_column='ManDay', blank=True, null=True)  # Field name made lowercase.
    subtasktype = models.IntegerField(db_column='SubTaskType', blank=True, null=True)  # Field name made lowercase.
    diff = models.IntegerField(db_column='Diff', blank=True, null=True)  # Field name made lowercase.
    difficulty = models.CharField(db_column='Difficulty', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf06 = models.CharField(db_column='UDF06', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf07 = models.DateTimeField(db_column='UDF07', blank=True, null=True)  # Field name made lowercase.
    udf08 = models.CharField(db_column='UDF08', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf11 = models.CharField(db_column='UDF11', max_length=20, blank=True, null=True)  # Field name made lowercase.
    calpriority = models.IntegerField(db_column='CalPriority', blank=True, null=True)  # Field name made lowercase.
    schpriority = models.FloatField(db_column='SchPriority', blank=True, null=True)  # Field name made lowercase.
    schedulestate = models.CharField(db_column='ScheduleState', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dayjob = models.CharField(db_column='DayJob', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mastno = models.CharField(db_column='MastNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cycletask = models.CharField(db_column='CycleTask', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tiddesc = models.CharField(db_column='TidDesc', max_length=3000, blank=True, null=True)  # Field name made lowercase.
    sessionflowchartno = models.CharField(db_column='SessionFlowChartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    sprogress = models.CharField(db_column='SProgress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    scontact = models.CharField(db_column='SContact', max_length=20, blank=True, null=True)  # Field name made lowercase.
    recordid = models.CharField(db_column='RecordID', max_length=6, blank=True, null=True)  # Field name made lowercase.
    projectid = models.CharField(db_column='ProjectID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    projectname = models.CharField(db_column='ProjectName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    outday = models.IntegerField(db_column='OutDay', blank=True, null=True)  # Field name made lowercase.
    pworktimeh = models.DecimalField(db_column='PWorkTimeH', max_digits=3, decimal_places=3)  # Field name made lowercase.
    eworktimeh = models.DecimalField(db_column='EWorkTimeH', max_digits=3, decimal_places=3)  # Field name made lowercase.
    findex = models.CharField(db_column='FIndex', max_length=200, blank=True, null=True)  # Field name made lowercase.
    rptvisible = models.CharField(db_column='RptVisible', max_length=1)  # Field name made lowercase.
    tasktypedesc = models.CharField(db_column='TaskTypeDesc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    subtasktypedesc = models.CharField(db_column='SubTaskTypeDesc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    displaytype = models.IntegerField(db_column='DisplayType', blank=True, null=True)  # Field name made lowercase.
    weekly = models.IntegerField(db_column='Weekly', blank=True, null=True)  # Field name made lowercase.
    quarterly = models.IntegerField(db_column='Quarterly', blank=True, null=True)  # Field name made lowercase.
    weight = models.FloatField(db_column='Weight', blank=True, null=True)  # Field name made lowercase.
    capacity = models.IntegerField(db_column='Capacity', blank=True, null=True)  # Field name made lowercase.
    projectscore = models.IntegerField(db_column='ProjectScore', blank=True, null=True)  # Field name made lowercase.
    dayjobtaskcaption = models.CharField(db_column='DayjobTaskCaption', max_length=503, blank=True, null=True)  # Field name made lowercase.
    nofscore = models.FloatField(db_column='NoFScore', blank=True, null=True)  # Field name made lowercase.
    schcount = models.IntegerField(db_column='SchCount', blank=True, null=True)  # Field name made lowercase.
    reference = models.CharField(db_column='Reference', max_length=30, blank=True, null=True)  # Field name made lowercase.
    hoperation = models.CharField(db_column='HOperation', max_length=1, blank=True, null=True)  # Field name made lowercase.
    charge = models.CharField(db_column='Charge', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tasktypescore = models.FloatField(db_column='TaskTypeScore', blank=True, null=True)  # Field name made lowercase.
    special = models.CharField(db_column='Special', max_length=1, blank=True, null=True)  # Field name made lowercase.
    process = models.CharField(db_column='Process', max_length=1, blank=True, null=True)  # Field name made lowercase.
    requestdate = models.DateTimeField(db_column='RequestDate', blank=True, null=True)  # Field name made lowercase.
    splanbdate = models.DateTimeField(db_column='SPlanBDate', blank=True, null=True)  # Field name made lowercase.
    splanedate = models.DateTimeField(db_column='SPlanEDate', blank=True, null=True)  # Field name made lowercase.
    squarterly = models.IntegerField(db_column='SQuarterly', blank=True, null=True)  # Field name made lowercase.
    realtasktype = models.CharField(db_column='RealTaskType', max_length=62, blank=True, null=True)  # Field name made lowercase.
    schprioritysp = models.FloatField(db_column='SchPrioritySP', blank=True, null=True)  # Field name made lowercase.
    taskcategory = models.CharField(db_column='TaskCategory', max_length=5, blank=True, null=True)  # Field name made lowercase.
    r_flag = models.NullBooleanField(db_column='R_Flag', blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID',  primary_key=True)  # Field name made lowercase.  
    lookupscore = models.FloatField(db_column='LookUpScore', blank=True, null=True)  # Field name made lowercase.
    tasktypedc = models.CharField(db_column='TaskTypeDC', max_length=100, blank=True, null=True)  # Field name made lowercase. 
    planbdates = models.CharField(db_column='PlanBDateS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    planedates = models.CharField(db_column='PlanEDateS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    bdates = models.CharField(db_column='BDateS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    edates = models.CharField(db_column='EDateS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    sessionpriority = models.DecimalField(db_column='SessionPriority', max_digits=11, decimal_places=2, blank=True, null=True)  # Field name made lowercase.    

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_Task'
        app_label = 'DataBase_MPMS'

class VTaskbonussl(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    selectflag = models.CharField(db_column='SelectFlag', max_length=1)  # Field name made lowercase.
    levelnum_1 = models.IntegerField(db_column='LevelNum_1', blank=True, null=True)  # Field name made lowercase.
    docflag = models.CharField(db_column='DocFlag', max_length=1)  # Field name made lowercase.
    tcontact = models.CharField(db_column='TContact', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tplanedate = models.DateTimeField(db_column='TPlanEDate', blank=True, null=True)  # Field name made lowercase.
    taskno = models.CharField(db_column='TaskNo', max_length=42, blank=True, null=True)  # Field name made lowercase.
    tasklistno = models.CharField(db_column='TaskListNo', max_length=31, blank=True, null=True)  # Field name made lowercase.
    pschedule = models.FloatField(db_column='PSchedule', blank=True, null=True)  # Field name made lowercase.
    aschedule = models.FloatField(db_column='ASchedule', blank=True, null=True)  # Field name made lowercase.
    tasktypecaption = models.IntegerField(db_column='TaskTypeCaption')  # Field name made lowercase.
    tidstr = models.CharField(db_column='TidStr', max_length=20, blank=True, null=True)  # Field name made lowercase.
    taskidstr = models.CharField(db_column='TaskIDStr', max_length=10, blank=True, null=True)  # Field name made lowercase.
    taskcaption = models.CharField(db_column='TaskCaption', max_length=546, blank=True, null=True)  # Field name made lowercase.
    taskcaption2 = models.CharField(db_column='TaskCaption2', max_length=599, blank=True, null=True)  # Field name made lowercase.
    docid = models.CharField(db_column='DocId', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pid = models.CharField(db_column='Pid', max_length=16)  # Field name made lowercase.
    tid = models.FloatField(db_column='Tid')  # Field name made lowercase.
    taskid = models.FloatField(db_column='TaskID')  # Field name made lowercase.
    task = models.CharField(db_column='Task', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=25, blank=True, null=True)  # Field name made lowercase.
    planbdate = models.DateTimeField(db_column='PlanBDate', blank=True, null=True)  # Field name made lowercase.
    etime = models.FloatField(db_column='Etime', blank=True, null=True)  # Field name made lowercase.
    planedate = models.DateTimeField(db_column='PlanEDate', blank=True, null=True)  # Field name made lowercase.
    atime = models.FloatField(blank=True, null=True)
    bdate = models.DateTimeField(db_column='BDate', blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='EDate', blank=True, null=True)  # Field name made lowercase.
    priority = models.IntegerField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=255, blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    revisedby = models.CharField(db_column='RevisedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    tasktype = models.IntegerField(db_column='TaskType', blank=True, null=True)  # Field name made lowercase.
    taskoption = models.IntegerField(db_column='Taskoption', blank=True, null=True)  # Field name made lowercase.
    relationid = models.CharField(db_column='relationID', max_length=200, blank=True, null=True)  # Field name made lowercase.
    relationprogress = models.CharField(db_column='relationProgress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
    docpath = models.CharField(db_column='DocPath', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emaildesp = models.TextField(db_column='EmailDesp', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf51 = models.CharField(db_column='UDF51', max_length=10, blank=True, null=True)  # Field name made lowercase.
    udf52 = models.DecimalField(db_column='UDF52', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    udf09 = models.CharField(db_column='UDF09', max_length=20, blank=True, null=True)  # Field name made lowercase.
    udf10 = models.CharField(db_column='UDF10', max_length=20, blank=True, null=True)  # Field name made lowercase.
    smsreceiver = models.CharField(db_column='SMSReceiver', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dispose = models.CharField(db_column='Dispose', max_length=2, blank=True, null=True)  # Field name made lowercase.
    editionid = models.CharField(db_column='EditionID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    oldprogress = models.CharField(db_column='OldProgress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    delayday = models.IntegerField(db_column='DelayDay', blank=True, null=True)  # Field name made lowercase.
    companyid = models.CharField(db_column='CompanyID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    subprojectid = models.CharField(db_column='SubProjectID', max_length=6, blank=True, null=True)  # Field name made lowercase.
    class_field = models.IntegerField(db_column='Class', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    sendctlemail = models.IntegerField(db_column='SendCTLEmail', blank=True, null=True)  # Field name made lowercase.
    generateddoc = models.CharField(db_column='GeneratedDoc', max_length=300, blank=True, null=True)  # Field name made lowercase.
    relationgoalid = models.CharField(db_column='RelationGoalId', max_length=200, blank=True, null=True)  # Field name made lowercase.
    escore = models.FloatField(db_column='EScore', blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    totalscore = models.FloatField(db_column='TotalScore', blank=True, null=True)  # Field name made lowercase.
    setting = models.CharField(db_column='Setting', max_length=1, blank=True, null=True)  # Field name made lowercase.
    questionno = models.CharField(db_column='QuestionNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    req_date = models.DateTimeField(db_column='Req_Date', blank=True, null=True)  # Field name made lowercase.
    reply_taskno = models.CharField(db_column='Reply_TaskNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    isschedule = models.CharField(db_column='IsSchedule', max_length=1, blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=500, blank=True, null=True)  # Field name made lowercase.
    environmentid = models.CharField(db_column='EnvironmentID', max_length=6, blank=True, null=True)  # Field name made lowercase.
    categoryid = models.FloatField(db_column='CategoryID', blank=True, null=True)  # Field name made lowercase.
    rank = models.IntegerField(db_column='Rank', blank=True, null=True)  # Field name made lowercase.
    correctness = models.CharField(db_column='Correctness', max_length=1, blank=True, null=True)  # Field name made lowercase.
    appraisalid = models.CharField(db_column='AppraisalId', max_length=20, blank=True, null=True)  # Field name made lowercase.
    progressprocent = models.IntegerField(db_column='ProgressProcent', blank=True, null=True)  # Field name made lowercase.
    classify = models.CharField(db_column='Classify', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flowchartno = models.CharField(db_column='FlowChartNo', max_length=200, blank=True, null=True)  # Field name made lowercase.
    spday = models.FloatField(db_column='SPDay', blank=True, null=True)  # Field name made lowercase.
    spaday = models.FloatField(db_column='SPADay', blank=True, null=True)  # Field name made lowercase.
    saday = models.FloatField(db_column='SADay', blank=True, null=True)  # Field name made lowercase.
    manday = models.IntegerField(db_column='ManDay', blank=True, null=True)  # Field name made lowercase.
    subtasktype = models.IntegerField(db_column='SubTaskType', blank=True, null=True)  # Field name made lowercase.
    diff = models.IntegerField(db_column='Diff', blank=True, null=True)  # Field name made lowercase.
    difficulty = models.CharField(db_column='Difficulty', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf06 = models.CharField(db_column='UDF06', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf07 = models.DateTimeField(db_column='UDF07', blank=True, null=True)  # Field name made lowercase.
    udf08 = models.CharField(db_column='UDF08', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf11 = models.CharField(db_column='UDF11', max_length=20, blank=True, null=True)  # Field name made lowercase.
    calpriority = models.IntegerField(db_column='CalPriority', blank=True, null=True)  # Field name made lowercase.
    schpriority = models.FloatField(db_column='SchPriority', blank=True, null=True)  # Field name made lowercase.
    schedulestate = models.CharField(db_column='ScheduleState', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dayjob = models.CharField(db_column='DayJob', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mastno = models.CharField(db_column='MastNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cycletask = models.CharField(db_column='CycleTask', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tiddesc = models.CharField(db_column='TidDesc', max_length=3000, blank=True, null=True)  # Field name made lowercase.
    sessionflowchartno = models.CharField(db_column='SessionFlowChartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    sprogress = models.CharField(db_column='SProgress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    scontact = models.CharField(db_column='SContact', max_length=20, blank=True, null=True)  # Field name made lowercase.
    recordid = models.CharField(db_column='RecordID', max_length=6, blank=True, null=True)  # Field name made lowercase.
    projectid = models.CharField(db_column='ProjectID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    projectname = models.CharField(db_column='ProjectName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    outday = models.IntegerField(db_column='OutDay', blank=True, null=True)  # Field name made lowercase.
    pworktimeh = models.DecimalField(db_column='PWorkTimeH', max_digits=3, decimal_places=3)  # Field name made lowercase.
    eworktimeh = models.DecimalField(db_column='EWorkTimeH', max_digits=3, decimal_places=3)  # Field name made lowercase.
    findex = models.CharField(db_column='FIndex', max_length=200, blank=True, null=True)  # Field name made lowercase.
    rptvisible = models.CharField(db_column='RptVisible', max_length=1)  # Field name made lowercase.
    tasktypedesc = models.CharField(db_column='TaskTypeDesc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    subtasktypedesc = models.CharField(db_column='SubTaskTypeDesc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    displaytype = models.IntegerField(db_column='DisplayType', blank=True, null=True)  # Field name made lowercase.
    weekly = models.IntegerField(db_column='Weekly', blank=True, null=True)  # Field name made lowercase.
    quarterly = models.IntegerField(db_column='Quarterly', blank=True, null=True)  # Field name made lowercase.
    weight = models.FloatField(db_column='Weight', blank=True, null=True)  # Field name made lowercase.
    capacity = models.IntegerField(db_column='Capacity', blank=True, null=True)  # Field name made lowercase.
    projectscore = models.IntegerField(db_column='ProjectScore', blank=True, null=True)  # Field name made lowercase.
    dayjobtaskcaption = models.CharField(db_column='DayjobTaskCaption', max_length=503, blank=True, null=True)  # Field name made lowercase.
    nofscore = models.FloatField(db_column='NoFScore', blank=True, null=True)  # Field name made lowercase.
    schcount = models.IntegerField(db_column='SchCount', blank=True, null=True)  # Field name made lowercase.
    reference = models.CharField(db_column='Reference', max_length=30, blank=True, null=True)  # Field name made lowercase.
    hoperation = models.CharField(db_column='HOperation', max_length=1, blank=True, null=True)  # Field name made lowercase.
    charge = models.CharField(db_column='Charge', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tasktypescore = models.FloatField(db_column='TaskTypeScore', blank=True, null=True)  # Field name made lowercase.
    special = models.CharField(db_column='Special', max_length=1, blank=True, null=True)  # Field name made lowercase.
    process = models.CharField(db_column='Process', max_length=1, blank=True, null=True)  # Field name made lowercase.
    requestdate = models.DateTimeField(db_column='RequestDate', blank=True, null=True)  # Field name made lowercase.
    splanbdate = models.DateTimeField(db_column='SPlanBDate', blank=True, null=True)  # Field name made lowercase.
    splanedate = models.DateTimeField(db_column='SPlanEDate', blank=True, null=True)  # Field name made lowercase.
    squarterly = models.IntegerField(db_column='SQuarterly', blank=True, null=True)  # Field name made lowercase.
    realtasktype = models.CharField(db_column='RealTaskType', max_length=62, blank=True, null=True)  # Field name made lowercase.
    schprioritysp = models.FloatField(db_column='SchPrioritySP', blank=True, null=True)  # Field name made lowercase.
    r_flag = models.BooleanField(db_column='R_Flag', blank=True, null=True)  # Field name made lowercase.
    inc_id = models.IntegerField(db_column='INC_ID',primary_key=True)
    lookupscore = models.FloatField(db_column='LookUpScore', blank=True, null=True)  # Field name made lowercase.
    tasktypedc = models.CharField(db_column='TaskTypeDC', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_Task_Bonus_SL'

class Tpdetail(models.Model):
    tpdetailid = models.FloatField(db_column='TpDetailId')  # Field name made lowercase.
    tpmastid = models.DecimalField(db_column='TpMastId', max_digits=18, decimal_places=0)  # Field name made lowercase.
    tptname = models.CharField(db_column='TptName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=50, blank=True, null=True)  # Field name made lowercase.
    priority = models.IntegerField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=1, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=256, blank=True, null=True)  # Field name made lowercase.
    revisedby = models.CharField(db_column='RevisedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    operate = models.CharField(db_column='Operate', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cycletime = models.DateTimeField(db_column='CycleTime', blank=True, null=True)  # Field name made lowercase.
    cycleperiod = models.IntegerField(db_column='CyclePeriod', blank=True, null=True)  # Field name made lowercase.
    day = models.IntegerField(db_column='Day', blank=True, null=True)  # Field name made lowercase.
    invalid = models.CharField(db_column='Invalid', max_length=1, blank=True, null=True)  # Field name made lowercase.
    sessionid = models.CharField(db_column='SessionId', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tasktype = models.IntegerField(db_column='TaskType', blank=True, null=True)  # Field name made lowercase.
    subtasktype = models.IntegerField(db_column='SubTaskType', blank=True, null=True)  # Field name made lowercase.
    diff = models.IntegerField(db_column='Diff', blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID',  primary_key=True)  # Field name made lowercase

    class Meta:
        managed = False
        db_table = 'TpDetail'
        unique_together = (('tpdetailid', 'tpmastid'),)
        app_label = 'DataBase_MPMS'
class Tpmast(models.Model):
    tpmastid = models.DecimalField(db_column='TpMastId', max_digits=18, decimal_places=0)  # Field name made lowercase.
    deptid = models.CharField(db_column='DeptId', max_length=12, blank=True, null=True)  # Field name made lowercase.
    deptname = models.CharField(db_column='DeptName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    tpno = models.CharField(db_column='TpNo', max_length=15, blank=True, null=True)  # Field name made lowercase.
    tpname = models.CharField(db_column='TpName', max_length=20, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=12, blank=True, null=True)  # Field name made lowercase.
    tpdesc = models.CharField(db_column='TpDesc', max_length=256, blank=True, null=True)  # Field name made lowercase.
    sessionid = models.CharField(db_column='SessionId', max_length=30, blank=True, null=True)  # Field name made lowercase.
    revisedby = models.CharField(db_column='RevisedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID',  primary_key=True)  # Field name made lowercase
    manager = models.CharField(db_column='Manager', max_length=1, blank=True, null=True)  # Field name made lowercase.
    

    class Meta:
        managed = False
        db_table = 'TpMast'
        app_label = 'DataBase_MPMS'

class VTaskRecordid(models.Model):
    recordid = models.CharField(db_column='RecordId', max_length=6, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pid = models.CharField(db_column='Pid', max_length=16)  # Field name made lowercase.
    tid = models.FloatField(db_column='Tid')  # Field name made lowercase.
    taskid = models.FloatField(db_column='TaskID')  # Field name made lowercase.
    task = models.CharField(db_column='Task', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=25, blank=True, null=True)  # Field name made lowercase.
    planbdate = models.DateTimeField(db_column='PlanBDate', blank=True, null=True)  # Field name made lowercase.
    etime = models.FloatField(db_column='Etime', blank=True, null=True)  # Field name made lowercase.
    planedate = models.DateTimeField(db_column='PlanEDate', blank=True, null=True)  # Field name made lowercase.
    atime = models.FloatField(blank=True, null=True)
    bdate = models.DateTimeField(db_column='BDate', blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='EDate', blank=True, null=True)  # Field name made lowercase.
    priority = models.IntegerField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=255, blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    revisedby = models.CharField(db_column='RevisedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    tasktype = models.IntegerField(db_column='TaskType', blank=True, null=True)  # Field name made lowercase.
    subtasktype = models.IntegerField(db_column='SubTaskType', blank=True, null=True)  # Field name made lowercase.
    diff = models.IntegerField(db_column='Diff', blank=True, null=True)  # Field name made lowercase.
    taskoption = models.IntegerField(db_column='Taskoption', blank=True, null=True)  # Field name made lowercase.
    relationid = models.CharField(db_column='relationID', max_length=200, blank=True, null=True)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
    docpath = models.CharField(db_column='DocPath', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emaildesp = models.TextField(db_column='EmailDesp', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf51 = models.CharField(db_column='UDF51', max_length=10, blank=True, null=True)  # Field name made lowercase.
    udf52 = models.DecimalField(db_column='UDF52', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    smsreceiver = models.CharField(db_column='SMSReceiver', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dispose = models.CharField(db_column='Dispose', max_length=2, blank=True, null=True)  # Field name made lowercase.
    editionid = models.CharField(db_column='EditionID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    oldprogress = models.CharField(db_column='OldProgress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    delayday = models.IntegerField(db_column='DelayDay', blank=True, null=True)  # Field name made lowercase.
    companyid = models.CharField(db_column='CompanyID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    subprojectid = models.CharField(db_column='SubProjectID', max_length=6, blank=True, null=True)  # Field name made lowercase.
    class_field = models.IntegerField(db_column='Class', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    sendctlemail = models.IntegerField(db_column='SendCTLEmail', blank=True, null=True)  # Field name made lowercase.
    generateddoc = models.CharField(db_column='GeneratedDoc', max_length=300, blank=True, null=True)  # Field name made lowercase.
    relationgoalid = models.CharField(db_column='RelationGoalId', max_length=200, blank=True, null=True)  # Field name made lowercase.
    escore = models.FloatField(db_column='EScore', blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    totalscore = models.FloatField(db_column='TotalScore', blank=True, null=True)  # Field name made lowercase.
    setting = models.CharField(db_column='Setting', max_length=1, blank=True, null=True)  # Field name made lowercase.
    questionno = models.CharField(db_column='QuestionNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    req_date = models.DateTimeField(db_column='Req_Date', blank=True, null=True)  # Field name made lowercase.
    reply_taskno = models.CharField(db_column='Reply_TaskNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    isschedule = models.CharField(db_column='IsSchedule', max_length=1, blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=500, blank=True, null=True)  # Field name made lowercase.
    environmentid = models.CharField(db_column='EnvironmentID', max_length=6, blank=True, null=True)  # Field name made lowercase.
    categoryid = models.FloatField(db_column='CategoryID', blank=True, null=True)  # Field name made lowercase.
    rank = models.IntegerField(db_column='Rank', blank=True, null=True)  # Field name made lowercase.
    correctness = models.CharField(db_column='Correctness', max_length=1, blank=True, null=True)  # Field name made lowercase.
    appraisalid = models.CharField(db_column='AppraisalId', max_length=20, blank=True, null=True)  # Field name made lowercase.
    progressprocent = models.IntegerField(db_column='ProgressProcent', blank=True, null=True)  # Field name made lowercase.
    classify = models.CharField(db_column='Classify', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flowchartno = models.CharField(db_column='FlowChartNo', max_length=200, blank=True, null=True)  # Field name made lowercase.
    spday = models.FloatField(db_column='SPDay', blank=True, null=True)  # Field name made lowercase.
    spaday = models.FloatField(db_column='SPADay', blank=True, null=True)  # Field name made lowercase.
    saday = models.FloatField(db_column='SADay', blank=True, null=True)  # Field name made lowercase.
    manday = models.IntegerField(db_column='ManDay', blank=True, null=True)  # Field name made lowercase.
    difficulty = models.CharField(db_column='Difficulty', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf06 = models.CharField(db_column='UDF06', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf07 = models.DateTimeField(db_column='UDF07', blank=True, null=True)  # Field name made lowercase.
    udf08 = models.CharField(db_column='UDF08', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf09 = models.CharField(db_column='UDF09', max_length=20, blank=True, null=True)  # Field name made lowercase.
    udf10 = models.CharField(db_column='UDF10', max_length=20, blank=True, null=True)  # Field name made lowercase.
    calpriority = models.IntegerField(db_column='CalPriority', blank=True, null=True)  # Field name made lowercase.
    schpriority = models.FloatField(db_column='SchPriority', blank=True, null=True)  # Field name made lowercase.
    schedulestate = models.CharField(db_column='ScheduleState', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dayjob = models.CharField(db_column='DayJob', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mastno = models.CharField(db_column='MastNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cycletask = models.CharField(db_column='CycleTask', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf11 = models.CharField(db_column='UDF11', max_length=20, blank=True, null=True)  # Field name made lowercase.
    reference = models.CharField(db_column='Reference', max_length=30, blank=True, null=True)  # Field name made lowercase.
    hoperation = models.CharField(db_column='HOperation', max_length=1, blank=True, null=True)  # Field name made lowercase.
    charge = models.CharField(db_column='Charge', max_length=1, blank=True, null=True)  # Field name made lowercase.
    special = models.CharField(db_column='Special', max_length=1, blank=True, null=True)  # Field name made lowercase.
    process = models.CharField(db_column='Process', max_length=1, blank=True, null=True)  # Field name made lowercase.
    requestdate = models.DateTimeField(db_column='RequestDate', blank=True, null=True)  # Field name made lowercase.
    schprioritysp = models.FloatField(db_column='SchPrioritySP', blank=True, null=True)  # Field name made lowercase.
    r_flag = models.NullBooleanField(db_column='R_Flag', blank=True, null=True)  # Field name made lowercase.
    taskcategory = models.CharField(db_column='TaskCategory', max_length=5, blank=True, null=True)  # Field name made lowercase.    
    inc_id = models.AutoField(db_column='INC_ID',  primary_key=True)  # Field name made lowercase
    
    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_Task_RecordId'
        app_label = 'DataBase_MPMS'
    
    
class VTasklist(models.Model):
    recordid = models.CharField(db_column='RecordId', max_length=6, blank=True, null=True)  # Field name made lowercase.
    sessionid = models.CharField(db_column='SessionId', max_length=37, blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pid = models.CharField(db_column='Pid', max_length=16)  # Field name made lowercase.
    tid = models.FloatField(db_column='Tid')  # Field name made lowercase.
    desp = models.BinaryField(db_column='Desp', blank=True, null=True)  # Field name made lowercase.
    priority = models.FloatField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    planbdate = models.DateTimeField(db_column='PlanBDate', blank=True, null=True)  # Field name made lowercase.
    etime = models.FloatField(db_column='Etime', blank=True, null=True)  # Field name made lowercase.
    planedate = models.DateTimeField(db_column='PlanEDate', blank=True, null=True)  # Field name made lowercase.
    bdate = models.DateTimeField(db_column='Bdate', blank=True, null=True)  # Field name made lowercase.
    atime = models.FloatField(db_column='Atime', blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='Edate', blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    sdesp = models.CharField(db_column='SDesp', max_length=3000, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=20, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=256, blank=True, null=True)  # Field name made lowercase.
    revisedby = models.CharField(db_column='RevisedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    msgflag = models.CharField(db_column='MsgFlag', max_length=1, blank=True, null=True)  # Field name made lowercase.
    recerver = models.CharField(db_column='Recerver', max_length=50, blank=True, null=True)  # Field name made lowercase.
    flowchartno = models.CharField(db_column='FlowChartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    parent = models.CharField(db_column='Parent', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=50, blank=True, null=True)  # Field name made lowercase.
    class_field = models.IntegerField(db_column='Class', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    weight = models.FloatField(db_column='Weight', blank=True, null=True)  # Field name made lowercase.
    goaltype = models.CharField(db_column='GoalType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    capacity = models.IntegerField(db_column='Capacity', blank=True, null=True)  # Field name made lowercase.
    djcapacity = models.IntegerField(db_column='DJCapacity', blank=True, null=True)  # Field name made lowercase.
    cycleno = models.CharField(db_column='CycleNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    schrate = models.IntegerField(db_column='SchRate', blank=True, null=True)  # Field name made lowercase.
    estimate = models.IntegerField(db_column='Estimate', blank=True, null=True)  # Field name made lowercase.
    handletype = models.CharField(db_column='HandleType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.IntegerField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    signify = models.IntegerField()
    request = models.IntegerField()
    completed = models.IntegerField()
    problems = models.IntegerField()
    earliesunfinish = models.DateTimeField(db_column='earliesUnFinish', blank=True, null=True)  # Field name made lowercase.
    lastunfinish = models.DateTimeField(db_column='lastUnFinish', blank=True, null=True)  # Field name made lowercase.
    score = models.IntegerField()
    minplanbdate = models.DateTimeField(db_column='MinPlanBDate', blank=True, null=True)  # Field name made lowercase.
    maxplanedate = models.DateTimeField(db_column='MaxPlanEDate', blank=True, null=True)  # Field name made lowercase.
    taskqty = models.IntegerField(db_column='TaskQty', blank=True, null=True)  # Field name made lowercase.
    pschedule = models.IntegerField(db_column='PSchedule')  # Field name made lowercase.
    aschedule = models.IntegerField(db_column='ASchedule')  # Field name made lowercase.
    outstandday = models.IntegerField(db_column='OutstandDay', blank=True, null=True)  # Field name made lowercase.
    outstandqty = models.IntegerField(db_column='OutstandQty', blank=True, null=True)  # Field name made lowercase.
    projectscore = models.IntegerField(db_column='ProjectScore', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_Tasklist'

class VTasklistS(models.Model):
    recordid = models.CharField(db_column='RecordId', max_length=6, blank=True, null=True)  # Field name made lowercase.
    sessionid = models.CharField(db_column='SessionId', max_length=37, blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pid = models.CharField(db_column='Pid', max_length=16)  # Field name made lowercase.
    tid = models.FloatField(db_column='Tid')  # Field name made lowercase.
    desp = models.BinaryField(db_column='Desp', blank=True, null=True)  # Field name made lowercase.
    priority = models.FloatField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    planbdate = models.DateTimeField(db_column='PlanBDate', blank=True, null=True)  # Field name made lowercase.
    etime = models.FloatField(db_column='Etime', blank=True, null=True)  # Field name made lowercase.
    planedate = models.DateTimeField(db_column='PlanEDate', blank=True, null=True)  # Field name made lowercase.
    bdate = models.DateTimeField(db_column='Bdate', blank=True, null=True)  # Field name made lowercase.
    atime = models.FloatField(db_column='Atime', blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='Edate', blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    sdesp = models.CharField(db_column='SDesp', max_length=3000, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=20, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=256, blank=True, null=True)  # Field name made lowercase.
    revisedby = models.CharField(db_column='RevisedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    msgflag = models.CharField(db_column='MsgFlag', max_length=1, blank=True, null=True)  # Field name made lowercase.
    recerver = models.CharField(db_column='Recerver', max_length=50, blank=True, null=True)  # Field name made lowercase.
    flowchartno = models.CharField(db_column='FlowChartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    parent = models.CharField(db_column='Parent', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=50, blank=True, null=True)  # Field name made lowercase.
    class_field = models.IntegerField(db_column='Class', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    weight = models.FloatField(db_column='Weight', blank=True, null=True)  # Field name made lowercase.
    goaltype = models.CharField(db_column='GoalType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    capacity = models.IntegerField(db_column='Capacity', blank=True, null=True)  # Field name made lowercase.
    djcapacity = models.IntegerField(db_column='DJCapacity', blank=True, null=True)  # Field name made lowercase.
    cycleno = models.CharField(db_column='CycleNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    schrate = models.IntegerField(db_column='SchRate', blank=True, null=True)  # Field name made lowercase.
    estimate = models.IntegerField(db_column='Estimate', blank=True, null=True)  # Field name made lowercase.
    handletype = models.CharField(db_column='HandleType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.IntegerField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    projectscore = models.IntegerField(db_column='ProjectScore', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_TaskList_S'

class Schperiod(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    period = models.CharField(db_column='Period', primary_key=True, max_length=20)  # Field name made lowercase.
    from_field = models.CharField(db_column='From', max_length=16, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    to = models.CharField(db_column='To', max_length=16, blank=True, null=True)  # Field name made lowercase.
    hour = models.FloatField(db_column='Hour', blank=True, null=True)  # Field name made lowercase.
    logic = models.CharField(db_column='Logic', max_length=255, blank=True, null=True)  # Field name made lowercase.
    prefix = models.CharField(db_column='Prefix', max_length=1, blank=True, null=True)  # Field name made lowercase.
    completion = models.FloatField(db_column='Completion', blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SchPeriod'


class Schtype(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    typeno = models.FloatField(db_column='TypeNo', primary_key=True)  # Field name made lowercase.
    typename = models.CharField(db_column='TypeName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    logic = models.CharField(db_column='Logic', max_length=255, blank=True, null=True)  # Field name made lowercase.
    formula = models.CharField(db_column='Formula', max_length=255, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=255, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SchType'


class Schuserparams(MultipleKeyBaseModel):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    quarterly = models.CharField(db_column='Quarterly', primary_key=True, max_length=6)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=20)  # Field name made lowercase.
    periods = models.CharField(db_column='Periods', max_length=50, blank=True, null=True)  # Field name made lowercase.
    periodscpt = models.CharField(db_column='PeriodsCpt', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mincpt = models.FloatField(db_column='MinCpt', blank=True, null=True)  # Field name made lowercase.
    maxcpt = models.FloatField(db_column='MaxCpt', blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SchUserParams'
        unique_together = (('quarterly', 'contact'),)

class VSchuserparamsQuarterly(models.Model):
    quarterlyflag = models.CharField(db_column='QuarterlyFlag', max_length=7)  # Field name made lowercase.
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    quarterly = models.CharField(db_column='Quarterly',primary_key=True, max_length=6)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=20)  # Field name made lowercase.
    periods = models.CharField(db_column='Periods', max_length=50, blank=True, null=True)  # Field name made lowercase.
    periodscpt = models.CharField(db_column='PeriodsCpt', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mincpt = models.FloatField(db_column='MinCpt', blank=True, null=True)  # Field name made lowercase.
    maxcpt = models.FloatField(db_column='MaxCpt', blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_SchUserParams_Quarterly'


class Syspara(MultipleKeyBaseModel):
    nfield = models.CharField(primary_key=True, max_length=30)
    ftype = models.CharField(max_length=30)
    fvalue = models.TextField(blank=True, null=True)  # This field type is a guess.
    desp = models.CharField(db_column='DESP', max_length=500, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Syspara'
        unique_together = (('nfield', 'ftype'),)

class Schformula(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    period = models.CharField(db_column='Period', primary_key=True, max_length=20)  # Field name made lowercase.
    typeno = models.FloatField(db_column='TypeNo')  # Field name made lowercase.
    class_field = models.IntegerField(db_column='Class', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    priority = models.IntegerField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    schpriority = models.FloatField(db_column='SchPriority', blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SchFormula'
    
class Schmh(models.Model):
    quarterly = models.CharField(db_column='Quarterly', max_length=6)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=20)  # Field name made lowercase.
    isnew = models.CharField(db_column='IsNew', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pid = models.TextField(db_column='Pid')  # Field name made lowercase.
    tid = models.FloatField(db_column='Tid')  # Field name made lowercase.
    taskid = models.FloatField(db_column='TaskId')  # Field name made lowercase.
    task = models.CharField(db_column='Task', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    planbdate = models.DateTimeField(db_column='PlanBDate', blank=True, null=True)  # Field name made lowercase.
    planedate = models.DateTimeField(db_column='PlanEDate', blank=True, null=True)  # Field name made lowercase.
    relationgoalid = models.TextField(db_column='RelationGoalId', blank=True, null=True)  # Field name made lowercase.
    category = models.IntegerField(db_column='Category', blank=True, null=True)  # Field name made lowercase.
    period = models.TextField(db_column='Period', blank=True, null=True)  # Field name made lowercase.
    tasktypeno = models.TextField(db_column='TaskTypeNo', blank=True, null=True)  # Field name made lowercase.
    tasktypepriority = models.FloatField(db_column='TaskTypePriority', blank=True, null=True)  # Field name made lowercase.
    flpriority = models.FloatField(db_column='FlPriority', blank=True, null=True)  # Field name made lowercase.
    sesspriority = models.FloatField(db_column='SessPriority', blank=True, null=True)  # Field name made lowercase.
    schpriority = models.FloatField(db_column='SchPriority', blank=True, null=True)  # Field name made lowercase.
    schbdate = models.DateTimeField(db_column='SchBDate', blank=True, null=True)  # Field name made lowercase.
    schedate = models.DateTimeField(db_column='SchEDate', blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID',  primary_key=True)  # Field name made lowercase.    

    class Meta:
        managed = False
        db_table = 'SCHMH'
        unique_together = (('quarterly', 'contact','pid','tid','taskid'),)

class Testtask(models.Model):
    pid = models.CharField(db_column='Pid', primary_key=True, max_length=16)  # Field name made lowercase.
    tid = models.FloatField(db_column='Tid')  # Field name made lowercase.
    taskid = models.FloatField(db_column='TaskId')  # Field name made lowercase.
    task = models.CharField(db_column='Task', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=25, blank=True, null=True)  # Field name made lowercase.
    planbdate = models.DateTimeField(db_column='PlanBDate', blank=True, null=True)  # Field name made lowercase.
    planedate = models.DateTimeField(db_column='PlanEDate', blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TestTask'
        unique_together = (('pid', 'tid', 'taskid'),)        
class Pmsut(models.Model):
    ut001 = models.CharField(db_column='UT001', max_length=15)  # Field name made lowercase.
    ut002 = models.CharField(db_column='UT002', max_length=16)  # Field name made lowercase.
    ut003 = models.FloatField(db_column='UT003')  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.DecimalField(db_column='UDF04', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.DecimalField(db_column='UDF05', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PMSUT'
        unique_together = (('ut001', 'ut002', 'ut003'),)        

class Tasktypelist(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    tasktype = models.IntegerField(db_column='TaskType')  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=100, blank=True, null=True)  # Field name made lowercase.
    time = models.FloatField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    difficulties1 = models.FloatField(db_column='Difficulties1', blank=True, null=True)  # Field name made lowercase.
    difficulties2 = models.FloatField(db_column='Difficulties2', blank=True, null=True)  # Field name made lowercase.
    difficulties3 = models.FloatField(db_column='Difficulties3', blank=True, null=True)  # Field name made lowercase.
    issubtype = models.CharField(db_column='IsSubType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    parenttype = models.IntegerField(db_column='ParentType', blank=True, null=True)  # Field name made lowercase.
    displaytype = models.IntegerField(db_column='DisplayType', blank=True, null=True)  # Field name made lowercase.
    scorechange = models.CharField(db_column='ScoreChange', max_length=1, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TaskTypeList'

class LSTasktypelist(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    tasktype = models.IntegerField(db_column='TaskType')  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=100, blank=True, null=True)  # Field name made lowercase.
    time = models.FloatField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    difficulties1 = models.FloatField(db_column='Difficulties1', blank=True, null=True)  # Field name made lowercase.
    difficulties2 = models.FloatField(db_column='Difficulties2', blank=True, null=True)  # Field name made lowercase.
    difficulties3 = models.FloatField(db_column='Difficulties3', blank=True, null=True)  # Field name made lowercase.
    issubtype = models.CharField(db_column='IsSubType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    parenttype = models.IntegerField(db_column='ParentType', blank=True, null=True)  # Field name made lowercase.
    displaytype = models.IntegerField(db_column='DisplayType', blank=True, null=True)  # Field name made lowercase.
    scorechange = models.CharField(db_column='ScoreChange', max_length=1, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LSTaskTypeList'

class Tecma(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    ma001 = models.CharField(db_column='MA001', max_length=11)  # Field name made lowercase.
    ma002 = models.CharField(db_column='MA002', max_length=11)  # Field name made lowercase.
    ma003 = models.CharField(db_column='MA003', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ma004 = models.CharField(db_column='MA004', max_length=200, blank=True, null=True)  # Field name made lowercase.
    ma005 = models.IntegerField(db_column='MA005', blank=True, null=True)  # Field name made lowercase.
    ma006 = models.CharField(db_column='MA006', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ma007 = models.CharField(db_column='MA007', max_length=11, blank=True, null=True)  # Field name made lowercase.
    ma008 = models.CharField(db_column='MA008', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID',primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TECMA'

class VTecma(models.Model):
    ma001 = models.CharField(db_column='MA001', max_length=11)  # Field name made lowercase.
    ma002 = models.CharField(db_column='MA002', max_length=11)  # Field name made lowercase.
    ma003 = models.CharField(db_column='MA003', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ma003c = models.CharField(db_column='MA003C', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ma003b = models.CharField(db_column='MA003B', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ma007 = models.CharField(db_column='MA007', max_length=11, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID',primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_TECMA'


class Tecmb(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mb001 = models.CharField(db_column='MB001', max_length=11, blank=True, null=True)  # Field name made lowercase.
    mb002 = models.CharField(db_column='MB002', max_length=4, blank=True, null=True)  # Field name made lowercase.
    mb003 = models.CharField(db_column='MB003', max_length=11, blank=True, null=True)  # Field name made lowercase.
    mb004 = models.CharField(db_column='MB004', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb005 = models.CharField(db_column='MB005', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mb006 = models.CharField(db_column='MB006', max_length=8, blank=True, null=True)  # Field name made lowercase.
    mb007 = models.TextField(db_column='MB007', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb008 = models.TextField(db_column='MB008', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb009 = models.TextField(db_column='MB009', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb010 = models.TextField(db_column='MB010', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb011 = models.TextField(db_column='MB011', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb012 = models.TextField(db_column='MB012', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb013 = models.CharField(db_column='MB013', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb015 = models.CharField(db_column='MB015', max_length=11, blank=True, null=True)  # Field name made lowercase.
    mb016 = models.CharField(db_column='MB016', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb017 = models.TextField(db_column='MB017', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb018 = models.CharField(db_column='MB018', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb019 = models.CharField(db_column='MB019', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb020 = models.CharField(db_column='MB020', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mb021 = models.TextField(db_column='MB021', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb022 = models.TextField(db_column='MB022', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pid = models.CharField(db_column='Pid', max_length=6, blank=True, null=True)  # Field name made lowercase.
    tid = models.FloatField(db_column='Tid', blank=True, null=True)  # Field name made lowercase.
    taskid = models.FloatField(db_column='TaskId', blank=True, null=True)  # Field name made lowercase.
    mb023 = models.CharField(db_column='MB023', max_length=15, blank=True, null=True)  # Field name made lowercase.
    mb024 = models.TextField(db_column='MB024', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb025 = models.TextField(db_column='MB025', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb026 = models.CharField(db_column='MB026', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb027 = models.IntegerField(db_column='MB027', blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    id = models.IntegerField(db_column='Id')  # Field name made lowercase.
    parentid = models.CharField(db_column='ParentId',max_length=20, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID',primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TECMB'

class VTecmb(models.Model):
    mb001c = models.CharField(db_column='MB001C', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb015c = models.CharField(db_column='MB015C', max_length=255, blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mb001 = models.CharField(db_column='MB001', max_length=11, blank=True, null=True)  # Field name made lowercase.
    mb002 = models.CharField(db_column='MB002', max_length=4, blank=True, null=True)  # Field name made lowercase.
    mb003 = models.CharField(db_column='MB003', max_length=11, blank=True, null=True)  # Field name made lowercase.
    mb004 = models.CharField(db_column='MB004', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb005 = models.CharField(db_column='MB005', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mb006 = models.CharField(db_column='MB006', max_length=8, blank=True, null=True)  # Field name made lowercase.
    mb007 = models.TextField(db_column='MB007', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb008 = models.TextField(db_column='MB008', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb009 = models.TextField(db_column='MB009', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb010 = models.TextField(db_column='MB010', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb011 = models.TextField(db_column='MB011', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb012 = models.TextField(db_column='MB012', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb013 = models.CharField(db_column='MB013', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb015 = models.CharField(db_column='MB015', max_length=11, blank=True, null=True)  # Field name made lowercase.
    mb016 = models.CharField(db_column='MB016', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb017 = models.TextField(db_column='MB017', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb018 = models.CharField(db_column='MB018', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb019 = models.CharField(db_column='MB019', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb020 = models.CharField(db_column='MB020', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mb021 = models.TextField(db_column='MB021', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb022 = models.TextField(db_column='MB022', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pid = models.CharField(db_column='Pid', max_length=6, blank=True, null=True)  # Field name made lowercase.
    tid = models.FloatField(db_column='Tid', blank=True, null=True)  # Field name made lowercase.
    taskid = models.FloatField(db_column='TaskId', blank=True, null=True)  # Field name made lowercase.
    mb023 = models.CharField(db_column='MB023', max_length=15, blank=True, null=True)  # Field name made lowercase.
    mb024 = models.TextField(db_column='MB024', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb025 = models.TextField(db_column='MB025', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    id = models.IntegerField(db_column='Id')  # Field name made lowercase.
    parentid = models.CharField(db_column='ParentId',max_length=20, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.IntegerField(db_column='INC_ID',primary_key=True)  # Field name made lowercase.
    mb026 = models.CharField(db_column='MB026', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb027 = models.IntegerField(db_column='MB027', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_TECMB'   


class Tecmc(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mc001 = models.CharField(db_column='MC001', max_length=11, blank=True, null=True)  # Field name made lowercase.
    mc002 = models.CharField(db_column='MC002', max_length=4, blank=True, null=True)  # Field name made lowercase.
    mc003 = models.CharField(db_column='MC003', max_length=1)  # Field name made lowercase.
    mc004 = models.CharField(db_column='MC004', max_length=4)  # Field name made lowercase.
    mc005 = models.TextField(db_column='MC005', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mc006 = models.BinaryField(db_column='MC006', blank=True, null=True)  # Field name made lowercase.
    mc007 = models.CharField(db_column='MC007', max_length=4, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    id = models.IntegerField(db_column='Id')  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TECMC'
        unique_together = (('mc003', 'mc004', 'id'),)


class Tecdailyplanner(models.Model):  
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=5)  # Field name made lowercase.
    inputdate = models.CharField(db_column='InputDate', max_length=8)  # Field name made lowercase.
    itemno = models.CharField(db_column='ItemNo', max_length=10)  # Field name made lowercase.
    taskno = models.CharField(db_column='TaskNo', max_length=53, blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    taskdescription = models.CharField(db_column='TaskDescription', max_length=500, blank=True, null=True)  # Field name made lowercase.
    goalachieve = models.CharField(db_column='GoalAchieve', max_length=500, blank=True, null=True)  # Field name made lowercase.
    platformused = models.CharField(db_column='PlatformUsed', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tasktype = models.CharField(db_column='TaskType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    framespecification = models.CharField(db_column='FrameSpecification', max_length=50, blank=True, null=True)  # Field name made lowercase. 
    designdoc = models.CharField(db_column='DesignDoc', max_length=50, blank=True, null=True)  # Field name made lowercase.
    flowchart = models.CharField(db_column='Flowchart', max_length=50, blank=True, null=True)  # Field name made lowercase.
    questions = models.CharField(db_column='Questions', max_length=50, blank=True, null=True)  # Field name made lowercase.
    newtechnicalneed = models.CharField(db_column='NewTechnicalNeed', max_length=500, blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=200, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=10, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    statusdesc = models.CharField(db_column='StatusDesc', max_length=80, blank=True, null=True)  # Field name made lowercase.
    dailyplannerstatus = models.CharField(db_column='DailyPlannerStatus', max_length=10, blank=True, null=True)  # Field name made lowercase.
    system = models.CharField(db_column='System', max_length=50, blank=True, null=True)  # Field name made lowercase. 
    abnormal = models.CharField(db_column='Abnormal', max_length=500, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TecDailyPlanner'
        unique_together = (('contact', 'inputdate', 'itemno'),)


class Tecsolutiontype(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.DecimalField(db_column='MODI_DATE', max_digits=17, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    flag = models.CharField(db_column='FLAG', max_length=3, blank=True, null=True)  # Field name made lowercase.
    solutiontype = models.CharField(db_column='SolutionType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    technical = models.CharField(db_column='Technical', max_length=100, blank=True, null=True)  # Field name made lowercase.
    condition = models.CharField(db_column='Condition', max_length=50, blank=True, null=True)  # Field name made lowercase.
    time = models.CharField(db_column='Time', max_length=10, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=200, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TecSolutionType'

class Tecdailyplannersolution(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=15)  # Field name made lowercase.
    inputdate = models.CharField(db_column='InputDate', max_length=8)  # Field name made lowercase.
    itemno = models.CharField(db_column='ItemNo', max_length=5)  # Field name made lowercase.
    stitemno = models.CharField(db_column='STItemNo', max_length=5)  # Field name made lowercase.
    mindmapid = models.CharField(db_column='MindMapId', max_length=18, blank=True, null=True)  # Field name made lowercase.
    mindmaplabel = models.CharField(db_column='MindMapLabel', max_length=50, blank=True, null=True)  # Field name made lowercase.
    technicid = models.CharField(db_column='TechnicId', max_length=50)  # Field name made lowercase.
    condition = models.CharField(db_column='Condition', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ftime = models.IntegerField(db_column='FTime', blank=True, null=True)  # Field name made lowercase.
    etime = models.IntegerField(db_column='ETime', blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tis = models.CharField(db_column='TIS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TecDailyPlannerSolution'
        unique_together = (('contact', 'inputdate', 'itemno', 'stitemno', 'technicid'),)    



class Tecdailyplannerimage(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=15)  # Field name made lowercase.
    inputdate = models.CharField(db_column='InputDate', max_length=8)  # Field name made lowercase.
    itemno = models.CharField(db_column='ItemNo', max_length=5)  # Field name made lowercase.
    imageno = models.CharField(db_column='ImageNo', max_length=5)  # Field name made lowercase.
    detailtext = models.TextField(db_column='DetailText', blank=True, null=True)  # Field name made lowercase.
    text = models.CharField(db_column='Text', max_length=255, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TecDailyPlannerImage'
        unique_together = (('imageno', 'itemno', 'inputdate', 'contact'),)        


class Tecmindmap(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    parentid = models.IntegerField(db_column='ParentId', blank=True, null=True)  # Field name made lowercase.
    sdesc = models.CharField(db_column='SDesc', max_length=500, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=255, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TecMindMap'


class Tecmindmapdetail(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mindmapid = models.IntegerField(db_column='MindMapId')  # Field name made lowercase.
    technicid = models.IntegerField(db_column='TechnicId')  # Field name made lowercase.
    ftime = models.IntegerField(db_column='FTime', blank=True, null=True)  # Field name made lowercase.
    etime = models.IntegerField(db_column='ETime', blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TecMindMapDetail'
        unique_together = (('mindmapid', 'technicid'),)
class Personalappraisal(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=15)  # Field name made lowercase.
    period = models.CharField(db_column='Period', max_length=10)  # Field name made lowercase.
    managements = models.TextField(db_column='Managements', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    comment = models.TextField(db_column='Comment', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    date = models.DateTimeField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    udf001 = models.CharField(db_column='UDF001', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf002 = models.CharField(db_column='UDF002', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf003 = models.CharField(db_column='UDF003', max_length=1, blank=True, null=True)  # Field name made lowercase.
    month = models.IntegerField(db_column='Month')  # Field name made lowercase.
    week = models.IntegerField(db_column='Week')  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PersonalAppraisal'
        unique_together = (('contact', 'period', 'month', 'week'),)


class VGoalmanagementM(models.Model):
    inc_id = models.IntegerField(db_column='INC_ID',  primary_key=True)  # Field name made lowercase.
    recordid = models.CharField(db_column='RecordId', max_length=6)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=15)  # Field name made lowercase.
    period = models.CharField(db_column='Period', max_length=10)  # Field name made lowercase.
    objective = models.TextField(db_column='Objective', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    taskno = models.CharField(db_column='TaskNo', max_length=48, blank=True, null=True)  # Field name made lowercase.
    task = models.CharField(db_column='Task', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    planbdate = models.DateTimeField(db_column='PlanBDate', blank=True, null=True)  # Field name made lowercase.
    planedate = models.DateTimeField(db_column='PlanEDate', blank=True, null=True)  # Field name made lowercase.
    class_field = models.IntegerField(db_column='Class', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    relationid = models.CharField(db_column='relationID', max_length=200, blank=True, null=True)  # Field name made lowercase.
    schpriority = models.FloatField(db_column='SchPriority', blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_GoalManagement_M'

class VGoalmanagementW(models.Model):
    inc_id = models.IntegerField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    recordid = models.CharField(db_column='RecordId', max_length=6)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=15)  # Field name made lowercase.
    period = models.CharField(db_column='Period', max_length=10)  # Field name made lowercase.
    objective = models.TextField(db_column='Objective', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    taskno = models.CharField(db_column='TaskNo', max_length=48, blank=True, null=True)  # Field name made lowercase.
    task = models.CharField(db_column='Task', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    planbdate = models.DateTimeField(db_column='PlanBDate', blank=True, null=True)  # Field name made lowercase.
    planedate = models.DateTimeField(db_column='PlanEDate', blank=True, null=True)  # Field name made lowercase.
    class_field = models.IntegerField(db_column='Class', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    relationid = models.CharField(db_column='relationID', max_length=200, blank=True, null=True)  # Field name made lowercase.
    schpriority = models.FloatField(db_column='SchPriority', blank=True, null=True)  # Field name made lowercase.
    relationgoalid = models.CharField(db_column='RelationGoalId', max_length=200, blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_GoalManagement_W'


class Mindmaptype(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    parentid = models.IntegerField(db_column='ParentId', blank=True, null=True)  # Field name made lowercase.
    sdesc = models.CharField(db_column='SDesc', max_length=500, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=255, blank=True, null=True)  # Field name made lowercase.
    order = models.IntegerField(db_column='Order', blank=True, null=True)  # Field name made lowercase.
    option1 = models.CharField(db_column='Option1', max_length=10, blank=True, null=True)  # Field name made lowercase.
    option2 = models.CharField(db_column='Option2', max_length=10, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'MindMapType'


class Mindmap(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    typeid = models.IntegerField(db_column='TypeId', blank=True, null=True)  # Field name made lowercase.
    sdesc = models.CharField(db_column='SDesc', max_length=500, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=255, blank=True, null=True)  # Field name made lowercase.
    data = models.TextField(db_column='Data', blank=True, null=True)  # Field name made lowercase.
    params = models.TextField(db_column='Params', blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    map_type = models.CharField(db_column='Map_Type', max_length=1,blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MindMap'

class VMindmapMenu(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    inc_id = models.IntegerField(db_column='INC_ID')  # Field name made lowercase.
    parentid = models.IntegerField(db_column='ParentId', blank=True, null=True)  # Field name made lowercase.
    sdesc = models.CharField(db_column='SDesc', max_length=500, blank=True, null=True)  # Field name made lowercase.
    order = models.IntegerField(db_column='Order', blank=True, null=True)  # Field name made lowercase.
    map_type = models.CharField(db_column='Map_Type', max_length=1,blank=True, null=True)  # Field name made lowercase.
    menu_type = models.CharField(db_column='Menu_Type', max_length=1,blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_MindMap_Menu'

class Solutiontype(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    solid = models.CharField(db_column='SOLId', max_length=15)  # Field name made lowercase.
    topic = models.TextField(db_column='Topic', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    usage = models.CharField(db_column='Usage', max_length=150, blank=True, null=True)  # Field name made lowercase.
    features = models.TextField(db_column='Features', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.
    area = models.CharField(db_column='Area', max_length=50, blank=True, null=True)  # Field name made lowercase.
    assumption = models.CharField(db_column='Assumption', max_length=200, blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mindmapid = models.IntegerField(db_column='MindmapId', blank=True, null=True)  # Field name made lowercase.
    mindmapprop = models.TextField(db_column='MindmapProp', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    codesnippet = models.TextField(db_column='CodeSnippet', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SolutionType'


class Solutiontypeassociate(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    solid = models.CharField(db_column='SOLId', max_length=15)  # Field name made lowercase.
    itemno = models.CharField(db_column='ItemNo', max_length=4)  # Field name made lowercase.
    aid = models.CharField(db_column='AId', max_length=20)  # Field name made lowercase.
    atype = models.CharField(db_column='AType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    descp = models.CharField(db_column='Descp', max_length=500, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SolutionTypeAssociate'
        unique_together = (('solid', 'itemno'),)

class SolutionTypeMindmap(models.Model):
    solid = models.CharField(db_column='SOLId', max_length=15, blank=True, null=True)  # Field name made lowercase.
    parentid = models.CharField(db_column='ParentId', max_length=4, blank=True, null=True)  # Field name made lowercase.
    curindex = models.CharField(db_column='CurIndex', max_length=100, blank=True, null=True)  # Field name made lowercase.
    curtype = models.CharField(db_column='CurType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    topic = models.TextField(db_column='Topic', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    usage = models.CharField(db_column='Usage', max_length=200, blank=True, null=True)  # Field name made lowercase.
    mindmapprop = models.TextField(db_column='MindmapProp', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    levels = models.IntegerField(db_column='Levels', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False

class MpGoals(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    quarterly = models.CharField(db_column='Quarterly', max_length=6)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=25)  # Field name made lowercase.
    qgoal = models.CharField(db_column='QGoal', max_length=100, blank=True, null=True)  # Field name made lowercase.
    wgoal = models.TextField(db_column='WGoal', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    remark = models.CharField(db_column='Remark', max_length=500, blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MP_Goals'
        unique_together = (('quarterly', 'contact'),)


class MpInvolved(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    quarterly = models.CharField(db_column='Quarterly',  max_length=6)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=25)  # Field name made lowercase.
    mindmap = models.CharField(db_column='Mindmap', max_length=200, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=500, blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MP_Involved'
        unique_together = (('quarterly', 'contact'),)


class MpChecksession(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    quarterly = models.CharField(db_column='Quarterly',  max_length=6)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=25)  # Field name made lowercase.
    checkedday = models.IntegerField(db_column='CheckedDay')  # Field name made lowercase.
    projects = models.CharField(db_column='Projects', max_length=500, blank=True, null=True)  # Field name made lowercase.
    checksessions = models.CharField(db_column='CheckSessions', max_length=500, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MP_CheckSession'
        unique_together = (('quarterly', 'contact', 'checkedday'),)


class MpStaffsessions(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    quarterly = models.CharField(db_column='Quarterly', max_length=6)  # Field name made lowercase.
    itemno = models.IntegerField(db_column='ItemNo')  # Field name made lowercase.
    recordid = models.CharField(db_column='RecordId', max_length=6, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=25, blank=True, null=True)  # Field name made lowercase.
    sessionid = models.CharField(db_column='SessionId', max_length=50, blank=True, null=True)  # Field name made lowercase.
    requirement = models.CharField(db_column='Requirement', max_length=200, blank=True, null=True)  # Field name made lowercase.
    sdesc = models.CharField(db_column='SDesc', max_length=500, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=500, blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MP_StaffSessions'
        unique_together = (('quarterly', 'itemno'),)        


class VTasklistP(models.Model):
    recordid = models.CharField(db_column='RecordId', max_length=6, blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pid = models.CharField(db_column='Pid', max_length=16)  # Field name made lowercase.
    tid = models.FloatField(db_column='Tid')  # Field name made lowercase.
    desp = models.BinaryField(db_column='Desp', blank=True, null=True)  # Field name made lowercase.
    priority = models.FloatField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    planbdate = models.DateTimeField(db_column='PlanBDate', blank=True, null=True)  # Field name made lowercase.
    etime = models.FloatField(db_column='Etime', blank=True, null=True)  # Field name made lowercase.
    planedate = models.DateTimeField(db_column='PlanEDate', blank=True, null=True)  # Field name made lowercase.
    bdate = models.DateTimeField(db_column='Bdate', blank=True, null=True)  # Field name made lowercase.
    atime = models.FloatField(db_column='Atime', blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='Edate', blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    sdesp = models.CharField(db_column='SDesp', max_length=3000, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=20, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=256, blank=True, null=True)  # Field name made lowercase.
    revisedby = models.CharField(db_column='RevisedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    msgflag = models.CharField(db_column='MsgFlag', max_length=1, blank=True, null=True)  # Field name made lowercase.
    recerver = models.CharField(db_column='Recerver', max_length=50, blank=True, null=True)  # Field name made lowercase.
    flowchartno = models.CharField(db_column='FlowChartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    parent = models.CharField(db_column='Parent', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=50, blank=True, null=True)  # Field name made lowercase.
    class_field = models.IntegerField(db_column='Class', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    weight = models.FloatField(db_column='Weight', blank=True, null=True)  # Field name made lowercase.
    goaltype = models.CharField(db_column='GoalType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    capacity = models.IntegerField(db_column='Capacity', blank=True, null=True)  # Field name made lowercase.
    djcapacity = models.IntegerField(db_column='DJCapacity', blank=True, null=True)  # Field name made lowercase.
    cycleno = models.CharField(db_column='CycleNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    schrate = models.IntegerField(db_column='SchRate', blank=True, null=True)  # Field name made lowercase.
    estimate = models.IntegerField(db_column='Estimate', blank=True, null=True)  # Field name made lowercase.
    handletype = models.CharField(db_column='HandleType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.IntegerField(db_column='INC_ID')  # Field name made lowercase.
    maxcreatedate = models.DateTimeField(db_column='MaxCreateDate', blank=True, null=True)  # Field name made lowercase.
    taskqty = models.IntegerField(db_column='TaskQty')  # Field name made lowercase.
    completedqty = models.IntegerField(db_column='CompletedQty')  # Field name made lowercase.
    allcontact = models.CharField(db_column='AllContact', max_length=100, blank=True, null=True)  # Field name made lowercase.
    projectname = models.CharField(db_column='ProjectName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    projectscore = models.IntegerField(db_column='ProjectScore', blank=True, null=True)  # Field name made lowercase.
    projectenddate = models.DateTimeField(db_column='ProjectEndDate', blank=True, null=True)  # Field name made lowercase.
    

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_TaskList_P'


class Docma(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    ma001 = models.CharField(db_column='MA001', max_length=50)  # Field name made lowercase.
    ma002 = models.CharField(db_column='MA002', max_length=10)  # Field name made lowercase.
    ma003 = models.CharField(db_column='MA003', max_length=150, blank=True, null=True)  # Field name made lowercase.
    ma004 = models.CharField(db_column='MA004', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ma005 = models.CharField(db_column='MA005', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ma006 = models.CharField(db_column='MA006', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ma007 = models.CharField(db_column='MA007', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ma008 = models.CharField(db_column='MA008', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ma009 = models.CharField(db_column='MA009', max_length=8, blank=True, null=True)  # Field name made lowercase.
    ma010 = models.CharField(db_column='MA010', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ma011 = models.CharField(db_column='MA011', max_length=8, blank=True, null=True)  # Field name made lowercase.
    ma012 = models.CharField(db_column='MA012', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ma013 = models.CharField(db_column='MA013', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ma014 = models.CharField(db_column='MA014', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ma015 = models.CharField(db_column='MA015', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    ma016 = models.CharField(db_column='MA016', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ma017 = models.CharField(db_column='MA017', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ma018 = models.TextField(db_column='MA018', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ma019 = models.CharField(db_column='MA019', max_length=12, blank=True, null=True)  # Field name made lowercase.
    ma020 = models.CharField(db_column='MA020', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ma021 = models.CharField(db_column='MA021', max_length=8, blank=True, null=True)  # Field name made lowercase.
    ma022 = models.CharField(db_column='MA022', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ma023 = models.CharField(db_column='MA023', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ma024 = models.CharField(db_column='MA024', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ma025 = models.CharField(db_column='MA025', max_length=60, blank=True, null=True)  # Field name made lowercase.
    ma026 = models.CharField(db_column='MA026', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ma027 = models.CharField(db_column='MA027', max_length=50, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DOCMA'
        unique_together = (('ma001', 'ma002'),)

class VDocma(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    ma001 = models.CharField(db_column='MA001', max_length=50)  # Field name made lowercase.
    ma002 = models.CharField(db_column='MA002', max_length=10)  # Field name made lowercase.
    ma003 = models.CharField(db_column='MA003', max_length=150, blank=True, null=True)  # Field name made lowercase.
    ma004 = models.CharField(db_column='MA004', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ma005 = models.CharField(db_column='MA005', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ma006 = models.CharField(db_column='MA006', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ma007 = models.CharField(db_column='MA007', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ma008 = models.CharField(db_column='MA008', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ma009 = models.CharField(db_column='MA009', max_length=8, blank=True, null=True)  # Field name made lowercase.
    ma010 = models.CharField(db_column='MA010', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ma011 = models.CharField(db_column='MA011', max_length=8, blank=True, null=True)  # Field name made lowercase.
    ma012 = models.CharField(db_column='MA012', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ma013 = models.CharField(db_column='MA013', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ma014 = models.CharField(db_column='MA014', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ma015 = models.CharField(db_column='MA015', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    ma016 = models.CharField(db_column='MA016', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ma017 = models.CharField(db_column='MA017', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ma018 = models.TextField(db_column='MA018', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ma019 = models.CharField(db_column='MA019', max_length=12, blank=True, null=True)  # Field name made lowercase.
    ma020 = models.CharField(db_column='MA020', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ma021 = models.CharField(db_column='MA021', max_length=8, blank=True, null=True)  # Field name made lowercase.
    ma022 = models.CharField(db_column='MA022', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ma023 = models.CharField(db_column='MA023', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ma024 = models.CharField(db_column='MA024', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ma025 = models.CharField(db_column='MA025', max_length=60, blank=True, null=True)  # Field name made lowercase.
    ma026 = models.CharField(db_column='MA026', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ma027 = models.CharField(db_column='MA027', max_length=50, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.IntegerField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    ma026c = models.CharField(db_column='MA026C', max_length=200, blank=True, null=True)  # Field name made lowercase.
    ma004c = models.CharField(db_column='MA004C', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_DOCMA'

class Docmg(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mg001 = models.CharField(db_column='MG001', max_length=50)  # Field name made lowercase.
    mg002 = models.CharField(db_column='MG002', max_length=10)  # Field name made lowercase.
    mg003 = models.BinaryField(db_column='MG003', blank=True, null=True)  # Field name made lowercase.
    mg004 = models.IntegerField(db_column='MG004')  # Field name made lowercase.
    mg005 = models.CharField(db_column='MG005', max_length=17, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DOCMG'
        unique_together = (('mg001', 'mg002', 'mg004'),)

class Requirement(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    rid = models.CharField(db_column='RID', max_length=30)  # Field name made lowercase.
    purpose = models.TextField(db_column='Purpose', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    feature = models.TextField(db_column='Feature', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    session_id = models.CharField(db_column='Session_id', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fr = models.TextField(db_column='FR', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    gh = models.TextField(db_column='GH', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mh = models.TextField(db_column='MH', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    uc = models.TextField(db_column='UC', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    nr = models.TextField(db_column='NR', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    attributes = models.TextField(db_column='Attributes', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    rt = models.CharField(db_column='RT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID',primary_key=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Requirement'

class Solutiontype(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    stid = models.CharField(db_column='STID', max_length=15)  # Field name made lowercase.
    sdescription = models.TextField(db_column='SDescription', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    courseref = models.CharField(db_column='CourseRef', max_length=255, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=16, blank=True, null=True)  # Field name made lowercase.
    mindmapid = models.CharField(db_column='MindmapId', max_length=20, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID',primary_key=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=255, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=500, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SolutionType'


class Course(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    courseid = models.IntegerField(db_column='CourseId')  # Field name made lowercase.
    subscription = models.CharField(db_column='Subscription', max_length=255, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sdescription = models.TextField(db_column='SDescription', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    videolink = models.TextField(db_column='VideoLink', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    contact = models.CharField(db_column='Contact', max_length=16, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=255, blank=True, null=True)  # Field name made lowercase.
    duration = models.CharField(db_column='Duration', max_length=50, blank=True, null=True)  # Field name made lowercase.
    rate = models.CharField(db_column='Rate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    sstatus = models.CharField(db_column='SStatus', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mindmapid = models.CharField(db_column='MindmapId', max_length=20, blank=True, null=True)  # Field name made lowercase.
    coursetype = models.CharField(db_column='CourseType', max_length=5, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID',primary_key=True)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'Course'

class Docma(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    ma001 = models.CharField(db_column='MA001', max_length=50)  # Field name made lowercase.
    ma002 = models.CharField(db_column='MA002', max_length=10)  # Field name made lowercase.
    ma003 = models.CharField(db_column='MA003', max_length=150, blank=True, null=True)  # Field name made lowercase.
    ma004 = models.CharField(db_column='MA004', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ma005 = models.CharField(db_column='MA005', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ma006 = models.CharField(db_column='MA006', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ma007 = models.CharField(db_column='MA007', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ma008 = models.CharField(db_column='MA008', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ma009 = models.CharField(db_column='MA009', max_length=8, blank=True, null=True)  # Field name made lowercase.
    ma010 = models.CharField(db_column='MA010', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ma011 = models.CharField(db_column='MA011', max_length=8, blank=True, null=True)  # Field name made lowercase.
    ma012 = models.CharField(db_column='MA012', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ma013 = models.CharField(db_column='MA013', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ma014 = models.CharField(db_column='MA014', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ma015 = models.CharField(db_column='MA015', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    ma016 = models.CharField(db_column='MA016', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ma017 = models.CharField(db_column='MA017', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ma018 = models.TextField(db_column='MA018', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ma019 = models.CharField(db_column='MA019', max_length=12, blank=True, null=True)  # Field name made lowercase.
    ma020 = models.CharField(db_column='MA020', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ma021 = models.CharField(db_column='MA021', max_length=8, blank=True, null=True)  # Field name made lowercase.
    ma022 = models.CharField(db_column='MA022', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ma023 = models.CharField(db_column='MA023', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ma024 = models.CharField(db_column='MA024', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ma025 = models.CharField(db_column='MA025', max_length=60, blank=True, null=True)  # Field name made lowercase.
    ma026 = models.CharField(db_column='MA026', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ma027 = models.CharField(db_column='MA027', max_length=50, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID' ,primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DOCMA'
        unique_together = (('ma001', 'ma002'),)

class Docmb(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mb001 = models.CharField(db_column='MB001', max_length=50)  # Field name made lowercase.
    mb002 = models.CharField(db_column='MB002', max_length=10)  # Field name made lowercase.
    mb003 = models.CharField(db_column='MB003', max_length=10)  # Field name made lowercase.
    mb004 = models.CharField(db_column='MB004', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mb005 = models.CharField(db_column='MB005', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mb006 = models.CharField(db_column='MB006', max_length=100, blank=True, null=True)  # Field name made lowercase.
    mb007 = models.TextField(db_column='MB007', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb008 = models.CharField(db_column='MB008', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mb009 = models.CharField(db_column='MB009', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mb010 = models.CharField(db_column='MB010', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mb011 = models.CharField(db_column='MB011', max_length=60, blank=True, null=True)  # Field name made lowercase.
    mb012 = models.BinaryField(db_column='MB012', blank=True, null=True)  # Field name made lowercase.
    mb013 = models.CharField(db_column='MB013', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mb014 = models.BinaryField(db_column='MB014', blank=True, null=True)  # Field name made lowercase.
    mb015 = models.CharField(db_column='MB015', max_length=500, blank=True, null=True)  # Field name made lowercase.
    mb016 = models.CharField(db_column='MB016', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mb017 = models.CharField(db_column='MB017', max_length=50, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DOCMB'
        unique_together = (('mb001', 'mb002', 'mb003'),)        

class Docmc(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mc001 = models.CharField(db_column='MC001', max_length=50)  # Field name made lowercase.
    mc002 = models.CharField(db_column='MC002', max_length=10)  # Field name made lowercase.
    mc003 = models.CharField(db_column='MC003', max_length=10)  # Field name made lowercase.
    mc004 = models.CharField(db_column='MC004', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mc005 = models.CharField(db_column='MC005', max_length=10, blank=True, null=True)  # Field name made lowercase.
    mc006 = models.CharField(db_column='MC006', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mc007 = models.CharField(db_column='MC007', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mc008 = models.CharField(db_column='MC008', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mc009 = models.CharField(db_column='MC009', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mc010 = models.CharField(db_column='MC010', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mc011 = models.CharField(db_column='MC011', max_length=60, blank=True, null=True)  # Field name made lowercase.
    mc012 = models.CharField(db_column='MC012', max_length=60, blank=True, null=True)  # Field name made lowercase.
    mc013 = models.CharField(db_column='MC013', max_length=500, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DOCMC'
        unique_together = (('mc001', 'mc002', 'mc003'),)

class Docmd(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    md001 = models.CharField(db_column='MD001', max_length=50)  # Field name made lowercase.
    md002 = models.CharField(db_column='MD002', max_length=10)  # Field name made lowercase.
    md003 = models.CharField(db_column='MD003', max_length=10)  # Field name made lowercase.
    md004 = models.CharField(db_column='MD004', max_length=50, blank=True, null=True)  # Field name made lowercase.
    md005 = models.CharField(db_column='MD005', max_length=50, blank=True, null=True)  # Field name made lowercase.
    md006 = models.CharField(db_column='MD006', max_length=50, blank=True, null=True)  # Field name made lowercase.
    md007 = models.CharField(db_column='MD007', max_length=100, blank=True, null=True)  # Field name made lowercase.
    md008 = models.CharField(db_column='MD008', max_length=1, blank=True, null=True)  # Field name made lowercase.
    md009 = models.CharField(db_column='MD009', max_length=30, blank=True, null=True)  # Field name made lowercase.
    md010 = models.CharField(db_column='MD010', max_length=30, blank=True, null=True)  # Field name made lowercase.
    md011 = models.CharField(db_column='MD011', max_length=60, blank=True, null=True)  # Field name made lowercase.
    md012 = models.CharField(db_column='MD012', max_length=60, blank=True, null=True)  # Field name made lowercase.
    md013 = models.CharField(db_column='MD013', max_length=500, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DOCMD'
        unique_together = (('md001', 'md002', 'md003'),)

class Docme(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    me001 = models.CharField(db_column='ME001', max_length=50)  # Field name made lowercase.
    me002 = models.CharField(db_column='ME002', max_length=10)  # Field name made lowercase.
    me003 = models.CharField(db_column='ME003', max_length=10)  # Field name made lowercase.
    me004 = models.CharField(db_column='ME004', max_length=10)  # Field name made lowercase.
    me005 = models.CharField(db_column='ME005', max_length=50, blank=True, null=True)  # Field name made lowercase.
    me006 = models.CharField(db_column='ME006', max_length=6, blank=True, null=True)  # Field name made lowercase.
    me007 = models.CharField(db_column='ME007', max_length=300, blank=True, null=True)  # Field name made lowercase.
    me008 = models.CharField(db_column='ME008', max_length=50, blank=True, null=True)  # Field name made lowercase.
    me009 = models.CharField(db_column='ME009', max_length=1, blank=True, null=True)  # Field name made lowercase.
    me010 = models.CharField(db_column='ME010', max_length=30, blank=True, null=True)  # Field name made lowercase.
    me011 = models.CharField(db_column='ME011', max_length=30, blank=True, null=True)  # Field name made lowercase.
    me012 = models.CharField(db_column='ME012', max_length=60, blank=True, null=True)  # Field name made lowercase.
    me013 = models.CharField(db_column='ME013', max_length=60, blank=True, null=True)  # Field name made lowercase.
    me014 = models.CharField(db_column='ME014', max_length=500, blank=True, null=True)  # Field name made lowercase.
    me015 = models.CharField(db_column='ME015', max_length=1, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DOCME'
        unique_together = (('me001', 'me002', 'me003', 'me004'),)
        
class Docmh(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mh001 = models.CharField(db_column='MH001', max_length=50)  # Field name made lowercase.
    mh002 = models.CharField(db_column='MH002', max_length=10)  # Field name made lowercase.
    mh003 = models.CharField(db_column='MH003', max_length=10)  # Field name made lowercase.
    mh004 = models.TextField(db_column='MH004', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mh005 = models.CharField(db_column='MH005', max_length=300, blank=True, null=True)  # Field name made lowercase.
    mh006 = models.CharField(db_column='MH006', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mh007 = models.CharField(db_column='MH007', max_length=8, blank=True, null=True)  # Field name made lowercase.
    mh008 = models.CharField(db_column='MH008', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mh009 = models.DecimalField(db_column='MH009', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mh010 = models.CharField(db_column='MH010', max_length=1, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DOCMH'
        unique_together = (('mh001', 'mh002', 'mh003'),)

class VDocmhTr(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mh001 = models.CharField(db_column='MH001', max_length=50)  # Field name made lowercase.
    mh002 = models.CharField(db_column='MH002', max_length=10)  # Field name made lowercase.
    mh003 = models.CharField(db_column='MH003', max_length=10)  # Field name made lowercase.
    mh004 = models.TextField(db_column='MH004', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mh005 = models.CharField(db_column='MH005', max_length=300, blank=True, null=True)  # Field name made lowercase.
    mh006 = models.CharField(db_column='MH006', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mh007 = models.CharField(db_column='MH007', max_length=8, blank=True, null=True)  # Field name made lowercase.
    mh008 = models.CharField(db_column='MH008', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mh009 = models.DecimalField(db_column='MH009', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mh010 = models.CharField(db_column='MH010', max_length=1, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    hastr = models.CharField(db_column='HasTR', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_DOCMH_TR'

class Docmi(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mi001 = models.CharField(db_column='MI001', max_length=50)  # Field name made lowercase.
    mi002 = models.CharField(db_column='MI002', max_length=10)  # Field name made lowercase.
    mi003 = models.CharField(db_column='MI003', max_length=10)  # Field name made lowercase.
    mi004 = models.TextField(db_column='MI004', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mi005 = models.CharField(db_column='MI005', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mi006 = models.CharField(db_column='MI006', max_length=10, blank=True, null=True)  # Field name made lowercase.
    mi007 = models.CharField(db_column='MI007', max_length=17, blank=True, null=True)  # Field name made lowercase.
    mi008 = models.CharField(db_column='MI008', max_length=10, blank=True, null=True)  # Field name made lowercase.
    mi009 = models.CharField(db_column='MI009', max_length=10, blank=True, null=True)  # Field name made lowercase.
    mi010 = models.BinaryField(db_column='MI010', blank=True, null=True)  # Field name made lowercase.
    mi011 = models.CharField(db_column='MI011', max_length=500, blank=True, null=True)  # Field name made lowercase.
    mi012 = models.CharField(db_column='MI012', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mi013 = models.CharField(db_column='MI013', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mi014 = models.CharField(db_column='MI014', max_length=60, blank=True, null=True)  # Field name made lowercase.
    mi015 = models.CharField(db_column='MI015', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DOCMI'
        unique_together = (('mi001', 'mi002', 'mi003'),)


class Docmj(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mj001 = models.CharField(db_column='MJ001', max_length=50)  # Field name made lowercase.
    mj002 = models.CharField(db_column='MJ002', max_length=10)  # Field name made lowercase.
    mj003 = models.CharField(db_column='MJ003', max_length=10)  # Field name made lowercase.
    mj004 = models.TextField(db_column='MJ004', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mj005 = models.CharField(db_column='MJ005', max_length=300, blank=True, null=True)  # Field name made lowercase.
    mj006 = models.CharField(db_column='MJ006', max_length=500, blank=True, null=True)  # Field name made lowercase.
    mj007 = models.CharField(db_column='MJ007', max_length=8, blank=True, null=True)  # Field name made lowercase.
    mj008 = models.CharField(db_column='MJ008', max_length=20, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DOCMJ'
        unique_together = (('mj001', 'mj002', 'mj003'),)

class Tecrequiremnt(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    specname = models.CharField(db_column='SpecName', max_length=50)  # Field name made lowercase.
    verno = models.CharField(db_column='VerNo', max_length=10)  # Field name made lowercase.
    funcitemno = models.CharField(db_column='FuncItemNo', max_length=10)  # Field name made lowercase.
    itemno = models.IntegerField(db_column='ItemNo')  # Field name made lowercase.
    ur = models.CharField(db_column='UR', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tr = models.CharField(db_column='TR', max_length=255, blank=True, null=True)  # Field name made lowercase.
    solution = models.TextField(db_column='Solution', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    rtype = models.CharField(db_column='RType', max_length=5, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID',primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TecRequiremnt'
        unique_together = (('specname', 'verno', 'funcitemno', 'itemno'),)

class VDocmhMi(models.Model):
    mh003 = models.CharField(db_column='MH003', max_length=500)  # Field name made lowercase.
    mh001 = models.CharField(db_column='MH001', primary_key=True, max_length=50)  # Field name made lowercase.
    mh004 = models.TextField(db_column='MH004', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=8, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_DOCMH_MI'

class Goalmanagement(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    goalid = models.IntegerField(db_column='GoalId')  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=15, blank=True, null=True)  # Field name made lowercase.
    period = models.CharField(db_column='Period', max_length=6, blank=True, null=True)  # Field name made lowercase.
    goaltype = models.CharField(db_column='GoalType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    month = models.CharField(db_column='Month', max_length=7, blank=True, null=True)  # Field name made lowercase.
    week = models.IntegerField(db_column='Week', blank=True, null=True)  # Field name made lowercase.
    goaldesc = models.TextField(db_column='GoalDesc', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    comment = models.TextField(db_column='Comment', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    sessions = models.CharField(db_column='Sessions', max_length=255, blank=True, null=True)  # Field name made lowercase.
    progress = models.IntegerField(db_column='Progress', blank=True, null=True)  # Field name made lowercase.
    priority = models.IntegerField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    allocateuser = models.FloatField(db_column='AllocateUser', blank=True, null=True)  # Field name made lowercase.
    recordid = models.CharField(db_column='RecordId', max_length=6, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    relationtasks = models.TextField(db_column='RelationTasks', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'GoalManagement'


class Tecfa(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=9, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    fa001 = models.BigAutoField(db_column='FA001', primary_key=True)  # Field name made lowercase.
    fa002 = models.CharField(db_column='FA002', max_length=11, blank=True, null=True)  # Field name made lowercase.
    fa003 = models.CharField(db_column='FA003', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fa004 = models.CharField(db_column='FA004', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fa005 = models.DateTimeField(db_column='FA005', blank=True, null=True)  # Field name made lowercase.
    fa006 = models.BigIntegerField(db_column='FA006', blank=True, null=True)  # Field name made lowercase.
    fa007 = models.BigIntegerField(db_column='FA007')  # Field name made lowercase.
    fa008 = models.CharField(db_column='FA008', max_length=1)  # Field name made lowercase.
    fa009 = models.CharField(db_column='FA009', max_length=1)  # Field name made lowercase.
    fa010 = models.CharField(db_column='FA010', max_length=11, blank=True, null=True)  # Field name made lowercase.
    fa011 = models.CharField(db_column='FA011', max_length=11, blank=True, null=True)  # Field name made lowercase.
    fa012 = models.IntegerField(db_column='FA012', blank=True, null=True)  # Field name made lowercase.
    fa013 = models.BigIntegerField(db_column='FA013', blank=True, null=True)  # Field name made lowercase.
    fa014 = models.TextField(db_column='FA014', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fa015 = models.CharField(db_column='FA015', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fa016 = models.IntegerField(db_column='FA016', blank=True, null=True)  # Field name made lowercase.
    fa017 = models.CharField(db_column='FA017', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fa018 = models.CharField(db_column='FA018', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fa019 = models.DateTimeField(db_column='FA019', blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    ma007 = models.CharField(db_column='MA007', max_length=11, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TECFA'        

class System(models.Model):
    revisedby = models.CharField(db_column='RevisedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    sysid = models.CharField(db_column='SysID', max_length=20)  # Field name made lowercase.
    sys = models.CharField(db_column='Sys', max_length=40)  # Field name made lowercase.
    parentid = models.CharField(db_column='ParentID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    sysremark = models.CharField(db_column='SysRemark', max_length=200, blank=True, null=True)  # Field name made lowercase.
    systype = models.CharField(db_column='SysType', max_length=10, blank=True, null=True)  # Field name made lowercase.
    sysicona = models.SmallIntegerField(db_column='SysIconA', blank=True, null=True)  # Field name made lowercase.
    sysiconb = models.SmallIntegerField(db_column='SysiconB', blank=True, null=True)  # Field name made lowercase.
    menuname = models.CharField(db_column='MenuName', max_length=80, blank=True, null=True)  # Field name made lowercase.
    flowchartid = models.CharField(db_column='FlowChartId', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sysname = models.CharField(db_column='SysName', max_length=20, blank=True, null=True)  # Field name made lowercase.
    sysorder = models.IntegerField(db_column='SysOrder', blank=True, null=True)  # Field name made lowercase.
    sqluser = models.CharField(db_column='SQLUser', max_length=20, blank=True, null=True)  # Field name made lowercase.
    sqlpassword = models.CharField(db_column='SQLPassword', max_length=20, blank=True, null=True)  # Field name made lowercase.
    syncflag = models.IntegerField(db_column='SyncFlag', blank=True, null=True)  # Field name made lowercase.
    syncdate = models.DateTimeField(db_column='SyncDate', blank=True, null=True)  # Field name made lowercase.
    serverip = models.CharField(db_column='ServerIP', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dbname = models.CharField(db_column='DBName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'System'



class Mettingmaster(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    id = models.CharField(db_column='Id', max_length=11)  # Field name made lowercase.
    topic = models.CharField(db_column='Topic', max_length=255, blank=True, null=True)  # Field name made lowercase.
    participants = models.TextField(db_column='Participants', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mustread = models.CharField(db_column='MustRead', max_length=50, blank=True, null=True)  # Field name made lowercase.
    discussprocess = models.TextField(db_column='DiscussProcess', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    summary = models.TextField(db_column='Summary', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    plandate = models.DateTimeField(db_column='PlanDate', blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MettingMaster'


class Mettingdetail(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    id = models.CharField(db_column='Id', max_length=11)  # Field name made lowercase.
    itemno = models.CharField(db_column='ItemNo', max_length=4)  # Field name made lowercase.
    subject = models.CharField(db_column='Subject', max_length=255, blank=True, null=True)  # Field name made lowercase.
    discussprocess = models.TextField(db_column='DiscussProcess', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    conclusion = models.TextField(db_column='Conclusion', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    arrange = models.TextField(db_column='Arrange', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MettingDetail'
        unique_together = (('id', 'itemno'),)


class Mettingdoc(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    id = models.CharField(db_column='Id', max_length=11)  # Field name made lowercase.
    itemno = models.CharField(db_column='ItemNo', max_length=4)  # Field name made lowercase.
    docname = models.CharField(db_column='DocName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mediatype = models.CharField(db_column='MediaType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    content = models.BinaryField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MettingDoc'
        unique_together = (('id', 'itemno'),)



class Document(models.Model):
    parentid = models.IntegerField(db_column='ParentID')  # Field name made lowercase.
    folderid = models.IntegerField(db_column='FolderID')  # Field name made lowercase.
    foldername = models.CharField(db_column='FolderName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    docid = models.CharField(db_column='DocId', max_length=50, blank=True, null=True)  # Field name made lowercase.
    docname = models.CharField(db_column='DocName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    docsize = models.CharField(db_column='DocSize', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mediatype = models.CharField(db_column='MediaType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    desp = models.CharField(db_column='Desp', max_length=255, blank=True, null=True)  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    revisedby = models.CharField(db_column='RevisedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=1, blank=True, null=True)  # Field name made lowercase.
    archiveflag = models.CharField(db_column='ArchiveFlag', max_length=1, blank=True, null=True)  # Field name made lowercase.
    obsolete = models.CharField(db_column='Obsolete', max_length=1, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Document'
        unique_together = (('folderid', 'parentid'),)


class Docdetail(models.Model):
    parentid = models.IntegerField(db_column='ParentID')  # Field name made lowercase.
    folderid = models.IntegerField(db_column='FolderID')  # Field name made lowercase.
    content = models.BinaryField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    revisedby = models.CharField(db_column='RevisedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DocDetail'
        unique_together = (('parentid', 'folderid'),)


class VDocument(models.Model):
    parentid = models.IntegerField(db_column='ParentID')  # Field name made lowercase.
    folderid = models.IntegerField(db_column='FolderID')  # Field name made lowercase.
    foldername = models.CharField(db_column='FolderName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    docid = models.CharField(db_column='DocId', max_length=50, blank=True, null=True)  # Field name made lowercase.
    docname = models.CharField(db_column='DocName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    obsolete = models.CharField(db_column='Obsolete', max_length=1, blank=True, null=True)  # Field name made lowercase.
    docsize = models.CharField(db_column='DocSize', max_length=32, blank=True, null=True)  # Field name made lowercase.
    mediatype = models.CharField(db_column='MediaType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    desp = models.CharField(db_column='Desp', max_length=255, blank=True, null=True)  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    revisedby = models.CharField(db_column='RevisedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=1, blank=True, null=True)  # Field name made lowercase.
    archiveflag = models.CharField(db_column='ArchiveFlag', max_length=1, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_Document'        



class Tasklist(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pid = models.CharField(db_column='Pid', max_length=16)  # Field name made lowercase.
    tid = models.FloatField(db_column='Tid')  # Field name made lowercase.
    desp = models.BinaryField(db_column='Desp', blank=True, null=True)  # Field name made lowercase.
    priority = models.FloatField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    planbdate = models.DateTimeField(db_column='PlanBDate', blank=True, null=True)  # Field name made lowercase.
    etime = models.FloatField(db_column='Etime', blank=True, null=True)  # Field name made lowercase.
    planedate = models.DateTimeField(db_column='PlanEDate', blank=True, null=True)  # Field name made lowercase.
    bdate = models.DateTimeField(db_column='Bdate', blank=True, null=True)  # Field name made lowercase.
    atime = models.FloatField(db_column='Atime', blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='Edate', blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    sdesp = models.CharField(db_column='SDesp', max_length=3000, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=20, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=256, blank=True, null=True)  # Field name made lowercase.
    revisedby = models.CharField(db_column='RevisedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    msgflag = models.CharField(db_column='MsgFlag', max_length=1, blank=True, null=True)  # Field name made lowercase.
    recerver = models.CharField(db_column='Recerver', max_length=50, blank=True, null=True)  # Field name made lowercase.
    flowchartno = models.CharField(db_column='FlowChartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    parent = models.CharField(db_column='Parent', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=50, blank=True, null=True)  # Field name made lowercase.
    class_field = models.IntegerField(db_column='Class', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    weight = models.FloatField(db_column='Weight', blank=True, null=True)  # Field name made lowercase.
    goaltype = models.CharField(db_column='GoalType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    capacity = models.IntegerField(db_column='Capacity', blank=True, null=True)  # Field name made lowercase.
    djcapacity = models.IntegerField(db_column='DJCapacity', blank=True, null=True)  # Field name made lowercase.
    cycleno = models.CharField(db_column='CycleNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    schrate = models.IntegerField(db_column='SchRate', blank=True, null=True)  # Field name made lowercase.
    estimate = models.IntegerField(db_column='Estimate', blank=True, null=True)  # Field name made lowercase.
    handletype = models.CharField(db_column='HandleType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tasklist'
        unique_together = (('pid', 'tid'),)        

class Ruledoc(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    recordid = models.CharField(db_column='RecordId', max_length=6)  # Field name made lowercase.
    itemno = models.IntegerField(db_column='ItemNo')  # Field name made lowercase.
    topic = models.CharField(db_column='Topic', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sdescription = models.TextField(db_column='SDescription', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    content = models.TextField(db_column='Content', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    sortno = models.IntegerField(db_column='SortNo', blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RuleDoc'
        unique_together = (('recordid', 'itemno'),)



class VTaskMeetingUnd(models.Model):
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pid = models.CharField(db_column='Pid', max_length=16)  # Field name made lowercase.
    tid = models.FloatField(db_column='Tid')  # Field name made lowercase.
    taskid = models.FloatField(db_column='TaskID')  # Field name made lowercase.
    task = models.CharField(db_column='Task', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=25, blank=True, null=True)  # Field name made lowercase.
    planbdate = models.DateTimeField(db_column='PlanBDate', blank=True, null=True)  # Field name made lowercase.
    etime = models.FloatField(db_column='Etime', blank=True, null=True)  # Field name made lowercase.
    planedate = models.DateTimeField(db_column='PlanEDate', blank=True, null=True)  # Field name made lowercase.
    atime = models.FloatField(blank=True, null=True)
    bdate = models.DateTimeField(db_column='BDate', blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='EDate', blank=True, null=True)  # Field name made lowercase.
    priority = models.IntegerField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=255, blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    revisedby = models.CharField(db_column='RevisedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    tasktype = models.IntegerField(db_column='TaskType', blank=True, null=True)  # Field name made lowercase.
    subtasktype = models.IntegerField(db_column='SubTaskType', blank=True, null=True)  # Field name made lowercase.
    diff = models.IntegerField(db_column='Diff', blank=True, null=True)  # Field name made lowercase.
    taskoption = models.IntegerField(db_column='Taskoption', blank=True, null=True)  # Field name made lowercase.
    relationid = models.CharField(db_column='relationID', max_length=200, blank=True, null=True)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
    docpath = models.CharField(db_column='DocPath', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emaildesp = models.TextField(db_column='EmailDesp', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf51 = models.CharField(db_column='UDF51', max_length=10, blank=True, null=True)  # Field name made lowercase.
    udf52 = models.DecimalField(db_column='UDF52', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    smsreceiver = models.CharField(db_column='SMSReceiver', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dispose = models.CharField(db_column='Dispose', max_length=2, blank=True, null=True)  # Field name made lowercase.
    editionid = models.CharField(db_column='EditionID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    oldprogress = models.CharField(db_column='OldProgress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    delayday = models.IntegerField(db_column='DelayDay', blank=True, null=True)  # Field name made lowercase.
    companyid = models.CharField(db_column='CompanyID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    subprojectid = models.CharField(db_column='SubProjectID', max_length=6, blank=True, null=True)  # Field name made lowercase.
    class_field = models.IntegerField(db_column='Class', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    sendctlemail = models.IntegerField(db_column='SendCTLEmail', blank=True, null=True)  # Field name made lowercase.
    generateddoc = models.CharField(db_column='GeneratedDoc', max_length=300, blank=True, null=True)  # Field name made lowercase.
    relationgoalid = models.CharField(db_column='RelationGoalId', max_length=200, blank=True, null=True)  # Field name made lowercase.
    escore = models.FloatField(db_column='EScore', blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    totalscore = models.FloatField(db_column='TotalScore', blank=True, null=True)  # Field name made lowercase.
    setting = models.CharField(db_column='Setting', max_length=1, blank=True, null=True)  # Field name made lowercase.
    questionno = models.CharField(db_column='QuestionNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    req_date = models.DateTimeField(db_column='Req_Date', blank=True, null=True)  # Field name made lowercase.
    reply_taskno = models.CharField(db_column='Reply_TaskNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    isschedule = models.CharField(db_column='IsSchedule', max_length=1, blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=500, blank=True, null=True)  # Field name made lowercase.
    environmentid = models.CharField(db_column='EnvironmentID', max_length=6, blank=True, null=True)  # Field name made lowercase.
    categoryid = models.FloatField(db_column='CategoryID', blank=True, null=True)  # Field name made lowercase.
    rank = models.IntegerField(db_column='Rank', blank=True, null=True)  # Field name made lowercase.
    correctness = models.CharField(db_column='Correctness', max_length=1, blank=True, null=True)  # Field name made lowercase.
    appraisalid = models.CharField(db_column='AppraisalId', max_length=20, blank=True, null=True)  # Field name made lowercase.
    progressprocent = models.IntegerField(db_column='ProgressProcent', blank=True, null=True)  # Field name made lowercase.
    classify = models.CharField(db_column='Classify', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flowchartno = models.CharField(db_column='FlowChartNo', max_length=200, blank=True, null=True)  # Field name made lowercase.
    spday = models.FloatField(db_column='SPDay', blank=True, null=True)  # Field name made lowercase.
    spaday = models.FloatField(db_column='SPADay', blank=True, null=True)  # Field name made lowercase.
    saday = models.FloatField(db_column='SADay', blank=True, null=True)  # Field name made lowercase.
    manday = models.IntegerField(db_column='ManDay', blank=True, null=True)  # Field name made lowercase.
    difficulty = models.CharField(db_column='Difficulty', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf06 = models.CharField(db_column='UDF06', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf07 = models.DateTimeField(db_column='UDF07', blank=True, null=True)  # Field name made lowercase.
    udf08 = models.CharField(db_column='UDF08', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf09 = models.CharField(db_column='UDF09', max_length=20, blank=True, null=True)  # Field name made lowercase.
    udf10 = models.CharField(db_column='UDF10', max_length=20, blank=True, null=True)  # Field name made lowercase.
    calpriority = models.IntegerField(db_column='CalPriority', blank=True, null=True)  # Field name made lowercase.
    schpriority = models.FloatField(db_column='SchPriority', blank=True, null=True)  # Field name made lowercase.
    schedulestate = models.CharField(db_column='ScheduleState', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dayjob = models.CharField(db_column='DayJob', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mastno = models.CharField(db_column='MastNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cycletask = models.CharField(db_column='CycleTask', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf11 = models.CharField(db_column='UDF11', max_length=20, blank=True, null=True)  # Field name made lowercase.
    reference = models.CharField(db_column='Reference', max_length=30, blank=True, null=True)  # Field name made lowercase.
    hoperation = models.CharField(db_column='HOperation', max_length=1, blank=True, null=True)  # Field name made lowercase.
    charge = models.CharField(db_column='Charge', max_length=1, blank=True, null=True)  # Field name made lowercase.
    special = models.CharField(db_column='Special', max_length=1, blank=True, null=True)  # Field name made lowercase.
    process = models.CharField(db_column='Process', max_length=1, blank=True, null=True)  # Field name made lowercase.
    requestdate = models.DateTimeField(db_column='RequestDate', blank=True, null=True)  # Field name made lowercase.
    schprioritysp = models.FloatField(db_column='SchPrioritySP', blank=True, null=True)  # Field name made lowercase.
    r_flag = models.BooleanField(db_column='R_Flag', blank=True, null=True)  # Field name made lowercase.
    taskcategory = models.CharField(db_column='TaskCategory', max_length=5, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    planbdates = models.CharField(db_column='PlanBDateS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    planedates = models.CharField(db_column='PlanEDateS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    bdates = models.CharField(db_column='BDateS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    edates = models.CharField(db_column='EDateS', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_Task_Meeting_und'


class VTaskMeeting(models.Model):
    meetingid = models.CharField(db_column='Meetingid', max_length=500, blank=True, null=True)  # Field name made lowercase.
    parent_pid = models.CharField(db_column='Parent_Pid', max_length=16)  # Field name made lowercase.
    parent_tid = models.FloatField(db_column='Parent_Tid')  # Field name made lowercase.
    parent_taskid = models.FloatField(db_column='Parent_TaskID')  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pid = models.CharField(db_column='Pid', max_length=16)  # Field name made lowercase.
    tid = models.FloatField(db_column='Tid')  # Field name made lowercase.
    taskid = models.FloatField(db_column='TaskID')  # Field name made lowercase.
    task = models.CharField(db_column='Task', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=25, blank=True, null=True)  # Field name made lowercase.
    planbdate = models.DateTimeField(db_column='PlanBDate', blank=True, null=True)  # Field name made lowercase.
    etime = models.FloatField(db_column='Etime', blank=True, null=True)  # Field name made lowercase.
    planedate = models.DateTimeField(db_column='PlanEDate', blank=True, null=True)  # Field name made lowercase.
    atime = models.FloatField(blank=True, null=True)
    bdate = models.DateTimeField(db_column='BDate', blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='EDate', blank=True, null=True)  # Field name made lowercase.
    priority = models.IntegerField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=255, blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    revisedby = models.CharField(db_column='RevisedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    tasktype = models.IntegerField(db_column='TaskType', blank=True, null=True)  # Field name made lowercase.
    subtasktype = models.IntegerField(db_column='SubTaskType', blank=True, null=True)  # Field name made lowercase.
    diff = models.IntegerField(db_column='Diff', blank=True, null=True)  # Field name made lowercase.
    taskoption = models.IntegerField(db_column='Taskoption', blank=True, null=True)  # Field name made lowercase.
    relationid = models.CharField(db_column='relationID', max_length=200, blank=True, null=True)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
    docpath = models.CharField(db_column='DocPath', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emaildesp = models.TextField(db_column='EmailDesp', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf51 = models.CharField(db_column='UDF51', max_length=10, blank=True, null=True)  # Field name made lowercase.
    udf52 = models.DecimalField(db_column='UDF52', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    smsreceiver = models.CharField(db_column='SMSReceiver', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dispose = models.CharField(db_column='Dispose', max_length=2, blank=True, null=True)  # Field name made lowercase.
    editionid = models.CharField(db_column='EditionID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    oldprogress = models.CharField(db_column='OldProgress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    delayday = models.IntegerField(db_column='DelayDay', blank=True, null=True)  # Field name made lowercase.
    companyid = models.CharField(db_column='CompanyID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    subprojectid = models.CharField(db_column='SubProjectID', max_length=6, blank=True, null=True)  # Field name made lowercase.
    class_field = models.IntegerField(db_column='Class', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    sendctlemail = models.IntegerField(db_column='SendCTLEmail', blank=True, null=True)  # Field name made lowercase.
    generateddoc = models.CharField(db_column='GeneratedDoc', max_length=300, blank=True, null=True)  # Field name made lowercase.
    relationgoalid = models.CharField(db_column='RelationGoalId', max_length=200, blank=True, null=True)  # Field name made lowercase.
    escore = models.FloatField(db_column='EScore', blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    totalscore = models.FloatField(db_column='TotalScore', blank=True, null=True)  # Field name made lowercase.
    setting = models.CharField(db_column='Setting', max_length=1, blank=True, null=True)  # Field name made lowercase.
    questionno = models.CharField(db_column='QuestionNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    req_date = models.DateTimeField(db_column='Req_Date', blank=True, null=True)  # Field name made lowercase.
    reply_taskno = models.CharField(db_column='Reply_TaskNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    isschedule = models.CharField(db_column='IsSchedule', max_length=1, blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=500, blank=True, null=True)  # Field name made lowercase.
    environmentid = models.CharField(db_column='EnvironmentID', max_length=6, blank=True, null=True)  # Field name made lowercase.
    categoryid = models.FloatField(db_column='CategoryID', blank=True, null=True)  # Field name made lowercase.
    rank = models.IntegerField(db_column='Rank', blank=True, null=True)  # Field name made lowercase.
    correctness = models.CharField(db_column='Correctness', max_length=1, blank=True, null=True)  # Field name made lowercase.
    appraisalid = models.CharField(db_column='AppraisalId', max_length=20, blank=True, null=True)  # Field name made lowercase.
    progressprocent = models.IntegerField(db_column='ProgressProcent', blank=True, null=True)  # Field name made lowercase.
    classify = models.CharField(db_column='Classify', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flowchartno = models.CharField(db_column='FlowChartNo', max_length=200, blank=True, null=True)  # Field name made lowercase.
    spday = models.FloatField(db_column='SPDay', blank=True, null=True)  # Field name made lowercase.
    spaday = models.FloatField(db_column='SPADay', blank=True, null=True)  # Field name made lowercase.
    saday = models.FloatField(db_column='SADay', blank=True, null=True)  # Field name made lowercase.
    manday = models.IntegerField(db_column='ManDay', blank=True, null=True)  # Field name made lowercase.
    difficulty = models.CharField(db_column='Difficulty', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf06 = models.CharField(db_column='UDF06', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf07 = models.DateTimeField(db_column='UDF07', blank=True, null=True)  # Field name made lowercase.
    udf08 = models.CharField(db_column='UDF08', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf09 = models.CharField(db_column='UDF09', max_length=20, blank=True, null=True)  # Field name made lowercase.
    udf10 = models.CharField(db_column='UDF10', max_length=20, blank=True, null=True)  # Field name made lowercase.
    calpriority = models.IntegerField(db_column='CalPriority', blank=True, null=True)  # Field name made lowercase.
    schpriority = models.FloatField(db_column='SchPriority', blank=True, null=True)  # Field name made lowercase.
    schedulestate = models.CharField(db_column='ScheduleState', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dayjob = models.CharField(db_column='DayJob', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mastno = models.CharField(db_column='MastNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cycletask = models.CharField(db_column='CycleTask', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf11 = models.CharField(db_column='UDF11', max_length=20, blank=True, null=True)  # Field name made lowercase.
    reference = models.CharField(db_column='Reference', max_length=30, blank=True, null=True)  # Field name made lowercase.
    hoperation = models.CharField(db_column='HOperation', max_length=1, blank=True, null=True)  # Field name made lowercase.
    charge = models.CharField(db_column='Charge', max_length=1, blank=True, null=True)  # Field name made lowercase.
    special = models.CharField(db_column='Special', max_length=1, blank=True, null=True)  # Field name made lowercase.
    process = models.CharField(db_column='Process', max_length=1, blank=True, null=True)  # Field name made lowercase.
    requestdate = models.DateTimeField(db_column='RequestDate', blank=True, null=True)  # Field name made lowercase.
    schprioritysp = models.FloatField(db_column='SchPrioritySP', blank=True, null=True)  # Field name made lowercase.
    r_flag = models.BooleanField(db_column='R_Flag', blank=True, null=True)  # Field name made lowercase.
    taskcategory = models.CharField(db_column='TaskCategory', max_length=5, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.IntegerField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    planbdates = models.CharField(db_column='PlanBDateS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    planedates = models.CharField(db_column='PlanEDateS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    bdates = models.CharField(db_column='BDateS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    edates = models.CharField(db_column='EDateS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_Task_Meeting'

class Goalmanagementdetail(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    goalid = models.IntegerField(db_column='GoalId')  # Field name made lowercase.
    itemno = models.IntegerField(db_column='ItemNo')  # Field name made lowercase.
    goaldesc = models.TextField(db_column='GoalDesc', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    comment = models.TextField(db_column='Comment', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    relationtasks = models.TextField(db_column='RelationTasks', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GoalManagementDetail'
        unique_together = (('goalid', 'itemno'),)

class VGoalmanagementdetail(models.Model):
    contact = models.CharField(db_column='Contact', max_length=15, blank=True, null=True)  # Field name made lowercase.
    period = models.CharField(db_column='Period', max_length=6, blank=True, null=True)  # Field name made lowercase.
    goaltype = models.CharField(db_column='GoalType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    month = models.CharField(db_column='Month', max_length=7, blank=True, null=True)  # Field name made lowercase.
    week = models.IntegerField(db_column='Week', blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    goalid = models.IntegerField(db_column='GoalId')  # Field name made lowercase.
    itemno = models.IntegerField(db_column='ItemNo')  # Field name made lowercase.
    goaldesc = models.TextField(db_column='GoalDesc', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    comment = models.TextField(db_column='Comment', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    relationtasks = models.TextField(db_column='RelationTasks', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    inc_id = models.IntegerField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_GoalManagementDetail'

class VTasklistSub(models.Model):
    recordid = models.CharField(db_column='RecordId', max_length=6, blank=True, null=True)  # Field name made lowercase.
    sessionid = models.CharField(db_column='SessionId', max_length=37, blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pid = models.CharField(db_column='Pid', max_length=16)  # Field name made lowercase.
    tid = models.FloatField(db_column='Tid')  # Field name made lowercase.
    desp = models.BinaryField(db_column='Desp', blank=True, null=True)  # Field name made lowercase.
    priority = models.FloatField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    planbdate = models.DateTimeField(db_column='PlanBDate', blank=True, null=True)  # Field name made lowercase.
    etime = models.FloatField(db_column='Etime', blank=True, null=True)  # Field name made lowercase.
    planedate = models.DateTimeField(db_column='PlanEDate', blank=True, null=True)  # Field name made lowercase.
    bdate = models.DateTimeField(db_column='Bdate', blank=True, null=True)  # Field name made lowercase.
    atime = models.FloatField(db_column='Atime', blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='Edate', blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    sdesp = models.CharField(db_column='SDesp', max_length=3000, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=20, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=256, blank=True, null=True)  # Field name made lowercase.
    revisedby = models.CharField(db_column='RevisedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    msgflag = models.CharField(db_column='MsgFlag', max_length=1, blank=True, null=True)  # Field name made lowercase.
    recerver = models.CharField(db_column='Recerver', max_length=50, blank=True, null=True)  # Field name made lowercase.
    flowchartno = models.CharField(db_column='FlowChartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    parent = models.CharField(db_column='Parent', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=50, blank=True, null=True)  # Field name made lowercase.
    class_field = models.IntegerField(db_column='Class', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    weight = models.FloatField(db_column='Weight', blank=True, null=True)  # Field name made lowercase.
    goaltype = models.CharField(db_column='GoalType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    capacity = models.IntegerField(db_column='Capacity', blank=True, null=True)  # Field name made lowercase.
    djcapacity = models.IntegerField(db_column='DJCapacity', blank=True, null=True)  # Field name made lowercase.
    cycleno = models.CharField(db_column='CycleNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    schrate = models.IntegerField(db_column='SchRate', blank=True, null=True)  # Field name made lowercase.
    estimate = models.IntegerField(db_column='Estimate', blank=True, null=True)  # Field name made lowercase.
    handletype = models.CharField(db_column='HandleType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.IntegerField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    signify = models.IntegerField()
    request = models.IntegerField()
    completed = models.IntegerField()
    problems = models.IntegerField()
    earliesunfinish = models.DateTimeField(db_column='earliesUnFinish', blank=True, null=True)  # Field name made lowercase.
    lastunfinish = models.DateTimeField(db_column='lastUnFinish', blank=True, null=True)  # Field name made lowercase.
    score = models.IntegerField()
    minplanbdate = models.DateTimeField(db_column='MinPlanBDate', blank=True, null=True)  # Field name made lowercase.
    maxplanedate = models.DateTimeField(db_column='MaxPlanEDate', blank=True, null=True)  # Field name made lowercase.
    maxcreatedate = models.DateTimeField(db_column='MaxCreateDate', blank=True, null=True)  # Field name made lowercase.
    taskqty = models.IntegerField(db_column='TaskQty', blank=True, null=True)  # Field name made lowercase.
    pschedule = models.IntegerField(db_column='PSchedule')  # Field name made lowercase.
    aschedule = models.IntegerField(db_column='ASchedule')  # Field name made lowercase.
    outstandday = models.IntegerField(db_column='OutstandDay', blank=True, null=True)  # Field name made lowercase.
    outstandqty = models.IntegerField(db_column='OutstandQty', blank=True, null=True)  # Field name made lowercase.
    overtaskqty = models.FloatField(db_column='OverTaskQty', blank=True, null=True)  # Field name made lowercase.
    projectscore = models.IntegerField(db_column='ProjectScore', blank=True, null=True)  # Field name made lowercase.
    quarterly = models.IntegerField(db_column='Quarterly', blank=True, null=True)  # Field name made lowercase.
    subpropriority = models.FloatField(db_column='SubProPriority', blank=True, null=True)  # Field name made lowercase.
    subplanbdate = models.DateTimeField(db_column='SubPlanBDate', blank=True, null=True)  # Field name made lowercase.
    allcontact = models.CharField(db_column='AllContact', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_TaskList_Sub'


class Testingnotes(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    sysid = models.CharField(db_column='SysID', max_length=20)  # Field name made lowercase.
    frmno = models.CharField(db_column='FrmNo', max_length=50)  # Field name made lowercase.
    itemno = models.CharField(db_column='ItemNo', max_length=10)  # Field name made lowercase.
    frmname = models.CharField(db_column='FrmName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    funcitemno = models.CharField(db_column='FuncItemNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    funcdesc = models.TextField(db_column='FuncDesc', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    functype = models.CharField(db_column='FuncType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=1, blank=True, null=True)  # Field name made lowercase.
    testdata = models.TextField(db_column='TestData', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    testresult = models.TextField(db_column='TestResult', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    question = models.TextField(db_column='Question', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TestingNotes'
        unique_together = (('sysid', 'frmno', 'itemno'),)

class Tasktype(models.Model):
    tasktype = models.CharField(db_column='TaskType', max_length=30, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=100, blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TaskType'

class TasktypeSl(models.Model):
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    tasktype = models.CharField(db_column='TaskType', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dtasktype = models.CharField(db_column='DTaskType', max_length=30, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=100, blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    oldscore = models.FloatField(db_column='OldScore', blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TaskType_SL'

class TasktypeSlHistory(models.Model):
    tasktype = models.CharField(db_column='TaskType', max_length=30)  # Field name made lowercase.
    verno = models.IntegerField(db_column='VerNo')  # Field name made lowercase.
    dtasktype = models.CharField(db_column='DTaskType', max_length=30, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=100, blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    oldscore = models.FloatField(db_column='OldScore', blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TaskType_SL_History'
        unique_together = (('tasktype', 'verno'),)

class Userbonusparam(models.Model):
    username = models.CharField(db_column='UserName', max_length=15, primary_key=True)  # Field name made lowercase.
    budgetallowance = models.TextField(db_column='BudgetAllowance', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    managementratio = models.TextField(db_column='ManagementRatio', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    performanaceratio = models.TextField(db_column='PerformanaceRatio', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ratioofm = models.TextField(db_column='RatioOFM', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ratioofp = models.TextField(db_column='RatioOFP', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ratioofs = models.TextField(db_column='RatioOFS', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    salary = models.TextField(db_column='Salary', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    unitpirce = models.TextField(db_column='UnitPrice', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_UserBonusParam'

class VUsers(models.Model):
    username = models.CharField(db_column='UserName',primary_key=True, max_length=15)  # Field name made lowercase.
    workno = models.CharField(db_column='Workno', max_length=10, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='PassWord', max_length=20, blank=True, null=True)  # Field name made lowercase.
    level = models.IntegerField(db_column='Level', blank=True, null=True)  # Field name made lowercase.
    groupname = models.CharField(db_column='GroupName', max_length=20, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=100, blank=True, null=True)  # Field name made lowercase.
    telno = models.CharField(db_column='telNo', max_length=15, blank=True, null=True)  # Field name made lowercase.
    lanflag = models.CharField(db_column='lanFlag', max_length=10, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(blank=True, null=True)
    shorttelno = models.CharField(db_column='shortTelNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    receiveflag = models.CharField(db_column='receiveFlag', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dept = models.CharField(db_column='Dept', max_length=30, blank=True, null=True)  # Field name made lowercase.
    companyid = models.CharField(db_column='CompanyID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    goalflag = models.CharField(db_column='GoalFlag', max_length=1, blank=True, null=True)  # Field name made lowercase.
    issuper = models.BooleanField(db_column='IsSuper', blank=True, null=True)  # Field name made lowercase.
    isremind = models.BooleanField(db_column='IsRemind', blank=True, null=True)  # Field name made lowercase.
    salesremind = models.BooleanField(db_column='SalesRemind', blank=True, null=True)  # Field name made lowercase.
    isautologin = models.BooleanField(db_column='IsAutoLogin', blank=True, null=True)  # Field name made lowercase.
    inneremail = models.CharField(db_column='InnerEmail', max_length=50, blank=True, null=True)  # Field name made lowercase.
    outeremail = models.CharField(db_column='OuterEmail', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_Users'

class VTasktypetreelist(models.Model):
    tasktype = models.CharField(db_column='TaskType',primary_key=True, max_length=23)  # Field name made lowercase.
    realtasktype = models.CharField(db_column='RealTaskType', max_length=23, blank=True, null=True)  # Field name made lowercase.
    indexno = models.CharField(db_column='IndexNo', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    parent = models.CharField(db_column='Parent', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    displaytype = models.IntegerField(db_column='DisplayType', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=100, blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    scorechange = models.CharField(db_column='ScoreChange', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_TaskTypeTreeList'           
    
class Technicaluserecord(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    taskno = models.CharField(db_column='TaskNo', max_length=53, blank=True, null=True)  # Field name made lowercase.
    inputdate = models.DateField(db_column='InputDate', blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=15, blank=True, null=True)  # Field name made lowercase.
    technicid = models.CharField(db_column='TechnicId', max_length=50, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=1, blank=True, null=True)  # Field name made lowercase.
    issue = models.CharField(db_column='Issue', max_length=200, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TechnicalUseRecord'

class VTaskArrage(models.Model):
    arrangedate = models.DateTimeField(db_column='ArrangeDate', blank=True, null=True)  # Field name made lowercase.
    arrageprogress = models.CharField(db_column='ArrageProgress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    taskno = models.CharField(db_column='TaskNo', max_length=42, primary_key=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pid = models.CharField(db_column='Pid', max_length=16)  # Field name made lowercase.
    tid = models.FloatField(db_column='Tid')  # Field name made lowercase.
    taskid = models.FloatField(db_column='TaskID')  # Field name made lowercase.
    task = models.CharField(db_column='Task', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=25, blank=True, null=True)  # Field name made lowercase.
    planbdate = models.DateTimeField(db_column='PlanBDate', blank=True, null=True)  # Field name made lowercase.
    etime = models.FloatField(db_column='Etime', blank=True, null=True)  # Field name made lowercase.
    planedate = models.DateTimeField(db_column='PlanEDate', blank=True, null=True)  # Field name made lowercase.
    atime = models.FloatField(blank=True, null=True)
    bdate = models.DateTimeField(db_column='BDate', blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='EDate', blank=True, null=True)  # Field name made lowercase.
    priority = models.IntegerField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=255, blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    revisedby = models.CharField(db_column='RevisedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    tasktype = models.IntegerField(db_column='TaskType', blank=True, null=True)  # Field name made lowercase.
    subtasktype = models.IntegerField(db_column='SubTaskType', blank=True, null=True)  # Field name made lowercase.
    diff = models.IntegerField(db_column='Diff', blank=True, null=True)  # Field name made lowercase.
    taskoption = models.IntegerField(db_column='Taskoption', blank=True, null=True)  # Field name made lowercase.
    relationid = models.CharField(db_column='relationID', max_length=200, blank=True, null=True)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
    docpath = models.CharField(db_column='DocPath', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emaildesp = models.TextField(db_column='EmailDesp', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf51 = models.CharField(db_column='UDF51', max_length=10, blank=True, null=True)  # Field name made lowercase.
    udf52 = models.DecimalField(db_column='UDF52', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    smsreceiver = models.CharField(db_column='SMSReceiver', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dispose = models.CharField(db_column='Dispose', max_length=2, blank=True, null=True)  # Field name made lowercase.
    editionid = models.CharField(db_column='EditionID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    oldprogress = models.CharField(db_column='OldProgress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    delayday = models.IntegerField(db_column='DelayDay', blank=True, null=True)  # Field name made lowercase.
    companyid = models.CharField(db_column='CompanyID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    subprojectid = models.CharField(db_column='SubProjectID', max_length=6, blank=True, null=True)  # Field name made lowercase.
    class_field = models.IntegerField(db_column='Class', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    sendctlemail = models.IntegerField(db_column='SendCTLEmail', blank=True, null=True)  # Field name made lowercase.
    generateddoc = models.CharField(db_column='GeneratedDoc', max_length=300, blank=True, null=True)  # Field name made lowercase.
    relationgoalid = models.CharField(db_column='RelationGoalId', max_length=200, blank=True, null=True)  # Field name made lowercase.
    escore = models.FloatField(db_column='EScore', blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    totalscore = models.FloatField(db_column='TotalScore', blank=True, null=True)  # Field name made lowercase.
    setting = models.CharField(db_column='Setting', max_length=1, blank=True, null=True)  # Field name made lowercase.
    questionno = models.CharField(db_column='QuestionNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    req_date = models.DateTimeField(db_column='Req_Date', blank=True, null=True)  # Field name made lowercase.
    reply_taskno = models.CharField(db_column='Reply_TaskNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    isschedule = models.CharField(db_column='IsSchedule', max_length=1, blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=500, blank=True, null=True)  # Field name made lowercase.
    environmentid = models.CharField(db_column='EnvironmentID', max_length=6, blank=True, null=True)  # Field name made lowercase.
    categoryid = models.FloatField(db_column='CategoryID', blank=True, null=True)  # Field name made lowercase.
    rank = models.IntegerField(db_column='Rank', blank=True, null=True)  # Field name made lowercase.
    correctness = models.CharField(db_column='Correctness', max_length=1, blank=True, null=True)  # Field name made lowercase.
    appraisalid = models.CharField(db_column='AppraisalId', max_length=20, blank=True, null=True)  # Field name made lowercase.
    progressprocent = models.IntegerField(db_column='ProgressProcent', blank=True, null=True)  # Field name made lowercase.
    classify = models.CharField(db_column='Classify', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flowchartno = models.CharField(db_column='FlowChartNo', max_length=200, blank=True, null=True)  # Field name made lowercase.
    spday = models.FloatField(db_column='SPDay', blank=True, null=True)  # Field name made lowercase.
    spaday = models.FloatField(db_column='SPADay', blank=True, null=True)  # Field name made lowercase.
    saday = models.FloatField(db_column='SADay', blank=True, null=True)  # Field name made lowercase.
    manday = models.IntegerField(db_column='ManDay', blank=True, null=True)  # Field name made lowercase.
    difficulty = models.CharField(db_column='Difficulty', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf06 = models.CharField(db_column='UDF06', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf07 = models.DateTimeField(db_column='UDF07', blank=True, null=True)  # Field name made lowercase.
    udf08 = models.CharField(db_column='UDF08', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf09 = models.CharField(db_column='UDF09', max_length=20, blank=True, null=True)  # Field name made lowercase.
    udf10 = models.CharField(db_column='UDF10', max_length=20, blank=True, null=True)  # Field name made lowercase.
    calpriority = models.IntegerField(db_column='CalPriority', blank=True, null=True)  # Field name made lowercase.
    schpriority = models.FloatField(db_column='SchPriority', blank=True, null=True)  # Field name made lowercase.
    schedulestate = models.CharField(db_column='ScheduleState', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dayjob = models.CharField(db_column='DayJob', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mastno = models.CharField(db_column='MastNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cycletask = models.CharField(db_column='CycleTask', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf11 = models.CharField(db_column='UDF11', max_length=20, blank=True, null=True)  # Field name made lowercase.
    reference = models.CharField(db_column='Reference', max_length=30, blank=True, null=True)  # Field name made lowercase.
    hoperation = models.CharField(db_column='HOperation', max_length=1, blank=True, null=True)  # Field name made lowercase.
    charge = models.CharField(db_column='Charge', max_length=1, blank=True, null=True)  # Field name made lowercase.
    special = models.CharField(db_column='Special', max_length=1, blank=True, null=True)  # Field name made lowercase.
    process = models.CharField(db_column='Process', max_length=1, blank=True, null=True)  # Field name made lowercase.
    requestdate = models.DateTimeField(db_column='RequestDate', blank=True, null=True)  # Field name made lowercase.
    schprioritysp = models.FloatField(db_column='SchPrioritySP', blank=True, null=True)  # Field name made lowercase.
    r_flag = models.BooleanField(db_column='R_Flag', blank=True, null=True)  # Field name made lowercase.
    taskcategory = models.CharField(db_column='TaskCategory', max_length=5, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.IntegerField(db_column='INC_ID')  # Field name made lowercase.
    name = models.CharField(max_length=35, blank=True, null=True)
    number = models.IntegerField()
    type = models.CharField(max_length=3)
    low = models.IntegerField(blank=True, null=True)
    high = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_Task_Arrage'

class Deductionitem(models.Model):
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=200, blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(db_column='Score', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DeductionItem'


class Userdeduction(models.Model):
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=20, blank=True, null=True)  # Field name made lowercase.
    deductiondate = models.DateField(db_column='DeductionDate', blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=200, blank=True, null=True)  # Field name made lowercase.
    penaltyid = models.FloatField(db_column='PenaltyID', blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=30, blank=True, null=True)  # Field name made lowercase.
    position = models.CharField(db_column='Position', max_length=30, blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'Bonus_Debit'

class Bonuscredit(models.Model):
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=20, blank=True, null=True)  # Field name made lowercase.
    creditdate = models.DateField(db_column='CreditDate', blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=200, blank=True, null=True)  # Field name made lowercase.
    rewardid = models.FloatField(db_column='RewardID', blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=30, blank=True, null=True)  # Field name made lowercase.
    position = models.CharField(db_column='Position', max_length=30, blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'Bonus_Credit'
        
class Tpparam(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pname = models.CharField(db_column='PName', max_length=50)  # Field name made lowercase.
    pdesc = models.CharField(db_column='PDesc', max_length=200, blank=True, null=True)  # Field name made lowercase.
    ptype = models.CharField(db_column='PType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pvalue = models.CharField(db_column='PValue', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pservice = models.CharField(db_column='PService', max_length=50, blank=True, null=True)  # Field name made lowercase.
    psql = models.TextField(db_column='PSQL', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TpParam'        


class Tecmf(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mf001 = models.CharField(db_column='MF001', max_length=60)  # Field name made lowercase.
    mf002 = models.CharField(db_column='MF002', max_length=60)  # Field name made lowercase.
    mf003 = models.CharField(db_column='MF003', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mf004 = models.CharField(db_column='MF004', max_length=200, blank=True, null=True)  # Field name made lowercase.
    mf005 = models.IntegerField(db_column='MF005', blank=True, null=True)  # Field name made lowercase.
    mf006 = models.CharField(db_column='MF006', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mf007 = models.CharField(db_column='MF007', max_length=60, blank=True, null=True)  # Field name made lowercase.
    mf008 = models.CharField(db_column='MF008', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TECMF'

class VTecmf(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mf001 = models.CharField(db_column='MF001', max_length=60)  # Field name made lowercase.
    mf002 = models.CharField(db_column='MF002', max_length=60)  # Field name made lowercase.
    mf003 = models.CharField(db_column='MF003', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mf004 = models.CharField(db_column='MF004', max_length=200, blank=True, null=True)  # Field name made lowercase.
    mf005 = models.IntegerField(db_column='MF005', blank=True, null=True)  # Field name made lowercase.
    mf006 = models.CharField(db_column='MF006', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mf007 = models.CharField(db_column='MF007', max_length=60, blank=True, null=True)  # Field name made lowercase.
    mf008 = models.CharField(db_column='MF008', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID',primary_key=True)  # Field name made lowercase.
    parentdsc = models.CharField(db_column='ParentDsc', max_length=60, blank=True, null=True)  # Field name made lowercase.
    categorydsc = models.CharField(db_column='CategoryDsc', max_length=60, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_TECMF'        

class VTecme(models.Model):
    mb001c = models.CharField(db_column='MB001C', max_length=11, blank=True, null=True)  # Field name made lowercase.
    mb015c = models.CharField(db_column='MB015C', max_length=11, blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mb001 = models.CharField(db_column='MB001', max_length=11, blank=True, null=True)  # Field name made lowercase.
    mb002 = models.CharField(db_column='MB002', max_length=4, blank=True, null=True)  # Field name made lowercase.
    mb003 = models.CharField(db_column='MB003', max_length=11, blank=True, null=True)  # Field name made lowercase.
    mb004 = models.CharField(db_column='MB004', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb005 = models.CharField(db_column='MB005', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mb006 = models.CharField(db_column='MB006', max_length=8, blank=True, null=True)  # Field name made lowercase.
    mb007 = models.TextField(db_column='MB007', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb008 = models.TextField(db_column='MB008', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb009 = models.TextField(db_column='MB009', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb010 = models.TextField(db_column='MB010', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb011 = models.TextField(db_column='MB011', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb012 = models.TextField(db_column='MB012', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb013 = models.CharField(db_column='MB013', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb015 = models.CharField(db_column='MB015', max_length=11, blank=True, null=True)  # Field name made lowercase.
    mb016 = models.CharField(db_column='MB016', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb017 = models.TextField(db_column='MB017', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb018 = models.CharField(db_column='MB018', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb019 = models.CharField(db_column='MB019', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb020 = models.CharField(db_column='MB020', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mb021 = models.TextField(db_column='MB021', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb022 = models.TextField(db_column='MB022', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pid = models.CharField(db_column='Pid', max_length=6, blank=True, null=True)  # Field name made lowercase.
    tid = models.FloatField(db_column='Tid', blank=True, null=True)  # Field name made lowercase.
    taskid = models.FloatField(db_column='TaskId', blank=True, null=True)  # Field name made lowercase.
    mb023 = models.CharField(db_column='MB023', max_length=15, blank=True, null=True)  # Field name made lowercase.
    mb024 = models.TextField(db_column='MB024', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb025 = models.TextField(db_column='MB025', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    id = models.IntegerField(db_column='Id')  # Field name made lowercase.
    parentid = models.IntegerField(db_column='ParentId', blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID',primary_key=True)  # Field name made lowercase.
    mb026 = models.CharField(db_column='MB026', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb027 = models.IntegerField(db_column='MB027', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_TECME'


class Tecme(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mb001 = models.CharField(db_column='MB001', max_length=11, blank=True, null=True)  # Field name made lowercase.
    mb002 = models.CharField(db_column='MB002', max_length=4, blank=True, null=True)  # Field name made lowercase.
    mb003 = models.CharField(db_column='MB003', max_length=11, blank=True, null=True)  # Field name made lowercase.
    mb004 = models.CharField(db_column='MB004', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb005 = models.CharField(db_column='MB005', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mb006 = models.CharField(db_column='MB006', max_length=8, blank=True, null=True)  # Field name made lowercase.
    mb007 = models.TextField(db_column='MB007', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb008 = models.TextField(db_column='MB008', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb009 = models.TextField(db_column='MB009', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb010 = models.TextField(db_column='MB010', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb011 = models.TextField(db_column='MB011', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb012 = models.TextField(db_column='MB012', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb013 = models.CharField(db_column='MB013', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb015 = models.CharField(db_column='MB015', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb016 = models.CharField(db_column='MB016', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb017 = models.TextField(db_column='MB017', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb018 = models.CharField(db_column='MB018', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb019 = models.CharField(db_column='MB019', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb020 = models.CharField(db_column='MB020', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mb021 = models.TextField(db_column='MB021', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb022 = models.TextField(db_column='MB022', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pid = models.CharField(db_column='Pid', max_length=6, blank=True, null=True)  # Field name made lowercase.
    tid = models.FloatField(db_column='Tid', blank=True, null=True)  # Field name made lowercase.
    taskid = models.FloatField(db_column='TaskId', blank=True, null=True)  # Field name made lowercase.
    mb023 = models.CharField(db_column='MB023', max_length=15, blank=True, null=True)  # Field name made lowercase.
    mb024 = models.TextField(db_column='MB024', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mb025 = models.TextField(db_column='MB025', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    id = models.IntegerField(db_column='Id')  # Field name made lowercase.
    parentid = models.IntegerField(db_column='ParentId', blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID',primary_key=True)  # Field name made lowercase.
    mb026 = models.CharField(db_column='MB026', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mb027 = models.IntegerField(db_column='MB027', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TECME'


class VSubprojectSession(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    recordid = models.CharField(db_column='RecordID', max_length=6)  # Field name made lowercase.
    projectid = models.CharField(db_column='ProjectID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    projectname = models.CharField(db_column='ProjectName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    filter = models.TextField(db_column='Filter', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    contact = models.CharField(db_column='Contact', max_length=12, blank=True, null=True)  # Field name made lowercase.
    planbdate = models.DateTimeField(db_column='PlanBDate', blank=True, null=True)  # Field name made lowercase.
    planedate = models.DateTimeField(db_column='PlanEDate', blank=True, null=True)  # Field name made lowercase.
    etime = models.FloatField(db_column='Etime', blank=True, null=True)  # Field name made lowercase.
    bdate = models.DateTimeField(db_column='BDate', blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='EDate', blank=True, null=True)  # Field name made lowercase.
    atime = models.FloatField(db_column='ATime', blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=255, blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    score = models.IntegerField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    resource = models.CharField(db_column='Resource', max_length=200, blank=True, null=True)  # Field name made lowercase.
    revisedby = models.CharField(db_column='RevisedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    searchtypeid = models.IntegerField(db_column='SearchTypeID', blank=True, null=True)  # Field name made lowercase.
    searchid = models.IntegerField(db_column='SearchID', blank=True, null=True)  # Field name made lowercase.
    method = models.CharField(db_column='Method', max_length=1, blank=True, null=True)  # Field name made lowercase.
    priority = models.FloatField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    udf03 = models.FloatField(db_column='UDF03', blank=True, null=True)  # Field name made lowercase.
    searchcreator = models.CharField(db_column='SearchCreator', max_length=30, blank=True, null=True)  # Field name made lowercase.
    relationdoc = models.CharField(db_column='RelationDoc', max_length=30, blank=True, null=True)  # Field name made lowercase.
    complete = models.CharField(db_column='Complete', max_length=8, blank=True, null=True)  # Field name made lowercase.
    fullcomplete = models.CharField(db_column='FullComplete', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mainflowchar = models.CharField(db_column='MainFlowChar', max_length=100, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.IntegerField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    sqty = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_Subproject_Session'  
class Improvearea(models.Model):
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=200, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=30, blank=True, null=True)  # Field name made lowercase.
    position = models.CharField(db_column='Position', max_length=30, blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(db_column='Score', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ImproveArea'

class VSubprojectSch(models.Model):
    recordid = models.CharField(db_column='RecordId',primary_key=True, max_length=6)  # Field name made lowercase.
    projectname = models.CharField(db_column='ProjectName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    score = models.IntegerField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    goal = models.TextField(db_column='Goal', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    taskqty = models.IntegerField(db_column='TaskQty', blank=True, null=True)  # Field name made lowercase.
    outtaskqty = models.IntegerField(db_column='OutTaskQty', blank=True, null=True)  # Field name made lowercase.
    schfinishdate = models.DateTimeField(db_column='SchFinishDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_SubProject_Sch'


class Schmm(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mm001 = models.CharField(db_column='MM001', max_length=25)  # Field name made lowercase.
    mm002 = models.CharField(db_column='MM002', max_length=1)  # Field name made lowercase.
    mm003 = models.CharField(db_column='MM003', max_length=50)  # Field name made lowercase.
    mm004 = models.IntegerField(db_column='MM004', blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SCHMM'
        unique_together = (('mm001', 'mm002', 'mm003'),)

class VSubporjectSessionUser(models.Model):
    isglobal = models.CharField(db_column='IsGlobal', max_length=1)  # Field name made lowercase.
    contactc = models.CharField(db_column='ContactC', max_length=15, blank=True, null=True)  # Field name made lowercase.
    userscore = models.IntegerField(db_column='UserScore', blank=True, null=True)  # Field name made lowercase.
    useronlyscore = models.IntegerField(db_column='UserOnlyScore', blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    recordid = models.CharField(db_column='RecordID', max_length=6)  # Field name made lowercase.
    projectid = models.CharField(db_column='ProjectID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    projectname = models.CharField(db_column='ProjectName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    filter = models.TextField(db_column='Filter', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    contact = models.CharField(db_column='Contact', max_length=12, blank=True, null=True)  # Field name made lowercase.
    planbdate = models.DateTimeField(db_column='PlanBDate', blank=True, null=True)  # Field name made lowercase.
    planedate = models.DateTimeField(db_column='PlanEDate', blank=True, null=True)  # Field name made lowercase.
    etime = models.FloatField(db_column='Etime', blank=True, null=True)  # Field name made lowercase.
    bdate = models.DateTimeField(db_column='BDate', blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='EDate', blank=True, null=True)  # Field name made lowercase.
    atime = models.FloatField(db_column='ATime', blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=255, blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    score = models.IntegerField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    resource = models.CharField(db_column='Resource', max_length=200, blank=True, null=True)  # Field name made lowercase.
    revisedby = models.CharField(db_column='RevisedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    searchtypeid = models.IntegerField(db_column='SearchTypeID', blank=True, null=True)  # Field name made lowercase.
    searchid = models.IntegerField(db_column='SearchID', blank=True, null=True)  # Field name made lowercase.
    method = models.CharField(db_column='Method', max_length=1, blank=True, null=True)  # Field name made lowercase.
    priority = models.FloatField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    udf03 = models.FloatField(db_column='UDF03', blank=True, null=True)  # Field name made lowercase.
    searchcreator = models.CharField(db_column='SearchCreator', max_length=30, blank=True, null=True)  # Field name made lowercase.
    relationdoc = models.CharField(db_column='RelationDoc', max_length=30, blank=True, null=True)  # Field name made lowercase.
    complete = models.CharField(db_column='Complete', max_length=8, blank=True, null=True)  # Field name made lowercase.
    fullcomplete = models.CharField(db_column='FullComplete', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mainflowchar = models.CharField(db_column='MainFlowChar', max_length=100, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.IntegerField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    mintid = models.FloatField(db_column='MinTid', blank=True, null=True)  # Field name made lowercase.
    maxtid = models.FloatField(db_column='MaxTid', blank=True, null=True)  # Field name made lowercase.
    sqty = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_Subproject_Session_User'      

class VTasklistSchUser(models.Model):
    isglobal = models.CharField(db_column='IsGlobal', max_length=1)  # Field name made lowercase.
    contactc = models.CharField(db_column='ContactC', max_length=20, blank=True, null=True)  # Field name made lowercase.
    userweight = models.FloatField(db_column='UserWeight', blank=True, null=True)  # Field name made lowercase.
    useronlyweight = models.FloatField(db_column='UserOnlyWeight', blank=True, null=True)  # Field name made lowercase.
    recordid = models.CharField(db_column='RecordId', max_length=6, blank=True, null=True)  # Field name made lowercase.
    sessionid = models.CharField(db_column='SessionId', max_length=37, blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pid = models.CharField(db_column='Pid', max_length=16)  # Field name made lowercase.
    tid = models.FloatField(db_column='Tid')  # Field name made lowercase.
    desp = models.BinaryField(db_column='Desp', blank=True, null=True)  # Field name made lowercase.
    priority = models.FloatField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    planbdate = models.DateTimeField(db_column='PlanBDate', blank=True, null=True)  # Field name made lowercase.
    etime = models.FloatField(db_column='Etime', blank=True, null=True)  # Field name made lowercase.
    planedate = models.DateTimeField(db_column='PlanEDate', blank=True, null=True)  # Field name made lowercase.
    bdate = models.DateTimeField(db_column='Bdate', blank=True, null=True)  # Field name made lowercase.
    atime = models.FloatField(db_column='Atime', blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='Edate', blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='Progress', max_length=1, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    sdesp = models.CharField(db_column='SDesp', max_length=3000, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=20, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=256, blank=True, null=True)  # Field name made lowercase.
    revisedby = models.CharField(db_column='RevisedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    msgflag = models.CharField(db_column='MsgFlag', max_length=1, blank=True, null=True)  # Field name made lowercase.
    recerver = models.CharField(db_column='Recerver', max_length=50, blank=True, null=True)  # Field name made lowercase.
    flowchartno = models.CharField(db_column='FlowChartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    parent = models.CharField(db_column='Parent', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=50, blank=True, null=True)  # Field name made lowercase.
    class_field = models.IntegerField(db_column='Class', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    weight = models.FloatField(db_column='Weight', blank=True, null=True)  # Field name made lowercase.
    goaltype = models.CharField(db_column='GoalType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    capacity = models.IntegerField(db_column='Capacity', blank=True, null=True)  # Field name made lowercase.
    djcapacity = models.IntegerField(db_column='DJCapacity', blank=True, null=True)  # Field name made lowercase.
    cycleno = models.CharField(db_column='CycleNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    schrate = models.IntegerField(db_column='SchRate', blank=True, null=True)  # Field name made lowercase.
    estimate = models.IntegerField(db_column='Estimate', blank=True, null=True)  # Field name made lowercase.
    handletype = models.CharField(db_column='HandleType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.IntegerField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    signify = models.IntegerField()
    request = models.IntegerField()
    completed = models.IntegerField()
    problems = models.IntegerField()
    earliesunfinish = models.DateTimeField(db_column='earliesUnFinish', blank=True, null=True)  # Field name made lowercase.
    lastunfinish = models.DateTimeField(db_column='lastUnFinish', blank=True, null=True)  # Field name made lowercase.
    score = models.IntegerField()
    minplanbdate = models.DateTimeField(db_column='MinPlanBDate', blank=True, null=True)  # Field name made lowercase.
    maxplanedate = models.DateTimeField(db_column='MaxPlanEDate', blank=True, null=True)  # Field name made lowercase.
    maxcreatedate = models.DateTimeField(db_column='MaxCreateDate', blank=True, null=True)  # Field name made lowercase.
    taskqty = models.IntegerField(db_column='TaskQty', blank=True, null=True)  # Field name made lowercase.
    pschedule = models.IntegerField(db_column='PSchedule')  # Field name made lowercase.
    aschedule = models.IntegerField(db_column='ASchedule')  # Field name made lowercase.
    outstandday = models.IntegerField(db_column='OutstandDay', blank=True, null=True)  # Field name made lowercase.
    outstandqty = models.IntegerField(db_column='OutstandQty', blank=True, null=True)  # Field name made lowercase.
    overtaskqty = models.FloatField(db_column='OverTaskQty', blank=True, null=True)  # Field name made lowercase.
    projectscore = models.IntegerField(db_column='ProjectScore', blank=True, null=True)  # Field name made lowercase.
    quarterly = models.IntegerField(db_column='Quarterly', blank=True, null=True)  # Field name made lowercase.
    subpropriority = models.FloatField(db_column='SubProPriority', blank=True, null=True)  # Field name made lowercase.
    subplanbdate = models.DateTimeField(db_column='SubPlanBDate', blank=True, null=True)  # Field name made lowercase.
    allcontact = models.CharField(db_column='AllContact', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'V_TaskList_Sch_User'

class Sessionlog(models.Model):
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    pid = models.CharField(db_column='PID', max_length=16)  # Field name made lowercase.
    tid = models.FloatField(db_column='TID')  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=25)  # Field name made lowercase.
    createlogtime = models.DateTimeField(db_column='CreateLogTime', blank=True, null=True)  # Field name made lowercase.
    exetime = models.DateTimeField(db_column='exeTime', blank=True, null=True)  # Field name made lowercase.
    updatelogtime = models.DateTimeField(db_column='UpdateLogTime', blank=True, null=True)  # Field name made lowercase.
    action = models.TextField(db_column='Action', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    actiontype = models.CharField(db_column='ActionType', max_length=25, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SessionLog'

class Pmstr(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    tr001 = models.IntegerField(db_column='TR001', blank=True, null=True)  # Field name made lowercase.
    tr002 = models.CharField(db_column='TR002', max_length=20)  # Field name made lowercase.
    tr003 = models.CharField(db_column='TR003', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tr004 = models.DateTimeField(db_column='TR004', blank=True, null=True)  # Field name made lowercase.
    tr005 = models.DateTimeField(db_column='TR005', blank=True, null=True)  # Field name made lowercase.
    tr006 = models.CharField(db_column='TR006', max_length=12)  # Field name made lowercase.
    tr007 = models.CharField(db_column='TR007', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tr008 = models.CharField(db_column='TR008', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tr009 = models.CharField(db_column='TR009', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tr010 = models.CharField(db_column='TR010', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tr011 = models.CharField(db_column='TR011', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tr012 = models.CharField(db_column='TR012', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tr013 = models.CharField(db_column='TR013', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tr014 = models.CharField(db_column='TR014', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tr015 = models.CharField(db_column='TR015', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tr016 = models.DateTimeField(db_column='TR016', blank=True, null=True)  # Field name made lowercase.
    tr017 = models.CharField(db_column='TR017', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tr018 = models.CharField(db_column='TR018', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tr019 = models.CharField(db_column='TR019', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tr020 = models.CharField(db_column='TR020', max_length=30, blank=True, null=True)  # Field name made lowercase.
    tr021 = models.DateTimeField(db_column='TR021', blank=True, null=True)  # Field name made lowercase.
    tr022 = models.DateTimeField(db_column='TR022', blank=True, null=True)  # Field name made lowercase.
    tr023 = models.CharField(db_column='TR023', max_length=60, blank=True, null=True)  # Field name made lowercase.
    tr024 = models.IntegerField(db_column='TR024', blank=True, null=True)  # Field name made lowercase.
    tr025 = models.CharField(db_column='TR025', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tr026 = models.CharField(db_column='TR026', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tr027 = models.CharField(db_column='TR027', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tr028 = models.CharField(db_column='TR028', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tr029 = models.IntegerField(db_column='TR029', blank=True, null=True)  # Field name made lowercase.
    tr030 = models.CharField(db_column='TR030', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tr031 = models.DateTimeField(db_column='TR031', blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PMSTR'
        unique_together = (('tr002', 'tr006'),)


class Project(models.Model):
    pid = models.CharField(db_column='Pid', max_length=16)  # Field name made lowercase.
    pname = models.CharField(db_column='PName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sourceloc = models.CharField(db_column='SourceLoc', max_length=50, blank=True, null=True)  # Field name made lowercase.
    requirement = models.BinaryField(db_column='Requirement', blank=True, null=True)  # Field name made lowercase.
    desp = models.BinaryField(db_column='Desp', blank=True, null=True)  # Field name made lowercase.
    frames = models.BinaryField(db_column='Frames', blank=True, null=True)  # Field name made lowercase.
    tablesstruct = models.BinaryField(db_column='TablesStruct', blank=True, null=True)  # Field name made lowercase.
    flowchart = models.BinaryField(db_column='Flowchart', blank=True, null=True)  # Field name made lowercase.
    alias = models.CharField(db_column='Alias', max_length=100, blank=True, null=True)  # Field name made lowercase.
    databasetype = models.CharField(db_column='DatabaseType', max_length=40, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='Version', max_length=7, blank=True, null=True)  # Field name made lowercase.
    vdate = models.DateTimeField(db_column='VDate', blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    deptid = models.CharField(db_column='DeptId', max_length=50, blank=True, null=True)  # Field name made lowercase.
    revisedby = models.CharField(db_column='RevisedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    companyid = models.CharField(db_column='CompanyID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Project'

class Sqlscript(models.Model):
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    id = models.IntegerField()  # Field name made lowercase.
    name = models.CharField(max_length=100, blank=True, null=True)
    sql = models.TextField(blank=True, null=True)  # This field type is a guess.
    desc = models.CharField(max_length=200, blank=True, null=True)
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    category = models.CharField(max_length=100, blank=True, null=True)
    isai = models.BooleanField(db_column='IsAI', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SqlScript'

class Aiqueryhistory(models.Model):
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    question = models.CharField(db_column='Question', max_length=200, blank=True, null=True)  # Field name made lowercase.
    timestamp = models.DateTimeField(db_column='TimeStamp', blank=True, null=True)  # Field name made lowercase.
    sql_query = models.TextField(db_column='SQL_query', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    excuted_by = models.CharField(db_column='Excuted_by', max_length=20, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=1, blank=True, null=True)  # Field name made lowercase.
    databaseobject = models.CharField(db_column='DatabaseObject', max_length=200, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AIQueryHistory'


class Admmd(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    md001 = models.CharField(db_column='MD001', primary_key=True, max_length=30)  # Field name made lowercase.
    md002 = models.CharField(db_column='MD002', max_length=4, blank=True, null=True)  # Field name made lowercase.
    md003 = models.CharField(db_column='MD003', max_length=30)  # Field name made lowercase.
    md004 = models.CharField(db_column='MD004', max_length=20, blank=True, null=True)  # Field name made lowercase.
    md005 = models.CharField(db_column='MD005', max_length=15, blank=True, null=True)  # Field name made lowercase.
    md006 = models.DecimalField(db_column='MD006', max_digits=4, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    md007 = models.CharField(db_column='MD007', max_length=255, blank=True, null=True)  # Field name made lowercase.
    md008 = models.CharField(db_column='MD008', max_length=10, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf06 = models.CharField(db_column='UDF06', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf51 = models.DecimalField(db_column='UDF51', max_digits=15, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    udf52 = models.DecimalField(db_column='UDF52', max_digits=15, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    udf53 = models.DecimalField(db_column='UDF53', max_digits=15, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    udf54 = models.DecimalField(db_column='UDF54', max_digits=15, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    udf55 = models.DecimalField(db_column='UDF55', max_digits=15, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    udf56 = models.DecimalField(db_column='UDF56', max_digits=15, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    syncflag = models.IntegerField(db_column='SyncFlag', blank=True, null=True)  # Field name made lowercase.
    syncdate = models.DateTimeField(db_column='SyncDate', blank=True, null=True)  # Field name made lowercase.
    udf60 = models.CharField(db_column='UDF60', max_length=25, blank=True, null=True)  # Field name made lowercase.
    udf61 = models.CharField(db_column='UDF61', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf62 = models.CharField(db_column='UDF62', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf63 = models.CharField(db_column='UDF63', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf64 = models.CharField(db_column='UDF64', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf65 = models.CharField(db_column='UDF65', max_length=20, blank=True, null=True)  # Field name made lowercase.
    udf66 = models.CharField(db_column='UDF66', max_length=20, blank=True, null=True)  # Field name made lowercase.
    udf67 = models.CharField(db_column='UDF67', max_length=50, blank=True, null=True)  # Field name made lowercase.
    udf68 = models.CharField(db_column='UDF68', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ADMMD'
        unique_together = (('md001', 'md003'),)

class Admmc(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mc001 = models.CharField(db_column='MC001', primary_key=True, max_length=30)  # Field name made lowercase.
    mc002 = models.CharField(db_column='MC002', max_length=24, blank=True, null=True)  # Field name made lowercase.
    mc003 = models.CharField(db_column='MC003', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mc004 = models.CharField(db_column='MC004', max_length=3, blank=True, null=True)  # Field name made lowercase.
    mc005 = models.CharField(db_column='MC005', max_length=255, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf06 = models.CharField(db_column='UDF06', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf51 = models.DecimalField(db_column='UDF51', max_digits=15, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    udf52 = models.DecimalField(db_column='UDF52', max_digits=15, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    udf53 = models.DecimalField(db_column='UDF53', max_digits=15, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    udf54 = models.DecimalField(db_column='UDF54', max_digits=15, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    udf55 = models.DecimalField(db_column='UDF55', max_digits=15, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    udf56 = models.DecimalField(db_column='UDF56', max_digits=15, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    syncflag = models.IntegerField(db_column='SyncFlag', blank=True, null=True)  # Field name made lowercase.
    syncdate = models.CharField(db_column='SyncDate', max_length=11, blank=True, null=True)  # Field name made lowercase.
    viewsql = models.TextField(db_column='ViewSQL', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    renovate = models.CharField(db_column='Renovate', max_length=1, blank=True, null=True)  # Field name made lowercase.
    auditdate = models.CharField(db_column='AuditDate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    auditname = models.CharField(db_column='AuditName', max_length=15, blank=True, null=True)  # Field name made lowercase.
    mc010 = models.CharField(db_column='MC010', max_length=500, blank=True, null=True)  # Field name made lowercase.
    mc011 = models.CharField(db_column='MC011', max_length=500, blank=True, null=True)  # Field name made lowercase.
    mc012 = models.CharField(db_column='MC012', max_length=500, blank=True, null=True)  # Field name made lowercase.
    mc013 = models.CharField(db_column='MC013', max_length=500, blank=True, null=True)  # Field name made lowercase.
    mc014 = models.CharField(db_column='MC014', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mc015 = models.CharField(db_column='MC015', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mc016 = models.CharField(db_column='MC016', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ADMMC'


class TasklistRelation(models.Model):
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pid = models.CharField(db_column='Pid', max_length=16)  # Field name made lowercase.
    tid = models.FloatField(db_column='Tid')  # Field name made lowercase.
    relationsessionid = models.CharField(db_column='RelationSessionId', max_length=20)  # Field name made lowercase.
    relationtype = models.CharField(db_column='RelationType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=1, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TaskList_Relation'
        unique_together = (('pid', 'tid', 'relationsessionid'),)

