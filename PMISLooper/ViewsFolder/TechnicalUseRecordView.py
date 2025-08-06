from django.forms import model_to_dict
from django.http import JsonResponse
from DataBase_MPMS.models import Technicaluserecord,Tecmb
from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
from BaseApp.library.cust_views.SWCreateView import SWCreateView
from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from BaseApp.library.cust_views.SWDeleteView import SWDeleteView
from django.db.models import Max


class TechnicaluserecordTable(DatatablesServerSideView):
    model = Technicaluserecord
    columns = '__all__'
    searchable_columns = ['contact', 'technicid', 'issue']

    def get_initial_queryset(self):
        return super().get_initial_queryset()
        '''
        if 'sysid' in self.request.GET:
            sysid = self.request.GET['sysid']
            if sysid == "" or sysid == None:
                return self.model.objects.none()
            return self.model.objects.filter(sysid=sysid)
        return super().get_initial_queryset()
        '''

class TechnicaluserecordCreate(SWCreateView):
    model = Technicaluserecord

    def save_check(self, instance):
        check_data = Technicaluserecord.objects.filter(
            taskno=instance.taskno,inputdate=instance.inputdate, contact=instance.contact, technicid=instance.technicid)
        if check_data.exists():
            return False, "當前記錄已存在"
        else:
            return True, ""

class TechnicaluserecordUpdate(SWUpdateView):
    model = Technicaluserecord


class TechnicaluserecordDelete(SWDeleteView):
    model = Technicaluserecord

def getTechnicalInfo(request):
    result = {'status': False, 'msg': '', 'data': []}
    technicid = request.GET.get('technicid')    
    try:
        if technicid and not technicid=='':
            technicalInfo = Tecmb.objects.filter(mb023=technicid).first() 
            if technicalInfo:       
                result['status'] = True
                result['data'] = model_to_dict(technicalInfo)
    except Exception as e:
        print(e)
        result['msg'] = e
    return JsonResponse(result, safe=False)