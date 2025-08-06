// 加載指定聯繫人下的Task數據
var query_filter_id = getParam("query_filter_id");
function get_Task_List() {
    var contactName = getParam("contact_name");
    var url = "/bonus/get_Task_List?contact_name=" + contactName
    if (query_filter_id != undefined) {
        url = "/bonus/get_Task_List?contact_name=" + contactName + "&query_filter_id=" + query_filter_id
    }

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
            { name: "tasktypedesc", data: "tasktypedesc"},
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
        ]
    });
};


get_Task_List();


$("#prev_page").click(function () {
    history.go(-1);
})


// 點擊任務數據跳轉詳細信息
$("#app-main").on('click', '.odd,.even', function () {
    var inc_id = $(this).find("td").eq(7).text();
    if (query_filter_id != undefined) {
        window.location.href = '/bonus/get_Task_Details/?inc_id=' + inc_id + "&query_filter_id=" + query_filter_id;
    } else {
        window.location.href = '/bonus/get_Task_Details/?inc_id=' + inc_id;
    }
});

