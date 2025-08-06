$(function () {
    //var url = "http://183.63.205.83:8000";
    ///////////////初始化UI///////////////////
    var nav_links = $(".header-nav .nav-link")
    var nav = $(nav_links[nav_links.length - 1])
    nav.attr("data-toggle", "modal");
    if (SWApp.os.isAndroid || SWApp.os.isPhone)
        nav.attr("data-target", "#add-task-module");
    else
        nav.attr("data-target", "#add-task");
    $("#add-task-module .nav-link").click(function () {
        $("#add-task-module .cHeight").css('height', $("#add-task-module .card-body").height());
    });

    var contact_cmpt = new SWCombobox("contact", "聯繫人", "/PMIS/user/get_user_names")
    contact_cmpt.input_dom.attr("data-live-search", "true");
    $("#user").append(contact_cmpt.dom);

    var progress_cmpt = new SWCombobox("progress", "進度", "/PMIS/task/progresses")
    $("#user").append(progress_cmpt.dom);
    var opera_cmpt = new SWCombobox("hoperation", "操作", ["F"]);
    $("#user").append(opera_cmpt.dom);
    var priority_cmpt = new SWCombobox("priority", "優先級", ["888", "8888", "8889"]);
    $("#user").append(priority_cmpt.dom);
    var class_cmpt = new SWCombobox("class_field","Class",[{value:1, desc:"Class 1"}, {value:2, desc:"Class 2"}, {value:3, desc:"Other"}], undefined, "value", "desc");
    $("#user").append(class_cmpt.dom);

    var planbdate_cmpt = new SWDate("planbdate","datetime-local","計劃開始");
    $("#planDate").prepend(planbdate_cmpt.dom);
    var planedate_cmpt = new SWDate("planedate","datetime-local","計劃结束");
    $("#planDate").prepend(planedate_cmpt.dom);

    var tasktype_cmpt = new SWCombobox("tasktype", "任務分類", "/PMIS/tasktype/tasktype_list", undefined, 'tasktype', 'description');
    $("#tasktype_c").append(tasktype_cmpt.dom);
    var subtasktype_cmpt = new SWCombobox("subtasktype", "子任務分類", []);
    $("#subtasktype_c").append(subtasktype_cmpt.dom);
    var diff_cmpt = new SWCombobox("diff", "難度", ["1", "2", "3"])
    $("#diff_c").append(diff_cmpt.dom);
    var sms_cmpt = new SWRadiobox("isradio", "sendSMS",true)
    $("#email").append(sms_cmpt.dom);   
    var email_cmpt = new SWRadiobox("isradio", "Off. hrs",false)
    $("#email").append(email_cmpt.dom);      
    $("#add-task-module form").prepend((new SWText("pid","hidden")).dom)
    $("#add-task-module form").prepend((new SWText("tid","hidden")).dom)
    $("#add-task-module form").prepend((new SWText("taskid","hidden")).dom)
    $("#add-task-module form").prepend((new SWText("relationgoalid","hidden")).dom)
    $("#task-description textarea").attr("name", "task");

    //處理保存按鈕的popver屬性
    $("#add-task-module .save").attr("data-container","body")
    $("#add-task-module .save").attr("data-toggle","popover")
    $("#add-task-module .save").attr("data-placement","top")
    $("#add-task-module .modal-header .floating-button").addClass("add");
    
    $('.nav-tabs .nav-item a').on('click',function(e) {
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

    // PC
    $("#add-task form").prepend((new SWText("pid","hidden")).dom)
    $("#add-task form").prepend((new SWText("tid","hidden")).dom)
    $("#add-task form").prepend((new SWText("taskid","hidden")).dom)    
    $("#add-task form").prepend((new SWText("relationgoalid","hidden")).dom)
    var description_pc = new SWTextarea("task", "任務描述",6)
    $("#description").append(description_pc.dom);
    var remark_pc = new SWTextarea("remark", "備註",3)
    $("#remark").append(remark_pc.dom);
    var users_pc = new SWCombobox("contact", "聯繫人", "/PMIS/user/get_user_names")
    users_pc.input_dom.attr("data-live-search", "true");
    $("#users").append(users_pc.dom);
    var priority_pc = new SWCombobox("priority", "優先級", ["888", "8888", "8889"])
    $("#priority_p").append(priority_pc.dom);
    var class_pc = new SWCombobox("class_field","Class",[{value:1, desc:"Class 1"}, {value:2, desc:"Class 2"}, {value:3, desc:"Other"}], undefined, "value", "desc");
    $("#class").append(class_pc.dom);
    var progress_pc = new SWCombobox("progress", "進度", "/PMIS/task/progresses")
    $("#progress_p").append(progress_pc.dom);
    var opera_pc = new SWCombobox("hoperation", "操作", ["F"]);
    $("#operation").append(opera_pc.dom);
    var score_pc = new SWText("score", "number","Score");
    $("#score").append(score_pc.dom);
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


    ///////////////初始化UI///////////////////
    var model_task_form = new SWBaseForm("#add-task-module");
    model_task_form.create_url = "/PMIS/task/add_task";
    model_task_form.update_url = "/PMIS/task/update_task?pk=[[pk]]"
    model_task_form.pk_in_url = false;
    model_task_form.on_after_init = function(data) {
        $("#add-task-module .SWCombobox select[name='subtasktype']").data("init-data", data["subtasktype"]);
        $("#add-task-module .SWCombobox select[name='tasktype']").change();
        $('#add-task-module a[href="#task-description"]').tab("show");
        $("#add-task-module p").text("{0}-{1}-{2}".format(data.pid, data.tid, data.taskid));
        
    }
    model_task_form.on_after_save = function(data) {
        $("#add-task-module p").text("{0}-{1}-{2}".format(data.pid, data.tid, data.taskid));
        $('#add-task-module a[href="#task-description"]').tab("show");                    
    }

    var pc_task_form = new SWBaseForm("#add-task");
    pc_task_form.create_url = "/PMIS/task/add_task";
    pc_task_form.update_url = "/PMIS/task/update_task?pk=[[pk]]"
    pc_task_form.pk_in_url = false;
    pc_task_form.on_after_init = function(data) {
        $("#add-task .SWCombobox select[name='subtasktype']").data("init-data", data["subtasktype"]);
        $("#add-task .SWCombobox select[name='tasktype']").change();
        $("#add-task .cust_taskId p").text("{0}-{1}-{2}".format(data.pid, data.tid, data.taskid));        
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
});