var profile_demo = function() {
    return {
        init:function() {
            var completionTasksOptions = {
                elementId: "canvas-achievement",
                url: "/PMIS/user/profile/get_chievement",
                query: {"username": "hb"},
                groups: { assigned:{field:"assigned",looper_color:"teal"}, complete: {field:"completed",looper_color:"purple"}},
                labelField: "date"
            }

            ComponentClass.displayCompletionTasksControl(completionTasksOptions);
        }
    }
}();

jQuery(document).ready(function () {
    profile_demo.init();
});