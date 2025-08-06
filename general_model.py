# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AiFollowupTbl(models.Model):
    followup_id = models.IntegerField(db_column='Followup_ID', primary_key=True)  # Field name made lowercase.
    item_no = models.IntegerField(db_column='Item_No')  # Field name made lowercase.
    category_id = models.IntegerField(db_column='Category_ID', blank=True, null=True)  # Field name made lowercase.
    main_question_id = models.IntegerField(db_column='Main_Question_ID', blank=True, null=True)  # Field name made lowercase.
    sub_question_id = models.IntegerField(db_column='Sub_Question_ID', blank=True, null=True)  # Field name made lowercase.
    auth_inc = models.CharField(db_column='Auth_inc', max_length=255)  # Field name made lowercase.
    question = models.TextField(db_column='Question')  # Field name made lowercase.
    reply = models.TextField(db_column='Reply', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Ai_Followup_tbl'
        unique_together = (('followup_id', 'item_no'),)
