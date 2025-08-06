from enum import Enum
PMS_TASK_SCHEDULE_FLAG = "TaskSchedule"
PMS_SCHEDULE_PARAMS = "ScheduleParams"
PMS_SCHEDULE_CATEGORY_PARAMS = "ScheduleCategoryParams"
PMS_AUTO_SCHEDULE_FLAG = "AutoSchedule"
SCHEDULE_WEEK_ARE_SCHEDULED = "Week are Scheduled"
SCHEDULE_RAISED_BY_SING = "Raised by Sing"
SCHEDULE_RAISED_BY_ROBERT = "Raised by Robert"
SCHEDULE_PROJECT_PRIORITY_BASE = "Project Priority Base"
SCHEDULE_PRIORITY_8889 = "Priority(8889)"
SCHEDULE_PRIORITY_8888 = "Priority(8888)"
SCHEDULE_PRIORITY_888 = "Priority(888)"
SCHEDULE_NORMAL_TASKR_ANGEF_ILTER = "NormalTaskRangeFilter"
SCHEDULE_MEETING_P = "Meeting P"
SCHEDULE_FIXED_DAY = "Fixed Day"
SCHEDULE_EXTERNAL_REQUEST = "External Request"
SCHEDULE_DAY_CAPACITY = "Day Capacity"
SCHEDULE_CLASS_1 = "Class(1)"
SCHEDULE_INTERVAL_FOR_SORT_VALUE = "Interval for Sort Value"
SCHEDULE_SESSION = "Session"
SCHEDULE_RAISED_BY_SING_CAPACITY = "Raised by Sing Capacity"
SCHEDULE_RAISED_BY_ROBERT_CAPACITY = "Raised by Robert Capacity"
SCHEDULE_MEETING_P_CAPACITY = "Meeting P Capacity"
SCHEDULE_FIXED_DAY_CAPACITY = "Fixed Day Capacity"
SCHEDULE_EXTERNAL_REQUEST_CAPACITY = "External Request Capacity"
SCHEDULE_MUTIL_PROJECT_QTY="Mutil Project Qty"
SCHEDULE_SCENARIO="Scenario"


##
SESSION_SCHEDULE_WEEKLYDAY = "SessionWeeklyDay"
SESSION_SCHEDULE_MAXWEEKLY = "MaxWeekly"
SESSION_BASE_CAPACITY = "BaseCapacity"
SESSION_GENARAL_Goal_FLAG = "GenaralGoalFlag"
SESSION_UPDATE_DATA_USER = "UpdateDataUser"
SESSION_MIN_CLEAR_PREV_WEEKLY = "MinClearPrevWeekly"
SESSION_COMPULSORY_PROJECT = "CompulsoryProject"
SESSION_CRITICAL_PROJECT = "CriticalProject"
SESSION_DAY_JOB = "DayJob"
SESSION_NEW_TASK_MAX_DAY = "NewTaskDay"
SESSION_NEW_TASK_MAX_WEEKLY = "NewTaskWeekly"
SESSION_MAX_SCH_PRIORITY = "MaxSchPriority"
SESSION_INTERVAL_SCH_PRIORITY = "IntervalSchPriority"
SESSION_INTERVAL_MONTH_SCH_PRIORITY = "IntervalMonthSchPriority"
SESSION_SCHEDULE_TYPE = "ScheduleType"
SESSION_MULTI_USER_WITH_SESSION = "MultiUserWithSession"
SESSION_DAY_CAPACITY = "DayCapacity"
SESSION_RPC = "RPC"
SCHEDULED_TASK_RANGE_FILTER = "ScheduledTaskRangeFilter"
SCHEDULE_DATE_FIELD = "ScheduleField"
SCHEDULE_CAL_PRIORITY_FIELD = "CalPriorityField"
SCHEDULE_DEFAULT_DAY_JOB = "DefaultDayJob"
SCHEDULE_DAY_JOB = "DayJob_"
SCHEDULE_OUT_DAY = "out_day"
SCHEDULE_EXTERNAL_WEEKLY = "ExternalWeekly"
SCHEDULE_DEV_WEEKLY = "DevWeekly"
SCHEDULE_NEWTASK_WEELY_LATELY = "NewTaskWeelyLately"
SCHEDULE_NEWWEEKLY_MAXDAY = "NewWeeklyMaxDay"
SCHEDULE_MULTI_USER_WITH_COMPULSORY_SESSION = "MultiUserCompsy"  # 單獨Session支持多人
PROJECT_SCHEDULE_FIELD = "RecordID"
SCHEDULE_PROJECT_PRIORITY_BASE = "Project Priority Base"


class ScheduleType(Enum):  #排期類型
    All   = 0
    One   = 1  #Scenario - One Project One Session
    Two   = 2  #Scenario - One Project Two Sessions
    Three = 3  #Scenario - Mutil Project One Session
    Four  = 4  #Scenario - Mutil Project Two Sessions
    

class ActionType(Enum):  #Action類型
    getSubProject = 1 #獲取子工程信息
    getSession    = 2 #獲取Session信息
    getTasks      = 3 #根據Session獲取Task信息
    getRule       = 4 #獲取排期規則信息
    arrageTask    = 5 #對任務進行排序
    getExistsSchPriority = 6 #獲取已經存在的排期優先級
    getExistTodayCapacity = 7 #獲取當前已經排期的任務數量
    getScheduleCategory = 8 #獲取排期的類型
    updateRecordId = 9 #登記任務的RecordId
    getSingleSessionFilter = 10 #獲取用戶Single Session的查詢條件

class AsyncFuncName(Enum):
    initScheduleParams= "initScheduleParams"
    scheduleData = "scheduleData"
    calCategoryTasksPriority = "calCategoryTasksPriority"

class ScheduleCategoryEnum(Enum):
    RaisedBySing = "Raised by Sing"
    RaisedByRobert = "Raised by Robert"
    MeetingP = "Meeting P"
    FixedDay = "Fixed Day"
    ExternalRequest = "External Request"