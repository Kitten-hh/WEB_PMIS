var gettext_ganttChart_editor = gettext("Gantt Chart Editor");
var gettext_ganttChart_view = gettext("Gantt View");
$(function () {
    $(".page").addClass("projects_page");
    setTimeout(function() {
        $(".page.projects_page").addClass("has-sidebar has-sidebar-expand-xl");
    }, 2000)
    $(".page.projects_page").on("click", '.nav-link[data-toggle="sidebar"]:not(.btn-switchTask)', function(e) {
        e.stopPropagation();
        Looper.showSidebar();
    })
    var projectNameStr = gettext('Project.ProjectName');
    var user = get_username()
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
    var summary_html = $("#summary_template").prop("innerHTML");
    var title_html = $("#title_template").prop("innerHTML");
    function init() {
        init_project_list();
    }
    function init_project_list() {
        var contact = get_username();
        var recordids = getParamFromUrl("recordids");
        var url = "/devplat/project/list";
        if (contact != undefined)
            url = url + "?contact=" + contact;
        if (recordids != undefined)
            if (url.indexOf("?") != -1)
                url += "&recordids=" + recordids
            else
                url += "?recordids=" + recordids;
        promiseGet(url).then((result)=>{
            if (result.status) {
                $("#project_list").empty();
                var total_temp = `<div class="col recordid_col" recordid="[[recordid]]" username="[[username]]">
                        <strong>Score</strong> <span class="d-block">[[projectscore]]</span>
                        </div><!-- /grid column -->
                        <!-- grid column -->
                        <div class="col">
                            <strong>Tasks</strong> <span class="d-block">[[task_qty]]</span>
                        </div><!-- /grid column -->`
                var projects = new SWProjectlist(gettext("Projects"), [],"projectenddate",
                "s_title","projectname","progress","last_update", total_temp);
                projects.processors_function = function(item){
                    if (Date.parse(item["planbdate"]) != null)
                        item["planbdate"] = Date.parse(item["planbdate"]).toString("yyyy-MM-dd");
                    if (Date.parse(item["planedate"]) != null)
                        item["planedate"] = Date.parse(item["planedate"]).toString("yyyy-MM-dd");
                    if (Date.parse(item['projectenddate']) != null)
                        item["projectenddate"] = Date.parse(item["projectenddate"]).toString("dd MMM yyyy");
                }
                projects.set_menu(`<div class="dropdown-arrow"></div>
                <a href="#" class="dropdown-item view_diagram project_diagram"><i class="fas fa-project-diagram mr-2"></i>` + gettext("View Diagram") + `</a>
                <a href="#" class="dropdown-item view_diagram mdinmap_diagram"><i class="fas fa-sitemap mr-2"></i>` + gettext("View Sitemap") + `</a>
                <a href="#" class="dropdown-item view_diagram deliverables"><i class="fas fa-list-ol fa-fw mr-2"></i>` + gettext("View Deliverables") + `</a>
                <a href="#" class="dropdown-item view_diagram project_mindmap"><i class="fab fa-cloudsmith fa-fw mr-2"></i>` + gettext("View Mindmap") + `</a>
                <a href="#" class="dropdown-item view_diagram project_gantt_view"><svg class="ganttIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M512 416l0-64c0-35.3-28.7-64-64-64L64 288c-35.3 0-64 28.7-64 64l0 64c0 35.3 28.7 64 64 64l384 0c35.3 0 64-28.7 64-64zM64 160l0-64 144 0 16 0 0 64L64 160zm224 0l0-64 80 0c8.8 0 16 7.2 16 16l0 16-38.1 0c-21.4 0-32.1 25.9-17 41L399 239c9.4 9.4 24.6 9.4 33.9 0L503 169c15.1-15.1 4.4-41-17-41L448 128l0-16c0-44.2-35.8-80-80-80L224 32l-16 0L64 32C28.7 32 0 60.7 0 96l0 64c0 35.3 28.7 64 64 64l160 0c35.3 0 64-28.7 64-64z"/></svg>` + gettext_ganttChart_view + `</a>                                
                <a href="#" class="dropdown-item view_diagram project_gantt_editor"><svg class="ganttIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M512 416l0-64c0-35.3-28.7-64-64-64L64 288c-35.3 0-64 28.7-64 64l0 64c0 35.3 28.7 64 64 64l384 0c35.3 0 64-28.7 64-64zM64 160l0-64 144 0 16 0 0 64L64 160zm224 0l0-64 80 0c8.8 0 16 7.2 16 16l0 16-38.1 0c-21.4 0-32.1 25.9-17 41L399 239c9.4 9.4 24.6 9.4 33.9 0L503 169c15.1-15.1 4.4-41-17-41L448 128l0-16c0-44.2-35.8-80-80-80L224 32l-16 0L64 32C28.7 32 0 60.7 0 96l0 64c0 35.3 28.7 64 64 64l160 0c35.3 0 64-28.7 64-64z"/></svg>` + gettext_ganttChart_editor + `</a>
                <a href="#" class="dropdown-item view_diagram session_task"><i class="fab fa-cloudsmith fa-fw mr-2"></i>` + gettext("View Task") + `</a>`);
                
                projects.after_search = function() {
                    $("#project_list .list_container .card-body:eq(0)").click();
                }                
                projects.addItems(result.data);
                $("#project_list").append(projects.dom);    
                // $("#project_list .SWProjectlist .list_container .item").removeClass("col-lg-6 col-xl-4").addClass("col-xl-6 col-xxl-4");
                
                var contact_cmpt = new SWCombobox("contact", gettext('Contact'), window.CommonData.PartUserNames, contact);
                var recordid_cmpt = new SWText("recordids","text", gettext('RecordID'));
                var projectname_cmpt = new SWText("projectname","text", projectNameStr);
                if (contact != undefined)
                    contact_cmpt.input_dom.val(contact);
                contact_cmpt.input_dom.attr("data-live-search", "true");
                projects.filter_content.append(recordid_cmpt.dom);
                projects.filter_content.append(contact_cmpt.dom);
                projects.filter_content.append(projectname_cmpt.dom);
                // $("div.item.col-lg-6.col-xl-4").first().click()
                $("#project_list .list_container .card-body:eq(0)").click();
                projects.datasource = url;
            }else {
                alert("Get project list fail!");
            }
        });
 
    }
    init();
    $("#project_list").on("click", ".list_container .card-body", function (e) {
        e.preventDefault();
        $('div.cardSelect').removeClass('cardSelect')
        $(this).parent().addClass("cardSelect")
        var recordid = $(this).find(".recordid_col").attr("recordid");
        var projectname = $(this).find(".title a").text();
        setCookie("projects_cur_name", projectname.replace(/^[0-9]+/, ''));
        change_Menu(recordid);
        change_MustTasks_new(recordid);
        $('#project_list .btn.btn-light.btn-icon.nav-link.d-xl-none').click();
    });
    $("#project_list").on("click", ".dropdown-item.view_diagram", async function (e) {
        e.preventDefault();
        var self = this;
        var recordid = $(this).closest(".card").find(".recordid_col").attr("recordid");
        if ($(self).hasClass("mdinmap_diagram")) {
            //window.open(`/devplat/sessions?recordid=${recordid}&menu_id=mi_${sessionid}&show_mindmap=true#Diagram`);
            window.open(`/devplat/sessions?recordid=${recordid}&show_mindmap=true#Diagram`);
        } else if ($(self).hasClass("deliverables")) {
            setTimeout(() => {
                window.open(`/devplat/sessions?recordid=${recordid}#Deliverables`);
            });
        }else if ($(self).hasClass("project_mindmap")) {
            var mindmap_id = await getProjectMindmapId(recordid);
            if (mindmap_id != undefined) {
                setTimeout(() => {
                    window.open(`/looper/mindmap?pk=${mindmap_id}`);
                });
            }
        }else if ($(self).hasClass("project_gantt_editor")) {
            setTimeout(() => {
                window.open(`/project/project_milestone?recordid=${recordid}`, "_blank");
            });
        }else if ($(self).hasClass("session_task")) {
            setTimeout(() => {
                window.open(`/looper/session_manager?recordid=${recordid}`, "_blank");
            });
        }else if ($(self).hasClass("project_gantt_view")) {
            $("#project_gantt iframe").attr("src", `/project/project_gantt_modal?recordid=${recordid}`);
            $("#project_gantt").modal("show");
        }else {
            setTimeout(() => {
                window.open(`/devplat/sessions?recordid=${recordid}#Diagram`);
            });
        }
    });

    function getProjectSessionId(recordid) {
        return new Promise((resolve, reject)=>{
            $.get("/devplat/sessions_list?recordid=" + recordid, function (result) {
                if (result.status) {
                    if (result.data.length > 0) {                
                        resolve(result.data[0].sessionid);
                    }else
                        resolve(undefined);
                }
            });
        })        
    }

    function getProjectMindmapId(recordid) {
        return new Promise((resolve, reject)=>{
            $.get(`/devplat/project/get_mindmap_id?recordid=${recordid}`, function(result) {
                if (result.status) {
                    resolve(result.data);
                }else
                    resolve(undefined);
            });
        });
    }

    function change_Menu(recordid) {
        clear_Menu();
        SWNavigationBar.setMenuItem("mi_1", gettext('Knowledge based'), "#");  
        SWNavigationBar.addSubMenu("mi_1_1", "mi_1", gettext('Solution Type'), "#");  
        SWNavigationBar.addSubMenu("mi_1_2", "mi_1", gettext('Repository'), "#");  
        var url = "/devplat/session/question?recordid={0}&menu_id=mi_2".format(recordid);
        SWNavigationBar.setMenuItem("mi_2", gettext('Question'), url);
        var url = "/devplat/course?recordid={0}&menu_id=mi_3".format(recordid);
        SWNavigationBar.setMenuItem("mi_3", gettext('Course'), "/devplat/course?recordid={0}&menu_id=mi_3".format(recordid));
        $("#mi_3 a").attr("target","_blank");
        SWNavigationBar.setMenuItem("mi_4", gettext('Control Center'), "#");  
        SWNavigationBar.setMenuItem("mi_5", gettext('Overview'), "/devplat/project/overview");
        $("#mi_5 a").attr("target","project");
        SWNavigationBar.setMenuItem("mi_6", gettext('Mindmap'), "/looper/mindmap");
        getProjectMindmapId(recordid).then((mindmap_id)=>{
            SWNavigationBar.setMenuItem("mi_6", gettext('Mindmap'), `/looper/mindmap?pk=${mindmap_id}`);
            $("#mi_6 a").attr("target","mindmap");
        })
        $("#mi_6 a").attr("target","mindmap");
        SWNavigationBar.setMenuItem("mi_7", gettext("RuleDoc"), "/devplat/ruledoc?recordid={0}&menu_id=mi_7".format(recordid));
        $("#mi_7 a").attr("target","_blank");
        $.get("/devplat/sessions_list?recordid="+recordid, function(result){
            if (result.status){
                result.data.forEach((session, index)=>{
                    SWNavigationBar.setMenuItem("mi_{0}".format(session.sessionid), session.sdesp, "#");                
                    $("#mi_{0}".format(session.sessionid)).attr("sessionid", session.sessionid);
                    $("#mi_{0}".format(session.sessionid)).attr("planbdate", session.planbdate);
                    $("#mi_{0}".format(session.sessionid)).attr("planedate", session.planedate);
                    $("#mi_{0} a".format(session.sessionid)).attr("target", "_blank");
                    $("#mi_{0} a".format(session.sessionid)).addClass("session_url");
                });
                
                $("#stacked-menu .menu-item a.session_url").on("click", function(e){
                    e.preventDefault();
                    setCookie("cur_projects_url", location.href);
                    //$("#stacked-menu .menu-item").removeClass("has-active");
                    //$(this).closest(".menu-item").addClass("has-active");
                    var menu_id = $(this).closest(".menu-item").attr("id");
                    var url = window.location.protocol +"//" + window.location.host + "/devplat/sessions?recordid=" + recordid + "&menu_id=" +menu_id;
                    //if (contact != undefined)
                        //url = url + "&contact="+contact;
                    setTimeout(() => {
                        window.open(url);
                    });
                    
                });
            }
        });
    }

    function clear_Menu() {
        $("#stacked-menu>.menu>.menu-item").each((index, menu) => {
            var id = $(menu).attr("id");
            var reg = /mi_([0-9]+)/;
            if (reg.test(id)) {
                var result = id.match(reg);
                var num = parseInt(result[1])
                if (num >= 1 && num <= 11) {
                    $(menu).removeClass("has-child");
                    $(menu).children("ul").remove();
                    $(menu).hide();
                } else
                    $(menu).remove();
            }
        });
    }



    function change_MustTasks(recordid) {
        $("#must_tasks").children().remove();

        var subtitle_tmpl =
            `<li class="timeline-item" inc_id="[[inc_id]]">
            <div class="timeline-figure">
                <span class="tile tile-circle tile-sm tile-custom"></span>
            </div>
            <div class="timeline-body">
                <div class="media">
                    <div class="media-body [[Class]]">
                        <div
                            class="d-flex justify-content-between align-items-center mb-2 font-weight-bolder">
                            <p class="mb-0 timeline-date text-dark">[[planbdate]] / [[planedate]]</p>
                            <span class="timeline-date text-dark mr-2"><i class="far fa-file mr-2"></i>[[progress]]</span>
                        </div>
                        <h5 class="step-title">[[task]]</h5>
                        <div class="mb-2">
                            <span class="text-dark"><i
                                    class="far fa-clipboard mr-2"></i>[[pid]]-[[tid]]-[[taskid]]</span>
                            <span class="ml-2 text-dark"><i class="far fa-list-alt mr-1"></i>[[schpriority]]</span>
                        </div>
                    </div>
                </div>
            </div>
        </li>`
        var strurl = '/zh-hans/devplat/project/search_mustTasks?recordid=' + recordid
        // var must_tasks = new SWTimeline2("Must Have Tasks", strurl,"planbdate",'', subtitle_tmpl, "planbdate asc");;  
        // $("#must_tasks").append(must_tasks.dom);


        $.get(strurl, function (result) {
            if (result.status) {
                result.data[0].MustTasks.forEach((task, index) => {
                    var strhtml = subtitle_tmpl.replace('[[planbdate]]', new Date(task.planbdate).toString("yyyy-MM-dd"))
                        .replace('[[planedate]]', new Date(task.planedate).toString("yyyy-MM-dd"))
                        .replace('[[task]]', task.task).replace('[[pid]]', task.pid)
                        .replace('[[tid]]', task.tid).replace('[[taskid]]', task.taskid)
                        .replace('[[schpriority]]', task.schpriority).replace('[[progress]]', task.progress).replace('[[inc_id]]', task.inc_id)
                    strhtml = task.process == 'F' ? strhtml.replace('[[Class]]', 'priorityTask') : strhtml.replace('[[Class]]', '')
                    $("#must_tasks").append(strhtml);
                });
                var strhead = `Must Have Tasks[[Message]]`
                var AnalysisData = result.data[0].AnalysisData[0]
                if (result.data[0].AnalysisData.length == 1) {
                    strhead = strhead.replace('[[Message]]', '(' + AnalysisData.recordid + ')' + '(' + AnalysisData.completed_qty + '/' + AnalysisData.task_qty + ')')
                } else {
                    strhead = strhead.replace('[[Message]]', '(HAS NOT TASK)')
                }
                $('#must_tasks_h').html(strhead)
            }
        });
    }
    function change_MustTasks_new(recordid) {
        var params = JSON.stringify({
            recordid: recordid, taskCategory: "all",
            user: "all"
        })
        var url = `/en/looper/user/AnalyseProjects?filter=${params}`;
        var goaldesc = ''
        $.ajax({
            url: '/en/looper/user/get_goaldesc?recordid=' + recordid,
            type: 'GET',
            async: false,
            success: function (response) {
                goaldesc = response.data
            },
            error: function (error) {
                console.error(error);
            }
        });
        $.get(url, function (result) {
            if (result.status) {
                var item = Object.values(result.data)[0];
                var users = new Set();
                var sessions = [];
                for (var task of item.tasks) {
                    if (task.taskcategory == 'MH')
                        task['taskcategory_desc'] = 'Must Have'
                    else
                        task['taskcategory_desc'] = 'Must Finish'
                    if (task.contact != null && task.contact.trim() != "")
                        users.add(task.contact)
                    if (sessions.filter((a) => a.id == task.sessionid).length == 0) {
                        sessions.push({ id: task.sessionid, desp: task.sdesp, parent: task.sparent });
                    }
                }
                var sindex = index + 1
                var strid = 'top' + sindex
                //SWTimeline2組件的容器
                var tasks = analysis_tasks(item.tasks)
                // for (let t of tasks) {
                //     if (t.contact != null && t.contact.trim() != "")
                //         users.add(t.contact);
                // }
                users = Array.from(users).sort();
                var top = new SWTimeline2(item.project.projectname + '(' + item.project.recordid + ')', tasks, "planedate", child_info, daily_tmpl, "planedate asc");
                top.dom.children(".card-header").html(title_html.render({ title: item.project.projectname + '(' + item.project.recordid + ')', goaldesc: goaldesc, recordid: item.project.recordid }));
                top.dom.children(".card-header").find(".filter_goal").data("data", item);
                top.dom.find(".example-preview").data("recordid", item.project.recordid);
                user_link = top.dom.children(".card-header").find(".filter_goal .dropdown-menu").find("a.user")
                if (user_link.length > 0)
                    user_link.remove();
                for (var user of users)
                    top.dom.children(".card-header").find(".filter_goal .dropdown-menu")
                        .append(`<a href="#" class="dropdown-item pl-4 user" filter_type="user" name="${user}">${user}</a>`);
                top.dom.children(".card-header").find(".filter_goal .dropdown-menu")
                    .append(`<a href="#" class="dropdown-item pl-4 user" filter_type="user" name="all">All</a>`);
                top.dom.data("component", top);
                top.dom.children(".card-body").first().addClass("scrollbar");
                load_filter_session(top.dom.find(".filter_session .session_treegrid"), sessions)
                load_sub_must_have(tasks, top, strid);
                $("#must_tasks").empty();
                $("#must_tasks").append(top.dom);
                //SWTimeline2組件下的統計數據顯示模塊
                $("#must_tasks").find(".SWTimeline2").append(summary_html.render(item.summary));
                $('.mustFinishMF').closest(".timeline-item").addClass('priorityTask');
                $("#must_tasks").find(".SWTimeline2 span.tile").removeClass("bg-primary");
                $("#must_tasks").find(".SWTimeline2 span.tile i").remove();
                $("#must_tasks").find("span.int").removeClass("d-none");
            }
        });
    }

    function filter_goal(dom, data, taskCategoryFilter, userFilter, restore_scroll = false) {
        var params = {
            recordid: data.project.recordid, taskCategory: taskCategoryFilter,
            user: userFilter, sessions: ""
        }
        if (dom.find(".session_treegrid").length > 0) {
            var selected_node = dom.find(".session_treegrid").jstree(true).get_selected(true);
            if (selected_node.length > 0) {
                params['sessions'] = selected_node.map((x) => x.id).join(",");
            }
        };
        params = JSON.stringify(params);
        var url = `/en/looper/user/AnalyseProjects?filter=${params}`;
        var scroll_top = dom.find(".example-preview").scrollTop();
        $.get(url, function (result) {
            if (result.status) {
                var item = Object.values(result.data)[0]
                // var users = new Set();
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
                // for (let t of tasks) {
                //     if (t.contact != null && t.contact.trim() != "")
                //         users.add(t.contact);
                // }
                // users = Array.from(users).sort();
                // user_link = dom.children(".card-header").find(".filter_goal .dropdown-menu").find("a.user")
                // if (user_link.length > 0)
                //     user_link.remove();
                // for (var user of users)
                //     dom.children(".card-header").find(".filter_goal .dropdown-menu")
                //         .append(`<a href="#" class="dropdown-item pl-4 user" filter_type="user" name="${user}">${user}</a>`);
                // dom.children(".card-header").find(".filter_goal .dropdown-menu")
                //     .append(`<a href="#" class="dropdown-item pl-4 user" filter_type="user" name="all">All</a>`);
                component.loadData(tasks);
                load_sub_must_have(tasks, component);
                $('.mustFinishMF').closest(".timeline-item").addClass('priorityTask');
                $("#must_tasks").find(".SWTimeline2 span.tile").removeClass("bg-primary");
                $("#must_tasks").find(".SWTimeline2 span.tile i").remove();
                $("#must_tasks").find("span.int").removeClass("d-none");
                if (restore_scroll)
                    dom.find(".example-preview").scrollTop(scroll_top);
            }
        });
    }

    function load_filter_session(dom, data) {
        dom.jstree({
            "core": {
                "check_callback": true,
                'multiple': true,
                'data': function (obj, callback) {
                    var jsonarray = new Array();
                    for (var item of data) {
                        var arr = {
                            "id": item.id,
                            "parent": item.id == item.parent || !item.parent || data.filter((x) => x.id == item.parent).length == 0 ? "#" : item.parent,  //將返回數據的parentid字段的值轉為tree data的parent, 如果為空，設置為#
                            "text": item.desp,
                            "icon": "d-none",
                            'state': {
                                'opened': true //默認展開節點
                            },
                        }
                        jsonarray.push(arr);
                    }
                    callback.call(this, jsonarray);
                }
            },
            "plugins": ['contextmenu', "checkbox"]
        });
        dom.on("click", function (e) {
            e.stopPropagation();
        });
    }

    function load_sub_must_have(tasks, component, index) {
        var medias = []
        for (var i = 0; i < tasks.length; i++) {
            medias.push(component.dom.find(`.mustFinishMF[inc_id='${tasks[i].inc_id}']`).closest(".timeline-item"));
        }
        for (var i = 0; i < tasks.length; i++) {
            var sub_items = tasks[i].sub_list;
            if (sub_items) {
                var tempTimeLine = new SWTimeline2('demo', sub_items, "planedate", child_info, daily_tmpl, "planedate asc");
                tempTimeLine.dom.find(".section-block").addClass("ml-1 mt-2");
                $(medias[i]).after(tempTimeLine.dom.find(".example-preview").html());

                if ($(medias[i]).next().length > 0 && $(medias[i]).next().children().length > 0) {
                    $(medias[i]).parent().addClass("card-expansion-item expanded");
                    $(medias[i]).next().wrap(`<div id="collapse-` + index + `-` + i + `" class="collapse show"></div>`);
                    $(medias[i]).append(`<button class="btn btn-reset px-2" data-toggle="collapse" data-target="#collapse-` + index + `-` + i + `" aria-expanded="true" aria-controls="collapse_session"><span class="collapse-indicator"><i class="fa fa-fw fa-chevron-down"></i></span></button>`);
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
                task.sub_list = tasks.filter(x => x.taskcategory == 'MH' && x.udf08 == getTaskNo(task))
                exists_tasknos.push(getTaskNo(task))
                task.sub_list.map(x => exists_tasknos.push(getTaskNo(x)))
                master.push(task);
            }
        }
        var not_master_task = tasks.filter(x => x.taskcategory == 'MH' && exists_tasknos.indexOf(getTaskNo(x)) == -1);
        master.push(...not_master_task);
        return master;
    }
    function reload(component) {
        var taskCategoryFilter = component.find(".filter_goal").find(`.dropdown-item.selected[filter_type='category']`).attr("name");
        var userFilter = component.find(".filter_goal").find(`.dropdown-item.selected[filter_type='user']`).attr("name");
        var data = component.find(".filter_goal").data("data");
        filter_goal(component, data, taskCategoryFilter, userFilter, true);
    }
    $('#must_tasks').on('dblclick', '.timeline-item', function () {
        var inc_id = $(this).find("div[class^='mustFinish']").attr("inc_id")
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
    })

    $("#must_tasks").on("click", ".btn_project_diagram", function (e) {
        var recordid = $(this).attr("recordid");
        $.get("/devplat/sessions_list?recordid=" + recordid, function (result) {
            if (result.status) {
                if (result.data.length > 0) {
                    var sessionid = result.data[0].sessionid;
                    setTimeout(() => {
                        window.open(`/devplat/sessions?recordid=${recordid}&menu_id=mi_${sessionid}#Diagram`);
                    });
                }
            }
        });
    });

    $("#must_tasks").on("click", ".filter_goal .dropdown-item", function (e) {
        e.preventDefault();
        var filter_type = $(this).attr('filter_type');
        $(this).closest(".filter_goal").find(`.dropdown-item[filter_type='${filter_type}']`).removeClass("selected");
        if ($(this).hasClass("selected")) {
            $(this).removeClass("selected");
        } else {
            $(this).addClass("selected");
        }
        if (filter_type == 'user' && $(this).closest(".filter_goal").find(`.dropdown-item.selected[filter_type='category']`).length == 0)
            $(this).closest(".filter_goal").find(`.dropdown-item[filter_type='category'][name="all"]`).addClass("selected");
        var taskCategoryFilter = $(this).closest(".filter_goal").find(`.dropdown-item.selected[filter_type='category']`).attr("name");
        var userFilter = $(this).closest(".filter_goal").find(`.dropdown-item.selected[filter_type='user']`).attr("name");
        var data = $(this).closest(".filter_goal").data("data");
        filter_goal($(this).closest(".SWTimeline2"), data, taskCategoryFilter, userFilter);
    });

    $("#must_tasks").on("click", ".btn_mindmap_diagram", function (e) {
        var recordid = $(this).attr("recordid");
        $.get("/devplat/sessions_list?recordid=" + recordid, function (result) {
            if (result.status) {
                if (result.data.length > 0) {
                    var sessionid = result.data[0].sessionid;
                    setTimeout(() => {
                        window.open(`/devplat/sessions?recordid=${recordid}&menu_id=mi_${sessionid}&show_mindmap=true#Diagram`, "_blank");
                    });
                }
            }
        });
    });

    $("#must_tasks").on("click", ".session_treegrid_operation", function (e) {
        if (!$(e.target).hasClass("apply")) {
            e.stopPropagation();
        }
    });
    $("#must_tasks").on("click", ".session_treegrid_operation .clear", function (e) {
        $(this).closest(".dropdown-menu").find(".session_treegrid").jstree("deselect_all");
    });
    $("#must_tasks").on("click", ".session_treegrid_operation .apply", function (e) {
        var component = $(this).closest(".SWTimeline2")
        reload(component);
    });
    $.contextMenu({
        selector: '.priorityTask',
        callback: function(key, options) {
            if (key == "add") {
                append_MH_task(options.$trigger)
            }
        },
        items: {
            "add": {name: gettext("Add must have task"), icon: "add"},
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
            "add": {name: gettext("Add must finish task"), icon: "add"},
        }
    });
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
                $('input[name="udf08"]').val(session)
                $('select[name="taskcategory"]').val('MH')
                $('div[name="taskcategory"]').find('.filter-option-inner-inner').html('MH:Must Have')
                $('div[name="taskcategory"]').find('.dropdown-toggle').attr('title','MH:Must Have')
                clearInterval(setdata);
            }
        }, 300);        
    }

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
            
        var is_show = false;
        var interval = setInterval(function () {
            var isShown = $(id).hasClass('in') || $(id).hasClass('show');
            if (isShown) {
                is_show = true;
                if (recordIdInput.val() == "")
                    recordIdInput.val(recordid);
            }
            if (!isShown && is_show) {
                $('[name="create_task"]').removeData("initParams");
                reload(component);
                clearInterval(interval);
            }
        }, 100);
        var searchSession = setInterval(function() {
            var isShown = $(id).hasClass('in') || $(id).hasClass('show');
            if (isShown) {
                recordIdInput.val(recordid);
                var e = jQuery.Event("keydown");
                e.which = 13; //回車
                recordIdInput.trigger(e);
                clearInterval(searchSession);
            }
        }, 100);
    }    

})
