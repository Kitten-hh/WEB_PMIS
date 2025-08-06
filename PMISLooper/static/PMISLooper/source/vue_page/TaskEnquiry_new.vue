<template>
    <div class="page-inner pt-2 pb-3 taskEnquiryPage">
        <div class="d-flex justify-content-between align-items-center mb-2">
            <h6 class="title mt-2">任務查詢</h6>
            <!-- 任務查詢-f -->
            <button @click="showModal" class="btn nav-link"><span class="oi oi-magnifying-glass"></span></button>
        </div>
        <div class="card-deck-xl mb-3">
            <div class="card card-body px-1 px-sm-3 px-xl-1 py-2 col-12 col-xl-7 col-xxxl-7 enquiryCard">
                <div class="enquiryCondition row mx-0">
                    <div class="form-group col-12 col-xs col-sm-22 col-xl-2 col-xxxl-22 order-first order-xl-0">
                        <label class="col-form-label caption col-auto pl-0" for="">工程編號</label>
                        <!-- 工程編號-f -->
                        <input type="text" class="form-control form-control-sm col" v-model="searchObj.pid">
                    </div>
                    <div class="form-group col-12 col-xs-6 col-sm-39 col-xl-5 col-xxxl-39">
                        <label class="col-form-label caption col-auto pl-0">類別編號</label>
                        <!-- 類別編號-f -->
                        <div class="input-group input-group-alt input-group-sm m-0">
                            <input type="text" class="form-control form-control-sm col" v-model="searchObj.tid_from" />
                            <div class="input-group-append">
                                <span class="input-group-text custom-text">到</span>
                                <!-- 到-f -->
                            </div>
                            <input type="text" class="form-control form-control-sm col" v-model="searchObj.tid_to" />
                        </div>
                    </div>
                    <div class="form-group col-12 col-xs-6 col-sm-39 col-xl-5 col-xxxl-39">
                        <label class="col-form-label caption col-auto pl-0">任務編號</label>
                        <!-- 任務編號-f -->
                        <div class="input-group input-group-alt input-group-sm m-0">
                            <input type="text" class="form-control form-control-sm col" v-model="searchObj.taskid_from" />
                            <div class="input-group-append">
                                <span class="input-group-text custom-text">到</span>
                                <!-- 到-f -->
                            </div>
                            <input type="text" class="form-control form-control-sm col" v-model="searchObj.taskid_to" />
                        </div>
                    </div>
                    <div class="form-group col-12 col-sm-6 col-xxxl-6 order-xxxxl-0">
                        <label class="col-form-label caption col-auto pl-0">實際開始</label>
                        <!-- 實際開始-f -->
                        <div class="input-group input-group-alt input-group-sm m-0">
                            <LPFlatpickerDate :small="true" v-model="searchObj.bdate_from"/>
                            <div class="input-group-append">
                                <span class="input-group-text custom-text">到</span> <!-- 到-f -->
                            </div>
                            <LPFlatpickerDate :small="true" v-model="searchObj.bdate_to"/>
                        </div>
                    </div>
                    <div class="form-group col-12 col-sm-6 col-xxxl-6 order-1 order-sm-0 order-xxxxl-0">
                        <label class="col-form-label caption col-auto pl-0">計劃開始</label>
                        <!-- 計劃開始-f -->
                        <div class="input-group input-group-alt input-group-sm m-0">
                            <LPFlatpickerDate :small="true" v-model="searchObj.planbdate_from"/>
                            <div class="input-group-append">
                                <span class="input-group-text custom-text">到</span> <!-- 到-f -->
                            </div>
                            <LPFlatpickerDate :small="true" v-model="searchObj.planbdate_to"/>
                        </div>
                    </div>
                    <div class="form-group col-12 col-sm-6 col-xxxl-6 order-xxxl-0">
                        <label class="col-form-label caption col-auto pl-0">實際結束</label>
                        <!-- 實際結束-f -->
                        <div class="input-group input-group-alt input-group-sm m-0">
                            <LPFlatpickerDate :small="true" v-model="searchObj.edate_from"/>
                            <div class="input-group-append">
                                <span class="input-group-text custom-text">到</span> <!-- 到-f -->
                            </div>
                            <LPFlatpickerDate :small="true" v-model="searchObj.edate_to"/>
                        </div>
                    </div>
                    <div class="form-group col-12 col-sm-6 col-xxxl-6 order-1 order-sm-0 order-xxxl-0">
                        <label class="col-form-label caption col-auto pl-0">計劃結束</label>
                        <!-- 計劃結束-f -->
                        <div class="input-group input-group-alt input-group-sm m-0">
                            <LPFlatpickerDate :small="true" v-model="searchObj.planedate_from"/>
                            <div class="input-group-append">
                                <span class="input-group-text custom-text">到</span> <!-- 到-f -->
                            </div>
                            <LPFlatpickerDate :small="true" v-model="searchObj.planedate_to"/>
                        </div>
                    </div>
                    <div class="form-group col-12 col-sm-6 col-xxxl-6 order-1 order-sm-0 order-xxxl-0">
                        <label class="col-form-label caption col-auto pl-0">工程描述</label>
                        <!-- 工程描述-f -->
                        <input type="text" class="form-control form-control-sm col" v-model="searchObj.sdesp" />
                    </div>
                    <div class="form-group contactWrap col-12 col-xs-3 col-sm-3 col_minWidth col-xxxl-3 order-first order-sm-0">
                        <label class="col-form-label caption col-auto pl-0">聯繫人</label>
                        <!-- 聯繫人-f -->
                        <input type="text" class="form-control form-control-sm col" v-model="searchObj.contact" />
                    </div>
                    <div class="form-group col-12 col-xs-6 col-sm-3 order-2 order-sm-0 order-xxxl-0 col_minWidth col-xxxl-3">
                        <label class="col-form-label caption col-auto pl-0">優先級</label>
                        <!-- 優先級-f -->
                        <input type="text" class="form-control form-control-sm col" v-model="searchObj.priority" />
                    </div>
                    <div class="form-group col-12 col-sm-6 col-xxxl-6 order-1 order-sm-0 order-xxxl-0">
                        <label class="col-form-label caption col-auto pl-0">任務描述</label>
                        <!-- 任務描述-f -->
                        <input type="text" class="form-control form-control-sm col" v-model="searchObj.task" />
                    </div>
                    <div class="form-group progressWrap col-12 col-xs-3 col-sm-3 col_minWidth col-xxxl-3 order-first order-sm-0 order-xxxl-0">
                        <label class="col-form-label caption col-auto pl-0">進度</label>
                        <!-- 進度-f -->
                        <input type="text" class="form-control form-control-sm col" v-model="searchObj.progress" />
                    </div>
                    <div class="form-group col-12 col-xs-6 col-sm-3 order-2 order-sm-0 order-xxl-1 order-xxxl-0 col_minWidth col-xxxl-3">
                        <label class="col-form-label caption col-auto pl-0">版本號</label>
                        <!-- 版本號-f -->
                        <input type="text" class="form-control form-control-sm col" v-model="searchObj.editionid" />
                    </div>
                </div>
                <hr class="my-2 d-xxxl-none">
                <div class="el-example d-flex searchBtnTools">
                    <button type="button" class="btn btn-sm btn-secondary btnClear" @click="searchObj = {}">清除條件</button>
                    <!-- 清除條件-f -->
                    <button type="button" class="btn btn-sm btn-primary btnEnquiry" @click="conditionQueryBtnClick">查詢</button><!-- 查詢-f -->
                    <button type="button" class="btn btn-sm btn-success">工程狀態圖</button><!-- 工程狀態圖-f -->
                    <button type="button" class="btn btn-sm btn-success">查詢SQL</button><!-- 查詢SQL-f -->
                    <button type="button" class="btn btn-sm btn-success">任務重排</button><!-- 任務重排-f -->
                    <button type="button" class="btn btn-sm btn-success">常用查詢</button><!-- 常用查詢-f -->
                </div>
            </div>
            <div class="card col-12 col-xl-5 col-xxxl-5 px-0 conditionCard">
                <div class="card-header d-flex align-items-center py-2">
                    <div class="input-group input-group-alt input-group-sm">
                        <input type="text" v-model="loginUser" @keypress="searchRecordFilter" class="form-control form-control-sm">
                        <div class="input-group-append">
                            <button @click="searchRecordFilter" class="btn btn-sm mr-2 btn-secondary no-caret h-100"><span class="oi oi-magnifying-glass"></span></button>
                        </div>
                    </div>
                    <label class="custom-control custom-checkbox m-0">
                        <input type="checkbox" id="IsDaily" class="custom-control-input control" checked="checked">
                        <span class="custom-control-label text-nowrap">每日</span><!-- 每日的-f -->
                    </label>
                </div>
                <div class="card-body py-0">
                    <LPDataTable ref="conditionTable" :datasource="taskTableSource" :columns="conditionColumns" :paging_inline="true"
                        :custom_options="ConditiontaskOptions" :searching="false" :paging="false" @on_dbclick="searchTask"
                        :custom_params_fun="undefined" />
                </div>
            </div>
        </div>
        <div class="card px-2 pb-2 mb-0">
            <LPDataTable ref="taskTable" :datasource="taskData" :columns="taskColumns" :custom_options="taskOptions"
                :searching="false" :paging="false" @on_dbclick="taskTableDblClick" :custom_params_fun="masterParamsFun" />
        </div>
    </div>
    <AdvancedSearchDlg ref="search" :masterColumns="taskColumns" @search="search" />
</template>
<script>
import axios from "axios";
import LPDataTable, { DateRender } from "@components/looper/tables/LPDataTable.vue";
import LPModal from "@components/looper/layout/LPModal.vue";
import AdvancedSearchDlg from "./AdvancedSearchDlg.vue";
import LPFlatpickerDate from "@components/looper/forms/LPFlatpickerDate.vue";
export default {
    name: "TaskEnquiry_vueFrm",
    components: {
        LPDataTable,
        LPModal,
        AdvancedSearchDlg,
        LPFlatpickerDate
    },
    data() {
        return {
            cid: '',
            isq: 1,
            loginUser: get_username(),
            taskData: [],
            taskColumns: [
                { field: "inc_id", label: this.$t("inc_id"), visible: false },
                { field: "pid", label: "工程編號" }, //工程編號
                { field: "tid", label: "類別編號" }, //類別編號
                { field: "taskid", label: "任務編號" }, //任務編號
                { field: "udf04", label: "窗口名稱" }, //窗口名稱
                { field: "editionid", label: "版本號" },//版本號
                { field: "task", label: "任務描述", width: '250px' }, //任務描述
                { field: "contact", label: "聯繫人" }, //聯繫人
                { field: "progress", label: "進度" }, //進度
                { field: "planbdate", label: "計劃開始時間", render: DateRender }, //計劃開始時間
                { field: "planedate", label: "計劃結束時間", render: DateRender }, //計劃結束時間
                { field: "priority", label: "優先級" }, //優先級
                { field: "clazz", label: "分類" }, //分類
                { field: "calpriority", label: "計算的優先級" }, //計算的優先級
                { field: "schpriority", label: "排期優先級" }, //排期優先級
                // { field: "qutday", label: this.$t("Qut day") }, //脫期天數
                { field: "quantity", label: "數量" }, //數量
                { field: "tasktype", label: "任務分類" }, //任務分類
                { field: "realtasktype", label: "任務分類編號" }, //任務分類編號
                { field: "score", label: "分數" }, //分數
                { field: "relationgoalid", label: "RelationGoalId" }, //RelationGoalId
                { field: "dayjob", label: "當天任務" }, //當天任務
                { field: "atime", label: "實際天數" }, //實際天數
                { field: "remark", label: "備註" }, //備註
                { field: "relationid", label: "關聯任務" }, //關聯任務
                { field: "reference", label: "參考" }, //參考
                { field: "charge", label: "收費" }, //收費
                { field: "requestdate", label: "需求日期", render: DateRender }, //需求日期
                { field: "createdate", label: "創建日期", render: DateRender }, //創建日期
                { field: "cycletask", label: "循環任務" }, //循環任務
                { field: "r_flag", label: "已讀" }, //已讀
                { field: "taskno", label: "任務" }, // 任務
                { field: "etime", label: "計劃天數" }, // 計劃天數
                { field: "bdate", label: "實際開始", render: DateRender }, // 實際開始
                { field: "edate", label: "實際結束", render: DateRender }, // 實際結束
                { field: "subtasktype", label: "任務子分類" }, // 任務子分類
                { field: "diff", label: "難度" }, //難度
                { field: "docpath", label: "關聯文檔" }, //關聯文檔
                { field: "udf02", label: "關聯進度" }, //關聯進度
                { field: "flowchartno", label: "流程編號" }, //流程編號
                { field: "revisedby", label: "修改人" }, //修改人
                { field: "udf10", label: "樣板單別" }, //樣板單別
                { field: "udf01", label: "樣板號" }, //樣板號
                { field: "sprogress", label: "模塊進度" }, //模塊進度
                { field: "scontact", label: "模塊聯繫人" }, //模塊聯繫人
                { field: "hoperation", label: "操作" }, //操作
                { field: "subprojectid", label: "序號" }, //序號
                { field: "projectid", label: "工程編號" }, //工程編號
                { field: "projectname", label: "工程名稱" }, //工程編號
            ],
            conditionColumns: [
                { field: 'qf012', label: "排序" }, //"排序"
                { field: 'qf003', label: "條件名稱", width: "300px" }, //"條件名稱"
                { field: 'qt002', label: "類別" }, //"類別"
                { field: 'qf008', label: "關鍵字" }, //"關鍵字"
                { field: 'qf023', label: "客戶" }, //"客戶"
                { field: 'qf024', label: "查詢類型" }, //"查詢類型"
                {
                    field: 'qf020', label: "同步Calendar", className: 'text-center', render: (data) => {
                        return `<input type="checkbox" ${data === "Y" ? "checked" : ""} disabled/>`
                    }
                }, //"同步Calendar"
                { field: 'qf021', label: "Google日曆名稱首碼" }, //"Google日曆名稱首碼"
            ],
            taskOptions: {
                responsive: false,
                scrollY: "57vh",
                scrollX: true,
                processing: true,
                autoWidth: false,
                deferLoading: 0,
            },
            ConditiontaskOptions: {
                responsive: false,
                scrollY: true,
                scrollX: true,
                processing: true,
                autoWidth: false,
                deferLoading: 0,
            },
            filterQueryData: [],
            searchObj: {},
            masterParamsFun: undefined,
            taskTableSource: [],
        }
    },
    watch: {
        "searchObj.tid_from"(v) {
            this.searchObj.tid_to = v;
        },
        "searchObj.taskid_from"(v) {
            this.searchObj.taskid_to = v;
        },
    },
    created() {
        loadCss("/static/BaseApp/vendor/jquery_contextmenu/jquery.contextMenu.min.css");
        loadJs(["/static/BaseApp/vendor/jquery_contextmenu/jquery.ui.position.min.js"], true);
        loadJs(["/static/BaseApp/vendor/jquery_contextmenu/jquery.contextMenu.min.js"], true);
    },
    mounted() {
        var self = this;
        if (this.loginUser == undefined || this.loginUser == "")
            this.loginUser == "sing"
        this.searchRecordFilter();
        $.contextMenu({
            selector: '.contextMenu',
            callback: function (key, options) {
                if (key == "analysisQuestion") {
                    self.analysisQuestion(options.$trigger)
                }
                if (key == "toFaqAnalysisPage") {
                    self.toFaqAnalysisPage(options.$trigger)
                }
            },
            items: {
                "analysisQuestion": { name: gettext(self.$t('analysis question')) }, //分析問題-f
                "toFaqAnalysisPage": { name: gettext(self.$t('Visit the FAQ analysis page')) }, //訪問FAQ分析頁面-f
            }
        });
    },
    methods: {
        showModal() {
            this.$refs.search.event.showModal()
        },
        hideModal() {
            this.$refs.search.event.hideModal()
        },
        search(filter) {
            console.log(filter);;
            var table = this.$refs.taskTable.datatable
            this.masterParamsFun = () => { return JSON.stringify({ attach_query: filter }) };
            this.$nextTick(function () {
                table.ajax.url("/looper/task/enquiry/task_table").load()
                this.$refs.taskTable.datatable.search('').draw();
            })
            // var search = {}
            // for (let rule of filter.rules) {
            //   search[rule['field']] = rule['value']
            // }
            // axios.get("/looper/task/enquiry/condition_search", { params: { param: search } })
            //   .then(res => {
            //     if (res.data.status)
            //       this.$refs.taskTable.datatable.clear().rows.add(res.data.data || []).draw();
            //       this.hideModal()
            //   }).catch(err => { console.log(err) })
        },
        submitQuestionType() {
            window.location.href = `http://${window.location.host}/zh-hans/looper/task/faqAnalysisTask?cid=${this.cid}&isq=${this.isq}`
        },
        analysisQuestion(d) {
            console.log(d)
        },
        toFaqAnalysisPage(d) {
            var key = d.find(".paramkey").html();
            axios.get("/looper/task/enquiry/get_param_for_qf025?qf025=" + key)
                .then(res => {
                    if (res.data.status) {
                        var data = res.data.data;
                        this.cid = `${data.qf001};${data.qf002};${data.qf006}`;
                        this.$refs.selectQuestionTypeModal.show();
                    }
                }).catch(err => { console.log(err) })
        },
        conditionQueryBtnClick() {
            axios.get("/looper/task/enquiry/condition_search", { params: { param: this.searchObj } })
                .then(res => {
                    if (res.data.status)
                        this.$refs.taskTable.datatable.clear().rows.add(res.data.data || []).draw();
                }).catch(err => { console.log(err) })
        },
        taskTableDblClick(data) {
            init_task(data.inc_id)
        },
        searchTask(data) {
            // $event.preventDefault();
            // $event.stopPropagation();
            axios.get("/PMIS/task/search_with_queryid/" + data.qf025)
                .then(res => {
                    if (res.data.status)
                        this.$refs.taskTable.datatable.clear().rows.add(res.data.data || []).draw();
                }).catch(err => { console.log(err) })
        },
        searchRecordFilter() {
            var is_dialy = $("#IsDaily").is(":checked") ? "Y" : "N";
            axios.get("/PMIS/query/search", { params: { filter: this.loginUser, is_dialy: is_dialy } })
                .then(res => {
                    this.$refs.conditionTable.datatable.clear().rows.add(res.data.data || []).draw();
                }).catch(err => { console.log(err) })
        },
    },
};
</script>
<style>
.context-menu {
    position: fixed;
    background-color: #fff;
    border: 1px solid #ccc;
    padding: 0.5rem;
    list-style: none;
    z-index: 999;
}
</style>