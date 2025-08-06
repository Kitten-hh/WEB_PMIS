$('title').html('BonusSimulationApp')

// //加載所有Task信息
var table = undefined

function get_Task() {
    var url = "/bonus/get_Tasts/?sort=" + sort;
    //Task预定义条件查询
    if (identifying == "query_search") {
        if (index == 4) {
            sort = "Edate";
        } else if (index == 0) {
            sort = "Contact";
        } else {
            sort = "RealTaskType";
        }
        url = "/bonus/task_enquiry/?query_filter_id=" + query_filter_id + "&sort=" + sort;
    }

    if (table != undefined) //不等于undefined就销毁当前table
        table.destroy();
    var groupColumn = index;
    $("#simple_datatable tbody").html("");//先清空在加载数据
    $("#simple_datatable thead").html("<tr><th style='width: 6%;'>Contact</th><th>TaskNo</th><th style='width: 15%;'>Task Description</th><th>Task Type</th><th>TaskType Description</th><th>Date</th><th>Score</th><th>Lookup Score</th><th>inc_id</th><th></th></tr>");
    table = $("#simple_datatable").DataTable({
        dom: `Z<'row'<'col-sm-12'tr>>`,
        serverSide: true,
        scrollX: false,
        responsive: true,
        ajax: {
            url: url
        },
        columns: [
            { name: "contact", data: "contact" },
            { name: "taskno", data: "taskno" },
            { name: "task", data: "task" },
            { name: "realtasktype", data: "realtasktype" },
            { name: "tasktypedesc", data: "tasktypedesc" },
            {
                data: "edate", //字段名稱
                //定義要處理的日期函數
                render: function ChangeDateFormat(value) {
                    var reg = /^\s*$/;
                    //返回值為true表示不是空字符串
                    if (value != null && value != undefined && !reg.test(value)) {
                        return formatTime(parseDjangoTime(value));
                    } else
                        return '';
                }
            },
            { name: "tasktypescore", data: "tasktypescore" },
            { name: "lookupscore", data: "lookupscore" },
            { name: "inc_id", data: "inc_id" },
            {
                data: null,
                "mRender": function (data, type, row, setting) {
                    return `<i class="fa fa-chevron-right"></i>`;
                }
            },

        ],
        "drawCallback": function (settings) {
            var api = this.api();
            var rows = api.rows({ page: 'current' }).nodes();
            var last = null;
            var sum = 0;
            var sum1 = 0;
            //var name = null;
            api.column(groupColumn, { page: 'current' }).data().each(function (group, i) {
                var client_btn = "<span class='client_span'><i style='color: white;'  class='fa fa-chevron-right'></i></span>";
                if (groupColumn == 0 || groupColumn == 3) {//联系人 和 Task类型需要分组
                    if (last !== group) {
                        if (groupColumn == 0) { //联系人需要统计分数
                            sum = 0;
                            sum1 = 0;
                            api.column(6, { page: 'current' }).data().each(function (score, i) {
                                if (group == api.column(0, { page: 'current' }).data()[i]) {
                                    sum += score;
                                }
                            });

                            api.column(7, { page: 'current' }).data().each(function (lookupscore, i) {
                                if (group == api.column(0, { page: 'current' }).data()[i]) {
                                    sum1 += lookupscore;
                                }
                            });
                            $(rows).eq(i).before(
                                '<tr class="group"><td style="display: block;"><div style="width: 200px">' + group + ' Score總分數為:' + sum +
                                ', LookupScore總分數為:' + sum1 + '</div></td><td align="right" colspan="9">' + client_btn + '</td></tr>'
                            );
                        } else {
                            $(rows).eq(i).before(
                                '<tr class="group"><td colspan="8">' + group + '</td></tr>'
                            );
                        }
                        last = group;
                    }
                }
            });
        }
    });
};

var index = 0;
sort = 'Contact';   //按時間排序
url = "/bonus/get_Tasts/?sort=" + sort;
var identifying = ""; //""==查詢Task、no Null==使用預定義條件查詢

var sum = [];
//var sum = {};
$.get(url, function (paraData) {
    var paradata = paraData.paraData;
    for (var index in paradata) {
        sum.push(paradata[index].fvalue)
    }
    //console.log(sum) //sum["30","11","70","11","100","100","10000" ]
    BudgetAllowance = parseFloat(sum[0])  // 30
    RatioOFM = parseFloat(sum[1])  // 11 
    RatioOFS = parseFloat(sum[2])  // 70
    RatioOFP = parseFloat(sum[3])  // 11
    ManagementRatio = parseFloat(sum[4])  //100
    PerformanaceRatio = parseFloat(sum[5]) // 100
    Salary = parseFloat(sum[6]) //10000
});

function sysparaBonus(Workdates, sum, sum1) {
    bonusarr = new Array();
    bonusarr[0] = PerfectScoring = Salary * (1 + BudgetAllowance / 100) * 3 / 2;
    bonusarr[1] = ManagementS = PerfectScoring * RatioOFM / 100;
    bonusarr[2] = PerformanceS = PerfectScoring * RatioOFP / 100;
    bonusarr[3] = SuggAvg = parseFloat((PerfectScoring - ManagementS - PerformanceS) / Workdates).toFixed(2);
    bonusarr[4] = SimulateScore = parseFloat(SuggAvg * Workdates + ManagementS + PerformanceS).toFixed(2);
    bonusarr[5] = Simulate$permth = parseFloat((SuggAvg * Workdates + ManagementRatio * ManagementS / 100 + PerformanaceRatio * PerformanceS / 100) * 2 / 3).toFixed(2);
    bonusarr[6] = scorePara = sum / 5 * Workdates + ManagementS + PerformanceS;
    bonusarr[7] = scoreBonus = scorePara - Salary * 3 / 2;
    bonusarr[8] = scoreActual = parseFloat(Salary * 3 / 2 + scoreBonus).toFixed(2);
    bonusarr[9] = lookuppara = sum1 / 5 * Workdates + ManagementS + PerformanceS;
    bonusarr[10] = lookupBonus = lookuppara - Salary * 3 / 2;
    bonusarr[11] = lookupActual = parseFloat(Salary * 3 / 2 + lookupBonus).toFixed(2);
    bonusarr[12] = Actpermth = parseFloat(scoreActual * 3 / 2).toFixed(2);

    return bonusarr;
}

//get_Task();           //默认通过时间排序條件為降序，查询Task信息

// // 各種分組排序Task
$("#kt_footer a").click(function () {
    var condition = $(this).text().replace(/^\s+|\s+$/g, "");
    if (condition == "DateGroup") {
        index = 5;
        sort = 'EDate';
        if (query_filter_id != "") {//query_filter_id不等于空就查询预定义条件的数据
            identifying = "query_search";
        }
        $("#simple_datatable").removeClass("hide_taskType"); //removeClass
        $("#simple_datatable").removeClass("hide_Contact");
    }
    if (condition == "ContactGroup") {
        index = 0;
        sort = 'Contact';
        if (query_filter_id != "") {
            identifying = "query_search";
        }
        $("#simple_datatable").addClass("hide_Contact");
        $("#simple_datatable").removeClass("hide_taskType");
    }
    if (condition == "TaskTypeGroup") {
        index = 3;
        sort = 'TaskType';
        if (query_filter_id != "") {
            identifying = "query_search";
        }
        $("#simple_datatable").addClass("hide_taskType");
        $("#simple_datatable").removeClass("hide_Contact");
    }
    get_Task();
});

// 聯繫人明細
$("#simple_datatable").on('click', '.client_span', function () {
    var contact_name = $(this).parents("tr").next().find("td").eq(0).text();
    window.location.href = '/bonus/get_Contact_Details/?contact_name=' + contact_name;
});


//查询功能,填充下拉框
$("#query_search").on("click", function () {
    var filter_val = $("#template-users").val();
    var is_dialy = $("#IsDaily").is(":checked") ? "Y" : "N";
    $.ajax({
        url: "/bonus/query/search/",
        data: { filter: filter_val, is_dialy: is_dialy },
        success: function (data) {
            var result = eval(data);
            var html = "";
            for (query of result.data) {
                html += '<li><a class="dropdown-item" id="' + query.qf025 + '" href="#">' + query.qf003 + '</a></li>';
                html += ' <li class="divider"></li>';
            }
            $("#queryfilter_dropdown_menu").html(html);
        },
        fail: function (data) {
            $("#queryfilter_dropdown_menu").html("");
        }
    })
})

var query_filter_id = "";
$("#queryfilter_dropdown_menu").on("click", ".dropdown-item", function () {
    $('#query_search').dropdown('toggle');

    query_filter_id = $(this).attr("id");
    identifying = "query_search";
    get_Task(index, identifying);
    if (index == 1) {
        $("#simple_datatable").addClass("hide_Contact");
        $("#simple_datatable").removeClass("hide_taskType");
    } else if (index == 2) {
        $("#simple_datatable").addClass("hide_taskType");
        $("#simple_datatable").removeClass("hide_Contact");
    }
    return false;
})

$("#task_search_box").click(function () {
    $(this).hide();
    $("#task_search_box").show();

})

$("#prev_page").click(function () {
    history.go(-1);
})

// 點擊任務數據跳轉詳細信息
$(".page").on('click', '.odd,.even', function () {
    var inc_id = $(this).find("td").eq(7).text();
    if (query_filter_id != "") {
        window.location.href = '/bonus/get_Task_Details/?inc_id=' + inc_id + "&query_filter_id=" + query_filter_id;
    } else {
        window.location.href = '/bonus/get_Task_Details/?inc_id=' + inc_id;
    }
});

//searchdate模态框搜索按钮
$("#searchdate").on('click', function () {
    
    var contact = $("#contact").val();
    var edateOne = $("#edateOne").val();
    var edateTwo = $("#edateTwo").val();
    if(contact==''){
        alert("請輸入聯繫人");
        return;
    }
    if(edateOne=='' || edateTwo==''){
        alert("請選擇時間範圍");
        return;
    }  

    if ($('.fade').css('display') == "none") {
        $('.fade').show();
    } else {
        $('.fade').hide();
    }
    $.ajax({
        url: "/bonus/query/searchdate/",
        data: { 'contact': contact, 'edateOne': edateOne, 'edateTwo': edateTwo },
        type: 'GET',
        dataType: 'json',
        cache: false,
        success: function (data) {
            var table_data = data;
            var groupColumn = index;
            table = $("#simple_datatable").DataTable({
                dom: `Z<'row'<'col-sm-12'tr>>`,
                serverSide: false,
                scrollX: false,
                responsive: true,
                ordering: false,
                pageLength: 100,
                data: table_data,
                destroy: true,
                columns: [
                    { name: "contact", data: "contact" },
                    { name: "taskno", data: "taskno" },
                    { name: "task", data: "task" },
                    { name: "realtasktype", data: "realtasktype" },
                    { name: "tasktypedesc", data: "tasktypedesc" },
                    {
                        data: "edate", //字段名稱
                        //定義要處理的日期函數
                        render: function ChangeDateFormat(value) {
                            var reg = /^\s*$/;
                            //返回值為true表示不是空字符串
                            if (value != null && value != undefined && !reg.test(value)) {
                                return formatTime(parseDjangoTime(value));
                            } else
                                return '';
                        }
                    },
                    { name: "tasktypescore", data: "tasktypescore" },
                    { name: "lookupscore", data: "lookupscore" },
                    { name: "inc_id", data: "inc_id" },
                    {
                        data: null,
                        "mRender": function (data, type, row, setting) {
                            return `<i class="fa fa-chevron-right"></i>`;
                        }
                    },

                ],
                "drawCallback": function (settings) {
                    var api = this.api();
                    var rows = api.rows({ page: 'current' }).nodes();
                    var last = null;
                    var sum = 0;
                    var sum1 = 0;
                    //var name = null;

                    api.column(groupColumn, { page: 'current' }).data().each(function (group, i) {
                        var client_btn = "<span class='client_span'><i style='color: white;'  class='fa fa-chevron-right'></i></span>";
                        if (groupColumn == 0 || groupColumn == 3) {//联系人 和 Task类型需要分组
                            if (last !== group) {
                                if (groupColumn == 0) { //联系人需要统计分数
                                    sum = 0;
                                    var startTime = new Date(Date.parse(edateOne.replace(/-/g, "/")));
                                    var endTime = new Date(Date.parse(edateTwo.replace(/-/g, "/")));

                                    var desc = Math.abs((startTime - endTime)) / (1000 * 60 * 60 * 24) + 1;
                                    var count = 0;
                                    var datetime = startTime < endTime ? startTime : endTime
                                    for (var j = 0; j < desc; j++) {
                                        var when = new Date(datetime.getFullYear(), datetime.getMonth(), datetime.getDate() + j);
                                        if (when.getDay() == 0) {
                                            count++;
                                        }
                                    }
                                    var Workdates = desc - count;

                                    api.column(6, { page: 'current' }).data().each(function (score, i) {
                                        if (group == api.column(0, { page: 'current' }).data()[i]) {
                                            sum += score;
                                        }
                                    });

                                    api.column(7, { page: 'current' }).data().each(function (lookupscore, i) {
                                        if (group == api.column(0, { page: 'current' }).data()[i]) {
                                            sum1 += lookupscore;
                                        }
                                    });
                                    sysparaBonus(Workdates, sum, sum1);
                                    let innHTML = '';

                                    innHTML += '<tr class="group"><td style="display: none;"><div></div></td><td colspan="3"><div>' + group + '</div><div>' + 'Score總分數為: ' + sum + '</div><div style="position: relative;margin-top: -20px;left: 230px;">' + 'S Score for the quarter.S的值: ' + bonusarr[6] + '</div><div style="position: relative;margin-top: -20px;left: 550px;">' + 'ScoreBonus的值: ' + bonusarr[7] +
                                        '</div><div style="position: relative;margin-top: 10px;">' + 'LookupScore總分數為: ' + sum1 + '</div><div style="position: relative;margin-top: -20px;left: 230px;">' + 'S LookupScore for the quarter.S的值: ' + bonusarr[9] + '</div><div style="position: relative;margin-top: -20px;left: 550px;">' + 'LookupBonus的值: ' + bonusarr[10] +
                                        '</div><div style="position: relative;margin-top: 10px;">' + 'PerfectScoring值为: ' + bonusarr[0] + '</div><div style="position: relative;margin-top: -20px;left: 230px;">' + 'Sugg.Avg的值: ' + bonusarr[3] + '</div><div style="position: relative;margin-top: -20px;left: 550px;">' + 'Simulate Score的值: ' + bonusarr[4] +
                                        '</div><div style="position: relative;margin-top: 10px;">' + 'Simulate$permth的值: ' + bonusarr[5] + '</div><div style="position: relative;margin-top: -20px;left: 230px;">' + 'Act in $ per mth的值: ' + bonusarr[12] + '</div></td><td align="right" colspan="7">' + client_btn + '</td></tr>'

                                    $(rows).eq(i).before(innHTML);
                                    
                                } else {
                                    $(rows).eq(i).before(
                                        '<tr class="group"><td colspan="7">' + group + '</td></tr>'
                                    );
                                }
                                last = group;
                            }
                        }
                        if (groupColumn == 5) {
                            if (last !== group) {

                            }
                        }
                    });
                }
            })

        },
        fail: function (data) {
            $("#simple_datatable").html("");
        }
    })
})

$("#dropdownbar .bartype").on('click',function(){
    if ($('.bartype').css('display') == "none") {
        $('.bartype').show();
    } else {
        $('.bartype').hide();
    }
})

// $(".container [data-toggle='popover']").on("shown.bs.popover", function () {
//     var canv = document.createElement("canvas");
//     canv.setAttribute('width', 100);
//     canv.setAttribute('height', 100);
//     canv.setAttribute("id", "myChart");
//     document.body.appendChild($(".search-content")[0]);
//     canvas = $(canv);
//     var ctx = canv.getContext("2d");
//     var oldBar = canvas.data("bar");
//     if (oldBar != undefined)
//         oldBar.destroy();
//     var myChart = new Chart(ctx, {
//         type: 'bar',
//         data: {
//             labels: ['qfq', 'hb', 'czz', 'Green', 'Purple', 'Orange'],
//             datasets: [{
//                 //label: '# of Votes',
//                 data: [120, 190, 30, 50, 20, 30],
//                 backgroundColor: [
//                     'rgba(255, 99, 132, 0.2)',
//                     'rgba(54, 162, 235, 0.2)',
//                     'rgba(255, 206, 86, 0.2)',
//                     'rgba(75, 192, 192, 0.2)',
//                     'rgba(153, 102, 255, 0.2)',
//                     'rgba(255, 159, 64, 0.2)'
//                 ],
//                 borderColor: [
//                     'rgba(255, 99, 132, 1)',
//                     'rgba(54, 162, 235, 1)',
//                     'rgba(255, 206, 86, 1)',
//                     'rgba(75, 192, 192, 1)',
//                     'rgba(153, 102, 255, 1)',
//                     'rgba(255, 159, 64, 1)'
//                 ],
//                 borderWidth: 1
//             }]
//         },
//         options: {
//             scales: {
//                 yAxes: [{
//                     ticks: {
//                         beginAtZero: true
//                     }
//                 }]
//             }
//         }
//     });
//     canvas.data("bar", myChart);
// });

$('.btn-success').html('DateGroup') // button1
$('.btn-light-danger').html('ContactGroup') // button2
$('.btn-light-primary').html('TaskTypeGroup') // button3

// //隔行变色
// // if (skin == "default") {
// //     $("#simple_datatable").addClass("change_color");
// // } else {
// //     $("#simple_datatable").removeClass("change_color");
// // }


