$(function () {
    var contact =  getParamFromUrl("contact");
    if (contact == null)
        contact = get_login_name();
    var all_user = new SWCombobox('user',gettext('User'),window.CommonData.PartUserNames, contact);        
    all_user.dom.addClass("row");
    all_user.dom.find(".caption").css({"font-size":"16px","font-weight":"600"});
    all_user.dom.find("label").addClass("col-auto");
    all_user.dom.children(".control").css("width","100px");
    all_user.dom.children(".control").wrap('<div class="col-auto"></div>');
    $(".page-inner .userlist").append(all_user.dom);
    var group_title = `<div><span>[[group_type]]</span></div>`
    var subtitle_tmpl = `<label class="custom-control custom-checkbox">
                        <input type="checkbox" class="custom-control-input" [[input_checked]]>
                        <span class="custom-control-label pk_label" group_order="[[group_order]]" pk="[[inc_id]]" outstanding="[[outstanding]]" todayt="[[todayt]]" progress="[[progress]]">
                        [[task_order_num_dom]][[task]]([[task_mark]])
                        </span>
                    </label>`
    var activeTaskNavDom = $(`<ul class="nav nav-pills activeTaskNav flex-nowrap">
                <li class="nav-item">
                    <a class="nav-link active" href="#group-task-views" show_style="group" data-toggle="tab"> <i class="fas fa-layer-group"></i> </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#list-task-views" show_style="list" data-toggle="tab"> <i class="fas fa-list-ul"></i> </a>
                </li>                           
                <li class="nav-item">
                <a class="nav-link" href="#top-task-views" show_style="top" data-toggle="tab" filter="null"><i class="fas fa-indent"></i></a>
                </li>
              <li class="nav-item">
                <a class="nav-link" href="#single-task-views" show_style="single" data-toggle="tab" filter="null"><i class="fas fa-clipboard-list"></i></a>
              </li>              
            </ul>`);
                        
    var today_task = new SWTodolist(gettext("Today's Tasks"), "/PMIS/task/get_today_fixed_tasks?style=group&contact="+contact, ['group_order'], group_title, subtitle_tmpl);
    today_task.dom.children(".card-header").append(activeTaskNavDom);
    today_task.dom.children(".card-header").addClass("d-flex justify-content-between")
    $("#today_tasks").append(today_task.dom);
    var schcategoryList = [];
    var processors_function = function(item){
        if (item.hasOwnProperty("schcategory") && schcategoryList.indexOf(`${item.group_order}-${item.schcategory}`) == -1) {
            schcategoryList.push(`${item.group_order}-${item.schcategory}`);
            this.todo_dom.append(`<div class="todo-header todo-subheader ml-2 py-0"><div><span style="font-size:14px">${item.schcategory}</span></div></div>`)
        }
        var task_mark = "Sch Priority:<span style='font-size:16px;margin-left:2px'>{0}</span> Today Priority:<span style='font-size:16px;margin-left:2px'>{1}</span>"
        task_mark = task_mark.format((item.schpriority != null ? item.schpriority : "0"), (item.schprioritysp != null ? item.schprioritysp : "0"))
        if (today_task.datasource.indexOf("style=single") != -1) {
            task_mark = "Session Priority:<span style='font-size:16px;margin-left:2px'>{0}</span> Today Priority:<span style='font-size:16px;margin-left:2px'>{1}</span>"                
            task_mark = task_mark.format((item.sessionpriority != null ? item.sessionpriority : "0"), (item.schprioritysp != null ? item.schprioritysp : "0"))
        }    
        if (item.class_field == 1)
            task_mark += " Class:<span style='font-size:16px;margin-left:2px'>1</span>"
        item['task_mark'] = task_mark;
        if (item.progress == "C" || item.progress == "F")
            item['input_checked'] = "checked";
        else
            item['input_checked'] = ""; 
        var task_order_num_dom = '';
        if (item.hasOwnProperty("task_order_num"))
            task_order_num_dom = `<span class="tile tile-sm task_order_num mr-2">{0}</span>`.format(item['task_order_num']);
        item['task_order_num_dom'] = task_order_num_dom;                       
    }
    var card_expansion_list = function (curitem, nextitem) {
        if (item.hasOwnProperty("parent_group_type") && (nextitem == undefined || nextitem.parent_group_type != curitem.parent_group_type)) {
            var group_type = $(this.todo_dom.children(".todo-header:not(.todo-subheader)")[0]).find("span").text();
            var prefixId = curitem.parent_group_type.replaceAll(" ","").replaceAll("'","");
            if (group_type == curitem.parent_group_type)
                this.todo_dom.children(".todo-header:not(.todo-subheader)").remove();
            createExpansionCard(`${prefixId}Group`, `${prefixId}GroupCollapse`, curitem.parent_group_type, this.todo_dom.children('.todo,.todo-header'), true);  
        }   
    }     
    var reloadTodayTask = function(){
        schcategoryList.length = 0;
        var styleName = $(".activeTaskNav .nav-link.active").attr("show_style");
        if ($(this).hasClass("nav-link"))
            styleName = $(this).attr("show_style");
        var url = `/PMIS/task/get_today_fixed_tasks?style=${styleName}&contact=${all_user.input_dom.val()}`;
        today_task.reload(url);
    }
    today_task.processors_function = processors_function;
    today_task.handle_after_append_todo =card_expansion_list;
    all_user.input_dom.on("change", reloadTodayTask)
    activeTaskNavDom.find(".nav-link").on("click", reloadTodayTask);


    var createExpansionCard = function (groupID, collapseID, groupName, taskList, insertBeforeLast) {
        var expansionCard_tmpl = `<div class="card card-expansion-item expanded expansionCard">
            <div class="card-header" id="${groupID}">
                <button class="btn btn-reset d-flex justify-content-between prevent-default text-primary" data-toggle="collapse"
                    data-target="#${collapseID}" aria-expanded="true" aria-controls="${collapseID}">
                    <span class="collapse-indicator"><i class="fa fa-fw fa-caret-right mr-2"></i></span>
                    <span>${groupName}</span>
                </button>
            </div>
            <div id="${collapseID}" class="collapse show" aria-labelledby="${groupID}">
                <div class="card-body py-0"></div>
            </div>
        </div>`;

        if (insertBeforeLast) {
            $(today_task.todo_dom).children(":last").before(expansionCard_tmpl);
        } else {
            $(today_task.todo_dom).append(expansionCard_tmpl);
        }

        $("#" + collapseID).find(".card-body").append(taskList);
    };

      

    function update_task(self) {
        var pk = $(self).find(".pk_label").attr("pk");
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
        ".SWTodolist .todo"
    );
});