$(function(){
    var modal_html = `
        <div class="modal fade" id="week_tasks" tabindex="-1" role="dialog" aria-labelledby="" aria-hidden="true">
            <div class="modal-dialog modal-dialog-scrollable modal-dialog-centered" role="document">
                <div class="modal-content">
                    <div class="modal-header align-items-center">
                        <h6 class="modal-title">` + gettext("Week's Tasks") + `</h6>
                        <button type="button" class="close text-dark" data-dismiss="modal" aria-label="Close" style="font-size: 1rem;"><i class="fas fa-times"></i></button>
                    </div>
                    <div class="modal-body p-0">
                    </div>
                    <div class="card-footer justify-content-end p-2">
                    </div>                    
                </div>
            </div>
        </div>        
    `;
    function init_week_tasks() {
        if ($("#week_tasks").length == 0)
            $("body").append(modal_html);
    }
    window.show_week_tasks = function(weekly_goal) {
        var load_data = new Promise((resolve,reject)=>{
            var sessions = weekly_goal.sessions;
            if (sessions == undefined || sessions == "")
                sessions = "{}";
            var relation_info = JSON.parse(sessions);
            var related_tasks = [];
            var related_querys = [];
            for (var [sessionid,taskids] of Object.entries(relation_info)) {
                if (taskids) {
                    var pid = sessionid.split("-")[0];
                    var tid = sessionid.split("-")[1];
                    var local_arr = taskids.split(",").map(x=>`${sessionid}-${x}`);
                    related_tasks.push(...local_arr);
                    taskids = `"` + taskids.replaceAll(",",`","`) + `"`;
                    query = `{"condition":"AND","rules":[
                        {"id":"pid","field":"pid","type":"string","input":"text","operator":"equal","value":"${pid}"},
                        {"id":"tid","field":"tid","type":"string","input":"text","operator":"equal","value":"${tid}"},
                        {"id":"taskid","field":"taskid","type":"string","input":"text","operator":"in","value":[${taskids}]}
                    ],"not":false,"valid":true}`;
                    related_querys.push(query)
                }
            }
            if (related_tasks.length > 0) {
                var tasks = `"` + related_tasks.join(",").replaceAll(",",`","`) + `"`;
                var params = {draw:0,length:-1,start:0,attach_query: `{"condition":"OR","rules":[${related_querys.join(",")}],"not":false,"valid":true}`};                                
                $.get("/PMIS/task/t_list", params, function(result_task){
                    resolve({goal:weekly_goal, tasks:result_task.data})               
                });                
            }else 
                resolve({goal:weekly_goal, tasks:[]})               
        });
        load_data.then((result)=>{
            var timeline_datas = []
            var goal = result.goal;
            var goaldesc = goal.goaldesc;
            var lines = goaldesc.replace(/\r\n/g, "\r").replace(/\n/g, "\r").split(/\r/);
            var tasks = result.tasks;
            var analysis_progress = {all_qty:tasks.length, f_qty:tasks.filter(x=>['C','F'].indexOf(x.progress) != -1).length, progress:0}
            if (analysis_progress.all_qty != 0)
                analysis_progress.progress = (analysis_progress.f_qty/analysis_progress.all_qty*100).toFixed(0);
            for (var i = 0; i < lines.length; i++) {
                var item = {pk:goal.inc_id, type:"goal", planbdate:new Date().toString("yyyy-MM-dd"), 'desc':lines[i], progress:"", sub_items:[]}
                if (/\(((\w+-\d+,?)+)\)$/i.test(lines[i])) {
                    var session_match = lines[i].match(/\(((\w+-\d+,?)+)\)$/i);
                    var sessionids = session_match[1];
                    var sub_tasks = tasks.filter(x=>sessionids.split(",").indexOf(x.taskno.substring(0, x.taskno.lastIndexOf("-"))) != -1)
                    for (var task of sub_tasks)
                        item.sub_items.push({pk:task.inc_id, type:"task", planbdate:new Date().toString("yyyy-MM-dd"), 'desc':task.task, progress:task.progress})
                }
                timeline_datas.push(item)
            }
            var sub_content_templ = `<div class="list-group list-group-messages list-group-flush list-group-bordered">
                <div class="list-group-item p-1 task-info" pk="[[pk]]">
                    <div class="list-group-item-figure pr-0">
                        <div class="tile tile-circle tile-sm bg-blue">[[progress]]</div>
                    </div>
                    <div class="list-group-item-body pl-2">[[desc]]
                    </div>
                </div>        
            </div>`;
            var progress_html = `<div class="d-flex w-100 align-items-center mt-2">
                <div class="progress progress-sm w-100">
                <div class="progress-bar bg-success progress-bar-striped progress-bar-animated" role="progressbar" style="width:[[progress]]%;" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
                </div>    
                <span class="ml-2 progress-desc">[[f_qty]]/[[all_qty]]([[progress]]%)</span>
            </div>`
            var title_tmpl = `<p class="font-weight-bold text-dark pt-1 mb-0 caption">[[desc]]</p><span class="d-none pk">[[inc_id]]</span><i class="far fa-right"></i>`;            
            var week_task_content = new SWTimeline2(gettext("Week's Tasks"), timeline_datas,"planbdate","",title_tmpl, undefined);        
            
            for (var i=0; i < timeline_datas.length; i++) {
                var sub_items = timeline_datas[i].sub_items;
                for (var sub_item of sub_items)
                    week_task_content.dom.find(".media:eq("+i+")").append(sub_content_templ.render(sub_item));              
            }
            week_task_content.dom.find(".card-header").hide();
            $("#week_tasks .modal-body").empty();
            $("#week_tasks .modal-body").append(week_task_content.dom);
            $("#week_tasks .card-footer").empty();
            $("#week_tasks .card-footer").append(progress_html.render(analysis_progress));
            $("#week_tasks").modal("show");
        })
    }
    init_week_tasks();
})