<script>
import axios from "axios";
import ShcedulePriority_vueFrm_UI from './SchedulePriority_UI.vue'
export default {
    name:"SchedulePriority_vueFrm",
    extends:ShcedulePriority_vueFrm_UI,
    data() {
        
    },
    mounted() {
        this.disableMasterSelectWithCondition();

    },
    created() {
        this.initScheduleParams();
        this.fetchSchParamsHistoryList(); // 獲取歴史記錄列錶
    },
    methods:{
        initScheduleParams() {
            for (var [group, params] of Object.entries(this.scheduleParams).concat(Object.entries(this.scheduleParamsOther))) {
                for (var param of params) {
                    param.fvalue = "";
                }
            }
            axios.get("/schedule/get_schedule_prarms").then((response)=>{
                var result = response.data;
                if (result.status) {
                    var params = result.data;
                    var paramsMap = new Map(
                        params.map(item => {
                            return [item.nfield, item];
                        }),
                    );
                    for (var [group, params] of Object.entries(this.scheduleParams).concat(Object.entries(this.scheduleParamsOther))) {
                        for (var param of params) {
                            if (paramsMap.has(param.nfield))
                                param.fvalue = paramsMap.get(param.nfield).fvalue
                        }
                    }
                    if (paramsMap.has("Scenario")) {
                        var scenarioParams = paramsMap.get("Scenario");
                        var scenarioArr = this.scenarioList.filter(x=>x.schType == parseInt(scenarioParams.fvalue));
                        if (scenarioArr.length > 0) {
                            this.scheduleParamsScenario = scenarioArr[0].label;
                        }
                    }
                }else {
                    alert(gettext("Get schedule parameter fail"));
                }
            })
        },
        saveScheduleParams() {
            var updateData = []
            for (var [group, params] of Object.entries(this.scheduleParams).concat(Object.entries(this.scheduleParamsOther))) {
                updateData.push(...params);
                for (var param of params) {
                    if (param["fvalue"] === "") {
                        alert(gettext(param.nfield) + gettext(" cannot be empty!"))
                        return;
                    }
                    if (param['nfield'] == "Day Capacity" && param["fvalue"] <= 0) {
                        alert(gettext("Day capacity must be greater than 0!"))
                        return;
                    }
                }
            }
            axios.post("/schedule/update_schedule_prarms", this.objectToFormData({updateData:JSON.stringify(updateData)})).then((response)=>{
                var result = response.data;
                if (result.status) {
                    alert(gettext("Save Success!"));
                }else {
                    alert(gettext("Save fail!"))
                }
            })
        },
        disableMasterSelectWithCondition() {
            var self =  this;
            this.$nextTick(function(){
                this.$refs.masterTable.datatable.on( 'user-select', function ( e, dt, type, cell, originalEvent ) {
                    if (self.getDetailChanged().length > 0) {
                        if (!confirm(gettext("Detail has modified and not saved")))
                            e.preventDefault();
                    }else {
                        var dt_rowid = $(originalEvent.target).closest("tr").attr("id");
                        if (originalEvent.target.nodeName.toLowerCase() == 'input' && $("#"+dt_rowid).hasClass("selected"))
                            e.preventDefault();
                    }
                });
            })
        },
        batchUpdatePriority() {
            var master = this.getMasterChanged();          
            var detail = this.getDetailChanged();
            if (master.priority.length == 0 && master.upriority.length == 0 && detail.weight.length == 0 && detail.uweight.length == 0) {
                alert(gettext("not priority changed!"))
            }else if(this.saveCheck(master, detail)) {
                axios.post("/schedule/batch_update_priority",this.objectToFormData({projects:JSON.stringify(master), sessions:JSON.stringify(detail)}))
                .then((response)=>{
                    var result = response.data;
                    if (result.status) {
                        alert(gettext("save success!"))
                        if (master.priority.length > 0 || master.upriority.length > 0) {
                            this.refreshDataTable(this.$refs.masterTable)
                        }else if (detail.weight.length > 0 || detail.uweight.length > 0)
                            this.refreshDataTable(this.$refs.detailTable)
                        //this.updateMasterTableData(master);
                        //this.updateDetailTableData(detail);
                    }else {
                        alert(gettext("save fail!"))
                    }
                })
            }
        },
        saveCheck(masterChange, detailChange) {
            for (var objName of ['priority','upriority'])
            for (var priority of masterChange[objName]) {
                if (priority.score != undefined && priority.score != "" && !(/^[0-9]*$/.test(priority.score))) {
                    alert(gettext("Priority must be an integer or empty!"));
                    return false;
                }
            }
            for (var objName of ['weight','uweight'])
            for (var priority of detailChange[objName]) {
                if (priority.weight != undefined && priority.weight != "" && !(/^[0-9]*$/.test(priority.weight))) {
                    alert(gettext("Priority must be an integer or empty!"));
                    return false;
                }
            }
            return true;
        },
        masterSearchHandle(){
            this.$refs.masterTable.filter_column_params_fun = undefined;
            var contact = this.masterSearch.contact.trim();
            this.masterTable.custom_params_fun = () => {
                var recordId = this.masterSearch.recordId.trim();
                var projectName = this.masterSearch.projectName.trim();
                var attach_query = {"condition":"AND","rules":[],"not":false,"valid":true}
                if (recordId != "")
                    attach_query.rules.push({"id":"recordid","field":"recordid","type":"string","input":"text","operator":"equal","value":`${recordId}`})
                if (projectName != "")
                    attach_query.rules.push({"id":"projectname","field":"projectname","type":"string","input":"text","operator":"contains","value":`${projectName}`})
                var result = undefined;
                if (recordId == "" && projectName == "")
                    result =  {};
                else
                    result = {attach_query: JSON.stringify(attach_query)};
                if (contact != "")
                    result['sea_contact'] = contact
                return result
            };
            if (contact != "") {
                this.$refs.masterTable.datatable.column(5).visible(true);
            }
            else {
                this.$refs.masterTable.datatable.column(5).visible(false);
            }
            this.masterSearch.isPersonSearch = contact != "";
            this.$nextTick(function () {
                var newOrder = [[4, 'desc']]; // columnIndex 是要排序的列索引，direction 是排序方向
                if (contact != "")
                    newOrder = [[7, 'desc']]                
                this.$refs.masterTable.datatable.order(newOrder).search("").draw();
            });
        },
        getDetailData() {
            this.$refs.detailTable.filter_column_params_fun = undefined;
            var contact = this.currentMaster.contactc.trim();
            this.detailTable.custom_params_fun = () => {
                var recordid = this.currentMaster.recordid.trim();
                var projectid = this.currentMaster.projectid.trim();
                var method = this.currentMaster.method.trim();
                var contact = this.currentMaster.contactc.trim();
                var query = undefined;
                if (method == 'B')
                    query = {"condition":"AND","rules":[{"id":"pid","field":"pid","type":"string","input":"text","operator":"equal","value":`${projectid}`},{"id":"recordid","field":"recordid","type":"string","input":"text","operator":"equal","value":`${recordid}`}],"not":false,"valid":true}                            
                else
                    query = {"condition":"AND","rules":[{"id":"recordid","field":"recordid","type":"string","input":"text","operator":"equal","value":`${recordid}`}],"not":false,"valid":true}
                if (this.detailFilter.contact != "")
                    query.rules.push({"id":"contact","field":"contact","type":"string","input":"text","operator":"equal","value":`${this.detailFilter.contact}`})
                if (this.detailFilter.progress != "")                    
                    query.rules.push({"id":"progress","field":"progress","type":"string","input":"text","operator":"equal","value":`${this.detailFilter.progress}`})
                if (this.detailFilter.desc)
                    query.rules.push({"id":"sdesp","field":"sdesp","type":"string","input":"text","operator":"contains","value":`${this.detailFilter.desc}`})
                var result = {attach_query: JSON.stringify(query)};
                if (this.masterSearch.isPersonSearch && contact != "" && contact != undefined) {
                    result['sea_contact'] = contact
                    this.$refs.detailTable.datatable.column(11).visible(true);
                }else {
                    this.$refs.detailTable.datatable.column(11).visible(false);
                }
                return result
            };
            this.$nextTick(function () {
                var newOrder = [[10, 'desc'],[12,'asc']]; // columnIndex 是要排序的列索引，direction 是排序方向
                if (this.masterSearch.isPersonSearch && contact != "" && contact != undefined)
                    newOrder = [[14, 'desc'], [12,'asc']];
                this.$refs.detailTable.datatable.order(newOrder).search("").draw();
            });            
        },
        base64toBlob(base64Data, contentType) {
            contentType = contentType || '';
            var sliceSize = 1024;
            var byteCharacters = atob(base64Data);
            var bytesLength = byteCharacters.length;
            var slicesCount = Math.ceil(bytesLength / sliceSize);
            var byteArrays = new Array(slicesCount);

            for (var sliceIndex = 0; sliceIndex < slicesCount; ++sliceIndex) {
                var begin = sliceIndex * sliceSize;
                var end = Math.min(begin + sliceSize, bytesLength);

                var bytes = new Array(end - begin);
                for (var offset = begin, i = 0; offset < end; ++i, ++offset) {
                    bytes[i] = byteCharacters[offset].charCodeAt(0);
                }
                byteArrays[sliceIndex] = new Uint8Array(bytes);
            }
            return new Blob(byteArrays, { type: contentType });
        },
        callScheduleServer(schTypeValue) {
            if (this.masterSearch.contact == "") {
                //"Please select the contact person who needs to be scheduled from the 'Contact' dropdown menu."
                alert(gettext("select the contact who needs to be scheduled."))
                return;
            }
            //if ([1,2].indexOf(schTypeValue) != -1) {
            if ([1].indexOf(schTypeValue) != -1) {
                var showScheduleResults = this.showScheduleResultsWithAll || this.showScheduleResultsWithUser;
                axios.get("/schedule/call_service", {params:{returnResults:showScheduleResults,exportExcel:window.scheduleExportExcel != undefined,schType:schTypeValue, contact:this.masterSearch.contact}}).then((response)=>{
                    var result = response.data;
                    if(result.status) {
                        alert("schedule Success!");
                        if (window.scheduleExportExcel != undefined) {
                            const fileName = "schedule.xlsx";
                            // 此处当返回json文件时需要先对data进行JSON.stringify处理，其他类型文件不用做处理
                            //const blob = new Blob([JSON.stringify(data)], ...)
                            const blob = this.base64toBlob(result.excelFile, "application/octet-stream")
                            let dom = document.createElement('a')
                            let url = window.URL.createObjectURL(blob)
                            dom.href = url
                            dom.download = decodeURI(fileName)
                            dom.style.display = 'none'
                            document.body.appendChild(dom)
                            dom.click()
                            dom.parentNode.removeChild(dom)
                            window.URL.revokeObjectURL(url)
                        }
                        if (showScheduleResults) {
                            this.$refs.scheduleResultTable.setSchedulResultData(result.resultTasks);
                        } else {
                            var recordId = result.recordId;
                            var sessionId = result.sessionId;
                            setTimeout(() => {
                                window.open(`/devplat/sessions?recordid=${recordId}&menu_id=mi_${sessionId}#Session_Tasks`, "sch_session_tasks");   
                            });                        
                        }
                        this.initScheduleParams();
                    }else {
                        if(result.msg)
                            alert("schedule fail with user:{0}".format(result.msg))
                        else
                            alert("schedule fail!");
                    }
                })
            }
        },
        schedule(schTypeValue) {
            if (this.schType != schTypeValue && (this.schType == 1 || schTypeValue == 1)) {
                this.reloadScheduleResultTable = false;
                this.schType = schTypeValue
                this.$nextTick(function(){
                    this.reloadScheduleResultTable = true;
                    this.$nextTick(function(){
                        this.callScheduleServer(schTypeValue);
                    })
                });
            }else
                this.callScheduleServer(schTypeValue);
        },
        async saveSchParamHistory(e, isCreate) {
            e.preventDefault();            
            var historyName = null;
            if (!isCreate) {
                await this.selectSchParamsHisotry();
                if (this.selectedSchParamHistory == null)
                    return;
            }else {
                // 實現保存當前排期參數為歴史記錄的邏輯
                historyName = prompt("Please enter schedule parameter name", "");            
                if (historyName == "")
                    return;
                else if (this.schParamHistoryList != undefined && this.schParamHistoryList.filter(x=>x.desp == historyName).length > 0) {
                    alert(gettext("The name already exists, please check!"));
                    return;
                }
            }
            var historyData = []
            for (var [group, params] of Object.entries(this.scheduleParams).concat(Object.entries(this.scheduleParamsOther))) {
                historyData.push(...params);
                for (var param of params) {
                    if (param["fvalue"] === "") {
                        alert(gettext(param.nfield) + gettext(" cannot be empty!"))
                        return;
                    }
                    if (param['nfield'] == "Day Capacity" && param["fvalue"] <= 0) {
                        alert(gettext("Day capacity must be greater than 0!"))
                        return;
                    }
                }
            }
            var params = {paramsData:JSON.stringify(historyData),name:historyName}
            if (!isCreate)
                params['nfield'] = this.selectedSchParamHistory.nfield;
            else
                params['name'] = historyName;
            // 調用後端接口保存歴史記錄
            axios.post("/schedule/save_params_history", this.objectToFormData(params))
                .then(response => {
                    // 處理響應
                    var result = response.data;
                    if (result.status) {
                        alert(gettext("Save Success!"));
                        this.fetchSchParamsHistoryList();
                    }else 
                        alert(gettext("Save fail!"))
                })
                .catch(error => {
                    console.error("Error saving history", error);
                });
        },
        loadSchParamsHistory(e) {
            e.preventDefault();
            this.selectSchParamsHisotry().then((rs)=>{
                if (this.selectedSchParamHistory) {
                    // 加載選中的歴史記錄
                    axios.get("/schedule/load_params_history", {params:{'nfield':this.selectedSchParamHistory.nfield}}).then(response=>{
                        var result = response.data;
                        if (result.status) {
                            this.initScheduleParams();
                            alert(gettext("Load Success!"));
                        }else {
                            alert(gettext("Load Fail!"))
                        }
                    })
                }
            })
        },
        delSchParamsHistory(e) {
            e.preventDefault();
            this.selectSchParamsHisotry().then((rs)=>{
                if (this.selectedSchParamHistory) {
                    // 刪除選中的歷史記錄
                    axios.post("/schedule/del_params_history", this.objectToFormData({'nfield':this.selectedSchParamHistory.nfield})).then(response=>{
                        var result = response.data;
                        if (result.status) {
                            this.fetchSchParamsHistoryList();
                            alert(gettext("Delete Success!"));
                        }else {
                            alert(gettext("Delete Fail!"))
                        }
                    })
                }
            })
        },
        
        fetchSchParamsHistoryList() {
            // 實現獲取歴史記錄列錶的邏輯
            axios.get("/schedule/get_params_history_list")
                .then(response => {
                    var result = response.data;
                    if (result.status) {
                        this.schParamHistoryList = result.data;
                    }else 
                        alert(gettext("Error fetching history list"))
                    
                })
                .catch(error => {
                    console.error("Error fetching history list", error);
                });
        },        
    }
}
</script>
