from django.db import models

# Create your models here.

class Ntfymessage(models.Model):
    id = models.IntegerField(db_column="id", null=False)
    category_id = models.IntegerField(blank=True, null=True)
    topic = models.CharField(max_length=255,blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    actions = models.TextField(blank=True, null=True)
    click_url = models.CharField(max_length=255, blank=True, null=True)
    attach_url = models.CharField(max_length=255, blank=True, null=True)
    is_markdown = models.BooleanField(blank=True, null=True)
    icon_url = models.CharField(max_length=255, blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True)
    delay = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    call_info = models.CharField(max_length=50, blank=True, null=True)
    receiver = models.CharField(max_length=50, blank=True, null=True)
    sent_time = models.DateTimeField(blank=True, null=True)
    received_time = models.DateTimeField(blank=True, null=True)
    delivery_status = models.CharField(max_length=1, blank=True, null=True)
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.
    msg_createdate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'NtfyMessage'


class Messagecategory(models.Model):
    id = models.IntegerField(db_column="id", null=False)
    category_name = models.CharField(max_length=255)
    title_format = models.CharField(max_length=255, blank=True, null=True)
    message_format = models.TextField(blank=True, null=True)
    click_url_format = models.CharField(max_length=255, blank=True, null=True)
    supported_actions = models.TextField(blank=True, null=True)
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MessageCategory'

class ActionFormat(models.Model):
    category = models.CharField(max_length=255)
    action_name = models.CharField(max_length=255)
    url_format = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.action_name} for {self.category.category_name}"
    class Meta:
        managed = False
        db_table = 'ActionFormat'
