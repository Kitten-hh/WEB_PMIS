import DiagramTest from "../vue_page/DiagramTest.vue"

set_router([
    { path: '/menu/:sysid', component:  DiagramTest},
    { path: '/:flowchartno', component:  DiagramTest},
    { path: '/', component:  DiagramTest},
]);

