from django.shortcuts import render
from DataBase_MPMS.models import Userbonusparam,Syspara
from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
from django.http import JsonResponse, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.shortcuts import redirect
from django.db.models import Q
from DataBase_MPMS import forms_base
from django.views.generic.edit import CreateView
from BaseApp.library.cust_views.SWCreateView import SWCreateView
from BaseApp.library.cust_views.SWUpdateView import SWUpdateView
from BaseApp.library.cust_views.SWDeleteView import SWDeleteView
from django.forms import ModelForm
from django.db import transaction
from BaseApp.library.tools import ModelTools
from django.forms.models import model_to_dict
from datetime import datetime


# get_systemParameters/ 显示首页table数据
#def get_systemParameters_List(request):
#    syspara = Syspara.objects.filter(desp='BonusApp').order_by('-inc_id')
#    sysparaList = list(syspara.values())
#    result = {}
#   result['state'] = 200
#    result['data'] = sysparaList
#    return JsonResponse(result)

class SysparaView(DatatablesServerSideView):
    model = Syspara
    columns =['nfield','ftype','desp','fvalue','inc_id']
    searchable_columns = columns

    def get_initial_queryset(self):
        #return self.model.objects.filter(bdate__range=(start_date,end_date),contact=name)
        return self.model.objects.filter(desp='BonusApp').order_by('-inc_id')

class UserBonusParamView(DatatablesServerSideView):
    model = Userbonusparam
    columns =['username','budgetallowance','managementratio','performanaceratio','ratioofm','ratioofp','ratioofs','salary','unitprice']
    searchable_columns = columns    

#Syspara详情页面数据显示
def get_Syspara_Details(request):
    inc_id = request.GET.get("inc_id")
    syspara = Syspara.objects.filter(inc_id=inc_id)
    SysparaList = list(syspara)
    context = {'Syspara':SysparaList[0]}
    return render(request, 'BonusApp/SystemParameters/Syspara_Details.html', context)    

# 查询
# def searchData(request):
#     term = request.GET.get('condition')
#     q = Q()
#     q.connector = 'OR'
#     q.children.append(('nfield__icontains',term))
#     q.children.append(('desp__icontains',term))
#     q.children.append(('ftype__icontains',term))
#     q.children.append(('inc_id__icontatins',term))
#     termlist = Syspara.objects.filter(q)
#     return JsonResponse(list(termlist.values(),safe=False))

 #新增数据
class CreateSyspara(SWCreateView):
    model = Syspara

#修改数据
class UpdateSyspara(SWUpdateView):
    model = Syspara

#删除数据
class DeleteSyspara(SWDeleteView):
    model = Syspara

#修改数据
class UpdateBonusParam(SWUpdateView):
    model = Userbonusparam

    def post(self, request, *args, **kwargs):
        '''
        功能描述:標準django http function view
        當http post 方式訪問該SWUpdateView類或它的子類時，調用此方法處理請求        
        '''
        class Dynamic_Form(ModelForm):
            class Meta:
                model = self.model
                fields = '__all__'
        
        result = {'status':False, 'msg':'', 'data':None}
        form = Dynamic_Form(data=request.POST)
        try:  
            with transaction.atomic(using="MPMS"): 
                sid = transaction.savepoint(using="MPMS")  # 开启事务设置事务保存点
                try:
                    self.syspara_save(form.data,'budgetallowance')
                    self.syspara_save(form.data,'managementratio')
                    self.syspara_save(form.data,'performanaceratio')
                    self.syspara_save(form.data,'ratioofm')
                    self.syspara_save(form.data,'ratioofp')
                    self.syspara_save(form.data,'ratioofs')
                    self.syspara_save(form.data,'salary')  
                    self.syspara_save(form.data,'unitprice')  
                    transaction.savepoint_commit(sid,using="MPMS")     
                except Exception as e: 
                    transaction.savepoint_rollback(sid,using="MPMS")  # 失败回滚事务(如果数据库操作发生异常，回滚到设置的事务保存点)                    
                        
            result['status'] = True
            result['data'] = {'pk':form.data['username'], 'instance':form.data}                
        except Exception as e:
            print(str(e))
            result['status'] = False
            result['msg'] = str(e)

        return JsonResponse(result, safe=False) 

    def syspara_save(self, formdata, name):
        paraname = ''      
        if name == 'budgetallowance': paraname = 'BudgetAllowance'
        if name == 'managementratio': paraname = 'ManagementRatio'
        if name == 'performanaceratio': paraname = 'PerformanaceRatio'
        if name == 'ratioofm': paraname = 'RatioOFM'
        if name == 'ratioofp': paraname = 'RatioOFP'
        if name == 'ratioofs': paraname = 'RatioOFS'
        if name == 'salary': paraname = 'Salary'
        if name == 'unitprice': paraname = 'UnitPrice'

        if formdata[name] != None:
            if paraname == 'BudgetAllowance' or paraname == 'UnitPrice':
                sysparas = Syspara.objects.filter(ftype='Bonus',nfield=paraname)  
            else:
                sysparas = Syspara.objects.filter(ftype=formdata['username'],nfield=paraname)  
            if(sysparas.exists()): 
                sysparas.update(fvalue=formdata[name]) # 修改
            else:
                # 新增
                syspara = Syspara()
                syspara.nfield = paraname
                if paraname == 'BudgetAllowance' or paraname == 'UnitPrice':
                    syspara.ftype = 'Bonus'
                else:
                    syspara.ftype = formdata['username']
                syspara.fvalue = formdata[name]
                syspara.desp = 'BonusApp' 
                syspara.t_stamp = datetime.now().date() 
                syspara.save()  


