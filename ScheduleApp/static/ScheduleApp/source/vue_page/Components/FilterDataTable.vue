<template>
    <div class="LPDataTable">
      <div v-show="searching" class="form-group mb-1">
        <!-- .input-group -->
        <div class="input-group input-group-alt">
          <!-- .input-group -->
          <div class="input-group has-clearable">
            <button
              ref="clear-search"
              type="button"
              class="close"
              aria-label="Close"
              @click="global_search_value = ''"
            >
              <span aria-hidden="true">
                <i class="fa fa-times-circle"></i>
              </span>
            </button>
            <div class="input-group-prepend">
              <span class="input-group-text">
                <span class="oi oi-magnifying-glass"></span>
              </span>
            </div>
            <input
              ref="table-search"
              @keyup="global_search"     
              type="text"
              class="form-control"
              :placeholder="gsearch_placeholder"
              v-model="global_search_value"
            >
          </div>
          <!-- /.input-group -->
          <!-- .input-group-append -->
          <div class="input-group-append">
            <button
              class="btn btn-secondary"
              data-toggle="modal"
              @click="filter_column_toggle"
            >{{$t('Filter Columns')}}</button>
          </div>
          <!-- /.input-group-append -->
        </div>
        <!-- /.input-group -->
      </div>
      <table ref="datatable" :class="[datatable_class]">
        <thead>
          <tr v-if="bands != undefined">
            <th v-for="(item, index) in bands" :key="index" :colspan="item.colspan">{{ item.caption }}</th>
          </tr>
          <tr>
            <th v-if="firstColSelected" style="min-width: 25px">
              <div class="thead-dd dropdown">
                <span class="custom-control custom-control-nolabel custom-checkbox">
                  <input
                    type="checkbox"
                    class="custom-control-input"
                    :id="table_id+'_check-handle'"
                    :indeterminate.prop="select_all_indeterminate"
                    v-model="select_all"
                  >
                  <label class="custom-control-label" :for="table_id+'_check-handle'"></label>
                </span>
                <div
                  class="thead-btn"
                  role="button"
                  data-toggle="dropdown"
                  aria-haspopup="true"
                  aria-expanded="false"
                >
                  <span
                    v-show="selected_count > 0"
                    class="selected-row-info text-muted pl-1"
                  >{{ selected_count }} {{$t('selected')}}</span>
                  <span class="fa fa-caret-down"></span>
                </div>
                <div class="dropdown-menu">
                  <div class="dropdown-arrow"></div>
                  <a class="dropdown-item" href="#" @click="select_all = true">{{$t('Select all')}}</a>
                  <a class="dropdown-item" href="#" @click="select_all = false">{{$t('Unselect all')}}</a>
                  <div class="dropdown-divider"></div>
                  <a class="dropdown-item" href="#">{{$t('Bulk remove')}}</a>
                  <a class="dropdown-item" href="#">{{$t('Bulk edit')}}</a>
                  <a class="dropdown-item" href="#">{{$t('Separate actions')}}</a>
                </div>
              </div>
            </th>
            <th v-for="(item, index) in heads" :key="index">
                <div>{{ item }}</div>
            </th>
          </tr>         
        </thead>
        <tfoot v-if="show_footer">
            <tr>
              <th v-if="firstColSelected"></th>
              <th v-for="(item, index) in heads" :key="index"></th>
            </tr>        
        </tfoot>
      </table>
      <teleport to="body">
        <div
          class="modal fade"
          ref="modalFilterColumns"
          tabindex="-1"
          role="dialog"
          aria-labelledby="modalFilterColumnsLabel"
          aria-hidden="true"
        >
          <!-- .modal-dialog -->
          <div class="modal-dialog modal-dialog-scrollable" role="document">
            <!-- .modal-content -->
            <div class="modal-content">
              <!-- .modal-header -->
              <div class="modal-header">
                <h5 class="modal-title">{{$t('Filter Columns')}}</h5>
              </div>
              <!-- /.modal-header -->
              <!-- .modal-body -->
              <div class="modal-body">
                <!-- #filter-columns -->
                <div>
                  <!-- .form-row -->
                  <div
                    v-for="(filter,index) in filter_column.filters"
                    :key="index"
                    class="form-group form-row filter-row"
                  >
                    <!-- form column -->
                    <div class="col">
                      <select class="custom-select filter-control filter-column" v-model="filter.field">
                        <option
                          v-for="(item, index) in filter_column.columns"
                          :key="index"
                          :value="item.value"
                        >{{item.label}}</option>
                      </select>
                    </div>
                    <!-- /form column -->
                    <!-- form column -->
                    <div class="col">
                      <select
                        class="custom-select filter-control filter-operator"
                        v-model="filter.operator"
                      >
                        <option
                          v-for="(item, index) in filter_column.operator"
                          :key="index"
                          :value="item.value"
                        >{{item.label}}</option>
                      </select>
                    </div>
                    <!-- /form column -->
                    <!-- form column -->
                    <div class="col">
                      <div class="input-group input-group-alt">
                        <input
                          type="text"
                          class="form-control filter-control filter-value rounded mr-2"
                          v-model="filter.value"
                        >
                        <div class="input-group-append">
                          <button
                            class="close remove-filter-row"
                            @click="filter_column_del_filter(filter.id)"
                          >×</button>
                        </div>
                      </div>
                    </div>
                    <!-- /form column -->
                  </div>
                  <!-- /.form-row -->
                </div>
                <!-- #filter-columns -->
                <!-- .btn -->
                <button class="btn btn-reset my-2" @click="filter_column_add_filter">
                  <i class="fa fa-plus mr-1"></i> {{$t('add filter')}}
                </button>
                <!-- /.btn -->
              </div>
              <!-- /.modal-body -->
              <!-- .modal-footer -->
              <div class="modal-footer justify-content-start">
                <button
                  type="button"
                  @click="columnSearch"
                  class="btn btn-primary"
                  data-dismiss="modal"
                >{{$t('Apply filters')}}</button>
                <button type="button" class="btn btn-light" data-dismiss="modal" @click="this.$emit('on_searchClose')">{{$t('Cancel')}}</button>
              </div>
              <!-- /.modal-footer -->
            </div>
            <!-- /.modal-content -->
          </div>
          <!-- /.modal-dialog -->
        </div>
      </teleport>
      <!-- /#modalFilterColumns -->
    </div>
  </template>  
<script>
import LPDataTable from "@components/looper/tables/LPDataTable.vue";
export default {
    name: "FilterDataTable",
    extends:LPDataTable,
}
</script>
