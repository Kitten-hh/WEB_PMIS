let debounceTimeout;
function Questions() {
    this.search = undefined; //搜索框
    this.content_search_btn = undefined; //全文搜索
    this.chatgpt_btn = undefined; //全文搜索
    this.search_btn = undefined; //搜索按鈕
    this.ai_search_cb = undefined; //是否ai search
    this.post_btn = undefined;//post
    this.technicTable = undefined
    this.technicTable_datatable = undefined
    this.test_search = undefined;
    this.search_skip_txt_arr = ['I','can','and','as','to','with','How'].map((a)=>a.toLowerCase());
    this.search_skip_txt_arr_cn = ["的","地"];
    var self = this;
    this.init = function () {
        //初始化搜索框
        var row = new SWRow()
        self.search = new SWTextarea("q_search", gettext('Question'), '7');
        
        $("#Questions>.row>div:first").append(self.search.dom);
        // $("label[for='tf6']").remove(); 
        self.search_btn = new SWButton('q_sea_btn', "btn-outline-primary", gettext("Search"));
        $("#Questions>.row>div").eq(1).find("div").append(self.search_btn.dom);
        self.content_search_btn = new SWButton('q_con_sea_btn', "btn-outline-primary", gettext("Research All"));
        self.content_search_btn.dom.addClass("mt-1");
        $("#Questions>.row>div").eq(1).find("div").append(self.content_search_btn.dom);

        
        self.chatgpt_btn = new SWButton('q_gpt_btn', "btn-outline-primary", gettext("ChatGPT"));
        self.chatgpt_btn.dom.addClass("mt-1");
        $("#Questions>.row>div").eq(1).find("div").append(self.chatgpt_btn.dom);

        self.post_btn = new SWButton('q_post_btn', "btn-outline-primary", gettext(" Post "));
        self.post_btn.dom.addClass("mt-1");
        $("#Questions>.row>div").eq(1).find("div").append(self.post_btn.dom);
        self.ai_search_cb = new SWCheckbox("ai_search", "Ai Search")
        $("#Questions>.row>div").eq(1).find("div").prepend(self.ai_search_cb.dom);
        self.init_advenced_search_dialog();
        self.bind_event();
        promiseGet("/PMIS/global/get_typelist?type_name=search_skip").then((result)=>{
            if(result.status && result.data.length > 0) {
                for(var row of result.data) {
                    var nfield = row.value;
                    if (nfield == "search_skip_txt")
                        self.search_skip_txt_arr = row.label.split(",").map((a)=>a.toLowerCase());
                    else if (nfield == "search_skip_txt")
                        self.search_skip_txt_arr_cn = row.label.split(",").map((a)=>a.toLowerCase());
                }
            }
        })
    }

    this.init_advenced_search_dialog = function () {
        self.test_search = new SWAdvancedsearch(self.search_btn.dom); //設置Search按鈕為觸發標籤
        var group = new SWAdvancedsearch.Group(SWAdvancedsearch.Condition.AND);
        var mb004 = new SWAdvancedsearch.Rule("mb004", SWAdvancedsearch.Type.STRING,
            SWAdvancedsearch.Operator.CONTAINS, gettext('Subject'));
        var mb005 = new SWAdvancedsearch.Rule("mb005", SWAdvancedsearch.Type.STRING,
            SWAdvancedsearch.Operator.CONTAINS, gettext('Contact'));
        var mb023 = new SWAdvancedsearch.Rule("technicalid_search", SWAdvancedsearch.Type.STRING,
            SWAdvancedsearch.Operator.CONTAINS, gettext('Technical Id'));
        var mb015 = new SWAdvancedsearch.Rule("mb015c", SWAdvancedsearch.Type.STRING,
            SWAdvancedsearch.Operator.CONTAINS, gettext('Category'));
        var mb016 = new SWAdvancedsearch.Rule("mb016", SWAdvancedsearch.Type.STRING,
            SWAdvancedsearch.Operator.CONTAINS, gettext('Area'));
        var mb019 = new SWAdvancedsearch.Rule("mb019", SWAdvancedsearch.Type.STRING,
            SWAdvancedsearch.Operator.CONTAINS, gettext('Compulsory'));

            
        var mb019 = new SWAdvancedsearch.Rule("udf03", SWAdvancedsearch.Type.STRING,
        SWAdvancedsearch.Operator.CONTAINS, gettext('Status'));
        group.addRule(mb004);
        group.addRule(mb005);
        group.addRule(mb023);
        group.addRule(mb015);
        group.addRule(mb016);
        group.addRule(mb019);
        self.test_search.addGroup(group);
        self.test_search.on_search_event = function (filter) {
            
            var quictfilter = JSON.parse(filter)
            if(quictfilter == null)
                quictfilter ={"condition":"AND","rules":[],"not":false,"valid":true}
            for(var item of quictfilter['rules']){
                if(item['id']=='technicalid_search'){
                    item['id']="mb023"
                    item['field']="mb023"
                } 
            }
            if($('#SWAdvancedsearch-Modal-1 .modal-body input[name="bmb006"]').val()!=''){
                quictfilter['rules'].push({"id": "mb006","field": "mb006","type": "string","input": "text",
                "operator": "greater_or_equal","value":$('#SWAdvancedsearch-Modal-1 .modal-body input[name="bmb006"]').val().replaceAll('-','')})
            }
            if($('#SWAdvancedsearch-Modal-1 .modal-body input[name="emb006"]').val()!=''){
                quictfilter['rules'].push({"id": "mb006","field": "mb006","type": "string","input": "text",
                "operator": "less_or_equal","value":$('#SWAdvancedsearch-Modal-1 .modal-body input[name="emb006"]').val().replaceAll('-','')})
            }
            //czz240919
            if($('#SWAdvancedsearch-Modal-1 .modal-body select[name="tec_status"]').val()!=''){
                quictfilter['rules'].push({"id": "udf03","field": "udf03","type": "string","input": "text",
                "operator": "equal","value":$('#SWAdvancedsearch-Modal-1 .modal-body select[name="tec_status"]').val()})
            }
            filter = JSON.stringify(quictfilter)

            self.technicTable.handle_response_fun = undefined;    
            $("#Technictable_info").closest(".row").show();        
            self.technicTable_datatable.search('form-search:' + filter).draw();
            $('#Technictable_filter input').val('')
        }

        
        
        var create_data = '<div class="form-group SWDate">'+
        '<label class="col-form-label caption">'+gettext('Create Date')+'</label><div class="input-group input-group-alt m-0">'+
        '<input class="form-control control col" type="date" value="" name="bmb006" required><div class="input-group-append" style="margin-right: -1px;"><span class="input-group-text custom-text">'+gettext('To')+'</span></div>'+'<input class="form-control control col" type="date" value="" name="emb006" required></div></div>'
        $('#SWAdvancedsearch-Modal-1 .modal-body').append(create_data);     

        //czz240919
        var tec_status = new SWCombobox("tec_status", gettext('Status'), 
        [{ 'value': 'S', 'label': 'S:'+gettext('SatisFied') },{ 'value': 'A', 'label': 'A:'+gettext('Alternative') },
        { 'value': 'N', 'label': 'N:'+gettext('UnKnown')},{ 'value': 'T', 'label': 'T:'+gettext('Need to Test') },
        { 'value': 'I', 'label': 'I:'+gettext('Checking') },{ 'value': 'C', 'label': 'C:'+gettext('Confirmed') }]);
        tec_status.setHorizontalDisplay(true)
        $('#SWAdvancedsearch-Modal-1 .modal-body').append(tec_status.dom.removeClass("input-group input-group-alt col-auto").addClass('form-group'));   
    }

    this.init_technical_table = function () {
        var technicTable = new SWDataTable("#questions_table", "Technictable"); //創建SWDataTable對象
        technicTable.pageLength = 10; //設置每頁顯示的數量為20
        technicTable.paging = true; //設置分頁顯示
        technicTable.searching = false; //設置不顯示查詢框

        technicTable.orderBy = [['mb023', 'desc']]; //設置按taskno 升序排序
        const mb004_width = SWApp.os.isMobile ? '60%' : (checkMediaQuery() ? '40rem' : '40%');
        //設置顯示字段
        technicTable.columns = [
            { field: "mb015c", label: gettext('Category')},
            { field: "mb004", label: gettext('Subject'), width: mb004_width },
            { field: "mb016", label: gettext('Area') },
            { field: "mb023", label: gettext('Technical ID')},
            { field: "mb001", label: gettext('Type Id'),visible:false },
            { field: "mb005", label: gettext('Contact') },
            {
                field: "mb006", label: gettext('Create Date'), render: function (data) {
                    if (data === null) return "";
                    return data.replace(/^(\d{4})(\d{2})(\d{2})$/, "$1-$2-$3");
                }
            },
            { field: "mb008", label: gettext('Usage'), width: checkMediaQuery() ? '20rem' : '10%', },
            { field: "score_value", label: gettext('Score'), width:"200px", visible:false, render:function (data, type, row) {
                    // 判断是否存在值，且为数字
                    if (typeof data === 'number') {
                        // 保留两位小数
                        return data.toFixed(2);
                    }
                    return data;
                }
            },
            { field: "inc_id", label: gettext('inc_id'), visible:false },
        ];
        // var mb004_width = SWApp.os.isMobile ? "60%" : "40%"
        technicTable.setOptions({
            autoWidth: !checkMediaQuery(),
            scrollX: checkMediaQuery(),
            responsive: true,
            columnDefs: [
                { "responsivePriority": 1, "className": "all", "targets": 0 },
                { "responsivePriority": 1, width: mb004_width, "className": "all", "targets": 1 },
                { "responsivePriority": 2, "className": "min-tablet-p", "targets": 2 },
                { "responsivePriority": 3, "className": "min-tablet-p", "targets": 3 },
                { "responsivePriority": 5, "className": "min-tablet-p", "targets": 5 },
                { "responsivePriority": 3, "className": "min-tablet-p", "targets": 6 },
                { "responsivePriority": 5, "className": "min-tablet-p", "targets": 7 },
            ],
            deferLoading: 0,
            drawCallback:function(settings) {
                self.bind_context_menu();
            }
        });
        self.technicTable = technicTable
        self.technicTable_datatable = technicTable.init('/PMIS/TechnicalDatatable');
    }
    this.bind_context_menu = function() {
        // 在每次 DataTable 绘制时绑定 contextMenu 到特定行
        $.contextMenu({
            // 选择器，这里选择 table 的 tbody 中的每一行
            selector: '#questions_table tbody tr',  
            callback: function(key, options) {
                // 你可以在这里根据用户点击的菜单项执行相关操作
                var rowData = self.technicTable_datatable.row(this).data(); // 获取行数据
                if (key === "generate_paraphrases") {
                    window.init_paraphrase_modal(rowData.inc_id);
                }
            },
            items: {
                "generate_paraphrases": { name: gettext("Generate Paraphrases"), icon: "add" }
            }
        });        
    }
    this.get_real_search_value = function(search_txt) {
        if (!search_txt)
            return ""
        search_txt = search_txt.trim();
        var chinese_match = search_txt.match(/[\u4e00-\u9fa5]+/g)
        var english_match = search_txt.match(/[^\u4e00-\u9fa5]+/g)
        var chinese_txt = chinese_match == null ? "" : chinese_match.join("");
        var english_txt = english_match == null ? "" : english_match.join("");
        var skip_txt = this.search_skip_txt_arr
        var english_txt = english_txt.trim().split(/\s+/).map((a)=>a.toLowerCase()).filter((x)=>x != "");
        var new_word = []
        for(var word of english_txt) {
            if (skip_txt.indexOf(word) == -1)
                new_word.push(word);
        }
        var chinese_txt = chinese_txt.trim().split("").filter((x)=>x != "");
        for(var word of chinese_txt) {
            if (this.search_skip_txt_arr_cn.indexOf(word) == -1)
                new_word.push(word);
        }
        if (new_word.length > 0)
            return new_word.join("+")
        else
            return ""
    }
    this.bind_event = function () {

        self.search.input_dom.on("input", function (e) {
            self.technicTable.handle_response_fun = undefined;
            $("#Technictable_info").closest(".row").show();
            if (self.technicTable_datatable != undefined) {
                if (self.ai_search_cb.input_dom.is(":checked")) {
                    var search_val = $(this).val();
                    if (search_val) {
                        clearTimeout(debounceTimeout);
                        debounceTimeout = setTimeout(() => {
                            self.technicTable_datatable.search("ai_search:"+search_val).draw();    
                        }, 1000);
                    }
                }else {
                    var search_val = self.get_real_search_value($(this).val())
                    if (search_val)
                        self.technicTable_datatable.search(search_val).draw();    
                }
            }
        });
        $('#questions_table').on('dblclick', 'tbody tr', function () {
            var strmb023 = self.technicTable_datatable.row(this).data()['mb023'];
            var inc_id = self.technicTable_datatable.row(this).data()['inc_id'];
            if(strmb023!=undefined && strmb023!=null && strmb023!='')
                window.open('/PMIS/opportunity/Technical_Material?param=' + strmb023.trim())
            else
                window.open('/PMIS/opportunity/Technical_Material?inc_id=' + inc_id)
        })
        self.ai_search_cb.input_dom.on("change", function(e){
            var value = $(this).is(":checked");
            self.technicTable_datatable.column(8).visible(value);   
        });
        self.content_search_btn.dom.on("click", function(e){
            var searchValue = self.search.input_dom.val();
            searchValue = self.get_real_search_value(searchValue)
            if (searchValue == "")
                return;
            searchValue = searchValue.replaceAll("+"," ");
            $.ajax({
                url:"/devplat/question/content_search",
                type:"POST",
                data:{searchValue:searchValue},
                beforeSend: function (request) {
                    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                },  
                success:function(result) {
                    if (result.status) {
                        self.technicTable.handle_response_fun = function(json) {
                            return result.data;
                        }
                        self.technicTable_datatable.search("xxxxxx").draw();
                        $("#Technictable_info").closest(".row").hide();
                    }else {
                        SWApp.popoverMsg(self.content_search_btn.dom, "查詢失敗!");
                    }
                }
            })
        });
        self.post_btn.dom.on("click", function (e) {
            self.post_btn.dom.attr("disabled", true); //防止重覆點擊
            var task = self.search.input_dom.val();
            if (task == "")
                return;
            var sessionid = undefined
            var active_item = $("#stacked-menu .menu-item.has-active");
            var data = {}
            if (active_item.length > 0) {
                sessionid = active_item.attr("sessionid");
                if (sessionid != undefined)
                    data['relationid'] = sessionid;
            }
            data['task'] = task;
            var url = "/devplat/question/post"
            $.ajax({
                type: "POST",
                url: url,
                data: data,
                datatype: "json",
                beforeSend: function (request) {
                    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                },
                success: function (data) {
                    if (data.status) {
                        SWApp.popoverMsg(self.post_btn.dom, "保存成功");
                    }
                    else {
                        var msg = Object.keys(data.msg)[0] + ":" + data.msg[Object.keys(data.msg)[0]];
                        SWApp.popoverMsg(self.post_btn.dom, msg);
                    }
                    self.post_btn.dom.attr("disabled", false); //防止重覆點擊
                },
                error: function () {
                    self.post_btn.dom.attr("disabled", false); //防止重覆點擊
                    alert("程序異常!");
                }
            });
        });

        $(window).on('orientationchange', function () {
            location.reload();
        });
    }
}

function checkMediaQuery() {
    var mediaQuery = window.matchMedia("(min-width: 481px) and (max-width: 1299.98px)");
    return mediaQuery.matches;
}