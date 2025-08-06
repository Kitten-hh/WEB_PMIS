<template>
  <div class="card mt-3 mb-0">
    <div class="card-header w-100">
      <ul class="nav nav-tabs card-header-tabs scrollbar">
        <li class="nav-item">
          <button
            type="button"
            class="btn btn-sm btn-light btn-icon text-darkblue"
            @click="toggleAIBox($event)"
          >
            <i
              :class="[
                isFullScreen ? 'fas fa-compress-alt' : 'fas fa-expand-alt',
              ]"
              style="font-size: 15px"
            ></i>
          </button>
        </li>
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
          <div class="dropdown-menu dropdown-menu-xl dropdown-scroll scrollbar" style="">
            <!-- <div class="dropdown-arrow"></div> -->
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
    <div class="card-body scrollbar right_pane w-100 py-2">
      <iframe
        :src="iframe_src"
        frameborder="0"
        class="iframe mb-0"
        id="ChatAI_iframe"
        height="98%"
      ></iframe>
    </div>
  </div>
</template>

<script>
import { watch } from "vue";
export default {
  name: "AIComBOX",
  data() {
    return {
      isFullScreen: false,
      InputVal: "",
      themeMode: "default-skin",
    };
  },
  props: {
    title: String,
    iframe_src: {
      default: "http://183.63.205.83:3000/aiChat",
    },
    predefinedData: {
      default: [],
    },
    defaultOptionSelected: {
      default: [],
    },
    aiPresetQuestion: {
      default: [],
    },
  },
  methods: {
    sendDataToReact(sendtype = "") {
      var iframeWindow = document.getElementById("ChatAI_iframe").contentWindow;
      var bodyClass = document.body;
      if (bodyClass.classList.contains('dark-skin')) {
        this.themeMode = 'dark-skin';
      }
      var message = {
        type: "updateData",
        sendData:
          "This is data to analyze. You don't have to do anything, okay'{0}'".format(
            JSON.stringify(this.predefinedData)
          ), // 示例数组
        className: this.themeMode,
      };
      switch (sendtype) {
        // case 'presetQuestion':{
        //     message = {
        //         type: 'presetQuestion',
        //         sendData:JSON.stringify(this.aiPresetQuestion) // 示例数组
        //     };
        //     break;
        // };
        case "InputVal": {
          message = {
            type: "InputVal",
            sendData: this.InputVal,
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
    toggleAIBox(e) {
      e.preventDefault();
      $("#ChatAI").toggleClass("fullScreen");
      this.isFullScreen = !this.isFullScreen;
    },
  },
  mounted() {},
  watch: {
    predefinedData: function (val) {
      this.sendDataToReact();
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
  border-radius: 0.25rem;
  /* height: 0; */
}

.fullScreen {
  width: 100% !important;
  height: 100vh !important;
  position: fixed !important;
  z-index: 1050 !important;
  left: 0px !important;
  top: 0px !important;
  background: #fff;
}
.fullScreen#ChatAI {
  margin-top: 0 !important;
}

.quit_btn {
  font-size: 25px;
  position: fixed !important;
  z-index: 1060 !important;
  right: 30px !important;
  top: 14px !important;
}

#ChatAI.card>.card-header .card-header-tabs {
  align-items: center;
}

#ChatAI.card>.card-header .card-header-tabs .nav-item.dropdown a.nav-link {
  padding-top: 10px;
  padding-bottom: 10px;
}

#ChatAI.card,
#ChatAI.card .nav-item.dropdown {
  position: static;
}

#ChatAI.card .dropdown-menu .custom-control-label {
  white-space: pre-wrap;
}

@media (max-width: 576px) {
  #ChatAI.card .dropdown-menu.dropdown-menu-xl {
    width: 20rem;
  }
}
@media (max-width: 385px) {
  #ChatAI.card>.card-body {
    padding: 2px !important;
  }
}
</style>