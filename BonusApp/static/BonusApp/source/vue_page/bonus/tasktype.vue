<template>
  <BlankPageLayout>
    <template v-slot:page-title-details>
      <h5>{{ $t('Lookup Task Type Management') }}</h5>
    </template>
    <template v-slot:page-Details>
      <div class="card">
        <div class="card-body">            
          <LPTreegrid
              ref="dt_tasktype"   
              id="treelist"
              :datasource="datasource"             
              :columns="tasktypeColumns"
              idField='tasktype'
              parentIdField='parenttype'               
          />
        </div>
      </div>
    </template>
  </BlankPageLayout>
  <LPModalForm
    :novalidate="true"
    ref="modalForm"
    @on_submit="submitModalForm"
  >
    <LPLabelInput :label="$t('Task Type')">
      <input
        type="text"
        class="form-control"
        v-model="currentObject.tasktype"        
        required
      >
    </LPLabelInput>     
    <LPLabelInput :label="$t('Description')">
      <textarea
        class="form-control scrollbar"
        v-model="currentObject.description"
        rows="3"
      ></textarea>
    </LPLabelInput> 
    <LPLabelInput :label="$t('Time')">
      <input
        type="text"
        class="form-control"
        v-model="currentObject.time" 
        required
      >
    </LPLabelInput>
    <LPLabelInput :label="$t('Score')">
      <input
        type="text"
        class="form-control"
        v-model="currentObject.score"
      >
    </LPLabelInput>  
    <LPLabelInput :label="$t('Diff1 Score')">
      <input
        type="text"
        class="form-control"
        v-model="currentObject.difficulties1"
      >      
    </LPLabelInput>  
    <LPLabelInput :label="$t('Diff2 Score')">
      <input
        type="text"
        class="form-control"
        v-model="currentObject.difficulties2"
      >      
    </LPLabelInput>
    <LPLabelInput :label="$t('Diff3 Score')">
      <input
        type="text"
        class="form-control"
        v-model="currentObject.difficulties3"
      >      
    </LPLabelInput> 
    <LPLabelInput :label="$t('Parent Type')">
      <input
        type="text"
        class="form-control"
        v-model="currentObject.parenttype"
      >      
    </LPLabelInput>
    <LPLabelInput :label="$t('Display Type')">
      <input
        type="text"
        class="form-control"
        v-model="currentObject.displaytype"
      >      
    </LPLabelInput>  
  </LPModalForm>
  <LPModal ref="SearchModal" title="查詢" class="col" id="SearchModal">
    <template v-slot:body>
      <!-- :gsearch_placeholder="a" -->
      <div class="row">
          <div class="form-group col-12">
              <label class="col-form-label caption">{{ $t('Task Type') }}</label>
              <input class="form-control control" type="text" name="tasktype" v-model="common_sea_params.tasktype">
          </div>
          <div class="form-group col-12">
              <label class="col-form-label caption">{{ $t('Description') }}</label>
              <input class="form-control control" type="text" name="description" v-model="common_sea_params.description">
          </div>
      </div>      
    </template>
    <template v-slot:footer>
      <button type="button" class="btn btn-primary" @click="search">{{ $t('Confirm') }}</button>
      <button type="button" class="btn btn-light" data-dismiss="modal">{{ $t('Close') }}</button>
    </template>
  </LPModal>
</template>
<script>
import axios from "axios";
import LPDataTable from "@components/looper/tables/LPDataTable.vue";
import LPTreegrid,{DateRender} from "@components/looper/tables/LPTreegrid.vue";
import LPModalForm from "@components/looper/layout/LPModalForm.vue";
import LPLabelInput from "@components/looper/forms/LPLabelInput.vue";
import BlankPageLayout from "@components/looper/layout/page/BlankPageLayout.vue";
import LPModal from "@components/looper/layout/LPModal.vue";
export default {
  name: "TaskType_vueFrm",
  components: {   
    LPDataTable,
    LPTreegrid,
    LPModalForm,
    LPModal,
    LPLabelInput,
    BlankPageLayout,
  },
  data() {
    return {
      currentObject: {},
      left_button:undefined,
      common_sea_params: {},  //共享條件
      datasource:[],
      tasktypeColumns: [
        { field: 'tasktype', label: this.$t('Task Type'),width:'100',
            render:(value, row, index) => {
                return '<span class="task-desp" id="' + row.inc_id + '">' + value + '</span>';
            }
        },              
        {field:'description',label: this.$t('Description'),width: '250',visible:true},
        {field:'time',label: this.$t('Time'),align: 'center',width:'40',visible:!SWApp.os.isMobile},
        {field:'score',label:this.$t('Score'),width:'40',visible:!SWApp.os.isMobile},
        {field:'difficulties1',label: this.$t('Diff1 Score'),width:'70', visible:!SWApp.os.isMobile},
        {field:'difficulties2',label: this.$t('Diff2 Score'),width:'70',visible:!SWApp.os.isMobile},   
        {field:'difficulties3',label: this.$t('Diff3 Score'),width:'70',visible:!SWApp.os.isMobile},  
        {field:'parenttype',label: this.$t('Parent Type'),width:'70',visible:!SWApp.os.isMobile}, 
        {field:'displaytype',label: this.$t('Display Type'),width:'70',visible:!SWApp.os.isMobile}, 
        {field:'operate',label: this.$t('Operation'),width:"30",
            render:function(value, row, index){    
                return `<div class="dropdown SWDropdown" inc_id="${row.inc_id}" tasktype="${row.tasktype}">
                <button class="btn caption" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><i class="fas fa-ellipsis-v"></i></button>  
                    <div class="dropdown-menu control" aria-labelledby="dropdownMenuButton">
                        <a class="dropdown-item edit" href="#" >` + gettext("Edit") + `</a>
                        <a class="dropdown-item delete" href="#">` + gettext("Delete") + `</a>
                        <a class="dropdown-item add" href="#">` + gettext("Add Task Type") + `</a>
                    </div>
                </div>` 
            }
        }   
      ],
    };
  },
  mounted() {
    this.reLoadTreegrid();
    this.listenButtonEvent();    
  },
  methods: {  
    listenButtonEvent(){        
        var self = this;
        //新增Tasktype
        $("#treelist").on("click",".add", function(e){
            e.preventDefault(); //阻止按鈕默認動作
            e.stopPropagation();
            var tasktype = $(this).closest(".SWDropdown").attr("tasktype");
            self.currentObject = {parenttype:tasktype}; 
            axios.get('/bonus/lstasktype/maxtasktype')
            .then((response)=>{
                var result = response.data;
                if(result.status){
                    self.currentObject.tasktype = result.data;
                    self.$refs.modalForm.title = "New";
                    self.$refs.modalForm.$refs.modal.show();
                }
            })           
            
        });    
        //刪除Tasktype
        $("#treelist").on("click", ".delete", function(e){
            e.preventDefault(); //阻止按鈕默認動作
            e.stopPropagation();
            var pk = $(this).closest(".SWDropdown").attr("inc_id");
            self.deleteTasktype(pk);
        });
        //修改Tasktype
        $("#treelist").on("click", ".edit", function(e){
            e.preventDefault(); //阻止按鈕默認動作
            e.stopPropagation();
            var pk = $(this).closest(".SWDropdown").attr("inc_id");
            axios.get('/bonus/lstasktype/update?pk='+pk)
            .then((response)=>{
                var result = response.data;
                if(result.status){
                    self.currentObject = result.data;
                    self.$refs.modalForm.title = "Modification";
                    self.$refs.modalForm.$refs.modal.show();
                }
            })
        });
    },
    //添加Treegrid左邊查詢按鈕
    addLeftMenu(id, icon, label) {
      var html_temp = `<div class="columns columns-left btn-group float-left">
          <div class="keep-open btn-group" title="Columns">
              <button class="btn btn-secondary" id="[[id]]" type="button" data-toggle="dropdown" aria-label="Columns" title="Columns">
                  <i class="[[icon]]"></i>
                  [[label]]
              </button>
          </div>
      </div>`;
      this.left_button = html_temp.render({"id":id, "icon":icon, "label":label});
      var self = this;
      this.$nextTick(function() {        
        $(".fixed-table-toolbar").append(self.left_button);
        $("#"+id).on("click",function(e){
          self.$refs.SearchModal.show();
        })
      })
    },
    //提交Tasktype的更新數據
    submitModalForm() {
      var self = this;
      var url = "/bonus/lstasktype/add";
      if (self.currentObject.inc_id)
        url = "/bonus/lstasktype/update?pk=" + self.currentObject.inc_id;
      return new Promise((resolve, reject) => {
        if (!this.currentObject.tasktype) {
          alert("Task Type不能為空");
          reject(false);
        }else if (!this.currentObject.description) {
          alert("Description不能為空");
          reject(false);        
        } else {
          axios
            .post(url, self.objectToFormData(self.currentObject))
            .then((response) => {
              if (!response.data.status) 
                return alert(response.data.msg.fail);               
              this.$nextTick(function () {
                self.reLoadTreegrid(); 
              });
              resolve(response);
            })
            .catch((error) => {
              console.log(error);
              reject(error);
            });
        }
      });
    },
    //查詢Tasktype
    search(){
      this.$refs.SearchModal.hide();
      this.reLoadTreegrid(); 
    },
    //重新加載Treegrid數據
    reLoadTreegrid(){
      var self = this;
      axios.get('/bonus/lstasktype/treelist',{
        params:this.common_sea_params
      })
      .then((response)=>{
          var result = response.data;
          if(result.status){
            this.datasource = result.data;
            this.$nextTick(function () {
              self.$refs.dt_tasktype.reLoad();              
              //$(".fixed-table-toolbar").find(".dropdown-toggle").find(".caret").remove();
              self.addLeftMenu("search_tasktype", "oi oi-magnifying-glass", this.$t('Search'));              
            })
          }
      })
    },
    //刪除Tasktype
    deleteTasktype(pk) {
      if (!confirm("delete this?")) return;
      var self = this;
      axios
        .post("/bonus/lstasktype/delete/" + pk)
        .then((response) => {
          if (!response.data.status) return alert(response.data.msg);
          this.$nextTick(function () {
            self.reLoadTreegrid(); 
          });
        })
        .catch((error) => {
          console.log(ereror);
        });
    },   
  },
};
</script>
