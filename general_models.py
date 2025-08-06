# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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
