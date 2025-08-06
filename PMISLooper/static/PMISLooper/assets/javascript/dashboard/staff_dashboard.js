function PageUI() {
    this.all_user = undefined;
    this.today_task = undefined;
    this.schcategoryList = [];
    var username = get_username();
    var self = this;
    function getDay(date) {
        var day = date.toString("dd");
        if (day.substring(0,1) == "0")
            return day.substring(1,2);
        else
            return day;
    }
    function init_box_link() {
        var quarterly = "{0}-{1}".format(new Date().toString("yyyy"), Math.ceil((new Date().getMonth() + 1)/3));
        $("#goal_link").attr("href", `/looper/goal/overall/quarterly_goal?contact=${username}&period=${quarterly}`);
        $("#session_link").attr("href", `/looper/user/sessions?contact=${username}&period=${quarterly}`);
        $("#act_tasks_link").attr("href", `/looper/user/activites?contact=${username}`);
        $(".today_task_link").attr("href", `/looper/task/today_task?contact=${username}`);
    }
    function modify_boardlist_tmpl() {
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
    this.init = function() {
        modify_boardlist_tmpl();
        init_box_link();
        self.init_analysis_task_type();
        self.init_analysis_solution_type();
        self.init_analysis_new_task();
        self.init_show_new_task();
        self.init_tasks_performance();
        self.init_week_goal();
        //創建選擇聯繫人
        self.all_user = new SWCombobox('user',gettext('User'),window.CommonData.PartUserNames,username);
        self.all_user.setHorizontalDisplay(true)
        self.all_user.dom.find(".caption").addClass("mr-2").css({"font-size":"16px","font-weight":"600"});
        self.all_user.dom.children(".control").css("width","100px");
        self.all_user.dom.addClass("pl-0");
        $(".page-title-bar .all_user_container").append(self.all_user.dom);    
        //初始化日期選擇
        $("#dpToday").attr("data-start", Date.today().toString("yyyy-MM-dd"));
        $("#dpToday").attr("data-end", Date.today().toString("yyyy-MM-dd"));
        $("#dpToday").next("label").find(".text-dark").text("{0} {1}".format(Date.today().toString("MMM"), getDay(Date.today())))
        $("#dpYesterday").attr("data-start", Date.today().add(-1).day().toString("yyyy-MM-dd"));
        $("#dpYesterday").attr("data-end", Date.today().add(-1).day().toString("yyyy-MM-dd"));
        $("#dpYesterday").next("label").find(".text-dark").text("{0} {1}".format(Date.today().add(-1).day().toString("MMM"), 
        getDay(Date.today().add(-1).day())));
        $("#dpWeek").attr("data-start", Date.monday().toString("yyyy-MM-dd"));
        $("#dpWeek").attr("data-end", Date.monday().add(6).day().toString("yyyy-MM-dd"));
        $("#dpWeek").next("label").find(".text-dark").text("{0} {1}-{2}".format(Date.monday().toString("MMM"), 
        getDay(Date.monday()), getDay(Date.monday().add(6).day())));
        $("#dpMonth").attr("data-start", Date.today().moveToFirstDayOfMonth().toString("yyyy-MM-dd"));
        $("#dpMonth").attr("data-end", Date.today().moveToLastDayOfMonth().toString("yyyy-MM-dd"));
        $("#dpMonth").next("label").find(".text-dark").text("{0} {1}-{2}".format(Date.today().moveToFirstDayOfMonth().toString("MMM"),         
        getDay(Date.today().moveToFirstDayOfMonth()), getDay(Date.today().moveToLastDayOfMonth())));
        var quarter = self.get_quarterly_date(Date.today());
        $("#dpQuarter").attr("data-start", quarter[0].toString("yyyy-MM-dd"))
        $("#dpQuarter").attr("data-end", quarter[1].toString("yyyy-MM-dd"))
        $("#dpQuarter").next("label").find(".text-dark").text("{0}-{1}".format(quarter[0].toString("MMM"), quarter[1].toString("MMM")));
        $("#dpYear").attr("data-start", "{0}-01-01".format(Date.today().toString("yyyy")));
        $("#dpYear").attr("data-end", "{0}-12-31".format(Date.today().toString("yyyy")));
        $("#dpYear").next("label").find(".text-dark").text("{0}".format(Date.today().moveToFirstDayOfMonth().toString("yyyy")));
        //初始化上個季度
        var last_quarter = self.get_last_quartely_date(Date.today());
        $("#ltQuarter").attr("data-start", last_quarter[0].toString("yyyy-MM-dd"))
        $("#ltQuarter").attr("data-end", last_quarter[1].toString("yyyy-MM-dd"))
        $("#ltQuarter").next("label").find(".text-dark").text("{0}-{1}".format(last_quarter[0].toString("MMM"), last_quarter[1].toString("MMM")));
        var dp_index = getParamFromUrl("dp");
        if (dp_index) {
            $($("input[name='dpFilter']")[dp_index]).prop("checked", true);
            $(".dpFilter_dropdown span").text($($("input[name='dpFilter']")[dp_index]).next("label").find("span:eq(0)").text());
        }
        self.init_todo_list(username);
        self.init_active_session(username);
        //初始化project的url
        var recordids = encodeURIComponent(window.projects.join(","))
        var recordid_params = ""
        if (recordids != "")
            recordid_params = `&recordids=${recordids}`
        $(".metric-row .metric-projects").attr("href", "/devplat/project/overview?contact={0}{1}"
            .format(username, recordid_params));
    }

    this.get_quarterly_date = function(currentDate) {
        var quarter = Math.ceil((currentDate.getMonth() + 1)/3)
        var qbdate = new Date(currentDate.getFullYear(), 3 * quarter - 3, 1);    
        var month = 3 * quarter
        var remaining = parseInt(month / 12)
        var qedate = new Date(currentDate.getFullYear() + remaining, month % 12, 1).addDays(-1);    
        return [qbdate, qedate]
    }

    this.get_last_quartely_date = function(currentDate) {
        var lastQuarterFirstDay = new Date(currentDate.getFullYear() , currentDate.getMonth() - 3 , 1);
        return self.get_quarterly_date(lastQuarterFirstDay)
    }

    this.init_todo_list = function(username) {
        var group_title = `<div><span style="font-size:16px">[[group_type]]</span></div>`;
        var subtitle_tmpl = `<label class="custom-control custom-checkbox">
                            <input type="checkbox" class="custom-control-input" [[input_checked]]>
                            <span class="custom-control-label pk_label" pk="[[inc_id]]" outstanding="[[outstanding]]" todayt="[[todayt]]" progress="[[progress]]">
                            [[task_order_num_dom]][[task]] ([[task_mark]]) 
                            </span>
                        </label>`

        self.today_task = new SWTodolist("Today's Tasks", "/PMIS/task/get_today_fixed_tasks?style=group&contact="+username, ['group_order'], group_title, subtitle_tmpl,undefined);
        self.today_task.dom.find("")
        $("#today_tasks").append(self.today_task.todo_dom);
        var processors_function = function(item){
            if (item.hasOwnProperty("schcategory") && self.schcategoryList.indexOf(`${item.group_order}-${item.schcategory}`) == -1) {
                self.schcategoryList.push(`${item.group_order}-${item.schcategory}`);
                this.todo_dom.append(`<div class="todo-header todo-subheader ml-2 py-0"><div><span style="font-size:14px">${item.schcategory}</span></div></div>`)
            }
            var task_mark = "Sch Priority:<span style='font-size:16px;margin-left:2px'>{0}</span> Today Priority:<span style='font-size:16px;margin-left:2px'>{1}</span>"
            task_mark = task_mark.format((item.schpriority != null ? item.schpriority : "0"), (item.schprioritysp != null ? item.schprioritysp : "0"))
            if (self.today_task.datasource.indexOf("style=single") != -1) {
                task_mark = "Session Priority:<span style='font-size:16px;margin-left:2px'>{0}</span> Today Priority:<span style='font-size:16px;margin-left:2px'>{1}</span>"                
                task_mark = task_mark.format((item.sessionpriority != null ? item.sessionpriority : "0"), (item.schprioritysp != null ? item.schprioritysp : "0"))
            }
            
            if (item.class_field == 1)
                task_mark += " Class:<span style='font-size:16px;margin-left:2px'>1</span>"
            item['task_mark'] = task_mark;
            if (item.progress == "C" || item.progress == "F")
                item['input_checked'] = "checked";
            else
                item['input_checked'] = "";            
            var task_order_num_dom = '';
            if (item.hasOwnProperty("task_order_num"))
                task_order_num_dom = `<span class="tile tile-sm task_order_num mr-2">{0}</span>`.format(item['task_order_num']);
            item['task_order_num_dom'] = task_order_num_dom;
        }
        var card_expansion_list = function (curitem, nextitem) {
            if (item.hasOwnProperty("parent_group_type") && (nextitem == undefined || nextitem.parent_group_type != curitem.parent_group_type)) {
                var group_type = $(this.todo_dom.children(".todo-header:not(.todo-subheader)")[0]).find("span").text();
                var prefixId = curitem.parent_group_type.replaceAll(" ","").replaceAll("'","");
                if (group_type == curitem.parent_group_type)
                    this.todo_dom.children(".todo-header:not(.todo-subheader)").remove();
                createExpansionCard(`${prefixId}Group`, `${prefixId}GroupCollapse`, curitem.parent_group_type, this.todo_dom.children('.todo,.todo-header'), true);  
            }   
        }        
        self.today_task.handle_after_append_todo = card_expansion_list;
        self.today_task.processors_function = processors_function;  
    }

    var createExpansionCard = function (groupID, collapseID, groupName, taskList, insertBeforeLast) {
        var expansionCard_tmpl = `<div class="card card-expansion-item expanded expansionCard">
            <div class="card-header" id="${groupID}">
                <button class="btn btn-reset d-flex justify-content-between prevent-default text-primary" data-toggle="collapse"
                    data-target="#${collapseID}" aria-expanded="true" aria-controls="${collapseID}">
                    <span class="collapse-indicator"><i class="fa fa-fw fa-caret-right mr-2"></i></span>
                    <span>${groupName}</span>
                </button>
            </div>
            <div id="${collapseID}" class="collapse show" aria-labelledby="${groupID}">
                <div class="card-body py-0"></div>
            </div>
        </div>`;

        if (insertBeforeLast) {
            $(self.today_task.todo_dom).children(":last").before(expansionCard_tmpl);
        } else {
            $(self.today_task.todo_dom).append(expansionCard_tmpl);
        }

        $("#" + collapseID).find(".card-body").append(taskList);
    };

 

    this.init_active_session = function(username) {
        var header_title = `<span class="recordid">[[recordid]]</span><span class="ml-2 sessionid">[[sessionid]]</span>`;
        var header_sub_title = `<h6 class="item-header-subtitle card-subtitle text-dark">
            <div class="ppsp"><span class="">[[planbdate]] / [[planedate]]</span><span class="ml-2 badge badge-subtle badge-dark font-size-lg">[[progress]]</span>
            <span class="ml-2 badge badge-subtle badge-dark font-size-lg milestone_activiites" style="cursor: pointer;">
                <i class="fas fa-location-arrow"></i>
            </span>

            <span class="ml-2 badge badge-subtle badge-dark font-size-lg gantt_chart" style="cursor: pointer;">
                <svg class="ganttIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M512 416l0-64c0-35.3-28.7-64-64-64L64 288c-35.3 0-64 28.7-64 64l0 64c0 35.3 28.7 64 64 64l384 0c35.3 0 64-28.7 64-64zM64 160l0-64 144 0 16 0 0 64L64 160zm224 0l0-64 80 0c8.8 0 16 7.2 16 16l0 16-38.1 0c-21.4 0-32.1 25.9-17 41L399 239c9.4 9.4 24.6 9.4 33.9 0L503 169c15.1-15.1 4.4-41-17-41L448 128l0-16c0-44.2-35.8-80-80-80L224 32l-16 0L64 32C28.7 32 0 60.7 0 96l0 64c0 35.3 28.7 64 64 64l160 0c35.3 0 64-28.7 64-64z"/></svg>
            </span>

            </div>
            </h6>`;
        var quarterly = "{0}-{1}".format(Date.today().format('yyyy'), parseInt(Date.today().getMonth()/3) + 1);
        var sessions = new SWBoardlist(gettext("Active Sessions"), "/PMIS/session/session_list?allcontact={0}&period={1}".format(username, quarterly),
        "", header_title, header_sub_title,"sdesp","taskc","taskqty");
        sessions.processors_function = function(item){
            if (Date.parse(item["planbdate"]) != null)
                item["planbdate"] = Date.parse(item["planbdate"]).toString("yyyy-MM-dd");
            if (Date.parse(item["planedate"]) != null)
                item["planedate"] = Date.parse(item["planedate"]).toString("yyyy-MM-dd");
            
        }
        $("#Active_Sessions").append(sessions.dom);
        sessions.dom.find(".task-header").addClass("card-header");
        var contact = new SWCombobox("contact", gettext("Contact"), window.CommonData.PartUserNames)
        contact.input_dom.attr("data-live-search", "true");
        var all_contact = new SWCombobox("allcontact", gettext("All Contacts"), window.CommonData.PartUserNames)
        all_contact.input_dom.attr("data-live-search", "true");
        var recordid = new SWCombobox("recordid", gettext("RecordID"), "/PMIS/subproject/get_all_recordid",undefined, 'recordid','recordid')
        recordid.input_dom.attr("data-live-search", "true");
        var period = new SWCombobox("period", gettext("Period"), "/PMIS/goalmaster/get_all_period")
        var layout = `<div class="row">
                    <div class="col-6"></div> 
                    <div class="col-6"></div> 
                    </div>`
        var first_col = $(layout).clone();
        first_col.children("div").eq(0).append(contact.dom);
        first_col.children("div").eq(1).append(all_contact.dom);
        var second_col = $(layout).clone();
        second_col.children("div").eq(0).append(recordid.dom);
        second_col.children("div").eq(1).append(period.dom);
        sessions.filter_content.append(first_col);
        sessions.filter_content.append(second_col); 
        $(".filter .search-content").find(".card-title").text(gettext("Search"));
        $(".filter .search-content").find(".cancel").text(gettext("Cancel"));
        $(".filter .search-content").find(".search").text(gettext("Search"));
        
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
        $(".page-inner").on("click",".SWBoardlist .task-issue .milestone_activiites", function(e){
            //xmm新增跳轉到重點項目的功能
            e.stopPropagation();
            var session_dom = $(this).closest(".task-issue")
            var sessionid = session_dom.find(".sessionid").text();
            var recordid = session_dom.find(".recordid").text();
            var user = get_username();
            window.open(`/looper/user/top5_projects?contact=${user}&recordid=${recordid}&sessions=${sessionid}`, "_blank");
        })        
        $(".page-inner").on("click",".SWBoardlist .task-issue .gantt_chart", function(e){
            //syl新增跳轉到甘特圖的功能
            e.stopPropagation();
            var session_dom = $(this).closest(".task-issue")
            var recordid = session_dom.find(".recordid").text();
            var sessionid = session_dom.find(".sessionid").text();
            // window.open(`/project/project_gantt_modal?recordid=${recordid}&sessionid=${sessionid}`, "_blank"); //甘特圖視圖
            $('#pciframe').attr('src', `/project/project_gantt_modal?recordid=${recordid}&sessionid=${sessionid}`); //打開甘特圖彈窗(只看對應Session)
            $("#session_gantt").modal("show");
        })   
        // 當模態框隱藏時，清空iframe的src屬性
        $('#session_gantt').on('hidden.bs.modal', function() {
            $('#pciframe').attr('src', '');
        });    
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
    }
    this.getDpFilterParams = function() {
        var dpFilter = $("input[name='dpFilter'][checked]");        
        var result_index = 3;
        $("input[name='dpFilter']").each(function(index, el){
            if ($(el).prop("checked")) {
                result_index = index;
                return false;
            }
        });
        return result_index;
    }
    this.get_params = function() {
        var username = get_username();
        var bdate = getParamFromUrl("bdate");
        var edate = getParamFromUrl("edate");
        //默認本周
        if (bdate == undefined) {
            bdate = Date.monday().toString("yyyy-MM-dd");
            edate = Date.monday().add(6).day().toString("yyyy-MM-dd");
        }
        return [username,bdate,edate]        
    }
    this.init_analysis_task_type = function() {
        function display(data) {
            var container = $(".analysis_container .task_type");
            container.empty();
            var templ = `<div class="list-group-item"><span class="oi oi-circle-check text-primary mr-2"></span>[[desc]]([[qty]])</div>`;
            container.append(`<div class="list-group-header">` + gettext("Task Type") + ` </div><div class="task_type_list"></div>`);
            var templ_wrap = $(".analysis_container .task_type .task_type_list");
            for(var item of data) {
                templ_wrap.append(templ.render({desc:"{0}-{1}".format(item.tasktypedesc, item.subtasktypedesc),qty:item.qty}));
            }
        }
        var param = self.get_params();
        var url = "/looper/dashboard/analysis_task_type"
        var data = {username:param[0], bdate:param[1], edate:param[2]}
        $.get(url, data, function(result){
            if (result.status) {
                display(result.data);
            }else {
                display([]);
            }
        });
    }

    this.init_analysis_new_task = function() {
        var param = self.get_params();
        var url = "/looper/dashboard/analysis_new_task"
        var data = {username:param[0], bdate:param[1], edate:param[2]}        
        $.get(url, data, function(result){
            if (result.status) {
                $("#act_new_tasks .value").text(result.data);
            }else {
                $("#act_new_tasks .value").text(0);
            }
        });
    }

    this.init_show_new_task = function() {
        /**
        var url = "/looper/dashboard/analysis_new_task?search_task=true"
        var param = self.get_params();
        var data = {username:param[0], bdate:param[1], edate:param[2]}        
        */
        var param = self.get_params();
        $("#act_new_tasks").on("click", function(e){
            e.preventDefault();
            window.open(`/looper/task/enquiry?newtask=true&username=${param[0]}`, "_blank");
            /**
            $.get(url, data, function(result){
                if (result.status) {
                    window.sessionStorage.setItem("task_enquiry_data", JSON.stringify(result.data));
                }else {
                    window.sessionStorage.setItem("task_enquiry_data", JSON.stringify([]));
                }
                window.open(`/looper/task/enquiry?newtask=true&username=${param[0]}`, "_blank");
            });
            */                
        });
    }

    this.init_analysis_solution_type = function() {
        function display(data) {
            var container = $(".analysis_container .solution_type");
            container.empty();
            var templ = `<li class="list-group-item"><span class="oi oi-fire text-primary mr-2" data-glyph="icon-name"></span>[[desc]]([[qty]])</li>`;
            container.append(`<li class="list-group-header">` + gettext("Solution Type") + `</li><div class="solution_type_list"></div>`);
            var templ_sol_wrap = $(".analysis_container .solution_type .solution_type_list");
            for(var item of data) {
                templ_sol_wrap.append(templ.render({desc:item.mindMaplabel,qty:item.qty}));
            }
        }
        var param = self.get_params();
        var url = "/looper/dashboard/analysis_solution_type"
        var data = {username:param[0], bdate:param[1], edate:param[2]}
        $.get(url, data, function(result){
            if (result.status) {
                display(result.data);
            }else {
                display([]);
            }
        });
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

    this.init_week_goal = function() {
        var all_tmpl = new TemplateWrapper().tmpls;        
        function desc_render(data) {
            var html = "";
            var lines = data.goaldesc.replace(/\r\n/g, "\r").replace(/\n/g, "\r").split(/\r/);            
            for(var line of lines) {
                
                html += `<li class="d-flex mb-2"><span>${line}</span></li>\r\n`;
            }
            return html;    
        }
        function show_task(container, data) {
            var week_tmpl = $(container).data("tmpl");
            var tasks = data.tasks_array;
            var task_tmpl = all_tmpl["week_task"];
            week_tmpl.solt['tasks'].empty();
            tasks.forEach(function(item,index){
                if (Date.parse(item["planbdate"]) != null)
                    item["planbdate"] = Date.parse(item["planbdate"]).toString("yyyy-MM-dd");
                if (Date.parse(item["planedate"]) != null)
                    item["planedate"] = Date.parse(item["planedate"]).toString("yyyy-MM-dd");
                week_tmpl.solt['tasks'].append(task_tmpl.render(item));
            });            
        }
        function get_week_title(index) {
            if (index == 0)
                return gettext("Last Week");
            else if (index == 1)
                return gettext("This Week");
            else
                return gettext("Next Week");
        }
        var tmpl = all_tmpl['week_goal'];        
        var tmpl_params = {solt:{desc:desc_render},};
        tmpl.init(tmpl_params);
        var container = $(".week_goal .goals");
        var url = '/PMIS/goal/overall/get_week_goal';
        var param = self.get_params();
        var data = {contact:param[0]}        
        $.get(url, data).then((result)=>{
            if (result.status) {
                result.data.forEach(function(item,index){
                    var local_item = $.extend({}, item);
                    local_item["week_title"] = get_week_title(local_item.week_num);
                    if (local_item.total_qty == 0)
                        local_item["finish_progress"] = 0;
                    else
                        local_item["finish_progress"] = (local_item["finish_qty"]/local_item['total_qty']).toFixed(2) * 100;
                    var week_dom = tmpl.render(local_item)
                    show_task(week_dom, item);
                    week_dom.find(".ribbon-content .task-inner li").on("click", function(){
                        window.show_week_tasks(item);                        
                    })
                    container.append(week_dom);
                });
            }
        });
    }
}

var UI  = new PageUI(); 

function bind_event() {
    function load_page() {
        var username = UI.all_user.input_dom.val();
        var dp_index = UI.getDpFilterParams()
        var dpFilter = $($("input[name='dpFilter']")[dp_index]);
        var bdate = dpFilter.attr("data-start");
        var edate = dpFilter.attr("data-end");        
        window.location.href = "/looper/staff_dashboard?username={0}&bdate={1}&edate={2}&dp={3}".format(username, bdate, edate, dp_index);
    }
    
    UI.all_user.input_dom.on("change", load_page)

    $("input[name='dpFilter']").on('change', function(){
        if ($(this).prop("checked"))
            load_page();
    });

    $(".activeTaskNav .nav-link").on("click", function(e){
        var username = UI.all_user.input_dom.val();
        var styleName = $(this).attr("show_style");
        var url = `/PMIS/task/get_today_fixed_tasks?style=${styleName}&contact=${username}`;
        UI.schcategoryList.length = 0;
        UI.today_task.reload(url);        
    })

    function update_task(self) {
        var pk = $(self).find(".pk_label").attr("pk");
        init_task(pk);
        jqueryEventBus.one('globalTaskOperation', function(event, result) {
            if (result == undefined)
                return;
            var method = result.method;
            if (method == "save" || method == "del") {
                UI.schcategoryList.length = 0;
                UI.today_task.reload();
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
        "#today_tasks .todo"
    );    
}

var dashboard_demo = function() {
    return {
        init:function() {
            var username = get_username();
            var dp_index = UI.getDpFilterParams()
            var dpFilter = $($("input[name='dpFilter']")[dp_index]);
            var bdate = dpFilter.attr("data-start").replaceAll("-","");
            var edate = dpFilter.attr("data-end").replaceAll("-","");                
            var completionTasksOptions = {
                elementId: "completion-tasks",
                url: "/PMIS/looper_dashboard/getCompletionTasks",
                // data:window.completion_tasks,
                query: {"start": bdate,"end":edate, contact:username },
                groups: { complete: {field:"task_qty", color:"#a99af0"}},
                labelField: "edatestr",
                sort:"edatestr"
            }

            ComponentClass.displayCompletionTasksControl(completionTasksOptions);
        }
    }
}();

var BonusUI = function() {
    var self = this;
    this.init = function() {
        var username = get_username();
        var bdate = getParamFromUrl("bdate");
        var edate = getParamFromUrl("edate");
        //默認本周
        if (bdate == undefined) {
            bdate = Date.monday().toString("yyyy-MM-dd");
            edate = Date.monday().add(6).day().toString("yyyy-MM-dd");
        }
        var arr = self.get_quarterly_date(new Date());
        var qbdate = arr[0].toString("yyyy-MM-dd");
        var qedate = arr[1].toString("yyyy-MM-dd");
        this.get_score(username, qbdate, qedate).then((value)=>{
            if (value != null) {
                var score = value.LookupScore;
                var scoreAvg = value.ScoreAvg;
                var suggAvg = value.SuggAvg;
                $("#bonus_target_score .metric-value").text(value.SimulateScore);
                $("#bonus_simulate_score .metric-value").text(value.SimulatePerMth);
                if (scoreAvg < suggAvg) {
                    $("#bonus_simulate_score").removeClass("info").addClass("warn");
                }else {
                    $("#bonus_simulate_score").removeClass("warn").addClass("info");
                }             
            }else {
                $("#bonus_simulate_score").removeClass("warn").removeClass("info");
                $("#bonus_simulate_score .metric-value").text("error");
            }
        });
        this.get_score(username, bdate, edate).then((value)=>{
            if (value != null) {
                var score = value.LookupScore;
                var scoreAvg = value.ScoreAvg;
                var suggAvg = value.SuggAvg;
                $("#bonus_score .metric-value").text(score);
                if (scoreAvg < suggAvg) {
                    $("#bonus_score").removeClass("info").addClass("warn");
                }else {
                    $("#bonus_score").removeClass("warn").addClass("info");
                }            
            }else {
                if(Date.today().toString("yyyyMMdd") == Date.monday().toString("yyyyMMdd")) {
                    $("#bonus_score").removeClass("warn").removeClass("info");
                    $("#bonus_score .metric-value").text("0");    
                }else {
                    $("#bonus_score").removeClass("warn").removeClass("info");
                    $("#bonus_score .metric-value").text("error");    
                }
            } 
        });
    }
    this.get_quarterly_date = function(currentDate) {
        var quarter = Math.ceil((currentDate.getMonth() + 1)/3)
        var qbdate = new Date(currentDate.getFullYear(), 3 * quarter - 3, 1);    
        var month = 3 * quarter
        var remaining = parseInt(month / 12)
        var qedate = new Date(currentDate.getFullYear() + remaining, month % 12, 1).addDays(-1);    
        return [qbdate, qedate]
    }

    this.get_score = function(contact, bdate, edate) {
        var quarterly_data = this.get_quarterly_date(new Date());
        var quarterbegin = quarterly_data[0].toString("yyyy-MM-dd");
        var quarterend = quarterly_data[1].toString("yyyy-MM-dd");
        return new Promise((resolve, reject)=>{
            var url = `/bonus/bonus_analysis?contact=${contact}&edatefrom=${bdate}&edateto=${edate}&quarterbegin=${quarterbegin}&quarterend=${quarterend}`;
            $.get(url ,function(data){
                if (data.errorMessage != "") {
                    resolve(null);
                }else {
                    resolve(data.bonusResult);
                }
            })
        })
    }
}

$(function(){
    var bonusUI = new BonusUI()
    bonusUI.init();
    UI.init();
    bind_event();
    dashboard_demo.init();
    
    var bdate = getParamFromUrl("bdate");
    var edate = getParamFromUrl("edate");
    //默認本周
    if (bdate == undefined) {
        bdate = Date.monday().toString("yyyy-MM-dd");
        edate = Date.monday().add(6).day().toString("yyyy-MM-dd");
    }
    $('#new_technicals').on('click',()=>{
        window.open("/PMIS/newOpportunity?bdate="+bdate+'&edate='+edate)
    })
    $('#unsolved_topics').on('click',()=>{
        window.open("http://121.13.252.164:8010/Forum/topic/unsolved?bdate="+bdate+'&edate='+edate)
    })
    //所有數據加載完成，才執行自動刷新
    $(window).on('load', function(){
        setInterval(() => {
            UI.init_analysis_new_task();
        }, 10000);
    })
    /**
    function checkWinExists(pages_targets) {
        return new Promise((resolve, reject)=>{
            var result = []
            function handleMessage(event) {
                var data = event.data;
                if (data.action === 'getWinResult') {
                    result.push(data); //有該頁面則添加到result中
                }
            }
            winChannel.addEventListener("message", handleMessage);
            //在300毫秒內取得指定頁面
            setTimeout(() => {
                winChannel.removeEventListener("message", handleMessage);
                resolve(result);
            }, 1000);
            //發消息到所有頁面
            winChannel.postMessage({action:"getWin"});
        })
    }
    var pages_targets = ['goal','project','mindmap','meeting']
    if(!SWApp.os.isMobile && getParamFromUrl("username") == undefined)
    checkWinExists(pages_targets).then((targetsInfo)=>{
        var exists_targets = targetsInfo.map(x=>x.target);
        var noexists_targets = [];
        var newWindow = undefined;
        for(const target of pages_targets) {
            if (exists_targets.indexOf(target) == -1) {
                noexists_targets.push(target);
                if (target == 'goal') {
                    setTimeout(() => {
                        newWindow = window.open($("#goal_link").attr("href"),"goal");
                    });
                }else if (target == 'project') {
                    var username = get_username();
                    var recordids = encodeURIComponent(window.projects.join(","))
                    var recordid_params = ""
                    if (recordids != "")
                        recordid_params = `&recordids=${recordids}`
                    setTimeout(() => {
                        newWindow =window.open("/devplat/project/overview?contact={0}{1}".format(username, recordid_params), "project")
                    });
                }else if (target == "mindmap") {
                    setTimeout(()=>{
                        newWindow = window.open($("#mindmap_link").attr("href"), "mindmap");
                    })
                }
                else if (target == 'meeting') {
                    setTimeout(() => {
                        newWindow = window.open("/looper/metting/newMeeting","meeting");
                    });
                }
            }else {
                window.focus();
            }
        }
        //如果有沒有打開的固定窗口，則需要從該新窗口跳轉回主頁面
        if (noexists_targets.length>0) {
            var interval = setInterval(() => {
                if (newWindow.winUUID != undefined) {
                    setTimeout(() => {
                        winChannel.postMessage({action:"goHome", target:newWindow.name});    
                    }, 200);
                    clearInterval(interval);
                }
            }, 200);
        }
        //清除窗口
        var closeWindow = [];
        var leaveTargets = [];
        var leaveUrlPathNames = [];
        for(var info of targetsInfo) {
            var tempTarget = info.target;
            if (tempTarget != "") {
                if(leaveTargets.indexOf(tempTarget) == -1 && !(window.winUUID != info.winUUID && tempTarget == "staff_dashboard"))
                    leaveTargets.push(tempTarget)
                else
                    closeWindow.push(info.winUUID);
            }else {
                if (leaveUrlPathNames.indexOf(info.urlPathName) == -1)
                    leaveUrlPathNames.push(info.urlPathName);
                else
                    closeWindow.push(info.winUUID);
            }
        }
        for(var uuid of closeWindow) {
            winChannel.postMessage({action:"closeWin", uuid:uuid});
        }
    });*/
});