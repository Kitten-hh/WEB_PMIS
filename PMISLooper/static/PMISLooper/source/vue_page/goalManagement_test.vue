<template>
  <div class="page-inner goalManagementPage">
    <LPCard :class_str="'goalQuery'" show_part="b">
      <template v-slot:body>
        <div :class="['filter row', lang_code_en ? 'en_filter' : '']">
          <div class="form-group d-flex col-sm-3 col-md-3 col-lg col-xxl-auto goal_contact">
            <label class="col-form-label caption col-auto pl-0">{{ $t("Contact") }}</label>
            <select class="status_select" data-toggle="selectpicker" data-size="5" data-width="100%"
              v-model="params.contact" data-none-selected-text>
              <option value></option>
              <option v-for="(option, index) in options" :key="index" :value="option.text">{{ option.text }}</option>
            </select>
          </div>
          <div class="form-group d-flex goalMgmt_desc col-sm col-md col-xxl">
            <label class="col-form-label caption col-auto pl-0">{{ $t("goal_desc") }}</label>
            <input id="goal_description" type="text" class="form-control col" v-model="params.goaldesc">
          </div>
          <div class="col-auto goal_tools">
            <button type="button" class="btn btn-primary mr-1 mr-sm-2" @click="clear">
              <span class="">{{ $t("Clear") }}</span></button>
            <button class="btn btn-primary" type="button" @click="search">
              <span class="">{{ $t("Search") }}</span></button>
          </div>
        </div>
      </template>
    </LPCard>
    <div class="goalManagementItems">
      <div class="row">
        <div class="col-12 col-xl-6 col-xxl-4" v-for="(project, index) in projects" :key="index">
          <div class="card">
            <div class="card-header list-group-item-warning">
              <h4 class="card-title mb-0">{{project.proname}}</h4>
            </div>
            <div class="card-body goalMagtContent scrollbar">
              <ul class="timeline goalMagt_tiimeline p-0">
                <li class="timeline-item mustFinishItem" v-for="(item, index) in project.mustFinishItem" :key="index">
                  <div class="timeline-figure timeline-figure-light-primary pt-0">
                    <span class="tile tile-circle tile-sm bg-light tile_down">
                      <i class="fa fa-fw fa-chevron-down"></i>
                    </span>
                  </div>
                  <div class="timeline-body item_flex pt-0">
                    <div class="media">
                      <div class="media-body timeline-content">
                        <div class="mb-3">
                          <div class="d-flex flex-column justify-content-between">
                            <h6 class="alert-heading text-primary mb-1 pr-2">{{item.MFTask}}</h6>
                            <p class="mb-0"><strong>{{item.date}}</strong></p>
                          </div>
                        </div>
                        <div class="timeline-item position-relative" v-for="(data, index) in item.MHTask" :key="index">
                            <span class="arrow"></span>
                            <div class="timeline-body mx-3 pt-2">
                              <div class="media">
                                <div class="media-body">
                                  <div class="d-flex align-items-center mb-2 justify-content-between">
                                    <p class="mb-0 text-dark font-weight-normal">{{data.taskId}}</p>
                                    <p class="mb-0 font-weight-normal mr-2">{{data.date}}</p>
                                  </div>

                                  <p class="font-weight-bolder text-dark mb-2 caption"><i
                                      class="far fa-flag text-primary mr-2"></i>{{data.taskDesc}}</p>
                                  <div class="mustFinishMH">
                                    <span class="mr-3 text-dark"><i class="far fa-calendar-alt mr-2"></i>{{data.time}}</span>
                                    <span class="mr-3 text-dark"><i
                                        class="far fa-list-alt mr-2"></i>{{data.contact}}</span>
                                    <span class="mr-3 text-dark"><i class="far fa-file mr-2"></i>{{data.progress}}</span>
                                    <span class="text-dark"><i class="far fa-list-alt mr-2"></i>{{data.progressH}}</span>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                      </div>
                    </div>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import LPCard from "@components/looper/layout/LPCard.vue";
import goalManagementItem from "./goalManagementItem.vue";
import goalManagementItemSingle from "./goalManagementItemSingle.vue";

export default {
  name: "goalManagement",
  components: {
    LPCard,
    goalManagementItem,
    goalManagementItemSingle
  },
  data() {
    return {
      params: { is_overall: false },
      list: [],
      task_list: [],
      options: [],
      quarterlys: [],
      monthly: [],
      is_overall_search: false,
      lang_code_en: true,
      default_monthly: [],

      projects: [
        {
          proname: "G2.Web PIMS(00331)",
          mustFinishItem: [
            {
              MFTask: "(UR - Schedule) 完成排期設計與邏輯，將本季度的任務排期到本季度，Meeting中優先級高的任務能在Dashboard中排出來",
              date: "2022-10-24",
              MHTask: [
                {
                  date: "2022-11-30",
                  taskId: "00001-14008-20",
                  taskDesc: "Metting上的議題可以排期出來，且要合理，準確，在Dashboard可以看得到(Class1和meeting上的P)",
                  time: "00 : 00", ontact: "hb", progress: "N", progressH: "Must Have"
                },
                {
                  date: "2022-12-2",
                  taskId: "00001-14008-50",
                  taskDesc: "結論需要設置優先級和時間，分配，在dashboard可以看到, today's task可以看得到，（重要任務）",
                  time: "00 : 00", contact: "hb", progress: "N", progressH: "Must Have"
                },
                {
                  date: "2022-12-8",
                  taskId: "00001-14008-30",
                  taskDesc: "Meeting上立即做的任務，要在Dashboard排出來",
                  time: "00 : 00", contact: "hb", progress: "N", progressH: "Must Have"
                },
                {
                  date: "2022-12-23",
                  taskId: "00001-14008-10",
                  taskDesc: "討論實現Meeting排期的方案",
                  time: "00 : 00", contact: "hb", progress: "N", progressH: "Must Have"
                }
              ]
            },
            {
              MFTask: "完成Gojs Diagram模塊",
              date: "2022-11-21",
              MHTask: [
                {
                  date: "2022-4-4",
                  taskId: "00001-14002-160",
                  taskDesc: "實現Gojs Flow Chart編輯預覽功能，參考Flash Flow Chart",
                  time: "00 : 00", ontact: "hb", progress: "N", progressH: "Must Have"
                },
                {
                  date: "2022-12-22",
                  taskId: "00001-14002-150",
                  taskDesc: "實現gojs 流程圖中跳轉功能",
                  time: "00 : 00", contact: "hb", progress: "N", progressH: "Must Have"
                }
              ]
            }
          ],
        },
        {
          proname: "G3.Flutter Application(00357)",
          mustFinishItem: [
            {
              MFTask: "(UR - Notification for system messaging)完成能簡單發信息及客戶端消息提醒功能",
              date: "2022-12-31",
              MHTask: [
                {
                  date: "2022-11-8",
                  taskId: "00001-17021-490",
                  taskDesc: "消息列表中的消息可以點擊用瀏覽器打開對應的URL",
                  time: "00 : 00", ontact: "hb", progress: "N", progressH: "Must Have"
                },
                {
                  date: "2022-11-23",
                  taskId: "00001-17021-540",
                  taskDesc: "處理FCM通道接收到消息回調App將消息添加到App中, 用於顯示所有接收到的消息",
                  time: "00 : 00", ontact: "hb", progress: "N", progressH: "Must Have"
                },
                {
                  date: "2022-11-26",
                  taskId: "00001-17021-560",
                  taskDesc: "處理手機只收到前多少條消息(系統限制)的問題, 超過該限制的消息可以收到但不顯示",
                  time: "00 : 00", ontact: "hb", progress: "N", progressH: "Must Have"
                },
                {
                  date: "2022-11-26",
                  taskId: "00001-17021-570",
                  taskDesc: "處理App被Kill後以廠商通道的方式收到的消息，不能在消息列表中顯示的問題",
                  time: "00 : 00", ontact: "hb", progress: "N", progressH: "Must Have"
                },
                {
                  date: "2022-12-3",
                  taskId: "00001-17021-420",
                  taskDesc: "測試處理所有廠商手機彈出顯示通知的問題",
                  time: "00 : 00", ontact: "hb", progress: "N", progressH: "Must Have"
                }
              ]
            },
          ],
        },
        {
          proname: "G4.WebSo(00359)",
          mustFinishItem: [
            {
              MFTask: "(UR - 提醒和預警管理) 完善樣板狀態、Dashboard, 消息通知",
              date: "2022-10-15",
              MHTask: [
                {
                  date: "2022-10-14",
                  taskId: "00300-18024-180",
                  taskDesc: "Grovesite添加消息通知(先做)",
                  time: "00 : 00", ontact: "hb", progress: "N", progressH: "Must Have"
                }
              ]
            },
            {
              MFTask: "(UR- Web PO)完成根據恒力的送貨單生成我們採購收貨單",
              date: "2022-10-28",
              MHTask: [
                {
                  date: "2022-12-26",
                  taskId: "00300-18037-210",
                  taskDesc: "部署Vender_RestApi程序到恒力廠，確認他們有沒有固定ip，如果沒有看以怎樣的方式部署Vender_RestApi",
                  time: "00 : 00", ontact: "hb", progress: "N", progressH: "Must Have"
                }
              ]
            }
          ],
        },
      ],
    };
  },
  mounted() {
    var self = this;
    self.init_quarter();
    self.init_contact();
    self.init_filter_combobox();
    this.search();
    this.get_lang_code();
  },
  methods: {
    init_quarter() {
      axios.get(`/PMIS/goalmaster/get_all_period`).then(response => {
        if (response.data.data.length > 0) {
          var contacts = [];
          response.data.data.forEach((strkey, index) => {
            contacts.push({ id: index, text: strkey });
          });
          this.quarterList = contacts;
        }
      });
    },
    init_contact() {
      axios.get(`/PMIS/user/get_part_user_names`).then(response => {
        if (response.data.data.length > 0) {
          var contacts = [];
          response.data.data.forEach((strkey, index) => {
            contacts.push({ id: index, text: strkey });
          });
          this.options = contacts;
          this.$nextTick(() => {
            $(".status_select").selectpicker("refresh");
          })
        }
      });
    },
    init_filter_combobox() {
      this.init_quarterly();
      this.init_month();
      this.init_week();
    },
    period_change() {
      if (this.params.period) {
        var arr = this.params.period.split("-")
        var year = arr[0]
        var seq = parseInt(arr[1]);
        var last_month = seq * 3
        this.monthly = []
        this.monthly.push(`${year}-${('0' + (last_month - 2)).slice(-2)}`)
        this.monthly.push(`${year}-${('0' + (last_month - 1)).slice(-2)}`)
        this.monthly.push(`${year}-${('0' + (last_month)).slice(-2)}`)
        if (this.monthly.indexOf(this.params.month) == -1)
          this.params.month = "";
      } else {
        this.monthly = this.default_monthly;
      }
      this.$nextTick(() => {
        $("#params_month").selectpicker("refresh");
      })
    },
    init_month() {
      //默認顯示當月和前後兩個月
      var curr_month = Date.today().moveToFirstDayOfMonth();
      var pre_month1 = new Date(curr_month).addDays(-1).moveToFirstDayOfMonth();
      var pre_month2 = new Date(pre_month1).addDays(-1).moveToFirstDayOfMonth();
      var next_month1 = new Date(curr_month).moveToLastDayOfMonth().addDays(1).moveToLastDayOfMonth();
      var next_month2 = new Date(next_month1).addDays(1).moveToLastDayOfMonth();
      this.default_monthly.push(`${pre_month2.getFullYear()}-${('0' + (pre_month2.getMonth() + 1)).slice(-2)}`)
      this.default_monthly.push(`${pre_month1.getFullYear()}-${('0' + (pre_month1.getMonth() + 1)).slice(-2)}`)
      this.default_monthly.push(`${curr_month.getFullYear()}-${('0' + (curr_month.getMonth() + 1)).slice(-2)}`)
      this.default_monthly.push(`${next_month1.getFullYear()}-${('0' + (next_month1.getMonth() + 1)).slice(-2)}`)
      this.default_monthly.push(`${next_month2.getFullYear()}-${('0' + (next_month2.getMonth() + 1)).slice(-2)}`)
      this.monthly = this.default_monthly;
      this.params.month = this.monthly[2];
    },
    init_week() {
      var first_month_week = Date.today().moveToFirstDayOfMonth().getWeek();
      var last_month_week = Date.today().moveToLastDayOfMonth().getWeek();
      var today_week = Date.today().getWeek();
      this.params.week = (today_week - first_month_week) + 1;
    },
    init_quarterly() {
      var curr_arr = this.get_quarterly_date(new Date());
      var pre_arr = this.get_quarterly_date(new Date(curr_arr[0]).addDays(-1));
      var pre_pre_arr = this.get_quarterly_date(new Date(pre_arr[0]).addDays(-1));
      var next_arr = this.get_quarterly_date(new Date(curr_arr[1]).addDays(1));
      this.quarterlys.push(this.get_quarterly_str(next_arr[0]))
      this.quarterlys.push(this.get_quarterly_str(curr_arr[0]))
      this.quarterlys.push(this.get_quarterly_str(pre_arr[0]))
      this.quarterlys.push(this.get_quarterly_str(pre_pre_arr[0]))
      this.params.period = this.get_quarterly_str(curr_arr[0]);
    },
    get_quarterly_str(quarterly_date) {
      var year = quarterly_date.getFullYear();
      var quarter = Math.ceil((quarterly_date.getMonth() + 1) / 3)
      return `${year}-${quarter}`;
    },
    get_quarterly_date(currentDate) {
      var quarter = Math.ceil((currentDate.getMonth() + 1) / 3)
      var qbdate = new Date(currentDate.getFullYear(), 3 * quarter - 3, 1);
      var month = 3 * quarter
      var remaining = parseInt(month / 12)
      var qedate = new Date(currentDate.getFullYear() + remaining, month % 12, 1).addDays(-1);
      return [qbdate, qedate]
    },
    clear() {
      this.params = {};
      this.$nextTick(() => {
        $("select").selectpicker("refresh");
      })
    },
    search() {
      var self = this;
      self.list = []
      self.task_list = []
      axios.get(`/looper/goal/search_goal`, { params: this.params }).then(response => {
        var result = response.data;
        self.is_overall_search = self.params.is_overall == true;
        if (result.status) {
          self.list = result.data;
          self.task_list = result.tasks;
        }
      });
    },
    get_lang_code() {
      if ($("#curr_language_code").val() !== "en") {
        this.lang_code_en = false;
      }
    }
  }
};
</script>
<style>
.goalManagementPage .card.goalQuery>.card-body {
  padding-bottom: 8px;
}

.goalManagementPage .goalQuery div>.form-group {
  margin-bottom: 8px;
}

.goalManagementPage .goalQuery .goal_contact {
  width: 150px !important;
}

.goalManagementPage .goalManagementLists .card {
  border: 1px solid rgba(231, 234, 243, 0.7);
}

.goalManagementPage .goalMagtContent {
  height: 42rem;
  overflow-y: auto;
}

.goalManagementPage .timeline.goalMagt_tiimeline .timeline-figure .tile.tile_down {
  box-shadow: 0 0 0 1px #d7dce5;
  width: 1.25rem;
  height: 1.25rem;
  line-height: 1.25rem;
}

.goalManagementPage .timeline.goalMagt_tiimeline .timeline-figure-light-primary:before {
  top: 2rem;
  height: calc(100% - 2rem);
  border-left-width: 1px;
  border-left-style: solid;
  border-left-color: #e4e6ef;
  background-color: transparent;
}

.goalManagementPage .timeline.goalMagt_tiimeline .timeline-item.mustFinishItem {
  border-radius: 1rem;
  padding: 1rem;
  margin-bottom: 1rem;
  border: 1px dashed #e4e6ef;
  background-color: rgb(219 227 229 / 30%);
}

.goalManagementPage .timeline.goalMagt_tiimeline .timeline-item.position-relative {
  border: 1px dashed #e4e6ef;
  border-radius: 1rem;
  margin-bottom: 1rem;
  background: #edf2f9;
  color: #3f80ea;
}

.goalManagementPage .timeline.goalMagt_tiimeline .mustFinishItem:last-child,
.goalManagementPage .timeline.goalMagt_tiimeline .position-relative:last-child,
.goalManagementPage .timeline.goalMagt_tiimeline .position-relative:last-child .timeline-body,
.goalManagementPage .timeline.goalMagt_tiimeline .mustFinishItem:last-child .timeline-body, 
.goalManagementPage .timeline.goalMagt_tiimeline .mustFinishItem:last-child .timeline-figure {
  margin-bottom: 0;
}

.goalManagementPage .timeline.goalMagt_tiimeline .timeline-item .arrow {
  border: 1px solid #e6e8f0;
  border-left: 12px solid #e6e8f0 !important;
  display: block;
  height: 0;
  left: -32px;
  position: absolute;
  top: 50%;
  width: 0;
}
</style>