<template>
    <BlankPageLayout>
        <template v-slot:page-Details>
          <FlowChartTopBar @on_load="on_load" @on_save="on_save"/>
          <FlowChart ref="FlowChart"/>
          <textarea id="mySavedModel" style="width:100%;height:300px">
          { "class": "go.GraphLinksModel",
          "linkFromPortIdProperty": "fromPort",
          "linkToPortIdProperty": "toPort",
          "nodeDataArray": [

            ],
          "linkDataArray": [

            ]}
          </textarea>          
        </template>
    </BlankPageLayout>
</template>

<script>
import FlowChart from '@components/gojs/FlowChart.vue'
import FlowChartTopBar from './components/FlowChartTopBar.vue'
import BlankPageLayout from '@components/looper/layout/page/BlankPageLayout.vue'
export default {
  name: 'Diagram',
  data() {
  },
  components:{
      FlowChart,
      FlowChartTopBar,
      BlankPageLayout
  },
  methods:{
    on_load() {
      this.$refs.FlowChart.load();
    },
    on_save() {
      document.getElementById("mySavedModel").value = this.$refs.FlowChart.getDiagram().model.toJson();
    }
  }
}
</script>

<style scoped>
  >>> .page-title-bar {
    display:none;
  }
  >>> .page-inner {
    padding:0px;
  }
</style>