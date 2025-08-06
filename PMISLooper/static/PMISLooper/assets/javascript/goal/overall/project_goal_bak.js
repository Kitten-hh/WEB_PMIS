var Goal = function() {
    this.container = $("#Goal");
    this.form_container = this.container.find(".card-body form");
    this.form = undefined;
    this.session_Selectquery = undefined;
    this.after_init = undefined;
    this.pk = getParamFromUrl("pk");
    var self = this;
    this.init = function() {
        self.init_form();
        self.init_link_session();
    }
    this.init_form = function() {
        var goalid = new SWText("goalid","hidden", "",10);
        self.form_container.append(goalid.dom);
        self.form_container.append(new SWText("contact","hidden", "").dom);
        self.form_container.append(new SWText("period","hidden", "").dom);
        self.form_container.append(new SWText("goaltype","hidden", "","Q").dom);
        self.form_container.append(new SWText("sessions","hidden", "").dom);
        var editor = new SWTextarea("goaldesc","", 5).setAutoSize(true);
        editor.dom.find("label").hide();
        self.form_container.append(editor.dom);

        self.form = new SWBaseForm("#Goal");
        self.form.pk_in_url = false;
        self.form.update_url = "/PMIS/goal/overall/update_goal_management/[[pk]]"
        self.form.set_pk(self.pk);
        self.form.init_data();       //調用該方法, 將立即執行新增或修改動作從後臺讀取數據，並填充到Form表單
        self.form.on_after_init = function(data) {
            $("#Goal textarea").trigger("change");
            if (self.after_init != undefined)
                self.after_init(data);
        }
        self.form.auto_save(true);
    }

    this.init_link_session = function() {
        self.session_Selectquery = new SWSelectquery("#link_session");  //設置Search按鈕為觸發標籤
        self.session_Selectquery.table.columns = [
            { field: "sessionid", label: "sessionid" },
            { field: "sdesp", label: "desc" },
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
            var old_sessions = self.form_container.find("input[name='sessions']").val();
            var session = new Set()
            if (old_sessions != "") {
                session = new Set(old_sessions.split(","));
            }
            session.add(data.sessionid);
            self.form_container.find("input[name='sessions']").val(Array.from(session).join(','));
            self.form.save_data("#link_session").then((status)=>{
                if (status) {
                    if (self.after_init != undefined) {
                        self.after_init({sessions:Array.from(session).join(',')});
                    }
                }
            })
        }    
    }

    this.unlink_session = function(sessionid) {
        var old_sessions = self.form_container.find("input[name='sessions']").val();
        var session = new Set()
        if (old_sessions != "") {
            session = new Set(old_sessions.split(","));
        }
        session.forEach((item)=>{
            if (item == sessionid) {
                session.delete(item);
            }
        });
        self.form_container.find("input[name='sessions']").val(Array.from(session).join(','));
        self.form.save_data("#link_session").then((status)=>{
            if (status) {
                if (self.after_init != undefined) {
                    self.after_init({sessions:Array.from(session).join(',')});
                }
            }
        })        
    }
}
var Sessions = function() {
    this.container = $("#Sessions");
    this.session_container = this.container.find(".card-body");
    this.boardlist = undefined;
    this.unlink_session_event = undefined;
    var self = this;
    this.init = function() {
    }

    this.init_sessions  = function(sessions) {
        if (sessions == null) {
            self.init_session_board([]);
        }else {
            var url = "/PMIS/session/task_list"
            var local_session = `"` + sessions.replace(",",`","`) + `"`;
            var params = {draw:0,length:-1,start:0,attach_query: `{"condition":"AND","rules":[{"id":"sessionid","field":"sessionid","type":"string","input":"text","operator":"in","value":[${local_session}]}],"not":false,"valid":true}`};
            $.get(url, params, function(result){
                self.init_session_board(result.data);
            });
        }
    }

    this.init_session_board = function(data) {
        self.session_container.empty();
        var header_title = `<span class="recordid">[[recordid]]</span><span class="ml-2 sessionid">[[sessionid]]</span>`;
        var header_sub_title = `<h6 class="item-header-subtitle card-subtitle text-dark">
            <div class="ppsp"><span class="">[[planbdate]] / [[planedate]]</span><span class="ml-2 badge badge-subtle badge-dark font-size-lg">[[progress]]</span>
            <a href="javascript:void(0);" class="unlink ml-1" sessionid="[[sessionid]]"><i class="fa fa-unlink"></i></a>
            </div>
            </h6>`;
        var quarterly = "{0}-{1}".format(Date.today().format('yyyy'), parseInt(Date.today().getMonth()/3) + 1);
        for(var item of data) {
            if (Date.parse(item["planbdate"]) != null)
                item["planbdate"] = Date.parse(item["planbdate"]).toString("yyyy-MM-dd");
            if (Date.parse(item["planedate"]) != null)
                item["planedate"] = Date.parse(item["planedate"]).toString("yyyy-MM-dd");
        }
        self.boardlist = new SWBoardlist("Active Sessions", data,
        "", header_title, header_sub_title,"sdesp","taskc","taskqty");
        self.session_container.append(self.boardlist.dom);

        self.boardlist.dom.find(".task-body").on("click", ".card-footer .right", function(e){
            e.preventDefault(); //阻止按鈕默認動作
            e.stopPropagation();
            var sessionid = $(this).closest(".card").find(".sessionid").text();
            init_task(undefined, {sessionid:sessionid});
        });

        self.boardlist.dom.find(".task-body").on("click", ".card-footer .left", function(e){
            e.preventDefault(); //阻止按鈕默認動作
            e.stopPropagation();            
            var session_dom = $(this).closest(".task-issue")
            var sessionid = session_dom.find(".sessionid").text();
            var arr = sessionid.split("-");
            pid = arr[0];
            tid = arr[1];
            var self = this;
            if (session_dom.next().hasClass("task-collapse")) {
                var collapse_dom = session_dom.next();
                collapse_dom.collapse('hide')
                collapse_dom.remove();
                return;
            }
            $.ajax({
                url:"/PMIS/session/search_task",
                data:{pid:pid,tid:tid},
                success:function(data){
                    if(data.status) {
                        session_dom.data("data", data.data);
                        show_task(data.data, self)
                    }
                }
            });
            function show_task(data, self, is_init=true) {
                var dom = $("#tasklist").clone();
                dom.removeAttr("id")
                var item = dom.find(".task-item").clone();
                dom.empty();
                if (is_init) {
                    show_filter(dom);
                }else {
                    dom = session_dom.next();
                    dom.find(".task-item").remove();
                }
                for(task of data) {
                    var local_item = item.clone();
                    var local_task = task;
                    if (Date.parse(local_task["planbdate"]) != null)
                        local_task["planbdate"] = Date.parse(local_task["planbdate"]).toString("yyyy-MM-dd");
                    if (Date.parse(local_task["planedate"]) != null)
                        local_task["planedate"] = Date.parse(local_task["planedate"]).toString("yyyy-MM-dd");                
                    dom.append(local_item.prop("outerHTML").render(local_task))
                }
                if (is_init) {
                    $(self).closest(".task-issue").after(dom);
                    dom.show();
                    dom.collapse();
                }
            }
            function show_filter(dom) {
                var progress = new SWCombobox("progress","進度",
                    [{label:"N:新工作",value:"N"},{label:"I:正在進行的工作",value:"I"},{label:"T:當天的工作",value:"T"},
                    {label:"S:已經開始的工作",value:"S"},{label:"F:已完成工作",value:"F"},{label:"C:基本完成",value:"C"},
                    {label:"NF:除F的工作",value:"NF"},{label:"H:被掛起的工作",value:"H"},{label:"R:復查",value:"R"}]);
                progress.setHorizontalDisplay(true)
                var contact = new SWCombobox("contact", "聯繫人", window.CommonData.PartUserNames)
                contact.setHorizontalDisplay(true)
                var process = new SWCombobox("process", "處理", "/PMIS/global/get_typelist?type_name=Process_Type");       
                process.setHorizontalDisplay(true)
                var container = $(`<div class="row task_filter mb-2"></div>`);
                container.append(contact.dom);
                container.append(process.dom);
                container.append(progress.dom);        
                dom.prepend(container);
                container.find(".SWCombobox select.control").on("change", filter_task);
            }
            function filter_task() {
                var data = session_dom.data("data");
                var container = $(this).closest(".task-collapse")
                var contact = container.find(".SWCombobox select[name='contact']").val();
                var process = container.find(".SWCombobox select[name='process']").val();
                var progress = container.find(".SWCombobox select[name='progress']").val();
                var filter_data = [];
                for (var item of data) {
                    var local_contact = contact == "" ? "" : item.contact;
                    var local_process = process == "" ? "" : item.process;
                    var local_progress = progress == "" ? "" : item.progress;
                    if (contact == local_contact && process == local_process && progress == local_progress)
                        filter_data.push(item);
                }
                show_task(filter_data, self, false);
            }
                
            function update_task(self) {
                var pk = $(self).closest(".task-item").find(".pk").text();
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
                ".task-item"
            );        
        });  
        
        $("#Sessions").on("click",".SWBoardlist .task-issue", function(e){
            //跳到對應Development的Session
            var session_dom = $(this).closest(".task-issue")
            var sessionid = session_dom.find(".sessionid").text();
            var recordid = session_dom.find(".recordid").text();
            window.open(`/devplat/sessions?recordid=${recordid}&menu_id=mi_${sessionid}#Requirements`, "_blank");
            
        })  
        self.session_container.on("click", "a.unlink", function(e){
            e.preventDefault(); //阻止按鈕默認動作
            e.stopPropagation();            
            var sessionid = $(this).attr("sessionid");
            if (self.unlink_session_event != undefined)
                self.unlink_session_event(sessionid);
        })
    }
}
var GoalSimulation = function() {
    this.container = $("#Simulation");
    this.simulation_container = this.container.find(".card-body");
    this.simulation_template = $("#simulation_item").html();
    this.default_data = {total_qty:0, finish_qty:0,unfinish_qty:0,active_qty:0,qty_ratio:0, 
    total_day:0, actived_day:0, lave_day:0, expected_date:Date.today().toString("yyyy-MM-dd"),day_ratio:0}
    var self = this;
    this.init = function() {
    }
    this.init_analysis_data = function(sessions) {
        if (sessions == null) {
            self.init_simulation_data(this.default_data);
        }else {
            var url = "/looper/goal/project_goal/analysis_simulation"
            var params = {sessions:sessions};
            $.get(url, params, function(result){
                if (result.data['qty_ratio'] > 0)
                    result.data['qty_ratio'] = result.data['qty_ratio'].toFixed(2) * 100;
                if (result.data['day_ratio'] > 0)
                    result.data['day_ratio'] = result.data['day_ratio'].toFixed(2) * 100;
                self.init_simulation_data(result.data);
            });
        }        
    }
    this.init_simulation_data = function(data) {        
        self.simulation_container.html(self.simulation_template.render(data));
    }
}

$(function(){
    var goal = new Goal();
    goal.after_init = goal_after_init;
    var sessions = new Sessions();
    sessions.unlink_session_event = unlink_session;
    var goalSimulation = new GoalSimulation
    function init() {
        goal.init();
        sessions.init();
        goalSimulation.init();
    }
    function goal_after_init(data) {
        var link_session = data.sessions;
        sessions.init_sessions(link_session);
        goalSimulation.init_analysis_data(link_session);
    }
    function unlink_session(sessionid) {
        goal.unlink_session(sessionid);
    }
    init();
});