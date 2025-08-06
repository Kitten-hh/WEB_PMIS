<script>
import LPDataTable, {
  DateRender,
} from "@components/looper/tables/LPDataTable.vue";
export default {
    name:"TaskDashboardDataTable",
    extends:LPDataTable,
    methods:{
        setHeaderMinWidth(el_obj) {
            var self = this;
            let api = undefined;
            let columns = undefined;
            el_obj.on("preInit.dt", function(e, settings) {
                api = new $.fn.dataTable.Api(settings);
                columns = api.settings().init().columns;
                api
                .columns()
                .header()
                .each((header, index) => {
                    var columnIndex = api.column(header).index();
                    var hasWidth = columns[columnIndex].width;
                    if(hasWidth && !(self.firstColSelected && index == 0)) {
                        $(header).css("max-width", hasWidth);
                        $(header).addClass("text-truncate");
                    }
                });
            });

        },
        init() {
            LPDataTable.methods.init.call(this);
            this.$nextTick(function(){
                $("#"+this.$refs.datatable.id).DataTable().columns.adjust();
            });
        },        
    }
}
</script>
