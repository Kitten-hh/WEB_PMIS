import requests
import uuid
from datetime import datetime, timedelta
from BaseApp.library.middleware import LogPortMiddleware
from django.core.cache import cache
from django.urls import reverse
from PMIS.Services.UserService import UserService
from DataBase_MPMS.models import VTask
from ..models import AiPageurls,AiFollowupTbl
from django.conf import settings
from BaseApp.library.tools import AsyncioTools
from django.core.serializers.json import DjangoJSONEncoder
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import openai
from httpx import Client
from tabulate import tabulate
from wcwidth import wcswidth
import json

# Set up default headers for authentication
headers = {
    'Authorization': 'Basic ' + 'sing:singfyx1110'.encode('utf-8').decode('utf-8'),
    'X-Requested-With': 'XMLHttpRequest',  # To indicate an AJAX request
    'Content-Type': 'application/json'
}

# 格式化日期为仅日期部分
def format_to_date(value):
    try:
        if isinstance(value, str):
            # 尝试支持多种日期时间格式
            for fmt in ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"]:
                try:
                    date_object = datetime.strptime(value, fmt)
                    return date_object.strftime("%Y-%m-%d")
                except ValueError:
                    continue
    except Exception as e:
        print(f"Error formatting date: {e}")
    return value  # 如果无法解析，则返回原值

def filter_empty_columns(data, headers):
    # 确保数据为列表的列表
    data = [list(row) for row in data]
    headers = list(headers)
    # 找出非空字段索引，强制排除 inc_id（无论大小写）
    valid_columns = [
        col_idx for col_idx in range(len(headers))
        if headers[col_idx].lower() != "inc_id" and (
            any(row[col_idx] not in [None, ""] for row in data)  # 检查数据
            or headers[col_idx]  # 确保保留有表头的列
        )
    ]
    # 过滤字段
    filtered_headers = [headers[col_idx] for col_idx in valid_columns]
    filtered_data = [[row[col_idx] for col_idx in valid_columns] for row in data]
    return filtered_headers, filtered_data

# 更新后的 tabulate_with_chinese 方法
def tabulate_with_chinese(data, headers):
    # 过滤所有值均为 None 的字段
    headers, data = filter_empty_columns(data, headers)

    # 确保 headers 是列表
    headers = list(headers) if not isinstance(headers, list) else headers
    # 确保 data 是列表的列表，且处理日期格式化
    data = [[format_to_date(cell) for cell in row] for row in data]

    # 计算每列的最大宽度（考虑中文字符宽度和多行）
    def get_col_widths(data, headers):
        widths = []
        for col_idx in range(len(headers)):
            max_width = max(
                max(wcswidth(line) for line in str(row[col_idx]).splitlines()) if row[col_idx] is not None else 0
                for row in data + [headers]
            )
            widths.append(max_width)
        return widths

    # 调整每行的单元格宽度
    def adjust_row(row, col_widths):
        adjusted_row = []
        for col_idx, cell in enumerate(row):
            cell_lines = str(cell).splitlines() if cell is not None else [""]
            padded_lines = [
                line + " " * (col_widths[col_idx] - wcswidth(line)) for line in cell_lines
            ]
            adjusted_row.append("\n".join(padded_lines))
        return adjusted_row

    # 计算每列宽度
    col_widths = get_col_widths(data, headers)

    # 调整所有数据和表头的宽度
    adjusted_headers = adjust_row(headers, col_widths)
    adjusted_data = [adjust_row(row, col_widths) for row in data]

    # 返回格式化表格
    return tabulate(adjusted_data, headers=adjusted_headers, tablefmt="grid", stralign="left", numalign="right")

def get_base_url():
    return settings.WEBPMIS_SERVER

def object_to_form_data(obj):
    return {k: v for k, v in obj.items() if v}

def handle_prompt_result_data(data):
    if not isinstance(data, list):
        data = [data]
    if len(data) == 0:
        return None
    message_text = ""
    for item in data:
        line_text = " ".join(str(value) for key, value in item.items())
        message_text += f"{line_text}\r\n" if message_text else line_text
    return message_text

def get_engineering():
    base_url = get_base_url()
    if not base_url:
        return None
    response = requests.post(f"{base_url}/schedule/api/get_prompt_answer_data", data=object_to_form_data({"promptName": "get engineering projects"}), headers=headers)
    result = response.json()
    if result.get("status"):
        return handle_prompt_result_data(result["data"])
    return None

def get_projects(args):
    contact = args.get('contact')
    top = args.get('top', 10)
    if not contact:
        raise ValueError("The parameters passed in are incorrect!")
    
    base_url = get_base_url()
    if not base_url:
        return None
    url = f"{base_url}/schedule/subproject_table"
    response = requests.get(url, params={"sea_contact": contact, "draw": 1, "start": 0, "length": -1}, headers=headers)
    result = response.json()

    datas = sorted(result['data'], key=lambda x: (x.get('userscore') is not None, x.get('userscore', 0)), reverse=True)[:top]
    messages = ""
    for project in datas:
        if messages == "":
            messages = f"{project['recordid']} {project['projectname']}"
        else:
            messages += f"\n{project['recordid']} {project['projectname']}"
    return messages

def create_project(args):
    pid = args.get('pid')
    name = args.get('name')
    if not pid or not name:
        raise ValueError("The parameters passed in are incorrect!")
    
    base_url = get_base_url()
    if not base_url:
        return None
    response = requests.post(f'{base_url}/chatwithai/create_project', data=object_to_form_data({'pid': pid, 'name': name}), headers=headers)
    result = response.json()
    if result.get("status"):
        project = result["data"]
        return f"Create project successfully! The current project is {project['recordid']} {project['projectname']}"
    return None

def get_sessions(args):
    recordid = args.get('recordid')
    contact = args.get('contact')
    top = args.get('top', 10)
    if not recordid or not contact:
        raise ValueError("The parameters passed in are incorrect!")
    
    base_url = get_base_url()
    if not base_url:
        return None
    url = f"{base_url}/schedule/session_table"
    response = requests.get(url, params={"recordid": recordid, "sea_contact": contact, "draw": 1, "start": 0, "length": -1}, headers=headers)
    result = response.json()

    sessions = sorted(result['data'], key=lambda x:(x.get('userweight') is not None, x.get('userweight', 0)), reverse=True)[:top]
    return "\n".join(f"{session['sessionid']} {session['sdesp']}" for session in sessions)

def create_session(args):
    recordid = args.get('recordid')
    name = args.get('name')
    if not recordid or not name:
        raise ValueError("The parameters passed in are incorrect!")
    
    base_url = get_base_url()
    if not base_url:
        return None
    url = f"{base_url}/PMIS/session/create?type=1&recordid={recordid}"
    response = requests.get(url, headers=headers)
    result = response.json()
    if result.get("status"):
        now = datetime.now()
        quarter = (now.month - 1) // 3
        first_date = datetime(now.year, quarter * 3 + 1, 1)
        end_date = datetime(first_date.year, first_date.month + 3, 1) - timedelta(days=1)
        data = {
            'pid': result['data']['pid'],
            'tid': result['data']['tid'],
            'progress': "I",
            'planbdate': first_date.strftime('%Y-%m-%d'),
            'planedate': end_date.strftime('%Y-%m-%d'),
            'sdesp': name,
            'contact': "sing"
        }
        response = requests.post(url, data=object_to_form_data(data), headers=headers)
        result = response.json()
        if result.get("status"):
            session = result['data']['instance']
            return f"Create session successfully! The current session is {session['pid']}-{session['tid']} {session['sdesp']}"
    return None

def create_task(args):
    base_url = get_base_url()
    if not base_url:
        return None
    url = f"{base_url}/PMIS/task/add_task"
    sessionid = args.get('sessionid')
    task_description = args.get('task')
    if not sessionid or not task_description:
        raise ValueError("The parameters passed in are incorrect!")

    response = requests.get(url, params={'sessionid': sessionid}, headers=headers)
    result = response.json()
    if result.get("status"):
        data = result['data']
        data['task'] = task_description
        data['contact'] = "sing"
        response = requests.post(url, data=object_to_form_data(data), headers=headers)
        result = response.json()
        if result.get("status"):
            task = result['data']['instance']
            return f"Create task successfully! The taskno is {task['pid']}-{task['tid']}-{task['taskid']}"
    return None

def get_tasks(args):
    sessionid = args.get('sessionid')
    class1 = args.get('class1')
    if not sessionid:
        raise ValueError("The parameters passed in are incorrect!")
    
    sessionid_arr = sessionid.split("-")
    params = {'pid': sessionid_arr[0], 'tid': sessionid_arr[1], 'session_filter': False}
    if class1:
        params['class_one'] = class1
    
    base_url = get_base_url()
    if not base_url:
        return None
    url = f"{base_url}/PMIS/session/search_task"
    response = requests.get(url, params=params, headers=headers)
    result = response.json()
    if result.get("status"):
        tasks = result['data']
        messages = ""
        for task in tasks:
            task_details = f"{task['taskno']} {task['contact']} {task['task']} "
            task_details += f"Remark:{task['remark']} " if task['remark'] else ""
            task_details += f"{task['planbdate'][:10] if task['planbdate'] else 'null'} {task['progress']}"
            messages += f"\n{task_details}" if messages else task_details
        return messages
    return "Could you be more specific, such as sessions, etc?"

def show_project_in_app(args):
    contact = args.get('contact')
    recordid = args.get('recordid')
    if not contact:
        raise ValueError("The parameters passed in are incorrect!")
    
    base_url = get_base_url()
    if not base_url:
        return None
    url = f"{base_url}/en/devplat/project/overview?contact={contact}"
    if recordid:
        url += f"&recordids={recordid}"
    # Simulate opening the URL in a browser (in real scenario, it would be done differently)
    print(f"Opening URL: {url}")

def show_milestone_in_app(args):
    contact = args.get('contact')
    recordid = args.get('recordid')
    if not contact or not recordid:
        raise ValueError("The parameters passed in are incorrect!")
    
    base_url = get_base_url()
    if not base_url:
        return None
    url = f"{base_url}/en/looper/user/top5_projects?contact={contact}&recordid={recordid}"
    # Simulate opening the URL in a browser (in real scenario, it would be done differently)
    print(f"Opening URL: {url}")

def show_session_in_app(args):
    recordid = args.get('recordid')
    sessionid = args.get('sessionid')
    if not recordid or not sessionid:
        raise ValueError("The parameters passed in are incorrect!")
    
    base_url = get_base_url()
    if not base_url:
        return None
    url = f"{base_url}/en/devplat/sessions?recordid={recordid}&menu_id=mi_{sessionid}#Session_Tasks"
    # Simulate opening the URL in a browser (in real scenario, it would be done differently)
    print(f"Opening URL: {url}")

def get_user(args):
    contact = args.get("contact")
    if not contact:
        users = UserService.GetPartUserNames()
        return json.dumps(users)  # 返回用戶列表以提示用戶
    else:
        return f"Information for user: {contact}"


def get_document_list(args):
    recordid = args.get('recordid')
    sessionid = args.get('sessionid')
    part_doc_name = args.get('part_doc_name')
    if not recordid or not sessionid:
        raise ValueError("The parameters passed in are incorrect!")
    
    base_url = get_base_url()
    if not base_url:
        return None
    url = f"{base_url}/devplat/sessions_list?recordid={recordid}"
    response = requests.get(url, headers=headers)
    result = response.json()
    if result.get("status"):
        sessions = result['data']
        attach_session = []
        s_arr = [x for x in sessions if x['sessionid'] == sessionid]
        if len(s_arr) == 0:
            return "No document list found!"
        select_title = s_arr[0]['sdesp']
        key_fields = ['Documentation', 'Design']
        def include(str_value, list_values):
            return any(e in str_value for e in list_values)
        if not include(select_title, key_fields):
            for session in sessions:
                title = session['sdesp']
                if title is None or '-' not in title:
                    continue
                if include(title, key_fields) and title.split('-')[1].strip() == select_title.split('-')[1].strip():
                    attach_session.append(session['sessionid'])
        array = sessionid.split("-")
        params = {
            'pid': array[0],
            'tid': array[1],
            'attach': json.dumps(attach_session)
        }
        url = f"{base_url}/PMIS/task/t_doc_list"
        response = requests.get(url, params=params, headers=headers)
        result = response.json()
        if result.get("status"):
            documents = result['data']
            msgs = []
            for item in documents:
                open_url = f"{base_url}/looper/metting/browse_task_image?inc_id={item['inc_id']}"
                if item['mediatype'] and item['mediatype'].lower() in ["image/jpeg", "image/png", "image/jpg", "image/gif", "image/bmp"]:
                    msgs.append({"docname": item['docname'], "openurl": open_url})
                elif item['mediatype'] and item['mediatype'].lower() in ['application/pdf', "pdf", ".pdf"]:
                    msgs.append({"docname": item['docname'], "openurl": f"{open_url}&state=convert_pdf"})
                else:
                    msgs.append({"docname": item['docname'], "openurl": f"{open_url}&state=download"})
            return  json.dumps(msgs)
    return "No document list found!"


def get_condition_data(args):
    prompt_name = args.get('sname')
    params = {'promptName': prompt_name}
    base_url = get_base_url()
    if not base_url:
        return None

    try:
        url = f"{base_url}/schedule/api/get_prompt_answer_data"
        response = AsyncioTools.async_fetch_http_json({"data":{"url":url, "params":params, "method":"POST", "basic_auth_user":"sing", "basic_auth_password":"singfyx1110"}})
        result = response['data']

        if result.get('status'):
            data = result.get('data', [])
            if not isinstance(data, list):
                data = [data]

            message_text = ""
            for item in data:
                line_text = ""
                for key, value in item.items():
                    if value is None:
                        continue
                    if isinstance(value, str):
                        value = value.replace('\r\n', '')
                    line_text += f"{value}" if line_text == "" else f"{value}"
                
                if message_text == "":
                    message_text = line_text
                else:
                    message_text += "\r\n" + line_text
            return message_text
        return ""
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None    
    

def get_session_information(sessions):
    sessionnos = [session['sessionno'] for session in sessions]
    qs = VTask.objects.values('taskno', 'contact', 'task', 'remark', 'planbdate','planedate', 'progress').filter(tasklistno__in=sessionnos)
    return json.dumps(list(qs), cls=DjangoJSONEncoder)


def filter_objects_by_params(data_array, params):
    # 創建參數的大小寫映射
    params_lower = {k.lower(): v for k, v in params.items() if v}
    
    filtered_data = []
    
    # 預處理：將所有數組對象的鍵名轉為小寫
    for item in data_array:
        # 轉換每個項目的字段名為小寫的映射
        item_lower = {k.lower(): v for k, v in item.items()}
        
        # 檢查是否所有的參數都匹配
        if all(str(item_lower.get(k, None)).lower() == str(v).lower() for k, v in params_lower.items()):
            filtered_data.append(item)
    
    return filtered_data

def get_condition_data_info(id, action_name, filter_variables):
    params = {'id': id}
    base_url = get_base_url()
    if not base_url:
        return None
    try:
        url = f"{base_url}/schedule/api/get_prompt_answer_data"
        response = AsyncioTools.async_fetch_http_json({"data":{"url":url, "params":params, "method":"POST", "basic_auth_user":"sing", "basic_auth_password":"singfyx1110"}})
        result = response['data']

        if result.get('status'):
            data = result.get('data', [])
            if not isinstance(data, list):
                data = [data]
            ##如果是帶參數的查詢條件，需要使用參數過濾數據
            if filter_variables:            
                filter_params = {key:value[key] for key, value in filter_variables.items()}
                data = filter_objects_by_params(data, filter_params)


            message_text = format_result(data)
            informaction = None
            if action_name:
                informaction = globals()[action_name](data)
            return message_text, informaction
        return "",""
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None       

def format_result(jsondata):
    if len(jsondata) == 0:
        return ""
    try:
        headers = jsondata[0].keys() if jsondata else []
        rows = [list(item.values()) for item in jsondata]

        # 使用 tabulate 格式化表格
        return "<pre class='text_table'>" + tabulate_with_chinese(headers=headers, data=rows) + "</pre>"    
    except Exception as e:
        message_text = ""
        for item in jsondata:
            line_text = ""
            for key, value in item.items():
                if value is None:
                    continue
                if isinstance(value, str):
                    value = value.replace('\r\n', '')
                line_text += f"{value}" if line_text == "" else f" {value}"
            
            if message_text == "":
                message_text = line_text
            else:
                message_text += "\r\n" + line_text        
        return message_text     

def format_result_bak(jsondata):
    try:
        # 初始化代理设置
        proxies = {
            "http://": settings.OPENAPI_PROXY_URL,
            "https://": settings.OPENAPI_PROXY_URL,
        } if settings.OPENAPI_PROXY_URL else None

        # 初始化 OpenAI 实例
        api_client = openai.OpenAI(
            api_key=settings.OPENAPI_KEY,
            http_client=Client(proxies=proxies)
        )

        # 构建请求消息
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a highly skilled formatting assistant. "
                    "Your task is to take JSON data and present it as well-organized and readable information. "
                    "Ensure no data is omitted, and format the output to be user-friendly and easy to understand."                )
            },
            {
                "role": "user",
                "content": (
                    "Here is the JSON data that needs to be formatted:\n"
                    f"{json.dumps(jsondata)}"
                )
            },
        ]

        # 调用 OpenAI API 进行处理
        response = api_client.chat.completions.create(
            model=settings.OPENAPI_MODEL,
            messages=messages,
        )

        # 返回格式化结果
        return response.choices[0].message.content.strip()
    except Exception as e:
        message_text = ""
        for item in jsondata:
            line_text = ""
            for key, value in item.items():
                if value is None:
                    continue
                if isinstance(value, str):
                    value = value.replace('\r\n', '')
                line_text += f"{value}" if line_text == "" else f" {value}"
            
            if message_text == "":
                message_text = line_text
            else:
                message_text += "\r\n" + line_text        
        return message_text

def get_condition_data_info_bak(id, action_name, filter_variables):
    params = {'id': id}
    base_url = get_base_url()
    if not base_url:
        return None
    try:
        url = f"{base_url}/schedule/api/get_prompt_answer_data"
        response = AsyncioTools.async_fetch_http_json({"data":{"url":url, "params":params, "method":"POST", "basic_auth_user":"sing", "basic_auth_password":"singfyx1110"}})
        result = response['data']

        if result.get('status'):
            data = result.get('data', [])
            if not isinstance(data, list):
                data = [data]
            ##如果是帶參數的查詢條件，需要使用參數過濾數據
            if filter_variables:            
                filter_params = {key:value[key] for key, value in filter_variables.items()}
                data = filter_objects_by_params(data, filter_params)


            message_text = ""
            for item in data:
                line_text = ""
                for key, value in item.items():
                    if value is None:
                        continue
                    if isinstance(value, str):
                        value = value.replace('\r\n', '')
                    line_text += f"{value}" if line_text == "" else f" {value}"
                
                if message_text == "":
                    message_text = line_text
                else:
                    message_text += "\r\n" + line_text
            informaction = None
            if action_name:
                informaction = globals()[action_name](data)
            return message_text, informaction
        return "",""
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None       

def execute_system_operation(id, action_name, variables):
    qs = AiPageurls.objects.filter(id=id)
    if len(qs) == 0:
        return None
    pageurl = qs[0].url
    pagename = qs[0].page_name
    if not pageurl:
        return None
    try:
        if not pageurl.startswith("http"):
            pageurl = settings.WEBPMIS_SERVER_OUT + pageurl

        # 解析 URL
        parsed_url = urlparse(pageurl)

        # 提取并解析原有参数
        existing_params = parse_qs(parsed_url.query)
        if not existing_params or not variables:
            return json.dumps({"action":"System Operation", "url":pageurl, "message":f"OK, I will executed the system operation. Open the page '{pagename}'."})
        
        variables_dict = {key:value[key] for key, value in variables.items()}
        # 将字典的键统一转换为小写
        params_dict_lower = {key.lower(): value for key, value in variables_dict.items()}

        # 解析 URL
        parsed_url = urlparse(pageurl)

        # 提取并解析原有参数
        existing_params = parse_qs(parsed_url.query)

        # 创建一个新的参数字典
        new_params = {}

        for param, values in existing_params.items():
            for value in values:
                # 如果值是 {xxx} 格式，尝试从 params_dict 中取值（不区分大小写）
                if value.startswith("{") and value.endswith("}"):
                    key = value[1:-1].lower()  # 去掉 {} 并转换为小写
                    if key in params_dict_lower:  # 如果字典中有对应的值
                        new_params[param] = params_dict_lower[key]
                    # 如果字典中没有对应的值，不添加到新参数字典中（即移除该参数）
                else:
                    # 如果值是静态值，直接保留
                    new_params[param] = value

        # 将新参数编码回 URL
        new_query = urlencode(new_params)
        new_url = urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            new_query,
            parsed_url.fragment
        ))
        return json.dumps({"action":"System Operation", "url":new_url, "message":f"OK, I will executed the system operation. Open the page '{pagename}'."})
    except Exception as e:
        return None


def getAiFollowUpResults(followup_id, main_question_id=None):
    try:
        proxies = {
                "http://": settings.OPENAPI_PROXY_URL,
                "https://": settings.OPENAPI_PROXY_URL,
        } if settings.OPENAPI_PROXY_URL else None
            
        # 初始化 openai 实例
        api_client = openai.OpenAI(
                api_key=settings.OPENAPI_KEY,
                http_client=Client(proxies=proxies)
        )    
        messages = [
            {"role": "system", "content": "You are a helpful assistant and just ask the questions given to you."},
        ]
        
        qs = AiFollowupTbl.objects.values('question','reply').filter(followup_id=followup_id)
        if main_question_id:
            qs = qs.filter(main_question_id=main_question_id)
        question_and_reply = json.dumps(list(qs))
        messages.append({"role":"user", "content":f"Based on the following questions and answers analysis and summaries the results.  Also, simply give yes or no that I should pay attention to any problems.  If so, what attentions are needed? {question_and_reply}"})
        response = api_client.chat.completions.create(
            model=settings.OPENAPI_MODEL,
            messages=messages,
        )    
        return response.choices[0].message.content.strip()  
    except Exception as e:
        return None