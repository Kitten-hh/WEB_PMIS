var gettext_viewGoal = gettext("View Goal");
var gettext_viewReport = gettext("View Report");
var gettext_viewCalendar = gettext("View Calendar");
var gettext_ganttView = gettext("Gantt View");

$(function () {
    var sea_user = new SWCombobox("user", gettext('Contact'), window.CommonData.PartUserNames, "sing");
    sea_user.setHorizontalDisplay();
    var today = new Date();
    var quarter = Math.floor((today.getMonth() + 3) / 3);
    var quarter_str = "{0}-{1}".format(today.toString("yyyy"), quarter);
    var sea_period = new SWCombobox("period", gettext('Period'), "/PMIS/goalmaster/get_all_period", quarter_str);
    sea_period.setHorizontalDisplay();
    $("#sea-container").prepend(sea_period.dom);
    $("#sea-container").prepend(sea_user.dom);
    var table = new SWDataTable("#goal_master_table", "table1"); //創建SWDataTable對象
    table.paging = false; //設置分頁顯示
    table.searching = false; //設置不顯示查詢框
    //設置DataTable顯示5個字段，分別是taskno, task,contact, planbdate, planedate
    table.columns = [
        { field: "recordid", label: gettext('RecordID') },
        { field: "period", label: gettext('Period') },
        { field: "contact", label: gettext('Contact') },
        { field: "objective", label: gettext('Project') },
        { field: "bdate", label: gettext('BDate'), render: SWDataTable.DateRender },
        { field: "edate", label: gettext('EDate'), render: SWDataTable.DateRender },
        { field: "pschedule", label: gettext('Plan Progress') },
        { field: "aschedule", label: gettext('Actual Progress') },
        {
            field: "operation", label: gettext('Operation'),
            render: function (data, type, row) {
                var id = row.DT_RowId;
                return `<button type="button" class="btn btn-sm" row_id='` + id + `' data-toggle="modal" data-target="#editModal">
                    <i class="fas fa-edit"></i></button>
                    <div class="dropdown d-inline-block">
                            <button type="button" class="btn btn-sm btn-hover-brand btn-elevate-hover" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"> <i class="fas fa-ellipsis-v"></i> </button>
                                <div class="dropdown-menu dropdown-menu-right" x-placement="bottom-end" style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(29px, 29px, 0px);">
                                    <a class="dropdown-item" href="/looper/goal/treelist?pk=`+ id + `"><i class="la la-plus"></i>` + gettext_viewGoal + `</a>
                                    <a class="dropdown-item" href="http://222.118.20.134:40010/s/34969?dc=false&id=`+ id + `"><i class="la la-plus"></i>` + gettext_viewReport + `</a>
                                    <a class="dropdown-item" href="/looper/goal/calendar?pk=` + id + `"><i class="la la-user"></i>` + gettext_viewCalendar + `</a>
                                    <a class="dropdown-item" href="/PMIS/looper_gantt?type=goal&id=` + id + `"><i class="la la-cloud-download"></i>` + gettext_ganttView + `</a>
                                </div>
                    </div>`;
            }
        }
    ];
    table.setOptions({
        responsive: true,
        deferLoading: 0,
        initComplete: function (settings) {
            self = this.api()
            $("#btnSearch").on("click", function () {
                var contact = sea_user.input_dom.val();
                var period = sea_period.input_dom.val();
                if (contact != '' && period != '')
                    self.columns(1).search(period).columns(2).search(contact).draw();
            });
            self.columns(1).search(quarter_str).columns(2).search("sing").draw();
        },
        columnDefs: [
            { "responsivePriority": 1, "targets": 0 },
            { "responsivePriority": 1, "width": "45%", "targets": 3 },
            { "responsivePriority": 2, "targets": 1 },
            { "responsivePriority": 3, "targets": 2 },
            { "responsivePriority": 5, "targets": 4 },
            { "responsivePriority": 6, "targets": 5 },
            { "responsivePriority": 7, "targets": 6 },
            { "responsivePriority": 8, "targets": 7 },
        ]
    })
    goal_table = table.init('/PMIS/goal/search'); //根據以上設置好的屬性，初始化table1，數據來源於/server/tasks這個地址  

    var form = new SWBaseForm("#editModal")
    form.update_url = "/PMIS/goalmaster/update?pk=[[pk]]";
    form.pk_in_url = false;
    form.on_after_save = function(data) {
        $("#editModal").modal("hide");
        $("#btnSearch").click();
    }
   

    //綁定事件
    $('#goal_master_table').on('click', 'button', function () {
        var id = $(this).attr('row_id');
        form.set_pk(id);
        form.init_data();
    });

    $("#allow_mutil_select").on("click", function () {
        var enabled = $(this).is(":checked");
        if (enabled)
            $('.datatable').DataTable().select.style('multi');
        else
            $('.datatable').DataTable().select.style('os');
    })
    $("#main_look_gantt").on('click', function () {
        var rows = $('.datatable').DataTable().rows({ selected: true }).data();
        var ids = ""
        for (var i = 0; i < rows.length; i++) {
            var row = rows[i];
            var id = data.DT_RowId;
            if (ids != "")
                ids += ";" + id;
            else
                ids = id;
        }
        if (ids != "")
            window.location = "/PMIS/Looper_gantt?type=goal&id=" + ids;
    })
    $("#goal_management").on("click", function(){
        var contact = sea_user.input_dom.val();
        var period = sea_period.input_dom.val();     
        if (contact == "" || period == "") {
            SWApp.popoverMsg(this,"请录入联系人和季度")
            return;
        }
        window.open("/looper/goal/overall/quarterly_goal?contact={0}&period={1}".format(contact, period), "goal");
    })
});