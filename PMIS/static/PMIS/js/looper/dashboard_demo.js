var dashboard_demo = function() {
    return {
        init:function() {
            var completionTasksOptions = {
                elementId: "completion-tasks",
                url: "/PMIS/looper_dashboard/getCompletionTasks",
                query: {"start": "20200701","end":"20200731" },
                groups: { complete: {field:"task_qty"}},
                labelField: "edatestr",
                sort:"edatestr"
            }

            ComponentClass.displayCompletionTasksControl(completionTasksOptions);
        }
    }
}();

jQuery(document).ready(function () {
    dashboard_demo.init();
});