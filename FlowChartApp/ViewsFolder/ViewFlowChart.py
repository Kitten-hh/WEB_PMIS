from shutil import ExecError
from django.shortcuts import render
from django.template import loader
from django.http import HttpRequest, HttpResponse,JsonResponse
from sympy import false
from ..models import Flowchart, Flowchart_Bak, Docdesign
from django.forms.models import model_to_dict
from BaseApp.library.cust_views.DatatablesServerSideView import DatatablesServerSideView
import xmltodict
import json

def convertFlashToGojs(request:HttpRequest):
    result = {'status':False, 'msg':'', 'data':None}
    flowChartNo = request.POST.get('flowChartNo');
    content = request.POST.get('content')
    try:
        rs = Flowchart.objects.filter(flowchartno = flowChartNo)
        if len(rs) > 0:
            rs[0].content = content
            rs[0].save()
            result['status'] = True
    except Exception as e:
        print(str(e))
    return JsonResponse(result, safe=False)
        

def get_source_flowchart(request:HttpRequest):
    result = {'status':False, 'msg':'', 'data':None}
    try:
        flowChartNo = request.GET.get("flowChartNo")
        format = request.GET.get("format","")
        sysid = request.GET.get("sysid")
        if flowChartNo:
            rs = Flowchart_Bak.objects.values('flowchartno','title','description','parentno','version','fc050','fc051','fc057','modifier','modi_date','content').filter(flowchartno = flowChartNo)
        elif sysid:
            rs = Flowchart_Bak.objects.values('flowchartno','title','description','parentno','version','fc050','fc051','fc057','modifier','modi_date','content').filter(fc051__in = ['system','module'], fc050 = sysid)
        if len(rs) > 0:
            result['status'] = True
            flowchartdata = rs[0]['content']
            if format and format=="json":
                flowchartdata = xmltojson(flowchartdata)
            result['data'] = {'flowchartinfo':{key:value for key,value in rs[0].items() if key != 'content'}, 'flowchartdata':flowchartdata}
            json.dumps(obj)
    except Exception as e:
        print(str(e))
    return JsonResponse(result, safe=False)

def xmltojson(xmlStr):
    def clean_nones(value):
        if isinstance(value, list):
            return [clean_nones(x) for x in value if x != "" and x is not None]
        elif isinstance(value, dict):
            return {key: clean_nones(val) for key, val in value.items() if val != "" and val is not None}
        else:
            return value
    xml_dict = xmltodict.parse(xmlStr, attr_prefix='')
    new_xml_dict = clean_nones(xml_dict)
    return json.dumps(new_xml_dict)


def get_flowchart_data(request:HttpRequest):
    result = {'status':False, 'msg':'', 'data':None}
    try:
        flowChartNo = request.GET.get("flowChartNo")
        sysid = request.GET.get("sysid")
        if flowChartNo:
            rs = Flowchart.objects.values('content', 'flowchartno').filter(flowchartno = flowChartNo)
        elif sysid:
            rs = Flowchart.objects.values('content', 'flowchartno').filter(fc051__in = ['system','module'], fc050 = sysid)
        if len(rs) > 0:
            result['status'] = True
            result['data'] = {'flowchartno':rs[0]['flowchartno'], 'content':rs[0]['content']}
    except Exception as e:
        print(str(e))
    return JsonResponse(result, safe=False)

def get_source_flowchart_desc(request:HttpRequest):
    result = {'status':False, 'msg':'', 'data':None}
    try:
        flowChartNos_str = request.GET.get("flowChartNos")
        flowChartNos = flowChartNos_str.split(",")
        rs = Flowchart_Bak.objects.values('flowchartno','description').filter(flowchartno__in = flowChartNos)
        if len(rs) > 0:
            result['status'] = True
            result['data'] = [{'value':item['flowchartno'], 'label':item['description']} for item in rs]
    except Exception as e:
        print(str(e))
    return JsonResponse(result, safe=False)



class DocdesignTableView(DatatablesServerSideView):
    model = Docdesign
    columns = [field.name for field in Docdesign._meta.fields]
    searchable_columns = columns
