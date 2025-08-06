import openai
from openai._utils import maybe_transform
from openai.types.chat import (completion_create_params)
import os
from ..models import TopicCategories, MainQuestions, SubQuestions
from django.conf import settings
from django.core.cache import cache
import logging
from httpx import Client
import json
from .AiToolsJson import ai_tools_funcs
from . import AiToolsFunctions
from inspect import getmembers, isfunction  
import copy
functions = {a[0]:a[1] for a in getmembers(AiToolsFunctions) if isfunction(a[1])}

class ConversationService:
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

        # 动态加载话题分类及其相关的主要问题和子问题
        self.categories = self.load_categories()

    def load_categories(self):
        categories = []
        topic_categories = TopicCategories.objects.all().order_by('itemno')
        for category in topic_categories:
            main_questions = MainQuestions.objects.filter(category=category).order_by('itemno')
            questions = []
            for main_question in main_questions:
                sub_questions = SubQuestions.objects.filter(main_question=main_question).order_by('itemno')
                questions.append({
                    "question": main_question.question,
                    "sub_questions": [sub.sub_question for sub in sub_questions],
                    "main_question": main_question,  # 记录主问题对象
                    "sub_questions_objects": list(sub_questions)  # 记录子问题对象列表
                })
            categories.append({
                "category": category.name,
                "type": category.itemno,
                "questions": questions
            })
        return categories

    def convert_to_openai_message(self, chat_completion_message):
        messages = []

        # 添加用户或助手的消息
        messages.append({
            "role": chat_completion_message.role,  # 使用 .role 来访问属性
            "content": chat_completion_message.content  # 使用 .content 来访问属性
        })

        # 如果包含工具调用，将其添加为系统消息
        if hasattr(chat_completion_message, "tool_calls"):
            for tool_call in chat_completion_message.tool_calls:
                messages.append({
                    "role": "system",
                    "content": f"Tool call: {tool_call.tool}, input: '{tool_call.input}', output: '{tool_call.output}'"
                })

        return messages


    def get_chatgpt_response(self, user_input, user_id, session, question_id=None):
        tools = ai_tools_funcs.get(str(question_id), None)
        messages = [
            {"role": "system", "content": "You are a helpful assistant and just ask the questions given to you. You don't need to add 'Next question' to your results for me."},
        ]
        
        if session['context']:
            messages.extend(session['context'])
        #messages.extend([{"role": "user", "content": user_input}])

        response = self.api_client.chat.completions.create(
            model=settings.OPENAPI_MODEL,
            messages=messages,
            #max_tokens=500,
            tools=tools,
            tool_choice="auto" if tools else None
        )
        

        tool_calls = getattr(response.choices[0].message, 'tool_calls', []) or []
        add_tool_message = False
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            if function_name in functions.keys():
                # Call our own function to get data
                function_args = json.loads(tool_call.function.arguments)
                function_result = functions[function_name](function_args)
                # Append result as message and call OpenAI API again with the result from our function
                if not add_tool_message:
                    messages.append(response.choices[0].message)
                    json_data = maybe_transform({"messages": [response.choices[0].message]},completion_create_params.CompletionCreateParams)
                    session['context'].append(json_data['messages'][0])
                    add_tool_message = True
                tool_message = {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_result,
                }
                session['context'].append(tool_message)
                messages.append(tool_message)
        if tool_calls:
            response = self.api_client.chat.completions.create(
                model=settings.OPENAPI_MODEL,
                messages=messages,
                #max_tokens=500
            )

        return response.choices[0].message.content.strip()  


    def get_user_selection_bak(self, user_input, user_id, context=None):
        # Create tools dynamically based on parameters
        tools = {
            "type": "function",
            "function": {
                "name": "extract_user_selection",
                "description": "Based on the last question, extract the specific options selected by the user from its nearest context and return only those specific options.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "options": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "A list of specific options selected by the user. Please do not modify the content of these options and return to the original content."
                        },
                    },
                    "required": ["options"]
                }
            }
        }
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Your task is to extract the user's specific selection from the provided options."},
        ]

        if context:
            messages.extend(context)
        messages.extend([{"role": "user", "content": user_input}])

        response = self.api_client.chat.completions.create(
            model=settings.OPENAPI_MODEL,
            messages=messages,
            tools=[tools],
            tool_choice="auto"
        )

        tool_calls = getattr(response.choices[0].message, 'tool_calls', []) or []

        if not tool_calls:
            # Handle the case where no tool_calls are returned
            return None

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            if function_name == "extract_user_selection":
                function_args = json.loads(tool_call.function.arguments)
                # Return the options parameter value directly
                return function_args.get("options")

        return None
    
    def ai_identify_topic(self, user_input, user_id):
        # Create tools dynamically based on parameters
        categories_list = [category['category'] for category in self.categories]
        categories_string = "\n".join(categories_list)

        system_messages = {
            "role": "system", 
            "content": "You are an manager. All my subsequent questions will be related to one of the following topics.  Please identify a most appropriate topic based on my question."}

        data_in_memory = {
            "role":"assistant",
            "content":f'The following are the options of  topics I can choose from \n"{categories_string}"'
        }        

        user_message = {
            "role":"user",
            "content":user_input
        }

        messages = [system_messages, data_in_memory, user_message]

        result_json_schema = {
            "name": "ExtractTopicSchema",
            "schema": {
            "type": "object",
            "properties": {
                "topic": {
                "type": "string"
                }
            },
            "required": ["topic"]
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
        topic = None
        try:
            topic_obj = json.loads(response.choices[0].message.content)
            topic = topic_obj['topic']
        except Exception as e:
            print(str(e))
        return topic

    def get_default_category_text(self):
        categories_list = "\n".join([f"{category['type']}: {category['category']}" for category in self.categories])
        return f"Please enter the topic name to select it:\n{categories_list}"                

    def get_category_selection(self, user_input, user_id, session):
        temp_context = copy.deepcopy(session['context'])
        if (not session['context'] or len(session['context']) == 1) and not session['init']:
                session['init'] = True
                return self.get_default_category_text()
        else:
            temp_context.insert(0, {"role": "assistant", "content":self.get_default_category_text()})

        # First try to find the category directly from the input
        for index, category in enumerate(self.categories):
            if user_input.lower() in category['category'].lower() or str(category['type']) == user_input:
                if len(category['questions']) > 0:
                    session['current_category_index'] = index
                    session['current_question_index'] = 0  # 默认进入 main questions 的第一个问题
                    return f"You have selected the category: {category['category']}. Let's begin.\nFirst question: {category['questions'][0]['question']}"
                else:
                    return f"You have selected the category: {category.get('category', 'Unknown')}. However, there are no questions in this category."

        # If not found, use get_user_selection to extract category
        selected_options = self.ai_identify_topic(user_input, user_id)

        if not selected_options:
            return "No valid category selected. Please try again."

        selected_option = selected_options.lower()
        for index, category in enumerate(self.categories):
            if selected_option in category['category'].lower():
                if len(category['questions']) > 0:
                    session['current_category_index'] = index
                    session['current_question_index'] = 0  # 默认进入 main questions 的第一个问题
                    return f"You have selected the category: {category['category']}. Let's begin.\nFirst question: {category['questions'][0]['question']}"
                else:
                    return f"You have selected the category: {category.get('category', 'Unknown')}. However, there are no questions in this category."
            
        return "Category not found. Please try again."


    def get_user_session(self, user_id):
        session_data = cache.get(f'ConversationService_{user_id}')
        if session_data:
            return json.loads(session_data)
        else:
            return {
                'user_responses': {},
                'current_category_index': None,  # 用户当前选择的分类索引
                'current_question_index': 0,
                'current_sub_question_index': 0,
                'in_sub_question': False,
                'wait_for_analysis': False,
                'init':False,
                'context': []  # 用于记录上下文信息
            }
    def clear_user_session(self, session):
        session.update({
            'init':False,
            'user_responses': {},
            'current_category_index': None,  # 用户当前选择的分类索引
            'current_question_index': 0,
            'current_sub_question_index': 0,
            'in_sub_question': False,
            'wait_for_analysis': False,
            'context': []  # 用于记录上下文信息
        })

    def save_user_session(self, user_id, session):
        cache.set(f'ConversationService_{user_id}', json.dumps(session), timeout=3 * 24 * 60 * 60)

    def handle_conversation(self, user_id, user_input):
        session = self.get_user_session(user_id)
        # 记录用户输入作为上下文
        session['context'].append({"role": "user", "content": user_input})
        analysis = self.sub_handle_conversation(user_id, user_input, session)
        if len(session['context']) > 0: #沒有清理上下文才添加到上下文
            session['context'].append({"role": "assistant", "content": analysis})
        #記錄AI分析的結果做為上下文
        self.save_user_session(user_id, session)
        return analysis

    def sub_handle_conversation(self, user_id, user_input, session):
        # 检查用户输入是否为跳过当前问题
        if user_input.lower() == 'skip' and session['current_category_index'] != None:
            if session['in_sub_question']:
                # 跳过当前子问题
                sub_questions = self.categories[session['current_category_index']]['questions'][session['current_question_index']]['sub_questions']
                session['current_sub_question_index'] += 1
                if session['current_sub_question_index'] < len(sub_questions):
                    next_sub_question = sub_questions[session['current_sub_question_index']]
                    return f"You chose to skip. \nNext sub-question: {next_sub_question}"
                else:
                    # 子问题全部跳过，进入下一个主问题
                    session['in_sub_question'] = False
                    session['current_question_index'] += 1
                    session['current_sub_question_index'] = 0
            else:
                # 跳过当前主问题
                session['current_question_index'] += 1
                if session['current_question_index'] >= len(self.categories[session['current_category_index']]['questions']):
                    # 所有问题跳过完毕，清理会话状态
                    self.clear_user_session(session)
                    return "You chose to skip. \nThank you! You have completed all the questions."
            if session['in_sub_question']:
                return f"You chose to skip. \nNext sub-question: {self.categories[session['current_category_index']]['questions'][session['current_question_index']]['sub_questions'][session['current_sub_question_index']]}"
            else:
                if session['current_question_index'] >= len(self.categories[session['current_category_index']]['questions']):
                    # 所有问题跳过完毕，清理会话状态
                    self.clear_user_session(session)
                    return "You chose to skip. \nThank you! You have completed all the questions."
                else:
                    return f"You chose to skip. \nNext question: {self.categories[session['current_category_index']]['questions'][session['current_question_index']]['question']}"

        # 检查用户是否需要选择话题分类
        if session['current_category_index'] is None:
            return self.get_category_selection(user_input, user_id, session)

        # 存储用户对主问题或子问题的回答
        category = self.categories[session['current_category_index']]
        questions = category['questions']
        if session['current_question_index'] >= len(questions):
            return "No more questions available."

        # 如果在问子问题
        if session['in_sub_question']:
            sub_questions = questions[session['current_question_index']]['sub_questions']
            if session['current_sub_question_index'] < len(sub_questions):
                sub_question = sub_questions[session['current_sub_question_index']]
                session['user_responses'][sub_question] = user_input

                # 调用 AI 分析用户对子问题的回答
                question_id = f"{questions[session['current_question_index']]['main_question'].id}-{questions[session['current_question_index']]['sub_questions_objects'][session['current_sub_question_index']].id}"
                analysis = self.get_chatgpt_response(user_input, user_id=user_id, question_id=question_id, session=session)
                
                session['current_sub_question_index'] += 1
                if session['current_sub_question_index'] < len(sub_questions):
                    next_sub_question = sub_questions[session['current_sub_question_index']]
                    session['wait_for_analysis'] = True
                    return f"Analysis: {analysis}. \nNext sub-question: {next_sub_question}"
                else:
                    # 子问题回答完毕，进入下一个主问题
                    session['in_sub_question'] = False
                    session['current_question_index'] += 1
                    session['current_sub_question_index'] = 0
                    if session['current_question_index'] >= len(questions):
                        # 所有问题回答完毕，清理会话状态
                        self.clear_user_session(session)
                        return f"Analysis: {analysis}. \nThank you! You have completed all the questions."
                    return f"Analysis: {analysis}. \nNext question: {questions[session['current_question_index']]['question']}"
            else:
                # 如果子问题索引超出范围，进入下一个主问题
                session['in_sub_question'] = False
                session['current_question_index'] += 1
                session['current_sub_question_index'] = 0
                if session['current_question_index'] >= len(questions):
                    # 所有问题回答完毕，清理会话状态
                    self.clear_user_session(session)                    
                    return "Thank you! You have completed all the questions."
                return f"Next question: {questions[session['current_question_index']]['question']}"

        # 如果在问主问题
        main_question = questions[session['current_question_index']]['question']
        session['user_responses'][main_question] = user_input
        # 调用 AI 分析用户对主问题的回答
        analysis = self.get_chatgpt_response(user_input, user_id=user_id, question_id=questions[session['current_question_index']]['main_question'].id, session=session)

        # 检查是否有子问题
        if questions[session['current_question_index']]['sub_questions']:
            session['in_sub_question'] = True
            session['current_sub_question_index'] = 0
            session['wait_for_analysis'] = True
            next_sub_question = questions[session['current_question_index']]['sub_questions'][0]
            return f"Analysis: {analysis}. \nNext sub-question: {next_sub_question}"
        else:
            # 准备下一个主问题
            session['current_question_index'] += 1
            if session['current_question_index'] >= len(questions):
                # 所有问题回答完毕，清理会话状态
                self.clear_user_session(session)                
                return f"Analysis: {analysis}. \nThank you! You have completed all the questions."
            return f"Analysis: {analysis}. \nNext question: {questions[session['current_question_index']]['question']}"