from .. import models
import re
from .PromptSqlService import PromptSqlService, PromptSqlName
#from . import Data
from BaseApp.library.tools import DateTools,ModelTools
from DataBase_MPMS.models import Task,Tasklist, VTasklist,Docma
from PMIS.Services.SessionService import SessionService
from PMIS.Services.TaskService import TaskService
from django.db import connections,transaction
from django.db.models import Sum,Count,Max,Min,Avg,Q
from django.utils.translation import ugettext_lazy as _
import json

class TaskForAIService:
    promptSqlService = PromptSqlService()
    destRecordId = '00511'
    def expandPromptData(self, promptText):
        promptText,sessionid = self.analysisPromptText(promptText)
        return promptText,sessionid
    
    def _getPromptText(self, topicid, cid, pid):
        qs = models.Prompttbl.objects.get(topicid=topicid, cid=cid, pid=pid)
        return qs.prompt
    
    def analysisPromptText(self, promptText):
        recordId = self._analysisProject(promptText)
        sessionDesp = self._analysisSessionDesp(promptText)
        taskNo = self._analysisTaskNo(promptText)
        if sessionDesp and recordId:
            session = self.promptSqlService.getData(PromptSqlName.GetURSessionWithName.value, {"RecordId":recordId, "SDesp":"%%{0}%%".format(sessionDesp)})
            if session and taskNo:
                sessionid = session[0]['sessionid']
                newTaskNo = "{0}-{1}".format(sessionid, taskNo.split("-")[2])
                promptText = promptText.replace(taskNo, newTaskNo)
                if re.search("schedule", promptText, re.IGNORECASE) and re.search("goal", promptText, re.IGNORECASE):
                    fr = self.promptSqlService.getData(PromptSqlName.UserRequirementForSession.value, {"RID":sessionid})
                    if fr:
                        fr = fr[0]['fr']
                        promptText = "{0} {1}".format(promptText, fr)
        return promptText,sessionid

    
    def _analysisProject(self, promptText):
        regex = "Project\\s*\\(([^)]+)\\)"
        match = re.search(regex, promptText, re.IGNORECASE)
        if match:
            return match.group(1)
        else:
            return ""

    def _analysisSessionDesp(self, promptText):
        regex = "User\\s+Requirement\\s+for\\s+(.*?)\\s+to"
        match = re.search(regex, promptText, re.IGNORECASE)
        if match:
            return match.group(1)
        else:
            return ""

    def _analysisTaskNo(self, promptText):
        regex = "\\((\d+-\d+-[x]+)\\)"
        match = re.search(regex, promptText, re.IGNORECASE)
        if match:
            return match.group(1)
        else:
            return ""

    def generateTaskWithAiResult(self, resulStr, parentSessionId, sessionid,request):
        #Month 2: November 2023
        if parentSessionId:
            arr = parentSessionId.split('-')
            pid = arr[0]
            tid = arr[1]
            session = Tasklist.objects.get(pid=pid, tid=tid)
            session,sessionExist = self.generateSession(session, request)
        else:
            arr = sessionid.split('-')
            pid = arr[0]
            tid = arr[1]
            session = Tasklist.objects.get(pid=pid, tid=tid)
            sessionExist = True
        """
        regex = "Month\\s+\d+:\\s*(.*?)(\d+)"
        iter = re.finditer(regex, resultStr, re.IGNORECASE)
        monthMap = {}
        for match in iter:
            monthMap[match.group(1)] = match.group(2)
        regex = "\\((\d+-\d+\d+\\)\\s*Task:(.*?)Schedule\\s+Date:\\s*(.*?)(\d+)(rd|td)"
        iter = re.finditer(regex, resultStr, re.IGNORECASE)"""
        taskIter = resulStr.split("\n")
        tasks = []
        maxTaskId = 0
        taskDate = DateTools.now()
        for taskStr in taskIter:   
            taskStr = taskStr.strip()
            if taskStr == "":
                continue
            task = Task()
            task.pid = session.pid
            task.tid = session.tid
            task.task = taskStr
            if maxTaskId == 0:
                maxTaskId = TaskService.get_max_taskid(task.pid, task.tid)
            else:
                maxTaskId += 10
            task.taskid = maxTaskId
            task.contact = request.user.username
            task.progress = 'N'
            task.planbdate = taskDate
            task.planedate = taskDate
            task.requestdate = taskDate
            ModelTools.set_basic_field_info(request, Task, task)
            taskDate = DateTools.addDay(taskDate, 3)
            tasks.append(task)
        if len(tasks) > 0:
            tasks.pop(0)
            
        with transaction.atomic(ModelTools.get_database(Task)):
            if not sessionExist:
                session.save()
            Task.objects.bulk_create(tasks, batch_size=20)
            
    def getSessionWithResult(self, resulStr):
        regex = "\\((\d+-\d+\d+\\)\\s*Task:(.*?)Schedule\\s+Date:\\s*(.*?)(\d+)(rd|td)"
        matchIter = re.finditer(regex, resultStr, re.IGNORECASE)
        if len(matchIter) > 0:
            taskNo = matchIter[0].group(1)
            arr = taskNo.split('-')
            pid = arr[0]
            tid = arr[1]
            session = Tasklist.objects.get(pid=pid, tid=tid)
            return session
        return None

    def generateSession(self, oldSession, request):
        '''
        功能描述:添加Session
        '''
        ##先檢查Session是否存在
        sessionDesp = oldSession.sdesp
        oldSessionId = "{0}-{1}".format(oldSession.pid, int(oldSession.tid))
        qs = VTasklist.objects.filter(recordid=self.destRecordId, parent=oldSessionId)
        if len(qs) > 0:
            return qs[0], True
        session = Tasklist()
        session.progress = "I"
        session.planbdate = DateTools.getBeginOfQuarter(DateTools.now())
        session.planedate = DateTools.getEndOfQuarter(DateTools.now())
        session.sdesp = sessionDesp 
        session.parent = oldSessionId
        session.contact = request.user.username
        ModelTools.set_basic_field_info(request, Tasklist, session)
        type = "1" #添加在User Requement範圍
        pid,min_tid,max_tid = SessionService.get_session_range(self.destRecordId)
        if pid and (min_tid or min_tid == 0) and max_tid:
            session.pid = pid
            tid = SessionService.get_max_tid(pid, min_tid, max_tid, type)
            session.tid = tid
        return session,False

    def getActionPage(self, topicid, cid, pid, params):
        prompt = models.Prompttbl.objects.values("action").get(topicid=topicid, cid=cid, pid=pid)
        action = prompt['action']
        regex = "(\d+)->([^:]+)"
        match = re.search(regex, action)
        #TaskEnquiry_Frm#Search#(Contact LIKE 'hb')
        if match:
            recordid = match.group(1)
            frameName = match.group(2)
            qs = Docma.objects.values("ma017").filter(ma001=frameName).extra(where=["MA002 = (Select MA002 from DOCMA B where B.MA001 = DOCMA.MA001)"])
            if len(qs) > 0:
                return qs[0]['ma017']
        return ""
    def saveContentToDB(self, topicid, cid, pid, datas):
        prompt = models.Prompttbl.objects.values("action").get(topicid=topicid, cid=cid, pid=pid)
        action = prompt['action']
        if not action:
            raise Exception("No action")
        actionAttr = action.split("->")
        tableName = actionAttr[0]
        fields = actionAttr[1].split(",")
        with transaction.atomic(ModelTools.get_database(models.Prompttbl)):
            with connections[ModelTools.get_database(models.Prompttbl)].cursor() as cursor:
                for data in datas:
                    tempFields = [field+"=%s" for field in fields if field.lower() in data]
                    params = [data[field.lower()] for field in fields if field.lower() in data]
                    if not tempFields:
                        continue
                    else:
                        strSQL = "update {0} set {1} where inc_id=%s".format(tableName, ",".join(tempFields))
                        params.append(data['inc_id'])
                        cursor.execute(strSQL, params)
            
    def findIteratedPromptType(self, relation):
        #獲取Iterated Prompt 的類別
        if relation.find("-") != -1:
            sessionArr = relation.split("-")
            issession = VTasklist.objects.filter(recordid='00183',pid=sessionArr[0], tid=sessionArr[1]).exists()
            if issession:
                return 1 #Iterated Prompt 的類型為Session
        return 0

    def getIteratedPromptWithRelation(self, prompt):
        promptText = ""
        question = ""
        try:
            relation = prompt['relation']
            promptType = self.findIteratedPromptType(relation)
            prompt_questions = []
            if promptType == 1: #表示從11580的Session中獲取Iterated Prompt
                sessionArr = relation.split("-")
                pid = sessionArr[0]
                tid = sessionArr[1]
                qs = Task.objects.values("task","remark").filter(pid=pid, tid=tid).order_by("tid")                
                for index in range(len(qs)):
                    row = qs[index]
                    if index == 0:
                        #prompt = ("" if not row['task'] else row['task']) + ("" if not row['remark'] else row['remark'])
                        promptText = "" if not row['task'] else row['task']
                    else:
                        prompt_questions.append("{0}. {1}".format(index, row['task']))
                        if question == "":
                            question = "{0}. {1}".format(index, row['task'])
                        else:
                            question += "\n" + "{0}. {1}".format(index, row['task'])
                promptText = re.sub(r"Options\s*[:：]", f"Options: \n{question}", promptText, flags=re.IGNORECASE)
                prompt['predefined_prompt'] = promptText
                prompt['iterated_prompt_questions'] = prompt_questions
        except Exception as e:
            print(str(e))

    def getErrorMsgWithParam(self, paramNames):
        if "StartDate" in paramNames or "EndDate" in paramNames:
            return _("Please input a time range!")
        elif "RecordId" in paramNames:
            return _("Please input recordid!")
        elif "SessionId" in paramNames:
            return _("Please input sessionid!")
        else:
            return ""

    def convertDataToText(self, datas):
        content = ""
        for item in datas:
            item = dict(item) if type(item) != dict else item
            lineText = ""
            for key,value in item.items():
                tempValue = value
                if not tempValue:
                    tempValue = "null"
                if type(tempValue) == str:
                    tempValue = tempValue.replace("\r\n","")
                if lineText == "":
                    lineText = f"{tempValue}"
                else:
                    lineText += f" {tempValue}"
            if content == "":
                content = lineText
            else:
                content += "\r\n" + lineText
        return content