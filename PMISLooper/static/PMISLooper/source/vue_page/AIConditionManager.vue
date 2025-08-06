<template>
    <div class="page-inner AIConditionManagerPage">
        <ActionToolbar ref="actionToolbar" :toolbarTitle="$t('AI Condition Manager')"
            module_power="65535" :function_items="functionItems" :audit_items="auditItems" :button_show="button_show"
            @on-search="doSearch" @on-add="doAdd" @on-edit="doEdit" @on-delete="doDelete">
            <!--AI條件管理(AIConditionConfigPanel_vueFrm)-->
        </ActionToolbar>
        <TabBar :tabList="tabs" :Hasdropdown="false" class="AIConditionManagerTab mb-0" ref="tabBar" @click="handleTabClick">
            <template v-slot:Category_list>
                <LPDataTable :paging="true" :paging_inline="true" :searching="1 != 1" :columns="categoryColumns"
                    :firstColSelected="true" :custom_params_fun="categoryParamsFun"
                    datasource="/looper/promptcategorytbl/table" :custom_options="categoryOptions"
                    @on_dbclick="category_dbclick" @on_row_click="category_row_click" ref="categoryTable" />
            </template>
            <template v-slot:PromtSQL_list>
                <LPDataTable :paging="true" :paging_inline="true" :searching="1 != 1" :columns="masterColumns"
                    :firstColSelected="true" :custom_params_fun="masterParamsFun"
                    datasource="/looper/promtsql/table" :custom_options="masterOptions" @on_dbclick="table_dbclick"
                    @on_row_click="table_row_click" ref="promtSQLTable" />
            </template>
        </TabBar>
    </div>

    <LPModalForm ref="edit_promtsqlForm" :title="modal_title" @on_submit="save_submit">
        <LPLabelInput :label="$t('SSID')" class="pt-2"><!--編號-->
            <input type="text" class="form-control" v-model="promtsql.ssid" disabled>
        </LPLabelInput>
        <LPLabelInput :label="$t('Category')"><!--分類-->
            <select class="select2-category form-control" v-model="promtsql.category"></select>
        </LPLabelInput>
        <LPLabelInput label="">
            <label>
                {{ $t('SName') }} <span class="required">*</span><!--名稱-->
            </label>
            <textarea class="form-control" rows="3" v-model="promtsql.sname"></textarea>
        </LPLabelInput>
        <LPLabelInput label="">
            <label>
                {{ $t('PromptByAi') }} <span class="required">*</span><!--生成AI的條件-->
            </label>
            <textarea class="form-control" rows="3" v-model="promtsql.promptbyai"></textarea>
        </LPLabelInput>
        <LPLabelInput>
            <div class="custom-control custom-control-inline custom-checkbox">
                <input type="checkbox" class="custom-control-input" id="ckb1" v-model="promtsql.isapproved"
                    true-value="Y"
                    false-value="N"
                    > 
                <label class="custom-control-label" for="ckb1">{{ $t('IsApproved') }}</label><!--是否審批-->
            </div>
        </LPLabelInput>
        <LPLabelInput>
            <div class="custom-control custom-control-inline custom-checkbox">
                <input type="checkbox" class="custom-control-input" id="ckb2" v-model="promtsql.isai"
                    true-value="Y"
                    false-value="N"
                    disabled> 
                <label class="custom-control-label" for="ckb2">{{ $t('IsAi') }}</label><!--是否AI生成-->
            </div>
        </LPLabelInput>
        <LPLabelInput>
            <div class="custom-control custom-control-inline custom-checkbox">
                <input type="checkbox" class="custom-control-input" id="ckb3" v-model="promtsql.isdatabasesql"
                    true-value="Y"
                    false-value="N"
                    disabled> 
                <label class="custom-control-label" for="ckb3">{{ $t('IsDatabaseSQL') }}</label><!--是否數據庫SQL-->
            </div>
        </LPLabelInput>
    </LPModalForm>

    <LPModalForm ref="edit_categoryForm" :title="category_title" @on_submit="save_category_submit">
        <LPLabelInput :label="$t('CategoryNo')" class="pt-2"><!--分類編號-->
            <input type="text" class="form-control" v-model="category.categoryno" disabled>
        </LPLabelInput>
        <LPLabelInput label="">
            <label>
                {{ $t('Category') }} <span class="required">*</span><!--分類-->
            </label>
            <input type="text" class="form-control" v-model="category.category">
        </LPLabelInput>
        <LPLabelInput :label="$t('Description')"><!--分類描述-->
            <textarea class="form-control" rows="3" v-model="category.description"></textarea>
        </LPLabelInput>
        <LPLabelInput :label="$t('Remark')"><!--備註-->
            <textarea class="form-control" rows="3" v-model="category.remark"></textarea>
        </LPLabelInput>
    </LPModalForm>

    <div class="modal fade my-modal-parent" id="messageModal" tabindex="-1" role="dialog"
        aria-labelledby="messageModalTitle" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ $t("Message") }}</h5>
                    <button type="button" class="close text-dark" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <p id="msg" class="font-weight-bolder text-dark"></p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary btn-cancel"
                        data-dismiss="modal">{{ $t("Close") }}</button>
                </div>
            </div>
        </div>
    </div>

</template>
<script>
import ActionToolbar from "@components/looper/layout/ActionToolbar.vue";
import LPDataTable, { DateRender } from "@components/looper/tables/LPDataTable.vue";
import LPLabelInput from "@components/looper/forms/LPLabelInput.vue";
import LPFlatpickerDate from "@components/looper/forms/LPFlatpickerDate.vue";
import LPModalForm from "@components/looper/layout/LPModalForm.vue";
import axios from "axios";
import TabBar from "@components/looper/navigator/TabBar.vue";
export default {
    name: "AIConditionManager_vueFrm",
    components: {
        ActionToolbar,
        LPDataTable,
        LPLabelInput,
        LPFlatpickerDate,
        LPModalForm,
        TabBar
    },
    data() {
        var self = this
        return {
            tabs: [
                { tabid: 'Category_list', label: this.$t("AI Condition Category List"), bodyname: 'Category_list' }, //AI條件類別列表
                { tabid: 'PromtSQL_list', label: this.$t("AI Condition List"), bodyname: 'PromtSQL_list' }, //AI條件列表
            ],
            masterOptions: {
                // deferLoading: 0,
                // scrollY: true,
                scrollX: true,
                autoWidth: false,
                responsive: false,
                scrollY: "67vh",
                drawCallback: function() {
                    self.$refs.promtSQLTable.getSelectedInfo();
                }
            },
            categoryOptions: {
                // deferLoading: 0,
                // scrollY: true,
                scrollX: true,
                autoWidth: false,
                responsive: false,
                scrollY: "67vh",
                drawCallback: function() {
                    self.$refs.categoryTable.getSelectedInfo();
                }
            },
            masterColumns: [
                { field: "inc_id", label: "inc_id", visible: false },
                { field: 'ssid', label: this.$t('SSID') }, //編號
                { field: 'sname', label: this.$t('SName') }, //名稱
                { field: 'category', label: this.$t('Category'), render: function (data, type, row){
                    return row.categoryname
                } }, //分類
                { field: 'categoryname', label: '', visible: false }, //分類名稱
                {
                    field: 'isai', label: this.$t('IsAi'), //是否AI生成
                    render: function (data, type, row) {
                        if (data != "1" && data != "0") return data
                        var checked = "";
                        if (data == "1") {
                            checked = "checked";
                        }
                        return `<input type='checkbox' {0} onclick="return false;"> `.format(checked);
                    },
                },
                {
                    field: 'isapproved', label: this.$t('IsApproved'), //是否審批
                    render: function (data, type, row) {
                        if (data != "1" && data != "0") return data
                        var checked = "";
                        if (data == "1") {
                            checked = "checked";
                        }
                        return `<input type='checkbox' {0} onclick="return false;"> `.format(checked);
                    },
                },
                {
                    field: 'isdatabasesql', label: this.$t('IsDatabaseSQL'), //是否數據庫SQL
                    render: function (data, type, row) {
                        if (data != "1" && data != "0") return data
                        var checked = "";
                        if (data == "1") {
                            checked = "checked";
                        }
                        return `<input type='checkbox' {0} onclick="return false;"> `.format(checked);
                    },
                },
                { field: 'sdate', label: this.$t('SDate'), render: DateRender }, //創建時間
                { field: 'ssql', label: this.$t('SSQL'), visible: false }, //sql語句
                { field: 'params', label: this.$t('Params'), visible: false }, //參數
                { field: 'remark', label: this.$t('Remark'), visible: false }, //備註
                { field: 'sql_description', label: this.$t('SQL_Description'), visible: false }, //SQL描述
                { field: 'timestamp', label: this.$t('TimeStamp'), render: DateRender, visible: false }, //操作時間
                { field: 'promptbyai', label: this.$t('PromptByAi'), visible: false }, //生成AI的條件
            ],
            categoryColumns: [
                { field: "inc_id", label: "inc_id", visible: false },
                { field: 'categoryno', label: this.$t('CategoryNo'), width: "120px", }, //分類編號
                { field: 'category', label: this.$t('Category') }, //分類
                { field: 'description', label: this.$t('Description'), width: "30%", }, //分類描述
                { field: 'remark', label: this.$t('Remark'), width: "30%", }, //備註
            ],
            masterParamsFun: undefined,
            categoryParamsFun: undefined,
            promtsql: {},
            category: {},
            modal_title: this.$t('Edit AI Condition'), //編輯AI條件
            category_title: this.$t('Edit AI Condition Category'), //編輯AI條件類別
            state: '1', //狀態標識對象 1:新增,2:修改
            status: '1', //明細狀態標識對象 1:新增,2:修改
            categoryData: [],
            button_show: '11100100', // 默認顯示查詢、新增、修改、刪除
            activeTab: 'Category_list', // 標簽卡記錄對象,默認為分類頁面
        }
    },
    mounted() {
        $('.wrapper').on("shown.bs.tab", "a[data-toggle='tab']", function (e) {
            $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
        });
        window.addEventListener('resize', () => { $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust() });
        this.updateButtonShow(this.activeTab);
        this.isNoExpanded();
        this.button_show = '11100100';

        this.$nextTick(() => {
            $(".AIConditionManagerTab .LPDataTable .thead-dd").removeClass('dropdown');
            $(".AIConditionManagerTab .LPDataTable .thead-btn").remove();
            $(".AIConditionManagerTab .LPDataTable .thead-dd .dropdown-menu").remove();

        })
        
        this.getBrowser();
    },
    methods: {
        //刪除按鈕點擊事件
        doDelete(){
            if(this.activeTab === 'Category_list'){
                this.category_delete();
            }else{
                this.deleteMaster();
            }
        },
        //修改按鈕點擊事件
        doEdit(){
            this.$refs.actionToolbar.$refs.buttonBar.setToolButtonState();
            if(this.activeTab === 'Category_list'){
                this.category_update();
            }else{
                this.updateMaster();
            }
        },
        //新增按鈕點擊事件(添加類別信息)
        doAdd(){
            this.$refs.actionToolbar.$refs.buttonBar.setToolButtonState();
            //根據用戶當前所在的標簽頁,調用對應的查詢方法
            this.status = '1';
            this.category = {};
            this.get_category_initial();
            this.$refs.edit_categoryForm.$refs.modal.show();
        },
        //查詢按鈕點擊事件
        doSearch(){
            //根據用戶當前所在的標簽頁,調用對應的查詢方法
            if(this.activeTab === 'Category_list'){
                this.category_search();
            }else{
                this.masterSearch();
            }
        },
        // 標簽卡點擊事件
        handleTabClick(event) {
            const target = event.target;
            if (target && target.getAttribute('href')) {
                const tabId = target.getAttribute('href').replace('#', ''); // 获取点击的tabId
                this.activeTab = tabId;
                this.updateButtonShow(tabId); // 更新按钮显示状态
            }
        },
        // 更新 button_show 的状态
        updateButtonShow(tabId) {
            if (tabId === 'Category_list') {
                this.button_show = '11100100'; // 显示查詢、新增、修改、刪除
            } else {
                this.button_show = '01100100'; // 只显示查詢、修改、刪除
            }
        },
        isNoExpanded() {
            if($(".actionToolbar").hasClass("expanded")) {
                $(".actionToolbar").removeClass("expanded");
                $(".actionToolbar .btn-reset").attr("aria-expanded", "false");
                $(".actionToolbar #collapseToolbar").removeClass("show");
            }
        },
        showMessage(msg) {
            $('#msg').html(msg);
            $('#messageModal').modal('show');
        },
        //設置類別下拉選信息
        async setCategoryOptions() {
            var _this = this;
            await axios.get(`/looper/category/array`).then(response => {
                if (response.data.status) {
                    _this.categoryData = response.data.data;
                    $('select.select2-category').empty()
                    for (let d of response.data.data) 
                        $('select.select2-category').append(new Option(d.category, d.categoryno))
                    $('select.select2-category').val(_this.promtsql.category)
                    this.$nextTick(function(){
                        $('select.select2-category').select2().on("select2:select", function (e) {
                            _this.promtsql.category = e.params.data.id;
                        });
                    })
                    
                }
            })
            .catch(error => {
                console.log(error);
            })
        },
        //參數刪除事件
        category_delete() {
            var detailArray = this.$refs.categoryTable.getSelectedFlagData()["datas"];
            // console.log(detailArray.length)
            if (detailArray.length == 0) return this.showMessage(this.$t('Please select data to delete')); //請勾選要刪除的數據
            let flag = confirm(this.$t('Delete selected data?')); //刪除所選數據?
            if (flag) {
                axios.post(`/looper/category/batch_delete`, { details: detailArray })
                    .then(response => {
                        if (response.data.status) {
                            this.category = {}
                            this.refresh_Table('categoryTable');
                        }
                        return this.showMessage(response.data.msg);
                    })
                    .catch(error => {
                        console.log(error);
                    });
            }
        },
        //參數列表雙擊事件
        category_dbclick(data) {
            if (data == undefined) return
            this.status = '2'
            this.$refs.edit_categoryForm.$refs.modal.show();
        },
        //參數列表單擊事件
        category_row_click(event, data) {
            if (data == undefined) return
            this.get_category_info(data.inc_id);
        },
        //獲取參數詳細信息
        get_category_info(inc_id) {
            axios
                .get(`/looper/category/update`, { params: { pk: inc_id } })
                .then((response) => {
                    if (response.data.status) {
                        this.category = response.data.data;
                    }
                });
        },
        //保存參數信息
        save_category_submit() {
            return new Promise((resolve, reject) => {
                if (String(this.category.category || "") == "") {
                    this.showMessage(this.$t('Required fields cannot be empty!')); //必填項不能為空!
                    return reject(false)
                }
                // 根據state值動態設置url
                var url = ''
                if (this.status === '1') {
                    url = `/looper/category/insert`; // 新增的URL
                } else if (this.status === '2') {
                    url = `/looper/category/update?pk=${this.category.inc_id}`; // 修改的URL
                }
                axios
                    .post(
                        url,
                        this.objectToFormData(this.category)
                    )
                    .then((response) => {
                        if (response.data.status) {
                            resolve(false);
                            this.refresh_Table('categoryTable');
                            this.refresh_Table('promtSQLTable');
                            this.category.categoryno = response.data.data.instance.categoryno;
                            this.category.inc_id = response.data.data.instance.inc_id;
                            this.status = '2';
                            return this.showMessage(this.$t('Save successful')); //保存成功
                        } else {
                            reject(false);
                            return this.showMessage(this.$t("fail"));
                        }
                    })
                    .catch((error) => {
                        console.log(error);
                    });
            });
        },
        //新增時設置默認參數
        get_category_initial() {
            axios.get(`/looper/category/insert`).then(response => {
                if (response.data.status) {
                    this.category = response.data.data;
                } else {
                    this.showMessage(this.$t('Failed to set default parameters!')); //設置默認參數失敗!
                }
            })
                .catch(error => {
                    console.log(error)
                })
        },
        //修改類別信息
        category_update() {
            if (String(this.category.inc_id || "") == "") return this.showMessage(this.$t('Please select data to modify!')); //請選擇要修改的數據!
            this.status = '2'
            this.$refs.edit_categoryForm.$refs.modal.show();
        },
        //查詢類別信息
        category_search() {
            var self = this;
            var columns = [];
            for (let item of self.categoryColumns) {
                if (["", "inc_id"].indexOf(item.field) != -1) continue;
                columns.push(item);
            }
            self
                .GetQueryExp(
                    "AIConditionManager_vueFrm_categoryTable",
                    columns
                )
                .then((query) => {
                    var query_value = {}
                    if (query.master != undefined)
                        query_value["attach_query"] = JSON.stringify(query.master);
                    self.categoryParamsFun = function () {
                        return query_value;
                    };
                    self.$nextTick(function () {
                        self.$refs.categoryTable.datatable.column(0).search("").draw();
                    });
                });
        },
        //保存方法
        save_submit() {
            return new Promise((resolve, reject) => {
                if (String(this.promtsql.sname || "") == "" || String(this.promtsql.promptbyai || "") == "") {
                    this.showMessage(this.$t('Required fields cannot be empty!')); //必填項不能為空!
                    return reject(false)
                }
                // 根據state值動態設置url
                var url = ''
                if (this.state === '1') {
                    url = `/looper/promtsql/insert`; // 新增的URL
                } else if (this.state === '2') {
                    url = `/looper/promtsql/update?pk=${this.promtsql.inc_id}`; // 修改的URL
                }
                axios
                    .post(
                        url,
                        this.objectToFormData(this.promtsql)
                    )
                    .then((response) => {
                        if (response.data.status) {
                            resolve(false);
                            this.refresh_Table('promtSQLTable');
                            this.promtsql.ssid = response.data.data.instance.ssid;
                            this.promtsql.inc_id = response.data.data.instance.inc_id;
                            this.state = '2';
                            return this.showMessage(this.$t('Save successful')); //保存成功
                        } else {
                            reject(false);
                            return this.showMessage(this.$t("fail"));
                        }
                    })
                    .catch((error) => {
                        console.log(error);
                    });
            });
        },
        //獲取詳細信息
        get_promtsql_info(inc_id) {
            axios
                .get(`/looper/promtsql/update`, { params: { pk: inc_id } })
                .then((response) => {
                    if (response.data.status) {
                        let data = response.data.data;
                        // 假設這些字段是布爾值需要進行轉換
                        let booleanFields = ['isai', 'isapproved', 'isdatabasesql']; // 布爾值字段名稱列表
                        booleanFields.forEach((field) => {
                            if (data[field] === true) {
                                data[field] = 'Y';  // True轉為'Y'
                            } else if (data[field] === false) {
                                data[field] = 'N';  // False轉為'N'
                            } // 否則保持原值
                        });
                        // 更新 promtsql 數據
                        this.promtsql = data;
                        this.$nextTick(function () {
                            $('select.select2-category').trigger('change');
                        })
                    }
                });
        },
        //列表單擊事件
        table_row_click(event, data) {
            if (data == undefined) return
            this.get_promtsql_info(data.inc_id);
        },
        //列表雙擊事件
        table_dbclick(data) {
            if (data == undefined) return
            this.state = '2'
            // 加載最新的類別選項數據
            this.setCategoryOptions();
            this.$refs.edit_promtsqlForm.$refs.modal.show();
        },
        //新增時設置默認參數
        get_initial() {
            axios.get(`/looper/promtsql/insert`).then(response => {
                if (response.data.status) {
                    this.promtsql = response.data.data;
                    this.$nextTick(function () {
                        $('select.select2-category').trigger('change');
                    })
                } else {
                    this.showMessage(this.$t('Failed to set default parameters!')); //設置默認參數失敗!
                }
            })
                .catch(error => {
                    console.log(error)
                })
        },
        //新增方法
        // addMaster() {
        //     this.state = '1';
        //     this.promtsql = {};
        //     this.get_initial();
        //     // this.$refs.actionToolbar.$refs.buttonBar.setToolButtonState();
        //     // this.$refs.edit_promtsqlForm.$refs.modal.width("30%");
        //     this.$refs.edit_promtsqlForm.$refs.modal.show();
        // },
        //修改方法
        updateMaster() {
            if (String(this.promtsql.inc_id || "") == "") {
                return this.showMessage(this.$t('Please select data to modify!')) //請選擇要修改的數據!
            }
            this.state = '2'
            this.setCategoryOptions();
            this.$refs.edit_promtsqlForm.$refs.modal.show();
        },
        //刪除方法
        deleteMaster() {
            var detailArray = this.$refs.promtSQLTable.getSelectedFlagData()["datas"];
            // console.log(detailArray.length)
            if (detailArray.length == 0) return this.showMessage(this.$t('Please select data to delete')); //請勾選要刪除的數據
            let flag = confirm(this.$t('Delete selected data?')); //刪除所選數據?
            if (flag) {
                axios.post(`/looper/promtsql/batch_delete`, { details: detailArray })
                    .then(response => {
                        if (response.data.status) {
                            this.promtsql = {}
                            this.refresh_Table('promtSQLTable');
                        }
                        return this.showMessage(response.data.msg);
                    })
                    .catch(error => {
                        console.log(error);
                    });
            }

            // if (String(this.promtsql.inc_id || "") == "") return this.showMessage("請選擇要刪除的數據!")
            // let flag = confirm(this.$t('Are you sure you want to delete it')); //刪除這條數據嗎 
            // if (flag) {
            //     axios
            //         .post(`/looper/promtsql/delete/${this.promtsql.inc_id}`)
            //         .then(response => {
            //             if (response.data.status) {
            //                 this.refresh_Table('promtSQLTable');
            //                 return this.showMessage(this.$t('deleted successfully')); //刪除成功
            //             }
            //             return this.showMessage(this.$t('deleted failed')); //刪除失敗
            //         })
            //         .catch(error => {
            //             console.log(error);
            //         });
            // }
        },
        //頁面默認的查詢方法
        masterSearch() {
            var self = this;
            var columns = [];
            for (let item of self.masterColumns) {
                if (["", "inc_id"].indexOf(item.field) != -1) continue;
                columns.push(item);
            }
            self
                .GetQueryExp(
                    "AIConditionManager_vueFrm_promtSQLTable",
                    columns
                )
                .then((query) => {
                    var query_value = {}
                    if (query.master != undefined)
                        query_value["attach_query"] = JSON.stringify(query.master);
                    self.masterParamsFun = function () {
                        return query_value;
                    };
                    self.$nextTick(function () {
                        self.$refs.promtSQLTable.datatable.column(0).search("").draw();
                    });
                });
        },
        objectToFormData(obj) {
            let fd = new FormData();
            // 需要進行轉換的字段名稱列表
            const fieldsToConvert = ['isai', 'isapproved', 'isdatabasesql']; // 替換為你的具體字段名稱
            for (let filedname in obj) {
                if (obj[filedname] != null) {
                    // 檢查字段是否在 fieldsToConvert 列表中
                    if (fieldsToConvert.includes(filedname)) {
                        // 如果字段的值是 'Y' 或 'N'，做相應轉換
                        if (obj[filedname] === 'Y') {
                            fd.append(filedname, true);  // 'Y' 轉換為 true
                        } else if (obj[filedname] === 'N') {
                            fd.append(filedname, false);  // 'N' 轉換為 false
                        } else {
                            fd.append(filedname, obj[filedname]);  // 保持其他原值
                        }
                    } else {
                        fd.append(filedname, obj[filedname]);  // 不需要轉換的字段，直接保留原值
                    }
                }
            }
            return fd;
        },
        //刷新DataTable列表信息
        refresh_Table(table) {
            let self = this;
            this.$nextTick(function () {
                self.$refs[table].datatable.search("").draw();
            });
        },
        getBrowser(){
            var isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
            var isSafari = /Safari/.test(navigator.userAgent) && /Apple Computer/.test(navigator.vendor);
            if (isChrome) {
                console.log("Chrome!");
            }
            if (isSafari) {
                $(".col-checker .custom-checkbox .custom-control-label").addClass("iosCheckbox");
            }
        },
    },
};
</script>
<style>
/* 輸入框和Label在一行顯示 */
.field {
    display: flex;
    align-items: center;
    margin-bottom: 0;
}

.field>label {
    margin-bottom: 0;
    padding-right: .5rem;
}

.toolbar>.btn {
    margin: 4px 2px;
}

/* dataTable 圖標 */
.LPDataTable table.dataTable thead .sorting:before {
    content: "\f0de" !important;
    right: 0.5em !important;
}

.LPDataTable table.dataTable thead .sorting:after {
    content: "\f0dd" !important;
}

.required {
    color: red;
    font-weight: bold;
}

.AIConditionManagerTab>.card-body {
    padding-top: 0;
}

.AIConditionManagerPage .card.AIConditionManagerTab .tab-content .LPDataTable .thead-btn {
    border: 0;
    box-shadow: none;
    background: transparent;
}

.AIConditionManagerPage .card.AIConditionManagerTab .tab-content .LPDataTable .thead-btn>* {
    display: none;
}
.AIConditionManagerPage .card.AIConditionManagerTab .tab-content .LPDataTable .thead-dd>.custom-control {
    position: relative;
}

.AIConditionManagerPage .tabs-border-card.AIConditionManagerTab {
    border-radius: 16px;
}

.AIConditionManagerPage .tabs-border-card.AIConditionManagerTab>.tabs_header {
    border-radius: 16px 16px 0 0;
}

@media (min-width: 768px) {
    .AIConditionManagerTab .tab-content .LPDataTable .thead-dd .custom-control:not(.custom-switch) .custom-control-label:after,
    .AIConditionManagerTab .tab-content .LPDataTable .thead-dd .custom-control:not(.custom-switch) .custom-control-label:before {
        top: .125rem;
    }
}
</style>