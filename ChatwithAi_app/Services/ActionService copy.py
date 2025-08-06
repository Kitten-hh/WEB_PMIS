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
            # 调用嵌入服务来查找相似的动作
            actions = self.aiembeddingService.get_similar_actions(question, similarity_threshold, message_type=message_type)
        except Exception as e:
            LOGGER.info(e)

        # 如果没有找到相关动作，直接返回 None
        if not actions or len(actions) == 0:
            LOGGER.info(f"No suitable actions found for the question: {question} with context: {context_params}")
            return None  # 这里可以返回一个适当的提示信息，避免返回随便的动作

        # 处理识别到的动作：删除相似度信息
        for key, items in actions.items():
            for item in items:
                del item['similarity']

        # 构建系统消息：向 AI 提供上下文
        system_messages = {
            "role": "system",
            "content": (
                "You are an assistant responsible for selecting the most appropriate action based on the user's question and context. "
                "You will receive a question and some contextual parameters. "
                "Use this information to determine the correct action from the provided list of actions."
                "If no suitable action can be identified, return 'None' instead of a random action."
            )
        }

        # 构建内存数据：传递给 AI 的动作列表
        data_in_memory = {
            "role": "assistant",
            "content": f"The following are the available actions you can choose from:\n{orjson.dumps(actions)}"
        }

        # 构建用户消息：提供问题和上下文
        user_message = {
            "role": "user",
            "content": f"Question: {question}\nContext: {context_params}"
        }

        # 将所有消息传递给 OpenAI API
        messages = [system_messages, data_in_memory, user_message]

        result_json_schema = {
            "name": "ExtractActionSchema",
            "schema": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string"
                    }
                },
                "required": ["action"]
            }
        }

        # 调用 OpenAI API 进行处理
        try:
            # 这里添加代码调用 OpenAI API 返回具体的识别结果
            result = self.openai_api_call(messages, result_json_schema)  # openai_api_call 方法根据实际情况定义
            return result.get('action')  # 返回识别的动作
        except Exception as e:
            LOGGER.error(f"Error during OpenAI API call: {e}")
            return None  # 如果调用失败，返回 None
    