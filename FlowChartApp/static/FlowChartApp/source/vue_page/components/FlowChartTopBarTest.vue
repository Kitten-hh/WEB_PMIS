<template>
  <div class="d-flex">
  <button class='bu' id="SaveButton" style="left:2px;top:300px;z-index:1500" @click="this.$emit('on_save')">Save</button>
  <button id='bu1'  style="left:50px;top:300px;z-index:1500" @click="this.$emit('on_load')">Load</button>
  <button id="edit" style="left:0px;top:-20px;z-index:1500">編輯流程圖</button>
  <button id="convert" style="left:0px;top:-20px;z-index:1500" @click="this.$emit('on_convert')">转换流程圖</button>
  <button id="convert_database" style="left:0px;top:-20px;z-index:1500" @click="this.$emit('on_convert_database')">轉換流程圖(數據庫)</button>  
  <label>顯示</label>
  <input @keyup.enter="show_flowchart" v-model="input_flowChartNo"/>
  </div>
</template>
<script>
export default {
    name:"FlowChartTopBarTest",
    props:{
      input_flowChartNo:String
    },
    data() {
        return {
            input_flowChartNo:""    
        }
    },
    methods:{
      show_flowchart() {
        this.$emit('show_flowchart',this.input_flowChartNo);
      }
    }
}
</script>