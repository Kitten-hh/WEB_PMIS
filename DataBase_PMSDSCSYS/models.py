from django.db import models

# Create your models here.
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
        app_label = "DataDictionaryDSCSYS"
        db_table = 'ADMMD'
        unique_together = (('md001', 'md003'),)        