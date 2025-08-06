import documentManagement from "../vue_page/documentManagement.vue"  //import index中的index與第1步中name:'index'名對應
set_router([
    {   path: '/', component: documentManagement,
    },   //添加路由，如果有多個一起添加到該數組中
]);