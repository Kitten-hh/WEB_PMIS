<template>
  <!-- 模态框，用于显示甘特图 -->
  <div>
    <div v-if="loading" class="loading-spinner">
      {{ $t("Translating...") }}
    </div>     
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
  </div>
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
</template>

<script>
import axios from "axios";
import LPGantt from "@components/looper/general/LPGantt.vue";
import LPModalForm from "@components/looper/layout/LPModalForm.vue";
import LPLabelInput from "@components/looper/forms/LPLabelInput.vue";
export default {
  name: 'ProjectGanttModal',
  components: { LPGantt,LPModalForm,LPLabelInput },
  data() {
    var self = this;
    return {
      loading:false,
      queryRecordId:'',
      isall:false,
      currentSession:{},
      partUserNames:[],
      taskProgress:[],
      parentSessionDesp:"",
      relationSessionDesp:"",      
      currentGanttTaskNumber:"",
      dataSource:[],
      ganttDataSource: [],
      sessionID:'',
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
    };
  },
  created() {
    var self = this;
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
    this.isall = getParamFromUrl('isall') != undefined && getParamFromUrl('isall') == "true";
    if (recordid){
      this.queryRecordId = recordid;
      if(sessionid){
        this.sessionID = sessionid;
      }
      this.fetchData(false)
    }
    // $(".editSessionForm .modal-body select").selectpicker('refresh'); 
    this.$nextTick(function(){
      $("title").html(this.$t("Gantt Chat"));
      this.addTranslateMenu();
    })       
  },
  methods: {
    bind_event() {
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
        </div>`
      if ($(".LPGantt_container .btn-group-toggle .ai-translate-menu").length === 0) {
        $(".LPGantt_container .btn-group-toggle").append(html);
        $(".ai-translate-menu").val("");
        $(".ai-translate-menu").selectpicker("refresh");
        $("body").off("click", ".ai-translate-menu .dropdown-item").on("click", ".ai-translate-menu .dropdown-item", function(e){
          var language = $(".LPGantt_container select.ai-translate-menu").val()
          self.translate(language);
        });
      }else {
        $(".ai-translate-menu").val("");
        $(".ai-translate-menu").selectpicker("refresh");
      }
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
    fetchData(saveExpandedState=false) {
      if (this.queryRecordId == "")
        return;
      var params = {record_id: this.queryRecordId};
      if (this.queryRecordId !=='' && this.sessionID !== '')
        params = {record_id: this.queryRecordId, session_id: this.sessionID};
      axios.get("/project/project_milestone/get_session_and_task", {params:params}).then((response)=>{
        var result = response.data;
        if (result.status) {
          this.dataSource = result.data
          this.$nextTick(function () {
              if(this.sessionID){
                this.showGantt(this.sessionID, true);
              }else{
                this.showGantt(this.queryRecordId, this.isall);
              }
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
            self.$nextTick(() => {
                self.$nextTick(()=>{
                    self.$refs.gantt.initGantt();
                });
            });
        }
      });
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
    editTask(inc_id) {
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
    ganttEventDbClick(item) {
        var id = item.id;
        var arr = id.split("-")
        if (arr.length == 2) {
            this.showEditSession(arr[0], arr[1]);
        }else if (arr.length == 3) {
            this.editTask(item.extendedProps.inc_id);
        }
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
      translate(language) {
      var data = this.getTaskAndSubtasks(this.currentGanttTaskNumber);
      if (language != "") {
          this.loading = true;
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
    }      
  },
};
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
  fill: #f97d7c !important;  /* Normal 状态的颜色 */
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
</style>

