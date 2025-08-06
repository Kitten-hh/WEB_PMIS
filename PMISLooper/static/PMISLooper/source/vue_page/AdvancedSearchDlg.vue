<script>
import axios from "axios"
import { getCurrentInstance, reactive, ref, onMounted } from 'vue'
import LPDataTable, { DateRender } from "@components/looper/tables/LPDataTable.vue";

export default {
  name: "AdvancedSearchDlg",
  components: {
    LPDataTable
  },
  props: {
    masterColumns: {
      type: Array,
      default: []
    },
    detailColumns: {
      type: Array,
      default: []
    },
  },
  setup(props,ctx) {
    loadCss("/static/BaseApp/vendor/devextreme/css/dx.common.css");
    loadCss("/static/BaseApp/vendor/devextreme/css/dx.dark.css");
    loadCss("/static/BaseApp/vendor/devextreme/css/dx.light.css");
    loadJs(["/static/BaseApp/vendor/devextreme/js/dx.all.js"], true);
    const $t = getCurrentInstance().appContext.config.globalProperties.$t;
    const modal = ref(null);
    const queryFilterTable = ref(null);
    const masterFilter = ref(null);
    const detailFilter = ref(null);
    const data = reactive({
      columns: [
        { field: 'qf013', label: $t("Query statement"), visible: false },
        { field: 'qf025', label: "查詢編號" }, //"查詢編號"
        { field: 'qf012', label: "排序" }, //"排序"
        { field: 'qf003', label: "條件名稱", width: '200px' }, //"條件名稱"
        { field: 'qt002', label: "類別" }, //"類別"
        { field: 'qf008', label: "關鍵字" }, //"關鍵字"
        { field: 'qf023', label: "客戶" }, //"客戶"
        { field: 'qf024', label: "查詢類型" }, //"查詢類型"
        {
          field: 'qf020', label: "同步Calendar", render: (d) => {
            return `<input type="checkbox" ${d === "Y" ? "checked" : ""} disabled/>`
          }
        }, //"同步Calendar"
        { field: 'qf021', label: "Google日曆名稱首碼" }, //"Google日曆名稱首碼"
      ],
      Options: {
        responsive: false,
        scrollY: 'calc(100% - 31.59px)',
        processing: true,
        autoWidth: false,
        scrollX: true,
        deferLoading: 0,
      },
      masterColumns: convertColumns(props.masterColumns),
      detailColumns: convertColumns(props.detailColumns),
      masterInstance: null,
      detailInstance: null,
      defaultOptions: {
        filterOperationDescriptions: {
          between: $t("Between"),
          contains: $t("Contains"),
          endsWith: $t("Ends with"),
          equal: $t("Equals"),
          greaterThan: $t("Greater than"),
          greaterThanOrEqual: $t("Greater than or equal to"),
          isBlank: $t("Is blank"),
          isNotBlank: $t("Is not blank"),
          lessThan: $t("Less than"),
          lessThanOrEqual: $t("Less than or equal to"),
          notContains: $t("Does not contain"),
          notEqual: $t("Does not equal"),
          startsWith: $t("Starts with")
        },
        groupOperationDescriptions: {
          and: $t("And"),
          notAnd: $t("Not And"),
          notOr: $t("Not Or"),
          or: $t("Or")
        }
      },
      queryStatement: ''
    })
    function convertColumns(columns) {
      if (columns == undefined)
        return undefined;
      var result = [];
      for (var column of columns)
        if (column.type != undefined && column.type.toLowerCase() == "date")
          result.push(Object.assign({
            format: "yyyy-MM-dd",
            editorOptions: {
              displayFormat: "yyyy-MM-dd",
              dateSerializationFormat: "yyyy-MM-dd"
            }
          }, { dataField: column.field, caption: column.label, dataType: column.type }))
        else
          result.push(Object.assign({}, { dataField: column.field, caption: column.label, dataType: column.type }))
      return result;
    };
    function dxFilterUtils() {
      const querybuilderCondition = Object.freeze({ and: 'AND', or: 'OR' });
      const querybuilderOperator = Object.freeze({
        IS_NULL: 'is_null',
        IS_NOT_NULL: 'is_not_null',
        "=": 'equal',
        "<>": 'not_equal',
        "<": 'less',
        "<=": 'less_or_equal',
        ">": 'greater',
        ">=": 'greater_or_equal',
        between: 'between',
        startswith: 'begins_with',
        endswith: 'ends_with',
        anyof: 'in',
        IS_EMPTY: 'is_empty',
        IS_NOT_EMPTY: 'is_not_empty',
        contains: 'contains',
        notcontains: 'not_contains',
      });
      const isArray = (val) => { return Object.prototype.toString.apply(val) === '[object Array]' };
      const isString = (val) => { return Object.prototype.toString.apply(val) === '[object String]' };
      const isIndexOf = (val) => { return ["and", "or", "!"].indexOf(val) != -1 }
      const convertOperation = (operation) => {
        operation = operation.toLowerCase();
        return querybuilderOperator[operation]
      }
      const parseOneDxFilter = (filterObj) => {
        try {
          const field = filterObj[0];
          const operation = filterObj[1];
          const values = filterObj[2];
          const qbOperation = convertOperation(operation);
          if (values === null || values === "") {
            if (operation === "=")
              qbOperation = querybuilderOperator.IS_NULL
            else
              qbOperation = querybuilderOperator.IS_NOT_NULL
          }
          return { "id": field, "field": field, "type": "string", "input": "text", "operator": qbOperation, "value": values }
        } catch (e) {
          return undefined;
        }
      }
      const subParseDxFilter = (filterValue) => {
        const result = {};
        if (!isArray(filterValue)) return undefined;
        const joinArray = filterValue.filter(x => isString(x) && isIndexOf(x));
        const filterArray = filterValue.filter(x => !(isString(x) && isIndexOf(x)));
        if (joinArray.length > 0) {
          const str = joinArray[0]
          if (str === "!") {
            joinArray = filterValue[1].filter(x => isString(x) && isIndexOf(x));
            if (joinArray.length > 0) {
              str = joinArray[0]
              filterArray = filterValue[1].filter(x => !(isString(x) && isIndexOf(x)));
              result["condition"] = querybuilderCondition[str];
              result["rules"] = [];
              result["not"] = true;
              result["valid"] = true;
            } else {
              result["condition"] = querybuilderCondition["and"];
              result["rules"] = [];
              result["not"] = true;
              result["valid"] = true;
            }
          } else {
            result["condition"] = querybuilderCondition[str];
            result["rules"] = [];
            result["not"] = true;
            result["valid"] = true;
          }
          for (var i = 0; i < filterArray.length; i++) {
            const condition = subParseDxFilter(filterArray[i]);
            if (condition != undefined) {
              result.rules.push(condition);
            }
          }
          return result;
        } else {
          return parseOneDxFilter(filterValue);
        }
      }
      this.subParseDxFilter = subParseDxFilter;
    }
    function parseDxFilter(filterValue) {
      const o = new dxFilterUtils();
      if (filterValue === null)
        return undefined;
      const result = o.subParseDxFilter(filterValue);
      if (!result.hasOwnProperty("condition")) {
        return { "condition": "AND", "rules": [result], "not": false, "valid": true };
      } else
        return result;
    }
    function init() {
      try {
        data.masterInstance = $(masterFilter.value).dxFilterBuilder("instance");
      } catch (e) {
        if (data.masterInstance === null) {
          $(masterFilter.value).dxFilterBuilder(Object.assign(data.defaultOptions, {
            fields: data.masterColumns, height: "100%"
          }));
          data.masterInstance = $(masterFilter.value).dxFilterBuilder("instance");
        }
      }
      if (data.detailColumns.length > 0) {
        try {
          data.detailInstance = $(detailFilter.value).dxFilterBuilder("instance");
        } catch (e) {
          if (data.detailInstance === null) {
            $(masterFilter.value).dxFilterBuilder(Object.assign(data.defaultOptions, { fields: data.detailColumns, height: "100%" }));
            data.detailInstance = $(detailFilter.value).dxFilterBuilder("instance");
          }
        }
      }
    }
    onMounted(() => {
      DevExpress.localization.loadMessages({
        "en": {
          "dxFilterBuilder-addCondition": $t("Add Condition"),
          "dxFilterBuilder-addGroup": $t("Add Group"),
          "dxFilterBuilder-enterValueText": $t("<enter a value>")
        }
      });
      init();
      String.prototype.render = undefined;
    })
    const event = reactive({
      showModal: () => { $(modal.value).modal("show") },
      hideModal: () => { $(modal.value).modal("hide") },
      allContion: () => {
        axios.get("/looper/task/enquiry/query_filter?username=" + get_username()).then(res => {
          if (res.data.status)
            queryFilterTable.value.datatable.clear().rows.add(res.data.data || []).draw();
        })
      },
      search: () => {
        const masterFilter = data.masterInstance.option("value");
        ctx.emit('search',parseDxFilter(masterFilter))
      },
      rightOneClick: () => {
        const selected = $("#fieldselect li.active");
        selected.each(function (index) {
          var field = $(this).attr("field");
          var label = $(this).text();
          if ($(`#fieldset li[field='${field}']`).length == 0) {
            var html = `<li class="list-group-item list-group-item-action px-2 py-1" field="${field}">${label}</li>`
            $("#fieldset").append(html);
          }
        });
      },
      leftOneClick: () => {
        const selected = $("#fieldset li.active");
        selected.each(function (index) {
          $(this).remove();
        });
      },
      fieldListClick: ($event) => {
        $($event.target).siblings().removeClass('active');
        $($event.target).toggleClass('active')
      },
      rowSelected: (e, d, t, i) => {
        if (e.type === "select") {
          const selectedData = queryFilterTable.value.datatable.row($(e.currentTarget).find("tr").eq(i[0] + 1)).data();
          if (selectedData)
            data.queryStatement = selectedData.qf013;
          console.log(data.queryStatement)
        } else if (e.type === "deselect") {
          data.queryStatement = '';
        }
      }
    })
    return {
      modal,
      queryFilterTable,
      event,
      data,
      masterFilter,
      detailFilter
    }
  }
}
</script>
<template>
  <div class="modal fade" tabindex="-1" role="dialog" aria-hidden="true" ref="modal">
    <div class="modal-dialog modal-dialog-scrollable" role="document" style="max-width: 1200px;">
      <div class="modal-content advancedSearchDlgContent">
        <div class="modal-header align-items-center py-2 shadow-none">
          <h5 class="modal-title">通用查詢</h5>
          <button type="button" class="close py-2" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">×</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="containers row search_container">
            <div class="col-12 col-md-7 d-flex flex-column">
              <LPDataTable ref="queryFilterTable" class="queryFilterTable" :datasource="[]" :columns="data.columns" :custom_options="data.Options"
                :searching="false" :paging="false" @on_selectornot="event.rowSelected" />
              <div class="el-example mt-2 py-2 border-top">
                <button type="button" class="btn btn-sm btn-outline-primary" @click="event.allContion">全部條件</button>
                <button type="button" class="btn btn-sm btn-outline-primary">修改</button>
                <button type="button" class="btn btn-sm btn-outline-primary">保存</button>
                <button type="button" class="btn btn-sm btn-outline-primary">刪除</button>
              </div>
            </div>
            <div class="col-12 col-md-5">
              <ul class="nav nav-tabs card-header-tabs mb-1 mt-0">
                <li class="nav-item">
                  <a class="nav-link font-weight-bold active" data-toggle="tab" href="#condition">基本條件</a>
                </li>
                <li class="nav-item" v-if="data.detailColumns.length > 0">
                  <a class="nav-link font-weight-bold" data-toggle="tab" href="#sub-condition">其他條件</a>
                </li>
              </ul>
              <div class="tab-content">
                <div class="tab-pane fade active show h-100" id="condition">
                  <div class="card shadow-none h-100">
                    <div class="card-body scrollbar" style="overflow-x:auto">
                      <div ref="masterFilter"></div>
                    </div>
                    <div class="card-footer">
                      <div id="field">
                        <div class="d-flex justify-content-between py-1">
                          <p class="mb-0 ml-1">設置排序字段</p>
                          <label class="custom-control custom-checkbox mb-0 mr-1" v-if="data.detailColumns.length > 0">
                            <input type="checkbox" class="custom-control-input control ck_detail"
                              @change="detailChackboxChange">
                            <span class="custom-control-label">
                              {{ $t('Sub-Condition') }}
                            </span>
                          </label>
                        </div>
                        <div class="d-flex flex-row field-list border-top">
                          <ul id="fieldselect" class="col m-0 list-group scrollbar">
                            <li v-for="(column, key) in data.masterColumns" :key="key"
                              class="list-group-item list-group-item-action px-2 py-1" :field="column.dataField"
                              @click="event.fieldListClick">
                              {{ column.caption }}</li>
                          </ul>
                          <div class="field_operation d-flex flex-column justify-content-center col-auto border-right border-left">
                            <a href="#" class="right_one" @click="event.rightOneClick"><i
                                class="fas fa-angle-double-right"></i></a>
                            <a href="#" class="left_one" @click="event.leftOneClick"><i
                                class="fas fa-angle-double-left"></i></a>
                          </div>
                          <ul id="fieldset" class="col m-0 list-group scrollbar">
                          </ul>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div id="sub-condition" class="tab-pane fade">
                  <div ref="detailFilter"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer justify-content-end py-1">
          <button type="button" class="btn btn-primary" @click="event.search">查詢</button>
          <button type="button" class="btn btn-primary" data-dismiss="modal">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>
<style>
.containers {
  /* height: 650px; */
  height: 100%;
}

/* .search_container .left{
    width:160px;
} */
#field {
  height: 154px;
  width: 100%;
}

#field .field-list {
  height: calc(100% - 24px);
}

.search_container .tab-content {
  /* height: calc(100% - 38px); */
  height: calc(100% - 46px);
  margin-left: -10px;
  margin-right: -10px;
}

/* .search_container .query_list {
    height: calc(100% - 34px);
    background-color: white;
}
.search_container .query_list .list-group {
    height: 100%;
} */
.search_container .scrollbar {
  overflow-y: auto;
}

/* #searchBox {
    height:calc(100%);
} */
/* .viewsqlname {
    font-size: 0.8rem;
} */
.search_container .nav-link {
  padding-top: .25rem;
  padding-bottom: .25rem;
}

#fieldselect,
#fieldset {
  font-size: 0.8rem;
}

/* 日历控件大小 */
.dx-datebox-wrapper-calendar .dx-calendar {
  margin: 10px;
  height: 220.6px;
  min-height: 220.6px;
}

.LPDataTable.queryFilterTable .dataTables_scrollHeadInner .table {
  margin-top: 0 !important;
}

.LPDataTable.queryFilterTable th,
.LPDataTable.queryFilterTable td {
  padding: .3rem;
  font-size: 14px;
}

.LPDataTable.queryFilterTable table.dataTable thead .sorting:before,
.LPDataTable.queryFilterTable table.dataTable thead .sorting_asc:before,
.LPDataTable.queryFilterTable table.dataTable thead .sorting_desc:before,
.LPDataTable.queryFilterTable table.dataTable thead .sorting:after,
.LPDataTable.queryFilterTable table.dataTable thead .sorting_asc:after,
.LPDataTable.queryFilterTable table.dataTable thead .sorting_desc:after {
  top: 8px;
}

/* model-body內容的高度調整 */
.LPDataTable.queryFilterTable {
  flex: 1;
  overflow-y: auto;
  height: 100%;
}
.LPDataTable.queryFilterTable .dataTables_wrapper,
.LPDataTable.queryFilterTable .dataTables_wrapper>div,
.LPDataTable.queryFilterTable .dataTables_wrapper>div>.dataTables_scroll {
  height: 100%;
}
.advancedSearchDlgContent {
  height: 750px;
}

/* 邊框樣式 */
.advancedSearchDlgContent .modal-footer,
.advancedSearchDlgContent #fieldselect,
.advancedSearchDlgContent #fieldset {
  box-shadow: none;
}
.search_container>div {
  border-radius: 0.3rem;
  border: 3px solid rgba(34, 34, 48, .1) !important;
}

.search_container>div:first-child {
  margin-bottom: .25rem;
  height: 48%;
}
.search_container>div:last-child {
  margin-bottom: 1rem;
  height: 50%;
}

@media (min-width: 768px) {
  .advancedSearchDlgContent .modal-body {
    overflow-y: hidden;
  }

  .search_container .tab-content {
    height: calc(100% - 40px);
  }

  .search_container>div:first-child {
    border-top-right-radius: 0;
    border-bottom-right-radius: 0;
    border-right: 0 !important;
    height: 100%;
  }
  .search_container>div:last-child {
    border-top-left-radius: 0;
    border-bottom-left-radius: 0;
    border-left-width: 1px !important;
    height: 100%;
  }

}
</style>
