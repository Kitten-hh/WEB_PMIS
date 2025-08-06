$(function () {
    var header_title = `<span class="recordid">[[recordid]]</span><span class="ml-2 sessionid">[[sessionid]]</span>`;
    var header_sub_title = `<h6 class="item-header-subtitle card-subtitle text-dark">
        <div class="ppsp"><span class="">[[planbdate]] / [[planedate]]</span><span class="ml-2 badge badge-subtle badge-dark font-size-lg">[[progress]]</span></div></h6>`;
    var contact =  get_username();
    if (contact == null)
        contact = 'sing'
    else
        update_tab_link();
    $(".activites_header .username").text(contact);
    var period = getParamFromUrl("period");
    if (period == null)
        period = "{0}-{1}".format(new Date().toString("yyyy"), Math.ceil((new Date().getMonth() + 1)/3));

    $("#SWBoardlist .task-issue .card-footer").html(`
        <a href="#" class="card-footer-item card-footer-item-bordered text-dark left"><i class="oi oi-comment-square mr-1"></i></a> 
        <div class="card-footer-item card-footer-item-bordered text-dark right scrollX">
            <div class="session_task_filter d-flex justify-content-between">
                <a href="#" class="badge badge-subtle badge-dark mr-1" progress="N">N</a>
                <a href="#" class="badge badge-subtle badge-dark mr-1" progress="I">I</a>
                <a href="#" class="badge badge-subtle badge-dark mr-1" progress="T">T</a>
                <a href="#" class="badge badge-subtle badge-dark mr-1" progress="C">C</a>
                <a href="#" class="badge badge-subtle badge-dark mr-1" progress="F">F</a>
                <a href="#" class="badge badge-subtle badge-dark mr-1" taskprogress="NF">NF</a>
                <a href="#" class="badge badge-subtle badge-dark mr-1" taskcategory="MF">MF</a>
                <a href="#" class="badge badge-subtle badge-dark mr-1" taskcategory="MH">MH</a>
                <a href="#" class="badge badge-subtle badge-dark mr-1" classField="C1">C1</a>
            </div>
        </div>
        <a href="#" class="card-footer-item card-footer-item-bordered text-dark add_task"><i class="fa fa-plus-circle"></i></a>
    `)

    var sessions = new SWBoardlist(gettext("On Going Session"), `/PMIS/session/session_list?allcontact=${contact}&period=${period}`,
    "", header_title, header_sub_title,"sdesp","taskc","taskqty");
    sessions.processors_function = function(item){
        if (Date.parse(item["planbdate"]) != null)
            item["planbdate"] = Date.parse(item["planbdate"]).toString("yyyy-MM-dd");
        if (Date.parse(item["planedate"]) != null)
            item["planedate"] = Date.parse(item["planedate"]).toString("yyyy-MM-dd");
    }
    $("#sessions").append(sessions.dom);
    var contact = new SWCombobox("contact", gettext('Contact'), window.CommonData.PartUserNames)
    contact.input_dom.attr("data-live-search", "true");
    var all_contact = new SWCombobox("allcontact", gettext("All Contacts"), window.CommonData.PartUserNames)
    all_contact.input_dom.attr("data-live-search", "true");
    var recordid = new SWCombobox("recordid", gettext("RecordID"), "/PMIS/subproject/get_all_recordid", undefined, 'recordid','recordid');
    recordid.input_dom.attr("data-live-search", "true");
    var period = new SWCombobox("period", gettext("Period"), "/PMIS/goalmaster/get_all_period")
    var layout = `<div class="row">
                <div class="col-6"></div> 
                <div class="col-6"></div> 
                </div>`
    var first_col = $(layout).clone();
    first_col.children("div").eq(0).append(contact.dom);
    first_col.children("div").eq(1).append(all_contact.dom);
    var second_col = $(layout).clone();
    second_col.children("div").eq(0).append(recordid.dom);
    second_col.children("div").eq(1).append(period.dom);
    sessions.filter_content.append(first_col);
    sessions.filter_content.append(second_col);
    
    sessions.dom.find(".task-body").on("click", ".card-footer .add_task", function(e){
        e.preventDefault(); //阻止按鈕默認動作
        e.stopPropagation();
        var sessionid = $(this).closest(".card").find(".sessionid").text();
        init_task(undefined, {sessionid:sessionid});
    });

    sessions.dom.find(".task-body").on("click", ".card-footer .right", function(e){
        e.preventDefault(); //阻止按鈕默認動作
        e.stopPropagation();
    });
    sessions.dom.find(".task-body").on("click", ".card-footer .session_task_filter a", function(e) {
        e.preventDefault(); //阻止按鈕默認動作
        e.stopPropagation();
        $(this).toggleClass("active");
        filter_task(e);
    });

    sessions.dom.find(".task-body").on("click", ".card-footer .left", filter_task);

    function filter_task(e) {
        e.preventDefault(); //阻止按鈕默認動作
        e.stopPropagation();
        var session_dom = $(e.currentTarget).closest(".task-issue")
        var sessionid = session_dom.find(".sessionid").text();
        var arr = sessionid.split("-");
        pid = arr[0];
        tid = arr[1];
        var self = this;
        if ($(e.currentTarget).hasClass("left")) {
            session_dom.find(".session_task_filter a").removeClass("active");
        }
        if (session_dom.next().hasClass("task-collapse")) {
            if ($(e.currentTarget).hasClass("left")) {
                var collapse_dom = session_dom.next();
                collapse_dom.collapse('hide')
                collapse_dom.remove();
                return;
            }
        }
        //判斷NF和F過濾，只能選擇一個
        if (session_dom.find(".session_task_filter a[taskprogress].active").length > 0 && session_dom.find(".session_task_filter a[progress='F'].active").length > 0 ) {
            //如果當前選中的F過濾
            if ($(e.currentTarget).attr("progress"))
                $(".session_task_filter a[taskprogress].active").removeClass("active");
            else if ($(e.currentTarget).attr("taskprogress"))
                $(".session_task_filter a[progress='F'].active").removeClass("active");
        }
        var progress_nf = session_dom.find(".session_task_filter a[taskprogress].active").length > 0;
        var progress_dom = session_dom.find(".session_task_filter a[progress].active");
        var progress_arr = []
        if(progress_dom.length > 0)
            for(let item of progress_dom)
                progress_arr.push($(item).attr("progress"))        
        var taskCategory_dom = session_dom.find(".session_task_filter a[taskcategory].active");
        var taskcategory_arr = []
        if(taskCategory_dom.length > 0)
            for(let item of taskCategory_dom)
                taskcategory_arr.push($(item).attr("taskcategory"))
        var class_dom = session_dom.find(".session_task_filter a[classField].active");
        var classOne = false;
        if (class_dom.length > 0)
            classOne = true;
        $.ajax({
            url:"/PMIS/session/search_task",
            data:{pid:pid,tid:tid,progress_or:progress_arr.join(","),progress_nf:progress_nf, taskcategory_or:taskcategory_arr.join(","),class_one:classOne},
            success:function(data){
                if(data.status) {
                    show_task(data.data, self)
                }
            }
        });
        function show_task(data, self) {
            var dom = $("#tasklist").clone();
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
            if (session_dom.next().hasClass("task-collapse")) {
                session_dom.next(".task-collapse").empty();
                session_dom.next(".task-collapse").append(dom.find(".task-item"));
            }else {
                $(e.currentTarget).closest(".task-issue").after(dom);
                dom.show();
                dom.collapse();
            }
        }

        function show_task2(data, sefl) {
            var dom = $("#tasklist").clone();
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
            $("#exampleModal .modal-body").empty();
            $("#exampleModal .modal-body").append(dom);
            dom.show();
            $("#exampleModal").modal("show");
        }

        function update_task(self) {
            var pk = $(self).closest(".task-item").find(".pk").text();
            init_task(pk);
        }
    
        $(".page-inner").on(
            {
                dblclick:function(){
                    update_task(this);
                },
                longpress:function() {
                    update_task(this);
                }
            },
            ".task-item"
        );        
    };
    function update_tab_link() {
        $(".page-navs .nav-link").each((index, item)=>{
            var href = $(item).attr("href");
            if (href != "#") {
                if (href.indexOf("?") == -1)
                    $(item).attr("href", href + "?contact="+contact)
                else
                    $(item).attr("href", href + "&contact="+contact)
            }
        });
    }

    $(".page-inner").on("click",".SWBoardlist .task-issue", function(e){
        //跳到對應Development的Session
        var session_dom = $(this).closest(".task-issue")
        var sessionid = session_dom.find(".sessionid").text();
        var recordid = session_dom.find(".recordid").text();
        window.open(`/devplat/sessions?recordid=${recordid}&menu_id=mi_${sessionid}#Requirements`, "_blank");
    })
});