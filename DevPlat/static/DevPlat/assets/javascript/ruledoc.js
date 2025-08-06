function RuleDoc() {
    this.content_rich = undefined;
    this.RuleTable = undefined;
    this.RuleDataTable = undefined;
    this.recordid = getParamFromUrl("recordid");
    var self = this;
    this.init = function() {
        var projectName = getCookie("projects_cur_name");
        var title = gettext("RuleDoc");
        if (projectName != undefined && projectName != "null" && projectName != "undefined")
            title = projectName + " - " + title;        
        $(".rule_container .rule_title").text(title);
        //初始化複文本
        self.content_rich = new SWRichText("rule_content");
        self.content_rich.dom.addClass("py-2 h-100 shadow-none");
        //初始化Table
        self.initRuleTable();
        self.load_rule_table();
        self.bind_event();
    }
    this.initRuleTable = function() {
        var table1 = new SWDataTable("#rule_table_container", "rule_table"); //創建SWDataTable對象
        table1.paging = false; //設置分頁顯示
        table1.searching = false; //設置不顯示查詢框
        table1.columns = [
        { field: "topic", label: gettext('Topics') },
        { field: "sdescription", label: gettext('Description') },
        {field: "operation", label: "", orderable: false,
        render: function (data, type, row) {
            var id = row.inc_id;
            return `<button class="btn btn-sm btn_edit_rule" pk="${id}" type="button"><i class="fa fa-pencil-alt fa-fw"></i> </button>
                    <button class="btn btn-sm btn_del_rule" pk="${id}" type="button"><i class="far fa-trash-alt fa-fw"></i> </button>                    
                    `;
            }

        }]
        table1.setOptions({
            responsive: true,
            scrollResize: true,
            scrollY: 100,
            deferLoading: 0,
            columnDefs: [
                { "responsivePriority": 1, "width":"200px","className": "all", "targets": 0 },
                { "responsivePriority": 1, "className": "all", "targets": 1 },    
                { "responsivePriority": 1, "className": "all","width":"60px", "targets": 2 }
            ]        
        });
        self.RuleTable = table1;
        self.RuleDataTable = table1.init([])
    }
    this.load_rule_table = function() {
        var params = {draw: 0,start: 0,length: -1,attach_query: `{"condition":"AND","rules":[{"id":"recordid","field":"recordid","type":"string","input":"text","operator":"equal","value":"${self.recordid}"}
            ],"not":false,"valid":true}`}
        $.get("/devplat/ruledoc/list", params, function(result){
            self.RuleDataTable.clear().rows.add(result.data).draw();
            if(result.data.length > 0)
                self.RuleDataTable.row(0).select();
        })
        self.RuleTable.custom_params_fun = function() {
            return ;
        }
        self.RuleDataTable.search("").draw();
    }
    this.edit_rule_item = function(e) {
        var pk = $(this).attr("pk");
        var row_dom = $(this).closest("tr");
        self.RuleDataTable.row(row_dom).select();
        var row_data = self.RuleDataTable.row(row_dom).data();
        if ($(e.currentTarget).data("state") == undefined) {
            var topic = new SWTextarea("topic","",3, row_data.topic);
            topic.dom.find("label").remove()
            var desc = new SWTextarea("sdescription","", 3, row_data.sdescription);
            desc.dom.find("label").remove()
            row_dom.find("td:eq(0)").html(topic.dom);
            row_dom.find("td:eq(1)").html(desc.dom);
            self.content_rich.dom.summernote();
            $(e.currentTarget).data("editor", {topic:topic, desc:desc});
            $(e.currentTarget).find("i").removeClass("fa-pencil-alt").addClass("fa-save");
            $(e.currentTarget).data("state","edit");
        }else {
            var editor = $(this).data("editor");
            var new_row_data = Object.assign({},row_data, {topic:editor.topic.input_dom.val(), sdescription:editor.desc.input_dom.val(),content:self.content_rich.dom.summernote("code")});
            $.ajax({
                type:"POST",
                url:`/devplat/ruledoc/update?pk=${new_row_data.inc_id}`,
                data:new_row_data,
                beforeSend: function (request) {
                    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                },    
                success:function(result){
                    if (result.status) {
                        self.RuleDataTable.row(row_dom).data(new_row_data).draw(false);
                        $(e.currentTarget).find("i").removeClass("fa-save").addClass("fa-pencil-alt");
                        $(e.currentTarget).removeData("state");
                        self.content_rich.save();
                        self.scrollto_row(row_dom);
                    }else {
                        SWHintMsg.showToast("#rule_table_container", "保存失敗!","info", {position_class:"toast-top-center"});                                                                    
                    }
                }
            });            
        }
    }
    this.add_rule_item = function(e) {
        var state = $(this).data("state");
        if (state == undefined) {
            if ($("#rule_table_container textarea").length > 0) {
                SWHintMsg.showToast("#rule_table_container", "還有數據沒有保存，請先保存!","info", {position_class:"toast-top-center"});                        
                return;
            }            
            $.get("/devplat/ruledoc/create", {recordid:self.recordid}, function(result){
                if (result.status) {
                    var new_data = result.data;
                    self.content_rich.dom.summernote("code","");
                    $(e.currentTarget).data("state", "add");
                    $(e.currentTarget).find("i").removeClass("fa-plus").addClass("fa-save");
                    self.RuleDataTable.rows().deselect();
                    self.RuleDataTable.row.add(new_data).draw(false);
                    var row = $('#rule_table tr:last');
                    self.RuleDataTable.row(row).select();
                    var topic = new SWTextarea("topic","",3, new_data.topic);
                    topic.dom.find("label").remove();
                    var desc = new SWTextarea("sdescription","", 3, new_data.sdescription);
                    desc.dom.find("label").remove();
                    row.find("td:eq(0)").html(topic.dom);
                    row.find("td:eq(1)").html(desc.dom);
                    $(e.currentTarget).data("editor", {topic:topic, desc:desc});
                    self.scrollto_row(row);
                }else {
                    SWHintMsg.showToast("#rule_table_container", "初始化失敗!","info", {position_class:"toast-top-center"});                                            
                }
            })
            
        }else {
            var row = $('#rule_table tr:last');
            var row_data = self.RuleDataTable.row(row).data();
            var editor = $(this).data("editor");
            var new_row_data = Object.assign({}, row_data, {topic:editor.topic.input_dom.val(), sdescription:editor.desc.input_dom.val(),content:self.content_rich.dom.summernote("code")})
            $.ajax({
                type:"POST",
                url:"/devplat/ruledoc/create",
                data:new_row_data,
                beforeSend: function (request) {
                    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                },    
                success:function(result){
                    if (result.status) {
                        self.RuleDataTable.row(row).data(result.data.instance).draw();
                        self.scrollto_row(row);
                        $(e.currentTarget).removeData("state");
                        $(e.currentTarget).find("i").removeClass("fa-save").addClass("fa-plus");
                        self.content_rich.save();
                    }else {
                        SWHintMsg.showToast("#rule_table_container", "保存失敗!","info", {position_class:"toast-top-center"});                        
                    }
                }
            });            

        }
    }
    this.scrollto_row = function(row) {
        self.RuleDataTable.context[0].nScrollBody.scrollTo(0, (row[0].offsetTop));
    }
    this.del_rule_item = function(e) {
        var pk = $(this).attr("pk");
        var row = $(this).closest("tr");
        SWHintMsg.showToastModal("­警示信息", "是否確認刪除該規則?", "confirm").then((value) => {
            if (value) {
                var url = "/devplat/ruledoc/delete/" + pk;
                $.ajax({
                    type:"POST",
                    url:url,
                    beforeSend: function (request) {
                        request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    },    
                    success:function(result){
                        if (result.status) {
                            var prev_row = row.prev("tr");
                            self.RuleDataTable.row(row[0]).remove().draw();
                            if (prev_row.length > 0) {
                                self.scrollto_row(prev_row);
                                self.RuleDataTable.row(prev_row).select();
                            }
                        }
                    }
                });        
            }
        });
    }
    this.user_selected_row = function(e, dt, type, indexes) {
        if ($("#rule_table_container textarea").length > 0) {
            if (indexes.index().row != dt.row($("#rule_table_container textarea").closest("tr")).index())
                SWHintMsg.showToast("#rule_table_container", "還有數據沒有保存，請先保存!","info", {position_class:"toast-top-center"});                        
            return false;
        }
    }
    this.selected_row = function(e, dt, type, indexes) {
        var row_data = dt.row(indexes).data();
        self.content_rich.dom.empty();
        self.content_rich.dom.append(row_data.content == undefined ? "" : row_data.content);
    }
    this.bind_event = function() {
        $("#rule_table_container").on("click", ".btn_edit_rule", self.edit_rule_item);
        $("#rule_table_container").on("click", ".btn_del_rule", self.del_rule_item);
        $("#items .btn_add_rule").on("click", self.add_rule_item);
        self.RuleDataTable.on("user-select", self.user_selected_row);
        self.RuleDataTable.on("select", self.selected_row);
    }
}
$(function () {
    $(".page").addClass("has-sidebar has-sidebar-expand-xl");    
    var ruleDoc = new RuleDoc();
    ruleDoc.init();
    window.update_menu_href = function () {
        window.update_session_url();
    }

    $("#ruledocExpandedBtn").on('click',function(e){
        e.preventDefault();
        $(this).parent().closest(".card.page-sidebar").toggleClass("ruledoc-expanded");
        var icon = $(this).find("i");
        if (icon.hasClass("fa-expand-alt")) {
            icon.removeClass("fa-expand-alt").addClass("fa-compress-alt");
        } else {
            icon.removeClass("fa-compress-alt").addClass("fa-expand-alt");
        }
    });
});