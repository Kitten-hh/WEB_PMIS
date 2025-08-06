var tables = {
    tasks:{id:"session_tasks_table",table:undefined, datatable:undefined},
}
var session_id = ''
var hoperation_type = {};
$(function () {
    console.log((new Date()).toString("HH:mm:ss"))    
    //用戶下拉框組件, 和recordid
    var user = get_username()
    $(".activites_header .username").text(user);
    var all_user = new SWCombobox('user',gettext('User'),window.CommonData.PartUserNames, user);
    $("#SWCombobox select.control").attr("data-live-search", "true");
    var recordid = new SWCombobox("recordid_select", gettext("RecordID"), [],undefined, 'recordid','recordid')
    $("#SWCombobox select.control").removeAttr("data-live-search");
    //子標題
    var child_info = `<p class="mb-0 timeline-date progress[[progress]] text-dark font-weight-normal" inc_id="[[inc_id]]">[[pid]]-[[tid]]-[[taskid]]</p>`
    //詳細內容
    var daily_tmpl = `<p class="font-weight-bolder progress[[progress]] text-dark mb-0 caption"><i class="fas fa-bullhorn text-primary mr-2"></i>[[task]]</p>
    <div class="mustFinish[[taskcategory]]" inc_id="[[inc_id]]">
    <span class="mr-3 text-dark progress[[progress]]"><i class="far fa-calendar-alt mr-2"></i>[[planedate]]</span>
    <span class="mr-3 text-dark progress[[progress]]"><i class="far fa-list-alt mr-2"></i>[[contact]]</span>
    <span class="mr-3 text-dark progress[[progress]]"><i class="far fa-file mr-2"></i>[[progress]]</span>
    <span class="text-dark progress[[progress]]"><i class="far fa-list-alt mr-2"></i>[[taskcategory_desc]]</span>
    </div>`    
    all_user.setHorizontalDisplay(true);
    recordid.setHorizontalDisplay(true);
    $(".page-inner .userlist").append(all_user.dom);
    $(".page-inner .userlist").append(recordid.dom);
    var recordidDOM = $(".page-inner .userlist").find('div[name="recordid_select"] select');
    //獲取summary template
    var summary_html = $("#summary_template").prop("innerHTML");
    var title_html = $("#title_template").prop("innerHTML");
    //獲取對應聯繫人優先級最高的5個Project及其任務
    function get_Projects(user, currentRecordid=undefined){
        var url = `/en/looper/user/AnalyseProjects?contact=${user}`;
        if (currentRecordid)
            url += `&recordid=${currentRecordid}`
        //移除原有的TopProject框
        $('#projectList').find('.top_wrap').remove()
        //獲取對應用戶前五的Project和其任務數據
        $.get(url, function(result){
            if (result.status){
                var projects = result.data;
                console.log((new Date()).toString("HH:mm:ss"))
                Object.entries(projects).forEach(([strkey,item], index)=>{
                    var strid = 'top'+(index+1)
                    var strhtml = `<div class="col-12 col-xl-6 col-xxl-4 top_wrap" id="[[id]]"></div>`.replace('[[id]]',strid);
                    $("#projectList").append(strhtml);                    
                    show_timeline(item,index).then((data)=>{
                        $("#"+data.strid).append(data.dom);                        
                    });
                });
                var recordids = result.recordids;
                recordidDOM.empty();
                var tempalte = `<option value></option>`
                for (let recordid of recordids)
                    if (currentRecordid == recordid)
                        tempalte += `<option selected value="${recordid}">${recordid}</option>`
                    else
                        tempalte += `<option value="${recordid}">${recordid}</option>`
                recordidDOM.html(tempalte);
                recordidDOM.selectpicker('refresh');
            }
        });  
    }

    function show_timeline(item, index) {
        return new Promise((resolve, reject)=>{
            setTimeout(() => {
                var tasks_bak = JSON.parse(JSON.stringify(item.tasks));
                var users = new Set()
                var sessions = [];
                for (var task of item.tasks) {
                    if (task.taskcategory == 'MH')
                        task['taskcategory_desc'] = 'Must Have'
                    else
                        task['taskcategory_desc'] = 'Must Finish'
                    if (task.contact != null && task.contact.trim() != "")
                        users.add(task.contact)
                    if (sessions.filter((a)=>a.id == task.sessionid).length == 0) {
                        sessions.push({id:task.sessionid, desp:task.sdesp, parent:task.sparent});    
                    }
                }
                users = Array.from(users).sort();
                var sindex = index+1
                var strid = 'top'+sindex
                var goal_num = get_goal_num(item.project.goaldesc)
                if (goal_num == -1)
                    goal_num = sindex
                //SWTimeline2組件的容器
                var tasks = analysis_tasks(item.tasks)
                var top = new SWTimeline2('G'+goal_num+'.'+item.project.projectname+'(' + item.project.recordid + ')', tasks, "planedate", child_info, daily_tmpl, "planedate asc");
                top.dom.children(".card-header").html(title_html.render({title:'G'+goal_num+'.'+item.project.projectname+'(' + item.project.recordid + ')', goaldesc:item.project.goaldesc, recordid:item.project.recordid}));
                top.dom.children(".card-header").find(".filter_goal").data("data", item);
                top.dom.find(".example-preview").data("recordid", item.project.recordid);
                for (var user of users)
                    top.dom.children(".card-header").find(".filter_goal .dropdown-menu")
                    .append(`<a href="#" class="dropdown-item pl-4 user" filter_type="user" name="${user}">${user}</a>`);
                top.dom.children(".card-header").find(".filter_goal .dropdown-menu")
                    .append(`<a href="#" class="dropdown-item pl-4 user" filter_type="user" name="all">All</a>`);
                top.dom.data("component", top);
                top.dom.data("tasks", tasks_bak);                
                load_filter_session(top.dom.find(".filter_session .session_treegrid"), sessions);
                load_sub_must_have(tasks, top, strid);
                top.dom.append(summary_html.render(item.summary)); 
                top.dom.find('.mustFinishMF').closest(".timeline-item").addClass('priorityTask');
                top.dom.find("span.tile").removeClass("bg-primary");
                top.dom.find("span.tile i").remove();
                top.dom.find("span.int").removeClass("d-none");            
                resolve({strid:strid, dom:top.dom})
                //SWTimeline2組件下的統計數據顯示模塊                    
            });
        })
    }
    function load_sub_must_have(tasks, component, index) {
        var medias = []
        for (var i=0; i < tasks.length; i++) {
            medias.push(component.dom.find(`.mustFinishMF[inc_id='${tasks[i].inc_id}']`).closest(".timeline-item"));
        }
        for (var i=0; i < tasks.length; i++) {
            var sub_items = tasks[i].sub_list;
            if (sub_items) {
                var tempTimeLine = new SWTimeline2('demo', sub_items, "planedate", child_info, daily_tmpl, "planedate asc");
                tempTimeLine.dom.find(".section-block").addClass("ml-4 mt-2");
                $(medias[i]).after(tempTimeLine.dom.find(".example-preview").html());  
                
                if($(medias[i]).next().length>0 && $(medias[i]).next().children().length>0) {
                    $(medias[i]).parent().addClass("card-expansion-item expanded");
                    $(medias[i]).next().wrap(`<div id="collapse-`+ index + `-` + i + `" class="collapse show"></div>`);
                    $(medias[i]).append(`<button class="btn btn-reset px-2" data-toggle="collapse" data-target="#collapse-`+ index + `-` + i + `" aria-expanded="true" aria-controls="collapse_session"><span class="collapse-indicator"><i class="fa fa-fw fa-chevron-down"></i></span></button>`);
                }
            }
        }
    }
    function analysis_tasks(tasks) {
        function getTaskNo(task) {
            return '{0}-{1}-{2}'.format(task.pid, parseInt(task.tid), parseInt(task.taskid))            
        }
        var master = []
        var exists_tasknos = []
        for (var task of tasks) {
            if (task.taskcategory == 'MF') {
                task.sub_list = tasks.filter(x=>x.taskcategory == 'MH' && x.udf08 == getTaskNo(task))
                exists_tasknos.push(getTaskNo(task))
                task.sub_list.map(x=>exists_tasknos.push(getTaskNo(x)))
                master.push(task);
            }
        }
        var not_master_task = tasks.filter(x=>x.taskcategory == 'MH' && exists_tasknos.indexOf(getTaskNo(x)) == -1);
        master.push(...not_master_task);
        return master;
    }

    function get_goal_num(goal_desc) {
        if (/^\s*G(\d+)/i.test(goal_desc)) {
            return  parseInt(goal_desc.match(/^\s*G(\d+)/i)[1])
        }else
            return -1;
    }

    function filter_goal(dom,data, taskCategoryFilter, userFilter, restore_scroll=false) {
        var params = {recordid:data.project.recordid, taskCategory:taskCategoryFilter,
                     user:userFilter, sessions:""}
        if (dom.find(".session_treegrid").length > 0) {
            var selected_node = dom.find(".session_treegrid").jstree(true).get_selected(true);
            if (selected_node.length > 0) {
                params['sessions'] = selected_node.map((x)=>x.id).join(",");
            }
        }
        params = JSON.stringify(params);
        var url = `/en/looper/user/AnalyseProjects?filter=${params}`;
        var scroll_top = dom.find(".example-preview").scrollTop();
        $.get(url, function(result){
            if (result.status) {
                var item = Object.values(result.data)[0]
                var tasks_bak = JSON.parse(JSON.stringify(item.tasks));                
                dom.find(".summary_wrap").remove();
                dom.append(summary_html.render(item.summary))
                var component = dom.data("component");
                for (var task of item.tasks) {
                    if (task.taskcategory == 'MH')
                        task['taskcategory_desc'] = 'Must Have'
                    else
                        task['taskcategory_desc'] = 'Must Finish'
                }                
                component.timeline_dom.empty();
                component.dom.data("tasks",tasks_bak);
                var tasks = analysis_tasks(item.tasks)
                component.loadData(tasks);
                load_sub_must_have(tasks, component);
                $('.mustFinishMF').closest(".timeline-item").addClass('priorityTask');
                $(".top5_mustHave").find(".SWTimeline2 span.tile").removeClass("bg-primary");
                $(".top5_mustHave").find(".SWTimeline2 span.tile i").remove();
                $(".top5_mustHave").find("span.int").removeClass("d-none");                
                if (restore_scroll)
                    dom.find(".example-preview").scrollTop(scroll_top);
            }
        });
    }
    function load_filter_session(dom, data) {
        dom.jstree({
            "core":{
                "worker":false,
                event: {
                    touchstart: {
                      passive: true
                    }
                },                
                "check_callback" : true,  
                'multiple' : true,
                'data' : function (obj, callback) {
                    var jsonarray = new Array();
                    for (var item of data) {
                        var arr = {
                            "id":item.id,
                            "parent":item.id == item.parent || !item.parent || data.filter((x)=>x.id==item.parent).length == 0 ? "#":item.parent,  //將返回數據的parentid字段的值轉為tree data的parent, 如果為空，設置為#
                            "text":item.desp,
                            "icon":"d-none",
                            'state': {
                                'opened': true //默認展開節點
                            },
                        }
                        jsonarray.push(arr);
                    }
                    callback.call(this, jsonarray);
                }
            },
            "plugins":['contextmenu',"checkbox"]
        });
        dom.on("click", function(e){
            e.stopPropagation();
        });
    }

    function bind_event() {
        $.contextMenu({
            selector: '.priorityTask',
            callback: function(key, options) {
                if (key == "add") {
                    append_MH_task(options.$trigger)
                }else if(key == "update"){
                    update_MH_task(options.$trigger)
                }else if (key == "addtask") {
                    add_task(options.$trigger)
                }
            },
            items: {
                "addtask":{name:gettext("Add Task"), icon:"add"},
                "add": {name: gettext("Add Must Have Task"), icon: "add"},
                "update": {name: gettext("Set Must Have Task"), icon: "add"},
            }
        });
        $.contextMenu({
            selector: '.example-preview',
            callback: function(key, options) {
                if (key == "add") {
                    append_MF_task(options.$trigger)
                }
            },
            items: {
                "add": {name: gettext("Add Must Finish Task"), icon: "add"},
            }
        });
        //User改變方法
        $("select[name='user']").on("change", function(){
            get_Projects($("select[name='user']").val())
        })
        //User改變方法
        $("button[name='refresh']").on("click", function(){
            get_Projects($("select[name='user']").val())
        })
        // recordid 的change事件
        recordidDOM.on("change",function(e){
            get_Projects($("select[name='user']").val(),e.target.value)
        })
        //任務雙擊事件顯示該任務詳情
        $('#projectList').on('dblclick','.timeline-item',function(){
            var inc_id = $(this).find('.font-weight-normal').attr('inc_id')
            var component = $(this).closest(".SWTimeline2")
            init_task(inc_id);
            jqueryEventBus.one('globalTaskOperation', function(event, result) {
                if (result == undefined)
                    return;
                var method = result.method;
                if (method == "save" || method == "del") {
                    reload(component);
                }
            });                                    
        });
        $("#projectList").on("click", ".filter_goal .dropdown-item", function(e){
            e.preventDefault();
            var filter_type = $(this).attr('filter_type');
            $(this).closest(".filter_goal").find(`.dropdown-item[filter_type='${filter_type}']`).removeClass("selected");
            if ($(this).hasClass("selected")) {
                $(this).removeClass("selected");
            }else {
                $(this).addClass("selected");
            }
            if (filter_type == 'user' && $(this).closest(".filter_goal").find(`.dropdown-item.selected[filter_type='category']`).length == 0)
                $(this).closest(".filter_goal").find(`.dropdown-item[filter_type='category'][name="all"]`).addClass("selected");
            var taskCategoryFilter = $(this).closest(".filter_goal").find(`.dropdown-item.selected[filter_type='category']`).attr("name");
            var userFilter = $(this).closest(".filter_goal").find(`.dropdown-item.selected[filter_type='user']`).attr("name");
            var data = $(this).closest(".filter_goal").data("data");
            filter_goal($(this).closest(".SWTimeline2"), data, taskCategoryFilter, userFilter);
        });
        $("#projectList").on("click", ".btn_project_diagram", function(e){
            var recordid = $(this).attr("recordid");
            $.get("/devplat/sessions_list?recordid="+recordid, function(result){
                if (result.status){
                    if (result.data.length > 0 ) {
                        var sessionid = result.data[0].sessionid;
                        setTimeout(() => {
                        window.open(`/devplat/sessions?recordid=${recordid}&menu_id=mi_${sessionid}#Diagram`, "_blank");
                        });
                    }
                }
            });            
        });
        $("#projectList").on("click", ".btn_mindmap_diagram", function(e){
            var recordid = $(this).attr("recordid");
            $.get("/devplat/sessions_list?recordid="+recordid, function(result){
                if (result.status){
                    if (result.data.length > 0 ) {
                        var sessionid = result.data[0].sessionid;
                        setTimeout(() => {
                            window.open(`/devplat/sessions?recordid=${recordid}&menu_id=mi_${sessionid}&show_mindmap=true#Diagram`, "_blank");
                        });
                    }
                }
            });            
        });
        $("#projectList").on("click", ".session_treegrid_operation", function(e){
            if (!$(e.target).hasClass("apply")) {
                e.stopPropagation();
            }
        });
        $("#projectList").on("click", ".session_treegrid_operation .clear", function(e){
            $(this).closest(".dropdown-menu").find(".session_treegrid").jstree("deselect_all");
        });
        $("#projectList").on("click", ".session_treegrid_operation .apply", function(e){
            var component = $(this).closest(".SWTimeline2")
            reload(component);
        });
        // $("#projectList").on('dblclick',".timeline .priorityTask",function(e){
        // });
        $("#projectList").on("click", ".btn_project_calendar", function(e){
            var component = $(this).closest(".SWTimeline2");
            var tasks = component.data("tasks");
            $('#project_calendar').modal("show");     
            $('#project_calendar').off('shown.bs.modal');
            $('#project_calendar').on('shown.bs.modal', function () {
                show_project_calendar(tasks);            
            });                
            //show_project_calendar(recordid);
        });        
        $("#projectList").on("click", ".btn_project_gantt", function(e){
            var component = $(this).closest(".SWTimeline2");
            var tasks = component.data("tasks")
            $('#project_gantt').modal("show");     
            $('#project_gantt').off('shown.bs.modal');
            $('#project_gantt').on('shown.bs.modal', function () {
                show_project_gantt(tasks);            
            });                
            $('#project_gannt').modal("show");
        });   
        //其他菜單中 add MF task的點擊事件
        $("#projectList").on("click", ".addMFTask", function(e){
            var recordid = $(this).attr("recordid");
            $(this).data("recordid", recordid);
            append_MF_task($(this));
        })
    }
    function show_project_calendar(tasks) {
        $("#project_calendar_container").empty();
        var calendar = new SWCalendar("#project_calendar_container");
        calendar.datasource = tasks;
        calendar.start_field = "planbdate";
        calendar.end_field = "planedate";
        calendar.title_field = "task";
        calendar.extended_fields = ['inc_id']
        calendar.eventClick = function(info) {
            var pk = info.event.extendedProps['inc_id'];
            init_task(pk);        
        }
        calendar.init();
    }
    function show_project_gantt(tasks) {
        for(var item of tasks) {
            item['taskno'] = "{0}-{1}-{2}".format(item['pid'], parseInt(item['tid']), parseInt(item['taskid']));
        }
        var tempTasks =  JSON.parse(JSON.stringify(tasks));
        var tasks = analysis_tasks(tempTasks)
        var gantt_data = []
        tasks.sort((a,b) => (a.planedate > b.planedate) ? 1 : 0)
        for (var task of tasks) {
            gantt_data.push(task);
            if (task.sub_list != undefined && task.sub_list.length > 0) {
                task.sub_list.sort((a,b) => (a.planedate > b.planedate) ? 1 : 0)
                gantt_data.push(...task.sub_list)
            }
        }

        $("#project_gantt_container").empty();
        var gantt = new SWGantt("#project_gantt_container");
        gantt.datasource = gantt_data;
        gantt.start_field = "planbdate";
        gantt.end_field = "planedate";
        gantt.title_field = "task";
        gantt.id_field = "taskno";
        gantt.dependencies_field = "udf08";
        gantt.extended_fields = ['inc_id']
        gantt.eventClick = function(task) {
            var pk = task['inc_id'];
            init_task(pk);        
        }
        gantt.init();        
    }
    function reload(component)   {
        var taskCategoryFilter = component.find(".filter_goal").find(`.dropdown-item.selected[filter_type='category']`).attr("name");
        var userFilter = component.find(".filter_goal").find(`.dropdown-item.selected[filter_type='user']`).attr("name");
        var data = component.find(".filter_goal").data("data");
        filter_goal(component, data, taskCategoryFilter, userFilter, true);
    }
    //增加Mast Have任務
    function append_MH_task(checkedli){
        var component = checkedli.closest(".SWTimeline2")
        var session = checkedli.find('.font-weight-normal').html()
        var sessionid = session.split('-')
        var sessionid = '{0}-{1}'.format(sessionid[0], sessionid[1])
        init_task(undefined,{sessionid:sessionid});
        jqueryEventBus.one('globalTaskOperation', function(event, result) {
            if (result == undefined)
                return;
            var method = result.method;
            if (method == "save" || method == "del") {
                reload(component);
            }
        });        
        var id = "#add-task"
        if (SWApp.os.isAndroid || SWApp.os.isPhone || SWApp.os.isTablet)
            id = "#add-task-module"
        var setdata = setInterval(function () {
            var isShown = $(id).hasClass('in') || $(id).hasClass('show');
            if (isShown){
                $('input[name="udf08"]').val(session)
                $('select[name="taskcategory"]').val('MH')
                $('div[name="taskcategory"]').find('.filter-option-inner-inner').html('MH:Must Have')
                $('div[name="taskcategory"]').find('.dropdown-toggle').attr('title','MH:Must Have')
                clearInterval(setdata);
            }
        }, 300);        
    }
    function add_task(checkedli){
        var component = checkedli.closest(".SWTimeline2")
        var session = checkedli.find('.font-weight-normal').html()
        var sessionid = session.split('-')
        var sessionid = '{0}-{1}'.format(sessionid[0], sessionid[1])
        init_task(undefined,{sessionid:sessionid});
    }    
    //修改Session下的任務為Must Have
    function update_MH_task(checkedli){
        var component = checkedli.closest(".SWTimeline2")
        var session = checkedli.find('.font-weight-normal').html()
        session_id = session
        $("#update_MH_task").modal("show");  
        $('[data-toggle="flatpickr"]').flatpickr();
        load_data(session)
    }
    
    //增加Mast Finish任務
    function append_MF_task(checkedli){
        var component = checkedli.closest(".SWTimeline2")
        var recordid = checkedli.data("recordid")
        init_task(undefined,{ initTaskCategory:"MF"});
        $('[name="create_task"]').data("initParams",{ initTaskCategory:"MF"});
        var recordIdInput = $(".switchTaskWrap").find("input[name='recordid']");
        var id = "#add-task"
        if (SWApp.os.isAndroid || SWApp.os.isPhone || SWApp.os.isTablet) {
            id = "#add-task-module"
            recordIdInput = $("#switchMobileTaskWrapper").find("input[name='recordid']");
        }
        jqueryEventBus.one('globalTaskOperation', function(event, result) {
            if (result == undefined)
                return;
            var method = result.method;
            if (method == "save" || method == "del") {
                $('[name="create_task"]').removeData("initParams");
                reload(component);
            }
        });
        var is_show = false;
        var interval = setInterval(function () {
            var isShown = $(id).hasClass('in') || $(id).hasClass('show');
            if (isShown) {
                is_show = true;
                if (recordIdInput.val() == "")
                    recordIdInput.val(recordid);
            }
            if (!isShown && is_show) {
                clearInterval(interval);
            }
        }, 100);
        var searchSession = setInterval(function() {
            var isShown = $(id).hasClass('in') || $(id).hasClass('show');
            if (isShown) {
                if ($("#" + recordid + "_anchor").length == 0) {
                    recordIdInput.val(recordid);
                    var e = jQuery.Event("keydown");
                    e.which = 13; //回車
                    recordIdInput.trigger(e);
                }
                clearInterval(searchSession);
            }
        }, 100);
    }    

    //session—task表格初始化
    function init_task_table() {
        for(var item of Object.values(tables)) {
            var table = new SWDataTable("#"+item.id, item.id.replace("table","datatable")); //創建SWDataTable對象
            table.searching = false;
            table.firstColSelected = true;
            table.pageLength = 25;
            if (["session_top_tasks_table","session_top_priority_tasks_table"].indexOf(item.id) != -1) {
                table.pageLength = 40;
                table.ajax_method = "POST";
                table.orderBy = [['schpriority','desc']];
            }else {
                table.orderBy = [['taskid', 'asc']];     //設置按taskno 升序排序，可以進行多字段排序，參考上面的重要屬性
            }
        
            //設置DataTable顯示5個字段，分別是taskno, task,contact, planbdate, planedate
            table.columns = [
                { field: "taskno", label: gettext('TaskNo') },
                { field: "task", label: gettext('Task')},
                { field: "contact", label: gettext('Contact') },
                { field: "schpriority", label: gettext('SchPriority')},
                { field: "planbdate", label: gettext('PlanBDate'), render:SWDataTable.DateRender},
                { field: "edate", label: gettext('EDate'), render:SWDataTable.DateRender},     
                { field: "progress", label: gettext('Progress'), width: "8%"},
                { field: "hoperation", label:gettext('HOperation'), render:function(data,type,row){
                    if (Object.keys(hoperation_type).indexOf(data) != -1)
                        return hoperation_type[data]
                    else
                        return data;
                }},
                { field: "taskid", label: "TaskId", visible: false },
                {field:"priority", label:"priority", visible:false},
                {field:"class_field", label:"class1", visible:false},
                {field:"docflag", label:"DocFlag", visible:false},
                {field:"taskcategory", label:"taskcategory", visible:false},
                {field:"inc_id", label:"inc_id", visible:false},
                
            ];
            //SWDataTable控件不支持的功能，可以使用原生jquery datatable的屬性設置
            // var task_width = SWApp.os.isMobile ? "60%" : "35%"
            table.setOptions({
                responsive: {
                    details: {
                        type: 'column',
                        target: 'tr'
                      }
                },  //是否支持手機展開和隱藏列
                // colReorder: true,  //启动列拖动
                scrollY: "500px",
                scrollX: true,
                columnDefs: [
                    { "responsivePriority": -1, "className": "all", "width": '1rem', "targets": 0 },
                    { "responsivePriority": 5, "className": "min-tablet-p", "targets": 1 },
                    { "responsivePriority": -1, "className": "all", "width": '80%', "targets": 2 },
                    { "responsivePriority": 2, "className": "desktop", "targets": 3 },
                    { "responsivePriority": 3, "className": "min-tablet-p", "targets": 4 },
                    { "responsivePriority": 4, "className": "min-tablet-p", "targets": 5 },
                    { "responsivePriority": 5, "className": "min-tablet-p", "targets": 6 },
                    { "responsivePriority": -1, "className": "all", "targets": 7 },
                    { "responsivePriority": 5, "className": "desktop", "targets": 8 },
                ],
                deferLoading: 0,
            });
            item.table = table;
            item.datatable = table.init('/PMIS/task/t_list');  //根據以上設置好的屬性，初始化table1，數據來源於/server/tasks這個地址
            item.datatable.on('dblclick', 'tbody tr', function () {
                var local_table = Object.values(tables).filter((a)=>{return a.id == $(this).closest(".SWDataTable").attr("id")})
                if(local_table.length > 0) {
                    var data = local_table[0].datatable.row(this).data();
                    init_task(data.DT_RowId);    
                }
            });        
            // SWApp.os.isMobile ? item.datatable.colReorder.move( 7, 1 ) : ""
        }
    }
    //session—task的表格數據初始化
    function load_data(sessionid) {
        tables.tasks.table.custom_params_fun = function () {
                if (sessionid != undefined) {
                    var array = sessionid.split("-")
                    var pid = array[0]
                    var tid = array[1]
                    var date_filter = {"condition":"AND","rules":[],"not":false}
                    var filter = {"condition":"AND","rules":[
                        {"id":"pid","field":"pid","type":"string","input":"text","operator":"equal","value":pid},
                        {"id":"tid","field":"tid","type":"double","input":"text","operator":"equal","value":tid},
                        {"id":"taskcategory","field":"taskcategory","type":"string","input":"text","operator":"not_in","value":['MH','MF']}
                        ],"not":false,"valid":true};
                    // date_filter.rules.push({"id":"taskcategory","field":"taskcategory","type":"string","input":"text","operator":"not_in","value":['MH']});    
                    // if (select_finished==false){
                    //     var progress_date_filter = {"condition":"OR","rules":[
                    //         {"id":"progress","field":"progress","type":"string","input":"text","operator":"not_in","value":["C","F"]}
                    //     ],"not":false}
                    //     if (date_filter.rules.length > 0)
                    //         progress_date_filter.rules.push(date_filter)
                    //     filter.rules.push(progress_date_filter);
                    // }
                    return {attach_query: JSON.stringify(filter)};
                }
                else
                    return {};
        } 
        $("#update_MH_task_div .SWCombobox select").val('').selectpicker('refresh');
        $("#update_MH_task_div input").val('');
        tables.tasks.datatable.search('').columns().search('').draw();
    }
    //session—task的hoperation字段值格式處理
    function init_hoperation_type() {
        var url = "/PMIS/global/get_typelist?type_name={0}".format("HOperation_Type");
        $.get(url, function(result){
            if (result.status) {
                for(var item of result.data) {
                    hoperation_type[item['value']] = item['label'];
                }
            }
        });
    }
    
    //session—task相關事件綁定
    function bind_search_event() {
        //session—task清除按鈕點擊事件
        $("#update_MH_task_div .btn-clear").on("click", function(){
            $("#update_MH_task_div .SWCombobox select").val('').selectpicker('refresh');
            $("#update_MH_task_div input").val('');
            load_data(session_id)
            // tables.tasks.datatable.search('').columns().search('').draw();
        });
        //session—task的查詢按鈕點擊事件
        $("#update_MH_task_div .btn-search").on("click", function(){
            var local_tables = [];
            Array.prototype.push.apply(local_tables, Object.values(tables).filter((item)=>{
                return $("#" + item.id).closest(".tab-pane").hasClass("show");
            }));
            Array.prototype.push.apply(local_tables, Object.values(tables).filter((item)=>{
                return $("#" + item.id).closest(".tab-pane").hasClass("show") == false;
            }));       
            
                
            var array = session_id.split("-")
            var pid = array[0]
            var tid = array[1]
            var filter = {"condition":"AND","rules":[
                {"id":"pid","field":"pid","type":"string","input":"text","operator":"equal","value":pid},
                {"id":"tid","field":"tid","type":"double","input":"text","operator":"equal","value":tid},
                {"id":"taskcategory","field":"taskcategory","type":"string","input":"text","operator":"not_in","value":['MH','MF']}
                ],"not":false,"valid":true};
            for(var item of local_tables) {
                var search_datatable = item.datatable
                var search_table = item.table;
                // return {attach_query: JSON.stringify(filter)};
                $("#update_MH_task_div .SWCombobox select, #update_MH_task_div .card-header input").each((index,el)=>{
                    var name = $(el).attr("name");
                    var val = $(el).val()
                    if(val!=undefined && val!=''){
                        if(name=='task')
                            filter['rules'].push({"id":name,"field":name,"type":"string","input":"text","operator":"contains","value":val})
                        else if(name=='planBDates')
                            filter['rules'].push({"id":'planbdate',"field":'planbdate',"type":"string","input":"text","operator":"greater_or_equal","value":val})
                        else if(name=='planBDatee')
                            filter['rules'].push({"id":'planbdate',"field":'planbdate',"type":"string","input":"text","operator":"less_or_equal","value":val})
                        else
                            filter['rules'].push({"id":name,"field":name,"type":"string","input":"text","operator":"equal","value":val})
                            // search_datatable = search_datatable.columns(search_table.getColumnIndexByName(name)+1).search(val)
                    }
                });
                search_table.custom_params_fun = function () {return {attach_query: JSON.stringify(filter)}} 
                search_datatable.search('').columns().search('').draw();  
            }
        });
    }

    //初始化session—task的查詢輸入框
    function init_html() {
        var progress = new SWCombobox("progress", gettext('Progress'),
            [{label:"N:新工作",value:"N"},{label:"I:正在進行的工作",value:"I"},{label:"T:當天的工作",value:"T"},
            {label:"S:已經開始的工作",value:"S"},{label:"F:已完成工作",value:"F"},{label:"C:基本完成",value:"C"},
            {label:"NF:除F的工作",value:"NF"},{label:"H:被掛起的工作",value:"H"},{label:"R:復查",value:"R"}]);
        progress.setHorizontalDisplay(true)
        var priority = new SWCombobox("priority",gettext('Priority'),['888','8888','8889']);
        priority.setHorizontalDisplay(true)
        var class1 = new SWCombobox("class_field", gettext('Class'),[{label:"class1",value:"1"}, {label:"class2", value:"2"},{label:"Other", value:"3"}]);
        class1.setHorizontalDisplay(true)
        var contact = new SWCombobox("contact", gettext('Contact'), window.CommonData.PartUserNames)
        contact.setHorizontalDisplay(true)
        var process = new SWCombobox("hoperation", gettext('Hoperation'), "/PMIS/global/get_typelist?type_name=HOperation_Type");       
        process.setHorizontalDisplay(true)

        
        // var planbdate = new SWText("planbdate","date", gettext('PlanBDate'), false)
        // planbdate.setHorizontalDisplay(true)   

        var task_desc = new SWText("task","text",gettext('Task Desp'));
        task_desc.setHorizontalDisplay(true)
        var container = $(`<div class="filter_f col-xs-6 col-sm-4 col-lg col-xl-2 f_progress"></div>`);
        $("#update_MH_task_div .filter .f_planDate").after($(`<div class="filter_t mt-xl-0 col-12 col-sm-12 col-lg col-xl f_task_desc"></div>`).append(task_desc.dom));
        // $("#update_MH_task_div .filter").prepend($(`<div class="filter_d col-xs-6 col-sm-4 col-lg-2 col-custom-xxl f_planbdate"></div>`).append(planbdate.dom));
        $("#update_MH_task_div .filter").prepend($(`<div class="filter_c col-xs-6 col-sm-4 col-lg-2 col-xl-1-5 f_class"></div>`).append(class1.dom));
        $("#update_MH_task_div .filter").prepend($(`<div class="filter_p col-xs-6 col-sm-4 col-lg-2 col-xl-1-5 f_priority"></div>`).append(priority.dom));
        $("#update_MH_task_div .filter").prepend($(`<div class="filter_p col-xs col-sm col-lg col-xl-1-5 f_process"></div>`).append(process.dom));
        $("#update_MH_task_div .filter").prepend($(`<div class="filter_t mt-lg-0 col-xs-6 col-sm-4 col-lg-2 col-xl-1-5 f_contact"></div>`).append(contact.dom));
        $("#update_MH_task_div .filter").prepend(container.clone().append(progress.dom));
        $("#update_MH_task_div .filter.row .input-group").removeClass("col-auto");
        var get_lang_code = $("#curr_language_code").val();
        if (get_lang_code == "en") {
            $("#update_MH_task_div .filter.row").addClass("en_filter");
        }

        // select_finished.input_dom.on("change", function (e) {
        //     var checked =  $(this).prop('checked')
        //     load_data(session_id,checked)
        // });

        bind_search_event();
        init_hoperation_type();
    }

    //批量修改任務分類未MH
    $('#update_MH_task_submit').on('click',function(){
        var select_data = tables.tasks.table.getSelectedFlagData()
        if(select_data['datas'].length==0){
            SWHintMsg.showToast("body", gettext('Pesase Select at least one piece of data'), "warning")
            return
        }
        $.ajax({
            type: "POST",
            url: "/looper/top_porject/batch_set_MHTask",
            data: JSON.stringify({'data':select_data,'sessiontask':session_id}),
            datatype: "json",
            processData: false, 
            contentType: false, 
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            success: function (response) {
                // 處理成功後的返回數據
                if (response.status)
                    alert('設置MH成功！')
                else
                    alert('設置MH失敗！')
            },
            error: function () {
                alert("程序異常!");
            }

        })
    })

    //獲取登陸者優先級最高的5個Project及其任務
    var recordid = getParamFromUrl('recordid');
    if(recordid){
        get_Projects(user, recordid)
    }else{
        get_Projects(user)
    }
    bind_event();
    init_html();
    init_task_table();

    getBrowser();

    function getBrowser(){
        var isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
        var isSafari = /Safari/.test(navigator.userAgent) && /Apple Computer/.test(navigator.vendor);
        if (isChrome) {
            console.log("Chrome!");
        }
        if (isSafari) {
            $("#session_tasks_table").addClass("iosCheckbox");
        }
    }
    //xmm新增可以從個人主頁和mindmap中跳轉過來,用定時器的方式等待projectlist加載完成後獲取填充在header上的recordid的值來匹配要選中的元素
    let timer = setInterval(() => { 
        var flag = $("#projectList").find(".SWTimeline2").length !== 0
        if (flag){
            var recordid = getParamFromUrl('recordid');
            var sessions = getParamFromUrl('sessions');
            var shrink = getParamFromUrl("shrink");
            var dom = undefined;
            $("#projectList").find(".SWTimeline2").each(function(i,v){
                var text = $(this).find(".card-header .card-title").text()
                var match = text.match(/\(\d+\)/);
                if (match){
                    var recordid_text = match[0].slice(1, -1);
                    if (recordid === recordid_text){
                        dom = $(this);
                        // $(this).find(".card-header .card-title").css("background","#f7c46c")
                        $(this).find(".card-header .card-title").addClass("bg_yellow")
                        $(this)[0].scrollIntoView(true);
                        window.scrollBy({top: -100});
                    }
                }
            })
            if (dom)
                filterGoalForUrlParams(dom,recordid,sessions, shrink);
            clearInterval(timer)
        }
    },1000)

    function filterGoalForUrlParams(dom, recordid, sessions, shrink){
        var params = {recordid:recordid, sessions:sessions}
        params = JSON.stringify(params);
        var url = `/en/looper/user/AnalyseProjects?filter=${params}`;
        $.get(url, function(result){
        if (result.status) {
            var item = Object.values(result.data)[0]
            dom.find(".summary_wrap").remove();
            dom.append(summary_html.render(item.summary))
            var component = dom.data("component");
            for (var task of item.tasks) {
                if (task.taskcategory == 'MH')
                    task['taskcategory_desc'] = 'Must Have'
                else
                    task['taskcategory_desc'] = 'Must Finish'
            }                
            component.timeline_dom.empty();
            var tasks = analysis_tasks(item.tasks)
            component.loadData(tasks);
            load_sub_must_have(tasks, component);
            $('.mustFinishMF').closest(".timeline-item").addClass('priorityTask');
            $(".top5_mustHave").find(".SWTimeline2 span.tile").removeClass("bg-primary");
            $(".top5_mustHave").find(".SWTimeline2 span.tile i").remove();
            $(".top5_mustHave").find("span.int").removeClass("d-none"); 
            if (shrink != undefined) {
                component.dom.find(".timeline.timeline2").removeClass("expanded");
                component.dom.find(".timeline.timeline2").find("button[aria-controls='collapse_session']").addClass("collapsed");
                component.dom.find(".timeline.timeline2").find("button[aria-controls='collapse_session']").attr("aria-expanded", "false");
                component.dom.find(".timeline.timeline2>div[id^='collapse-']").removeClass("show");
                var sessArr = sessions.split(",");
                for (var sessionid of sessArr) {
                    $(".SWTimeline2 .filter_session li[role='treeitem']")
                    component.dom.find(".filter_session li[role='treeitem']").find("a[id='{0}_anchor']".format(sessionid)).click();
                }
            }
        }
        });
    }
});