"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

// Class Template
// =============================================================
var stepsDemo = /*#__PURE__*/function () {
    function stepsDemo() {
        _classCallCheck(this, stepsDemo);

        this.init();
    }

    _createClass(stepsDemo, [{
        key: "init",
        value: function init() {
            // event handlers
            this.handleValidations();
            this.handleSteps();
        }
    }, {
        key: "validateBy",
        value: function validateBy(trigger) {
            var isNextBtn = $(trigger).hasClass('btn');
            var from = isNextBtn ? null : $(trigger).parents('ul').children('.active').index();
            var to = isNextBtn ? null : $(trigger).parent().index();
            var $trigger = isNextBtn ? $(trigger) : $(trigger).parents('ul').children('.active');
            var group = $trigger.data().validate;
            var groupId = $trigger.parents('.content').attr('id');
            var $groupStep = isNextBtn ? $("[data-target=\"#".concat(groupId, "\"]")) : $trigger;
            $('#stepper-form').parsley().on('form:validate', function (formInstance) {
                var isValid = formInstance.isValid({
                    group: group
                }); // normalize states
                var check_promise = new Promise((resolve, reject) => {
                    if (isValid) {
                        if (window.edit_spec_form != undefined) {
                            var form_dom = $("#spec_from_div form");
                            var form_data = form_dom.data("form_data");
                            if (form_data['pk'] == undefined) {
                                window.edit_spec_form.save_data(trigger).then((flag) => {
                                    resolve(flag);
                                });
                            } else
                                resolve(true);
                        } else
                            resolve(true);
                    } else {
                        resolve(false);
                    }
                });
                $groupStep.removeClass('success error'); // give step item a validate state
                check_promise.then((flag) => {
                    if (flag) {
                        $groupStep.addClass('success'); // go to next step or submit
                        if ($trigger.hasClass('submit')) {
                            $('#submitfeedback').toast('show');
                            console.log($('#stepper-form').serializeArray());
                        } else if (isNextBtn) {
                            stepperDemo.next();
                        } else {
                            stepperDemo.to(to + 1);
                        }
                    } else {
                        $groupStep.addClass('error');
                    }
                });
            }).validate({
                group: group
            }); // kill listener

            $('#stepper-form').parsley().off('form:validate');
        }
    }, {
        key: "handleValidations",
        value: function handleValidations() {
            var self = this; // validate on next buttons

            $('.next, .step-trigger').on('click', function () {
                self.validateBy(this);
            }); // prev buttons

            $('.prev').on('click', function () {
                var $trigger = $(this);
                var groupId = $trigger.parents('.content').attr('id');
                var $groupStep = $("[data-target=\"#".concat(groupId, "\"]")); // normalize states

                $groupStep.removeClass('success error');
                $groupStep.prev().removeClass('success error');
                stepperDemo.previous();
            }); // save creadit card

            $('#savecc').on('click', function () {
                $('#stepper-form').parsley().whenValidate({
                    group: 'creditcard'
                });
            }); // submit button

            $('.submit').on('click', function () {
                self.validateBy(this);
                return false;
            });
        }
    }, {
        key: "handleSteps",
        value: function handleSteps() {
            var selector = document.querySelector('#stepper');
            window.stepperDemo = new Stepper(selector, {
                linear: false,
                unbind_link_click: true
            });
        }
    }]);

    return stepsDemo;
}();
var SpecMaintain = function () {
    this.table = undefined;
    this.datatable = undefined;
    this.table_params_fun = undefined;
    this.need_init = false;
    this.edit_form = undefined;
    var maintain_ctr = undefined;
    var self = this;
    var remarkShowLength = 10;//默认现实的字符串长度
    this.init = function () {
        maintain_ctr = $("#spec-l-5 .field-section");
        self.init_edit_form();
        self.bind_event();
    }
    this.init_edit_form = function () {
        let form1 = new SWForm("#edit_spec_maintain .modal-body", "", "url", "GET", false);
        form1.addComponent(new SWText("mi001", "hidden"));
        form1.addComponent(new SWText("mi002", "hidden"));
        var mi003 = new SWText('mi003', "text", gettext('SeqNo'));
        mi003.input_dom.attr("readonly", "readonly");
        form1.addComponent(mi003);
        var mi004 = new SWTextarea("mi004", gettext('Description'), 3).setAutoSize(true);
        form1.addComponent(mi004);
        form1.addComponent(new SWText('mi005', "text", gettext('TaskID')).setMaxLength(50));
        form1.addComponent(new SWText('mi006', "text", gettext('Contact')).setMaxLength(10));
        form1.addComponent(new SWText('mi007', "text", gettext('BDate')).setMaxLength(17));
        form1.addComponent(new SWText('mi008', "number", gettext('FDay')).setMaxLength(10));
        form1.addComponent(new SWText('mi009', "number", gettext('FTime')).setMaxLength(10));
        form1.addComponent(new SWText('mi011', "text", gettext('Par.Function')).setMaxLength(500));
        form1.dom.find(".card-header").hide();
        form1.dom.find(".card-footer").hide();
        form1.dom.find(".page-inner").addClass("p-0");
        form1.create_url = "/devplat/spec/docmi/create"
        form1.update_url = "/devplat/spec/docmi/update?pk=[[pk]]"
        form1.on_after_save = function (data) {
            $("#edit_spec_maintain").modal("hide");
            self.datatable.search("").draw();
        }
        form1.on_after_init = function (data) {
            $("#edit_spec_maintain textarea").trigger("change");
        }
        self.edit_form = form1;
        $("#edit_spec_maintain .new_save").on("click", function () {
            self.edit_form.save_data($(this));
        });
    }

    this.init_table = function () {
        var table = new SWDataTable("#spec-l-5 .field-section", "spec_maintain_table"); //創建SWDataTable對象
        table.paging = false;
        table.searching = false;  //設置不顯示查詢框
        //設置DataTable顯示5個字段，分別是taskno, task,contact, planbdate, planedate
        table.columns = [
            { field: "mi003", label: gettext('SeqNo') },
            { field: "mi004", label: gettext('Description') },
            { field: "mi005", label: gettext('TaskID') },
            { field: "mi006", label: gettext('Contact') },
            { field: "mi007", label: gettext('BDate'), render: SWDataTable.DateRender },
            { field: "mi008", label: gettext('FDay') },
            { field: "mi009", label: gettext('FTime') },
            { field: "mi011", label: gettext('Par.Function') },
            {
                field: "operation", label: gettext('Operation'),
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
                { "responsivePriority": 1, width: "100px", "className": "all", "targets": 0 },
                { "responsivePriority": 2, "className": "all", "targets": 1 },
                { "responsivePriority": 3, width: "100px", "className": "min-tablet-p", "targets": 2 },
                { "responsivePriority": 4, width: "100px", "className": "min-tablet-p", "targets": 3 },
                { "responsivePriority": 5, width: "100px", "className": "min-tablet-p", "targets": 4 },
                { "responsivePriority": 6, width: "100px", "className": "min-tablet-p", "targets": 5 },
                { "responsivePriority": 7, width: "100px", "className": "min-tablet-p", "targets": 6 },
                { "responsivePriority": 8, width: "100px", "className": "min-tablet-p", "targets": 7 },
            ],
            deferLoading: 0
        });
        table.custom_params_fun = function () {
            if (self.table_params_fun != null)
                return self.table_params_fun();
            else
                return {
                    attach_query: `{"condition":"AND","rules":[{"id":"mi001","field":"mi001","type":"string","input":"text","operator":"equal","value":"dddddddc"},
                {"id":"mi002","field":"mi002","type":"string","input":"text","operator":"equal","value":"0000"}],"not":false,"valid":true}`};
        }
        self.table = table;
        self.datatable = table.init("/devplat/spec/edit/docmi_list")
        $("#spec_maintain_table_wrapper").on("click", ".btn-edit", function () {
            var id = $(this).attr("id");
            self.edit_form.set_pk(id);
            self.edit_form.init_data();
            $("#edit_spec_maintain textarea").change();
            $("#edit_spec_maintain").modal("show");
        });
    }
    this.bind_event = function () {
        $("#add_maintain_function").on("click", function () {
            var ma001 = $("#spec-l-1 .field-section input[name='ma001']").val();
            var ma002 = $("#spec-l-1 .field-section input[name='ma002']").val();
            var params = { mi001: ma001, mi002: ma002 }
            self.edit_form.set_pk(undefined);
            self.edit_form.init_data(params);
            $("#edit_spec_maintain").modal("show");
        });
        $("#spec-l-5 .field-section").on("click", ".del-btn", function () {
            var id = $(this).attr("id");
            if (confirm('Are you sure you want to delete this data?')) {
                var id = $(this).attr("id")
                var url = `/devplat/spec/docmi/delete/${id}`;
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
var SpecLogical = function () {
    this.table = undefined;
    this.datatable = undefined;
    this.table_params_fun = undefined;
    this.need_init = false;
    this.edit_form = undefined;
    var logical_ctr = undefined;
    var self = this;
    this.init = function () {
        logical_ctr = $("#spec-l-3 .field-section");
        self.init_edit_form();
        self.bind_event();
    }
    this.init_edit_form = function () {
        let form1 = new SWForm("#edit_spec_logical .modal-body", "", "url", "GET", false);
        form1.addComponent(new SWText("mj001", "hidden"));
        form1.addComponent(new SWText("mj002", "hidden"));
        var mj003 = new SWText('mj003', "text", gettext('SeqNo'));
        mj003.input_dom.attr("readonly", "readonly");
        form1.addComponent(mj003);
        var mj004 = new SWTextarea("mj004", gettext('Description'), 3).setAutoSize(true);
        form1.addComponent(mj004);
        form1.addComponent(new SWText('mj005', "text", gettext('Type')).setMaxLength(300));
        form1.addComponent(new SWText('mj006', "text", gettext('Par.Function')).setMaxLength(500));
        form1.dom.find(".card-header").hide();
        form1.dom.find(".card-footer").hide();
        form1.dom.find(".page-inner").addClass("p-0");
        form1.create_url = "/devplat/spec/docmj/create"
        form1.update_url = "/devplat/spec/docmj/update?pk=[[pk]]"
        form1.on_after_save = function (data) {
            $("#edit_spec_logical").modal("hide");
            self.datatable.search("").draw();
        }
        form1.on_after_init = function (data) {
            $("#edit_spec_logical textarea").trigger("change");
        }
        self.edit_form = form1;
        $("#edit_spec_logical .new_save").on("click", function () {
            self.edit_form.save_data($(this));
        });
    }

    this.init_table = function () {
        var table = new SWDataTable("#spec-l-4 .field-section", "spec_logical_table"); //創建SWDataTable對象
        table.paging = false;
        table.searching = false;  //設置不顯示查詢框
        //設置DataTable顯示5個字段，分別是taskno, task,contact, planbdate, planedate
        table.columns = [
            { field: "mj003", label: gettext('SeqNo') },
            { field: "mj004", label: gettext('Description') },
            { field: "mj005", label: gettext('Type') },
            { field: "mj006", label: gettext('Par.Function') },
            {
                field: "operation", label: gettext('Operation'),
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
                { "responsivePriority": 1, width: "100px", "className": "all", "targets": 0 },
                { "responsivePriority": 2, "className": "min-tablet-p", "targets": 1 },
                { "responsivePriority": 3, width: "150px", "className": "min-tablet-p", "targets": 2 },
                { "responsivePriority": 4, width: "100px", "className": "min-tablet-p", "targets": 3 },
            ],
            deferLoading: 0
        });
        table.custom_params_fun = function () {
            if (self.table_params_fun != null)
                return self.table_params_fun();
            else
                return {
                    attach_query: `{"condition":"AND","rules":[{"id":"mj001","field":"mj001","type":"string","input":"text","operator":"equal","value":"dddddddc"},
                {"id":"mj002","field":"mj002","type":"string","input":"text","operator":"equal","value":"0000"}],"not":false,"valid":true}`};
        }
        self.table = table;
        self.datatable = table.init("/devplat/spec/edit/docmj_list")
        $("#spec_logical_table_wrapper").on("click", ".btn-edit", function () {
            var id = $(this).attr("id");
            self.edit_form.set_pk(id);
            self.edit_form.init_data();
            $("#edit_spec_logical textarea").change();
            $("#edit_spec_logical").modal("show");
        });
    }
    this.bind_event = function () {
        $("#add_logical_function").on("click", function () {
            var ma001 = $("#spec-l-1 .field-section input[name='ma001']").val();
            var ma002 = $("#spec-l-1 .field-section input[name='ma002']").val();
            var params = { mj001: ma001, mj002: ma002 }
            self.edit_form.set_pk(undefined);
            self.edit_form.init_data(params);
            $("#edit_spec_logical").modal("show");
        });
        $("#spec-l-4 .field-section").on("click", ".del-btn", function () {
            var id = $(this).attr("id");
            if (confirm('Are you sure you want to delete this data?')) {
                var id = $(this).attr("id")
                var url = `/devplat/spec/docmj/delete/${id}`;
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
var SpecInstructions = function () {
    this.table = undefined;
    this.datatable = undefined;
    this.table_params_fun = undefined;
    this.need_init = false;
    this.edit_form = undefined;
    var inst_ctr = undefined;
    var self = this;
    this.init = function () {
        inst_ctr = $("#spec-l-3 .field-section");
        self.init_edit_form();
        self.bind_event();
    }   
    this.init_edit_form = function() {
        let form1 = new SWForm("#edit_spec_inst .modal-body", "", "url", "GET", false);
        form1.addComponent(new SWText("mb001", "hidden"));
        form1.addComponent(new SWText("mb002", "hidden"));
        var mb003 = new SWText('mb003', "text", gettext('SeqNo'));
        mb003.input_dom.attr("readonly", "readonly");
        form1.addComponent(mb003);
        form1.addComponent(new SWCombobox("mb004",gettext('OI Type'), [{value:"A", label:"1.主界面"},{value:"B", label:"2:操作說明"}]));
        var mb007 = new SWTextarea("mb007",gettext('OI'), 2).setAutoSize(true);
        form1.addComponent(mb007);       
        form1.addComponent(new SWText('mb015', "text", gettext('Par.Function')).setMaxLength(500));       
        form1.layout.append(`<div class="form-group" style="">
                    <input class="mb012_input" name="mb012" type="file"  accept="image/jpg" style="display:none">
                    <label class="col-form-label caption" for="tf6">圖片說明(支持粘貼圖片到此處,點擊圖片區域上傳)</label>
                    <image src="" class="mb012_img"/>
                    </div>`);
        form1.dom.find(".card-header").hide();
        form1.dom.find(".card-footer").hide();
        form1.dom.find(".page-inner").addClass("p-0");
        form1.create_url = "/devplat/spec/docmb/create"
        form1.update_url = "/devplat/spec/docmb/update?pk=[[pk]]"
        form1.on_after_save = function (data) {
            $("#edit_spec_inst").modal("hide");
            self.datatable.search("").draw();
        }
        form1.on_after_init = function (data) {
            $("#edit_spec_inst textarea").trigger("change");
            $("#edit_spec_inst .mb012_input").val(null);
            if (data.inc_id == undefined || data.inc_id == "")
                $("#edit_spec_inst .mb012_img").attr("src", "")
            else
                $("#edit_spec_inst .mb012_img").attr("src", `/devplat/spec/docmb/show_image?pk=${data.inc_id}`);
            
        }
        self.edit_form = form1;
        $("#edit_spec_inst .new_save").on("click", function () {
            self.edit_form.save_data($(this));
        });
    }

    this.init_table = function () {
        var table = new SWDataTable("#spec-l-3 .field-section", "spec_inst_table"); //創建SWDataTable對象
        table.paging = false;
        table.searching = false;  //設置不顯示查詢框
        //設置DataTable顯示5個字段，分別是taskno, task,contact, planbdate, planedate
        table.columns = [
           {field: "mb003", label: gettext('SeqNo')},
           {field:"mb004", label:gettext('Description'), render:function(data, type, row) {
                if (data == "A")
                    return `1.主界面`;
                else if (data == "B")
                    return "2:操作說明";
                else
                    return data;
           }},
           {field: "mb007", label: gettext('OI')},
           {field:"company", label:gettext('Picture Help'),render:function(data, type, row){
            return `<a href="#" class="img_link" link="/devplat/spec/docmb/show_image?pk=${row.inc_id}"><i class="fas fa-image"></i></a>`
           }},
           {field: "mb015", label: gettext('Par.Function')},
           {
            field: "operation", label: gettext('Operation'),
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
                {"responsivePriority": 1, width:"100px","className":"all", "targets": 0 },
                {"responsivePriority": 2, width:"100px","className":"all", "targets": 1 },
                {"responsivePriority": 3, "className":"min-tablet-p", "targets": 2 },
                {"responsivePriority": 4, width:"80px","className":"min-tablet-p", "targets": 3 },
                {"responsivePriority": 5, width:"150px", "className":"min-tablet-p lb-a", "targets": 4 },
                {"responsivePriority": 5, width:"100px", "className":"min-tablet-p", "targets": 5 },
            ],
            deferLoading: 0
        });
        table.custom_params_fun = function () {
            if (self.table_params_fun != null)
                return self.table_params_fun();
            else
                return {
                    attach_query: `{"condition":"AND","rules":[{"id":"mb001","field":"mb001","type":"string","input":"text","operator":"equal","value":"dddddddc"},
                {"id":"mb002","field":"mb002","type":"string","input":"text","operator":"equal","value":"0000"}],"not":false,"valid":true}`};
        }
        self.table = table;
        self.datatable = table.init("/devplat/spec/edit/docmb_list")
        $("#spec_inst_table_wrapper").on("click", ".btn-edit", function () {
            var id = $(this).attr("id");
            self.edit_form.set_pk(id);
            self.edit_form.init_data();
            $("#edit_spec_inst textarea").change();
            $("#edit_spec_inst").modal("show");
        });
    }
    this.bind_event = function () {
        $("#add_inst_function").on("click", function () {
            var ma001 = $("#spec-l-1 .field-section input[name='ma001']").val();
            var ma002 = $("#spec-l-1 .field-section input[name='ma002']").val();
            var params = { mb001: ma001, mb002: ma002 }
            self.edit_form.set_pk(undefined);
            self.edit_form.init_data(params);
            $("#edit_spec_inst").modal("show");
        });
        $("#spec-l-3 .field-section").on("click", ".del-btn", function () {
            var id = $(this).attr("id");
            if (confirm('Are you sure you want to delete this data?')) {
                var id = $(this).attr("id")
                var url = `/devplat/spec/docmb/delete/${id}`;
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
        $("#edit_spec_inst .mb012_img").on("click", function(e) {
            $("#edit_spec_inst .mb012_input").click();
        })
        $("#edit_spec_inst .mb012_input").on("change", function(e){
            const file = e.target.files[0];
            const fr = new FileReader();
            fr.onload = function (e) {
                $("#edit_spec_inst .mb012_img").attr("src", e.target.result);
            };    
            fr.readAsDataURL(file);
        });             
        window.addEventListener('paste', e => {
            if ($("#edit_spec_inst .mb012_img").is(":visible")) {
                $("#edit_spec_inst .mb012_input")[0].files = e.clipboardData.files;
                $("#edit_spec_inst .mb012_input").change();
            }
        });
        $("#spec-l-3 .field-section").on("click",".img_link", function(e){
            e.preventDefault();
			if($("#image-Modal").hasClass("show")==false){
				if ($("#image-Modal img").attr("src")!=$(this).attr("link")) {
					$("#image-Modal img").attr("src",$(this).attr("link"))
				}
				$("#image-Modal").modal("show");
			}
        });
    }
}
var SpecFunction = function () {
    this.table = undefined;
    this.datatable = undefined;
    this.table_params_fun = undefined;
    this.need_init = false;
    this.edit_form = undefined;
    this.TechRequirement = undefined;
    var func_ctr = undefined;
    var self = this;
    this.init = function () {
        func_ctr = $("#spec-l-2 .field-section");
        self.TechRequirement = new TechRequirement();
        self.TechRequirement.init();
        self.init_edit_form();
        self.bind_event();
    }
    this.init_edit_form = function () {
        let form1 = new SWForm("#edit_spec_func .modal-body", "", "url", "GET", false);
        form1.addComponent(new SWText("mh001", "hidden"));
        form1.addComponent(new SWText("mh002", "hidden"));
        var mh003 = new SWText('mh003', "text", gettext('SeqNo'));
        mh003.input_dom.attr("readonly", "readonly");
        form1.addComponent(mh003);
        var mh004 = new SWTextarea('mh004', gettext('Description'), 1).setAutoSize(true);
        form1.addComponent(mh004);
        form1.addComponent(new SWText('mh005', "text", gettext('Type')).setMaxLength(300));
        form1.dom.find(".card-header").hide();
        form1.dom.find(".card-footer").hide();
        form1.dom.find(".page-inner").addClass("p-0");
        form1.create_url = "/devplat/spec/docmh/create"
        form1.update_url = "/devplat/spec/docmh/update?pk=[[pk]]"
        form1.on_after_save = function (data) {
            $("#edit_spec_func").modal("hide");
            self.datatable.search("").draw();
        }
        form1.on_after_init = function (data) {
            $("#edit_spec_func textarea").trigger("change");
        }
        self.edit_form = form1;
        $("#edit_spec_func .new_save").on("click", function () {
            self.edit_form.save_data($(this));
        });
    }

    this.init_table = function () {
        var table = new SWDataTable("#spec-l-2 .field-section", "spec_func_table"); //創建SWDataTable對象
        table.paging = false;
        table.searching = false;  //設置不顯示查詢框
        //設置DataTable顯示5個字段，分別是taskno, task,contact, planbdate, planedate
        table.columns = [
           {field: "mh003", label: gettext('SeqNo')},
           {field:"mh004", label:gettext('Description')},
           {field: "mh005", label: gettext('Type')},
           {
            field: "operation", label: gettext('Operation'),
            render: function (data, type, row) {
                var id = row.DT_RowId;
                var hastr = "btn-secondary"
                if (row.hastr == 'N')
                    hastr = "btn-warning";
                return `<a class="btn btn-show-tecreq btn-sm btn-icon ${hastr}" href="#" id="${id}">TR</a>
                        <a class="btn btn-edit btn-sm btn-icon btn-secondary" href="#" id="${id}"><i class="fa fa-pencil-alt"></i></a>
                        <a class="btn del-btn btn-sm btn-icon btn-secondary" href="#" id="${id}"><i class="far fa-trash-alt"></i></a>`;
                }
            }
        ];
        //SWDataTable控件不支持的功能，可以使用原生jquery datatable的屬性設置
        table.setOptions({
            responsive: true,
            columnDefs: [
                { "responsivePriority": 1, width: "100px", "className": "all", "targets": 0 },
                { "responsivePriority": 2, "className": "all", "targets": 1 },
                { "responsivePriority": 3, width: "150px", "className": "min-tablet-p", "targets": 2 },
                { "responsivePriority": 4, width: "100px", "className": "min-tablet-p", "targets": 3 },
            ],
            deferLoading: 0
        });
        table.custom_params_fun = function () {
            if (self.table_params_fun != null)
                return self.table_params_fun();
            else
                return {
                    attach_query: `{"condition":"AND","rules":[{"id":"mh001","field":"mh001","type":"string","input":"text","operator":"equal","value":"dddddddc"},
                {"id":"mh002","field":"mh002","type":"string","input":"text","operator":"equal","value":"0000"}],"not":false,"valid":true}`};
        }
        self.table = table;
        self.datatable = table.init("/devplat/spec/edit/docmh_list")
        $("#spec_func_table_wrapper").on("click", ".btn-edit", function () {
            var id = $(this).attr("id");
            self.edit_form.set_pk(id);
            self.edit_form.init_data();
            $("#edit_spec_func textarea[name='mh004']").change();
            $("#edit_spec_func").modal("show");
        });
    }

    this.bind_event = function () {
        $("#add_spec_function").on("click", function () {
            var ma001 = $("#spec-l-1 .field-section input[name='ma001']").val();
            var ma002 = $("#spec-l-1 .field-section input[name='ma002']").val();
            var params = { mh001: ma001, mh002: ma002 }
            self.edit_form.set_pk(undefined);
            self.edit_form.init_data(params);
            $("#edit_spec_func").modal("show");
        });
        $("#spec-l-2 .field-section").on("click", ".del-btn", function () {
            var id = $(this).attr("id");
            if (confirm('Are you sure you want to delete this data?')) {
                var id = $(this).attr("id")
                var url = `/devplat/spec/docmh/delete/${id}`;
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
        $("#spec-l-2 .field-section").on("click", ".btn-show-tecreq", function () {
            var row_tr = $(this).closest("tr")
            if (row_tr.hasClass("child"))
                row_tr = row_tr.prev()[0];
            var row = self.datatable.row(row_tr).data();
            self.TechRequirement.show_tecreq({specname:row.mh001, verno:row.mh002, funcitemno:row.mh003});
        });
    }
}
var SpecForm = function () {
    this.form = undefined;
    this.ma001 = undefined;
    this.ma002 = undefined;
    this.ma003 = undefined;
    this.ma026 = undefined;
    this.ma004 = undefined;
    var basic_ctr = undefined;
    var func_ctr = undefined;
    var inst_ctr = undefined;
    var logical_ctr = undefined;
    var maintain_ctr = undefined;
    this.system_tree_grid = undefined;
    this.SpecFunction = undefined;
    this.SpecInstructions = undefined;
    this.SpecLogical = undefined;
    this.SpecMaintain = undefined;
    this.task_pk = undefined;
    this.showSpecAIDocument = undefined;
    var self = this;
    this.init = function () {
        basic_ctr = $("#spec-l-1 .field-section")
        func_ctr = $("#spec-l-2 .field-section")
        inst_ctr = $("#spec-l-3 .field-section")
        logical_ctr = $("#spec-l-4 .field-section")
        maintain_ctr = $("#spec-l-5 .field-section")
        self.SpecFunction = new SpecFunction();
        self.SpecFunction.init();
        self.SpecInstructions = new SpecInstructions();
        self.SpecInstructions.init();
        self.SpecLogical = new SpecLogical();
        self.SpecLogical.init();
        self.SpecMaintain = new SpecMaintain();
        self.SpecMaintain.init();
        self.init_edit_form();
        self.init_select_system();
        self.bind_event();
    }
    this.init_edit_form = function () {
        var row = new SWRow();
        self.ma001 = new SWText("ma001", "text", gettext('ProgramNo')).setMaxLength(50);
        row.addComponent(self.ma001)
        self.ma002 = new SWText("ma002", "text", gettext('EditionID'));
        self.ma002.input_dom.attr("readonly", "readonly");
        row.addComponent(self.ma002)
        self.ma003 = new SWText("ma003", "text", gettext('Program Name')).setMaxLength(150);
        row.addComponent(self.ma003);
        basic_ctr.append(row.dom);
        row = new SWRow();
        row.addComponent(new SWText("ma007", "text", gettext('TaskID')).setMaxLength(20));
        row.addComponent(new SWText("ma013", "text", gettext('User Department')).setMaxLength(20));
        row.addComponent(new SWText("ma014", "text", gettext('Job')).setMaxLength(100));
        basic_ctr.append(row.dom)
        row = new SWRow();
        self.ma026 = new SWText("ma026", "text", gettext('System'));
        self.ma026.input_dom.attr("readonly", "readonly");
        row.addComponent(self.ma026)
        self.ma004 = new SWText("ma004", "text", gettext('SubSys'));
        self.ma004.input_dom.attr("readonly", "readonly");
        row.addComponent(self.ma004);
        self.task_pk = new SWText("task_pk", "text", gettext('Select Task'),);
        row.addComponent(self.task_pk);
        basic_ctr.append(row.dom)
        basic_ctr.append(new SWTextarea("ma015", gettext('Pre-processing'), 3).setAutoSize(true).setMaxLength(8000).dom);
        basic_ctr.append(new SWTextarea("ma016", gettext('Necessary Step'), 1).setAutoSize(true).setMaxLength(100).dom);
        basic_ctr.append(new SWTextarea("ma018", gettext('Frame Descp'), 5).setAutoSize(true).dom);
        basic_ctr.append(new SWTextarea("ma017", gettext('Method Call'), 1).setAutoSize(true).setMaxLength(100).dom);
        $(basic_ctr).find("input[name='task_pk']").attr("placeholder",gettext('Please select task after you have saved'))
        if (SWApp.os.isMobile) {
            $("#spec_edit .SWRow div[class*='div-']").addClass("col-12");
            $("#spec_edit .SWRow div[class*='div-']").addClass("p-0");
        }

        var form = new SWBaseForm("#spec_from_div");
        form.create_url = "/devplat/spec/create";
        form.update_url = "/devplat/spec/update?pk=[[pk]]";
        form.pk_in_url = false;
        form.on_after_init = function (data) {
            $("#spec_from_div textarea").trigger("change");
        }
        form.on_init_format = function (data) {
            self.SpecFunction.need_init = true;
            self.SpecInstructions.need_init = true;
            self.SpecLogical.need_init = true;
            self.SpecMaintain.need_init = true;
            stepperDemo.reset();
            self.showSpecAIDocument = new SWAIComBox('#showSpecAIDocument', "showSpecAIDocument_AIComBox");
        }
        self.form = form;
        window.edit_spec_form = form;
    }
    window.check_spec_edit_form_save = async function (target) {
        let result = true;
        if (window.edit_spec_form != undefined) {
            var form_dom = $("#spec_from_div form");
            var form_data = form_dom.data("form_data");
            if (form_data['pk'] == undefined) {
                result = await window.edit_spec_form.save_data(target);
            }
        }
        return result;
    }
    this.init_select_system = function () {
        var tree_grid = new SWTreegrid("#select_system .data_wrapper");
        tree_grid.idField = "sysid";
        tree_grid.selected = true;
        tree_grid.parentIdField = "parentid";
        tree_grid.columns = [
            {
                field: 'sysremark', label: gettext('Description'), render: (value, row, index) => {
                    return `<span sysname="${row.sysname}">${value}</span>`;
                }
            },
            //{field: 'sys',label: '系統名稱',sortable: true,width: '170',visible:!SWApp.os.isMobile},
            { field: 'sysid', label: gettext('SysNO'), sortable: true, align: 'center', width: '100', visible: !SWApp.os.isMobile }
        ];
        tree_grid.setOptions({
            showColumns: false,
            singleSelect: true
        })
        tree_grid.init("/devplat/spec/get_system");
        self.system_tree_grid = tree_grid;
    }
    this.bind_event = function () {
        self.task_pk.input_dom.on("click", function () {
            var udf04 = $("#stepper-form input[name='ma001']").val();
            var session =  $("#stacked-menu li.has-active").attr("sessionid");
            var session_id =session.trim().split("-");
            var session_pid = session_id[0];
            var session_tid = session_id[1];
            var table_taskID = new SWSelectquery(self.task_pk.input_dom);
            table_taskID.table.columns = [
                { "field": "taskid", "label": gettext('Task') ,render:function(data){return `${session}-${data}`}},
                { "field": "modifier", "label": gettext('Modifier') },
                { "field": "task", "label": gettext('TaskDescriptions') },
                { "field": "contact", "label": gettext('Contact') },
                { "field": "udf04", "label": gettext('ProgramNo'), render: function (data) { if (data === null) return ""; return data } },
            ]
            table_taskID.height(600);
            if (SWApp.os.isMobile) {
                table_taskID.width("auto");
            } else {
                table_taskID.width(1100);
            }
            table_taskID.datasource = `/devplat/select_TaskID?pid=${session_pid}&tid=${session_tid}`;
            table_taskID.on_selected_event = function (data) {
                var ajax_data = {};
                ajax_data['udf04'] = udf04;
                ajax_data['pid'] = session_pid;
                ajax_data['tid'] = session_tid;
                ajax_data['taskid'] = data.taskid;
                self.task_pk.input_dom.val(`${session_pid}-${session_tid}-${data.taskid}`);
                self.task_pk.input_dom.attr("readonly","readonly");
                $.ajax({
                    type: "POST",
                    url: '/devplat/save_docwin',
                    data: ajax_data,
                    beforeSend: function (request) {
                        request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    },
                    success: function (result) {
                    }
                })
            }
        })
        self.ma001.input_dom.on("change", function () {
            var local_self = $(this);
            var value = $(this).val();
            if (value != "") {
                var url = "/devplat/spec/edit/get_max_verno?sepc_no={0}".format(value);
                $.get(url, function (result) {
                    if (result.status) {
                        self.ma002.input_dom.val(result.data);
                    } else {
                        SWApp.popoverMsg(local_self, "獲取最大版本號失敗")
                    }
                })
            }
        });
        self.ma026.input_dom.on("click", function () {
            $("#select_system .SWTreegrid").treegrid('collapseAll');
            $("#select_system").modal("show");
        });
        $("#select_system .btn-selected").on("click", function (e) {
            var selected_row = $("#select_system tr.selected");
            if (selected_row.length == 0) {
                SWApp.popoverMsg($(this), "請選擇數據");
            } else {
                var row = $(selected_row[0]);
                var sysname = row.find("td:eq(1)").find("span[sysname]").attr("sysname")
                var sysid = row.find("td:eq(2)").text();
                self.ma026.input_dom.val(sysname.trim());
                self.ma004.input_dom.val(sysid.trim());
                $("#select_system").modal("hide");
            }
        });
        $("#spec_edit #stepper")[0].addEventListener('shown.bs-stepper', function (event) {
            if (event.detail.indexStep == 1) {
                if (self.SpecFunction.table == undefined)
                    self.SpecFunction.init_table();
                var ma001 = self.ma001.input_dom.val();
                var ma002 = self.ma002.input_dom.val();
                if (self.SpecFunction.need_init) {
                    self.SpecFunction.table_params_fun = function () {
                        return {
                            attach_query: `{"condition":"AND","rules":[{"id":"mh001","field":"mh001","type":"string","input":"text","operator":"equal","value":"${ma001}"},
                        {"id":"mh002","field":"mh002","type":"string","input":"text","operator":"equal","value":"${ma002}"}],"not":false,"valid":true}`
                        };
                    }
                    self.SpecFunction.datatable.search("").draw();
                    self.SpecFunction.need_init = false;
                    $("#stepper-form input[name='task_pk']").removeAttr("disabled");
                }
            } else if (event.detail.indexStep == 2) {
                if (self.SpecInstructions.table == undefined)
                    self.SpecInstructions.init_table();
                var ma001 = self.ma001.input_dom.val();
                var ma002 = self.ma002.input_dom.val();
                if (self.SpecInstructions.need_init) {
                    self.SpecInstructions.table_params_fun = function () {
                        return {
                            attach_query: `{"condition":"AND","rules":[{"id":"mb001","field":"mb001","type":"string","input":"text","operator":"equal","value":"${ma001}"},
                        {"id":"mb002","field":"mb002","type":"string","input":"text","operator":"equal","value":"${ma002}"}],"not":false,"valid":true}`
                        };
                    }
                    self.SpecInstructions.datatable.search("").draw();
                    self.SpecInstructions.need_init = false;
                    $("#stepper-form input[name='task_pk']").removeAttr("disabled");
                }
            } else if (event.detail.indexStep == 3) {
                if (self.SpecLogical.table == undefined)
                    self.SpecLogical.init_table();
                var ma001 = self.ma001.input_dom.val();
                var ma002 = self.ma002.input_dom.val();
                if (self.SpecLogical.need_init) {
                    self.SpecLogical.table_params_fun = function () {
                        return {
                            attach_query: `{"condition":"AND","rules":[{"id":"mj001","field":"mj001","type":"string","input":"text","operator":"equal","value":"${ma001}"},
                        {"id":"mj002","field":"mj002","type":"string","input":"text","operator":"equal","value":"${ma002}"}],"not":false,"valid":true}`
                        };
                    }
                    self.SpecLogical.datatable.search("").draw();
                    self.SpecLogical.need_init = false;
                    $("#stepper-form input[name='task_pk']").removeAttr("disabled");
                }
            } else if (event.detail.indexStep == 4) {
                if (self.SpecMaintain.table == undefined)
                    self.SpecMaintain.init_table();
                var ma001 = self.ma001.input_dom.val();
                var ma002 = self.ma002.input_dom.val();
                if (self.SpecMaintain.need_init) {
                    self.SpecMaintain.table_params_fun = function () {
                        return {
                            attach_query: `{"condition":"AND","rules":[{"id":"mi001","field":"mi001","type":"string","input":"text","operator":"equal","value":"${ma001}"},
                        {"id":"mi002","field":"mi002","type":"string","input":"text","operator":"equal","value":"${ma002}"}],"not":false,"valid":true}`
                        };
                    }
                    self.SpecMaintain.datatable.search("").draw();
                    self.SpecMaintain.need_init = false;
                    $("#stepper-form input[name='task_pk']").removeAttr("disabled");
                }
            }
        });
        $("#spec_edit").on("click", "#spec_q_ai_btn", this.questionWithAI);        
    }
    this.questionWithAI = function () {
    var form_dom = $("#spec_from_div form");
    var form_data = form_dom.data("form_data");
    if (form_data['pk'] == undefined) {
        alert("Please save your data before asking Ai questions!");
        return;
    }
    var frameSpecification =  form_dom.serializeObject();
    var ma001 = self.ma001.input_dom.val();
    var ma002 = self.ma002.input_dom.val();

    // Define parameters for AJAX requests
    var paramsMH = {
        draw: 0,
        length: -1,
        start: 0,
        attach_query: `{"condition":"AND","rules":[{"id":"mh001","field":"mh001","type":"string","input":"text","operator":"equal","value":"${ma001}"},{"id":"mh002","field":"mh002","type":"string","input":"text","operator":"equal","value":"${ma002}"}],"not":false,"valid":true}`
    };
    var paramsMB = {
        draw: 0,
        length: -1,
        start: 0,
        attach_query: `{"condition":"AND","rules":[{"id":"mb001","field":"mb001","type":"string","input":"text","operator":"equal","value":"${ma001}"},{"id":"mb002","field":"mb002","type":"string","input":"text","operator":"equal","value":"${ma002}"}],"not":false,"valid":true}`
    };
    var paramsMI = {
        draw: 0,
        length: -1,
        start: 0,
        attach_query: `{"condition":"AND","rules":[{"id":"mi001","field":"mi001","type":"string","input":"text","operator":"equal","value":"${ma001}"},{"id":"mi002","field":"mi002","type":"string","input":"text","operator":"equal","value":"${ma002}"}],"not":false,"valid":true}`
    };
    var paramsMJ = {
        draw: 0,
        length: -1,
        start: 0,
        attach_query: `{"condition":"AND","rules":[{"id":"mj001","field":"mj001","type":"string","input":"text","operator":"equal","value":"${ma001}"},{"id":"mj002","field":"mj002","type":"string","input":"text","operator":"equal","value":"${ma002}"}],"not":false,"valid":true}`
    };
    // 添加docmc和docme數據獲取
    var paramsMC = {
        draw: 0,
        length: -1,
        start: 0,
        attach_query: `{"condition":"AND","rules":[{"id":"mc001","field":"mc001","type":"string","input":"text","operator":"equal","value":"${ma001}"},{"id":"mc002","field":"mc002","type":"string","input":"text","operator":"equal","value":"${ma002}"}],"not":false,"valid":true}`
    };
    
    var paramsME = {
        draw: 0,
        length: -1, 
        start: 0,
        attach_query: `{"condition":"AND","rules":[{"id":"me001","field":"me001","type":"string","input":"text","operator":"equal","value":"${ma001}"},{"id":"me002","field":"me002","type":"string","input":"text","operator":"equal","value":"${ma002}"},
        {"id":"me008","field":"me008","type":"string","input":"text","operator":"is_not_null","value":""}
        ],"not":false,"valid":true}`
    };

    // Fetch data from relevant tables with correct parameters
    var functionList = $.get(`/devplat/spec/edit/docmh_list`, paramsMH);
    var instructionsList = $.get(`/devplat/spec/edit/docmb_list`, paramsMB);
    var maintainList = $.get(`/devplat/spec/edit/docmi_list`, paramsMI);
    var logicalList = $.get(`/devplat/spec/edit/docmj_list`, paramsMJ);
    var datatableList = $.get(`/devplat/spec/edit/docmc_list`, paramsMC); // docmc對應datatableList
    var flowchartList = $.get(`/devplat/spec/edit/docme_list`, paramsME); // docme對應flowchartList
    var externalProblems = $.get(`/devplat/spec/get_external_problems`, {ma001:ma001,ma002:ma002}); // 从/spec/get_external_problems读取系统问题上报数据

    $.when(functionList, instructionsList, logicalList, maintainList, datatableList, flowchartList,externalProblems).done(function(functionData, instructionsData, logicalData, maintainData, datatableData, flowchartData,externalProblems) {
        var consolidatedData = {
            frameSpecification:frameSpecification,
            functions: functionData[0].data,
            instructions: instructionsData[0].data,
            logicDescriptions: logicalData[0].data,
            maintenanceRecords: maintainData[0].data,
            // 添加docmc和docme数据
            datatableList: datatableData[0].data,  // docmc数据
            flowchartList: flowchartData[0].data,    // docme数据
            systemProblemReports: externalProblems[0].data // 添加系统问题上报数据
        };

        var documentInfo = JSON.stringify(consolidatedData, null, 2);

        // Send consolidated document information to AI
        self.showSpecAIDocument.sendDataToReact(documentInfo, 'documentData');
        self.showSpecAIDocument.show();
    });    
}
}
var Specification = function () {
    this.spec_table = undefined;
    this.spec_table_datatable = undefined;
    this.add_spec_btn = undefined;
    this.back_link = undefined;
    this.SpecForm = undefined;
    var self = this;
    this.init = function () {
        new stepsDemo();
        this.add_spec_btn = $("#add_spec");
        this.back_link = $("#spec_edit .back");
        this.bind_event();
        self.SpecForm = new SpecForm()
        self.SpecForm.init();
    }

    this.init_spec_table = function () {
        var table = new SWDataTable("#spec_table_container", "spec_table_table"); //創建SWDataTable對象
        table.searching = false;  //設置不顯示查詢框
        //設置DataTable顯示5個字段，分別是taskno, task,contact, planbdate, planedate 
        table.columns = [
            { field: "ma001", label: gettext('ProgramNo') },
            { field: "ma002", label: gettext('EditionID'), visible: false },
            { field: "ma003", label: gettext('Program Name') },
            //{field:"ma018", label:"窗口描述"},
            { field: "ma010", label: gettext('Modifier') },
            {
                field: "ma011", label: gettext('Modifly Date'), render:
                    function (data) {
                        if (data === null) return "";
                        return data.replace(/^(\d{4})(\d{2})(\d{2})$/, "$1-$2-$3");
                    }
            },
            {
                field: "operation", label: gettext('Operation'),
                render: function (data, type, row) {
                    var id = row.DT_RowId;
                    return `<a class="btn show_pdf" target="_blank" href="/devplat/spec/show_pdf?spec_id=${row.ma001}&spec_seq=${row.ma002}">
                    <i class="fas fa-file-pdf"></i></button>,
                    <a class="btn btn-edit btn-sm btn-icon btn-secondary" href="#" id="${id}"><i class="fa fa-pencil-alt"></i></a>`;
                }
            }
        ];
        //SWDataTable控件不支持的功能，可以使用原生jquery datatable的屬性設置
        table.setOptions({
            responsive: true,
            columnDefs: [
                { "responsivePriority": 1, "className": "all", "targets": 2 },
                { "responsivePriority": 2, "className": "min-tablet-p", "targets": 0 },
                { "responsivePriority": 3, "className": "min-tablet-p", "targets": 3 },
                { "responsivePriority": 4, "className": "min-tablet-p", "targets": 4 },
            ],
            deferLoading: 0
        });
        self.spec_table_datatable = table.init("/devplat/spec/list");
        self.spec_table = table;
    }

    this.bind_event = function() {
        this.add_spec_btn.on("click", function(){
            //check_login().then(()=>{
                $("#Specification .tech_title").text("Add Specification")
                self.SpecForm.form.set_pk(undefined);
                self.SpecForm.ma001.input_dom.removeAttr("readonly");
                $("#stepper-form input[name='task_pk']").attr("disabled","disabled");
                self.SpecForm.form.init_data();
                $("#Specification .nav-item a.nav-link[href='#spec_edit']").tab("show");
            //})
        });

        this.back_link.on("click", function (e) {
            e.preventDefault();
            $("#Specification .nav-item a.nav-link[href='#spec_table']").tab("show");
        })
        $("#spec_table_container").on("click",".btn-edit", function(){
            $("#Specification .tech_title").text("Edit Specification")
            var id = $(this).attr("id");
            self.SpecForm.form.set_pk(id)
            self.SpecForm.ma001.input_dom.attr("readonly", "readonly");
            self.SpecForm.form.init_data();
            $("#stepper-form input[name='task_pk']").removeAttr("disabled");
            $("#Specification .nav-item a.nav-link[href='#spec_edit']").tab("show");
        });
    }
}

window.addEventListener('message', function(event) {
    console.log('Message received:', event.data);
    if (event.data && event.data.type === 'SELECT_SPECIFICATION') {
        const framespecification = event.data.framespecification;

        // 延迟处理，以确保DOM已经完全加载
        setTimeout(() => {
            const rows = document.querySelectorAll('#spec_table_container tr');
            let found = false;

            rows.forEach(row => {
                if (row.textContent.includes(framespecification)) {
                    const editButton = row.querySelector('.btn-edit');
                    if (editButton) {
                        console.log('Clicking edit button for:', framespecification);
                        editButton.click();
                        found = true;
                    }
                }
            });

            if (!found) {
                console.log('Specification not found:', framespecification);
            }
        }, 1000); // 延迟1秒
    }
}, false);
