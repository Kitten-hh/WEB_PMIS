import Preview from "../vue_page/Preview.vue"

set_router([
    { path: '/menu/:sysid', component:  Preview},
    { path: '/:flowchartno', component:  Preview},
    { path: '/', component:  Preview},
]);