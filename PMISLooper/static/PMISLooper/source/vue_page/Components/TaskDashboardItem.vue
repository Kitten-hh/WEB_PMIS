<template>
    <div ref="dashboardItem" class="card card-fluid">
              <div class="card-header py-2 d-flex align-items-center">
                <select class="status_select mr-2 text_darkBlue card_select" data-toggle="selectpicker" data-width="100%" data-size="5" @change="queryFilterChange" v-model="kanbanIdIndexOnContactQuerFilter"
                  data-none-selected-text>
                  <option v-for="(item, index) in queryFilters" :key="index" :value="index">{{ item.qf003 }}</option>
                </select>
                <div class="message-header-actions">
                  <button type="button" :class="['btn btn-icon btn-secondary', isExpend ? '' : 'mr-2']" @click="$emit('expander', $event)"><i
                      :class="[isExpend ? 'fas fa-compress-alt' : 'fas fa-expand-alt']"></i></button>
                  <button type="button" class="btn btn-icon btn-secondary" v-if="!isExpend" @click="$emit('tile', $event)"><i :class="[isTile ? 'far fa-window-restore' : 'fas fa-grip-horizontal']"></i></button>
                </div>
              </div>
              <div class="card-body p-0 pb-1" v-if="changeData">
                <LPTreegrid  v-if="showTreeGrid" ref="treeGrid" :custom_options="treeGridOptions" :datasource = "currentDataSource" :paging="1!=1" :searching="1!=1" :columns="currentColumns" idField="taskNo" parentIdField="tempRelationGoalId" />
                <TaskDashboardDataTable v-else ref="taskTable" :custom_options="taskDashboardItemTableOptions" :datasource="currentDataSource" @on_dbclick="showTaskDetail" @on_selectornot="selectChange"
                  :row_nowrap="1==1"
                  :columns="currentColumns" :searching="false" :paging="false" />
            </div>   
    </div>
</template>
<script>
import {
  DateRender,
} from "@components/looper/tables/LPDataTable.vue";
import TaskDashboardDataTable from "./TaskDashboardDataTable.vue";
import LPTreegrid from "@components/looper/tables/LPTreegrid.vue";
import axios from "axios";
export default {
    name:"TaskDashboardItem",
    components:{
        TaskDashboardDataTable,
        LPTreegrid
    },
    props:{
        itemParams:Object,
        dashBoardParam:Object,
        dashBoardParaModel:Object,
        isExpend:Boolean,
        isTile:Boolean,
        dashboardIndex:Number,
        firstDashboardIsProject:Function,
        setDashboardHeight:Function
    },
    data() {
        var local_self = this;
        return {
            defaultQueryFilter:{},
            queryFilters:[],
            dashBoardPara:{},
            showTreeGrid:false,
            changeData:false,
            kanbanIdIndexOnContactQuerFilter:0,
            taskDashboardItemTableOptions: {
                responsive: false,
                scrollY: "456px",
                processing: true,
                autoWidth: false,
                scrollX: true,
                deferLoading: 0,
                createdRow: function(row, data, dataIndex, cells) {
                    if (local_self.dashBoardPara.db007 && local_self.dashBoardPara.db007.indexOf("Project")!=-1 && dataIndex == 0) {
                        local_self.$nextTick(function(){
                            local_self.$refs.taskTable.datatable.row(':eq(0)', { page: 'current' }).select();
                        })
                    }
                }                
            },
            treeGridOptions:{
                uniqueId:"taskNo",
                responsive: false,
                scrollY: "456px",
                processing: true,
                autoWidth: false,
                scrollX: true,
            },
            currentColumns:[],
            currentDataSource:[],
            taskDashBoardItemColumn: [
                { field: "taskno", label: gettext("TaskDashboard.taskno")},
                { field: "progress", label: gettext("TaskDashboard.progress")},
                { field: "task", label: gettext("TaskDashboard.task") },
                { field: "contact", label: gettext("TaskDashboard.contact") },
                { field: "planbdate", label: gettext("TaskDashboard.planbdate"), render:this.custtomDateRender },
                { field: "schPriority", label: gettext("TaskDashboard.schPriority") },
                { field: "createDate", label: gettext("TaskDashboard.createDate"), render:this.custtomDateRender },
            ],
            taskDashBoardItemColumn1: [
                { field: "taskno", label: gettext("TaskDashboard.taskno") },
                { field: "progress", label: gettext("TaskDashboard.progress") },
                { field: "task", label: gettext("TaskDashboard.task") },
                { field: "udf04", label: gettext("TaskDashboard.udf04") },
            ],
            taskDashBoardItemColumn3: [
                { field: "taskno", label: gettext("TaskDashboard.taskno") },
                { field: "progress", label: gettext("TaskDashboard.progress") },
                { field: "task", label: gettext("TaskDashboard.task") },
                { field: "planbdate", label: gettext("TaskDashboard.planbdate"), render:this.custtomDateRender },
                { field: "planedate", label: gettext("TaskDashboard.planedate"), render:this.custtomDateRender },
            ],            
            taskDashBoardItemColumn4: [
                { field: "taskno", label: gettext("TaskDashboard.taskno") },
                { field: "progress", label: gettext("TaskDashboard.progress") },
                { field: "task", label: gettext("TaskDashboard.task") },
                { field: "planbdate", label: gettext("TaskDashboard.planbdate"),render:this.custtomDateRender },
                { field: "planedate", label: gettext("TaskDashboard.planedate"),render:this.custtomDateRender },
            ],   
            taskDashBoardItemColumn5: [
                { field: "taskno", label: gettext("TaskDashboard.taskno") },
                { field: "progress", label: gettext("TaskDashboard.progress") },
                { field: "task", label: gettext("TaskDashboard.task") },
                { field: "planbdate", label: gettext("TaskDashboard.planbdate"),render:this.custtomDateRender },
                { field: "bdate", label: gettext("TaskDashboard.bdate"),render:this.custtomDateRender},
            ],                     
            taskDashBoardItemColumn6: [
                { field: "taskno", label: gettext("TaskDashboard.taskno") },
                { field: "progress", label: gettext("TaskDashboard.progress") },
                { field: "task", label: gettext("TaskDashboard.task") },
                { field: "contact", label: gettext("TaskDashboard.contact") },
                { field: "planbdate", label: gettext("TaskDashboard.planbdate"),render:this.custtomDateRender},
            ],   
            taskDashBoardItemColumn7: [
                { field: "taskno", label: gettext("TaskDashboard.taskno") },
                { field: "progress", label: gettext("TaskDashboard.progress") },
                { field: "task", label: gettext("TaskDashboard.task") },
                { field: "createDate", label: gettext("TaskDashboard.createDate"),render:this.custtomDateRender },
                { field: "planbdate", label: gettext("TaskDashboard.planbdate"),render:this.custtomDateRender },
                { field: "planedate", label: gettext("TaskDashboard.planedate"),render:this.custtomDateRender },
            ],               
            //SubProject
            projectDashBoardItemColumn0:[
                { field: "recordid", label: gettext("TaskDashboard.recordid") },
                { field: "projectid", label: gettext("TaskDashboard.projectid") },
                { field: "projectname", label: gettext("TaskDashboard.projectname") },
                { field: "progress", label: gettext("TaskDashboard.progress") },
                { field: "fullcomplete", label: gettext("TaskDashboard.fullcomplete") },
            ],
            projectDashBoardItemColumn4:[
                { field: "pid", label: gettext("TaskDashboard.pid") },
                { field: "tid", label: gettext("TaskDashboard.pid") },
                { field: "sdesp", label: gettext("TaskDashboard.sdesp") },
                { field: "pSchedule", label: gettext("TaskDashboard.pSchedule") },
                { field: "aSchedule", label: gettext("TaskDashboard.aSchedule") },
                { field: "priority", label: gettext("TaskDashboard.priority") },
                { field: "progress", label: gettext("TaskDashboard.progress") },
                { field: "contact", label: gettext("TaskDashboard.contact") },
            ],
            treeGridColumn:[
                { field: "taskNo", label: gettext("TaskDashboard.taskno") },
                { field: "priority", label: gettext("TaskDashboard.priority"), render:function(value, row, index){
                    if(value == null)
                        return ""
                    else
                        return value;
                } },
                { field: "progress", label: gettext("TaskDashboard.progress") },                
                { field: "task", label: gettext("TaskDashboard.task") },                
            ]
        }
    },
    created(){
        var local_self = this;
        this.init();
        if (!this.firstDashboardIsProject() || (this.dashBoardPara.db007 && this.dashBoardPara.db007.indexOf("Project")!=-1))
            this.getQueryFilterDataWithParam();
        this.$eventBus.on("afterProjectChange", function(){
            if(local_self.dashBoardPara.db007 && local_self.dashBoardPara.db007.indexOf("Project")!=-1)
                return;
            else {
                local_self.init();
                local_self.getQueryFilterDataWithParam();
            }
        })
    },
    methods: {
        init() {
            if (this.itemParams.hasOwnProperty('dashBoardPara') && this.itemParams.hasOwnProperty('queryFilters')) {
                this.dashBoardPara = this.itemParams.dashBoardPara
                this.queryFilters = this.itemParams.queryFilters;
                if (this.dashBoardPara.db005 > 0 && this.queryFilters.length > (this.dashBoardPara.db005 - 1))
                    this.kanbanIdIndexOnContactQuerFilter = this.dashBoardPara.db005 - 1
                if (this.queryFilters.length > 0)
                    this.defaultQueryFilter = this.queryFilters[this.kanbanIdIndexOnContactQuerFilter]

            } else {
                alert("傳入單個Dashboard的參數不正確，請檢查!");
            }
        },
        queryFilterChange() {
            this.defaultQueryFilter = this.queryFilters[this.kanbanIdIndexOnContactQuerFilter];
            this.getQueryFilterDataWithParam();
        },
        setCurrentColumns() {
            this.currentColumns = this.taskDashBoardItemColumn;//默認
            if (this.dashBoardPara) {
                if (this.dashBoardPara.db009 && this.dashBoardPara.db009.toLowerCase().indexOf("tree") != -1) {
                    this.showTreeGrid = true;
                    this.currentColumns = this.treeGridColumn;
                } else {
                    this.showTreeGrid = false;
                    var columnId = this.getDashBoardColumnName();
                    if (columnId && columnId.length > 0)
                        this.currentColumns = this[columnId];
                }
            }
            this.setCurrentColumnWidth()            
        },
        showTaskDetail(task) {
            this.getTaskKey(task.pid,task.tid,task.taskid).then((pk)=>{
                init_task(pk);
            });
            var local_self = this;
            jqueryEventBus.one('globalTaskOperation', function(event, result) {
                if (result == undefined)
                    return;
                var method = result.method;
                if (method == "save")
                    if (local_self.showTreeGrid)
                        local_self.updateTreeGridData(task.taskno, task.data_index, result.data)
                    else
                        local_self.updateTaskTableData(task.taskno, result.data)
                else if (method == "del") 
                    local_self.getQueryFilterDataWithParam()
                });                
        },
        updateTaskTableData(taskno, dict_value) {
            var tableObj = this.$refs.taskTable;
            var table = tableObj.datatable;
            var row = table.row(`#${this.dashboardIndex}_${taskno}`)
            if (row.length > 0) {
                var row_index = row.index();
                for (const [key, value] of Object.entries(dict_value)) {
                    var col_index = tableObj.getColumnIndexByName(key);
                    if(col_index)
                        table.cell({ row: row_index, column: col_index }).data(value);
                }
            }             
        },
        updateTreeGridData(taskno, index, dict_value) {
            var data = {}
            for (var column of this.treeGridColumn) {
                var colName = column.field;
                if (colName == "taskNo")
                    data['taskNo'] = taskno;
                else
                    data[colName] = dict_value[colName];
            }
            var oldData = $(this.$refs.dashboardItem).find(".SWTreegrid").bootstrapTable("getRowByUniqueId",taskno);
            var rowData = $.extend(oldData, data);
            $(this.$refs.dashboardItem).find(".SWTreegrid").bootstrapTable("updateRow", {
                index:index,
                row:rowData
            });
        },
        getTaskKey(pid,tid,taskid) {
            return new Promise((resolve, reject)=>{
                var params = {draw:0,length:-1,start:0,attach_query: JSON.stringify(JSON.parse(`{"condition":"AND","rules":[
                        {"id":"pid","field":"pid","type":"string","input":"text","operator":"equal","value":"${pid}"},
                        {"id":"tid","field":"tid","type":"string","input":"text","operator":"equal","value":"${tid}"},
                        {"id":"taskid","field":"taskid","type":"string","input":"text","operator":"equal","value":"${taskid}"}
                    ],"not":false,"valid":true}`))};                
                axios.get("/PMIS/task/t_list", {params:params}).then((response)=>{
                    var tasks = response.data.data;
                    if (tasks.length != 0)  {
                        resolve(tasks[0].inc_id);
                    }else {
                        reject();
                    }
                });
            });
        },
        /**
         * 功能描述：根據查詢條件獲取數據
         */
        getQueryFilterDataWithParam() {
            if (this.defaultQueryFilter) {
                var key = {};
                var localDashBoardPara = this.dashBoardPara;
                if (this.dashBoardPara.db011 == 1) {
                    //自定義查詢條件
                    var tempDashBoardPara = JSON.parse(JSON.stringify(this.dashBoardPara))
                    tempDashBoardPara.db004 = `[{"qf013":"${this.defaultQueryFilter.qf013}"}]`;
                    localDashBoardPara = tempDashBoardPara;
                }else {
                    key = {qf001:this.defaultQueryFilter.qf001, qf002:this.defaultQueryFilter.qf002, qf006:this.defaultQueryFilter.qf006, qf009:this.defaultQueryFilter.qf009, qf010:this.defaultQueryFilter.qf010};
                }
                //查詢數據
                var localParams = [localDashBoardPara, key, this.dashBoardParam];
                axios.get("/looper/task_dashboard/get_data", {params:{method:"queryFilterGetDataWithParam", params:JSON.stringify(localParams)}}).then((response)=>{
                    var result = response.data;
                    if (result.status) {
                        if(this.showTreeGrid)
                            this.currentDataSource = this.handelTreeData(result.data)
                        else
                            this.currentDataSource =  this.handleRowIdData(result.data);
                        this.reloadGrid();
                    }else {
                        alert(gettext("TaskDashboard.get ") + this.$data.defaultQueryFilter.qf003 + gettext("TaskDashboard.data fail"));
                    }
                });
            }
        },
        reloadGrid() {
            this.setCurrentColumns();
            this.changeData = false;
            this.$nextTick(function() {
                this.changeData = true;
                this.$nextTick(function(){
                    this.$nextTick(function(){
                        $(this.$refs.dashboardItem).find("table.table").addClass("border-top-0 table-sm");
                        $(this.$refs.dashboardItem).find(".dataTables_wrapper>.row").addClass("d-none");                            
                        this.setDashboardHeight();
                    });
                });
            });
        },
        handelTreeData(data) {
            var taskNos = data.map((x)=>x['taskNo'])
            var newData = data.map((x)=>{
                if (taskNos.indexOf(x.relationGoalId) == -1) 
                    x.tempRelationGoalId = null; 
                else
                    x.tempRelationGoalId = x.relationGoalId; 
                return x;
            })            
            return newData;
        },
        handleRowIdData(data) {
            for (var row of data) {
                row['DT_RowId'] = `${this.dashboardIndex}_${row.taskno}`
            }
            return data;
        },
		getDashBoardColumnName(){
			if(this.dashBoardParaModel.queryFitlerTypes && this.dashBoardParaModel.queryFitlerTypes.length>0 && this.dashBoardPara){
				var name ="Task";//默認
				if(this.dashBoardPara.db009 && this.dashBoardPara.db009.length>0)
					name = this.dashBoardPara.db009;
				for(var queryType of this.dashBoardParaModel.queryFitlerTypes){
					if(queryType.set && queryType.set.length>0){
						for(var dataType of queryType.set){
							if(dataType.data==name)
								return dataType.columnId;
						}
					}
				}
			}
			return "";
		},
        selectChange(e, dt, type, i) {
            if ( type === 'row' && e.type == "select") {
              var rowData =  this.$refs.taskTable.datatable.row($(e.currentTarget).find("tr").eq(i[0] + 1)).data();
              if(this.dashBoardPara.db007 && this.dashBoardPara.db007.indexOf("Project")!=-1) {
                this.$eventBus.emit("changeProject", rowData);
              }            
          }             
        },
        /**
         * 
         * @param {*} noTileWidth 折疊時的寬度
         * @param {*} tileWidth 平鋪時的寬度
         * @param {*} expanderWidth 全屏的寬度
         */
        getColumnWidth(noTileWidth, tileWidth, expanderWidth) {
            if (this.isExpend)
                return expanderWidth;
            else if (this.isTile)
                return tileWidth;
            else
                return noTileWidth;
        },
        setCurrentColumnWidth() {
            var despCol = undefined;
            for (var col of this.currentColumns) {
                var colName = col.field.toLowerCase();
                if (colName == 'taskno'){
                    if (this.showTreeGrid)
                        col['width'] = this.getColumnWidth("150px", "120px", "180px")
                    else
                        col['width'] = this.getColumnWidth("120px", "80px", "150px")
                }
                else if (colName == "progress")
                    col['width'] = this.getColumnWidth("50px", "25px", "60px")
                else if (["planbdate","planedate","createdate","bdate"].indexOf(colName) != -1)
                    col['width'] = this.getColumnWidth("75px","75px","75px")
                else if (["priority","schpriority"].indexOf(colName) != -1)
                    col['width'] = this.getColumnWidth("50px","40px","60px")                    
                else if (["pid","tid", "recordid","projectid","fullcomplete","pschedule","aschedule"].indexOf(colName) != -1)
                    col['width'] = this.getColumnWidth("50px","50px","50px")
                else if (["sdesp","task","projectname"].indexOf(colName) != -1) {
                    despCol = col;
                    continue;
                }
                else
                    col['width'] = this.getColumnWidth("50px","50px","50px")
            }
            if (despCol) {
                var totalWidth = $(this.$refs.dashboardItem).closest(".card-item").width()
                var otherColWidth = 0;
                var sumWithInitial =  this.currentColumns.reduce((accumulator, col) => accumulator + (["sdesp","task","projectname"].indexOf(col.field) != -1 ? 0 : parseFloat(col.width.replace("px","")) + 10), otherColWidth)
                despCol['width'] = "{0}px".format(totalWidth - sumWithInitial - 80);
            }
        },
        custtomDateRender(data, type, full, meta){
            try {
                var data = DateRender(data, type, full, meta);
                data = data ? data : "";
                var width  = meta.settings.aoColumns[meta.col].sWidth
                return "<label title='" + data + "' class='text-truncate d-inline-block' style='width:" + width + ";text-decoration: none;'>" + data + "</label>";                  
            } catch (error) {
                return data;
            }
        }
    },
    mounted() {
        $(".status_select").selectpicker('refresh');
        var local_self= this;
        $(this.$refs.dashboardItem).on("dblclick", ".SWTreegrid tr", function(){
            var taskno = $(this).attr("data-uniqueid");
            var index = $(this).attr("data-index")
            var tasknoArr = taskno.split("-");
            var task = $(local_self.$refs.dashboardItem).find(".SWTreegrid").bootstrapTable("getRowByUniqueId", taskno)
            task.pid = tasknoArr[0];
            task.tid = tasknoArr[1];
            task.taskid = tasknoArr[2];
            task.taskno = taskno;
            task.data_index = parseInt(index);
            local_self.showTaskDetail(task);
        });
    }
}
</script>
