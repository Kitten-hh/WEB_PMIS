<template>
  <BlankPageLayout>
    <template v-slot:page-Details>
      <div class="message">
        <div class="d-flex justify-content-between">
          <div>
            <div class="input-group input-group-sm input-group-alt mt-1 mx-2">
              <div class="input-group-prepend">
                <span class="input-group-text">{{ $t('FlowChartNo') }}:</span>
              </div>
              <input type="text" class="form-control br_radius" @keyup.enter="show_flowchart" v-model="input_flowChartNo"/>
              <div class="input-group-append">
                <button type="button" class="btn btn-sm btn-primary ml-2 bl_radius" @click="show">{{ $t('Load') }}</button>
              </div>
            </div>
  
          </div>
          <div><a :class="['view_history mr-1',history.length > 1 ? '':'disabled' ]" href="#" @click="prevFlowChart"><i
                class="fas fa-arrow-alt-circle-left"></i></a>
          </div>
        </div>
          <FlowChart ref="FlowChart" flowchart_status="preview" @nodeDubleClick="nodeDubleClick"
            @diagramClick="diagramClick" style="flex: 1;overflow-y: auto;"/>
        <FlowChartSysList_Component ref="sysList" @show_doc_click="show_doc_click" />
      </div>
    </template>
  </BlankPageLayout>
</template>

<script>
import FlowChart from '@components/gojs/FlowChart.vue'
import BaseFlowChart_vueFrm from "./BaseFlowChart.vue"
import FlowChartSysList_Component from "./components/FlowChartSysList.vue"
import BlankPageLayout from '@components/looper/layout/page/BlankPageLayout.vue'
export default {
  name: 'DiagramTest',
  extends: BaseFlowChart_vueFrm,
  data() {
    return {
      input_flowChartNo: ""
    }
  },
  components: {
    FlowChart,
    BlankPageLayout,
    FlowChartSysList_Component
  },
  mounted() {
    this.flowChartInstance = this.$refs.FlowChart;
    this.show_flowchart_with_route_param(this.$route)
    this.show();
    
    if (SWApp.os.isAndroid || SWApp.os.isPhone) {
      $(".page-section").height("calc(100vh - 7rem)")
    }
  },
  methods: {
    diagramClick(modelData) {
      this.$refs.sysList.setFlowChartInfo(modelData)
    },
    show() {
      var tempFlowChartNo = this.input_flowChartNo;
      if (!tempFlowChartNo)
        tempFlowChartNo = getParamFromUrl("flowChartNo");
      if (!tempFlowChartNo)
        tempFlowChartNo = this.$route.query.flowChartNo;
      if (tempFlowChartNo != undefined && tempFlowChartNo != "")
        this.show_flowchart(tempFlowChartNo)
    },
    show_flowchart_with_route_param(route) {
      if (route.params.flowchartno)
        this.show_flowchart(route.params.flowchartno);
      else
        this.show_flowchart(undefined, route.params.sysid);
    }
  },
  watch: {
    $route(to, from) {
      this.show_flowchart_with_route_param(to)
    }
  }
}
</script>

<style scoped>
>>>.page-title-bar {
  display: none;
}

>>>.page-inner {
  padding: 0px;
}

>>>#myDiagramDiv {
  height: calc(100vh - 133px) !important;
}

textarea {
  width: 450px;
  height: 250px;
}

.input-group {
  width: auto;
}

input {
  width: 200px;
}

.view_history {
  font-size: 25px;
}

>>>.page-section {
  height: calc(100vh - 3.5rem);
}

.br_radius {
  border-top-right-radius: .25rem !important;
  border-bottom-right-radius: .25rem !important;
}
.bl_radius {
  border-top-left-radius: .25rem !important;
  border-bottom-left-radius: .25rem !important;
}
.view_history.disabled {
  color:#888c9b;
  opacity: .5;
  pointer-events:none;
}
</style>