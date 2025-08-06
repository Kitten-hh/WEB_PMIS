from django.db import models


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
