<template>
    <BlankPageLayout>
        <template v-slot:page-Details>
            <LPCard show_part="hb" class_str="mb-2">
                <template v-slot:header>
                    <h5 class="mb-0">{{ $t("Schedule Dashboard") }}</h5>
                </template>
                <template v-slot:body>
                    <LPDataTable :paging="false" :columns="masterTable.columns" :datasource="masterTable.datasource"
                        :custom_params_fun="masterTable.custom_params_fun" :custom_options="masterTable.custom_options"
                        :orderBy="masterTable.orderBy"
                        @on_selectornot="masterTable.select_row"
                        :handle_response_fun="masterTable.handle_response_fun" :searching="1 == 1" :paging_inline="1 == 1" ref="masterTable" />
                </template>
            </LPCard>
        </template>
    </BlankPageLayout>    
</template>
<script>
import axios from "axios";
import BlankPageLayout from "@components/looper/layout/page/BlankPageLayout.vue";
import LPCard from "@components/looper/layout/LPCard.vue";
import LPDataTable, { DateRender } from "@components/looper/tables/LPDataTable.vue";
import LPCombobox from "@components/looper/forms/LPCombobox.vue";
export default {
    name:"ScheduleDashboard_vueFrm_UI",        
    components: {
        BlankPageLayout,
        LPCard,
        LPDataTable,
        LPCombobox
    },
    mounted() {
        this.$nextTick(function () {
            $("table.table").addClass("border-top-0 table-sm");
        });
        $(window).on('resize', function () {
            $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
        });
    },
    data() {
        var self = this;
        return {
            masterTable: {
                columns: [
                    { field: "recordid", label: gettext("Project Record ID"), width: "150px" },
                    { field: "projectname", label: gettext("Project Description"), width:"200px", render:function(data, type, full, meta){
                        data = data ? data : "";
                        return "<label title='" + data + `' class='text-truncate d-inline-block' style="width:200px;text-decoration: none;">` + data + "</label>";                  
                    }},
                    { field: "goal", label: gettext("Project Goal"), render:function(data, type, full, meta){
                        data = data ? data : "";
                        var tableWidth = $(".dataTables_scrollBody").width();
                        return "<label title='" + data + `' class='text-truncate d-inline-block' style="width:calc(${tableWidth}px - 950px);text-decoration: none;">` + data + "</label>";                  
                    } },
                    { field: "score", label: gettext("Priority"), width: "80px" },
                    { field: "taskqty", label: gettext("Total Tasks"), width: "100px" },
                    { field: "outtaskqty", label: gettext("Outstanding Tasks"), width: "140px" },
                    { field: "progress", label: gettext("Progress"), width: "60px" },
                    { field: "schfinishdate", label: gettext("Scheduled Finish Date"), width: "180px", render:DateRender },
                ],
                custom_options: {
                    responsive: true,  //是否支持手機展開和隱藏列
                    scrollX: true,
                    row_nowrap: true,
                    autoWidth: false,
                    scrollResize: true,
                    scrollY: "76vh",
                    drawCallback: function( settings ) {
                        self.$nextTick(function(){
                            var row_data = self.$refs.masterTable.datatable.row(':eq(0)', { page: 'current' }).data()
                            self.$refs.masterTable.datatable.row(':eq(0)', { page: 'current' }).select();
                        });
                    },
                    select: {
                        style:'single',
                        info: false,
                        //selector: "tr>td:nth-child(1), tr>td:nth-child(2), tr>td:nth-child(3), tr>td:nth-child(4)",
                    },
                    columnDefs: [
                    { "responsivePriority": 1, "className": "all", "targets": 0 },
                    { "responsivePriority": 1, "className": "all", "targets": 1 },
                    { "responsivePriority": 2, "className": "min-tablet-p", "targets": 2 },
                    { "responsivePriority": 3, "className": "min-tablet-p", "targets": 3 },
                    { "responsivePriority": 4, "className": "min-tablet-p", "targets": 4 },
                    { "responsivePriority": 5, "className": "min-tablet-p", "targets": 5 },
                    { "responsivePriority": 6, "className": "min-tablet-p", "targets": 6 },
                    { "responsivePriority": 7, "className": "min-tablet-p", "targets": 7 },
                    ],                                                            
                },
                datasource: [],
                //orderBy:[['score','desc']],
            },            
        }
    }

}
</script>
<style>
.page-inner {
    padding: 0px !important;
}

.page-inner .page-title-bar {
    margin: 0px !important;
}

.page-inner .card .card-body {
    padding-top: 0px !important;
}
.LPDataTable>.form-group {
    margin-bottom: 0px !important;
    margin-top: 0.25rem !important;
}
.LPDataTable>.form-group .input-group-append {
    display: none;
}
.LPDataTable>.form-group .input-group-alt>.input-group:first-child {
    border-top-right-radius: 0.25rem !important;
    border-bottom-right-radius: 0.25rem !important;
}
</style>