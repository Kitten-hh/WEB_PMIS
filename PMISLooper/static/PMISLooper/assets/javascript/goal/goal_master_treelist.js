var gettext_addMonthlyGoal = gettext("Add Monthly Goal");

$(function () {
    var tree_grid = new SWTreegrid("#treelist");
    tree_grid.idField = "TaskNo";
    tree_grid.parentIdField = "RelationGoalId";
    tree_grid.columns = [
        { field: 'Task', label: gettext('Task Description'),render:(value, row, index) => {
            return '<span class="task-desp" id="' + row.inc_id + '">' + value + '</span>';
            }
        },              
        {field: 'TaskNo',label: gettext('TaskID'),sortable: true,width: '170',visible:!SWApp.os.isMobile},
        {field: 'Contact',label: gettext('Contact'),sortable: true,align: 'center',width:'40',visible:!SWApp.os.isMobile},
        {field:'PlanBDate',label:gettext('PSDate'),sortable: true, render: SWTreegrid.dateRender, visible:!SWApp.os.isMobile},
        {field:'PlanEDate',label: gettext('PFDate'),sortable: true, render: SWTreegrid.dateRender, visible:!SWApp.os.isMobile},
        {field:'Progress',label: gettext('Progress'),visible:!SWApp.os.isMobile},
        {field:'operate',label: gettext('Operation'),width:"30",render:function(value, row, index){
            var menu = new SWDropdown(`<i class="fas fa-ellipsis-v"></i>`);
            menu.dom.find(".dropdown-toggle").removeClass("btn-secondary dropdown-toggle");
            menu.addItem("edit_task", "#", gettext('Edit'));
            menu.addItem("del_task", "#", gettext('Delete'));
            if (row.LevelNum == 1) 
                menu.addItem("create_task", "#", gettext_addMonthlyGoal);
            else if (row.LevelNum == 2) {
                var tid = row.Tid.toString().replace(/55$/, "57")
                menu.addItem("create_task", "#", gettext('Add Weekly Goal'));
            }
            else if (row.LevelNum == 3)
                menu.addItem("create_task", "#", gettext('Add Task'));
            menu.dom.attr("taskno", row.TaskNo);
            menu.dom.attr("task_pk", row.INC_ID);
            return menu.dom.prop("outerHTML");
        }}
    ];
    var url = "/PMIS/goalmaster/show_treelist/{0}".format(getParamFromUrl("pk"));
    tree_grid.addLeftMenu("add_quarterly", "fas fa-plus", gettext('Add Quarterly Goal'));
    tree_grid.init(url);

    $("#treelist").on("click","#add_quarterly", function(e){
        e.preventDefault(); //阻止按鈕默認動作
        e.stopPropagation();
        var appraisal_id = getParamFromUrl("pk");
        init_task(undefined, {appraisal_id:appraisal_id})
    });    
    $("#treelist").on("click", ".create_task", function(e){
        e.preventDefault(); //阻止按鈕默認動作
        e.stopPropagation();
        var taskno = $(this).closest(".SWDropdown").attr("taskno");
        var appraisal_id = getParamFromUrl("pk");
        init_task(undefined, {appraisal_id:appraisal_id, parent_goal:taskno});
    });
    $("#treelist").on("click", ".edit_task", function(e){
        e.preventDefault(); //阻止按鈕默認動作
        e.stopPropagation();
        var pk = $(this).closest(".SWDropdown").attr("task_pk");
        init_task(pk);
    });
});