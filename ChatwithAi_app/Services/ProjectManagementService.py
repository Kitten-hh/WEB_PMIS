from DataBase_MPMS.models import Requirement, Syspara, VTask,VTasklist
from .OpenaiBaseService import OpenAiBaseService,OpenAIException
from ..models import Aisummaryrecord
from BaseApp.library.tools import DateTools,SWTools
from django.db.models import Sum,Count,Max,Min,Avg,Q
import json
import os
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
import copy

class ProjectManagementService(OpenAiBaseService):
    def summaryProjectStatus(self, recordid, sessionids):
        """
        功能描述：使用ai匯總多個ProjectStatus的進度
        """
        qs = Syspara.objects.values('fvalue').filter(ftype='ProjectStatusSysRole', nfield="Summary").order_by("nfield")
        system_role_content = "你是一個概括總結信息的工程師，我會給你多個模塊的進度信息，你需要幫我將總結所有事情的進度。"
        if len(qs) > 0:
            system_role_content = qs[0]['fvalue']
        messages = [
            {"role": "system", "content": system_role_content}
        ]
        qs = Syspara.objects.values('fvalue').filter(ftype='SummaryProjectStatusQuestion').order_by("nfield")
        questions = [item['fvalue'] for item in qs]        

        result = []
        formatted_sessionids = ','.join([f"'{x}'" for x in sessionids])
        project_status_qs = Aisummaryrecord.objects.filter(recordid=recordid)\
            .extra(where=[f"CAST(sessionids AS varchar(max)) IN ({formatted_sessionids}) and id = (Select max(id) from AiSummaryRecord A where AiSummaryRecord.recordid = A.recordid and convert(varchar(200),AiSummaryRecord.sessionids) = convert(varchar(200),A.sessionids))"])
        session_qs = VTasklist.objects.values("sessionid","sdesp").filter(sessionid__in=sessionids)
        session_dict = {row['sessionid']:row['sdesp'] for row in session_qs}
        
        project_status_content = ""
        for row in project_status_qs:
            sessionid = row.sessionids
            desp = session_dict.get(sessionid, "")
            project_status = row.aisummary
            if project_status_content:
                project_status_content += f"\n{sessionid}:{desp}\n{project_status}"
            else:
                project_status_content += f"{sessionid}:{desp}\n{project_status}"
        
        messages.append({"role":"user", "content":f"以下是多个Session的进度总结：\n{project_status_content}"})
        result = ""
        temp_messages = messages.copy()
        for question in questions:
            temp_messages.append({"role": "user", "content": question})
            if result:
                result += self.processMessageToChatGPT(temp_messages)
            else:
                result = self.processMessageToChatGPT(temp_messages)
        #保存Ai分析結果信息到數據表
        maxId = Aisummaryrecord.objects.aggregate(Max('id'))['id__max']
        maxId = (maxId or 0) + 10
        record = Aisummaryrecord(
            id=maxId,
            createdat=DateTools.now(), 
            recordid=recordid, 
            sessionids=','.join(sessionids),
            aisummary=result)
        record.save()
        return record.inc_id
    
    def getProjectStatus(self, recordid, sessionids):
        """
        功能描述：使用ai獲取sessionids裏所有Session的進度
        """
        qs = Syspara.objects.values('fvalue').filter(ftype='ProjectStatusQuestion').order_by("nfield")

        questions = [item['fvalue'] for item in qs]
        """
        questions = [
            "Based on the requirement and the tasks given, have we met our goal and can the system be used realistically, if not, we need to be done immediately?",
            "Can you show me not finish class one tasks?",
            "Could you base on the outstanding just given and also the requirement and the tasks of the session, just give me a very brief status of this session?",
        ]
        """
        messages = [
            {"role": "system", "content": """Please answer my question in Chinese,
                Outstanding Task Explanation:
                    Outstanding Task refers to tasks with the Progress(進度) other than C (Completed) or F (Finished).                
                The data format includes the following fields:
                    1. **TaskNo (任務編號)**: A unique identifier for the task.
                    2. **Contact (聯繫人)**: The name or code of the responsible or related contact person.
                    3. **Task (任務描述)**: A brief description of the task content.
                    4. **PlanBDate (計畫日期)**: The planned start or completion date of the task.
                    5. **Progress (進度)**: The current progress status of the task,where:
                        N: New task
                        I: Task in progress
                        T: Today Task
                        S: Task started
                        C: Completed
                        F: Finished
                        R: Review
                    6. **Class (分類)**: Indicates whether the task is a critical task(class 1 task) (e.g., 'class1').

                    ### Example Data Entry

                    ```
                    00300-21010-1290 qfq 把深圳庫存請求相應的操作介面截圖出來 2023-03-06 C class1
                    ```

                    ### Explanation of the Example Data Entry

                    - **TaskNo**: 00300-21010-1290
                    - **Contact**: qfq
                    - **Task**: 把深圳庫存請求相應的操作介面截圖出來
                    - **PlanBDate**: 2023-03-06
                    - **Progress**: C
                    - **Class**: class1

                    Use this format for inputting and tracking tasks, ensuring clarity and consistency in task management. The **Class** field helps prioritize the most urgent tasks."""},
        ]
        result = []
        """
        allSessions = []
        for sessionid in sessionids:
            relationSessions = self.getRelationShip(sessionid)
            allSessions += [sessionid] + relationSessions
        allSessions = ['00900-51520']
        """
        for sessionid in sessionids:
            projectStatus = []
            requirement = self.getSessionRequement(sessionid)
            tasks = self.getSessionTask(sessionid)
            tempMessage = messages.copy()
            tempMessage += [
                {"role":"user", "content":"What’s the requirements for {0}?".format(sessionid)},
                {"role":"assistant", "content":requirement},
                {"role":"user", "content":"What are the tasks for {0}?".format(sessionid)},
                {"role":"assistant", "content":tasks}
            ]
            for question in questions:
                tempMessage.append({"role":"user","content":question})
                aiResult = self.processMessageToChatGPTWithTools(tempMessage, sessionid)
                tempMessage.append({"role":"assistant", "content":aiResult})
                projectStatus.append({"question":question, "result":aiResult})
            result.append({"sessionid":sessionid, "results":projectStatus})
        #record = self.saveAiSummaryRecord(recordid, allSessions, result)
        record = self.saveAiSummaryRecord(recordid, sessionids, result)
        return record.inc_id


    def processMessageToChatGPTWithTools(self, messages, sessionid):        
        http_methods = {}
        apiBody =  copy.deepcopy(OpenAiBaseService.defaultApiBody)
        apiBody['messages'] = messages
        apiBody['tools'] = [
            {
                "type": "function",
                "function": {
                    "name": "get_unfinish_critical_tasks",
                    "description": "get the not finish class 1 tasks",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "unfinish": {
                                "type": "string",
                                "description": "Check if 'not finish' or 'not complete' is mentioned in the question. If it is, return true; if not, return false.",
                                "enum":["true","false"]
                            },
                            "class1":{
                                "type":"string",
                                "description":"Check if 'class one' or 'critical task' is mentioned in the question. If it is, return true; if not, return false.",
                                "enum":["true","false"]                        
                            }
                        },
                        "required": ["unfinish","class1"]
                    }
                }        
            },
        ]
        http_methods['data'] = {**OpenAiBaseService.baseParams,"params":apiBody}        
        try:                    
            response = self.async_fetch_http_json(http_methods)
        except Exception as e:
            raise OpenAIException("調用Open AI失敗")
        if ('tool_calls' in response['data']['choices'][0]['message']):
            funcs = response['data']['choices'][0]['message']['tool_calls']
            for f in funcs:
                func_name = f['function']['name'];
                args = f['function']['arguments'];
                args = json.loads(args)
                if func_name == 'get_unfinish_critical_tasks':
                    unfinish = args['unfinish']
                    class1 = args['class1']
                    tasks = self.getSessionTask(sessionid, class1, unfinish)
                    if not tasks:
                        tasks = "There are no more Critical Tasks (Class 1 tasks) in this project."
                    messages.append(response['data']['choices'][0]['message']),
                    messages.append(
                        {
                            "tool_call_id": f['id'],
                            "role": "tool",
                            "name": func_name,
                            "content": tasks,                            
                        }
                    )                    
            return self.processMessageToChatGPT(messages)
        else:
            content = response['data']['choices'][0]['message']['content']
            return content;    

    def getRelationShip(self, sessionid):
        qs = Syspara.objects.values('fvalue').filter(ftype='ProjectStatus_RelationShip', nfield=sessionid)
        sessions = []
        if len(qs) > 0 and qs[0]['fvalue']:
            sessions = qs[0]['fvalue'].split(",")
        return sessions

    def saveAiSummaryRecord(self, recordid, sessionids, result):
        maxId = Aisummaryrecord.objects.aggregate(Max('id'))['id__max']
        maxId = (maxId or 0) + 10
        record = Aisummaryrecord(
            id=maxId,
            createdat=DateTools.now(), 
            recordid=recordid, 
            sessionids=','.join(sessionids),
            aisummary=self.getAiSummary(result))
        record.save()
        return record

    def getAiSummary(self, mutilSessionResults):
        summary = ""
        for item in mutilSessionResults:
            sessionid = item['sessionid']
            sessionResult = item['results']
            for index,singleResult in enumerate(sessionResult):
                question = f"""Question {index + 1}: {singleResult['question']}"""
                result = singleResult['result']
                if summary == "":
                    summary = question
                else:
                    summary += "\r\n{0}".format(question)
                summary += "\r\n{0}".format(result)
                summary += "\r\n"
        return summary
                    

    def getSessionRequement(self, sessionid):
        qs = Requirement.objects.filter(rid=sessionid)[:1]
        content = ""
        if len(qs) > 0:
            requirement = qs[0]
            if requirement.purpose:
                content += "***Purpose***\n{0}\n".format(requirement.purpose)
            if requirement.feature:
                content += "***Feature***\n{0}\n".format(requirement.feature)
            if requirement.fr:
                content += "***Functional Requirement***\n{0}\n".format(requirement.fr)
        else:
            content = "the requirement is empty!"
        return content
    
    def getSessionTask(self, sessionId, class1=None, unfinish=None):
        sessArr = sessionId.split('-')
        qs = VTask.objects.values('taskno','contact','task','planbdate','progress','remark','class_field').filter(pid = sessArr[0], tid = sessArr[1])
        if class1 == "true":
            qs = qs.filter(class_field=1)
        if unfinish == "true":
            qs = qs.filter(~Q(progress__in=['C','F']))
        content = ""
        for task in qs:
            remark = "" if not task['remark'] else f"Remark:{task['remark']}"
            if content == "":
                content = "{0} {1} {2} {3} {4} {5}".\
                    format(task['taskno'], task['contact'], task['task'], remark,  \
                    'null' if not task['planbdate'] else DateTools.formatf(task['planbdate'], '%Y-%m-%d'), task['progress'], 
                    'null' if not task['class_field'] and task['class_field'] != 1 else 'class1')
            else:
                content += "\n{0} {1} {2} {3} {4} {5}".\
                    format(task['taskno'], task['contact'], task['task'],remark, \
                    'null' if not task['planbdate'] else DateTools.formatf(task['planbdate'], '%Y-%m-%d'), task['progress'],
                    'null' if not task['class_field'] and task['class_field'] != 1 else 'class1')

        return content