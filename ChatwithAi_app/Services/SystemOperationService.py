import numpy as np
from django.db import connections
from django.core.cache import cache
from scipy.spatial.distance import cosine
from scipy.spatial.distance import euclidean
import requests
from django.conf import settings
from ..models import AiSentences, AiPageurls
from BaseApp.library.tools import AsyncioTools
import orjson

class SystemOperationService:
    def __get_embedding(self, text):
        """
        使用 API 获取文本的 Embedding 向量。
        """
        embedding_url = "{0}/api/embedding/openai".format(settings.PMIS_REST_API_SERVER_NEW)
        embedding_http_methods = {
            'url': embedding_url,
            'method': 'POST',
            'params': {'data': [{"question":text}], 'field':"question", 'model':"text-embedding-ada-002"},
            'basic_auth_user': settings.PMIS_REST_API_USERNAME,
            'basic_auth_password': settings.PMIS_REST_API_PASSWORD
        }
        embedding_response = AsyncioTools.async_fetch_http_json({"data": embedding_http_methods})
        embedding_result = embedding_response['data']

        if embedding_result['status']:
            embeddings_data = embedding_result.get("data", [])        
            return embeddings_data[0].get("question_embedding")
        else:
            raise Exception("Error fetching embedding from API")

    def __calculate_cosine_similarity(slef, vector1, vector2):
        """
        手動計算兩個向量之間的餘弦相似度。
        """
        dot_product = np.dot(vector1, vector2)
        norm1 = np.linalg.norm(vector1)
        norm2 = np.linalg.norm(vector2)
        return dot_product / (norm1 * norm2)

    
    def get_page_embeddings(self):
        """
        从数据库加载 embedding 数据，并按 reference_id 分组，将所有数据存储到一个 Redis 键中。
        """
        cache_name = "{0}:{1}".format(__name__, self.get_page_embeddings.__name__)
        cached_data = cache.get(cache_name)
        
        # 如果缓存中有数据，则将 JSON 字符串解析为字典
        if cached_data:
            return orjson.loads(cached_data)
        else:
            # 查询数据库中的 embedding 数据
            rows = AiSentences.objects.filter(reference_type="page").values('reference_id', 'embedding_vector')
            
            # 构建一个字典，将所有 embedding 按 reference_id 分组存储在一起
            embedding_data = {}
            for row in rows:
                reference_id = str(row['reference_id'])
                embedding_vector = row['embedding_vector']
                
                # 将 JSON 格式的字符串转换为数值列表
                embedding = orjson.loads(embedding_vector)
                
                # 如果 reference_id 不在字典中，初始化一个空列表
                if reference_id not in embedding_data:
                    embedding_data[reference_id] = []
                
                # 将该向量追加到该 reference_id 的列表中
                embedding_data[reference_id].append(embedding)

            # 将所有 embedding 数据作为 JSON 字符串存储到 Redis 中的单一键
            cache.set(cache_name, orjson.dumps(embedding_data))
            return embedding_data
        

    def get_similar_pages(self, user_question,recordid=None, system_name=None, similarity_threshold=0.8):
        """
        根据用户输入的问题，生成 Embedding 并计算与缓存中的 Embedding 的相似度，返回最相似的 reference_id 列表。
        
        :param user_question: 用户输入的问题
        :param limit: 返回相似度最高的前 n 个 reference_id
        :return: List of tuples (reference_id, similarity_score)
        """
        # 1. 获取问题的 embedding
        question_embedding = self.__get_embedding(user_question)
        
        # 2. 从缓存中获取 embedding 数据并计算相似度
        pages_embeddings = self.get_page_embeddings()
        if recordid or system_name:
            qs = AiPageurls.objects.values("id").all()
            if recordid:
                qs = qs.filter(recordid=recordid)
            if system_name:
                qs = qs.filter(system_name__icontains=system_name)
            pages_embeddings = {key:value for key,value in pages_embeddings.items() if int(key) in [row["id"] for row in qs]}

        similarity_scores = {
            reference_id: max(1 - cosine(question_embedding, embedding) for embedding in embeddings)
            for reference_id,embeddings in pages_embeddings.items()
        }          

        # 筛选出相似度大于阈值的其他 topics
        similarity_topics = {item_id:score for item_id, score in similarity_scores.items() if score >= similarity_threshold}

        qs = AiPageurls.objects.filter(id__in=list(similarity_topics.keys())).values()
        simpilare_pages = [{**page, **{'score_value':0 if str(page['id']) not in similarity_topics else similarity_topics[str(page['id'])]}} for page in qs]
        
        # 按相似度排序
        simpilare_pages = sorted(simpilare_pages, key=lambda x: x['score_value'], reverse=True)

        return simpilare_pages