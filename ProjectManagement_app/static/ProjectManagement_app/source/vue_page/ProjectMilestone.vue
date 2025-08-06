<template>
  <div v-if="loading_pdf" class="overlay">
    <div class="spinner">
        {{ $t("Loading PDF...") }}
    </div>
  </div>  
  <div class="query-section d-flex">
    <div class="form-group col mb-2">
      <label for="recordId" class="sr-only">RecordID</label>
      <input 
        v-model="queryRecordId" 
        type="text" 
        class="form-control" 
        id="recordId" 
        :placeholder="$t('Enter RecordID')" />
    </div>
    <div class="col-auto">
      <button @click="fetchData(false)" class="btn btn-primary mb-2">{{$t('Search')}}</button>
    </div>
  </div>
  <div v-if="loading" class="loading-spinner">
    {{ $t("Translating...") }}
  </div>  
  <LPTreegrid 
    ref="tree_grid"
    class="project_milestone_treegrid"
    :columns="columns" 
    :datasource="dataSource" 
    idField="task_number" 
    parentIdField="parent" 
    :paging="true" 
    :searching="true" 
    :expand="1==1"
    @onPostBody="treeGridLoad"
    :pageLength="10">
  </LPTreegrid>
  <!-- 模态框，用于显示甘特图 -->
  <LPModal ref="ganttModal" class="ganttModal" :title="$t('Gantt View')" size="lg" :show_part="'hb'">
    <template v-slot:body>      
    <LPGantt 
      ref="gantt" 
      startField="plan_start"
      endField="plan_end"
      :titleField="ganttGetDesc"
      idField="task_number"
      dependenciesField="parent"
      defaultExpandLevel="2"
      progressField="progress"
      :extendedFields="ganttExtendedFields"
      :datasource="ganttDataSource"
      :eventDbClick="ganttEventDbClick"
      :customOptions="ganttCustomOptions"
      :getCustomClass="ganttCustomClass"
    />
    </template>
  </LPModal>
  <LPModal ref="calendarModal" :title="$t('Calendar View')" size="lg" :show_part="'hb'">
    <template v-slot:body>      
    <LPCalendar
      ref="calendar" 
      class="project_milestone_calendar"
      startField="plan_start"
      endField="plan_end"
      titleField="task_description"
      :extendedFields="calendarExtendedFields"
      :datasource="calendarDataSource"
    />
    </template>
  </LPModal>
  <LPModal ref="taskModal" :title="$t('Task View')" size="lg" :show_part="'hb'">
    <template v-slot:body>      
    <LPDataTable
      ref="tasksDataTable" 
      class="project_milestone_tasksDataTable" 
      :columns="taskColumns"
      :datasource="[]"
      :paging_inline="true"
      :searching="false"
      :paging="false"
      :custom_options="task_custom_options"
    />
    </template>
  </LPModal>
  <LPModalForm
       ref="sessionModal"
       class="editSessionForm"
       :title="$t('Edit Session')"
       @on_submit="edit_session_submit_event">
       <div class="sessionWrap d-flex mb-2">
            <label class="mr-2 mb-0">{{$t("Session") }}:</label>
            <p id="edit_session_sessionID" class="text-mute mb-0">{{ currentSession.pid }}-{{currentSession.tid}} {{currentSession.sdesp}}</p>
        </div>       

       <!-- 表單內容 -->
       <LPLabelInput :label="$t('Contact')">
        <select data-toggle="selectpicker" data-size="5" data-width="100%" class="control status_select" data-none-selected-text v-model="currentSession.contact" data-container="body"> 
            <option></option>
            <option v-for="(item, index) in partUserNames" :key="index" :value="item"> {{ item }} </option>
        </select>        
       </LPLabelInput>
       <!-- 其他表單內容 -->
       <LPLabelInput :label="$t('Progress')">
        <select data-toggle="selectpicker" data-size="5" data-width="100%" class="control status_select" data-none-selected-text v-model="currentSession.progress" data-container="body"> 
            <option></option>
            <option v-for="(item, index) in taskProgress" :key="index" :value="item"> {{ item }} </option>
        </select>        
       </LPLabelInput>
       <LPLabelInput :label="$t('PlanBDate')">
            <input class="form-control control" type="datetime-local" v-model="currentSession.planbdate" required/>   
       </LPLabelInput>
       <LPLabelInput :label="$t('PlanEDate')">
            <input class="form-control control" type="datetime-local" v-model="currentSession.planedate" required/>   
       </LPLabelInput>
       <LPLabelInput :label="$t('Relation Session')">
            <input class="form-control control" type="text" v-model="currentSession.relationsessionid" @focusout="checkRelationSession($event.target.value)"/>   
       </LPLabelInput>       
       <LPLabelInput :label="$t('Relation Status')">
        <select data-toggle="selectpicker" data-size="5" data-width="100%" class="control status_select" data-none-selected-text v-model="currentSession.relationstatus" data-container="body"> 
            <option></option>
            <option value="I">I:{{$t("relation_status_I") }}</option>
            <option value="F">F:{{$t("relation_status_F") }}</option>
        </select>        
       </LPLabelInput>
       <div class="parentSessionWrap d-flex">
        <i id="parentSessionIcon" class="fas fa-level-up-alt fa-rotate-by text-purple"></i>
        <p id="editSession_relationSession" class="text-mute mb-0 ml-3">{{ relationSessionDesp }}</p></div>          
       <LPLabelInput :label="$t('Parent Session')">
            <input class="form-control control" type="text" v-model="currentSession.parent" @focusout="checkParentSession($event.target.value)"/>   
       </LPLabelInput>
       <div class="parentSessionWrap d-flex">
        <i id="parentSessionIcon" class="fas fa-level-up-alt fa-rotate-by text-purple"></i>
        <p id="editSession_parentSession" class="text-mute mb-0">{{ parentSessionDesp }}</p></div>       
     </LPModalForm>  
     <LPAIComBox ref="aicombox"
      :predefinedData="aiPredefinedData" /> 
     <input type="hidden" v-model="send_gantt_email"/>
</template>

<script>
import axios from "axios";
import LPTreegrid,{DateRender} from "@components/looper/tables/LPTreegrid.vue";
import LPDataTable from "@components/looper/tables/LPDataTable.vue";
import LPGantt from "@components/looper/general/LPGantt.vue";
import LPCalendar from "@components/looper/general/LPCalendar.vue";
import LPModal from "@components/looper/layout/LPModal.vue";
import LPModalForm from "@components/looper/layout/LPModalForm.vue";
import LPLabelInput from "@components/looper/forms/LPLabelInput.vue";
import LPAIComBox from "@components/looper/general/LPAIComBox.vue";
export default {
  name: 'TaskListTreeGrid',
  components: { LPTreegrid,LPGantt,LPModal,LPCalendar,LPDataTable,LPModalForm,LPLabelInput, LPAIComBox },
  data() {
    var self = this;
    return {
      loading_pdf:false,
      send_gantt_email:"Y",
      loading:false,
      queryRecordId:'',
      currentSession:{},
      partUserNames:[],
      taskProgress:[],
      aiPredefinedData:[],
      parentSessionDesp:"",
      relationSessionDesp:"",
      currentGanttTaskNumber:"",
      columns: [
        { field: 'task_description', label: this.$t('Task'), width: 400, orderable: true, visible: true, class: "taskWrap" },
        { field: 'task_number', label: this.$t('TaskNo'), width: 150, orderable: true, visible: true },
        { field: 'contact', label: this.$t('Contact'), width: 80, orderable: true, visible: true },
        { field: 'plan_start', label:this.$t('PlanBDate'), width: 80, orderable: true, visible: true,render:DateRender },
        { field: 'plan_end', label: this.$t('PlanEDate'), width: 80, orderable: true, visible: true,render:DateRender },
        { field: 'status', label: this.$t('Progress'), width: 40, orderable: true, visible: true },
        { field:'operate',label: this.$t('Operation'),width:"30",
        render: function(value, row, index) {    
            var arr = row.task_number.split("-");

            // Task related menus
            var addtask_menu = arr.length >= 2 ? `<a class="dropdown-item addtask-view" href="#" task_number="${row.task_number}"><i class="la la-cloud-download"></i>` + self.$t("Add Task") + `</a>` : "";            
            var edit_menu = arr.length == 3 ? `<a class="dropdown-item edit-view" href="#" task_number="${row.task_number}" inc_id="${row.inc_id}"><i class="la la-cloud-download"></i>` + self.$t("Edit Task") + `</a>` : "";            
            var tasklist_view_menu = arr.length !== 3 ? `<a class="dropdown-item tasklist-view" href="#" task_number="${row.task_number}"><i class="la la-cloud-download"></i>` + self.$t("Show Class1 Tasks") + `</a>`:"";

            // Session related menus
            var edit_session_menu = arr.length === 2 ? `<a class="dropdown-item edit-session" href="#" task_number="${row.task_number}"><i class="la la-cloud-download"></i>` + self.$t("Edit Session") + `</a>` : "";
            var del_session_menu = arr.length === 2 ? `<a class="dropdown-item del-session" href="#" inc_id="${row.inc_id}"><i class="la la-cloud-download"></i>` + self.$t("Delete Session") + `</a>` : "";
            var goto_requirement_menu = arr.length === 2 ? `<a class="dropdown-item goto-requirement" href="#" task_number="${row.task_number}"><i class="la la-cloud-download"></i>` + self.$t("Go to Requirement") + `</a>` : "";
            var show_session_task_menu = arr.length === 2 ? `<a class="dropdown-item show-session-task" href="#" task_number="${row.task_number}"><i class="la la-cloud-download"></i>` + self.$t("Show Session Tasks") + `</a>` : "";
            var gantt_summary_menu = arr.length === 2 ? `<a class="dropdown-item gantt-summary" href="#" task_number="${row.task_number}"><i class="la la-cloud-download"></i>` + self.$t("Go to Summary") + `</a>` : "";            
            var ai_analysis_session_menu = arr.length === 2 ? `<a class="dropdown-item gantt-ai-analysis" href="#" task_number="${row.task_number}"><i class="la la-cloud-download"></i>` + self.$t("Ai Analysis") + `</a>` : "";            

            // View related menus
            var gantt_view_menu = `<a class="dropdown-item gantt-view" href="#" task_number="${row.task_number}"><i class="la la-cloud-download"></i>` + self.$t("Gantt View") + `</a>`;
            var gantt_view_all_menu = `<a class="dropdown-item gantt-view-all" href="#" task_number="${row.task_number}"><i class="la la-cloud-download"></i>` + self.$t("Gantt Chart View (All)") + `</a>`;
            var calendar_view_menu = `<a class="dropdown-item calendar-view" href="#" task_number="${row.task_number}"><i class="la la-cloud-download"></i>` + self.$t("Calendar View") + `</a>`

            //Project menus
            var gantt_milestone_menu = `<a class="dropdown-item gantt-milestone" href="#" task_number="${row.task_number}"><i class="la la-cloud-download"></i>` + self.$t("Go to Milestone") + `</a>`;
            var ai_analysis_project_menu = arr.length === 1 ? `<a class="dropdown-item gantt-ai-analysis" href="#" task_number="${row.task_number}"><i class="la la-cloud-download"></i>` + self.$t("Ai Analysis") + `</a>` : "";
            
            
            var content = `
                <div class="dropdown SWDropdown" inc_id="${row.task_number}">
                <button class="btn caption" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <i class="fas fa-ellipsis-v"></i>
                </button>
                <div class="dropdown-menu control dropdown-scroll scrollbar gantt-operation-dropdown" aria-labelledby="dropdownMenuButton">
                    
                    <!-- View group -->
                    <h6 class="dropdown-header">${self.$t('View')}</h6>
                    ${gantt_view_menu}
                    ${gantt_view_all_menu}
                    ${calendar_view_menu}
                    <div class="dropdown-divider"></div>
                    
                    <h6 class="dropdown-header">${self.$t('Project')}</h6>
                    ${gantt_milestone_menu}
                    ${ai_analysis_project_menu}
                    <div class="dropdown-divider"></div>                    

                    <!-- Session group -->
                    ${arr.length == 2 ? '<h6 class="dropdown-header">' + self.$t('Session') + '</h6>' :''}
                    ${edit_session_menu}
                    ${del_session_menu}
                    ${show_session_task_menu}
                    ${goto_requirement_menu}
                    ${gantt_summary_menu}
                    ${ai_analysis_session_menu}
                    ${arr.length == 2 ? '<div class="dropdown-divider"></div>' :''}

                    <!-- Task group -->
                    <h6 class="dropdown-header">${self.$t('Gantt Task Group')}</h6>
                    ${addtask_menu}
                    ${edit_menu}
                    ${tasklist_view_menu}
                </div>
                </div>`;
                
            return content;
            }
        }
      ],
      currentLanguage:"",
      dataSource: [],
      ganttDataSource: [],
      ganttCustomOptions: {
        custom_popup_html: function(task) {
            const startDate = new Date(task.start);
            const endDate = new Date(task.end);
            const duration = Math.round((endDate - startDate) / (1000 * 60 * 60 * 24)) + 1; // 四舍五入并加1以包含开始日期
            const startDateStr = moment(task.start).format("MMM D");
            const endDateStr = moment(task.end).format("MMM D");
            return `
            <div class="details-container">
                <h5>${task.name}: ${startDateStr} - ${endDateStr}</h5>
                <p>Duration: ${duration} days</p>
            </div>
            `;
        }     
      },
      ganttGetDesc(item){
        var arr = item.task_number.split("-");
        if (arr.length == 2) { //如果是Session則顯示用戶名，end date, 進度15/20
            var desc = item.task_description || '';
            var contact = item.contact || "";
            var endDate = item.plan_end == null || item.plan_end == undefined ? "" : moment(item.plan_end).format("MMM D");
            desc = "{0}({1}, {2}, {3}%)[{4}-{5}]".format(desc, contact, endDate, item.progress, arr[0], arr[1]);
            return desc;
        }else if (arr.length == 3) {
            var contact = item.contact || "";
            var desc = item.task_description || '';
            desc = "{0}({1})[{2}]".format(desc,contact, arr[2]);
            return desc;
        }
        else
            return item.task_description || '';
      },
      ganttExtendedFields:['inc_id','show_all_tasks'],
      calendarDataSource:[],
      taskColumns:[
            { field: "taskno", label: gettext('TaskNo')},
            { field: "task", label: gettext('Task'), width: SWApp.os.isMobile || SWApp.os.isTablet ? "16rem" : ''},
            { field: "contact", label: gettext('Contact') },
            { field: "planbdate", label: gettext('PlanBDate'), render:DateRender},
            { field: "edate", label: gettext('EDate'), render:DateRender},
            { field: "schpriority", label: gettext('SchPriority'), visible:false},
            { field: "progress", label: gettext('Progress'), width: "8%"},            
            {field:"priority", label:gettext("priority")},
            {field:"class_field", label:gettext("Class")},
            {field:"inc_id", label:"inc_id", visible:false},
      ],
      task_custom_options:{
        responsive: false,
        scrollX: true,
        scrollY: 400,
        deferLoading: 0,
        autoWidth: false,
      },      
      calendarExtendedFields:['task_number'],
      sessionID: '',
    };
  },
  created() {
    var self = this;
    const urlParams = new URLSearchParams(window.location.search);
    const showGanttPdf = urlParams.get('show_gantt_chat_pdf');
    
    if (showGanttPdf)
      this.loading_pdf = true;

    this.getPartUserNames();
    this.getTaskProgress();
    window.setTimeout(function () {
      $(".status_select").selectpicker("refresh");
    }, 2000);
  },
  mounted() {
    this.bind_event()
    var recordid = getParamFromUrl('recordid');
    var sessionid = getParamFromUrl('sessionid');
    if (recordid && sessionid){
      this.queryRecordId = recordid;
      this.sessionID = sessionid;
      this.fetchData(false)
    }else if (recordid){
      this.queryRecordId = recordid;
      this.fetchData(false)
    }
    
    // $(".editSessionForm .modal-body select").selectpicker('refresh'); 
    this.$nextTick(function(){
      $("title").html(this.$t("Gantt Chat"));
    })
    this.$nextTick(function(){
      this.addTranslateMenu();
    })
  },
  methods: {
    treeGridLoad() {
      this.addTreeGridTranslateMenu();
    },    
    addTreeGridTranslateMenu() {
      var self = this;
      var html = `    
        <div class="btn-group mr-3 align-items-center">
          <label class="col-form-label caption col-auto pl-0 pr-2">`+this.$t("Language")+`</label>
          <select class="ai-tree-translate-menu control col px-0" data-toggle="selectpicker" data-width="100px" data-size="5"
            data-none-selected-text data-container="body">
            <option></option>
            <option value="Chinese">`+ this.$t("Chinese") + `</option>
            <option value="English">`+ this.$t("English") + `</option>
            <option value="Vietnamese">`+ this.$t("Vietnamese") + `</option>
          </select>
        </div>`
      if ($(".LPTreegrid .fixed-table-toolbar .columns-right .ai-tree-translate-menu").length === 0) {
        $(".LPTreegrid .fixed-table-toolbar .columns-right").prepend(html);
        $(".ai-tree-translate-menu").val(this.currentLanguage);
        $(".ai-tree-translate-menu").selectpicker("refresh");
        $("#app").off("change", ".LPTreegrid .fixed-table-toolbar .columns-right select.ai-tree-translate-menu").on("change", ".LPTreegrid .fixed-table-toolbar .columns-right select.ai-tree-translate-menu", function(e){
          var language = $(this).val()
          if (language != "") 
            self.treeTranslate(language)
          else
            self.fetchData(false)
        });
      }else {
        $(".ai-translate-menu").val(this.currentLanguage);
        $(".ai-translate-menu").selectpicker("refresh");
      }
    },    
    addTranslateMenu() {
      var self = this;
      var html = `    
        <div class="btn-group ml-1 align-items-center">
          <label class="col-form-label caption col-auto pl-0 pr-2 d-none d-md-block">`+this.$t("Language")+`</label>
          <label class="col-form-label caption col-auto pl-0 pr-2 d-block d-md-none"">`+this.$t("Lng")+`</label>
          <select class="ai-translate-menu control col px-0" data-toggle="selectpicker" data-width="100px" data-size="5"
            data-none-selected-text data-container="body">
            <option></option>
            <option value="Chinese">`+ this.$t("Chinese") + `</option>
            <option value="English">`+ this.$t("English") + `</option>
            <option value="Vietnamese">`+ this.$t("Vietnamese") + `</option>
          </select>
        </div>
        <div class="ml-2">
        <button type="button" class="btn btn-primary gantt_print_report">
          <span class="d-none d-md-inline">` + this.$t("Print PDF")+`</span>
            <span class="d-md-none">
              <i class="fas fa-file-pdf"></i>
            </span>          
          </button>
        </div>         
        `
      if ($(".LPGantt_container .btn-group-toggle .ai-translate-menu").length === 0) {
        $(".LPGantt_container .btn-group-toggle").append(html);
        $(".ai-translate-menu").val("");
        $(".ai-translate-menu").selectpicker("refresh");
        $("body").off("click", ".ai-translate-menu .dropdown-item").on("click", ".ai-translate-menu .dropdown-item", function(e){
          var language = $(".LPGantt_container select.ai-translate-menu").val()
          self.translate(language);
        });
        $("body").off("click", ".gantt_print_report").on("click", ".gantt_print_report", function(e){
          self.print_report()
        })        
      }else {
        $(".ai-translate-menu").val("");
        $(".ai-translate-menu").selectpicker("refresh");
      }
    },
    bind_event() {
      var self = this;
      $("#app").on("click", ".gantt-view", function(e){
        e.preventDefault();
        var task_number = $(this).attr("task_number");
        self.showGantt(task_number);
      });
      $("#app").on("click", ".gantt-view-all", function(e){
          e.preventDefault();
          var task_number = $(this).attr("task_number");
          self.showGantt(task_number, true);
      });
      
      $("#app").on("click", ".gantt-milestone", function(e){
        e.preventDefault();
        var task_number = $(this).attr("task_number");
        self.gotoMilestone(task_number);
      });
      $("#app").on("click", ".gantt-summary", function(e){
        e.preventDefault();
        var task_number = $(this).attr("task_number");
        self.gotoSummary(task_number);
      });
            
      $("#app").on("click", ".calendar-view", function(e){
        e.preventDefault();
        var task_number = $(this).attr("task_number");
        self.showCalendar(task_number);
      });
      $("#app").on("click", ".tasklist-view", function(e){
        e.preventDefault();
        var task_number = $(this).attr("task_number");
        self.showTaskListView(task_number);
      });
      $("#app").on("click", ".addtask-view", function(e){
        e.preventDefault();
        var task_number = $(this).attr("task_number");
        self.addTask(task_number);
      });
      $("#app").on("click", ".edit-view", function(e){
        e.preventDefault();
        var inc_id = $(this).attr("inc_id");
        var task_number = $(this).attr("task_number");
        var arr = task_number.split("-")
        var params = { sessionid: `{0}-{1}`.format(arr[0],arr[1])}
        self.editTask(inc_id, params);
      });
      $("#app").on("click", ".edit-session", function(e){
        e.preventDefault();
        var task_number = $(this).attr("task_number");
        var arr = task_number.split("-")
        self.showEditSession(arr[0], arr[1]);
      });
      $("#app").on("click", ".goto-requirement", function(e){
        e.preventDefault();
        var sessionid = $(this).attr("task_number");
        self.gotoRequirement(sessionid);
      });
      $("#app").on("click", ".show-session-task", function(e){
        e.preventDefault();
        var sessionid = $(this).attr("task_number");
        self.showSessionTasks(sessionid);
      });
      $("#app").on("click", ".del-session", function(e){
        e.preventDefault();
        var inc_id = $(this).attr("inc_id");
        self.delSession(inc_id);
      });
      $("#app").on("click", ".gantt-ai-analysis", function(e){
        e.preventDefault();
        var task_number = $(this).attr("task_number");
        self.aiAnalysis(task_number);
      });
      
    },
    gotoSummary(task_number) {
        axios.get("/project/project_milestone/get_project_summary_id", {params:{task_number:task_number}}).then((response)=>{
            var result = response.data;
            if (result.status) {
                setTimeout(() => {
                    window.open(`/chatwithai/project_status?id=${result.data}`)   
                });
            }else {
                alert("There is no project summary.")
            }
        })
    },
    getPartUserNames() {
        axios.get("/PMIS/user/get_part_user_names").then((response)=>{
            this.partUserNames = response.data.data;
        })
    },
    getTaskProgress() {
        axios.get("/PMIS/task/progresses").then((response)=>{
            this.taskProgress = response.data.data;
        })
    },
    gotoMilestone(task_number) {
        var numberArr = task_number.split("-");
        var sessions = new Set([])
        if (numberArr.length != 1) {
            var childrenData = this.$refs.tree_grid.getChildrenData(task_number)
            for (var row of childrenData) {
                var tnumber = row['task_number'];
                var nbArr = tnumber.split("-");
                if (nbArr.length == 2)
                    sessions.add(tnumber)
                else if (nbArr.length == 3)
                    sessions.add("{0}-{1}".format(nbArr[0], nbArr[1]))
            }
        }
        sessions = Array.from(sessions);
        axios.get("/project/project_milestone/get_milestone_info", {params:{task_number:task_number}}).then((response)=>{
            var result = response.data;
            if (result.status) {
                var recordid = result.data.recordid;
                var contact = result.data.contact;
                setTimeout(() => {
                    var url = "/looper/user/top5_projects?contact={0}&recordid={1}&shrink=true".format(contact, recordid)                
                    if (sessions.length > 0)
                        url = "{0}&sessions={1}".format(url, sessions.join(","))
                    window.open(url);
                });
            }else {
                alert("There is no milestone!");
            }
        });
    },
    fetchData(saveExpandedState=false) {
      if (this.queryRecordId == "")
        return;
      if (saveExpandedState==false)
        this.currentLanguage = "";
      var params = {record_id: this.queryRecordId};
      if (this.queryRecordId !=='' && this.sessionID !== '')
        params = {record_id: this.queryRecordId, session_id: this.sessionID};
      axios.get("/project/project_milestone/get_session_and_task", {params:params}).then((response)=>{
        var result = response.data;
        if (result.status) {
          this.dataSource = result.data
          this.$nextTick(function () {
              this.$refs.tree_grid.reLoad(saveExpandedState);   //重新加載控件      
              this.notifyComponentLoaded("TreeGrid");
          })
        }else {
          alert(gettext("get data fail!"))
        }
      });
    },
    getTaskAndSubtasks(taskNumber, targetDataSource) {
      const result = [];
      if (targetDataSource == undefined)
        targetDataSource = this.dataSource;
      const findTasks = (tasks, parentTaskNumber, parent_level_num) => {
        tasks.forEach(task => {
          if (task.parent === parentTaskNumber) {
            task['level_num'] = parent_level_num + 1;
            result.push(task);
            findTasks(tasks, task.task_number, task['level_num']);
          }
        });
      };

      // 先找到根任务
      const rootTask = targetDataSource.find(task => task.task_number === taskNumber);
      if (rootTask) {
        rootTask['level_num'] = 0;
        result.push(rootTask);
        findTasks(targetDataSource, taskNumber, 0);
      }

      return result;
    },
    showCalendar(taskNumber) {
        var self = this;
        this.$refs.calendarModal.show();
        $(this.$refs.calendarModal.$refs.modal).off("shown.bs.modal");
        $(this.$refs.calendarModal.$refs.modal).on("shown.bs.modal", function(){
            self.calendarDataSource = self.getTaskAndSubtasks(taskNumber);        
            self.$nextTick(() => {
                self.$nextTick(()=>{
                    self.$refs.calendar.initCalendar();
                })
        });
      });        
    },
    showGantt(taskNumber, show_all_task=false) {
      //判斷是否需要從後臺刷新數據，如果當前數據為Project或Session，
      //取得當前數據中的show_all_task是否與參數show_all_task不一致
      //如果不一致則需要刷新數據
      // 先找到根任务
      //將語言恢復默認值
      $(".ai-translate-menu").val("");
      $(".ai-translate-menu").selectpicker("refresh");            
      var self = this;
      var refreshDataPromise = new Promise((resolve, reject)=>{
        var arr = taskNumber.split("-");
        if (arr.length <= 2) {
            const currentData = this.dataSource.find(task => task.task_number === taskNumber);
            var subTasks = this.getTaskAndSubtasks(taskNumber);  
            var subTasksFilter = subTasks.filter(x=>x.show_all_task == show_all_task)
            if(subTasksFilter.length != subTasks.length) { //判斷是否當前層和所有下層的show_all_task與參數中的一致，如果不一致則需要刷新數據
                var sessions = subTasks.filter((x)=>x.data_type== 2)
                var sessionids = sessions.map(x=>x.task_number);
                var url ="project/project_milestone/get_session_tasks"
                axios.post(url, self.objectToFormData({sessionids:sessionids.join(","), show_all_task:show_all_task})).then((response)=>{
                var result = response.data;
                if (result.status) {
                    //更新現有數據的show_all_task的狀態
                    subTasks.forEach(item => {
                        item.show_all_task = show_all_task;
                        item.progress = item.task_number in result.sessionProgress ? result.sessionProgress[item.task_number] : item.progress;
                    });
                    //刷新現有數據
                    var newDataSource = this.dataSource.filter(x => !(x.data_type ==3 && sessionids.indexOf(x.parent) != -1))
                    newDataSource.push(...result.data)
                    self.dataSource = newDataSource;                
                    self.$nextTick(function(){
                        self.$refs.tree_grid.reLoad(true);   //重新加載控件      
                        resolve(true);
                    })
                }else {
                    alert(gettext("get data fail!"))
                    resolve(false);
                }
                })      
            }else 
                resolve(true)
        }else
            resolve(true)
      })
      refreshDataPromise.then((status)=>{
        if (status) {
            // 获取甘特图数据
            self.ganttDataSource = self.getTaskAndSubtasks(taskNumber);
            self.currentGanttTaskNumber = taskNumber;
            self.$refs.ganttModal.show();
            self.$nextTick(() => {
                self.$nextTick(()=>{
                    self.$refs.gantt.initGantt();
                    self.$nextTick(()=>{
                        self.notifyComponentLoaded("Gantt");
                    })
                });
            });
        }
      });
    },
    showTaskListView(taskNumber) {
      this.$refs.taskModal.show();
      if(!(this.$refs.tasksDataTable.datatable == undefined))
            this.$refs.tasksDataTable.datatable.clear();
      var tasks = this.getTaskAndSubtasks(taskNumber);
      var sessions = new Set([]);
      for( var task of tasks) {
        var task_number = task['task_number'];
        var arr = task_number.split("-")
        if (arr.length == 2)
            sessions.add(task_number)
      }
      sessions = Array.from(sessions);
      axios.post("/project/project_milestone/get_tasks", this.objectToFormData({sessions:JSON.stringify(sessions), class1:true})).then((response)=>{
        var result = response.data;
        if (result.status) {  
          this.$refs.tasksDataTable.datatable.rows.add(result.data).draw();          
        }
      })        
    },
    addTask(taskNumber) {
        var arr = taskNumber.split("-");
        var sessionid = "{0}-{1}".format(arr[0], arr[1])
        init_task(undefined, {sessionid:sessionid});
        var self = this;
        jqueryEventBus.one('globalTaskOperation', function(event, result) {
            if (result == undefined)
                return;
            var method = result.method;
            if (method == "save") {
                self.fetchData(true);
            }
        });                
    },
    editTask(inc_id, params) {
        if (params != undefined)
          init_task(inc_id, params);
        else
          init_task(inc_id);
        var self = this;
        jqueryEventBus.one('globalTaskOperation', function(event, result) {
            if (result == undefined)
                return;
            var method = result.method;
            if (method == "save" || method == "del") {
                self.fetchData(true);
            }
        });                
    },
    showEditSession(pid,tid) {
        this.parentSessionDesp = "";
        this.parentSessionState = true;
        this.relationSessionDesp = "";
        var purl = `/PMIS/session/update?pid=${pid}&tid=${tid}`
        this.currentSession = {}
        this.$refs.sessionModal.$refs.modal.show();
        axios.get(purl).then((response)=>{
            var result = response.data;
            if (result.status) {
                this.currentSession = result.data;
                if(result.data.parent != null && result.data.parent != undefined)
                    this.checkParentSession(result.data.parent);
                if(result.data.relationsessionid != null && result.data.relationsessionid != undefined)
                    this.checkRelationSession(result.data.relationsessionid);
                this.$nextTick(function() {
                    $(".editSessionForm .modal-body select").selectpicker('refresh');                    
                })
            }
        })
    },
    objectToFormData(obj) {
        var fd = new FormData();
        for (let o in obj) {
            if(obj[o]){
                fd.append(o, obj[o]);
            }          
        }
        return fd;
    },    
    edit_session_submit_event(){
        var data = {
            pid:this.currentSession.pid, tid:this.currentSession.tid,
            planbdate:this.currentSession.planbdate, planedate:this.currentSession.planedate,
            contact:this.currentSession.contact, progress:this.currentSession.progress,
            parent:this.currentSession.parent,
            relationsessionid:this.currentSession.relationsessionid,
            relationstatus:this.currentSession.relationstatus
        }
        var self =this;
        return new Promise((resolve, reject)=>{
            this.checkParentSession(this.currentSession.parent).then((flag)=>{
                if (flag == false) {
                    alert(gettext('enter error parents Session'));
                }else {
                    this.checkRelationSession(this.currentSession.relationsessionid).then((sflag)=>{
                    if (sflag == false) {
                      alert(gettext('enter error relation Session'));
                    }else {
                      var formData = this.objectToFormData(data);
                      if (data.parent == "")
                          formData.append('parent', '');
                      axios.post(`/PMIS/session/update`, formData).then((response)=>{
                          var result = response;
                          if (result.status) {
                              alert(gettext('Success'));
                              resolve(true);
                              self.$nextTick(function(){
                                  self.fetchData(true);                            
                              })
                          }
                          else
                              alert(gettext('Fail'));
                      });
                    }
                    })
                }
            });
        })
    },
    ganttCustomClass(item) {
        var className = undefined;
        if (item.status) {
            switch(item.status) {
                case 'S':
                    className = 'bar-S';
                    break;
                case 'F':
                    className = 'bar-Finish';
                    break;
                case 'I':
                    className = 'bar-InGoing';
                    break;
                case 'C':
                    className = 'bar-Complete';
                    break;
                case 'N':
                    className = 'bar-Normal';
                    break;
                case 'H':
                    className = 'bar-Hold';
                    break;
                case 'T':
                    className = 'bar-Today';
                    break;
                case 'R':
                    className = 'bar-Reviews';
                    break;
                default:
                    className = undefined;
            }
        }else
            className = undefined;
        var levelClassName = "bar-level-{0}".format(item.level_num);
        if (item.task_number.split("-").length == 2)
          levelClassName += " session"        
        className = className == undefined ? levelClassName : className + " " + levelClassName;
        return className;
    },
    checkParentSession(sessionid) {
        var self = this;
        return new Promise((resolve, reject)=>{
            if (sessionid == undefined || sessionid == "" || sessionid == null) 
                resolve(true);
            else {
                var parent = sessionid.split("-")
                if (parent && parent.length != 2)
                    resolve(false)
                else {
                    var purl = `/PMIS/session/update?pid=${parent[0]}&tid=${parent[1]}`
                    axios.get(purl).then((response)=>{
                        var result = response.data;
                        if (result.status) {
                            self.parentSessionDesp = "{0}-{1} {2}".format(result.data.pid, result.data.tid, result.data.sdesp);
                            resolve(true);
                        }else {
                            self.parentSessionDesp = gettext('no session');
                            resolve(false);
                        }
                    });
                }
            }
        })
    },
    checkRelationSession(sessionid) {
        var self = this;
        return new Promise((resolve, reject)=>{
            if (sessionid == undefined || sessionid == "" || sessionid == null) 
                resolve(true);
            else {
                var parent = sessionid.split("-")
                if (parent && parent.length != 2)
                    resolve(false)
                else {
                    var purl = `/PMIS/session/update?pid=${parent[0]}&tid=${parent[1]}`
                    axios.get(purl).then((response)=>{
                        var result = response.data;
                        if (result.status) {
                            self.relationSessionDesp = "{0}-{1} {2}".format(result.data.pid, result.data.tid, result.data.sdesp);
                            resolve(true);
                        }else {
                            self.relationSessionDesp = gettext('no session');
                            resolve(false);
                        }
                    });
                }
            }
        })
    },    
    async gotoRequirement(sessionid){
        var recordid = await this.getRecordId(sessionid)
        setTimeout(() => {
            window.open(`/devplat/sessions?recordid=${recordid}&menu_id=mi_${sessionid}#Requirements`, "_blank");
        });
    },
    async showSessionTasks(sessionid) {
        var recordid = await this.getRecordId(sessionid)
        var relationInfo = await this.getSessionRelationInfo(sessionid);
        if (relationInfo !=undefined && relationInfo.recordid != null && relationInfo.relationsessionid != null) {
          setTimeout(() => {
            window.open(`/devplat/sessions?recordid=${relationInfo.recordid}&menu_id=mi_${relationInfo.relationsessionid}#Session_Tasks`, "_blank");
          });
        }
        setTimeout(() => {
            window.open(`/devplat/sessions?recordid=${recordid}&menu_id=mi_${sessionid}#Session_Tasks`, "_blank");
        });
    },
    getSessionRelationInfo(sessionid) {
      return new Promise((resolve,reject)=>{
            axios.get("/project/session/get_relation_info", {params:{sessionid:sessionid}}).then((response)=>{
            var result = response.data;
            if (result.status) {
                var recordid = result.data.recordid;
                var relationsessionid = result.data.relationsessionid;
                resolve({recordid:recordid, relationsessionid})
            }else
                resolve(undefined)
            });            
        })
    },
    getRecordId(sessionid) {
        return new Promise((resolve,reject)=>{
            axios.get("/project/project_milestone/get_milestone_info", {params:{task_number:sessionid}}).then((response)=>{
            var result = response.data;
            if (result.status) {
                var recordid = result.data.recordid;
                resolve(recordid)
            }else
                resolve(undefined)
            });            
        })
    },
    ganttEventDbClick(item) {
        var id = item.id;
        var arr = id.split("-")
        if (arr.length == 2) {
            this.showEditSession(arr[0], arr[1]);
        }else if (arr.length == 3) {
            var sessionid = `${arr[0]}-${arr[1]}`;
            var params = {sessionid:sessionid}
            this.editTask(item.extendedProps.inc_id, params);
        }
    },
    showSessionAllTasks(sessionid, show_all_task) {
      var subTasks = this.getTaskAndSubtasks(sessionid);  
      var sessions = subTasks.filter((x)=>x.data_type== 2)
      var sessionids = sessions.map(x=>x.task_number);
      var url ="project/project_milestone/get_session_tasks"
      var self = this;
      axios.get(url, {params:{sessionids:sessionids.join(","), show_all_task:show_all_task}}).then((response)=>{
        var result = response.data;
        if (result.status) {
          self.refreshTreeGridWithSessionTasks(result.data, sessionids);
        }else {
          alert(gettext("get data fail!"))
        }
      })
    },
    refreshTreeGridWithSessionTasks(tasks, sessionids, show_all_task) {
      var newDataSource = this.dataSource.filter(x => !(x.data_type ==3 && sessionids.indexOf(x.parent) != -1))
      newDataSource.push(...tasks)
      this.dataSource = newDataSource;
      this.$nextTick(function () {
          this.$refs.tree_grid.reLoad(true);   //重新加載控件      
      })
    },
    delSession(inc_id) {
        var flag = confirm("Are you sure you want to delete it?");
        var self = this;
        if (flag) {        
            axios.post(`/project/session/delete?pk=${inc_id}`).then((response)=>{
                var result = response.data;
                if (result.status) {
                    alert(gettext('Success'));
                    self.$nextTick(function(){
                        self.fetchData(true);                            
                    })                    
                }else {
                    if (result.msg != "" && result.msg != undefined && result.msg != null) {
                        if(typeUtils.isString(result.msg)) {
                            alert(result.msg);
                        }else {
                            var msg = result.msg[Object.keys(result.msg)[0]];
                            alert(msg);
                        }
                    }
                    else
                        alert(gettext('Fail'));
                }
            })
        }
    },
    aiAnalysis(task_number) {
      var tasks =  this.getTaskAndSubtasks(task_number);
      var datas = []
      for (var task of tasks) {
        var arr = task.task_number.split("-");
        if (arr.length != 3)
          continue;
        datas.push({
          taskno:task.task_number, 
          task:task.task_description, 
          contact:task.contact,
          planbdate:task.plan_start, 
          planedate:task.plan_end, 
          bdate:task.bdate,
          edate:task.edate,
          priority:task.priority,
          class:task.class_field,
          progress:task.status, 
          percentage_progress:task.progress,
          parent:task.parent,
          level:task._level
        })
      }
      this.aiPredefinedData = datas;
      this.$nextTick(function(){
        //this.$refs.aicombox.$refs.modal.width('800px')
        this.$refs.aicombox.$refs.modal.show()      
      })
    },
    translate(language) {
      if (language != "") {
          this.loading = true;        
          var data = this.getTaskAndSubtasks(this.currentGanttTaskNumber);        
          axios.post("/project/translate", this.objectToFormData({data:JSON.stringify(data), fields:JSON.stringify(['task_description']), target_language:language})).then((response)=>{
          this.loading = false;
          var result = response.data;
          if(result.status) {
            this.ganttDataSource = this.getTaskAndSubtasks(this.currentGanttTaskNumber, result.data)
            var viewModel = this.$refs.gantt.$data.viewMode;
            this.$refs.gantt.$data.options['view_mode'] = viewModel;
            this.$nextTick(() => {
                this.$nextTick(()=>{
                    this.$refs.gantt.initGantt();
                    this.$refs.gantt.$nextTick(()=>{
                      this.$refs.gantt.$data.options['view_mode'] = 'Day';
                    })
                });
            });            
          }else 
            alert(this.$t("Translation failed!"))
        })
      }else {
            this.ganttDataSource = this.getTaskAndSubtasks(this.currentGanttTaskNumber);
            var viewModel = this.$refs.gantt.$data.viewMode;
            this.$refs.gantt.$data.options['view_mode'] = viewModel;
            this.$nextTick(() => {
                this.$nextTick(()=>{
                    this.$refs.gantt.initGantt();
                    this.$refs.gantt.$nextTick(()=>{
                      this.$refs.gantt.$data.options['view_mode'] = 'Day';
                    })
                });
            });         
      }
    },
    treeTranslate(language) {
      this.currentLanguage = language;
      this.loading = true;
      axios.post("/project/translate", this.objectToFormData({data:JSON.stringify(this.dataSource), fields:JSON.stringify(['task_description']), target_language:language})).then((response)=>{
        this.loading = false;
        var result = response.data;
        if(result.status) {
          this.dataSource = result.data
          this.$nextTick(function () {
              this.$refs.tree_grid.reLoad(true);   //重新加載控件      
          })
        }else 
          alert(this.$t("Translation failed!"))
      }) 
    },          
    print_report(isDownload=true) {
      // 獲取該元素的ID
      if (this.ganttDataSource.length == 0)
        return;
      var item = this.ganttDataSource[0];
      var file_name = "Project progress"; //默認的文件名
      if (item.task_description != null && item.task_description != undefined && item.task_description != "") {
        file_name = `${file_name}(${item.task_number} - ${item.task_description})`;
      }
      var file_name = file_name.replace(/[/\\?%*:|"<>]/g, "_");      
      var self = this;
      var svg_print_promise = function() {
      return new Promise((resolve, reject)=>{
          const ganttId = self.$refs.gantt.$refs.gantt_svg.id;                
          var ganttContentElement = document.getElementById(ganttId);
          svgExport.downloadPdf(ganttContentElement, file_name, 
            {    
              isDownload:isDownload,
              onDone:function(fileData) {
                resolve(true);
                self.notifyComponentLoaded("PDF_File", file_name, fileData)
              },
              pdfOptions:{
                pdfTextFontFamily: "Microsoft YaHei",
                customFonts: [ 
                  { url: "/static/BaseApp/assets/fonts/MicrosoftYahei.ttf", fontName: "Microsoft YaHei" },
                  { url: "/static/BaseApp/assets/fonts/MicrosoftYahei-Bold.ttf", fontName: "Microsoft YaHei-Bold" },
                ]
              }       
            }
          )
        });
      }
      this.$refs.gantt.print(svg_print_promise);
    },
    notifyComponentLoaded(component_name, file_name, fileData) {
        if (this.loading_pdf) {
            const urlParams = new URLSearchParams(window.location.search);
            const showGanttPdf = urlParams.get('show_gantt_chat_pdf');
            const recordid = urlParams.get('recordid');
            const sessionid = urlParams.get('sessionid');
            var task_number = sessionid == null ? recordid : sessionid;
            if (component_name == "TreeGrid") {
                this.$refs.gantt.$data.options['view_mode'] = "Month";
                if (sessionid == null) //表示是Project
                  this.showGantt(task_number, false)
                else
                  this.showGantt(task_number, true);
            }else if (component_name == "Gantt") {
                this.print_report(false);
            }else if (component_name == "PDF_File") {
                // 将 fileData 转换为 Blob 对象
                var blob = new Blob([fileData], { type: "application/pdf" });

                // 创建 Blob URL
                var url = URL.createObjectURL(blob);     
                window.location.href=url;           
            }
        }
    }
  }
}
</script>

<style scoped>
/* 添加样式根据实际需求 */
/* 添加样式根据实际需求 */
>>>.LPGantt_container .gantt .bar-S .bar{
  fill: #0dfbfa !important; /* S 状态的颜色 */
}
>>>.LPGantt_container .gantt .bar-Finish .bar{
  fill: #5edf60 !important; /* Finish 状态的颜色 */
}
>>>.LPGantt_container .gantt .bar-InGoing .bar{
  fill:#f4fc0d !important; /* InGoing 状态的颜色 */
}
>>>.LPGantt_container .gantt .bar-Complete .bar{
  fill: #a99af0 !important; /* Complete 状态的颜色 */
}
>>>.LPGantt_container .gantt .bar-Normal .bar{
  fill: #f97d7c !important; /* Normal 状态的颜色 */
}
>>>.LPGantt_container .gantt .bar-Hold .bar{
  fill: #a09e9e !important; /* Hold 状态的颜色 */
}
>>>.LPGantt_container .gantt .bar-Today .bar{
  /*fill: #f97d7c !important;  Today 状态的颜色 */
  fill: #ff00a0 !important; /* Today 状态的颜色 */
}
>>>.LPGantt_container .gantt .bar-Reviews .bar{
  fill: #b76ba3 !important; /* Reviews 状态的颜色 */
}

>>>.LPGantt_container .gantt .bar-level-0 .bar-label{
    font-size: 16px;
    text-decoration: underline;
}
>>>.LPGantt_container .gantt .bar-level-1.session .bar{
    /*fill: #008500 !important;  第一層的顏色 */
    fill: #f6ad55 !important; /* 第一層的顏色 */
}

.query-section {
  margin-top: 10px;
  display: flex;
  align-items: center;
}

/* .query-section .form-group {
  margin-right: 10px;
} */

.query-section input {
  padding: 10px;
  font-size: 16px;
}

.query-section button {
  /* padding: 10px 20px; */
  font-size: 16px;
}

.LPTreegrid {
  padding-left: 10px;
  padding-right: 10px;
}
.loading-spinner {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1080;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  font-size: 18px;
  color: #333;
}
/* 遮掩层样式 */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.spinner {
  color: #333;
  font-size: 18px;
  font-weight: bold;
}
</style>

