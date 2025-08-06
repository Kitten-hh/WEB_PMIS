import SchedulePriority_UI from "../vue_page/SchedulePriority_UI.vue"
import SchedulePriority from "../vue_page/SchedulePriority.vue"
//set_router為  BaseApp中Base Html定義的設置路由的公共方法
set_router([
    { path: '/', component: window.Design == "Y" ? SchedulePriority_UI : SchedulePriority},
]);