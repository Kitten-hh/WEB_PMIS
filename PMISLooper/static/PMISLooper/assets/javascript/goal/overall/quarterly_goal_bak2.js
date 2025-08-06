function ManagerQuarterlyGoal(contact, period) {
    var contact = contact;
    var period = period;
    var goal_target = "#qGoals_pc .manager_quarterly_goal"
    var dom = $(goal_target);
    var item_html =  `<li class="mb-2 pl-3 pr-3 d-flex justify-content-start"><span class="task_num">[[seqno]] <i class="fas fa-arrow-right pl-2"></i></span><p class="task_contents">[[goal]]</p></li>`;
    if (SWApp.os.isMobile) {
        goal_target = "#qGoals_mobile .manager_quarterly_goal";
        dom = $(goal_target);
        item_html = `<li class="mb-2 d-flex justify-content-start"><i class="icofont-tick-mark mr-2"></i><p class="task_contents">[[goal]]</p></li>`;
    }
    var all_goals = dom.find(".all_goals");
    this.cur_month_str = 'monthly-' + Date.today().format("yyyy-MM");
    this.source = undefined;
    var editor_container = undefined;
    var editor_form = undefined;
    var self = this;
    this.load_source = function(source) {
        this.source = source;
        all_goals.find("li").remove();
        if (source == undefined) 
            return;
        var goaltype = $(goal_target + " .SWCombobox select.control[name='period']").val();
        var username = $(goal_target + " .SWCombobox select.control[name='contact']").val();
        var goals = [];
        for(var name of Object.keys(source)) {
            if (username == "")
                all_goals.append(item_html.render({goal:name}));
            if (goaltype == "Q" && source[name]['quarterly'] != undefined)
                goals = source[name]['quarterly'];
            else if (goaltype == "M" && this.cur_month_str in source[name] && "data" in source[name][this.cur_month_str]) {                
                if (this.cur_month_str in source[name] && "data" in source[name][this.cur_month_str])
                    goals.push(source[name][this.cur_month_str]['data']);
            } else if (goaltype == "W" && this.cur_month_str in source[name]) {
                if (Date.today().compareTo(Date.parse(Date.today().format("yyyy-MM") + "-15")) < 0) {
                    if ("weekly-1" in source[name][this.cur_month_str])
                        goals.push(source[name][this.cur_month_str]['weekly-1']);
                    if ("weekly-2" in source[name][this.cur_month_str])
                        goals.push(source[name][this.cur_month_str]['weekly-2']);
                }else {
                    if ("weekly-3" in source[name][this.cur_month_str])
                        goals.push(source[name][this.cur_month_str]['weekly-3']);
                    if ("weekly-4" in source[name][this.cur_month_str])
                        goals.push(source[name][this.cur_month_str]['weekly-4']);
                    if ("weekly-5" in source[name][this.cur_month_str])
                        goals.push(source[name][this.cur_month_str]['weekly-5']);
                }
            }
        }
        goals.forEach((goal,index) => {
            this.load_goal(goal, index+1);
        });
    }

    this.load_goal = function(goal, index) {
        var managements = goal['goaldesc'];
        /**var lines = managements.replace(/\r\n/g, "\r").replace(/\n/g, "\r").split(/\r/);
        var seqno_length = (lines.length + "").length < 2 ? 2 : (lines.length + "").length;
        for (var i = 0; i < lines.length; i++) {
            var data = {'goal':lines[i]};
            data['seqno'] = ((i + 1) + "").padStart(seqno_length, "0");
            all_goals.append(item_html.render(data))
        }*/
        var data = {goal:managements, seqno:"G"+index};
        all_goals.append(item_html.render(data));
    }

    dom.on("click", ".edit" ,function(){
        if ($(this).find("i").hasClass("fa-edit")) {
            all_goals.find("li").hide();
            $(this).find("i").removeClass("fa-edit")
            $(this).find("i").addClass("fa-save")
            if (editor_container == undefined) {
                editor_container = $(`<form class="form"></form>`);
                editor = new SWTextarea("managements","", 6);
                editor.dom.find("label").hide();
                editor_container.append(editor.dom);
                editor_container.append(new SWText("contact","hidden", "", contact).dom);
                editor_container.append(new SWText("period","hidden", "", period).dom);
                editor_container.append(new SWText("month","hidden", "", "0").dom);
                dom.find("ul").before(editor_container);


                editor_form = new SWBaseForm(goal_target);
                editor_form.create_url = "/PMIS/goal/overall/create_manager_goal";
                editor_form.update_url = "/PMIS/goal/overall/update_manager_goal/[[pk]]"
                editor_form.pk_in_url = false;
                //editor_form.init_data()
                editor_form.on_after_save = function(data){
                    self.load_source(data);                
                    $(goal_target).find(".edit").find("i").removeClass("fa-save");
                    $(goal_target).find(".edit").find("i").addClass("fa-edit");
                    editor_container.hide();
                }
                if (self.source != undefined) {
                    editor.input_dom.val(self.source["managements"]);
                    editor_form.set_pk(self.source["inc_id"]);
                }
            }else {
                editor_container.show();
            }
        } else {
            //內容相同不保存
            if (self.source != undefined && self.source["managements"].replace(/\r\n/g, "\r").replace(/\n/g, "\r") == 
                editor.input_dom.val().replace(/\r\n/g, "\r").replace(/\n/g, "\r")) {
                $(goal_target).find(".edit").find("i").removeClass("fa-save");
                $(goal_target).find(".edit").find("i").addClass("fa-edit");
                editor_container.hide();
                all_goals.find("li").show();
            }else 
                $(goal_target).find(".save").click();
        }
    });
}    

function ManagerMonthlyGoal(contact, period, month) {
    var contact = contact;
    var period = period;
    var month = month;
    var goal_target = "#qGoals_pc .month-{0} .sing_goals".format(month);
    var dom = $(goal_target);
    var item_html =  `<li class="task d-flex mb-2"><span>[[goal]]</span></li>`;
    if (SWApp.os.isMobile) {
        goal_target = "#qGoals_mobile .month-{0} .sing_goals".format(month);
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
                editor = new SWTextarea("managements","", 10);
                editor.dom.find("label").hide();
                editor_container.append(editor.dom);
                editor_container.append(new SWText("contact","hidden", "", contact).dom);
                editor_container.append(new SWText("period","hidden", "", period).dom);
                editor_container.append(new SWText("month","hidden", "", month).dom);
                dom.append(editor_container);


                editor_form = new SWBaseForm(goal_target);
                editor_form.create_url = "/PMIS/goal/overall/create_manager_goal";
                editor_form.update_url = "/PMIS/goal/overall/update_manager_goal/[[pk]]"
                editor_form.pk_in_url = false;
                //editor_form.init_data()
                editor_form.on_after_save = function(data){
                    self.load_source(data);                
                    $(goal_target).find(".edit").find("i").removeClass("fa-save");
                    $(goal_target).find(".edit").find("i").addClass("fa-edit");
                    editor_container.hide();
                }
                if (self.source != undefined) {
                    editor.input_dom.val(self.source["managements"]);
                    editor_form.set_pk(self.source["inc_id"]);
                }
            }else {
                editor_container.show();
            }
        } else {
            //內容相同不保存
            if (self.source != undefined && self.source["managements"].replace(/\r\n/g, "\r").replace(/\n/g, "\r") == 
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

$(function(){

    var contact = getParamFromUrl("contact");
    var period = getParamFromUrl("period");
    var year = period.split("-")[0];
    var period_num = period.split("-")[1];
    var first_month_str = Date.parse("{0}-{1}".format(year, period_num*3 - 2)).toString("yyyy-MM");
    var second_month_str = Date.parse("{0}-{1}".format(year, period_num*3 - 1)).toString("yyyy-MM");
    var third_month_str = Date.parse("{0}-{1}".format(year, period_num*3)).toString("yyyy-MM");

    var contact_cmpt = undefined;
    var period_cmpt = undefined;
    var base_container = "#qGoals_pc"
    if (SWApp.os.isMobile)
        base_container = "#qGoals_mobile"
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
    if (SWApp.os.isMobile) {
        title_goal_year = $(base_container +" .goal_title");
        title_goal = $(base_container +" .page-title-right .breadcrumb-item");
    }

    var manager_quarterly_goal = new ManagerQuarterlyGoal(contact, period);
    var manager_monthly1_goal = new ManagerMonthlyGoal("all", period, 1);
    var manager_monthly2_goal = new ManagerMonthlyGoal("all", period, 2);
    var manager_monthly3_goal = new ManagerMonthlyGoal("all", period, 3);

    function init_data() {
        var year = period.split("-")[0];
        //設置goal for year
        title_goal_year.text("Goals for {0}".format(year));

        //設置哪個季度
        title_goal.text("{0} Quarterly Goal".format(period));
        init_month_desc();
        contact_cmpt = new SWCombobox("contact", "Contact", window.CommonData.PartUserNames, contact);
        contact_cmpt.setHorizontalDisplay();
        quarter_goal_ti_right.prepend(contact_cmpt.dom);
        period_cmpt = new SWCombobox("period", "Period", [{label:"Quarterly",value:"Q"},{label:"Monthly",value:"M"},{label:"Weekly",value:"W"}], "W");
        period_cmpt.setHorizontalDisplay();
        quarter_goal_ti_right.prepend(period_cmpt.dom);
        $(base_container + " .goals_ti").text("Weekly Goals");
        $(base_container + " .SWCombobox select.control[name='period'], " + 
        base_container + " .SWCombobox select.control[name='contact']").on("change", function(){
            init_quarterly_goal()     
            var goaltype = period_cmpt.input_dom.val()
            if (goaltype == "Q")
                $(base_container + " .goals_ti").text("Quarterly Goals");
            else if (goaltype == "M")
                $(base_container + " .goals_ti").text("Monthly Goals");
            else
                $(base_container + " .goals_ti").text("Weekly Goals");
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
        if (SWApp.os.isMobile)
            link = "a h6";
        else {
            $(".month-1").find("h2.month").text(first_month);
            $(".month-2").find("h2.month").text(second_month);
            $(".month-3").find("h2.month").text(third_month);
        }
        $(monthly_tabs[0]).find(link).text(first_month);
        $(monthly_tabs[1]).find(link).text(second_month);
        $(monthly_tabs[2]).find(link).text(third_month);
    }

    function init_quarterly_goal() {
        var url = "/PMIS/goal/overall/goal_management";
        var goaltype = period_cmpt.input_dom.val();
        var local_contact = contact_cmpt.input_dom.val();
        var params = {contact:local_contact, period:period, goaltype:goaltype};
        $.get(url, params, function(data){  
            if (data.status) {                
                manager_quarterly_goal.load_source(data.data);
            }
        });
    }

    function init_manager_goal() {
        var url = "/PMIS/goal/overall/goal_management";
        var params = {contact:contact, period:period};
        $.get(url, params, function(data){
            if (data.status) {                
                var quarterly = undefined;
                var monthly1 = undefined;
                var monthly2 = undefined;
                var monthly3 = undefined;
                if (Object.keys(data.data).length > 0)
                    data.data = data.data[contact];
                if ("quarterly" in data.data)
                    quarterly = data.data['quarterly'];
                if ('monthly-'+first_month_str in data.data && "data" in data.data['monthly-'+first_month_str])
                    monthly1 = data.data['monthly-'+first_month_str]['data']
                if ('monthly-'+second_month_str in data.data && "data" in data.data['monthly-'+second_month_str])
                    monthly2 = data.data['monthly-'+second_month_str]['data']

                if ('monthly-'+third_month_str in data.data && "data" in data.data['monthly-'+third_month_str])
                    monthly3 = data.data['monthly-'+third_month_str]['data']
                //manager_quarterly_goal.load_source(quarterly);
                manager_monthly1_goal.load_source(monthly1);
                manager_monthly2_goal.load_source(monthly2);
                manager_monthly3_goal.load_source(monthly3);
            }
        });
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
        if (SWApp.os.isMobile) {
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
    init_quarterly_goal();
    init_manager_goal();
    init_monthly();
    init_weekly();
    init_select_goal();
    init_select_weekly_goal();
    init_eidt_user_goal();

    function update_task(self) {
        var pk = $(self).attr("pk")
        init_task(pk);
    }

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
});