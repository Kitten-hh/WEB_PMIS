var PageUI = function () {
    this.all_question_table = undefined;
    this.all_question_datatable = undefined;
    this.session_question_table = undefined;
    this.session_question_datatable = undefined;
    this.session_question_params_fun = undefined;
    this.session_list_cmpt = undefined;
    this.Questions = undefined
    this.quesyion_adv_search_btn = undefined;
    this.question_query = undefined;
    var self = this;
    this.init = function () {
        //self.init_all_question();
        //self.init_session_question();
        self.Questions = new Questions();
        self.Questions.init();
        self.Questions.init_technical_table();
        self.bind_event();

    }

    this.init_advenced_query_question = function () {
        self.question_query = new SWAdvancedsearch(self.quesyion_adv_search_btn); //設置Search按鈕為觸發標籤
        var group = new SWAdvancedsearch.Group(SWAdvancedsearch.Condition.AND);
        var taskno = new SWAdvancedsearch.Rule("taskno", SWAdvancedsearch.Type.STRING,
            SWAdvancedsearch.Operator.CONTAINS, gettext('TaskID'));
        var task = new SWAdvancedsearch.Rule("task", SWAdvancedsearch.Type.STRING,
            SWAdvancedsearch.Operator.CONTAINS, gettext('Task Description'));
        var contact = new SWAdvancedsearch.Rule("contact", SWAdvancedsearch.Type.STRING,
            SWAdvancedsearch.Operator.CONTAINS, gettext('Contact'));
        var planbcdate = new SWAdvancedsearch.Rule("createdate", SWAdvancedsearch.Type.DATE,
            SWAdvancedsearch.Operator.GREATER_OR_EQUAL, gettext('Create Date(before)'));
        var planbedate = new SWAdvancedsearch.Rule("createdate", SWAdvancedsearch.Type.DATE,
            SWAdvancedsearch.Operator.LESS_OR_EQUAL, gettext('Create Date(after)'));
        var cdate = new SWAdvancedsearch.Rule("edate", SWAdvancedsearch.Type.DATE,
            SWAdvancedsearch.Operator.GREATER_OR_EQUAL, gettext('Actual EDate(before)'));
        var edate = new SWAdvancedsearch.Rule("edate", SWAdvancedsearch.Type.DATE,
            SWAdvancedsearch.Operator.LESS_OR_EQUAL, gettext('Actual EDate(after)'));
        var progress = new SWAdvancedsearch.Rule("progress", SWAdvancedsearch.Type.STRING,
            SWAdvancedsearch.Operator.CONTAINS, gettext('Progress'));
        group.addRule(taskno);
        group.addRule(task);
        group.addRule(contact);
        group.addRowRule([planbcdate, planbedate])
        group.addRowRule([cdate, edate]);
        group.addRule(progress);
        self.question_query.addGroup(group);
        self.question_query.on_search_event = function (filter) {
            self.all_question_datatable.search('form-search:' + filter).draw();
            $('#all_question_table_filter input[type="search"]').val('')
            $("#SWAdvancedsearch-Modal-2 .modal-body input").val("");
        }
    }
    this.init_session_list = function () {
        var session_list_datasource = []
        $("#stacked-menu .menu-item[sessionid]").each((index, item) => {
            var sessionid = $(item).attr("sessionid");
            var session_desc = $(item).find(".menu-text").text();
            session_list_datasource.push({ value: sessionid, label: session_desc });
        });

        self.session_list_cmpt = new SWCombobox("session_list", gettext("Session"), session_list_datasource);
        self.session_list_cmpt.setHorizontalDisplay();
        $("#session_question .session_list").append(self.session_list_cmpt.dom);
        self.session_list_cmpt.input_dom.on("change", function () {
            var sessionid = $(this).val();
            self.session_question_params_fun = function () {
                return {
                    attach_query: `{"condition":"AND","rules":[{"id":"pid","field":"pid","type":"string","input":"text","operator":"equal","value":"00500"},
                {"id":"tid","field":"tid","type":"double","input":"text","operator":"equal","value":95},
                {"id":"relationid","field":"relationid","type":"string","input":"text","operator":"equal","value":"${sessionid}"}],"not":false,"valid":true}`
                };
            }
            self.session_question_datatable.search('').draw();
        });
    }
    this.init_all_question = function () {
        var table = new SWDataTable("#all_question", "all_question_table"); //創建SWDataTable對象
        table.pageLength = 10;   //設置每頁顯示的數量為20

        table.paging = true;   //設置分頁顯示

        table.searching = true;  //設置不顯示查詢框

        table.orderBy = [['taskid', 'desc']];     //設置按taskno 升序排序，可以進行多字段排序，參考上面的重要屬性

        //設置DataTable顯示5個字段，分別是taskno, task,contact, planbdate, planedate
        table.columns = [
            { field: "taskno", label: gettext('TaskID') },
            { field: "task", label: gettext('Task Description') },
            { field: "contact", label: gettext('Contact') },
            { field: "createdate", label: gettext('Create Date'), render: SWDataTable.DateRender },
            {
                field: "edate", label: gettext('Actual EDate'), render: //SWDataTable.DateRender 
                    function (data) {
                        if (data === null) return "";
                        date_data = data.match(/(\d){4}-(\d){2}-(\d){2}/)[0]
                        return date_data;
                    }
            },
            { field: "progress", label: gettext('Progress') },
            { field: "taskid", label: "TaskId", visible: false }
        ];
        //SWDataTable控件不支持的功能，可以使用原生jquery datatable的屬性設置
        var task_width = SWApp.os.isMobile ? "60%" : "35%"
        table.setOptions({
            responsive: true,  //是否支持手機展開和隱藏列
            columnDefs: [
                { "responsivePriority": 1, "className": "all", "targets": 0 },
                { "responsivePriority": 1, "className": "all", "width": task_width, "targets": 1 },
                { "responsivePriority": 2, "className": "desktop", "targets": 2 },
                { "responsivePriority": 3, "className": "desktop", "targets": 3 },
                { "responsivePriority": 4, "className": "desktop", "targets": 4 },
                { "responsivePriority": 5, "className": "desktop", "targets": 5 },
            ]
        });
        table.custom_params_fun = function () {
            return {
                attach_query: `{"condition":"AND","rules":[{"id":"pid","field":"pid","type":"string","input":"text","operator":"equal","value":"00500"},
                {"id":"tid","field":"tid","type":"double","input":"text","operator":"equal","value":95}],"not":false,"valid":true}`};
        }
        self.all_question_table = table
        self.all_question_datatable = table.init('/PMIS/task/t_list');  //根據以上設置好的屬性，初始化table1，數據來源於/server/tasks這個地址
        self.quesyion_adv_search_btn = $('<button class="btn btn-sm btn-outline-primary search_more" style="margin-left:20px"><i class="fa fa-search mr-1"></i>' + gettext("Search") + '</button>');
        if (SWApp.os.isMobile || SWApp.os.isTablet)
            self.quesyion_adv_search_btn = $('<button class="btn btn-sm btn-outline-primary search_more ml-1"><i class="fa fa-search"></i></button>');
        $('#all_question_table_filter').append(self.quesyion_adv_search_btn)
        $("#all_question_table_info").parent().removeClass("col-md-5").addClass("col-xl-4");
        $("#all_question_table_paginate").parent().removeClass("col-md-7").addClass("col-xl-8 dataTables_pager");

    }
    this.init_session_question = function () {
        var table = new SWDataTable("#session_question_table", "session_question_table1"); //創建SWDataTable對象
        table.pageLength = 10;   //設置每頁顯示的數量為20

        table.paging = true;   //設置分頁顯示

        table.searching = false;  //設置不顯示查詢框

        table.orderBy = [['taskid', 'desc']];     //設置按taskno 升序排序，可以進行多字段排序，參考上面的重要屬性

        //設置DataTable顯示5個字段，分別是taskno, task,contact, planbdate, planedate
        table.columns = [
            { field: "taskno", label: gettext('TaskID') },
            { field: "task", label: gettext('Task Description') },
            { field: "contact", label: gettext('Contact') },
            { field: "planbdate", label: gettext('PlanBDate'), render: SWDataTable.DateRender },
            { field: "edate", label: gettext('Actual EDate'), render: SWDataTable.DateRender },
            { field: "progress", label: gettext('Progress') },
            { field: "taskid", label: "TaskId", visible: false }
        ];
        //SWDataTable控件不支持的功能，可以使用原生jquery datatable的屬性設置
        var task_width = SWApp.os.isMobile ? "60%" : "35%"
        table.setOptions({
            responsive: true,  //是否支持手機展開和隱藏列
            columnDefs: [
                { "responsivePriority": 1, "className": "all", "targets": 0 },
                { "responsivePriority": 1, "className": "all", "width": task_width, "targets": 1 },
                { "responsivePriority": 2, "className": "min-tablet-p", "targets": 2 },
                { "responsivePriority": 3, "className": "min-tablet-p", "targets": 3 },
                { "responsivePriority": 4, "className": "min-tablet-p", "targets": 4 },
                { "responsivePriority": 5, "className": "min-tablet-p", "targets": 5 },
            ],
            deferLoading: 0
        });
        table.custom_params_fun = function () {
            if (self.session_question_params_fun != undefined)
                return self.session_question_params_fun();
            else
                return {
                    attach_query: `{"condition":"AND","rules":[{"id":"pid","field":"pid","type":"string","input":"text","operator":"equal","value":"00500"},
                    {"id":"tid","field":"tid","type":"double","input":"text","operator":"equal","value":95}],"not":false,"valid":true}`};
        }
        self.session_question_table = table
        self.session_question_datatable = table.init('/PMIS/task/t_list');  //根據以上設置好的屬性，初始化table1，數據來源於/server/tasks這個地址         
    }
    this.bind_event = function () {
        $('#all_question').on('dblclick', '#all_question_table tbody tr', function () {
            var data = self.all_question_datatable.row(this).data();
            var pk = data.DT_RowId;
            init_task(pk);
        });
        $('#session_question_table').on('dblclick', '#session_question_table1 tbody tr', function () {
            var data = self.session_question_datatable.row(this).data();
            var pk = data.DT_RowId;
            init_task(pk);
        });
        $('.question_container .tab-menu .nav-tabs a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
            var tab = $(this).attr("href");
            if (tab == "#Question_List") {
                if ($("#Question_List").is(":visible")) {
                    if (self.all_question_table == undefined) {
                        self.init_all_question();
                        self.init_advenced_query_question();
                    }
                    if (self.session_question_table == undefined) {
                        self.init_session_question();
                        //默認選中第一個
                        var first_session = $("#stacked-menu .menu-item[sessionid]:first").attr("sessionid");
                        self.session_list_cmpt.input_dom.val(first_session);
                        self.session_list_cmpt.input_dom.selectpicker('refresh')
                        self.session_list_cmpt.input_dom.siblings(".dropdown-menu").prepend($("<div class=\"dropdown-arrow\"></div>"));
                        self.session_list_cmpt.input_dom.change();
                    }
                }
            }
        });
    }
}
$(function () {
    var UI = new PageUI();
    UI.init();

    window.update_menu_href = function () {
        window.update_session_url();
        UI.init_session_list();
    }
});