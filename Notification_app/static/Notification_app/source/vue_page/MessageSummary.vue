<template>
  <div class="container container-custl py-3 pt-xl-5 summaryStyle2">
    <div class="card MesgSumCard">
      <div class="card-header">
        <div class="header_leftPane">
          <h6 class="MesgDate">{{ currentDate }}</h6>
          <h4 class="MesgSumCardTitle mb-0">{{ $t("Message Summary of Today") }}</h4>
        </div>
        <div class="header_rightPane">
          <span class="badge badge-pill badge-lg badge-subtle badge-secondry">{{ totalQty }}</span>
        </div>
      </div>
      <div class="card-body py-3 scrollbar">
        <div v-for="(item, index) in summary" :key="item.category_id" class="card sumCard"
          @click="getMessageList(item.category_id, item.category_name)" :style="getTransformStyle(index)">
          <div class="card-body">
            <h3 class="card-title mb-3">{{ item.category_name }}</h3>
            <p class="metric-value h3">
              <sup><i :class="item.icon"></i></sup> <span class="value">{{ item.num }}</span>
            </p>
            <!-- <p class="metric-value text-truncate metricDetailInfo">{{ item.detailInfo }}</p> -->
          </div>
        </div>
      </div>
    </div>
  </div>
  <LPModal ref="mesgModal" :title="detailMesgModalTitle" class="mesgModal" show_part="'hb'">
    <template v-slot:body>
      <div class="form-row mx-0 queryWrapper">
        <div class="form-group d-flex query_contact col-6 col-md-3">
          <label class="col-form-label caption col-auto pl-0">{{ $t("Contact") }}</label>
          <select class="status_select control col px-0" data-toggle="selectpicker" data-width="100%" data-size="5"
            data-none-selected-text v-model="detailFilter.contact" data-container="body">
            <option></option>
            <option v-for="(option, inx) in contactData" :key="inx" :value="option">{{ option }}</option>
          </select>
        </div>
        <div class="form-group d-flex query_date col-6 col-md-3">
          <label class="col-form-label caption col-auto pl-0">{{ $t("Date") }}</label>
          <LPFlatpickerDate v-model="detailFilter.date" />
        </div>
        <div class="form-group d-flex query_recordID col col-md-3">
          <label class="col-form-label caption col-auto pl-0">{{ $t("RecordID") }}</label>
          <input class="form-control" v-model="detailFilter.RID" />
        </div>
        <div class="col-auto query_tools">
          <button class="btn btn-primary mr-1" @click="masterClear">
            <i class="fa fa-broom d-xxxl-none"></i>
            <span class="d-none d-xxxl-inline-block">{{ $t("Clear") }}</span>
          </button>
          <button type="button" class="btn btn-primary" @click="searchMessage">
            <i class="oi oi-magnifying-glass d-xxxl-none"></i>
            <span class="d-none d-xxxl-inline-block">{{ $t("Search") }}</span>
          </button>
        </div>
      </div>
      <LPDataTable :paging="true" :paging_inline="true" :searching="1 != 1" :columns="columns"
        :datasource="'/ntfy/detail_messageTable_view?format=datatables'" :custom_options="options"
        ref="detailMessageListTable" @on_dbclick="on_dbclick" :custom_params_fun="messageListParamsFun" />
    </template>
  </LPModal>
</template>

<script>
import axios from "axios";
import LPDataTable from "@components/looper/tables/LPDataTable.vue";
import LPModal from "@components/looper/layout/LPModal.vue";
import LPFlatpickerDate from "@components/looper/forms/LPFlatpickerDate.vue";
export default {
  name: "MessageSummary",
  components: {
    LPDataTable,
    LPModal,
    LPFlatpickerDate,
  },
  data() {
    var _this = this;
    return {
      summary: [],
      totalQty: '',
      messageList: [],
      columns: [
        { field: 'inc_id', label: 'INC_ID', visible: false },
        {
          field: 'message', label: "Message", width: '280px',
          render: function (data) {
            const index = data.indexOf("\nDate");
            return index !== -1 ? data.substring(0, index) : data;
          }
        },
        { field: 'title', label: "Title", width: '160px' },
        {
          field: 'sent_time', label: "Send Time", width: '140px',
          render: function (data,s,row) { 
            if (row.msg_createdate)
              return _this.$moment(row.msg_createdate).format('YYYY-MM-DD HH:mm') 
            else
              return _this.$moment(data).format('YYYY-MM-DD HH:mm') 
          }
        },
        {
          field: 'actions', label: "Actions", visible: false
        },
      ],
      options: {
        responsive: false,
        processing: true,
        scrollY: "72vh",
        paging: false,
        autoWidth: false,
        scrollX: true,
        deferLoading: 0,
      },
      currentDate: '',
      contactData: [],
      detailFilter: {
        contact: "",
        RID: "",
        category_id: "",
        date: "",
      },
      messageListParamsFun: undefined,
      detailMesgModalTitle: '',
      summaryicon: [
        { id: 10, icon: "far fa-lightbulb" },
        { id: 20, icon: "fab fa-autoprefixer" },
        { id: 30, icon: "far fa-star" },
        { id: 40, icon: "fas fa-hourglass" },
        { id: 50, icon: "fab fa-fonticons-fi" },
        { id: 60, icon: "fas fa-signal" },
        { id: 70, icon: "fab fa-foursquare" },
        { id: 80, icon: "fas fa-check" },
        { id: 90, icon: "fas fa-bell" },
        { id: 100, icon: "fas fa-tasks" },
        { id: 110, icon: "far fa-comment-dots" },
        { id: 120, icon: "fab fa-linkedin-in" },
        { id: 130, icon: "fas fa-signal" },
        { id: 140, icon: "fab fa-hire-a-helper" },
      ],
      windowWidth: window.innerWidth,
    };
  },
  mounted() {
    $('.wrapper').on('shown.bs.modal', function (e) {
      $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
    });
    //窗口初始化時調用方法獲得後端數據
    this.getSummary();
    this.getCurrentDate();
    window.addEventListener('resize', this.updateWindowWidth);

    this.$nextTick(function () {
      $("title").html(this.$t("Message Summary"));
    })
  },
  created() {
    var self = this;
    self.init_contact();
    window.setTimeout(function () {
      $(".status_select").selectpicker("refresh");
    }, 2000);
  },
  methods: {
    async getSummary() {
      //使用axios插件庫訪問Django請求
      var contact = getParamFromUrl("contact");
      if (contact == undefined)
        contact = ""
      var date = getParamFromUrl("date");
      if (date == undefined)
        date == "";
      await axios
        .get("/ntfy/get_mesg_summary", { params: { contact: contact, date: date } })
        .then(response => {
          //處理返回數據
          let result = response.data;
          if (Array.isArray(result)) {
            const filteredData = result.filter(item => item.category_name !== null);
            this.summary = filteredData.map(item => {
              const iconInfo = this.summaryicon.find(icon => icon.id === item.category_id);
              return {
                ...item,
                icon: iconInfo ? iconInfo.icon : ''
              };
            });
            this.totalQty = this.summary.reduce((sum, item) => sum + item.num, 0);
          }
        })
        .catch(error => {
          console.log(error);
        });
    },
    async getMessageList(categoryID, categoryName) {
      var contact = getParamFromUrl("contact");
      if (contact == undefined)
        contact = ""
      var date = getParamFromUrl("date");
      if (date == undefined)
        date == "";
      this.detailFilter.category_id = categoryID
      this.messageListParamsFun = () => {
        return { contact: contact, category_id: categoryID, date: date };
      };

      this.$nextTick(function () {
        const categoryId = this.detailFilter.category_id;
        this.detailFilter = {};
        this.detailFilter.category_id = categoryId;

        this.$nextTick(() => {
          $(".status_select").selectpicker('refresh');
        })
        this.$refs.detailMessageListTable.datatable.clear().search("").draw();
        this.detailMesgModalTitle = categoryName;
        this.$refs.mesgModal.show();
      });
    },
    //初始化联系人員選項
    init_contact() {
      axios.get(`/PMIS/user/get_part_user_names`).then((response) => {
        if (response.data.data.length > 0) {
          this.contactData = response.data.data;
        }
      });
    },
    getCurrentDate() {
      const date = new Date();
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      this.currentDate = `${year}-${month}-${day}`;
    },
    on_dbclick(data) {
      var actions = JSON.parse(data.actions);
      if (actions.length > 0 && actions[0].url) {
        window.location.href = actions[0].url;
        // window.location.href = 'http://222.118.20.236:8074/en/chatwithai/project_status?id=2017#/'; //測試用
      }
    },
    searchMessage() {
      var contact = getParamFromUrl("contact");
      if (contact == undefined)
        contact = ""
      this.messageListParamsFun = () => {
        return {
          search_contact: this.detailFilter.contact,
          RID: this.detailFilter.RID, 
          contact: contact, 
          category_id: this.detailFilter.category_id,
          date: this.detailFilter.date
        };
      };
      this.$nextTick(function () {
        this.$refs.detailMessageListTable.datatable.search("").draw();
      });
    },
    masterClear() {
      for (var [key, value] of Object.entries(this.detailFilter)) {
        if (key !== 'category_id')
          this.detailFilter[key] = "";
      }
      this.$nextTick(() => {
        $(".status_select").selectpicker('refresh');
      })
    },
    updateWindowWidth() {
      this.windowWidth = window.innerWidth;
    },
    getTransformStyle(index) {
      let transformValue;
      if (this.windowWidth >= 1200) {
        const baseXValues = [10, 116, 316, 516];
        const baseYValues = [0, 88, 0, 88];

        const groupIndex = Math.floor(index / 4);
        const positionInGroup = index % 4;

        // 獲取當前索引相對於本組的 x 和 y 位移
        const baseX = baseXValues[positionInGroup];
        const baseY = baseYValues[positionInGroup];

        // 計算實際的 y 位移，隨著組數增加，y 軸的位移也增加
        const actualY = baseY + groupIndex * 260;
        transformValue = `translate3d(${baseX}px, ${actualY}px, 0px)`;
      } else {
        let yOffset = 0;
        if (index === 0) {
          yOffset = 0;
        } else if (index === 1) {
          yOffset = 88;
        } else if (index === 2) {
          yOffset = 200;
        } else {
          if (index % 2 === 1) {
            yOffset = this.summary[index - 2].yOffset + 200;
          } else {
            yOffset = this.summary[index - 2].yOffset + 200;
          }
        }
        this.summary[index].yOffset = yOffset;
        transformValue = `translate3d(${index % 2 === 0 ? 10 : 116}px, ${yOffset}px, 0)`;
      }

      return {
        transform: transformValue
      };
    },
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.updateWindowWidth);
  },
};
</script>