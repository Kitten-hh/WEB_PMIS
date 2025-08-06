<template>
  <BlankPageLayout>
    <template v-slot:page-title-details>
      <h5>{{ $t("Improve Area") }}</h5>
    </template>
    <template v-slot:page-Details>
      <div class="card mb-0">
        <div class="card-header">
          <div class="card-title dropdown m-0" id="task_search_box">                    
            <div class="task_search_tools">                    
                <button id="btnNew" type="button" class="btn btn-primary font-weight-bolder" @click="newItem">
                  {{ $t("New Item") }}
                </button>
            </div>
          </div>  
        </div>   
        <div class="card-body">          
          <LPDataTable
            id="dt_improvearea"
            :paging_inline="true"
            :paging="false"
            :columns="improveareaColumns"
            datasource="/bonus/improvearea/datatable"
            :custom_options="improvearea_custom_options"
            :custom_params_fun="improvearea_params_fun"
            :show_footer="true"
            ref="dt_improvearea"
          /> 
        </div>
      </div>
    </template>
  </BlankPageLayout>
  <LPModalForm
    :novalidate="true"
    ref="improveAreaItemForm"
    :title="improveAreaItemFormTitle"
    @on_submit="submitModalForm"
  >
    <LPLabelInput :label="$t('Description')">
      <input
          type="text"
          class="form-control"
          v-model="currentImproveArea.description"
      >
    </LPLabelInput> 
    <LPLabelInput :label="$t('Category')">
      <input
          type="text"
          class="form-control"
          v-model="currentImproveArea.category"
      >
    </LPLabelInput> 
    <LPLabelInput :label="$t('Position')">
      <input
        type="text"
        class="form-control"
        v-model="currentImproveArea.position"
      />
    </LPLabelInput>    
    <LPLabelInput :label="$t('Score')">
      <input
        type="text"
        class="form-control"
        v-model="currentImproveArea.score"
      />
    </LPLabelInput>    
  </LPModalForm>  
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
import LPCombobox from "@components/looper/forms/LPCombobox.vue";
export default {
  name: "ImproveArea_vueFrm",
  components: {
    LPDataTable,
    LPModalForm,
    LPModal,
    LPLabelInput,
    BlankPageLayout,
    LPCombobox,
  },
  data() {
    return {
      currentObject: {},
      left_button: undefined,
      common_sea_params: {}, //共享條件
      improveareaColumns: [
        { field: "inc_id", label: this.$t("ID") },
        { field: "description", label: this.$t("Description") , width: "400px"},
        { field: "category", label: this.$t("Category")},
        { field: "position", label: this.$t("Position")},
        { field: "score", label: this.$t("Score") },       
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
      improvearea_custom_options: {
        responsive: false,
        scrollX: true,
        scrollY: 550,
        //deferLoading: 0,
        autoWidth: false,        
      },
      currentImproveArea: {},
      improveAreaItemFormTitle: "",
      improvearea_params_fun: undefined,       
    };
  },
  mounted() {
    this.listenButtonEvent();    
    $('.LPDataTable .input-group-append .btn-secondary').addClass("d-none");
  },
  methods: {    
    listenButtonEvent() {
      var self = this;
      //刪除記錄
      $("#dt_improvearea").on("click", ".delete", function (e) {
        e.preventDefault(); //阻止按鈕默認動作
        e.stopPropagation();
        var pk = $(this).closest(".SWDropdown").attr("inc_id");
        self.deleteimproveAreaItem(pk);
      });
      //修改記錄
      $("#dt_improvearea").on("click", ".edit", function (e) {
        e.preventDefault(); //阻止按鈕默認動作
        e.stopPropagation();
        var pk = $(this).closest(".SWDropdown").attr("inc_id");
        axios.get("/bonus/improvearea/update?pk=" + pk).then((response) => {
          var result = response.data;
          if (result.status) {
            self.currentImproveArea = result.data;
            self.improveAreaItemFormTitle = "Eidt Item";
            self.$refs.improveAreaItemForm.$refs.modal.show();
          }
        });
      });
    },
    newItem() {
      this.currentImproveArea = {penaltyid:0};
      this.improveAreaItemFormTitle = this.$t("New Item");
      this.$refs.improveAreaItemForm.$refs.modal.show();
    },
    submitModalForm() {
      var self = this;
      var url = "/bonus/improvearea/add";
      if (self.currentImproveArea.inc_id)
        url =
          "/bonus/improvearea/update?pk=" + self.currentImproveArea.inc_id;
      return new Promise((resolve, reject) => {
        if (!this.currentImproveArea.description) {
          self.showMessage("Description can not be empty");
          reject(false);
        } else if (!this.currentImproveArea.category) {
          self.showMessage("Category can not be empty");
          reject(false);
        } else if (!this.currentImproveArea.score) {
          self.showMessage("Score can not be empty");
          reject(false);
        } else {
          axios
            .post(url, self.objectToFormData(self.currentImproveArea))
            .then((response) => {
              if (!response.data.status)
                return self.showMessage(response.data.msg.fail);
              this.$nextTick(function () {
                self.$refs.dt_improvearea.datatable.draw();
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
    deleteimproveAreaItem(pk) {
      if (!confirm("確定刪除嗎?")) return;
      var self = this;
      axios
        .post("/bonus/improvearea/delete/" + pk)
        .then((response) => {
          if (!response.data.status) return self.showMessage(response.data.msg);
          this.$nextTick(function () {
            self.$refs.dt_improvearea.datatable.draw();
          });
        })
        .catch((error) => {
          console.log(ereror);
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