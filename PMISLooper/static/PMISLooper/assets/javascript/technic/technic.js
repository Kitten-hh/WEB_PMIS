"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

// Class Template
// =============================================================
var stepsDemo = /*#__PURE__*/function () {
    function stepsDemo() {
        _classCallCheck(this, stepsDemo);

        this.init();
    }

    _createClass(stepsDemo, [{
        key: "init",
        value: function init() {
            // event handlers
            this.handleValidations();
            this.handleSteps();
        }
    }, {
        key: "validateBy",
        value: function validateBy(trigger) {
            var isNextBtn = $(trigger).hasClass('btn');
            var from = isNextBtn ? null : $(trigger).parents('ul').children('.active').index();
            var to = isNextBtn ? null : $(trigger).parent().index();
            var $trigger = isNextBtn ? $(trigger) : $(trigger).parents('ul').children('.active');
            var group = $trigger.data().validate;
            var groupId = $trigger.parents('.content').attr('id');
            var $groupStep = isNextBtn ? $("[data-target=\"#".concat(groupId, "\"]")) : $trigger;
            $('#stepper-form').parsley().on('form:validate', function (formInstance) {
                var isValid = formInstance.isValid({
                    group: group
                }); // normalize states
                var check_promise = new Promise((resolve, reject) => {
                    if (isValid) {
                        if (window.edit_spec_form != undefined) {
                            var form_dom = $("#spec_from_div form");
                            var form_data = form_dom.data("form_data");
                            if (form_data['pk'] == undefined) {
                                window.edit_spec_form.save_data(trigger).then((flag) => {
                                    resolve(flag);
                                });
                            } else
                                resolve(true);
                        } else
                            resolve(true);
                    } else {
                        resolve(false);
                    }
                });
                $groupStep.removeClass('success error'); // give step item a validate state
                check_promise.then((flag) => {
                    if (flag) {
                        $groupStep.addClass('success'); // go to next step or submit
                        if ($trigger.hasClass('submit')) {
                            $('#submitfeedback').toast('show');
                            console.log($('#stepper-form').serializeArray());
                        } else if (isNextBtn) {
                            stepperDemo.next();
                        } else {
                            stepperDemo.to(to + 1);
                        }
                    } else {
                        $groupStep.addClass('error');
                    }
                });
            }).validate({
                group: group
            }); // kill listener

            $('#stepper-form').parsley().off('form:validate');
        }
    }, {
        key: "handleValidations",
        value: function handleValidations() {
            var self = this; // validate on next buttons

            $('.next, .step-trigger').on('click', function () {
                self.validateBy(this);
            }); // prev buttons

            $('.prev').on('click', function () {
                var $trigger = $(this);
                var groupId = $trigger.parents('.content').attr('id');
                var $groupStep = $("[data-target=\"#".concat(groupId, "\"]")); // normalize states

                $groupStep.removeClass('success error');
                $groupStep.prev().removeClass('success error');
                stepperDemo.previous();
            }); // save creadit card

            $('#savecc').on('click', function () {
                $('#stepper-form').parsley().whenValidate({
                    group: 'creditcard'
                });
            }); // submit button

            $('.submit').on('click', function () {
                self.validateBy(this);
                return false;
            });
        }
    }, {
        key: "handleSteps",
        value: function handleSteps() {
            var selector = document.querySelector('#stepper');
            window.stepperDemo = new Stepper(selector, {
                linear: false,
                unbind_link_click: true
            });
        }
    }]);

    return stepsDemo;
}();

var indexno = 1;  //用於確定Tenical的name
var Goal = 2;    //用於確定Goal的name
var thisGoal = ''; //用於確定MindMapid下標
var TechnicInputid = ''; //用於確定選中的Technic
var agoTechnicidlabel = '';
var agoTechnicid = '';
var agoMindmapidlabel = '';
var agoMindmapid = '';
$(function () {
    if (SWApp.os.isAndroid || SWApp.os.isPhone) {
        $("#pc_technic").attr("id", "mobile_technic");
    }
    else {
        $("#mobile_technic").attr("id", "pc_technic");
    }

    $("body").addClass("technic_daily_planner");
    //添加控件
    var per_row1 = new SWRow();
    var task_id = new SWText("taskno", "text", gettext("Task ID") + " :", "");
    per_row1.addComponent(task_id);
    var contact = new SWText("contact", "text", gettext("Contact") + " :", "");
    per_row1.addComponent(contact);
    var date = new SWDate("startdate", "date", gettext("Date") + " :", "");
    per_row1.addComponent(date);

    var date2 = new SWText("inputdate", "hidden");
    var date3 = new SWText("itemno", "hidden");
    var date4 = new SWText("modi_date", "hidden");
    $("#stepper_from_div form").eq(0).prepend(date2.dom);
    $("#stepper_from_div form").eq(0).prepend(date3.dom);
    $("#stepper_from_div form").eq(0).prepend(date4.dom);



    var task_row2 = new SWRow();
    var task_desc = new SWTextarea("taskdescription", gettext("Task Description") + " :", 3, "");
    task_row2.addComponent(task_desc);
    var goal_achieve = new SWTextarea("goalachieve", gettext("Goal Achieve") + " :", 3, "設計WEB PMIS中Technic Daily Planner錄入頁面");
    task_row2.addComponent(goal_achieve);

    var task_row3 = new SWRow();
    var p_used = new SWText("platformused", "text", gettext("Platform Used") + " :", "__vscode0");
    task_row3.addComponent(p_used);
    var system = new SWText("system", "text", gettext("System") + " :", "WEB PMIS");  //？？？
    task_row3.addComponent(system);
    var task_type = new SWText("tasktype", "text", gettext("Task type") + " :", "");
    task_row3.addComponent(task_type);
    var score = new SWText("score", "text", gettext("Score") + " :", "");
    task_row3.addComponent(score);

    var task_row4 = new SWRow();
    var frame_spec = new SWText("framespecification", "text", gettext("Frame Specification") + " :");
    task_row4.addComponent(frame_spec);
    var design_doc = new SWText("designdoc", "text", gettext("Design Doc") + " :");
    task_row4.addComponent(design_doc);

    var tech_row = new SWRow();
    //var solution_type = new SWCombobox("solution[0].mindmapid", "Solution Type","/looper/DailyPlanner/getTecMindMap", "","inc_id","sdesc");
    //$("#mindmapinput1" ).prepend(solution_type.dom);
    //var dailyplannerstatus_type = new SWText("dailyplannerstatus", "hidden", "DailyPlanner Status：", "");
    //$("#mindmapinput1" ).prepend(dailyplannerstatus_type.dom);
    //var statusdesc_type = new SWText("statusdesc", "hidden", "Etatus Desc：", "");
    //$("#mindmapinput1" ).prepend(statusdesc_type.dom);

    var solution_type = new SWText("solution[0].mindmapid", "hidden", gettext("Solution Type") + " :", "");
    $("#mindmapinput1").prepend(solution_type.dom);
    var solution_stitemno = new SWText("solution[0].stitemno", "hidden", "stitemno：", "");
    $("#mindmapinput1").prepend(solution_stitemno.dom);
    var Technic_type = new SWText("solution[0].technicid", "hidden", gettext("Technical") + " :", "");
    $("#mindmapinput1").prepend(Technic_type.dom);
    var mindmaplabel = new SWText("solution[0].mindmaplabel", "hidden", "mindmaplabel：", "");
    $("#mindmapinput1").prepend(mindmaplabel.dom);
    $("input[name='solution[0].mindmapid']").addClass("mindmapidinput");
    $("input[name='solution[0].mindmaplabel']").addClass("mindmaplabelinput");

    var solution_type = new SWText("solution[0].mindmapidlabel", "text", gettext("Solution Type") + " :", "");
    tech_row.addComponent(solution_type);
    var ftime = new SWText("solution[0].ftime", "text", gettext("FTime") + " :");
    tech_row.addComponent(ftime);
    var etime = new SWText("solution[0].etime", "text", gettext("ETime") + " :");
    tech_row.addComponent(etime);    //？？？

    var tech_row1 = new SWRow();
    var technical = new SWText("solution[0].technicidlabel", "text", gettext("Technical") + " :", "");  //？？？
    tech_row1.addComponent(technical);
    var satisfactory = new SWCheckbox("solution[0].satisfactory", gettext("Satisfactory"));
    tech_row1.addComponent(satisfactory);
    var refinement = new SWCheckbox("solution[0].refinement", gettext("Refinement"));
    tech_row1.addComponent(refinement);
    var ambiguous = new SWCheckbox("solution[0].ambiguous", gettext("Ambiguous"));
    tech_row1.addComponent(ambiguous);   ///????


    var tech_row2 = new SWRow();
    var remark = new SWTextarea("solution[0].remark", gettext("Remark") + " :", 3);
    tech_row2.addComponent(remark);




    var sta_row1 = new SWRow();
    var diagram = new SWText("flowchart", "text", gettext("Flowchart/Diagram") + " :");
    sta_row1.addComponent(diagram);
    var questions = new SWText("questions", "text", gettext("Questions") + " :");
    sta_row1.addComponent(questions);

    var status = new SWText("status", "text", gettext("Status") + " :", "");
    sta_row1.addComponent(status);
    var ecdate = new SWDate("enddate", "date", gettext("Estimated Completion Day") + " :", "");
    sta_row1.addComponent(ecdate);

    var sta_row2 = new SWRow();
    var new_tech = new SWTextarea("newtechnicalneed", gettext("New Technical Need/Found") + " :", 3);
    sta_row2.addComponent(new_tech);
    var comment = new SWTextarea("comment", gettext("Comment") + " :", 3);
    sta_row2.addComponent(comment);




    $(".per-section").append(per_row1.dom);
    $(".task-section").append(task_row2.dom);
    $(".task-section").append(task_row3.dom);
    $(".task-section").append(task_row4.dom);
    $(".goal1").append(tech_row.dom);
    $(".goal1").append(tech_row1.dom);
    $(".goal1").append(tech_row2.dom);

    $(".sta-section").append(sta_row1.dom);
    $(".sta-section").append(sta_row2.dom);
    // 调整控件
    $("#mobile_technic .div-1").addClass("col-12");
    $("#mobile_technic .div-2").addClass("col-12");
    $("#mobile_technic .div-3").addClass("col-12");
    $("#mobile_technic .div-4").addClass("col-12");
    $("input[name='solution[0].mindmapidlabel']").addClass("mindmapid");
    $("input[name='solution[0].technicidlabel']").addClass("technicid");
    // 添加tooltip
    $('body').tooltip({
        selector: '[data-toggle="tooltip"]'
    });
    $(".add_goal").attr({ "data-toggle": "tooltip", "data-placement": "right", "title": "", "data-original-title": "添加goal" });
    // label(不带*标记的)
    $("label:not(.custom-checkbox>label)").prepend(`<abbr class="require" title="Required">*</abbr>`);
    $(".task-section").find(".SWText .caption").eq(1).addClass("no_attr");
    $(".task-section").find(".SWText .caption").eq(3).addClass("no_attr");
    $(".task-section").find(".SWText .caption").eq(4).addClass("no_attr");
    $(".task-section").find(".SWText .caption").eq(5).addClass("no_attr");

    $(".sta-section").find(".SWText .caption").eq(0).addClass("no_attr");
    $(".sta-section").find(".SWText .caption").eq(1).addClass("no_attr");
    $(".sta-section").find(".SWTextarea .caption").eq(0).addClass("no_attr");
    $(".sta-section").find(".SWTextarea .caption").eq(1).addClass("no_attr");
    $(".no_attr").find(".require").remove();


    // goal1 增加technic
    $("#addGoal").click(function () {
        var thehtml = '<div id="mindmapinput' + Goal + '"></div>' +
            '<div class="d-flex align-items-center titlegoal' + Goal + '"><span class="ml-1" style="color: #9d5d8e;">'+ gettext("For Goal") + '' + Goal + '</span>' +
            '<button type="button" onclick="toRemoveGoal(' + Goal + ')" class="btn btn-subtle-danger" style="margin-left: 2%">' +
            '<i class="fas fa-minus"></i></button>' +
            '<button type="button" onclick="toDeleteTechnic(' + Goal + ')" class="btn btn-subtle-danger ml-auto">' +
            '<i class="fas fa-minus"></i></button>' +
            '<button type="button" onclick="toAddTechnic(' + Goal + ')" class="btn btn-subtle-danger " style="margin-left: 2%"">' +
            '<i class="fas fa-plus"></i></button></div><div class="goal' + Goal + '"></div><div class="goal' + Goal + '_tech"></div>'
        $("#goaldiv").append(thehtml)
        var tech2_row = new SWRow();
        var solution_type = new SWText("solution[" + indexno + "].mindmapidlabel", "text", gettext("Solution Type") + " :", "");
        tech2_row.addComponent(solution_type);
        var ftime = new SWText("solution[" + indexno + "].ftime", "text", gettext("FTime") + " :");
        tech2_row.addComponent(ftime);
        var etime = new SWText("solution[" + indexno + "].etime", "text", gettext("ETime") + " :");
        tech2_row.addComponent(etime);   //？？？

        var tech2_row1 = new SWRow();
        var technical = new SWText("solution[" + indexno + "].technicidlabel", "text", gettext("Technical") + " :", "");
        tech2_row1.addComponent(technical);     
        var satisfactory = new SWCheckbox("solution[" + indexno + "].satisfactory", gettext("Satisfactory"));
        tech2_row1.addComponent(satisfactory);
        var refinement = new SWCheckbox("solution[" + indexno + "].refinement", gettext("Refinement"));
        tech2_row1.addComponent(refinement);
        var ambiguous = new SWCheckbox("solution[" + indexno + "].ambiguous", gettext("Ambiguous"));
        tech2_row1.addComponent(ambiguous); //？？？
        var tis = new SWCombobox("solution["+ indexno + "].tis", "TIS", ["R","Y"])
        tis.dom.addClass("technical-tis");
        tis.setHorizontalDisplay()
        tech2_row1.dom.find(".col_right").prepend(tis.dom);           
    

        var tech2_row2 = new SWRow();
        var remark = new SWTextarea("solution[" + indexno + "].remark", gettext("Remark") + " :", 3);  //？？？
        tech2_row2.addComponent(remark);

        var solution_type = new SWText("solution[" + indexno + "].mindmapid", "hidden", "Solution Type", "");
        $("#mindmapinput" + Goal).prepend(solution_type.dom);
        var Technic_type = new SWText("solution[" + indexno + "].technicid", "hidden", "Technical：：", "");
        $("#mindmapinput" + Goal).prepend(Technic_type.dom);
        var solution_stitemno = new SWText("solution[" + indexno + "].stitemno", "hidden", "Solution Type：", "");
        $("#mindmapinput" + Goal).prepend(solution_stitemno.dom);
        var mindmaplabel = new SWText("solution[" + indexno + "].mindmaplabel", "hidden", "Mindmap Label：", "");
        $("#mindmapinput" + Goal).prepend(mindmaplabel.dom);

        $(".goal" + Goal).append(tech2_row.dom);
        $(".goal" + Goal).append(tech2_row1.dom);
        $(".goal" + Goal).append(tech2_row2.dom);
        
        $("input[name='solution[" + indexno + "].mindmaplabel']").addClass("mindmaplabelinput");
        $("input[name='solution[" + indexno + "].mindmapid']").addClass("mindmapidinput");
        $("input[name='solution[" + indexno + "].mindmapidlabel']").addClass("mindmapid");
        $("input[name='solution[" + indexno + "].technicidlabel']").addClass("technicid");
        Goal = Goal + 1
        indexno = indexno + 1
    })


    $("#removeGoal").click(function () {
        $("#mindmapinput" + Goal).remove()
        $(".titlegoal" + Goal).remove()
        $(".goal" + Goal).remove()
        $(".goal" + Goal + "_tech").remove()
        Goal = Goal - 1
    })
    // 添加说明
    var question_msg =  gettext("Question status, or progress on the technical");
    $(".sta-section .div-1 .SWTextarea .caption").append(`<br><small class="text-muted">(` + gettext("Adding technical that will be helpful to") + `)</small>`);
    $(".sta-section .div-2 .SWTextarea .caption").append(`<br><small class="text-muted">(` + question_msg + `)</small>`);
    var initSolutionType = function() {
        var tech_row = new SWRow();        
        var solution_type = new SWText("solution[0].mindmapid", "hidden", gettext("Solution Type") + " :", "");
        $("#mindmapinput1").prepend(solution_type.dom);
        var solution_stitemno = new SWText("solution[0].stitemno", "hidden", "stitemno：", "");
        $("#mindmapinput1").prepend(solution_stitemno.dom);
        var Technic_type = new SWText("solution[0].technicid", "hidden", gettext("Technical") + " :", "");
        $("#mindmapinput1").prepend(Technic_type.dom);
        var mindmaplabel = new SWText("solution[0].mindmaplabel", "hidden", "mindmaplabel：", "");
        $("#mindmapinput1").prepend(mindmaplabel.dom);
        $("input[name='solution[0].mindmapid']").addClass("mindmapidinput");
        $("input[name='solution[0].mindmaplabel']").addClass("mindmaplabelinput");
    
        var solution_type = new SWText("solution[0].mindmapidlabel", "text", gettext("Solution Type") + " :", "");
        tech_row.addComponent(solution_type);
        var ftime = new SWText("solution[0].ftime", "text", gettext("FTime") + " :");
        tech_row.addComponent(ftime);
        var etime = new SWText("solution[0].etime", "text", gettext("ETime") + " :");
        tech_row.addComponent(etime);    //？？？
    
        var tech_row1 = new SWRow();
        var technical = new SWText("solution[0].technicidlabel", "text", gettext("Technical") + " :", "");  //？？？
        tech_row1.addComponent(technical);
        var satisfactory = new SWCheckbox("solution[0].satisfactory", gettext("Satisfactory"));
        tech_row1.addComponent(satisfactory);
        var refinement = new SWCheckbox("solution[0].refinement", gettext("Refinement"));
        tech_row1.addComponent(refinement);
        var ambiguous = new SWCheckbox("solution[0].ambiguous", gettext("Ambiguous"));
        tech_row1.addComponent(ambiguous);   ///????
        var tis = new SWCombobox("solution[0].tis", "TIS", ["R","Y"])
        tis.setHorizontalDisplay();
        tis.dom.addClass("technical-tis");
        tech_row1.dom.find(".col_right").prepend(tis.dom);        
    
    
        var tech_row2 = new SWRow();
        var remark = new SWTextarea("solution[0].remark", gettext("Remark") + " :", 3);
        tech_row2.addComponent(remark);  
        $(".goal1").append(tech_row.dom);
        $(".goal1").append(tech_row1.dom);
        $(".goal1").append(tech_row2.dom)        
        $("input[name='solution[0].mindmapidlabel']").addClass("mindmapid");
        $("input[name='solution[0].technicidlabel']").addClass("technicid");    
    }
    var form1 = new SWBaseForm("#stepper_from_div");
    form1.create_url = "/looper/DailyPlanner/create";
    form1.update_url = "/looper/DailyPlanner/update?pk=[[pk]]";
    form1.init_data({});
    //form1.redirect_url = "/looper/technic/selectdailyplanner";
    form1.on_init_format = form1_format
    function form1_format (data) {
        data.inputdate = Date.parseExact(data.inputdate, 'yyyyMMdd').toString("yyyy-MM-dd");
        data.startdate = new Date(data.startdate).toString('yyyy-MM-dd');
        if(parameterinputdate != ''){
            data.inputdate = new Date(parameterinputdate).toString('yyyy-MM-dd');
            data.startdate = new Date(parameterinputdate).toString('yyyy-MM-dd');
        }
        data.enddate = new Date(data.enddate).toString('yyyy-MM-dd');
        //獲取對應的SolutionType
        $.ajax({
            url: "/looper/DailyPlanner/displaysolutionType",
            type: "GET",
            dataType: 'json',
            data: { "contact": data.contact, "inputdate": Date.parse(data.inputdate).toString("yyyyMMdd"), "itemno": data.itemno },
            cache: false,
            success: function (json) {
                if (json.status) {
                    var jsondata = json.data
                    var mindmapid = ''
                    var solutionNo = 0;
                    indexno = 1;
                    Goal = 2;
                    $("#mindmapinput1,#ContainerGoal1 .goal1, #ContainerGoal1 .goal1_tech, #goaldiv").empty();
                    initSolutionType();
                    for (var i = 0; i < jsondata.length; i++) {
                        if (mindmapid == jsondata[i].mindmapsdesc && mindmapid != "") {
                            toAddTechnic(Goal - 1)
                        }
                        if (mindmapid != jsondata[i].mindmapsdesc && mindmapid != "") {
                            $("#addGoal").click()
                        }
                        $("input[name='solution[" + solutionNo + "].technicid']").val(jsondata[i].inc_id);
                        $("input[name='solution[" + solutionNo + "].technicidlabel']").val(jsondata[i].Technicalcode);
                        $("input[name='solution[" + solutionNo + "].mindmapid']").val(jsondata[i].mindmapid);
                        $("input[name='solution[" + solutionNo + "].mindmapidlabel']").val(jsondata[i].mindmapsdesc);
                        $("input[name='solution[" + solutionNo + "].mindmaplabel']").val(jsondata[i].mindmapsdesc);
                        $("input[name='solution[" + solutionNo + "].ftime']").val(jsondata[i].ftime);
                        $("input[name='solution[" + solutionNo + "].etime']").val(jsondata[i].etime);
                        $("input[name='solution[" + solutionNo + "].stitemno']").val(jsondata[i].stitemno);
                        $("textarea[name='solution[" + solutionNo + "].remark']").val(jsondata[i].remark);
                        switch(jsondata[i].condition){
                            case 'S':
                                $("input[name='solution[" + solutionNo + "].satisfactory']").attr('checked','true')
                                break;
                            case 'R':
                                $("input[name='solution[" + solutionNo + "].refinement']").attr('checked','true')
                                break;
                            case 'A':
                                $("input[name='solution[" + solutionNo + "].ambiguous']").attr('checked','true')
                                break;
                        }
                        $("select[name='solution[" + solutionNo + "].tis']").val(jsondata[i].tis);
                        $("select[name='solution[" + solutionNo + "].tis']").selectpicker('refresh');
                        solutionNo = solutionNo + 1
                        mindmapid = jsondata[i].mindmapsdesc
                    }

                }
            }
        })


    };
    form1.on_save_format = function (data) {
        data.inputdate = Date.parse(data.inputdate).toString("yyyyMMdd");
    };
    form1.on_after_save = function (data) {
        parent.selectDetailPlanner()
        form1_format(data)
    };

    //技術文檔下一步按鈕點擊事件
    $("#test-l-3 .d-flex .next").on("click", function () { mindmapidChange() })
    $("#stepper_form_submit").on("click", function () { mindmapidChange() })
    
    //修改隱藏的mindmapid輸入框值
    function mindmapidChange() {
        var mindmapid = 0
        for (var i = 1; i < Goal; i++) {
            var mindmapid = ''
            var mindmaplabel = ''
            var mindmapinput = $("#mindmapinput" + i + " .mindmapidinput")
            for (var n = 0; n < mindmapinput.length; n++) {
                if (mindmapinput[n].value != '') {
                    mindmapid = mindmapinput[n].value;
                    break
                }
            }
            $("#mindmapinput" + i + " .mindmapidinput").val(mindmapid)

            
            var mindmaplabelinput = $(".goal" + i + " .mindmapid")
            for (var n = 0; n < mindmaplabelinput.length; n++) {
                if (mindmaplabelinput[n].value != '') {
                    mindmaplabel = mindmaplabelinput[n].value;
                    break
                }
            }
            $("#mindmapinput" + i + " .mindmaplabelinput").val(mindmaplabel)
        }
        //print(mindmapid)
    }
    //taskType改變獲取對應的TaskType翻譯
    $("input[name='taskno']").on("change", function () {
        var taskno = $(this).val();
        var inputdate = $('input[name="inputdate"]').val();
        $.ajax({
            url: "/looper/technic/get_task?taskno=" + taskno+"&inputdate="+inputdate,
            type: 'GET',
            dataType: 'json',
            cache: false,
            success: function (json) {
                if (json.status) {
                    var data = json.data
                    $("input[name='contact']").val(data[0].contact);
                    $("textarea[name='taskdescription']").val(data[0].task);
                    if (data[0].tasktype != null){$("input[name='tasktype']").val(data[0].tasktype + '-->' + data[0].subtasktype);}
                    $("input[name='score']").val(data[0].score);
                    $("input[name='status']").val(data[0].progress);
                    $("input[name='itemno']").val(data[1]);
                }
            }
        })
    });

    //SolutionType表格創建
    var table = new SWDataTable("#db_wapper", "Mindmapidtable"); //創建SWDataTable對象
    table.pageLength = 20; //設置每頁顯示的數量為20
    table.paging = true; //設置分頁顯示
    table.searching = true; //設置不顯示查詢框

    table.orderBy = [['inc_id', 'asc']]; //設置按taskno 升序排序
    //設置顯示字段
    table.columns = [
        { field: "inc_id", label: "INC_ID", visible: false },
        { field: "parentid", label: gettext("ParentId") },
        { field: "sdesc", label: gettext("Description") },
    ];
    //SWDataTable控件不支持的功能，可以使用原生jquery datatable的屬性設置
    table.setOptions({ 
        responsive: true, //是否支持手機展開和隱藏列
        //隱藏的規則，responsivePriority值越大越先隱藏，width設置列寬度
        columnDefs: [
            { "responsivePriority": 1, "targets": 0 },
            { "responsivePriority": 1, "width": "45%", "targets": 1 },
            { "responsivePriority": 2, "targets": 2 },
        ]
    });
    table.init('/looper/DailyPlanner/TecmindmapDatatable');

    var theinc_id = ''
    $('#Mindmapidtable tbody').on('click', 'tr', function () {
        var table = $('#Mindmapidtable').DataTable();
        $("input[name='solution[" + thisGoal + "].mindmapidlabel']").val(table.row(this).data()['sdesc']);
        $("input[name='solution[" + thisGoal + "].mindmapid']").val(table.row(this).data()['inc_id']);
        theinc_id = table.row(this).data()['inc_id'];
    });

    //MindMap選擇窗口取消按鈕點擊事件
    
    $("#MindmapEnterbtn").on("click", function () {
        $('#SearchNewModal').modal('hide');
        var json_data = mindmap.selector_node();
        console.log(json_data);
        var childs_node = json_data['childs_node']
        var myself_node = json_data['myself_node']
        var parent_node = json_data['parent_node']
        var mindmapid = json_data['inc_id']
        var indexnum = 0
        for (var i = 0; i < childs_node.length; i++){
            var parameter = childs_node[i]['url'].slice(-13)
            $.ajax({
                type: "GET",
                url: "/looper/DailyPlanner/getTechnicid",
                dataType: "json",
                data: {'mb023':parameter},
                async: false,
                success: function (result) {
                    if (result.status) {
                        var jsondata = result.data
                        if(jsondata.length>0){
                            if (Goal > 2 || indexnum > 0) {
                                if (indexnum > 0) { toAddTechnic(Goal - 1);}
                                var solutionNo = indexno - 1;
                                $("input[name='solution[" + solutionNo + "].technicid']").val(jsondata[0].inc_id);
                                $("input[name='solution[" + solutionNo + "].technicidlabel']").val(jsondata[0].Technicalcode);
                                $("input[name='solution[" + solutionNo + "].mindmapid']").val(mindmapid+'_'+myself_node['key']);
                                $("input[name='solution[" + solutionNo + "].mindmaplabel']").val(myself_node['text']);
                                $("input[name='solution[" + solutionNo + "].mindmapidlabel']").val(myself_node['text']);
                                indexnum = indexnum+1
                            } else {
                                $("input[name='solution[0].technicid']").val(jsondata[0].inc_id);
                                $("input[name='solution[0].technicidlabel']").val(jsondata[0].Technicalcode);
                                $("input[name='solution[0].mindmapid']").val(mindmapid+'_'+myself_node['key']);
                                $("input[name='solution[0].mindmaplabel']").val(myself_node['text']);
                                $("input[name='solution[0].mindmapidlabel']").val(myself_node['text']);
                                indexnum = indexnum+1
                            }
                        }
                    }
                }
            })
        }

    })
    
    //MindMapID輸入框點擊事件
    $("#test-l-3").on("dblclick", ".mindmapid", function (obj) {
        $("#modalbtn").click()
        $("#rightPane").css({
            "width": "298.5px"
        })
        thisGoal = obj.target.name.replace(/[^0-9]/ig, "");
        agoMindmapidlabel = $("input[name='solution[" + thisGoal + "].mindmapidlabel']").val();
        agoMindmapid = $("input[name='solution[" + thisGoal + "].mindmapid']").val();
    })




    //Technic選擇窗口單身點擊事件
    $('#Technictable tbody').on('click', 'tr', function () {
        var table = $('#Technictable').DataTable();
        var technicidlabel = table.row(this).data()['mb023'] + '(' + table.row(this).data()['mb004'] + ')'
        var technicid = table.row(this).data()['inc_id']
        $("input[name='solution[" + TechnicInputid + "].technicidlabel']").val(technicidlabel);
        $("input[name='solution[" + TechnicInputid + "].technicid']").val(technicid);
    });
    //Technic選擇窗口取消按鈕點擊事件
    $('.technicmodelhidden').on('click', function () {
        //還原輸入框內容
        $("input[name='solution[" + TechnicInputid + "].technicidlabel']").val(agoTechnicidlabel);
        $("input[name='solution[" + TechnicInputid + "].technicid']").val(agoTechnicid);
        TechnicInputid = '';
        agoTechnicidlabel = '';
        agoTechnicid = '';
    });
    //Technic選擇窗口確定按鈕點擊事件
    $('#technicEnterbtn').on('click', function () {
        $("#SearchTechnicModal").modal('hide')
        TechnicInputid = '';
    });



    var test_search = new SWSelectquery("#Technicmodelbtn"); //設置Search按鈕為觸發標籤
    test_search.table.columns = [
        { field: "inc_id", label: gettext("INC_ID"), visible: false },
        { field: "mb023", label: gettext("Technical ID") },
        { field: "mb004", label: gettext("Technical Topic") },
        { field: "mb008", label: gettext("Usage") },
        { field: "mb005", label: gettext("Contact") },
    ];
    test_search.height(500);
    test_search.width(1100);
    test_search.datasource = '/looper/DailyPlanner/TechnicDatatable';

    test_search.on_selected_event = function (data) {
        var technicidlabel = data['mb023'] + '(' + data['mb004'] + ')'
        var technicid = data['inc_id']
        $("input[name='solution[" + TechnicInputid + "].technicidlabel']").val(technicidlabel);
        $("input[name='solution[" + TechnicInputid + "].technicid']").val(technicid);
        TechnicInputid = '';
    }
    //Technic選擇窗口取消按鈕點擊事件
    $('#SWSelectquery-Modal-1 .modal-footer .btn-light').on('click', function () {
        //還原輸入框內容
        $("input[name='solution[" + TechnicInputid + "].technicidlabel']").val(agoTechnicidlabel);
        $("input[name='solution[" + TechnicInputid + "].technicid']").val(agoTechnicid);
        TechnicInputid = '';
        agoTechnicidlabel = '';
        agoTechnicid = '';
    });

    //Technic輸入框點擊事件
    $("#test-l-3").on("click", ".technicid", function (obj) {
        $("#Technicmodelbtn").click()
        TechnicInputid = obj.target.name.replace(/[^0-9]/ig, "");
        agoTechnicidlabel = $("input[name='solution[" + TechnicInputid + "].technicidlabel']").val();;
        agoTechnicid = $("input[name='solution[" + TechnicInputid + "].technicid']").val();

    })

    $("input[name='startdate']").on("change", function(){
        $("input[name='inputdate']").val($(this).val());
        var inputdate = $(this).val();
        var taskno = $("input[name='taskno']").val();
        if (taskno != '' && inputdate != '') {
            var params = {'taskno':taskno, 'inputdate':inputdate};
            $.get("/looper/technic/get_task", params, function(result){
                if (result.status) {
                    $("input[name='itemno']").val(result.data[1]);
                }
            })
        }
    })



    //獲取路由的參數
    function getQueryString(name) {  
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");  
        var r = window.location.search.substr(1).match(reg);  
        if (r != null) return decodeURI(r[2]);
        return '';  
    }

    //獲取對應參數
    var parameterinputdate = getQueryString('inputdate'); 
    
    // if(inputdate != ''){
    //     $('input[name="startdate"]').val(inputdate)
    // }

});

function toAddTechnic(mindmapindex) {
    //增加Technical的方法
    var goal1_addT = new SWRow();
    var technical = new SWText("solution[" + indexno + "].technicidlabel", "text", gettext("Technical") + " :");
    goal1_addT.addComponent(technical);
    var ftime = new SWText("solution[" + indexno + "].ftime", "text", gettext("FTime") + " :");
    goal1_addT.addComponent(ftime);
    var etime = new SWText("solution[" + indexno + "].etime", "text", gettext("ETime") + " :");
    goal1_addT.addComponent(etime);
    var goal1_addT1 = new SWRow();
    var satisfactory = new SWCheckbox("solution[" + indexno + "].satisfactory", gettext("Satisfactory"));
    goal1_addT1.addComponent(satisfactory);
    var refinement = new SWCheckbox("solution[" + indexno + "].refinement", gettext("Refinement"));
    goal1_addT1.addComponent(refinement);
    var ambiguous = new SWCheckbox("solution[" + indexno + "].ambiguous", gettext("Ambiguous"));
    goal1_addT1.addComponent(ambiguous);
    var goal1_addT2 = new SWRow();
    var tis = new SWCombobox("solution[" + indexno + "].tis", "TIS", ["R","Y"])
    tis.dom.addClass("technical-tis");    
    tis.setHorizontalDisplay()
    goal1_addT1.dom.find(".col_right").prepend(tis.dom);    
    var remark = new SWTextarea("solution[" + indexno + "].remark", gettext("Remark") + " :", 3);
    goal1_addT2.addComponent(remark);
    $(".goal" + mindmapindex + "_tech").append(goal1_addT.dom);
    $(".goal" + mindmapindex + "_tech").append(goal1_addT1.dom);
    $(".goal" + mindmapindex + "_tech").append(goal1_addT2.dom);

    var solution_type = new SWText("solution[" + indexno + "].mindmapid", "hidden", "Solution Type：", "");
    $("#mindmapinput" + mindmapindex).prepend(solution_type.dom);
    var Technic_type = new SWText("solution[" + indexno + "].technicid", "hidden", "Technical：", "");
    $("#mindmapinput" + mindmapindex).prepend(Technic_type.dom);
    var solution_stitemno = new SWText("solution[" + indexno + "].stitemno", "hidden", "Solution Type：", "");
    $("#mindmapinput" + mindmapindex).prepend(solution_stitemno.dom);
    var mindmaplabel = new SWText("solution[" + indexno + "].mindmaplabel", "hidden", "Mindmap Label：", "");
    $("#mindmapinput" + mindmapindex).prepend(mindmaplabel.dom);

    
    $("input[name='solution[" + indexno + "].mindmaplabel']").addClass("mindmaplabelinput");
    $("input[name='solution[" + indexno + "].mindmapid']").addClass("mindmapidinput");
    $("input[name='solution[" + indexno + "].technicidlabel']").addClass("technicid");

    $("#mobile_technic .div-1").addClass("col-12");
    $("#mobile_technic .div-2").addClass("col-12");
    $("#mobile_technic .div-3").addClass("col-12");
    indexno = indexno + 1
}

function toDeleteTechnic(mindmapindex) {
    //刪除Technical的方法
    var divChildren = $(".goal" + mindmapindex + "_tech").children().length
    var inputindex = indexno - 1
    if (divChildren == 0) { return }
    for (var i = divChildren - 1; i > divChildren - 4; i--) {
        $(".goal" + mindmapindex + "_tech").children()[i].remove()
    }
    $("input[name='solution[" + inputindex + "].technicid']").remove()
    $("input[name='solution[" + inputindex + "].mindmapid']").remove()
    $("input[name='solution[" + inputindex + "].stitemno']").remove()
    indexno = indexno - 1
}

function toRemoveGoal(Goalindex) {
    if (Goalindex == 1) {
        $("#ContainerGoal1").remove()
        $(".titlegoal" + Goalindex).remove()
    } else {
        $("#mindmapinput" + Goalindex).remove()
        $(".titlegoal" + Goalindex).remove()
        $(".goal" + Goalindex).remove()
        $(".goal" + Goalindex + "_tech").remove()
    }
}


