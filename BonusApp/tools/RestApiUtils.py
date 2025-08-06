from django.conf import settings
import aiohttp
import asyncio
import json
import copy
import logging
from BaseApp.library.tools import RequestTools
from django.http.multipartparser import MultiPartParser

LOGGER = logging.Logger(__name__)

def get_all_url():
    '''
    功能描述:根據設置構造所有Rest API端點url
    '''
    server = settings.EMP_REST_API_SERVERS
    endpoint = settings.EMP_RESTAPI_ENDPOINT
    username = settings.EMP_REST_API_USERNAME
    password = settings.EMP_REST_API_PASSWORD
    result = {}
    for key,value in endpoint.items():
        url = value.get('url')
        method = value.get('method','GET').upper()
        exclude = value.get('exclude',[])
        result[key] = {server_key:{'url':server_baseurl+url,'method':method,'basic_auth_user':username,'basic_auth_password':password} \
            for server_key, server_baseurl in server.items() \
            if server_key not in exclude}
    return result
            
urls = get_all_url()

def get_urls(endpoint,params):
    '''
    功能描述:根據Rest Api端點獲取它對應的所有分佈式url
    '''
    location = params.get('location')
    local_urls = urls.get(endpoint)
    if location and location.split(",")[0] in local_urls.keys():
        local_urls = {key:value for key,value in local_urls.items() if key in location.split(",")}
    return local_urls

def get_params(request, param_names):
    request_params = getattr(request, request.method)
    params = { 'location':request_params.get("location")}
    for param_name in param_names:
        params[param_name] = request_params.get(param_name)
    return params
    

def get_restapi_data(endpoint, params):
    urls = get_urls(endpoint, params)
    for key,value in urls.items():
        value['params'] = params
    return async_fetch_http_json(urls)

def async_fetch_http_json(http_methods):
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
        headers={'Content-Type': 'application/json'}
        auth = None
        if basic_auth_user and basic_auth_password:
            auth = aiohttp.BasicAuth(basic_auth_user, basic_auth_password)
        async with aiohttp.ClientSession(headers=headers, auth=auth) as client:
            if method_type.upper() == 'POST':
                async with client.post(url,data=json.dumps(params,ensure_ascii=False)) as resp:
                    assert resp.status == 200 or resp.status == 201
                    return await resp.json()
            elif method_type.upper() == 'OPTIONS':
                async with client.options(url,params=params) as resp:
                    assert resp.status == 200
                    return await resp.json()
            elif method_type.upper() == 'PUT':
                async with client.put(url,data=json.dumps(params,ensure_ascii=False)) as resp:
                    assert resp.status == 200
                    return await resp.json()
            elif method_type.upper() == 'DELETE':
                async with client.delete(url,data=json.dumps(params,ensure_ascii=False)) as resp:
                    assert resp.status == 200 or resp.status == 204
                    return {'status':resp.status == 204}
            else:
                async with client.get(url,params=params) as resp:
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


def operateRemote(request):   
    result = {'status':False, 'msg':'', 'data':None}
    if (request.method == "GET"):
        result = {'draw': 1, 'recordsTotal': 0, 'recordsFiltered': 0, 'data': None}
    try:
        params = {}#get_params(request,[])
        endpoint=request.GET.get('endpoint')
        location=request.GET.get('location')
        id = request.GET.get('id')
        if (request.method == "GET"):
            params.update(request.GET.dict())
        elif (request.method == "POST"):
            params.update(request.POST.dict())           
        else:
            params.update(RequestTools.getRequestData(request).dict())         
        if (request.method == "GET"): 
            if 'format' in params:
                data = get_restapi_data(endpoint, params)
                result = data[params['location']]
            else:
                urls = copy.deepcopy(get_urls(endpoint, params))
                for key,value in urls.items():                     
                    if id:
                        value['url'] = value['url'] + id + "/" 
                    else:
                        value['params'] = params   
                        value['params']['company'] = key
                        value['params']['username'] = request.user.username 
                data = async_fetch_http_json(urls)
                result['status'] = True
                if 'location' in params:
                    # 處理單個數據返回
                    if 'data' in data[params['location']]:
                        result['data'] = data[params['location']]['data']
                    else:
                        result['data'] = data[params['location']]
                else:
                    # 處理多個數據返回
                    result['data'] = data
        else:
            if location:
                params['location'] = location
            urls = copy.deepcopy(get_urls(endpoint, params))
            for key,value in urls.items():   
                if 'location' in params:         
                    del params['location']                
                value['params'] = params   
                value['params']['company'] = key
                value['params']['username'] = request.user.username  
                value['method'] = request.method
                if id:
                    value['url'] = value['url'] + id + "/"  
            
            data = async_fetch_http_json(urls)        
            result['data'] = data
            result['status'] = True
    except Exception as e:
        LOGGER.error(e)
    return result