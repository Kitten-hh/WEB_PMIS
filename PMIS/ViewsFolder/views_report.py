import os
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.template import loader
from django.http import HttpResponse,JsonResponse
from django.db.models import Sum,Count,Max,Min,Avg,Q
from DataBase_MPMS import models
from .. import forms
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from datatableview import Datatable
from django.db import connections
from datatableview.views import MultipleDatatableView
from datatableview.views.legacy import LegacyDatatableView
from datatableview import helpers
def display_report(request):
    return render(request, 'PMIS/report.html')

def get_themes_list(request):
    list = '[{"Id":"Active.rdlx-theme","Title":"Active","Dark1":"#000000","Dark2":"#1F497D","Light1":"#FFFFFF","Light2":"#EEECE1","Accent1":"#4F81BD","Accent2":"#C0504D","Accent3":"#9BBB59","Accent4":"#8064A2","Accent5":"#4BACC6","Accent6":"#F79646","MajorFontFamily":"Arial","MinorFontFamily":"Times New Roman"},{"Id":"Autumn.rdlx-theme","Title":"Autumn","Dark1":"#2F2B20","Dark2":"#675E47","Light1":"#FFFFFF","Light2":"#DFDCB7","Accent1":"#A9A57C","Accent2":"#9CBEBD","Accent3":"#D2CB6C","Accent4":"#8064A2","Accent5":"#C89F5D","Accent6":"#B1A089","MajorFontFamily":"Verdana","MinorFontFamily":"Georgia"},{"Id":"Clarity.rdlx-theme","Title":"Clarity","Dark1":"#292934","Dark2":"#D2533C","Light1":"#FFFFFF","Light2":"#F3F2DC","Accent1":"#93A299","Accent2":"#AD8F67","Accent3":"#726056","Accent4":"#4C5A6A","Accent5":"#808DA0","Accent6":"#79463D","MajorFontFamily":"Tahoma","MinorFontFamily":"Palatino Linotype"},{"Id":"Cool.rdlx-theme","Title":"Cool","Dark1":"#000000","Dark2":"#46464A","Light1":"#FFFFFF","Light2":"#E3DCCF","Accent1":"#6F6F74","Accent2":"#A7B789","Accent3":"#BEAE98","Accent4":"#92A9B9","Accent5":"#9C8265","Accent6":"#8D6974","MajorFontFamily":"Lucida Sans Unicode","MinorFontFamily":"Book Antiqua"},{"Id":"Cordial.default.rdlx-theme","Title":"Cordial.default","Dark1":"#000000","Dark2":"#09213B","Light1":"#FFFFFF","Light2":"#D5EDF4","Accent1":"#2C7C9F","Accent2":"#244A58","Accent3":"#E2751D","Accent4":"#FFB400","Accent5":"#7EB606","Accent6":"#C00000","MajorFontFamily":"Arial","MinorFontFamily":"Times New Roman"},{"Id":"Cosmo.rdlx-theme","Title":"Cosmo","Dark1":"#58585A","Dark2":"#000000","Light1":"#FFFFFF","Light2":"#ABACAD","Accent1":"#008FC5","Accent2":"#7BC143","Accent3":"#005568","Accent4":"#00498B","Accent5":"#0098A1","Accent6":"#F5F5F5","MajorFontFamily":"Calibri","MinorFontFamily":"Calibri"},{"Id":"Deep.rdlx-theme","Title":"Deep","Dark1":"#000000","Dark2":"#2B142D","Light1":"#FFFFFF","Light2":"#C3AFCC","Accent1":"#663366","Accent2":"#330F42","Accent3":"#666699","Accent4":"#999966","Accent5":"#F7901E","Accent6":"#A3A101","MajorFontFamily":"Verdana","MinorFontFamily":"Georgia"},{"Id":"Grays.rdlx-theme","Title":"Grays","Dark1":"#000000","Dark2":"#000000","Light1":"#FFFFFF","Light2":"#F8F8F8","Accent1":"#DDDDDD","Accent2":"#B2B2B2","Accent3":"#969696","Accent4":"#808080","Accent5":"#5F5F5F","Accent6":"#4D4D4D","MajorFontFamily":"Tahoma","MinorFontFamily":"Palatino Linotype"},{"Id":"Handsome.rdlx-theme","Title":"Handsome","Dark1":"#000000","Dark2":"#564B3C","Light1":"#FFFFFF","Light2":"#ECEDD1","Accent1":"#93A299","Accent2":"#CF543F","Accent3":"#B5AE53","Accent4":"#848058","Accent5":"#E8B54D","Accent6":"#786C71","MajorFontFamily":"Lucida Sans Unicode","MinorFontFamily":"Book Antiqua"},{"Id":"Northwest.rdlx-theme","Title":"Northwest","Dark1":"#000000","Dark2":"#D1282E","Light1":"#FFFFFF","Light2":"#C8C8B1","Accent1":"#7A7A7A","Accent2":"#F5C201","Accent3":"#526DB0","Accent4":"#989AAC","Accent5":"#DC5924","Accent6":"#B4B392","MajorFontFamily":"Arial","MinorFontFamily":"Times New Roman"},{"Id":"Placid.rdlx-theme","Title":"Placid","Dark1":"#000000","Dark2":"#646B86","Light1":"#FFFFFF","Light2":"#D5EDF4","Accent1":"#D16349","Accent2":"#CCB400","Accent3":"#8CADAE","Accent4":"#8C7B70","Accent5":"#8FB08C","Accent6":"#D19049","MajorFontFamily":"Verdana","MinorFontFamily":"Georgia"},{"Id":"Reels.rdlx-theme","Title":"Reels","Dark1":"Black","Dark2":"#3184BD","Light1":"White","Light2":"#F4F9FF","Accent1":"#6d91d0","Accent2":"#e8ae4b","Accent3":"#e6e84b","Accent4":"#c5e84b","Accent5":"#e6ab56","Accent6":"#a1e2e2","MajorFontFamily":"Tahoma","MinorFontFamily":"Tahoma"},{"Id":"Seabreeze.rdlx-theme","Title":"Seabreeze","Dark1":"#000000","Dark2":"#242852","Light1":"#FFFFFF","Light2":"#ACCBF9","Accent1":"#629DD1","Accent2":"#297FD5","Accent3":"#7F8FA9","Accent4":"#4A66AC","Accent5":"#5AA2AE","Accent6":"#9D90A0","MajorFontFamily":"Tahoma","MinorFontFamily":"Palatino Linotype"},{"Id":"Summertime.rdlx-theme","Title":"Summertime","Dark1":"#000000","Dark2":"#434342","Light1":"#FFFFFF","Light2":"#CDD7D9","Accent1":"#797B7E","Accent2":"#F96A1B","Accent3":"#08A1D9","Accent4":"#7C984A","Accent5":"#C2AD8D","Accent6":"#506E94","MajorFontFamily":"Lucida Sans Unicode","MinorFontFamily":"Book Antiqua"},{"Id":"Wind.rdlx-theme","Title":"Wind","Dark1":"#2F2B20","Dark2":"#675E47","Light1":"#FFFFFF","Light2":"#DFDCB7","Accent1":"#A9A57C","Accent2":"#9CBEBD","Accent3":"#D2CB6C","Accent4":"#8064A2","Accent5":"#C89F5D","Accent6":"#B1A089","MajorFontFamily":"Arial","MinorFontFamily":"Times New Roman"}]'
    return JsonResponse(json.loads(list), safe=False);
def save_report_content(request):
    if request.method == 'POST':
        name = request.GET.get('name')
        if 'isTemporary' in request.GET:
            isTemporary = request.GET.get('isTemporary') == 'true'
            if isTemporary:
                pwd=os.path.dirname(__file__)
                report_path = pwd + "/reports/$temp_7d9df2a4-7685-4405-81d2-527106109e44.rdlx/content.json"
                os.makedirs(pwd + "/reports/$temp_7d9df2a4-7685-4405-81d2-527106109e44.rdlx", exist_ok=True)
                with open(report_path, 'wb') as report_file:
                    report_file.write(request.body)
            return JsonResponse({"Id":"$temp_7d9df2a4-7685-4405-81d2-527106109e44.rdlx"})
        else:
            return JsonResponse({"id":"test"})
    return JsonReponse()
def get_report_content(request, report_name):
    if request.method == 'GET':
        pwd=os.path.dirname(__file__)
        report_path = pwd + "/reports/" + report_name + "/content.json"
        with open(report_path) as report_file:
            data = json.load(report_file);
            return JsonResponse(data, safe=False);
        return JsonResponse()
    elif request.method == 'POST':
        name = request.GET.get('name')
        if 'isTemporary' in request.GET:
            isTemporary = request.GET.get('isTemporary') == 'true'
            return JsonReponse({"Id":"$temp_7d9df2a4-7685-4405-81d2-527106109e44.rdlx"})
        else:
            return JsonReponse({"id":"test"})
    return JsonReponse()
def get_datasets_list(request):
        pwd=os.path.dirname(__file__)
        dataset_list_path = pwd + "/reports/datasets/list.json"
        with open(dataset_list_path) as dataset_list_file:
            data = json.load(dataset_list_file);
            return JsonResponse(data, safe=False);
        return JsonResponse()

def get_dataset_content(request, dataset_name):
        pwd=os.path.dirname(__file__)
        dataset_content_path = pwd + "/reports/datasets/"+ dataset_name + "/content.json"
        with open(dataset_content_path) as dataset_content_file:
            data = json.load(dataset_content_file);
            return JsonResponse(data, safe=False);
        return JsonResponse()
def preview_report(request, report_name):
    return render(request, 'PMIS/report_preview.html', {'report_id': report_name})

def get_report_info(reqport, report_name):
    data = '{"name":"未命名","galleyModeAllowed":true,"parameters":[],"exports":["Doc","Docx","Pdf","Xlsx","Csv","Json","Xml","Tiff"],"displayType":"Page","sizeType":"Default"}'
    return JsonResponse(json.loads(data), safe=False)

def get_appraisal(request):
    name = request.GET.get('name')
    data = models.Goalmaster.objects.filter(Q(period = '2020-1') & Q(contact = name)).all()
    data = list(data.values())
    return JsonResponse(data, safe=False)