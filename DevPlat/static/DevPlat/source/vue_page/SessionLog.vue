<template>
  <div class="card my-1 mx-2 sessionLogCard">
    <div class="card-header pb-0 px-2">
      <div :class="['leftPane', lang_code_en ? 'lang_en' : '']">
        <div class="form-group d-flex query_contact">
          <label class="col-form-label caption col-auto pl-0">{{ $t('Contact') }}</label>
          <select class="select2 form-control noFirstVal" name="username" v-model="search.username"></select>
        </div>
        <div class="form-group query_date d-flex">
          <label class="col-form-label caption col-auto pl-0">{{ $t('Date') }}</label>
          <div class="input-group input-group-alt m-0">
            <LPFlatpickerDate v-model="search.exetimeb" />
            <div class="input-group-append">
              <span class="input-group-text custom-text">{{ $t('To') }}</span>
            </div>
            <LPFlatpickerDate v-model="search.exetimes" />
          </div>
        </div>
        <div class="form-group query_type d-flex select2Style">
          <label class="col-form-label caption col-auto pl-0">{{ $t('Type') }}</label>
          <select class="select2 form-control noFirstVal" name="actiontype" v-model="search.actiontype"></select>
        </div>
        <div class="form-group d-flex">
          <label class="col-form-label caption col-auto pl-0">{{ $t('Log ID') }}</label>
          <input class="form-control" v-model="search.inc_id" />
        </div>
        <div class="form-group d-flex">
          <label class="col-form-label caption col-auto pl-0">{{ $t('Log Description') }}</label>
          <input class="form-control" v-model="search.action" />
        </div>
        <div class="form-group col-auto query_checkAll">
          <label class="custom-control custom-checkbox mb-0 checkAll">
            <input type="checkbox" class="custom-control-input control" name="ischeck_All">
            <span class="custom-control-label">{{ $t("All Sessions") }}</span>
          </label>
        </div>
        <div class="col-auto query_tools mb-3 d-flex align-items-center">
          <button type="button" class="btn btn-primary specialBtn" @click="chatWithAI">
            <i class="fas fa-robot d-xl-none"></i>
            <span class="d-none d-xl-inline-block">{{ $t('AI') }}</span>
          </button>
          <button type="button" class="btn btn-primary specialBtn" @click="searchLog">
            <i class="oi oi-magnifying-glass d-xl-none"></i>
            <span class="d-none d-xl-inline-block">{{ $t('Search') }}</span>
          </button>
          <button class="btn btn-info specialBtn" type="button" @click="clear">
            <i class="fa fa-broom d-xl-none"></i>
            <span class="d-none d-xl-inline-block">{{ $t('Clear') }}</span>
          </button>
          <OperationBar class="masterQuery flex-shrink-0" ref="bar" module_power="65535" @on-add="addLog"
            @on-delete="deleteLog" @on-edit="updateLog" button_show="111" />
        </div>
      </div>
    </div>
    <div class="card-body p-0 pb-3">
      <LPDataTable :paging="true" :paging_inline="true" :searching="1 != 1" :columns="columns"
        :custom_params_fun="paramsFun" datasource="/devplat/session/log_table" :custom_options="options" ref="table"
        @on_selectornot="rowSelected" @on_dbclick="dblClickRow" />
    </div>
  </div>
  <LPModal ref="logModal" :title="logModalTitle" class="logModal">
    <template v-slot:body>
      <div class="form addFormWrap row">
        <div class="form-group field col-3">
          <label class="col-form-label caption col-auto pl-0">{{ $t('Contact') }}</label>
          <select class="select2 form-control" disabled name="username-modal" v-model="logObject.username">
          </select>
        </div>
        <LPLabelInput :label='$t("Date")' class="field col-4">
          <LPFlatpickerDate class="form-control" v-model="logObject.exetime" :options="dateOptions" />
        </LPLabelInput>

        <LPLabelInput :label='$t("Type")' class="field col select2Style">
          <select class="select2 form-control" v-model="logObject.actiontype" name="actiontype-modal"></select>
        </LPLabelInput>

        <LPLabelInput :label='$t("Log Description")' class="field col-12">
          <textarea class="form-control" :rows=calculateRows() v-model="logObject.action"></textarea>
        </LPLabelInput>
      </div>
    </template>
    <template v-slot:footer>
      <button type="button" class="btn btn-primary" @click="submitLog">{{ $t('Save') }}</button>
      <button type="button" class="btn btn-light" data-dismiss="modal">{{ $t('Cancel') }}</button>
    </template>
  </LPModal>
  <LPAIComBox ref="aicombox" class="mb-0" :iframe_src="'http://183.63.205.83:3000/aiChat'"  :aiPresetQuestion="aiPresetQuestion" :predefinedData="predefinedData"/>
</template>
<script>
import LPDataTable from "@components/looper/tables/LPDataTable.vue";
import OperationBar from "@components/looper/navigator/OperationBar.vue";
import LPFlatpickerDate from "@components/looper/forms/LPFlatpickerDate.vue";
import LPModal from "@components/looper/layout/LPModal.vue";
import LPLabelInput from "@components/looper/forms/LPLabelInput.vue";
import LPAIComBox from "@components/looper/general/LPAIComBox.vue";
import axios from "axios";
export default {
  name: "SessionLog",
  components: {
    OperationBar,
    LPDataTable,
    LPFlatpickerDate,
    LPModal,
    LPLabelInput,
    LPAIComBox,
  },
  data() {
    var _this = this;
    return {
      search: {},
      columns: [
        { field: 'inc_id', label: _this.$t('Log ID'), width: '70px'}, // 主鍵 
        { field: 'action', label: _this.$t('Log Description'), orderable: false }, // log信息
        { field: 'username', label: _this.$t('Contact'), width: '100px' }, //人員
        { field: 'actiontype', label: _this.$t('Type'), width: '150px' }, // log類型
        { field: 'sessionid', label: _this.$t('Session'), width: '120px' }, // session 
        { field: 'exetime', label: _this.$t('Date'), width: '140px', render: function (data) { return _this.$moment(data).format('YYYY-MM-DD HH:mm') } }, // 執行時間
      ],
      options: {
        responsive: false,
        processing: true,
        scrollY: "75vh",
        paging: false,
        autoWidth: false,
        scrollX: true,
        deferLoading: 0,
      },
      dateOptions: {
        dateFormat: "Y-m-d H:i",
        enableTime: true, // 启用时间选择
        time_24hr: true, // 24小时制
      },
      paramsFun: undefined,
      sessionid: '',
      sessionName: '',
      logModalTitle: '',
      logObject: {},
      loginUser: get_username() || '',
      status: 0, // 1為新增, 2為修改
      modalMessage: '',
      contactData:[],
      lang_code_en: true,
      aiPresetQuestion:[],
      predefinedData:[],
    }
  },
  created() {
    // loadCss('/static/BaseApp/vendor/Looper/assets/vendor/select2/css/select2.min.css');
    // loadJs(['/static/BaseApp/vendor/Looper/assets/vendor/select2/js/select2.min.js'], false)
  },
  mounted() {
    var _this = this;
    this.setContactOptions();
    this.getSessionTypeData();
    $(window).on('resize', function () {
      $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
    });
    if (window.parent) {
      window.parent.childWindowMenuClick = function (e) {
        if (e.target.tagName !== 'LI') {
          _this.sessionid = $(e.target).parents('li.has-active').attr('sessionid');
          _this.sessionName = $(e.target).parents('li.has-active').attr('title');
        }
        else {
          _this.sessionid = $(e.target).attr('sessionid');
          _this.sessionName = $(e.target).attr('title');
        }
        _this.logObject = {};
        _this.$refs.logModal.hide();
      }
    }
    $(this.$refs.logModal.$refs.modal).on('hidden.bs.modal', function (e) {
      _this.$refs.bar.isEdit = false;
    })

    this.$refs.logModal.show = function() {
      $(this.$refs.modal).modal({
          backdrop: 'static',  // 防止点击背景关闭
          keyboard: false       // 禁用 Esc 关闭
      });
    };
    this.$nextTick(function () {
      this.$refs.table.datatable.on('xhr.dt', function (e, settings, json, xhr) {
        //檢測父窗口中是否選擇了Log標籤.
        var selectedLabelFlag = window.parent.document.getElementById('Session_Log').classList.contains('active');
        if (selectedLabelFlag == false) return;
        if (json.empty_condition){
          // window.SWApp.popoverMsg($('.query_tools button[type="button"].btn-primary'), json.empty_condition)
          alert(json.empty_condition)
        }
      })

      _this.get_lang_code();
      _this.setBodyClass();  // 初始化時設置類名
      window.addEventListener('resize', this.setBodyClass);  // 監聽視窗大小變化

      // 监听 select2:open 事件
      $(".noFirstVal").on('select2:open', () => {
        setTimeout(() => {
          $(".select2-container.select2-container--open ul.select2-results__options>li.select2-results__option").each(function () {
            if ($(this).attr("id") === undefined) {
              $(this).addClass("d-none"); //當select2下拉選屬性中的id為空時,設置隱藏
            }
          });
        }, 0);
      });
      
    })

    // window.addEventListener('message', (event) => {
    //   if (event.data.type === 'resize') {
    //     _this.applyCustomStyles(event.data.width);
    //   }
    // });

    // 為每個媒體查詢添加事件監聽並調用方法
    this.mediaQueries.forEach(media => {
        const mediaQuery = window.matchMedia(media.query);
        mediaQuery.addEventListener('change', () => this.applyCustomStyles(mediaQuery));
        // 初始調用
        this.applyCustomStyles(mediaQuery);
    });
  },
  watch: {
    sessionid: function (val) {
      if (String(this.sessionid || '') !== '') {
        this.clear();
        this.searchLog();
      }
    }
  },
  methods: {
    dblClickRow(data) {
      var _this = this;
      this.logObject = JSON.parse(JSON.stringify(data));
      this.$refs.table.datatable.rows().every(function () {
        if (_this.logObject.inc_id == this.data().inc_id)
          this.select();
      })
      this.updateLog();
    },
    async updateLog() {
      if (!('inc_id' in this.logObject)) {
        this.$refs.bar.isEdit = false;
        return alert(this.$t('no select'));
      }
      var response = await axios.get('/devplat/session/get_session_name?sessionid='+this.logObject.sessionid);
      var sessionName = ''
      if (response.data.status){
        sessionName = response.data.name.sdesp;
      }
      this.status = 2;
      this.logModalTitle = this.$t('SessionLog infomation update') + ` (${this.logObject.sessionid}) ${sessionName}`;
      this.logObject.exetime = this.$moment(this.logObject.exetime).format('YYYY-MM-DD HH:mm');
      // this.$refs.logModal.width('60%');
      this.$refs.logModal.show();
      this.$nextTick(function () {
        $('select.select2').trigger('change');
      })
    },
    deleteLog() {
      if (!('inc_id' in this.logObject)) return alert(this.$t('no select'));
      if (!['sing', 'lmy'].includes(this.loginUser)) {
        if (this.logObject.username !== this.loginUser)
          return alert(this.$t('No permission to delete')) //沒有權限刪除
      }
      if (!confirm(this.$t('delete this') + '?')) return;
      axios.post('/devplat/session/log_delete/' + this.logObject.inc_id).then(res => {
        if (res.data.status) {
          // this.clear();
          // this.searchLog();
          this.$nextTick(function () {
            this.$refs.table.datatable.search('').draw();
          })
        } else {
          var msg = res.data.msg.error;
          alert(this.$t('fail') + ': ' + msg);
        }
      })
    },
    rowSelected(e, d, t, i) {
      if (e.type === 'select')
        this.logObject = JSON.parse(JSON.stringify(d.row(i).data()));
      else
        this.logObject = {};
    },
    submitLog() {
      if (String(this.logObject.username || '') === '') return alert('Contact is empty');
      if (String(this.logObject.exetime || '') === '') return alert('Date is empty');
      if (String(this.logObject.actiontype || '') === '') return alert('Type is empty');
      if (String(this.logObject.action || '') === '') return alert('Log info is empty');
      if (this.loginUser !== 'xmm')
        if (this.logObject.username !== this.loginUser) return alert('Cannot modify other user');
      if (this.status === 1) {
        this.logObject.pid = this.sessionid.split('-')[0];
        this.logObject.tid = this.sessionid.split('-')[1];
        this.logObject.createlogtime = new Date().format('yyyy-MM-dd hh:mm:ss');
        var url = "/devplat/session/log_add"; //新增
      }
      else if (this.status === 2) {
        this.logObject.pid = this.logObject.sessionid.split('-')[0];
        this.logObject.tid = this.logObject.sessionid.split('-')[1];
        url = "/devplat/session/log_update?pk=" + this.logObject.inc_id;
      }
      axios.post(url, this.objectToFormData(this.logObject)).then(res => {
        if (res.data.status) {
          this.$refs.logModal.hide();
          this.$nextTick(function () {
            this.$refs.table.datatable.search('').draw();
            this.getSessionTypeData();
          })
          // this.clear();
          // this.searchLog();
        } else {
          var msg = ''
          if (this.status === 1)
            msg = res.data.msg.fail || res.data.msg;
          else
            msg = res.data.msg.error || res.data.msg;
          alert(this.$t('fail') + ': ' + msg);
        }
      })
    },
    searchLog() {
      if (String(this.sessionid || '') === '') return alert(this.$t('no selected session'));
      var allSession = $("input[name='ischeck_All']").prop('checked') ? 'true' : 'false';
      this.search.all_session = allSession;
      this.paramsFun = () => {
        return { sessionid: this.sessionid, ...this.search };
      }
      this.$nextTick(function () {
        this.$refs.table.datatable.search('').draw();
        this.logObject = {};
      })
    },
    clear() {
      this.search = {};
      $("input[name='ischeck_All']").prop('checked', false);
      this.$nextTick(function () {
        $('select.select2').trigger('change');
      })
    },
    addLog() {
      if (String(this.sessionid || '') === '') {
        this.$refs.bar.isEdit = false;
        return alert(this.$t('no selected session'));
      }
      this.logModalTitle = this.$t('SessionLog infomation add') + ` (${this.sessionid}) ${this.sessionName}`;
      this.status = 1;
      this.logObject = {}; // 清空上次錄入的內容
      this.logObject.username = this.loginUser;
      this.logObject.exetime = this.$moment(new Date).format('YYYY-MM-DD HH:mm');
      this.$nextTick(function () {
        $('select.select2').trigger('change');
      })
      // this.$refs.logModal.width('60%');
      this.$refs.logModal.show();
    },
    // async setContactOptions() {
    //   var _this = this;
    //   await window.parent.CommonData.PartUserNames.then(res => {
    //     _this.contactData = ['', ...res.data]
    //   });
    //   $('select.select2[name="username"]').select2({ data: _this.contactData }).on("select2:select", function (e) {
    //     _this.search.username = e.params.data.text;
    //   });
    //   $('select.select2[name="username-modal"]').select2({ data: _this.contactData });
    //   $('select.select2[name="username-modal"]').val(this.loginUser).trigger('change');
    // },
    setContactOptions() {
      var _this = this;
      axios.get(`/PMIS/user/get_part_user_names`)
        .then((response) => {
          _this.contactData = response.data.data?.length > 0 
            ? ['', ...response.data.data]  // 添加空選項
            : [''];  // 默認空選項
          _this.initSelect2();
        })
        .catch((error) => {
          console.log("Failed to load user names:", error);
          _this.contactData = [''];
          _this.initSelect2();
        });
    },
    initSelect2() {
      // 封裝 Select2 初始化
      const $usernameSelect = $('select.select2[name="username"]');
      const $modalSelect = $('select.select2[name="username-modal"]');
      // $usernameSelect.select2('destroy');
      // $modalSelect.select2('destroy');
      $usernameSelect
        .select2({ data: this.contactData })
        .on("select2:select", (e) => {
          this.search.username = e.params.data.text;
        });
      $modalSelect
        .select2({ data: this.contactData })
        .val(this.loginUser)
        .trigger('change');
    },
    getSessionTypeData() {
      var _this = this;
      axios.get('/devplat/session/get_type').then(res => {
        if (res.data.status) {
          var data = res.data.data;
          data = ['', ...data];
          $('select.select2[name="actiontype-modal"]').select2({ tags: true, data: data }).on("select2:select", function (e) {
            _this.logObject.actiontype = e.params.data.text;
          });
          $('select.select2[name="actiontype"]').select2({ data: data }).on("select2:select", function (e) {
            _this.search.actiontype = e.params.data.text;
          });
        }
      })
    },
    get_lang_code() {
      if ($("#curr_language_code").val() !== "en") {
        this.lang_code_en = false;
      }
    },
    // applyCustomStyles(width) {
    //   const body = document.body;
    //   document.body.classList.forEach(className => { // 清除所有樣式類
    //     if (className.endsWith('_screen')) {
    //       document.body.classList.remove(className);
    //     }
    //   });

    //   if (width >= 1800) {
    //     body.classList.add('xxxxl_screen');
    //   } else if (width >= 1200 && width <= 1799.98) {
    //     body.classList.add('xlx_screen');
    //   } else if (width >= 992) {
    //     body.classList.add('lg_screen');
    //   } else if (width >= 768) {
    //     body.classList.add('md_screen');
    //   } else if (width >= 576) {
    //     body.classList.add('sm_screen');
    //   } else if (width <= 575) {
    //     body.classList.add('xs_screen');
    //   }
    // },
    calculateRows() {
      return SWApp.os.isMobile ? 8 : 18;
    },
    //彈出AI會話框
    chatWithAI(){
      // this.$refs.aicombox.$refs.modal.width('800px')
      this.$refs.aicombox.$refs.modal.show()
      var Tempdata = this.$refs.table.datatable.data().toArray()
      this.predefinedData = Tempdata
      console.log(Tempdata)
    },
    setBodyClass() {
      try {
        const parentBodyWidth = window.parent.document.body.clientWidth;

        // 媒體查詢條件和對應類名
        const mediaQueries = [
          { minWidth: 3400, className: 'largest_screen' },
          { minWidth: 2200, className: 'larger_screen' },
          { minWidth: 1800, className: 'xxxxl_screen' },
          { minWidth: 1600, maxWidth: 1799.98, className: 'xxlx_screen' },
          { minWidth: 1200, maxWidth: 1799.98, className: 'xlx_screen' },
          { minWidth: 992, maxWidth: 1199.98, className: 'lg_screen' },
          { minWidth: 768, maxWidth: 991.98, className: 'md_screen' },
          { minWidth: 576, maxWidth: 767.98, className: 'sm_screen' },
          { maxWidth: 575, className: 'xs_screen' }
        ];

        // 遍歷媒體查詢條件，並為子頁面添加對應的類名
        const selectedClass = mediaQueries.find(item => {
          return (item.minWidth ? parentBodyWidth >= item.minWidth : true) &&
            (item.maxWidth ? parentBodyWidth <= item.maxWidth : true);
        })?.className || '';

        let currentClassName = document.body.className;
        currentClassName = currentClassName.split(' ').filter(className => !className.endsWith('_screen')).join(' ');

        if (selectedClass && !currentClassName.includes(selectedClass)) {
          document.body.className = `${currentClassName} ${selectedClass}`.trim();
        } else {
          document.body.className = currentClassName.trim();
        }

      } catch (error) {
        console.error('無法獲取父頁面寬度，請檢查跨域問題。', error);
      }
    }
  },
};
</script>
<style>
.leftPane {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
}

.leftPane>.form-group,
.leftPane>.query_tools {
  padding-left: 5px;
  padding-right: 5px;
}

.masterQuery.border-bottom {
  border-bottom: 0 !important;
}

.masterQuery.border-bottom .order-button {
  display: flex;
  align-items: center;
  margin-bottom: 0;
  margin-top: 0;
  margin-right: .5rem;
}

.masterQuery.border-bottom>.card.toolbox {
  background-color: transparent;
  margin-bottom: 0;
  box-shadow: none;
  padding: 0 !important;
  border: 0
}

.form-group.query_date .input-group-append {
  margin-right: -1px;
}

/* 輸入框和Label在一行顯示 */
.field {
  display: flex;
  align-items: center;
}

.field>label {
  margin-bottom: 0;
  padding-right: .5rem;
  white-space: nowrap;
}

.addFormWrap .field:first-child>label,
.addFormWrap .field:last-child>label {
  min-width: 55px;
}

/* dataTable 圖標 */
.LPDataTable table.dataTable thead .sorting:before {
  content: "\f0de" !important;
  right: 0.5em !important;
}

.LPDataTable table.dataTable thead .sorting:after {
  content: "\f0dd" !important;
}

.flatpickr-day {
  padding: 0;
}

.select2Style select.select2-type+.select2-container {
  width: 100% !important;
  min-height: 2.25rem;
}

select.selectpicker-log+.select2-container {
  width: 100% !important;
  min-height: 2.25rem;
}

.select2Style .select2-container--default .select2-selection--single {
  border-color: #c6c9d5;
}

.select2-container {
  width: 100% !important;
  min-width: 0;
}

.logModal .modal-footer {
  box-shadow: none;
  padding-top: .5rem;
  padding-bottom: .5rem;
}

.logModal .modal-footer>.btn {
  margin-top: 0;
  margin-bottom: 0;
}

.addFormWrap {
  margin-top: .5rem;
}

.sessionLogCard>.card-body .LPDataTable .table thead th {
  white-space: nowrap;
}

@media (max-width: 575.98px) {
  .leftPane .query_tools>.btn,
  .leftPane .query_tools .order-button {
    margin-right: .25rem;
  }
}

@media (min-width: 576px) {
  .leftPane .query_tools>.btn {
    margin-left: 2px;
    margin-right: .5rem;
  }

  /* .leftPane:not(.lang_en) .form-group:nth-child(3) label:not(.checkAll) {
    min-width: 58px
  } */

  .logModal .modal-dialog {
    max-width: 750px;
  }
}

@media (min-width: 768px) {
  .select2Style .select2-container .select2-selection--single {
    height: 2.25rem;
  }

  .addFormWrap {
    margin-top: 1rem;
  }

  .addFormWrap>.form-group {
    margin-bottom: 1.5rem;
  }
}

.leftPane .custom-checkbox .custom-control-label::before,
.leftPane .custom-checkbox .custom-control-label::after {
  top: 0.25rem;
}

@media (max-width: 1599.98px) {
  .query_tools .specialBtn>span {
    display: none;
  }
}

/* iframe頁面媒體查詢樣式 */
body.xs_screen .leftPane>.form-group {
  flex: 0 0 100%;
  max-width: 100%
}

body.xs_screen .leftPane .query_contact,
body.xs_screen .leftPane .query_type {
  order: -1;
  flex: 0 0 50%;
  max-width: 50%;
}

body.xs_screen .leftPane>.form-group.query_checkAll {
  flex: 0 0 auto;
  width: auto;
  max-width: 100%
}

body.xs_screen .leftPane:not(.lang_en) .form-group:not(:nth-child(3)) label:not(.checkAll) {
  min-width: 74px
}

body.xs_screen .leftPane.lang_en .form-group:not(:nth-child(3)) label:not(.checkAll) {
  min-width: 126px
}

body.xs_screen .logModal .addFormWrap .form-group:not(:nth-last-child(2)){
  flex: 0 0 50%;
  max-width: 50%;
}
body.xs_screen .logModal .addFormWrap .form-group:nth-last-child(2),
body.xs_screen .logModal .addFormWrap .form-group:nth-last-child(1) {
  flex: 0 0 100%;
  max-width: 100%;
}
body.md_screen .page.lang_en .logModal .addFormWrap .form-group:not(:nth-child(2)) label {
  /* min-width: 67px */
  min-width: 111px
}
body.xs_screen .page.lang_en .logModal .addFormWrap .form-group:not(:nth-child(2)) label {
  min-width: 99px
}
body.xs_screen .page:not(.lang_en) .logModal .addFormWrap .form-group:not(:nth-child(2)) label {
  min-width: 72px
}
body.md_screen .page:not(.lang_en) .logModal .addFormWrap .form-group:not(:nth-child(2)) label {
  min-width: 72px
}

body.xs_screen .page .logModal .addFormWrap .form-group:last-child label,
body.sm_screen .page .logModal .addFormWrap .form-group:last-child label {
  white-space: pre-wrap;
}

@media (max-width: 379.98px) {
 .leftPane:not(.lang_en) .query_checkAll {
    flex: 0 0 100%;
    max-width: 100%;
 }

  body.xs_screen .leftPane:not(.lang_en) .query_contact,
  body.xs_screen .leftPane:not(.lang_en) .query_type {
    flex: 0 0 100%;
    max-width: 100%
  }
  body.xs_screen .leftPane:not(.lang_en) .query_type {
    order: 0;
  }

  .leftPane:not(.lang_en) .form-group label:not(.checkAll) {
    min-width: 58px
  }

  .leftPane.lang_en .form-group label:not(.checkAll) {
    min-width: 70px
  }

  body.xs_screen .leftPane:not(.lang_en) .form-group:nth-child(3) label:not(.checkAll) {
    min-width: 74px
  }

  .leftPane .form-group.query_date .input-group>.flatpickr-input:first-child {
    border-top-left-radius: .25rem;
    border-bottom-left-radius: .25rem;
  }

  body.xs_screen .logModal .addFormWrap .form-group:not(:last-child){
    flex: 0 0 100%;
    max-width: 100%;
  }

  .page.lang_en .logModal .addFormWrap .form-group label {
    min-width: 99px
  }
  
  .page:not(.lang_en) .logModal .addFormWrap .form-group label {
    min-width: 72px
  }
}

@media (max-width: 396.98px) {
  .leftPane.lang_en .query_tools>.btn,
  .leftPane.lang_en .query_tools .order-button {
    height: calc(1.5em + .5rem + 2px);
    padding: .25rem .5rem;
    font-size: .875rem;
    line-height: 1.5;
  }
}

@media (max-width: 479.98px) {
 .leftPane.lang_en .query_checkAll {
    flex: 0 0 100%;
    max-width: 100%;
 }

  body.xs_screen .leftPane.lang_en .query_contact,
  body.xs_screen .leftPane.lang_en .query_type {
    flex: 0 0 100%;
    max-width: 100%
  }

  body.xs_screen .leftPane.lang_en .query_type {
    order: 0;
  }

  body.xs_screen .leftPane.lang_en .form-group label:not(.checkAll) {
    min-width: 140px !important
  }
}

.masterQuery div.el-example {
  margin-top: 0;
}

body.sm_screen .leftPane.lang_en>.form-group:not(.query_checkAll) {
  flex: 0 0 100%;
  max-width: 100%;
}

body.sm_screen .leftPane:not(.lang_en) .form-group:nth-child(2),
body.sm_screen .leftPane:not(.lang_en) .form-group:nth-child(4) {
  flex: 0 0 50%;
  max-width: 50%;
}

body.sm_screen .leftPane .form-group:nth-child(5),
body.md_screen .leftPane .form-group:nth-child(5) {
  flex: 0 0 100%;
  max-width: 100%;
}

body.sm_screen .leftPane .query_contact,
body.sm_screen .leftPane .query_type {
  order: -1;
  flex: 0 0 50%;
  max-width: 50%;
}

/* .leftPane:not(.lang_en) .form-group:not(:nth-child(3)) label:not(.checkAll) {
  min-width: 58px
} */

body.sm_screen .leftPane:not(.lang_en) .form-group label:not(.checkAll) {
  min-width: 74px;
}

body.sm_screen .leftPane.lang_en .form-group:not(.query_checkAll) label {
  min-width: 126px;
}

body.sm_screen .page .logModal .addFormWrap .form-group:first-child label,
body.sm_screen .page .logModal .addFormWrap .form-group:last-child label {
  min-width: 64px;
}

body.md_screen .leftPane .query_contact,
body.md_screen .leftPane .query_type {
  flex: 0 0 41.666667%;
  max-width: 41.666667%
}
body.md_screen .leftPane .form-group:nth-child(2),
body.md_screen .leftPane .form-group:nth-child(4) {
  flex: 0 0 58.333333%;
  max-width: 58.333333%
}
body.md_screen .leftPane:not(.lang_en) .form-group label {
  min-width: 74px !important
}

body.md_screen .leftPane.lang_en .form-group:nth-child(1) label,
body.md_screen .leftPane.lang_en .form-group:nth-child(3) label {
  min-width: 76px;
}
body.md_screen .leftPane.lang_en .form-group:nth-child(2) label,
body.md_screen .leftPane.lang_en .form-group:nth-child(4) label {
  min-width: 60px;
}
body.md_screen .logModal .addFormWrap .form-group:nth-child(1),
body.md_screen .logModal .addFormWrap .form-group:nth-child(2) {
  flex: 0 0 50%;
  max-width: 50%;
}

body.lg_screen .leftPane .query_contact,
body.lg_screen .leftPane .query_type {
  flex: 0 0 25%;
  max-width: 25%;
}
/* body.lg_screen .leftPane.lang_en .form-group:nth-child(4) {
  flex-basis:0;
  flex-grow: 1;
  min-width: 0;
  max-width: 100%
} */
body.lg_screen .leftPane .form-group:nth-child(4) {
  flex: 0 0 25%;
  max-width:25%
}
body.lg_screen .leftPane .form-group:nth-child(5) {
  flex: 0 0 75%;
  max-width:75%
}
body.lg_screen .leftPane .form-group:nth-child(2) {
  flex: 0 0 50%;
  max-width: 50%;
}
body.lg_screen .leftPane .query_tools>.btn,
body.lg_screen .leftPane .query_tools .order-button {
  margin-right: .25rem;
}
.leftPane .query_tools .order-button:last-child {
  margin-right: 0;
}
body.lg_screen .leftPane:not(.lang_en) .form-group:not(:nth-child(3)) label {
  min-width: 74px
}
body.lg_screen .leftPane:not(.lang_en) .form-group:nth-child(3) label {
  min-width: auto
}
body.lg_screen .leftPane.lang_en .form-group:nth-child(1) label,
body.lg_screen .leftPane.lang_en .form-group:nth-child(4) label {
  /* min-width: 70px; */
  min-width: 76px;
}
body.lg_screen .leftPane .query_tools {
  margin-left: auto;
}

body.xlx_screen .leftPane .query_contact,
body.xlx_screen .leftPane .query_type {
  flex: 0 0 16.666667%;
  max-width: 16.666667%;
}
body.xlx_screen .leftPane .form-group:nth-child(3),
body.xlx_screen .leftPane .form-group:nth-child(4) {
  flex: 0 0 25%;
  max-width: 25%;
}
body.xlx_screen .leftPane .form-group.query_date {
  flex: 0 0 33.333333%;
  max-width: 33.333333%;
}
body.xlx_screen .leftPane .form-group:nth-child(5) {
  flex-basis: 0;
  flex-grow: 1;
  max-width: 100%
}
body.xlx_screen .leftPane:not(.lang_en) .form-group:nth-child(1) label,
body.xlx_screen .leftPane:not(.lang_en) .form-group:nth-child(5) label {
  min-width: 66px
}
body.xlx_screen .leftPane:not(.lang_en) .form-group:nth-child(2) label,
body.xlx_screen .leftPane:not(.lang_en) .form-group:nth-child(3) label,
body.xlx_screen .leftPane:not(.lang_en) .form-group:nth-child(4) label {
  min-width: auto
}
body.xlx_screen .leftPane.lang_en .form-group:nth-child(5) label {
  min-width: 111px;
}
body.xlx_screen .leftPane.lang_en .form-group:nth-child(2) label,
body.xlx_screen .leftPane.lang_en .form-group:nth-child(3) label,
body.xlx_screen .leftPane.lang_en .form-group:nth-child(4) label {
  min-width: auto;
}

/* body.xxlx_screen */
body.xxlx_screen .leftPane .query_contact,
body.xxlx_screen .leftPane .form-group:nth-child(5) {
  order: -2;
}

body.xxlx_screen .leftPane .form-group:nth-child(4) {
  order: -1;
}

body.xxlx_screen .leftPane .form-group:nth-child(1),
body.xxlx_screen .leftPane .form-group:nth-child(3),
body.xxlx_screen .leftPane .form-group:nth-child(4) {
  flex: 0 0 16.666667%;
  max-width: 16.666667%;
}

body.xxlx_screen .leftPane .form-group:nth-child(2) {
  flex-basis: 0;
  flex-grow: 1;
  max-width: 100%
}

body.xxlx_screen .leftPane .form-group:nth-child(5) {
  flex: 0 0 83.333333%;
  max-width: 83.333333%
}
body.xxlx_screen .leftPane:not(.lang_en) .form-group:not(.checkAll):not(:nth-child(3)) label {
  min-width: 66px
}
body.xxlx_screen .leftPane .form-group:nth-child(3) label,
body.xxlx_screen .leftPane.lang_en .form-group:nth-child(2) label {
  min-width: auto
}
body.xxlx_screen .leftPane.lang_en .form-group:nth-child(5) label {
  min-width: 111px
}
body.xxlx_screen .leftPane.lang_en .form-group:nth-child(1) label,
body.xxlx_screen .leftPane.lang_en .form-group:nth-child(4) label {
  min-width: 68px
}

body.xxxxl_screen:not(.lang_en) .leftPane .query_contact,
body.xxxxl_screen:not(.lang_en) .leftPane .form-group:nth-child(3),
body.xxxxl_screen:not(.lang_en) .leftPane .form-group:nth-child(4)  {
  flex: 0 0 10%;
  max-width: 10%;
}
body.xxxxl_screen:not(.lang_en) .leftPane .query_date {
  flex: 0 0 20%;
  max-width: 20%;
}
body.xxxxl_screen .leftPane .form-group:nth-child(5) {
  flex-basis:0;
  flex-grow: 1;
  min-width: 0;
  max-width: 100%
}
body.xxxxl_screen .leftPane:not(.lang_en) .form-group label:not(.checkAll) {
  min-width: auto
}

body.larger_screen .leftPane .query_contact,
body.larger_screen .leftPane .form-group:nth-child(3),
body.larger_screen .leftPane .form-group:nth-child(4) {
  flex: 0 0 10%;
  max-width: 10%;
}
body.larger_screen .leftPane .query_date {
  flex: 0 0 16.666667%;
  max-width: 16.666667%;
}
body.larger_screen .leftPane .form-group:nth-child(5) {
  flex-basis:0;
  flex-grow: 1;
  min-width: 0;
  max-width: 100%
}
body.larger_screen .leftPane:not(.lang_en) .form-group label:not(.checkAll) {
  min-width: auto
}

body.largest_screen .leftPane .query_contact,
body.largest_screen .leftPane .form-group:nth-child(3),
body.largest_screen .leftPane .form-group:nth-child(4) {
  flex: 0 0 8%;
  max-width: 8%;
}
body.largest_screen .leftPane .query_date {
  flex: 0 0 10%;
  max-width: 10%;
}
body.largest_screen .leftPane .form-group:nth-child(5) {
  flex-basis:0;
  flex-grow: 1;
  min-width: 0;
  max-width: 100%
}
body.largest_screen .leftPane:not(.lang_en) .form-group label:not(.checkAll) {
  min-width: auto
}

/* @media (min-width: 1040px) and (max-width: 1199.98px) {
  body.lg_screen .leftPane.lang_en .form-group:nth-child(4) label {
    min-width: 62px;
  }
} */

.select2-container--open .select2-results__option {
  word-wrap: break-word;
}

.input-group>.flatpickr-mobile.form-control {
  border-top-left-radius: .25rem;
  border-bottom-left-radius: .25rem;
}

@media (min-width: 1528px) and (max-width: 1727.98px), (min-width: 1704px) and (max-width: 1927.98px) {
  body.xxxxl_screen .leftPane.lang_en .query_contact,
  body.xxxxl_screen .leftPane.lang_en .form-group:nth-child(5) {
    order: -2 ;
  }

  body.xxxxl_screen .leftPane.lang_en .form-group:nth-child(4) {
    order: -1;
  }

  body.xxxxl_screen .leftPane.lang_en .form-group:nth-child(1),
  body.xxxxl_screen .leftPane.lang_en .form-group:nth-child(3),
  body.xxxxl_screen .leftPane.lang_en .form-group:nth-child(4) {
    flex: 0 0 16.666667% !important;
    max-width: 16.666667% !important;
  }

  body.xxxxl_screen .leftPane.lang_en .form-group:nth-child(2) {
    flex-basis: 0;
    flex-grow: 1;
    max-width: 100%
  }

  body.xxxxl_screen .leftPane.lang_en .form-group:nth-child(5) {
    flex: 0 0 83.333333%;
    max-width: 83.333333%
  }

  body.xxxxl_screen .leftPane.lang_en .form-group:nth-child(2) label,
  body.xxxxl_screen .leftPane.lang_en .form-group:nth-child(5) label {
    min-width: 111px !important
  }

  body.xxxxl_screen .leftPane.lang_en .form-group:nth-child(1) label,
  body.xxxxl_screen .leftPane.lang_en .form-group:nth-child(4) label {
    min-width: 62px !important
  }
}

@media (min-width: 1428px) and (max-width: 1527.98px) {
  body.xxlx_screen .leftPane.lang_en .form-group:nth-child(2) label,
  body.xxlx_screen .leftPane.lang_en .form-group:nth-child(5) label {
    min-width: 111px;
  }
}
@media (min-width: 1178px) and (max-width: 1327.98px) {
  body.xlx_screen .leftPane.lang_en .form-group:nth-child(1) label,
  body.xlx_screen .leftPane.lang_en .form-group:nth-child(5) label {
    min-width: 111px;
  }
}

@media (min-width: 768px) {
  .page:not(.lang_en) .addFormWrap>.form-group:nth-child(1)>label,
  .page:not(.lang_en) .addFormWrap>.form-group:nth-child(4)>label {
    min-width: 64px;
 }
 .page.lang_en .addFormWrap>.form-group:nth-child(1) {
    flex: 0 0 33.333333%;
    max-width: 33.333333%;
  }
  .page.lang_en .addFormWrap>.form-group:nth-child(1)>label,
  .page.lang_en .addFormWrap>.form-group:nth-child(4)>label {
    min-width: 111px !important;
 }
}

@media (min-width: 720px) and (max-width: 767.98px) {

  .page:not(.lang_en) .addFormWrap>.form-group:nth-child(1)>label,
  .page:not(.lang_en) .addFormWrap>.form-group:nth-child(3)>label,
  .page:not(.lang_en) .addFormWrap>.form-group:nth-child(4)>label {
    min-width: 72px !important;
 }
 .page.lang_en .addFormWrap>.form-group:nth-child(1) {
    flex: 0 0 33.333333%;
    max-width: 33.333333%;
  }
  .page.lang_en .addFormWrap>.form-group:nth-child(1)>label,
  .page.lang_en .addFormWrap>.form-group:nth-child(4)>label {
    min-width: 105px !important;
 }
}

/* @media (min-width: 496px) and (max-width: 719.98px) {
  .page:not(.lang_en) .addFormWrap>.form-group:nth-child(1)>label,
  .page:not(.lang_en) .addFormWrap>.form-group:nth-child(4)>label {
    min-width: 72px !important;
 }
} */

@media (min-width: 496px) {
  .page.lang_en .addFormWrap>.form-group:nth-child(4)>label {
    white-space: pre-wrap;
 }
}

@media (min-width: 600px) and (max-width: 767.98px) {

  body.sm_screen .leftPane.lang_en .form-group:nth-child(n+1):nth-child(-n+4) {
    flex: 0 0 50%;
    max-width: 50%;
  }

  body.sm_screen .leftPane.lang_en .form-group.query_checkAll {
    flex-basis: 0;
    flex-grow: 1;
    max-width: 100%
  }

  body.sm_screen .leftPane.lang_en .form-group:nth-child(1) label,
  body.sm_screen .leftPane.lang_en .form-group:nth-child(2) label,
  body.sm_screen .leftPane.lang_en .form-group:nth-child(5) label {
    min-width: 126px !important;
  }

  body.sm_screen .leftPane.lang_en .form-group:nth-child(3) label,
  body.sm_screen .leftPane.lang_en .form-group:nth-child(4) label {
    min-width: 60px;
  }
}

@media (min-width: 577px) and (max-width: 735.98px) {
  .leftPane:not(.lang_en) .form-group label:not(.checkAll) {
    min-width: 74px;
  }
}
@media (min-width: 576px) and (max-width: 735.98px), (min-width: 992px) {
  .page.lang_en .addFormWrap>.form-group:nth-child(1)>label,
  .page.lang_en .addFormWrap>.form-group:nth-child(4)>label {
    min-width: 67px;
 }
}
/* @media (min-width: 576px) and (max-width: 596.98px) { */
@media (min-width: 544px) and (max-width: 596.98px) {
  body.sm_screen .addFormWrap>.form-group:first-child {
    flex: 0 0 30%;
    max-width: 30%;
 }
 body.sm_screen .addFormWrap>.form-group:nth-child(3) {
    flex: 0 0 36.666667%;
    max-width: 36.666667%;
 }
}
</style>