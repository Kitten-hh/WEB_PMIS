aiResultStr = """Month 1: October 2023

Week 1: October 1st - October 7th

(00390-1000-10) Task: 車間人員信息的增刪改
Schedule Date: October 3rd
(00390-1000-20) Task: 查詢車間人員信息
Schedule Date: October 5th
Week 2: October 8th - October 14th

(00390-1000-30) Task: 設置崗位和計件性質參數
Schedule Date: October 11th
(00390-1000-40) Task: 審核車間人員信息
Schedule Date: October 13th
Week 3: October 15th - October 21st

(00390-1000-50) Task: 車間設備信息列表
Schedule Date: October 17th
(00390-1000-60) Task: 車間設備明細編輯
Schedule Date: October 19th
Week 4: October 22nd - October 28th

(00390-1000-70) Task: 錄入車間設備類型
Schedule Date: October 24th
(00390-1000-80) Task: 審核車間設備信息
Schedule Date: October 26th
Month 2: November 2023

Week 1: November 1st - November 7th

(00390-1000-90) Task: 反審核車間設備信息
Schedule Date: November 2nd
(00390-1000-100) Task: 車間模夾具信息列表
Schedule Date: November 4th
Week 2: November 8th - November 14th

(00390-1000-110) Task: 編輯車間模夾具信息
Schedule Date: November 9th
(00390-1000-120) Task: 審核車間模夾具信息
Schedule Date: November 11th
"""

        """
        regex = "Month\\s+\d+:\\s*(.*?)(\d+)"
        iter = re.finditer(regex, resultStr, re.IGNORECASE)
        monthMap = {}
        for match in iter:
            monthMap[match.group(1)] = match.group(2)
        regex = "\\((\d+-\d+\d+\\)\\s*Task:(.*?)Schedule\\s+Date:\\s*(.*?)(\d+)(rd|td)"
        iter = re.finditer(regex, resultStr, re.IGNORECASE)"""
        '''taskIter = resulStr.split("\n")
        tasks = []
        maxTaskId = 0
        for match in taskIter:        
            taskNo = match.group(1)
            task = match.group(2)
            month = match.group(3)
            day = match.group(4)
            if month in monthMap:
                year = monthMap[month]
                taskDate = DateTools.parsef("{0}-{1}-{2}".format(year, month, day), "%Y%B%d")
                task = Task()
                task.pid = session.pid
                task.tid = session.tid
                if maxTaskId == 0:
                    maxTaskId = TaskService.get_max_taskid(task.pid, task.tid)
                else:
                    maxTaskId += 10
                task.taskid = maxTaskId
                task.task = task
                task.contact = request.user.username
                task.progress = 'N'
                task.planbdate = taskDate
                task.planedate = taskDate
                task.requestdate = taskDate
                ModelTools.set_basic_field_info(request, task, instance)
                tasks.append(task)'''