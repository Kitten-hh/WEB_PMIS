$(function () {

    var searchfilter = ''
    var row1 = new SWRow()
    var contact = new SWCombobox("selectcontact", gettext("Contact"), window.CommonData.PartUserNames);
    contact.setHorizontalDisplay();
    row1.addComponent(contact);
    $("#Optiondiv").append(row1.dom);


    /** 第一個table */

    // var table1 = new SWDataTable("#AllDistictContact", "tableDistictContact"); //創建SWDataTable對象
    // table1.paging = false; //設置分頁顯示
    // table1.searching = false; //設置不顯示查詢框

    // //設置顯示字段
    // table1.columns = [
    //     { field: "alldistictsolution", label: "所有人Distinct Solution Type數量" },
    // ];
    // //SWDataTable控件不支持的功能，可以使用原生jquery datatable的屬性設置
    // table1.setOptions({
    //     responsive: true, //是否支持手機展開和隱藏列
    //     //隱藏的規則，responsivePriority值越大越先隱藏，width設置列寬度
    //     columnDefs: [
    //         { "responsivePriority": 1, "width": "45%", "targets": 0 },
    //     ]
    // });
    // table1.init('/looper/DailyPlanner/Alldistictsolution');


    /** 第二個table */


    var table2 = new SWDataTable("#AllContact", "tableAllContact"); //創建SWDataTable對象
    //table.pageLength = 20; //設置每頁顯示的數量為20
    table2.paging = false; //設置分頁顯示
    table2.searching = false; //設置不顯示查詢框

    table2.orderBy = [['contact','asc']]; //contact 排序
    //設置顯示字段
    table2.columns = [
        { field: "contact", label: gettext('Contact') },
        { field: "taskcount", label: gettext('Total Tasks') },
        { field: "solutioncount", label: gettext('Total Solution Type') },
        { field: "distictsolution", label: gettext('Distinct Solution Type Count') },
    ];
    //SWDataTable控件不支持的功能，可以使用原生jquery datatable的屬性設置
    table2.setOptions({
        responsive: true, //是否支持手機展開和隱藏列
        //隱藏的規則，responsivePriority值越大越先隱藏，width設置列寬度
        columnDefs: [
            { "responsivePriority": 1, "width": "45%", "targets": 0 },
            { "responsivePriority": 2, "targets": 1 },
        ]
    });
    table2.init('/looper/DailyPlanner/AllContactSolution');


    /** 第三個table */
    
    //在以上db_wapper控件中添加一個DataTable，生成的datatable的id為table1
    var table3 = new SWDataTable("#db_wapper", "Solutiondetailtable"); //創建SWDataTable對象
    //table.pageLength = 20; //設置每頁顯示的數量為20
    table3.paging = false; //設置分頁顯示
    table3.searching = false; //設置不顯示查詢框

    table3.orderBy = [['mindMaplabel','asc']]; //設置按taskno 升序排序
    //設置顯示字段
    table3.columns = [
        { field: "contact", label: gettext('Contact') },
        { field: "mindMaplabel", label: gettext('Solution Type') },
        { field: "Total", label: gettext('Solution Type Count') },
    ];
    $('#Solutiondetailtable').append('<tfoot><tr><th></th></tr></tfoot>')
    //SWDataTable控件不支持的功能，可以使用原生jquery datatable的屬性設置
    table3.setOptions({
        responsive: true, //是否支持手機展開和隱藏列
        //隱藏的規則，responsivePriority值越大越先隱藏，width設置列寬度
        columnDefs: [
            { "responsivePriority": 1, "targets": 0 },
            { "responsivePriority": 0, "width": "45%", "targets": 1 },
            { "responsivePriority": 2, "targets": 2 },
        ],
        "footerCallback": function( tfoot, data, start, end, display ) {
            var api = this.api();
            $(api.column(0).footer()).html("Total:");
            $(api.column(1).footer()).html(data.length);
            $( api.column(2).footer()).html(
                api.column(2).data().reduce( function ( a, b ) {
                    return a + b;
                }, 0 )
            );
        },
    });
    table3.init('/looper/DailyPlanner/AnalyseSolutionType');



    var test_search = new SWAdvancedsearch(".search_more"); //設置Search按鈕為觸發標籤
    var group = new SWAdvancedsearch.Group(SWAdvancedsearch.Condition.AND);
    var start_date = new SWAdvancedsearch.Rule("inputdate", SWAdvancedsearch.Type.DATE_TO_STR,
        SWAdvancedsearch.Operator.GREATER_OR_EQUAL, gettext('StartDate'))
    var end_date = new SWAdvancedsearch.Rule("inputdate", SWAdvancedsearch.Type.DATE_TO_STR,
        SWAdvancedsearch.Operator.LESS_OR_EQUAL, gettext('End Date'))
    group.addRowRule([start_date, end_date]);
    test_search.addGroup(group);
    test_search.on_search_event = function (filter) {
        searchfilter = ''
        if (filter != 'null') {
            var filter_obj = JSON.parse(filter);
            if(filter_obj['rules'].length !=2){
                var date = new Date()
                var nowdate=Date.parse(date).toString("yyyyMMdd")
                var enddate_filter = {"id":"inputdate","field":"inputdate","type":"string","input":"text","operator":"less_or_equal","value":nowdate}
                filter_obj['rules'].push(enddate_filter)
                filter = JSON.stringify(filter_obj)
            }
            getAllDistictContact(filter)
            $('#tableAllContact').DataTable().search('form-search:' + filter).draw();
            $('#Solutiondetailtable').DataTable().search('form-search:' + filter).columns(0).search('hb').draw();
            searchfilter = filter
        }
    }

    
    $("[name='selectcontact'] select").change(function () {
        if($("[name='selectcontact'] select").val()!=''){
            if (searchfilter!=''){
                $('#Solutiondetailtable').DataTable().search('form-search:' + searchfilter).columns(0).search($("[name='selectcontact'] select").val()).draw();
            }else{
                $('#Solutiondetailtable').DataTable().columns(0).search($("[name='selectcontact'] select").val()).draw();
            }
        }
    })

    $('#Optiondiv .col .input-group label').css("padding-right","10px");
    // $("#Optiondiv .col .input-group").width('10%');
    $('.todo-header').css("font-size","1.0rem");

    

    var thefilter = getthefilter()
     
    getAllDistictContact(thefilter)
    
});



function getAllDistictContact(filter){
    $.ajax({
        url: "/looper/DailyPlanner/Alldistictsolution",
        type: "GET",
        dataType: 'json',
        data: {'search[value]':'form-search:' + filter},
        cache: false,
        success: function (json) {
            if (json.status) {
                jsondata = json.data
                $('#AllDistictContact').text(jsondata[0].alldistictsolution)
            }
        }
    })
}



function getthefilter(){
    var date = new Date()
    var startdate=Date.parse(date).toString("yyyyMM")
    var nowdate=Date.parse(date).toString("yyyyMMdd")
    var thefilter = {'condition' : "AND",'not': false,'rules': [{id: "inputdate", field: "inputdate", type: "string", input: "text", operator: "greater_or_equal","value":startdate+'01'},
     {"id":"inputdate","field":"inputdate","type":"string","input":"text","operator":"less_or_equal","value":nowdate}],'valid': true}
    return JSON.stringify(thefilter)  
}


















