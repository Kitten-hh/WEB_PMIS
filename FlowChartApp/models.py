from django.db import models

# Create your models here.
class Flowchart_Bak(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    flowchartno = models.CharField(db_column='FlowChartNo', max_length=30)  # Field name made lowercase.
    version = models.CharField(db_column='Version', max_length=3)  # Field name made lowercase.
    parentno = models.CharField(db_column='ParentNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=50, blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(db_column='Content', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    description = models.CharField(db_column='Description', max_length=500, blank=True, null=True)  # Field name made lowercase.
    tooltipimage = models.BinaryField(db_column='TooltipImage', blank=True, null=True)  # Field name made lowercase.
    fc050 = models.CharField(db_column='FC050', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fc051 = models.CharField(db_column='FC051', max_length=20, blank=True, null=True)  # Field name made lowercase.
    fc052 = models.CharField(db_column='FC052', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fc053 = models.CharField(db_column='FC053', max_length=20, blank=True, null=True)  # Field name made lowercase.
    fc054 = models.CharField(db_column='FC054', max_length=20, blank=True, null=True)  # Field name made lowercase.
    fc055 = models.DecimalField(db_column='FC055', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    fc056 = models.FloatField(db_column='FC056', blank=True, null=True)  # Field name made lowercase.
    fc057 = models.CharField(db_column='FC057', max_length=50, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        app_label='DataBase_MPMS'
        db_table = 'FlowChart'
        unique_together = (('flowchartno', 'version'),)

class Flowchart(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    flowchartno = models.CharField(db_column='FlowChartNo', max_length=30)  # Field name made lowercase.
    version = models.CharField(db_column='Version', max_length=3)  # Field name made lowercase.
    parentno = models.CharField(db_column='ParentNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=50, blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(db_column='Content', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    description = models.CharField(db_column='Description', max_length=500, blank=True, null=True)  # Field name made lowercase.
    tooltipimage = models.BinaryField(db_column='TooltipImage', blank=True, null=True)  # Field name made lowercase.
    fc050 = models.CharField(db_column='FC050', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fc051 = models.CharField(db_column='FC051', max_length=20, blank=True, null=True)  # Field name made lowercase.
    fc052 = models.CharField(db_column='FC052', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fc053 = models.CharField(db_column='FC053', max_length=20, blank=True, null=True)  # Field name made lowercase.
    fc054 = models.CharField(db_column='FC054', max_length=20, blank=True, null=True)  # Field name made lowercase.
    fc055 = models.DecimalField(db_column='FC055', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    fc056 = models.FloatField(db_column='FC056', blank=True, null=True)  # Field name made lowercase.
    fc057 = models.CharField(db_column='FC057', max_length=50, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        app_label='DataBase_MPMS'
        db_table = 'FlowChart_GOJS'
        unique_together = (('flowchartno', 'version'),)


class Docdesign(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    md001 = models.CharField(db_column='MD001', max_length=10)  # Field name made lowercase.
    md002 = models.CharField(db_column='MD002', max_length=50)  # Field name made lowercase.
    md003 = models.CharField(db_column='MD003', max_length=20)  # Field name made lowercase.
    md004 = models.CharField(db_column='MD004', max_length=100, blank=True, null=True)  # Field name made lowercase.
    md005 = models.CharField(db_column='MD005', max_length=20, blank=True, null=True)  # Field name made lowercase.
    md006 = models.CharField(db_column='MD006', max_length=50, blank=True, null=True)  # Field name made lowercase.
    md007 = models.CharField(db_column='MD007', max_length=50, blank=True, null=True)  # Field name made lowercase.
    md008 = models.CharField(db_column='MD008', max_length=50, blank=True, null=True)  # Field name made lowercase.
    md009 = models.CharField(db_column='MD009', max_length=50, blank=True, null=True)  # Field name made lowercase.
    md010 = models.CharField(db_column='MD010', max_length=50, blank=True, null=True)  # Field name made lowercase.
    md011 = models.BooleanField(db_column='MD011', blank=True, null=True)  # Field name made lowercase.
    md012 = models.CharField(db_column='MD012', max_length=200, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID',primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DocDesign'
        app_label='DataBase_MPMS'
        unique_together = (('md001', 'md002', 'md003'),)
