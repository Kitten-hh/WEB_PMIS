import ScheduleDashboard_UI from "../vue_page/ScheduleDashboard_UI.vue"
import ScheduleDashboard from "../vue_page/ScheduleDashboard.vue"
//set_router為BaseApp中Base Html定義的設置路由的公共方法
set_router([
    { path: '/', component: window.Design == "Y" ? ScheduleDashboard_UI : ScheduleDashboard},
]);