<template>
  <BlankPageLayout>
    <template v-slot:page-title-details>
      <h5>{{ $t("Bonus Debit Management") }}</h5>
    </template>
    <template v-slot:page-Details>
      <div class="card mb-0">
        <div class="card-header">
          <div class="card-title dropdown m-0" id="task_search_box">                    
            <div class="task_search_tools">   
                <button class="btn btn-fixed-height btn-primary font-weight-bolder mr-2" @click="search">
                  <i class="fa fa-search mr-2"></i>{{ $t("Search") }}
                </button>   
                <button id="btnNew" type="button" class="btn btn-primary font-weight-bolder" @click="newDeductionItem">
                  {{ $t("New Item") }}
                </button>
            </div>
          </div>  
        </div>
        <div class="card-body">  
          <ul class="nav nav-tabs">
            <li class="nav-item mr-2">
                <a
                    class="nav-link active"           
                    data-toggle="tab"
                    href="#tab_list"
                >
                    <h3 class="card-title"> 
                        <!-- <label name="lb_contact"></label> -->
                        <label class="text-dark-75 trm-title-with-divider mb-0">{{$t("Deduction List")}}</label>     
                    </h3> 
                </a>
            </li>
            <li class="nav-item">
                <a
                    class="nav-link"
                    data-toggle="tab"
                    href="#tab_chart"
                >
                    <h3 class="card-title"> 
                        <!-- <label name="lb_contact"></label> -->
                        <label class="text-dark-75 trm-title-with-divider mb-0">{{$t("Deduction Analysis")}}</label>     
                    </h3> 
                </a>
            </li>                           
        </ul>   
        <div class="tab-content pt-1">
          <div
              class="tab-pane fade show active"
              id="tab_list"
              role="tabpanel"
          >
              <div class="card card-reflow mb-0">
                  <div class="card-body no-drag grid-item-body py-0 pb-2">                           
                    <LPDataTable
                      id="dt_userdeduction"
                      :paging_inline="true"
                      :paging="false"
                      :columns="userDeductionColumns"
                      datasource="/bonus/userdeduction/datatable"
                      :custom_options="userDeduction_custom_options"
                      :custom_params_fun="userDeduction_params_fun"
                      :searching="false"
                      :show_footer="true"
                      ref="dt_userdeduction"
                    />               
                  </div>
              </div>
          </div>
          <div
              class="tab-pane fade"
              id="tab_chart"
              role="tabpanel"
          >
            <div class="row">
              <div class="col-12 col-lg-8 col-xl-8"> 
                <LPBarChart
                  :chartData="BarData"
                  :showlegend="true"
                  ref="barChar"
                />      
              </div>
              <div class="col-12 col-lg-4 col-xl-4">
                <!-- .card -->
                <div class="card card-fluid">
                  <div class="card-header card-title">{{$t("Area of Improvement")}}</div>
                  <!-- .card-body -->
                  <div class="card-body">  
                    <LPDataTable
                      id="dt_improve"
                      :paging_inline="true"
                      :paging="false"
                      :columns="improveColumns"                      
                      :custom_options="improve_custom_options"
                      :datasource="improveDataSource"
                      :searching="false"
                      :show_footer="true"
                      ref="dt_improve"
                    />                  
                  </div><!-- /.card-body -->                
                </div><!-- /.card -->
              </div>
            </div>
          </div>   
        </div> 
        </div>
      </div>
    </template>
  </BlankPageLayout>
  <LPModalForm
        :novalidate="true"
        ref="deductionItemForm"
        :title="deductionItemFormTitle"
        @on_submit="submitModalForm"
    >  
        <LPLabelInput :label="$t('Area of Improvement')">
            <LPCombobox url='/looper/metting/get_Improvement' :labelFields="['tpdesc']"            
            valueField='tpdesc' @on_item_selected="manageChange"
            :value="currentDeductionItem.improvement" @on_Blur="(value) => { currentDeductionItem.improvement = value }"
            />            
        </LPLabelInput> 
        <LPLabelInput :label="$t('Description')">
          <LPCombobox url='/looper/metting/get_Improvement_item' ref="description_LPCasombobox" :labelFields="['tptname']"
            :filter="Improvement_item_filter"
            valueField='TptName' :value="currentDeductionItem.description" @on_item_selected="onDescriptionDesc_change"
            @on_Blur="(value) => { currentDeductionItem.description = value }" />
        </LPLabelInput> 
        <LPLabelInput :label="$t('PenaltyID')">
        <input
            type="text"
            class="form-control"
            v-model="currentDeductionItem.penaltyid"
        >
        </LPLabelInput> 
        <LPLabelInput :label="$t('Contact')">
        <input
            type="text"
            class="form-control"
            v-model="currentDeductionItem.username"
            @change="getUserPosition"
        >
        </LPLabelInput>     
        <LPLabelInput :label="$t('Category')">
            <LPCombobox url='/bonus/userdeduction/get_duction_category' :labelFields="['category']"
                valueField='category' :value="currentDeductionItem.category" @on_item_selected="(item) => { currentDeductionItem.category = item.category }"
                @on_Blur="(value) => { currentDeductionItem.category = value }" />
        </LPLabelInput>    
        <LPLabelInput :label="$t('Position')">            
        <input
            type="text"
            class="form-control"
            v-model="currentDeductionItem.position"            
        >
        </LPLabelInput>    
        <!-- <LPLabelInput :label="$t('Description')">
        <textarea
            class="form-control scrollbar"
            v-model="currentDeductionItem.description"
            rows="3"
        ></textarea>
        </LPLabelInput>  -->
        <LPLabelInput :label="$t('Deduct Score')">
        <input
            type="text"
            class="form-control"
            v-model="currentDeductionItem.score"
        >
        </LPLabelInput> 
        <LPLabelInput :label="$t('Date')">
        <input 
            type="date"
            class="form-control" 
            v-model="currentDeductionItem.deductiondate"
            required
        >
        </LPLabelInput> 
    </LPModalForm> 
  <LPModal ref="SearchModal" :title="$t('Filter')" class="col" id="SearchModal">
    <template v-slot:body>
      <!-- :gsearch_placeholder="a" -->
      <div class="row">
          <div class="form-group col-12">
              <label class="col-form-label caption">{{$t('Pre-Condition')}}</label>
              <select class="form-control" data-none-selected-text v-model="cycle" @change="setDate">  
                <option value=""></option>                    
                <!-- <option value="WithNoInvoice">{{$t('Order with no invoice')}}</option>  -->
                <option value="lastweek">{{ $t("Last Week") }}</option>         
                <option value="week">{{ $t("This Week") }}</option>   
                <option value="lastmonth">{{$t("Last Month")}}</option>   
                <option value="month">{{$t("This Month")}}</option>              
                <option value="lastquarter">{{$t("Last Quarter")}}</option>   
                <option value="quarter">{{$t("This Quarter")}}</option>           
              </select>  
          </div>
      </div>
      <div class="row">
          <div class="form-group col-12">
              <label class="col-form-label caption">{{ $t("UserName") }}</label>
              <input class="form-control control" type="text" name="contact" id="contact" v-model="contact">
          </div>
      </div>
      <div class="row">
          <div class="form-group col-6">
              <label class="col-form-label caption">{{ $t("Date From") }}</label>
              <input class="form-control control" type="date" name="edatefrom" id="edatefrom" v-model="datefrom" required>           
          </div>
          <div class="form-group col-6">
              <label class="col-form-label caption">{{ $t("Date To") }}</label>
              <input class="form-control control" type="date" name="edateto" id="edateto" v-model="dateto" required>
          </div>
      </div>
    </template>
    <template v-slot:footer>
      <button type="button" class="btn btn-primary" @click="deductionSearch">{{ $t("Search") }}</button>
      <button type="button" class="btn btn-light" data-dismiss="modal">{{ $t("Close") }}</button>
    </template>
  </LPModal>
  <div class="modal fade my-modal-parent" id="messageModal" tabindex="-1" role="dialog" aria-labelledby="messageModalTitle"
      aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">{{ $t("Tooltip") }}</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                <p id="msg"></p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-cancel" data-dismiss="modal">{{ $t("Close") }}</button>
            </div>
        </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import LPDataTable, {
  DateRender,
} from "@components/looper/tables/LPDataTable.vue";
import LPModalForm from "@components/looper/layout/LPModalForm.vue";
import LPLabelInput from "@components/looper/forms/LPLabelInput.vue";
import BlankPageLayout from "@components/looper/layout/page/BlankPageLayout.vue";
import LPModal from "@components/looper/layout/LPModal.vue";
import LPBarChart from "@components/looper/chart/LPBarChart.vue";
import LPCombobox from "@components/looper/forms/LPCombobox.vue";
import {
    formatDate,
    getToday,
    getWeekStartDate,
    getLastWeekStartDate,
    getLastWeekEndDate,
    getMonthStartDate,
    getMonthEndDate,
    getLastMonthStartDate,
    getLastMonthEndDate,
    getQuarterStartDate,
    getQuarterEndDate,
    getLastQuarterStartDate,
    getLastQuarterEndDate,
    get_quarterly_date
} from "/BonusApp/static/BonusApp/source/javascript/datatime_common.js";
export default {
  name: "Deduction_vueFrm",
  components: {
    LPDataTable,
    LPModalForm,
    LPModal,
    LPLabelInput,
    BlankPageLayout,
    LPBarChart,
    LPCombobox,
  },
  data() {
    return {
      currentObject: {},
      left_button: undefined,
      common_sea_params: {}, //共享條件
      userDeductionColumns: [
        { field: "inc_id", label: this.$t("ID"), visible: false },
        { field: "username", label: this.$t("UserName") },
        { field: "penaltyid", label: this.$t("PenaltyID")},
        { field: "description", label: this.$t("Description"), width: "400px" },
        { field: "score", label: this.$t("Score") },
        { field: "deductiondate", label: this.$t("Date"), render: DateRender },
        {
          field: "operate",
          label: this.$t("Operation"),
          width: "30",
          render: function (data, type, row) {
            return `<div class="dropdown SWDropdown" inc_id="${row.inc_id}">
                <button class="btn caption" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><i class="fas fa-ellipsis-v"></i></button>  
                    <div class="dropdown-menu control" aria-labelledby="dropdownMenuButton">
                        <a class="dropdown-item edit" href="#" >` + gettext("Edit") + `</a>
                        <a class="dropdown-item delete" href="#">` + gettext("Delete") + `</a>
                    </div>
                </div>`;
          },
        },
      ],
      userDeduction_custom_options: {
        responsive: false,
        scrollX: true,
        scrollY: 550,
        //deferLoading: 0,
        autoWidth: false,
        footerCallback: function (tfoot, data, start, end, display) {
          /*
          var api = this.api();
          $(api.column(0).footer()).html("");
          $(api.column(1).footer()).html("");
          $(api.column(2).footer()).html("");
          $(api.column(2).footer()).html(gettext("Total")+":");
          $(api.column(3).footer()).html(
            api
              .column(3)
              .data()
              .reduce(function (a, b) {
                return a + b;
              }, 0)
          );
          */
          var api = this.api();
          var allcolumns = api.settings().init().columns;  //取得DataTable的字段列表
          var sum_columns = ['score']  //設置需要匯總的字段              
          api.columns().every(function () {
              var column_name = allcolumns[this.index()].name;           
              if (sum_columns.indexOf(column_name) != -1) {
                var total = this.data().reduce(function (a, b) {                   
                  return a + b;                     
                }, 0); 
                $(this.footer()).html(total);                 
              }

              if (column_name == 'description') {
                  $(this.footer()).text(gettext("Total:"));
              }                      
          });
        },
      },
      improveColumns: [        
        { field: "tpdetailid", label: this.$t("ImproveArea No"), width:'120px'},
        { field: "tptname", label: this.$t("Description")},        
      ],
      improve_custom_options: {
        responsive: true,
        scrollX: true,  
        //deferLoading: 0,
        autoWidth: false,        
      },
      improveDataSource:[
        {'tpdetailid':10, 'tptname':'未按要求提供Project跟進大圖'},
        {'tpdetailid':20, 'tptname':'不注重結果'},
        {'tpdetailid':30, 'tptname':'不寫文檔'},
        {'tpdetailid':40, 'tptname':'不做每天要求做的固定任務'},
        {'tpdetailid':50, 'tptname':'說了也沒做'},
        {'tpdetailid':60, 'tptname':'沒有及時跟進陳生要求做的任務'},
      ],
      currentDeductionItem: {},
      deductionItemFormTitle: "",
      userDeduction_params_fun: undefined,
      Improvement_item_filter:'',
      management_selected:[],
      BarData: {},
      datefrom:'',
      dateto:'',
      cycle:'',
      contact:'',
    };
  },
  mounted() {
    //this.reLoadTreegrid();
    this.listenButtonEvent();  
    this.getChartData();  
    this.init_penalty();
    /*
    $('.wrapper').on("shown.bs.tab","a[data-toggle='tab']", function (e) {
      $($.fn.dataTable.tables(true)).DataTable().columns.adjust();
    });
    */
  },
  methods: {
    setDate(){
        if(this.cycle=='today'){
            this.datefrom = getToday();
            this.dateto = getToday();
        }
        else if(this.cycle=='yesterday'){
            var yesterday = new Date();
            yesterday.setDate(yesterday.getDate()-1); 
            this.datefrom = formatDate(yesterday);
            this.dateto = formatDate(yesterday);
        }else if(this.cycle=='lastweek'){
            this.datefrom = getLastWeekStartDate();
            this.dateto = getLastWeekEndDate();
        }else if(this.cycle=='week'){
            this.datefrom = getWeekStartDate();
            this.dateto = getToday();
        }else if(this.cycle=='lastmonth'){
            this.datefrom = getLastMonthStartDate();
            this.dateto = getLastMonthEndDate();
        }else if(this.cycle=='month'){
            this.datefrom = getMonthStartDate();
            this.dateto = getToday();
        }else if(this.cycle=='lastquarter'){
            this.datefrom = getLastQuarterStartDate();
            this.dateto = getLastQuarterEndDate();
        }else if(this.cycle=='quarter'){
            this.datefrom = getQuarterStartDate();
            this.dateto = getToday();
        }else{
            this.datefrom = '';
            this.dateto = '';
            this.contact = '';
        }       
    },
    listenButtonEvent() {
      var self = this;
      //刪除扣分記錄
      $("#dt_userdeduction").on("click", ".delete", function (e) {
        e.preventDefault(); //阻止按鈕默認動作
        e.stopPropagation();
        var pk = $(this).closest(".SWDropdown").attr("inc_id");
        self.deleteDeductionItem(pk);
      });
      //修改扣分記錄
      $("#dt_userdeduction").on("click", ".edit", function (e) {
        e.preventDefault(); //阻止按鈕默認動作
        e.stopPropagation();
        var pk = $(this).closest(".SWDropdown").attr("inc_id");
        axios.get("/bonus/userdeduction/update?pk=" + pk).then((response) => {
          var result = response.data;
          if (result.status) {
            self.currentDeductionItem = result.data;
            self.deductionItemFormTitle = "Eidt Item";
            self.$refs.deductionItemForm.$refs.modal.show();
          }
        });
      });
    },
    init_penalty(){
        var self = this
        axios.get("/looper/metting/get_Improvement",{
            params:{ "manager": '2', "tpdesc": 'AreasofImprovementfor'}
        })    
        .then((response)=>{
            var result = response.data;
            if(result.status){                 
                self.management_selected=result.data             
            }            
        });   

    },
    newDeductionItem() {
      this.currentDeductionItem = {penaltyid:0};
      this.deductionItemFormTitle = this.$t("New Item");
      this.$refs.deductionItemForm.$refs.modal.show();
    },
    submitModalForm() {
      var self = this;
      var url = "/bonus/userdeduction/add";
      if (self.currentDeductionItem.inc_id)
        url =
          "/bonus/userdeduction/update?pk=" + self.currentDeductionItem.inc_id;
      return new Promise((resolve, reject) => {
        if (!this.currentDeductionItem.deductiondate) {
          self.showMessage("日期不能為空");
          reject(false);
        } else if (!this.currentDeductionItem.description) {
          self.showMessage("描述不能為空");
          reject(false);
        } else if (!this.currentDeductionItem.username) {
          self.showMessage("用戶名不能為空");
          reject(false);
        } else if (!this.currentDeductionItem.score) {
          self.showMessage("分數不能為空");
          reject(false);
        } else {
          axios
            .post(url, self.objectToFormData(self.currentDeductionItem))
            .then((response) => {
              if (!response.data.status)
                return self.showMessage(response.data.msg.fail);
              this.$nextTick(function () {
                self.$refs.dt_userdeduction.datatable.draw();
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
    deleteDeductionItem(pk) {
      if (!confirm("確定刪除嗎?")) return;
      var self = this;
      axios
        .post("/bonus/userdeduction/delete/" + pk)
        .then((response) => {
          if (!response.data.status) return self.showMessage(response.data.msg);
          this.$nextTick(function () {
            self.$refs.dt_userdeduction.datatable.draw();
          });
        })
        .catch((error) => {
          console.log(ereror);
        });
    },    
    //查詢Tasktype
    search() {
      this.$refs.SearchModal.show();
    },
    manageChange(item){
        this.currentDeductionItem.management = item.tpmastid; 
        this.currentDeductionItem.improvement=item.tpdesc
        if (this.currentDeductionItem.management)
            this.Improvement_item_filter=`tpmastid=${this.currentDeductionItem.management}`
        else
            this.Improvement_item_filter=''
    },
    deductionSearch(){  
      var contact=$('#contact').val();
      var datefrom = $('#edatefrom').val();
      var dateto = $('#edateto').val();
      var self = this;
      this.userDeduction_params_fun = () => {  
        if (contact=='' && datefrom=='' && dateto==''){
            return null;
        }  
        let filter = "";
        if(contact!=''){
          filter+='{"id":"username","field":"username","type":"string","input":"text","operator":"equal","value":"{0}"},'.format(contact);
        }
        if(datefrom!=''){
          filter+='{"id":"deductiondate","field":"deductiondate","type":"string","input":"text","operator":"greater_or_equal","value":"{0}"},'.format(datefrom);
        }
        if(dateto!=''){
          filter+='{"id":"deductiondate","field":"deductiondate","type":"string","input":"text","operator":"less_or_equal","value":"{0}"},'.format(dateto);
        }
        filter=filter.substr(0,filter.length-1);
        return {  
          attach_query:
            `{"condition":"AND","rules":[{0}],"not":false,"valid":true}`.format(filter),
        };
      };
      this.$nextTick(() => {
        self.$refs.dt_userdeduction.datatable.draw();
      });
      //讀取Chart的數據
      this.getChartData();
      this.$refs.SearchModal.hide();

    },
    getChartData(){
      var self = this;
      axios
        .get("/bonus/userdeduction/chart",{params:{'datefrom':this.datefrom,'dateto':this.dateto,'contact':this.contact}})
        .then((response) => {
          if (!response.data.status) return self.showMessage(response.data.msg);          
          self.redrawBarChar(response.data.data.labels,response.data.data.datas);
          self.$refs.dt_improve.datatable.clear(); //清空明細 
          self.$refs.dt_improve.datatable.rows
              .add(response.data.areadata)
              .draw(); 
        })
        .catch((error) => {
          console.log(ereror);
        });
    },
    redrawBarChar(labels, datas) {
      this.BarData = {
        labels: labels,
        datasets: [
          //一組數據
          {
            //頂部案例名稱
            label: this.$t("Score"),
            borderColor: "#00A28A", //柱狀圖顏色
            backgroundColor: "#00A28A",
            fill: true, //柱狀圖實際數據
            data: datas
          }
        ]
      };
    },
    onDescriptionDesc_change(item){
        var array = item.tptname.split('-')
        if (array.length>1){
            this.currentDeductionItem.penaltyid = array[0];
            this.currentDeductionItem.description = array[1];            
        }else{
            this.currentDeductionItem.description = array[0];
        }
        this.currentDeductionItem.username = item.contact;
        this.getUserPosition();
        
    },
    getUserPosition(){
        if(this.currentDeductionItem.username)   
            axios.get("/bonus/userdeduction/get_position",{
                params:{ "contact": this.currentDeductionItem.username}
            })    
            .then((response)=>{
                var result = response.data;
                if(result.status){                 
                    this.currentDeductionItem.position = result.data;         
                }            
            }); 
    },
    showMessage(msg){
      $('#msg').html(msg);
      $('#messageModal').modal('show'); 
    }
  },
};
</script>
<style scoped>
.card-title {
    margin-bottom: 0.5rem;
}
.nav-tabs .nav-link {
    padding: 0.5rem;
    border-width: 0 0 3px;
}
</style>