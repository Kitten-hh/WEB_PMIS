<script>
import axios from 'axios';
import ScheduleDashboard_UI from './ScheduleDashboard_UI.vue';
export default {
    name:"ScheduleDashboard_vueFrm",
    extends:ScheduleDashboard_UI,
    mounted(){
        this.getData();
    },
    methods:{
        getData() {
            axios.get("/schedule/get_schedule_dashboard_data").then((response)=>{
                var result = response.data;
                if (result.status) {
                    this.$refs.masterTable.datatable.clear();
                    this.$refs.masterTable.datatable.rows.add(result.data).draw();
                }else {
                    alert(gettext("get data fail!"))
                }
            })
        }
    }

}
</script>