from DataBase_MPMS.models import Requirement, Syspara, VTask,VTasklist
from .OpenaiBaseService import OpenAiBaseService
from ..models import Aisummaryrecord
from BaseApp.library.tools import DateTools,SWTools
from django.db.models import Sum,Count,Max,Min,Avg,Q
import json
import os
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from BaseApp.library.tools import AsyncioTools
import re
class AiManagementService(OpenAiBaseService):
    def getAiSummary(self, topic):
        """
        功能描述：獲取某個topic對應的Ai分析結果
        """
        prompt = self.getPrompt(topic)
        iteratedPromptContent = self.getPredefinedPrompt(prompt)
        questions = prompt['iterated_prompt_questions']
        aiSummary = []
        messages = [
                {"role": "system", "content": "Please answer my question in Chinese"},
                {"role":"user", "content":iteratedPromptContent},
                {"role":"assistant", "content":"I'm ready to assist with your queries based on the detailed content provided. Please go ahead with your questions."},
        ]
        for question in questions:
            messages.append({"role":"user","content":question})
            aiResult = self.processMessageToChatGPT(messages)
            messages.append({"role":"assistant", "content":aiResult})
            aiSummary.append({"question":question, "result":aiResult})
        record = self.saveAiSummary(topic, aiSummary)
        return record.inc_id
        

    def saveAiSummary(self,topic, aiSummary):
        maxId = Aisummaryrecord.objects.aggregate(Max('id'))['id__max']
        maxId = (maxId or 0) + 10
        record = Aisummaryrecord(
            id=maxId,
            createdat=DateTools.now(), 
            chattopic=topic,
            aisummary=self.convertToText(aiSummary))
        record.save()
        return record

    def convertToText(self, aiSummary):
        summary = ""
        for item in aiSummary:
            question = item['question']
            result = item['result']
            if summary == "":
                summary = question
            else:
                summary += "\r\n{0}".format(question)
            summary += "\r\n{0}".format(result)
        return summary

    def getPrompt(self, topic):
        """
        功能描述：根據topic獲取對應的Prompt
        """
        url = "{0}/schedule/api/prompt/".format(settings.WEBPMIS_SERVER)
        http_methods = {'url':url, 'params':{'chat_topic':topic}, 'basic_auth_user':'admin','basic_auth_password':'sing11'}
        response = AsyncioTools.async_fetch_http_json({"prompt":http_methods})
        prompt = response['prompt']['results'][0]
        return prompt

    def getPredefinedPrompt(self, prompt):
        """
        功能描述：根據Prompt獲取它對應的Predefined Iterated Prompt
        """
        url = "{0}/schedule/api/get_prompt_answer_data".format(settings.WEBPMIS_SERVER)
        http_methods = {'url':url,'method':'POST', 'params':{'promptName':prompt['prompt']}, 'basic_auth_user':'admin','basic_auth_password':'sing11'}
        response = AsyncioTools.async_fetch_http_json({"data":http_methods})
        result = response['data']
        if result['status']:
            info = []
            data = result['data']
            if type(data) == str:
                data = [data]
            if len(data) == 0:
                return None
            messageText = ""
            for item in data:
                lineText = ""
                for key,value in item.items():
                    if not value:
                        continue
                    if type(value) == str:
                        value = re.sub(r'/\r/\n', '', value)
                    if lineText == "":
                        lineText = "{0}".format(value)
                    else:
                        lineText += " {0}".format(value)
                if messageText == "":
                    messageText = lineText
                else:
                    messageText += "\r\n" + lineText
            predefined_prompt = prompt['predefined_prompt']
            if predefined_prompt:
                content = '{0}\n{1}'.format(predefined_prompt, messageText)
                return content
            else:
                return None