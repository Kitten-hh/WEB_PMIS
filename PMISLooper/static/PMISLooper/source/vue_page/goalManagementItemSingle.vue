<template>
<div class="col-sm-6 col-md-12 col-lg-6 col-xl-4">
    <LPCard :class_str="'cshadow goal_desc_wrapper mb-0'" @dblclick="show_detail">
    <template v-slot:header>
        <div class="d-flex align-items-center goal_descs">
        <div class="qua mt-1 mr-2 mr-sm-3">
            <h5 class="card-subtitle text-darkblue">
            <i class="fas fa-calendar text-darkblue mr-2"></i>
            <span class="font-weight-bolder mr-1">{{item.period}}</span>{{$t("period")}}
            </h5>
        </div>
        <div class="qua mt-1 mr-2 mr-sm-3">
            <h5 class="card-subtitle text-darkblue">
            <i class="fas fa-calendar-alt text-darkblue mr-2"></i>
            <span class="font-weight-bolder mr-1">{{item.month}}</span>{{$t("month")}}
            </h5>
        </div>
        <div class="qua mt-1 mr-2 mr-sm-3 order-first">
            <h5 class="card-subtitle text-darkblue">
            <i class="fas fa-calendar-week text-darkblue mr-2"></i>
            {{$t("where_week")}}<span class="font-weight-bolder mx-1">{{item.week}}</span>{{$t("week")}}
            </h5>
        </div>
        <div class="qua mt-1">
            <h5 class="card-subtitle text-darkblue">
            <i class="oi oi-person text-darkblue mr-2"></i>
            <span class="font-weight-bolder">{{item.contact}}</span>
            </h5>
        </div>
        </div>
    </template>
    <template v-slot:body>
        <div class="scrollbar">
        <div class="log-divider my-1">
            <span class="text-darkblue">
            <i class="oi oi-flag mr-1"></i>{{$t("goal_desc")}}
            </span>
        </div>
        <div class="task">
            <ul class="task-inner m-0 pl-2">
            <li class="task d-flex flex-column align-items-start border-0 p-0 mb-2">
                <span>
                {{item.goaldesc}}
                </span>
                <div class="d-flex w-100 align-items-center mt-2">
                <div class="progress progress-xs w-100">
                    <div
                    class="progress-bar bg-success"
                    role="progressbar"
                    :style="'width:'+item.progress+'%;'"
                    :aria-valuenow="item.progress"
                    aria-valuemin="0"
                    aria-valuemax="100"
                    ></div>
                </div>
                <span class="ml-2 progress-desc">{{item.f_qty}}/{{item.all_qty}}({{item.progress}}%)</span>
                </div>
            </li>
            </ul>
        </div>
        </div>
    </template>
    </LPCard>  
</div>
</template>

<script>
import LPCard from "@components/looper/layout/LPCard.vue";
export default {
    name:"goalManagementItemSingle",
    components: {
        LPCard
    },    
    data() {
        item:{}
    },
    props:{
        data:Object,
    },
    methods:{
        show_detail() {
            var temp_data = Object.assign({}, this.data);
            if (this.data.relationtasks) {
                var relationtasks = this.data.relationtasks.split(",");
                var sessions = {};
                for (var taskno of relationtasks) {
                    var arr = taskno.split("-");
                    var sessionid = arr[0] + "-" + arr[1];
                    if (!sessions.hasOwnProperty(sessionid))
                        sessions[sessionid] = arr[2];
                    else
                        sessions[sessionid] += "," +arr[2];
                }
                temp_data['sessions'] = JSON.stringify(sessions);
            }
            window.show_week_tasks(temp_data);        
        },        
        analysis_single_goal_progress() {
            this.item = this.data;
            this.item['progress'] = this.item.all_qty == 0 ? 0 : (this.item.f_qty/this.item.all_qty*100).toFixed(0);
        }
    },
    created() {
        this.analysis_single_goal_progress();
    }
}
</script>

<style>
</style>