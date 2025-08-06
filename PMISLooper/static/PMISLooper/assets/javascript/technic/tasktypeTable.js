$(function () {
   

    //在以上db_wapper控件中添加一個DataTable，生成的datatable的id為table1
    var table = new SWDataTable("#db_wapper", "table1"); //創建SWDataTable對象
    //table.pageLength = 20; //設置每頁顯示的數量為20
    table.paging = false; //設置分頁顯示
    table.searching = false; //設置不顯示查詢框

    table.orderBy = [['realtasktype']]; //設置按taskno 升序排序
    //設置顯示字段
    table.columns = [
        { field: "realtasktype", label: gettext('Real Task Type') },
        { field: "subtasktypedesc", label: gettext('Task Type') },
        { field: "Total", label: gettext('Task Type Count') },
    ];
    //SWDataTable控件不支持的功能，可以使用原生jquery datatable的屬性設置
    table.setOptions({
        //responsive: true, //是否支持手機展開和隱藏列
        //隱藏的規則，responsivePriority值越大越先隱藏，width設置列寬度
        columnDefs: [
            { "responsivePriority": 1, "targets": 0 },
            { "responsivePriority": 2, "width": "45%", "targets": 2 },
            { "responsivePriority": 2, "targets": 2 },
        ]
    });
    table.init('/looper/DailyPlanner/AnalyseTaskType');


    var test_search = new SWAdvancedsearch(".search_more"); //設置Search按鈕為觸發標籤
    var group = new SWAdvancedsearch.Group(SWAdvancedsearch.Condition.AND);
    var username = new SWAdvancedsearch.Rule("contact", SWAdvancedsearch.Type.STRING,
        SWAdvancedsearch.Operator.EQUAL, gettext('Contact'));
    group.addRule(username);
    var start_date = new SWAdvancedsearch.Rule("inputdate", SWAdvancedsearch.Type.DATE,
        SWAdvancedsearch.Operator.GREATER_OR_EQUAL, gettext('StartDate'))
    var end_date = new SWAdvancedsearch.Rule("inputdate", SWAdvancedsearch.Type.DATE,
        SWAdvancedsearch.Operator.LESS_OR_EQUAL, gettext('End Date'))
    group.addRowRule([start_date, end_date]);
    test_search.addGroup(group);
    test_search.on_search_event = function (filter) {
        $('#table1').DataTable().search('form-search:' + filter).draw();
    }

});