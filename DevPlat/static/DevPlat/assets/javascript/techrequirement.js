function TechRequirement() {   
    this.datatable = undefined;
    this.table = undefined;
    this.edit_solution_richtext = undefined;
    this.edit_form = undefined;
    this.need_init = undefined;
    var function_params = undefined;
    var self = this;
    this.init = function() {
        this.init_edit_form();
        this.bind_event();
    }

    this.show_tecreq = function(params) {
        function_params = params;
        $('#Specification .nav-tabs a[href="#TechRequirement"]').tab('show');
        self.need_init = true;
    }

    this.init_edit_form = function() {
        let form1 = new SWForm("#edit_tecreq .modal-body", "", "url", "GET", false);
        form1.addComponent(new SWText("specname", "hidden"));
        form1.addComponent(new SWText("verno", "hidden"));
        form1.addComponent(new SWText("funcitemno", "hidden"));
        form1.addComponent(new SWText("itemno", "hidden"));
        form1.addComponent(new SWTextarea("ur", "User Requirement", 2).setAutoSize(true).setMaxLength(255));
        form1.addComponent(new SWTextarea("tr", "Techincal  Requirement", 2).setAutoSize(true).setMaxLength(255));
        var solution_container = $(`<div class="form-group soluton_container" style="">
                                    <label class="col-form-label caption" for="tf6">Solution Type/Technical</label>
                                </div>`);
        form1.layout.append(solution_container);
        self.edit_solution_richtext = new SWRichText("soluton_container");        
        
        form1.addComponent(new SWText('rtype',"text", "Requirement Type").setMaxLength(5));
        form1.dom.find(".card-header").hide();
        form1.dom.find(".page-inner").removeClass("page-inner");
        form1.dom.find(".card-footer").hide();
        form1.create_url = "/devplat/tecreq/create"
        form1.update_url = "/devplat/tecreq/update?pk=[[pk]]"
        form1.on_save_format = function(data) {
            data['solution'] = self.edit_solution_richtext.dom.summernote('code');
        }
        form1.on_after_save = function(data) {
            $("#edit_tecreq").modal("hide");
            self.datatable.search("").draw();
        }
        form1.on_after_init = function (data) {
            if (data.solution == undefined || data.solution == null)
            data.solution = ""
            self.edit_solution_richtext.dom.summernote("code", data.solution);
            $("#TechRequirement .textarea").trigger("change");
        }
        self.edit_form = form1;       
        $("#edit_tecreq .new_save").on("click", function() {
            self.edit_form.save_data($(this));
        });
    }

    this.init_tecreq_table = function() {
        if (self.table != undefined)
            return;
        var table = new SWDataTable("#tecreq_table_container", "tec_req_table"); //創建SWDataTable對象
        table.searching = false;  //設置不顯示查詢框
        //設置DataTable顯示5個字段，分別是taskno, task,contact, planbdate, planedate
        table.columns = [
           {field: "ur", label: "User Requirement"},
           {field:"tr", label:"Techincal  Requirement"},
           {field: "solution", label: "Solution Type/Technical"},
           {field:"rtype", label:"Requirement Type"},
           {
            field: "operation", label: "操作",
            render: function (data, type, row) {
                var id = row.DT_RowId;
                return `<a class="btn btn-edit btn-sm btn-icon btn-secondary" href="#" id="${id}"><i class="fa fa-pencil-alt"></i></a>
                        <a class="btn del-btn btn-sm btn-icon btn-secondary" href="#" id="${id}"><i class="far fa-trash-alt"></i></a>`;            
            }
            }           
        ];
        //SWDataTable控件不支持的功能，可以使用原生jquery datatable的屬性設置
        table.setOptions({
            responsive: true,  
            columnDefs: [
                {"responsivePriority": 1, "className":"all", "targets": 0 },
                {"responsivePriority": 2, "className":"min-tablet-p", "targets": 1 },
                {"responsivePriority": 1, "className":"all", "targets": 2 },
                {"responsivePriority": 3, "className":"min-tablet-p", "targets": 3 },
                {"responsivePriority": 3, "className":"min-tablet-p", "targets": 3 }
            ],
            deferLoading:0
        });     
        self.table = table;        
        self.datatable = table.init("/devplat/tecreq/list");
    }

    this.bind_event = function() {
        $('#Specification .nav-tabs a[data-toggle="tab"]').on('shown.bs.tab', function (e) {        
            var tab = $(this).attr("href");
            if (tab == "#TechRequirement") {
                self.init_tecreq_table();
                if (self.need_init) {
                self.table.custom_params_fun = function () {
                    var params = function_params;
                    return {
                        attach_query: `{"condition":"AND","rules":[{"id":"specname","field":"specname","type":"string","input":"text","operator":"equal","value":"${params.specname}"},
                        {"id":"verno","field":"verno","type":"string","input":"text","operator":"equal","value":"${params.verno}"},
                        {"id":"funcitemno","field":"funcitemno","type":"string","input":"text","operator":"equal","value":"${params.funcitemno}"}
                        ],"not":false,"valid":true}`};
                }
                self.datatable.search("").draw();
                self.need_init = false;
            }
            }
        });
        $("#TechRequirement .back").on("click", function(e){
            $('#Specification .nav-tabs a[href="#spec_edit"]').tab('show');            
        });
        $("#TechRequirement #add_tecreq").on("click", function() {
            self.edit_form.set_pk(undefined);
            self.edit_form.init_data(function_params);
            $("#edit_tecreq").modal("show");
        });
        $("#TechRequirement").on("click", ".btn-edit", function(){ 
            var id = $(this).attr("id");
            self.edit_form.set_pk(id)
            self.edit_form.init_data();
            $("#edit_tecreq").modal("show");
        });

        $("#TechRequirement").on("click", ".del-btn", function(){ 
            var id = $(this).attr("id");
            if (confirm('Are you sure you want to delete this data?')) {
                var id = $(this).attr("id")
                var url = `/devplat/tecreq/delete/${id}`;
                $.ajax({
                    type: "POST",
                    url: url,
                    beforeSend: function (request) {
                        request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    },
                    success: function (result) {
                        if (result.status) {
                            //刷新數據
                            self.datatable.search("").draw();
                        } else
                            alter("刪除失敗");
                    }
                });
            }            
        });
    }
}