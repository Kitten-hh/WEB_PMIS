<template>
  <BlankPageLayout>
    <template v-slot:page-title-details>
      <h5>{{ $t('Record management of developers use technical') }}</h5>
    </template>
    <template v-slot:page-Details>
      <div class="card">
        <div class="card-body">            
            <LPDataTable
                ref="dt_technicalUseRecord"   
                datasource="/looper/technicalUseRecord/table"             
                :columns="technicalUseRecordColumns"
                :custom_options="technicalUseRecordOptions" 
                :paging_inline="true"   
                @on_row_click="on_row_click"
                @on_dbclick="on_row_dbclick"
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
    <LPLabelInput :label="$t('TaskNo')">
      <input
        type="text"
        class="form-control"
        v-model="currentObject.taskno"        
        required
      >
    </LPLabelInput>
    <LPLabelInput :label="$t('Date')">
      <input type="date" 
        class="form-control col" 
        v-model="currentObject.inputdate"
        required>
    </LPLabelInput>
    <LPLabelInput :label="$t('Contact')">
      <input
        type="text"
        class="form-control"
        v-model="currentObject.contact" 
        required
      >
    </LPLabelInput>
    <LPLabelInput :label="$t('Technical Id')">
      <input
        type="text"
        class="form-control"
        @blur="onTechnicIdChange"
        v-model="currentObject.technicid"
      >
    </LPLabelInput>   
    <LPLabelInput :label="$t('Description')">
      <textarea
        class="form-control scrollbar"
        v-model="currentObject.description"
        rows="3"
      ></textarea>
    </LPLabelInput> 
    <LPLabelInput :label="$t('Status')">
      <select
        class="form-control"
        v-model="currentObject.status"
      >
        <option value="N">N</option>
        <option value="Y">Y</option>
      </select>
    </LPLabelInput>
    <LPLabelInput :label="$t('Issue')">
      <textarea
        class="form-control scrollbar"
        v-model="currentObject.issue"
        rows="3"
      ></textarea>
    </LPLabelInput>  
  </LPModalForm>
</template>
<script>
import axios from "axios";
import LPDataTable from "@components/looper/tables/LPDataTable.vue";
import LPModalForm from "@components/looper/layout/LPModalForm.vue";
import LPLabelInput from "@components/looper/forms/LPLabelInput.vue";
import BlankPageLayout from "@components/looper/layout/page/BlankPageLayout.vue";
export default {
  name: "TechnicalUseRecordFrm",
  components: {   
    LPDataTable,
    LPModalForm,
    LPLabelInput,
    BlankPageLayout,
  },
  data() {
    return {
      currentObject: {},
      technicalUseRecordOptions: { 
        responsive: false,
        scrollX: true,
        scrollY: 600,
        autoWidth: false,
        pageLength: 100,
      },
      technicalUseRecordColumns: [
        { field: "taskno", label: this.$t('TaskNo'), width: "80px" },
        { field: "inputdate", label: this.$t('Date'), width: "80px",type: "date" },
        { field: "contact", label: this.$t('Contact'), width: "80px" },
        { field: "technicid", label: this.$t('Technical Id'), width: "120px",
          render: function (data, type, row) {  
            return `<a href="/PMIS/opportunity/Technical_Material?param=${data}" class="menu-link" target="_blank">${data}</a>`;                
            
          },
        },  
        { field: "description", label: this.$t('Description'), width: "350px" },  
        { field: "status", label: this.$t('Status') },  
        { field: "issue", label: this.$t('Issue'), width: "350px" },  
        {
          field: "operation",
          label: this.$t('Operation'),
          render: function (data, type, row) {
            var id = row.DT_RowId;       
            return `<a class="btn del-btn btn-sm btn-icon btn-secondary" href="#" id="${id}" ><i class="far fa-trash-alt"></i></a></div>`;
          },
        },
      ],
      technicalUseRecordParamsFun: undefined,
    };
  },
  mounted() {
    this.addNewButton();
  },
  methods: {  
    addNewButton() {
      var self = this;
      this.$nextTick(function () {
        var btnNew =
          `<button id="btnNew" type="button" class="btn btn-primary">
          {0}
        </button>`.format(this.$t("New Item"));   
        //$('.LPDataTable .input-group-append').addClass('ml-auto');
        $('.LPDataTable .input-group-append').append(btnNew);   
        $('#btnNew').on('click',function(){
          self.addTechnicalUseRecord();
        }); 
      });
    },
    onTechnicIdChange() {
      axios
        .get("/looper/technicalUseRecord/technical", {
          params: {
            technicid: this.currentObject.technicid,
          },
        })
        .then((response) => {
          var result = response.data;
          if (result.status){
            this.currentObject.description = result.data.mb004
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },  
    on_row_click(e, data) {
      var Element = e.target.tagName;
      if (Element == "path" || Element == "svg") {
        this.deleteTechnicalUseRecord(data);
       
      }
    },
    submitModalForm() {
      var self = this;
      var url = "/looper/technicalUseRecord/add";
      if (self.currentObject.inc_id)
        url = "/looper/technicalUseRecord/update?pk=" + self.currentObject.inc_id;
      return new Promise((resolve, reject) => {
        if (!this.currentObject.taskno) {
          alert("TaskNo不能為空");
          reject(false);
        }else if (!this.currentObject.inputdate) {
          alert("Date不能為空");
          reject(false);
        }else if (!this.currentObject.contact) {
          alert("Contact不能為空");
          reject(false);
        }else if (!this.currentObject.technicid) {
          alert("Technical Id不能為空");
          reject(false);
        } else {
          axios
            .post(url, self.objectToFormData(self.currentObject))
            .then((response) => {
              if (!response.data.status) return alert(response.data.msg.fail);               
              this.$nextTick(function () {
                this.$refs.dt_technicalUseRecord.datatable.search("").draw();
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
    deleteTechnicalUseRecord(data) {
      if (!confirm("delete this?")) return;
      axios
        .post("/looper/technicalUseRecord/delete/" + data.inc_id)
        .then((response) => {
          if (!response.data.status) return alert(response.data.msg);
          this.$nextTick(function () {
            this.$refs.dt_technicalUseRecord.datatable.search("").draw();
          });
        })
        .catch((error) => {
          console.log(ereror);
        });
    },
    on_row_dbclick(data) {
      this.currentObject = data;
      this.$refs.modalForm.$refs.modal.show();
    },
    addTechnicalUseRecord() {
      this.currentObject = {};
      this.$refs.modalForm.title = "New";
      this.$refs.modalForm.$refs.modal.show();
    },    
  },
};
</script>
<style>
pre {
  font-size: 100%;
}
table tbody tr:first-child td:first-child {
  width: 400px;
}
.has-sidebar-fluid {
  position: relative;
}
.sidebar-section {
  padding-top: 0;
}

.nav-item .fa, .nav-item .fas, .nav-item .fa_add_tasks {
  position: relative;
  top: .125rem;
}
</style>