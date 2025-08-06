$(function () {
   

    //在以上db_wapper控件中添加一個DataTable，生成的datatable的id為table1
    var table = new SWDataTable("#db_wapper", "DailyPlannerTable"); //創建SWDataTable對象
    //table.pageLength = 20; //設置每頁顯示的數量為20
    table.paging = false; //設置分頁顯示
    table.searching = false; //設置不顯示查詢框

    table.orderBy = [['inputdate','desc']] //設置按taskno 升序排序

    //設置顯示字段
    table.columns = [
        { field: "contact", label: gettext('Contact') },
        { field: "inputdate", label: gettext('Input Date') },
        { field: "taskno", label: gettext('Task ID') },
        { field: "taskdescription", label: gettext('Task Description') },
        { field: "abnormal", label: gettext('Abnormal') },
        { field: "inc_id", label: "inc_id",'visible':false},
    ];


    //SWDataTable控件不支持的功能，可以使用原生jquery datatable的屬性設置
    table.setOptions({
        responsive: true, //是否支持手機展開和隱藏列
        //隱藏的規則，responsivePriority值越大越先隱藏，width設置列寬度
        columnDefs: [
            { "responsivePriority": 1,"className":"all", "targets": 0 },
            { "responsivePriority": 1,"className":"all","targets": 1 },
            { "responsivePriority": 2,"className":"min-tablet-p","targets": 2 },
            { "responsivePriority": 3,"className":"min-tablet-p","targets": 3 },
            { "responsivePriority": 4,"className":"min-tablet-p","width": "45%", "targets": 4 },
            { "responsivePriority": 5,"className":"min-tablet-p","targets": 5 },
        ]
    });


    table.init('/looper/DailyPlanner/AnalyseDailyPlanner');


    $('#DailyPlannerTable tbody').on('dblclick', 'tr', function () {
        var tabledata = $('#DailyPlannerTable').DataTable().row(this).data()
        var inc_id = tabledata['inc_id']
        var contact = tabledata['contact']
        var inputdate = tabledata['inputdate']
        var url = `/looper/technic/selectdailyplanner?inc_id=${inc_id}&contact=${contact}&inputdate=${inputdate}`
        window.open(url)
        // window.open("/looper/technic/technical_statement?pk="+inc_id)
    })


});