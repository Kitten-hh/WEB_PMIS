import newMeeting from "../vue_page/newMeeting.vue"  //import index中的index與第1步中name:'index'名對應
import create_MettingMaster from "../vue_page/create_MettingMaster.vue"  //import index中的index與第1步中name:'index'名對應
set_router([
    {   path: '/', component:  newMeeting,
        children: [
            {
                path: 'create',  component: create_MettingMaster,
            },
        ]
    },   //添加路由，如果有多個一起添加到該數組中
]);