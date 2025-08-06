from DataBase_MPMS.models import Subproject,Project
from BaseApp.library.tools import DateTools
import math
import re
from django.forms.models import model_to_dict

class SubprojectService:
    def create_project(self,pid, name):
        projectFilter = self.getProjectFilter(pid)
        recordid = self.get_max_recordid()
        subProject = Subproject(
            projectid=pid, 
            projectname=name, 
            recordid=recordid, 
            contact="sing",
            method="B",
            filter=projectFilter,
            planbdate=DateTools.getBeginOfQuarter(DateTools.now()),
            planedate=DateTools.getEndOfQuarter(DateTools.now()))
        subProject.save()
        return model_to_dict(subProject)
        

    def get_max_recordid(self):
        qs = Subproject.objects.values('recordid').extra(where=["ISNUMERIC(RecordID) > 0"]).order_by("-recordid")[:1]
        record_id = '10'
        if len(qs) > 0:
            # 将字符串转换为整数，加1，然后转换回字符串
            record_id = str(int(qs[0]['recordid']) + 1)

        # 根据长度在前面补零
        if len(record_id) == 4:
            new_record_id = '0' + record_id
        elif len(record_id) == 3:
            new_record_id = '00' + record_id
        elif len(record_id) == 2:
            new_record_id = '000' + record_id
        elif len(record_id) == 1:
            new_record_id = '0000' + record_id
        else:
            new_record_id = record_id        
        return new_record_id

    def getProjectFilter(self, pid):
        """
        功能描述：獲取該Project所有SubProject信息，從中獲取最大的Tid
        """
        max_tid = 0
        qs = Subproject.objects.values('filter').filter(projectid=pid)
        if len(qs) > 0:
            for project  in qs:
                temp_tid = self.get_max_tid(project['filter']) # 假设 sp 有一个 filter 属性
                if max_tid < temp_tid:
                    max_tid = temp_tid
        if max_tid == 0:
            return "Tid > 0 and Tid <= 999"
        else:
            if max_tid % 1000 == 0:
                cur_min_tid = max_tid
                cur_max_tid = cur_min_tid + 1000
            else:
                cur_min_tid = math.floor(max_tid/1000)*1000 + 1000
                cur_max_tid = cur_min_tid + 1000 - 1
            return f"Tid > {cur_min_tid} and Tid <= {cur_max_tid}"

    def get_max_tid(self, filter_str):
        tid = 0
        pattern = re.compile("[0-9]+")
        matcher = pattern.findall(filter_str)
        for match in matcher:
            if tid < int(match):
                tid = int(match)
        return tid


