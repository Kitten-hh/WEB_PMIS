<template>

    <LPButton
    :text="'新增'"
    @on_click="add_click"
    />
    <LPDataTable
        :paging="true"
        :columns="MMaster_columns"
        datasource="MettingmasterView"
        :custom_params_fun="MMaster_params_fun"
        :pageLength="10"
        @on_row_click="on_row_click"
        ref="MettingMasterTable"
    />

    
    <LPModalForm
        ref="edit_form"
        :title="Modal_title"
        @on_submit="submitForm"
    >
        <div class="margin-t-32">
            <div class="form-group row">
                <div class="form-group col-12" hidden>
                    <div class="form-inline container">
                        <label class="col-form-label text-lg-right col-3">主鍵值</label>
                        <div class="col-lg-8">
                            <input v-model="MMasterData.inc_id" readonly="readonly" class="form-control " style="min-width:100%;">
                        </div>
                    </div>
                </div>
                <div class="form-group col-12" hidden>
                    <div class="form-inline container">
                        <label class="col-form-label text-lg-right col-3">會議ID</label>
                        <div class="col-lg-8">
                            <input v-model="MMasterData.id" readonly="readonly" class="form-control " style="min-width:100%;">
                        </div>
                    </div>
                </div>
                <div class="form-group col-12">
                </div>
                <div class="form-group col-12">
                    <div class="form-inline container">
                        <label class="col-form-label text-lg-right col-3">參會人員</label>
                        <div class="col-lg-8">
                            <input  v-model="MMasterData.participants" class="form-control " style="min-width:100%;">
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </LPModalForm>
</template>
    
<script>
    import axios from "axios";
    import LPDataTable, {DateRender} from "@components/looper/tables/LPDataTable.vue";
    import LPButton from "@components/looper/general/LPButton.vue";
    import LPModalForm from "@components/looper/layout/LPModalForm.vue";
    
    export default {
        //定義頁面控件的名稱為index
        name: 'MettingDataTable',
        components:{
            LPDataTable,
            LPButton,
            LPModalForm,
        },
        data() {
            return {
                //MettingMasterTable的過濾函數（如果有需要對數據進行過濾的話，需要定義）
                MMaster_params_fun: Function,      
                //MettingMasterTable的Columns對象
                MMaster_columns: [
                    { field: "inc_id", label: "inc_id", visible: false },
                    { field: "id", label: "會議ID" },
                    { field: "topic", label: "主題" },
                    { field: "participants", label: "參會人員" },
                    { field: "mustread", label: "必讀材料" },
                    {
                        field: null,
                        label: "操作",
                        render: function(data, type, row, meta) {
                            var inc_id = data.inc_id;
                            return `<div class="row"><a class="btn btn-edit btn-sm btn-icon btn-secondary" href="#" id="update${inc_id}" ><i class="fa fa-pencil-alt"></i></a>
                                            <a class="btn del-btn btn-sm btn-icon btn-secondary" href="#" id="delete${inc_id}" ><i class="far fa-trash-alt"></i></a></div>`;
                        }
                    }
                ],
                
                //會議記錄單頭
                MMasterData : {
                    id:'',//會議ID
                    topic:'',//主題
                    participants:'',//參會人員
                    mustread:'',//必讀材料
                    inc_id:'',
                },
                Modal_title:'新增會議'
            }
        },
        methods: {
            //把對象轉成FormData
            objectToFormData(obj){
                let fd = new FormData();
                for (let o in obj) {
                    if(obj[o]){
                        fd.append(o, obj[o]);
                    }          
                }
                return fd;
            },
            getMettingMaster(){
                var self = this;
                // 定義過濾函數
                this.MMaster_params_fun = function() {
                    let attach_query = {
                    attach_query: `{"condition":"AND","rules":[{"id":"custno","field":"custno","type":"string","input":"text",
                            "operator":"contains","value":"${self.currentClient.custno}"}],"not":false,"valid":true}`
                    };
                    return attach_query;
                };
                // 刷新LPDataTable數據
                this.$nextTick(function(){
                    this.$refs.MettingMasterTable.datatable.search('').draw();
                });
            },
            //新增按鈕點擊事件
            add_click() {
                //獲取會議記錄默認值 
                axios
                    .get(`/looper/metting/MettingmasterCreateView?contact=${get_username()}`)
                    .then(response => {
                        // 處理成功後的返回數據
                        this.MMasterData = response.data.data;
                        this.submitForm()
                    })
                    .catch(error => {
                        console.log(error);
                    });
            },
            //datatable行點擊事件
            on_row_click(event, data) {
                //對表頭table中的行點擊進行了事件委托處理,判斷點擊的元素並執行相應的函數
                var Element = event.target.tagName;
                var target = event.target.className;
                if (Element == "A" || Element == "I") {
                    event.preventDefault();
                    if (target.includes("fa-pencil") || target.includes("btn-edit")) {
                        window.open(`http://222.118.20.236:8033/zh-hans/looper/metting/MettingMaster_Add?id=${data.id}`)
                    }
                    if (target.includes("fa-trash") || target.includes("del-btn")) {
                        this.DeleteClick(data);
                    }
                }
            },
            //會議記錄信息刪除事件
            DeleteClick(data) {
                var flag = confirm("你確定要刪除該記錄嗎?");
                var self = this;
                if (flag) {
                    var id = data.inc_id;
                    var url = `/looper/metting/MettingmasterDeleteView/${id}`;
                    axios
                    .post(url)
                    .then(response => {
                        if (response.data.status && response.data.other){
                            alert("刪除成功!");
                            this.$refs.MettingMasterTable.setDraw(false, 0);
                        }
                    })
                    .catch(error => {
                    console.log(error);
                    });
                }
            },
            
            //保存產品屬性值
            async submitForm() {
                console.log(this.objectToFormData(this.MMasterData))
                axios
                    .post('/looper/metting/MettingmasterCreateView',this.objectToFormData(this.MMasterData))
                    .then(response => {
                        // debugger
                        // 處理成功後的返回數據
                        if(response.data.status){
                            window.open(`/looper/metting/MettingMaster_Add?id=${response.data.data.instance.id}`)
                            this.MMasterData = {
                                id:'',//會議ID
                                topic:'',//主題
                                participants:'',//參會人員
                                mustread:'',//必讀材料
                                inc_id:'',
                            }
                            this.$refs.MettingMasterTable.setDraw(false, 0);
                        }
                    })
                    .catch(error => {
                    console.log(error);
                    });
            },
        }
    }
</script>