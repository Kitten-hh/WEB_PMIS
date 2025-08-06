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

class AiEmbeddingService:
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

    def __get_embedding(self, text):
        """
        使用 API 获取文本的 Embedding 向量。
        """
        try:
            response = self.api_client.embeddings.create(
                input=[text],
                model="text-embedding-ada-002"
            )      
            embeddings = [res.embedding for res in response.data]          
            return embeddings[0]
        except Exception as e:
            raise Exception("Error fetching embedding")

    def __calculate_cosine_similarity(self, vector1, vector2):
        """
        手动计算两个向量之间的余平相似度。
        """
        dot_product = np.dot(vector1, vector2)
        norm1 = np.linalg.norm(vector1)
        norm2 = np.linalg.norm(vector2)
        return dot_product / (norm1 * norm2)
    
    def __calculate_similarity_scores(self, vector1, vector2):
        """
        计算余平相似度、欧凡相似度和曼哈顿相似度。
        """
        cosine_sim = 1 - cosine(vector1, vector2)
        euclidean_sim = 1 / (1 + euclidean(vector1, vector2))
        manhattan_sim = 1 / (1 + cityblock(vector1, vector2))
        pearson_corr = (np.corrcoef(vector1, vector2)[0, 1] + 1) / 2  # 标准化皮尔逊相关系数到 [0, 1]
        return cosine_sim, euclidean_sim, manhattan_sim, pearson_corr

    def get_embeddings(self):
        """
        从数据库加载 embedding 数据，并按 reference_id 分组，将所有数据存储到一个 Redis 键中。
        """
        cache_name = "{0}:{1}".format(__name__, self.get_embeddings.__name__)
        cached_data = cache.get(cache_name)
        
        # 如果缓存中有数据，则将 JSON 字符串解析为字典
        if cached_data:
            return orjson.loads(cached_data)
        else:
            # 查询数据库中的 embedding 数据
            rows = AiSentences.objects.filter(reference_type="pre-condition").values('reference_id','reference_type', 'embedding_vector')
            
            # 构建一个字典，将所有 embedding 按 reference_id 分组存储在一起
            embedding_data = {}
            for row in rows:
                key = f"{row['reference_type']}::{str(row['reference_id'])}"
                embedding_vector = row['embedding_vector']
                
                # 将 JSON 格式的字符串转换为数值列表
                embedding = orjson.loads(embedding_vector)
                
                # 如果 key 不在字典中，初始化一个空列表
                if key not in embedding_data:
                    embedding_data[key] = []
                
                # 将该向量追加到该 key 的列表中
                embedding_data[key].append(embedding)

            # 将所有 embedding 数据作为 JSON 字符串存储到 Redis 中的单一键
            cache.set(cache_name, orjson.dumps(embedding_data), timeout=None)
            return embedding_data
        

    def get_similar_actions(self, user_question, similarity_threshold=0.8, message_type=None):
        """
        根据用户输入的问题，生成 Embedding 并计算与缓存中的 Embedding 的相似度，返回最相似的action 列表。
        
        :param user_question: 用户输入的问题
        :param similarity_threshold: 返回相似度最高的前 n 个 reference_id
        :return: List of actions
        """
        # 1. 获取问题的 embedding
        question_embedding = self.__get_embedding(user_question)
        
        # 2. 从缓存中获取 embedding 数据并计算相似度
        actions_embeddings = self.get_embeddings()
        
        similar_actions = []
        for key, embeddings_list in actions_embeddings.items():
            reference_type, reference_id = key.split("::")
            if message_type and message_type.lower() != reference_type.lower():
                continue
            max_similarity = 0
            for embedding in embeddings_list:
                cosine_sim, euclidean_sim, manhattan_sim,pearson_corr = self.__calculate_similarity_scores(question_embedding, embedding)
                
                # 加权平均法计算总相似度
                overall_similarity = 0.7 * cosine_sim + 0.1 * euclidean_sim + 0.05 * manhattan_sim + 0.15 * pearson_corr
                
                # 取该 action 中的最大相似度
                if overall_similarity > max_similarity:
                    max_similarity = overall_similarity
            
            if max_similarity >= similarity_threshold:
                similar_actions.append((key, max_similarity))
        
        # 按相似度从高到低进行排序
        similar_actions.sort(key=lambda x: x[1], reverse=True)
        
        return self.get_action_details(similar_actions)

    def get_action_details(self, similar_actions):
        """
        根据相似的 actions 获取具体的 action 数据。
        如果 key 是 "pre-condition"，则从数据表 PromtSQL 中读取 SName。
        
        :param similar_actions: 相似的 action 列表
        :return: Dictionary of action details grouped by reference_type
        """
        action_details = {}
        actions_by_type = {}
        
        # 按 reference_type 分组
        for key, similarity in similar_actions:
            reference_type, reference_id = key.split("::")
            if reference_type not in actions_by_type:
                actions_by_type[reference_type] = []
            actions_by_type[reference_type].append((reference_id, similarity))
        
        # 查询 PromtSQL 数据表
        if "pre-condition" in actions_by_type:
            reference_ids = [int(ref_id) for ref_id, _ in actions_by_type["pre-condition"]]
            prompt_sql_records = Promtsql.objects.filter(inc_id__in=reference_ids).values('inc_id', 'sname')
            prompt_sql_dict = {str(record['inc_id']): record['sname'] for record in prompt_sql_records}
            
            action_details["pre-condition"] = []
            for reference_id, similarity in actions_by_type["pre-condition"]:
                if reference_id in prompt_sql_dict:
                    action_details["pre-condition"].append({"id": reference_id, "name": prompt_sql_dict[reference_id], "similarity": similarity})
        
        return action_details
