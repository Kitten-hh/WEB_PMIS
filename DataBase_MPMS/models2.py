# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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
    inc_id = models.IntegerField(db_column='INC_ID',primary_key=True)  # Field name made lowercase.
    mb026 = models.CharField(db_column='MB026', max_length=255, blank=True, null=True)  # Field name made lowercase.

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
    inc_id = models.IntegerField(db_column='INC_ID',primary_key=True)  # Field name made lowercase.
    mb026 = models.CharField(db_column='MB026', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TECME'
