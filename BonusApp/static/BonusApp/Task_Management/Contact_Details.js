var query_filter_id = getParam("query_filter_id");  //獲取query_filter_id如果為空就通過聯繫人查看當月的Task，否則按預定義條件查詢
var contactName = getParam("contact_name");         //獲取聯繫人查詢Task信息
var Contact_DetailsVM = new Vue({
    el: ".main",
    data: {
        Contact: {},
    },
    methods: {
        get_Contact: function () {
            $.ajax({
                url: '/bonus/get_Contact_Details/',
                type: 'GET',
                data: { contact_name: getParam("contact_name") },
                dataType: 'json',
                cache: false,
                success: function (json) {
                    var data = json.data;
                    Contact_DetailsVM.Contact = data;
                }
            })
        },
        get_Task: function () {
            $(function () {
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
                        { name: "taskno", data: "taskno" },
                        { name: "task", data: "task" },
                        { name: "realtasktype", data: "realtasktype" },
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

                    ], "drawCallback": function (settings) {
                        $("#count").text("Related Task[Users](" + $("#simple_datatable tbody tr").length + ")");
                    }
                });
            })

        }
    },
    created: function () {
        this.get_Contact();
        this.get_Task();
    }
})



// 點擊任務數據跳轉詳細信息
$("#app-main").on('click', '.odd,.even', function () {
    var inc_id = $(this).find("td").eq(6).text();
    if (query_filter_id != undefined) {
        window.location.href = '/bonus/get_Task_Details/?inc_id=' + inc_id + "&query_filter_id=" + query_filter_id;
    } else {
        window.location.href = '/bonus/get_Task_Details/?inc_id=' + inc_id;
    }
});


// 點擊view
$("#view_contact").click(function () {
    if (query_filter_id != undefined) {
        window.location.href = '/bonus/get_Task_List/?contact_name=' + contactName + '&query_filter_id=' + query_filter_id;
    } else {
        window.location.href = '/bonus/get_Task_List/?contact_name=' + contactName;
    }
})


$("#prev_page").click(function () {
    history.go(-1);
})






