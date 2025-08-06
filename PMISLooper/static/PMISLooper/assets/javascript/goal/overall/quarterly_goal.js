function ManagerQuarterlyGoal(contact, period) {
    var contact = contact;
    var period = period;
    var goal_target = "#qGoals_pc .manager_quarterly_goal"
    var dom = $(goal_target);
    //var item_html =  `<li class="mb-2 pl-3 pr-3 d-flex justify-content-start"><span class="task_num">[[seqno]] <i class="fas fa-arrow-right pl-2"></i></span><p class="task_contents">[[goal]]</p></li>`;
    var item_html =  `<li class="mb-2 pl-3 pr-3 d-flex justify-content-start" pk="[[inc_id]]"><span class="task_num">[[seqno]] <i class="fas fa-arrow-right"></i></span><p class="task_contents">[[goal]]</p></li>`;    
    if (SWApp.os.isMobile || checkMediaQuery()) {
        goal_target = "#qGoals_mobile .manager_quarterly_goal";
        dom = $(goal_target);
        //item_html = `<li class="mb-2 d-flex justify-content-start"><i class="icofont-tick-mark mr-2"></i><p class="task_contents">[[goal]]</p></li>`;
        item_html = `<li class="mb-2 d-flex justify-content-start" pk="[[inc_id]]"><i class="icofont-tick-mark mr-2"></i><p class="task_contents">[[goal]]</p></li>`;
    }
    var all_goals = dom.find(".all_goals");
    this.source = undefined;
    var editor_container = undefined;
    var editor_form = undefined;
    var self = this;
    this.load_source = function(source) {
        this.source = source;
        all_goals.find("li").remove();
        if (source == undefined) 
            return;
        source.forEach((goal, index)=>{
            var desc = goal.goaldesc;
            var lines = desc.replace(/\r\n/g, "\r").replace(/\n/g, "\r").split(/\r/);
            //var seqno_length = (lines.length + "").length < 2 ? 2 : (lines.length + "").length;
            for (var i = 0; i < lines.length; i++) {
                var data = {'goal':lines[i],'inc_id':goal.inc_id};
                all_goals.append(item_html.render(data));                
            }            
            //var data = {goal:goal.goaldesc, seqno:"G"+(index+1)};
            //all_goals.append(item_html.render(data));            
        });
    }

    dom.on("click", ".edit" ,function(){
        var url = `/looper/goal/project_goal?contact=${contact}&period=${period}`;
        window.location.href = url;
    });
    dom.on("click", ".lookup" ,function(){
        var local_self = this;
        if ($(this).find("i").hasClass("fa-book-open")) {
            all_goals.hide();
            $(this).find("i").addClass("fa-save").removeClass("fa-book-open");
            if (editor_container == undefined) {
                editor_container = $(`<div class="q_goal_cat"></div>`);
                editor = new SWTextarea("goaldesc","", 10);
                editor.dom.find("label").hide();
                editor_container.append(editor.dom);
                dom.find("ul").before(editor_container);
            }else {
                editor_container.show();
            }
            if (self.source != undefined && self.source.length >0 ) {
                var content = ""
                self.source.forEach((goal, index)=>{
                    content += goal.goaldesc + "\r\n";
                });                
                editor.input_dom.val(content);
            }    
        } else {
            var content = editor_container.find("textarea[name='goaldesc']").val();
            $.ajax({
                type: "POST",
                url: "/PMIS/goal/overall/save_text_quarterly_goal",
                data: {contact:contact, period:period, content:content},
                datatype: "json",
                beforeSend: function (request) {
                    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                },
                success: function (result) {
                    if (result.status) {
                        editor_container.hide();
                        $(local_self).find("i").addClass("fa-book-open").removeClass("fa-save");
                        self.load_source(result.data.quarterly);
                        all_goals.show();
                        SWApp.popoverMsg(dom.find(".lookup"), gettext("Save success!"));
                    }else {
                        SWApp.popoverMsg(dom.find(".lookup"), gettext("Save fail!"));                        
                    }
                }                                
            });
        } 

        let hasExpandClass = dom.hasClass("page-expanded");
        if (SWApp.os.isMobile || checkMediaQuery()) {
            editor_container.find("textarea[name='goaldesc']").attr("rows", hasExpandClass ? '22' : '10');
        }else {
            editor_container.find("textarea[name='goaldesc']").attr("rows", hasExpandClass ? '40' : '10');
        }
    });

    dom.on("click", ".expandGoals" ,function(){
        dom.toggleClass("page-expanded");
        $("body").toggleClass("overflow-y-hidden");
        let hasExpandClass = dom.hasClass("page-expanded");
        dom.find(".expandGoals>i").attr("class", hasExpandClass ? 'fas fa-compress-alt' : 'fas fa-expand-alt');
    });

    $(".home-img").parent().append(`<h4 class="goal_contact text-center mb-0">${contact}</h4>`);
}    

function ManagerMonthlyGoal(contact, period, month) {
    var contact = contact;
    var period = period;
    var month = month;
    var year = period.split("-")[0];
    var period_num = period.split("-")[1];
    var month_str = Date.parse("{0}-{1}".format(year, period_num*3 - (3-month))).toString("yyyy-MM");
    var goal_target = "#qGoals_pc .month-{0} .month_goals".format(month);
    var dom = $(goal_target);
    var item_html =  `<li class="task d-flex mb-2"><span>[[goal]]</span></li>`;
    if (SWApp.os.isMobile || checkMediaQuery()) {
        goal_target = "#qGoals_mobile .month-{0} .month_goals".format(month);
        dom = $(goal_target);
    }    
    this.source = undefined;
    var editor_container = undefined;
    var editor_form = undefined;
    var self = this;
    this.load_source = function(source) {
        this.source = source;
        dom.find("li").remove();
        if (source == undefined) 
            return;
        var managements = this.source['goaldesc'];
        var lines = managements.replace(/\r\n/g, "\r").replace(/\n/g, "\r").split(/\r/);
        //var seqno_length = (lines.length + "").length < 2 ? 2 : (lines.length + "").length;
        for (var i = 0; i < lines.length; i++) {
            var data = {'goal':lines[i]};
            //data['seqno'] = ((i + 1) + "").padStart(seqno_length, "0");
            dom.find("ul").append(item_html.render(data));
            dom.find("ul").show();
        }
    }

    dom.on("click", ".edit" ,function(){
        if ($(this).find("i").hasClass("fa-edit")) {
            dom.find("ul").hide();
            $(this).find("i").removeClass("fa-edit")
            $(this).find("i").addClass("fa-save")
            if (editor_container == undefined) {
                editor_container = $(`<form class="form"></form>`);
                editor = new SWTextarea("goaldesc","", 10);
                editor.dom.find("label").hide();
                editor_container.append(editor.dom);
                goalid = new SWText("goalid","hidden", "",10);
                editor_container.append(goalid.dom);
                editor_container.append(new SWText("contact","hidden", "", contact).dom);
                editor_container.append(new SWText("period","hidden", "", period).dom);
                editor_container.append(new SWText("goaltype","hidden", "", "M").dom);
                editor_container.append(new SWText("month","hidden", "", month_str).dom);
                dom.append(editor_container);


                editor_form = new SWBaseForm(goal_target);
                editor_form.create_url = "/PMIS/goal/overall/create_goal_management";
                editor_form.update_url = "/PMIS/goal/overall/update_goal_management/[[pk]]"
                editor_form.pk_in_url = false;
                //editor_form.init_data()
                editor_form.on_after_save = function(data){
                    self.load_source(data);                
                    $(goal_target).find(".edit").find("i").removeClass("fa-save");
                    $(goal_target).find(".edit").find("i").addClass("fa-edit");
                    editor_container.hide();
                }
            }else {
                editor_container.show();
            }
            if (self.source != undefined) {
                //editor.input_dom.val(self.source["goaldesc"]);
                //goalid.input_dom.val(self.source['goalid']);
                editor_form.set_pk(self.source["inc_id"]);
                editor_form.init_data();
            }
        } else {
            //內容相同不保存
            if (self.source != undefined && self.source["goaldesc"].replace(/\r\n/g, "\r").replace(/\n/g, "\r") == 
                    editor.input_dom.val().replace(/\r\n/g, "\r").replace(/\n/g, "\r")) {
                $(goal_target).find(".edit").find("i").removeClass("fa-save");
                $(goal_target).find(".edit").find("i").addClass("fa-edit");
                editor_container.hide();
                dom.find("ul").show();
            }else 
                $(goal_target).find(".save").click();
        }
    });    
}

function ManagerWeeklyGoal(contact, period, month) {
    var contact = contact;
    var period = period;
    var month = month;
    var year = period.split("-")[0];
    var period_num = period.split("-")[1];
    var month_str = Date.parse("{0}-{1}".format(year, period_num*3 - (3-month))).toString("yyyy-MM");
    var goal_target = "#qGoals_pc .month-{0} .desc_week1".format(month);
    var relation_tasks_template = $("#task_template").html();
    var dom = $(goal_target);
    var item_html =  `<li class="task d-flex mb-2"><span>[[goal]]</span></li>`;
    var item_relation_html = `<li class="task d-flex flex-column align-items-start border-0 p-0 mb-2"><span>[[goal]]
    <a href="javascript:void(0);" class="relation_task_btn" sessionid="[[sessionid]]">
    <i class="oi oi-task ml-2"></i>
    </a></span>
    <div class="d-flex w-100 align-items-center mt-2">
        <div class="progress progress-xs w-100">
        <div class="progress-bar bg-success" role="progressbar" style="width: 0%;" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
        </div>    
        <span class="ml-2 progress-desc">0/0(0%)</span>
    </div>
    </li>`
    if (SWApp.os.isMobile || checkMediaQuery()) {
        goal_target = "#qGoals_mobile .month-{0} .desc_week1".format(month);
        dom = $(goal_target);
    }
    this.get_weekly_dom = function(index) {
        if (SWApp.os.isMobile || checkMediaQuery())
            return dom.find(".card").eq(index - 1);
        else
            return dom.find(".weekly_task_widget").eq(index - 1);          
    }

    this.get_weekly_target = function(index) {
        if (SWApp.os.isMobile || checkMediaQuery())
            return "{0} .card:eq({1})".format(goal_target, index);
        else
            return "{0} .weekly_task_widget:eq({1})".format(goal_target, index);
    }

    this.source = undefined;
    var self = this;
    this.load_source = function(source) {
        this.source = source;
        dom.find(".task-inner li").remove();
        if (source == undefined) {
            this.source = {};
            return;
        }
        for (const [key, value] of Object.entries(source)) {
            if (key.startsWith("weekly")) {
                var index = parseInt(key.replace("weekly-", ""))
                var weekly_dom = self.get_weekly_dom(index);
                this.load_one_weekly(weekly_dom, value);
            }
        }            
    }

    this.load_one_weekly = function(weekly_dom, source) {
        weekly_dom.find(".task-inner li").remove();
        var goaldesc = source['goaldesc'];
        var lines = goaldesc.replace(/\r\n/g, "\r").replace(/\n/g, "\r").split(/\r/);
        //var seqno_length = (lines.length + "").length < 2 ? 2 : (lines.length + "").length;
        for (var i = 0; i < lines.length; i++) {
            var data = {'goal':lines[i]};
            var local_item_html = item_html;
            var sessionids = undefined;
            if (/\(((\w+-\d+,?)+)\)$/i.test(lines[i])) {
                var session_match = lines[i].match(/\(((\w+-\d+,?)+)\)$/i);
                sessionids = session_match[1];
                local_item_html = item_relation_html;
                data['sessionid'] = sessionids;
            }
            var item_dom = $(local_item_html.render(data));
            weekly_dom.find("ul").append(item_dom);
            if (sessionids)
                self.load_goal_progress(item_dom, sessionids, source);
            weekly_dom.find("ul").show();
        }        
    }
    
    
    dom.on("click", ".edit" ,function(){
        var week_num = $(this).closest(".desc_week1").find(".edit").index($(this));
        var weekly_key = "weekly-"+(week_num + 1);
        var weekly_target = self.get_weekly_target(week_num);
        var editor_container = undefined;
        var editor_form = undefined;
        if ($(weekly_target).data("editor_container") != undefined) {
            editor_container = $(weekly_target).data("editor_container");
            editor_form = $(weekly_target).data("editor_form");
        }
        if ($(this).find("i").hasClass("fa-edit")) {
            $(weekly_target).find("ul").hide();
            $(this).find("i").removeClass("fa-edit")
            $(this).find("i").addClass("fa-save")
            if (editor_container == undefined) {
                editor_container = $(`<form class="form"></form>`);
                editor = new SWTextarea("goaldesc","", 10);
                editor.dom.find("label").hide();
                editor_container.append(editor.dom);
                goalid = new SWText("goalid","hidden", "",10);
                editor_container.append(goalid.dom);
                editor_container.append(new SWText("contact","hidden", "", contact).dom);
                editor_container.append(new SWText("period","hidden", "", period).dom);
                editor_container.append(new SWText("goaltype","hidden", "", "W").dom);
                editor_container.append(new SWText("month","hidden", "", month_str).dom);
                
                editor_container.append(new SWText("week","hidden", "", week_num + 1).dom);
                $(weekly_target).append(editor_container);


                editor_form = new SWBaseForm(weekly_target);
                editor_form.create_url = "/PMIS/goal/overall/create_goal_management";
                editor_form.update_url = "/PMIS/goal/overall/update_goal_management/[[pk]]"
                editor_form.pk_in_url = false;
                //editor_form.init_data()
                editor_form.on_after_save = function(data){
                    self.source[weekly_key] = data;
                    self.load_one_weekly($(weekly_target), data);
                    $(weekly_target).find(".edit").find("i").removeClass("fa-save");
                    $(weekly_target).find(".edit").find("i").addClass("fa-edit");
                    editor_container.hide();
                }
                $(weekly_target).data("editor_container", editor_container);
                $(weekly_target).data("editor_form", editor_form);    
            }else {
                editor_container.show();
            }
            if (self.source != undefined && weekly_key in self.source) {
                var data = self.source[weekly_key];
                //goalid.input_dom.val(data["goalid"]);
                //editor.input_dom.val(data["goaldesc"]);
                editor_form.set_pk(data["inc_id"]);
                editor_form.init_data();
            }            
        } else {
            //內容相同不保存
            if (self.source != undefined && self.source[weekly_key] != undefined && self.source[weekly_key]["goaldesc"].replace(/\r\n/g, "\r").replace(/\n/g, "\r") == 
                    editor.input_dom.val().replace(/\r\n/g, "\r").replace(/\n/g, "\r")) {
                $(weekly_target).find(".edit").find("i").removeClass("fa-save");
                $(weekly_target).find(".edit").find("i").addClass("fa-edit");
                editor_container.hide();
                dom.find("ul").show();
            }else 
                editor_form.save_data($(this));
        }
    });
    dom.on("click", ".list", function(){
        var week_num = $(this).closest(".desc_week1").find(".list").index($(this));
        var weekly_key = "weekly-"+(week_num + 1);
        var data = self.source[weekly_key];        
        if (data != undefined)
            window.show_week_tasks(data);
    })
    this.load_goal_progress = function(item_dom, sessionids, goal) {
        var relation_info = goal.sessions;
        if (relation_info) {
            relation_info = JSON.parse(relation_info);
            var session_arr = sessionids.split(",");
            var related_tasks = [];
            var related_querys = [];
            for(var sessionid of session_arr) {
                var tasks = relation_info[sessionid];
                if (tasks) {
                    var pid = sessionid.split("-")[0];
                    var tid = sessionid.split("-")[1];
                    var local_arr = tasks.split(",").map(x=>`${sessionid}-${x}`);
                    related_tasks.push(...local_arr);
                    var taskids = `"` + tasks.replaceAll(",",`","`) + `"`;
                    query = `{"condition":"AND","rules":[
                        {"id":"pid","field":"pid","type":"string","input":"text","operator":"equal","value":"${pid}"},
                        {"id":"tid","field":"tid","type":"string","input":"text","operator":"equal","value":"${tid}"},
                        {"id":"taskid","field":"taskid","type":"string","input":"text","operator":"in","value":[${taskids}]}
                    ],"not":false,"valid":true}`;
                    related_querys.push(query)
                }
            }
            if (related_tasks.length > 0) {
                tasks = `"` + related_tasks.join(",").replaceAll(",",`","`) + `"`;
                var params = {draw:0,length:-1,start:0,attach_query: `{"condition":"OR","rules":[${related_querys.join(",")}],"not":false,"valid":true}`};
                $.get("/PMIS/task/t_list", params, function(result){
                    self.load_goal_progress_with_data(item_dom, result.data);
                });                
            }            
        }
    }   
    this.load_goal_progress_with_data = function(item_dom, data) {
        var total_count = data.length;
        var complete_count = data.filter(x=>['C','F'].indexOf(x.progress) != -1).length;
        if (total_count > 0) {
            var progress = complete_count/total_count * 100;
            var bar = item_dom.find(".progress-bar");
            bar.attr("style", `width:${progress}%;`);
            bar.attr("aria-valuenow", `${progress}`);
            item_dom.find(".progress-desc").html(`${complete_count}/${total_count}(${progress.toFixed(0)}%)`);
        }else {
            var bar = item_dom.find(".progress-bar");
            bar.attr("style", `width:0%;`);
            bar.attr("aria-valuenow", `0`);
            item_dom.find(".progress-desc").html(`0/0(0%)`);
        }
    }
    this.init_relation_tasks = function(sessionids) {
        //初始化任務列表
        var related_tasks = undefined;
        var weekly_data = $("#relation_task").data("weekly_data");
        var relation_info = weekly_data.sessions;
        if (relation_info) {
            relation_info = JSON.parse(relation_info);
            var sessionid_arr = sessionids.split(",");
            var related_tasks = [];
            var related_querys = [];
            for(var sessionid of sessionid_arr) {
                var tasks = relation_info[sessionid];
                if (tasks) {
                    var pid = sessionid.split("-")[0];
                    var tid = sessionid.split("-")[1];
                    var local_arr = tasks.split(",").map(x=>`${sessionid}-${x}`);
                    related_tasks.push(...local_arr);
                    var taskids = `"` + tasks.replaceAll(",",`","`) + `"`;
                    query = `{"condition":"AND","rules":[
                        {"id":"pid","field":"pid","type":"string","input":"text","operator":"equal","value":"${pid}"},
                        {"id":"tid","field":"tid","type":"string","input":"text","operator":"equal","value":"${tid}"},
                        {"id":"taskid","field":"taskid","type":"string","input":"text","operator":"in","value":[${taskids}]}
                    ],"not":false,"valid":true}`;
                    related_querys.push(query)
                }
            }            
            if (related_tasks.length > 0) {
                tasks = `"` + related_tasks.join(",").replaceAll(",",`","`) + `"`;
                var params = {draw:0,length:-1,start:0,attach_query: `{"condition":"OR","rules":[${related_querys.join(",")}],"not":false,"valid":true}`};                
                $.get("/PMIS/task/t_list", params, function(result){
                    self.show_relation_tasks(result.data);
                });                
            }else {
                self.show_relation_tasks([]);                            
            }
        }else {
            self.show_relation_tasks([]);            
        }
        return related_tasks;
    }
    this.get_relation_tasks = function() {
        //初始化任務列表
        var related_tasks = [];
        var weekly_data = $("#relation_task").data("weekly_data");
        var relation_info = weekly_data.sessions;
        if (relation_info) {
            relation_info = JSON.parse(relation_info);
            for(var [sessionid, taskids] of Object.entries(relation_info)) {
                if (taskids != "" && taskids != undefined) {
                    var local_arr = taskids.split(",").map(x=>`${sessionid}-${x}`);
                    related_tasks.push(...local_arr);
                }
            }            
        }
        return related_tasks;        
    }
    this.init_relation_modal = function(sessionids, month) {
        //初始化任務列表
        self.init_relation_tasks(sessionids);
        $("#source_tasks .filter .btn-clear").click(); //清除之前的查詢條件
        //初始化選擇的任務列表
        var table = $("#source_tasks .card-body").data("table");
        var datatable = $("#source_tasks .card-body").data("datatable");
        var startDate = Date.parse(month+"-01").add(-7).day().toString("yyyy-MM-dd");
        var endDate = Date.parse(month+"-01").addMonths(1).add(7).day().toString("yyyy-MM-dd");
        table.custom_params_fun = function() {
            var filter = {"condition":"AND","rules":[
                {"id":"contact","field":"contact","type":"string","input":"text","operator":"equal","value":contact},
                {"condition":"OR","rules":[
                    {"id":"progress","field":"progress","type":"string","input":"text","operator":"not_in","value":["C","F"]},
                    {"condition":"AND","rules":[
                        {"id":"progress","field":"progress","type":"string","input":"text","operator":"in","value":["C","F"]},
                        {"id":"edate","field":"edate","type":"string","input":"text","operator":"greater_or_equal","value":startDate},
                        {"id":"edate","field":"edate","type":"string","input":"text","operator":"less_or_equal","value":endDate}
                    ],"not":false}
                ],"not":false}
                ],"not":false,"valid":true};
            var session_filter = {"condition":"OR","rules":[],"not":false}

            for (var sessionid of sessionids.split(",")) {
                var array = sessionid.split("-")
                var pid = array[0]
                var tid = array[1]    
                session_filter.rules.push({"condition":"AND","rules":[
                    {"id":"pid","field":"pid","type":"string","input":"text","operator":"equal","value":pid},
                    {"id":"tid","field":"tid","type":"double","input":"text","operator":"equal","value":tid}
                    ],"not":false});
            }
            filter.rules.push(session_filter);
            return {attach_query: JSON.stringify(filter)};
        }
        $("#source_tasks .card-body").data("init_custom_params_fun", table.custom_params_fun);
        table.handle_response_fun = function(json) {
            var related_tasks = self.get_relation_tasks();
            for(var i = json.length - 1; i >= 0; i--) {
                var task = json[i];
                if (related_tasks != undefined && related_tasks.indexOf(task.taskno) != -1)
                    json.splice(i, 1); //刪除這個任務
            }
            return json;
        }
        datatable.search('').columns().search('').draw();
    }
    this.show_relation_tasks = function(data) {
        $("#relation_task .related_tasks").empty();
        for(var task of data) {
            var task_dom = relation_tasks_template.render(task);
            $(task_dom).data("task", task).appendTo("#relation_task .related_tasks");
        }
    }
    
    dom.on("click", ".relation_task_btn", function(e){
        e.preventDefault();
        var sessionids = $(this).attr("sessionid");
        var weekly_html_tag = ".weekly_task_widget";
        if (SWApp.os.isMobile || checkMediaQuery())
            weekly_html_tag = ".card"
        var week_num = $(this).closest(".desc_week1").find(weekly_html_tag).index($(this).closest(weekly_html_tag));
        var weekly_key = "weekly-"+(week_num + 1);
        var weekly_data = self.source[weekly_key];
        $("#relation_task").data("weekly_data", weekly_data);
        $("#relation_task").data("week_num", week_num);
        $("#relation_task").data("sessionid", sessionids);
        $("#relation_task").data("item_dom", $(this).closest("li"));
        self.init_relation_modal(sessionids, weekly_data.month);
        $("#source_tasks").collapse('hide');
        $("#relation_task").modal("show");
        $("#relation_task .relation_btn").unbind("click", self.select_tasks);
        $("#relation_task .relation_btn").on("click", self.select_tasks)
        $("#relation_task").unbind("click",".unlink", self.unlink_tasks);
        $("#relation_task").on("click",".unlink", self.unlink_tasks)
    });
    this.unlink_tasks = function(e) {
        var taskno = $(this).attr("taskno");
        var taskid = $(this).attr("taskid");
        var tasklistno = taskno.substring(0, taskno.lastIndexOf("-"));
        var week_num = $("#relation_task").data("week_num");
        var item_dom = $("#relation_task").data("item_dom");
        var sessionids = $("#relation_task").data("sessionid");
        var weekly_key = "weekly-"+(week_num + 1);
        var weekly_data = self.source[weekly_key];
        var relation_info = weekly_data.sessions;
        if (!relation_info)
            relation_info = "{}"
        relation_info = JSON.parse(relation_info);
        for(var sessionid of sessionids.split(",")) {
            if (sessionid == tasklistno) {
                var tasks = relation_info[sessionid].split(",");
                tasks = tasks.filter(x=>x != taskid)
                if (tasks.length == 0)
                    delete relation_info[sessionid]
                else
                    relation_info[sessionid] = tasks.join(",")
            }
        }
        var related_tasks = $("#relation_task .related_tasks .list-group").not($(this).closest(".list-group")).get().map(x=>$(x).data("task"));
        var send_data = {goalid:weekly_data.goalid,contact:contact, period:period, goaltype:"W", month:weekly_data.month, week:weekly_data.week, sessions:JSON.stringify(relation_info)}
        self.update_relation(weekly_data.inc_id, send_data, item_dom, weekly_key, related_tasks);
    }
    this.select_tasks = function() {
        var week_num = $("#relation_task").data("week_num");
        var sessionids = $("#relation_task").data("sessionid");
        var item_dom = $("#relation_task").data("item_dom");
        var weekly_key = "weekly-"+(week_num + 1);
        var weekly_data = self.source[weekly_key];
        var table = $("#source_tasks .card-body").data("table");
        var select_tasks = table.getSelectedFlagData().datas;
        var related_tasks = $("#relation_task .related_tasks .list-group").not($(this).closest(".list-group")).get().map(x=>$(x).data("task"));
        related_tasks.push(...select_tasks)        
        var relation_info = weekly_data.sessions;
        if (!relation_info)
            relation_info = "{}"
        relation_info = JSON.parse(relation_info);
        for(var sessionid of sessionids.split(",")) {
            var tasks = []
            for(var task of related_tasks)
                if (task.taskno.substring(0, task.taskno.lastIndexOf("-")) == sessionid)
                    tasks.push(task.taskid);
            if (tasks.length == 0 && sessionid in relation_info)        
                delete relation_info[sessionid];
            else
                relation_info[sessionid] = tasks.join(",");
        }
        var send_data = {goalid:weekly_data.goalid,contact:contact, period:period, goaltype:"W", month:weekly_data.month, week:weekly_data.week, sessions:JSON.stringify(relation_info)}
        self.update_relation(weekly_data.inc_id, send_data, item_dom, weekly_key, related_tasks);
    }
    this.update_relation = function(inc_id, data, item_dom, weekly_key, relation_tasks) {
        return new Promise((resolve, reject)=>{
            $.ajax({
                url:`/PMIS/goal/overall/update_goal_management/${inc_id}`,
                type: "POST",
                data: data,
                datatype: "json",
                beforeSend: function (request) {
                    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                },
                success: function (result) {
                    if (result.status) {
                        resolve(true);
                        var datatable = $("#source_tasks .card-body").data("datatable");   
                        self.source[weekly_key].sessions = result.data.instance.sessions;
                        $("#relation_task").data("weekly_data", self.source[weekly_key]);
                        self.show_relation_tasks(relation_tasks);
                        datatable.search('').columns().search('').draw();                        
                        self.load_goal_progress_with_data(item_dom, relation_tasks);
                    }else {
                        resolve(false);
                        alert(gettext("Fail to save"))
                    }
                }
            });    
        });
    }
}

var gettext_Goalsfor = gettext("Goals for");
$(function(){
    $("title").html(gettext('Quarterly Goal'));
    var contact = getParamFromUrl("contact");
    var period = getParamFromUrl("period");
    var year = period.split("-")[0];
    var period_num = period.split("-")[1];
    var first_month_str = Date.parse("{0}-{1}".format(year, period_num*3 - 2)).toString("yyyy-MM");
    var second_month_str = Date.parse("{0}-{1}".format(year, period_num*3 - 1)).toString("yyyy-MM");
    var third_month_str = Date.parse("{0}-{1}".format(year, period_num*3)).toString("yyyy-MM");

    var base_container = "#qGoals_pc"
    if (SWApp.os.isMobile || checkMediaQuery()){
        base_container = "#qGoals_mobile"
    }
    //初始化period
    var period_cmpt = new SWCombobox("period", gettext("Period"), get_quarterly(period), period, "value","label",false);
    period_cmpt.setHorizontalDisplay();
    period_cmpt.dom.addClass("pl-0 pr-0");
    period_cmpt.dom.find(".caption").addClass("pr-1");
    $(base_container + " .period").append(period_cmpt.dom);
    period_cmpt.input_dom.on("change", function () {
        var period = $(this).val();
        window.location.href = `/looper/goal/overall/quarterly_goal?contact=${contact}&period=${period}`;
    });
    //初始化聯繫人
    var all_user = new SWCombobox('user',gettext('User'),window.CommonData.PartUserNames, contact);        
    all_user.dom.addClass("row");
    all_user.dom.find("label").addClass("col-auto pr-1");
    all_user.dom.addClass("mb-0");
    all_user.dom.children(".control").css("width","100px");
    all_user.dom.children(".control").wrap('<div class="col-auto pl-0"></div>');
    $(base_container + " .page-title-left").append(all_user.dom);
    all_user.input_dom.on("change", function(){
        var contact = $(this).val();
        window.location.href = `/looper/goal/overall/quarterly_goal?contact=${contact}&period=${period}`;
    });
    //定義頁面dom
    var title_goal_year = $($(base_container +" .breadcrumb-item")[0]).find("a");
    var title_goal = $($(base_container +" .breadcrumb-item")[1]);
    var monthly_tab = $(base_container +" .monthly-tab");
    var monthly_dom = $(base_container +" .mine_goals .task-inner")
    var quarter_goal_ti_right = $(base_container +" .manager_quarterly_goal .goals_ti_right")
    var monthly_templ = `<li class="task d-flex mb-2">
            <span pk="[[inc_id]]" class="task-info">[[task]]([[session_desc]])</span>
            <div class="ml-auto">
                <a href="javascript:void(0);" class="text-info del" data-toggle="tooltip" data-placement="top" title="" data-original-title="Delete">
                    <i class="far fa-times-circle"></i>
                </a>
            </div>
        </li>`
    var weekly_dom = $(base_container + " .desc_week1")
    var weekly_templ = `<li class="task-item">
                        <span class="mr-2 task-info" pk="[[inc_id]]">[[task]]</span>
                        <a href="javascript:void(0);" class="text-info del" data-toggle="tooltip" data-placement="top" title="" data-original-title="Delete">
                        <i class="far fa-times-circle"></i>
                        </a>                        
                        </li>`
    var month_select_query = undefined;
    $(".user_month_goals_ti").text("by {0}".format(contact)); 
    if (SWApp.os.isMobile || checkMediaQuery()) {
        title_goal_year = $(base_container +" .goal_title");
        title_goal = $(base_container +" .page-title-right .breadcrumb-item");
    }

    var manager_quarterly_goal = new ManagerQuarterlyGoal(contact, period);
    var manager_monthly1_goal = new ManagerMonthlyGoal(contact, period, 1);
    var manager_monthly2_goal = new ManagerMonthlyGoal(contact, period, 2);
    var manager_monthly3_goal = new ManagerMonthlyGoal(contact, period, 3);
    var manager_weekly1_goal = new ManagerWeeklyGoal(contact, period, 1);
    var manager_weekly2_goal = new ManagerWeeklyGoal(contact, period, 2);
    var manager_weekly3_goal = new ManagerWeeklyGoal(contact, period, 3);

    function init_data() {
        var year = period.split("-")[0];
        //設置goal for year
        title_goal_year.text("{0} ".format(year) + gettext_Goalsfor);

        //設置哪個季度
        //title_goal.text(gettext("{0} Quarterly Goal").format(period));
        init_month_desc();
    }

    function get_quarterly(period) {
        var curr_arr = get_quarterly_date(new Date());
        var pre_arr = get_quarterly_date(new Date(curr_arr[0]).addDays(-1));
        var pre_pre_arr = get_quarterly_date(new Date(pre_arr[0]).addDays(-1));
        var next_arr = get_quarterly_date(new Date(curr_arr[1]).addDays(1));
        var quarterlys = new Set()
        quarterlys.add(period)
        quarterlys.add(get_quarterly_str(next_arr[0]))
        quarterlys.add(get_quarterly_str(curr_arr[0]))
        quarterlys.add(get_quarterly_str(pre_arr[0]))
        quarterlys.add(get_quarterly_str(pre_pre_arr[0]))
        quarterlys = Array.from(quarterlys);
        quarterlys.sort().reverse();
        return quarterlys;
    }

    function get_quarterly_str(quarterly_date){
        var year = quarterly_date.getFullYear();
        var quarter = Math.ceil((quarterly_date.getMonth() + 1)/3)
        return `${year}-${quarter}`;
    }

    function get_quarterly_date(currentDate) {
          var quarter = Math.ceil((currentDate.getMonth() + 1)/3)
          var qbdate = new Date(currentDate.getFullYear(), 3 * quarter - 3, 1);    
          var month = 3 * quarter
          var remaining = parseInt(month / 12)
          var qedate = new Date(currentDate.getFullYear() + remaining, month % 12, 1).addDays(-1);    
          return [qbdate, qedate]
      }    

    function init_session_tasks_table() {
        var table = new SWDataTable("#source_tasks .card-body", "session_tasks_table"); //創建SWDataTable對象
        table.searching = false;
        table.paging = false;
        table.firstColSelected = true;
    
        table.orderBy = [['taskid', 'asc']];     //設置按taskno 升序排序，可以進行多字段排序，參考上面的重要屬性
        table.columns = [
            { field: "taskid", label: "TaskId", visible:false},
            { field: "task", label: gettext("Task") },
            { field: "progress", label: gettext("Progress")}
        ]
        table.setOptions({
            responsive: true,  //是否支持手機展開和隱藏列
            scrollY:"350px",
            columnDefs: [
                { "responsivePriority": 1, "className": "all", "targets": 2 },
                { "responsivePriority": 1, "className": "all", "targets": 3 },
            ],
            deferLoading: 0
        });        
        
        var session_tasks_datatable = table.init('/PMIS/task/t_list');  //根據以上設置好的屬性，初始化table1，數據來源於/server/tasks這個地址
        $("#source_tasks .card-body").data("table", table);
        $("#source_tasks .card-body").data("datatable", session_tasks_datatable);
        init_session_tasks_filter();
    }

    function init_session_tasks_filter() {
        var progress = new SWCombobox("progress", gettext('Progress'),
        [{label:"N:新工作",value:"N"},{label:"I:正在進行的工作",value:"I"},{label:"T:當天的工作",value:"T"},
        {label:"S:已經開始的工作",value:"S"},{label:"F:已完成工作",value:"F"},{label:"C:基本完成",value:"C"},
        {label:"NF:除F的工作",value:"NF"},{label:"H:被掛起的工作",value:"H"},{label:"R:復查",value:"R"}]);
        progress.setHorizontalDisplay(true)
        var priority = new SWCombobox("priority",gettext('Priority'),['888','8888','8889']);
        priority.setHorizontalDisplay(true)
        var class1 = new SWCombobox("class_field", gettext('Class'),[{label:"class1",value:"1"}, {label:"class2", value:"2"},{label:"Other", value:"3"}]);
        class1.setHorizontalDisplay(true)
        var hoperation = new SWCombobox("hoperation", gettext('Hoperation'), window.CommonData.TaskHOperation);       
        hoperation.setHorizontalDisplay(true)    
        var task_desc = new SWText("task","text",gettext('Task Desp'));
        task_desc.setHorizontalDisplay(true) 
        $("#source_tasks .filter .f_progress").append(progress.dom);
        $("#source_tasks .filter .f_priority").append(priority.dom);
        $("#source_tasks .filter .f_class").append(class1.dom);
        $("#source_tasks .filter .f_hoperation").append(hoperation.dom);
        $("#source_tasks .filter .f_progress").append(progress.dom);
        $("#source_tasks .filter .f_task_desc").append(task_desc.dom);
        var get_lang_code = $("#curr_language_code").val();
        if (get_lang_code == "en") {
            $("#source_tasks .filter.row").addClass("en_filter");
        }

        $("#source_tasks .filter .btn-clear").on("click", function(){        
            $("#source_tasks .filter .SWCombobox select").val('').selectpicker('refresh');
            $("#source_tasks .filter input").val('');
        });

        $("#source_tasks .filter .btn-search").on("click", function(){    
            var table = $("#source_tasks .card-body").data("table");
            var datatable = $("#source_tasks .card-body").data("datatable");            
            var init_custom_params_fun = $("#source_tasks .card-body").data("init_custom_params_fun");
            var filter = {"condition":"AND","rules":[],"not":false,"valid":true};            
            $("#source_tasks .filter .SWCombobox select, #source_tasks .filter input").each((index,el)=>{
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
                }
            });
            table.custom_params_fun = function () {                
                var query = init_custom_params_fun();
                query = JSON.parse(query.attach_query);
                query.rules.push(filter)
                return {attach_query: JSON.stringify(query)}
            } 
            datatable.search('').columns().search('').draw();  
            $("#source_tasks_search_collapse").collapse('hide')
        });
    }

    function init_month_desc() {
        var year = period.split("-")[0];
        var period_num = period.split("-")[1];
        //根據季度設置每個月份的英文描述
        var monthly_date = "{0}-{1}".format(year, period_num)
        var monthly_tabs = monthly_tab.find("li");
        var link = "a";
        var first_month = Date.parse("{0}-{1}".format(year, period_num*3 - 2)).toString("MMMM");
        var second_month = Date.parse("{0}-{1}".format(year, period_num*3 - 1)).toString("MMMM");
        var third_month = Date.parse("{0}-{1}".format(year, period_num*3)).toString("MMMM");
        if (SWApp.os.isMobile || checkMediaQuery())
            link = "a h6";
        else {
            $(".month-1").find("h2.month").text(gettext(first_month));
            $(".month-2").find("h2.month").text(gettext(second_month));
            $(".month-3").find("h2.month").text(gettext(third_month));
        }
        $(monthly_tabs[0]).find(link).text(gettext(first_month));
        $(monthly_tabs[1]).find(link).text(gettext(second_month));
        $(monthly_tabs[2]).find(link).text(gettext(third_month));
        //自動選中當前月份
        var current_index = (Date.today().getMonth())%3;
        $(monthly_tabs[current_index]).find("a").tab("show");
    }

    

    function init_goal_management() {
        var url = "/PMIS/goal/overall/goal_management";
        var params = {contact:contact, period:period};
        $.get(url, params, function(data){
            if (data.status) {                
                var quarterly = undefined;
                var monthly1 = undefined;
                var monthly2 = undefined;
                var monthly3 = undefined;
                var monthly1_weeklys = undefined;
                var monthly2_weeklys = undefined;
                var monthly3_weeklys = undefined;
                if ("quarterly" in data.data)
                    quarterly = data.data['quarterly'];
                if ('monthly-'+first_month_str in data.data && "data" in data.data['monthly-'+first_month_str])
                    monthly1 = data.data['monthly-'+first_month_str]['data']
                    monthly1_weeklys = data.data['monthly-'+first_month_str]
                if ('monthly-'+second_month_str in data.data && "data" in data.data['monthly-'+second_month_str])
                    monthly2 = data.data['monthly-'+second_month_str]['data']
                    monthly2_weeklys = data.data['monthly-'+second_month_str]

                if ('monthly-'+third_month_str in data.data && "data" in data.data['monthly-'+third_month_str])
                    monthly3 = data.data['monthly-'+third_month_str]['data']                
                    monthly3_weeklys = data.data['monthly-'+third_month_str];
                manager_quarterly_goal.load_source(quarterly);
                manager_monthly1_goal.load_source(monthly1);
                manager_monthly2_goal.load_source(monthly2);
                manager_monthly3_goal.load_source(monthly3);
                manager_weekly1_goal.load_source(monthly1_weeklys);
                manager_weekly2_goal.load_source(monthly2_weeklys);
                manager_weekly3_goal.load_source(monthly3_weeklys);
            }
        })
    }    

    function init_select_goal(target) {
        month_select_query = new SWSelectquery(".monthly-1_goals a.search");
        month_select_query.table.columns = [
            {field:"recordid",label:"recordid"},
            {field:"objective", label:"objective"},
            {field:"task", label:"task"},
            {field:"inc_id", label:"inc_id"}
        ]
        month_select_query.datasource = "/PMIS/goal/overall/select_appraisal_view";
        month_select_query.width(600);
        month_select_query.height(300);
        if (SWApp.os.isMobile || checkMediaQuery()) {
            month_select_query.width("calc(100% - 10px)");
            month_select_query.height("auto");
        }
        month_select_query.show_refresh_data = true;
        month_select_query.table.setOptions({
            columnDefs:[
                {
                    "targets": [3],
                    "visible": false
                }
            ]
        })
        month_select_query.custom_params = {contact:contact, period:period};
        month_select_query.on_selected_event = function(data) {
            var url = "/PMIS/goal/overall/add_overall_goal"
            var pk = data['inc_id'];
            var params = {pk:pk};
            $.get(url, params, function(data){
                if (data.status) {
                    init_monthly();
                    init_weekly();
                }else {
                    SWApp.popoverMsg($(self), "添加重要goal失敗");
                }
            })        
        }

        var year = period.split("-")[0];
        var period_num = period.split("-")[1];
        
        $(".monthly-1_goals a.search").on("click", function(){
            var index = $(this).closest(".tab-pane").index()
            var month_param = "{0}-{1}".format(year, period_num*3 - (2 - index))
            month_select_query.custom_params['month'] = month_param;
        })
    }

    function init_select_weekly_goal(target) {
        weekly_select_query = new SWSelectquery(".desc_week1 a.search");
        weekly_select_query.table.columns = [
            {field:"recordid",label:"recordid"},
            {field:"objective", label:"objective"},
            {field:"task", label:"task"},
            {field:"inc_id", label:"inc_id"}
        ]
        weekly_select_query.datasource = "/PMIS/goal/overall/select_weekly_view";
        weekly_select_query.height(300);
        weekly_select_query.width(600);
        weekly_select_query.show_refresh_data = true;
        weekly_select_query.table.setOptions({
            columnDefs:[
                {
                    "targets": [3],
                    "visible": false
                }
            ]
        })
        weekly_select_query.custom_params = {contact:contact, period:period};
        weekly_select_query.on_selected_event = function(data) {
            var url = "/PMIS/goal/overall/add_overall_goal"
            var pk = data['inc_id'];
            var params = {pk:pk};
            $.get(url, params, function(data){
                if (data.status) {
                    init_weekly();
                }else {
                    SWApp.popoverMsg($(self), "添加重要goal失敗");
                }
            })        
        }

        var year = period.split("-")[0];
        var period_num = period.split("-")[1];
        
        $(".desc_week1 a.search").on("click", function(){
            var index = $(this).closest(".tab-pane").index()
            var month_param = "{0}-{1}".format(year, period_num*3 - (2 - index))
            var wideget_title = $(this).closest(".widget").find(".widget-title").text();
            var weekly = wideget_title.replace("weekly", "").trim();
            weekly_select_query.custom_params['month'] = month_param;
            weekly_select_query.custom_params['weekly'] = weekly;
        })        
    }


    function init_monthly() {
        var url = "/PMIS/goal/overall/monthly";
        var params = {contact:contact, period:period};
        
        $.get(url, params, function(data){
            if (data.status) {
                monthly_dom.find("li").remove();
                for (var i = 0; i < Object.keys(data.data).length; i++) {
                    var monthly = data.data[Object.keys(data.data)[i]];
                    var item = $(monthly_templ);
                    var j = 0;
                    for (task of monthly) {
                        var local_item = item.clone();
                        var local_task = task;
                        local_task["task"] = "{0}. {1}".format(j+1,local_task.task);
                        $(monthly_dom[i]).append(local_item.prop("outerHTML").render(local_task));
                        j = j + 1
                    }
                }
            }
        })
    }

    function init_eidt_user_goal() {
        monthly_dom.on("click","a.del", function(){
            var self = this;
            var url = "/PMIS/goal/overall/del_overall_goal"
            var pk = $(this).closest(".task").find("span").attr("pk");
            var params = {pk:pk};
            $.get(url, params, function(data){
                if (data.status) {
                    init_monthly();
                    init_weekly();
                }else {
                    SWApp.popoverMsg($(self), "取消重要goal失敗");
                }
            })
        });
        
        weekly_dom.find(".task-inner").on("click", "a.del", function() {
            var self = this;
            var url = "/PMIS/goal/overall/del_overall_goal"
            var pk = $(this).closest(".task").find("span").attr("pk");
            var params = {pk:pk};
            $.get(url, params, function(data){
                if (data.status) {
                    init_weekly();
                }else {
                    SWApp.popoverMsg($(self), "取消重要goal失敗");
                }
            });
        });
    }    

    function init_weekly() {
        var url = "/PMIS/goal/overall/weekly";
        var params = {contact:contact, period:period};
        $.get(url, params, function(data){
            if (data.status) {
                var weeklys = weekly_dom.find(".task-inner");
                weeklys.find("li").remove();
                for (var i = 0; i < Object.keys(data.data).length; i++) {
                    var group = data.data[Object.keys(data.data)[i]];
                    for (var j = 0; j < Object.keys(group).length; j++) {
                        var weekly = group[Object.keys(group)[j]];
                        for (task of weekly) {
                            var local_item = $(weekly_templ).clone();
                            $($(weekly_dom[i]).find(".task-inner")[j]).append(local_item.prop("outerHTML").render(task));
                        }
                    }
                }
            }
        })
    }

   

    init_data();
    init_session_tasks_table();
    init_goal_management();
    /**init_monthly();
    init_weekly();
    init_select_goal();
    init_select_weekly_goal();
    init_eidt_user_goal();*/

    getBrowser();

    $(window).on('orientationchange', function () {
        location.reload();
    });

    function getBrowser(){
        var isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
        var isSafari = /Safari/.test(navigator.userAgent) && /Apple Computer/.test(navigator.vendor);
        if (isChrome) {
            console.log("Chrome!");
        }
        if (isSafari) {
            $("#source_tasks .card-body").addClass("iosCheckbox");
        }
    }

    function update_task(self) {
        var pk = $(self).attr("pk")
        init_task(pk);
    }

    $("#source_tasks").on('shown.bs.collapse', function () {
        $($.fn.dataTable.tables(true)).DataTable().columns.adjust();
    });
    $(".wrapper").on(
        {
            dblclick:function(){
                update_task(this);
            },
            longpress:function() {
                update_task(this);
            }
        },
        ".task-info"
    );        
    $("#relation_task .related_tasks").on(
        {
            dblclick:function(){
                update_task(this);
                $(".modal[id^='add-task']").css('z-index', '1060');
            },
            longpress:function() {
                update_task(this);
            }
        },
        ".task-info"
    );

    if (SWApp.os.isMobile || checkMediaQuery()) {
        $("#qGoals_mobile .week-filter .nav-item").on("click", "a.week-item", function(e) {
            var self = this;
            var target_dom = $(e.target).attr("href");
            var collapse_target = $(target_dom).find(".btn").attr("data-target");
            var isShow = $(collapse_target).hasClass("show");
            if (!isShow) {
                $(self).closest(".blog-quota").find(collapse_target).collapse('show');
            }        
        });
    };

    $('[data-toggle="flatpickr"]').flatpickr();
});

function checkMediaQuery() {
    var mediaQuery = window.matchMedia("(max-width: 991.98px)");
    return mediaQuery.matches;
}