from DataBase_MPMS import models
from . import QueryFilterService
import json

class MindmapService:
    def generateMindmap(self,queryFilterId, queryFilterKey, conditon):
        """
        功能描述：
        """
        data,rootdesc = self.search_data(queryFilterId, queryFilterKey, conditon)
        tree = self.convertToTree(data)
        mindmap_json = self.generateMindmapWithTree(rootdesc, tree)
        print(mindmap_json)
        return json.dumps(mindmap_json)


    def search_data(self, queryFilterId, queryFilterKey, conditon):
        if queryFilterId:
            str_filter,top = QueryFilterService.get_query_filter_advanced(queryFilterId)
        elif queryFilterKey:
            rs = models.Queryfilter.objects.values('qf025').filter(qf001=queryFilterKey['qf001'], qf002=queryFilterKey['qf002'], \
             qf006=queryFilterKey['qf006'], qf009=queryFilterKey['qf009'], qf010 = queryFilterKey['qf010'])
            if len(rs) > 0:
                queryFilterId = rs[0]['qf025']
                str_filter,top = QueryFilterService.get_query_filter_advanced(queryFilterId)
            else:
                raise Exception("不存在該查詢條件{0}-{1}-{2}-{3}-{4}".format(queryFilterKey['qf001'],queryFilterKey['qf002'],queryFilterKey['qf006'],queryFilterKey['qf009'],queryFilterKey['qf010']))
        else:
            str_filter = '1<>1'            
            top = None
        
        if queryFilterId:
            rs = models.Queryfilter.objects.values('qf003').get(qf025=queryFilterId)
            rootdesc = rs['qf003']
        else:
            rootdesc = "Task Enquiry"

        strSQL = """
            Select NULL INC_ID,B.RecordId recordid,B.ProjectName projectname, M.* from 
             (Select distinct * from (select {0}
                Pid,Tid,TidDesc tiddesc,Weight from V_Task A where ({1}) {2}) T) M
            OUTER APPLY (
                Select TOP 1 RecordId,ProjectName,Score from SubProject where ProjectId like M.Pid and dbo.ValidateTid(M.Tid,Filter) = 1
            ) B
            order by B.Score Desc, ISNULL(M.Weight,999999)
            """
        if top:
            strSQL = strSQL.format("top {0}".format(top), str_filter, " order by SchPriority Desc")
        else:
            strSQL = strSQL.format("", str_filter, "")
        rs = models.VTask.objects.raw(strSQL)
        return list(rs), rootdesc
    def convertToTree(self, data):
        tree = {}
        for row in data:
            recordid = row.recordid
            if recordid in tree:
                tree[recordid]['children'].append({'desc':"({0}-{1}) {2}".format(row.pid, row.tid, row.tiddesc)})
            else:
                tree[recordid] = {'desc':"({0}) {1}".format(recordid, row.projectname), 'children':[{'desc':"({0}-{1}) {2}".format(row.pid, int(row.tid), row.tiddesc)}]}
        return tree;
    
    def generateMindmapWithTree(self,rootdesc, data):
        mindmap_json = {"class": "TreeModel", "nodeDataArray": []}
        ##添加根節點
        key = 0
        root = {"text":rootdesc,"brush":"#adc2ff","color":"#adc2ff","key":key,"loc":"0 0", "url":""}
        mindmap_json['nodeDataArray'].append(root)
        for recordid,project in data.items():
            key = key - 1
            project_json_obj = {"text":project['desc'],"brush":"#adc2ff","color":"#adc2ff","parent":root['key'],"key":key,"loc":"0,0", "url":""}
            mindmap_json['nodeDataArray'].append(project_json_obj)
            for session in project['children']:
                key = key - 1
                session_json_obj = {"text":session['desc'],"brush":"#adc2ff","color":"#adc2ff","parent":project_json_obj['key'],"key":key,"loc":"0,0", "url":""}
                mindmap_json['nodeDataArray'].append(session_json_obj)
        return mindmap_json
