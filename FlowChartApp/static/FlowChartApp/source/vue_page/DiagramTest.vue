<template>
    <BlankPageLayout>
        <template v-slot:page-Details>
          <FlowChartTopBarTest @on_load="on_load" @on_save="on_save" @on_convert="on_convert" 
          @on_convert_database="on_convert_database" @show_flowchart="show_flowchart"/>
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
    <LPModalForm ref="modal_form" @on_submit="convert_demo">
            <textarea v-model="source_text" rows="30"/>
    </LPModalForm>
    <LPModalForm ref="modal_form_database" @on_submit="convert_database">
            <label>請錄入需要轉的FlowChartNo,多個以回車分隔</label>
            <textarea v-model="source_flowchartnos" rows="30"/>
    </LPModalForm>    
</template>

<script>
import {xml2json} from "xml2json-light"
import convertTool from "../javascript/ConvertTool"
import FlowChart from '@components/gojs/FlowChart.vue'
import FlowChartTopBarTest from './components/FlowChartTopBarTest.vue'
import BlankPageLayout from '@components/looper/layout/page/BlankPageLayout.vue'
import LPModalForm from "@components/looper/layout/LPModalForm.vue";
import axios from 'axios'
import { resolveComponent } from '@vue/runtime-core'
export default {
  name: 'DiagramTest',
  data() {
    return {
      source_text:"",
      source_flowchartnos:"",
    }
  },
  components:{
      FlowChart,
      FlowChartTopBarTest,
      BlankPageLayout,
      LPModalForm
  },
  methods:{
    on_load() {
      this.$refs.FlowChart.load();
    },
    on_save() {
      document.getElementById("mySavedModel").value = this.$refs.FlowChart.getDiagram().model.toJson();
    },
    on_convert() {
      this.$refs.modal_form.$refs.modal.show();
    },
    on_convert_database() {
      this.$refs.modal_form_database.$refs.modal.show();
    },
    show_flowchart(flowchartno, sysid=undefined, once=false) {
        var self = this;
        var url = '/flowchart/get_flowchart_data'
        if (sysid == undefined)
          url += `?flowChartNo=${flowchartno}`
        else
          url += `?sysid=${sysid}`
        axios.get(url).then((result)=>{
          if (result.data.status) {      
            try {
              self.$refs.FlowChart.getDiagram().model = go.Model.fromJson(result.data.data.content);
            }catch(e) {
              if (once == false) {
                self.convert_item(result.data.data.flowchartno).then((status)=>{
                  if (status) {
                    self.show_flowchart(result.data.data.flowchartno, undefined, true)
                  }
                });
              }
            }
          }
        });
    },
    convert_item(flowChartNo) {
      return new Promise((resolve, reject)=>{
        axios.get(`/flowchart/get_old_flowchart_data?flowChartNo=${flowChartNo}`).then((result)=>{
          if (result.data.status) {
            var gojs_data = convertTool.convert(result.data.data);
            var formData = new FormData();
            formData.append("flowChartNo", flowChartNo);
            formData.append("content", gojs_data);
            axios.post(`/en/flowchart/convert`, formData).then((result)=>{
              if (result.data.status)
                resolve(true)
              else
                resolve(false)
            }).catch(function (error) {
              console.log(error);
              resolve(false)
            });
          }
        }).catch(function (error) {
              console.log(error);
              resolve(false)
          });
      });
    },
    async convert_database() {
      var self = this;
      for (var flowChartNo of this.source_flowchartnos.split("\n")) {
        try {
          var status = await self.convert_item(flowChartNo);
          if (status)
            console.log(`轉換FlowChartNo:${flowChartNo} 成功`);
          else
            console.log(`轉換FlowChartNo:${flowChartNo} 失敗`);
        }catch(e) {
          console.log(e)
        }
      }
    },
    convert_demo() {
      var data = this.convert(this.source_text);
      this.$refs.FlowChart.getDiagram().model = go.Model.fromJson(data);
    },
    show_flowchart_with_route_param(route) {
      if (route.params.flowchartno)
        this.show_flowchart(route.params.flowchartno);
      else
        this.show_flowchart(undefined, route.params.sysid);
    }
  },
  mounted() {
    this.show_flowchart_with_route_param(this.$route)
  },
  watch:{
      $route (to, from){
        this.show_flowchart_with_route_param(to)
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
  textarea {
    width:450px; height:250px;
  }
</style>