<template>
  <div :class="{ 'PmsSessionManager page': true, 'lang_en': lang_code_en }">
    <div :class="['card sessionSearchCard', isMobile ? 'card-expansion-item expanded' : 'mb-0']">
      <div id="sessionSearchCollapse" class="collapse show" aria-labelledby="sessionSearchHeading">
          <div class="card-body search-scope pb-0 d-flex flex-wrap">
            <div class="form-group col-sm-6 col-md-6 col-lg-3 col-xl-2">
              <label class="col-form-label caption col-auto pl-0">{{ $t("Record ID") }}</label>
              <input class="form-control col" v-model="recordID">
            </div>
            <div class="form-group col-sm-6 col-md-6 col-lg-3 col-xl-2">
              <label class="col-form-label caption col-auto pl-0">{{ $t("Contact") }}</label>
              <select class="col select2-contact noFirstVal">
                <option v-for="(c, key) in contactOptions" :key="key" :value="c">{{ c }}</option>
              </select>
            </div>
            <div class="form-group col-sm col-md col-xl-4">
              <label class="col-form-label caption col-auto pl-0">{{ $t("All Contact") }}</label>
              <select multiple class="col select2-contact-mul noFirstVal">
                <option v-for="(c, key) in contactOptions" :key="key" :value="c">{{ c }}</option>
              </select>
            </div>
            <div class="form-group col-auto">
              <button class="btn btn-primary btn_search mr-2" @click="queryClickHandler">
                <i class="oi oi-magnifying-glass d-xl-none"></i>
                <span class="d-none d-xl-inline-block">{{ $t("Search") }}</span>
              </button>
              <button class="btn btn-secondary btn_clear" @click="clearHandler">
                <i class="fa fa-broom d-xl-none"></i>
                <span class="d-none d-xl-inline-block">{{ $t("Clear") }}</span>
              </button>
            </div>
          </div>
      </div>
      <div v-if="isMobile" class="card-header border-0 p-2" id="sessionSearchHeading">
        <button class="btn btn-reset" data-toggle="collapse"
          data-target="#sessionSearchCollapse" aria-expanded="true"
          aria-controls="sessionSearchCollapse"><span class="collapse-indicator">
            <i class="fa fa-fw fa-chevron-down"></i>
          </span></button>
      </div>
    </div>

    <div class="page-inner">
      <div class="topPane card cardShadow">
        <LPTreegrid ref="sessionTable" :datasource="sessionDataSource" :columns="sessionColumns" idField='sessionid'
          parentIdField='parentid' :custom_options="sessionOption" />
      </div>
      <div class="bottomPane card cardShadow detailInfo mb-0">
        <ul class="nav nav-tabs skinableNavTab">
          <li class="nav-item">
            <a class="nav-link show active" data-toggle="tab" href="#task-list">{{ $t("Task list") }}</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" data-toggle="tab" href="#task-list-all">{{ $t("Task list(All)") }}</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" id="tab_tasks" data-toggle="tab" href="#top-task">{{ $t("Prompt Tasks") }}</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" id="tab_sql" data-toggle="tab" href="#sql-script">{{ $t("SQL Script") }}</a>
          </li>
        </ul>
        <div  :class="{'card-body tab-content scrollbar': true, 'isSpecialTabCard': isTaskTabActive}">
          <fieldset class="col-12 taskSearch card-expansion-item expanded">
            <legend class="mb-0">
              <button class="btn btn-reset d-flex justify-content-between prevent-default pl-0" data-toggle="collapse"
                data-target="#sessionMgnTaskSearchCollapse" aria-expanded="true"
                aria-controls="sessionMgnTaskSearchCollapse"><span class="collapse-indicator"><i
                    class="fa fa-fw fa-caret-right mr-1"></i></span><span>{{ $t('Task Query') }}</span></button>
            </legend>
            <div id="sessionMgnTaskSearchCollapse" class="collapse show row search_list mx-0">
              <div class="form-group col-sm-6 col-md-4 col-lg-3" v-show="!isTaskTabActive">
                <label class="col-form-label caption col-auto pl-0">{{ $t("Progress") }}</label>
                <select v-model="selectedProgress" class="select2-progress noFirstVal">
                  <option v-for="(progress, key) in progressOptions" :key="key" :value="progress.data">
                    {{ progress.name }}
                  </option>
                </select>
              </div>
              <div class="form-group col-sm-6 col-md-4 col-lg-3" v-show="!isTaskTabActive">
                <label class="col-form-label caption col-auto pl-0">{{ $t("Priority") }}</label>
                <select v-model="selectedPriority" class="select2-priority noFirstVal">
                  <option v-for="(priority, key) in priorityOptions" :key="key" :value="priority">{{ priority }}
                  </option>
                </select>
              </div>
              <div class="form-group col-sm-6 col-md-4 col-lg-3" v-show="!isTaskTabActive">
                <label class="col-form-label caption col-auto pl-0">{{ $t("Class") }}</label>
                <select v-model="selectedClass" class="select2-class noFirstVal">
                  <option v-for="(classOption, key) in classOptions" :key="key" :value="classOption.value">
                    {{ classOption.label }}</option>
                </select>
              </div>
              <div class="form-group col-sm-6 col-md-8 col-lg-9" v-show="!isTaskTabActive">
                <label class="col-form-label caption col-auto pl-0">{{ $t("Task desc") }}</label>
                <input v-model="taskText" class="form-control" @keyup.enter="taskListChange">
              </div>
              <!--
              <div class="form-group d-flex col-sm-6 col-md-4 col-lg">
                <label class="col-form-label caption col-auto pl-0">{{ $t("Condition") }}:</label>
                <select class="col ml-2 select2-condition-task" v-model="selectedCondition">
                  <option v-for="(option, key) in conditions" :key="key" :value="option.inc_id">{{ option.desc }}</option>
                </select>
              </div>
              -->
              <div :class="['form-group col-sm-6 col-md-4 col-lg-3', isTaskTabActive ? 'isTaskTab' : '']">
                <label class="col-form-label caption col-auto pl-0">{{ $t("Contact") }}</label>
                <select class="col ml-2 select2-contact-task noFirstVal" v-model="selectedContact">
                  <option v-for="(c, key) in contactOptions" :key="key" :value="c">{{ c }}</option>
                </select>
              </div>
              <div class="form-group col-sm-6 col-md-4 col-lg-3">
                <label class="col-form-label caption col-auto pl-0">{{ $t("Record ID") }}</label>
                <input class="form-control" v-model="ai_recordID">
              </div>
              <div class="form-group col-sm-12 col-md-8 col-lg">
                <label class="col-form-label caption col-auto pl-0">{{ $t("Category") }}</label>
                <LPCombobox url='/looper/session_manager/get_category_data' ref="category_LPCasombobox"
                  :labelFields="['category']" valueField='category' :value="category"
                  @on_item_selected="(item) => { this.category = item.category }"
                  @on_Blur="(value) => { this.category = value }" showCount="20" width="500px"
                  class="dropdownMenuScroll" />
              </div>    
              <div class="form-group col-sm-12 col-md-8 col-lg query_condition">
                <label class="col-form-label caption col-auto pl-0">{{ $t("Prompt") }}</label>
                <LPCombobox url='/looper/session_manager/get_conditon_data' ref="condition_LPCasombobox"
                  :labelFields="['sname']" valueField='sname' :value="currentPrompt.sname"
                  @on_item_selected="onConditionSelected" @on_Blur="onConditionBlur" showCount="20" width="500px"
                  :filter="prompt_filter" class="dropdownMenuScroll" />
              </div>
              <div class="form-group col-auto">
                <div class="custom-control custom-control-inline custom-checkbox mr-0">
                  <input type="checkbox" class="custom-control-input" id="approved" v-model="isapproved" @change="setPromptFilter">
                  <label class="custom-control-label cursor-pointer" for="approved">{{ $t("Approved") }}</label>
                </div>
              </div>
              <div class="form-group col-auto">
                <button class="btn btn-primary mr-2" @click="getTasks">{{ $t("Search") }}</button>
                <button class="btn btn-primary mr-2" @click="aiAnalysis">{{ $t("AI Analysis") }}</button>
                <button class="btn btn-secondary btn_clear" @click="clearTasksHandler">{{ $t("Clear") }}</button>
              </div>
            </div>
          </fieldset>
          <div class="tab-pane fade active show" id="task-list" role="tabpanel">
            <LPDataTable ref="taskTable" :datasource="[]" :columns="taskColumns" :row_nowrap="true"
              :custom_options="taskOptions" :searching="false" :paging_inline="true" :custom_params_fun="taskParamsFun"
              @on_selectornot="taskTableRowSelected" :paging="false" @on_dbclick="showTaskDetail" />
          </div>
          <div class="tab-pane fade" id="task-list-all" role="tabpanel">
            <LPDataTable ref="taskAllTable" :datasource="[]" :columns="taskColumns" :row_nowrap="true"
              :custom_options="taskOptions" :searching="false" :paging_inline="true" :custom_params_fun="taskParamsFun"
              @on_selectornot="taskTableRowSelected" :paging="false" @on_dbclick="showTaskDetail" />
          </div>
          <div class="tab-pane fade" id="top-task" role="tabpanel">
            <div v-if="showTaskData">
              <LPDataTable ref="topTask" :datasource="[]" :columns="dataColumns" :row_nowrap="true"
                :custom_options="taskOptions" :searching="false" :paging_inline="true" :paging="false" @on_dbclick="showTaskDetail" />
            </div>
          </div>
          <div class="tab-pane fade" id="sql-script" role="tabpanel">
            <div class="row mx-0 sqlScriptRow">
              <div class="form-group col-12">
                <label class="col-form-label caption" for="tf6">{{ $t("SQL Query") }}</label>
                <textarea class="form-control control" id="tf6" rows="14" name="q_sql" v-model="currentPrompt.ssql"
                  @input="handleSsqlChange"></textarea>
              </div>
              <div class="form-group d-flex col-12">
                <label class="col-form-label caption col-auto pl-0">{{ $t("Prompt By Ai") }}</label>
                <input class="form-control mr-2" v-model="currentPrompt.promptbyai">
                <button class="btn btn-primary flex-shrink-0" @click="currentPrompt.ssql = historySsql">{{ $t("Restore") }}</button>
              </div>  
              <div class="form-group d-flex col-12 col-sm">
                <label class="col-form-label caption col-auto pl-0">{{ $t("Category") }}</label>
                <LPCombobox url='/looper/session_manager/get_category_data' ref="category_LPCasombobox"
                  :labelFields="['category']" valueField='category' :value="currentPrompt.category"
                  @on_item_selected="(item)=>{this.currentPrompt.category=item.category}"
                  @on_Blur="(value)=>{this.currentPrompt.category=value}" showCount="20" width="500px"
                  class="dropdownMenuScroll" />
              </div>
              <div class="form-group col-auto">
                <div class="custom-control custom-control-inline custom-checkbox">
                  <input type="checkbox" class="custom-control-input" id="isai" v-model="currentPrompt.isai" disabled>
                  <label class="custom-control-label cursor-pointer" for="isai">{{ $t("IsAi") }}</label>
                </div>
                <div class="custom-control custom-control-inline custom-checkbox mr-0">
                  <input type="checkbox" class="custom-control-input" id="isapproved"
                    v-model="currentPrompt.isapproved" :disabled="!canApprove">
                  <label class="custom-control-label cursor-pointer" for="isapproved">{{ $t("Approved") }}</label>
                </div>
              </div>
              <div class="form-group col-auto">
                <button class="btn btn-primary" @click="savePrompt">{{ $t("Save") }}</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <LPAIComBox ref="aicombox" :predefinedData="aiPredefinedData" />
</template>
<script>
import axios from "axios";
import LPTreegrid from "@components/looper/tables/LPTreegrid.vue";
import LPLabelInput from "@components/looper/forms/LPLabelInput.vue";
import LPCombobox from "@components/looper/forms/LPCombobox.vue";
import LPDataTable, { DateRender } from "@components/looper/tables/LPDataTable.vue";
import LPAIComBox from "@components/looper/general/LPAIComBox.vue";
export default {
  name: 'PmsSessionManager_vueFrm',
  components: { LPTreegrid, LPDataTable,LPLabelInput,LPCombobox,LPAIComBox,},
  data() {
    return {
      sessionColumns: [
        { field: 'sessionid', label: this.$t('Session ID'), width: 150 }, // 模版編號
        { field: 'parentid', label: '', visible: false }, // 模版編號
        { field: 'recordid', label: this.$t('Record ID'), width: '250px' }, //子工程編號
        { field: 'sdesp', label: this.$t('Description') }, // 任務描述
        { field: 'contact', label: this.$t('Contact') }, // 聯繫人
        { field: 'allcontact', label: this.$t('All Contact') }, // 所有聯繫人
        { field: 'progress', label: this.$t('Progress') }, // 進度
        {
          field: 'pschedule', label: this.$t('Plan schedule'), render: (value) => {
            return `<div style="width: 100%; height: 100%;">
              <div style="display: flex; width: 100%; height: 100%;">
                <div style="width: ${value}%; height: 100%; background-color: #0000FF;"></div>
                <div style="width: ${100 - value}%;"></div>
              </div>
              <div style="color: #FF3300; text-align: center;">${value}%</div>
            </div>`
          },
        }, // 計劃進度
        { field: 'aschedule', label: this.$t('Actual schedule') }, // 實際進度
        { field: 'planbdate', label: this.$t('Plan begin date'), render: DateRender }, // 計劃開始
        { field: 'planedate', label: this.$t('Plan end date'), render: DateRender }, // 計劃結束
        { field: 'priority', label: this.$t('Priority') }, // 優先級
        { field: 'projectscore', label: this.$t('Project scheduling priority') }, // 工程排期優先級
        { field: 'weight', label: this.$t('Scheduling priority') }, // 排期優先級
        { field: 'capacity', label: this.$t('Capacity') }, // 產能
        { field: 'djcapacity', label: this.$t('Day job capacity') }, // DayJob產能
        { field: 'outstandday', label: this.$t('Outstand day') }, // 拖期天數
        { field: 'outstandqty', label: this.$t('Outstand qty') }, // 拖期數量
        { field: 'flowchartno', label: this.$t('Flowchart') }, // 流程圖
        { field: 'type', label: this.$t('Type') }, // 類型
      ],
      sessionOption: {
        height: "460",
        uniqueId: "sessionid",
      },
      sessionDataSource: [],
      taskColumns: [
        { field: 'taskno', label: this.$t('Taskno') }, // 模版編號  
        { field: 'udf04', label: this.$t('Frame name') }, // 窗口名稱  
        { field: 'task', label: this.$t('Task Description'), width: '360px', className: 'subLabelMB' }, // 任務描述  
        { field: 'contact', label: this.$t('Contact') }, // 聯繫人  
        { field: 'progress', label: this.$t('Progress') }, // 進度  
        { field: 'planbdate', label: this.$t('Plan begin date'), render: DateRender }, // 計劃開始  
        { field: 'planedate', label: this.$t('Plan end date'), render: DateRender }, // 計劃結束  
        { field: 'score', label: this.$t('Score') }, // 分數  
        { field: 'relationid', label: this.$t('Relation ID') }, // 關聯任務  
        { field: 'bdate', label: this.$t('BDate'), render: DateRender }, // 實際開始  
        { field: 'edate', label: this.$t('EDate'), render: DateRender }, // 實際結束  
        { field: 'priority', label: this.$t('Priority') }, // 優先權 
        { field: 'schpriority', label: this.$t('Scheduling priority') }, // 排期優先級 
        { field: 'dayjob', label: this.$t('Day task') }, // 當天任務 
        { field: 'remark', label: this.$t('Remark') }, // 備註 
        { field: 'revisedby', label: this.$t('Revised by') }, // 修改人 
        { field: 'subprojectid', label: this.$t('Subproject iD') }, // 序號 
        { field: 'projectname', label: this.$t('Project name') }, // 工程名稱 
      ],
      /*
      topTaskColumns: [
        { field: "taskno", label: "TaskNo" },
        { field: "task", label: "Task", width: '360px' },
        { field: "contact", label: "Contact" },
        { field: "planbdate", label: "Plan Begin Date", render: DateRender },
        { field: "planedate", label: "Plan End Date", render: DateRender },
        { field: "progress", label: "Progress" },
        { field: "class", label: "Class" },
        { field: "remark", label: "Remark", width: '360px' },
        { field: "schpriority", label: "Schedule Priority" },
        { field: "projectname", label: "Project Name" },        
        { field: "recordid", label: "RecordID" },
        { field: "sdesp", label: "Session Name", width: '200px' },
        { field: "tasklistcontact", label: "Session Contact" },
        { field: "tasklistplanbdate", label: "Session Plan Begin Date", render: DateRender },
        { field: "tasklistplanedate", label: "Session Plan End Date", render: DateRender },
        { field: "tasklistprogress", label: "Session Progress" },
        { field: "tasklistremark", label: "Session Remark" },
      ], 
      */   
      dataColumns:[],
      taskOptions: {
        responsive: false,
        autoWidth: false,
        scrollX: true,
        scrollY: "45vh",
        // scrollCollapse: true, // 啟用滾動折疊
        deferLoading: 0,
      },
      contact: '', // 聯繫人
      allContact: [], // 所有聯繫人
      recordID: '', // 記錄ID
      period: '', // 時間範圍
      selectedProgress: '',
      selectedPriority: '',
      selectedContact: '',
      selectedCondition: null,
      selectedClass: '',
      taskText: '',
      progressOptions: [{ name: "", data: "" },
      { name: "N:新工作", data: "N" }, { name: "I:正在進行的工作", data: "I" }, { name: "T:當天的工作", data: "T" },
      { name: "S:已經開始的工作", data: "S" }, { name: "F:已完成工作", data: "F" }, { name: "C:基本完成", data: "C" },
      { name: "NF:除F的工作", data: "NF" }, { name: "H:被掛起的工作", data: "H" }, { name: "R:復查", data: "R" }
      ],
      priorityOptions: ['', '888', '8888', '8889'],
      classOptions: [{ label: '', value: '' }, { label: "class1", value: "1" }, { label: "class2", value: "2" }, { label: "Other", value: "3" }],
      contactOptions: [],
      selsectedTreeRow: {},
      allQuerySession: [],
      topTasks:[],
      conditions:[],
      loading:false,
      currentPrompt:{'inc_id':null, 'sname':'', 'isai':true, 'category':'','isapproved':false,'ssql':''},
      showTaskData:false,
      aiPredefinedData:[],
      ai_recordID:'',
      lang_code_en: true,
      isQueryCollapse: true,
      isTaskTabActive: false,
      sql_script:'', //查詢任務的SQL語句
      category:'',
      isapproved:false,
      prompt_filter:'',
      historySsql:'',
      canApprove:false,
      isMobile: false,
      bottomPaneMax: false,
      isclearPane: false,
    }
  },
  mounted() {
    this.get_lang_code();
    this.getPromptApprove();
    var _this = this;
    this.$nextTick(function () {
      if ($(".fixed-table-toolbar").attr('class').indexOf('d-none') == -1)
        $(".fixed-table-toolbar").addClass('d-none');
      var table = $(this.$refs.sessionTable.$el).find('table.SWTreegrid'); //TreeTable元素
      table.attr('data-toggle', 'table');
      table.attr('data-click-to-select', 'true');
      table.on('click-row.bs.table', function (e, row, el) {
        var dt = _this.$refs.taskTable.datatable; //task table 對象
        if ($(el).attr('class').indexOf("selected") != -1) {
          $(el).removeClass('selected');
          dt.clear().rows.add([]).draw();
          _this.selsectedTreeRow = {};
          return;
        } else {
          $(el).siblings().removeClass('selected')
          $(el).addClass('selected')
          _this.selsectedTreeRow = row;
        }
        _this.getTopTaskData([row.sessionid], dt)     

        if(SWApp.os.isMobile) {
          if (_this.bottomPaneMax) {
            _this.bottomPaneMax = false;
            _this.$nextTick(() => {
              _this.bottomPaneMax = true;
            });
          } else {
            // 如果是 false，直接设置为 true
            _this.bottomPaneMax = true;
          }
        }
      })

      $('.taskSearch .btn-reset').on('click', function () {
        _this.isQueryCollapse = !_this.isQueryCollapse;
      })

      // 监听 select2:open 事件
      $(".noFirstVal").on('select2:open', () => {
        setTimeout(() => {
          $(".select2-container.select2-container--open ul.select2-results__options>li.select2-results__option").each(function() {
            if ($(this).attr("id") === undefined) {
              $(this).addClass("d-none"); //當select2下拉選屬性中的id為空時,設置隱藏
            }
          });
        }, 0);
      });

      $('.PmsSessionManager .detailInfo a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        if ($(e.currentTarget).attr('id') === 'tab_tasks' || $(e.currentTarget).attr('id') === 'tab_sql') {
          _this.isTaskTabActive = true
        } else {
          _this.isTaskTabActive = false
        }
      });

      _this.mobileUI();
      $(".PmsSessionManager .LPDataTable .dataTables_info").closest(".row").addClass("mx-0");

      if(SWApp.os.isMobile) {
        _this.isMobile = true;
      }else {
        $(".search-scope").unwrap();
      }

    })

    var recordid = getParamFromUrl('recordid');
    if (recordid) {
      this.recordID = recordid;
      this.ai_recordID = recordid;
      this.queryClickHandler();      
    }
    // 聯繫人和全部聯繫人選擇框的處理
    $('.select2-contact').select2().on("select2:select", function (e) { _this.contact = e.params.data.text });
    $('.select2-contact-mul').select2().on("select2:select", function (e) {
      var text = e.params.data.text
      if (!_this.allContact.includes(text)) _this.allContact.push(text);
    }).on('select2:unselect', function (e) {
      var text = e.params.data.text
      if (_this.allContact.includes(text)) {
        _this.allContact.splice(_this.allContact.indexOf(text), 1);
      };
    });
    $('.select2-progress').select2().on("select2:select", function (e) { _this.selectedProgress = e.params.data.id });
    $('.select2-priority').select2().on("select2:select", function (e) { _this.selectedPriority = e.params.data.id });
    $('.select2-contact-task').select2().on("select2:select", function (e) { _this.selectedContact = e.params.data.id });
    //$('.select2-condition-task').select2().on("select2:select", function (e) { _this.selectedCondition = e.params.data.id });
    $('.select2-class').select2().on("select2:select", function (e) { _this.selectedClass = e.params.data.id });
    //
    $('.wrapper').on('shown.bs.modal', function (e) {
      $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
    });
    $(".wrapper").on("shown.bs.tab", "a[data-toggle='tab']", function (e) {
      $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
    });
  },
  created() {
    this.getContacts();
    //this.fetchSqlscriptData();
  },
  computed: {
    topPaneSize() {
      return this.bottomPaneMax ? 0 : 41;
    },
    bottomPaneSize() {
      return this.bottomPaneMax ? 100 : 59;
    }
  },
  watch: {
    selectedProgress: function () { this.taskListChange() },
    selectedPriority: function () { this.taskListChange() },
    selectedContact: function () { this.taskListChange() },
    selectedClass: function () { this.taskListChange() },
    isQueryCollapse() {
    },
    category: function(){ this.setPromptFilter() },
  },
  methods: {
    taskListChange() {
      if (this.selsectedTreeRow.sessionid !== undefined) {
        this.getTopTaskData([this.selsectedTreeRow.sessionid], this.$refs.taskTable.datatable);
      }
      this.getTopTaskData(this.allQuerySession, this.$refs.taskAllTable.datatable);
    },
    async getTopTaskData(sessionList, table) {
      const params = new URLSearchParams();
      params.append('selectedProgress', this.selectedProgress);
      params.append('selectedPriority', this.selectedPriority);
      params.append('selectedContact', this.selectedContact);
      params.append('taskText', this.taskText);
      params.append('selectedClass', this.selectedClass);
      params.append('sessionData', sessionList.join(','));

      try {
        const response = await axios.get('/looper/session_manager/get_filtered_tasks', { params });
        table.clear().rows.add(response.data.tasks || []).draw();
      } catch (error) {
        console.error(error);
      }
    },
    trim(str) {
      return str.replace(/^\s+|\s+$/g, '');
    },
    getTasks() {  
      $("#tab_tasks").click();
      this.showTaskData = false;     
      axios
        .get('/looper/session_manager/get_tasks', {
          params: {
            record_id: this.ai_recordID, // 替換為您的SubProjectID
            contact: this.selectedContact, // 替換為您的聯繫人
            condition: this.currentPrompt.inc_id,// 當前選中的條件
            question: this.currentPrompt.sname //查詢的內容
          },
        })
        .then(response => {     
          //this.sql_script = response.data.sql;    
          //this.currentPrompt.ssql=response.data.sql;  
          this.currentPrompt=response.data.promtsql;       
          this.historySsql = this.currentPrompt.ssql;
          if (!response.data.status)
            return alert('Data reading failed.')
          //const { columns, data } = response.data;
          this.topTasks = response.data.data;                    
          this.generateHeaders(response.data.columns)
          this.showTaskData = true;
          this.$nextTick(function(){
            this.$nextTick(function(){
              this.$refs.topTask.datatable.clear().rows.add(this.topTasks || []).draw();
            })
            
          })     
        })
        .catch(error => {
          console.log(error);
        });
    },
    queryClickHandler() {
      const params = {
        contact: this.trim(this.contact),
        allContact: this.trim(this.allContact.join(',')),
        recordID: this.trim(this.recordID),
        period: this.trim(this.period)
      };
      try {
        axios.get('/looper/session_manager/get_vtask_list_tree', { params }).then(res => {
          this.sessionDataSource = res.data;
          this.$nextTick(function () {
            this.$refs.sessionTable.reLoad();
            if ($(".fixed-table-toolbar").attr('class').indexOf('d-none') == -1)
              $(".fixed-table-toolbar").addClass('d-none');
          })
          this.allQuerySession = this.sessionDataSource.map(v => v.sessionid)
          if (this.allQuerySession.length !== 0)
            this.getTopTaskData(this.allQuerySession, this.$refs.taskAllTable.datatable)
          this.$refs.taskTable.datatable.clear().rows.add([]).draw();
          this.sessionEnquiryMobileUI();
        });
      } catch (error) {
        console.error(error);
      }
    },
    getContacts() {
      this.contactOptions.push('');
      axios.get(`/PMIS/user/get_part_user_names`).then(response => {
        if (response.data.data.length > 0) {
          response.data.data.forEach((contact) => {
            this.contactOptions.push(contact);
          });
        }
      });
    },
    fetchSqlscriptData() {
      axios.get('/looper/session_manager/get_conditon_data')
        .then(response => {
          this.conditions.push({'inc_id':null,'sname':''})
          if (response.data.length > 0) {
            response.data.forEach((condition) => {
              this.conditions.push(condition);
            });
          }
          var a = this.conditions;
        })
        .catch(error => {
          //console.error(error);
        });
    },
    generateHeaders(columns) {
      this.dataColumns = columns.map(column => {
        let header = {
          label: column.toUpperCase(),
          field: column
        };
        if (['TASK', 'REMARK'].includes(column.toUpperCase())) {
          header.width = '360px';
        }
        if (column.toUpperCase().includes('DATE')) {
          header.render = DateRender;
        }
        if (column.toUpperCase().includes('INC_ID')) {
          header.visible = false;
        }
        return header;
      });
    },
    showTaskDetail(task) {
      if (task.taskno && task.inc_id)
        init_task(task.inc_id);      
    },
    onConditionSelected(item) {  
      //this.currentPrompt = item;   
      this.fetchPromtsql(item.inc_id)
      //this.selectedCondition=item.inc_id;
      //this.getTasks();
    },
    onConditionBlur(text){           
      this.currentPrompt.sname = text;      
    },
    aiAnalysis() {      
      this.aiPredefinedData = this.topTasks;
      this.$nextTick(function(){
        this.$refs.aicombox.$refs.modal.show()      
      })
    },
    get_lang_code() {
      if ($("#curr_language_code").val() !== "en") {
        this.lang_code_en = false;
      }
    },
    clearHandler() {
      this.recordID = '';
      this.$nextTick(function () {
        $('select.select2-contact').val(null).trigger('change');
        $('select.select2-contact-mul').val([]).trigger('change').siblings('span.select2-container').find('ul.select2-selection__rendered').empty();
      })
    },
    clearTasksHandler() {
      this.taskText = '';
      this.ai_recordID = '';
      this.isapproved = false;
      this.currentPrompt = {'inc_id':null, 'sname':'', 'isai':true, 'category':'','isapproved':false,'ssql':''};
      this.category = '';
      this.$nextTick(function () {
        $('select.select2-progress, select.select2-priority, select.select2-class, select.select2-contact-task').val(null).trigger('change');
      })
    },
    mobileUI() {
      if(SWApp.os.isMobile || SWApp.os.isTablet && $(".taskSearch").hasClass("expanded")) {
        $(".taskSearch").removeClass("expanded");
        $(".taskSearch .btn-reset").attr("aria-expanded", "false");
        $(".taskSearch #sessionMgnTaskSearchCollapse").removeClass("show");
      }
    },
    sessionEnquiryMobileUI() {
      if($(".sessionSearchCard").hasClass("expanded")) {
        $(".sessionSearchCard").removeClass("expanded");
        $("#sessionSearchHeading>.btn-reset").attr("aria-expanded", "false");
        $(".sessionSearchCard #sessionSearchCollapse").removeClass("show");
      }
    },
    savePrompt() {
      if (this.currentPrompt.sname=='')
        return alert(this.$t('Prompt cannot be empty.'));
      //this.currentPrompt.ssql = this.sql_script;
      axios.post('/looper/session_manager/approve_condition', this.currentPrompt)
        .then(response => {
          if(response.data.status){
            this.currentPrompt = response.data.data;
            alert('保存成功');
          }else{
            alert(response.data.msg);
          }          
        })
        .catch(error => {
          console.error('保存失敗:', error);
        });
    },
    setPromptFilter(){
      var isap = this.isapproved ? 1 : 0;
      if (this.category)
        this.prompt_filter = 'category={0};isapproved={1}'.format(this.category,isap)
      else
        this.prompt_filter = 'isapproved={0}'.format(isap)      
    },   
    fetchPromtsql(inc_id) {
      axios.get(`/looper/session_manager/promtsql?id=${inc_id}`)
        .then(response => {
          if (response.data.status) {
            this.currentPrompt = response.data.data;
            this.historySsql = this.currentPrompt.ssql;
          } else {
            alert(response.data.msg || 'Failed to fetch Promtsql data.');
          }
        })
        .catch(error => {         
          alert('An error occurred while fetching Promtsql data.');
        });
    },
    getPromptApprove() {
      axios.get('/looper/session_manager/get_user_prompt_approve')
        .then(response => {
          if (response.data.status) {
            this.canApprove = response.data.data;
          } else {
            this.canApprove = false
          }
        })
        .catch(error => {         
          this.canApprove = false
        });
    },
    handleSsqlChange() {
      // 當 ssql 的值發生變化時，將 isai 賦值為 false
      if (this.currentPrompt.ssql === this.historySsql) {
        this.currentPrompt.isai = true;
      } else {
        this.currentPrompt.isai = false;
      }
    },
  },
}
</script>
<style>
/* dataTable 圖標 */
.LPDataTable table.dataTable thead .sorting:before {
  content: "\f0de" !important;
  right: 0.5em !important;
}

.LPDataTable table.dataTable thead .sorting:after {
  content: "\f0dd" !important;
}

.select2-container--open .select2-results__option {
  word-wrap: break-word;
}
</style>