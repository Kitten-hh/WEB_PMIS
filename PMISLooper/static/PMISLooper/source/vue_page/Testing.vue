<template>
  <BlankPageLayout :customClass="'testingPage'">
    <template v-slot:page-title-details>
      <h5 class="page-navs">{{ $t('System Test') }}</h5>
    </template>
    <template v-slot:page-Details>
      <SidebarFluidLayout>
        <template v-slot:pageDetails>
          <div class="board testing_tree py-2 px-3 scrollbar">
            <LPTree ref="LPTree" :data="treeData" @selectNode="nodeSelect" />
          </div>
        </template>
        <template v-slot:sidebarDetails>
          <div class="card card-reflow mb-0">
            <div class="card-header py-2">
              <a class="btn btn-sm btn-primary" href="#" @click="addTestingInfo">
                <i class="fa fa-plus"></i>
              </a>
              <a class="btn btn-sm btn-primary ml-2" href="#" @click="$refs.excelTemplateModal.show()">
                <i class="fa fa-download"></i>
              </a>
              <a class="btn btn-sm btn-primary ml-2" href="#" @click="$refs.uploadExcelModal.show()">
                <i class="fa fa-upload"></i>
              </a>
            </div>
            <div class="card-body testInfoTable_wrapper">
              <LPDataTable ref="testInfoTable" datasource="/looper/testing/note_tab" :columns="testInfoColumns"
                :custom_options="testInfoOptions" :custom_params_fun="testInfoParamsFun" :paging_inline="true"
                @on_row_click="on_row_click" @on_dbclick="dblclickTable" />
            </div>
          </div>
        </template>
      </SidebarFluidLayout>
    </template>
  </BlankPageLayout>
  <LPModalForm :novalidate="true" ref="testingForm" @on_submit="submitTestingInfo">
    <LPLabelInput :label="$t('SysName')">
      <input type="text" class="form-control" v-model="testInfoObject.sysid" disabled required>
    </LPLabelInput>
    <LPLabelInput :label="$t('SeqNo')">
      <input type="text" class="form-control" v-model="testInfoObject.itemno" required disabled>
    </LPLabelInput>
    <LPLabelInput :label="$t('DocID')">
      <input type="text" class="form-control" v-model="testInfoObject.frmno" @change="frmnoFieldChange" required>
    </LPLabelInput>
    <LPLabelInput :label="$t('Function SeqNo')">
      <input type="text" class="form-control" v-model="testInfoObject.funcitemno">
    </LPLabelInput>
    <LPLabelInput :label="$t('Function Description')">
      <textarea class="form-control scrollbar" v-model="testInfoObject.funcdesc" rows="3"></textarea>
    </LPLabelInput>
    <LPLabelInput :label="$t('Function Tpye')">
      <input type="text" class="form-control" v-model="testInfoObject.functype">
    </LPLabelInput>
    <LPLabelInput :label="$t('Test')">
      <select class="form-control" v-model="testInfoObject.state">
        <option value="1">{{ $t('Yes') }}</option>
        <option value="0">{{ $t('No') }}</option>
      </select>
    </LPLabelInput>
    <LPLabelInput :label="$t('Test Data')">
      <textarea class="form-control scrollbar" v-model="testInfoObject.testdata" rows="3"></textarea>
    </LPLabelInput>
    <LPLabelInput :label="$t('Test Operation And Result')">
      <textarea class="form-control scrollbar" v-model="testInfoObject.testresult" rows="3"></textarea>
    </LPLabelInput>
    <LPLabelInput :label="$t('Bug')">
      <textarea class="form-control scrollbar" v-model="testInfoObject.question" rows="3"></textarea>
    </LPLabelInput>
  </LPModalForm>
  <LPModal ref="excelTemplateModal" class="excelTemplateModal" :title="$t('Choose the interface to test')">
    <template v-slot:body>
      <label>{{ $t('Test interface')}}: </label>
      <select class="form-control" id="frm-select">
        <option value=""></option>
        <option v-for="(frm, i) in frameList" :key="i" :value="frm.ma001">{{ frm.ma003 }}</option>
      </select>
    </template>
    <template v-slot:footer>
      <button type="button" class="btn btn-primary" @click="frmConfirm">{{ $t("Confirm") }}</button>
      <button type="button" class="btn btn-secondary" data-dismiss="modal">{{ $t("Close") }}</button>
    </template>
  </LPModal>
  <LPModal ref="uploadExcelModal" class="uploadExcelModal" :title="$t('Choose file to upload')">
    <template v-slot:body>
      <label>{{ $t('Upload Excel')}}: </label>
      <div class="input-group input-group-alt" style="width: 350px;">
        <div class="custom-file">
          <input type="file" class="custom-file-input" ref="import_excel" name="excelFile" 
            accept="application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet">
          <label class="custom-file-label" for="excelFile">{{$t("Select Excel File")}}</label>
        </div>
        <div class="input-group-append d-none">
          <button type="button" class="btn btn-success">{{$t("Import Excel")}}</button>
        </div>
      </div> 
    </template>
    <template v-slot:footer>
      <button type="button" class="btn btn-primary" @click="uploadExcel">{{ $t("Confirm") }}</button>
      <button type="button" class="btn btn-secondary" data-dismiss="modal">{{ $t("Close") }}</button>
    </template>
  </LPModal>
</template>
<script>
import axios from "axios";
import LPTree from "@components/looper/general/LPTree.vue";
import LPDataTable from "@components/looper/tables/LPDataTable.vue";
import LPModalForm from "@components/looper/layout/LPModalForm.vue";
import LPModal from "@components/looper/layout/LPModal.vue";
import LPLabelInput from "@components/looper/forms/LPLabelInput.vue";
import SidebarFluidLayout from "@components/looper/layout/page/SidebarFluidLayout.vue";
import BlankPageLayout from "@components/looper/layout/page/BlankPageLayout.vue";
export default {
  name: "Testing",
  components: {
    LPTree,
    LPDataTable,
    LPModalForm,
    LPLabelInput,
    SidebarFluidLayout,
    BlankPageLayout,
    LPModal
  },
  data() {
    return {
      testInfoObject: {},
      treeData: [],
      testInfoOptions: {
        deferLoading: 0,
        responsive: false,
        autoWidth: false,
        scrollX: true,
        scrollY: "65vh",
      },
      testInfoColumns: [
        { field: "sysid", label: "系統編號", visible: false },
        { field: "frmname", label: "文檔名稱", visible: false },
        { field: "itemno", label: this.$t('SeqNo'), width: "50px" },
        { field: "frmno", label: this.$t('DocID') },
        { field: "funcitemno", label: this.$t('Function SeqNo') },
        {
          field: "funcdesc",
          label: this.$t('Function Description'),
          render: (data) => {
            return `<pre>${data}</pre>`;
          },
        },
        { field: "functype", label: this.$t('Function Tpye') },
        {
          field: "state",
          label: this.$t('Test'),
          render: (data) => {
            if (data == null) return "";
            if (data == 0) return this.$t('No');
            return this.$t('Yes');
          },
        },
        {
          field: "testdata",
          label: this.$t('Test Data'),
          render: (data) => {
            return `<pre>${data}</pre>`;
          },
        },
        {
          field: "testresult",
          label: this.$t('Test Operation And Result'),
          width: "110px",
          render: (data) => {
            return `<pre>${data}</pre>`;
          },
        },
        {
          field: "question",
          label: this.$t('Bug'),
          width: "150px",
          render: (data) => {
            return `<pre style="color: red;">${data}</pre>`;
          },
        },
        { field: "creator", label: this.$t('Creator') },
        {
          field: "create_date", label: this.$t('Create Date'),
          render: function (data) {
            if (data !== null) {
              data = data.trim().replace(/^(\d{4})(\d{2})(\d{2})$/, "$1-$2-$3");;
            }
            return data;
          }
        },
        {
          field: "operation",
          label: this.$t('Operation'),
          render: function (data, type, row) {
            var id = row.DT_RowId;
            return `<a class="btn btn-edit btn-sm btn-icon btn-secondary" href="#" id="${id}"><i class="fa fa-pencil-alt"></i></a>
                        <a class="btn del-btn btn-sm btn-icon btn-secondary" href="#" id="${id}"><i class="far fa-trash-alt"></i></a>`;
          },
        },
      ],
      systemObject: {},
      testInfoParamsFun: undefined,
      edit_status: false,
      currentObj: {},
      deleteDOM: undefined,
      frameList: [],
    };
  },
  mounted() {
    this.getTreeData();
    var _this = this;
    var formEL = $(this.$refs.testingForm.$el);
    var parent = formEL.find("button:submit").parent();
    parent.append(`<button name="delete" class="btn btn-danger">${this.$t("Delete")}</button>`);
    parent.find("button[name='delete']").on("click", function (e) {
      e.preventDefault();
      _this.deleteTestingInfo(_this.currentObj);
      _this.$refs.testingForm.$refs.modal.hide();
    })
    this.deleteDOM = parent.find("button[name='delete']");
    document.documentElement.style.setProperty('--browseText', `'${this.$t("Browse")}'`);
  },
  methods: {
    uploadExcel(){
      if (!("sysid" in this.systemObject)) return alert(this.$t("Unselected System"));
      let formData = new FormData();
      let file = this.$refs.import_excel.files[0];
      formData.append("excelFile", file);
      formData.append("sysid", this.systemObject.sysid);
      axios.post('/looper/testing/upload_excel', formData)
      .then(res => {
        if (!res.data.status) return alert(res.data.msg);
        alert(this.$t('Upload successful'));
        this.$refs.uploadExcelModal.hide();
        this.nodeSelect(this.systemObject);
      })
      .catch(error => {
        console.error(this.$t('Upload failed') + ':', error);
      });
    },
    frmnoFieldChange() {
      axios
        .get("/looper/testing/add", {
          params: {
            sysid: this.systemObject.sysid,
            frmno: this.testInfoObject.frmno,
          },
        })
        .then((response) => {
          this.testInfoObject.itemno = response.data.data.itemno;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    on_row_click(e, data) {
      if (!(e.target.tagName == "A" || e.target.tagName == "I")) return;
      if (
        e.target.className.split(" ").indexOf("fa-pencil-alt") != -1 ||
        e.target.className.split(" ").indexOf("btn-edit") != -1
      ) {
        this.editTestingInfo(data);
      } else {
        this.deleteTestingInfo(data);
      }
    },
    submitTestingInfo() {
      var self = this;
      var url = "/looper/testing/add";
      if (this.edit_status)
        url = "/looper/testing/update?pk=" + self.testInfoObject.inc_id;
      return new Promise((resolve, reject) => {
        if (this.testInfoObject.frmno == "") {
          alert(this.$t('Document number cannot be empty'));
          reject(false);
        } else {
          var data = new FormData();
          for (let test in self.testInfoObject)
            if (self.testInfoObject[test] != null)
              data.append(test, self.testInfoObject[test])
          axios
            .post(url, data)
            .then((response) => {
              if (!response.data.status) return alert(response.data.msg.fail);
              this.$refs.testInfoTable.filter_column_params_fun = undefined;
              this.testInfoParamsFun = () => {
                return { sysid: this.testInfoObject.sysid || "" };
              };
              this.$nextTick(function () {
                this.$refs.testInfoTable.datatable.search("").draw();
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
    deleteTestingInfo(data) {
      if (!confirm(this.$t("Delete this?"))) return;
      axios
        .post("/looper/testing/delete/" + data.inc_id)
        .then((response) => {
          if (!response.data.status) return alert(response.data.msg);
          this.$refs.testInfoTable.filter_column_params_fun = undefined;
          this.testInfoParamsFun = () => {
            return { sysid: this.testInfoObject.sysid || "" };
          };
          this.$nextTick(function () {
            this.$refs.testInfoTable.datatable.search("").draw();
          });
        })
        .catch((error) => {
          console.log(ereror);
        });
    },
    dblclickTable(data) {
      this.currentObj = data;
      this.editTestingInfo(data);
    },
    editTestingInfo(data) {
      this.testInfoObject = data;
      this.edit_status = true;
      this.$refs.testingForm.$refs.modal.show();
      this.deleteDOM.removeClass('d-none');
    },
    addTestingInfo() {
      if (!("sysid" in this.systemObject)) return alert(this.$t("Unselected System"));
      this.edit_status = false;
      this.testInfoObject = {};
      this.testInfoObject.sysid = this.systemObject.sysid;
      this.$refs.testingForm.$refs.modal.show();
      this.deleteDOM.addClass('d-none');
    },
    getTreeData() {
      axios
        .get("/looper/testing/get_sys_tree")
        .then((response) => {
          this.treeData = response.data.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    frmConfirm() {
      var frmid = $('#frm-select').val();
      axios({
        url: '/looper/testing/get_template_excel', 
        method: 'GET',
        responseType: 'blob', 
        params: {
          ma001: frmid
        }
      }).then((response) => {
        const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        const downloadUrl = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.setAttribute('download', frmid + '.xlsx'); // 设置下载文件的名称
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(downloadUrl);
      }).catch((error) => {
        console.error(this.$t('Error downloading file') + ':', error);
      });
    },
    nodeSelect(data) {
      this.systemObject = data;
      this.testInfoObject.sysid = this.systemObject.sysid;
      this.$refs.testInfoTable.filter_column_params_fun = undefined;
      this.testInfoParamsFun = () => {
        return { sysid: this.testInfoObject.sysid || "" };
      };
      this.$nextTick(function () {
        this.$refs.testInfoTable.datatable.search("").draw();
        $(".testingPage .has-sidebar").addClass("has-sidebar-open")
      });
      axios.get('/looper/testing/get_sys_frm?sysid=' + this.testInfoObject.sysid).then(res => {
        if (res.data.status)
          this.frameList = res.data.data;
      })
    },
  },
};
</script>
<style>
.uploadExcelModal .custom-file-input:lang(en)~.custom-file-label {
  border-top-right-radius: .25rem;
  border-bottom-right-radius: .25rem;
}

.uploadExcelModal .custom-file-input:lang(en)~.custom-file-label:after {
  content: var(--browseText);
}
</style>