<template>
    <BlankPageLayout>
        <template v-slot:page-Details>
            <LPCard show_part="hb" class_str="mb-0 main_card">
                <template v-slot:header>
                    <div class="d-flex align-items-center justify-content-between">
                        <h5 class="mb-0">{{ $t("Set Project-Session Prioirty") }}</h5>
                        <div class="dropdown" style="">
                            <button type="button" class="btn btn-info dropdown-toggle order-button" data-toggle="dropdown"
                                aria-haspopup="true" aria-expanded="false"><i class="fa fa-bars m-0 mr-xl-1"
                                    aria-hidden="true"></i><span class="d-none d-xl-inline">Schedule Method</span></button>
                            <div class="dropdown-menu">
                                <div v-for="(item,index) in scenarioList" :key="index" @click="schedule(item.schType)">
                                    <div class="dropdown-arrow right"></div><a class="dropdown-item" href="#">Scenario - {{ item.label }}</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </template>
                <template v-slot:body>
                    <div :class="['row h-100', lang_code_en ? 'lang_en' : '']">
                        <div class="col-12 col-lg-6 col-xl-5 col-xxl-4 col-xxxxl-3 mb-4 mb-sm-0 d-none d-md-block pr-0 h-100">
                            <div class="wrapper_test pb-2" id="card_para">
                                <div class="schparam_container scrollbar">
                                    <div class="col-12 px-0">
                                        <h3 class="text-dark-75 trm-title-with-divider mb-0">
                                            {{ $t("Schedule Parameter") }}
                                            <label name="lb_contact" class="m-0 text-warning"></label>
                                            <span class="m-0"></span>
                                        </h3>
                                    </div>
                                    <div class="card-body px-0 p-sm-3 card_para_body">
                                        <div class="row pc_parameter px-0">
                                            <div v-for="(params, group, index) in scheduleParams" :key="index"
                                                class="col-12 mb-3">
                                                <div class="box boxs">
                                                    <div v-if="index == 0" class="cs_content flex-row-fluid">
                                                        <h4 class="flex-grow-1 text-dark">{{ $t("Show Schedule Results") }}</h4>
                                                        <input type="checkbox" class="form-control"
                                                            v-model="showScheduleResultsWithAll" style="width: 20px;height:20px">
                                                    </div>                                                    
                                                    <div v-for="(param, subIndex) in params" :key="subIndex"
                                                        class="cs_content flex-row-fluid">
                                                        <h4 v-if="param.nfield == 'Week are Scheduled'"
                                                            class="flex-grow-1 text-dark">{{ $t(param.nfield) }}{{ $t("(Red is selected)")}}</h4>
                                                        <h4 v-else class="flex-grow-1 text-dark">{{ $t(param.nfield) }}</h4>
                                                        <div v-if="param.nfield == 'Week are Scheduled'"
                                                            class="d-flex mt-2 justify-content-end WeekAreScheduled w-100">
                                                            <a href="#"
                                                                :class="['badge badge-subtle mr-1', getWeekAreScheduledDay(1) ? 'active' : '']"
                                                                @click="selectWeekAreScheduledDay($event, 1)">{{ $t("Mon") }}</a>
                                                            <a href="#"
                                                                :class="['badge badge-subtle mr-1', getWeekAreScheduledDay(2) ? 'active' : '']"
                                                                @click="selectWeekAreScheduledDay($event, 2)">{{ $t("Tue") }}</a>
                                                            <a href="#"
                                                                :class="['badge badge-subtle mr-1', getWeekAreScheduledDay(3) ? 'active' : '']"
                                                                @click="selectWeekAreScheduledDay($event, 3)">{{ $t("Wed") }}</a>
                                                            <a href="#"
                                                                :class="['badge badge-subtle mr-1', getWeekAreScheduledDay(4) ? 'active' : '']"
                                                                @click="selectWeekAreScheduledDay($event, 4)">{{ $t("Thu") }}</a>
                                                            <a href="#"
                                                                :class="['badge badge-subtle mr-1', getWeekAreScheduledDay(5) ? 'active' : '']"
                                                                @click="selectWeekAreScheduledDay($event, 5)">{{ $t("Fri") }}</a>
                                                            <a href="#"
                                                                :class="['badge badge-subtle mr-1', getWeekAreScheduledDay(6) ? 'active' : '']"
                                                                @click="selectWeekAreScheduledDay($event, 6)">{{ $t("Sat") }}</a>
                                                            <a href="#"
                                                                :class="['badge badge-subtle', getWeekAreScheduledDay(0) ? 'active' : '']"
                                                                @click="selectWeekAreScheduledDay($event, 0)">{{ $t("Sun") }}</a>
                                                        </div>
                                                        <input v-else class="textEdit form-control" type="number" min="0"
                                                            onkeypress="return (event.charCode !=8 && event.charCode ==0 || (event.charCode >= 48 && event.charCode <= 57))"
                                                            v-model="param.fvalue" style="width: 75px;">
                                                        <input v-if="group == 'group2'" class="textEdit form-control ml-1"
                                                            type="number" min="0"
                                                            onkeypress="return (event.charCode !=8 && event.charCode ==0 || (event.charCode >= 48 && event.charCode <= 57))"
                                                            v-model="scheduleParamsOther.categoryCapacity[subIndex]['fvalue']"
                                                            style="width: 40px;">
                                                    </div>
                                                    <div v-if="index == 0 && scheduleParamsScenario != undefined" class="cs_content flex-row-fluid">
                                                        <h4 class="flex-grow-1 text-dark">{{ $t("Scenario") }}</h4>
                                                        <span class="schedule_scenario">{{ scheduleParamsScenario }}</span>
                                                    </div>                                                       
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-12 p-0 pl-3 pr-4 pt-1">
                                    <div class="box flex-row inner-box" style="height: 100%;">
                                        <div class="cs_content flex-row-fluid" style="justify-content: flex-end;">
                                            <div class="btn-group">
                                                <button id="btn_saveParam" class="btn btn-subtle-primary"
                                                    style="font-weight: 900;font-size: larger;"
                                                    @click="saveScheduleParams">{{ $t("Save") }}</button>
                                                <button type="button" class="btn btn-subtle-primary dropdown-toggle dropdown-toggle-split mr-2" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                </button>
                                                <div class="dropdown-menu save-params">
                                                    <a class="dropdown-item" @click="loadSchParamsHistory($event)" href="#">{{$t("Load from History")}}</a>
                                                    <a class="dropdown-item" @click="saveSchParamHistory($event, true)" href="#">{{$t("Save as History")}}</a>
                                                    <a class="dropdown-item" @click="saveSchParamHistory($event)" href="#">{{$t("Update to History")}}</a>
                                                    <a class="dropdown-item" @click="delSchParamsHistory" href="#">{{ $t("Delete History") }}</a>
                                                </div>                                                
                                            </div>
                                            <button id="btn_restore" class="btn btn-subtle-primary"
                                                style="font-weight: 900;font-size: larger;"
                                                @click="restore">{{ $t("Cancel") }}</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-12 col-lg-6 col-xl-7 col-xxl-8 col-xxxxl-9 p-0 h-100 mt-md-3 mt-lg-0">
                            <div class="card card-fluid tabs-border-card border-top-0 mb-0 h-100" style="border-top-left-radius: 0;border-top-right-radius: 0;">
                                <div class="card-header tabs_header">
                                    <ul class="nav nav-tabs card-header-tabs">
                                        <li class="nav-item">
                                            <a class="nav-link show active py-2" data-toggle="tab" href="#projectSessionPriority">{{ $t("Set Priority") }}</a>
                                        </li>
                                        <li class="nav-item">
                                            <a class="nav-link py-2" data-toggle="tab" href="#scheduleResult">{{ $t("Schedule Result") }}</a>
                                        </li>
                                    </ul>
                                </div>
                                <div id="priorityTabContent" class="tab-content">
                                    <div class="tab-pane fade active show h-100" id="projectSessionPriority">
                                        <splitpanes ref="splitpanesRef" class="default-theme" horizontal @resized="getPriorityHeight" @splitter-click="handleSplitterDoubleClick">
                                            <pane class="topPane" size="40">
                                                <LPCard show_part="b" class_str="master_card card-reflow h-100">
                                                    <template v-slot:body>
                                                        <div class="masterWrapper h-100">
                                                            <div class="row mt-2 mx-0">
                                                                <div class="form-group d-flex col-12 col-xs-5 col-sm col-lg-5 col-xl-4 col-xxl-2 px-1">
                                                                    <label class="col-form-label caption col-auto pl-0" for="tf1">{{
                                                                        $t('Contact') }}</label>
                                                                    <select class="status_select control"
                                                                        data-toggle="selectpicker" data-width="100%" data-size="5"
                                                                        data-none-selected-text v-model="masterSearch.contact" data-container="body">
                                                                        <option></option>
                                                                        <option v-for="(option, inx) in allContacts" :key="inx"
                                                                            :value="option">{{ option }}</option>
                                                                    </select>
                                                                </div>
                                                                <div class="form-group d-flex col-12 col-xs-7 col-sm col-lg-7 col-xl col-xxl-3 col-xxxxl-2 px-1">
                                                                    <label class="col-form-label caption col-auto pl-0" for="tf1">{{
                                                                        $t('RecordId') }}</label>
                                                                    <input type="text" class="form-control control col"
                                                                        v-model="masterSearch.recordId" />
                                                                </div>
                                                                <div
                                                                    class="form-group d-flex col-12 col-xs-7 col-sm-12 col-lg-7 col-xl-12 col-xxl px-1 order-first order-xxl-0">
                                                                    <label class="col-form-label caption col-auto pl-0" for="tf1">{{
                                                                        $t('ProjectName') }}</label>
                                                                    <input type="text" class="form-control control col"
                                                                        v-model="masterSearch.projectName" />
                                                                </div>
                                                                <div class="col-12 col-sm-auto px-1 btnTools">
                                                                    <button class="btn btn-primary" @click="masterClear"><i
                                                                            class="fa fa-broom d-xxxl-none"></i><span
                                                                            class="d-none d-xxxl-inline-block">{{ $t("Clear")
                                                                            }}</span></button>
                                                                    <button class="btn btn-primary"
                                                                        @click="masterSearchHandle"><i
                                                                            class="oi oi-magnifying-glass d-xxxl-none"></i><span
                                                                            class="d-none d-xxxl-inline-block">{{ $t("Search")
                                                                            }}</span></button>
                                                                    <button class="btn btn-primary save_btn"
                                                                        @click="batchUpdatePriority"><i
                                                                            class="fa fa-save d-xxxl-none"></i><span
                                                                            class="d-none d-xxxl-inline-block">{{ $t("Save")
                                                                            }}</span></button>
                                                                </div>
                                                            </div>
                                                            <LPDataTable :paging="false" :columns="masterTable.columns"
                                                                :datasource="masterTable.datasource"
                                                                :custom_params_fun="masterTable.custom_params_fun"
                                                                :custom_options="masterTable.custom_options"
                                                                :orderBy="masterTable.orderBy"
                                                                @on_selectornot="masterTable.select_row"
                                                                :handle_response_fun="masterTable.handle_response_fun"
                                                                :searching="1 != 1" :paging_inline="1 == 1" ref="masterTable" />
                                                        </div>
                                                    </template>
                                                </LPCard>
                                            </pane>
                                            <pane class="bottomPane" size="60">
                                                <LPCard show_part="b" class_str="mb-0 detail_card card-reflow h-100">
                                                    <template v-slot:body>
                                                        <div class="row m-0 mt-2">
                                                            <div class="form-group mb-1 d-flex col-12 col-xs-6 col-sm-6 col-xl-4 col-xxl-2 px-1">
                                                                <label class="col-form-label caption col-auto pl-0">{{ $t('Contact')
                                                                }}</label>
                                                                <select class="status_select control"
                                                                    data-toggle="selectpicker" data-width="100%" data-size="5" data-none-selected-text
                                                                    v-model="detailFilter.contact" data-container="body">
                                                                    <option></option>
                                                                    <option v-for="(option, inx) in allContacts" :key="inx"
                                                                        :value="option">{{ option }}</option>
                                                                </select>
                                                            </div>
                                                            <div class="form-group mb-1 d-flex col-12 col-xs-6 col-sm-6 col-xl col-xxl-2 px-1">
                                                                <label class="col-form-label caption col-auto pl-0" for="tf1">{{
                                                                    $t('Progress') }}</label>
                                                                <select class="status_select" data-width="100%" data-toggle="selectpicker"
                                                                    data-none-selected-text v-model="detailFilter.progress" data-container="body">
                                                                    <option value=""></option>
                                                                    <option value="I">I:正在進行</option>
                                                                    <option value="T">T:當天必須完成任務</option>
                                                                    <option value="N">N:未開始</option>
                                                                    <option value="S">S:已經開始的工作</option>
                                                                    <option value="C">C:基本完成</option>
                                                                    <option value="F">F:已經完成</option>
                                                                </select>
                                                            </div>
                                                            <div class="form-group mb-1 d-flex col col-xl-12 col-xxl px-1">
                                                                <label class="col-form-label caption col-auto pl-0" for="tf1">{{
                                                                    $t('Description') }}</label>
                                                                <input type="text" class="form-control control col"
                                                                    v-model="detailFilter.desc" />
                                                            </div>
                                                            <div class="col-auto px-1">
                                                                <button type="button" class="btn btn-primary btn-clear mr-2"
                                                                    @click="detailClear"><i
                                                                        class="fa fa-broom d-xxxl-none"></i><span
                                                                        class="d-none d-xxxl-inline-block">{{ $t("Clear")
                                                                        }}</span></button>
                                                                <button type="button" class="btn btn-primary btn-search"
                                                                    @click="getDetailData"><i
                                                                        class="oi oi-magnifying-glass d-xxxl-none"></i><span
                                                                        class="d-none d-xxxl-inline-block">{{ $t("Filter")
                                                                        }}</span></button>
                                                            </div>
                                                        </div>
                                                        <LPDataTable :paging="false" :columns="detailTable.columns"
                                                            :datasource="detailTable.datasource"
                                                            :custom_params_fun="detailTable.custom_params_fun"
                                                            :custom_options="detailTable.custom_options"
                                                            :orderBy="detailTable.orderBy"
                                                            :handle_response_fun="detailTable.handle_response_fun"
                                                            @on_selectornot="detailTable.select_row"
                                                            @on_dbclick="detailTable.dbclick" :searching="1 != 1"
                                                            :paging_inline="1 == 1" ref="detailTable" />
                                                    </template>
                                                </LPCard>
                                            </pane>
                                        </splitpanes>
                                    </div>
                                    <div class="tab-pane fade" id="scheduleResult">
                                        <ScheduleResultTable v-if="reloadScheduleResultTable" ref="scheduleResultTable" :scheduleParams="scheduleParams" :schType="schType"/>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </template>
            </LPCard>
        </template>
    </BlankPageLayout>
    <LPModalForm id="schParamsHistoryListForm" ref="schParamsHistoryListForm" :title="$t('Schedule Parameters History')" @on_submit="submitSchParamsHistoryListForm">
        <div class="list-group list-group-bordered">
            <a href="#"
            class="list-group-item list-group-item-action"
            v-for="(history,index) in schParamHistoryList"
            :key="index"
            :class="{ active: selectedSchParamHistory != null && selectedSchParamHistory.nfield === history.nfield }"
            @click.prevent="selectedSchParamHistory = (selectedSchParamHistory == history ? null : history)">
            {{ history.desp }}
            </a>
        </div>        
    </LPModalForm>
</template>
<script>
import axios from "axios";
import BlankPageLayout from "@components/looper/layout/page/BlankPageLayout.vue";
import LPCard from "@components/looper/layout/LPCard.vue";
import LPDataTable, { DateRender } from "@components/looper/tables/LPDataTable.vue";
import ScheduleResultTable from "./Components/ScheduleResultTable.vue"
import LPCombobox from "@components/looper/forms/LPCombobox.vue";
import LPModalForm from "@components/looper/layout/LPModalForm.vue";
import { Splitpanes, Pane } from 'splitpanes';  // 導入Splitpanes元件和Pane元件
import 'splitpanes/dist/splitpanes.css';
export default {
    name: "ShcedulePriority_vueFrm_UI",
    components: {
        BlankPageLayout,
        LPCard,
        LPDataTable,
        LPCombobox,
        ScheduleResultTable,
        LPModalForm,
        Splitpanes,
        Pane,
    },
    mounted() {
        this.init();
        var self = this
        this.$nextTick(function () {
            $("table.table").addClass("border-top-0 table-sm");
            //$(".dataTables_wrapper>.row").addClass("d-none");
            $('.tabs-border-card>.tabs_header a[data-toggle="tab"]').on("shown.bs.tab", function (e) {
                self.getPriorityHeight();
            })
            self.getPriorityHeight();
        });
        $(window).on('resize', function () {
            $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
            $(".status_select").selectpicker('refresh');
        });
        $(".page").on("blur", ".textEdit", function () {
            var value = $(this).val();
            var oldvalue = $(this)[0].hasAttribute("oldscore") ? $(this).attr("oldscore") : $(this)[0].hasAttribute("oldweight") ? $(this).attr("oldweight") : $(this).attr("oldcapacity");
            if (value != oldvalue) {
                $(this).removeClass("text-dark");
                // Update the useronlyscore field in the datatable
                if ($(this)[0].hasAttribute("field")) {
                    var row = $(this).closest('tr');
                    var datatable = $(this).closest('.dataTable').DataTable();
                    var row_index = datatable.row(row).index();
                    var columnname = $(this).attr("field").replace("only","");
                    var column = datatable.column(columnname + ':name');
                    if (column) {
                        var col_index = column.index()
                        datatable.cell({ row: row_index, column: col_index }).data(parseFloat(value));
                    }
                }
            }
            else
                if (!$(this).hasClass("text-dark"))
                    $(this).addClass("text-dark");
        });

        window.addEventListener('resize', this.getPriorityHeight);
        const splitter = document.querySelector('.splitpanes__splitter');
        splitter.addEventListener('dblclick', this.handleSplitterDoubleClick);

        this.get_lang_code();
    },
    data() {
        var self = this;
        return {
            schType:2,
            reloadScheduleResultTable:true,
            showScheduleResultsWithAll:false,
            scenarioList:[
                {schType:1, label:"One Project One Session"},
                {schType:2, label:"One Project Two Session"},
                {schType:3, label:"Mutil Project One Session"},
                {schType:4, label:"Mutil Project Two Session"}
            ],
            masterTable: {
                columns: [
                    { field: "recordid", label: gettext("RecordID"), width: "100px" },
                    { field: "projectname", label: gettext("Project Name") },
                    { field: "contact", label: gettext("Contact") },
                    { field: "sqty", label: gettext("Session Qty") },
                    {
                        field: "score", label: gettext("Priority"), width: "120px", className: "rendered-input-cell",
                        render: function (data, type, row) {
                            var value = data == null ? "" : data;
                            if (row['score'] == row['oldscore'])
                                return `<input class="textEdit priority form-control text-dark" type="text" value="${value}" inc_id="${row.inc_id}" oldvalue="${value}" oldscore="${row.oldscore}" style="width: 100px;">`;
                            else
                                return `<input class="textEdit priority form-control" type="text" value="${value}" inc_id="${row.inc_id}" oldvalue="${value}" oldscore="${row.oldscore}" style="width: 100px;">`;
                        }
                    },
                    {
                        field: "useronlyscore", label: gettext("UPriority"), width: "120px", className: "rendered-input-cell", visible: false,
                        render: function (data, type, row) {
                            var value = data == null ? "" : data;
                            if (row['useronlyscore'] == row['olduseronlyscore'])
                                return `<input class="textEdit upriority form-control text-dark" type="text" field="useronlyscore" value="${value}" contact="${row.contactc}" recordid="${row.recordid}" oldvalue="${value}" oldscore="${row.olduseronlyscore}" style="width: 100px;">`;
                            else
                                return `<input class="textEdit upriority form-control" type="text" value="${value}" field="useronlyscore" contact="${row.contactc}" recordid="${row.recordid}" oldvalue="${value}" oldscore="${row.olduseronlyscore}" style="width: 100px;">`;
                        }
                    },
                    { field: "contactc", label: gettext("Contact"), visible:false },
                    {field: "userscore", label: gettext("UPriority"), width: "120px", className: "rendered-input-cell", visible: false}
                ],
                custom_params_fun: undefined,
                custom_options: {
                    responsive: false,  //是否支持手機展開和隱藏列
                    scrollX: true,
                    row_nowrap: true,
                    autoWidth: false,
                    scrollResize: true,
                    scrollY: true,
                    drawCallback: function (settings) {
                        var rows = self.$refs.masterTable.datatable.rows().data().toArray();
                        var row_id = undefined;
                        if (self.currentMaster.hasOwnProperty('DT_RowId')) {
                            var selectedRows = rows.filter((row) => row.DT_RowId == self.currentMaster.DT_RowId);
                            if (selectedRows.length > 0)
                                row_id = selectedRows[0].DT_RowId;
                        }
                        self.$nextTick(function () {
                            if (row_id == undefined) {
                                var row_data = self.$refs.masterTable.datatable.row(':eq(0)', { page: 'current' }).data()
                                self.$refs.masterTable.datatable.row(':eq(0)', { page: 'current' }).select();
                                $("#" + row_data.DT_RowId)[0].scrollIntoView(false);
                            }
                            else {
                                self.$refs.masterTable.datatable.row('#' + row_id, { page: 'current' }).select();
                                $("#" + row_id)[0].scrollIntoView(false);
                            }
                        });
                    },
                    select: {
                        style: 'single',
                        info: false,
                        //selector: "tr>td:nth-child(1), tr>td:nth-child(2), tr>td:nth-child(3), tr>td:nth-child(4)",
                    }
                },
                datasource: "/schedule/subproject_table",
                orderBy: [['score', 'desc']],
                select_row: self.masterTableSelected,
                handle_response_fun: self.masterHandleResponse
            },
            detailTable: {
                columns: [
                    { field: "sessionid", label: gettext("SessionId"), width: "100px" },
                    { field: "sdesp", label: gettext("Description") },
                    { field: "contact", label: gettext("Contact"), width: "60px" },
                    {
                        field: "allcontact", label: gettext("AllContact"), width: "70px", render: function (data, type, full, meta) {
                            data = data ? data : "";
                            return "<label title='" + data + "' class='text-truncate d-inline-block' style='width:70px;text-decoration: none;'>" + data + "</label>";
                        }
                    },
                    { field: "progress", label: gettext("Progress"), width: "70px" },
                    { field: "taskqty", label: gettext("Task Qty"), width: "70px" },
                    { field: "planbdate", label: gettext("PlanBDate"), render: DateRender, width: "90px" },
                    { field: "planedate", label: gettext("PlanEDate"), render: DateRender, width: "90px" },
                    {
                        field: "udf04", label: gettext("FIFO"), width: "40px", render: function (data, type, row) {
                            var value = data == null ? "Y" : data.trim();
                            return `<label class="custom-control custom-checkbox">
                                    <input type="checkbox" class="fifoCheck custom-control-input control" {0} inc_id="${row.inc_id}" oldvalue="${value}">
                                    <span class="custom-control-label">
                                    </span>
                                    </label>`.format(value == "Y" ? "checked" : "");
                        }
                    },
                    {
                        field: "capacity", label: gettext("Capacity"), className: "rendered-input-cell", width: "70px",
                        render: function (data, type, row) {
                            var value = data == null ? "" : data;
                            if (row['capacity'] == row['oldcapacity'])
                                return `<input class="textEdit capacity form-control text-dark" type="text" value="${value}" inc_id="${row.inc_id}" oldvalue="${value}" oldcapacity="${row.oldcapacity}" style="width: 70px;">`;
                            else
                                return `<input class="textEdit capacity form-control" type="text" value="${value}" inc_id="${row.inc_id}" oldvalue="${value}" oldcapacity="${row.oldcapacity}" style="width: 70px;">`;
                        }
                    },                    
                    {
                        field: "weight", label: gettext("Priority"), className: "rendered-input-cell", width: "70px",
                        render: function (data, type, row) {
                            var value = data == null ? "" : data;
                            if (row['weight'] == row['oldweight'])
                                return `<input class="textEdit weight form-control text-dark" type="text" value="${value}" inc_id="${row.inc_id}" oldvalue="${value}" oldweight="${row.oldweight}" style="width: 70px;">`;
                            else
                                return `<input class="textEdit weight form-control" type="text" value="${value}" inc_id="${row.inc_id}" oldvalue="${value}" oldweight="${row.oldweight}" style="width: 70px;">`;
                        }
                    },
                    {
                        field: "useronlyweight", label: gettext("UPriority"), className: "rendered-input-cell", width: "85px", visible: false,
                        render: function (data, type, row) {
                            var value = data == null ? "" : data;
                            if (row['useronlyweight'] == row['olduseronlyweight'])
                                return `<input class="textEdit uweight form-control text-dark" type="text" value="${value}" field="useronlyweight" contact="${row.contactc}" sessionid="${row.sessionid}" oldvalue="${value}" oldweight="${row.useronlyweight}" style="width: 85px;">`;
                            else
                                return `<input class="textEdit uweight form-control" type="text" value="${value}" field="useronlyweight" contact="${row.contactc}" sessionid="${row.sessionid}" oldvalue="${value}" oldweight="${row.useronlyweight}" style="width: 85px;">`;
                        }
                    },
                    { field: "tid", label: gettext("tid"), width: "100px", visible: false },
                    { field: "contactc", label: gettext("Contact"), visible:false },
                    { field: "userweight", label: gettext("UPriority"), className: "rendered-input-cell", width: "85px", visible: false}
                ],
                custom_params_fun: undefined,
                custom_options: {
                    responsive: false,  //是否支持手機展開和隱藏列
                    scrollX: true,
                    row_nowrap: true,
                    autoWidth: false,
                    scrollResize: true,
                    scrollY: true,
                    select: true,
                    deferLoading: 0,
                    columnDefs: [
                        { orderDataType: 'dom-text-numeric', "targets": 7 },
                    ],
                    select: {
                        style: 'single',
                    },
                    drawCallback: function (settings) {
                        self.$nextTick(function () {
                            self.$refs.detailTable.datatable.row(':eq(0)', { page: 'current' }).select();
                        });
                    },
                },
                select_row: self.detailTableSelected,
                dbclick:self.detailTableDbclick,
                datasource: "/schedule/session_table",
                orderBy: [['weight', 'desc'], ['tid', 'asc']],
                handle_response_fun: self.detailHandleResponse
            },
            detailFilter: {
                contact: "",
                progress: "I",
                desc: ""
            },
            masterSearch: {
                isPersonSearch: false,
                contact: "",
                recordId: "",
                projectName: ""
            },
            scheduleParams: {
                group1: [
                    { nfield: "Project Priority Base", fvalue: 3000 },
                    { nfield: "Day Capacity", fvalue: 3 },
                    { nfield: "Week are Scheduled", fvalue: "0111111" },
                ],
                group2: [
                    { nfield: "Raised by Robert", fvalue: 230 },
                    { nfield: "Raised by Sing", fvalue: 220 },
                    { nfield: "Meeting P", fvalue: 200 },
                    { nfield: "External Request", fvalue: 150 },
                    { nfield: "Fixed Day", fvalue: 1000 }
                ],
                group3: [
                    { nfield: "Class(1)", fvalue: 200 },
                    { nfield: "Priority(8889)", fvalue: 150 },
                    { nfield: "Priority(8888)", fvalue: 100 },
                    { nfield: "Priority(888)", fvalue: 50 },
                ]
            },
            scheduleParamsOther: {
                categoryCapacity: [
                    { nfield: "Raised by Robert Capacity", fvalue: 2 },
                    { nfield: "Raised by Sing Capacity", fvalue: 3 },
                    { nfield: "Meeting P Capacity", fvalue: 1 },
                    { nfield: "External Request Capacity", fvalue: 1 },
                    { nfield: "Fixed Day Capacity", fvalue: 1 }
                ]
            },
            scheduleParamsScenario: undefined,
            allContacts: [],
            currentMaster: {},
            currentDetail: {},
            loginUserName:window.get_login_name(),
            schParamHistoryList: [], // 用於存儲歴史記錄列錶
            selectedSchParamHistory: null, // 當前選擇的歴史記錄   
            lang_code_en: true,         
        }
    },
    methods: {
        init() {
            window.CommonData.PartUserNames.then((result) => {
                this.allContacts = result.data;
                this.$nextTick(function () {
                    $(".status_select").selectpicker('refresh');
                });
            });
        },        
        masterTableSelected(e, dt, type, indexes) {
            if (e.type === "select") {
                this.currentMaster = this.$refs.masterTable.datatable.row($(e.currentTarget).find("tr").eq(indexes[0] + 1)).data();
                this.getDetailData();
            }
        },
        detailTableSelected(e, dt, type, indexes) {
            if (e.type === "select") {
                this.currentDetail = this.$refs.detailTable.datatable.row($(e.currentTarget).find("tr").eq(indexes[0] + 1)).data();
            }
        },
        detailTableDbclick(data) {
            var recordId = this.currentMaster.recordid;
            var sessionId = data.sessionid;
            setTimeout(() => {
                window.open(`/devplat/sessions?recordid=${recordId}&menu_id=mi_${sessionId}#Session_Tasks`, "sch_session_tasks");   
            });             
        },
        detailHandleResponse(data) {
            for (var row of data) {
                row.oldweight = row.weight;
                row.olduseronlyweight = row.useronlyweight;
                row.oldcapacity = row.capacity;
                row['DT_RowId'] = `master_rowid_${row.inc_id}`
            }
            return data;
        },
        masterHandleResponse(data) {
            for (var row of data) {
                row.oldscore = row.score;
                row.olduseronlyscore = row.useronlyscore;
                row['DT_RowId'] = `master_rowid_${row.inc_id}`
            }
            return data;
        },
        getMasterChanged() {
            var priorityDomList = $(this.$refs.masterTable.table).find(".textEdit.priority");
            var changeList = { priority: [], upriority: [] }
            for (var dom of priorityDomList) {
                if ($(dom).val() != $(dom).attr("oldvalue")) {
                    changeList.priority.push({ inc_id: $(dom).attr("inc_id"), score: $(dom).val() })
                }
            }

            if (this.masterSearch.isPersonSearch) {
                var upriorityDomList = $(this.$refs.masterTable.table).find(".textEdit.upriority");
                for (var dom of upriorityDomList) {
                    if ($(dom).val() != $(dom).attr("oldvalue")) {
                        var recordid = $(dom).attr("recordid");
                        var contact = $(dom).attr("contact")
                        changeList.upriority.push({ contact: contact, recordid: recordid, score: $(dom).val() })
                    }
                }
            }
            return changeList;
        },
        getDetailChanged() {
            var domList = $(this.$refs.detailTable.table).find(".textEdit.weight");
            var fifoDomList = $(this.$refs.detailTable.table).find(".fifoCheck");
            var capacityDomList = $(this.$refs.detailTable.table).find(".textEdit.capacity");
            var changeObject = { weight: [], uweight: [] };
            var changeWeightObject = {}
            for (var dom of domList) {
                if ($(dom).val() != $(dom).attr("oldvalue")) {
                    var priorityValue = $(dom).val();
                    var fifoValue = $(dom).closest("tr").find(".fifoCheck").prop("checked") ? "Y" : "N";
                    var capacityValue = $(dom).closest("tr").find(".capacity").val();
                    var inc_id = $(dom).attr("inc_id");
                    changeWeightObject[inc_id] = { inc_id: inc_id, fifo: fifoValue, weight: priorityValue, capacity:capacityValue };
                }
            }
            for (var dom of fifoDomList) {
                var fifoValue = $(dom).prop("checked") ? "Y" : "N";
                if (fifoValue != $(dom).attr("oldvalue")) {
                    var priorityValue = $(dom).closest("tr").find(".weight").val();
                    var capacityValue = $(dom).closest("tr").find(".capacity").val();
                    var inc_id = $(dom).attr("inc_id");
                    changeWeightObject[inc_id] = { inc_id: inc_id, fifo: fifoValue, weight: priorityValue,capacity: capacityValue };
                }
            }
            for (var dom of capacityDomList) {
                if ($(dom).val() != $(dom).attr("oldvalue")) {
                    var capacityValue = $(dom).val();
                    var priorityValue = $(dom).closest("tr").find(".weight").val();
                    var fifoValue = $(dom).closest("tr").find(".fifoCheck").prop("checked") ? "Y" : "N";
                    var inc_id = $(dom).attr("inc_id");
                    changeWeightObject[inc_id] = { inc_id: inc_id, fifo: fifoValue, weight: priorityValue, capacity: capacityValue};
                }
            }
            
            changeObject.weight = Object.values(changeWeightObject);
            if (this.masterSearch.isPersonSearch) {
                var uweightDomList = $(this.$refs.detailTable.table).find(".textEdit.uweight");
                for (var dom of uweightDomList) {
                    if ($(dom).val() != $(dom).attr("oldvalue")) {
                        var priorityValue = $(dom).val();
                        var contact = $(dom).attr("contact");
                        var sessionid = $(dom).attr("sessionid");
                        changeObject.uweight.push({ contact: contact, sessionid: sessionid, weight: $(dom).val() });
                    }
                }
            }
            return changeObject;
        },
        refreshDataTable(tableObj) {
            var table = tableObj.datatable;
            var pageInfo = table.page.info();
            var currentPage = pageInfo.page;
            this.$nextTick(() => {
                table.page(currentPage).draw(false);
            });
        },
        masterClear() {
            for (var [key, value] of Object.entries(this.masterSearch)) {
                this.masterSearch[key] = "";
            }
            this.$nextTick(() => {
                $(".status_select").selectpicker('refresh');
            })
        },
        detailClear() {
            for (var [key, value] of Object.entries(this.detailFilter)) {
                this.detailFilter[key] = "";
            }
            this.$nextTick(function () {
                $(".status_select").selectpicker('refresh');
            });
        },
        getWeekAreScheduledDay(index) {
            var weekAreScheduled = this.scheduleParams.group1[2].fvalue;
            if (index < weekAreScheduled.length)
                return parseInt(weekAreScheduled.charAt(index)) == 1
            else
                return false
        },
        selectWeekAreScheduledDay(e, index) {
            e.preventDefault();
            var weekAreScheduled = this.scheduleParams.group1[2].fvalue
            if (index < weekAreScheduled.length) {
                var arr = weekAreScheduled.split("");
                arr[index] = parseInt(weekAreScheduled.charAt(index)) == 1 ? "0" : "1"
                this.scheduleParams.group1[2].fvalue = arr.join("");
            }
            e.currentTarget.blur();
        },
        submitSchParamsHistoryListForm(event) {
            var self = this;
            return new Promise((resolve, reject)=>{
                if (self.selectedSchParamHistory !== null)
                    resolve(true);
                else {
                    reject(false);
                }
            });
        },
        selectSchParamsHisotry() {
            var self = this;
            return new Promise((resolve, reject)=>{
                this.selectedSchParamHistory = null;
                this.$refs.schParamsHistoryListForm.$refs.modal.show();            
                $("#schParamsHistoryListForm>.modal").off("hidden.bs.modal");
                $("#schParamsHistoryListForm>.modal").on("hidden.bs.modal", function(e){
                    reject(true);
                });
                $("#schParamsHistoryListForm button[type='submit']").off("click");
                $("#schParamsHistoryListForm button[type='submit']").on("click", function(e){
                    if (self.selectedSchParamHistory !== null)
                        resolve(true);
                    else {
                        alert(gettext("Please select history record!"))
                    }                    
                });
            });
        },
        handleSplitterDoubleClick() {
            this.$forceUpdate();
            setTimeout(() => {
                this.getPriorityHeight();
            }, 200);
        },
        getPriorityHeight() {
            const mediaQuery = window.matchMedia('(min-width: 768px) and (max-width: 991.98px)');
            $("div.splitpanes").height(mediaQuery.matches ? '900px' : '100%');

            var splitTopPane = $('div.splitpanes>.topPane').height();
            var topPaneHeaderHeight = $('.topPane .masterWrapper>.row').height();
            var topPaneDataTablesHeadHeight = $('.topPane .dataTables_scrollHead').height();
            
            var splitBottomPane = $('div.splitpanes>.bottomPane').height();
            var bottomPaneHeaderHeight = $('.bottomPane .detail_card .card-body>.row').height();
            var bottomPaneDataTablesHeadHeight = $('.bottomPane .dataTables_scrollHead').height();
            
            $('.topPane .LPDataTable .dataTables_scrollBody').height(splitTopPane - topPaneHeaderHeight - 24 - topPaneDataTablesHeadHeight);
            $('.bottomPane .LPDataTable .dataTables_scrollBody').height(splitBottomPane - bottomPaneHeaderHeight - 24 - bottomPaneDataTablesHeadHeight);
        },
        // 獲取當前語言
        get_lang_code() {
            if($("#curr_language_code").val() !== "en") {
                this.lang_code_en = false;
            }
        },
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.getPriorityHeight);
        const splitter = document.querySelector('.splitpanes__splitter');
        splitter.removeEventListener('dblclick', this.handleSplitterDoubleClick);
    },
}
</script>
<style>.page-inner {
    padding: 0px !important;
}

.page-inner .page-title-bar {
    margin: 0px !important;
}

.page-inner .card .card-body:not(.card_para_body) {
    padding-top: 0px !important;
}

.main_card>.card-body {
    padding-left: 0px !important;
    padding-right: 0px !important;
    padding-bottom: 0px !important;
}

.main_card {
    background-color: inherit !important;
}

.schparam_container {
    overflow: auto;
    height: calc(100% - 70px);
}

.params_select .custom-select {
    padding-top: 4px !important;
    padding-bottom: 4px !important;
    height: 31px !important;
}

.WeekAreScheduled .badge {
    font-size: 13px !important;
    background-color: #cbdeff !important;
}

.WeekAreScheduled .badge.active {
    color: rgb(255 0 0 / 70%);
}

.schparam_container .schedule_scenario {
    color: rgb(255 0 0 / 70%);
}
#scheduleResult>.card {
    margin-bottom: 0px !important;
}
#priorityTabContent .LPDataTable table.dataTable>thead>tr>th {
    font-size: 14px;
    font-weight: 800 !important;
}
#schParamsHistoryListForm .list-group-item.active {
    background-color: #346cb0;
    color:white;
}

#schParamsHistoryListForm .modal-body {
    padding-left: 0px !important;
    padding-right: 0px !important;
    height: 40vh;
}
#schParamsHistoryListForm .list-group {
    box-shadow:none !important;
}
</style>
