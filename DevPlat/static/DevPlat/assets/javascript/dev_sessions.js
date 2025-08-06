// const { $ } = require("vue/macros");

var gettext_flowChart = gettext("FlowChart");
function PageUI() {
    this.Questions = undefined;
    this.Design = undefined;
    this.Requirements = undefined;
    this.Overview = undefined;
    this.Specification = undefined;
    this.SessionTasks = undefined;
    this.ControlCenter = undefined;
    // this.SessionLog = undefined;
    var self = this;
    this.init = function() {
        self.Questions = new Questions();
        self.Questions.init();
        // self.Design = new Design();
        // self.Design.init(getParamFromUrl("recordid"));
        self.Requirements = new Requirements();
        self.Requirements.init();
        self.Overview = new Overview();
        self.Overview.Requirement = self.Requirements;
        self.Overview.init();
        self.Specification = new Specification();
        self.Specification.init();
        this.SessionTasks = new SessionTasks();
        self.SessionTasks.init();
        this.ControlCenter = new ControlCenter()
        self.ControlCenter.init();
        // this.SessionLog = new SessionLog()
        // self.SessionLog.init();
        self.init_workflow();
        self.bind_event();
    }
    this.init_workflow = function() {
        var recordid = getParamFromUrl("recordid");
        var show_mindmap = getParamFromUrl("show_mindmap");
        if (recordid != undefined ) {
            $.get("/PMIS/global/get_typelist?type_name=Project_WorkFlow", function(result){
                if (result.status) {
                    var arr = result.data.filter(x=>x.value == recordid);
                    if (arr.length >0){
                        var flowchartnos = arr[0].label;
                        if (flowchartnos) {
                            if (!show_mindmap)
                                $("#Diagram iframe").attr("src",`/flowchart/preview_diagram?hidetm=true#/?flowChartNo=${flowchartnos.split(",")[0]}`);
                            $.get("/flowchart/get_flowchart_desc", {flowChartNos:flowchartnos}).then((result)=>{
                                if(result.status) {
                                   var default_flowchartno = flowchartnos.split(",")[0]
                                   if (show_mindmap) {
                                        var mindmap_arr = result.data.filter(x=>x.label.match(/site\s*map/gi));
                                        if (mindmap_arr.length > 0) {
                                            default_flowchartno = mindmap_arr[0].value;
                                            $("#Diagram iframe").attr("src",`/flowchart/preview_diagram?hidetm=true#/?flowChartNo=${default_flowchartno}`);
                                        }
                                   }
                                   var flowchart_cmpt = new SWCombobox("", gettext_flowChart, result.data, default_flowchartno);
                                   flowchart_cmpt.setHorizontalDisplay(true);
                                    flowchart_cmpt.input_dom.on("change", function(){
                                        var flowchart = $(this).val();
                                        if (flowchart)
                                            $("#Diagram iframe").attr("src",`/flowchart/preview_diagram?hidetm=true#/?flowChartNo=${flowchart}`);                                    
                                    });
                                    $("#Diagram .select_flowchart").empty();
                                    $("#Diagram .select_flowchart").append(flowchart_cmpt.dom);
                                }
                            });
                        }
                    }
                }
            });
        }
    }
    this.bind_event = function() {        
    }
}

$(function () {
    window.menu_on_click_fun = function() {
        var sessionid = $(this).closest(".menu-item").attr("sessionid");
        change_session(sessionid);
    }

    $('.wrapper').on("shown.bs.tab","a[data-toggle='tab']", function () {
        caclIframeHgiht();
    });

    $("#pciframe").on("load", function(){
        caclIframeHgiht();
    });


    function caclIframeHgiht() {
        $(".iframe_wrapper").height($("#Diagram").height() - $(".select_flowchart").outerHeight(true) - 20);
        $("#pciframe").height($(".iframe_wrapper").height());
        $(window.frames[0].document).find("#myDiagramDiv").height($(".iframe_wrapper").height());
        $(window.frames[0].document).find("#myDiagramDiv>div").height($(".iframe_wrapper").height());
    }

    var UI = new PageUI();
    UI.init();
    function show_spec(sessionid) {
        if (UI.Specification.spec_table == undefined && $("#spec_table").is(":visible")) {
            UI.Specification.init_spec_table();
        }
        if (sessionid == undefined)
            sessionid = get_active_session();
        if (sessionid != undefined && $("#spec_table").data('sessionid') != sessionid) {
            UI.Specification.spec_table_datatable.ajax.url("/devplat/spec/list?sessionid=" + sessionid).load()
            $("#spec_table").data('sessionid', sessionid)
        }
    }
    function show_session_tasks(sessionid) {
        if (Object.values(UI.SessionTasks.tables)[0].table == undefined && $("#Session_Tasks").is(":visible")) {
            UI.SessionTasks.init_task_table();
        }
        if (sessionid == undefined)
            sessionid = get_active_session();
        if (sessionid != undefined && $("#session_tasks_table").data('sessionid') != sessionid) {
            UI.SessionTasks.load_data(sessionid);
            $("#session_tasks_table").data('sessionid', sessionid);
        }
    }
    function show_req(sessionid) {
        if (sessionid == undefined)
            sessionid = get_active_session();
        if (sessionid != undefined ) {
            UI.Requirements.edit_form.dom.show();
            if ($("#req_edit").data("sessionid") != sessionid) {                
                var session_desc = $(`#stacked-menu .menu-item[sessionid='${sessionid}'] .menu-text`).text();
                UI.Requirements.edit_form.dom.find(".card-title").text("User Requirement - {0}".format(session_desc));    
                UI.Requirements.get_pk_with_rid(sessionid).then((pk)=>{
                    if (pk == "") {
                        UI.Requirements.edit_form.set_pk(undefined);       
                        UI.Requirements.edit_form.init_data({sessionid:sessionid});     
                    }else {
                        UI.Requirements.edit_form.set_pk(pk);
                        UI.Requirements.edit_form.init_data();        
                    }
                });
                $("#req_edit").data('sessionid', sessionid);
            }
        }else {
            UI.Requirements.edit_form.dom.hide();
        }
        /**if (UI.Requirements.req_session_table == undefined && $("#req_session_table").is(":visible")) {
            UI.Requirements.init_session_table();
        }
        //暫時讀取所有
        UI.Requirements.req_session_datatable.search('').draw();*/
    }
    function show_question() {
        if (UI.Questions.technicTable == undefined && $("#Questions").is(":visible")) {
            UI.Questions.init_technical_table();
        }
        var session = get_active_session();
        if (session != undefined)
            $('#Questions .nav-tabs a[href="#q_session"]').tab('show');
        else
            $('#Questions .nav-tabs a[href="#q_session"]').tab('show');
    }
    function bind_event() {
        $('.session_container .tab-menu .nav-tabs a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
            $('.session_container .tab-menu .nav-tabs a[data-toggle="tab"]').not($(this)).removeClass("active show");
            var tab = $(this).attr("href");
            if (tab == "#Requirements")
                show_req()
            else if (tab == "#Specification")
                show_spec();
            else if (tab == "#Questions")
                show_question();
            else if (tab == "#Session_Tasks")
                show_session_tasks();
            // else if (tab == '#Session_log')
            //     UI.SessionLog.sessionChange(get_active_session());
        });        
    }
    
    function get_active_session() {
        var active_item = $("#stacked-menu .menu-item.has-active");
        if (active_item.length > 0)
            return active_item.attr("sessionid");
        else
            return undefined;
    }

    function change_session(sessionid) {
        var show_content_id = $("#pagecontrol_content>.tab-pane.show").attr("id");
        if (show_content_id == 'Specification')
            show_spec(sessionid);
        else if (show_content_id == "Requirements")
            show_req(sessionid);
        else if (show_content_id == 'Session_Tasks')
            show_session_tasks(sessionid);
        // else if (show_content_id == 'Session_log')
        //     UI.SessionLog.sessionChange(get_active_session());
    }
    function goto_tab() {
        if (window.location.href.indexOf("#") != -1) {
            var arr = window.location.href.split("#");
            if (arr.length = 2) {
                var tab_name = arr[1];
                var tab =  $(`.session_container .tab-menu .nav-tabs a[data-toggle="tab"][href='#${tab_name}']`).not(":hidden");
                if(tab.length > 0)
                    tab.tab("show");
                else {
                    var tab =  $(`.session_container .tab-menu .nav-tabs .dropdown a[data-toggle="tab"][href='#${tab_name}']`);                    
                    if (tab.length > 0) {
                        tab.tab("show")
                    }
                }
            }
        }
    }

    // function sendWidthToIframe() {
    //     const iframe = document.getElementById('logiframe');
    //     if (iframe && iframe.contentWindow) {
    //         iframe.contentWindow.postMessage({
    //             type: 'resize',
    //             width: window.innerWidth
    //         }, '*');
    //     }
    // }
    const showAI = SWAIComBox('#showAI', '', 'Chat With AI', true)
    $.ajax({
        url:`/PMIS/public/get_syspara?ftype=ProjectStatusQuestion`,
        type:"GET",
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", self.getCookie('csrftoken'));
        },                
        success:function(response) {
            if (response.status) {
                var resultdata = []
                for(var item of response.data){
                    resultdata.push(item['fvalue'])
                }
                showAI.init_QuestionSelect(resultdata)
            }
        }
    })
    
    $('#chataibtn').on('click', function() {
        var table_name = 'tasks'; // 預設情況下使用的數據表名
        var tab_name = ''
        var active_tab = $('#Session_Tasks .card-body.pt-0 .tab-content .tab-pane.fade.active.show')
        // 判斷當前活動的標籤頁
        if (active_tab.length > 0) {
            for (var tab of active_tab) {
                if (tab.id.indexOf('Session') != -1) {
                    tab_name = tab.id; // 獲取活動標籤的 ID
                }
            }
        }
        // 根據不同的標籤頁，選擇對應的數據表
        if (tab_name == 'SessionTopTasks')
            table_name = 'top_tasks';
        if (tab_name == 'SessionTopPriorityTasks')
            table_name = 'top_priority_tasks';
        
        // 調用 init_AI 函數，將當前數據表的數據作為預定義數據傳遞
        // init_AI('session', 'questionType',false);
        // init_AI(UI.SessionTasks.tables[table_name].datatable.data().toArray(), 'predefinedData');
        showAI.sendDataToReact(UI.SessionTasks.tables[table_name].datatable.data().toArray(), 'predefinedData')
        showAI.show()
    });
    
    // window.addEventListener('resize', sendWidthToIframe);
    // window.addEventListener('load', sendWidthToIframe);

    bind_event();
    // goto_tab();
    setTimeout(goto_tab, 500);
});
