$(function () {
    ///////////////初始化UI///////////////////
    window.CommonData = {
        PartUserNames:promiseGet("/PMIS/user/get_part_user_names"), //電腦部用戶
        TaskProgress:promiseGet("/PMIS/task/progresses"), //任務進度
        TaskHOperation:promiseGet("/PMIS/global/get_typelist?type_name=HOperation_Type"), //任務操作
        TaskProcess:promiseGet("/PMIS/global/get_typelist?type_name=Process_Type"), //任務處理
        TaskCategory:promiseGet("/PMIS/global/get_typelist?type_name=taskcategory"), //任務Category
        TaskType:promiseGet("/PMIS/tasktype/tasktype_list"), //任務分類
    }      
    var nav_links = $(".top-bar-item-right .header-nav .nav-link")
    var nav = $(nav_links[0])
    var treeId = '' //將session數狀圖顯示的容器的id
    var formName = ''
    var task_session = []
    var old_task = undefined //轉任務時用於存在被轉任務內容
    var select_parents = undefined //轉任務時設置關聯任務的完整taskNo
    nav.attr("data-toggle", "modal");
    if (SWApp.os.isAndroid || SWApp.os.isPhone){
        nav.attr("data-target", "#add-task-module");
        treeId ='treeMenu_m'
        formName ='add-task-module'
    }else{
        nav.attr("data-target", "#add-task");
        treeId ='treeMenu'
        formName ='add-task'
    }
    $("#add-task-module .nav-link").click(function () {
        $("#add-task-module .cHeight").css('height', $("#add-task-module .card-body").height());
    });

    var contact_cmpt = new SWCombobox("contact", "聯繫人", window.CommonData.PartUserNames)
    contact_cmpt.input_dom.attr("data-live-search", "true");
    $("#user").append(contact_cmpt.dom);

    var progress_cmpt = new SWCombobox("progress", "進度", "/PMIS/task/progresses")
    $("#user").append(progress_cmpt.dom);
    var opera_cmpt = new SWCombobox("hoperation", "操作", "/PMIS/global/get_typelist?type_name=HOperation_Type");
    $("#user").append(opera_cmpt.dom);
    var priority_cmpt = new SWCombobox("priority", "優先級", ["888", "8888", "8889"]);
    $("#user").append(priority_cmpt.dom);
    var class_cmpt = new SWCombobox("class_field","Class",[{value:1, desc:"Class 1"}, {value:2, desc:"Class 2"}, {value:3, desc:"Other"}], undefined, "value", "desc");
    $("#user").append(class_cmpt.dom);

    var planbdate_cmpt = new SWDate("planbdate","datetime-local","計劃開始");
    $("#planDate").prepend(planbdate_cmpt.dom);
    var planedate_cmpt = new SWDate("planedate","datetime-local","計劃结束");
    $("#planDate .SWDate").append(planedate_cmpt.dom);

    var bdate_cmpt = new SWDate("bdate","datetime-local","實際開始");
    $("#actualDate").append(bdate_cmpt.dom);
    var edate_cmpt = new SWDate("edate","datetime-local","實際结束");
    $("#actualDate").append(edate_cmpt.dom);

    var tasktype_cmpt = new SWCombobox("tasktype", "任務分類", "/PMIS/tasktype/tasktype_list", undefined, 'tasktype', 'description');
    $("#tasktype_c").append(tasktype_cmpt.dom);
    var subtasktype_cmpt = new SWCombobox("subtasktype", "子任務分類", []);
    $("#subtasktype_c").append(subtasktype_cmpt.dom);
    var diff_cmpt = new SWCombobox("diff", "難度", ["1", "2", "3"])
    $("#diff_c").append(diff_cmpt.dom);
    var process_cmpt = new SWCombobox("process", "處理", "/PMIS/global/get_typelist?type_name=Process_Type");
    $("#process_c").append(process_cmpt.dom);
    var taskcategory_cmpt = new SWCombobox("taskcategory", "任務類別", "/PMIS/global/get_typelist?type_name=taskcategory");
    $("#taskcategory_c").append(taskcategory_cmpt.dom);
    var sms_cmpt = new SWRadiobox("isradio", "sendSMS",true)
    $("#email").append(sms_cmpt.dom);   
    var email_cmpt = new SWRadiobox("isradio", "Off. hrs",false)
    $("#email").append(email_cmpt.dom);      
    $("#add-task-module form").prepend((new SWText("inc_id","hidden")).dom)
    $("#add-task-module form").prepend((new SWText("subprojectid","hidden")).dom)
    $("#add-task-module form").prepend((new SWText("pid","hidden")).dom)
    $("#add-task-module form").prepend((new SWText("tid","hidden")).dom)
    $("#add-task-module form").prepend((new SWText("taskid","hidden")).dom)
    $("#add-task-module form").prepend((new SWText("relationgoalid","hidden")).dom)
    $("#add-task-module form").prepend((new SWText("editionid","hidden")).dom)
    $("#add-task-module form").prepend((new SWText("docpath","hidden")).dom)
    $("#add-task-module form").prepend((new SWText("relationid","hidden")).dom)
    
    $("#task-description textarea").attr("name", "task");
    //初始TextArea href
    var task_module_textarea_href = new SWTextAreaHref("#task-description textarea");
    var remark_module_textarea_href = new SWTextAreaHref("input[name='remark']");    

    // 
    var taskSwitch_users_m = new SWCombobox("contact_session", "聯繫人", window.CommonData.PartUserNames)
    taskSwitch_users_m.input_dom.attr("data-live-search", "true");
    $("#ts_user_m").append(taskSwitch_users_m.dom);

    var taskSwitch_desc_m = new SWText("description", "text","描述");
    $("#ts_desc_m").append(taskSwitch_desc_m.dom);

    var taskSwitc_recordid_m = new SWCombobox("recordid", "项目编号", "/PMIS/subproject/get_all_recordid")
    taskSwitc_recordid_m.input_dom.attr("data-live-search", "true");
    $("#ts_recordid_m").append(taskSwitc_recordid_m.dom);

    var taskSwitc_session_m = new SWText("session","text","工程编号");
    $("#ts_session_m").append(taskSwitc_session_m.dom);
    // 

    //處理保存按鈕的popver屬性
    $("#add-task-module .save").attr("data-container","body")
    $("#add-task-module .save").attr("data-toggle","popover")
    $("#add-task-module .save").attr("data-placement","top")
    $("#add-task-module .modal-header .floating-button").addClass("add");
    
    $('.quick-add-task .nav-tabs .nav-item a').on('click',function(e) {
        e.preventDefault(); //阻止按鈕默認動作
        //刪除所有tab標籤的class active
        $(this).parent().parent().find(".nav-item a").removeClass("active");
        //給點擊的tab標籤添加class active
        $(this).addClass("active");
        //查找tab標籤
        var content_id = $(this).attr("data-target");
        if (content_id == undefined)
            content_id = $(this).attr("href");
        var content = $(".tab-content " + content_id);

        //刪除所有tab content的class active和show
        content.parents(".tab-content").find(".tab-pane").removeClass("active");
        content.parents(".tab-content").find(".tab-pane").removeClass("show");
        //對當前tab content添加class active和show
        content.addClass("active");
        content.addClass("show");
    });

    // PCd
    $("#add-task form").prepend((new SWText("inc_id","hidden")).dom)
    $("#add-task form").prepend((new SWText("subprojectid","hidden")).dom)
    $("#add-task form").prepend((new SWText("pid","hidden")).dom)
    $("#add-task form").prepend((new SWText("tid","hidden")).dom)
    $("#add-task form").prepend((new SWText("taskid","hidden")).dom)    
    $("#add-task form").prepend((new SWText("relationgoalid","hidden")).dom)
    $("#add-task form").prepend((new SWText("editionid","hidden")).dom)
    $("#add-task form").prepend((new SWText("docpath","hidden")).dom)
    $("#add-task form").prepend((new SWText("relationid","hidden")).dom)
    
    var description_pc = new SWTextarea("task", "任務描述",4)
    $("#add-task #description").append(description_pc.dom);
    var remark_pc = new SWTextarea("remark", "備註",3)
    $("#remark").append(remark_pc.dom);
    //初始化TextArea href
    var task_pc_textarea_href = new SWTextAreaHref(description_pc.input_dom);
    var remark_pc_textarea_href = new SWTextAreaHref(remark_pc.input_dom);    
    
    var users_pc = new SWCombobox("contact", "聯繫人", window.CommonData.PartUserNames)
    users_pc.input_dom.attr("data-live-search", "true");
    $("#users").append(users_pc.dom);
    var priority_pc = new SWCombobox("priority", "優先級", ["888", "8888", "8889"])
    $("#priority_p").append(priority_pc.dom);
    var taskcategory_pc = new SWCombobox("taskcategory", "任務類別", "/PMIS/global/get_typelist?type_name=taskcategory");
    $("#taskcategory_p").append(taskcategory_pc.dom);
    var class_pc = new SWCombobox("class_field","Class",[{value:1, desc:"Class 1"}, {value:2, desc:"Class 2"}, {value:3, desc:"Other"}], undefined, "value", "desc");
    $("#class").append(class_pc.dom);
    var progress_pc = new SWCombobox("progress", "進度", "/PMIS/task/progresses")
    $("#progress_p").append(progress_pc.dom);
    var opera_pc = new SWCombobox("hoperation", "操作", "/PMIS/global/get_typelist?type_name=HOperation_Type");
    $("#operation").append(opera_pc.dom);
    var process_pc = new SWCombobox("process", "處理", "/PMIS/global/get_typelist?type_name=Process_Type");
    $("#add-task #process").append(process_pc.dom);
    var score_pc = new SWText("score", "number","分数");
    $("#score").append(score_pc.dom);
    var schedule_priority_pc = new SWText("schpriority","number","排期優先級")
    $("#schedule_priority").append(schedule_priority_pc.dom);
    var planbdate_pc = new SWDate("planbdate","datetime-local","計劃開始");
    $("#planbdate").append(planbdate_pc.dom);
    var planedate_pc = new SWDate("planedate","datetime-local","計劃结束");
    $("#planedate").append(planedate_pc.dom);
    var bdate_pc = new SWDate("bdate","datetime-local","實際開始");
    $("#bdate").append(bdate_pc.dom);
    var edate_pc = new SWDate("edate","datetime-local","實際结束");
    $("#edate").append(edate_pc.dom);    
    var tasktype_pc = new SWCombobox("tasktype", "任務分類", "/PMIS/tasktype/tasktype_list", undefined, 'tasktype', 'description');
    $("#tasktype_p").append(tasktype_pc.dom);
    var subtasktype_pc = new SWCombobox("subtasktype", "子任務分類", []);
    $("#subtasktype_p").append(subtasktype_pc.dom);
    var diff_pc = new SWCombobox("diff", "難度", ["1", "2", "3"])
    $("#diff_p").append(diff_pc.dom);   
    var email_pc1 = new SWRadiobox("isradio", "sendSMS", true)
    email_pc1.dom.css("display", "inline-block");
    $("#email_p").append(email_pc1.dom);
    var email_pc2 = new SWRadiobox("isradio", "Off. hrs", false)
    email_pc2.dom.css("display", "inline-block");
    $("#email_p").append(email_pc2.dom);
    var dayjoy_pc = new SWCheckbox("ischeck", "dayjob", true)
    $("#dayjoy").append(dayjoy_pc.dom);       

    var ts_session = new SWText("session","text","工程编号");
    $("#task_switch_session").append(ts_session.dom);

    var recordid = new SWCombobox("recordid", "项目编号", "/PMIS/subproject/get_all_recordid")
    recordid.input_dom.attr("data-live-search", "true");
    $("#task_switch_recordid").append(recordid.dom);

    var switch_users_pc = new SWCombobox("contact_session", "聯繫人", window.CommonData.PartUserNames)
    switch_users_pc.input_dom.attr("data-live-search", "true");
    $("#task_switch_users").append(switch_users_pc.dom);

    var task_switch_desc = new SWText("description", "text","描述");
    $("#task_switch_description").append(task_switch_desc.dom);

    ///////////////初始化UI///////////////////
    var model_task_form = new SWBaseForm("#add-task-module");
    model_task_form.create_url = "/PMIS/task/add_task";
    model_task_form.update_url = "/PMIS/task/update_task?pk=[[pk]]"
    model_task_form.pk_in_url = false;
    model_task_form.on_after_init = function(data) {
        process_cmpt.input_dom.data("old_value", data.progress);
        $("#add-task-module .SWCombobox select[name='subtasktype']").data("init-data", data["subtasktype"]);
        $("#add-task-module .SWCombobox select[name='tasktype']").change();
        $('#add-task-module a[href="#task-description"]').tab("show");
        $("#add-task-module p").text("{0}-{1}-{2}".format(data.pid, data.tid, data.taskid));
    }
    model_task_form.on_after_save = function(data) {
        $("#add-task-module p").text("{0}-{1}-{2}".format(data.pid, data.tid, data.taskid));
        $('#add-task-module a[href="#task-description"]').tab("show");                    
    }
    
    model_task_form.on_init_format = function(data) {
        if(old_task!=undefined){
            data = set_task_detail(data)
        }
    }

    var pc_task_form = new SWBaseForm("#add-task");
    pc_task_form.create_url = "/PMIS/task/add_task";
    pc_task_form.update_url = "/PMIS/task/update_task?pk=[[pk]]"
    pc_task_form.pk_in_url = false;
    pc_task_form.on_after_init = function(data) {
        process_pc.input_dom.data("old_value", data.progress);
        $("#add-task .SWCombobox select[name='subtasktype']").data("init-data", data["subtasktype"]);
        $("#add-task .SWCombobox select[name='tasktype']").change();
        $("#add-task .cust_taskId p").text("{0}-{1}-{2}".format(data.pid, data.tid, data.taskid));       
        // var projectid = "{0}-{1}".format(data.pid.replaceAll(' ',''), data.tid)
        var parentid = ''
        if(data.subprojectid!='' && data.subprojectid!=null){
            parentid = data.subprojectid
        }else{
            var selected = $('#'+treeId).jstree(true).get_selected(true)
            if (selected.length>0){
                var select_parent = selected[0].parents
                for(var i=0;i<select_parent.length;i++){
                    if(select_parent[i]=='#'){
                        parentid = select_parent[i-1].slice(0,5);
                        break;
                    }
                }
            }
        }
        //獲取對應session翻譯
        $.get(`/PMIS/subproject/get_recordid_list?recordid=${parentid}&pid=${data.pid}&tid=${data.tid}`, function(result){
            if (result.status) {
                result_list = result.data
                if(result_list.length>0){
                    if(result_list[0].subproject.length>0){
                        var subproject = result_list[0].subproject[0]
                        data.subprojectid = subproject.recordid
                        $('.cust_projectDetails span').text(subproject.projectname);      
                    }
                    if(result_list[0].tasklist.length>0){
                        var tasklist = result_list[0].tasklist[0]
                        $('.cust_module_name span').text(tasklist.sdesp);       
                        $('.cust_module_flowchart span').text(tasklist.flowchartno);       
                    }
                }
            }
        }); 
    }
    
    pc_task_form.on_init_format = function(data) {
        if(old_task!=undefined){
            data = set_task_detail(data)
        }
    }
    //轉任務時設置任務內容
    function set_task_detail(data){
        var task_keys = Object.keys(old_task)
        for(task_key of task_keys){
            if(!['inc_id','pid','tid','taskid','relationid','schpriority','schedulestate','editionid'].includes(task_key))
            data[task_key]=old_task[task_key]
        }
        //關聯任務
        data['relationid']= "{0}-{1}-{2}".format(old_task['pid'],old_task['tid'],old_task['taskid'])
        //子工程編號
        for(var i=0;i<select_parents.length;i++){
            if(select_parents[i]=='#'){
                data['subprojectid']=select_parents[i-1].slice(0,5);
                break;
            }
        }
        old_task = undefined
        select_parents = undefined
        return data
    }

    //添加任務
    $("a[data-target='#add-task-module']").on("click", function () {
        model_task_form.set_pk(undefined);
        model_task_form.init_data();
    });

    tasktype_cmpt.input_dom.on("change", function () {
        var tasktype = $(this).val();
        if (tasktype == "")
            return;
        var init_data = subtasktype_cmpt.input_dom.data("init-data");
        subtasktype_cmpt = new SWCombobox("subtasktype", "子任務分類", "/PMIS/tasktype/subtasktype_list/" + tasktype, init_data, 'tasktype', 'description');
        $("#subtasktype_c").empty();
        $("#subtasktype_c").append(subtasktype_cmpt.dom);
    });

    tasktype_pc.input_dom.on("change", function(){
        var tasktype = $(this).val();
        if (tasktype == "")
            return;
        var init_data = subtasktype_pc.input_dom.data("init-data");
        subtasktype_pc = new SWCombobox("subtasktype", "子任務分類", "/PMIS/tasktype/subtasktype_list/" + tasktype, init_data, 'tasktype', 'description');
        $("#subtasktype_p").empty();
        $("#subtasktype_p").append(subtasktype_pc.dom);
    })  

    progress_pc.input_dom.on("change", function(){
        var progress = $(this).val();
        var old_progress = process_pc.input_dom.data("old_value");
        if (progress == "I") {
            bdate_pc.input_dom.val(Date.today().toString("yyyy-MM-ddTHH:mm"));
            edate_pc.input_dom.val("");
        }else if (progress == "T") {
            if (old_progress == "I") {
                planbdate_pc.input_dom.val(Date.today().toString("yyyy-MM-ddTHH:mm"));
                planedate_pc.input_dom.val(Date.today().toString("yyyy-MM-ddTHH:mm"));
                bdate_pc.input_dom.val(Date.today().toString("yyyy-MM-ddTHH:mm"));
            }
        }else if (progress == "C") {
            edate_pc.input_dom.val(Date.today().toString("yyyy-MM-ddTHH:mm"));
            if (bdate_pc.input_dom.val() == "") {
                bdate_pc.input_dom.val(Date.today().toString("yyyy-MM-ddTHH:mm"));
            }
        }
    });

    progress_cmpt.input_dom.on("change", function(){
        var progress = $(this).val();
        var old_progress = process_cmpt.input_dom.data("old_value");
        if (progress == "I") {
            bdate_cmpt.input_dom.val(Date.today().toString("yyyy-MM-ddTHH:mm"));
            edate_cmpt.input_dom.val("");
        }else if (progress == "T") {
            if (old_progress == "I") {
                planbdate_cmpt.input_dom.val(Date.today().toString("yyyy-MM-ddTHH:mm"));
                planedate_cmpt.input_dom.val(Date.today().toString("yyyy-MM-ddTHH:mm"));
                bdate_cmpt.input_dom.val(Date.today().toString("yyyy-MM-ddTHH:mm"));
            }
        }else if (progress == "C") {
            edate_cmpt.input_dom.val(Date.today().toString("yyyy-MM-ddTHH:mm"));
            if (bdate_cmpt.input_dom.val() == "") {
                bdate_cmpt.input_dom.val(Date.today().toString("yyyy-MM-ddTHH:mm"));
            }
        }
    });

    

    //添加任務
    $("a[data-target='#add-task']").on("click", function () {
        pc_task_form.set_pk(undefined);
        pc_task_form.init_data();
    });

    $("#add-task button[type='reset']").on("click", function(){
        $("#add-task .SWCombobox select").val('').selectpicker('refresh');
    });

    window.init_task = function(pk, params) {
        var id = "#add-task"
        if (SWApp.os.isAndroid || SWApp.os.isPhone) {
            id = "#add-task-module"        
            model_task_form.set_pk(pk);
            model_task_form.init_data(params);
        }else {
            pc_task_form.set_pk(pk);
            pc_task_form.init_data(params);
        }
        $(id).modal("show");
    }

    window.gloal_typelist = {};
    var init_global_typelist = function(type_name) {
        var url = "/PMIS/global/get_typelist?type_name={0}".format(type_name);
        $.get(url, function(result){
            if (result.status) {
                window.gloal_typelist[type_name] = result.data;
            }
        });
    }
    init_global_typelist("Process_Type");

    //獲取議題session
    // $.get("/PMIS/global/get_typelist?type_name=mettingsession", function(result){
    //     if (result.status) {
    //         task_session.push(result.data[0]['value'])
    //     }
    // });

    $('.task_switch_container').children().keydown(enterclick);
    $('#ts_container_m').children().keydown(enterclick);

    //回車鍵點方法
    function enterclick(e){
        GetSeeeionTree() 
    }

    //初始化樹狀圖
    $('#'+treeId).jstree({
        "core": {
            "themes": {
                "responsive": false,
                "dots": false,
            },
            "check_callback": true,
            'data':[]
        },
        "types": {
            "default": {
                "icon": false,
            }
        },
        "plugins": [
            "contextmenu",
            "dnd",
            "types",
            "wholerow",
            "unique"
        ],
        'contextmenu': {
            'select_node': false,
        }
    });

    //查詢session並重構樹狀圖
    function GetSeeeionTree(){
      if (SWApp.os.isAndroid || SWApp.os.isPhone){
        var contact = $('#ts_user_m [name="contact_session"]select').val()  //聯繫人
        var session = $('#ts_session_m [name="session"]').val()     //工程編號
        var recordid = $('#ts_recordid_m [name="recordid"]select').val()   //子工程編號
        var description = $('#ts_desc_m [name="description"]').val() //描述
      }else{
        var contact = $('#task_switch_users [name="contact_session"]select').val() //聯繫人
        var session = $('#task_switch_session [name="session"]').val()     //工程編號
        var recordid = $('#task_switch_recordid [name="recordid"]select').val()   //子工程編號
        var description = $('#task_switch_description [name="description"]').val() //描述
      }
        var url = `/PMIS/session/session_sessionList?contact=${contact}&pid=${session}&recordid=${recordid}&desc=${description}`
        $.get(url,function(result){
            if (result.status) {
                var jsonarray = new Array();
                var arrays = result.data;
                for (var i = 0; i < arrays.length; i++) {
                    var arr = {
                        "id": arrays[i].keyid,
                        "parent": arrays[i].parentid == '' ? "#" : arrays[i].parentid,
                        "text": arrays[i].recordid +'    '+ arrays[i].desp,
                        "data": arrays[i],
                        'state': {
                            'opened': false
                        },
                    }
                    jsonarray.push(arr);
                }
                $('#'+treeId).jstree(true).destroy();// 清除树节点
                // 重新设置树的JSON数据集
                $('#'+treeId).jstree({
                    "themes": {
                        "responsive": false,
                        "dots": false,
                    },
                    "check_callback": true,
                    'core': { 'data': jsonarray },
                    "types": {
                        "default": {
                            "icon": false,
                        }
                    },
                    "plugins": [
                        "contextmenu",
                        "dnd",
                        "types",
                        "wholerow",
                        "unique"
                    ],
                    'contextmenu': {
                        'select_node': false,
                    }
                })
                $('#'+treeId).jstree(true).refresh(); // 刷新树
            }
        });
    }

    //獲取對應session的默認任務數據並返回
    async function get_default_task(sessionid){
        var data =  await $.get(
            "/PMIS/task/add_task", 
            { contact: get_username(), sessionid: sessionid },
            function(result){
                if (result.status) {
                    return result.data
                }
            }
        );
        return data.data
    }

    //保存任務並在彈出框中加載該任務
    function post_task(new_task){
        $.ajax({
            type: "POST",
            url: "/PMIS/task/add_task",
            data: new_task,
            datatype: "json",
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            success: function (result) {
                if (result.status) {
                    if (SWApp.os.isAndroid || SWApp.os.isPhone) {
                        model_task_form.set_pk(result.data.pk);
                        model_task_form.init_data(result.data.pk);
                    }else {
                        pc_task_form.set_pk(result.data.pk);
                        pc_task_form.init_data(result.data.pk);
                        $("a[href='#task_detail']").addClass("active").parent().siblings().children().removeClass('active');
                        $('#task_detail').addClass("active").addClass("show").siblings().removeClass('active').removeClass('show');
                    }
                    alert('保存任務成功！')
                }
            },
            error: function () {
                alert("程序異常!");
            }
        })
    }

    //修改任務
    function update_task(new_task){
        $.ajax({
            type: "POST",
            url: `/PMIS/task/update_task?pk=${new_task.inc_id}`,
            data: new_task,
            datatype: "json",
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            success: function (result) {
                if (!result.status) {
                    alert('修改任務失敗！')
                }
            },
            error: function () {
                alert("程序異常!");
            }
        })
    }
    
    //轉任務按鈕點擊方法
    $('[name="trun_to_task"]').on('click',function(){
        var select_nodes = $('#'+treeId).jstree(true).get_selected(true)
        if(!select_nodes.length>0){
            alert('請選擇session！')
            return
        }
        for(select_node of select_nodes){
            if(select_node.data.pid== ''){
                alert('請選擇session！')
                return
            }
        }
        if(confirm("你確定要轉入該session碼?")){
            //轉任務:獲取選中session的默認數據並將原任務除部分字段以外的字段值寫入session數據中，並保存
            for(select_node of select_nodes){
                var sessionId = select_node.data.pid+'-'+select_node.data.tid
                old_task = $('#'+formName+' form').serializeObject()
                select_parents = select_node.parents
                if (SWApp.os.isAndroid || SWApp.os.isPhone) {
                    model_task_form.set_pk(undefined);
                    model_task_form.init_data({sessionid:sessionId});
                }else {
                    pc_task_form.set_pk(undefined);
                    pc_task_form.init_data({sessionid:sessionId});
                }
                // get_default_task(sessionId).then((reason)=>{
                //     var old_task = $('#'+formName+' form').serializeObject()
                //     var new_task = reason
                //     var task_keys = Object.keys(old_task)
                //     for(task_key of task_keys){
                //         if(!['inc_id','pid','tid','taskid','relationid','schpriority','schedulestate','editionid'].includes(task_key))
                //             new_task[task_key]=old_task[task_key]
                //     }
                //     new_task['relationid']=old_task['pid']+ "-" + String(old_task['tid']) + "-" + String(old_task['taskid'])
                //     var select_parents = select_node.parents
                //     for(var i=0;i<select_parents.length;i++){
                //         if(select_parents[i]=='#'){
                //             new_task['subprojectid']=select_parents[i-1].slice(0,5);
                //             break;
                //         }
                //     }
                //     new_task['progress']='N'
                //     //轉任務時若是將會議轉為任務則判斷是否為優先處理會議並將會議設置為已分配
                //     // if((old_task['class_field']==1) && task_session.indexOf((old_task['pid']+ "-" + String(old_task['tid']))!=-1))new_task['hoperation']='F'
                //     // if(task_session.indexOf((old_task['pid']+ "-" + String(old_task['tid']))!=-1)){
                //     //     old_task['process']='A'
                //     //     update_task(old_task)
                //     // }
                //     post_task(new_task)
                // })
                
            }
        }
    });
    
    //新增任務按鈕點擊方法
    $('[name="create_task"]').on('click',async function(){
        var select_nodes = $('#'+treeId).jstree(true).get_selected(true)
        if(!select_nodes.length>0){
            alert('請選擇session！')
            return
        }
        if(select_nodes[0].data.pid== ''){
            alert('請選擇session！')
            return
        }
        var sessionId = select_nodes[0].data.pid+'-'+select_nodes[0].data.tid
        if (SWApp.os.isAndroid || SWApp.os.isPhone) {
            model_task_form.set_pk(undefined);
            model_task_form.init_data({sessionid:sessionId});
        }else {
            pc_task_form.set_pk(undefined);
            pc_task_form.init_data({sessionid:sessionId});
        }
    });
    
    //刪除任務按鈕點擊方法
    $('[name="delete_task"]').on('click',async function(){
        var old_task = $('#'+formName+' form').serializeObject()
        if(old_task.inc_id =='' || old_task.inc_id == null){
            alert('未保存任務，無需刪除！')
            return
        }
        if(confirm("你確定要刪除該任務嗎?")){
            $.ajax({
                type: "POST",
                url: `/PMIS/task/delete_task/${old_task.inc_id}`,
                datatype: "json",
                beforeSend: function (request) {
                    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                },
                success: function (result) {
                    if (result.status) {
                        alert('刪除任務成功！')
                        var id = "#add-task"
                        if (SWApp.os.isAndroid || SWApp.os.isPhone) id = "#add-task-module"
                        $(id).modal("hide");
                    }
                },
                error: function () {
                    alert("程序異常!");
                }
            })
        }
    });

});