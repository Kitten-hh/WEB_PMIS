import ScheduleDistrMap_UI from "../vue_page/ScheduleDistrMap_UI.vue"
import ScheduleDistrMap from "../vue_page/ScheduleDistrMap.vue"
//set_router為BaseApp中Base Html定義的設置路由的公共方法
set_router([
    { path: '/', component: window.Design == "Y" ? ScheduleDistrMap_UI : ScheduleDistrMap},
]);