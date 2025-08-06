from django.conf import settings
from BaseApp.library.tools import AsyncioTools
import json
from DataBase_MPMS import models

class ElasticService(object):
    def __init__(self):
        self.serverName = settings.ELASTICSERVERS_SERVERNAME #Elasticsearch的服務器地址
        self.index_pmstechinc=settings.ELASTICSERVERS_ELASTICINDEXNAME #Elasticsearch pms techinc的index名
        self.index_pmsdoc=settings.ELASTICSERVERS_ELASTICDOCINDEXNAME #Elasticsearch pms doc的index名

    def fullTextSearchDoc(self, searchValue:str, size=100):
        """
        功能描述：對技術文檔進行全文搜索
        """
        jsonObj = {"query":{"query_string":{"query":"","default_operator": "and","analyzer": "ik","fuzziness": "AUTO"}},"_source":["IndexId","TechNo","MindId","Questions","Topic","Usage","PMindId","Category","Contact","date","Area"],"size":size}
        if searchValue:
            jsonObj['query']['query_string']['query'] = searchValue
        url = "{0}/{1}/_search".format(self.serverName, self.index_pmstechinc)
        response = AsyncioTools.async_fetch_http_json({"data":{"url":url,"method":"POST","params":jsonObj}})
        return response['data']
    

    def UpdateElastic(self,instance):
        Stepsdata = models.Tecmc.objects.filter(id=instance.id,mc003='1').values()
        Exampledata = models.Tecmc.objects.filter(id=instance.id,mc003='2').values()
        Precautiondata = models.Tecmc.objects.filter(id=instance.id,mc003='3').values()

        DocJson = {}
        DocJson['IndexId'] = self.HandleSpecialStr(instance.id)
        DocJson['TechNo'] = self.HandleSpecialStr(instance.mb023)
        DocJson['Contact'] = self.HandleSpecialStr(instance.mb005)
        DocJson['date'] = self.HandleSpecialStr(instance.mb006)
        DocJson['MindId'] = self.HandleSpecialStr(instance.id)
        DocJson['PMindId'] = self.HandleSpecialStr(instance.parentid)
        DocJson['Category'] = self.HandleSpecialStr(instance.mb015c)
        DocJson['Questions'] = self.HandleSpecialStr(instance.mb013)
        DocJson['Topic'] = self.HandleSpecialStr(instance.mb004)
        DocJson['Usage'] = self.HandleSpecialStr(instance.mb008)
        DocJson['Concept'] = self.HandleSpecialStr(instance.mb007)
        DocJson['Control'] = self.HandleSpecialStr(instance.mb025)
        DocJson['Dependancy'] = self.HandleSpecialStr(instance.mb009)


        DocJson['Steps'] = self.getOtherData(Stepsdata)
        DocJson['Example'] = self.getOtherData(Exampledata)
        DocJson['Precaution'] = self.getOtherData(Precautiondata)
        
        
        DocJson['Html'] = self.HandleSpecialStr(instance.mb022)
        DocJson['Area'] = self.HandleSpecialStr(instance.mb016)
        DocJson['Reference'] = self.HandleSpecialStr(instance.mb017)
        DocJson['Compulsory'] = self.HandleSpecialStr(instance.mb019)
        DocJson['Status'] = self.HandleSpecialStr(instance.mb020)
        id = instance.id
        AResource = "{}/_doc/{}".format(self.index_pmstechinc,id)
        url = "{0}/{1}".format(self.serverName, AResource)
        try:
            response = None
            response = AsyncioTools.async_fetch_http_json({"data":{"url":url,"method":"POST","params":DocJson}})
        except Exception as e:
            try:
                response = AsyncioTools.async_fetch_http_json({"data":{"url":url,"method":"POST","params":DocJson}})
            except Exception as e:
                self.UpdateFlag(False,instance)
                print(str(e)) 
        self.UpdateFlag(True,instance)


    def HandleSpecialStr(self,strValue):
        return str(strValue).replace('#9','    ')
                                 
    def getOtherData(self,other_data):
        result = ''
        for item in other_data:
            result = "{}{}\n".format(result,self.HandleSpecialStr(item['mc005']))
        return result
    
    def UpdateFlag(self,Flag,instance):
        strudf01 = 'Y' if Flag else 'N'
        instance.udf01 = strudf01
        instance.save()