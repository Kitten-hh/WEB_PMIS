from DataBase_MPMS import forms_base as fb
from django.utils.translation import gettext as _,gettext_lazy as _
from BaseProject.tools import utils


class TaskType_main_form(fb.TaskType_Form):
    class Meta(fb.TaskType_Form.Meta):
        fields = ['tasktype','description','score','id']
        labels = utils.subDict(fb.TaskType_Form.Meta.labels, ['tasktype','description','score','id'])

# class VTask_main_form(fb.VTask_Form):
#     class Meta(fb.VTask_Form.Meta):
#         fields = ['inc_id','tasktype','subtasktype','diff','task','remark','progress','score',
#             'class_field','priority','planbdate','planedate','bdate','edate','delayday','requestdate']
#         labels = utils.subDict(fb.VTask_Form.Meta.labels, ['inc_id','tasktype','subtasktype','diff','task','remark','progress','score',
#             'class_field','priority','planbdate','planedate','bdate','edate','delayday','requestdate'])