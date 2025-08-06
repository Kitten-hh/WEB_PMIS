/**** Bonus Simulation分析頁面的腳本文件 ****/
var filter_id = undefined;
var global_edatefrom= undefined; // 
var global_edateto= undefined
$(function () {    
    var isBounsSearch = false; //是否查詢Bonus
    var taskData; //任務列表數據
    var groupBy;
    var taskTable;
    var bonusData;
    var contactBonusData;
    var cloneBonusData;
    var search_tab = $("#search_tab").clone();
    search_tab.removeClass("d-none");
    $("#search_tab").remove();
    /*
    if ($(document).width() < 768) {
        var i = 4
        while (i <= 12) {
            $("#c" + i).remove();
            i++;
        }
    }*/
    //$('.btn-success').hide(); // button1
    //$('.btn-light-danger').html('By Contact'); // button2
    //$('.footer .nav a').eq(2).html('By TaskType'); // button3
    $('.footer .nav').children().remove();
    //開始設置查詢對話框
    var search = new SWAdvancedsearch(".search_more"); //設置Search按鈕為觸發標籤
    var group = new SWAdvancedsearch.Group(SWAdvancedsearch.Condition.AND);

    var contact = new SWAdvancedsearch.Rule("contact", SWAdvancedsearch.Type.STRING,
        SWAdvancedsearch.Operator.EQUAL, "聯繫人");
    group.addRule(contact);

    var start_date = new SWAdvancedsearch.Rule("edatefrom", SWAdvancedsearch.Type.DATE,
        SWAdvancedsearch.Operator.GREATER_OR_EQUAL, "從實際結束時間")

    var end_date = new SWAdvancedsearch.Rule("edateto", SWAdvancedsearch.Type.DATE,
        SWAdvancedsearch.Operator.LESS_OR_EQUAL, "到實際結束時間")

    group.addRowRule([start_date, end_date]);

    search.addGroup(group);
    search.dom.find(".modal-body").append(search_tab);
    search.dom.find(".modal-body").addClass("p-0");
    search.dom.find(".modal-body .tab-content").addClass("pl-3 pr-3");
    search.dom.find(".modal-body div:eq(0)").detach().appendTo("#search_basic");
    $("#search_modal .modal-body").append(search.dom);

    search.on_check_data = function(){
        var id = $('#search_tab .tab-content .active').attr('id');
        if (id == "search_basic") {
            var edatefrom = $(":input[name='edatefrom']").val();
            var edateto = $(":input[name='edateto']").val();
            if (edatefrom=="") {
                //alert("請輸入開始時間"); 
                showMessage("請輸入[從實際結束時間]");                     
                return false;
            }
            if (edateto=="") {        
                showMessage("請輸入[到實際結束時間]");           
                return false;
            } 
        }else {
            if ($("#search_tab .list-group a.active").length == 0) {
                showMessage("請查詢並選擇一個查詢條件!");
                return false;
            }
        }
        return true;
    }

    search.on_search_event = function (filter) {
        console.info(filter);
        var id = $('#search_tab .tab-content .active').attr('id');
        if (id == "search_basic") {
            if (filter != "null") {
                var jsonArray = JSON.parse(filter)
                var j = 0;            
                var contact="";
                var edatefrom;
                var edateto;
                for (j in jsonArray.rules) {
                    var jsonObj = jsonArray.rules[j];
                    console.info(jsonObj.value);
                    if (jsonObj.id == "contact") {
                        contact = jsonObj.value;
                    } else if (jsonObj.id == "edatefrom") {
                        edatefrom = jsonObj.value;
                    } else if (jsonObj.id == "edateto") {
                        edateto = jsonObj.value;
                    }
                } 
                bonus_analysis(contact,edatefrom,edateto);
                //$("[name='lb_contact']").html("（" + contact + "）");
                //var contact='qfq';
                //var edatefrom='2021-03-01';
                //var edateto='2021-03-31';
                /*
                $.ajax({
                    method: "GET",
                    url: "/bonus/bonus_analysis",
                    data: { "contact": contact, "edatefrom": edatefrom, "edateto": edateto },
                    success: function (result) {
                        
                        message = result.errorMessage;
                        if (message != '') {
                            //alert(message);
                            showMessage(message);                  
                            return;
                        }
                        if(contact!=""){
                            showBonusResult(result.bonusResult);                                    
                            isBounsSearch = true;     
                            setComponent(contact,'');                                           
                            showTaskTypes(result.tasktypedata);
                        }else{
                            isBounsSearch = false;
                            var filter = "EDate Between {0} and {1}".format(edatefrom,edateto);
                            setComponent('',filter);  
                        }
                        
                        showTasks(result.data);                   
                    },
                    error: function (xhr, textStatus, errorThrown) {
                        removeload();
                        showMessage("错误信息:" + xhr.statusText);
                    }
                })*/
            }
            else {
                showMessage("請輸入條件");                
            }
        } else {
            search_task($("#search_tab .list-group a.active")[0]);
        }
    }

    function bonus_analysis(contact,edatefrom,edateto){
        var isChecked = $('#cb_calSat').prop('checked');        
        $.ajax({
            method: "GET",
            url: "/bonus/bonus_analysis",
            data: { "contact": contact, "edatefrom": edatefrom, "edateto": edateto , "calSat":isChecked},
            success: function (result) {                
                message = result.errorMessage;
                if (message != '') {
                    //alert(message);
                    showMessage(message);                  
                    return;
                }
                if(contact!=""){
                    cloneBonusData = JSON.parse(JSON.stringify(result.bonusResult));
                    showBonusResult(result.bonusResult);                                    
                    isBounsSearch = true;     
                    setComponent(contact,'');                                           
                    showTaskTypes(result.tasktypedata);
                }else{
                    isBounsSearch = false;
                    var filter = "EDate Between {0} and {1}".format(edatefrom,edateto);
                    setComponent('',filter);  
                }
                
                showTasks(result.data);                   
            },
            error: function (xhr, textStatus, errorThrown) {
                removeload();
                showMessage("错误信息:" + xhr.statusText);
            }
        })
    }
    //結束設置查詢對話框

    //顯示Bonus的計算結果
    function showBonusResult(data,isShowHint=true) {
        contactBonusData = data;
        //$("#BudgetAllowance").html(data["BudgetAllowance"]);
        $("#BudgetAllowance").val(data["BudgetAllowance"]);
        $("#PerfectScoring").html(data["PerfectScoring"]);
        //$("#RatioOFM").html(data["RatioOFM"]);
        //$("#RatioOFS").html(data["RatioOFS"]);
        //$("#RatioOFP").html(data["RatioOFP"]);
        $("#RatioOFM").val(data["RatioOFM"]);
        $("#RatioOFS").val(data["RatioOFS"]);
        $("#RatioOFP").val(data["RatioOFP"]);
        $("#ManagementS").html(data["ManagementS"]);
        $("#PerformanceS").html(data["PerformanceS"]);
        $("#QuarterWorkingDay").html(data["QuarterWorkingDay"]);
        $("#WorkingDay").html(data["WorkingDay"]);
        //$("#ManagementRatio").html(data["ManagementRatio"]);
        //$("#PerformanaceRatio").html(data["PerformanaceRatio"]);
        $("#ManagementRatio").val(data["ManagementRatio"]);
        $("#PerformanaceRatio").val(data["PerformanaceRatio"]);
        $("#Salary").html(data["Salary"]);

        $("#Score").html(data["Score"]);
        $("#LookupScore").html(data["LookupScore"]);
        $("#ScoreAvg").html(data["ScoreAvg"]);
        $("#SuggAvg").html(data["SuggAvg"]);
        $("#QuarterScore").html(data["QuarterScore"]);
        $("#QuarterLookupScore").html(data["QuarterLookupScore"]);
        $("#SimulateScore").html(data["SimulateScore"]);
        $("#ScoreBonus").html(data["ScoreBonus"]);
        $("#LookupScoreBonus").html(data["LookupScoreBonus"]);
        $("#SimulatePerMth").html(data["SimulatePerMth"]);
        $("#ScoreActualQuarter").html(data["ScoreActualQuarter"]);
        $("#LookupScoreActualQuarter").html(data["LookupScoreActualQuarter"]);
        $("#ActInPerMth").html(data["ActInPerMth"]);
        var differ = data["SuggAvg"]-data["ScoreAvg"];
        //當每日實際得分比建議分少20時，則提示
        if (data["SuggAvg"]-data["ScoreAvg"]>20 && isShowHint)
            showMessage("Avg: {0} 比 Sugg.Avg: {1} 低 {2} （不達標）".format(data["ScoreAvg"],data["SuggAvg"],differ.toFixed(2)));
    }

    function calculate_bonus(bonusPara,isShowHint=true){   
        /*     
        var PerfectScoring = data["Salary"] * (1 + data["BudgetAllowance"]/100) * 3/2;
        var ManagementS = PerfectScoring * data["RatioOFM"]/100;
        var PerformanceS = PerfectScoring * data["RatioOFP"]/100;
        var ScoreAvg = data["TotalScore"] / data["WorkingDay"];
        var LookupScoreAvg = data["TotalLookupScore"] / data["WorkingDay"];
        var SuggAvg = (PerfectScoring - ManagementS - PerformanceS) / data["QuarterWorkingDay"];
        var QuarterScore = ScoreAvg * data["QuarterWorkingDay"] + ManagementS + PerformanceS;
        var QuarterLookupScore = LookupScoreAvg * data["QuarterWorkingDay"] + ManagementS + PerformanceS;
        var SimulateScore = SuggAvg * data["QuarterWorkingDay"] + ManagementS + PerformanceS;
        var ScoreBonus = QuarterScore - data["Salary"]*3/2;
        var LookupScoreBonus = QuarterLookupScore - data["Salary"]*3/2;
        var SimulatePerMth = (SuggAvg * data["QuarterWorkingDay"] + ManagementS * data["ManagementRatio"]/100 + PerformanceS * data["PerformanaceRatio"]/100)*2/3;
        var ScoreActualQuarter = data["Salary"]*3/2 + ScoreBonus;
        var LookupScoreActualQuarter = data["Salary"]*3/2 + LookupScoreBonus;
        var ActInPerMth = ScoreActualQuarter/3*2;
        
        data["PerfectScoring"] = Math.round(PerfectScoring,2);
        data["ManagementS"] = Math.round(ManagementS,2);
        data["PerformanceS"] = Math.round(PerformanceS,2);
        data["ScoreAvg"] = Math.round(ScoreAvg,2);
        data["LookupScoreAvg"] = Math.round(LookupScoreAvg,2);
        data["SuggAvg"] = Math.round(SuggAvg);
        data["QuarterScore"] = Math.round(QuarterScore);
        data["QuarterLookupScore"] = Math.round(QuarterLookupScore);
        data["SimulateScore"] = Math.round(SimulateScore);
        data["ScoreBonus"] = Math.round(ScoreBonus);
        data["LookupScoreBonus"] = Math.round(LookupScoreBonus);
        data["SimulatePerMth"] = Math.round(SimulatePerMth);
        data["ScoreActualQuarter"] = Math.round(ScoreActualQuarter);
        data["LookupScoreActualQuarter"] = Math.round(LookupScoreActualQuarter);
        data["ActInPerMth"] = Math.round(ActInPerMth);
        showBonusResult(data,isShowHint);  
        */
        var isChecked = $('#cb_calSat').prop('checked');      
        $.ajax({
            method: "GET", 
            url: "/bonus/bonus_recalculate",  
            data: {"bonusPara":JSON.stringify(bonusPara)}, //把Json轉成字符串                        
            success: function (result) { 
                //cloneBonusData = JSON.parse(JSON.stringify(result.data));
                showBonusResult(result.data,isShowHint);  
            },
            error: function (xhr, textStatus, errorThrown) {                
                showMessage("错误信息:" + xhr.statusText);
            }
        });
       
    }

    //查询功能,填充下拉框
    $("#search_filter_btn").on("click", function () {
        var filter_val = $("#template-users").val();
        var is_dialy = $("#IsDaily").is(":checked") ? "Y" : "N";
        $.ajax({
            url: "/bonus/query/search/",
            data: { filter: filter_val, is_dialy: is_dialy },
            success: function (data) {
                var result = eval(data);
                display_filter_list(result.data);
                $('#no_content').addClass("d-none");
                $('#card_task').removeClass("d-none");
            },
            fail: function (data) {
                $("#search_advanced .pre-scrollable").empty();
            }
        })
    })    
    
    //上周
    $(".search_lastweek").on("click", function () {          
        global_edatefrom = getLastWeekStartDate();
        global_edateto= getLastWeekEndDate();      
        $('#selectUserModal').modal('show');        
    })
    //昨日
    $(".search_yesterday").on("click", function () {  
        var yesterday = new Date();
        yesterday.setDate(yesterday.getDate()-1);       
        global_edatefrom = formatDate(yesterday);
        global_edateto= formatDate(yesterday);      
        $('#selectUserModal').modal('show');        
    })
    //本日
    $(".search_today").on("click", function () {          
        global_edatefrom = formatDate(now);
        global_edateto= formatDate(now);      
        $('#selectUserModal').modal('show');        
    })
    //本周
    $(".search_week").on("click", function () {    
        global_edatefrom = getWeekStartDate();
        //global_edateto= getWeekEndDate();
        global_edateto= formatDate(now);
        $('#selectUserModal').modal('show');  
    })    
    //上月
    $(".search_lastmonth").on("click", function () {
        global_edatefrom = getLastMonthStartDate();
        global_edateto= getLastMonthEndDate();
        $('#selectUserModal').modal('show');  
    })
    //本月
    $(".search_month").on("click", function () {
        global_edatefrom = getMonthStartDate();
        //global_edateto= getMonthEndDate();
        global_edateto= formatDate(now);
        $('#selectUserModal').modal('show');  
    })
    //本季度
    $(".search_quarter").on("click", function () {
        global_edatefrom = getQuarterStartDate();
        //global_edateto= getQuarterEndDate();
        global_edateto= formatDate(now);
        $('#selectUserModal').modal('show');  
    })
    //上季度
    $(".search_lastquarter").on("click", function () {
        global_edatefrom = getLastQuarterStartDate();
        global_edateto= getLastQuarterEndDate();
        $('#selectUserModal').modal('show');  
    })

    $(".search_summary").on("click", function () {
        //$("#edatefrom").val(getQuarterStartDate());
        //$("#edateto").val(getQuarterEndDate());
        var edatefrom = getQuarterStartDate();   
        var edateto= formatDate(now);
        /*
        if ((edatefrom=='') || (edateto=='')){
            alert('參數不能為空');
        }
        $('#selectDateModal').modal('hide');  
        */
        $('#summaryModal').modal('show'); 
        $("#dt_summary tbody").children().remove();
        $("#lb_progress").html("（正在加載...）");

        //var edatefrom = getQuarterStartDate();   
        //var edateto= formatDate(now);    
        var isChecked = $('#cb_calSat').prop('checked');  
        $.ajax({
            method: "GET",
            url: "/bonus/analyse_bar",
            data: {"edatefrom": edatefrom, "edateto": edateto, "calSat": isChecked},
            success: function (result) { 
                bonusData = result;            
                bonusData = sortBonusData(bonusData);
                displaySummaryData(bonusData);
                $("#lb_progress").html("");
            },
            error: function (xhr, textStatus, errorThrown) {
                $("#lb_progress").html("");
                showMessage("错误信息:" + xhr.statusText);
            }
        }) 
        
    })
    
    $(".bonus_summary").on("click", function () {
        var edatefrom = $("#edatefrom").val();   
        var edateto= $("#edateto").val();
        if ((edatefrom=='') || (edateto=='')){
            alert('參數不能為空');
        }
        $('#selectDateModal').modal('hide');  

        $('#summaryModal').modal('show'); 
        $("#dt_summary tbody").children().remove();
        $("#lb_progress").html("（正在加載...）");

        //var edatefrom = getQuarterStartDate();   
        //var edateto= formatDate(now);    
        var isChecked = $('#cb_calSat').prop('checked');  
        $.ajax({
            method: "GET",
            url: "/bonus/analyse_bar",
            data: {"edatefrom": edatefrom, "edateto": edateto, "calSat": isChecked},
            success: function (result) { 
                bonusData = result;            
                bonusData = sortBonusData(bonusData);
                displaySummaryData(bonusData);
                $("#lb_progress").html("");
            },
            error: function (xhr, textStatus, errorThrown) {
                $("#lb_progress").html("");
                showMessage("错误信息:" + xhr.statusText);
            }
        }) 
    })
    //把Bonus的結果轉成數組，並按達表值從小到大進行排序
    function sortBonusData(bonusData){
        var result=[];
        for(let contact in bonusData) {  
            let data =  bonusData[contact]
            let ScoreAvg = data["ScoreAvg"];
            let SuggAvg = data["SuggAvg"];
            //計算達到值
            let percent = parseInt((ScoreAvg-SuggAvg)/SuggAvg*100); 
            data["percent"] = percent;
            data["contact"]= contact;  
            result.push(data);          
        }
        //按達表值從小到大進行排序
        result = result.sort(function(a,b){
            return a.percent-b.percent;
        });
        return result;
    }
    //把匯總的結果顯示到表格中
    function displaySummaryData(bonusData){               
        for(let data of bonusData) {   
            let contact = data["contact"];
            let RatioOFM = data["RatioOFM"];
            let RatioOFS = data["RatioOFS"];
            let RatioOFP = data["RatioOFP"];
            let ManagementRatio = data["ManagementRatio"];
            let PerformanaceRatio = data["PerformanaceRatio"];

            let LookupScore = data["LookupScore"];
            let QuarterLookupScore = data["QuarterLookupScore"];
            let LookupScoreBonus = data["LookupScoreBonus"];
            let LookupScoreActualQuarter = data["LookupScoreActualQuarter"];

            let ScoreAvg = data["ScoreAvg"];
            let SuggAvg = data["SuggAvg"];
            let SimulateScore = data["SimulateScore"];
            let SimulatePerMth = data["SimulatePerMth"];
            let ActInPerMth = data["ActInPerMth"];

            let percent = data["percent"]; 

            let newTd0 = `<td>
                            <div class="symbol symbol-35 symbol-light-info flex-shrink-0 mr-2">
                                <span
                                    class="symbol-label font-weight-bold font-size-lg text-uppercase">{0}</span>
                            </div>
                        </td>`.format(contact);       

            let newTd1 = `<td class="text-center">
                        <div
                            class="d-flex align-items-center justify-content-center font-weight-bold font-size-h5 font-size-h6-md font-size-h5-xl">
                            <p class="mb-0 text-warning text-hover-danger">{0}</p>
                            <span class="mx-2">:</span>
                            <p class="mb-0 text-warning text-hover-danger">{1}</p>
                            <span class="mx-2">:</span>
                            <p class="mb-0 text-warning text-hover-danger">{2}</p>
                        </div>
                    </td>`.format(RatioOFM,RatioOFS,RatioOFP);


            let newTd2 = `<td class="text-center">
                            <span class="font-weight-bold text-warning text-hover-danger font-size-h5 font-size-h6-md font-size-h5-xl">{0}</span>
                        </td>`.format(ManagementRatio);

            let newTd3 = `<td class="text-center border-right">
                            <span class="font-weight-bold text-warning text-hover-warning font-size-h5 font-size-h6-md font-size-h5-xl">0</span>
                        </td>`.format(PerformanaceRatio);     

            let newTd4 = `<td class="text-center">
                            <span class="font-weight-bolder d-block font-size-h5 font-size-h6-md font-size-h5-xl text-danger text-hover-warning">{0}</span>
                        </td>`.format(LookupScore);        

            let newTd5 = `<td class="text-center">
                            <span class="font-weight-bolder d-block font-size-h5 font-size-h6-md font-size-h5-xl text-danger text-hover-warning">{0}</span>
                        </td>`.format(QuarterLookupScore);            

            let newTd6 = `<td class="text-center">
                            <span class="font-weight-bolder d-block font-size-h5 font-size-h6-md font-size-h5-xl text-danger text-hover-warning">{0}</span>
                        </td>`.format(LookupScoreBonus);

            let newTd7 = `<td class="text-center border-right">
                            <span class="font-weight-bolder d-block font-size-h5 font-size-h6-md font-size-h5-xl text-danger text-hover-warning">{0}</span>
                        </td>`.format(LookupScoreActualQuarter);

            let newTd8 = `<td class="text-center">
                            <span class="font-weight-bolder d-block font-size-h5 font-size-h6-md font-size-h5-xl text-primary text-hover-warning">{0}</span>
                        </td>`.format(ScoreAvg);

            let newTd9 = `<td class="text-center">
                            <span class="font-weight-bolder d-block font-size-h5 font-size-h6-md font-size-h5-xl text-primary text-hover-warning">{0}</span>
                        </td>`.format(SuggAvg);

            let newTd10 = `<td class="text-center">
                            <span class="font-weight-bolder d-block font-size-h5 font-size-h6-md font-size-h5-xl text-primary text-hover-warning">{0}</span>
                        </td>`.format(SimulateScore);

            let newTd11 = `<td class="text-center">
                                <span class="font-weight-bolder d-block font-size-h5 font-size-h6-md font-size-h5-xl text-primary text-hover-warning">{0}</span>
                            </td>`.format(SimulatePerMth);

            let newTd12 = `<td class="text-center">
                                <span class="font-weight-bolder d-block font-size-h5 font-size-h6-md font-size-h5-xl text-primary text-hover-warning">{0}</span>
                            </td>`.format(ActInPerMth);

            let newTd13 = `<td class="text-center pr-0">
                                <div class="d-flex align-items-center text-success font-size-h4 font-size-h5-md font-size-h4-lg"> <i
                                    class="fas fa-caret-up text-success mr-2"></i> {0}% </div>
                            </td>`.format(percent)
            if (percent<0) 
                newTd13 = `<td class="text-center pr-0">
                                <div class="d-flex align-items-center text-danger font-size-h4 font-size-h5-md font-size-h4-lg"> <i
                                    class="fas fa-caret-down text-danger mr-2"></i> {0}% </div>
                            </td>`.format(percent)
            
            let newRow = '<tr>'+ newTd0 + newTd1 + newTd2 + newTd3 + newTd4 + newTd5 + newTd6 + newTd7 + newTd8 + newTd9 + newTd10 + newTd11 + newTd12 + newTd13 + '</tr>'

            $("#dt_summary tbody").append(newRow); 
        }
    }

    $(".bonus_analysis").on("click", function () {
        var contact=$('#txtContact').val();    
        if (contact==''){
            setPopover($('#txtContact'),'請輸入聯繫人');
            return;
        } 
        $('#selectUserModal').modal('hide'); 
        bonus_analysis(contact,global_edatefrom,global_edateto);
    })

    function setPopover(el, text) {
        el.popover({
          content: text,
          container: "body",
          placement: "top",
        });
        el.popover("show");
        setTimeout(function () {
          el.popover("dispose");
        }, 1500);
    }
    

    function display_filter_list(data) {
        var dom = $("#SWListgroup").clone();
        dom.removeAttr("id");
        dom.addClass("SWListgroup");
        var item = dom.find("a");
        dom.empty();
        for(d of data) {
            var local_item = item.clone();
            dom.append(local_item.prop("outerHTML").render(d));
        }
        $("#search_advanced .pre-scrollable").empty()
        dom.show();
        $("#search_advanced .pre-scrollable").append(dom);

        $('#search_advanced .list-group .list-group-item').on("click", function(e) {
            e.preventDefault()
            $(this).parent().find('.list-group-item').removeClass('active');
            $(this).addClass('active');
        });        
    }  


    function search_task(self){
        var id = $(self).attr("pk");  
        //var filter_text = $("#template-users").val();
        var filter_text = $(self).children(".list-group-item-body").text()
        $.ajax({
            method: "GET",                
            url: "/bonus/task_enquiry",
            data: { "query_filter_id": id, "sort": "Contact"},
            success: function (result) {                
                taskData = result.data;                    
                isBounsSearch = false; 
                setComponent('',filter_text);
                showTasks(result.data);               
            },
            error: function (xhr, textStatus, errorThrown) {
                removeload();
                showMessage("错误信息:" + xhr.statusText);
            }                
        });
    }    

    function init_task_table() {
        if (taskTable == undefined) {
            taskTable = new SWDataTable("#db_wapper", "dt_task");
    
            //table.pageLength = 10; 
            taskTable.paging = false;
            taskTable.searching = false;
            taskTable.firstColSelected = true;
            taskTable.firstColIdTmpl = "[[taskno]]";
            taskTable.checked_with_selected = false;
            /*
            { "data": "name",       className: "all" },
                { "data": "position",   className: "min-phone-l" },
                { "data": "office",     className: "min-tablet" },
                { "data": "start_date", className: "never" },
                { "data": "salary",     className: "desktop" },
                { "data": "extn",       className: "none" }
            */
            //table.groupBy = "contact";        
            taskTable.columns = [     
                { field: "contact", label: "Contact" , className: 'all'},  
                { field: "taskno", label: "TaskNo", width: "15%" , className: 'min-phone-l'},
                { field: "progress", label: "Progress", visible:false},
                { field: "task", label: "Description", width: "50%" , className: 'min-tablet'},
                //{field:"edate", label:"E Date", render:SWDataTable.DateRender},            
                {
                    field: "edate", label: "E Date", width:"15%",
                    className: 'desktop',
                    render: function ChangeDateFormat(value) {
                        var reg = /^\s*$/;
                        //返回值为true表示不是空字符串
                        if (value != null && value != undefined && !reg.test(value)) {
                            var orderdate = new Date(value);
                            var month = orderdate.getMonth() + 1;
                            var day = orderdate.getDate();
                            month = (month.toString().length == 1) ? ("0" + month) : month;
                            day = (day.toString().length == 1) ? ("0" + day) : day;
                            //当前日期 yyyy-MM-dd
                            return orderdate.getFullYear() + '-' + month + '-' + day;
                        } else
                            return '';
                    }
                },
                { field: "score", label: "S", width: "5%", className: "fontBlue" , className: 'desktop'},
                { field: "lookupscore", label: "LS", width: "5%", className: "fontRed" , className: 'desktop'}, 
                { field: "realtasktype", label: "Task Type" , width: "10%", className: 'desktop'},
                { field: "tasktypedc", label: "TaskType Description" , className: 'desktop'},   
                {
                    field: "inc_id",  
                    label:"Detail",      
                    className: 'desktop',          
                    render: function showDetail(id) {
                        //return `<a target="_blank" href="/bonus/get_Task_Details/?inc_id=`+ id +`"><i class="fa fa-chevron-right"></i></a>`;
                        return `<a href="javascript:void(0);" onclick="showTaskDetail(`+id+`)"><i class="fa fa-chevron-right"></i></a>`;
                    }                       
                },             
            ];
    
            taskTable.setOptions(
            {                        
                responsive: true,
                scrollY: "420px",
                deferRender: true,
                scrollCollapse: true,
                //select: {
                    //style: 'multi'
                //},
                //分組統計
                drawCallback: function (settings) {
                    //設置分組信息
                    var groupColumn = undefined;
                    var scoreColumn = undefined;
                    var lookupScoreColumn = undefined;        
                    if(isBounsSearch==false && groupBy!="" && groupBy!=undefined){
                        //當分組不為空時，根據列名得到列序號
                        groupColumn = taskTable.getColumnIndexByName(groupBy);
                        if(groupBy=="contact"){
                            scoreColumn = taskTable.getColumnIndexByName("score");
                            lookupScoreColumn = taskTable.getColumnIndexByName("lookupscore");
                        }
                    }
    
                    var api = this.api();
                    $("#dt_task tbody tr").dblclick(function(e){               
                        //var table = $('#dt_task').DataTable();
                        //得到當前行的id
                        var id = api.row(this).data()['inc_id'];                        
                        init_task(id);   
                        //showTaskDetail(id);                    
                    });
                    if(groupColumn==undefined) return;  
                    var rows = api.rows({ page: 'current' }).nodes();
                    var last = null;
                    var sumScore = 0;
                    var sumLookupScore = 0;
                    //var name = null;
                    api.column(groupColumn, { page: 'current' }).data().each(function (group, i) {
                        var client_btn = `<span class='client_span'><i class="fa fa-chevron-right"></i></span>`;                    
                            if (last !== group) {
                                if (groupBy == "contact") { 
                                    //联系人需要统计分数
                                    sumScore = 0;
                                    sumLookupScore = 0;
                                    api.column(scoreColumn, { page: 'current' }).data().each(function (score, i) {
                                        if (group == api.column(groupColumn, { page: 'current' }).data()[i]) {
                                            if(score!=null)
                                                sumScore += score;
                                        }
                                    });
        
                                    api.column(lookupScoreColumn, { page: 'current' }).data().each(function (lookupscore, i) {
                                        if (group == api.column(groupColumn, { page: 'current' }).data()[i]) {
                                            if(lookupscore!=null)
                                                sumLookupScore += lookupscore;
                                        }
                                    });
                                    $(rows).eq(i).before(
                                        `<tr class="group"><td colspan="3"><div class="row"><a target="_blank" href="/bonus/get_Contact_Details/?contact_name=`+group+'&query_filter_id='+filter_id+'">' + group + ' Score總分數為:' + sumScore +
                                        ', LookupScore總分數為:' + sumLookupScore + '</a></div></td></tr>'
                                        //<td>' + client_btn + '</td>
                                    );
                                } else {
                                    $(rows).eq(i).before(
                                        '<tr class="group"><td colspan="8">' + group + '</td></tr>'
                                    );
                                }
                                last = group;
                            }
                        
                    });
                }
            });
            taskTable.init([]);
        }
    }

    //顯示任務信息
    function showTasks(data){        
        if(isBounsSearch){
            $('#query_wrapper').parent().removeClass("fullscreen");
        }else {
            $('#query_wrapper').parent().addClass("fullscreen");
        }
        var first = new Date().getTime();
        var table = $('#dt_task').DataTable();
        table.columns(taskTable.getColumnIndexByName("progress")).visible(!isBounsSearch);
        table.clear().rows.add(data).columns.adjust().draw();
        console.log((new Date().getTime() - first)/1000);
    }
   

    //顯示任務的TaskType統計列表
    function showTaskTypes(data){
        $("#db_tasktype").empty();
        //var tasktype_data = result.tasktypedata;                           
        //初始化SWDataTable
        var table2 = new SWDataTable("#db_tasktype", "table2");                            
        table2.paging = false;
        table2.searching = false;
        $("#table2").append(`<tfoot><tr><th></th></tr></tfoot>`);

        table2.columns = [                               
            { field: "tasktype", label: "Task Type" , width: "130px"}, 
            { field: "description", label: "Description"},  
            { field: "score", label: "Score" , className: "fontBlue", width :"5%"},                                
            //{ field: "lookupscore", label: "LScore" ,className: "fontRed"},  
            { field: "count", label: "Count" },   
            { field: "totalscore", label: "TotalScore" , className: "fontBlue", width :"5%"},                                
            //{ field: "totallookupscore", label: "TotalLScore" ,className: "fontRed"},    
                            
        ];
        table2.setOptions(
        {                                                     
            responsive: true,
            scrollY: "600px",           
            footerCallback: function( tfoot, data, start, end, display ) {                                  
                //var dTable = $('#table2').DataTable(); 
                //$(dTable.table().footer()).html('Your html content here ....'); 
                
                var api = this.api();
                $( api.column( 0 ).footer() ).html("");
                $( api.column( 1 ).footer() ).html("");
                $( api.column( 2 ).footer() ).html("Total:");

                $( api.column( 3 ).footer() ).html(
                    api.column( 3 ).data().reduce( function ( a, b ) {
                        return a + b;
                    }, 0 )
                );

                $( api.column( 4 ).footer() ).html(
                    api.column( 4 ).data().reduce( function ( a, b ) {
                        return a + b;
                    }, 0 )
                );            

                //$( api.column( 5 ).footer() ).html("");
            }
        });
        //把RestApi返回來的JSON數據顯示在DataTable中
        table2.init(data);
    }
    /*
    $(".btn-light-danger").click(function () { 
        //按用戶分組
        if(isBounsSearch) return;  
        groupBy = "contact";             
        showTasks(taskData,);
    });

    $(".btn-light-primary").click(function () { 
        //按TaskType分組
        if(isBounsSearch) return;   
        groupBy = "realtasktype";              
        showTasks(taskData);
    });
    */
    function setComponent(contact, Condition){
        $("#btn_auditScore").show();
        if(isBounsSearch){
            $("#btn_showTaskType").show();
            $('#card_task').removeClass("d-none");
            $('#no_content').addClass("d-none");
            $("#card_para").show();
            $("#card_result").show();
            $('#query_wrapper').removeClass("d-none");
        }
        else{
            $("#btn_showTaskType").hide();
            $("#card_para").hide();
            $("#card_result").hide();
        }
        $("[name='lb_contact']").html("");
        $("[name='lb_condition']").html("");
        if(contact!=""){
            $("[name='lb_contact']").html("（" + contact + "）");
            $("#contact").val(contact);
        }
        if(Condition!="")
            $("[name='lb_condition']").html("（" + Condition + "）");
    }

    window.showTaskDetail = function (pk){
        init_task(pk);    
        //$("#editModal").modal("show");
    }

    function showMessage(msg){
        $('#msg').html(msg);
        $('#messageModal').modal('show'); 
    }

    $("#btn_showTaskType").on("click", function () { 
        $('#tasktypeModal').modal('handleUpdate');       
        $('#tasktypeModal').modal('show'); 
    });   
    

    $("#tasktypeModal").on("shown.bs.modal", function(){
        if ($.fn.DataTable.isDataTable($("#db_tasktype #table2"))) {
            var table = $("#db_tasktype #table2").DataTable();                
            table.columns.adjust();    
            setTimeout(() => {
                var table = $("#db_tasktype #table2").DataTable();                
                table.columns.adjust();                    
            }, 200);
        }
    });

    $("#btn_auditScore").on("click", function () { 
        var tasks = taskTable.getSelectedFlagData(); //得到DataTable勾選的記錄
        $.ajax({
            method: "POST", 
            url: "/bonus/audit_source",  
            data: {"tasks":JSON.stringify(tasks.datas)}, //把Json轉成字符串
            dataType: 'json',            
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },                  
            success: function (data) { 
                //showMessage(data.msg);
                showMessage('審核成功！');
            },
            error: function (xhr, textStatus, errorThrown) {                
                showMessage("错误信息:" + xhr.statusText);
            }
        });
    });

    $("#BudgetAllowance").blur(function(){
        if($("#BudgetAllowance").val() != contactBonusData["BudgetAllowance"]){
            contactBonusData["BudgetAllowance"] = Number($("#BudgetAllowance").val());
            calculate_bonus(contactBonusData,false);
        }   
    })

    $("#RatioOFM").blur(function(){
        if($("#RatioOFM").val() != contactBonusData["RatioOFM"]){
            contactBonusData["RatioOFM"] = Number($("#RatioOFM").val());
            calculate_bonus(contactBonusData,false);
        }   
    })

    $("#RatioOFS").blur(function(){
        if($("#RatioOFS").val() != contactBonusData["RatioOFS"]){
            contactBonusData["RatioOFS"] = Number($("#RatioOFS").val());
            calculate_bonus(contactBonusData,false);
        }   
    })

    $("#RatioOFP").blur(function(){
        if($("#RatioOFP").val() != contactBonusData["RatioOFP"]){
            contactBonusData["RatioOFP"] = Number($("#RatioOFP").val());
            calculate_bonus(contactBonusData,false);
        }   
    })

    $("#ManagementRatio").blur(function(){
        if($("#ManagementRatio").val() != contactBonusData["ManagementRatio"]){
            contactBonusData["ManagementRatio"] = Number($("#ManagementRatio").val());
            calculate_bonus(contactBonusData,false);
        }   
    })

    $("#PerformanaceRatio").blur(function(){
        if($("#PerformanaceRatio").val() != contactBonusData["PerformanaceRatio"]){
            contactBonusData["PerformanaceRatio"] = Number($("#PerformanaceRatio").val());
            calculate_bonus(contactBonusData,false);
        }   
    })
    
    $("#btn_restore").on("click", function () { 
        contactBonusData = JSON.parse(JSON.stringify(cloneBonusData));        
        calculate_bonus(contactBonusData,false);                
    });

    $("#btn_saveParam").on("click", function () { 
        var formData = new FormData();
        var contact = $("#contact").val();
        if (contact==""){
            alert('當前參數用戶名為空');
            return;
        }        
        formData.append('username', contact);
        formData.append('budgetallowance', $('#BudgetAllowance').val());
        formData.append('managementratio', $('#ManagementRatio').val());
        formData.append('performanaceratio', $('#PerformanaceRatio').val());
        formData.append('salary', $('#Salary').html());
        formData.append('ratioofm', $('#RatioOFM').val());
        formData.append('ratioofp', $('#RatioOFP').val());
        formData.append('ratioofs', $('#RatioOFS').val());

        $.ajax({
            method: "POST", 
            url: "/bonus/bonus/update/{0}".format(contact),  
            data: formData,
            processData:false,  
            contentType:false,
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },                  
            success: function (data) { 
                alert("保存成功");
                cloneBonusData = JSON.parse(JSON.stringify(contactBonusData));
                //bonus_analysis(contact,global_edatefrom,global_edateto);                
            },
            error: function (xhr, textStatus, errorThrown) {                
                showMessage("错误信息:" + xhr.statusText);
            }
        });
    });
    init_task_table();
});


