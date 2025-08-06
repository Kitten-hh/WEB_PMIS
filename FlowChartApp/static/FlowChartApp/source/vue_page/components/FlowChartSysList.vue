<template>
    <div class="card card-fluid mb-0 flowChartSysListCard card-expansion-item">    
        <div class="card-header py-2">
          <button class="btn btn-reset d-flex justify-content-center w-100 collapsed" data-toggle="collapse" data-target="#flowChartCollapse" aria-expanded="false" aria-controls="flowChartCollapse"><span class="collapse-indicator text-dark"><i class="fa fa-fw fa-chevron-down"></i></span></button>
        </div>
        <div id="flowChartCollapse" class="card-body p-0 collapse" aria-labelledby="flowChartCollapse">
          <ul class="nav nav-pills scrollX px-2">
              <li class="nav-item"><a class="nav-link show" data-toggle="tab" href='#FlowChart'>{{ $t("Flow chart") }}</a></li>
              <li class="nav-item"><a class="nav-link show" data-toggle="tab" href='#Introduction'>{{ $t("Introduction") }}</a></li>
              <li class="nav-item"><a class="nav-link show active" data-toggle="tab" href='#SystemDoc'>{{ $t("System doc") }}</a></li>
          </ul>      

          <div class="tab-pane fade" id="FlowChart"></div>
          <div class="tab-pane fade" id="Introduction"></div>
          <div class="tab-pane fade show active" id="SystemDoc">
            <LPDataTable
                :columns="systemDocTableColumns"
                datasource="/flowchart/list_docdesign"
                :paging_inline="true"
                :searching="1!=1"
                :row_nowrap="1==1"
                :orderBy="systemDocTable_order_by"
                :del_useless_params="1==1"
                @on_dbclick="systemDocTable_dbclick"
                :custom_options="systemDocTable_custom_options"
                :custom_params_fun="get_systemDocTable_custom_params_fun"
                ref="systemDocTable"
              />
          </div>
        </div>    
    </div>
  </template>
  <script>
import LPDataTable, {DateRender} from "@components/looper/tables/LPDataTable.vue";
  export default {
      name:"FlowChartSysList_Component",
      components:{
        LPDataTable
      },
      data() {
          return {
              systemDocTable_custom_options:{
                responsive:false,
                processing:true,
                scrollY:"20vh",
                paging:false,
                autoWidth:false,
                scrollX:true,
                deferLoading:0                
              },
              systemDocTable_order_by: [
                ["md008", "asc"],
              ],
              systemDocTableColumns:[
                  { field: "md002", label: "md002", visible:false },
                  { field: "md009", label: this.$t("State") },
                  { field: "md008", label: this.$t("Seq No") },
                  { field: "md005", label: this.$t("Catalog No") },
                  { field: "md004", label: this.$t("Catalog Name") },
                  { field: "md003", label: this.$t("Version") },
                  { field: "md006", label: this.$t("Flow Chart No/Doc TaskNo") },
                  { field: "md007", label: this.$t("Data Type") },
                  { field: "md010", label: this.$t("Doc Type") },
                  { field: "md011", label: this.$t("On Going") },
                  { field: "md012", label: this.$t("Remark") },
                  { field: "modi_date", label: this.$t("Modified Date") },
                  { field: "modifier", label: this.$t("Modifier") }
              ],
              flowchartinfo:{}
          }
      },
      mounted() {
        $('.wrapper').on("shown.bs.tab","a[data-toggle='tab']", function (e) {
            $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
        });
      },
      methods:{
          get_systemDocTable_custom_params_fun() {
              if (this.flowchartinfo) {
                  var systemormodule = this.flowchartinfo.systemormodule;
                  var flowcharttype = this.flowchartinfo.flowcharttype;
                  if (flowcharttype == "system" && systemormodule != undefined && systemormodule != "")
                      return {
                          attach_query: `{"condition":"AND",
                        "rules":[
                            {"id":"md002","field":"md002","type":"string","input":"text","operator":"equal","value":"${systemormodule}"}],
                            "not":false,"valid":true}`
                      };
              }
              return {
                  attach_query: `{"condition":"AND",
                    "rules":[
                        {"id":"md002","field":"md002","type":"string","input":"text","operator":"equal","value":"xxx"}],
                        "not":false,"valid":true}`
              };
          },
          setFlowChartInfo(info) {
            this.flowchartinfo = Object.assign({}, info);
            this.$refs.systemDocTable.datatable.search("").draw()
          },
          systemDocTable_dbclick(data) {
            var no = data.md006;
            var dataType = data.md007
            this.$emit("show_doc_click", dataType, no);
          }
      }
  }
  </script>
<style>
.flowChartSysListCard.card-expansion-item.expanded .card-header {
  border-bottom: 0;
  padding-top: 0 !important;
  padding-bottom: 0 !important;
}

#SystemDoc .LPDataTable .dataTables_wrapper div:nth-child(2).row {
  display: none;
}

#SystemDoc .LPDataTable .table thead th {
  padding-top: .5rem;
  padding-bottom: .5rem;
}

/* dataTable */
.LPDataTable table.dataTable thead .sorting:before,
.LPDataTable table.dataTable thead .sorting_asc:before,
.LPDataTable table.dataTable thead .sorting_desc:before,
.LPDataTable table.dataTable thead .sorting_asc_disabled:before,
.LPDataTable table.dataTable thead .sorting_desc_disabled:before {
  content: "\f0de" !important;
  right: 0.5em !important;
  top: 12px;
}

.LPDataTable table.dataTable thead .sorting:after,
.LPDataTable table.dataTable thead .sorting_asc:after,
.LPDataTable table.dataTable thead .sorting_desc:after,
.LPDataTable table.dataTable thead .sorting_asc_disabled:after,
.LPDataTable table.dataTable thead .sorting_desc_disabled:after {
  content: "\f0dd" !important;
  right: 0.5em !important;
  top: 12px;
}

</style>