$.fn.template = function() {
    this.dom = $(this);
    this.solt = {};
    this.solt_render = {};
    this.params = {};
    this.action = {};
    this.data = {};
    var init_params = undefined;
    var self = this;
    this.dom.find("[solt_name]").each((index, element)=>{
        var name = $(element).attr("solt_name");
        self.solt[name] = $(element);
    })
    this.dom.find("[tmpl_action]").each((index, element)=>{
        var name = $(element).attr("tmpl_action");
        self.action[name] = $(element);
    });
    this.dom.find("[tmpl_params]").each((index, element)=>{
        var name = $(element).attr("tmpl_params");
        for(var item of name.split(",")) {
            if (!$(element).is(`[${item}]`)) {
                $(element).attr(item, "[[{0}]]".format(item));
            }
            self.params[item] = $(element);
        }        
    });
    if (this.dom.is("[tmpl_params]")) {
        var name = self.dom.attr("tmpl_params");
        for(var item of name.split(",")) {
            if (!self.dom.is(`[${item}]`)) {
                self.dom.attr(item, "[[{0}]]".format(item));
            }
            self.params[item] = self.dom;
        }        
    }
    /***
     * 功能描述：初始化模板信息
     */
    this.init = function(params, with_data=false) {
        init_params = params;
        if (params == undefined)
            return;
        if ("solt" in params)
        for(const [key, value] of Object.entries(params.solt)) {
            if (key in self.solt) {
                if (!with_data)
                    self.solt[key].empty();
                if (typeof params['solt'][key] === 'function' ) {
                    self['solt_render'][key] = params['solt'][key];
                }else 
                    self.solt[key].append(params['solt'][key])
            }
        }
        if ("bind_event" in params) {
            var func = params["bind_event"];
            if (func != undefined)
                func.call(null, self);            
        }
    }
    this.clone = function(withDataAndEvents=false, deepWithDataAndEvents=false) {
        var tmpl_clone = $.extend(true, self.dom.clone(withDataAndEvents, deepWithDataAndEvents), self);
        return tmpl_clone;

    }
    this.render = function(data) {
        var temp_dom = self.dom.clone();
        for(const [key,vlaue] of Object.entries(self.solt_render)) {
            var func = self.solt_render[key];
            if (func != undefined) {
                var html = func.call(null, data);
                temp_dom.find(`[solt_name='${key}']`).html(html);
            }
        }
        var tmpl = $(temp_dom.prop("outerHTML").render(data)).template();
        tmpl.init(init_params,true);
        tmpl.dom.data("tmpl", tmpl);
        tmpl.dom.data("data", data);
        return tmpl.dom;
    }
    return this;
}

var TemplateWrapper = function() {
    var all_template = $("#templates");
    this.tmpls = {}
    var self = this;
    all_template.find("[tmpl_name]").each((index, element)=>{
        var name = $(element).attr("tmpl_name");
        self.tmpls[name] = $(element).template();
    });
    for(const [key, value] of Object.entries(self.tmpls)) {
        //刪除子template
        self.tmpls[key].dom.find("[tmpl_name]").remove();
    }
}

var tmpl = new TemplateWrapper().tmpls;

var TaskUI = function() {
    this.container = $("[container_name='Task']");
    this.task_filter_dom = $(".task_filter");
    this.tmpl = tmpl["task"];
    var self = this;
    this.show_tasks = function(data) {
        self.container.empty();
        self.task_filter_dom.data("all_data", data);
        var data = this.task_filter(data);
        for(var item of data) {
            if (item.planbdate != null)
                item.planbdate = Date.parse(item.planbdate).toString("yyyy-MM-dd");
            if (item.planedate != null)
                item.planedate = Date.parse(item.planedate).toString("yyyy-MM-dd");
            var task_dom = self.tmpl.render(item)
            self.container.append(task_dom);
            task_dom.on("dblclick", function(){
                self.update_task($(this));
            });
        }
    }

    this.update_task = function(dom) {
        var inc_id = dom.data("data").inc_id;
        init_task(inc_id);
    }

    this.task_filter = function(data){
        var must_have = self.task_filter_dom.find(".dropdown-item.selected[name='mh']");
        var nf = self.task_filter_dom.find(".dropdown-item.selected[name='nf']");
        var cf = self.task_filter_dom.find(".dropdown-item.selected[name='cf']");
        var process = "C";
        var progress = ['C','F'];
        var filter_data = [];
        for (var item of data) {
            var local_process = must_have.length > 0 ? item.process: "C";
            var local_progress = nf.length > 0 ? item.progress:"";
            var cf_progress = cf.length > 0 ? item.progress : "C";
            if (process == local_process && progress.indexOf(local_progress) == -1 && 
                progress.indexOf(cf_progress) != -1)
                filter_data.push(item);
        }
        return filter_data;
    }
}

var SessionUI = function() {
    this.tmpl = tmpl['session'];
    var self = this;
    this.GoalUI = undefined;
    this.taskUI = new TaskUI();
    this.init = function() {
        this.tmpl.init({"bind_event":self.tmpl_bind_event})
        $("#close_back").on("click", function(){
            var contact = getParamFromUrl("contact");
            var period = getParamFromUrl("period");    
            window.location.href = `/looper/goal/overall/quarterly_goal?contact=${contact}&period=${period}`;
        });
    }
    this.tmpl_bind_event = function(tmpl) {
        tmpl.action["view"].on("click", function(e){
            e.preventDefault();
            e.stopPropagation();
            var sessionid = tmpl.params["sessionid"].attr("sessionid");
            var arr = sessionid.split("-");
            var pid = arr[0];
            var tid = arr[1];
            var is_init = $(this).data("init") != undefined ? true : false;
            if (!is_init) {
                if ($("#expend_task_list").is(":visible")) {
                    $("#expend_task_list").click();
                }
            }else {
                $(this).removeData("init");
            }
            $.ajax({
                url:"/PMIS/session/search_task",
                data:{pid:pid,tid:tid},
                success:function(data){
                    if(data.status) {
                        self.taskUI.show_tasks(data.data);
                    }
                }
            });
        });
        tmpl.dom.on("click", function(e){
            e.preventDefault();
            e.stopPropagation();
            var sessionid = tmpl.dom.data("data").sessionid;
            var recordid = tmpl.dom.data("data").recordid;
            window.open(`/devplat/sessions?recordid=${recordid}&menu_id=mi_${sessionid}#Requirements`, "_blank");
        });
        tmpl.action["unlink"].on("click", function(e){
            e.preventDefault();
            e.stopPropagation();
            self.unlink_session(tmpl);
        });
    }
    this.show_session = function(container, data) {
        var all_sessions = ""
        return new Promise((resolve, reject)=>{
            if (data == undefined) {
                var goal_tmpl = $(container).data("tmpl");
                goal_tmpl.solt['sessions'].empty();
                var sessions = goal_tmpl.dom.data("data").sessions;
                var url = "/PMIS/session/task_list"
                var local_session = `"` + sessions.replaceAll(",",`","`) + `"`;
                var params = {draw:0,length:-1,start:0,attach_query: `{"condition":"AND","rules":[{"id":"sessionid","field":"sessionid","type":"string","input":"text","operator":"in","value":[${local_session}]}],"not":false,"valid":true}`};
                $.get(url, params, function(result){
                    resolve(result.data);
                });
            }else {
                resolve(data);
            }
        }).then((sessions)=>{
            var goal_tmpl = $(container).data("tmpl");
            goal_tmpl.solt['sessions'].empty();
            for(var session of sessions) {
                goal_tmpl.solt['sessions'].append(self.tmpl.render(session));
            }
            return true;
        });
    }

    this.unlink_session = function(tmpl) {
        var goal_tmpl = tmpl.dom.closest("[tmpl_name='goal']").data("tmpl");
        var sessionid = tmpl.dom.data("data").sessionid;
        var old_sessions = goal_tmpl.dom.data("data").sessions;
        var pk = goal_tmpl.dom.data("data").inc_id;
        var session = new Set()
        if (old_sessions != "") {
            session = new Set(old_sessions.split(","));
        }
        session.forEach((item)=>{
            if (item == sessionid) {
                session.delete(item);
            }
        });
        var local_self = this;
        self.GoalUI.form.on_after_init = function(data) {
            self.GoalUI.form_container.find("input[name='sessions']").val(Array.from(session).join(','));
            self.GoalUI.form.save_data(tmpl.solt['session']).then((status)=>{
                if (status) {
                    goal_tmpl.dom.data("data").sessions = Array.from(session).join(',');
                    tmpl.dom.remove();
                }
            });
        }        
        self.GoalUI.form.set_pk(pk);
        self.GoalUI.form.init_data();       //調用該方法, 將立即執行新增或修改動作從後臺讀取數據，並填充到Form表單
    }    
}

var Goal = function() {
    this.container = $("[container_name='goal']");
    this.form_container = $('#goal_form .form');
    this.simulation_container = $("#goal_simulation .modal-body");
    this.tmpl = tmpl['goal'];
    this.tmpl_params = {solt:{goal_body:this.goal_body_render}};
    this.session_Selectquery = undefined;
    this.after_init = undefined;
    this.goals_data = [];
    this.sessionUI = new SessionUI();
    this.taskUI = new TaskUI();
    var self = this;
    this.init = function() {
        self.init_form();
        this.sessionUI.init();
        this.tmpl_params.solt.goal_body = self.goal_body_render;
        this.tmpl_params['bind_event'] = self.tmpl_bind_event;
        self.tmpl.init(self.tmpl_params);
        this.sessionUI.GoalUI = self;
        self.init_goal();
        self.init_link_session();
        self.init_add_form();
        $(".task_filter .dropdown-item").on("click", function(){
            var name  = $(this).attr("name");
            if (!$(this).hasClass("selected")) {
                if (name == "nf") {
                    $(".task_filter .dropdown-item.selected[name='cf']").removeClass("selected");
                } if (name == 'cf') {
                    $(".task_filter .dropdown-item.selected[name='nf']").removeClass("selected");
                }
            }
            if ($(this).hasClass("selected")) {
                $(this).removeClass("selected");
            }else {
                $(this).addClass("selected");
            }
            var data = $(".task_filter").data("all_data");
            self.taskUI.show_tasks(data == undefined ? [] : data);
        })
    }
    this.tmpl_bind_event = function(tmpl) {
        tmpl.action["link_session"].on("click", function(e){
            e.stopPropagation()
            self.session_Selectquery.dom.data("goal_dom", tmpl.dom);
            self.session_Selectquery.show();
        });
        tmpl.action["edit_goal"].on("dblclick", function(e){
            e.preventDefault();
            e.stopPropagation();
            self.edit_goal(tmpl);
        });
        tmpl.on("dblclick", function(e){
            e.preventDefault();
            e.stopPropagation();
            self.show_simulation($(this).data("tmpl"));
        });
        tmpl.action['del_goal'].on("click", function(e){
            e.preventDefault();
            e.stopPropagation();
            self.delete_goal(tmpl);
        });
        tmpl.action["collapse"].on("click", function(e){
            e.stopPropagation();
            self.collapse_session(tmpl);
        }); 
    }
    this.goal_body_render = function(goal) {
        var html = "";
        var lines = goal.goal_body.replace(/\r\n/g, "\r").replace(/\n/g, "\r").split(/\r/);            
        for(var line of lines) {
            html += `<p>${line}</p>\r\n`;
        }
        return html;
    }
    this.init_goal = function() {
        var contact = getParamFromUrl("contact");
        var period = getParamFromUrl("period");
        var url = `/looper/goal/project_goal/get_project_goal?contact=${contact}&period=${period}`;
        $.get(url, function(result){
            if (result.status) {
                self.show_goals("init", undefined, result.data);
            }
        });
    }
    this.show_goals = function(show_type, dom, data) {
        var handle_goal = function(goal) {
            var desc = goal.goaldesc;
            var lines = desc.replace(/\r\n/g, "\r").replace(/\n/g, "\r").split(/\r/);            
            var goal_header = lines[0];
            var goal_body = desc.replace(goal_header, "");
            var data = $.extend(goal,{goal_header:goal_header, goal_body:goal_body})
            var goal_dom = self.tmpl.render(data)
            return goal_dom;
        }
        if (show_type == "init") {
            this.container.empty();            
            for(var i = 0; i < data.quarterly.length; i++) {
                var goal =  data.quarterly[i];
                var goal_dom = handle_goal(goal);
                this.container.append(goal_dom);
                var sessions = []
                if (goal.sessions != null) {
                    sessions = goal.sessions.split(",");
                }
                //默認選中第一個，顯示第一個的任務
                if (i==0) {
                    var goal_tmpl = goal_dom.data("tmpl");
                    self.sessionUI.show_session(goal_dom, data.sessions.filter((a)=>{return sessions.indexOf(a.sessionid) != -1})).then((status)=>{
                        goal_tmpl.dom.click();
                        var first_session_dom = goal_tmpl.dom.find("[tmpl_name='session']:eq(0)");
                        if (first_session_dom.length > 0) {
                            $(first_session_dom[0]).data("tmpl").action['view'].data("init", true);
                            $(first_session_dom[0]).data("tmpl").action['view'].click();
                        }
                    });
                }
                else
                    self.sessionUI.show_session(goal_dom, data.sessions.filter((a)=>{return sessions.indexOf(a.sessionid) != -1}));
            }
        }else if (show_type == "update") {
            var new_dom = handle_goal(data);
            if (dom.data("data").sessions == data.sessions) {
                dom.find("[tmpl_name='session']").detach().appendTo(new_dom.data("tmpl").solt["sessions"]);
                dom.replaceWith(new_dom);
            }else {
                dom.replaceWith(new_dom);
                self.sessionUI.show_session(new_dom, undefined);
            }
        }else if (show_type == "add") {
            var goal_dom = handle_goal(data);
            this.container.append(goal_dom);
            goal_dom[0].scrollIntoView();
        }else if (show_type == "delete") {
            dom.remove();
        }
    }

    this.init_form = function() {
        var goalid = new SWText("goalid","hidden", "",10);
        self.form_container.append(goalid.dom);
        self.form_container.append(new SWText("contact","hidden", "").dom);
        self.form_container.append(new SWText("period","hidden", "").dom);
        self.form_container.append(new SWText("goaltype","hidden", "","Q").dom);
        self.form_container.append(new SWText("sessions","hidden", "").dom);
        self.form_container.append(new SWText("allocateuser","hidden",gettext('Personnel Allocation'),"1").dom);
        var recordid_cmpt = new SWCombobox("recordid", gettext('RecordID'), "/PMIS/subproject/get_all_recordid", undefined, 'recordid','CompDesc');
        recordid_cmpt.input_dom.attr("data-live-search", "true");
        self.form_container.append(recordid_cmpt.dom);
        var editor = new SWTextarea("goaldesc","", 5).setAutoSize(true);
        editor.dom.find("label").hide();
        self.form_container.append(editor.dom);
        

        self.form = new SWBaseForm("#goal_form");
        self.form.pk_in_url = false;
        self.form.update_url = "/PMIS/goal/overall/update_goal_management/[[pk]]"
    }
    this.init_add_form = function() {
        var contact = getParamFromUrl("contact");
        var period = getParamFromUrl("period");
        var local_container = $("#add_goal");
        var goalid = new SWText("goalid","hidden", "",10);
        local_container.find(".modal-body").append(goalid.dom);
        local_container.find(".modal-body").append(new SWText("contact","hidden", "", contact).dom);
        local_container.find(".modal-body").append(new SWText("period","hidden", "",period).dom);
        local_container.find(".modal-body").append(new SWText("goaltype","hidden", "","Q").dom);
        var recordid_cmpt = new SWCombobox("recordid", gettext('RecordID'), "/PMIS/subproject/get_all_recordid", undefined, 'recordid','CompDesc')
        recordid_cmpt.input_dom.attr({"data-live-search": "true","data-size":"4"});
        local_container.find(".modal-body").append(recordid_cmpt.dom);
        var editor = new SWTextarea("goaldesc","", 5);
        editor.dom.find("label").hide();
        local_container.find(".modal-body").append(editor.dom);

        if (SWApp.os.isMobile || SWApp.os.isTablet) {
            local_container.find(".modal-body").width($(window).width() - 10);
        } else {
            local_container.find(".modal-body").width(800);
        }    

        self.add_form = new SWBaseForm("#add_goal");
        self.add_form.pk_in_url = false;
        self.add_form.create_url = "/PMIS/goal/overall/create_goal_management"
        self.add_form.update_url = "/PMIS/goal/overall/update_goal_management/[[pk]]"
        $('#add_goal').on('show.bs.modal', function () {
            editor.input_dom.val("");
        });
        $('#add_goal').on('shown.bs.modal', function () {
            self.add_form.set_pk(undefined);
            self.add_form.init_data();
        });
        self.add_form.on_after_init = function(data) {
            local_container.find("input[name='contact']").val(contact);
            local_container.find("input[name='period']").val(period);
            local_container.find("input[name='goaltype']").val('Q');
            local_container.find("input[name='goaldesc']").val('');
        }
        self.add_form.on_after_save = function(data) {
            self.show_goals("add",undefined, data);
            $("#add_goal").modal("hide")
        }
    }

    this.init_link_session = function() {
        self.session_Selectquery = new SWSelectquery("");  //設置Search按鈕為觸發標籤
        $(self.session_Selectquery.dom).find(".modal-title").text(gettext("Search"));
        self.session_Selectquery.table.columns = [
            { field: "sessionid", label: gettext('Session ID') },
            { field: "sdesp", label: gettext('Description') },
            { field: "recordid", label: "recordid",visible:false },
        ];    
        if (SWApp.os.isMobile || SWApp.os.isTablet) {
            self.session_Selectquery.height($(window).height() - 236 - 10);
            self.session_Selectquery.width($(window).width() - 10);
        } else {
            self.session_Selectquery.height(600);
            self.session_Selectquery.width(800);
        }    
        self.session_Selectquery.datasource = '/PMIS/session/session_list_all';
        self.session_Selectquery.on_selected_event = function(data) {
            var goal_dom  = self.session_Selectquery.dom.data("goal_dom");
            var old_sessions = goal_dom.data("data").sessions;
            var pk = goal_dom.data("data").inc_id;
            var session = new Set()
            if (old_sessions != null && old_sessions != "") {
                session = new Set(old_sessions.split(","));
            }
            session.add(data.sessionid);
            self.form.on_after_init = function(data) {
                self.form_container.find("input[name='sessions']").val(Array.from(session).join(','));
                self.form.save_data(goal_dom.data("tmpl").action['link_session']).then((status)=>{
                    if (status) {
                        goal_dom.data("data").sessions = Array.from(session).join(',');
                        self.sessionUI.show_session(goal_dom, undefined);
                    }
                });
            }        
            self.form.set_pk(pk);
            self.form.init_data();                 
        }    
    }
    this.delete_goal = function(local_tmpl) {
        SWHintMsg.showToastModal(gettext("Warning message"), gettext("Confirm deletion of Goal?"), "confirm").then((value) => {
            if (value) {
                var pk = local_tmpl.dom.data("data").inc_id;
                var url = "/PMIS/goal/overall/del_goal_management/" + pk;
                $.ajax({
                    type:"POST",
                    url:url,
                    beforeSend: function (request) {
                        request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    },    
                    success:function(result){
                        if (result.status) {
                            local_tmpl.dom.remove();
                        }
                    }
                });        
            }
        });
    }

    this.edit_goal = function(local_tmpl){
        //先清除之前打開的編輯編輯
        for(var d of local_tmpl.dom.siblings()) {
            var container = $(d).data("tmpl").action["edit_goal"];
            if (container.next().length > 0) {
                container.next().remove();
                container.remove("d-none").addClass("d-flex");
            }
        }
        var edit_goal_tmpl = tmpl['edit_goal'].clone();
        var local_container = local_tmpl.action['edit_goal'];
        var recordid = local_tmpl.dom.data("data").recordid;
        var goaldesc = local_tmpl.dom.data("data").goaldesc;
        var user_num = local_tmpl.dom.data("data").allocateuser;
        var recordid_cmpt = new SWCombobox("recordid", gettext('RecordID'), "/PMIS/subproject/get_all_recordid", recordid, 'recordid','CompDesc');
        recordid_cmpt.input_dom.attr("data-live-search", "true");
        recordid_cmpt.setHorizontalDisplay(true);
        var editor = new SWTextarea("goaldesc","", 5, goaldesc).setAutoSize(true);
        var allocateuser = new SWText("allocateuser","number",gettext('Personnel Allocation'), user_num);
        allocateuser.setHorizontalDisplay(true);
        editor.dom.find("label").hide();
        edit_goal_tmpl.solt['body'].empty();
        edit_goal_tmpl.solt['body'].append(editor.dom);
        var row = new SWRow();
        row.addComponent(recordid_cmpt);
        row.addComponent(allocateuser)
        edit_goal_tmpl.solt['body'].append(row.dom);
        
        edit_goal_tmpl.action["save"].on("click", function(){
            var target = $(this);
            if (editor.input_dom.val() != local_tmpl.dom.data("data").goaldesc || 
                allocateuser.input_dom.val() != local_tmpl.dom.data("data").allocateuser ||
                recordid_cmpt.input_dom.val() != local_tmpl.dom.data("data").recordid) {
                var pk = local_tmpl.dom.data("data").inc_id;
                self.form.on_after_init = function(data) {
                    self.form_container.find("textarea[name='goaldesc']").val(editor.input_dom.val());
                    self.form_container.find("input[name='allocateuser']").val(allocateuser.input_dom.val());
                    self.form_container.find("select[name='recordid']").val(recordid_cmpt.input_dom.val());
                    self.form.save_data(target).then((status)=>{
                        if (status) {
                            local_tmpl.dom.data("data").goaldesc = editor.input_dom.val();
                            local_tmpl.dom.data("data").allocateuser = allocateuser.input_dom.val();
                            local_tmpl.dom.data("data").recordid = recordid_cmpt.input_dom.val();
                            self.show_goals("update", local_tmpl.dom, local_tmpl.dom.data("data"));
                        }
                    });
                } 
                self.form.set_pk(pk);
                self.form.init_data();
            }else {
                local_container.remove("d-none").addClass("d-flex");
                local_container.next().remove();
            }
        });
        edit_goal_tmpl.action["calcel"].on("click", function(){
            local_container.remove("d-none").addClass("d-flex");
            local_container.next().remove();
        });
        edit_goal_tmpl.dom.on("dblclick", function(e){
            e.preventDefault();
            e.stopPropagation();
        });
        local_container.removeClass("d-flex").addClass("d-none");
        local_container.after(edit_goal_tmpl.dom);
        editor.input_dom.trigger("change");
    }    
    this.show_simulation = function(local_tmpl) {
        var default_data = {total_qty:0, finish_qty:0,unfinish_qty:0,left_days:0,ratio:0,expected_date:Date.today().toString("yyyy-MM-dd"),
            total_qty_simu:0, finish_qty_simu:0,unfinish_qty_simu:0,left_days_simu:0,ratio_simu:0,expected_date_simu:Date.today().toString("yyyy-MM-dd")}        
        var sessions = local_tmpl.dom.data("data").sessions;
        var pk = local_tmpl.dom.data("data").inc_id;
        if (sessions == null) {
            self.simulation_container.empty();
            self.simulation_container.append(tmpl['simulation'].render(default_data));
        }else {
            var url = "/looper/goal/project_goal/analysis_simulation"
            var params = {pk:pk};
            $.get(url, params, function(result){
                if (result.data['ratio'] > 0)
                    result.data['ratio'] = result.data['ratio'].toFixed(2) * 100;
                if (result.data['ratio_simu'] > 0)
                    result.data['ratio_simu'] = result.data['ratio_simu'].toFixed(2) * 100;
                self.simulation_container.empty();
                self.show_simulation_barchart(result.data);
                self.simulation_container.append(tmpl['simulation'].render(result.data));
            });
        }
        if (SWApp.os.isMobile || SWApp.os.isTablet) {
            $("#goal_simulation").find(".modal-dialog").height($(window).height() - 236 - 10);
            $("#goal_simulation").find(".modal-dialog").width($(window).width() - 10);
        } else {
            $("#goal_simulation").find(".modal-dialog").height(600);
            $("#goal_simulation").find(".modal-dialog").width(800);
        }
        $("#goal_simulation").modal("show");
    }

    this.show_simulation_barchart = function(data) {
        var local_container = $(`<div class="bar_chart"></div>`);
        self.simulation_container.append(local_container);
        var bar_chart = new SWBarChart_AC(local_container,"過去一年的銷量");
        var series_data = [];
        series_data.push((Date.parse(data.expected_date) - Date.parse(Date.today().toString("yyyy-MM-dd")))/(1000 * 60 * 60 * 24));
        series_data.push((Date.parse(data.expected_date_simu) - Date.parse(Date.today().toString("yyyy-MM-dd")))/(1000 * 60 * 60 * 24));
        bar_chart.height = 200;
        bar_chart.horizontal = true;
        bar_chart.setOptions({
            yaxis: {
                labels: {
                    style: {
                        fontSize: '14px'
                    }
               }
           },
           tooltip: {
            y: {
                formatter: function(value){
                    return "到{0}完成,還有{1}天".format(Date.today().addDays(value).toString("yyyy-MM-dd"), value);
                },
                title: {
                    formatter: function(seriesName){
                        return "";
                    }
                },
                },                   
            }
        });
        bar_chart.load({
             series: [{
                 data: series_data
              }],        
            categories: ['Estimated','Simulation']
       });                     
    }

    this.collapse_session = function(local_tmpl) {
        local_tmpl.action["collapse"].attr("aria-expanded", local_tmpl.action["collapse"].attr("aria-expanded") == "false" ? "true" : "false");
        local_tmpl.action["collapse"].closest(".card").find(".collapse").collapse("toggle");
    }
}

$(function() {
    var goal = new Goal();
    var init = function() {
        goal.init();
    }

    init();
    $("title").html(gettext('Project Goals'));
})