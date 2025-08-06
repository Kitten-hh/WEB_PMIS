$(document).ready(function () {
    var Task_DetailsVm = new Vue({
        el: ".content-wrap",
        data: {
            Task: {},
            query_filter_id: getParam("query_filter_id"),
            TaskTypeList: {}
        },
        methods: {
            // 获取任务类型
            get_TaskTypeList: function () {
                $.ajax({
                    url: '/bonus/get_TaskTypeList/',
                    type: 'GET',
                    dataType: 'json',
                    cache: false,
                    success: function (json) {
                        var data = json.data;
                        Task_DetailsVm.TaskTypeList = data;
                    }
                })
            },
            //获取Task明细
            get_Task: function () {
                $.ajax({
                    url: '/bonus/get_Task_Details/',
                    type: 'GET',
                    data: { inc_id: getParam("inc_id") },
                    dataType: 'json',
                    cache: false,
                    success: function (json) {
                        var data = json.data;
                    
                        if (data.planbdate != null) { data.planbdate = formatChatTime2(parseDjangoTime(data.planbdate)); }
                        if (data.planedate != null) { data.planedate = formatChatTime2(parseDjangoTime(data.planedate)); }
                        if (data.bdate != null) { data.bdate = formatChatTime(parseDjangoTime(data.bdate)); }
                        if (data.edate != null) { data.edate = formatChatTime(parseDjangoTime(data.edate)); }
                        if (data.requestdate != null) { data.requestdate = formatChatTime(parseDjangoTime(data.requestdate)); }
                        Task_DetailsVm.Task = data;
                        
                    }
                })
            },
            // 进入联系人明细
            contact_Details: function (contactName) {
                var query_filter_id = Task_DetailsVm.query_filter_id;
                if (query_filter_id != undefined) {
                    window.location.href = '/bonus/get_Contact_Details/?contact_name=' + contactName + '&query_filter_id=' + query_filter_id;
                } else {
                    window.location.href = '/bonus/get_Contact_Details/?contact_name=' + contactName;
                }
            },
            // 删除Task 删除按钮
            DeleteTask: function () {
                layer.confirm("确认删除？", { btn: ['确认', '取消'], icon:3, offset:'30%'}, function () {
                    $.ajax({
                        url:'/bonus/Task_Del',
                        type:'GET',
                        data:{ inc_id: getParam("inc_id")},
                        dataType:'json',
                        cache: false,
                        success:function(data){
                            if(data.flg){
                                alert(data.message);
                                window.location.href='/bonus/';
                            }
                        },
                        error:function(){
                            alert("程序异常")
                        }
                    })
                })
            },
            // 修改Task 保存按钮
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
            },

            // 选择任务类型给当前Task赋值
            selectTaskTypeList: function (taskTypeList) {
                Task_DetailsVm.Task.tasktype = taskTypeList.tasktype;
                Task_DetailsVm.Task.tasktypedesc = taskTypeList.description;
            },
            // 选择子任务类型给当前Task赋值
            selectTaskTypeList_son: function (taskTypeList) {
                Task_DetailsVm.Task.subtasktype = taskTypeList.tasktype;
                Task_DetailsVm.Task.subtasktypedesc = taskTypeList.description;
            }
        },
        created: function () {
            this.get_TaskTypeList();//填充任务类型及子任务类型数据
            this.get_Task();
        }
    })
 
    $("#prev_page").click(function () {
        history.go(-1);
    })

})


