<template>
    <div id="scheduleResultContent">
        <TabBar :Hasdropdown="1==1" :tabList="tabList" :downList="downList">
            <template v-for="(tabdata, index) in tabList" :key="index" v-slot:[tabdata.bodyname]>
                <div class="mt-xl col-xs col-sm col-md mt-2 pl-1">
                    <div class="input-group input-group-alt" style="">
                        <label class="col-form-label caption formula-label pr-1">{{ $t("Formula") }}</label> 
                        <input type="text" class="form-control control col-auto" placeholder=""  v-model="tabdata.formula">
                    </div>
                </div>                
                <FilterDataTable :paging="false" :columns="scheduleResultColumns" :datasource="tabdata.tasks"
                :custom_options="custom_options"
                :row_nowrap="1==1"
                :orderBy="orderBy"
                @on_selectornot="select_row"
                @on_dbclick="dbclick"
                :searching="1 != 1" :paging_inline="1 == 1" :ref="'scheduleResultTable_'+tabdata.contact" />
            </template>
        </TabBar>
    </div>
</template>
<script>
import { DateRender } from "@components/looper/tables/LPDataTable.vue";
import FilterDataTable from "./FilterDataTable.vue";
import TabBar from "@components/looper/navigator/TabBar.vue";
export default {
    name: "ScheduleResultTable",
    components:{
        FilterDataTable,
        TabBar
    },
    props:{
        scheduleParams:{
            type: Object,
            default: undefined
        },
        schType:{
            type:Number,
            default:2
        }
    },
    data() {
        var self = this;
        return {
            tabList:[
            ],
            custom_options:{
                responsive: false,  //是否支持手機展開和隱藏列
                scrollX: true,
                row_nowrap: true,
                autoWidth: false,
                scrollResize: true,
                scrollY: "60vh",
                select:true,
                deferLoading:0,
                select: {
                    style:'single',
                },
                initComplete: function () {
                    var table = this.api();
                    self.refreshTableFilter(table);
                }, 
                drawCallback: function (settings) {
                    var table = this.api();
                    table.columns().every(function () {
                        var column = this;
                        var select = $(column.header()).find("select").length > 0 ? $($(column.header()).find("select")[0]) : undefined;
                        if (select != undefined) {
                            select.attr("style", $(column.header()).attr("style"));
                        }
                    });                    
                }
            },
            downList:[],
            scheduleResultColumns:[
                { field: "inc_id", label: gettext("INC_ID")},                
                { field: "taskno", label: gettext("Task No") },                
                { field: "contact", label: gettext("Contact") },                
                { field: "sch_create_date", label: gettext("Create Date"), render: DateRender },                
                { field: "seqno", label: gettext("Seq No") },                
                { field: "projectpriority", label: gettext("Project Priority") },                
                { field: "sessionpriority", label: gettext("Session Priority") },                
                { field: "sessioncapacity", label: gettext("Session Capacity"), visible:false},           
                { field: "loopseqno", label: gettext("Loop Seq No"), visible:false },                                                                                   
                { field: "task", label: gettext("Task Description"),width:"300px", render:self.taskRender },                
                { field: "subprojectid", label: gettext("Project") },                
                { field: "priority", label: gettext("priority") },                
                { field: "class_field", label: gettext("Class") },                
                { field: "planbdate", label: gettext("PlanBDate"),render: DateRender },                                
                { field: "schcategory", label: gettext("Schedule Type") },                                
                { field: "methodofcalculation", label: gettext("Method of calculation") },  
                { field: "tpseqno", label: gettext("Tp Seq No"), visible:false},                                
                { field: "temppriority", label: gettext("Temp Priority"), visible:false},
                { field: "adjustpriority", label: gettext("Adjust Priority") },
                { field: "schpriority", label: gettext("Sch Priority") },                                
                { field: "schdate", label: gettext("Sch Date"),render: DateRender },                                                
                { field: "schpriority_formula", label: gettext("Sch Priority(Formula)") },                                                
                { field: "diff", label: gettext("Diff") },                                                
            ],
            orderBy: [['schpriority', 'desc']],
        }
    },
    created() {
        if (this.schType == 1) {
            var scenarioOneNotShowFields = ['sessioncapacity','tpseqno','loopseqno','temppriority','adjustpriority'];
            for (var i = this.scheduleResultColumns.length-1; i>=0; i--) {
                if (scenarioOneNotShowFields.indexOf(this.scheduleResultColumns[i].field) != -1)
                    this.scheduleResultColumns.splice(i, 1);
            }
        }
        for (var column of this.scheduleResultColumns) {
            this.downList.push({href:column.field, label:column.label})
        }
    },
    mounted() {
        var self = this;
        $('#scheduleResultContent').on("shown.bs.tab","a[data-toggle='tab']", function (e) {
            $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
        });
        $("#scheduleResultContent .nav-item.dropdown>a").text("");
        $("#scheduleResultContent .nav-item.dropdown>a").prepend("<i class='fa fa-th-list'/><span class='caret'></span>");
        $("#scheduleResultContent .nav-item .dropdown-menu").addClass("dropdown-scroll stop-propagation");
        $("#scheduleResultContent .nav-item .dropdown-menu").css("overflowX","hidden");
        var activeFields = this.scheduleResultColumns.filter(x=>x.visible == undefined || x.visible).map(x=>x.field)
        $("#scheduleResultContent .dropdown-menu .dropdown-item").filter(function() {
            return activeFields.indexOf($(this).attr('href')) != -1;
        }).addClass("col_active");
        $("#scheduleResultContent .dropdown-menu .dropdown-item").on("click", function(e){
            e.preventDefault();
            $(this).toggleClass("col_active");
            var isShow = $(this).hasClass("col_active");
            var colName = $(this).attr("href");
            for (var tabdata of self.tabList) {
                var contact = tabdata.contact;
                var tableColumn = self.$refs['scheduleResultTable_'+contact].datatable.columns(self.$refs['scheduleResultTable_'+contact].getColumnIndexByName(colName));
                tableColumn.visible(isShow);
            }
        });
        $("#scheduleResultContent .card-header-tabs").addClass("align-items-center");
        var clearButton = $(`<button class="btn btn-sm btn-primary"><i class="fa fa-broom d-xxxl-none"></i><span class="d-none d-xxxl-inline-block">Clear</span></button>`)
        $("#scheduleResultContent .card-header-tabs").append(clearButton)
        clearButton.on("click", function(e){
            if ($('#scheduleResultContent .nav-link.active').length > 0) {
                var id = $('#scheduleResultContent .nav-link.active').attr("href").replace("#","")
                $("#"+id + " .scheduleResultFilterSelect").val("");
                //清除Datatable的filter
                var contact = id.replace("scheduleResult_","");
                self.$refs['scheduleResultTable_'+contact].datatable.search('').columns().search('').draw();
            }
        });
    },
    methods: {
        setSchedulResultData(resultDatas) {
            //先刪除不需要的
            var contacts = Object.keys(resultDatas);
            for (var i = this.tabList.length-1; i>=0; i--) {
                if (contacts.indexOf(this.tabList[i].contact) == -1)
                    this.tabList.splice(i, 1);
            }
            for(var [contact, tasks] of Object.entries(resultDatas)) {
                for (var task of tasks) {
                    if (task.schpriority != null && task.schpriority != undefined)  {
                        var formulaArr = this.getFormula(task)
                        task['schpriority_formula'] = formulaArr[1];
                        task['diff'] = task['schpriority_formula'] - task['schpriority'];
                    }
                }
                var index = this.tabList.findIndex(x=>x.contact == contact)
                if (index == -1) {
                    this.tabList.push({contact:contact, tabid:"scheduleResult_" + contact, label:contact, bodyname:"scheduleResult_" + contact, tasks:tasks, formula:""})
                }
                else {
                    this.tabList[index].tasks = tasks
                    this.$refs['scheduleResultTable_'+contact].datatable.clear();
                    //清除之前的過濾
                    this.$refs['scheduleResultTable_'+contact].datatable.search('').columns().search('').draw();                    
                    this.$refs['scheduleResultTable_'+contact].datatable.rows.add(tasks).draw();
                    this.refreshTableFilter(this.$refs['scheduleResultTable_'+contact].datatable);
                }
            }
            this.$nextTick(function () {
                this.$nextTick(function(){
                    $("table.table").addClass("border-top-0 table-sm");
                    $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
                })
            });
        },
        refreshTableFilter(table) {
            table.columns().every(function () {
                var column = this;
                var select = $(column.header()).find("select").length > 0 ? $($(column.header()).find("select")[0]) : undefined;
                if (select == undefined) {
                    var selectParent = $("<div><div>").append($(`<select class="scheduleResultFilterSelect" style="${$(column.header()).attr("style")}"></select>`)
                        .on('change', function () {
                            var val = $.fn.dataTable.util.escapeRegex($(this).val());
                            column.search(val ? '^' + val + '$' : '', true, false).draw();
                        })).on("click", function(e) {
                            e.stopPropagation();
                        }).appendTo($(column.header()))                   
                    select = $(selectParent.find("select")[0])
                }
                select.empty();
                select.append('<option value=""></option>');
                var addDisplayData = ["sch_create_date","planbdate","schdate"].indexOf(column.dataSrc()) != -1
                var displayDatas = []
                column.data().unique().sort().each(function (d, j) {
                    if (addDisplayData) {
                        var displayData = DateRender(d);
                        if (displayDatas.indexOf(displayData) == -1) {
                            select.append('<option value="' + displayData + '">' + displayData + '</option>');                        
                            displayDatas.push(displayData);
                        }
                    }else 
                        select.append('<option value="' + d + '">' + d + '</option>');
                });
                $(column.footer()).empty();
            });
        },
        taskRender(data, type, full, meta){
            try {
                var width  = meta.settings.aoColumns[meta.col].sWidth
                data = data ? data : "";
                data = $('<div>').text(data).html();
                return "<label title='" + data + "' class='text-truncate d-inline-block' style='width:" + width + ";text-decoration: none;'>" + data + "</label>";                  
            } catch (error) {
                return data;
            }
        },
        select_row(e, dt, type, indexes) {
            if (e.type === "select") {
                var contact = $(e.currentTarget).closest(".tab-pane").attr("id").replace("scheduleResult_","");
                var index = this.tabList.findIndex(x=>x.contact == contact)
                if (index != -1) {
                    var rows = dt.rows({selected: true}).data();                    
                    var rowData = rows[0]
                    var formulaArr = this.getFormula(rowData);
                    this.tabList[index].formula = formulaArr[0] + "=" + formulaArr[1]
                }
            }
        },
        getFormula(rowData) {
            var values = []
            var formulaStr = ""
            if (rowData.projectpriority != undefined && rowData.projectpriority != null) {
                formulaStr += `Project Priority[${rowData.projectpriority}]`
                values.push(rowData.projectpriority);
            }
            else
                formulaStr += `Project Priority[0]`
            if (rowData.sessionpriority != undefined && rowData.sessionpriority != null) {
                formulaStr += ` + Session Priority[${rowData.sessionpriority}]`
                values.push(rowData.sessionpriority);
            }else
                formulaStr += ` + Session Priority[0]`
                
            if (rowData.class_field === "Class 1") {
                formulaStr += ` + Class 1[${this.scheduleParams.group3[0]['fvalue']}]`
                values.push(this.scheduleParams.group3[0]['fvalue']);
            }
            else
                formulaStr += ` + Class 1[0]`
            var priorityIndex=  this.scheduleParams.group3.findIndex(x=>x.nfield === "Priority("+rowData.priority+")")
            if (priorityIndex != -1) {
                var param = this.scheduleParams.group3[priorityIndex];
                formulaStr += ` + ${param.nfield}[${param.fvalue}]`
                values.push(param.fvalue);
            }else
                formulaStr += ` + Priority[0]`
            formulaStr += ` + Seq No[${rowData.seqno}] `
            values.push(rowData.seqno);
            var scheduleTypeIndex=  this.scheduleParams.group2.findIndex(x=>x.nfield === rowData.schcategory)
            if (scheduleTypeIndex != -1) {
                var param = this.scheduleParams.group2[scheduleTypeIndex];
                formulaStr += ` + Schedule Type(${param.nfield})[${param.fvalue}]`
                values.push(param.fvalue);
            }else
                formulaStr += ` + Schedule Type[0]`
            if (rowData.methodofcalculation === "Formula 2") {
                if (rowData.adjustpriority != undefined && rowData.adjustpriority != null) {
                    formulaStr += ` + Adjust Priority[${rowData.adjustpriority}]`
                    values.push(rowData.adjustpriority);
                }else
                    formulaStr += ` + Adjust Priority[0]`;                
            }
            var result = 0
            for (var val of values)
                result += parseInt(val);
            return [formulaStr,result];
        },
        dbclick(data) {
            init_task(data.inc_id);
        },
        setContactLabShow(flag) {
            if (flag)
                $("#scheduleResultContent>.card .nav-item:not(.dropdown)").show();
            else
                $("#scheduleResultContent>.card .nav-item:not(.dropdown)").hide();
        }
    }
}
</script>
<style>
#scheduleResultContent>.card {
    margin-bottom: 0px !important;
}
#scheduleResultContent .dropdown-menu .dropdown-item {
    position: relative;
    padding-right: 26px;
}
#scheduleResultContent .dropdown-menu .dropdown-item.col_active::before {
    position: absolute;
    top: 50%;
    margin-top: -10px;
    right: 0.8em;
    display: inline-block;
    content: "✓";
    color: inherit;
}    
#scheduleResultContent .scheduleResultFilterSelect {
    -moz-appearance: none;
    -webkit-appearance: none;
    appearance: none;
    background-image: url(data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23000000%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E);
    background-repeat: no-repeat;
    background-position: right 0.3em top 50%;
    background-size: 0.55em auto;
    border-radius: 0.25rem;
    border-color: #c9c8c8;
    fill: #ccc;
    padding-right: 1em;
}
#scheduleResultContent .formula-label {
    font-weight: 600;
    font-size: 16px;    
}
</style>