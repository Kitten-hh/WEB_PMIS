<template>
  <div class="aisummary_container">
    <div class="containerWrap scrollbar" :style="computedStyle">
      <pre>{{ compiledMarkdown }}</pre>
      <div v-if="reviewText != ''">
        <h2 class="review_title">Review</h2>
        <pre>{{ reviewText }}</pre>
      </div>
      <div class="floating-button-ai">
        <button class="btn btn-primary btn-icon btn-lg btn_aibox" @click="showAI"><i class="fas fa-robot"></i> <span class="sr-only">Chat With AI</span> </button>
        <button class="btn btn-primary btn-icon btn-lg" @click="showForm = true"><i class="fas fa-plus"></i><span class="sr-only">Add Review</span></button>
        <button class="btn btn-primary btn-icon btn-lg mt-3" @click="toGantt"><svg class="ganttIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M512 416l0-64c0-35.3-28.7-64-64-64L64 288c-35.3 0-64 28.7-64 64l0 64c0 35.3 28.7 64 64 64l384 0c35.3 0 64-28.7 64-64zM64 160l0-64 144 0 16 0 0 64L64 160zm224 0l0-64 80 0c8.8 0 16 7.2 16 16l0 16-38.1 0c-21.4 0-32.1 25.9-17 41L399 239c9.4 9.4 24.6 9.4 33.9 0L503 169c15.1-15.1 4.4-41-17-41L448 128l0-16c0-44.2-35.8-80-80-80L224 32l-16 0L64 32C28.7 32 0 60.7 0 96l0 64c0 35.3 28.7 64 64 64l160 0c35.3 0 64-28.7 64-64z"/></svg><span class="sr-only">Gantt</span></button>
      </div>
    </div>
    <div v-if="showForm" class="review-form" ref="review_form">
      <div class="form-group">
        <label for="reviewText">Your Review</label>
        <textarea class="form-control" id="reviewText" v-model="reviewText" rows="10"></textarea>
      </div>
      <button class="btn btn-success mr-2" @click="saveReview">Save</button>
      <button class="btn btn-secondary" @click="cancelReview">Cancel</button>
    </div>
  </div>

  <LPAIComBox ref="aicombox" class="mb-0" :iframe_src="'http://183.63.205.83:3000/aiChat'"  :aiPresetQuestion="aiPresetQuestion" :predefinedData="predefinedData"/>
    

  <div class="modal fade" id="session_gantt" tabindex="-1" role="dialog" aria-labelledby="form" aria-hidden="true"
    style="display: none;">
    <div class="modal-dialog modal-xl modal-dialog-scrollable " role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">
                    Gantt View
                </h5>
                <button type="button" class="close text-dark" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">×</span>
                </button>
            </div>
            <div class="modal-body"   style="overflow-y: hidden;">
                <div class="iframe_wrapper">
                    <iframe src="" frameborder="0" width='100%' id="pciframe" class="iframe" style="height:100%"></iframe>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import axios from 'axios';
import marked from 'marked';
import LPAIComBox from "@components/looper/general/LPAIComBox.vue";
export default {
  name: "ProjectStatus",
  components: {
    LPAIComBox,
  },
  data() {
    return {
      compiledMarkdown: "",
      showForm: false,
      reviewText: "",
      inc_id: undefined,
      review_form_height: 0,
      viewportHeight: this.getViewportHeight(),
      aiPresetQuestion:[],
      predefinedData:[],
      sessionids:'',
      recordid: '',
    }
  },
  created() {
    var id = getParamFromUrl("id");
    if (id != undefined)
      this.initData(id);
    window.addEventListener('resize', this.updateViewportHeight);
  },
  mounted() {
    window.addEventListener('resize', this.updateViewportHeight);
  },
  destroyed() {
    window.removeEventListener('resize', this.updateViewportHeight);
  },
  computed: {
    computedStyle() {
      return {
        height: this.showForm ? `calc(${this.viewportHeight}px - ${this.review_form_height}px)` : `calc(${this.viewportHeight}px)`
      };
    }
  },
  watch: {
    showForm(val) {
      if (val) {
        this.$nextTick(() => {
          this.getReviewHeight();
          this.observeReviewForm();
        });
      } else {
        if (this.observer) {
          this.observer.disconnect();
        }
      }
    },
    "compiledMarkdown": function (val) {
      var self = this
      setTimeout(() => {
        self.predefinedData = [val];
      }, 1000);
    },
  },
  methods: {
    toGantt() {
      $("#session_gantt iframe").attr("src", `/project/project_gantt_modal?recordid=${this.recordid}&sessionid=${this.sessionids}`);
      $("#session_gantt").find(".modal-dialog").width('98%').css("max-width","none")
      $("#session_gantt").modal("show");
    },
    initData(id) {
      axios.get("/chatwithai/project_status/update", { params: { pk: id } }).then((response) => {
        var result = response.data;
        if (result.status) {
          this.inc_id = result.data.inc_id;
          this.compiledMarkdown = result.data.aisummary;
          this.sessionids = result.data.sessionids
          this.recordid = String(result.data.recordid || '').padStart(5, '0') //左側添0
          if (result.data.review != null)
            this.reviewText = result.data.review
        }
      });
    },
    saveReview() {
        // 在此处添加您的保存数据逻辑，例如通过AJAX发送到服务器
        var id = getParamFromUrl("id");
        var formData = this.objectToFormData({ review: this.reviewText, id: id, review_isempty:this.reviewText === ""})
        axios.post("/chatwithai/project_status/update?pk={0}".format(this.inc_id), formData).then((response) => {
          var result = response.data;
          if (result.status) {
            alert(gettext("Save successfully"))
          } else
            alert(gettext("Save fail!"))
        })
        this.showForm = false;
    },
    cancelReview() {
      this.showForm = false;
    },
    getReviewHeight() {
      this.$nextTick(() => {
        const reviewForm = this.$refs.review_form;
        if (reviewForm) {
          this.review_form_height = reviewForm.offsetHeight;
        }
      });
    },
    getViewportHeight() {
      return window.visualViewport ? window.visualViewport.height : window.innerHeight;
    },
    updateViewportHeight() {
      this.viewportHeight = this.getViewportHeight();
    },
    observeReviewForm() {
      const reviewForm = this.$refs.review_form;
      if (reviewForm) {
        this.observer = new MutationObserver(() => {
          this.getReviewHeight();
        });
        this.observer.observe(reviewForm, { attributes: true, childList: true, subtree: true });
      }
    },

    showAI(){
      // this.$refs.aicombox.$refs.modal.width('900px')
      this.$refs.aicombox.$refs.modal.show()
    },
  },
};
</script>
<style scoped>
/* 添加一些基本样式来美化 Markdown 输出 */
div {
  line-height: 1.6;
  font-size: 16px;
}

#session_gantt .iframe_wrapper {
    height:calc(100vh - 3.5rem - 62px);
}
.ganttIcon {
    text-align: center;
    /* margin-right: .5rem; */
    fill: #f6f7f9;
    /* width: 1.25em; */
    width: 1.3em;
    margin-top: -6px;
    /* margin-left: .2rem; */
    /* font-size: 11px; */
}
</style>