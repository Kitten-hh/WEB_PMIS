from lib2to3.pytree import Node
from DataBase_MPMS import models
from django.forms.models import model_to_dict
from django.http import JsonResponse,HttpResponse,HttpRequest
from BaseApp.library.tools import DateTools
from django.utils.translation import ugettext_lazy as _
from PMIS.Services.GoalService import GoalService
import logging

LOGGER = logging.Logger(__name__)

def search_goal(request):
    def get_params():
        name_params = ['period','month','week','contact','goaldesc']
        local_fields = {a.attname:a.column for a in models.Goalmanagement._meta.get_fields() if a.attname in name_params}
        progress = request.GET.get('progress','')
        filter_str = "GoalType = 'W'"
        params = []
        for param in name_params:
            value = request.GET.get(param)
            if value:
                field_name = local_fields[param]
                if param == 'goaldesc':
                    filter_str += " and " + field_name + " like '%{}%'"
                else:
                    filter_str += " and " + field_name + " = '{}'"
                params.append(value)
        filter_str = filter_str.format(*params)
        return filter_str, progress
    filter_str, progress = get_params()
    is_overall = request.GET.get('is_overall','false') == 'true'
    result = {'status':False, 'msg':'', 'data':[]}
    try:
        if not is_overall:
            datas,tasks = GoalService.search_goal_progress_single(filter_str, progress)
        else:
            datas,tasks = GoalService.search_goal_progress(filter_str, progress)
        result['status'] = True
        result['data'] = datas
        result['tasks'] = tasks
    except Exception as e:
        LOGGER.error(str(e))
    return JsonResponse(result, safe=False)
