<template>
  <sidebarLayout :isPageInnerFill="true" :isSidebarSectionFill="true" class="faqAnalysisTask">
    <template v-slot:pageNavsBtn>
      <div :class="['el-example', isMobile ? '' : 'pr-2 border-right']">
        <a class="btn btn-light btn-sm" href="#"><i class="fa fa-flip-horizontal fa-share"></i></a>
        <button class="btn btn-secondary btn-sm">問題按SubProject</button>
        <button class="btn btn-secondary btn-sm">問題按Session</button>
        <button class="btn btn-secondary btn-sm">Task按SubProject</button>
        <button class="btn btn-secondary btn-sm">Task按Session</button>
      </div>
      <small class="badge mx-2"><span class="text-danger mr-2">10</span><span class="text-primary">{{ $t('Task total')
      }}</span></small>
    </template>
    <template v-slot:pageSections>
      <div class="message-body h-100 overflow-y-auto scrollbar p-3">
        <div class="card card-body p-2">
          <h3 class="card-title text-center"> Horizontal Bar Chart </h3>
          <div id="flot-barhor" class="flot" style="padding: 0px; position: relative; height: 350px;"></div>
        </div>
        <div class="card masterTableCard">
          <LPDataTable ref="masterTable" :datasource="dataSource" :columns="masterColumns" :custom_options="masterOptions"
            :searching="1 != 1" :paging="1 != 1" />
        </div>
        <div class="card card-fluid totalByPieChart mb-0">
          <div class="card-body px-2 py-0 d-flex align-items-center">
            <div class="col-12 col-sm-4 pl-3 pt-3 p-sm-0 totalLeftPane">
                <div class="form-group col-6 mb-2">
                  <label class="col-form-label col-form-label-sm caption col-auto pl-0" for="">問題總計</label>
                  <input type="text" class="form-control form-control-sm col" value="54" readonly>
                </div>
                <div class="form-group col-6 mb-2">
                  <label class="col-form-label col-form-label-sm caption col-auto pl-0" for="">重要問題總計</label>
                  <input type="text" class="form-control form-control-sm col" value="0" readonly>
                </div>
                <div class="form-group col-6 mb-2">
                  <label class="col-form-label col-form-label-sm caption col-auto pl-0" for="">新需求總計</label>
                  <input type="text" class="form-control form-control-sm col" value="0" readonly>
                </div>
                <div class="form-group col-6 mb-2">
                  <label class="col-form-label col-form-label-sm caption col-auto pl-0" for="">完成總計</label>
                  <input type="text" class="form-control form-control-sm col" value="0" readonly>
                </div>
                <div class="form-group col-6 mb-2">
                  <label class="col-form-label col-form-label-sm caption col-auto pl-0" for="">未完成最早日期</label>
                  <input type="text" class="form-control form-control-sm col" value="2021-01-03" rnly>
                </div>
                <div class="form-group col-6 mb-0">
                  <label class="col-form-label col-form-label-sm caption col-auto pl-0" for="">未完成最近日期</label>
                  <input type="text" class="form-control form-control-sm col" value="2023-04-12" readonly>
                </div>
            </div>
            <div class="col-12 col-sm-8 totalRightPane px-1 justify-content-center">
              <div class="chartjs">
                <canvas ref="totalImportant" class="chartjs-render-monitor"></canvas>
              </div>
              <div class="chartjs">
                <canvas id="totalNewReq" class="chartjs-render-monitor"></canvas>
              </div>
              <div class="chartjs">
                <canvas id="totalCompleted" class="chartjs-render-monitor"></canvas>
              </div>
              <div class="chartjs">
                <canvas id="totalStatu" class="chartjs-render-monitor"></canvas>
              </div>
              <div class="chartjs">
                <canvas id="moduleProblemSummary" class="chartjs-render-monitor"></canvas>
              </div>
              <div class="chartjs">
                <canvas id="score" class="chartjs-render-monitor"></canvas>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    <template v-slot:sidebarSections>
      <div class="card card-reflow h-100">
        <div class="card-body p-2 h-100">
          <h4 class="card-title mb-1">問題分析條件面板</h4>
          <form name="searchform">
            <div class="row mx-0">
              <div class="form-group col-6 mb-1">
                <label class="col-form-label col-form-label-sm caption col-auto pl-0" for="">工程編號</label>
                <input type="text" class="form-control form-control-sm col">
              </div>
              <div class="form-group col-6 mb-1">
                <label class="col-form-label col-form-label-sm caption col-auto pl-0" for="">子工程編號</label>
                <input type="text" class="form-control form-control-sm col">
              </div>
              <div class="form-group col-12 mb-1">
                <label class="col-form-label col-form-label-sm caption col-auto pl-0">選擇子工程</label>
                <select class="status_select status_select_sm" data-toggle="selectpicker" data-width="100%" data-none-selected-text>
                  <option value="">{{ $t('Select Subproject') }}</option>
                  <option value="0">{{ $t('Catalogue') }}</option>
                  <option value="1">{{ $t('* SW BarCode') }}</option>
                </select>
              </div>
              <div class="form-group col-12 mb-1">
                <label class="col-form-label col-form-label-sm caption col-auto pl-0">{{ $t('PlanBDate') }}</label>
                <div class="input-group input-group-sm input-group-alt m-0">
                  <LPFlatpickerDate :small="true" v-model="planbs"/>
                  <div class="input-group-append" style="margin-right: -1px;">
                    <span class="input-group-text custom-text">{{ $t('To') }}</span>
                  </div>
                  <LPFlatpickerDate :small="true" v-model="planbe"/>
                </div>
              </div>
            </div>
            <div class="card-body pt-1 pb-2 px-2 questionTypeList">
              <fieldset class="scrollbar">
                <legend class="mb-0">問題分類列表</legend>
                <div class="list-group list-group-bordered mt-2 mb-3" data-toggle="radiolist">
                  <a href="#" class="list-group-item list-group-item-action active">UR - Technical Request</a>
                  <a href="#" class="list-group-item list-group-item-action">ERP 工程備份測試session安裝</a>
                  <a href="#" class="list-group-item list-group-item-action">UR - Django Repository</a>
                  <a href="#" class="list-group-item list-group-item-action">UR - UI Refinement</a>
                  <a href="#" class="list-group-item list-group-item-action">UR - Technical Cycle Management</a>
                  <a href="#" class="list-group-item list-group-item-action">UR - Web Design Production Course</a>
                  <a href="#" class="list-group-item list-group-item-action">Development UI Refinement</a>
                  <a href="#" class="list-group-item list-group-item-action">UR - Components</a>
                  <a href="#" class="list-group-item list-group-item-action">UR - Forum use django</a>
                  <a href="#" class="list-group-item list-group-item-action">User Requirement - 需求上報 Flutter</a>
                  <a href="#" class="list-group-item list-group-item-action">UR - App Gallery 實現一個含有多個App的網站，以手機顯示為主</a>
                  <a href="#" class="list-group-item list-group-item-action">UI Design with Js Component</a>
                  <a href="#" class="list-group-item list-group-item-action">UR - Notification for system messaging</a>
                </div>
              </fieldset>
            </div>
            <div class="form-actions border-top col">
              <button type="submit" class="btn btn-primary btn-block mr-1">分析問題</button>
              <button class="btn btn-block btn-link mt-0">清除</button>
            </div>
          </form>
        </div>
      </div>
    </template>
  </sidebarLayout>
</template>
<script>
import axios from "axios";
import LPCard from "@components/looper/layout/LPCard.vue";
import LPDataTable, {
  DateRender,
} from "@components/looper/tables/LPDataTable.vue";
import sidebarLayout from "@components/looper/layout/page/SidebarLayout.vue";
import LPFlatpickerDate from "@components/looper/forms/LPFlatpickerDate.vue";
export default {
  name: "FaqAnalysisTask_vueFrm",
  components: {
    LPCard,
    LPDataTable,
    sidebarLayout,
    LPFlatpickerDate,
  },
  data() {
    return {
      isMobile: false,
      planbs: '',
      planbe: '',
      masterOptions: {
        responsive: false,
        scrollY: "20vh",
        processing: true,
        autoWidth: false,
        scrollX: true,
        deferLoading: 0,
      },
      masterColumns: [
        { field: "itemno", label: "序號", },
        { field: "session", label: "名稱" },
        { field: "important_question", label: "重要問題" },
        { field: "new_requirement", label: "新需求" },
        { field: "completed_problem", label: "完成的問題" },
        { field: "question_qty", label: "問題數量" },
        { field: "earliest_incomplete", label: "未完成最早" },
        { field: "last_incomplete", label: "未完成最近" },
      ],
      dataSource: [
        { itemno: "00339", session: "Cloud CRM", important_question: "0", new_requirement: "0", completed_problem: "0", question_qty: "7", earliest_incomplete: "2023-01-03", last_incomplete: "2022-11-05" },
        { itemno: "00339", session: "Cloud CRM", important_question: "0", new_requirement: "0", completed_problem: "0", question_qty: "7", earliest_incomplete: "2023-01-03", last_incomplete: "2022-11-05" },
        { itemno: "00339", session: "Cloud CRM", important_question: "0", new_requirement: "0", completed_problem: "0", question_qty: "7", earliest_incomplete: "2023-01-03", last_incomplete: "2022-11-05" },
        { itemno: "00339", session: "Cloud CRM", important_question: "0", new_requirement: "0", completed_problem: "0", question_qty: "7", earliest_incomplete: "2023-01-03", last_incomplete: "2022-11-05" },
        { itemno: "00339", session: "Cloud CRM", important_question: "0", new_requirement: "0", completed_problem: "0", question_qty: "7", earliest_incomplete: "2023-01-03", last_incomplete: "2022-11-05" },
        { itemno: "00339", session: "Cloud CRM", important_question: "0", new_requirement: "0", completed_problem: "0", question_qty: "7", earliest_incomplete: "2023-01-03", last_incomplete: "2022-11-05" },
        { itemno: "00339", session: "Cloud CRM", important_question: "0", new_requirement: "0", completed_problem: "0", question_qty: "7", earliest_incomplete: "2023-01-03", last_incomplete: "2022-11-05" },
      ],
    };
  },
  mounted() {
    if (SWApp.os.isMobile) {
      this.isMobile = true
    }

    this.$nextTick(function () {
      $(".masterTableCard table.table").addClass("border-top-0 table-sm");
      $(".dataTables_wrapper>.row").addClass("d-none");
    });

    this.importantPieChart();
    this.newReqPieChart();
    this.completedPieChart();
    this.statuPieChart();
    this.summaryPieChart();
    this.scorePieChart();

    this.horizontalBarChart();
  },
  created() {
    window.setTimeout(function () {
      $(".status_select").selectpicker('refresh');
    }, 100);
  },
  updated() {
    $(".status_select").selectpicker('refresh');
  },
  methods: {
    horizontalBarChart() {
      var data_barhor = [[1, 0],
      [3, 1],
      [1, 2],
      [2, 3],
      [2, 4],
      [12, 0],
      ];
      var dataSet_barhor = [{
        label: 'Precious Metal Price',
        data: data_barhor,
        color: Looper.colors.brand.teal
      }];
      var ticks_barhor = [[0, 'UR -WebsO UI Enhancement'], [1, 'UR - temp task of meetting'], [2, 'UR - UI Refinement(Flex Replacement System)'], [3, 'UR - UI Enhancement of Second stage Management and Operational Flow'], [4, 'UR - Third stage of PMIS enhancement'], [5, 'UR - Meeting']];
      var options = {
        series: {
          bars: {
            show: true
          }
        },
        bars: {
          align: 'center',
          barWidth: 0.5,
          horizontal: true,
          fillColor: {
            colors: [{
              opacity: 1
            }, {
              opacity: 1
            }]
          },
          lineWidth: 1
        },
        xaxis: {
          axisLabelUseCanvas: true,
          axisLabelFontSizePixels: 12,
          axisLabelPadding: 10,
          axisLabelFontFamily: 'inherit, sans-serif',
          axisLabelColour: Looper.getMutedColor(),
          tickFormatter: function tickFormatter(v, axis) {
            return v;
          },
          max: 12
        },
        yaxis: {
          axisLabelUseCanvas: true,
          axisLabelFontSizePixels: 12,
          axisLabelPadding: 3,
          axisLabelFontFamily: 'inherit, sans-serif',
          axisLabelColour: Looper.getMutedColor(),
          tickLength: 0,
          ticks: ticks_barhor
        },
        legend: {
          noColumns: 0,
          position: 'ne'
        },
        grid: {
          hoverable: true,
          borderWidth: 0,
          color: Looper.getMutedColor()
        }
      }; // merge our setting with flot options

      options = $.extend(true, {}, Looper.flotDefaultOptions(), options); // init chart

      $('#flot-barhor').plot(dataSet_barhor, options);
    },
    randomScaling() {
      return Math.round(Math.random() * 100);
    },
    importantPieChart() {
      var data = {
        type: 'pie',
        data: {
          datasets: [{
            data: [this.randomScaling()],
            borderColor: [Looper.colors.brand.indigo],
            backgroundColor: [Looper.colors.brand.indigo],
            label: 'General'
          }],
        },
        options: {
          responsive: true,
          // 将hover动画设置为0，防止鼠标悬停产生闪烁
          // hover: {animationDuration: 0},
          animation: {
                onComplete: function (animation) {
                    var chartInstance = animation.chart;

                    ctx = chartInstance.ctx;
                    ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);
                    ctx.fillStyle = "#fff";
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'bottom';

                    this.data.datasets.forEach(function (dataset, i) {
                        var meta = chartInstance.getDatasetMeta(i);
                        meta.data.forEach(function (bar, index) {
                            var data = dataset.data[index];
                            ctx.fillText(data, bar.x, bar.y - 5);
                        });
                    });
                }
            },
        },
        plugins: {
          tooltip: {
          }
        }
      }; // init chart pie

      // var canvas = $('#totalImportant')[0].getContext('2d');
      var canvas = this.$refs.totalImportant;          
      var ctx = canvas.getContext('2d');
      var chart = new Chart(ctx, data);
    },
    newReqPieChart() {
      var data = {
        type: 'pie',
        data: {
          datasets: [{
            data: [this.randomScaling(), this.randomScaling(), this.randomScaling(), this.randomScaling(), this.randomScaling()],
            borderColor: [this.borderColor, this.borderColor, this.borderColor, this.borderColor, this.borderColor],
            backgroundColor: [Looper.colors.brand.red, Looper.colors.brand.purple, Looper.colors.brand.yellow, Looper.colors.brand.teal, Looper.colors.brand.indigo],
            label: 'Dataset 1'
          }],
          // labels: ['Red', 'Purple', 'Yellow', 'Green', 'Blue']
        },
        options: {
          responsive: true,
          legend: {
            display: false
          },
          title: {
            display: true,
            text: 'Pie Chart'
          }
        }
      }; // init chart pie

      var canvas = $('#totalNewReq')[0].getContext('2d');
      var chart = new Chart(canvas, data);
    },
    completedPieChart() {
      var data = {
        type: 'pie',
        data: {
          datasets: [{
            data: [this.randomScaling(), this.randomScaling(), this.randomScaling(), this.randomScaling(), this.randomScaling()],
            borderColor: [this.borderColor, this.borderColor, this.borderColor, this.borderColor, this.borderColor],
            backgroundColor: [Looper.colors.brand.red, Looper.colors.brand.purple, Looper.colors.brand.yellow, Looper.colors.brand.teal, Looper.colors.brand.indigo],
            label: 'Dataset 1'
          }],
          // labels: ['Red', 'Purple', 'Yellow', 'Green', 'Blue']
        },
        options: {
          responsive: true,
          legend: {
            display: false
          },
          title: {
            display: true,
            text: 'Pie Chart'
          }
        }
      }; // init chart pie

      var canvas = $('#totalCompleted')[0].getContext('2d');
      var chart = new Chart(canvas, data);
    },
    statuPieChart() {
      var data = {
        type: 'pie',
        data: {
          datasets: [{
            data: [this.randomScaling(), this.randomScaling(), this.randomScaling(), this.randomScaling(), this.randomScaling()],
            borderColor: [this.borderColor, this.borderColor, this.borderColor, this.borderColor, this.borderColor],
            backgroundColor: [Looper.colors.brand.red, Looper.colors.brand.purple, Looper.colors.brand.yellow, Looper.colors.brand.teal, Looper.colors.brand.indigo],
            label: 'Dataset 1'
          }],
          // labels: ['Red', 'Purple', 'Yellow', 'Green', 'Blue']
        },
        options: {
          responsive: true,
          legend: {
            display: false
          },
          title: {
            display: true,
            text: 'Pie Chart'
          }
        }
      }; // init chart pie

      var canvas = $('#totalStatu')[0].getContext('2d');
      var chart = new Chart(canvas, data);
    },
    summaryPieChart() {
      var data = {
        type: 'pie',
        data: {
          datasets: [{
            data: [this.randomScaling(), this.randomScaling(), this.randomScaling(), this.randomScaling(), this.randomScaling()],
            borderColor: [this.borderColor, this.borderColor, this.borderColor, this.borderColor, this.borderColor],
            backgroundColor: [Looper.colors.brand.red, Looper.colors.brand.purple, Looper.colors.brand.yellow, Looper.colors.brand.teal, Looper.colors.brand.indigo],
            label: 'Dataset 1'
          }],
          // labels: ['Red', 'Purple', 'Yellow', 'Green', 'Blue']
        },
        options: {
          responsive: true,
          legend: {
            display: false
          },
          title: {
            display: true,
            text: 'Pie Chart'
          }
        }
      }; // init chart pie

      var canvas = $('#moduleProblemSummary')[0].getContext('2d');
      var chart = new Chart(canvas, data);
    },
    scorePieChart() {
      var data = {
        type: 'pie',
        data: {
          datasets: [{
            data: [this.randomScaling(), this.randomScaling(), this.randomScaling(), this.randomScaling(), this.randomScaling()],
            borderColor: [this.borderColor, this.borderColor, this.borderColor, this.borderColor, this.borderColor],
            backgroundColor: [Looper.colors.brand.red, Looper.colors.brand.purple, Looper.colors.brand.yellow, Looper.colors.brand.teal, Looper.colors.brand.indigo],
            label: 'Dataset 1'
          }],
          // labels: ['Red', 'Purple', 'Yellow', 'Green', 'Blue']
        },
        options: {
          responsive: true,
          legend: {
            display: false
          },
          title: {
            display: true,
            text: 'Pie Chart'
          }
        }
      }; // init chart pie

      var canvas = $('#score')[0].getContext('2d');
      var chart = new Chart(canvas, data);
    },
  },
};
</script>