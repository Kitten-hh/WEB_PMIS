function PageUI() {
    var self = this;
    function getDay(date) {
        var day = date.toString("dd");
        if (day.substring(0,1) == "0")
            return day.substring(1,2);
        else
            return day;
    }
    this.init = function() {
        self.modify_boardlist_tmpl();
        self.init_tasks_performance();
        self.init_active_session();
        //初始化日期選擇
        $("#dpToday").attr("data-start", Date.today().toString("yyyy-MM-dd"));
        $("#dpToday").attr("data-end", Date.today().toString("yyyy-MM-dd"));
        $("#dpToday").next("label").find(".text-muted").text("{0} {1}".format(Date.today().toString("MMM"), getDay(Date.today())))
        $("#dpYesterday").attr("data-start", Date.today().add(-1).day().toString("yyyy-MM-dd"));
        $("#dpYesterday").attr("data-end", Date.today().add(-1).day().toString("yyyy-MM-dd"));
        $("#dpYesterday").next("label").find(".text-muted").text("{0} {1}".format(Date.today().add(-1).day().toString("MMM"), 
        getDay(Date.today().add(-1).day())));
        $("#dpWeek").attr("data-start", Date.monday().toString("yyyy-MM-dd"));
        $("#dpWeek").attr("data-end", Date.monday().add(6).day().toString("yyyy-MM-dd"));
        $("#dpWeek").next("label").find(".text-muted").text("{0} {1}-{2}".format(Date.monday().toString("MMM"), 
        getDay(Date.monday()), getDay(Date.monday().add(6).day())));
        $("#dpMonth").attr("data-start", Date.today().moveToFirstDayOfMonth().toString("yyyy-MM-dd"));
        $("#dpMonth").attr("data-end", Date.today().moveToLastDayOfMonth().toString("yyyy-MM-dd"));
        $("#dpMonth").next("label").find(".text-muted").text("{0} {1}-{2}".format(Date.today().moveToFirstDayOfMonth().toString("MMM"), 
        getDay(Date.today().moveToFirstDayOfMonth()), getDay(Date.today().moveToLastDayOfMonth())));
        var quarter = self.get_quarterly_date(Date.today());
        $("#dpQuarter").attr("data-start", quarter[0].toString("yyyy-MM-dd"))
        $("#dpQuarter").attr("data-end", quarter[1].toString("yyyy-MM-dd"))
        $("#dpQuarter").next("label").find(".text-dark").text("{0}-{1}".format(quarter[0].toString("MMM"), quarter[1].toString("MMM")));        
        $("#dpYear").attr("data-start", "{0}-01-01".format(Date.today().toString("yyyy")));
        $("#dpYear").attr("data-end", "{0}-12-31".format(Date.today().toString("yyyy")));
        $("#dpYear").next("label").find(".text-muted").text("{0}".format(Date.today().moveToFirstDayOfMonth().toString("yyyy")));
        var dp_index = getParamFromUrl("dp");
        if (dp_index) {
            $($("input[name='dpFilter']")[dp_index]).prop("checked", true);
            $(".dpFilter_dropdown span").text($($("input[name='dpFilter']")[dp_index]).next("label").find("span:eq(0)").text());
        }
        self.computer_completion_rate_with();
    }
    this.computer_completion_rate_with = function() {
        var min_width = 0;
        $(".completion_rate .list-group-item-figure span").each((index, item)=>{
            var metrics = $(item).textMetrics();
            if (metrics['width'] > min_width)
                min_width = metrics['width']
        });
        $(".completion_rate .list-group-item-figure span").css("min-width", "{0}px".format(min_width));
    }
    
    this.getDpFilterParams = function() {
        var dpFilter = $("input[name='dpFilter'][checked]");        
        var result_index = 2;
        $("input[name='dpFilter']").each(function(index, el){
            if ($(el).prop("checked")) {
                result_index = index;
                return false;
            }
        });
        return result_index;
    }


    this.get_quarterly_date = function(currentDate) {
        var quarter = Math.ceil((currentDate.getMonth() + 1)/3)
        var qbdate = new Date(currentDate.getFullYear(), 3 * quarter - 3, 1);    
        var month = 3 * quarter
        var remaining = parseInt(month / 12)
        var qedate = new Date(currentDate.getFullYear() + remaining, month % 12, 1).addDays(-1);    
        return [qbdate, qedate]
    }    

    this.init_tasks_performance = function() {
        $('.easypiechart').each(function() {
            var e = $(this).data();
            e.barColor = e.barColor || t.colors.brand.teal,
            e.trackColor = e.trackColor;
            e.scaleColor = e.scaleColor;
            e.lineWidth = e.lineWidth ? parseInt(e.lineWidth) : 8,
            e.size = e.size ? parseInt(e.size) : 120,
            e.rotate = e.rotate ? parseInt(e.rotate) : 0,
            e.trackColor = "false" != e.trackColor && "" != e.trackColor && e.trackColor,
            e.scaleColor = "false" != e.scaleColor && "" != e.scaleColor && e.scaleColor,
            $(this).easyPieChart(e)
        })                
    }    
    this.modify_boardlist_tmpl = function(){
        $("#SWBoardlist .task-issue .card-footer").html(`
            <a href="#" class="card-footer-item card-footer-item-bordered text-dark left"><i class="oi oi-comment-square mr-1"></i></a> 
            <div class="card-footer-item card-footer-item-bordered text-dark right scrollX">
                <div class="session_task_filter d-flex justify-content-between">
                <a href="#" class="badge badge-subtle badge-dark mr-1" progress="N">N</a>
                <a href="#" class="badge badge-subtle badge-dark mr-1" progress="I">I</a>
                <a href="#" class="badge badge-subtle badge-dark mr-1" progress="T">T</a>
                <a href="#" class="badge badge-subtle badge-dark mr-1" progress="C">C</a>
                <a href="#" class="badge badge-subtle badge-dark mr-1" progress="F">F</a>
                <a href="#" class="badge badge-subtle badge-dark mr-1" taskprogress="NF">NF</a>
                <a href="#" class="badge badge-subtle badge-dark mr-1" taskcategory="MF">MF</a>
                <a href="#" class="badge badge-subtle badge-dark mr-1" taskcategory="MH">MH</a>
                <a href="#" class="badge badge-subtle badge-dark mr-1" classField="C1">C1</a>
                </div>
            </div>
            <a href="#" class="card-footer-item card-footer-item-bordered text-dark add_task"><i class="fa fa-plus-circle"></i></a>
        `)
        
    }    

    this.init_active_session = function() {
        var header_title = `<span class="recordid">[[recordid]]</span><span class="ml-2 sessionid">[[sessionid]]</span>
        <span class="ml-2">[</span>
        <span class="">[[owner]]</span>
        <span class="">]</span>`;
        var header_sub_title = `<h6 class="item-header-subtitle card-subtitle text-dark">
            <div class="ppsp"><span class="">[[planbdate]] / [[planedate]]</span><span class="ml-2 badge badge-subtle badge-dark font-size-lg">[[progress]]</span>
            </div>
            </h6>`;
        var quarterly = "{0}-{1}".format(Date.today().format('yyyy'), parseInt(Date.today().getMonth()/3) + 1);
        var sessions = new SWBoardlist(gettext("Active Sessions"), "/looper/team_dashboard/get_followup_sessions",
        "", header_title, header_sub_title,"sdesp","taskc","taskqty");
        sessions.processors_function = function(item){
            if (Date.parse(item["planbdate"]) != null)
                item["planbdate"] = Date.parse(item["planbdate"]).toString("yyyy-MM-dd");
            if (Date.parse(item["planedate"]) != null)
                item["planedate"] = Date.parse(item["planedate"]).toString("yyyy-MM-dd");
            
        }
        $("#Active_Sessions").append(sessions.dom);
        
        sessions.dom.find(".task-body").on("click", ".card-footer .add_task", function(e){
            e.preventDefault(); //阻止按鈕默認動作
            e.stopPropagation();
            var sessionid = $(this).closest(".card").find(".sessionid").text();
            
            init_task(undefined, {sessionid:sessionid});
            if ($(this).closest(".task-issue").next(".task-collapse").length > 0) {
                var session_dom = $(this).closest(".task-issue");
                jqueryEventBus.one('globalTaskOperation', function(event, result) {
                    if (result == undefined)
                        return;
                    var method = result.method;
                    if (method == "save" && session_dom != undefined) 
                        UI.filter_task(event, session_dom);
                });                
            }
        });
        sessions.dom.find(".task-body").on("click", ".card-footer .right", function(e) {
            e.preventDefault(); //阻止按鈕默認動作
            e.stopPropagation();
        });
        sessions.dom.find(".task-body").on("click", ".card-footer .session_task_filter a", function(e) {
            e.preventDefault(); //阻止按鈕默認動作
            e.stopPropagation();
            $(this).toggleClass("active");
            self.filter_task(e);
        });

        sessions.dom.find(".task-body").on("click", ".card-footer .left", this.filter_task);
    
        $(".page-inner").on("click",".SWBoardlist .task-issue", function(e){
            //跳到對應Development的Session
            var session_dom = $(this).closest(".task-issue")
            var sessionid = session_dom.find(".sessionid").text();
            var recordid = session_dom.find(".recordid").text();
            window.open(`/devplat/sessions?recordid=${recordid}&menu_id=mi_${sessionid}#Requirements`, "_blank");
            
        })        
    }

    this.filter_task = function(e, dom) {
        e.preventDefault(); //阻止按鈕默認動作
        e.stopPropagation();            
        var session_dom = $(e.currentTarget).closest(".task-issue")
        if (dom != undefined)
            session_dom = dom;
        var sessionid = session_dom.find(".sessionid").text();
        var arr = sessionid.split("-");
        pid = arr[0];
        tid = arr[1];
        var self = this;
        if ($(e.currentTarget).hasClass("left") && dom == undefined) {
            session_dom.find(".session_task_filter a").removeClass("active");
        }
        if (session_dom.next().hasClass("task-collapse") && dom == undefined) {
            if ($(e.currentTarget).hasClass("left")) {
                var collapse_dom = session_dom.next();
                collapse_dom.collapse('hide')
                collapse_dom.remove();
                return;
            }
        }
        //判斷NF和F過濾，只能選擇一個
        if (session_dom.find(".session_task_filter a[taskprogress].active").length > 0 && session_dom.find(".session_task_filter a[progress='F'].active").length > 0 ) {
            //如果當前選中的F過濾
            if ($(e.currentTarget).attr("progress"))
                $(".session_task_filter a[taskprogress].active").removeClass("active");
            else if ($(e.currentTarget).attr("taskprogress"))
                $(".session_task_filter a[progress='F'].active").removeClass("active");
        }
        var progress_nf = session_dom.find(".session_task_filter a[taskprogress].active").length > 0;
        var progress_dom = session_dom.find(".session_task_filter a[progress].active");
        var progress_arr = []
        if(progress_dom.length > 0)
            for(let item of progress_dom)
                progress_arr.push($(item).attr("progress"))        
        var taskCategory_dom = session_dom.find(".session_task_filter a[taskcategory].active");
        var taskcategory_arr = []
        if(taskCategory_dom.length > 0)
            for(let item of taskCategory_dom)
                taskcategory_arr.push($(item).attr("taskcategory"))        
        var class_dom = session_dom.find(".session_task_filter a[classField].active");                
        var classOne = false;
        if (class_dom.length > 0)
            classOne = true;
        $.ajax({
            url:"/PMIS/session/search_task",
            data:{pid:pid,tid:tid,progress_or:progress_arr.join(","),progress_nf:progress_nf, taskcategory_or:taskcategory_arr.join(","),class_one:classOne},
            success:function(data){
                if(data.status) {
                    show_task(data.data, self)
                }
            }
        });

        function show_task(data, self) {
            var dom = $("#tasklist").clone();
            dom.removeAttr("id")
            var item = dom.find(".task-item").clone();
            dom.empty();
            for(task of data) {
                var local_item = item.clone();
                var local_task = task;
                if (Date.parse(local_task["planbdate"]) != null)
                    local_task["planbdate"] = Date.parse(local_task["planbdate"]).toString("yyyy-MM-dd");
                if (Date.parse(local_task["planedate"]) != null)
                    local_task["planedate"] = Date.parse(local_task["planedate"]).toString("yyyy-MM-dd");                
                dom.append(local_item.prop("outerHTML").render(local_task))
            }
            if (session_dom.next().hasClass("task-collapse")) {
                var scrollTop = session_dom.next(".task-collapse").scrollTop()                
                session_dom.next(".task-collapse").empty();
                session_dom.next(".task-collapse").append(dom.find(".task-item"));
                session_dom.next(".task-collapse").scrollTop(scrollTop);                
            }else {
                $(e.currentTarget).closest(".task-issue").after(dom);
                dom.show();
                dom.collapse();
            }
        }

        function show_task2(data, sefl) {
            var dom = $("#tasklist").clone();
            dom.removeAttr("id")
            var item = dom.find(".task-item").clone();
            dom.empty();
            for(task of data) {
                var local_item = item.clone();
                var local_task = task;
                if (Date.parse(local_task["planbdate"]) != null)
                    local_task["planbdate"] = Date.parse(local_task["planbdate"]).toString("yyyy-MM-dd");
                if (Date.parse(local_task["planedate"]) != null)
                    local_task["planedate"] = Date.parse(local_task["planedate"]).toString("yyyy-MM-dd");                
                dom.append(local_item.prop("outerHTML").render(local_task))
            }
            $("#exampleModal .modal-body").empty();
            $("#exampleModal .modal-body").append(dom);
            dom.show();
            $("#exampleModal").modal("show");
        }
        
        
    }    

}

var UI  = new PageUI();

var dashboard_demo = function() {
    return {
        init:function() {        
            var dp_index = UI.getDpFilterParams()
            var dpFilter = $($("input[name='dpFilter']")[dp_index]);
            var bdate = dpFilter.attr("data-start").replaceAll("-","");
            var edate = dpFilter.attr("data-end").replaceAll("-","");                
            var completionTasksOptions = {
                elementId: "completion-tasks",
                url: "/PMIS/looper_dashboard/getCompletionTasks",
                query: {"start": bdate,"end":edate},
                groups: { complete: {field:"task_qty",color:"#a99af0"}},
                labelField: "edatestr",
                sort:"edatestr"
            }

            ComponentClass.displayCompletionTasksControl(completionTasksOptions);
        }
    }
}();

$(function(){
    function bind_event() {
        function load_page() {
            var dp_index = UI.getDpFilterParams()
            var dpFilter = $($("input[name='dpFilter']")[dp_index]);
            var bdate = dpFilter.attr("data-start");
            var edate = dpFilter.attr("data-end");        
            window.location.href = "/looper?bdate={0}&edate={1}&dp={2}".format(bdate, edate, dp_index);
        }
    
        $("input[name='dpFilter']").on('change', function(){
            if ($(this).prop("checked"))
                load_page();
        });
    
        function update_task(element) {
            var pk = $(element).closest(".task-item").find(".pk").text();
            init_task(pk);
            jqueryEventBus.one('globalTaskOperation', function(event, result) {
                if (result == undefined)
                    return;
                var method = result.method;
                var task = result.data;
                if (method == "save") {
                    var local_item = $("#tasklist").find(".task-item").clone();
                    var local_task = task;
                    local_task['taskno'] = '{0}-{1}-{2}'.format(local_task.pid, parseInt(local_task.tid), parseInt(local_task.taskid));
                    if (Date.parse(local_task["planbdate"]) != null)
                        local_task["planbdate"] = Date.parse(local_task["planbdate"]).toString("yyyy-MM-dd");
                    if (Date.parse(local_task["planedate"]) != null)
                        local_task["planedate"] = Date.parse(local_task["planedate"]).toString("yyyy-MM-dd");                
                    var dom = local_item.prop("outerHTML").render(local_task);
                    $(element).replaceWith($(dom));
                } else if (method == "del") {
                    var session_dom = $(element).closest(".task-collapse").prev(".task-issue");
                    UI.filter_task(event, session_dom);
                }
            });            
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
            ".task-item"
        );  
        
        function update_todo_task(self) {
            var pk = $(self).attr("pk");
            init_task(pk);                
        }
    
        $(".page-inner").on(
            {
                dblclick:function(){
                    update_todo_task(this);
                },
                longpress:function() {
                    update_todo_task(this);
                }
            },
            "#today_tasks .todo"
        );        
    }

    UI.init();
    bind_event();
    dashboard_demo.init();
    $("#mi_1_1").addClass("has-active");
})