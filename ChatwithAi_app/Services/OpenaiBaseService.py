import aiohttp
import asyncio
import json
from aiohttp_socks import ProxyConnector, ProxyType
from django.conf import settings
from operator import itemgetter
from itertools import groupby
import copy
from django.db import connections,transaction
import re
from time import sleep

class OpenAIException(Exception):
    pass

class OpenAiBaseService(object):
    baseParams = {"proxy_url":settings.OPENAPI_PROXY_URL,"url":settings.OPENAPI_URL, "method":"POST","headers":{"Authorization": "Bearer " + settings.OPENAPI_KEY}}
    defaultApiBody = {
      "model": settings.OPENAPI_MODEL,
      "messages": [
            {
                "role": "system",
                "content": "Explain all concepts like I am expert."
            }
        ]
    }

    def async_fetch_http_json(self,http_methods):
        ''' 
        功能描述:異步獲取數據
        '''
        async def fetch(method):
            url = method.get('url')
            method_type = method.get('method')
            if not method_type:
                method_type = 'GET'
            method_type = method_type.upper()
            params = method.get('params')
            if not params:
                params = {}
            basic_auth_user = method.get('basic_auth_user')
            basic_auth_password = method.get('basic_auth_password')
            proxy_url = method.get('proxy_url')
            headers={'Content-Type': 'application/json'}
            headers_params = method.get('headers')
            if headers_params:
                headers.update(headers_params)
            auth = None
            if basic_auth_user and basic_auth_password:
                auth = aiohttp.BasicAuth(basic_auth_user, basic_auth_password)
            async with aiohttp.ClientSession(headers=headers, auth=auth) as client:
                if method_type == 'POST':
                    async with client.post(url,data=json.dumps(params), proxy=proxy_url) as resp:
                        assert resp.status == 200
                        return await resp.json()
                else:
                    async with client.get(url,params=params, proxy=proxy_url) as resp:
                        assert resp.status == 200
                        return await resp.json()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop) 
        tasks = []
        keys = []
        if type(http_methods) == dict:
            for key,method in http_methods.items():
                task = asyncio.ensure_future(fetch(method))
                keys.append(key)
                tasks.append(task)
        elif type(http_methods) == list:
            for method in http_methods:
                task = asyncio.ensure_future(fetch(method))
                tasks.append(task)
        result = loop.run_until_complete(asyncio.gather(*tasks))        
        if len(keys) > 0:
            result = {keys[idx]:value for idx,value in enumerate(result)}
        return result
    
    def processMessageToChatGPT(self, messages):        
        http_methods = {}
        apiBody =  copy.deepcopy(OpenAiBaseService.defaultApiBody)
        apiBody['messages'] = messages
        http_methods['data'] = {**OpenAiBaseService.baseParams,"params":apiBody}        
        try:                    
            response = self.async_fetch_http_json(http_methods)
        except Exception as e:
            raise OpenAIException("調用Open AI失敗")
        content = response['data']['choices'][0]['message']['content']
        return content;