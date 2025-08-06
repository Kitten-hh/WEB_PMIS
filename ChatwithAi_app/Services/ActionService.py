import numpy as np
from django.db import connections
from django.core.cache import cache
from scipy.spatial.distance import cosine, euclidean, cityblock
import requests
from django.conf import settings
from ..models import AiSentences, AiPageurls
from BaseApp.library.tools import AsyncioTools
import orjson
import openai
import logging
from ScheduleApp.models import Promtsql
from httpx import Client
from .AiEmbeddingService import AiEmbeddingService

LOGGER = logging.Logger(__name__)

class ActionService:
    def __init__(self):
        # 设置代理（如果需要）
        self.LOGGER = logging.getLogger(__name__)
        proxies = {
            "http://": settings.OPENAPI_PROXY_URL,
            "https://": settings.OPENAPI_PROXY_URL,
        } if settings.OPENAPI_PROXY_URL else None
        
        # 初始化 openai 实例
        self.api_client = openai.OpenAI(
            api_key=settings.OPENAPI_KEY,
            http_client=Client(proxies=proxies)
        )
        self.aiembeddingService = AiEmbeddingService()

    def ai_identify_action(self, question, context_params, similarity_threshold=0.8, message_type=None):
        # Create tools dynamically based on parameters
        actions = None
        try:
            actions = self.aiembeddingService.get_similar_actions(question, similarity_threshold, message_type=message_type)
        except Exception as e:
            LOGGER.info(e)
        if not actions:
            return None
        for key, items in actions.items():
            for item in items:
                del item['similarity']
        system_messages = {
            "role": "system", 
            "content": (
                "You are an assistant responsible for selecting the most appropriate action based on the user's question and context. "
                "You will receive a question and some contextual parameters. "
                "Use this information to determine the correct action from the provided list of actions."
                "If no suitable action can be identified, return 'None' instead of a random action."
            )
        }

        data_in_memory = {
            "role": "assistant",
            "content":f"The following are the available actions you can choose from:\n{orjson.dumps(actions)}"
        }        

        user_message = {
            "role": "user",
            "content": f"Question: {question}\nContext: {context_params}"
        }

        messages = [system_messages, data_in_memory, user_message]

        result_json_schema = {
            "name": "ExtractActionSchema",
            "schema": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "The ID of the action"
                            },
                            "name": {
                                "type": "string",
                                "description": "The name of the action"
                            },
                            "type": {
                                "type": "string",
                                "description": "The name of the action type that this action belongs to"
                            }
                        },
                        "required": ["id", "name", "type"]
                    }
                },
                "required": ["action"]
            }
        }
        

        response = self.api_client.chat.completions.create(
            model=settings.OPENAPI_MODEL,
            temperature=0.1,
            messages=messages,
            response_format={
                "type": "json_schema",
                "json_schema": result_json_schema
            },
        )
        topic = None
        try:
            return orjson.loads(response.choices[0].message.content)['action']
        except Exception as e:
            print(str(e))
        return topic        