var gettext_addCourse = gettext("Add Course");
var gettext_addSolution = gettext("Add Solution");

var PageUI = function () {
    this.course_table = undefined
    this.course_datatable = undefined
    this.course_add_btn = undefined;
    this.solution_table = undefined;
    this.solution_datatable = undefined;
    this.course_task_table = undefined;
    this.course_task_datatable = undefined;    
    this.solution_add_btn = undefined;
    this.edit_form = undefined;
    this.solution_edit_form = undefined;
    this.mindmap_browser = undefined;
    this.course_adv_search_btn = undefined;
    var self = this;
    this.init = function () {
        this.init_course_edit_form();
        this.init_solution_edit_form();
        this.init_course_table();
        this.init_course_advenced_search_dialog();
        this.init_solution_table();
        this.bind_event();
        $("#myDiagramDiv").css("height","60vh")
        self.mindmap_browser = new SWMindmapBrowse("#Mindmap");
        self.mindmap_browser.beforeLoadMindmap = function(mindmap){
            var input_val = $('#course_table1_filter input[type="search"].form-control-sm').val()
            let pattern = /^[A-Za-z]{3}-[A-Za-z]{3}-\d{5}$/; //文檔編號的形式
            if (!pattern.test(input_val)) return; //不匹配則退出
            var load_data = JSON.parse(mindmap.node_data).nodeDataArray;
            for (key in load_data) {
                if (load_data[key]['text'].toUpperCase().indexOf(input_val.toUpperCase()) != -1) {
                    load_data[0] = load_data[key];
                    break;
                }
            }
            var data_key = load_data[0].key;
            var key_sel = mindmap.myDiagram.model.findNodeDataForKey(data_key);
            var node_da = mindmap.myDiagram.findNodeForData(key_sel);
            mindmap.myDiagram.select(node_da);
            mindmap.myDiagram.centerRect(node_da.actualBounds);
        }
        $("#course_table1_filter .search_more").insertAfter("#course_table1_wrapper #add_course")
    }
    this.init_solution_edit_form = function () {
        let form1 = new SWForm("#edit_solution .modal-body", "", "url", "GET", false);
        form1.addComponent(new SWText("stid", "hidden"));
        form1.addComponent(new SWText("courseref", "hidden"));
        form1.addComponent(new SWTextarea("sdescription", gettext('Description')).setAutoSize(true));
        form1.addComponent(new SWCombobox("contact", gettext('Contact'), window.CommonData.PartUserNames))
        form1.addComponent(new SWText("mindmapid", "text", gettext('MindmapId')));
        form1.create_url = "/devplat/solution/create";
        form1.update_url = "/devplat/solution/update?pk=[[pk]]";
        form1.pk_in_url = false;
        form1.dom.find(".card-header").hide();
        form1.dom.find(".card-footer").hide();
        form1.dom.find(".page-inner").addClass("p-0");
        form1.on_after_save = function (data) {
            $("#edit_solution").modal("hide");
            self.solution_datatable.search("").draw();
        }
        form1.on_init_format = function(data) {
            if (data.courseref == undefined)
                data.courseref = $("#solution_table").data("courseid");
        }
        form1.on_after_init = function (data) {
            $("#edit_solution textarea").trigger("change");
        }
        self.solution_edit_form = form1;
        $("#edit_solution #new_save").on("click", function () {
            self.solution_edit_form.dom.find(".save").click();
        });
    }
    this.init_course_edit_form = function () {
        let form1 = new SWForm("#edit_course .modal-body", "", "url", "GET", false);
        form1.addComponent(new SWText("courseid", "hidden"));
        form1.addComponent(new SWText("subscription", "text", gettext('Subscription')));
        form1.addComponent(new SWText("category", "text", gettext('Category')));
        form1.addComponent(new SWTextarea("sdescription", gettext('Description'), 3).setAutoSize(true));
        form1.addComponent(new SWTextarea("videolink", gettext('VideoLink'), 3).setAutoSize(true));
        form1.addComponent(new SWCombobox("contact", gettext('Contact'), window.CommonData.PartUserNames))
        form1.addComponent(new SWTextarea("remark", gettext('Remark'), 3).setAutoSize(true));
        form1.addComponent(new SWTextarea("duration", gettext('Duration'), 3).setAutoSize(true));
        form1.addComponent(new SWTextarea("rate", gettext('Rate'), 2).setAutoSize(true));
        form1.addComponent(new SWText("coursetype", "text", gettext('Course Type')));
        form1.addComponent(new SWCombobox("sstatus", gettext('Status'), ["N", "I", "T","H", "C", "F"]));
        form1.addComponent(new SWText("mindmapid", "text", gettext('MindmapId')));
        form1.addComponent(new SWText("udf01", "text", gettext('Task Filter')));
        form1.dom.find("input[name='udf01']").attr("placeholder", "格式:pid-tid:contact, 至少錄入pid-tid");
        form1.create_url = "/devplat/course/create";
        form1.update_url = "/devplat/course/update?pk=[[pk]]";
        form1.pk_in_url = false;
        form1.dom.find(".card-header").hide();
        form1.dom.find(".card-footer").hide();
        form1.dom.find(".page-inner").addClass("p-0");
        form1.on_after_save = function (data) {
            $("#edit_course").modal("hide");
            var sea_value = $("#course_table input[type='search']").val()
            self.course_datatable.draw();
        }
        form1.on_after_init = function (data) {
            $("#edit_course textarea").trigger("change");
        }
        self.edit_form = form1;
        $("#edit_course #new_save").on("click", function () {
            self.edit_form.dom.find(".save").click();
        });
    }
    this.init_course_advenced_search_dialog = function () {
        var test_search = new SWAdvancedsearch(self.course_adv_search_btn); //設置Search按鈕為觸發標籤
        var group = new SWAdvancedsearch.Group(SWAdvancedsearch.Condition.AND);
        var subscription = new SWAdvancedsearch.Rule("subscription", SWAdvancedsearch.Type.STRING,
            SWAdvancedsearch.Operator.CONTAINS, gettext('Subscription'));
        var category = new SWAdvancedsearch.Rule("category", SWAdvancedsearch.Type.STRING,
            SWAdvancedsearch.Operator.CONTAINS, gettext('Category'));
        var sdescription = new SWAdvancedsearch.Rule("sdescription", SWAdvancedsearch.Type.STRING,
            SWAdvancedsearch.Operator.CONTAINS, gettext('Description'));
        var contact = new SWAdvancedsearch.Rule("contact", SWAdvancedsearch.Type.STRING,
            SWAdvancedsearch.Operator.CONTAINS, gettext('Contact'));
        var sstatus = new SWAdvancedsearch.Rule("sstatus", SWAdvancedsearch.Type.STRING,
            SWAdvancedsearch.Operator.CONTAINS, gettext('Status'));
        var coursetype = new SWAdvancedsearch.Rule("coursetype", SWAdvancedsearch.Type.STRING,
            SWAdvancedsearch.Operator.CONTAINS, gettext('Course Type'));
        group.addRule(subscription);
        group.addRule(category);
        group.addRule(sdescription);
        group.addRule(contact);
        group.addRule(sstatus);
        group.addRule(coursetype);
        test_search.addGroup(group);
        test_search.on_search_event = function (filter) {
            self.course_datatable.search('form-search:' + filter).draw();
            $('#course_table1_filter input').val('')
        }
    }    

    this.init_course_table = function () {
        var table1 = new SWDataTable("#course_table", "course_table1"); //創建SWDataTable對象
        table1.paging = false; //設置分頁顯示
        table1.searching = true; //設置不顯示查詢框
        const desc_width = SWApp.os.isMobile ? '60%' : (checkMediaQuery() ? '30rem' : '30%');
        //設置顯示字段
        table1.columns = [
            { field: "subscription", label: gettext('Subscription') },
            { field: "category", label: gettext('Category') },
            { field: "sdescription", label: gettext('Description'), width: desc_width, },
            {
                field: "videolink", label: gettext('VideoLink'), render: function (data, type, row) {
                    return `<a href="${data}" target="_blank">link</a>`;
                }
            },
            { field: "contact", label: gettext('Contact') },
            { field: "remark", label: gettext('Remark'), width: checkMediaQuery() ? '20rem' : "20%", },
            { field: "duration", label: gettext('Duration') },
            { field: "rate", label: gettext('Rate') },
            { field: "coursetype", label: gettext('Course Type') },
            { field: "sstatus", label: gettext('Status') },
            {
                field: "operation", label: gettext('Operation'),
                render: function (data, type, row) {
                    var id = row.inc_id;
                    return `<a class="btn btn-show-task btn-sm btn-icon btn-secondary" href="#" filter="${row.udf01}">T</a>
                            <a class="btn btn-edit btn-sm btn-icon btn-secondary" href="#" id="${id}"><i class="fa fa-pencil-alt"></i></a>
                            <a class="btn del-btn btn-sm btn-icon btn-secondary" href="#" id="${id}"><i class="far fa-trash-alt"></i></a>`;
                }
            }
        ];
        // var desc_width = SWApp.os.isMobile ? "60%" : "30%";
        table1.setOptions({
            responsive: true,
            autoWidth: !checkMediaQuery(),
            scrollX: checkMediaQuery(),
            columnDefs: [//revolt specialist carpet meditation 
                { "responsivePriority": 2, "className": "min-tablet-p", "targets": 0 },
                { "responsivePriority": 3, "className": "min-tablet-p", "targets": 1 },
                { "responsivePriority": 1, "className": "all", "targets": 2 },
                { "responsivePriority": 1, "className": "all", "targets": 3 },
                { "responsivePriority": 2, "className": "min-tablet-p", "targets": 4 },
                { "responsivePriority": 5, "className": "min-tablet-p", "targets": 5 },
                { "responsivePriority": 6, "className": "min-tablet-p", "targets": 6 },
                { "responsivePriority": 7, "className": "min-tablet-p", "targets": 7 },
                { "responsivePriority": 8, "className": "min-tablet-p", "targets": 8 },
                { "responsivePriority": 9, "className": "min-tablet-p", "targets": 9 },
                { "responsivePriority": 10, "className": "min-tablet-p", "targets": 10 }
            ],
            deferLoading: 0
        });
        self.course_table = table1
        self.course_datatable = table1.init('/devplat/course/list');
        self.course_add_btn = $(`<a class="btn btn-sm btn-outline-primary" id="add_course" href="#"><i class="fa fa-plus mr-2"></i>` + gettext_addCourse + `</a>`);
        $("#course_table1_wrapper>.row:first .text-left").append(self.course_add_btn);
        self.course_adv_search_btn = $(`<button class="btn btn-sm btn-outline-primary search_more" style="margin-left: 10px"><i class="fa fa-search mr-2"></i>` + gettext("Search") + `</button>`);
        if (SWApp.os.isMobile)
            self.course_adv_search_btn = $(`<button class="btn btn-sm btn-outline-primary search_more" style="margin-left: 10px"><i class="fa fa-search"></i>` + gettext("Search") + `</button>`);
        $('#course_table1_filter').append(self.course_adv_search_btn)
    }

    this.init_solution_table = function () { 
        var table1 = new SWDataTable("#SolutionType", "solution_table"); //創建SWDataTable對象
        table1.paging = false; //設置分頁顯示
        table1.searching = false; //設置不顯示查詢框
        table1.orderBy = [['inc_id', 'asc']];
        //設置顯示字段
        table1.columns = [
            {field:"inc_id", label:"inc_id", visible:false},
            { field: "sdescription", label: gettext('Description') },
            { field: "contact", label: gettext('Contact') },
            {
                field: "operation", label: gettext('Operation'),
                render: function (data, type, row) {
                    var id = row.inc_id;
                    return `<a class="btn btn-edit btn-sm btn-icon btn-secondary" href="#undefined" id="${id}"><i class="fa fa-pencil-alt"></i></a>
                            <a class="btn del-btn btn-sm btn-icon btn-secondary" href="#undefined" id="${id}"><i class="far fa-trash-alt"></i></a>`;
                }
            }
        ];
        var desc_width = SWApp.os.isMobile ? "60%" : "50%";
        table1.setOptions({
            scrollY:'56vh',
            scrollCollapse: true,
            responsive: true,
            columnDefs: [
                { "responsivePriority": 2, width:desc_width,"className": "all", "targets": 0 },
                { "responsivePriority": 4, "targets": 1 },
                { "responsivePriority": 2, "className": "min-tablet-p", "targets": 2 },            
            ],
            deferLoading: 0
        });
        table1.custom_params_fun = function () {
            var courseid = undefined;
            if (self.solution_table != undefined) {
                courseid = $("#solution_table").data("courseid");
                if (courseid != undefined)
                    return {
                        attach_query: `{"condition":"AND","rules":[{"id":"courseref","field":"courseref","type":"string","input":"text","operator":"equal","value":"${courseid}"}],"not":false,"valid":true}`};
                else
                    return {};
            }
        }
        self.solution_table = table1
        self.solution_datatable = table1.init('/devplat/solution/list');
        self.solution_add_btn = $(`<a class="btn btn-sm btn-edit btn-subtle-primary" id="add_course" href="#"><i class="fa fa-plus mr-2"></i>` + gettext_addSolution + `</a>`);
        $("#solution_table_wrapper").prepend(self.solution_add_btn);
    }
    this.init_task_table = function () {
        var table = new SWDataTable("#course_task_table", "course_task_datatable"); //創建SWDataTable對象

        table.paging = false;   //設置分頁顯示

        table.orderBy = [['taskid', 'asc']];     //設置按taskno 升序排序，可以進行多字段排序，參考上面的重要屬性

        //設置DataTable顯示5個字段，分別是taskno, task,contact, planbdate, planedate
        table.columns = [
            { field: "taskno", label: gettext('TaskNo') },
            { field: "task", label: gettext('Task') },
            { field: "contact", label: gettext('Contact') },
            { field: "schpriority", label: gettext('SchPriority')},
            { field: "planbdate", label: gettext('PlanBDate'), render:SWDataTable.DateRender},
            { field: "edate", label: gettext('EDate'), render:SWDataTable.DateRender},            
            { field: "progress", label: gettext('Progress'),render:function(data, type, row) {
                if (row.progress == 'S')
                return '<span class="status primary">S </span>';                
                else if (row.progress == 'F')
                    return '<span class="status success">Finish</span>';
                else if (row.progress == 'I')
                    return '<span class="status danger">InGoing</span>';
                else if (row.progress == 'C')
                    return '<span class="status success">Complete</span>';
                else if (row.progress == 'N')
                    return '<span class="status Info">Normal</span>';
                else if (row.progress == 'H')
                    return '<span class="status primary">Hold</span>';
                else if (row.progress == 'T')
                    return '<span class="status warning">Today</span>';
                else if (row.progress == 'R')
                    return '<span class="status warning">Reviews</span>';                
                else
                    return row.progress;
            }
            },
            { field: "taskid", label: gettext('TaskId'), visible: false }
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
                { "responsivePriority": 5, "className": "min-tablet-p", "targets": 6 },
            ],
            deferLoading: 0
        });
        self.course_task_table = table
        self.course_task_datatable = table.init('/PMIS/task/t_list');  //根據以上設置好的屬性，初始化table1，數據來源於/server/tasks這個地址
    }

    

    this.bind_event = function () {
        $("#course_table").on("click", ".btn-edit", function (e) {
            e.preventDefault();
            var id = $(this).attr("id");
            self.edit_form.set_pk(id);
            self.edit_form.init_data();
            $("#edit_course").modal("show");
        });
        $("#course_table").on("click", ".btn-show-task", function (e) {
            e.preventDefault();
            var row_tr = $(this).closest("tr")
            if (row_tr.hasClass("child"))
                row_tr = row_tr.prev()[0];            
            var row = self.course_datatable.row(row_tr).data();
            $(".course_nav a[href='#course_task']").data("course", row);
            $(".course_nav a[href='#course_task']").tab("show");
        });
        $("#course_task_table").on("dblclick", "tbody tr", function(){
            var row = self.course_task_datatable.row(this).data();
            init_task(row.DT_RowId);
        });
        $("#course_task .back").on("click", function(e){
            e.preventDefault();
            $(".course_nav a[href='#course']").tab("show");
        });
        $('.course_nav a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
            var tab = $(this).attr("href");
            if (tab == "#course_task") {
                if (self.course_task_table == undefined)
                    self.init_task_table();

                var data=$(this).data("course");
                if (data.udf01 != $(this).data("filter")) {
                    var udf01 = data.udf01;
                    if (udf01 == undefined)
                        $("#course_task_datatable tbody").empty();
                    else if (/([^-]+)-([0-9]+)(:([^:]+))?$/.test(udf01)) {
                        self.course_task_table.custom_params_fun = function() {
                            var group = udf01.match(/([^-]+)-([0-9]+)(:([^:]+))?$/i)
                            var pid = group[1];
                            var tid = group[2];
                            var contact = group[4];
                            var filter = `{"id":"pid","field":"pid","type":"string","input":"text","operator":"equal","value":"${pid}"},
                                {"id":"tid","field":"tid","type":"string","input":"text","operator":"equal","value":"${tid}"}`
                            if (contact != undefined)
                                filter = filter + `,{"id":"contact","field":"contact","type":"string","input":"text","operator":"equal","value":${contact}}`
                            return {attach_query: `{"condition":"AND","rules":[${filter}],"not":false,"valid":true}`}                        
                        }    
                        self.course_task_datatable.search("").draw();
                    }else {
                        $("#course_task_datatable tbody").empty();
                        alert("Course 中錄入的Task Filter格式錯誤!");
                    }
                    $(this).data("filter", data.udf01);
                }
            }
        });
        self.course_add_btn.on("click", function () {
            self.edit_form.set_pk(undefined);
            self.edit_form.init_data();
            $("#edit_course").modal("show");
        });
        $("#course_table").on("click", ".del-btn", function () {
            var id = $(this).attr("id");
            if (confirm('Are you sure you want to delete this data?')) {
                var id = $(this).attr("id")
                var url = `/devplat/course/delete/${id}`;
                $.ajax({
                    type: "POST",
                    url: url,
                    beforeSend: function (request) {
                        request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    },
                    success: function (result) {
                        if (result.status) {
                            //刷新數據
                            self.course_datatable.search("").draw();
                        } else
                            alter("刪除失敗");
                    }
                });
            }
        });
        self.course_datatable.on("select", function(e, dt, type, indexes){
            var data = self.course_datatable.row(indexes).data();
            var mindmapid = data.mindmapid
            var courseid = data.courseid;
            $("#solution_table").data("courseid", courseid);
            if (mindmapid != undefined)
                self.mindmap_browser.set_url("/PMIS/mindmap/update?pk=" + mindmapid);
            else
                self.mindmap_browser.set_url("");
            self.solution_datatable.search("").draw();
        });
        self.solution_datatable.on("select", function(e, dt, type, indexes){
            var data = self.solution_datatable.row(indexes).data();
            var mindmapid = data.mindmapid
            if (mindmapid != undefined)
                self.mindmap_browser.set_url("/PMIS/mindmap/update?pk=" + mindmapid);
            else {
                var data=self.course_datatable.rows( { selected: true }).data();
                if (data.length > 0 && data[0].mindmapid != undefined ) {
                    var local_mindmapid = data[0].mindmapid;
                    self.mindmap_browser.set_url("/PMIS/mindmap/update?pk=" + local_mindmapid);
                }else {
                    self.mindmap_browser.set_url("");
                }
            }
        });        

        /**self.course_datatable.on( 'draw', function () {
                if (self.course_datatable.rows().count() > 0)
                    self.course_datatable.rows(0).select()  
        });*/

        $("#solution_table").on("click", ".btn-edit", function () {
            var id = $(this).attr("id");
            self.solution_edit_form.set_pk(id);
            self.solution_edit_form.init_data();
            $("#edit_solution").modal("show");
        });
        self.solution_add_btn.on("click", function () {
            var courseid = $("#solution_table").data("courseid");        
            if (courseid == undefined)
                SWApp.popoverMsg($(this), "請先選擇Course");
            else {
                self.solution_edit_form.set_pk(undefined);
                self.solution_edit_form.init_data();
                $("#edit_solution").modal("show");
            }
        });
        $("#solution_table").on("click", ".del-btn", function () {
            var id = $(this).attr("id");
            if (confirm('Are you sure you want to delete this data?')) {
                var id = $(this).attr("id")
                var url = `/devplat/solution/delete/${id}`;
                $.ajax({
                    type: "POST",
                    url: url,
                    beforeSend: function (request) {
                        request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    },
                    success: function (result) {
                        if (result.status) {
                            //刷新數據
                            self.solution_datatable.search("").draw();
                        } else
                            alter("刪除失敗");
                    }
                });
            }
        });

        $(window).on('orientationchange', function () {
            location.reload();
        });
    }
}

function checkMediaQuery() {
    var mediaQuery = window.matchMedia("(min-width: 768px) and (max-width: 1499.98px)");
    return mediaQuery.matches;
}

$(function () {
    var UI = new PageUI();
    UI.init();
    UI.course_datatable.search("").draw();
    UI.course_datatable.columns.adjust();
    UI.course_datatable.columns.adjust().responsive.rebuild();
    UI.course_datatable.columns.adjust().responsive.recalc();
    window.update_menu_href = function () {
        window.update_session_url();
    }
});
