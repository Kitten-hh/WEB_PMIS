
$("#app-footer").on('click', '#cencel', function () {
    var taskType_Id = $("#taskType_Id").val();
    window.location.href = '/bonus/tasktype/detail?taskType_Id=' + taskType_Id;
})

$("#app-footer").on('click', '#save', function () {
    var taskType_Id = $("#taskType_Id").val()
    //var tasktype = {id:taskType_Id, descrption:"123", score:100, tasktype:"456"}; 
    if (confirm("確定修改？")) {
        $.ajax({
            type: "POST",
            url: "/en/bonus/tasktype/update/save?pk="+taskType_Id,
            data: $(".myForm").serialize(),
            //data: tasktype,
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", getCookie('csrftoken_WEB_PMIS'));
            },
            datatype: "json",
            success: function (result) {                
                if (result.status) {
                    alert("保存成功！");
                    window.location.href = "/bonus/tasktype/detail?taskType_Id=" + taskType_Id
                }else{
                    alert("保存失敗！");
                }
            },
            error: function () {
                alert("程序异常！");
            }
        })
    }
})