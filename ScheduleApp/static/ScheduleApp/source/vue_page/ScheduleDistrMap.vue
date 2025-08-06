<script>
import axios from "axios";
import ScheduleDistrMap_vueFrm_UI from './ScheduleDistrMap_UI.vue'
export default {
    name:"ScheduleDistrMap_vueFrm",
    extends:ScheduleDistrMap_vueFrm_UI,
    data() {
        return {
            tasks:[{"RecordId":"00359","ProjectName":"WebSo","Task":"跟進Web PO上線後的情況","PlanBDate":"2023-09-05T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"添加模擬計畫日期，排期計畫到該日期，先給數據流程圖和表結構給陳生","PlanBDate":"2023-09-06T00:00:00"},{"RecordId":"00188","ProjectName":"*Knowledge based project","Task":"這個季度要將技術文檔的Category\/Area\/SubArea和描述改的準確（精準），如果需要添加英文描述，要找陳生確認（為了可以在查詢中更好的查詢）","PlanBDate":"2023-09-07T00:00:00"},{"RecordId":"00188","ProjectName":"*Knowledge based project","Task":"將我們認為標準的文檔使用ChartGPT將主題轉為英文後添加到技術文檔的主題中","PlanBDate":"2023-09-08T00:00:00"},{"RecordId":"00286","ProjectName":"CRM - 220V","Task":"跟進GISP Stock的Outstanding Transer Requests from China的邏輯","PlanBDate":"2023-09-09T00:00:00"},{"RecordId":"00188","ProjectName":"*Knowledge based project","Task":"將Rect放在Repository並將步驟清楚的給陳生","PlanBDate":"2023-09-11T00:00:00"},{"RecordId":"00188","ProjectName":"*Knowledge based project","Task":"將Django的基礎技術文檔(顯示數據， CRUD)寫出來給陳生確認","PlanBDate":"2023-09-12T00:00:00"},{"RecordId":"00188","ProjectName":"*Knowledge based project","Task":"陳生的文檔對應我們的文檔，如果沒有的就檢查陳生的文檔能不能用，再跟陳生確認就將文檔確認下來","PlanBDate":"2023-09-13T00:00:00"},{"RecordId":"00188","ProjectName":"*Knowledge based project","Task":"到w3schools網站看React","PlanBDate":"2023-09-14T00:00:00"},{"RecordId":"00371","ProjectName":"CRM Backend","Task":"給出Backend中產品與Catalog對接的設計方案","PlanBDate":"2023-09-15T00:00:00"},{"RecordId":"00235","ProjectName":"00235 Cloud","Task":"查找OutSource服務器222.118.20.236重啟的原因，並解決自動重啟問題。","PlanBDate":"2023-09-15T00:00:00"},{"RecordId":"00327","ProjectName":"ERP - Android","Task":"無線移料添加庫存交易單","PlanBDate":"2023-09-16T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"WebSo添加權限管理","PlanBDate":"2023-09-18T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"Operation FlowChart使用Mindmap顯示","PlanBDate":"2023-09-19T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"跟進lsy談如何可以搜索网络组的文档","PlanBDate":"2023-09-19T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"將course中的Task Filter去掉，可以選擇任務批量關聯Course","PlanBDate":"2023-09-20T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"Weekly考慮可以跨周顯示準確","PlanBDate":"2023-09-21T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"Mindmap可以跳轉到Top Project對應的Session","PlanBDate":"2023-09-22T00:00:00"},{"RecordId":"00327","ProjectName":"ERP - Android","Task":"檢查無線移料移料品檢介面，從移料單同步數據是否有問題","PlanBDate":"2023-09-23T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"在Dashboard和Project的中間打開Goal頁面","PlanBDate":"2023-09-25T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"Meeting實現多人編輯要開始做","PlanBDate":"2023-09-26T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"Meeting同步編輯的任務要開始做","PlanBDate":"2023-09-27T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"將Project Manager頁面的Rule Doc準備好了找陳生確認Project優先級","PlanBDate":"2023-09-28T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"將陳生加的任務以手機提醒的方式提醒用戶","PlanBDate":"2023-09-29T00:00:00"},{"RecordId":"00371","ProjectName":"CRM Backend","Task":"(UR - CRM Backend Test)完成所有模塊測試","PlanBDate":"2023-09-30T00:00:00"},{"RecordId":"00329","ProjectName":"Generic Orderwise","Task":"走貨的過程怎麼用Barcode","PlanBDate":"2023-09-30T00:00:00"},{"RecordId":"00329","ProjectName":"Generic Orderwise","Task":"將orderwise系統的數據轉為mysql，將表結構給陳生","PlanBDate":"2023-09-30T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"Task Enquiry UI跟桌面版先","PlanBDate":"2023-10-02T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"Project中Mindmap可以跳轉到對應Project Mindmap","PlanBDate":"2023-10-03T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"Project可以看到Top Project及Meething中討論的內容","PlanBDate":"2023-10-04T00:00:00"},{"RecordId":"00329","ProjectName":"Generic Orderwise","Task":"Flex做過Custom Service, 走貨的流程明天找陳生談","PlanBDate":"2023-10-05T00:00:00"},{"RecordId":"00510","ProjectName":"SZ Orderwise","Task":"跟qfq確定毛巍的倉庫如何實現，更改到流程圖,並跟陳生確認","PlanBDate":"2023-10-06T00:00:00"},{"RecordId":"00510","ProjectName":"SZ Orderwise","Task":"支持從外廠到OC到SZ庫多套單據","PlanBDate":"2023-10-09T00:00:00"},{"RecordId":"00359","ProjectName":"WebSo","Task":"将Vender_RestAPi放到雲門","PlanBDate":"2023-10-10T00:00:00"},{"RecordId":"00033","ProjectName":"* PMS","Task":"top project階段性的, Activity workflow準備好後 找陳生","PlanBDate":"2023-10-11T00:00:00"},{"RecordId":"00360","ProjectName":"Production Course","Task":"下周給出Python 導出Excel技術文檔","PlanBDate":"2023-10-12T00:00:00"},{"RecordId":"00360","ProjectName":"Production Course","Task":"將Django開發中的UI和業務邏輯分開","PlanBDate":"2023-10-13T00:00:00"},{"RecordId":"00182","ProjectName":"00182 MOC","Task":"外掛介面《車間生產進度》介面增加小介面，可以顯示下層工單的工藝WJ等。（之前有寫上報要委外SC工藝進度一起做）。","PlanBDate":"2023-10-14T00:00:00"},{"RecordId":"00183","ProjectName":"MIS Management（Monday）","Task":"跟進整理czz的任務的goal","PlanBDate":"2023-10-16T00:00:00"},{"RecordId":"00179","ProjectName":"00179 PMS Desktop","Task":"处理FAQ用不到的问题，使用陈生的电脑测试一下","PlanBDate":"2023-10-17T00:00:00"},{"RecordId":"00255","ProjectName":"VC220 Web Site","Task":"補VC220 Web Site的用例圖，活動國","PlanBDate":"2023-10-18T00:00:00"},{"RecordId":"00357","ProjectName":"Flutter Application","Task":"處理Notification使用FCM通道收不到消息的問題","PlanBDate":"2023-10-19T00:00:00"},{"RecordId":"00357","ProjectName":"Flutter Application","Task":"檢查一下Notification是否發送","PlanBDate":"2023-10-20T00:00:00"},{"RecordId":"00182","ProjectName":"00182 MOC","Task":"找出上報《車間反饋生產任務單查詢界面預覽後打印的匯總產品標識卡有漏顯示問題》的原因","PlanBDate":"2023-10-21T00:00:00"},{"RecordId":"00259","ProjectName":"00259 MES","Task":"整理好WJ MES工程跟陳生談","PlanBDate":"2023-10-23T00:00:00"},{"RecordId":"00373","ProjectName":"ERP 韶關玖方系統","Task":"整理新玖方系統的Goal Project和任務","PlanBDate":"2023-10-24T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"Mindmap delete按鈕添加確認才可以","PlanBDate":"2023-10-24T00:00:00"},{"RecordId":"00379","ProjectName":"橋頭燈罩Web ERP System","Task":"在橋頭燈罩廠只能限制某些用戶登陸，就算我們的人過去，也不能使用他們的用戶登陸系統","PlanBDate":"2023-10-25T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"Mind Map中添加Session放到彈出框裏實現","PlanBDate":"2023-10-26T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"Project添加Priority字段為優先級","PlanBDate":"2023-10-27T00:00:00"},{"RecordId":"00182","ProjectName":"00182 MOC","Task":"工單批量變更單（採購件）模塊除替換材料作用外，增加一個批量更改工單需領數量的功能。\r\n","PlanBDate":"2023-10-28T00:00:00"},{"RecordId":"00510","ProjectName":"SZ Orderwise","Task":"SZ向OC請求時可以通過Excel導入","PlanBDate":"2023-10-30T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"可以修改Priroity","PlanBDate":"2023-10-31T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"Project中選Session時可以顯示對應的Meeting","PlanBDate":"2023-11-01T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"Goal如何去關聯Project","PlanBDate":"2023-11-02T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"添加一個Project Flow up in WEBPMIS的頁面","PlanBDate":"2023-11-03T00:00:00"},{"RecordId":"00182","ProjectName":"00182 MOC","Task":"按黃經理要求，在<工單挪料管理>介面增加批量挪料程序，可以一個未完工工單所有材料一次挪入另一個工單。","PlanBDate":"2023-11-04T00:00:00"},{"RecordId":"00179","ProjectName":"00179 PMS Desktop","Task":"PMIS Color Code標準化","PlanBDate":"2023-11-06T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"將循環任務中Fixed Day的任務排期到前面","PlanBDate":"2023-11-06T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"將循環任務中Fixed Day的任務排期到前面","PlanBDate":"2023-11-07T00:00:00"},{"RecordId":"00188","ProjectName":"*Knowledge based project","Task":"哪些是重點的Construct，這個月做出來","PlanBDate":"2023-11-08T00:00:00"},{"RecordId":"00028","ProjectName":"00028 ERP","Task":"現在的ERP數據接近150G，hb需要做拆分。統計出每個表有多少模塊，每個表有多大。","PlanBDate":"2023-11-09T00:00:00"},{"RecordId":"00183","ProjectName":"MIS Management（Monday）","Task":"開一個新的工程管控網站日誌","PlanBDate":"2023-11-10T00:00:00"},{"RecordId":"00182","ProjectName":"00182 MOC","Task":"云門車間反饋YM5120\/5122不能挑選出來做磨光材料領用計劃單據，請核查原因，謝謝！","PlanBDate":"2023-11-11T00:00:00"},{"RecordId":"00211","ProjectName":"*公司網絡(Wednesday)","Task":"將Django網站使用Delphi打印報表服務發布到104服務器","PlanBDate":"2023-11-13T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"dashboard中項目的分配，完成不會理，需要調整","PlanBDate":"2023-11-14T00:00:00"},{"RecordId":"00331","ProjectName":"Web PIMS","Task":"Goal Management有一個報表發給陳生，上周有哪些Outstanding","PlanBDate":"2023-11-15T00:00:00"}],
            groupTasks:{},
            projectInfo:{},
            
        }
    },
    mounted() {
        this.loadTask()
    },
    methods: {
        handleTask() {
            this.groupTasks = this.tasks.reduce(function(map, obj) {
                if (obj.RecordId in map)
                    map[obj.RecordId].push(obj);
                else
                    map[obj.RecordId] = [obj];
                    return map;
                }, {});
            this.projectInfo = this.tasks.reduce(function(map, obj) {
                map[obj.RecordId] = obj.ProjectName;
                    return map;
                }, {});
        },
        loadTask() {
            this.handleTask();
            var diagramJson = { "class": "go.GraphLinksModel","nodeDataArray": [], "linkDataArray": []};
            var count = 0;
            for(var [recordId, projectName] of Object.entries(this.projectInfo)) {
                if (count == 0)
                    diagramJson.nodeDataArray.push({"key":recordId, "text":projectName, "isGroup":true, "loc":"0 0"})
                else 
                    diagramJson.nodeDataArray.push({"key":recordId, "text":projectName, "isGroup":true, "color":"0", "loc":"0 0"})
                count++;
            }
            var key = 1;            
            for(var [recordId, tasks] of Object.entries(this.groupTasks)) {
                for (var task of tasks) {
                    diagramJson.nodeDataArray.push({"key":key, "text":task.Task, "group":recordId, "loc":"0 0"});
                    key++;
                }
            }
            this.$refs.DistrMap.load(diagramJson);
        }
    }
}
</script>
