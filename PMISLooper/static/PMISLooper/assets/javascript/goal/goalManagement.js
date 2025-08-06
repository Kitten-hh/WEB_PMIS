$(function () {
    //用戶下拉框組件
    var user = get_username()
    var all_user = new SWCombobox('user',gettext('User'),window.CommonData.PartUserNames, user);
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
    all_user.input_dom.attr("data-live-search", "true");
    all_user.setHorizontalDisplay(true);
    $(".page-inner .query_tools").before(all_user.dom);
    var recordid_cmpt = new SWCombobox("recordid", gettext("RecordID"), "/PMIS/subproject/get_all_recordid", undefined, 'recordid','recordid');
    recordid_cmpt.input_dom.attr("data-live-search", "true");
    recordid_cmpt.dom.addClass("recordid");
    recordid_cmpt.setHorizontalDisplay(true);
    $(".page-inner .query_tools").before(recordid_cmpt.dom);
    //獲取summary template
    var summary_html = $("#summary_template").prop("innerHTML");
    var title_html = $("#title_template").prop("innerHTML");
    
    //獲取對應聯繫人優先級最高的5個Project及其任務
    function get_Projects(user, recordid){
        var search_params = {};
        if (user)
            search_params['contacts'] = user;
        if (recordid)
            search_params['recordids'] = recordid;
        var url = `/en/PMIS/goal/management/search?search_filter=${JSON.stringify(search_params)}`;

        //移除原有的TopProject框
        $('#projectList').find('.top_wrap').remove()
        //獲取對應用戶前五的Project和其任務數據
        $.get(url, function(result){
            if (result.status){
                var projects = result.data;
                Object.entries(projects).forEach(([strkey,item], index)=>{
                    show_timeline(item, index);
                })
                $('.mustFinishMF').closest(".timeline-item").addClass('priorityTask');
                $(".top5_mustHave").find(".SWTimeline2 span.tile").removeClass("bg-primary");
                $(".top5_mustHave").find(".SWTimeline2 span.tile i").remove();
                $(".top5_mustHave").find("span.int").removeClass("d-none");

                // test

            }
        });  
    }

    function show_timeline(item, index) {
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
        var strhtml = `<div class="col-12 col-xl-6 col-xxl-4 top_wrap" id="[[id]]"></div>`.replace('[[id]]',strid);
        $("#projectList").append(strhtml);
        var tasks = analysis_tasks(item.tasks)
        var top = new SWTimeline2('G'+goal_num+'.'+item.project.projectname+'(' + item.project.recordid + ')', tasks, "planedate", child_info, daily_tmpl, "planedate asc");
        top.dom.children(".card-header").html(title_html.render({title:'G'+goal_num+'.'+item.project.projectname+'(' + item.project.recordid + ')', goaldesc:item.project.goaldesc, recordid:item.project.recordid}));
        top.dom.children(".card-header").find(".filter_goal").data("data", item);
        for (var user of users)
            top.dom.children(".card-header").find(".filter_goal .dropdown-menu")
            .append(`<a href="#" class="dropdown-item pl-4 user" filter_type="user" name="${user}">${user}</a>`);
        top.dom.children(".card-header").find(".filter_goal .dropdown-menu")
            .append(`<a href="#" class="dropdown-item pl-4 user" filter_type="user" name="all">All</a>`);
        top.dom.data("component", top);
        load_filter_session(top.dom.find(".filter_session .session_treegrid"), sessions);
        load_sub_must_have(tasks, top, strid);
        $("#"+strid).append(top.dom);
        //SWTimeline2組件下的統計數據顯示模塊
        $("#"+strid).find(".SWTimeline2").append(summary_html.render(item.summary)); 
               
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
                console.log(i)
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
                task.sub_list = tasks.filter(x=>x.taskcategory == 'MH' && x.relationgoalid == getTaskNo(task))
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
        var contact = $("select[name='user']").val();
        var url = `/en/PMIS/goal/management/search?filter=${params}`;
        if (contact)
            url += `&search_filter=${JSON.stringify({contacts:contact})}`;
        var scroll_top = dom.find(".example-preview").scrollTop();
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
                if (restore_scroll)
                    dom.find(".example-preview").scrollTop(scroll_top);
            }
        });
    }
    function load_filter_session(dom, data) {
        dom.jstree({
            "core":{
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
                }
            },
            items: {
                "add": {name: gettext("添加MustHave任務"), icon: "add"},
            }
        });     
        //User改變方法
        /**
        $("select[name='user'],select[name='recordid']").on("change", function(){
            get_Projects($("select[name='user']").val(), $("select[name='recordid']").val())
        });*/
        $("#btn_search").on("click", function() {
            var contact = $("select[name='user']").val();
            var recordid = $("select[name='recordid']").val();
            get_Projects($("select[name='user']").val(), $("select[name='recordid']").val())
        });
        $("#btn_clear").on("click", function() {
            $("select[name='user']").val("");
            $("select[name='recordid']").val("");
            $(".page-inner .userlist .SWCombobox").find("select.control").selectpicker('refresh');
        });
        //任務雙擊事件顯示該任務詳情
        $('#projectList').on('dblclick','.timeline-item',function(){
            var inc_id = $(this).find('.font-weight-normal').attr('inc_id')
            var component = $(this).closest(".SWTimeline2")
            init_task(inc_id);
            var id = "#add-task"
            if (SWApp.os.isAndroid || SWApp.os.isPhone || SWApp.os.isTablet)
                id = "#add-task-module"
            var is_show = false;
            var interval = setInterval(function () {
                var isShown = $(id).hasClass('in') || $(id).hasClass('show');
                if (isShown)
                    is_show = true;
                if (!isShown && is_show) {
                    reload(component);
                    clearInterval(interval);
                }
            }, 100);
        });
        function reload(component, self)   {
            var taskCategoryFilter = component.find(".filter_goal").find(`.dropdown-item.selected[filter_type='category']`).attr("name");
            var userFilter = component.find(".filter_goal").find(`.dropdown-item.selected[filter_type='user']`).attr("name");
            var data = component.find(".filter_goal").data("data");
            filter_goal(component, data, taskCategoryFilter, userFilter, true);
        }
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
                        window.open(`/devplat/sessions?recordid=${recordid}&menu_id=mi_${sessionid}#Diagram`);
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
                        window.open(`/devplat/sessions?recordid=${recordid}&menu_id=mi_${sessionid}&show_mindmap=true#Diagram`);
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

    }

    function append_MH_task(checkedli){
        var component = checkedli.closest(".SWTimeline2")
        var session = checkedli.find('.font-weight-normal').html()
        var session_id = session.split('-')
        var session_id = '{0}-{1}'.format(session_id[0], session_id[1])
        init_task(undefined,{sessionid:session_id});
        var id = "#add-task"
        if (SWApp.os.isAndroid || SWApp.os.isPhone || SWApp.os.isTablet)
            id = "#add-task-module"
        var is_show = false;
        var interval = setInterval(function () {
            var isShown = $(id).hasClass('in') || $(id).hasClass('show');
            if (isShown)
                is_show = true;
            if (!isShown && is_show) {
                reload(component);
                clearInterval(interval);
            }
        }, 100);
        var setdata = setInterval(function () {
            var isShown = $(id).hasClass('in') || $(id).hasClass('show');
            if (isShown){
                $('input[name="relationgoalid"]').val(session)
                $('select[name="taskcategory"]').val('MH')
                $('div[name="taskcategory"]').find('.filter-option-inner-inner').html('MH:Must Have')
                $('div[name="taskcategory"]').find('.dropdown-toggle').attr('title','MH:Must Have')
                clearInterval(setdata);
            }
        }, 300);
    }

    function init_data(){
        var param_user = getParamFromUrl("contact");
        var param_recordid = getParamFromUrl("recordid");
        if (param_user != undefined & param_recordid != undefined) {
            all_user.input_dom.val(param_user).selectpicker('refresh');
            let timer = setInterval(() => { 
                var flag = recordid_cmpt.input_dom.val() == "";
                if (flag){
                    recordid_cmpt.input_dom.val(param_recordid).selectpicker("refresh");
                    clearInterval(timer)
                }
            },1000)            
            get_Projects(param_user, param_recordid)
        }
        else
            get_Projects(user);
    }
    
    init_data();
    //獲取登陸者優先級最高的5個Project及其任務
    bind_event();
});