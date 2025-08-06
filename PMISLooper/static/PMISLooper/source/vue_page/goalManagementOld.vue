<template>
  <div class="page-inner page-inner-fill">
    <div class="message">
      <div class="message-header justify-content-around">
        <h5 class="mb-0">{{ $t("Goal Management") }}</h5>
      </div>
      <div class="message-body goalMgt_style2">
        <LPCard :class_str="'goalManagement mb-0'">
          <template v-slot:header>
            <div :class="['filter row', lang_code_en ? 'en_filter' : '']">
              <div class="form-group d-flex col col-sm-3 col-md-3 col-lg col-xxl-auto goal_contact">
                <label class="col-form-label caption col-auto pl-0">{{ $t("contact") }}</label>
                <select class="status_select" data-toggle="selectpicker" data-size="5" data-width="100%"
                  v-model="params.contact" data-none-selected-text>
                  <option value></option>
                  <option v-for="(option, index) in options" :key="index" :value="option.text">{{ option.text }}</option>
                </select>
              </div>
              <!--
                          <div class="form-group d-flex col-sm-3 col-md-3 col-lg col-xxl-auto goal_progress">
                            <label class="col-form-label caption col-auto pl-0">{{$t("progress")}}</label>
                            <select
                              class="status_select"
                              data-toggle="selectpicker"
                              data-size="5"
                              data-width="100%"
                              v-model="params.progress"
                              data-none-selected-text
                            >
                              <option value></option>
                              <option value="N">N</option>
                              <option value="I">I</option>
                              <option value="C">C</option>
                            </select>
                          </div>
                          -->
              <div class="form-group d-flex goalMgmt_desc col-12 col-sm col-md col-xxl">
                <label class="col-form-label caption col-auto pl-0">{{ $t("goal_desc") }}</label>
                <input id="goal_description" type="text" class="form-control col" v-model="params.goaldesc">
              </div>
              <div class="col-auto goal_tools">
                <button type="button" class="btn btn-primary mr-1 mr-sm-2" @click="clear">
                  <!-- <i class="fas fa-trash d-block d-sm-none"></i> -->
                  <span class="">{{ $t("clear") }}</span></button>
                <button class="btn btn-primary" type="button" @click="search">
                  <!-- <i class="fas fa-search d-block d-sm-none"></i> -->
                  <span class="">{{ $t("search") }}</span></button>
              </div>
            </div>
          </template>
          <template v-slot:body>
            <LPDataTable :paging="true" :columns="masterTable.columns" :datasource="masterTable.datasource"
              :custom_params_fun="masterTable.custom_params_fun" :custom_options="masterTable.custom_options"
              @on_selectornot="masterTable.select_row" @on_dbclick="masterTable.dbclick"
              :handle_response_fun="masterTable.handle_response_fun" :searching="1 != 1" :paging_inline="1 == 1"
              ref="masterTable" />
            <div class="card-body pt-2 MHTask_wrapper">
              <LPCard :class_str="'goalManagement mb-0'">
                <template v-slot:header>
                  <h6 class="text-left mb-0">{{ $t("Must Have Task") }}</h6>
                </template>
                <template v-slot:body>
                  <LPDataTable :paging="false" :columns="detailTable.columns" :datasource="detailTable.datasource"
                    :custom_params_fun="detailTable.custom_params_fun" :custom_options="detailTable.custom_options"
                    @on_dbclick="detailTable.dbclick" :searching="1 != 1" :paging_inline="1 == 1" ref="detailTable" />
                </template>
              </LPCard>
            </div>
          </template>
        </LPCard>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import LPCard from "@components/looper/layout/LPCard.vue";
import LPDataTable, {DateRender} from "@components/looper/tables/LPDataTable.vue";

export default {
  name: "goalManagementOld",
  components: {
    LPCard,
    LPDataTable
  },
  data() {
    var self =this;
    var desc_width = SWApp.os.isMobile ? "80%" : "50%";
    return {
      params:{},
      options: [],
      cur_master:{},
      masterTable:{
        datasource:"/PMIS/goal/management/table",
        columns:[
            { field: "taskno", label: gettext('TaskNo') },
            { field: "task", label: gettext('Task')},
            { field: "contact", label: gettext('Contact') },
            { field: "planedate", label: gettext('PlanEDate'), render:DateRender},
            { field: "progress", label: gettext('Progress')},          
        ],
        custom_params_fun:function(){
          return self.params;
        },
        custom_options:{
          deferLoading: 0,
          scrollY:'30vh',
          scrollCollapse: true,
          responsive: true,
          select: {
            style:'single'
          },
          columnDefs:  SWApp.os.isMobile ? []:[
                { "responsivePriority": 4, width:150, "targets": 0 },
                { "responsivePriority": 1, width:desc_width,"className": "all", "targets": 1 },
                { "responsivePriority": 4, "targets": 2 },
                { "responsivePriority": 2, "targets": 3 },
                { "responsivePriority": 4, "targets": 4 },            
          ],         
        },
        select_row:function(e, dt, type, indexes) {
          if ( type === 'row' && e.type == "select") {
              var rows = dt.rows({selected: true}).data();                    
              self.cur_master = rows[0];
              self.$refs.detailTable.datatable.search("").draw();
          }            
        },
        handle_response_fun:function(data) {
          self.$nextTick(function(){
            //默認選中第一行
            self.$refs.masterTable.datatable.row(':eq(0)', { page: 'current' }).select();
          });
          return data;
        },
        dbclick:function(data) {
          init_task(data.DT_RowId,{});
        }
      },
      detailTable:{
        datasource:"/PMIS/goal/management/table?read_detail=true",
        columns:[
            { field: "taskno", label: gettext('TaskNo') },
            { field: "task", label: gettext('Task')},
            { field: "contact", label: gettext('Contact') },
            { field: "planedate", label: gettext('PlanEDate'), render:DateRender},
            { field: "progress", label: gettext('Progress')},          
        ],
        custom_params_fun:function(){
          if (self.cur_master.hasOwnProperty('taskno')) {
            return {master_taskno:self.cur_master.taskno,master_recordid:self.cur_master.recordid}
          }else {
            return {}
          }
        },
        custom_options:{
          deferLoading: 0,
          scrollY:'40vh',
          scrollCollapse: true,
          responsive: true,
          columnDefs: SWApp.os.isMobile ? []:[
                { "responsivePriority": 4, width:150, "className": "min-tablet-p","targets": 0 },
                { "responsivePriority": 2, width:desc_width,"className": "all", "targets": 1 },
                { "responsivePriority": 4, "className": "min-tablet-p", "targets": 2 },
                { "responsivePriority": 2, "className": "min-tablet-p", "targets": 3 },
                { "responsivePriority": 4, "className": "min-tablet-p", "targets": 4 },            
          ], 
        },
        dbclick:function(data) {
          init_task(data.DT_RowId,{});
        }
      },
      lang_code_en: true,      
    };
  },
  created() {
    this.init_contact();
    this.get_lang_code();
  },
  mounted() {
    this.$nextTick(function(){
      try {
      this.params['default'] = true;
      this.$refs.masterTable.datatable.search("").order([3, 'asc' ]).draw();
      }finally {
        this.params['default'] = false;
      }
    });
  },
  methods: {
    clear() {
        this.params = {};
        this.$nextTick(()=>{
            $("select").selectpicker("refresh");
          })        
    },
    init_contact() {
      axios.get(`/PMIS/user/get_part_user_names`).then(response => {
        if (response.data.data.length > 0) {
          var contacts = [];
          response.data.data.forEach((strkey, index) => {
            contacts.push({ id: index, text: strkey });
          });
          this.options = contacts;
          this.$nextTick(()=>{
            $(".status_select").selectpicker("refresh");
          })
        }
      });
    },    
    search() {
      if (this.params) {
        this.$refs.masterTable.datatable.search("").draw();
      }
    },
    get_lang_code() {
      if($("#curr_language_code").val() !== "en") {
          this.lang_code_en = false;
      }
    },
  }
};
</script>