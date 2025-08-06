
function Requirements() {
    this.req_session_table = undefined;
    this.req_session_datatable = undefined;
    this.edit_form = undefined;
    this.FR_dom = undefined;
    this.GH_dom = undefined
    this.UC_dom = undefined;
    this.NR_dom = undefined;
    var req_task_container = `<div class="form-group SWTextarea" style="">
                                <label class="col-form-label caption" for="tf6">[[desc]]</label>
                                <div class="req_task [[type]]" style=""></div>
                            </div>`
    var self = this;
    this.init = function() {
        let form1 = new SWForm("#req_edit","User Requirement","url","GET",false);
        form1.addComponent(new SWText("rid","text",gettext('Requirement ID')));
        $("#req_edit input[name='rid']").attr("readonly","readonly");
        form1.addComponent(new SWTextarea("purpose",gettext('Purpose'), 3).setAutoSize(true));
        form1.addComponent(new SWTextarea("feature",gettext('Feature'), 3).setAutoSize(true));
        form1.addComponent(new SWTextarea("fr",gettext('Functional Requirement'), 5).setAutoSize(true));
        form1.addComponent(new SWTextarea("gh",gettext('Good to Have'), 5).setAutoSize(true));
        form1.addComponent(new SWTextarea("mh",gettext('Must Have'), 5).setAutoSize(true));
        form1.addComponent(new SWTextarea("uc",gettext('Under Consideration'), 5).setAutoSize(true));
        form1.addComponent(new SWTextarea("nr",gettext('Non-Functional Requirement'), 5).setAutoSize(true));
        form1.addComponent(new SWText("sessionid","hidden","Session id"));
        form1.addComponent(new SWTextarea("attributes",gettext('Requirement attributes'), 3).setAutoSize(true));
        form1.addComponent(new SWCombobox("rt",gettext('Requirement Type'), "/devplat/requement/gettypes"));
        form1.create_url = "/devplat/requement/create";  
        form1.update_url = "/devplat/requement/update?pk=[[pk]]";  
        form1.pk_in_url = false;
        form1.auto_save(true);
        form1.on_after_save = function(data) {
        }
        form1.on_after_init = function(data) {
            $("#req_edit textarea").trigger("change");
        }
        self.edit_form = form1;
    }

    this.get_pk_with_rid = function(rid) {
        return new Promise((resover, reject)=>{
            var url = "/devplat/requement/update?rid=" + rid
            $.get(url, function(result){
                if (result.status)
                    resover(result.data.inc_id);
                else
                    resover("");
            });
        })
    }

    this.init_requirement_task = function(sessionid) {
        function show_task(data, container) {
            container.empty();
            var dom = $("#task_item_template").clone();
            dom.removeAttr("id")
            var item = dom.find(".task-item").clone();
            dom.empty();
            for(task of data) {
                var local_item = item.clone();
                var local_task = task;
                if (Date.parse(local_task["planbdate"]) != null)
                    local_task["planbdate"] = Date.parse(local_task["planbdate"]).toString("yyyy-MM-dd");
                if (Date.parse(local_task["planedate"]) != null)
                    local_task["planedate"] = Date.parse(local_task["planedate"]).toString("yyyy-MM-dd");                
                dom.append(local_item.prop("outerHTML").render(local_task))
            }
            container.append(dom);
            dom.show();
            dom.collapse();
        }        
        var url = "/devplat/requement/req_task_list?sessionid=" + sessionid;
        $.get(url, function(result){
            if (result.status) {
                for (key in result.data) {
                    if (key == "FR") {
                        show_task(result.data['FR'], self.FR_dom);
                    }else if (key == "GH") {
                        show_task(result.data['GH'], self.GH_dom);
                    }else if (key == "UC") {
                        show_task(result.data['UC'], self.GH_dom);
                    }else if (key == "NR") {
                        show_task(result.data['NR'], self.GH_dom);
                    }
                }
            }
        })
        
    }

    this.init_session_table = function() {
       //在以上db_wapper控件中添加一個DataTable，生成的datatable的id為table1
       var table = new SWDataTable("#req_session_table", "req_table1"); //創建SWDataTable對象
       table.pageLength = 20;   //設置每頁顯示的數量為20

       table.paging = true;   //設置分頁顯示

       //設置DataTable顯示5個字段，分別是taskno, task,contact, planbdate, planedate
       table.columns = [
           { field: "rp016", label: "單別" },
           { field: "rp017", label: "問題單號" },
           { field: "rp004", label: "提出人" },
           { field: "rp005", label: "問題描述" },
           { field: "rp043", label: "原始提出人" },
           { field: "rp002", label: "提出日期", render:SWDataTable.DateRender},
           { field: "rp044", label: "需求" },
           { field: "rp011", label: "處理狀態" },
           {
               field: "operation", label: "操作",
               render: function (data, type, row) {
                   var id = row.inc_id;
                   return `<a href="#" class="btn btn-edit btn-sm btn-outline-secondary" id="${id}">修改</a>
                           <button type="button" class="del-btn btn btn-subtle-danger" inc_id="${id}">刪除</button>`
               }
           },
       ];
       var rp005_width = SWApp.os.isMobile ? "60%":"35%"
       //SWDataTable控件不支持的功能，可以使用原生jquery datatable的屬性設置
       table.setOptions({
            responsive: true,  //是否支持手機展開和隱藏列
           //隱藏的規則，responsivePriority值越大越先隱藏，width設置列寬度         
           columnDefs: [
            {"responsivePriority": 1, "className":"all", "targets": 1 },
            {"responsivePriority": 1, width:rp005_width, "className":"all",  "targets": 3 },
            {"responsivePriority": 2, "className":"min-tablet-p", "targets": 0 },
            {"responsivePriority": 3, "className":"min-tablet-p", "targets": 2 },
            {"responsivePriority": 4, "className":"min-tablet-p", "targets": 4 },
            {"responsivePriority": 5, "className":"min-tablet-p", "targets": 5 },
            {"responsivePriority": 6, "className":"min-tablet-p", "targets": 6 },   
            {"responsivePriority": 7, "className":"min-tablet-p", "targets": 7 },
           ],
           deferLoading:0
       });
       self.req_session_table = table
       self.req_session_datatable = table.init('/devplat/requement/list');  //根據以上設置好的屬性，初始化table1，數據來源於/server/tasks這個地址        
       $("#req_table1_wrapper .dataTables_length").empty();
       $("#req_table1_wrapper .dataTables_length").append(`
       <div class="form-inline">
       <a href="#" class="btn btn-add btn-sm btn-outline-secondary">新增</a>
       <label class="custom-control custom-checkbox ml-2 mt-1">
        <input type="checkbox" class="custom-control-input control">
        <span class="custom-control-label">
          All
        </span>
        </label> 
        </div>
       `);

       $("#req_session_table").on("click", "#req_table1_length .btn-add", function(){
            $('#Requirements .nav-tabs a[href="#req_edit"]').tab('show');
       });
       $("#req_session_table").on("click", ".btn-edit", function(){
            var id = $(this).attr("id");
            self.edit_form.set_pk(id);
            self.edit_form.init_data();    
            $('#Requirements .nav-tabs a[href="#req_edit"]').tab('show');
       });   
    }
}