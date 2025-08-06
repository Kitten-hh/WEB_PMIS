<script>
import TaskDashboard_vueFrm_UI from './TaskDashboard_UI.vue'
export default {
    name:"TaskDashboard_vueFrm_Tools",
    extends:TaskDashboard_vueFrm_UI,
    data() {
        return {
            DASHBOARD_GENERAL_QUERYFILTER_CONTACT:"XXX" //看板查詢條件中默認聯繫人
        }
    },
    methods:{
        getDashBoardModelName(nfield) {
            if(this.dashBoardParaModel.dashboarTypes && this.dashBoardParaModel.dashboarTypes.length>0){
				for(var syspara of this.dashBoardParaModel.dashboarTypes){
					if(syspara.nfield==nfield){
						return syspara.fvalue;
					}
				}
			}
			return "";            
        },
        firstDashboardIsProject() {
            return this.dashBoardParas.length > 0 && this.dashBoardParas[0].dashBoardPara.db009.toLowerCase().indexOf("project") != -1;
        },
        getDashBoardPara() {
            var param = undefined;
            if(builderDashBoardIndex<0)
                return undefined;
            var paras = undefined;
            if(this.currentDashBoardModel == this.dashBoardParaModel.dashboarSessionModelName){
                paras = this.dashboardSessionParas;
            }else{
                paras = this.dashBoardParas;
            }
            if(paras && paras.length>0){
                for(var dashBoardPara  in paras){
                    if(dashBoardPara && dashBoardPara.db003==(builderDashBoardIndex+1)){
                        param = dashBoardPara;
                        break;
                    }
                }
            }
            return param;            
        },
        handleDashboardPara(datas) {
            var result = []
            for(var dashBoardPara of datas) {
                var queryFilters = JSON.parse(dashBoardPara.db004);
                queryFilters = this.generalToContact(queryFilters);
                var params = {dashBoardPara:dashBoardPara, queryFilters:queryFilters}
                result.push(params)
            }
            return result;
        },
        generalToContact(queryFilters) {
            if(queryFilters && queryFilters.length>0){
                for(var queryFilter of queryFilters) {
                    queryFilter.qf003 = queryFilter.qf003.replaceAll(this.DASHBOARD_GENERAL_QUERYFILTER_CONTACT, this.currentContact);
                    queryFilter.qf003 = queryFilter.qf003.replaceAll(this.DASHBOARD_GENERAL_QUERYFILTER_CONTACT.toLowerCase(), this.currentContact);
                }
                return queryFilters;
            }
            return queryFilters;
        }        
    }
}
</script>
