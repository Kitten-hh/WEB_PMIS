import sys
from enum import Enum
import os
import django
import datetime,dateutil,calendar,math
from dateutil import rrule,relativedelta
import json
import re

# 這兩行很重要，用來尋找專案根目錄，os.path.dirname要寫多少個根據要運行的python檔到根目錄的層數決定
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WEB_PMIS.settings')
django.setup()
from django.db.models import IntegerField,CharField, Value as V
from django.db.models.functions import Cast, Substr
from django.db.models import Sum,Count,Max,Min,Avg,Q
from django.forms import Form,ModelForm
from django.forms.fields import CharField,BooleanField,\
    CharField,DateField,DecimalField,DateTimeField,IntegerField,FloatField,Field


from PMIS import forms

def general_html_with_form(form:Form, config, vue_tablename=None):
    '''
    功能描述:根據form中的字段信息生成html
    '''
    html = ''
    for field_name in config:
        locate = field_name.find(':')
        param = ''
        if locate != -1:
            param = field_name[locate+1:]
            field_name = field_name[:locate]
        field = form[field_name]
        ##生成錄入框group
        html +='''  <div class="form-group row align-middle mb-3 col-sm-12 col-md-6 col-lg-4 col-xl-3">\n'''
        ##生成label
        html +='''      <label class="col-form-label text-right col-sm-4" for="{0}">{1} </label>\n'''.format('id_'+field_name, field.label)
        ##生成錄入框
        html += '     <div class="input-group col-sm-7">\n'
        input_str = str(field)
        ##如果是日期字段，則生成日期錄入框
        if type(field.field) in [DateField, DateTimeField]:
            input_str = re.sub(r'type="\w+"', r'type="date"', input_str)
        input_str = re.sub(r'<(\w+) ',r'<\1 class="form-control" ', input_str)
        if vue_tablename:
            replace_str = r'\1 v-model="' + vue_tablename + r'_CurData.' + field_name + r'"'
            input_str = re.sub(r'(name="\w+")', replace_str, input_str)
        html +='      ' + input_str + '\n'
        ##如果參數中有b表示需要添加Button
        if 'b' in param:
            html += '    <div class="input-group-append">\n'
            html += '      <button type="button" class="btn btn-secondary"><i class="fa fa-bars"></i></button>\n'
            html += '     </div>\n'
        html += '    </div>\n'
        html +='  </div>\n'
    print(html)
    with open('qita.html','w') as fout:
        fout.write(html)
if __name__ == "__main__":
    form = forms.SchType_main_form()
    config = ('typeno','typename','logic','formula','remark')
    general_html_with_form(form,config, "SchType")
