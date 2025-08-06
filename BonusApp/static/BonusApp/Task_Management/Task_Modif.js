// 加載需要修改的數據
var TaskVm = new Vue({
    el: '#Modif_Task',
    data: {
        task: {},
        taskTypes: {},
        taskTypes_two: {},
        search_values: ''
    },
    methods: {
        //獲取Task
        getTask: function () {
            $.ajax({
                url: '/bonus/get_Task_Modif_Page/',
                type: 'GET',
                data: { inc_id: getParam("inc_id") },
                dataType: 'json',
                cache: false,
                success: function (json) {
                    if (json.state == 200) {
                        // 時間轉換
                        if (json.data.edate != null) {
                            json.data.edate = formatTime(parseDjangoTime(json.data.edate));
                        }
                        TaskVm.task = json.data;
                    } else {
                        layer.confirm(json.message, { btn: ['確定'], icon: 2, offset: 't' }, function () {
                            history.back(-1)
                        });
                    }
                }
            })
            // 获取所有TaskType
        }, getTaskType: function () {
            $.ajax({
                url: '/bonus/tasktype/datatable/',
                type: 'GET',
                dataType: 'json',
                cache: false,
                success: function (json) {
                    if (json.state == 200) {
                        TaskVm.taskTypes = json.data;
                        TaskVm.taskTypes_two = json.data;
                    } else {
                        layer.confirm(json.message, { btn: ['確定'], icon: 2, offset: 't' }, function () {
                            history.back(-1)
                        });
                    }
                }
            })
            // 把选择的TaskType进行更改
        }, selectTaskType: function (taskType) {
            TaskVm.task.realtasktype = taskType.tasktype;
            TaskVm.task.subtasktypedesc = taskType.description;
            TaskVm.task.tasktypescore = taskType.score;
            $("#myModal_TaskType").modal('hide');

            //跳转到TaskType Add页面
        }, new_TaskType: function () {
            location.href = "/bonus/tasktype/add/";

            // 搜索框
        }, taskTypeSearch: function (value) {
            if (value == '') {
                TaskVm.taskTypes = TaskVm.taskTypes_two; //等於空就顯示所有數據
                return;
            }
            var newTaskTypes = {}
            for (var item in TaskVm.taskTypes_two) {
                if (TaskVm.taskTypes_two[item].tasktype.includes(value) || TaskVm.taskTypes_two[item].description.includes(value) || String(TaskVm.taskTypes_two[item].score).includes(value)) {
                    newTaskTypes[item] = TaskVm.taskTypes_two[item];
                }
            }
            // 篩選过后改变显示的值
            TaskVm.taskTypes = newTaskTypes;
        }

    }, created: function () {
        this.getTask();
        this.getTaskType();
    }
})


var modifTaskVm = new Vue({
    el: '#app-footer',
    methods: {
        // 修改Task
        TaskModif: function () {
            layer.confirm("確定修改？", { btn: ['確定', '取消'], icon: 3, offset: '30%' }, function () {
                $.ajax({
                    url: '/bonus/Modif_Task/',
                    type: 'POST',
                    data: $(".myForm").serialize(),
                    dataType: 'json',
                    cache: false,
                    success: function (json) {
                        if (json.state == 200) {
                            var url = "/bonus/get_Task_Details?inc_id=" + json.data;
                            layer.confirm("修改成功！", { btn: ['確定'], icon: 1, offset: '30%' }, function () {
                                location.href = url;
                            });
                        } else {
                            var url = "/bonus/get_Task_Details?inc_id=" + json.data;
                            layer.msg(json.message, { btn: ['確定'], icon: 2, offset: '30%' }, function () {
                                history.back(-1)
                            });
                        }
                    }
                })
            });
        }
    }
})

$("#prev_page").click(function () {
    history.go(-1);
})


$("#app-footer").on('click', '#cancel', function () {
    var task_id = $("#task_id").val();
    window.location.href = '/bonus/get_Task_Details?inc_id=' + task_id;
})