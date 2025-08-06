// 刪除TaskType
$("#del_TaskType").click(function () {
    var taskType_Id = $("#taskType_Id").val()
    
    if (confirm("确定删除？")) {
        $.ajax({       
            type:"POST",
            url:"/en/bonus/tasktype/delete/"+taskType_Id,
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", getCookie('csrftoken_WEB_PMIS'));
            }, 
            success: function (result) {
                if(result.status){
                    alert("刪除成功！");
                    window.location.href = '/bonus/tasktype';
                }
            },
            error:function(){
                alert("程序异常！");
            }
        })
    }
})