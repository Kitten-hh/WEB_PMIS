<template>
    <LPCard :class_str="'cshadow goal_desc_wrapper'" @dblclick="show_detail">
    <template v-slot:header>
        <div class="d-flex align-items-center goal_descs">
        <div class="qua mt-1 mr-3">
            <h5 class="card-subtitle text-darkblue">
            <i class="fas fa-calendar text-darkblue mr-2"></i>
            <span class="font-weight-bolder mr-1">{{item.period}}</span>{{$t("period")}}
            </h5>
        </div>
        <div class="qua mt-1 mr-3">
            <h5 class="card-subtitle text-darkblue">
            <i class="fas fa-calendar-alt text-darkblue mr-2"></i>
            <span class="font-weight-bolder mr-1">{{item.month}}</span>{{$t("month")}}
            </h5>
        </div>
        <div class="qua mt-1 mr-3 order-first">
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
            <li v-for="(sub_item, sub_index) in item.single_goal" :key="sub_index" class="task d-flex flex-column align-items-start border-0 p-0 mb-2">
                <span>
                {{sub_item.desc}}
                </span>
                <div class="d-flex w-100 align-items-center mt-2">
                <div class="progress progress-xs w-100">
                    <div
                    class="progress-bar bg-success"
                    role="progressbar"
                    :style="'width:'+sub_item.progress+'%;'"
                    :aria-valuenow="sub_item.progress"
                    aria-valuemin="0"
                    aria-valuemax="100"
                    ></div>
                </div>
                <span class="ml-2 progress-desc">{{sub_item.f_qty}}/{{sub_item.all_qty}}({{sub_item.progress}}%)</span>
                </div>
            </li>
            </ul>
        </div>
        </div>
    </template>
    <template v-slot:footer>
        <div class="d-flex w-100 align-items-center p-3">
        <div class="progress progress-sm w-100">
            <div
            class="progress-bar progress-bar-striped progress-bar-animated"
            role="progressbar"
            :style="'width:' + item.progress + '%;'"
            :aria-valuenow="item.progress"
            aria-valuemin="0"
            aria-valuemax="100"
            ></div>
        </div>
        <span class="ml-2 progress-desc">{{item.f_qty}}/{{item.all_qty}}({{item.progress}}%)</span>
        </div>
    </template>
    </LPCard>  
</template>

<script>
import LPCard from "@components/looper/layout/LPCard.vue";
export default {
    name:"goalManagementItem",
    components: {
        LPCard
    },    
    data() {
        item:{}
    },
    props:{
        data:Object,
        tasks:Array
    },
    methods:{
        show_detail() {
            window.show_week_tasks(this.data);        
        },        
        analysis_single_goal_progress() {
            this.item = this.data;
            this.item['progress'] = this.item.all_qty == 0 ? 0 : (this.item.f_qty/this.item.all_qty*100).toFixed(0);
            var goaldesc = this.data['goaldesc'];
            var lines = goaldesc.replace(/\r\n/g, "\r").replace(/\n/g, "\r").split(/\r/);
            this.item['single_goal'] = []
            for (var i = 0; i < lines.length; i++) {
                var single_goal = lines[i]
                var all_qty = 0;
                var f_qty = 0;
                if (/\(((\w+-\d+,?)+)\)$/i.test(single_goal)) {
                    var session_match = single_goal.match(/\(((\w+-\d+,?)+)\)$/i);
                    var sessionids = session_match[1];
                    var relation_info = this.item.sessions;
                    if (relation_info) {
                        relation_info = JSON.parse(relation_info);
                        var session_arr = sessionids.split(",");
                        var related_tasks = [];
                        for(var sessionid of session_arr) {
                            var temp_tasks = relation_info[sessionid];
                            if (temp_tasks) {
                                var local_arr = temp_tasks.split(",").map(x=>`${sessionid}-${x}`);
                                related_tasks.push(...local_arr);
                            }
                        }
                        if (related_tasks.length > 0) {
                            var all_tasks = this.tasks.filter(x=>related_tasks.indexOf(x.taskno) != -1)
                            all_qty = all_tasks.length;
                            f_qty = all_tasks.filter(x=>x.progress == 'C' || x.progress == 'F').length;                        
                        }
                    }
                   
                }
                var progress = all_qty == 0 ? 0 : (f_qty/all_qty*100).toFixed(0)
                this.item['single_goal'].push({desc:single_goal, f_qty:f_qty, all_qty:all_qty, progress:progress})
            }
        }
    },
    created() {
        this.analysis_single_goal_progress();
    }
}
</script>

<style>
</style>