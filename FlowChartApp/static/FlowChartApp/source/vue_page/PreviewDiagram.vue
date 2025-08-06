<template>
    <BlankPageLayout>
        <template v-slot:page-Details>
        <!--<div class="d-flex">
        <div class="input-group input-group-sm input-group-alt">
            <div class="input-group-prepend">
              <span class="input-group-text">流程圖編號:</span>
            </div>
            <input type="text" class="form-control" @keyup.enter="show_flowchart" v-model="input_flowChartNo"/>
        </div>          
        <button type="button" class="btn btn-sm btn-primary ml-2" @click="show_flowchart">加載</button>
        </div>-->
          <FlowChart ref="FlowChart" flowchart_status="preview"  @nodeDubleClick="nodeDubleClick" @diagramClick="diagramClick"/>
        </template>
    </BlankPageLayout>   
</template>

<script>
import FlowChart from '@components/gojs/FlowChart.vue'
import BaseFlowChart_vueFrm from "./BaseFlowChart.vue"
import BlankPageLayout from '@components/looper/layout/page/BlankPageLayout.vue'
import axios from 'axios'
import { resolveComponent } from '@vue/runtime-core'
export default {
  name: 'PreviewDiagram',
  extends:BaseFlowChart_vueFrm,
  data() {
    return {
      input_flowChartNo:""
    }
  },
  components:{
      FlowChart,
      BlankPageLayout,
  },
  mounted(){
    const hashParams = new URLSearchParams(window.location.hash.split('?')[1]); // 分割並解析哈希中的查詢字符串
    const theme = hashParams.get('theme') || 'light';  // 默認為 light
    const pageClass = hashParams.get('pageClass');
    this.setTheme(theme);
    this.setPageClass(pageClass);

    this.flowChartInstance = this.$refs.FlowChart;
    if (this.$route.query.flowChartNo != undefined)
      this.show_flowchart(this.$route.query.flowChartNo)
  },
  methods:{
    setTheme(theme) {
      const themeClass = theme === 'dark' ? 'dark-theme' : 'default-theme';
      $(".wrapper").addClass(themeClass);
    },
    setPageClass(pageClass) {
      $(".wrapper").addClass(pageClass);
    }
  },  
}
</script>

<style scoped>
  >>> .page-title-bar {
    display:none;
  }
  >>> .page-inner {
    padding:0px;
  }
  textarea {
    width:450px; height:250px;
  }
  .input-group {
    width: auto;
  }
  input {
    width:200px;
  }
</style>
<style>
.previewDiagramPage #myDiagramDiv {
  height: calc(100vh - 2px) !important;
}

@supports (height: 100dvh) {
  .previewDiagramPage #myDiagramDiv {
    height: calc(100dvh - 2px) !important;
  }
}

.previewDiagramPage.default-theme #myDiagramDiv {
  background-color: white !important;
}

.previewDiagramPage.dark-theme #myDiagramDiv {
  background-color: #2d2d3f !important;
}

@media (min-width: 576px) {
  .previewDiagramPage #myDiagramDiv {
    height: calc(100vh - 2px) !important;
  }
}
</style>