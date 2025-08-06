import TaskDashboard from "../vue_page/TaskDashboard.vue"  //import index中的index與第1步中name:'index'名對應
import TaskDashboard_UI from "../vue_page/TaskDashboard_UI.vue"  //import index中的index與第1步中name:'index'名對應
set_router([
    {   path: '/', component: window.Design == "Y" ? TaskDashboard_UI : TaskDashboard,
    },   //添加路由，如果有多個一起添加到該數組中
]);