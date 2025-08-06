from django.shortcuts import render
from django.forms.models import model_to_dict
from django.template import loader
from django.http import HttpResponse,JsonResponse
from django.db.models import Sum,Count,Max,Min,Avg,Q
from DataBase_MPMS.models import Queryfilter 
# from PMIS import forms
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from datatableview import Datatable
from django.db import connections
from datatableview.views import MultipleDatatableView
from datatableview.views.legacy import LegacyDatatableView
from datatableview import helpers
import datetime
import re
from BaseProject.tools import DateTools
import random



def get_query_filter(id):
    '''
    功能描述：根據查詢條件的id獲取查詢條件的queryset
    '''
    query_filter = Queryfilter.objects.values('qf013').get(qf025=id)
    str_filter = query_filter['qf013']
    str_filter = convertDate(str_filter)
    str_filter = handlePercent(str_filter)
    str_filter = analyzeQueryFilter(str_filter)
    return str_filter

def handlePercent(result):
    '''
    功能描述：處理百分號
    '''
    locate = result.find('%')
    if locate >= 0:
        result = result.replace('%', '%%')
    return result


def convertDate(result):
    '''
    功能描述：把查詢條件中定義的變量替換成相應的日期
    '''
    if not result:
        return result
    locate = result.find('2000/')
    if locate >= 0: #判斷SQL語句中是否有"2000/06/01"
        Month = result[locate + 5:locate + 7]
        SourDate = ""
        BeginDate = ""
        if Month.strip() == '6/' or Month.find("/") >= 0: # 判斷日期格式是否為"2000/06/01" 或"2006/6/1"
            Month = Month[0:1]
            BeginDate = "2000/6/1"
            if (not result[locate + 8: locate + 9].strip() == "/") and (not result[locate + 8: locate + 9].strip() == "'"):
                SourDate = result[locate:locate + 9]
            else:
                SourDate = result[locate:locate + 8]
        else:
            BeginDate = "2000/06/01"
            SourDate = result[locate: locate + 10]
        CurDay = datetime.datetime.now().strftime('%Y/%m/%d')
        if SourDate == BeginDate:
            result = result.replace(SourDate, CurDay)
        else: #將字符轉換為日期,以便計算出一個日期相差的天數
            ADate = datetime.datetime.strptime(SourDate, "%Y/%m/%d")
            BDate = datetime.datetime.strptime(BeginDate, "%Y/%m/%d")
			#如果月份大於6月則查詢當天以後的任務否則查詢當天以前的任務
            if int(Month) >= 6:
                day = ADate - BDate
                day = day.days
                result = result.replace(SourDate, (datetime.datetime.now() + datetime.timedelta(days=day)).strftime('%Y/%m/%d'))
            else:
                day = BDate - ADate
                day = -1 * day.days
                result = result.replace(SourDate, (datetime.datetime.now() + datetime.timedelta(days=day)).strftime('%Y/%m/%d'))
        if result.find("2000") >= 0: # 判斷SQL語句中是否還有未替換的日期
            result = convertDate(result)
    return result


def analyzeQueryFilter(queryFilter, doubleSeparate=False):
    '''
    功能描述：分析查詢條件
    '''
    separate = "'"
    if doubleSeparate:
        separate = "''"
    if queryFilter:
        if re.search('QUARTERLY', queryFilter, re.IGNORECASE):
            queryFilter = checkParameter(queryFilter, 'QUARTERLY', separate)
        if re.search('WEEKLY', queryFilter, re.IGNORECASE):
            queryFilter = checkParameter(queryFilter, 'WEEKLY', separate)
        if re.search('DAY', queryFilter, re.IGNORECASE):
            queryFilter = checkParameter(queryFilter, 'DAY', separate)
    return queryFilter

def checkParameter(queryFilter, type, separate):
    '''
    功能描述：處理查詢條件中的QUARTERLY,WEEKLY,Day
    '''
    startWeeklyStep = -1
    endWeeklyStep = -1
    startDate = ""
    endDate = ""   
    regex = "(((AND)|(OR))*\\s*\\("+type+"\\s*=\\s*([-]*\\d+)\\))|(((AND)|(OR))*\\s*\\("+type+"\\s+BETWEEN\\s+([-]*\\d+)\\s+AND\\s+([-]*\\d+)\\))|(((AND)|(OR))*\\s*\\("+type+"\\s*([><]=)\\s*([-]*\\d+)\\))"
    iter = re.finditer(regex, queryFilter, re.IGNORECASE)
    for match in iter:
        print('aaa')
        if match.group(12) and (match.group(12).find('>') >= 0 or match.group(12).find('<') >= 0): # 查詢條件Weekly >= 1 或Weekly < 1模式
            startWeeklyStep = int(match.group(17))
            if type == 'QUARTERLY':
                startDate = DateTools.format(DateTools.getSeasonFirstTime(startWeeklyStep))
                endDate = DateTools.format(DateTools.getSeasonFinallyTime(startWeeklyStep))
            elif type == 'WEEKLY':
                startDate = DateTools.format(DateTools.addDay(DateTools.getBeginOfWeek(datetime.datetime.now()), startWeeklyStep * 7))
                endDate = DateTools.format(DateTools.addDay(DateTools.getEndOfWeek(datetime.datetime.now()), startWeeklyStep * 7))
            elif type == 'DAY':
                if startWeeklyStep > 0:
                    startDate = DateTools.format(DateTools.addDay(datetime.datetime.now(), startWeeklyStep))
                else:
                    endDate = DateTools.format(DateTools.addDay(datetime.datetime.now(), startWeeklyStep))
            if match.group(16) == '>':
                queryFilter = queryFilter[0: queryFilter.find(match.group(12))] + match.group(14) + ' (PlanBDate ' + match.group(16) + ' ' +  separate + startDate + separate + ')' + queryFilter[queryFilter.find(match.group(12)) + len(match.group(12)):]
            else:
                queryFilter = queryFilter[0: queryFilter.find(match.group(12))] + match.group(14) + ' (PlanBDate ' + match.group(16) + ' ' +  separate + endDate + separate + ')' + queryFilter[queryFilter.find(match.group(12)) + len(match.group(12)):]
        elif match.group(1) and match.group(1).find('=') >= 0: #查詢條件Weekly = 0模式
            startWeeklyStep = int(match.group(5))
            if type == 'QUARTERLY':
                startDate = DateTools.format(DateTools.getSeasonFirstTime(startWeeklyStep))
                endDate = DateTools.format(DateTools.getSeasonFinallyTime(startWeeklyStep))
            elif type == 'WEEKLY':
                startDate = DateTools.format(DateTools.addDay(DateTools.getBeginOfWeek(datetime.datetime.now()), startWeeklyStep * 7))
                endDate = DateTools.format(DateTools.addDay(DateTools.getEndOfWeek(datetime.datetime.now()), startWeeklyStep * 7))
            elif type == 'DAY':
                if startWeeklyStep > 0:
                    startDate = DateTools.format(DateTools.addDay(datetime.datetime.now(), startWeeklyStep))
                else:
                    endDate = DateTools.format(DateTools.addDay(datetime.datetime.now(), startWeeklyStep))
            str_g = ''
            if match.group(3):
                str_g = match.group(3)
            queryFilter = queryFilter[0:queryFilter.find(match.group(1))] + str_g + ' ((PlanBDate >= '+separate+startDate+separate+' AND PlanBDate <= ' + separate+endDate+separate + ") OR (PlanEDate >= "+separate+startDate+separate+" AND PlanEDate <= "+separate+endDate+separate+"))" + queryFilter[queryFilter.find(match.group(1)) + len(match.group(1)):]
        elif match.group(6) and match.group(6).find("BETWEEN") >= 0: #查詢條件Weekly Betwween -1 AND 1模式
            startWeeklyStep = int(match.group(10))
            endWeeklyStep = int(match.group(11))
            if type == 'QUARTERLY':
                startDate = DateTools.format(DateTools.getSeasonFirstTime(startWeeklyStep))
                endDate = DateTools.format(DateTools.getSeasonFinallyTime(endWeeklyStep))
            elif type == 'WEEKLY':
                startDate = DateTools.format(DateTools.addDay(DateTools.getBeginOfWeek(datetime.datetime.now()), startWeeklyStep * 7))
                endDate = DateTools.format(DateTools.addDay(DateTools.getEndOfWeek(datetime.datetime.now()), endWeeklyStep * 7))
            elif type == 'DAY':
                if startWeeklyStep > 0:
                    startDate = DateTools.format(DateTools.addDay(datetime.datetime.now(), startWeeklyStep))
                else:
                    endDate = DateTools.format(DateTools.addDay(datetime.datetime.now(), startWeeklyStep))            
            queryFilter = queryFilter[0:queryFilter.find(match.group(6))]+match.group(8)+" ((PlanBDate >= "+separate+startDate+separate+" AND PlanBDate <= "+separate+endDate+separate+") OR (PlanEDate >= "+separate+startDate+separate+" AND PlanEDate <= "+separate+endDate+separate+"))"+queryFilter[queryFilter.find(match.group(6))+ len(match.group(6)):]
    return queryFilter
