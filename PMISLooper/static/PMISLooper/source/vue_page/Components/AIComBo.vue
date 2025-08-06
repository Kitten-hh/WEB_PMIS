<template>
    <LPModal ref="modal" v-bind="$attrs"  :title="title" @on_open_state="open_state">
      <template v-slot:body>
        <div class="card mt-3">
          <div class="card-header w-100">
            <ul class="nav nav-tabs card-header-tabs scrollbar">
              <li class="nav-item dropdown ml-auto">
                <a
                  class="nav-link"
                  data-toggle="dropdown"
                  href="#"
                  role="button"
                  aria-expanded="false"
                >
                  <span class="font-weight-bold mr-2">{{
                    $t("Preset Question")
                  }}</span>
                  <span class="caret"></span>
                </a>
                <div class="dropdown-menu dropdown-scroll scrollbar" style="">
                  <div class="dropdown-arrow"></div>
                  <div
                    class="custom-control custom-radio dropdown-item"
                    v-for="(item, key) in aiPresetQuestion"
                    :key="key"
                  >
                    <label
                      class="custom-control-label d-flex justify-content-between"
                      @click="setInputVal(item)"
                      v-html="item"
                    ></label>
                  </div>
                </div>
              </li>
            </ul>
          </div>
          <div class="card-body scrollbar right_pane w-100">
            <iframe
              :src="iframe_src"
              frameborder="0"
              class="iframe mb-0"
              id="AIComBox_ChatAI_iframe"
              height="100%"
            ></iframe>
          </div>
        </div>
      </template>
      <template v-slot:footer>
        <button type="button" class="btn btn-secondary" data-dismiss="modal">
          {{$t('Close')}}
        </button>
      </template>
    </LPModal>
</template>

<script>
import LPModal from "@components/looper/layout/LPModal.vue";
export default {
  name: "AIComBox",
  components: {
    LPModal,
  },
  data() {
    return {
      isFullScreen: false,
      InputVal: "",
    };
  },
  props: {
    title:{ default:gettext('Chat With AI')},
    iframe_src: {
      default: "http://183.63.205.83:3000/aiChat",
    },
    predefinedData: {
      default: [],
    },
    predefinedData_master: {
      default: {},
    },
    aiPresetQuestion: {
      default: [],
    },
  },
  methods: {
    sendDataToReact(sendtype = "") {
      var iframeWindow = document.getElementById("AIComBox_ChatAI_iframe").contentWindow;
      var message = {
        type: "updateData",
        sendData:
          "This is data to analyze. You don't have to do anything, okay:{0}".format(
            JSON.stringify(this.predefinedData)
          ), // 示例数组
      };
      switch (sendtype) {
        case "InputVal": {
          message = {
            type: "InputVal",
            sendData: this.InputVal,
          };
          break;
        }
        case "predefinedData_master": {
          message = {
            type: "updateData",
            sendData: "For the following master and detail data that you need to analyze, you don't need to do anything at the moment:'{0}'".format(
            JSON.stringify(this.predefinedData_master)
          ), // 示例数组
          };
          break;
        }
      }
      iframeWindow.postMessage(message, this.iframe_src); // 确保URL与iframe的src匹配
    },
    setInputVal(val) {
      this.InputVal = val;
      this.sendDataToReact("InputVal");
    },
  },
  mounted() {},
  watch: {
    predefinedData: function (val) {
      this.sendDataToReact();
    },
    predefinedData_master: function (val) {
      this.sendDataToReact('predefinedData_master');
    },
    aiPresetQuestion: function (val) {
      this.sendDataToReact("presetQuestion");
    },
  },
};
</script>
<style>
.iframe {
  min-width: 100%;
  min-height: 500px;
  border-radius: 0.25rem;
}
</style>