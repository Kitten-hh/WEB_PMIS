    <script>
    import App from '@components/../javascript/vue_looper_base/base_form2/source/vue_page/App.vue'
    export default {
      name:"BaseApp",
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
          ]
        },
      }
    </script>