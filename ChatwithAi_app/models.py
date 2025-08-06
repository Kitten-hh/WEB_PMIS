from django.db import models

# Create your models here.
class TopicMindMapData(models.Model):
    map_id = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=255, blank=True, null=True)
    Seqno = models.IntegerField(blank=True, null=True)
    boundary = models.TextField(blank=True, null=True)
    callout = models.TextField(blank=True, null=True)
    colour = models.CharField(max_length=255, blank=True, null=True)
    cost = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    displayText = models.TextField(blank=True, null=True)
    dueDate = models.DateTimeField(blank=True, null=True)
    effort = models.CharField(max_length=255, blank=True, null=True)
    effort_hours = models.CharField(max_length=255, blank=True, null=True)
    icons = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    index = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    level0 = models.CharField(max_length=255, blank=True, null=True)
    level1 = models.TextField(blank=True, null=True)
    level10 = models.CharField(max_length=255, blank=True, null=True)
    level11 = models.TextField(blank=True, null=True)
    level12 = models.CharField(max_length=255, blank=True, null=True)
    level13 = models.TextField(blank=True, null=True)
    level14 = models.CharField(max_length=255, blank=True, null=True)
    level15 = models.CharField(max_length=255, blank=True, null=True)
    level16 = models.CharField(max_length=255, blank=True, null=True)
    level17 = models.CharField(max_length=255, blank=True, null=True)
    level18 = models.CharField(max_length=255, blank=True, null=True)
    level19 = models.CharField(max_length=255, blank=True, null=True)
    level2 = models.CharField(max_length=1000, blank=True, null=True)
    level20 = models.CharField(max_length=255, blank=True, null=True)
    level3 = models.TextField(blank=True, null=True)
    level4 = models.CharField(max_length=255, blank=True, null=True)
    level5 = models.CharField(max_length=255, blank=True, null=True)
    level6 = models.CharField(max_length=255, blank=True, null=True)
    level7 = models.CharField(max_length=255, blank=True, null=True)
    level8 = models.CharField(max_length=255, blank=True, null=True)
    level9 = models.CharField(max_length=255, blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    position = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=255, blank=True, null=True)
    progress = models.CharField(max_length=255, blank=True, null=True)
    remainingEffort_hours = models.CharField(max_length=255, blank=True, null=True)
    resources = models.TextField(blank=True, null=True)
    shape = models.TextField(blank=True, null=True)
    startDate = models.DateTimeField(blank=True, null=True)
    uuid = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # Defining a composite unique constraint
        managed = False
        constraints = [
            models.UniqueConstraint(fields=['topic', 'Seqno'], name='unique_topic_seqno')
        ]
        db_table = "TopicMindMapData"

    def __str__(self):
        # Assuming 'topic' and 'Seqno' are significant for identifying a record
        return f"Topic: {self.topic}, Sequence Number: {self.Seqno}"


class Topic(models.Model):
    TopicID = models.AutoField(primary_key=True)
    BookID = models.IntegerField(null=True, blank=True)
    BookSectionID = models.IntegerField(null=True, blank=True)
    Topic = models.CharField(max_length=255, null=True, blank=True)
    Description = models.TextField(null=True, blank=True)
    StartPage = models.IntegerField(null=True, blank=True)
    EndPage = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "Topics"
    def __str__(self):
        return self.Topic

class ChatTopics(models.Model):
    topic_id = models.IntegerField(null=False)
    topic_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_at = models.DateTimeField(blank=True, null=True)
    parent_topic_id = models.IntegerField(blank=True, null=True)
    topic_type = models.IntegerField(blank=True, null=True)
    level = models.IntegerField()
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'chat_topics'


class Chathistory(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    id = models.IntegerField(db_column='Id')  # Field name made lowercase.
    sessionname = models.CharField(db_column='SessionName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    topic = models.CharField(db_column='Topic', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fullconversation = models.TextField(db_column='FullConversation', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fulldisplayconversation = models.TextField(db_column='FullDisplayConversation', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    createdby = models.CharField(db_column='CreatedBy', max_length=255, blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)  # Field name made lowercase.
    recordid = models.CharField(db_column='RecordId', max_length=255, blank=True, null=True)  # Field name made lowercase.
    reference = models.CharField(db_column='Reference', max_length=255, blank=True, null=True)  # Field name made lowercase.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    def save(self, *args, **kwargs):
        if not self.pk:  # 检查是否为新创建的对象
            # 获取当前最大序号
            max_id = Chathistory.objects.aggregate(Max('id'))['id__max']
            # 如果还没有记录，则设置为 1，否则设置为最大序号加一
            self.id = (max_id or 0) + 10
        super(Chathistory, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'ChatHistory'        


class Aisummaryrecord(models.Model):
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(db_column='CREATOR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    create_date = models.CharField(db_column='CREATE_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    modifier = models.CharField(db_column='MODIFIER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modi_date = models.CharField(db_column='MODI_DATE', max_length=17, blank=True, null=True)  # Field name made lowercase.
    flag = models.DecimalField(db_column='FLAG', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    t_stamp = models.DateTimeField(db_column='T_Stamp', blank=True, null=True)  # Field name made lowercase.
    id = models.IntegerField(db_column='Id')  # Field name made lowercase.
    recordid = models.IntegerField(db_column='RecordId', blank=True, null=True)  # Field name made lowercase.
    sessionids = models.TextField(db_column='SessionIds', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    chattopic = models.CharField(db_column='ChatTopic', max_length=255, blank=True, null=True)  # Field name made lowercase.
    aisummary = models.TextField(db_column='AiSummary', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)  # Field name made lowercase.
    comment = models.TextField(db_column='Comment', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    review = models.TextField(db_column='Review', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    udf01 = models.CharField(db_column='UDF01', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf02 = models.CharField(db_column='UDF02', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udf03 = models.CharField(db_column='UDF03', max_length=1, blank=True, null=True)  # Field name made lowercase.
    udf04 = models.CharField(db_column='UDF04', max_length=60, blank=True, null=True)  # Field name made lowercase.
    udf05 = models.CharField(db_column='UDF05', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AiSummaryRecord'


class TopicCategories(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    itemno = models.IntegerField()
    role = models.TextField(blank=True, null=True)  # This field type is a guess.
    role_content = models.TextField(blank=True, null=True)  # This field type is a guess.
    parameters = models.CharField(max_length=500, blank=True, null=True)    

    class Meta:
        managed = False
        db_table = 'topic_categories'


class MainQuestions(models.Model):
    category = models.ForeignKey('TopicCategories', models.DO_NOTHING, blank=True, null=True)
    question = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    itemno = models.IntegerField()
    message_type = models.IntegerField(blank=True, null=True)
    message_type_relationid = models.IntegerField(blank=True, null=True)
    has_params = models.BooleanField(blank=True, null=True)
    parameters = models.CharField(max_length=500, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)
    ai_question = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'main_questions'


class SubQuestions(models.Model):
    main_question = models.ForeignKey(MainQuestions, models.DO_NOTHING, blank=True, null=True)
    sub_question = models.CharField(max_length=255)
    itemno = models.IntegerField()
    message_type = models.IntegerField(blank=True, null=True)
    message_type_relationid = models.IntegerField(blank=True, null=True)
    has_params = models.BooleanField(blank=True, null=True)
    parameters = models.CharField(max_length=500, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)
    ai_question = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sub_questions'

class AiSentences(models.Model):
    reference_id = models.IntegerField()
    reference_type = models.CharField(max_length=50)
    sentence = models.TextField()
    language = models.CharField(max_length=10)
    embedding_vector = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ai_sentences'

class AiActionTypes(models.Model):
    type_name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ai_action_types'


class AiQuestionActions(models.Model):
    action_type = models.ForeignKey(AiActionTypes, models.DO_NOTHING)
    question_id = models.IntegerField()
    question_reference = models.CharField(max_length=50)
    question_type = models.CharField(max_length=255, blank=True, null=True)
    action_question = models.TextField(blank=True, null=True)
    parameters = models.TextField(blank=True, null=True)
    response_format = models.TextField(blank=True, null=True)
    action_details = models.TextField(blank=True, null=True)
    itemno = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ai_question_actions'



class AiPageurls(models.Model):
    recordid = models.CharField(max_length=50)
    page_name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    system_name = models.CharField(max_length=255, blank=True, null=True)
    parameters = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Ai_PageUrls'


class AiMessageType(models.Model):
    message_type = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ai_message_type'


class AiFollowupTbl(models.Model):
    followup_id = models.IntegerField(db_column='Followup_ID')  # Field name made lowercase.
    item_no = models.IntegerField(db_column='Item_No')  # Field name made lowercase.
    category_id = models.IntegerField(db_column='Category_ID', blank=True, null=True)  # Field name made lowercase.
    main_question_id = models.IntegerField(db_column='Main_Question_ID', blank=True, null=True)  # Field name made lowercase.
    sub_question_id = models.IntegerField(db_column='Sub_Question_ID', blank=True, null=True)  # Field name made lowercase.
    auth_inc = models.CharField(db_column='Auth_inc', max_length=255)  # Field name made lowercase.
    question = models.TextField(db_column='Question')  # Field name made lowercase.
    reply = models.TextField(db_column='Reply', blank=True, null=True)  # Field name made lowercase.
    create_date = models.DateTimeField(db_column='CREATE_DATE', blank=True, null=True)  # Field name made lowercase.
    inc_id = models.AutoField(db_column='INC_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Ai_Followup_tbl'
        unique_together = (('followup_id', 'item_no'),)



class TopicViews(models.Model):
    view_name = models.CharField(max_length=255, unique=True)
    view_description = models.TextField()
    sql_statement = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.view_name
    
    class Meta:
        managed = False
        db_table = 'topic_view_table'    

class TopicRelationTables(models.Model):
    topic = models.ForeignKey(TopicCategories, on_delete=models.CASCADE, related_name='relations')
    table_name = models.CharField(max_length=255, blank=True, null=True)
    view = models.ForeignKey(TopicViews, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    limit_type = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        return f"Relation for {self.topic.name}"        
    
    class Meta:
        managed = False
        db_table = 'topic_relation_table'