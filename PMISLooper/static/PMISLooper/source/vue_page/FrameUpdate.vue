<template>
  <div class="row">
    <div class="col-12">
      <div class="card">
        <div class="card-header">
          <div class="">
            <h5 class="text-center tech_title">{{ $t("Frame Update") }}</h5>
          </div>
        </div>
        <div class="card-body" id="stepper_from_div">
          <div class="form-row lang_en">
            <div
              class="
                form-group
                query_planBDate
                d-flex
                col-xxl-3 col-xxxl-3 col-sm-12 col-md-12 col-lg-4 col-xl-4
              "
            >
              <label class="col-form-label caption col-auto pl-0">{{
                $t("Contact")
              }}</label>
              <select
                class="status_select control"
                data-toggle="selectpicker"
                data-width="100%"
                data-size="5"
                data-none-selected-text
                v-model="contact"
              >
                <option></option>
                <option
                  v-for="(option, inx) in options"
                  :key="inx"
                  :value="option"
                >
                  {{ option }}
                </option>
              </select>
            </div>
            <div
              class="
                form-group
                query_planBDate
                d-flex
                col-xxl-5 col-xxxl-4 col-sm-12 col-md-12 col-lg-6 col-xl-6
              "
            >
              <label
                class="col-form-label caption col-auto pl-0"
                for="planBDates"
                >{{ $t("PlanBDate") }}</label
              >
              <div class="input-group input-group-alt m-0">
                <input
                  id="planBDates"
                  type="text"
                  class="form-control col"
                  data-toggle="flatpickr"
                  v-model="bdate"
                />
                <div class="input-group-append">
                  <span class="input-group-text custom-text">{{
                    $t("To")
                  }}</span>
                </div>
                <input
                  id="planBDatee"
                  type="text"
                  class="form-control col"
                  data-toggle="flatpickr"
                  v-model="edate"
                />
              </div>
            </div>
            <div class="col-auto query_tools order-sm-5 query_tools_col">
              <button class="btn btn-primary" @click="init_frame()" type="button">Search</button>
              <button class="btn btn-primary" @click="design" type="button">Design</button>
              <button class="btn btn-primary" @click="preview" type="button">Preview</button>
            </div>
          </div>
          <div id="Main_Page">
            <LPDataTable
              :paging="true"
              :searching="false"
              :columns="Frame_columns"
              :datasource="FrameupdateView"
              :pageLength="20"
              ref="FrameTable"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from "axios";
import LPMultipleSelect2 from "@components/looper/forms/LPMultipleSelect2.vue";
import LPCard from "@components/looper/layout/LPCard.vue";
import LPDataTable, {
  DateRender,
} from "@components/looper/tables/LPDataTable.vue";
import LPButton from "@components/looper/general/LPButton.vue";
import LPModalForm from "@components/looper/layout/LPModalForm.vue";
export default {
  name: "FrameUpdate_vueFrm",
  components: {
    LPMultipleSelect2,
    LPCard,
    LPDataTable,
    LPButton,
    LPModalForm,
  },
  props: {},
  data() {
    return {
      Frame_columns: [
        { field: "mh001", label: "窗口編號" },
        { field: "mh003", label: "功能序號" },
        { field: "mh004", label: "功能描述" },
      ],
      bdate: "",
      edate: "",
      contact: get_username(),
      FrameupdateView: [],
      options: [],
    };
  },
  mounted() {},
  created() {
    var self = this;
    self.init_contact();
    window.setTimeout(function () {
      self.bdate = self.getRecentDay_Date(-7);
      self.edate = self.getRecentDay_Date(0);
      self.init_frame();
    }, 1000);
    window.setTimeout(function () {
      $(".status_select").selectpicker("refresh");
    }, 2000);
  },
  methods: {
    //初始化联系人員選項
    init_contact() {
      axios.get(`/PMIS/user/get_part_user_names`).then((response) => {
        if (response.data.data.length > 0) {
          this.options = response.data.data;
        }
      });
    },
    init_frame() {
      //獲取會議記錄默認值
      axios
        .get(`/looper/frame/search_frames_list?bdate=${this.bdate}&edate=${this.edate}&username=${this.contact}`)
        .then((response) => {
          if (response.data.status) {
            this.$refs.FrameTable.datatable
              .clear()
              .rows.add(response.data.data)
              .draw();
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    design() {
      var data = {variables:{contact:this.contact,bdate:this.bdate, edate:this.edate}, datasource:{framelist:this.$refs.FrameTable.datatable.rows().data().toArray()}}
      this.design_report(`/static/PMISLooper/report/FrameUpdate.mrt`, data);      
    },
    preview() {
      var data = {variables:{contact:this.contact,bdate:this.bdate, edate:this.edate}, datasource:{framelist:this.$refs.FrameTable.datatable.rows().data().toArray()}}
      this.preview_report(`/static/PMISLooper/report/FrameUpdate.mrt`, data);      
    },    
    getRecentDay_Date: function (n) {
      var dd = new Date();
      dd.setDate(dd.getDate() + n); //获取n天后的日期
      var y = dd.getFullYear();
      var m = dd.getMonth() + 1; //获取当前月份的日期
      var d = dd.getDate();
      let day = y + "-" + m + "-" + d;
      console.log(day);
      return day;
    },
  },
};
</script>
<style>
.form-row {
    display: flex;
    flex-wrap: wrap;
    margin-right: -5px;
    margin-left: -5px;
}
</style>