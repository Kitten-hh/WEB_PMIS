<template>
  <LPCard>
    <template v-slot:header> 
        <div class="float-l">
            <h5 class="title" v-html="title"></h5>
        </div>
    </template>
    <template v-slot:body>
        <div id="mettingForm">
            <div class="form-group col-3">
                <div class="form-inline">
                    <label class="col-form-label text-lg-right col-lg-3">Metting ID</label>
                    <div class="col-lg-9">
                        <input v-model="strid" name="id" readonly class="form-control " style="min-width:100%;">
                    </div>
                </div>
            </div>
            <form v-for="(task, index) in tasks" :key="index" @submit.prevent="submitForm(task,index)">
                <div>
                    <div>
                        <div class="form-group" name="search_list">
                            <div class="form-group col-3">
                                <div class="form-inline">
                                    <label class="col-form-label text-lg-right col-lg-3" v-html="username"></label>
                                    <div class="col-lg-9" id="describe">
                                        <textarea v-model="task.task" name="task" @keyup="delayUpdate(task, index)" @keypress="delayUpdate(task, index)" 
                                        @paste="delayUpdate(task,index)"  @input="delayUpdate(task,index)"  cols="85" rows="3"></textarea>
                                    </div>
                                </div>
                            </div>

                        </div>
                    </div>
                </div>
            </form>         
            <button type="button" class="btn btn-primary" @click="addSubject(true)">Add Subject</button>
            <div id="othercontact">
                <div v-for="(items, username, index) in otherTasks" :key="index">

                    <div v-for="(item, sub_index) in items" :key="sub_index" class="form-group col-3">
                        <div class="form-inline">
                            <label class="col-form-label text-lg-right col-lg-3">{{username}}</label>
                            <div class="col-lg-9" id="describe">
                                <textarea v-model="item.task" readonly cols="85" rows="3"></textarea>
                            </div>
                        </div>
                    </div>
                </div>
            </div>       
        </div>
    </template>
  </LPCard>
</template>

<script>
import axios from "axios";
import LPDataTable, {DateRender} from "@components/looper/tables/LPDataTable.vue";
import LPCard from "@components/looper/layout/LPCard.vue";
import LPModalForm from "@components/looper/layout/LPModalForm.vue";
import LPModal from "@components/looper/layout/LPModal.vue";

export default {
    name: "MettingMaster_Add",
    components: {
        LPDataTable,
        LPCard,
        LPModalForm,
        LPModal,
    },

    data() {
        return {
            //登錄用戶名
            username:get_username(),
            //會議ID
            strid:'',
            //參會人員
            participants:[],
            //窗口標題
            title:'會議記錄',
            //登錄人員會議記錄
            tasks:[],
            //其他參會人員會議記錄
            otherTasks:{},
            //更新數據定時
            updateTime:{},
        };
    },
    created(){
        this.init_params()
        this.init_metting_item()
        this.init_timer();
    },
    methods: {
        //初始化獲取參數
        init_params(){
            //获取參數會議ID和參會人員
            this.strid = getParamFromUrl("id");
        },
        //初始化獲取會議記錄詳情
        init_metting_item() {
            var self = this;
            //獲取用戶會議記錄信息
            axios
                .get(`/looper/metting/get_metting_item`,{params:{id:this.strid}})
                .then(response => {
                    //若存在會議記錄則顯示，否則默認創建三條會議記錄輸入框
                    if(response.data.status){
                        if (response.data.data[this.username] != undefined)
                            response.data.data[this.username].forEach((strkey, index)=>{
                                this.tasks.push(strkey)
                            });
                        else {
                            for(var i =0; i < 3; i++){
                                this.addSubject(false)
                            }
                        }
                        if (Object.keys(response.data.data).length > 0) {
                            delete response.data.data[this.username];
                            this.otherTasks = response.data.data;
                        }
                    }
                })
            
        },
        //初始化獲取其他用戶會議記錄定時器
        init_timer() {
            var self = this
            setInterval(() => {
                self.getOtherMettingItem()
            }, 5000)                
        },
        //保存會議記錄
        async submitForm(task,index) {
            // 把對象轉成FormData對象
            task.contact = this.username
            task.docpath = this.strid
            let data = this.objectToFormData(task)
            //當會議記錄存在inc_id字段值時表示該數據已保存過
            if(task.inc_id!='' && task.inc_id!=null && task.inc_id!=undefined){
                this.update_MettingItem(data,task.inc_id,index)
            }else{
                this.create_MettingItem(data,index)
            }
        },
        //新增會議記錄數據
        create_MettingItem(data,index){
            // 使用axios的post方式調用以上發布的CreateView
            axios
                .post(`/PMIS/task/add_task`,data)
                .then(response => {
                    // 處理成功後的返回數據
                    if(response.data.status){
                        this.tasks[index]=response.data.data.instance;
                        console.log('新增成功！')
                    }
                })
                .catch(error => {
                console.log(error);
                });
        },
        //修改會議記錄數據
        update_MettingItem(data,inc_id){
            // 使用axios的post方式調用以上發布的UpdateView
            axios
                .post(`/PMIS/task/update_task?pk=${inc_id}`,data)
                .then(response => {
                    // 處理成功後的返回數據
                    if(response.data.status){
                        console.log('修改成功！')
                    }
                })
                .catch(error => {
                console.log(error);
                });
        },
        //增加輸入框
        addSubject(IsSave){
            axios
                .get('/PMIS/task/add_task',{params:{contact:this.username, sessionid:"00001-14004"}})
                .then(response => {
                    // 處理成功後的返回數據
                    if(response.data.status){
                        this.tasks.push(response.data.data)
                        //根據傳入的參數判斷是否要直接保存數據
                        if(IsSave){this.submitForm(response.data.data,this.tasks.length-1)}
                    }
                })
        },
        //textarea輸入框改變事件
        delayUpdate(task, index) {
            var self = this;
            if (index in this.updateTime) {
                clearTimeout(this.updateTime[index]);
                this.updateTime[index] = null;
            }
            this.updateTime[index] = setTimeout(() => {
                self.submitForm(task,index);
            }, 3000);            
        },
        //獲取其他參會人員會議記錄並展示
        async getOtherMettingItem(){
            axios
                .get(`/looper/metting/get_metting_item`,{params:{id:this.strid}})
                .then(response => {
                    if(response.data.status){
                        delete response.data.data[this.username];
                        this.otherTasks = response.data.data;
                    }
                })

        },
    }

};
</script>

<style>
</style>
