$(function () {     
    var contactData=[];
    var bar1Data=[];
    var bar2Data=[];
    var bonusData;
    reloadChartBar('scoreChart', 'Total Score', 'Total Lookup Score',bar1Data,bar2Data);
    reloadChartBar('avgScoreChart', 'Avg', 'Sugg.Avg',bar1Data,bar2Data);

    var search = new SWAdvancedsearch(".search_more"); //設置Search按鈕為觸發標籤
    var group = new SWAdvancedsearch.Group(SWAdvancedsearch.Condition.AND);

    var start_date = new SWAdvancedsearch.Rule("edatefrom", SWAdvancedsearch.Type.DATE,
        SWAdvancedsearch.Operator.GREATER_OR_EQUAL, "從實際結束時間")

    var end_date = new SWAdvancedsearch.Rule("edateto", SWAdvancedsearch.Type.DATE,
        SWAdvancedsearch.Operator.LESS_OR_EQUAL, "到實際結束時間")

    group.addRowRule([start_date, end_date]);

    search.addGroup(group);

    search.on_check_data = function(){
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
        return true;
    }

    function showMessage(msg){
        $('#msg').html(msg);
        $('#messageModal').modal('show'); 
    }

    search.on_search_event = function (filter) {
        console.info(filter);
        if (filter != "null") {
            var jsonArray = JSON.parse(filter)
            var j = 0;           
           
            var edatefrom='';
            var edateto='';
            for (j in jsonArray.rules) {
                var jsonObj = jsonArray.rules[j];
                console.info(jsonObj.value);
                if (jsonObj.id == "edatefrom") {
                    edatefrom = jsonObj.value;
                } else if (jsonObj.id == "edateto") {
                    edateto = jsonObj.value;
                }
            } 
            $.ajax({
                method: "GET",
                url: "/bonus/analyse_bar",
                data: {"edatefrom": edatefrom, "edateto": edateto, "calSat": true},
                success: function (result) { 
                    bonusData = result;
                    contactData=[]; 
                    let scoreBar1Data=[];
                    let scoreBar2Data=[];
                    let avgScoreBar1Data=[];
                    let avgScoreBar2Data=[];
                    for(let contact in result) {                        
                        contactData.push(contact);
                        scoreBar1Data.push(result[contact].Score);
                        scoreBar2Data.push(result[contact].LookupScore);

                        avgScoreBar1Data.push(result[contact].ScoreAvg);
                        avgScoreBar2Data.push(result[contact].SuggAvg);
                    }
                    reloadChartBar('scoreChart', 'Total Score', 'Total Lookup Score', scoreBar1Data, scoreBar2Data);
                    reloadChartBar('avgScoreChart', 'Avg', 'Sugg.Avg', avgScoreBar1Data, avgScoreBar2Data);
    
                },
                error: function (xhr, textStatus, errorThrown) {                    
                    showMessage("错误信息:" + xhr.statusText);
                }
            })
            

        } else {
            showMessage("請輸入條件");         
        }
    }        

    function reloadChartBar(chartId, bar1Label, bar2Label, bar1Data, bar2Data){
        var barData = {//新建dataset对象
            labels: contactData,
            datasets: [{
                label: bar1Label,
                backgroundColor: 'rgba(256, 255, 132, 0.2)',
                borderWidth: 1,
                data: bar1Data
            }, {
                label: bar2Label,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderWidth: 1,
                data: bar2Data
            }]
        }   
        
        var canvas = $("#" + chartId);
        var ctx = canvas[0].getContext('2d');
        var oldBar = canvas.data("bar");
        if (oldBar != undefined)
            oldBar.destroy();    
        
        //var ctx = document.getElementById(chartId).getContext('2d');//声明绘制2d对象     
        var myChart = new Chart(ctx, {//绑定标签并渲染
            type: 'bar',//声明为条形图bar
            data: barData,
            options: {//配置项
                maintainAspectRatio: true,//是否响应式选项
                onHover: function () {
                    //alert("我是鼠标移入移出事件");
                },
                onClick: function (c,i) {                    
                    e = i[0]; 
                    if(e){
                        console.log(e._index)
                        var x_value = this.data.labels[e._index];
                        //var y_value = this.data.datasets[0].data[e._index];
                        var y_value = this.data.datasets[e._datasetIndex].data[e._index];
                        console.log(x_value);
                        console.log(y_value);  
                        
                        $("#lb_contact").html(x_value);
                        showBonusResult(bonusData[x_value]);
                    }                   
                                    
                    
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true//值是否从0开始递增
                        }
                    }]
                }
            }
        }); 
        canvas.data("bar", myChart);
    }  
    
    //顯示Bonus的計算結果
    function showBonusResult(data) {
        $("#BudgetAllowance").html(data["BudgetAllowance"]);
        $("#PerfectScoring").html(data["PerfectScoring"]);
        $("#RatioOFM").html(data["RatioOFM"]);
        $("#RatioOFS").html(data["RatioOFS"]);
        $("#RatioOFP").html(data["RatioOFP"]);
        $("#ManagementS").html(data["ManagementS"]);
        $("#PerformanceS").html(data["PerformanceS"]);
        $("#QuarterWorkingDay").html(data["QuarterWorkingDay"]);
        $("#WorkingDay").html(data["WorkingDay"]);
        $("#ManagementRatio").html(data["ManagementRatio"]);
        $("#PerformanaceRatio").html(data["PerformanaceRatio"]);
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
    }
});  