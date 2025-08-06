<script>
import TaskDashboard_vueFrm_Tools from './TaskDashboard_Tools.vue'
import {toRaw} from 'vue'
import axios from 'axios'
export default {
    name:"TaskDashboard_vueFrm",
    extends:TaskDashboard_vueFrm_Tools,
    data() {
        return {
            DASHBOARD_SYSPARA_TASK:"DashBoardTask", //默認顯示的Dashboard Model
            DASHBOARD_SYSPARA_PROJECT:"DashBoardPro",
            dashBoardParaModel:{},
            usernames:[],
            currentContact:"",
            currentDashBoardModel:"",
            dashBoardParas:[],
            projectDashBoardSubProject:{}
        }
    },
    created() {

    },
    mounted() {
        this.$eventBus.on("changeProject", this.changeProject)
    },
    created() {
        Promise.all([this.getDashBoardParas(), this.getCurrentPMSUserDailyQueryAllUser()]).then((value)=>{
            this.getDashboard(true)
        })
    },
    methods:{
        getDashBoardParas() {
            return axios.get("/looper/task_dashboard/get_data", {params:{method:"initSyspara"}}).then((response)=>{
                var result = response.data;
                if (result.status) {
                    this.dashBoardParaModel = result.data
                    this.currentDashBoardModel = this.getDashBoardModelName(this.DASHBOARD_SYSPARA_TASK)
                }else {
                    alert(gettext("Init dashboard fail!"))
                }
            });
        },
        changeProject(project) {
            this.projectDashBoardSubProject = project;
            this.setProjectParam();
            this.$eventBus.emit("afterProjectChange");
        },
        setProjectParam() {
            this.dashBoardParam["PID"] = this.projectDashBoardSubProject.projectid;
            this.dashBoardParam["TID"] = "";
            if(this.projectDashBoardSubProject && this.projectDashBoardSubProject.filter){
                this.dashBoardParam["FITLER"] = this.projectDashBoardSubProject.filter;
            }else{
                this.dashBoardParam["FITLER"] = "1=1";
            }
            if(this.projectDashBoardSubProject && this.projectDashBoardSubProject.recordid){
                this.dashBoardParam["RECORDID"] = this.projectDashBoardSubProject.recordid;
            }else{
                this.dashBoardParam["RECORDID"] = "1=1";
            }
		},
        //獲取Task看板聯系人
        getCurrentPMSUserDailyQueryAllUser() {
            return axios.get("/looper/task_dashboard/get_data", {params:{method:"getAllUsers"}}).then((response)=>{
                var result = response.data;
                var user = get_username().toUpperCase();
                if (result.status) {
                    this.usernames = result.data;
                    for(var username of this.usernames) {
                        if (username.toUpperCase() == user) {
                            this.currentContact = username;
                            break;
                        }   
                    }
                }else {
                    alert(gettext("Init dashboard fail!"))
                }
            });
        },
        getDashboard(changeParam=false) {
            if (changeParam) {
                for (var key of Object.keys(this.dashBoardParam)) {
                    delete this.dashBoardParam[key];
                }
                this.dashBoardParam['USERNAME'] = this.currentContact;
                this.dashBoardParam['PID'] = "";
                this.dashBoardParam['TID'] = "";
            }            
            if (this.currentDashBoardModel)
                axios.get("/looper/task_dashboard/get_data", {params:{method:"getDashBoardPara",dashBoardModel:this.currentDashBoardModel}}).then((response)=>{
                    var result = response.data;
                    if (result.status) {
                        this.dashBoardParas = this.handleDashboardPara(result.data);
                        this.$nextTick(function(){
                            this.cardArea();
                        });
                        //取消afterProjectChange全局事件， 因為重新加載Dashboard將導致全局事件重覆
                        this.$eventBus.off("afterProjectChange");
                        if (result.data == null || result.data.length == 0) {
                            alert(gettext("notContactCondition"));
                        }
                    }else {
                        alert(gettext("Get dashboard params fail!"))
                    }
                });
        },

    },
    watch: {
        currentContact: function(value) {
            this.dashBoardParas = [];
            this.$nextTick(function(){
                this.getDashboard(true);
            });
            
        },
        currentDashBoardModel:function(value) {
            this.dashBoardParas = [];
            this.$nextTick(function(){
                this.getDashboard(true);
            });
        }
    }   
}
</script>
