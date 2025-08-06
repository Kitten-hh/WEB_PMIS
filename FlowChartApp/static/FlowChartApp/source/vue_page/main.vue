<template>
    <MenuBar v-if="show_flowchart_menu" :menu_items="menu_items"/>
    <router-view/>
</template>
<script>
import App from '@components/../javascript/vue_looper_base/base_form1/source/vue_page/App.vue'
import axios from 'axios'
import MenuBar from "@components/looper/navigator/MenuBar.vue";
export default {
  name:"FlowChartMain",
  extends:App,
  components:{
    MenuBar
  },
  created() {
        var showFlowChartMenu = getParamFromUrl('showFlowChartMenu')
        this.show_flowchart_menu = showFlowChartMenu != "N";
   },
   data() {
    return {
        menu_items:[],
        show_flowchart_menu:true,
    }
   },
   methods:{
        list_to_tree(items, id = null, parent = 'parentid') {
            return items
            .filter(item => id == null ? item[parent] === id || item[parent] === "" : item[parent] === id)
            .map(item => ({ ...item,text:item.sysremark,url:"/menu/"+item.sysid,isnew: false, child: this.list_to_tree(items, item.sysid) }))
        },
        init_menu() {
            var self = this;
            axios.get("/devplat/spec/get_system").then((response)=>{
                if (response.data.status) {
                    self.menu_items = self.list_to_tree(response.data.data);
                    self.$nextTick(function(){
                        Looper.asideMenu();
                    });
                }
            })
        }
    },
    mounted() {
        if(this.show_flowchart_menu) {
            this.init_menu();
        }else {
            $(".app>.app-aside").show();
        }
        $("#app #stacked-menu").addClass("stacked-menu-has-collapsible");
        $("#app").on("click", ".stacked-menu .menu-item", function(e){
            e.stopPropagation();
            if ($(this).hasClass("has-child")) {
                $(this).toggleClass("has-open");
            }
        })
    }
  }
</script>
<style scoped>
  .hide_top_menu {
    padding-top:0px;
  }
  >>>.menu-item .menu-icon {
      width: 0px !important;
      margin-right:0px !important;
  }
</style>