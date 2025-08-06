function SessionTasks() {
    this.tables = {
        tasks: { id: "session_tasks_table", table: undefined, datatable: undefined },
        top_tasks: { id: "session_top_tasks_table", table: undefined, datatable: undefined },
        top_priority_tasks: { id: "session_top_priority_tasks_table", table: undefined, datatable: undefined },
    }
    
        
    const showAIDocument = SWAIComBox('#showAIDocument')
    this.hoperation_type = {};
    var self = this;
    var fileViews = undefined;
    this.init = function () {
        var progress = new SWCombobox("progress", gettext('Progress'),
            [{ label: "N:新工作", value: "N" }, { label: "I:正在進行的工作", value: "I" }, { label: "T:當天的工作", value: "T" },
            { label: "S:已經開始的工作", value: "S" }, { label: "F:已完成工作", value: "F" }, { label: "C:基本完成", value: "C" },
            { label: "NF:除F的工作", value: "NF" }, { label: "H:被掛起的工作", value: "H" }, { label: "R:復查", value: "R" }]);
        progress.setHorizontalDisplay(true)
        var priority = new SWCombobox("priority", gettext('Priority'), ['888', '8888', '8889']);
        priority.setHorizontalDisplay(true)
        var class1 = new SWCombobox("class_field", gettext('Class'), [{ label: "class1", value: "1" }, { label: "class2", value: "2" }, { label: "Other", value: "3" }]);
        class1.setHorizontalDisplay(true)
        var contact = new SWCombobox("contact", gettext('Contact'), window.CommonData.PartUserNames)
        contact.input_dom.attr("data-live-search", "true");
        contact.setHorizontalDisplay(true)
        var process = new SWCombobox("hoperation", gettext('Hoperation'), "/PMIS/global/get_typelist?type_name=HOperation_Type");
        process.setHorizontalDisplay(true)

        var docflag = new SWCombobox("docflag", gettext('File'), [{ 'docflag': 'Y', 'describe': '存在附件' },
        { 'docflag': 'N', 'describe': '不存在附件' }], '', 'docflag', 'describe');
        docflag.setHorizontalDisplay(true)

        var task_desc = new SWText("task", "text", gettext('Task Desp'));
        task_desc.setHorizontalDisplay(true)
        //syl 20231005
        var planbdate_start = new SWDate("planbdate_start", "date", gettext('PlanBDate')); //計劃日期開始
        planbdate_start.setHorizontalDisplay(true)
        var planbdate_end = new SWDate("planbdate_end", "date", gettext('To')); //到
        planbdate_end.setHorizontalDisplay(true)
        //syl 20231005
        var container = $(`<div class="filter_f col-xs-6 col-sm-4 col-lg-2 col-custom-xxl f_progress"></div>`);

        $("#Session_Tasks .filter").prepend($(`<div class="filter_t mt-xl-0 col-xs col-sm col-md f_task_desc"></div>`).append(task_desc.dom));
        $("#Session_Tasks .filter").prepend($(`<div class="filter_t mt-xl-0 col-xs-6 col-sm-6 col-md-6 col-lg-2 col-custom-xxl_13 f_planbdate_end"></div>`).append(planbdate_end.dom)); //syl 20231005
        $("#Session_Tasks .filter").prepend($(`<div class="filter_t mt-xl-0 col-xs-6 col-sm-6 col-md-6 col-lg-2 col-custom-xxl_15 f_planbdate_start"></div>`).append(planbdate_start.dom)); //syl 20231005
        $("#Session_Tasks .filter").prepend($(`<div class="filter_d col-xs-6 col-sm-4 col-lg-2 col-custom-xxl f_docflag"></div>`).append(docflag.dom));
        $("#Session_Tasks .filter").prepend($(`<div class="filter_c col-xs-6 col-sm-4 col-lg-2 col-custom-xxl_10"></div>`).append(class1.dom));
        $("#Session_Tasks .filter").prepend($(`<div class="filter_p col-xs-6 col-sm-4 col-lg-2 col-custom-xxl_10 f_priority"></div>`).append(priority.dom));
        $("#Session_Tasks .filter").prepend($(`<div class="filter_p col-xs-6 col-sm-4 col-lg-2 col-custom-xxl f_process"></div>`).append(process.dom));
        $("#Session_Tasks .filter").prepend($(`<div class="filter_t mt-lg-0 col-xs-6 col-sm-4 col-lg-2 col-custom-xxl f_contact"></div>`).append(contact.dom));
        $("#Session_Tasks .filter").prepend(container.clone().append(progress.dom));
        $("#Session_Tasks .filter.row .input-group").removeClass("col-auto");
        var get_lang_code = $("#curr_language_code").val();
        if (get_lang_code == "en") {
            $("#Session_Tasks .filter.row").addClass("en_filter");
        }

        self.bind_event();
        $('.session_tasks_menu a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
            $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
        });
        self.init_hoperation_type();
        fileViews = new fileViewsComponent('DocumentList'); // 新增文件列表顯示在id為DocumentList
        fileViews.download = function (el) { // 下載文件的處理
            var pk = $(el).attr('pk');
            $.ajax({
                url: `/PMIS/task/get_t_doc?inc_id=${pk}`,
                method: "GET",
                xhrFields: {
                    responseType: 'blob' // 重要: 设置响应类型为 blob
                },
                success: function (data, status, xhr) {
                    var a = document.createElement('a');
                    var url = window.URL.createObjectURL(data);
                    a.href = url;
                    var contentDisposition = xhr.getResponseHeader('Content-Disposition');
                    var filename = contentDisposition.split('filename*=')[1].split("''")[1];  // 提取文件名
                    filename = decodeURIComponent(filename);  // 对文件名进行解码
                    a.download = filename;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                },
                error: function (xhr, status, error) {
                    console.error("Error in file download: " + error);
                }
            })
        }
        fileViews.preview = function (el) {
            var pk = $(el).attr('pk');
            $.ajax({
                url: `/PMIS/task/preview_t_doc?inc_id=${pk}`,
                method: "GET",
                xhrFields: {
                    responseType: 'blob' // 設置響應類型為 blob
                },
                success: function (data) {
                    if (data.type.startsWith('application/pdf')) {
                        const blobUrl = window.URL.createObjectURL(data);
                        window.open(blobUrl, '_blank');
                    } else {
                        // 非 PDF 文件：触发下载
                        const blobUrl = window.URL.createObjectURL(data);
                        const link = document.createElement('a');
                        link.href = blobUrl;
                        link.download = '';  // 可以设置为具体的文件名
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                        window.URL.revokeObjectURL(blobUrl);
                    }
                },
                error: function (xhr, status, error) {
                    console.error("Error in file download: " + error);
                }
            });
        };

        // createDocumentViews(); //初始化
    }
    this.init_hoperation_type = function () {
        var url = "/PMIS/global/get_typelist?type_name={0}".format("HOperation_Type");
        $.get(url, function (result) {
            if (result.status) {
                for (var item of result.data) {
                    self.hoperation_type[item['value']] = item['label'];
                }
            }
        });
    }
    this.bind_event = function () {
        $("#Session_Tasks .btn-clear").on("click", function () {
            $("#Session_Tasks .SWCombobox select").val('').selectpicker('refresh');
            $("#Session_Tasks input").val('');
            self.tables.tasks.datatable.search('').columns().search('').draw();
        });

        $("#Session_Tasks .btn-search").on("click", function () {
            var local_tables = [];
            Array.prototype.push.apply(local_tables, Object.values(self.tables).filter((item) => {
                return $("#" + item.id).closest(".tab-pane").hasClass("show");
            }));
            /**
            Array.prototype.push.apply(local_tables, Object.values(self.tables).filter((item)=>{
                return $("#" + item.id).closest(".tab-pane").hasClass("show") == false;
            }));            
            */
            for (var item of local_tables) {
                var search_datatable = item.datatable
                var search_table = item.table;
                $("#Session_Tasks .SWCombobox select, #Session_Tasks .filter input").each((index, el) => {
                    var name = $(el).attr("name");
                    var columnIndex = search_datatable.column(name+':name').index()
                    if (!(name == "planbdate_start" || name == "planbdate_end" || name == undefined))
                        search_datatable = search_datatable.columns(columnIndex).search($(el).val())
                });
                search_datatable.draw();
            }
        });
        $("#Session_Tasks .btn-add").on("click", function () {
            var sessionid = self.getSessionid();
            if (sessionid != undefined) {
                var params = { sessionid: sessionid, contact: get_login_name() }
                init_task(undefined, params);
            }
        });
        // $("#Session_Tasks .SWCombobox select, #Session_Tasks input").on("change", function(){
        //     var search_table = self.datatable;
        //     $("#Session_Tasks .SWCombobox select, #Session_Tasks input").each((index,el)=>{
        //         var name = $(el).attr("name");
        //         search_table = search_table.columns(self.table.getColumnIndexByName(name)).search($(el).val())
        //     });
        //     search_table.draw();
        // });

        $(window).on('orientationchange', function () {
            location.reload();
        });
    }
    this.getSessionid = function () {
        var udf04 = $("#stepper-form input[name='ma001']").val();
        var session = $("#stacked-menu li.has-active").attr("sessionid");
        return session;
    }
    this.init_task_table = function () {
        for (var item of Object.values(self.tables)) {
            var table = new SWDataTable("#" + item.id, item.id.replace("table", "datatable")); //創建SWDataTable對象
            table.searching = false;
            table.pageLength = 25;
            if (["session_top_tasks_table", "session_top_priority_tasks_table"].indexOf(item.id) != -1) {
                table.pageLength = 40;
                table.ajax_method = "POST";
                table.orderBy = [['schpriority', 'desc']];
            } else {
                table.orderBy = [['taskid', 'asc']];     //設置按taskno 升序排序，可以進行多字段排序，參考上面的重要屬性
            }

            //設置DataTable顯示5個字段，分別是taskno, task,contact, planbdate, planedate
            table.columns = [
                { field: "taskno", label: gettext('TaskNo'), width: checkMediaQuery() ? '8.5rem' : "12%", },
                { field: "task", label: gettext('Task'), width: checkMediaQuery() ? '40rem' : '80%', },
                { field: "contact", label: gettext('Contact') },
                { field: "sessionpriority", label: gettext('SessionPriority') },
                { field: "schpriority", label: gettext('SchPriority') },
                { field: "planbdate", label: gettext('PlanBDate'), width: checkMediaQuery() ? '6rem' : '', render: SWDataTable.DateRender },
                { field: "edate", label: gettext('EDate'), width: checkMediaQuery() ? '6rem' : '', render: SWDataTable.DateRender },
                { field: "progress", label: gettext('Progress') },
                { field: "priority", label: gettext('Priority'), visible: true },
                { field: "class_field", label: gettext('Class'), visible: true },
                {
                    field: "hoperation", label: gettext('HOperation'), render: function (data, type, row) {
                        if (Object.keys(self.hoperation_type).indexOf(data) != -1)
                            return self.hoperation_type[data]
                        else
                            return data;
                    }
                },
                { field: "taskid", label: "TaskId", visible: false },
                { field: "docflag", label: "DocFlag", visible: false },
            ];
            //SWDataTable控件不支持的功能，可以使用原生jquery datatable的屬性設置
            var progress_width = SWApp.os.isMobile ? "8%" : ""
            table.setOptions({
                responsive: true,  //是否支持手機展開和隱藏列
                // responsive: {
                //     breakpoints: [
                //         { name: 'desktop', width: 1799 },
                //         { name: 'mdesktop', width: 1299 },
                //         { name: 'tablet', width: 1199 },
                //         { name: 'mtablet', width: 1023 },
                //         { name: 'fablet', width: 767 },
                //         { name: 'phone', width: 379 },
                //     ]
                // },
                autoWidth: !checkMediaQuery(),
                scrollX: checkMediaQuery(),
                colReorder: true,  //启动列拖动
                columnDefs: [
                    { "responsivePriority": 5, "className": "not-mobile", "targets": 0 },
                    { "responsivePriority": 1, "className": "all", "targets": 1 },
                    { "responsivePriority": 2, "className": "not-mobile", "targets": 2 },
                    { "responsivePriority": 3, "className": "not-mobile", "targets": 3 },
                    { "responsivePriority": 3, "className": "not-mobile", "targets": 4 },
                    { "responsivePriority": 4, "className": "not-mobile", "targets": 5 },
                    { "responsivePriority": 5, "className": "not-mobile", "targets": 6 },
                    { "responsivePriority": -1, "className": "all", "width": progress_width, "targets": 7 },
                    { "responsivePriority": 7, "className": "not-mobile", "targets": 8 },
                    { "responsivePriority": 8, "className": "not-mobile", "targets": 9 },
                    { "responsivePriority": 9, "className": "not-mobile", "targets": 10 },
                ],
                deferLoading: 0,
            });
            item.table = table;
            item.datatable = table.init('/PMIS/task/t_list');  //根據以上設置好的屬性，初始化table1，數據來源於/server/tasks這個地址
            item.datatable.on('dblclick', 'tbody tr', function () {
                var local_table = Object.values(self.tables).filter((a) => { return a.id == $(this).closest(".SWDataTable").attr("id") })
                if (local_table.length > 0) {
                    var data = local_table[0].datatable.row(this).data();
                    init_task(data.DT_RowId);
                }
            });
            SWApp.os.isMobile || SWApp.os.isTablet ? item.datatable.colReorder.move(6, 0) : "";
        }
        $("#Session_Tasks #session_tasks_table .dataTables_scrollBody").addClass("scrollbar");
    }

    get_date = function (data) {
        try {
            if (/[.][0-9]+$/.test(data))
                data = data.replace(/[.][0-9]+$/, "");
            if (/z$/i.test(data))
                data = data.replace(/z$/i, "");
            var date_data = Date.parse(data);
            return date_data.toString("yyyy-MM-dd");
        } catch (error) {
            return "";
        }
    }


    this.load_data = function (sessionid, planbdate, planedate) {
        var active_item = $("#stacked-menu .menu-item.has-active");
        var planbdate = get_date(active_item.attr("planbdate"));
        var planedate = get_date(active_item.attr("planedate"));
        self.tables.tasks.table.custom_params_fun = function () {
            if (sessionid != undefined) {
                var array = sessionid.split("-")
                var pid = array[0]
                var tid = array[1]
                //var date_filter = { "condition": "AND", "rules": [], "not": false } 取消Session限制
                var filter = {
                    "condition": "AND", "rules": [
                        { "id": "pid", "field": "pid", "type": "string", "input": "text", "operator": "equal", "value": pid },
                        { "id": "tid", "field": "tid", "type": "double", "input": "text", "operator": "equal", "value": tid }
                    ], "not": false, "valid": true
                };
                // $("#Session_Tasks .SWCombobox select, #Session_Tasks .filter input").each((index, el) => {
                //     var name = $(el).attr("name");
                //     if($(el).val()){
                //         if (!(name == "planbdate_start" || name == "planbdate_end" || name == undefined))
                //             filter['rules'].push({ "id": name, "field": name, "type": "string", "input": "text", "operator": "equal", "value": $(el).val() })
                //         if (name == "planbdate_start")
                //             filter['rules'].push({ "id": 'planbdate', "field": 'planbdate', "type": "string", "input": "text", "operator": "greater_or_equal", "value": $(el).val() })
                //         if (name == "planbdate_end")
                //             filter['rules'].push({ "id": 'planbdate', "field": 'planbdate', "type": "string", "input": "text", "operator": "less_or_equal", "value": $(el).val() })
                //     }
                // });
                /** 取消Session限制
                if (planbdate != "")
                    date_filter.rules.push({ "id": "planbdate", "field": "planbdate", "type": "string", "input": "text", "operator": "greater_or_equal", "value": planbdate });
                if (planedate != "")
                    date_filter.rules.push({ "id": "planedate", "field": "planedate", "type": "double", "input": "text", "operator": "less_or_equal", "value": planedate });
                var progress_date_filter = {
                    "condition": "OR", "rules": [
                        { "id": "progress", "field": "progress", "type": "string", "input": "text", "operator": "not_in", "value": ["C", "F"] }
                    ], "not": false
                }
                if (date_filter.rules.length > 0)
                    progress_date_filter.rules.push(date_filter)
                filter.rules.push(progress_date_filter);
                */
                var otherFilter = self.getOtherFilter()
                if (otherFilter != undefined)
                    filter.rules.push(otherFilter);
                return { attach_query: JSON.stringify(filter) };
            }
            else
                return {};
        }
        $("#Session_Tasks .SWCombobox select").val('').selectpicker('refresh');
        $("#Session_Tasks input").val('');
        self.tables.tasks.datatable.search('').columns().search('').draw();
        this.load_top_tasks_data()
        // Documentation session的任務文檔根據名稱匹配然後顯示到列表中, Documentation session為專門存放文檔的地方
        var attachSession = []; //匹配到的session 例如任務文檔session或設計文檔session
        var keyFields = ['Documentation', 'Design'];
        var selectTitle = active_item.attr('title');
        var menus = $("#stacked-menu li.menu-item[title]");
        function include (str, list) {
            return list.some(e => str.includes(e));
        }
        if (!include(selectTitle, keyFields)){
            // 將需要附帶查詢的session的文檔也查出來,放到此session中去
            var selectTitleSplit =  selectTitle.split('-');
            var contrastTitle = '';
            if (selectTitleSplit.length == 1)
                contrastTitle = selectTitleSplit[0]; //處理用戶錄入的Session名沒有-分割的, 例如 SALC Implementation
            else if (selectTitleSplit.length == 2)
                contrastTitle = selectTitleSplit[1]; //處理用戶錄入的Session名有-分割的, 例如 IP - SALC Implementation
            // 其餘的Session名稱錄入方式需要規範.
            for (let menu of menus){
                var title = $(menu).attr('title');
                if (!title.includes('-')) continue; // 若是session的名稱對不上則直接返回
                if (include(title,keyFields))
                    if (title.split('-')[1].trim() === contrastTitle.trim())
                        attachSession.push($(menu).attr('sessionid'));
            }
        } // 附屬查詢session完成
        var array = sessionid.split("-")
        var params = {};
        params.pid = array[0];
        params.tid = array[1];
        params.attach = JSON.stringify(attachSession)
        $.get(`/PMIS/task/t_doc_list`, params, function (res) {
            var docData = []
            if (res.status) {
                for (let data of res.data) {
                    var d = {};
                    d.taskid = data.foldername
                    d.date = get_date(data.t_stamp)
                    d.docname = data.docname
                    d.contact = data.revisedby
                    d.pk = data.inc_id
                    docData.push(d)
                }
            }
            fileViews.update(docData); //根據session獲取數據展示出來
        })
    }
    this.getOtherFilter = function () {
        var filter = { "condition": "AND", "rules": [], "not": false };
        $("#Session_Tasks .SWCombobox select, #Session_Tasks .filter input").each((index, el) => {
            var name = $(el).attr("name");
            if (name == "planbdate_start" || name == "planbdate_end") {
                var operator = 'contains'
                var val = $(el).val();
                if (val == "")
                    return;
                if (name == 'planbdate_start') {
                    name = 'planbdate'
                    operator = 'greater_or_equal'
                    val = val.slice(0, 10);
                } else if (name == 'planbdate_end') {
                    name = 'planbdate'
                    operator = 'less_or_equal'
                    val = val.slice(0, 10);
                }
                filter.rules.push({ "id": name, "field": name, "type": "string", "input": "text", "operator": operator, "value": val });
            }
        });
        if (filter.rules.length == 0)
            return undefined
        else
            return filter;
    }

    this.load_top_tasks_data = function () {
        var table_filter = function (id) {
            var sessions = self.getAllSessionIds();
            var filter = { "condition": "AND", "rules": [], "not": false }
            var session_filter = { "condition": "OR", "rules": [], "not": false }
            for (var session of sessions) {
                session_filter.rules.push(
                    {
                        "condition": "AND", "rules": [
                            { "id": "pid", "field": "pid", "type": "string", "input": "text", "operator": "equal", "value": session.pid },
                            { "id": "tid", "field": "tid", "type": "double", "input": "text", "operator": "equal", "value": session.tid }
                        ], "not": false, "valid": true
                    }
                );
            }
            if (session_filter.rules.length > 0)
                filter.rules.push(session_filter)
            filter.rules.push({ "id": "progress", "field": "progress", "type": "string", "input": "text", "operator": "not_in", "value": ["C", "F"] });
            if (id == "session_top_priority_tasks_table")
                filter.rules.push({ "id": "class_field", "field": "class_field", "type": "string", "input": "text", "operator": "equal", "value": "1" })
            var otherFilter = self.getOtherFilter()
            if (otherFilter != undefined)
                filter.rules.push(otherFilter);
            return filter
        }

        self.tables.top_tasks.table.custom_params_fun = function () {
            var filter = table_filter("session_top_tasks_table");
            return { attach_query: JSON.stringify(filter) };
        }

        self.tables.top_priority_tasks.table.custom_params_fun = function () {
            var filter = table_filter("session_top_priority_tasks_table");
            return { attach_query: JSON.stringify(filter) };
        }
        self.tables.top_tasks.datatable.search('').columns().search('').draw();
        self.tables.top_priority_tasks.datatable.search('').columns().search('').draw();
    }

    this.getAllSessionIds = function () {
        var sessions = []
        $("#stacked-menu li[sessionid]").each(function (index) {
            var arr = $(this).attr('sessionid').split("-");
            sessions.push({ pid: arr[0], tid: arr[1] });
        });
        return sessions;
    }

    function fileViewsComponent(containerId, files) {
        var _this = this;
        var container = document.getElementById(containerId);
        files = type(files, 'Array') ? files : []; // 檢測類型
        render(); //渲染模板元素
        addEvent();

        this.update = function (newFiles) { // 更新數據
            files = type(files, 'Array') ? newFiles : [];
            type(_this.beforeUpdate, 'Function') && _this.beforeUpdate(files);
            document.getElementById('com-fileViews-grid').querySelector('div.row').innerHTML = gridRender(files);
            document.getElementById('com-fileViews-list').innerHTML = listRender(files);
            type(_this.afterUpdate, 'Function') && _this.afterUpdate();
        }

        function search(e) {
            var val = e.target.value.trim();
            if (val === '') return clear();
            var renderFiles = files.filter(file => file.docname.includes(val) || file.taskid.includes(val))
            type(_this.beforeSearch, 'Function') && _this.beforeSearch(val, renderFiles, files)
            var grid = document.getElementById('com-fileViews-grid').querySelector('div.row');
            var list = document.getElementById('com-fileViews-list');
            grid.innerHTML = gridRender(renderFiles);
            list.innerHTML = listRender(renderFiles);
            type(_this.afterSearch, 'Function') && _this.afterSearch(grid, list);
        }

        function clear() {
            _this.update(files);
        }

        function type(property, typeName) {
            var types = ['Function', 'Object', 'Array', 'String', 'Date', 'Number', 'Null', 'Undefined'];
            if (types.includes(typeName))
                return Object.prototype.toString.call(property).includes(typeName)
            return false
        }

        function addEvent() {
            container.querySelector('input.form-control').addEventListener('input', search)
            container.querySelector('button.close').addEventListener('click', clear)
            container.addEventListener('click', function (e) { // 委託事件至容器上,防止未加載元素就綁定下載事件
                var tag = e.target.tagName;
                var flag = e.target.className.includes('download');
                if ((tag === 'I' || tag === 'BUTTON') && flag) {
                    var el = undefined;
                    el = tag === 'I' ? e.target.parentElement : e.target
                    type(_this.download, 'Function') ? _this.download(el) : alert('沒有設置下載函數')
                }
                var previewFlag = e.target.className.includes('preview');
                if (tag === 'A' && previewFlag) {
                    type(_this.preview, 'Function') && _this.preview(e.target)
                }
            })
            $(".toggle-fullscreen").click(function () {
                $(this).toggleClass("fullscreen");
            });
            $("#DocumentList").on("click", "#q_gpt_btn", questionWithChatgpt);
            $("#DocumentList").on("click", "#q_ai_btn", questionWithAI);
            $("#DocumentList").on("click", ".file-item", function (e) {
                var tag = e.target.className.includes('download');
                var a_tag = e.target.tagName == 'A'
                if (!tag && !a_tag)
                    $(this).toggleClass("selected");
            })
        }
        
        // function questionWithAI(){
        //     var showTab = $("#myFilesContent .tab-pane.show");
        //     if (showTab.length > 0) {
        //         var id = showTab.attr("id");
        //         var selectRow = $("#" + id + " .file-item.selected");
        //         if (selectRow.length == 0) {
        //             alert("Please select document！");
        //         } 
        //         // 判断是否选中了多条记录
        //         if (selectRow.length > 1) {
        //             alert("You can only select one document!");
        //             return;
        //         }
        //         else {
        //             console.log(selectRow[0].innerText);
        //             var frameName ;
        //             // var frameVersion;
                    
        //             // 检查是否存在括号
        //             var startIndex = selectRow[0].innerText.indexOf('(');
        //             var endIndex = selectRow[0].innerText.indexOf(')');

        //             // 判断括号是否存在并进行截取
        //             if (startIndex !== -1 && endIndex !== -1 && startIndex < endIndex) {
        //                 // 从括号内截取内容并赋值给 frameName
        //                 frameName = selectRow[0].innerText.substring(startIndex + 1, endIndex);
        //                 console.log("Extracted frameName:", frameName);
        //             } else {
        //                 console.log("No frameName found in the text.");
        //                 return;
        //             }

        //             $.ajax({
        //                 url:  `/devplat/session/get_frame_data`, 
        //                 type: "GET",
        //                 data: { 
        //                     frameName: frameName
        //                 },
        //                 success: function(response) {
        //                     console.log("framedata:", response.data.framedata);
        //                     console.log("framedictionary:", response.data.framedictionary);

        //                     var framedataStr = JSON.stringify(response.data.framedata, null, 2);  // 格式化为可读的 JSON 字符串
        //                     var framedictionaryStr = JSON.stringify(response.data.framedictionary, null, 2);  // 同样处理字典

        //                     // console.log(framedataStr);
        //                     // console.log(framedictionaryStr);

        //                     // 构建对话内容
        //                     var sentData = "这是窗口文档的相关数据，其中功能和操作为多对多关系" + framedataStr + "。这是我提供给你的数据字典：" + framedictionaryStr;
                                    
        //                     // 設定發送數據到 AI 服務的方法，處理不同類型的數據發送需求。
        //                     showAIDocument.sendDataToReact(sentData, 'predefinedData')
        //                     //展示模態窗口
        //                     showAIDocument.show()
        //                     // 在这里处理后端返回的数据
        //                 },
        //                 error: function(error) {
        //                     console.error("Error fetching frame data:", error);
        //                 }
        //             });
                    
        //         }
        //     }
        // }

        function questionWithAI() {
            var showTab = $("#myFilesContent .tab-pane.show");
            if (showTab.length > 0) {
                var id = showTab.attr("id");
                var selectRow = $("#" + id + " .file-item.selected");
        
                // 如果没有选中文档
                if (selectRow.length == 0) {
                    alert("Please select a document!");
                    return;  // 提前返回，结束函数
                }
        
                // 如果选中了多条文档
                if (selectRow.length > 1) {
                    alert("You can only select one document!");
                    return;  // 提前返回，结束函数
                }
        
                // 如果选中了一条文档
                if (selectRow.length == 1) {
                    console.log(selectRow[0].innerText);
                    var frameName;
                    
                    // 检查是否存在括号
                    var startIndex = selectRow[0].innerText.indexOf('(');
                    var endIndex = selectRow[0].innerText.indexOf(')');
        
                    // 判断括号是否存在并进行截取
                    if (startIndex !== -1 && endIndex !== -1 && startIndex < endIndex) {
                        // 从括号内截取内容并赋值给 frameName
                        frameName = selectRow[0].innerText.substring(startIndex + 1, endIndex);
                        console.log("Extracted frameName:", frameName);
                    } else {
                        alert("No frameName found in the text.");
                        return;
                    }
        
                    // 发送AJAX请求
                    $.ajax({
                        url: `/devplat/session/get_frame_data`,
                        type: "GET",
                        data: {
                            frameName: frameName
                        },
                        success: function(response) {
                            console.log("response:", response);
                            console.log("framedata:", response.data.framedata);
                            console.log("framedictionary:", response.data.framedictionary);

                            // 判断 response.status 是否为 false
                            if (response.status === false) {
                                alert("No data found for the selected document.");
                                return;  // 终止后续操作
                            }


                            var framedataStr = JSON.stringify(response.data.framedata, null, 2);  // 格式化为可读的 JSON 字符串
                            var framedictionaryStr = JSON.stringify(response.data.framedictionary, null, 2);  // 同样处理字典
        
                            // 构建对话内容
                            var sentData = "这是窗口文档的相关数据:" + framedataStr + "。这是我提供给你的数据字典：" + framedictionaryStr;
                                            
                            // 設定發送數據到 AI 服務的方法，處理不同類型的數據發送需求。
                            showAIDocument.sendDataToReact(sentData, 'predefinedData');
                            // 展示模態窗口
                            showAIDocument.show();
                        },
                        error: function(error) {
                            console.error("Error fetching frame data:", error);
                        }
                    });
                }
                
            }
        }
        
        function questionWithChatgpt() {
            var showTab = $("#myFilesContent .tab-pane.show");
            if (showTab.length > 0) {
                var id = showTab.attr("id");
                var selectRow = $("#" + id + " .file-item.selected");
                if (selectRow.length == 0) {
                    alert("Please select document！");
                } else {
                    var ids = [];
                    for (var row of selectRow)
                        ids.push($(row).attr("pk"))
                    ids = ids.join(",");
                    var url = `/devplat/session/question_doc?ids=${ids}`;
                    setTimeout(() => {
                        window.open(url, target = "LangChain")
                    });
                }
            }
        }

        function render() {
            container.innerHTML = `    
                <div class="mt-3">
                    <div class="d-flex align-items-center justify-content-between mb-3">
                        <div class="input-group has-clearable mr-3">
                            <button type="button" class="close" aria-label="Close">
                                <span aria-hidden="true"> <i class="fa fa-times-circle"></i> </span>
                            </button>
                            <div class="input-group-prepend">
                                <span class="input-group-text"> <span class="oi oi-magnifying-glass"></span> </span>
                            </div>
                            <input type="text" class="form-control" placeholder=` + gettext("Search") + `>
                        </div>
                        <ul class="nav nav-pills filesNav flex-nowrap">
                            <li class="nav-item">
                                <a class="nav-link" href="#com-fileViews-grid" data-toggle="tab"> <i class="fas fa-th-large"></i> </a>
                            </li>
                            <li class="nav-item mr-2">
                                <a class="nav-link active" href="#com-fileViews-list" data-toggle="tab"> <i class="fas fa-list-ul"></i> </a>
                            </li>
                            <li class="nav-item">
                                <button type="button" class="btn btn-sm SWButton btn-outline-primary px-1 h-100" id="q_ai_btn" style="width:70px">AI</button>
                            </li>
                        
                            <li class="nav-item">
                                <button type="button" class="btn btn-sm SWButton btn-outline-primary px-1 h-100" id="q_gpt_btn" style="width:70px">Chat GPT</button>
                            </li>                            
                        </ul>
                    </div>
                    <div id="myFilesContent" class="tab-content">
                        <div class="tab-pane fade pt-1 scrollbar" id="com-fileViews-grid"> 
                            <div class="row mx-0"> ${gridRender(files)} </div>
                        </div>
                        <div class="tab-pane fade active show px-1 pt-1 scrollbar" id="com-fileViews-list">
                            ${listRender(files)} 
                        </div>
                    </div>
                </div> 
            `
        }

        function listRender(renderFiles) {
            return renderFiles.map(file =>
                `<div class="card card-fluid mb-2 file-item" pk=${file.pk}>
                    <div class="list-group list-group-flush list-group-divider">
                        <div class="list-group-item">
                            <div class="list-group-item-figure">
                                <span class="tile tile-img toggle-fullscreen">
                                    <i class="fa fa-file"></i>
                                    <div class="close-button">
                                        <i class="fa fa-times" style="font-size: 18px;"></i>
                                    </div>
                                </span>
                            </div>
                            <div class="list-group-item-body">
                                <div class="row">
                                    <div class="col-12 col-lg-3 d-none d-lg-block">
                                        <h4 class="list-group-item-title taskIdTitle text-darkblue">${file.taskid}</h4>
                                        <p class="list-group-item-text uploadFileDate text-indigo">${file.date}</p>
                                    </div>
                                    <div class="col-12 col-sm-9">
                                        <h4 class="list-group-item-title text-truncate">
                                            <a href="#" class="preview" pk="${file.pk}" style="text-decoration: underline;">${file.docname}</a>
                                        </h4>
                                        <p class="list-group-item-text fs-14 text-dark text-truncate">${file.contact}</p>
                                    </div>
                                </div>
                            </div>
                            <div class="list-group-item-figure">
                                <button pk="${file.pk}" class="btn btn-sm btn-icon btn-light text-dark download">
                                    <i class="oi oi-data-transfer-download"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div> `).join('');
        }

        function gridRender(renderFiles) {
            return renderFiles.map(file =>
                `<div class='col-lg-6 col-xl-3 file-item' pk=${file.pk}>
                    <div class='card card-fluid'>
                        <div class='card-header border-0 d-flex justify-content-between align-items-center px-2'>
                            <div class='d-flex align-items-center'>
                                <span class="badge badge-subtle badge-primary text-truncate mr-1">${file.taskid}</span>
                                <span class="badge bg-white text-truncate mr-1">${file.date}</span>
                            </div>
                            <button pk="${file.pk}" class="btn btn-sm btn-icon btn-light text-dark download">
                                <i class="oi oi-data-transfer-download"></i>
                            </button>
                        </div>
                        <div class='card-body text-center'>
                            <div class='user-avatar user-avatar-md'>
                                <i class="fa fa-file"></i>
                            </div>
                            <h5 class='card-title mt-3 text-truncate'>
                                <a href="#" class="preview" pk="${file.pk}" style="text-decoration: underline;">${file.docname}</a>
                            </h5>
                            <p class='card-subtitle text-dark text-truncate fs-14'>${file.contact}</p>
                        </div>
                    </div>
                </div>`).join('')
        }
    }


    function createDocumentViews(documentsData) {
        if (documentsData == undefined) documentsData = [];
        $("#fileViewList").empty();
        $('#fileGrid>.row').empty();
        $.each(documentsData, function (index, document) {
            var documentCard = $("<div>").addClass("card card-fluid mb-2 displayDocuments");
            var listGroup = $("<div>").addClass("list-group list-group-flush list-group-divider");
            var listItem = $("<div>").addClass("list-group-item");
            var listGroupItemBody = $("<div>").addClass("list-group-item-body");
            listItem.append(createListFigure(document.imgUrl),
                listGroupItemBody.append(
                    $("<div>").addClass("row").append(
                        createTitleAndDate(document.taskID, document.date),
                        createDescription(document.title, document.desc)
                    )
                ),
                $("<div>").addClass("list-group-item-figure").append(`<button data="${document.inc_id}" class="btn btn-sm btn-icon btn-light text-dark"><i class="oi oi-data-transfer-download"></i></button>`)
            )

            listGroup.append(listItem);
            documentCard.append(listGroup);
            $("#fileViewList").append(documentCard);
        });

        function createListFigure(imgUrl) {
            return $("<div>").addClass("list-group-item-figure").append(
                $("<span>").addClass("tile tile-img toggle-fullscreen").append(
                    $("<img>").attr("src", imgUrl).attr("alt", ""),
                    $("<div>").addClass("close-button").append(
                        $("<i>").addClass("fa fa-times").css("font-size", "18px")
                    )
                )
            );
        }

        function createTitleAndDate(taskID, date) {
            return (
                $("<div>").addClass("col-12 col-lg-3 d-none d-lg-block").append(
                    $("<h4>").addClass("list-group-item-title taskIdTitle text-darkblue").html(taskID),
                    $("<p>").addClass("list-group-item-text uploadFileDate text-indigo").text(date)
                )
            );
        }

        function createDescription(title, desc) {
            return $("<div>").addClass("col-12 col-sm-9").append(
                $("<h4>").addClass("list-group-item-title text-truncate").html('<a href="#">' + title + '</a>'),
                $("<p>").addClass("list-group-item-text fs-14 text-dark text-truncate").text(desc)
            );
        }

        $(".toggle-fullscreen").click(function () {
            $(this).toggleClass("fullscreen");
        });

        $.each(documentsData, function (index, item) {
            var cardWrap = $('<div>').addClass('col-lg-6 col-xl-3 ');
            var card = $('<div>').addClass('card card-fluid');
            var cardHeader = $('<div>').addClass('card-header border-0 d-flex justify-content-between align-items-center px-2');
            var badge = $('<div>').addClass('d-flex align-items-center').html(`<span class="badge badge-subtle badge-primary text-truncate mr-1">` + item.taskID + `</span>` + '<span class="badge bg-white text-truncate mr-1">' + item.date + `</span>`);
            var downloadBtn = `<button data="${item.inc_id}" class="btn btn-sm btn-icon btn-light text-dark"><i class="oi oi-data-transfer-download"></i></button>`;
            var cardBody = $('<div>').addClass('card-body text-center');
            var userAvatar = $('<a>').addClass('user-avatar user-avatar-xl').attr('href', '#');
            var avatarImage = $('<img>').attr({ 'src': item.imgUrl, 'alt': '' });
            var cardTitle = $('<h5>').addClass('card-title mt-3 text-truncate').html('<a href="#">' + item.title + '</a>');
            var cardSubtitle = $('<p>').addClass('card-subtitle text-dark text-truncate fs-14').text(item.desc);

            cardHeader.append(badge, downloadBtn);
            userAvatar.append(avatarImage);
            cardBody.append(userAvatar, cardTitle, cardSubtitle);
            card.append(cardHeader, cardBody);
            cardWrap.append(card);

            $('#fileGrid>.row').append(cardWrap);
        });
        $('#document_list_table  button').on('click', function () {
            var inc_id = $(this).attr('data');
            $.ajax({
                url: `/PMIS/task/get_t_doc?inc_id=${inc_id}`,
                method: "GET",
                xhrFields: {
                    responseType: 'blob' // 重要: 设置响应类型为 blob
                },
                success: function (data, status, xhr) {
                    var a = document.createElement('a');
                    var url = window.URL.createObjectURL(data);
                    a.href = url;
                    var contentDisposition = xhr.getResponseHeader('Content-Disposition');
                    var filename = contentDisposition.split('filename*=')[1].split("''")[1];  // 提取文件名
                    filename = decodeURIComponent(filename);  // 对文件名进行解码
                    a.download = filename;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                },
                error: function (xhr, status, error) {
                    console.error("Error in file download: " + error);
                }
            })
        })
    }
}

function checkMediaQuery() {
    var mediaQuery = window.matchMedia("(min-width: 768px) and (max-width: 1499.98px)");
    return mediaQuery.matches;
}