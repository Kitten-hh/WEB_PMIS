##########################################################
##功能描述：Schedule排期邏輯
##
##
##########################################################
from DataBase_MPMS import models as models
from django.forms.models import model_to_dict
import inspect
from django.db import transaction
from BaseProject.tools import DateTools
from django.db import connections,DataError
from ..Services import QueryFilterService as qs
import datetime
import pandas as pd
from pandas import Series, DataFrame
import math as Math
from django.db.models import Sum,Count,Max,Min,Avg,Q
import pytz

FIXED_DATE_CATEGORY = 1

class ScheduleParam(object):
    SCHEDULE_PARAM_FLAG = 'ScheduleParams'
    @staticmethod
    def read_sys_params():
        rs = models.Syspara.objects.filter(ftype=ScheduleParam.SCHEDULE_PARAM_FLAG)
        result = {row.nfield:row.fvalue for row in list(rs)} 
        return result

    @staticmethod
    def read_user_params(user_name:str):
        period_rs = models.Schperiod.objects.values('period','completion').all()
        periods_sys = {row['period']:row['completion'] for row in period_rs}
        rs = models.VSchuserparamsQuarterly.objects.filter(contact = user_name)
        curr_quarter_user_params = {}
        next_quarter_user_params = {}
        for row in list(rs):
            cpt_obj = periods_sys
            if row.periods and row.periodscpt:
                periods = [period.strip().replace('[','').replace(']','') for period in row.periods.split('+')]
                periodsCpt = [cpt.strip().replace('[','').replace(']','') for cpt in row.periodscpt.split('+')]
                if len(periods) == len(periodsCpt):
                    for index, period in enumerate(periods):
                        if period in periods_sys.keys():
                            cpt_obj[period] = int(periodsCpt[index])                    
                row.periods = periods
            if 'Current' == row.quarterlyflag:
                curr_quarter_user_params = model_to_dict(row)
                curr_quarter_user_params.update(cpt_obj)
            else:
                next_quarter_user_params = model_to_dict(row)
                next_quarter_user_params.update(cpt_obj)
        return periods_sys,curr_quarter_user_params, next_quarter_user_params

    @staticmethod
    def get_type_list():
        rs = models.Schtype.objects.values('typeno','typename').all()
        result = {}
        for row in rs:
            result[row['typeno']] = row['typename']
        return result
        
    @staticmethod
    def save_params(user,sys_params, cur_user_parasm):
        sys_params_arr = []
        for key,value in sys_params.items():
            param = models.Syspara(nfield=key, ftype=ScheduleParam.SCHEDULE_PARAM_FLAG, fvalue=value)
            sys_params_arr.append(param)
        data = {key:value for key,value in cur_user_parasm.items() if key in [a.attname for a in models.Schuserparams._meta.get_fields()]}
        user_params = models.Schuserparams(**data)
        user_params.quarterly = '{0}-{1}'.format(DateTools.formatf(datetime.datetime.now(), '%Y') ,DateTools.getQuarter(datetime.datetime.now()))
        user_params.contact = user
        user_params.periods = '+'.join(['[{0}]'.format(i) for i in user_params.periods])
        if user_params.periods:
            user_params.periodscpt = '+'.join(['[{0}]'.format(cur_user_parasm[period.strip().replace('[','').replace(']','')]) for period in cur_user_parasm['periods']])
        try:
            with transaction.atomic():
                user_params.save()
                for param in sys_params_arr:
                    param.save()
            return True
        except Exception as e:
            print(str(e))
        return False
    @staticmethod
    def get_user_list():
        rs = models.Users.objects.values('username').filter(dept='Mis', groupname='電腦部')
        return [row['username'] for row in rs]
    @staticmethod
    def get_max_sch_type_no():
        qs = models.Schtype.objects.values('typeno').all().order_by('-typeno')[:1]
        max_no = 10
        if len(qs) > 0:
            max_no = qs[0]['typeno']
            max_no += 10
        return max_no

class ScheduleSource(object):
    '''
    功能描述：獲取排期任務來源對象
    '''
    def __init__(self, quarterly=None,users:set=None, **kwargs):
        self._quarterly = quarterly
        self.users = users
        self.source = {}
        for key, value in kwargs.items():
            setattr(self, key, value)
         
    def parse_sch_type_filter(self):
        '''
        功能描述：解析排期任務類型中的Logic查詢條件，並保存加數據庫
        '''
        rs = models.Schtype.objects.all()
        sch_types = list(rs)
        for row in sch_types:
            str_filter = row.logic
            #轉換查詢條件中的日期，將2000/06/01轉為當前日期
            str_filter = qs.convertDate(str_filter)
            #轉換查詢條件中的Quarterly weekly等參數
            str_filter = qs.analyzeQueryFilter(str_filter)
            row.udf01 = str_filter
        #將解析好的查詢條件，保存回數據庫
        with transaction.atomic():
            models.Schtype.objects.bulk_update(sch_types, fields=['udf01'])

    def get_session_task(self):
        '''
        功能描述：獲取用戶需要排期的Session和任務列表
        主要調用存儲過程GetSchSessionAndTask來讀取數據，注意該存儲過程返回的是兩個數據集
        '''
        self.parse_sch_type_filter()
        start, end = self.get_quarterly_date()
        #構造查詢Session的查詢條件
        str_filter = '''((',' + ISNULL(AllContact,' ') + ',' like '%%,{0},%%') and Progress='I') and 
                    ((PlanBDate <= '{1}' and PlanEDate >= '{2}') or (PlanBDate <= '{3}' and PlanEDate >= '{4}'))'''
        
        #如果有多個用戶，分用戶讀取
        for user in self.users:
            local_filter = str_filter.format(user, DateTools.format(start), DateTools.format(start), DateTools.format(end), DateTools.format(end))
            params = [user,self._quarterly,'', local_filter, '']
            with connections['MPMS'].cursor() as cursor:
                cursor.execute('SET NOCOUNT ON {CALL GetSchSessionAndTask (%s,%s,%s,%s,%s)}', params)
                #將數據裝載到model中
                local_fields = {a.column:a.attname for a in models.VTasklist._meta.get_fields()}
                columns = [(lambda m:local_fields[m] if m in local_fields.keys() else m)(column[0]) for column in cursor.description]
                ##columns = [column[0] for column in cursor.description]
                sessions = []
                for row in cursor.fetchall():
                    obj = {key:value for key,value in dict(zip(columns,row)).items() if key in local_fields.values()}
                    sessions.append(models.VTasklist(**obj))
                ##讀取Tasks內容
                cursor.nextset()
                local_fields = {a.column:a.attname for a in models.VTask._meta.get_fields()}
                columns = [(lambda m:local_fields[m] if m in local_fields.keys() else m)(column[0]) for column in cursor.description]
                tasks = []
                for row in cursor.fetchall():
                    obj = dict(zip(columns,row))
                    vtask = models.VTask()
                    for key,value in obj.items():
                        setattr(vtask, key,value)
                    tasks.append(vtask)
                self.source[user] = {'sessions':sessions, 'tasks': tasks}
    def get_fixeddate_task(self):
        '''
        功能描述：獲取用戶需要排期的fixeddate任務列表
        '''
        self.parse_sch_type_filter()
        start, end = self.get_quarterly_date()
        #構造查詢Session的查詢條件
        str_filter = '''((',' + ISNULL(AllContact,' ') + ',' like '%%,{0},%%') and Progress='I') and 
                    ((PlanBDate <= '{1}' and PlanEDate >= '{2}') or (PlanBDate <= '{3}' and PlanEDate >= '{4}'))'''
        
        #如果有多個用戶，分用戶讀取
        for user in self.users:
            local_filter = str_filter.format(user, DateTools.format(start), DateTools.format(start), DateTools.format(end), DateTools.format(end))
            params = [user,self._quarterly,'', local_filter, '','Y']
            with connections['MPMS'].cursor() as cursor:
                cursor.execute('SET NOCOUNT ON {CALL GetSchSessionAndTask (%s,%s,%s,%s,%s,%s)}', params)
                #將數據裝載到model中
                ##讀取Tasks內容
                local_fields = {a.column:a.attname for a in models.VTask._meta.get_fields()}
                columns = [(lambda m:local_fields[m] if m in local_fields.keys() else m)(column[0]) for column in cursor.description]
                tasks = []
                for row in cursor.fetchall():
                    obj = dict(zip(columns,row))
                    vtask = models.VTask()
                    for key,value in obj.items():
                        setattr(vtask, key,value)
                    tasks.append(vtask)
                ##讀取已經存在的Priority
                cursor.nextset()
                exists_priority_list = []
                for row in cursor.fetchall():
                    exists_priority_list.append(row[0])
                ##讀取最大Priority及已經完成的FixedDate
                cursor.nextset()
                row = cursor.fetchone()
                self.source[user] = {'tasks': tasks, 'exists_prioritys': exists_priority_list, 'max_sch_no':row[0], 'exists_finish_qty':row[1]}

    def get_quarterly_date(self):
        '''
        功能描述：根據季度字段串獲取季度開始與結束日期,
        如果沒有傳入季度字符串，則以獲取當前季度
        '''
        if self._quarterly:
            quar_arr = self._quarterly.split('-')
            year = int(quar_arr[0])
            month = 3 * (int(quar_arr[1]) - 1) + 1
            start_date = datetime.date(year, month, 1)
            end_date = DateTools.getEndOfQuarter(start_date)
        else:
            self._quarterly = '{0}-{1}'.format(DateTools.formatf(datetime.datetime.now(),'%Y'), DateTools.getQuarter(datetime.datetime.now()))
            start_date = DateTools.getBeginOfQuarter(datetime.datetime.now())
            end_date = DateTools.getEndOfQuarter(datetime.datetime.now())

        return start_date, end_date

class QuarterlyScheduleLogic(object):
    '''
    功能描述：
    '''
    def __init__(self, quarterly=None,users:set=None,start_date=None, **kwargs):
        self.quarterly = quarterly
        self.users = users
        self.source = {}
        self.sch_source = None
        if start_date:
            self.start_date = start_date
        else:
            self.start_date = datetime.datetime.now()
        self.in_session_logic = None
        self.sys_params = None #排期系統參數
        self.user_params = {} #排期用戶參數
        self.noon_start = None
        self.noon_end = None
        self.fixed_date_type = 10
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.init_data()            

    def init_data(self):
        '''
        功能描述:初始化數據，獲取排期排期的Session及任務列表，對任務Session內排期
        '''
        #獲取排期系統參數
        self.sys_param = ScheduleParam.read_sys_params()
        try:
            self.fixed_date_type = int(self.sys_param['FixedDateType'])
        except:
            pass
        #獲取排期用戶參數
        for user in self.users:
            self.user_params[user] = ScheduleParam.read_user_params(user)
        #讀取用戶需要排期的Session及任務列表
        self.sch_source = ScheduleSource(self.quarterly, self.users)        
        self.sch_source.get_session_task()
        #計算任務在Session內的排期優先級
        self.in_session_logic = ScheduleInSessionLogic(source=self.sch_source.source, fixed_date_type=self.fixed_date_type)
        self.in_session_logic.calculate_priority_insession()
        self.source = self.in_session_logic.source
        #初始中午休息時間
        noon_break = self.sys_param['NoonBreak'] #中午休息時間
        noon_arry = noon_break.split(',')
        self.noon_start = DateTools.parsef(noon_arry[0], '%H:%M')
        self.noon_end = DateTools.parsef(noon_arry[1], '%H:%M')

    def big_schedule(self):
        '''
        功能描述：以Session循環的方式對任務進行大排期
        '''
        for key, value in self.source.items():
            self.schedule_with_user(key, value)
    def get_user_param(self, user):
        '''
        功能描述：根據排期季度及用戶獲取用戶排期參數
        '''
        user_param = self.user_params[user]
        curr_quarterly = '{0}-{1}'.format(DateTools.formatf(datetime.datetime.now(), '%Y') ,DateTools.getQuarter(datetime.datetime.now()))
        param = user_param[1]
        if curr_quarterly != self.quarterly:
            param = user_param[2]
        return param

    def get_user_period(self, user):
        '''
        功能描述：根據排期季度及用戶獲取排期期間
        '''
        param = self.get_user_param(user)
        if param:
            return param.get('periods')
        else:
            return []
    def get_user_period_info(self, user):
        param = self.get_user_param(user)
        periods = {a:{'Capacity':param[a],} for a in param.get('periods')}
        qs = models.Schperiod.objects.all()
        ##處理某些用戶沒有某個period,需要將該period的時間分配給其他Period
        sys_periods = {row.period:row.__dict__ for row in qs}
        self.merge_split_period(sys_periods, periods, False)
        for key,row in sys_periods.items():
            period = periods[key]
            period.update(row)
        return periods
            
    def is_allEmpty(self, session, Task_Arry):
        for row in session.itertuples():
            if not Task_Arry[row.Index].empty:
                return False
        return True

    def schedule_with_user(self, user, source):
        '''
        功能描述：對單個用戶進行大排期
        '''
        sessions = source['sessions'] #session列表
        tasks = source['tasks']  #任務列表
        session = pd.DataFrame(list(session.__dict__ for session in sessions), columns=['sessionid','capacity','djcapacity', 'schrate'])
        session['order'] = session.index
        tasks_frame = pd.DataFrame(list(task.__dict__ for task in tasks), columns=['tasklistno','Period','taskno','TypeNo','sess_priority'])        
        ##從任務列表中取出session及不同period的不重覆數據，下面會用於分組
        tasks_group_session:DataFrame = tasks_frame[['tasklistno','Period']].drop_duplicates()
        tasks_group_session.rename(columns={'tasklistno':'sessionid'}, inplace=True)
        ##重建索引
        tasks_group_session.reset_index(drop=True, inplace=True)
        tasks_group_session = tasks_group_session.merge(session, on=['sessionid'], how='left')
        ##設置默認session capacity, djcapacity
        if self.sys_param.get('DefaultCapacity'):
            tasks_group_session['capacity'] = tasks_group_session['capacity'].fillna(int(self.sys_param.get('DefaultCapacity'))).astype(int)
        ##設置Sch Rate
        tasks_group_session['schrate'] = tasks_group_session['schrate'].fillna(0)
        Task_Arry = {}
        ##將任務按Period和Session分成多個數據表
        for row in tasks_group_session.itertuples():
            SessionId = row.sessionid
            Period = row.Period
            Tasks = tasks_frame.loc[(tasks_frame['tasklistno'] == SessionId) & (tasks_frame['Period'] == Period), ['taskno','TypeNo', 'sess_priority']]
            Tasks.sort_values(['sess_priority'], ascending=[False], inplace=True)
            Task_Arry[row.Index] = Tasks        
        
        ##將數據按Period和Session分成多個數據表
        user_priods = self.get_user_period(user)
        result = {}
        for period in user_priods:
            result[period] = pd.DataFrame(columns=tasks_frame.columns)
            period_session = tasks_group_session.loc[tasks_group_session['Period'] == period].sort_values(['order'], ascending=[True]) #將Session排序
            user_capacity = self.get_user_param(user).get(period,None)
            #if user_capacity:
                #period_session['capacity'] = period_session['capacity'].apply(lambda x: int(user_capacity) if int(x) < user_capacity else int(x))
            rate_record = {} #用於記錄排期頻率

            while(not self.is_allEmpty(period_session, Task_Arry)):
                for row in period_session.itertuples():
                    if Task_Arry[row.Index].empty:
                        continue
                    ##設置排期頻率
                    if not row.Index in rate_record and row.schrate > 0:
                        rate_record[row.Index] = -1
                    get_rows = Task_Arry[row.Index].iloc[0:row.capacity]
                    ##將取出的任務添加到結果集中
                    result[period] = result[period].append(get_rows, ignore_index=False)
                    ##刪除這些已經添加過的任務
                    Task_Arry[row.Index].drop(get_rows.index, inplace=True)
                    ##累加所有排期頻率
                    for key,value in rate_record.items():
                        local_value = value + 1
                        local_row = period_session.loc[key]
                        if local_value >= local_row.schrate and not Task_Arry[key].empty:
                            get_rows = Task_Arry[key].iloc[0:local_row.capacity]
                            result[period] = result[period].append(get_rows, ignore_index=False)
                            Task_Arry[key].drop(get_rows.index, inplace=True)
                            rate_record[key] = 0
                        else:
                            rate_record[key] = local_value                
            if self.sys_param.get('IntervalSchPriority'):
                interval = int(self.sys_param.get('IntervalSchPriority'))
            result[period]['SchPriority'] = range(len(result[period]) * interval, 0, interval * -1)
            ##將計算的排期值寫回Task中
            for row in result[period].itertuples():
                setattr(tasks[row.Index], 'SchPriority', row.SchPriority)
                setattr(tasks[row.Index], 'SchBDate', None)
                setattr(tasks[row.Index], 'SchEDate', None)
        self.assignment_date(user, result, tasks)
        UpdateScheduleTask(user,self.quarterly, tasks)
    def assignment_date(self,user,period_tasks, tasks_array):
        '''
        功能描述：根據Period分配任務的計畫日期
        '''
        if not period_tasks:
            return
        #fixed date不需要分配日期
        period_tasks = {key:value.loc[value['TypeNo'] != self.fixed_date_type] for key,value in period_tasks.items()}
        print('a')
        print(datetime.datetime.now())
        periods = self.get_user_period_info(user)
        result = pd.DataFrame(columns= next(iter(period_tasks.values())).columns)
        result['start'] = datetime.datetime.now()
        result['end'] = datetime.datetime.now()
        tasks = {key:value for key,value in period_tasks.items() if key in periods.keys()}
        period_list = list(a[0] for a in sorted(tasks.items(), key=lambda d: Math.ceil(len(d[1])/periods[d[0]]['Capacity'])))        
        self.merge_split_period(periods, tasks)
        local_date = self.start_date
        while(not self.is_allEmptyWithPeriodTask(tasks)):
            for period in period_list:
                #如果該Period的任務已經排完，則需要重新合併period
                if tasks[period].empty:
                    del tasks[period]
                    period_list.remove(period);
                    self.merge_split_period(periods,tasks)
                    local_date = DateTools.addDay(local_date, -1)
                    break
                capacity = periods[period]['Capacity']
                get_rows = period_tasks[period].iloc[0:capacity]
                get_rows['start'] = list(self.merge_date(local_date,i[0]) for i in periods[period]['times'])[:len(get_rows)]
                get_rows['end'] = list(self.merge_date(local_date,i[1]) for i in periods[period]['times'])[:len(get_rows)]
                result = result.append(get_rows, ignore_index=False)
                period_tasks[period].drop(get_rows.index, inplace=True)
            local_date = DateTools.addDay(local_date, 1)
        print(datetime.datetime.now())
        for row in result.itertuples():     
            setattr(tasks_array[row.Index], 'SchBDate', row.start)        
            setattr(tasks_array[row.Index], 'SchEDate', row.end)        
            

    def merge_split_period(self, cur_periods_dict, dest_periods, is_split_time=True):
        '''
        功能描述：合並period,並根據產能拆分時間
        '''
        cur_periods = list(cur_periods_dict.items())
        cur_periods.sort(key=lambda x: x[1].get('from_field'))
        ##只要有沒有合併的period，則繼續合並
        while(len([period[1].get('period') for period in cur_periods if not period[1].get('period') in dest_periods.keys()]) > 0):
            for i in range(len(cur_periods)):
                #判斷是否有下一個period,如果有將當前period合併到下一個,刪除當前這個
                if not cur_periods[i][1]['period'] in dest_periods.keys():
                    if i < len(cur_periods) - 1:
                        cur_periods[i+1][1]['from_field'] = cur_periods[i][1]['from_field']
                    else:
                        cur_periods[i-1][1]['to'] = cur_periods[i][1]['to']
                    del cur_periods_dict[cur_periods[i][1]['period']]
                    del cur_periods[i]
                    break;        
        if is_split_time:
            ##計算時間
            for period in cur_periods_dict.values():
                self.split_time(period)

    def is_allEmptyWithPeriodTask(self, period_tasks):
        for task in period_tasks.values():
            if not task.empty:
                return False;
        return True
    def merge_date(self, date_obj, time_obj):
        return datetime.datetime(date_obj.year,date_obj.month, date_obj.day, time_obj.hour, time_obj.minute, time_obj.second, tzinfo=pytz.UTC)

    def split_time(self, period):
        start = period['from_field']
        end = period['to']
        capacity = period['Capacity']
        start_date = datetime.datetime(self.noon_start.year,self.noon_start.month, self.noon_start.day, start.hour, start.minute, start.second)
        end_date = datetime.datetime(self.noon_start.year,self.noon_start.month, self.noon_start.day, end.hour, end.minute, end.second)
        interval =  (end_date - start_date).seconds
        if start_date < self.noon_start and end_date > self.noon_end:
            interval = interval - (self.noon_end - self.noon_start).seconds
        interval = Math.floor(interval/capacity)
        local_date = start_date
        times = []
        for i in range(capacity - 1):
            local_start = local_date
            local_date = (local_date + datetime.timedelta(seconds=interval))
            if local_date > self.noon_start:
                local_date = (local_date + datetime.timedelta(seconds=(self.noon_end - self.noon_start).seconds))
            times.append((local_start.time(), local_date.time()))
        if times:
            times.append((times[len(times) - 1][1], end))
        else:
            times.append((start, end))
        period['times'] = times

class FixedDateScheduleLogic(object):
    '''
    功能描述：處理Fixed Date類型的任務排期
    '''
    def __init__(self, quarterly=None,users:set=None,start_date=None, **kwargs):
        self.users = users
        self.source = {}
        self.quarterly = quarterly
        self.sch_source = None        
        self.sys_params = None #排期系統參數
        self.user_params = {} #排期用戶參數
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.init_data()

    def init_data(self):
        '''
        功能描述：初始化數據
        '''
        #獲取排期系統參數
        self.sys_param = ScheduleParam.read_sys_params()
        #獲取排期用戶參數
        for user in self.users:
            self.user_params[user] = ScheduleParam.read_user_params(user)
        #讀取用戶需要排期的Session及任務列表
        self.sch_source = ScheduleSource(self.quarterly, self.users)        
        self.sch_source.get_fixeddate_task()
    

class ScheduleInSessionLogic(object):
    '''
    功能描述：處理Session內排期的邏輯，
    1) 獲取Session內根據FLType(0：先進先出， 1：先進後出 None:先進先出), 計算Session優先級
    2) 獲取任務的TaskType優先級
    3) 獲取Session內根據TaskType優先級降序和Session FL優先級降序計算出的優先級
    '''
    def __init__(self, source:ScheduleSource=None, fixed_date_type=None,**kwargs):
        self.source = source
        self.fixed_date_type = fixed_date_type
        for key, value in kwargs.items():
            setattr(self, key, value)    
    
    def calculate_priority_insession(self):
        '''
        功能描述：計算任務在Session內的優先級,需要計算的內容有
        1) 任務根據Session FLType(先進先出或先進後出) 的順序, 以任務數量按10分隔給一個排序數
        2）根據任務的 Period, TaskType, Class, Priority計算任務的TaskType優先級
        3) 根據任務的TaskType優先級及Fl優先級，再次計算出該任務在Session內的排序數
        '''
        normal_objects, class_objects, priority_objects = self.get_task_type_formula()
        for key,value in self.source.items():
            tasks = value['tasks']
            #計算任務的TaskType Priority
            self.calculate_task_type_priority(normal_objects, class_objects, priority_objects, tasks)
            sessions = value['sessions']
            tasks_frame = pd.DataFrame(list(task.__dict__ for task in tasks), columns=['pid','tid','taskid','taskno','tasklistno','Period','TaskTypePriority'])
            tasks_frame['fl_priority'] = 0
            tasks_frame['sess_priority'] = 0
            print(datetime.datetime.now())
            #將任務列表以Session分組
            groups = tasks_frame.groupby(['tasklistno','Period'])
            fl_types = {a.sessionid:a.fltype for a in sessions}
            for key,group in groups:
                #將分組後的任務以Session的Fl Type，1:先進後出 （0或其他）：先進先出
                #先進先出 以TaskId升序排序， 先進後出 以TaskId降序排序
                session = key[0]
                group.sort_values(['taskid'], ascending=[fl_types[session] != 1], inplace=True)
                #根據順序給定fl_priority的數
                group['fl_priority'] = range(len(group) * 10, 0, -10)
                #分組後的任務以TaskTypePriority fl_priority降序排序
                group.sort_values(['TaskTypePriority', 'fl_priority'], ascending=[False, False], inplace=True)
                #根據順序給定sess_priority的數
                group['sess_priority'] = range(len(group) * 10, 0, -10)
                #將該組數據中的fl_priority及sess_priority更新到所有任務列表中
                tasks_frame.update(group.loc[:,['fl_priority', 'sess_priority']])
            #將pandas數據表中經過計算過的TaskTypePriority, fl_priority, sess_priority更新到任務列表的Model中
            for row in tasks_frame.itertuples():
                setattr(tasks[row.Index], 'TaskTypePriority', row.TaskTypePriority)
                setattr(tasks[row.Index], 'fl_priority', row.fl_priority)
                setattr(tasks[row.Index], 'sess_priority', row.sess_priority)

    def calculate_task_type_priority(self, normal_objects, class_objects, priority_objects, list):
        '''
        功能描述：計算任務分類的優先級
        '''
        print(datetime.datetime.now())
        for task in list:
            Period = task.Period
            TypeNo = task.TypeNo
            class_val = task.class_field
            priority = task.priority
            if TypeNo == self.fixed_date_type:
                setattr(task, 'Category', FIXED_DATE_CATEGORY)
                setattr(task, 'TaskTypePriority', 1)
                continue
            str_pro = '{0}_{1}'.format(Period, format(TypeNo,'.3f'))
            sch_priority = 0
            if not class_val and not priority:
                sch_priority = normal_objects.get(str_pro, 0)
            else:
                if class_val:
                    sch_priority += class_objects.get('{0}_{1}'.format(str_pro, format(class_val, '.3f')), 0)
                if priority:
                     sch_priority += priority_objects.get('{0}_{1}'.format(str_pro, format(priority, '.3f')), 0)
                if sch_priority == 0:
                    sch_priority = normal_objects.get(str_pro, 0)
            setattr(task, 'Category', 0)                    
            setattr(task, 'TaskTypePriority', sch_priority)
        print(datetime.datetime.now())

    def get_task_type_formula(self):
        '''
        功能描述：讀取任務分類的formula, 這個邏輯暫時未確定
        '''
        rs = models.Schformula.objects.values('period','typeno','class_field','priority','schpriority').all()
        data = list(rs)
        class_objects = {'{0}_{1}_{2}'.format(a['period'], format(a['typeno'],'.3f'), format(a['class_field'], '.3f')):a['schpriority'] for a in data if a['class_field']}
        priority_objects = {'{0}_{1}_{2}'.format(a['period'], format(a['typeno'],'.3f'), format(a['priority'], '.3f')):a['schpriority'] for a in data if a['priority']}
        normal_objects = {'{0}_{1}'.format(a['period'], format(a['typeno'],'.3f')):a['schpriority'] for a in data if not a['priority'] and not a['class_field']}
        return normal_objects, class_objects, priority_objects


def UpdateScheduleTask(contact, quarterly, tasks, is_override=True):
    '''
    功能描述：保存排期後的任務，包含排期歷史及更新任務信息
    '''
    print('保存開始')
    print(datetime.datetime.now())
    schmh_insert_list = list()
    schmh_update_list = list()
    update_task_list = list()
    old_schmh_list = models.Schmh.objects.values('quarterly','contact','pid','tid','taskid','inc_id').filter(contact=contact, quarterly=quarterly)
    old_id_dict = {"{0}-{1}-{2}-{3}-{4}".format(a['quarterly'].strip(), a['contact'].strip(), a['pid'].strip(), a['tid'], a['taskid']):a['inc_id'] for a in old_schmh_list}
    for task in tasks:
        data = {key.lower():value for key,value in task.__dict__.items() if key.lower() in [a.attname for a in models.Schmh._meta.get_fields()]}        
        data['contact'] = contact
        data['quarterly'] = quarterly
        data['tasktypeno'] = task.TypeNo
        data['flpriority'] = task.fl_priority
        data['sesspriority'] = task.sess_priority
        data['category'] = task.Category

        schmh = models.Schmh(**data)
        inc_id = old_id_dict.get("{0}-{1}-{2}-{3}-{4}".format(schmh.quarterly.strip(), schmh.contact.strip(), schmh.pid.strip(), schmh.tid, schmh.taskid))
        if inc_id:
            schmh.inc_id = inc_id
            schmh_update_list.append(schmh)
        else:
            schmh_insert_list.append(schmh)

        update_task = models.Task()
        update_task.pid = task.pid
        update_task.tid = task.tid
        update_task.taskid = task.taskid
        update_task.schpriority = task.SchPriority
        update_task.inc_id = task.inc_id
        if task.Category != FIXED_DATE_CATEGORY:
            update_task.planbdate = task.SchBDate
            update_task.planedate = task.SchEDate
        else:
            update_task.planbdate = task.planbdate
            update_task.planedate = task.planedate
        update_task_list.append(update_task)    
    print(datetime.datetime.now())
    with transaction.atomic(using='MPMS'):
        models.Schmh.objects.bulk_create(schmh_insert_list, batch_size=50)
        update_fields = [a.attname for a in models.Schmh._meta.get_fields() if a.attname not in models.Schmh._meta.unique_together[0] and a.attname != models.Schmh._meta.pk.name]
        ##for schmh in schmh_update_list:
            ##schmh.save(update_fields=update_fields)
        models.Schmh.objects.bulk_update(schmh_update_list, fields=update_fields, batch_size=50)
        print(datetime.datetime.now())
        models.Task.objects.bulk_update(update_task_list, fields=['schpriority','planbdate','planedate'], batch_size=100)
    print(datetime.datetime.now())
    print('保存結果')