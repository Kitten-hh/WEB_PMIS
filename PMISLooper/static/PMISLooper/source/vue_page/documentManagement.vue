<template>
  <header class="page-title-bar documentMagtHeader mb-0 py-1">
    <div class="d-flex justify-content-between align-items-center">
      <h4 class="card-title mb-0 px-3"> 文件管理窗體 </h4>
      <div class="btn-toolbar">
        <OperationBar class="buttonBar border-bottom-0" ref="buttonBar" :audit_items="auditItems"
          :function_items="functionItems" @on-add="doAdd" @on-undo="doUndo" @on-edit="doEdit" @on-save="doSave"
          @on-delete="doDelete" @on-search="doSearch" @onAudit="doAudit" @onUnAduit="doAudit" @onFun1="onFun1"
          @onFun2="onFun2" @onFun3="onFun3" @onFun4="onFun4" :size="'btn-sm'" />
      </div>
    </div>
  </header>
  <div class="page-section position-relative border-top">
    <sidebarFluidLayout customClass="documentMagtPage">
      <template v-slot:pageDetails>
        <div class="board document_tree py-2 pl-4 pr-3 scrollbar">
          <LPTree ref="lpTree" :data="treeData" @selectNode="nodeSelect" @dblclickNode="Nodedblclick"
            :set_menus="set_menus" :key="treeKey" />
        </div>
      </template>
      <template v-slot:sidebarDetails>
        <div class="card managerMasterCard">
          <div class="card-body scrollHeight scrollbar p-0">
            <h4 class="fs14 py-2 px12 mb-0 border-bottom"> 文件最新版本 </h4>
            <LPDataTable :paging="false" :paging_inline="true" :searching="false" :custom_options="MasterOptions"
              :columns="MasterColumns" :datasource="MasterDatasource" :pageLength="10" @on_row_click="on_row_click_tab"
              class="managerMasterTable" />
          </div>
        </div>
        <div class="card-deck-xl">
          <div class="card card-fluid documentDetailCard">
            <div class="card-header">
              <ul class="nav nav-tabs card-header-tabs">
                <li class="nav-item">
                  <a class="nav-link active show" data-toggle="tab" href="#file_history_version">文件歷史版本</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" data-toggle="tab" href="#file_correction_record">文件修正記錄</a>
                </li>
              </ul>
            </div>
            <div class="card-body scrollHeight scrollbar p-0">
              <div class="tab-content">
                <div class="tab-pane fade active show" id="file_history_version">
                  <h4 class="fs14 pt-2 px12 mb-0" v-show="fileID"> 文件編號為{{ fileID }}的歷史文件！ </h4>
                  <LPDataTable :paging="false" :paging_inline="true" :searching="false" :columns="HistoryDetailColumns"
                    :datasource="HistoryDetailDatasource" :pageLength="10" ref="historyDetailTable_tab" />
                </div>
                <div class="tab-pane fade show" id="file_correction_record">
                  <LPDataTable :paging="false" :paging_inline="true" :searching="false" :columns="CorrectionDetailColumns"
                    :datasource="CorrectionDetailDatasource" :pageLength="10" ref="correctionDetailTable_tab" />
                </div>
              </div>
            </div>
          </div>
          <div class="card card-fluid attachmentsCard">
            <div class="card-body scrollHeight scrollbar p-0">
              <h4 class="fs14 pt-2 px12 mb-0" v-show="fileID"> 文件編號為{{ fileID }}的A版附件！ </h4>
              <LPDataTable :paging="false" :paging_inline="true" :searching="false" :columns="attachmentsColumns"
                :datasource="attachmentsDatasource" :pageLength="10" ref="attachmentsTable" />
            </div>
          </div>
        </div>
      </template>
    </sidebarFluidLayout>
  </div>
</template>
<script>
import sidebarFluidLayout from "@components/looper/layout/page/SidebarFluidLayout.vue";
import LPTree from "@components/looper/general/LPTree.vue";
import LPDataTable, { DateRender } from "@components/looper/tables/LPDataTable.vue";
import OperationBar from "@components/looper/navigator/OperationBar.vue";

export default {
  name: "documentManagement_vueFrm",
  components: {
    sidebarFluidLayout,
    LPTree,
    LPDataTable,
    OperationBar,
  },
  data() {
    return {
      functionItems: [
        { label: "上傳文件", event: "onFun1" },
        { label: "錄入變更單", event: "onFun2" },
        { label: "版本變更", event: "onFun3" },
        { label: "修正記錄", event: "onFun4" },
      ],
      auditItems: [
        { label: "審核", event: "onAudit" },
        { label: "反審核", event: "onUnAduit" },
      ],

      treeData: [
        {
          icon: "fa fa-folder text-yellow",
          name: "質量手冊",
          selected: "false",
        },
        {
          icon: "fa fa-folder text-yellow",
          name: "程序文件",
          selected: "false",
        },
        {
          icon: "fa fa-folder text-yellow",
          name: "三級文件",
          selected: "false",
          children: [
            {
              name: "文控中心",
              icon: "fa fa-folder text-yellow",
              selected: "false",
            },
            {
              name: "管理部",
              icon: "fa fa-folder text-yellow",
              selected: "false",
            },
            {
              name: "品管部",
              icon: "fa fa-folder text-yellow",
              selected: "false",
            },
            {
              name: "電腦部",
              icon: "fa fa-folder text-yellow",
              selected: "false",
            },
          ]
        }
      ],
      MasterOptions: {
        deferLoading: 0,
        scrollY: '40vh',
        scrollX: true,
        autoWidth: false,
        responsive: false,
      },
      MasterColumns: [
        { field: "d0001", label: "文件編號", },
        { field: "d0002", label: "版本", },
        { field: "d0003", label: "文件名稱", },
        { field: "d0004", label: "文件類別", },
        { field: "d0005", label: "文件內容", },
        { field: "d0006", label: "審核碼", },
        { field: "d0007", label: "審核人", },
        { field: "d0008", label: "審核時間", },
        { field: "d0009", label: "批准人", },
        { field: "d0010", label: "生效時間", },
        { field: "d0011", label: "總頁數", },
        { field: "d0012", label: "備註", },
        { field: "d0013", label: "編寫人", },
      ],
      MasterDatasource: [
        { d0001: "WI-4110-001", d0002: 'A', d0003: '作業指導書', d0004: '三級文件', d0005: '', d0006: 'Y:審核', d0007: '廖梅', d0008: '2009-08-01', d0009: '葛雄威', d0010: '2009-08-01', d0011: 3, d0012: ' ', d0013: '唐愛君', },
        { d0001: "WI-4110-002", d0002: 'A', d0003: '作業指導書', d0004: '三級文件', d0005: '', d0006: 'Y:審核', d0007: '廖梅', d0008: '2009-08-01', d0009: '葛雄威', d0010: '2009-08-01', d0011: 3, d0012: ' ', d0013: '唐愛君', },
      ],
      HistoryDetailColumns: [
        { field: "d0001", label: "文件編號", },
        { field: "d0002", label: "版本", },
        { field: "d0003", label: "文件名稱", },
        { field: "d0004", label: "文件類別", },
        { field: "d0005", label: "文件內容", },
        { field: "d0006", label: "審核碼", },
        { field: "d0007", label: "審核人", },
        { field: "d0008", label: "審核時間", },
        { field: "d0009", label: "批准人", },
        { field: "d0010", label: "生效時間", },
        { field: "d0011", label: "總頁數", },
        { field: "d0012", label: "修改內容", },
        { field: "d0013", label: "備註", },
        { field: "d0014", label: "修改時間", },
        { field: "d0015", label: "編寫人", },
      ],
      HistoryDetailDatasource: [
        { d0001: "WI-4110-001", d0002: 'A', d0003: '作業指導書', d0004: '三級文件', d0005: '', d0006: 'Y:審核', d0007: '廖梅', d0008: '2009-08-01', d0009: '葛雄威', d0010: '2009-08-01', d0011: 3, d0012: ' ', d0013: '唐愛君', d0014: '唐愛君', d0015: '唐愛君', },
        { d0001: "WI-4110-001", d0002: 'A', d0003: '作業指導書', d0004: '三級文件', d0005: '', d0006: 'Y:審核', d0007: '廖梅', d0008: '2009-08-01', d0009: '葛雄威', d0010: '2009-08-01', d0011: 3, d0012: ' ', d0013: '唐愛君', d0014: '唐愛君', d0015: '唐愛君', },
      ],
      CorrectionDetailColumns: [
        { field: "c0001", label: "版本", },
        { field: "c0002", label: "修正日期", },
        { field: "c0003", label: "生效時間", },
        { field: "c0004", label: "主要修正內容", },
        { field: "c0005", label: "匯簽部門", },
        { field: "c0006", label: "編寫人", },
        { field: "c0007", label: "審核人", },
        { field: "c0008", label: "批准人", },
        { field: "c0009", label: "批准人", },
        { field: "c0010", label: "備註", },
      ],
      CorrectionDetailDatasource: [],
      attachmentsColumns: [
        { field: "a0001", label: "附件名稱", },
        { field: "a0002", label: "文件名稱", },
        { field: "a0003", label: "版本", },
      ],
      attachmentsDatasource: [
        { a0001: 'WI-1300-001-A硬件及網絡維護作業指導書.doc', a0002: 'WI-1300-001', a0003: 'A' }
      ],
      fileID: ''
    }
  },
  mounted() {
    this.checkAndAddOpenClass();
    $(".documentMagtHeader").parent().addClass("documentMagtPageInner")
  },
  methods: {
    checkAndAddOpenClass() {
      const treeContent = $('.tree-menu li.tree-content');
      const hasCaretDownClass = $('.tree-menu span.fa-caret-down').length > 0;

      if (hasCaretDownClass) {
        treeContent.addClass('tree-open');
      } else {
        $('.tree-menu span.icon').on('click', function () {
          $(this).closest('li.tree-content').toggleClass('tree-open');
        });
      }
    },
    on_row_click_tab(event, data) {
      this.fileID = data['d0001'];

    },
  },
};
</script>