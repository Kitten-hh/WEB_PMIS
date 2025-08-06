<script>
import App from '@components/../javascript/vue_looper_base/base_form2/source/vue_page/App.vue'
export default {
  name:"FlowChartApp",
  extends:App,
  created() {
    this.menu_items = [
      {       
        text: "Dialy",
        url: "/flowchart/dialy",
        icon: "fas fa-home",
        is_href:true,
        isnew: false
      },
      {       
        text: "FlowChart",
        url: "/flowchart",
        icon: "fas fa-home",
        is_href:true,
        isnew: false
      },
      {       
        text: "FlowChartTest",
        url: "/flowchart/test",
        icon: "fas fa-home",
        is_href:true,
        isnew: false
      },
      {
        text:"Preview FlowChart",
        url: "/flowchart/preview",
        icon: "fas fa-home",
        is_href:true,
        isnew: false
      }     
      ]
    },
  }
</script>
<style scoped>
  .hide_top_menu {
    padding-top:0px;
  }
</style>