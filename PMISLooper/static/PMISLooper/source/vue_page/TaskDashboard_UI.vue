<template>
  <div class="page-inner page-inner-fill crmDashboard">
    <div class="el-example">
      <button type="button" class="btn btn-primary" @click="showTwoLineDashborad">{{ $t("TaskDashboard.Title") }}</button>
    </div>
  </div>
  <LPModal :show_part="'hb'" ref="crmTwoLineDashboardModal" class="crmDashboardModal fullScreenModal"
    :title="$t('TaskDashboard.Title')">
    <template v-slot:body>
      <div class="section-block my-2 d-flex flex-wrap align-items-center">
        <div class="d-flex align-items-center col-3">
          <label class="col-form-label col-form-label-sm caption col-auto pl-0">{{ $t("TaskDashboard.Dashtype") }}</label>
          <select class="status_select status_select_sm" data-toggle="selectpicker" data-width="100%" data-size="5" v-model="currentDashBoardModel"
            data-none-selected-text>
            <option v-for="item in dashBoardParaModel.dashboarTypes"  :key="item.fvalue" :value="item.fvalue">{{item.fvalue }}</option>            
          </select>
        </div>
        <div class="d-flex align-items-center col-1">
          <label class="col-form-label col-form-label-sm caption col-auto pl-0">{{ $t("contact") }}</label>
          <select class="status_select status_select_sm" data-toggle="selectpicker" data-width="100%" data-size="5" v-model="currentContact"
            data-none-selected-text>
            <option v-for="username in usernames" :key="username" :value="username">{{ username }}</option>
          </select>
        </div>
        <button type="button" class="btn btn-sm btn-primary">{{ $t("TaskDashboard.weekreport") }}</button>
      </div>
      <div id="cardAreaWrapper" class="tasks flex-row twoLineStyle">
        <ul :class="['task-body d-flex mb-0', isTile ? 'tilemode flex-wrap py-05 px-1' : 'overlapModel position-relative p-3', dashBoardParas.length <= 6 ? 'justify-content-center':'']">
          <li :class="['card-item',dashBoardParas.length <= 6 ? 'card-item-single-col':'']" :id="'twoColumnCard-' + index" v-for="(dashBoardItem, index) in dashBoardParas" :key="index" :style="setTransformStyle(index)">
            <TaskDashboardItem :ref="'item'+index" :itemParams="dashBoardItem" :dashBoardParam="dashBoardParam" :dashBoardParaModel="dashBoardParaModel" :isExpend="isExpend" :dashboardIndex="index" :isTile="isTile" @expander="expander" @tile="tile"
            :firstDashboardIsProject="firstDashboardIsProject"
            :setDashboardHeight="setDashboardHeight"/>
          </li>
        </ul>
      </div>
    </template>
  </LPModal>
</template>
<script>
import LPModal from "@components/looper/layout/LPModal.vue";
import TaskDashboardItem from "./Components/TaskDashboardItem.vue";
import LPDataTable, {
  DateRender,
} from "@components/looper/tables/LPDataTable.vue";
export default {
  name: "TaskDashboard_vueFrm_UI",
  components: {
    LPModal,
    LPDataTable,
    TaskDashboardItem,
  },
  data() {
    return {
      dashBoardParaModel:{dashboarTypes:[{fvalue:"Help Center"}, {fvalue:"Task Based"}, {fvalue:"Project Based"}]},
      dashBoardParam:{},
      usernames:['hb','sing','qfq'],
      currentDashBoardModel:"Task Based",
      currentContact:"sing",
      isExpend: false,
      isTile: false,
      searchCardLists: ["All Request", "hb's Recest Request for pass month", "hb's Outstanding External Request for pass month", "External Problem for pass eight days", "hb's External Problem for Class 1", "hb's Outstanding User Requirement","All Request", "hb's Recest Request for pass month", "hb's Outstanding External Request for pass month", "External Problem for pass eight days", "hb's External Problem for Class 1", "hb's Outstanding User Requirement"],
      dashBoardParas:[{"dashBoardPara":{"db010":false,"db011":false,"db012":null,"db013":null,"db003":1,"db002":"Task Based","db005":2,"db004":"[{\"qf001\":\"3\",\"qf002\":\"18\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"xxx's outstanding T\"},{\"qf001\":\"3\",\"qf002\":\"63\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"xxx's today task(T)\"},{\"qf001\":\"3\",\"qf002\":\"64\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"xxx‘s today task\"},{\"qf001\":\"290\",\"qf002\":\"74\",\"qf006\":\"sing\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Staff - Calendar\"},{\"qf001\":\"3\",\"qf002\":\"31\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"xxx's yesterday C\"}]","db001":"Default","db007":"Task","db006":"","db009":"","db008":"0"},"queryFilters":[{"qf001":"3","qf002":"18","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"hb's outstanding T"},{"qf001":"3","qf002":"63","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"hb's today task(T)"},{"qf001":"3","qf002":"64","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"hb‘s today task"},{"qf001":"290","qf002":"74","qf006":"sing","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Staff - Calendar"},{"qf001":"3","qf002":"31","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"hb's yesterday C"}]},{"dashBoardPara":{"db010":false,"db011":false,"db012":null,"db013":null,"db003":2,"db002":"Task Based","db005":3,"db004":"[{\"qf001\":\"3\",\"qf002\":\"32\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Weekly-xxx's scoring for pass week\"},{\"qf001\":\"3\",\"qf002\":\"19\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Specific-xxx's External Problem Schedule N\"},{\"qf001\":\"3\",\"qf002\":\"8\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Weekly-xxx's 8889 for this week\"}]","db001":"Default","db007":"Task","db006":"","db009":"TaskWithFrm","db008":"0"},"queryFilters":[{"qf001":"3","qf002":"32","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Weekly-hb's scoring for pass week"},{"qf001":"3","qf002":"19","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Specific-hb's External Problem Schedule N"},{"qf001":"3","qf002":"8","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Weekly-hb's 8889 for this week"}]},{"dashBoardPara":{"db010":false,"db011":false,"db012":null,"db013":null,"db003":3,"db002":"Task Based","db005":1,"db004":"[{\"qf001\":\"3\",\"qf002\":\"17\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Goal - xxx's weekly goal for this week(One week)\"},{\"qf001\":\"3\",\"qf002\":\"5\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Outstanding-xxx's 8888 outstanding\"},{\"qf001\":\"3\",\"qf002\":\"9\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Outstanding-xxx's 8889 outstanding\"},{\"qf001\":\"3\",\"qf002\":\"11\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Outstanding-xxx's OutStanding for Tasks Allocations\"},{\"qf001\":\"3\",\"qf002\":\"14\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Outstanding-xxx's All outstanding weekly goal\"},{\"qf001\":\"3\",\"qf002\":\"22\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Outstanding-xxx's Tasks Allocations for Bonus\"},{\"qf001\":\"3\",\"qf002\":\"29\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Outstanding-xxx's outstanding scoring\"},{\"qf001\":\"3\",\"qf002\":\"30\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Outstanding-xxx's Class 1 outstanding\"},{\"qf001\":\"3\",\"qf002\":\"13\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Weekly-xxx's complete tasks for pass week\"},{\"qf001\":\"3\",\"qf002\":\"15\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Weekly-xxx's scoring for last week\"},{\"qf001\":\"3\",\"qf002\":\"16\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Weekly-xxx's scoring for this week\"},{\"qf001\":\"3\",\"qf002\":\"8\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Weekly-xxx's 8889 for this week\"},{\"qf001\":\"3\",\"qf002\":\"24\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Goal-xxx's Quarterly Goal\"},{\"qf001\":\"3\",\"qf002\":\"25\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Goal-xxx's Monthly Goal\"},{\"qf001\":\"3\",\"qf002\":\"26\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Goal-xxx's Quarterly and Monthly Goal\"},{\"qf001\":\"3\",\"qf002\":\"27\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Goal-xxx's All Weekly Goal\"},{\"qf001\":\"3\",\"qf002\":\"28\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Goal-xxx's All weekly Goal with task\"},{\"qf001\":\"3\",\"qf002\":\"17\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Goal - xxx's weekly goal for this week(One week)\"},{\"qf001\":\"3\",\"qf002\":\"10\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Goal - xxx's weekly goal with tasks（one week)\"},{\"qf001\":\"3\",\"qf002\":\"12\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Goal - xxx's comming two week planning\"},{\"qf001\":\"3\",\"qf002\":\"23\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Goal - xxx's must complete goal\"},{\"qf001\":\"3\",\"qf002\":\"6\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Goal - xxx's last weekly goal\"},{\"qf001\":\"3\",\"qf002\":\"3\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Specific-xxx' all session in progress (See Project List Page\"},{\"qf001\":\"3\",\"qf002\":\"7\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Specific-xxx's 888-100 for past eight days\"},{\"qf001\":\"3\",\"qf002\":\"2\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Specific-xxx's task for past 8 days\"},{\"qf001\":\"3\",\"qf002\":\"4\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Specific-xxx's critical one for the pass 8 days\"},{\"qf001\":\"3\",\"qf002\":\"19\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Specific-xxx's External Problem Schedule N\"},{\"qf001\":\"3\",\"qf002\":\"20\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Specific-xxx's External Request Schedule N\"}]","db001":"Default","db007":"TreeTask","db006":"","db009":"TreeTask","db008":"0"},"queryFilters":[{"qf001":"3","qf002":"17","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Goal - hb's weekly goal for this week(One week)"},{"qf001":"3","qf002":"5","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Outstanding-hb's 8888 outstanding"},{"qf001":"3","qf002":"9","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Outstanding-hb's 8889 outstanding"},{"qf001":"3","qf002":"11","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Outstanding-hb's OutStanding for Tasks Allocations"},{"qf001":"3","qf002":"14","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Outstanding-hb's All outstanding weekly goal"},{"qf001":"3","qf002":"22","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Outstanding-hb's Tasks Allocations for Bonus"},{"qf001":"3","qf002":"29","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Outstanding-hb's outstanding scoring"},{"qf001":"3","qf002":"30","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Outstanding-hb's Class 1 outstanding"},{"qf001":"3","qf002":"13","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Weekly-hb's complete tasks for pass week"},{"qf001":"3","qf002":"15","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Weekly-hb's scoring for last week"},{"qf001":"3","qf002":"16","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Weekly-hb's scoring for this week"},{"qf001":"3","qf002":"8","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Weekly-hb's 8889 for this week"},{"qf001":"3","qf002":"24","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Goal-hb's Quarterly Goal"},{"qf001":"3","qf002":"25","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Goal-hb's Monthly Goal"},{"qf001":"3","qf002":"26","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Goal-hb's Quarterly and Monthly Goal"},{"qf001":"3","qf002":"27","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Goal-hb's All Weekly Goal"},{"qf001":"3","qf002":"28","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Goal-hb's All weekly Goal with task"},{"qf001":"3","qf002":"17","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Goal - hb's weekly goal for this week(One week)"},{"qf001":"3","qf002":"10","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Goal - hb's weekly goal with tasks（one week)"},{"qf001":"3","qf002":"12","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Goal - hb's comming two week planning"},{"qf001":"3","qf002":"23","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Goal - hb's must complete goal"},{"qf001":"3","qf002":"6","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Goal - hb's last weekly goal"},{"qf001":"3","qf002":"3","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Specific-hb' all session in progress (See Project List Page"},{"qf001":"3","qf002":"7","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Specific-hb's 888-100 for past eight days"},{"qf001":"3","qf002":"2","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Specific-hb's task for past 8 days"},{"qf001":"3","qf002":"4","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Specific-hb's critical one for the pass 8 days"},{"qf001":"3","qf002":"19","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Specific-hb's External Problem Schedule N"},{"qf001":"3","qf002":"20","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Specific-hb's External Request Schedule N"}]},{"dashBoardPara":{"db010":false,"db011":false,"db012":null,"db013":null,"db003":4,"db002":"Task Based","db005":1,"db004":"[{\"qf001\":\"3\",\"qf002\":\"2\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Specific-xxx's task for past 8 days\"},{\"qf001\":\"3\",\"qf002\":\"65\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Weekly-xxx's scoring for pass week不含循環任務\"},{\"qf001\":\"3\",\"qf002\":\"66\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Specific-xxx's task for past 8 days(不含循環任務）\"},{\"qf001\":\"3\",\"qf002\":\"70\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"xxx‘'s Past 8 days tasks raised by Mr. Chan\"}]","db001":"Default","db007":"Task","db006":"","db009":"TaskWithCteTime","db008":"0"},"queryFilters":[{"qf001":"3","qf002":"2","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Specific-hb's task for past 8 days"},{"qf001":"3","qf002":"65","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Weekly-hb's scoring for pass week不含循環任務"},{"qf001":"3","qf002":"66","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Specific-hb's task for past 8 days(不含循環任務）"},{"qf001":"3","qf002":"70","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"hb‘'s Past 8 days tasks raised by Mr. Chan"}]},{"dashBoardPara":{"db010":false,"db011":false,"db012":null,"db013":null,"db003":5,"db002":"Task Based","db005":2,"db004":"[{\"qf001\":\"3\",\"qf002\":\"5\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Outstanding-xxx's 8888 outstanding\"},{\"qf001\":\"3\",\"qf002\":\"9\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Outstanding-xxx's 8889 outstanding\"},{\"qf001\":\"3\",\"qf002\":\"14\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Outstanding-xxx's All outstanding weekly goal\"},{\"qf001\":\"3\",\"qf002\":\"29\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Outstanding-xxx's outstanding scoring\"},{\"qf001\":\"3\",\"qf002\":\"30\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Outstanding-xxx's Class 1 outstanding\"}]","db001":"Default","db007":"Task","db006":"","db009":"TaskWithTime","db008":"0"},"queryFilters":[{"qf001":"3","qf002":"5","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Outstanding-hb's 8888 outstanding"},{"qf001":"3","qf002":"9","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Outstanding-hb's 8889 outstanding"},{"qf001":"3","qf002":"14","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Outstanding-hb's All outstanding weekly goal"},{"qf001":"3","qf002":"29","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Outstanding-hb's outstanding scoring"},{"qf001":"3","qf002":"30","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Outstanding-hb's Class 1 outstanding"}]},{"dashBoardPara":{"db010":false,"db011":false,"db012":null,"db013":null,"db003":6,"db002":"Task Based","db005":1,"db004":"[{\"qf001\":\"3\",\"qf002\":\"27\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"TaskEnquiry_Frm\",\"qf003\":\"Goal-xxx's All Weekly Goal\"},{\"qf001\":\"1077\",\"qf002\":\"9\",\"qf006\":\"xxx\",\"qf009\":\"PMS\",\"qf010\":\"QueryFilter_Frm\",\"qf003\":\"XXX's Outstanding WorkFlow\"}]","db001":"Default","db007":"Task","db006":"","db009":"TaskWithTime","db008":"0"},"queryFilters":[{"qf001":"3","qf002":"27","qf006":"xxx","qf009":"PMS","qf010":"TaskEnquiry_Frm","qf003":"Goal-hb's All Weekly Goal"},{"qf001":"1077","qf002":"9","qf006":"xxx","qf009":"PMS","qf010":"QueryFilter_Frm","qf003":"hb's Outstanding WorkFlow"}]}],
      testOptions: {
        responsive: false,
        scrollY: "32vh",
        processing: true,
        autoWidth: false,
        scrollX: true,
        deferLoading: 0,
      },
      testColumns: [
        { field: "tid", label: "任務編號" },
        { field: "progress", label: "進度" },
        { field: "description", label: "任務描述" },
        { field: "contact", label: "聯繫人" },
        { field: "planbdate", label: "計劃開始" },
        { field: "priority", label: "優先級" },
        { field: "createDate", label: "創建日期" },
      ],
      testDataSourse: [
        { tid: "11580-3738-173", progress: "C", description: "入军就:GRY0089451易金额不顯示，烦處理一下", contact: "czz", planbdate: "2023-05-03", priority: "3011", createDate: "2023-05-03" },
        { tid: "11580-3738-173", progress: "C", description: "盘花课的外拼全空白，急，忙击快维修，谢谢。", contact: "czz", planbdate: "2023-05-03", priority: "3012", createDate: "2023-05-03" },
        { tid: "11580-3738-173", progress: "C", description: "限更改事直:原(Yuan)人事中", contact: "lsy", planbdate: "2023-05-03", priority: "3013", createDate: "2023-05-03" },
        { tid: "11580-3738-173", progress: "C", description: "CAD打不開，忙理，谢谢", contact: "lsy", planbdate: "2023-05-03", priority: "3014", createDate: "2023-05-03" },
      ],
      transLeft: 46,
      transTop: 46,
    }
  },
  mounted() {
    $('.wrapper').on('shown.bs.modal', function (e) {
      $(".status_select").selectpicker('refresh');
    });

    this.$nextTick(function () {
      $("table.table").addClass("border-top-0 table-sm");
      $(".dataTables_wrapper>.row").addClass("d-none");

      this.cardArea();
    });
    this.showTwoLineDashborad();
  },
  updated() {
    $(".status_select").selectpicker('refresh');
  },
  methods: {
    showDashborad() {
      this.$refs.crmDashboardModal.width("100vw");
      this.$refs.crmDashboardModal.show();
    },
    showTwoLineDashborad() {
      $(this.$refs.crmDashboardModal).remove();
      this.$refs.crmTwoLineDashboardModal.width("100vw");
      this.$refs.crmTwoLineDashboardModal.show();
    },
    expander(e) {
      e.preventDefault();
      this.isExpend = !this.isExpend;
      var wrapper = $(e.currentTarget).closest("li.card-item").attr("id");
      this.setDashboardHeight();
      if (this.isExpend)
        $("#cardAreaWrapper .card-item").removeClass("card-item-single-col");
      else
        $("#cardAreaWrapper .card-item").addClass("card-item-single-col");
      $("#" + wrapper).toggleClass("page-expanded");
      var index = parseInt(wrapper.split("-")[1]);
      this.$nextTick(() => {
        //$.fn.dataTable.tables({ visible: true, api: true }).columns.adjust().draw();
        this.relayoutDashboard(index);
      });
    },
    tile(e) {
      e.preventDefault();
      this.isTile = !this.isTile;
      this.setDashboardHeight();
      if (this.isTile)
        $("#cardAreaWrapper .card-item").removeClass("card-item-single-col");
      else
        $("#cardAreaWrapper .card-item").addClass("card-item-single-col");
      this.$nextTick(() => {
        //$.fn.dataTable.tables({ visible: true, api: true }).columns.adjust().draw();
        this.relayoutDashboard();
      });
    },
    relayoutDashboard(index=undefined) {
      if (index != undefined)
        this.$refs['item'+index][0].reloadGrid();
      else
        for(var i = 0; i < this.dashBoardParas.length; i++) {
          this.$refs['item'+i][0].reloadGrid();
        }
    },
    setDashboardHeight() {
      $(".LPDataTable .dataTables_scrollBody").css("height",(this.isExpend ? (this.isTile ? "calc(100vh - 8.5rem)" : "calc(100vh - 7rem)"): (this.isTile ? "32vh" : "456px")));
      $(".LPTreegrid .fixed-table-body").css("cssText", (this.isExpend ? (this.isTile ? "height:calc(100vh - 8.5rem + 37.59px) !important" : "height:calc(100vh - 7rem + 37.59px) !important"): (this.isTile ? "height:calc(32vh + 37.59px) !important" : "495.59px !important")))
    },
    cardArea() {
      return $(this).each(function () {
        $("#cardAreaWrapper .card-item").unbind("mouseenter click");
        $("#cardAreaWrapper .card-item").on("mouseenter click",
          function () {
            $(this).addClass("active").siblings().removeClass("active")
          })
      })
    },
    setTransformStyle(index) {
      var count = this.searchCardLists.length;
      var perContainer = 6;
      var self = this
      if(!this.isTile) {
        if (count > perContainer) {
          if(index < perContainer){
            return {transform: `translate3d(${index * self.transLeft}px, ${index * self.transLeft}px, 0)`}
          }else {
            var num = index - perContainer
            return {transform: `translate3d(${index * self.transLeft + 640}px, ${num * self.transTop}px, 0)`};
          }
        }else {
          return {transform: `translate3d(${index * self.transLeft}px, ${index * self.transTop}px, 0)`}
        }
      }
    },
  },
};
</script>