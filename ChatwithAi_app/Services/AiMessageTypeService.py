from ..models import AiMessageType
import logging
from .AiToolsJson import ai_tools_funcs,ai_tools
from ScheduleApp.models import Promtsql
from django.conf import settings
from ..models import AiPageurls
import openai
from httpx import Client
from .ActionService import ActionService
import json

class AiMessageService:
    def __init__(self):
        # 设置代理（如果需要）；
        self.LOGGER = logging.getLogger(__name__)
        self.messageTypes = self.getMessageTypes()
        proxies = {
            "http://": settings.OPENAPI_PROXY_URL,
            "https://": settings.OPENAPI_PROXY_URL,
        } if settings.OPENAPI_PROXY_URL else None
        
        # 初始化 openai 实例
        self.api_client = openai.OpenAI(
            api_key=settings.OPENAPI_KEY,
            http_client=Client(proxies=proxies)
        )
        self.actionService = ActionService()

    def getMessageTypes(self):
        qs = AiMessageType.objects.all().order_by("id")   
        return {row.id:{"id":row.id, "name":row.message_type,"keywords":[] if not row.keywords else row.keywords.split(",")}  for row in qs}

    """
    def determineMessageType(self, message:str, message_type_id=None):
        if message_type_id:
            if message_type_id in self.messageTypes:
                return self.messageTypes[message_type_id]
            else:
                return None
        if not message:
            return None
        
        for _, message_type in self.messageTypes.items():
            keywords = message_type['keywords']
            for keyword in keywords:
                if message.lower().find(keyword.lower()) != -1:
                    return message_type
        return None
    """

    def determineAiProxyManagementType(self, user_input, question, session):
        message_type = self.getDefinedMessageType(question)
        if message_type:
            return message_type
        #message_type = self.getMessageTypeWithEmbedding(user_input, question, session)
        return None

    def getDefinedMessageType(self, question):
        if not question:
            return None
        message_type_id = question.message_type
        has_params = question.has_params
        relationid = question.message_type_relationid
        if message_type_id and relationid and message_type_id in self.messageTypes:
            message_type = self.messageTypes[message_type_id]
            if message_type_id == 1: #Pre-condition
                qs = Promtsql.objects.filter(ssid = relationid)
                if len(qs) > 0:     
                    action_id = qs[0].inc_id
                    action_name = qs[0].sname
                    chatdata_call = qs[0].action
                    message_type.update({"has_params":has_params, "actions":[{"id":action_id, "name":action_name, "chatdata_call":chatdata_call}]})
                    return message_type
            elif message_type_id == 2: #System Operation
                qs = AiPageurls.objects.filter(id = relationid)
                if len(qs) > 0:     
                    action_id = qs[0].id
                    action_name = qs[0].page_name
                    chatdata_call = None
                    message_type.update({"has_params":has_params, "actions":[{"id":action_id, "name":action_name, "chatdata_call":chatdata_call}]})
                    return message_type
            elif message_type_id == 6: #Function Calling
                    action_id = 1
                    action_name = ""
                    chatdata_call = None
                    message_type.update({"has_params":has_params, "actions":[{"id":action_id, "name":action_name, "chatdata_call":chatdata_call}]})
                    return message_type
        return None            
        
    def getMessageTypeWithEmbedding(self, user_input, question, session):
        if  question: #暫時只處理main question和sub question
            has_params = question['has_params']
            context_params = ""
            if has_params:
                context_params = json.dumps({parameter:value_obj[parameter] for parameter,value_obj in session['variables'].items()})
            
            if hasattr(question, 'question'):
                action = self.actionService.ai_identify_action(question.question, context_params, 0.65,)
            else:
                action = self.actionService.ai_identify_action(question.sub_question, context_params, 0.65)
            if action and action['type'] == "pre-condition":
                message_type = self.messageTypes[1]
                qs = Promtsql.objects.filter(inc_id = action['id'])
                if len(qs) > 0:     
                    action_id = qs[0].inc_id
                    action_name = qs[0].sname
                    chatdata_call = qs[0].action
                    message_type.update({"has_params":has_params, "actions":[{"id":action_id, "name":action_name, "chatdata_call":chatdata_call}]})
                return message_type
        return None


    def determineGeneralyMessageType(self, parameters, ai_chat_historys):
        """
        功能描述：使用ai從ai聊天記錄中獲取多個系統參數
        """
        variables = {}
        if not ai_chat_historys:
            return variables
        for param in parameters:
            value = self.get_topic_parameters(param, ai_chat_historys)
            if value:
                variables[param] = value
        return variables
    
    def get_topic_parameters(self, parameter, ai_chat_historys):
        """
        功能描述：使用AI從聊天記錄中獲取指定的參數
        :param parameter: 要提取的參數名
        :param ai_chat_historys: AI聊天記錄
        :return: 提取的參數值
        """
        
        # System role description to guide AI in parameter extraction
        messages = [
            {"role": "system", 
            "content": "You are a helpful assistant tasked with responding to user queries using structured function calls. "
                        "For each question asked, you will provide the response in a predefined data format. Ensure that the response includes key-value pairs that are easy to parse and process. "
                        "Follow the format based on the user's request, and adapt accordingly if the user specifies a different structure. "
                        "Each response must be concise, relevant, and structured to fit the requested format. "
                        "Always ensure clarity and precision in your responses, and avoid adding any extra context or explanations unless explicitly requested."
                        "If the response cannot be provided in a clear, accurate, and properly structured format, return None."
            },
        ]
        
        # If there are AI chat history, clean out "system" role messages
        last_messages = ai_chat_historys[len(ai_chat_historys) - 1]
        question = last_messages['content']
        historys = list(filter(lambda x: "role" in x and x['role'].lower() != "system", ai_chat_historys[:len(ai_chat_historys) - 1]))
        messages.extend(historys)
        
        prompt = f'if the statement is "{question}", could you use the structure call give me response with the type of statement and the {parameter}'
        messages.append({"role":"user", "content":prompt})


        result_json_schema = {
            "name": "ExtractParametersSchema",
            "schema": {
            "type": "object",
            "properties": {
                "response": {
                    "type":"string"
                },
                "type_of_statement": {
                    "type":"string"
                },
                parameter: {
                    "type": "string"
                }
            },
            "required": [parameter, "type_of_statement"]
            }
        };        
        
        response = self.api_client.chat.completions.create(
            model=settings.OPENAPI_MODEL,
            temperature=0.1,
            messages=messages,
            response_format={
                "type": "json_schema",
                "json_schema": result_json_schema
            },
        )
        

        try:
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(str(e))
        return None


        
