
# views.py
from sqlite3 import Timestamp
from django.http import JsonResponse
#from django.db import connection
# from contextlib import closing
from django.db import connections
from django.db.models import Q,Max
from django.forms.models import model_to_dict
from DataBase_MPMS.models import VTask,Aiqueryhistory,Syspara,Mettingmaster,Task,Goalmanagement, VTecmb
from ScheduleApp.models import Promtsql,PromptcategoryTbl
from django.shortcuts import render
from django.db import connection
from django.views import View
from django.conf import settings
import re
import os
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from PMIS.Services.TypeListService import TypeListService

from openai import OpenAI
from httpx import Client
# 默認的過濾詞
DEFAULT_SKIP_TXT_ARR = ['i', 'can', 'and', 'as', 'to', 'with', 'how']  # 英文默認過濾詞
DEFAULT_SKIP_TXT_ARR_CN = ["的", "地"]  # 中文默認過濾詞

from django.http import HttpResponse
from django.db import transaction

def get_vtask_list_tree(request):
    contact = request.GET.get('contact', '')
    all_contact = request.GET.get('allContact', '')
    record_id = request.GET.get('recordID', '')
    # period = request.GET.get('period', '')

    # Initial filter
    filter = "Progress='I'"

    # Build the filter string
    if contact:
        filter += f" AND Contact = '{contact}'"
    
    if all_contact:
        filter += f" AND ',' + ISNULL(AllContact, ' ') + ',' LIKE '%{all_contact}%'"
    
    if record_id:
        filter += f" AND RecordId = '{record_id}'"

    # if period:
    #     if '-' in period:
    #         periods = period.split('-')
    #         if len(periods) == 2:
    #             year_b = periods[0]
    #             year_e = periods[0]
    #             month_b = ""
    #             month_e = ""

    #             if periods[1] == "1":
    #                 month_b = "01"
    #                 month_e = "04"
    #             elif periods[1] == "2":
    #                 month_b = "04"
    #                 month_e = "07"
    #             elif periods[1] == "3":
    #                 month_b = "07"
    #                 month_e = "10"
    #             elif periods[1] == "4":
    #                 month_b = "10"
    #                 month_e = "01"
    #                 year_e = str(int(year_e) + 1)
                
    #             b_date_str = f"{year_b}-{month_b}-01"
    #             e_date_str = f"{year_e}-{month_e}-01"

    #             filter += f" AND ((PlanBDate >= '{b_date_str}' AND PlanBDate < '{e_date_str}') OR " \
    #                       f"(PlanEDate >= '{b_date_str}' AND PlanEDate < '{e_date_str}') OR " \
    #                       f"(PlanBDate <= '{b_date_str}' AND PlanEDate >= '{e_date_str}'))"

    # Call the stored procedure
    tree = []
    with connections['MPMS'].cursor() as cursor:
        # sql = f"EXEC dbo.GetSessionTrees @Filter = '{filter}', @UserName = '{request.user.username}', @FilterPeriod = ''"
        sql = "SET NOCOUNT ON {CALL dbo.GetSessionTrees(%s, %s, %s)}" # @Filter = '{filter}', @UserName = '{request.user.username}'
        cursor.execute(sql, [request.user.username, filter, ''])
        # cursor.callproc('GetSessionTrees', [filter, request.user.username, ''])
        columns = [column[0].lower() for column in cursor.description]
        for row in cursor.fetchall():
            obj = dict(zip(columns, row))
            tree.append(obj) 
        # rows = cursor.fetchall()
        # for row in rows:
        #     temp = {
        #         'sessionid': row[0],
        #         'recordid': row[1],
        #         'parentid': row[2],
        #         'allcontact': row[3],
        #         'pid': row[4],
        #         'tid': row[5],
        #         'sdesp': row[6],
        #         'contact': row[7],
        #         'progress': row[8],
        #         'pschedule': row[9],
        #         'aschedule': row[10],
        #         'planbdate': row[11],
        #         'planedate': row[12],
        #         'priority': row[13],
        #         'projectscore': row[14],
        #         'weight': row[15],
        #         'capacity': row[16],
        #         'outstandday': row[17],
        #         'outstandqty': row[18],
        #         'flowchartno': row[19],
        #         'djcapacity': row[20],
        #         'type': row[21]
        #     }
        #     tree.append(temp)

    # task_list = [task._asdict() for task in tree]
    return JsonResponse(tree, safe=False)


def get_filtered_tasks(request):
    selected_progress = request.GET.get('selectedProgress')
    selected_priority = request.GET.get('selectedPriority')
    selected_contact = request.GET.get('selectedContact')
    task_text = request.GET.get('taskText')
    selected_class = request.GET.get('selectedClass')
    session_data = request.GET.get('sessionData')  # Assume this is a list of dictionaries

    # Build the query
    sessions_query = Q()
    for session in session_data.split(','):

        pid, tid = session.split('-')
        sessions_query |= Q(pid=pid, tid=tid)

    # base_query = ~Q(progress='C') & ~Q(progress='F') & sessions_query
    base_query = sessions_query

    if selected_progress:
        base_query &= Q(progress=selected_progress)
    if selected_priority:
        base_query &= Q(priority=selected_priority)
    if selected_contact:
        base_query &= Q(contact=selected_contact)
    if task_text:
        base_query &= Q(task__icontains=task_text)
    if selected_class:
        base_query &= Q(class_field=selected_class)

    tasks = VTask.objects.filter(base_query).order_by('-schpriority')

    task_list = list(tasks.values())  # Convert queryset to list of dictionaries
    return JsonResponse({'tasks': task_list})


class GetTasksView(View):
    def contains_delete_or_update(self,sql_query):
        if not sql_query:
            return False
        pattern = re.compile(r'\b(delete|update|drop)\b', re.IGNORECASE)
        return bool(pattern.search(sql_query))
        
    def get(self, request):
        result = {'status':False, 'msg':'', 'data':None, 'columns':None, 'sql':''}
        record_id = request.GET.get('record_id','')
        contact = request.GET.get('contact','')
        inc_id = request.GET.get('condition','')
        question = request.GET.get('question','')
        if question.startswith('*'):
            question = question[1:] 
        query = None
        if inc_id:  
            query = Promtsql.objects.get(inc_id=inc_id)
        columns = []
        rows = []
        isai = True
        category = ''
        if query:               
            if query.ssql and query.sname == question:      
                isai = False  
                sql_query = query.ssql 
            elif query.sname == question: 
                category = query.category  
                query.isai = True
            else:
                query = Promtsql(category='',sname=question,isai=True,isapproved=False)
        else:
            query = Promtsql(category='',sname=question,isai=True,isapproved=False)              
       
        if isai:
            questions = []
            questions.append(question)   
            questions.append(category)
            if record_id:
                questions.append(f'RecordID is {record_id}')
            if contact:
                questions.append(f'Task Contact is {contact}')

            sql_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Data', 'Table Script.sql')
            # 讀取SQL文件內容
            sql_content = read_sql_file(sql_file_path)
            # 提問
            #question = "查詢聯繫人為qfq今天的任務"
            # 創建服務實例
            service = AnalysisService()
            # 調用服務方法進行分析            
            sql_query = service.question_from_sql(sql_content, questions)
            query.ssql = sql_query
            query.promptbyai = question
            query.category = category
            #query = Promtsql(category=category,sname=question,ssql=sql_query,isai=True,isapproved=False)
        #result['sql'] = sql_query
        if self.contains_delete_or_update(sql_query):
            result['msg'] = 'SQL statements containing DELETE or UPDATE keywords cannot be executed.'
        elif sql_query:
            history = None
            if isai:
                tables = extract_tables(sql_query)
                history = Aiqueryhistory(
                        question=question,
                        timestamp=datetime.now(),
                        sql_query=sql_query,
                        databaseobject=tables,
                        category=category,
                        status='N',
                        excuted_by=request.user.username
                    )
                print(tables)
            try:
                with connections['MPMS'].cursor() as cursor:   
                    # 執行查詢
                    #if params:
                        #cursor.execute(sql_query,params)
                    #else:
                    #cursor.execute(sql_query)
                    try:
                        cursor.execute(sql_query)
                    except Exception as exec_error:
                        print("Error executing SQL query:", str(exec_error))                        
                        # Handle or log the specific SQL execution error as needed
                        raise  # Re-raise the exception if you want the outer exception block to handle it
                    columns = [col[0].lower() for col in cursor.description]
                    rows = [dict(zip(columns, row)) for row in cursor.fetchall()] 
                    result['status'] = True      
                    result['data'] = rows                                  
                    result['columns'] = columns    
                    if isai:
                        history.status='Y'
            except Exception as e:
                print(str(e))  
                result['msg'] = "Error executing SQL query."              
            if history:
                history.save()
            if query.category and query.category.strip() != "":
                qs = PromptcategoryTbl.objects.filter(categoryno=query.category).first()
                # 構建返回數據
                if qs:
                    query.category = qs.category #返回在頁面顯示時不要用編號,改為用對應的描述
            result['promtsql'] = model_to_dict(query) 
        return JsonResponse(result, safe=False)


# 從數據庫中獲取設置的跳過文本
def get_skip_text():
    skip_txt_arr = DEFAULT_SKIP_TXT_ARR.copy()  # 深拷貝列表，避免修改默認值
    skip_txt_arr_cn = DEFAULT_SKIP_TXT_ARR_CN.copy()  # 深拷貝列表，避免修改默認值    

    try:
        result = TypeListService.get_typelist("search_skip")
        for row in result:
            if row['value'] == "search_skip_txt":
                # 將跳過的英文文本轉換為小寫
                skip_txt_arr = [word.lower() for word in row['label'].split(",")]
            elif row['value'] == "search_skip_txt_cn":
                # 將跳過的中文文本轉換為小寫
                skip_txt_arr_cn = [word.lower() for word in row['label'].split(",")]
    except Exception as e:
        print("Error fetching skip texts:", str(e))

    return skip_txt_arr, skip_txt_arr_cn

# 使用跳過文本過濾查詢
def get_real_search_value(search_txt, skip_txt_arr, skip_txt_arr_cn):
    if not search_txt:
        return ""

    # 去掉空格
    search_txt = search_txt.strip()

    # 匹配中文和非中文（包括英文和其他字符）
    chinese_match = re.findall(r'[\u4e00-\u9fa5]+', search_txt)
    english_match = re.findall(r'[^\u4e00-\u9fa5]+', search_txt)

    chinese_txt = "".join(chinese_match) if chinese_match else ""
    english_txt = "".join(english_match) if english_match else ""

    # 分割並處理英文字符，轉換為小寫並過濾掉無用的單詞
    english_txt = [word.lower() for word in english_txt.strip().split() if word.lower() not in skip_txt_arr]

    # 分割並處理中文字符，過濾掉無用的字符
    chinese_txt = [char for char in chinese_txt.strip() if char not in skip_txt_arr_cn]

    # 合併處理後的中英文結果
    new_word = english_txt + chinese_txt

    # 返回處理後的查詢字符串
    return new_word

def get_sqlscript_data(request):
    # 定義要返回的對象
    result = {'status': False, 'msg': '', 'data': None}
    desc = request.GET.get('searchvalue', '')
    filter_str = request.GET.get('filter', '')
    
    if desc.startswith('*'):
        desc = desc[1:]

    desc_words = []
    if desc:
        # 從後端獲取動態跳過文本，默認使用設定值
        skip_txt_arr, skip_txt_arr_cn = get_skip_text()

        # 從查詢內容中提取需要查詢的單詞
        desc_words = get_real_search_value(desc, skip_txt_arr, skip_txt_arr_cn)
    desc_conditions = Q()
    desc_conditions.connector = Q.AND
    for word in desc_words:
        desc_conditions.children.append(('sname__icontains', word))

    # 初始化查詢條件
    query_conditions = Q(params__isnull=True) | Q(params='')
    if filter_str:
        # 解析 filter_str 中的條件
        filter_conditions = {}
        for item in filter_str.split(';'):
            if '=' in item:
                key, value = item.split('=')
                filter_conditions[key] = value

        # 添加 filter 中的 category 條件
        if 'category' in filter_conditions and filter_conditions['category']:
            # 提取等號後面的值
            category_value = filter_conditions['category']
            
            # 從 PromptcategoryTbl 表中查詢對應的 categoryno
            category_record = PromptcategoryTbl.objects.filter(category=category_value).first()

            if category_record:
                # 如果找到對應的 categoryno，替換 filter_conditions 中的 category
                filter_conditions['category'] = category_record.categoryno
            query_conditions &= Q(category=filter_conditions['category'])

        # 添加 filter 中的 isapproved 條件
        if 'isapproved' in filter_conditions:
            if filter_conditions['isapproved'] == '0':
                query_conditions &= Q(isapproved=0) | Q(isapproved__isnull=True)
            else:
                query_conditions &= Q(isapproved=filter_conditions['isapproved'])

    try:
        if desc_words:
            data = Promtsql.objects.filter(desc_conditions & query_conditions).values('inc_id', 'sname', 'isai', 'category', 'isapproved')
        else:
            data = Promtsql.objects.filter(query_conditions).values('inc_id', 'sname', 'isai', 'category', 'isapproved')
        
        result['status'] = True
        result['data'] = [
            {**item, 'sname': '*' + item['sname'] if item['isai'] else item['sname']}
            for item in data
        ]
    except Exception as e:
        print(str(e))
        result['status'] = False
        result['msg'] = 'Error: ' + str(e)
    
    return JsonResponse(result, safe=False)




def read_sql_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        sql_content = file.read()
    return sql_content


class BaseService(object):
    def __init__(self, *args, **kwargs):
        super(BaseService, self).__init__(*args, **kwargs)
        self.apiClient = OpenAI(
            api_key=settings.OPENAPI_KEY,
            #organization=settings.OPENAI_ORGANIZATION,
            http_client=Client(proxies={
                "http://": settings.OPENAPI_PROXY_URL,
                "https://": settings.OPENAPI_PROXY_URL,
            }) 
        )

class AnalysisService(BaseService):

    def extract_sql(self, text):
        # 定义正则表达式来匹配以```sql```包裹的SQL语句
        sql_pattern = re.compile(
            r"```sql\s*(.*?)\s*```",
            re.IGNORECASE | re.DOTALL
        )

        # 搜索匹配的SQL语句
        match = sql_pattern.search(text)

        if match:
            sql_query = match.group(1)
            # 替换SQL语句中的分号
            cleaned_sql_query = sql_query.replace(';', '')
            return cleaned_sql_query
        else:
            return None

    def question_from_sql(self, sql_content, questions):
        # 將SQL內容轉為字符串
        data_str = sql_content

        # 構造對話內容
        conversation = [
            {"role": "system", "content": "Explain all concepts like I am expert."},
            {"role": "user", "content": f"我給了你三個表的結構，他們是有關聯的，我需要你根據這四個數據表結構和我給你的問題幫我生成可以執行的sql語句:[{data_str}]"},

            # {"role": "user", "content": "我給了你“會議主表”MettingMaster的表結構，當我查詢會議相關的數據時，應該查出此表且關聯V_Task表"},
            {"role": "user", "content": "我給了你“會議主表”MettingMaster的表結構"},
            {"role": "user", "content": '''
                MettingMaster 表結構:
                - COMPANY (char): COMPANY
                - CREATOR (char): 創建此會議的用戶
                - USR_GROUP (char): USR_GROUP
                - CREATE_DATE (char): 創建日期,格式為YYYYMMDD
                - MODIFIER (char): MODIFIER
                - MODI_DATE (char): 修改日期,格式為YYYYMMDDhhmmss
                - FLAG (numeric): FLAG
                - Id (char): 會議id,與Task表的DocPath字段相關聯。格式為YYMMDD+兩位數,如22042201,22042202,22042203  即代表2022年4月22日創建了三個會議。例如查詢最近三天的數據WHERE m.id >= CONVERT(VARCHAR(6), CONVERT(DATE, GETDATE() - 3), 12)；查詢昨天的數據where m.Id like (CONVERT(VARCHAR(6), CONVERT(DATE, GETDATE() - 1), 12)+'%')
                - Topic (varchar): 主題
                - Participants (text): 參會人員
                - MustRead (varchar): 必讀材料
                - UDF01 (varchar): 備用字段
                - UDF02 (varchar): 備用字段
                - UDF03 (char): 備用字段
                - UDF04 (varchar): 備用字段
                - UDF05 (varchar): 備用字段
                - INC_ID (int): INC_ID,自增主鍵
                - DiscussProcess (text): 討論過程
                - Summary (text): 會議摘要

                當需要查詢任務Task時，Task表與MettingMaster表之間的關係為:
                - Task 表通过 DocPath 关联 MettingMaster 表的 Id，即Task.DocPath=MettingMaster.id，且Task.Pid='11580' and Task.Tid='12' and Task.EditionID<>'1'
                - meeting的操作指的是Task表中的HOperation，當HOperation為空是未分配。
                '''},

            {"role": "user", "content": "我給了你“目標表”GoalManagement的表結構"},
            {"role": "user", "content": '''
            GoalManagement 表結構:
                - COMPANY (char): 公司名稱
                - CREATOR (char): 創建目標的用戶
                - USR_GROUP (char): 用戶組
                - CREATE_DATE (char): 創建日期，如20240614
                - MODIFIER (char): 修改目標的用戶
                - MODI_DATE (char): 修改日期，如20240614085144
                - FLAG (numeric): 狀態標記（如：目標狀態）
                - GoalId (int): 目標ID
                - CONTACT (char): 聯繫人。主要以此字段作為條件判斷
                - PERIOD (char): 目標週期，如2024-4，表示2024年的第四季度。主要以此字段作為條件判斷，若要轉換當前年份可以CAST(YEAR(GETDATE()) AS VARCHAR)
                - GOALTYPE (char): 目標類型，Q表示季度目標，M表示月目標，W表示周目標。主要以此字段作為條件判斷
                - MONTH (char): 月份，格式為YYYY-MM，通常不以此字段作為條件判斷
                - WEEK (int): 周次，範圍1-52，通常不以此字段作為條件判斷
                - GOALDESC (text): 目標描述
                - COMMENT (text): 評論或備註
                - SESSIONS (varchar): 目標關係到的sessions
                - PROGRESS (int): 進度
                - PRIORITY (int): 優先級
                - ALLOCATEUSER (numeric): 分配的用戶數量
                - RECORDID (char): 目標關係到的工程id
                - INC_ID (int): 自增主鍵，唯一標識符
                - UDF01 (varchar): 備用字段1
                - UDF02 (varchar): 備用字段2
                - UDF03 (char): 備用字段3
                - UDF04 (varchar): 備用字段4
                - UDF05 (varchar): 備用字段5
                - RELATIONTASKS (text): 目標關係到的Tasks

            '''},
            {"role": "user", "content": "Task表與SubProject表的關係是SubProjectID  = RecordID, 這裏是一個查詢語句的實例，你可以參考這個實例中的返回值和關聯關係。"},
            {"role": "user", "content": '''
            SELECT  
                task.INC_ID,        
                task.Pid + '-' + CAST(task.Tid AS VARCHAR) + '-' + CAST(task.TaskID AS VARCHAR) AS TaskNo,
                task.Task,
                task.Contact,
                task.PlanBDate,
                task.PlanEDate,
                task.Progress,
                task.Remark,
                task.SessionPriority,
                task.SchPriority,
                task.Class,
                task.relationID,
                task.HOperation,
                sp.ProjectName,                
                sp.RecordID,    
                tl.SDesp,
                tl.Contact AS TasklistContact,
                tl.PlanBDate AS TasklistPlanBDate,
                tl.PlanEDate AS TasklistPlanEDate,
                tl.Progress AS TasklistProgress          
            FROM 
                [dbo].[Task] task
            LEFT JOIN 
                [dbo].[SubProject] sp ON task.SubProjectID = sp.RecordID
            LEFT JOIN 
                [dbo].[tasklist] tl ON task.Pid = tl.Pid AND task.Tid = tl.Tid
            '''},            
            {"role": "user", "content": "我需要你根據下面的問題生成sql語句, 只需要返回sql語句即可，返回的sql語句的格式如下:```sql語句```,不需要其他信息"},
            
        ]
        if questions:
            for question in questions:
                conversation.append({"role": "user", "content": question})

        # 訪問ChatGPT並打印返回結果
        response = self.apiClient.chat.completions.create(
            model=settings.OPENAPI_MODEL,
            messages=conversation
        )

        for choice in response.choices:
            sqlStr = self.extract_sql(choice.message.content)
            print(sqlStr)
            return sqlStr

# def get_category_data(request):
#     # 定義要返回的對象
#     result = {'status': False, 'msg': '', 'data': None}
#     desc = ''
#     if 'searchvalue' in request.GET:
#         desc = request.GET.get('searchvalue')     

#     try:
#         if desc:
#             data = Promtsql.objects.filter(Q(category__icontains=desc) & (Q(params__isnull=True) | Q(params=''))).values('category').distinct()
#         else:
#             data = Promtsql.objects.filter(Q(params__isnull=True) | Q(params='')).values('category').distinct()                           
#         result['status'] = True
#         result['data'] = list(data)
#     except Exception as e:
#         print(str(e))
#     return JsonResponse(result, safe=False)

def get_category_data(request):
    # 定义返回的对象
    result = {'status': False, 'msg': '', 'data': None}
    desc = ''
    
    if 'searchvalue' in request.GET:
        desc = request.GET.get('searchvalue')

    try:
        if desc:
            # 根据输入值筛选分类数据
            data = PromptcategoryTbl.objects.filter(Q(category__icontains=desc)).values('category').distinct()
        else:
            # 如果没有输入值，返回所有分类数据
            data = PromptcategoryTbl.objects.all().values('category').distinct()
        
        # 如果有输入值且没有匹配到任何数据，返回空数据
        if not data:
            result['data'] = []
        else:
            result['data'] = list(data)
            
        result['status'] = True
    except Exception as e:
        result['msg'] = str(e)
    
    return JsonResponse(result, safe=False)



@csrf_exempt
def approve_condition(request):    
    def add_promtsql(category_no):
        max_ssid = int(Promtsql.objects.aggregate(Max('ssid'))['ssid__max'] or 0) + 10
        return Promtsql(ssid=max_ssid, sname=data['sname'], ssql=data['ssql'], isai=data['isai'], isapproved=data['isapproved'], category=category_no, timestamp=datetime.now(),promptbyai=data['promptbyai'])  

    result = {'status': False, 'msg': '', 'data':None}
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            inc_id = data.get('inc_id')
            if data['sname'].startswith('*'):
                data['sname'] = data['sname'][1:] 

            category_description = data['category'].strip()
            category_no = data['category']
            #類別為空時不查詢類別表獲取數據
            if category_description != '':
                # 查詢 PromptcategoryTbl 表，根據類別描述 (英文) 獲取對應的數字編號
                category_record = PromptcategoryTbl.objects.filter(category=category_description).first()

                if category_record:
                    # 如果找到類別，則使用其編號
                    category_no = category_record.categoryno
                else:
                    # 如果沒有找到類別，生成新的類別編號（每次加10）
                    max_category_no = PromptcategoryTbl.objects.aggregate(Max('categoryno'))['categoryno__max'] or 0
                    category_no = max_category_no + 10

                    # 創建新的 PromptcategoryTbl 記錄，這部分邏輯會在事務中保存
                    new_category_record = PromptcategoryTbl(
                        category=category_description,
                        categoryno=category_no
                    )

            if inc_id:
                promtsql = Promtsql.objects.get(inc_id=inc_id)
                if promtsql:
                    promtsql.sname=data['sname']
                    promtsql.isai=data['isai']
                    promtsql.isapproved=data['isapproved']
                    promtsql.ssql=data['ssql']
                    promtsql.category=category_no 
                    promtsql.timestamp=datetime.now() 
                    promtsql.promptbyai=data['promptbyai']                  
            else:
                if category_description != '':
                    promtsql = add_promtsql(category_no)
                else:
                    promtsql = add_promtsql('')

            # 開啟事務處理，只保存數據，不查詢
            with transaction.atomic('MPMS'):
                # 創建事務保存點
                save_id = transaction.savepoint(using='MPMS')
                # 異常捕獲
                try:
                    # category_description等於 "" 時不新增類別數據
                    if category_description != '':
                        # 如果新類別記錄存在，保存它
                        if not category_record:
                            new_category_record.save()
                    # 保存 Promtsql
                    promtsql.save()
                    # 成功提交事務
                    transaction.savepoint_commit(save_id, using='MPMS')
                except Exception as e:
                    # 發生異常，回滾到保存點
                    transaction.savepoint_rollback(save_id, using='MPMS')
                    # 可以選擇拋出異常或處理異常
                    raise e
            # 如果事務執行成功，則返回結果
            promtsql.category=category_description
            result['data'] = model_to_dict(promtsql)
            result['status'] = True
        except Exception as e:
            print(str(e))
            result['msg'] = 'Failed to save the prompt.'
        
    return JsonResponse(result, safe=False)

def get_promtsql_by_inc_id(request):
    result = {'status': False, 'msg': '', 'data': None}
    id = request.GET.get('id', '')

    # 檢查 id 是否為空
    if not id:
        result['msg'] = 'ID cannot be empty.'
        return JsonResponse(result, safe=False)

    try:
        # 根據 inc_id 獲取 Promtsql 的記錄
        promtsql = Promtsql.objects.get(inc_id=id)
        if promtsql.category and promtsql.category.strip() != "":
            qs = PromptcategoryTbl.objects.filter(categoryno=promtsql.category).first()
            # 構建返回數據
            if qs:
                promtsql.category = qs.category #返回在頁面顯示時不要用編號,改為用對應的描述
        result['data'] = model_to_dict(promtsql)
        result['status'] = True
    except Promtsql.DoesNotExist:
        result['msg'] = f'No Promtsql record found with inc_id {id}.'
    except Exception as e:
        print(str(e))
        result['msg'] = 'An error occurred while fetching the data.'

    return JsonResponse(result, safe=False)

def get_user_prompt_approve(request):
    result = {'status': False, 'msg': '', 'data': False}
    try:
        username = request.user.username    
        # 获取 'PromptApprove' 对应的 fvalue
        param = Syspara.objects.filter(nfield='PromptApprove').values_list('fvalue', flat=True).first()
        
        if param:
            # 将 fvalue 拆分为列表，并检查 username 是否存在其中
            approved_users = param.split(',')
            if username in approved_users:
                result['data'] = True
        result['status']=True
    except Exception as e:
        print(str(e))
    
    return JsonResponse(result, safe=False)

def extract_tables(sql):
    import re
    # 正则表达式匹配表名
    table_pattern = re.compile(r'\[dbo\]\.\[(\w+)\]')
    tables = table_pattern.findall(sql)
    
    # 去重并按字母顺序排序
    tables = sorted(set(tables))
    
    # 将表名连接成一个逗号分隔的字符串
    return ','.join(tables)

# @csrf_exempt
# def session_group_task(request):
#     if request.method == 'POST':
#         session_list = request.POST.get('sessionList')
        
#         # 确认 session_list 是否存在
#         if not session_list:
#             return JsonResponse({'error': 'Session list is missing'}, status=400)
        
#         # 在这里可以处理 session_list，做任何你需要的操作
#         context = {'session_list': session_list}
        
#         # 返回一个 JSON 响应，表示数据已经成功接收
#         return JsonResponse({'message': 'Data received successfully', 'session_list': session_list})
    
#     # 如果不是 POST 请求，返回错误响应
#     return JsonResponse({'error': 'Invalid request method'}, status=405)

# 定义全局变量
global_session_data = {}

@csrf_exempt
def session_group_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_list = data.get('sessionList')
            
            if not session_list:
                return JsonResponse({'error': 'Session list is missing'}, status=400)
            
            # 日期格式化函数，将 "YYYY-MM-DDTHH:MM:SS" 转换为 "YYYY-MM-DD"
            def format_date(date_string):
                if date_string:
                    try:
                        # 将日期字符串解析为 datetime 对象
                        date_obj = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
                        # 返回 "YYYY-MM-DD" 格式的日期字符串
                        return date_obj.strftime('%Y-%m-%d')
                    except ValueError:
                        # 如果日期格式不正确，返回原始字符串或处理错误
                        return date_string
                return None

            # 对 session_list 进行处理，拆分 taskno 为 pid、tid 和 taskid，并格式化日期
            for session in session_list:
                taskno = session.get('taskno', '')
                if taskno:
                    try:
                        # 按 - 分割 taskno
                        pid, tid, taskid = taskno.split('-')
                        # 将 pid, tid, taskid 加入 session
                        session['pid'] = pid
                        session['tid'] = tid
                        session['taskid'] = taskid
                    except ValueError:
                        # 处理 taskno 不能正确拆分的情况
                        session['pid'] = session['tid'] = session['taskid'] = None

                # 格式化相关日期字段
                session['planbdate'] = format_date(session.get('planbdate'))
                session['planedate'] = format_date(session.get('planedate'))
                session['tasklistplanbdate'] = format_date(session.get('tasklistplanbdate'))
                session['tasklistplanedate'] = format_date(session.get('tasklistplanedate'))
            
            # 打印 session_list 确认数据是否正确
            print(f"Processed session list: {session_list}")
            
            # 使用全局变量存储处理后的 session_list
            global global_session_data
            global_session_data['session_list'] = session_list  # 存储数据到全局变量
            
            return JsonResponse({'message': 'Data received successfully'})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)



def get_session_list(request):
    # 从全局变量中获取 session_list
    global global_session_data
    session_list = global_session_data.get('session_list', [])
    
    print(f"确认数据是否正确: {session_list}")
    
    return JsonResponse({'session_list': session_list})


@csrf_exempt
def execute_sql(request):
    if request.method == 'POST':
        try:
            # 从请求体获取SQL
            data = json.loads(request.body)
            sql_query = data.get('sql', '')

            # 检查SQL是否为空
            if not sql_query.strip():
                return JsonResponse({'status': False, 'msg': 'SQL查询不能为空'})

            # 防止执行删除、更新等危险操作
            if any(keyword in sql_query.lower() for keyword in ['delete', 'update', 'drop']):
                return JsonResponse({'status': False, 'msg': '禁止执行DELETE、UPDATE或DROP语句'})

            with connections['MPMS'].cursor() as cursor:
                cursor.execute(sql_query)
                columns = [col[0] for col in cursor.description]  # 获取列名
                rows = cursor.fetchall()  # 获取结果数据
                data = [dict(zip(columns, row)) for row in rows]  # 将数据转为字典形式

            return JsonResponse({'status': True, 'data': data, 'columns': columns})

        except Exception as e:
            print(f"SQL执行错误: {e}")
            return JsonResponse({'status': False, 'msg': 'SQL执行出错'})

    return JsonResponse({'status': False, 'msg': '只接受POST请求'})

def get_sysbugno(request):
    """
    功能描述: 獲取系統問題上報單別,單號
    """
    taskno = request.GET.get('taskno', '')
    result = {'udf10':'','udf01':''}
    try:
        if taskno:
            task = VTask.objects.filter(taskno=taskno).first()
            if task:
                result['udf01'] = task.udf01
                result['udf10'] = task.udf10
    except Exception as e:
        print(str(e))
    return JsonResponse(result)



def get_meeting_master(request):
    try:
        # 从 GET 参数中获取 start_date 和 end_date
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        # 校验 start_date 参数是否存在
        if not start_date:
            return JsonResponse({'status': False, 'message': 'Missing start_date'}, status=400)

        # 将 start_date 和 end_date 转换为日期对象
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        
        # 如果没有传入 end_date，则默认使用当前日期
        if not end_date:
            end_date_obj = datetime.today()
        else:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

        # 将日期转换为 YYYYMMDD 格式
        start_date_str = start_date_obj.strftime('%Y%m%d')
        end_date_str = end_date_obj.strftime('%Y%m%d')

        # 使用 id 的前 6 位进行转换（YYDDMM 转换为 YYYYMMDD）
        data = Mettingmaster.objects.filter(id__gte='{}01'.format(start_date_str[2:]), id__lte='{}01'.format(end_date_str[2:]))

        # 将查询结果转换为需要的格式（根据实际字段调整）
        result_data = list(data.values())

        # 返回 JSON 响应
        return JsonResponse({'status': True, 'data': result_data})

    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)}, status=500)
    

def get_meeting_detail(request):
    # 从查询参数中获取 id
    id = request.GET.get('id')

    if not id:
        return JsonResponse({'status': False, 'message': 'Missing id parameter'}, status=400)

    try:
        # 查询 Task 模型中符合条件的数据
        task_data = VTask.objects.filter(docpath=id, pid='11580', tid='12')

        # 如果没有找到匹配的记录
        if not task_data.exists():
            return JsonResponse({'status': False, 'message': 'No matching task found'}, status=404)

        # 转换查询结果为列表
        result_data = list(task_data.values())
        # 将查询结果转换为字典，并添加 taskno 字段
        # result_data = []
        # for task in task_data:
        #     task_dict = model_to_dict(task)  # 转换 Task 对象为字典

        #     # 拼接 taskno
        #     task_dict['taskno'] = f"{task.pid}-{int(task.tid)}-{int(task.taskid)}"

        #     result_data.append(task_dict)

        # 返回 JSON 响应
        return JsonResponse({'status': True, 'data': result_data})

    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)}, status=500)



def get_Goal_master(request):
    try:
        contact = request.GET.get('contact')
        goaltype = request.GET.get('goaltype')
        year = request.GET.get('year')
        number = request.GET.get('number')

        # 校验 year 是否存在，number 可以为空
        if not year:
            return JsonResponse({'status': False, 'message': 'Missing year parameter'}, status=400)

        # 根据是否有 number 来设置 period 字段
        if number:
            period = f"{year}-{number}"  # 精确匹配
        else:
            period = f"{year}-"  # 模糊匹配

        # 构建查询条件
        filters = {'period__icontains': period}  # 进行模糊匹配

        # 如果 contact 不是空字符串，则加入筛选条件
        if contact != '':
            filters['contact'] = contact
        
        # 如果 goaltype 不是空字符串，则加入筛选条件
        if goaltype != '':
            filters['goaltype'] = goaltype

        # 查询 Goalmanagement 表并返回结果
        data = Goalmanagement.objects.filter(**filters)

        # 将查询结果转换为字典列表
        result_data = list(data.values())

        # 返回 JSON 响应
        return JsonResponse({'status': True, 'data': result_data})

    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)}, status=500)
    

def get_technical(request):
    try:
        bdate = request.GET.get('bdate', '')
        edate = request.GET.get('edate', '')
        # content = request.GET.get('content', '')
        category = request.GET.get('category', '')
        area = request.GET.get('area', '')
        technicalID = request.GET.get('technicalID', '')
        contact = request.GET.get('contact', '')
        queryset = VTecmb.objects.all().values('mb015c', 'mb004', 'mb016', 'mb023', 'mb008', 'creator', 'create_date')

        filters = {}

        if bdate and edate:
            filters['create_date__range'] = [bdate, edate]

        if category:
            filters['mb015c__icontains'] = category

        if area:
            filters['mb016__icontains'] = area

        if technicalID:
            filters['mb023__icontains'] = technicalID

        if contact:
            filters['creator'] = contact

        if filters:
            queryset = VTecmb.objects.filter(**filters).values('mb015c', 'mb004', 'mb016', 'mb023', 'mb008', 'creator', 'create_date')

        result = list(queryset)
        return JsonResponse({'status': True, 'data': result})
    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)}, status=500)

