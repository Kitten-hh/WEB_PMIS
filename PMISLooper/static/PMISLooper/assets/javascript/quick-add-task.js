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
    var nav_links = $(".top-bar-item-right .header-nav .nav-item:first .dropdown-menu")
    var nav = $(nav_links).find(".addTasks")
    var treeId = '' //將session數狀圖顯示的容器的id
    var formName = ''
    var task_session = []
    var task_delete = []
    var old_task = undefined //轉任務時用於存在被轉任務內容
    var select_parents = undefined //轉任務時設置關聯任務的完整taskNo
    var file_list = {} //文件信息
    var file_array = [] //文件列表
    var relationID = ''
    var hoperation_type = {};
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
        task_delete = []
        console.log(task_delete)
        $("#add-task-module .cHeight").css('height', $("#add-task-module .card-body").height());
    });

    var contact_cmpt = new SWCombobox("contact", gettext('Contact'), window.CommonData.PartUserNames)
    contact_cmpt.input_dom.attr("data-live-search", "true");
    $("#user").append(contact_cmpt.dom);

    var progress_cmpt = new SWCombobox("progress", gettext('Progress'), window.CommonData.TaskProgress)
    $("#user").append(progress_cmpt.dom);
    var opera_cmpt = new SWCombobox("hoperation", gettext('Hoperation'), window.CommonData.TaskHOperation);
    $("#user").append(opera_cmpt.dom);
    var priority_cmpt = new SWCombobox("priority", gettext('Priority'), ["888", "8888", "8889"]);
    $("#user").append(priority_cmpt.dom);
    var class_cmpt = new SWCombobox("class_field", gettext('Class'),[{value:1, desc:"Class 1"}, {value:2, desc:"Class 2"}, {value:3, desc:"Other"}], undefined, "value", "desc");
    $("#user").append(class_cmpt.dom);

    var planbdate_cmpt = new SWDate("planbdate","datetime-local",gettext('PlanBDate'));
    $("#planDate").prepend(planbdate_cmpt.dom);
    var planedate_cmpt = new SWDate("planedate","datetime-local",gettext('PlanEDate'));
    $("#planDate .SWDate").append(planedate_cmpt.dom);

    var bdate_cmpt = new SWDate("bdate","datetime-local",gettext('BDate'));
    $("#actualDate").append(bdate_cmpt.dom);
    var edate_cmpt = new SWDate("edate","datetime-local",gettext('EDate'));
    $("#actualDate").append(edate_cmpt.dom);

    var tasktype_cmpt = new SWCombobox("tasktype", gettext('Task Type'), window.CommonData.TaskType, undefined, 'tasktype', 'description');
    $("#tasktype_c").append(tasktype_cmpt.dom);
    var subtasktype_cmpt = new SWCombobox("subtasktype", gettext('Sub TaskType'), []);
    $("#subtasktype_c").append(subtasktype_cmpt.dom);
    var diff_cmpt = new SWCombobox("diff", gettext('Diff'), ["1", "2", "3"])
    $("#diff_c").append(diff_cmpt.dom);
    var schedule_priority_cmpt = new SWText("schpriority","number",gettext('SchPriority'))
    $("#schedule_priority_c").append(schedule_priority_cmpt.dom);
    var process_cmpt = new SWCombobox("process", gettext('Process'), window.CommonData.TaskProcess);
    $("#process_c").append(process_cmpt.dom);
    var taskcategory_cmpt = new SWCombobox("taskcategory", gettext('TaskCategory'), window.CommonData.TaskCategory);
    $("#taskcategory_c").append(taskcategory_cmpt.dom);

    var relationid_cmpt = new SWText("relationid", "text",gettext('RelationID'));
    $("#email .email_wrapper").before(relationid_cmpt.dom);
    var relationGoalId_cmpt = new SWText("relationgoalid", "text",gettext('RelationGoalID'));
    $("#email .email_wrapper").before(relationGoalId_cmpt.dom);


    var sms_cmpt = new SWRadiobox("isradio", gettext('sendSMS'),true)
    $(".email_wrapper").append(sms_cmpt.dom);   
    var email_cmpt = new SWRadiobox("isradio", gettext('Off. hrs'),false)
    $(".email_wrapper").append(email_cmpt.dom); 
    var dayjoy_cmpt = new SWCheckbox("ischeck", gettext('dayjob'), true)
    $(".email_wrapper").append(dayjoy_cmpt.dom);          

        
    //新增代碼
    var flowchartno_cmpt = new SWText("flowchartno", "text",gettext('Flowchart'));
    $("#flowchartno_c").append(flowchartno_cmpt.dom);
    var udf04_cmpt = new SWText("udf04", "text",gettext('FrameName'));
    $("#udf04_c").append(udf04_cmpt.dom);
    var udf08_cmpt = new SWText("udf08", "text", gettext("RelationMustID"))
    $("#relationMustID_c").append(udf08_cmpt.dom);
    var reference_cmpt = new SWText("reference", "text",gettext('Reference'));
    $("#reference_c").append(reference_cmpt.dom);
    var delayday_cmpt = new SWText("delayday", "text",gettext('Delay Day'));
    $("#delayday_c").append(delayday_cmpt.dom);
    var requestdate_cmpt = new SWText("requestdate", "datetime-local",gettext('RequestDate'));
    $("#requestdate_c").append(requestdate_cmpt.dom);
    var manday_cmpt = new SWText("manday", "text",gettext('ManDay'));
    $("#manday_c").append(manday_cmpt.dom);
    var escore_cmpt = new SWText("lookupscore", "text",gettext('EScore'));
    $("#escore_c").append(escore_cmpt.dom);

    $("#add-task-module form").prepend((new SWText("inc_id","hidden")).dom)
    $("#add-task-module form").prepend((new SWText("subprojectid","hidden")).dom)
    $("#add-task-module form").prepend((new SWText("pid","hidden")).dom)
    $("#add-task-module form").prepend((new SWText("tid","hidden")).dom)
    $("#add-task-module form").prepend((new SWText("taskid","hidden")).dom)
    $("#add-task-module form").prepend((new SWText("editionid","hidden")).dom)
    $("#add-task-module form").prepend((new SWText("docpath","hidden")).dom)
    
    $("#task-description textarea").attr("name", "task");
    //初始TextArea href
    var task_module_textarea_href = new SWTextAreaHref("#task-description textarea");
    var remark_module_textarea_href = new SWTextAreaHref("input[name='remark']");    

    // 
    var taskSwitch_users_m = new SWText("contact_session", "text", gettext('Contact'))
    $("#ts_user_m").append(taskSwitch_users_m.dom);

    var taskSwitch_desc_m = new SWText("description", "text",gettext('Description'));
    $("#ts_desc_m").append(taskSwitch_desc_m.dom);

    var taskSwitc_recordid_m = new SWText("recordid", "text", gettext('RecordID'))
    $("#ts_recordid_m").append(taskSwitc_recordid_m.dom);

    var taskSwitc_session_m = new SWText("session","text",gettext('PID'));
    $("#ts_session_m").append(taskSwitc_session_m.dom);
    
    // 添加上報號在關聯信息 
    var udf01_cmpt = new SWText("udf01","text", gettext('System Issue Rpt No'));  // 系統問題上報號
    $("#udf01").append(udf01_cmpt.dom);
    $("#udf01 .form-group").css("position", "relative"); // 给 #udf01 额外添加样式
    $('input[name="udf01"]').css("padding-right", "30px").attr('title', gettext('Please double-click to view.'));
    // 创建并插入 <span> 元素到 input[name="udf01"] 后面
    const translatedText = gettext('Please double-click to view.');
    $(`<span class="oi oi-magnifying-glass" title="${translatedText}" style="position: absolute; top: 41px; right: 12px; font-size: 13px; cursor: pointer;"></span>`).insertAfter('input[name="udf01"]');

    $('input[name="udf01"]').hover(
        // function () {
        //     // 鼠标悬停时改变背景渐变和边框颜色
        //     $(this).css({
        //         "background": "linear-gradient(180deg, #f6f7f9, #f6f7f9)",
        //         "border-color": "#d7dce5",
        //     });
        // },
        function () {
            // 移开鼠标时恢复默认背景渐变和边框颜色
            // $(this).css({
            //     "background": "linear-gradient(180deg, #fff, #f6f7f9)",
            //     "border-color": "#d7dce5",
            // });
        }
    );

    //處理保存按鈕的popver屬性
    $("#add-task-module .save").attr("data-container","body")
    $("#add-task-module .save").attr("data-toggle","popover")
    $("#add-task-module .save").attr("data-placement","top")
    $("#add-task-module .modal-header .addtaskbtn").addClass("add");
    $("#add-task .modal-footer .addtaskbtn").addClass("add");
    
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
    $("#add-task form").prepend((new SWText("editionid","hidden")).dom)
    $("#add-task form").prepend((new SWText("docpath","hidden")).dom)
    
    var description_pc = new SWTextarea("task", gettext('Task'),4)
    $("#add-task #description").append(description_pc.dom);
    var remark_pc = new SWTextarea("remark", gettext('Remark'),3)
    $("#remark").append(remark_pc.dom);
    //初始化TextArea href
    var task_pc_textarea_href = new SWTextAreaHref(description_pc.input_dom);
    var remark_pc_textarea_href = new SWTextAreaHref(remark_pc.input_dom);    
    
    var users_pc = new SWCombobox("contact", gettext('Contact'), window.CommonData.PartUserNames)
    users_pc.input_dom.attr("data-live-search", "true");
    $("#add-task #users").append(users_pc.dom);
    var priority_pc = new SWCombobox("priority", gettext('Priority'), ["888", "8888", "8889"])
    $("#add-task #priority_p").append(priority_pc.dom);
    var taskcategory_pc = new SWCombobox("taskcategory", gettext('TaskCategory'), window.CommonData.TaskCategory);
    $("#taskcategory_p").append(taskcategory_pc.dom);
    var class_pc = new SWCombobox("class_field",gettext('Class'),[{value:1, desc:"Class 1"}, {value:2, desc:"Class 2"}, {value:3, desc:"Other"}], undefined, "value", "desc");
    $("#class").append(class_pc.dom);
    var progress_pc = new SWCombobox("progress", gettext('Progress'), window.CommonData.TaskProgress)
    $("#progress_p").append(progress_pc.dom);
    var opera_pc = new SWCombobox("hoperation", gettext('Hoperation'), window.CommonData.TaskHOperation);
    $("#operation").append(opera_pc.dom);
    var process_pc = new SWCombobox("process", gettext('Process'), window.CommonData.TaskProcess);
    $("#add-task #process").append(process_pc.dom);
    var score_pc = new SWText("score", "number",gettext('Score'));
    $("#score").append(score_pc.dom);
    var schedule_priority_pc = new SWText("schpriority","number",gettext('SchPriority'))
    $("#schedule_priority").append(schedule_priority_pc.dom);
    var planbdate_pc = new SWDate("planbdate","datetime-local",gettext('PlanBDate'));
    $("#planbdate").append(planbdate_pc.dom);
    var planedate_pc = new SWDate("planedate","datetime-local",gettext('PlanEDate'));
    $("#planedate").append(planedate_pc.dom);
    var bdate_pc = new SWDate("bdate","datetime-local",gettext('BDate'));
    $("#bdate").append(bdate_pc.dom);
    var edate_pc = new SWDate("edate","datetime-local",gettext('EDate'));
    $("#edate").append(edate_pc.dom);    
    var tasktype_pc = new SWCombobox("tasktype", gettext('Task Type'), window.CommonData.TaskType, undefined, 'tasktype', 'description');
    $("#tasktype_p").append(tasktype_pc.dom);
    var subtasktype_pc = new SWCombobox("subtasktype", gettext('Sub TaskType'), []);
    $("#subtasktype_p").append(subtasktype_pc.dom);
    var diff_pc = new SWCombobox("diff", gettext('Diff'), ["1", "2", "3"])
    $("#diff_p").append(diff_pc.dom);   
    var email_pc1 = new SWRadiobox("isradio", gettext('sendSMS'), true)
    email_pc1.dom.css("display", "inline-block");
    $("#email_p").append(email_pc1.dom);
    var email_pc2 = new SWRadiobox("isradio", gettext('Off. hrs'), false)
    email_pc2.dom.css("display", "inline-block");
    $("#email_p").append(email_pc2.dom);
    var dayjoy_pc = new SWCheckbox("ischeck", gettext('dayjob'), true)
    $("#dayjoy").append(dayjoy_pc.dom);       

    var ts_session = new SWText("session","text",gettext('PID'));
    $("#task_switch_session").append(ts_session.dom);

    var recordid = new SWText("recordid","text",gettext('RecordID'));
    $("#task_switch_recordid").append(recordid.dom);

    var switch_users_pc = new SWText("contact_session","text",gettext('Contact'));
    $("#task_switch_users").append(switch_users_pc.dom);

    // var recordid = new SWCombobox("recordid", "项目编号", "/PMIS/subproject/get_all_recordid",undefined, 'recordid','recordid')
    // recordid.input_dom.attr("data-live-search", "true");
    // $("#task_switch_recordid").append(recordid.dom);

    // var switch_users_pc = new SWCombobox("contact_session", "聯繫人", window.CommonData.PartUserNames)
    // switch_users_pc.input_dom.attr("data-live-search", "true");
    // $("#task_switch_users").append(switch_users_pc.dom);

    var task_switch_desc = new SWText("description", "text",gettext('Description'));
    $("#task_switch_description").append(task_switch_desc.dom);

    var relationid = new SWText("relationid", "text",gettext('RelationID'));
    $("#relationid").append(relationid.dom);

    var relationGoalId = new SWText("relationgoalid", "text",gettext('RelationGoalID'));
    $("#relationGoalId").append(relationGoalId.dom);

    
    //新增代碼
    var relationGoalId = new SWText("flowchartno", "text",gettext('Flowchart'));
    $("#flowchartno").append(relationGoalId.dom);
    var udf04 = new SWText("udf04", "text",gettext('FrameName'));
    $("#udf04").append(udf04.dom);

    var udf08 = new SWText("udf08", "text", gettext("RelationMustID"))
    $("#relationMustID").append(udf08.dom);

    //syl 20240807
    var users_bft = new SWCombobox("contact_relation", gettext('Contact'), window.CommonData.PartUserNames)
    users_bft.input_dom.attr("data-live-search", "true");
    $("#add-task #users_other").append(users_bft.dom);
    $("#add-task a.users_other_relation").on('click', function(e) {
        var taskno = $('#add-task div.cust_taskId p.text-mute').html();
        var relation_user = $('select[name="contact_relation"]').val()
        var user = $('#add-task select[name="contact"]').val();
        if (relation_user === '') return alert(gettext('Contact cannot be empty')); //聯繫人不能為空
        if (relation_user === user) return alert(gettext('Contacts must be unique')); //聯繫人不能相同
        e.stopPropagation(); //阻止事件傳播
        $.ajax({
            type: "POST",
            url: "/PMIS/task/add_otheruser_relation_task/",
            // data: `${taskno};${relation_user}`,
            data: {taskno: taskno, relation_user: relation_user},
            datatype: "json",
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", getCookie('csrftoken')); //設置CSRF令牌
            },
            success: function (res) {
                if (res.status){
                    $("#relationid input[name='relationid']").val(res.data)
                    var msgTemplate = gettext('Task has been assigned to ({user})'); //已為({user})分配任務
                    var msg = msgTemplate.replace('{user}',relation_user); // 使用 relation_user 替换 {user}
                    alert(msg); //已為relation_user分配任務
                }else{
                    alert(gettext('fail')) //保存失敗
                } 
            },
        })
    })
    //syl 20240807

    
    var reference = new SWText("reference", "text",gettext('Reference'));
    $("#reference").append(reference.dom);
    var delayday = new SWText("delayday", "text",gettext('Delay Day'));
    $("#delayday").append(delayday.dom);
    var requestdate = new SWText("requestdate", "datetime-local",gettext('RequestDate'));
    $("#requestdate").append(requestdate.dom);
    var manday = new SWText("manday", "text",gettext('ManDay'));
    $("#manday").append(manday.dom);
    var escore = new SWText("lookupscore", "text",gettext('EScore'));
    $("#escore").append(escore.dom);
    // var schedulestate = new SWCheckbox("schedulestate", "是否排期")
    // $("#schedulestate").append(schedulestate.dom);      

    var reportPerson = new SWText("udf09", "text",gettext('Reporter'));
    $("#report_person").append(reportPerson.dom);

    var reportDepartment = new SWText("udf11", "text",gettext('ReportingDept'));
    $("#report_department").append(reportDepartment.dom);

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
        get_filelist("{0}-{1}-{2}".format(data.pid.replaceAll(' ',''),data.tid,data.taskid))
        $(".approve_required").attr("disabled", data.inc_id ? false : true);
    }
    model_task_form.on_after_save = function(data) {
        $("#add-task-module p").text("{0}-{1}-{2}".format(data.pid, data.tid, data.taskid));
        $('#add-task-module a[href="#task-description"]').tab("show");   
        
        if(file_list['file']!=undefined && file_list['file']!=null){
            file_list['task_inc_id'] = data.inc_id
            var filedata = objectToFormData(file_list)
            save_file(filedata) 
            get_filelist("{0}-{1}-{2}".format(data.pid.replaceAll(' ',''),data.tid,data.taskid))
        }
        if(task_delete.length>0){
            delete_old_tasks()
        }
        $("#add-task-module").data("task_info", {method:"save", data:data});
        $("#add-task-module input[name='inc_id']").val(data.inc_id);
        $(".approve_required").attr("disabled", data.inc_id ? false : true);                        
    }
    
    model_task_form.on_init_format = function(data) {
        data.requestdate = data.requestdate==null ? null:FormatSecond(data.requestdate)
        data.planbdate = data.planbdate==null ? null:FormatSecond(data.planbdate)
        data.planedate = data.planedate==null ? null:FormatSecond(data.planedate)
        data.bdate = data.bdate==null ? null:FormatSecond(data.bdate)
        data.edate = data.edate==null ? null:FormatSecond(data.edate)
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
                        parentid = i-1>=0?select_parent[i-1].slice(0,5):'';
                        break;
                    }
                }
                $('#'+treeId).jstree(true).deselect_node(selected[0].id)
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
                    }else{
                        $('.cust_projectDetails span').text('');   
                    }
                    if(result_list[0].tasklist.length>0){
                        var tasklist = result_list[0].tasklist[0]
                        $('.cust_module_name span').text(tasklist.sdesp);       
                        $('.cust_module_flowchart span').text(tasklist.flowchartno);       
                    }else{
                        $('.cust_module_name span').text('');       
                        $('.cust_module_flowchart span').text('');   
                    }
                }
            }
        }); 
        get_filelist("{0}-{1}-{2}".format(data.pid.replaceAll(' ',''),data.tid,data.taskid))
        $(".approve_required").attr("disabled", data.inc_id ? false : true);
    }

    
    pc_task_form.on_after_save = function(data) {
        if(file_list['file']!=undefined && file_list['file']!=null){
            file_list['task_inc_id'] = data.inc_id
            var filedata = objectToFormData(file_list)
            save_file(filedata) 
            get_filelist("{0}-{1}-{2}".format(data.pid.replaceAll(' ',''),data.tid,data.taskid))
        }
        if(task_delete.length>0){
            delete_old_tasks()
        }
        $("#add-task").data("task_info", {method:"save", data:data});
        $("#add-task input[name='inc_id']").val(data.inc_id);
        $(".approve_required").attr("disabled", data.inc_id ? false : true);
    }

    pc_task_form.on_init_format = function(data) {
        data.requestdate = data.requestdate==null ? null:FormatSecond(data.requestdate)
        data.planbdate = data.planbdate==null ? null:FormatSecond(data.planbdate)
        data.planedate = data.planedate==null ? null:FormatSecond(data.planedate)
        data.bdate = data.bdate==null ? null:FormatSecond(data.bdate)
        data.edate = data.edate==null ? null:FormatSecond(data.edate)
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
        if(task_delete.length<=0)
            data['relationid']= "{0}-{1}-{2}".format(old_task['pid'],old_task['tid'],old_task['taskid'])
        //子工程編號
        for(var i=0;i<select_parents.length;i++){
            if(select_parents[i]=='#'){
                if(select_parents.length<2){
                    var select_nodes = $('#'+treeId).jstree(true).get_selected(true)
                    var projectid = select_nodes[0].data.parentid
                    projectid = projectid.split('_')
                    data['subprojectid'] = projectid.length>0?projectid[0]:''
                }else{
                    data['subprojectid'] = select_parents.length>2?select_parents[i-1].slice(0,5):''
                }
                break;
            }
        }
        old_task = undefined
        select_parents = undefined
        return data
    }

    //刪除原任務
    function delete_old_tasks(){
        for(var task of task_delete){
            $.ajax({
                type: "POST",
                url: `/PMIS/task/delete_task/${task['inc_id']}`,
                datatype: "json",
                processData: false, 
                contentType: false, 
                beforeSend: function (request) {
                    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                },
                success: function (response) {
                    // 處理成功後的返回數據
                    if (!response.status)
                        alert('刪除原任務失敗！')
                    else
                        task_delete = []
                },
                error: function () {
                    alert("程序異常!");
                }
    
            })
        }
    }

    //添加任務
    $("a[data-target='#add-task-module']").on("click", function () {
        model_task_form.set_pk(undefined);
        model_task_form.init_data();
    });

    //TaskType改變事件
    tasktype_cmpt.input_dom.on("change", function () {
        var tasktype = $(this).val();
        if (tasktype == "")
            return;
        var init_data = subtasktype_cmpt.input_dom.data("init-data");
        subtasktype_cmpt = new SWCombobox("subtasktype", gettext('Sub TaskType'), "/PMIS/tasktype/subtasktype_list/" + tasktype, init_data, 'tasktype', 'description');
        $("#subtasktype_c").empty();
        $("#subtasktype_c").append(subtasktype_cmpt.dom);
        //SubTaskType改變事件
        subtasktype_cmpt.input_dom.on("change", function () {
            var subtasktype = $(this).val();
            if (subtasktype == "")
                return;
            Set_escore('#add-task-module')
        });
    
    });

    //Diff改變事件
    diff_cmpt.input_dom.on("change", function () {
        var diff = $(this).val();
        if (diff == "")
            return;
        Set_escore('#add-task-module')
    });

    //TaskType改變事件
    tasktype_pc.input_dom.on("change", function(){
        var tasktype = $(this).val();
        if (tasktype == "")
            return;
        var init_data = subtasktype_pc.input_dom.data("init-data");
        subtasktype_pc = new SWCombobox("subtasktype", gettext('Sub TaskType'), "/PMIS/tasktype/subtasktype_list/" + tasktype, init_data, 'tasktype', 'description');
        $("#subtasktype_p").empty();
        $("#subtasktype_p").append(subtasktype_pc.dom);
        //SubTaskType改變事件
        subtasktype_pc.input_dom.on("change", function () {
            var subtasktype = $(this).val();
            if (subtasktype == "")
                return;
            Set_escore('#add-task')
        });
    })  

    
    //Diff改變事件
    diff_pc.input_dom.on("change", function () {
        var diff = $(this).val();
        if (diff == "")
            return;
        Set_escore('#add-task')
    });

    progress_pc.input_dom.on("change", function(){
        var progress = $(this).val();
        var old_progress = process_pc.input_dom.data("old_value");
        if (progress == "I") {
            bdate_pc.input_dom.val(Date.today().toString("yyyy-MM-ddTHH:mm"));
            edate_pc.input_dom.val("");
        }else if (progress == "T") {
            if (old_progress != "I") {
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
            if (old_progress != "I") {
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
    
    //操作字段變化事件
    opera_cmpt.input_dom.on("change", function(){
        var progress = $(this).val();
        var old_progress = process_cmpt.input_dom.data("old_value");
        if(progress=='P'){
            class_cmpt.input_dom.val(1);
            class_cmpt.dom.find(".filter-option-inner-inner").html('Class1')
            // var class_cmpt = new SWCombobox("class_field",gettext('Class'),[{value:1, desc:"Class 1"}, {value:2, desc:"Class 2"}, {value:3, desc:"Other"}], 1, "value", "desc");    
            // $("#class").empty();
            // $("#class").append(class_cmpt.dom);
        }
    });
    
    //操作字段變化事件
    opera_pc.input_dom.on("change", function(){
        var progress = $(this).val();
        var old_progress = process_cmpt.input_dom.data("old_value");
        if(progress=='P'){
            class_pc.input_dom.val(1);
            class_pc.dom.find(".filter-option-inner-inner").html('Class1')
            // var class_pc = new SWCombobox("class_field",gettext('Class'),[{value:1, desc:"Class 1"}, {value:2, desc:"Class 2"}, {value:3, desc:"Other"}], 1, "value", "desc");    
            // $("#class").empty();
            // $("#class").append(class_pc.dom);
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
        if (params)
            params = Object.assign({read_task:true}, params);
        else
            params = {read_task:true};
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
        task_delete = []
        console.log(task_delete)
    }
    $("#add-task,#add-task-module").on("hidden.bs.modal", function(){
        var data = $(this).data("task_info")
        data = Object.keys(data).length == 0 ? undefined : data;
        jqueryEventBus.trigger('globalTaskOperation', data);
    });

    $("#add-task,#add-task-module").on("shown.bs.modal", function(){
        $(this).data("task_info",{});
    });    

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

    $('.task_switch_container').children().keydown(Sessionenterclick);
    $('#ts_container_m').children().keydown(Sessionenterclick);

    function debounce(func, wait) {
        var timeout;
        return function() {
            var context = this, args = arguments;
            clearTimeout(timeout);
            timeout = setTimeout(function() {
                func.apply(context, args);
            }, wait);
        };
    }
    
    // 使用防抖技术包装您的 GetSeeeionTree 方法
    var debouncedGetSeeeionTree = debounce(GetSeeeionTree, 500); // 500ms 作为延迟时间
    
    // 在输入事件上应用防抖函数
    $('.task_switch_container').find('input').on('input', debouncedGetSeeeionTree);
    

    $('.task_switch_container').find('input').on('input',debouncedGetSeeeionTree)
    //回車鍵點方法
    function Sessionenterclick(e){
        GetSeeeionTree() 
    }

    //初始化樹狀圖
    $('#'+treeId).jstree({
        "core": {
            "worker":false,
            event: {
                touchstart: {
                  passive: true
                }
            },             
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
        var contact = $('#ts_user_m [name="contact_session"]').val()  //聯繫人
        var session = $('#ts_session_m [name="session"]').val()     //工程編號
        var recordid = $('#ts_recordid_m [name="recordid"]').val()   //子工程編號
        var description = $('#ts_desc_m [name="description"]').val() //描述
      }else{
        var contact = $('#task_switch_users [name="contact_session"]').val() //聯繫人
        var session = $('#task_switch_session [name="session"]').val()     //工程編號
        var recordid = $('#task_switch_recordid [name="recordid"]').val()   //子工程編號
        var description = $('#task_switch_description [name="description"]').val() //描述
      }
        var url = `/PMIS/session/session_sessionList?contact=${contact}&pid=${session}&recordid=${recordid}&desc=${description}`;
        $.get(url,function(result){
            if (result.status) {
                var jsonarray = new Array();
                var parentArray = new Array();
                var arrays = result.data;
                //獲取所有節點ID
                for (var i = 0; i < arrays.length; i++) {
                    parentArray.push(arrays[i].keyid);
                }
                for (var i = 0; i < arrays.length; i++) {
                    if(parentArray.indexOf(arrays[i].parentid)==-1 && arrays[i].levelnum!=1){
                        parentidlist = arrays[i].parentid.split('_')
                        if(parentidlist.length>0){
                            arrays[i].parentid= parentidlist[0]    
                        }
                    }
                    var arr = {
                        "id": arrays[i].keyid,
                        "parent": arrays[i].parentid == '' || parentArray.indexOf(arrays[i].parentid)==-1 ? "#" : arrays[i].parentid,
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
        task_delete = []
        old_task = $('#'+formName+' form').serializeObject()

        SWHintMsg.showToastModal(gettext('Important Note'), gettext('Delete the original task?'), "confirm",'',gettext('Yes'),gettext('No')).then((value) => {
            if (value){
                if (old_task.inc_id!=undefined && old_task.inc_id!=null && old_task.inc_id!='')
                    task_delete.push({'inc_id':old_task.inc_id,'pid':old_task.pid,'tid':old_task.tid,'taskid':old_task.taskid})
                console.log(task_delete)
            }
        });
        // if(confirm("是否刪除原任務?")){
        //     if (old_task.inc_id!=undefined && old_task.inc_id!=null && old_task.inc_id!='')
        //         task_delete.push({'inc_id':old_task.inc_id,'pid':old_task.pid,'tid':old_task.tid,'taskid':old_task.taskid})
        //     console.log(task_delete)
        // }
        // if(confirm("你確定要轉入該session碼?")){
            //轉任務:獲取選中session的默認數據並將原任務除部分字段以外的字段值寫入session數據中，並保存
            for(select_node of select_nodes){
                var sessionId = select_node.data.pid+'-'+select_node.data.tid
                // old_task = $('#'+formName+' form').serializeObject()
                select_parents = select_node.parents
                if (SWApp.os.isAndroid || SWApp.os.isPhone) {
                    model_task_form.set_pk(undefined);
                    model_task_form.init_data({sessionid:sessionId});
                    $('#switchMobileTaskWrapper').modal('hide');
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
        // }
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
        initParams = $(this).data("initParams");
        if (SWApp.os.isAndroid || SWApp.os.isPhone) {
            model_task_form.set_pk(undefined);
            if (initParams)
                model_task_form.init_data($.extend({sessionid:sessionId}, initParams));
            else
                model_task_form.init_data({sessionid:sessionId});
            $('#switchMobileTaskWrapper').modal('hide');
        }else {
            pc_task_form.set_pk(undefined);
            if (initParams)
                pc_task_form.init_data($.extend({sessionid:sessionId}, initParams));
            else
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
                        $(id).data("task_info", {method:"del", data:result.data});                
                    }
                },
                error: function () {
                    alert("程序異常!");
                }
            })
        }
    });



    //文件輸入框改變事件
    $('input[name="avatar"]').on("change", function(e){
      var thefile = e.target.files[0];
      //文件信息
      file_list ={'file':thefile}
    })

    //保存文件
    function save_file(thedata){
        $.ajax({
            type: "POST",
            url: "/looper/metting/save_met_file",
            data: thedata,
            datatype: "json",
            processData: false, 
            contentType: false, 
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            success: function (response) {
                // 處理成功後的返回數據
                if (!response.status)
                    SWHintMsg.showToast("body", gettext('Failed to upload file'), "success")
                else{
                    SWHintMsg.showToast("body", gettext('Success to upload file'), "success")
                    file_list = {}
                }
            },
            error: function () {
                alert("程序異常!");
            }

        })
    }

    //任務流程圖輸入框雙擊事件
    $('#flowchartno').on('dblclick',function(){
        if($('input[name="flowchartno"]').val()=='')return
        var url = `http://222.118.20.236:8000/zh-hans/flowchart/preview_diagram?hidetm=true#/?flowChartNo={0}`.format($('input[name="flowchartno"]').val())
        window.open(url)
    })

    // 系統問題上報號（udf01）輸入框雙擊事件
    $('#udf01').on('dblclick',function(){
        // 跳轉到對應的系統問題上報
        if($('input[name="udf01"]').val()=='')return
        var url = `http://183.63.205.83:8000/zh-hans/systembugrpt/?rp017={0}`.format($('input[name="udf01"]').val().trim())
        window.open(url)
    })

    $('div[name="showFiles"]').on('click',function(){
        $('#uploadFileDetails_task').modal('show');
    })

    //功能：獲取文件信息
    //參數：pid-tid-taskid
    function get_filelist(taskid){
        if(taskid=='')return
        $.ajax({
            type:"GET",
            url:"/looper/task/get_task_file?taskid={0}".format(taskid),
            datatype:"json",
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            success:function(response){
                //設置查看圖片列表按鈕默認隱藏
                $('div[name="showFiles"]').attr("hidden",true)
                if(response.status){
                    if(response.data.length==0)return
                    file_array = response.data
                    show_filearray()
                }
            },
            error:function(){
                alert('程序異常')
            },
        })
    }

    //根據文件列表生成相關html
    function show_filearray(){
        var strhtml = ''
        var fileion = '<span class="fa-stack">'+
                            '<i class="fa fa-square fa-stack-2x text-primary"></i>'+
                            '<i class="fa fa-file-pdf fa-stack-1x fa-inverse""></i>'+
                        '</span>'
        for(var item of file_array){
            var headhtml = '<div class="list-group-item-figure pl-0" style="max-width: 52px;max-height: 52px;line-width: 52px;line-height: 52px;">{0}</div>'
            var bodyhtml = '<div class="list-group-item-body"><h4 class="list-group-item-title text-truncate">{0}</h4></div>'
            var footerhtml = '<div class="list-group-item-figure pr-0">{0}{1}</div>'
            var imghtml =  '<img src="{0}" alt="{1}" style="max-width: 100%;max-height: 100%;">'.format(item.fileurl,item.docname)
            var deletebtn = '<button type="button" name="deletefile" class="btn btn-sm btn-icon btn-light text-dark" inc_id="{0}"><i class="far fa-trash-alt"></i></button>'.format(item.inc_id)
            var pullbtn = '<button type="button" name="pullfile" class="btn btn-sm btn-icon btn-light text-dark" inc_id="{0}"><i class="oi oi-data-transfer-download"></i></button>'.format(item.inc_id)
            footerhtml = footerhtml.format(pullbtn,deletebtn)
            if(item.docname.lastIndexOf('.jpg') >= 0 || item.docname.lastIndexOf('.png') >= 0){
                if(item.fileurl==undefined || item.fileurl==null || item.fileurl==''){
                    headhtml = headhtml.format('<span class="tile tile-img">'+
                        '<i class="fa fa-square fa-stack-2x text-primary"></i>'+
                        '<i class="fa fa-file-image fa-stack-1x fa-inverse"></i>{0}'+
                    '</span>')
                }else{
                    headhtml = headhtml.format(imghtml)
                }
            }else{
                headhtml = headhtml.format(fileion)
            }
            if(item.fileurl==undefined || item.fileurl==null || item.fileurl==''){
                bodyhtml = bodyhtml.format('<a href="javascript:;">{0}</a>'.format(item.docname))
            }else{
                bodyhtml = bodyhtml.format('<a target="_blank" href="{0}">{1}</a>'.format(item.fileurl,item.docname))

            }
            strhtml = strhtml+'{0}'
            strhtml = strhtml.format('<div class="list-group-item">{0}{1}{2}</div>'.format(headhtml,bodyhtml,footerhtml))
        }
        //生成文件列表並顯示查看圖片列表按鈕
        $('.filelist').html(strhtml)
        $('div[name="showFiles"]').attr("hidden",false)

    }

    
    //-----------關聯任務表格--------------------------------

    $("#add-task-module [name='relationid'], #add-task [name='relationid']").on("dblclick", function(e){
        relationID = $(this).val()
        relationTable.search('').columns().search('').draw();
        $('#relationTask_modal').modal('show');   
    });
        //SolutionType表格創建
        var table = new SWDataTable("#relationTask_table", "relationTask_SWDTable"); //創建SWDataTable對象
        table.pageLength = 20; //設置每頁顯示的數量為20
        table.paging = false; //設置分頁顯示
        table.searching = false; //設置不顯示查詢框
        table.orderBy = [['inc_id', 'pid','tid','taskid']]; //設置排序
        //設置顯示字段
        table.columns = [
            { field: "taskno", label: gettext('TaskNo'),visible: false },
            { field: "pid", label: gettext('Pid')},
            { field: "tid", label: gettext('Tid')},
            { field: "taskid", label: gettext('TaskId')},

            { field: "task", label: gettext('Task')},
            { field: "contact", label: gettext('Contact') },

            { field: "planbdate", label: gettext('PlanBDate'), render:SWDataTable.DateRender},
            { field: "planedate", label: gettext('PlanBDate'), render:SWDataTable.DateRender},
            { field: "etime", label: gettext('Etime')},

            { field: "bdate", label: gettext('EDate'), render:SWDataTable.DateRender},     
            { field: "edate", label: gettext('EDate'), render:SWDataTable.DateRender},
            { field: "atime", label: gettext('Atime')},

            { field: "schpriority", label: gettext('SchPriority')},
            
            { field: "progress", label: gettext('Progress'), width: "8%"},
            { field: "remark", label: gettext('Remark')},
            

            // { field: "hoperation", label:gettext('HOperation'), render:function(data,type,row){
            //     if (Object.keys(hoperation_type).indexOf(data) != -1)
            //         return hoperation_type[data]
            //     else
            //         return data;
            // }},
            {field:"priority", label:"priority", visible:false},
            {field:"class_field", label:"class1", visible:false},
            {field:"docflag", label:"DocFlag", visible:false},
            {field:"taskcategory", label:"taskcategory", visible:false},
            {field:"inc_id", label:"inc_id", visible:false},
        ];
        //SWDataTable控件不支持的功能，可以使用原生jquery datatable的屬性設置
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
                { "responsivePriority": -1, "className": "all","targets": 0 },
                { "responsivePriority": 5, "className": "min-tablet-p","targets": 1 },
                { "responsivePriority": -1, "className": "all", "targets": 2 },
                { "responsivePriority": 2, "className": "desktop", "targets": 3 },
                { "responsivePriority": 3, "className": "min-tablet-p", "targets": 4 },
                { "responsivePriority": 4, "className": "min-tablet-p", "targets": 5 },
                { "responsivePriority": 5, "className": "min-tablet-p", "targets": 6 },
                { "responsivePriority": -1, "className": "all", "targets": 7 },
                { "responsivePriority": 5, "className": "desktop", "targets": 8 },
                { "responsivePriority": 5, "className": "min-tablet-p", "targets": 6 },
                { "responsivePriority": -1, "className": "all", "targets": 7 },
                { "responsivePriority": 5, "className": "desktop", "targets": 8 },
                { "responsivePriority": 5, "className": "min-tablet-p", "targets": 6 },
                { "responsivePriority": -1, "className": "all", "targets": 7 },
            ],
            deferLoading: 0,
        });
        
        table.custom_params_fun = function () {
            if (relationID != undefined) {
                var array = relationID.split(";")
                if(array.length<=0){
                    return {attach_query: JSON.stringify({"condition":"AND","rules":[
                        {"id":"pid","field":"pid","type":"string","input":"text","operator":"equal","value":null},
                        ],"not":false,"valid":true})};
                }
                var filter = {"condition":"AND","rules":[
                    {"id":"taskno","field":"taskno","type":"string","input":"text","operator":"in","value":array},
                    ],"not":false,"valid":true};
                return {attach_query: JSON.stringify(filter)};
            }
            else
                return {};
    } 
    
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
        const relationTable = table.init('/PMIS/task/t_list');

    //-----------結束關聯任務表格--------------------------------
    //文件列表下載按鈕點擊事件
    $('#uploadFileDetails_task').on('click','button[name="pullfile"]',function(){
        var inc_id = $(this).attr('inc_id')
        var imageurl = ''
        //根據inc_id獲取對應的文件請求路徑
        for(var i=0;i<file_array.length;i++){
            if(file_array[i]['inc_id']==inc_id)
                imageurl = file_array[i]['fileurl']
        }
        if(imageurl!='')
            window.location.replace(imageurl+'&state=download')
    });
    
    //文件列表刪除按鈕點擊事件
    $('#uploadFileDetails_task').on('click','button[name="deletefile"]',function(){
        if (confirm("你確定要刪除該文件?")) {
            var inc_id = $(this).attr('inc_id')
            //用於標記文件信息若刪除成功則將此條文件信息移出並重繪列表
            for(var i=0;i<file_array.length;i++){
                if(file_array[i]['inc_id']==inc_id){
                    file_list = file_array[i]
                    file_list['indexno'] = i
                }
            }
            $.ajax({
                type:'POST',
                url:'/looper/metting/DocumentDeleteView/{0}'.format(inc_id),
                datatype:"json",
                beforeSend: function (request) {
                    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                },
                success:function(response){
                    if(response.status){
                        file_array.splice(file_list['indexno'], 1)
                        if(file_array.length==0)
                            $('#uploadFileDetails_task').modal('hide');
                        show_filearray()
                    }
                    file_list = {}
                },
                error:function(){
                    alert('程序異常')
                },
            })
            }
    });
    
    function objectToFormData(obj){
        let fd = new FormData();
        for (let o in obj) {
            if(obj[o]){
                fd.append(o, obj[o]);
            }          
        }
        return fd;
    }

    function Set_escore(model){
        var modelid =model
        var tasktype = $(model+' select[name="tasktype"]').val()
        var subtasktype = $(model+' select[name="subtasktype"]').val()
        var diff = $(model+' select[name="diff"]').val()
        tasktype = tasktype==null?'':tasktype
        subtasktype = subtasktype==null?'':subtasktype
        diff = diff==null?'':diff
        if(tasktype!='' && subtasktype!='' && diff!=''){
            $.ajax({
                type:"GET",
                url:"/PMIS/tasktype/subtasktype_score?tasktype={0}&subtasktype={1}".format(tasktype,subtasktype),
                datatype:"json",
                beforeSend: function (request) {
                    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                },
                success:function(response){
                    if(response.status){
                        if(response.data.length<=0){
                            alert('未找到對應任務分類數據')
                            return
                        }
                        var resdata = response.data[0]
                        switch(diff){
                            case '1':
                                $(modelid+' input[name="lookupscore"]').val(resdata.difficulties1)
                                break;
                            case '2':
                                $(modelid+' input[name="lookupscore"]').val(resdata.difficulties2)
                                break;
                            case '3':
                                $(modelid+' input[name="lookupscore"]').val(resdata.difficulties3)
                                break;
                        }
                    }else{
                        alert('獲取預計績效分失敗！')
                    }
                },
                error:function(){
                    alert('程序異常')
                },
            })
        }
    }

    //----------開始發送消息的邏輯-----------------------------
    var notifForm = new SWBaseForm("#setNotifDialog")
    notifForm.pk_in_url = false;  //這種情況必須設置pk_in_url = false
    notifForm.create_url = "/looper/notif/create";  //新增動作url 
    notifForm.update_url = "/looper/notif/update/[[pk]]";  //更新動作url
    notifForm.on_after_save = function(data) {
        $("#setNotifDialog").modal("hide");  //保存成功後，隱藏該modal,   edtiModal為第1步中id="edtiModal"
    }      
    notifForm.on_init_format = function(data)   {
        data['istr024'] = data.tr024 != null && data.tr024 != undefined && data.tr024 > 0;
        if (data['istr024']) {
            data['tr024h'] = data.tr024/60;
            data['tr024m'] = data.tr024%60;
        }
        if (data.tr004 != null && data.tr004 != undefined) {
            var date_data = Date.parse(data.tr004.replace(/z$/i, "").replace(/[.][0-9]+$/, ""));
            data.tr004 = date_data.toString("HH:mm");
        }
        if (data.tr005 != null && data.tr005 != undefined) {
            var date_data = Date.parse(data.tr005.replace(/z$/i, "").replace(/[.][0-9]+$/, ""));
            data.tr005 = date_data.toString("HH:mm");
        }
        if (data.tr021 != null && data.tr021 != undefined) {
            var date_data = Date.parse(data.tr021.replace(/z$/i, "").replace(/[.][0-9]+$/, ""));
            data.tr021 = date_data.toString("yyyy-MM-dd");
        }
        if (data.tr022 != null && data.tr022 != undefined) {
            var date_data = Date.parse(data.tr022.replace(/z$/i, "").replace(/[.][0-9]+$/, ""));
            data.tr022 = date_data.toString("yyyy-MM-dd");
        }
    }
    notifForm.on_after_init = function(data) {
        $("#remindRepeat").prop("checked", data['istr024']);
        $("#remindRepeat").trigger("change");
        $(`#setNotifDialog input[name='tr028'],#setNotifDialog input[name='tr030']`).each((i, item)=>{
            $(item).val($(item).attr("init_value"));
            if ($(item).attr("init_value") == data[$(item).attr("name")])
                $(item).prop("checked", true);
        });
    }
    notifForm.on_save_format = function(data) {
        if (data.tr004 != null && data.tr004 != undefined) {
            data.tr004 = Date.today().toString('yyyy-MM-dd') + 'T' + data.tr004;
        }
        if (data.tr005 != null && data.tr005 != undefined) {
            data.tr005 = Date.today().toString('yyyy-MM-dd') + 'T' + data.tr005;
        }
        data.istr024 = $("#setNotifDialog input[name='istr024'").prop("checked");
    }

    $("#add-task-module .send-instant-notif, #add-task .send-instant-notif").on("click", function(e){
        e.preventDefault();
        var taskNo =  $("#add-task .cust_taskId p").text();
        if (SWApp.os.isAndroid || SWApp.os.isPhone)
            taskNo = $("#add-task-module .cust_taskId p").text();
        var url = `/PMIS/task/send_instant_notif?taskNo=${taskNo}`
        $.get(url, function(result){
            if (result.status) {
                alert(gettext("Send notification success!"));
            }else {
                if (result.msg !== "" && result.msg != undefined)
                    alert(result.msg);
                else
                    alert(gettext("Send notification fail!"));
            }
        });
    });
    $("#add-task-module .setting-notif, #add-task .setting-notif").on("click", function(e){
        e.preventDefault();
        var taskNo =  $("#add-task .cust_taskId p").text();
        $.get("/looper/notif/get_pmstr_with_task", {taskno:taskNo}).then((result)=>{
            if (result.status) {
                if (result.data != "")
                    notifForm.set_pk(result.data);
                else
                    notifForm.set_pk(undefined);
                notifForm.init_data({taskno:taskNo});        
            }
        })
        $('#setNotifDialog').modal('show');   
        
          
    });
    
    $('#setNotifDialog').on('shown.bs.modal', function() {
        $("#add-task-module.show, #add-task.show").addClass('blur'); 
    }).on('hidden.bs.modal', function() {
        $("#add-task-module.show, #add-task.show").removeClass('blur'); 
    });
    
    function generateRemindRound() {
        for (var i = 0; i < 24; i++) {
            $("#remindRoundHour").append(`<option value="${i}">${i} ${gettext("hour")}</option>`);
        }
        for (var i = 0; i < 60; i++) {
            $("#remindRoundMinute").append(`<option value="${i}">${i} ${gettext("minute")}</option>`);
        }
    }
    $("#remindRepeat").on("change", function(){
        if ($(this).is(":checked"))
            $("#remindRound").removeClass("d-none");
        else
            $("#remindRound").addClass("d-none");
    })
    $(`#setNotifDialog input[name='tr028']`).on("change", function(){
        if (parseInt($(this).val()) > 1) {
            $("#setNotifDialog input[name='tr021']").val("");
        }
        if(parseInt($(this).val()) == 1)
            $("#setNotifDialog select[name='tr029']").val("0");
        
    }) 
    $(`#setNotifDialog input[name='tr030']`).on("change", function(){
        if (parseInt($(this).val()) > 1) {
            $("#setNotifDialog input[name='tr022']").val("")
        }
    })
    generateRemindRound();
    //----------結束發送消息的邏輯-----------------------------

    //----------設置審批信息的邏輯-----------------------------
    var approver_cmpt = new SWCombobox("approver", gettext('Approver'), window.CommonData.PartUserNames)
    approver_cmpt.input_dom.attr("data-live-search", "true");
    $("#approveModal .approver-group").append(approver_cmpt.dom)
    $("#add-task-module .approve_required, #add-task .approve_required").on("click", function(e){
        var inc_id =  $("#add-task input[name='inc_id']").val();
        var task = $("#add-task textarea[name='task']").val();
        if (SWApp.os.isAndroid || SWApp.os.isPhone) {
            inc_id = $("#add-task-module input[name=['inc_id']").val();
            task = $("#add-task-module textarea[name=['task']").val();
        }
        $("#approveModal .approver-group select[name='approver']").val("");
        $("#approveModal .approver-group select[name='approver']").selectpicker('refresh');
        $("#approveContent").val(task)
        $("#approveModal input[name='task_inc_id']").val(inc_id);
        $("#approveModal").modal("show");
    });

    $("#approveModal .submit_approve_btn").on("click", function(e){
        var task_inc_id = $("#approveModal input[name='task_inc_id']").val();
        var approver =  $("#approveModal .approver-group select[name='approver']").val();
        var approveContent = $("#approveContent").val();
        if (task_inc_id == "") {
            alert(gettext("This task does not exist!"))
            return;
        }else if (approver == "") {
            alert(gettext("Please input approver!"))
            return;
        }else if (approveContent == "") {
            alert(gettext("Please input content!"))
            return;
        }
        var data = {task_inc_id:task_inc_id, approver:approver, approveContent:approveContent};

        var url = "/PMIS/task/approve_request";
        $.ajax({
            type: "POST",
            url: url,
            data: data,
            datatype: "json",
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            success: function (result) {
                if (result.status) {
                    alert(gettext("Approval request successful."));
                }else {
                    alert(gettext("Approval request fail."));
                }
            }
        });
    });
     
    //----------結束審核信息的邏輯-----------------------------

    //將日期秒歸零
    function FormatSecond(originalTimestamp){
        var date = new Date(originalTimestamp);  
        // 设置秒和毫秒为0  
        date.setSeconds(0);  
        date.setMilliseconds(0);  
        // 将更新后的Date对象转换回字符串 
        return date.toString('yyyy-MM-dd hh:mm:ss')
    }
    function display_task() {
        var task_pk = getParamFromUrl("dp_task_pk");
        if (task_pk != undefined) {
            init_task(task_pk)
        }
    }    
    display_task();
})