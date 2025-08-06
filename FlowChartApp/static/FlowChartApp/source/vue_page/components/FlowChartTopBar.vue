<template>
  <div class="d-flex">
  <button class='bu' id="SaveButton" style="left:2px;top:300px;z-index:1500" @click="this.$emit('on_save')">Save</button>
  <button id='bu1'  style="left:50px;top:300px;z-index:1500" @click="this.$emit('on_load')">Load</button>
  <button id="edit" style="left:0px;top:-20px;z-index:1500">編輯流程圖</button>
  </div>
</template>
<script>
export default {
    name:"FlowChartTopBar",
    data() {
        return {
            
        }
    },
}
</script>