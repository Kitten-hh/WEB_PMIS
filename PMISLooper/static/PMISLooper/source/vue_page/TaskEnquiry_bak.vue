<template>
  <nav class="page-navs flex-wrap LoanManagePage justify-content-between">
    <h6 class="title mb-0"> {{ $t("Task Enquiry") }} </h6>
    <div class="btn-tools d-flex align-items-center justify-content-between">
      <OperationBar class="buttonBar border-bottom-0" ref="buttonBar" button_show="0000011" module_power="65535"
        @on-search="String.prototype.render = undefined; $refs.advancedSearchDlg.event.showModal()"
        :function_items="function_items" @func1="auditScore('Y')" @func2="auditScore('R')" @func3="exportGoalExcel('T')"
        @func4="exportGoalExcel('T')" @func5="$refs.goalsPlanning.show()" size="btn-sm" />
    </div>
  </nav>
  <div class="page-inner py-3 taskEnquiryPage">
    <div class="card-deck-xl mb-3">
      <!-- 用戶輸入查詢 -->
      <QueryInput ref='queryInput' @queryTask="queryTask" />
      <!-- 預設條件查詢 -->
      <QueryRecord ref='queryRecord' @getRecord="getRecord" @searchTask="searchTask"
        @table="(table) => recordTable = table" />
    </div>
    <div class="card card-fluid mb-0">
      <div class="card-header">
        <ul class="nav nav-tabs card-header-tabs">
          <li class="nav-item">
            <a class='nav-link' data-toggle="tab" href="#project-list">{{ $t('Project List') }}</a>
          </li>
          <li class="nav-item">
            <a class='nav-link show active' data-toggle="tab" href="#task-list">{{ $t('Task List') }}</a>
          </li>
          <li class="nav-item">
            <a class='nav-link' data-toggle="tab" href="#taskitem-list">{{ taskitemLabel }}</a>
          </li>
          <li class="nav-item">
            <a class='nav-link' data-toggle="tab" href="#itemall-list">{{ $t('Item List') }}</a>
          </li>
          <li class="nav-item">
            <a class='nav-link' data-toggle="tab" href="#sms-list">{{ $t('SMS List') }}</a>
          </li>
        </ul>
      </div>
      <div class="card-body p-2">
        <div class="tab-content">
          <div class="tab-pane fade" id="project-list">
            <ProjectList @table="(table) => { projectTable = table }" @show="$refs.questionType.show()" />
          </div>
          <div class="tab-pane fade active show" id="task-list">
            <LPDataTable ref="taskTable" :datasource="[]" :columns="taskColumns" :custom_options="taskOptions"
              :searching="false" :paging="true" :pageLength="25" @on_dbclick="taskTableRowDblClick"
              @on_row_click="taskTableRowClick" :firstColSelected="true" />
          </div>
          <div class="tab-pane fade" id="taskitem-list">
            <TaskItemList @table="(table) => { taskItemTable = table }" />
          </div>
          <div class="tab-pane fade" id="itemall-list">
            <TaskItemAllList @table="(table) => { taskItemAllTable = table }" />
          </div>
          <div class="tab-pane fade" id="sms-list">
            <SMSList @table="(table) => { smsTable = table }" />
          </div>
        </div>
      </div>
    </div>
  </div>
  <AdvancedSearchDlg ref="advancedSearchDlg" :masterColumns="taskColumns" @search="advanceSearch" />
  <SelectQuestionType ref="questionType" @confirm="questionTypeConfirm" />
  <UploadOrReviewDoc ref="uploadOrReviewDoc" @submit="documentSubmit" @select="documentSelect"
    @table="(table) => { documentTable = table }" />
  <SendEmail ref="email" @send="sendEmail" :emailObj="emailObj" />
  <BatchTranTask ref="batchTranTask" :columns="taskColumns" @select-table="(table) => { selectTranTaskTable = table }" />
  <GoalsPlanning ref="goalsPlanning"/>
  <GenerateWorkflow ref="generateWorkflow"/>
  <GeneralFlowupTask ref="generalFlowupTask"/>
  <AddRelationTask ref="addRelationTask"/>
  <div id="form"></div>
</template>
<script>
import axios from "axios";
import LPDataTable, { DateRender } from "@components/looper/tables/LPDataTable.vue";
import OperationBar from "@components/looper/navigator/OperationBar.vue";
import AdvancedSearchDlg from "./AdvancedSearchDlg.vue";
import QueryInput from "./TaskEnquiryFolder/QueryInput.vue";
import QueryRecord from "./TaskEnquiryFolder/QueryRecord.vue";
import ProjectList from "./TaskEnquiryFolder/ProjectList.vue";
import TaskItemList from "./TaskEnquiryFolder/TaskItemList.vue";
import TaskItemAllList from "./TaskEnquiryFolder/TaskItemAllList.vue";
import SMSList from "./TaskEnquiryFolder/SMSList.vue";
import SelectQuestionType from "./TaskEnquiryFolder/SelectQuestionType.vue";
import UploadOrReviewDoc from "./TaskEnquiryFolder/UploadOrReviewDoc.vue";
import SendEmail from "./TaskEnquiryFolder/SendEmail.vue";
import BatchTranTask from "./TaskEnquiryFolder/BatchTranTask.vue";
import GoalsPlanning from "./TaskEnquiryFolder/GoalsPlanning.vue";
import GenerateWorkflow from "./TaskEnquiryFolder/GenerateWorkflow.vue";
import GeneralFlowupTask from "./TaskEnquiryFolder/GeneralFlowupTask.vue";
import AddRelationTask from "./TaskEnquiryFolder/AddRelationTask.vue";
export default {
  name: "TaskEnquiry_vueFrm",
  components: {
    LPDataTable,
    OperationBar,
    AdvancedSearchDlg,
    QueryInput,
    QueryRecord,
    ProjectList,
    TaskItemList,
    TaskItemAllList,
    SMSList,
    SelectQuestionType,
    UploadOrReviewDoc,
    SendEmail,
    BatchTranTask,
    GoalsPlanning,
    GenerateWorkflow,
    GeneralFlowupTask,
    AddRelationTask,
  },
  data() {
    var self = this;
    return {
      cid: "", // 跳轉到任務分析界面需要時用到的參數
      conditions: "", //當前查詢任務的SQL,從後台返回的(可以嘗試二進制)
      filter: "", //後台傳出的當前任務列表的過濾條件
      user: '', // 輸入的需要查詢的用戶,並非是當前登錄系統的人
      loginUser: get_username(), // 當前系統登錄的用戶
      menuData: {}, // 任務列表中右鍵選中的行數據
      emailObj: {}, // 發送email的參數對象
      taskitemLabel: this.$t('Task Item List'), //任務明細的標題,選中任務時顯示 `pid-tid-taskid`
      recordTable: undefined, // 記錄列表的DataTable實例
      projectTable: undefined,// 工程列表的DataTable實例
      taskItemTable: undefined,// 任務明細列表的DataTable實例
      taskItemAllTable: undefined,// 任務明細All列表的DataTable實例
      smsTable: undefined,// 短信(SMS)列表的DataTable實例
      documentTable: undefined, // 任務上傳的文檔列表的DataTable實例
      selectTranTaskTable: undefined, // 批量轉換任務中當前所有任務顯示列表的DataTable實例
      taskColumns: [
        { field: "inc_id", label: this.$t("inc_id"), visible: false },
        { field: "pid", label: this.$t("PID") }, //工程編號
        { field: "tid", label: this.$t("TID") }, //類別編號
        { field: "taskid", label: this.$t("Task ID") }, //任務編號
        { field: "udf04", label: this.$t("Window name") }, //窗口名稱
        { field: "editionid", label: this.$t("Edition ID") },//版本號
        { field: "task", label: this.$t("Task"), width: '250px' }, //任務描述
        { field: "contact", label: this.$t("Contact") }, //聯繫人
        { field: "progress", label: this.$t("Progress") }, //進度
        { field: "planbdate", label: this.$t("Plan Begin Date"), render: DateRender }, //計劃開始時間
        { field: "planedate", label: this.$t("Plan End Date"), render: DateRender }, //計劃結束時間
        { field: "priority", label: this.$t("Priority") }, //優先級
        { field: "clazz", label: this.$t("Class") }, //分類
        { field: "calpriority", label: this.$t("Computed Priority") }, //計算的優先級
        { field: "schpriority", label: this.$t("SchPriority") }, //排期優先級
        // { field: "qutday", label: this.$t("Qut day") }, //脫期天數
        { field: "quantity", label: this.$t("Quantity") }, //數量
        { field: "tasktype", label: this.$t("Task type") }, //任務分類
        { field: "realtasktype", label: this.$t("Real Task Type") }, //任務分類編號
        { field: "score", label: this.$t("Score") }, //分數
        { field: "relationgoalid", label: this.$t("RelationGoalId") }, //RelationGoalId
        { field: "dayjob", label: this.$t("Day job") }, //當天任務
        { field: "atime", label: this.$t("Atime") }, //實際天數
        { field: "remark", label: this.$t("Remark") }, //備註
        { field: "relationid", label: this.$t("RelationID") }, //關聯任務
        { field: "reference", label: this.$t("Reference") }, //參考
        { field: "charge", label: this.$t("Charge") }, //收費
        { field: "requestdate", label: this.$t("Request Date"), render: DateRender }, //需求日期
        { field: "createdate", label: this.$t("Create Date"), render: DateRender }, //創建日期
        { field: "cycletask", label: this.$t("Cycle Task") }, //循環任務
        { field: "r_flag", label: this.$t("Read") }, //已讀
        { field: "taskno", label: this.$t("TaskNo") }, // 任務
        { field: "etime", label: this.$t("ETime") }, // 計劃天數
        { field: "bdate", label: this.$t("BDate"), render: DateRender }, // 實際開始
        { field: "edate", label: this.$t("EDate"), render: DateRender }, // 實際結束
        { field: "subtasktype", label: this.$t("SubTask Type") }, // 任務子分類
        { field: "diff", label: this.$t("Diff") }, //難度
        { field: "docpath", label: this.$t("DocPath") }, //關聯文檔
        { field: "udf02", label: this.$t("Associated progress") }, //關聯進度
        { field: "flowchartno", label: this.$t("FlowChart no") }, //流程編號
        { field: "revisedby", label: this.$t("Revised By") }, //修改人
        { field: "udf10", label: this.$t("Sample list") }, //樣板單別
        { field: "udf01", label: this.$t("Template no") }, //樣板號
        { field: "sprogress", label: this.$t("S.Progress") }, //模塊進度
        { field: "scontact", label: this.$t("S.Contact") }, //模塊聯繫人
        { field: "hoperation", label: this.$t("Operation") }, //操作
        { field: "subprojectid", label: this.$t("Subproject ID") }, //序號
        { field: "projectid", label: this.$t("Project ID") }, //工程編號
        { field: "projectname", label: this.$t("Project name") }, //工程名稱
      ],
      taskOptions: {
        responsive: false,
        scrollY: "65vh",
        scrollX: true,
        processing: true,
        autoWidth: false,
        deferLoading: 0,
        "drawCallback": function (s) {
          var api = this.api();
          var data = api.rows({ page: 'current' }).data().toArray()
          if (data.length < 1) return;
          var projects = {};
          for (let item of data) {
            if (`${item.pid}-${item.tid}` in projects)
              continue;
            else {
              projects[`${item.pid}-${item.tid}`] = { pid: item.pid, tid: item.tid }
            }
          }
          var url = "/looper/task/enquiry/get_projects";
          axios.get(url, { params: { param: projects } }).then(res => {
            if (res.data.status)
              self.projectTable.clear().rows.add(res.data.data || []).draw();
          })
        },
        "rowCallback": (r) => {
          $(r).addClass('contextMenu-task')
        }
      },
      function_items: [
        { label: this.$t('Audit Score'), event: 'func1' },
        { label: this.$t('unAudit Score'), event: 'func2' },
        { label: this.$t('Export MS Project_T'), event: 'func3' },
        { label: this.$t('Export MS Project_G'), event: 'func4' },
        { label: this.$t('Export Goals'), event: 'func5' },
      ],
    }
  },
  created() {
    // 導入右鍵菜單的js和css
    loadCss("/static/BaseApp/vendor/jquery_contextmenu/jquery.contextMenu.min.css");
    loadJs(["/static/BaseApp/vendor/jquery_contextmenu/jquery.ui.position.min.js"], true);
    loadJs(["/static/BaseApp/vendor/jquery_contextmenu/jquery.contextMenu.min.js"], true);
  },
  mounted() {
    var self = this;
    $('.modal').on('shown.bs.modal', function (e) {
      $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
    });
    $('.wrapper').on("shown.bs.tab", "a[data-toggle='tab']", function (e) {
      $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
    });
    $.contextMenu({
      selector: '.contextMenu-task',
      callback: function (key, options) {
        self.menuData = self.$refs.taskTable.datatable.row($(options.$trigger)).data()
        if (key == "1") {
          self.$refs.uploadOrReviewDoc.upload();
        }
        if (key == "2") {
          self.getDocumentList();
          self.$refs.uploadOrReviewDoc.review();
        }
        if (key == "3") {
          var taskno = self.menuData.taskno || '';
          var task = self.menuData.task || '';
          var contact = self.menuData.contact || '';
          var progress = self.menuData.progress || '';
          var priority = self.menuData.priority || '';
          var remark = self.menuData.remark || '';
          var planbdate = self.menuData.planbdate || '';
          var planedate = self.menuData.planedate || '';
          self.emailObj.sender = 'pms@mail.kingshing.com';
          self.emailObj.topic = `${taskno}: ${task.substring(0, 20)}...`;
          self.emailObj.content = `TaskNo: ${taskno}.\nTaskDesc: ${task}.\nContact: ${contact}.\nProgress: ${progress}.\nPriority: ${priority}.\nRemark: ${remark}.\nPlanBDate: ${DateRender(planbdate)}.\nPlanEDate: ${DateRender(planedate)}.`;
          self.$refs.email.showSend();
        }
        if (key == "4") {
          self.exportTaskExcel();
        }
        if (key == "5") {
          var arr = self.$refs.taskTable.datatable.data();
          self.selectTranTaskTable.clear().rows.add(arr).draw();
          self.$refs.batchTranTask.showTran();
        }
        if (key == "6") {
          self.$refs.generateWorkflow.show(self.menuData);
        }
        if (key == "7") {
          self.$refs.generalFlowupTask.show(self.loginUser,self.menuData);
        }
        if (key == "8") {
          self.$refs.addRelationTask.show(self.menuData);
        }
      },
      items: {
        "1": { name: gettext(self.$t('upload document')) }, //上傳文檔
        "2": { name: gettext(self.$t('review document')) }, //查看文檔
        "3": { name: gettext(self.$t('Send Email')) }, //發送郵件
        "4": { name: gettext(self.$t('Export Excel')) }, //導出Excel
        "5": { name: gettext(self.$t('Batch Tran Task')) }, //批量轉任務
        "6": { name: gettext(self.$t('Generate Workflow')) }, //生成工作流
        "7": { name: gettext(self.$t('General Flowup Task')) }, //生成跟進任務
        // "8": { name: gettext(self.$t('Relation Task')) }, //關聯任務
      }
    });
  },
  methods: {
    exportGoalExcel(flag) {
      // 按當前任務的過濾條件查詢出的Goal導出為MS project格式
      var url = "/looper/task/enquiry/goal_excel"
      if (this.filter == '') return alert(this.$t('no query filter'))
      var param = { "filter": this.filter, "status": true }
      if (flag == 'G') // MS project_G
        param['is_downup'] = false
      var data = this.objectToFormData(param)
      axios.post(url, data, { responseType: 'blob' })
        .then(res => {
          const { data, headers } = res
          const fileName = headers['content-disposition'].replace(/\w+;filename=(.*)/, '$1')
          const blob = new Blob([data], { type: headers['content-type'] })
          let dom = document.createElement('a')
          let url = window.URL.createObjectURL(blob)
          dom.href = url
          dom.download = decodeURI(fileName)
          dom.style.display = 'none'
          document.body.appendChild(dom)
          dom.click()
          dom.parentNode.removeChild(dom)
          window.URL.revokeObjectURL(url)
        }).catch(err => { alert(this.$t("no data")) });
    },
    auditScore(state) {
      // 審核與反審核績效分
      var url = "/looper/task/enquiry/audit_score"
      var tasks = this.$refs.taskTable.getSelectedFlagData()["datas"];
      if (tasks && tasks.length == 0)
        return alert(this.$t("Please select task record"));
      axios.post(url, this.objectToFormData({ "tasks": JSON.stringify(tasks), "audit": state }))
        .then((response) => {
          var result = response.data;
          if (result.status)
            if (state == 'Y')
              alert(this.$t("Post Success"));
            else
              alert(this.$t("Un Post Success"));
          else
            alert(result.msg);
        }).catch(err => { console.log(err) });
    },
    exportTaskExcel() {
      // 將當前顯示在task列表中的任務以excel的形式導出
      var table = this.$refs.taskTable.datatable;
      var arr = table.data().map(v => v.inc_id).join(';');
      var url = '/looper/task/enquiry/export_excel'
      var taskCol = JSON.parse(JSON.stringify(this.taskColumns))
      for (let item of taskCol) { // 不要刪除代碼,此處用於去掉寬度在後台讓程序自動計算,不然會報錯
        if ('width' in item)
          delete item.width
      }
      var table_header = JSON.stringify(taskCol)
      axios.get(url, {
        params: {
          arr: arr, export_excel: 'TaskList',
          table_header: table_header
        }, responseType: 'blob'
      }).then(res => {
        const { data, headers } = res
        const fileName = headers['content-disposition'].replace(/\w+;filename=(.*)/, '$1')
        const blob = new Blob([data], { type: headers['content-type'] })
        let dom = document.createElement('a')
        let url = window.URL.createObjectURL(blob)
        dom.href = url
        dom.download = decodeURI(fileName)
        dom.style.display = 'none'
        document.body.appendChild(dom)
        dom.click()
        dom.parentNode.removeChild(dom)
        window.URL.revokeObjectURL(url)
      }).catch(err => { console.log(err) })
    },
    sendEmail(emailStatus) {
      // 將任務信息以郵件形式發送 
      var url = '/looper/task/enquiry/send_email'
      if (this.emailObj.addr === "") return alert('no email addr')
      this.emailObj['status'] = emailStatus;
      axios.get(url, { params: this.emailObj }).then(res => {
        if (res.data.ststus) {
          alert(this.$t('Success'))
        }
        this.$refs.email.hideSend();
      }).catch(err => { console.log(err) })
    },
    documentSelect(rowObj) {
      // 用戶選擇了任務文檔之後,瀏覽器自動下載
      if (rowObj.parentid == undefined || rowObj.folderid == undefined)
        return alert('Please select row');
      $("#form").children().remove();
      var form = $("<form method='post'></form>");
      let url = `/looper/task/enquiry/display_file?parentid=${rowObj.parentid}&folderid=${rowObj.folderid}`;
      form.attr({ "action": url });
      $("#form").append($(form));
      form.submit();
    },
    getDocumentList() {
      // 獲取當前任務所有上傳了的文檔數據
      var url = "/looper/task/enquiry/review_doc"
      var params = {};
      params.pid = this.menuData.pid;
      params.tid = this.menuData.tid;
      params.docpath = this.menuData.docpath == null ? '' : this.menuData.docpath;
      params.taskid = this.menuData.taskid;
      axios.get(url, { params: params }).then(res => {
        this.documentTable.clear().rows.add(res.data.data || []).draw();
      }).catch(err => { console.log(err) })
    },
    documentSubmit(file) {
      // 用戶上傳文件操作的處理函數
      var fd = new FormData();
      fd.append('file', file);
      fd.append('pid', this.menuData.pid);
      fd.append('docpath', this.menuData.docpath == null ? '' : this.menuData.docpath);
      fd.append('taskno', this.menuData.taskno);
      fd.append('revisedby', this.loginUser);
      axios.post('/looper/task/enquiry/import_doc_file', fd).then(res => {
        if (res.data.status)
          alert('上傳成功')
        else
          alert('上傳失敗')
        this.$refs.uploadOrReviewDoc.hideUpload();
      }).catch(err => { console.log(err) })
    },
    advanceSearch(filter) {
      // 任務界面的高級查詢處理
      var url = "/looper/task/enquiry/task_table?format=datatables";
      axios.get(url, {
        params: {
          'search[value]': 'form-search:' + JSON.stringify(filter),
          'draw': 0,
          "start": 0,
          'length': -1,
          'username': this.user
        },
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      }).then(res => {
        if (res.status == 200) {
          this.$refs.taskTable.datatable.clear().rows.add(res.data.data || []).draw();
          this.$refs.advancedSearchDlg.event.hideModal();
        }
      })
    },
    questionTypeConfirm() {
      // 在工程列表上右鍵菜單點擊訪問FAQ頁面,選擇了類型後的提交事件
      var url = `http://${window.location.host}/zh-hans/looper/task/faqAnalysisTask?`
      if (this.cid !== '')
        window.location.href = url + `cid=${this.cid}&isq=${this.isq}`
      else
        window.location.href = url + `condition=${encodeURIComponent(this.conditions)}&isq=${this.isq}`
    },
    taskTableRowClick(e, data) {
      // 任務列表的行單擊事件,主要顯示當前選中任務的明細信息
      var url = "/looper/task/enquiry/get_taskitem"
      this.taskitemLabel = `${data.pid}-${data.tid}-${data.taskid}`
      axios.get(url, { params: { pid: data.pid, tid: data.tid, taskid: data.taskid } }).then(res => {
        this.taskItemTable.clear().rows.add(res.data.data || []).draw();
      }).catch(err => { console.log(err) })
    },
    taskTableRowDblClick(data) {
      // 任務列表的行雙擊事件,顯示任務的詳細信息以及可以修改任務內容.
      // 因為高級查詢的dxfilter組件的字符串渲染中使用到了render函數判定,所以在彈出高級查詢前將render給undefined了
      String.prototype.render = function (context) {
        return this.replace(/\[\[(.*?)\]\]/g, (match, key) => {
          if (context[key.trim()] == undefined || context[key.trim()] == null)
            return "";
          else {
            if (typeUtils.isString(context[key.trim()]))
              return context[key.trim()].trim();
            else
              return context[key.trim()];
          }
        });
      }
      init_task(data.inc_id);
    },
    searchTask(data) {
      // 根據用戶選擇的預設條件來查詢任務
      this.cid = `${data.qf001};${data.qf002};${data.qf006}`
      axios.get("/looper/task/enquiry/query_task", { params: { queryid: data.qf025, type: "record", username: this.user } })
        .then(res => {
          if (res.data.status) {
            this.$refs.taskTable.datatable.clear().rows.add(res.data.data || []).draw();
            this.taskItemAllTable.clear().rows.add(res.data.item_data || []).draw();
            this.smsTable.clear().rows.add(res.data.sms_data || []).draw();
            this.filter = res.data.filter
          }
        }).catch(err => { console.log(err) })
    },
    queryTask(searchObj) {
      // 根據用戶輸入的條件來查詢任務
      this.cid = ''; // cid設置為空則表示使用conditions來訪問問題分析界面
      searchObj['username'] = this.user;
      searchObj['type'] = "input";
      axios.get("/looper/task/enquiry/query_task", { params: searchObj })
        .then(res => {
          if (res.data.status) {
            this.$refs.taskTable.datatable.clear().rows.add(res.data.data || []).draw();
            this.taskItemAllTable.clear().rows.add(res.data.item_data || []).draw();
            this.smsTable.clear().rows.add(res.data.sms_data || []).draw();
            this.conditions = res.data.sql;
            this.filter = res.data.filter
          }
        }).catch(err => { console.log(err) })
    },
    getRecord(user, is_dialy) {
      // 獲取預設的任務查詢條件填充到數據表中
      this.user = user;
      axios.get("/PMIS/query/search", { params: { filter: user, is_dialy: is_dialy } })
        .then(res => {
          this.recordTable.clear().rows.add(res.data.data || []).draw();
        }).catch(err => { console.log(err) })
    },
  }
};
</script>
<style>
.buttonBar>.card {
  box-shadow: none;
  margin-bottom: 0;
  padding: 0 !important;
  background-color: transparent;
}

.context-menu {
  position: fixed;
  background-color: #fff;
  border: 1px solid #ccc;
  padding: 0.5rem;
  list-style: none;
  z-index: 999;
}

.faqAnalysisTask .email_address {
  height: 35rem;
  overflow-y: auto;
}

.faqAnalysisTask .email_address fieldset {
  border: solid 1px #CCC;
  border-radius: 8px;
  padding: 0 1rem;
  height: 100%;
  overflow-y: auto;
}

.faqAnalysisTask .email_address legend {
  width: auto;
  color: #333;
  font-size: 14px;
  padding: 0em 0.5em;
  font-weight: bold;
}
</style>