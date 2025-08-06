$(function () {
    var group_title = `<div><span>[[recordid]]</span><span class=ml-4>[[tasklistno]]</span><span class="ml-4">[[tiddesc]]</span></div>`
    var subtitle_tmpl = `<div class="row" style="min-width:0;"><div class="col-12 font-weight-bolder"><span class="timeline-date text-primary time">[[contact]]</span>
                        <span class="ml-4 timeline-date text-primary time">[[progress]]</span>
                        <span class="ml-4 timeline-date text-primary time">[[schpriority]]</span>
                        <span class="d-none pk">[[inc_id]]</span></div>
                        <div class="col-12"><p class="font-weight-normal text-dark pt-1 mb-0 caption">[[task]]</p></div></div>`;
    var today_task = new SWTodolist(gettext("Group Tasks"), "/PMIS/task/group_tasks", ["tasklistno"], group_title, subtitle_tmpl, "schpriority desc");
    $("#group_tasks").append(today_task.dom);

    function update_task(self) {
        var pk = $(self).find(".pk").text();
        init_task(pk);
    }

    $(".page-inner").on(
        {
            dblclick:function(){
                update_task(this);
            },
            longpress:function() {
                update_task(this);
            }
        },
        ".SWTodolist .todo"
    );
});