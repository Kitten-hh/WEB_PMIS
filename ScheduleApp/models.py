from django.db import models

# Create your models here.
class Chattopictbl(models.Model):
    topicid = models.IntegerField(db_column='TopicID')  # Field name made lowercase.
    cid = models.IntegerField(db_column='CID')  # Field name made lowercase.
    topic = models.CharField(db_column='Topic', max_length=255)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=255)  # Field name made lowercase.
    tdescription = models.TextField(db_column='TDescription', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    cdescription = models.TextField(db_column='CDescription', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    tdate = models.DateField(db_column='TDate', blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID',  primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ChatTopicTbl'
        unique_together = (('topicid', 'cid'),)


class Prompttbl(models.Model):
    topicid = models.IntegerField(db_column='TopicID')  # Field name made lowercase.
    cid = models.IntegerField(db_column='CID')  # Field name made lowercase.    
    pid = models.IntegerField(db_column='PID')  # Field name made lowercase.
    topic = models.CharField(db_column='Topic', max_length=255, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=255, blank=True, null=True)  # Field name made lowercase.
    prompt = models.TextField(db_column='Prompt', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    action = models.CharField(db_column='Action', max_length=255, blank=True, null=True)  # Field name made lowercase.
    post_bool = models.CharField(db_column='Post_Bool', max_length=1, blank=True, null=True)  # Field name made lowercase.
    predefined_questions = models.TextField(db_column='Predefined_Questions', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    predefined_prompt = models.TextField(db_column='Predefined_Prompt', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    relation = models.CharField(db_column='Relation', max_length=255, blank=True, null=True)  # Field name made lowercase.
    app_bool = models.CharField(db_column='App_Bool', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdate = models.DateField(db_column='PDate', blank=True, null=True)  # Field name made lowercase.
    chat_topic = models.CharField(db_column='Chat_Topic', max_length=255, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID',  primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PromptTbl'
        unique_together = (('topicid', 'topicid', 'cid', 'cid', 'pid'),)


class Promtsql(models.Model):
    ssid = models.IntegerField(db_column='SSID')  # Field name made lowercase.
    sname = models.CharField(db_column='SName', max_length=255)  # Field name made lowercase.
    ssql = models.TextField(db_column='SSQL', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    params = models.CharField(db_column='Params', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sdate = models.DateTimeField(db_column='SDate', blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=255, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    sql_description = models.CharField(db_column='SQL_Description', max_length=200, blank=True, null=True)  # Field name made lowercase.
    isai = models.BooleanField(db_column='IsAi', blank=True, null=True)  # Field name made lowercase.
    isapproved = models.BooleanField(db_column='IsApproved', blank=True, null=True)  # Field name made lowercase.
    isdatabasesql = models.BooleanField(db_column='IsDatabaseSQL', blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=100, blank=True, null=True)  # Field name made lowercase.
    timestamp = models.DateTimeField(db_column='TimeStamp', blank=True, null=True)  # Field name made lowercase.
    promptbyai = models.CharField(db_column='PromptByAi', max_length=500)  # Field name made lowercase.
    action = models.CharField(db_column='Action', max_length=200, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'PromtSQL'


class PromptcategoryTbl(models.Model):
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    categoryno = models.IntegerField(db_column='CategoryNo')  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=100, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=250, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Promptcategory_tbl'