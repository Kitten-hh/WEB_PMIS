$("#app-footer").on('click', '#cencel', function () {
    window.location.href = '/bonus/Task_Management'
})

$("#app-footer").on('click', '#save', function () {
    var taskType_Id = $("#taskType_Id").val()
    if (confirm("確定添加？")) {
        $.ajax({
            type: "POST",
            url: "/bonus/tasktype/add/save/",
            data: $(".myForm").serialize(),
            datatype: "json",
            success: function (result) {
                if (result.state == 200) {
                    alert(result.message);
                    window.location.href = "/bonus/Task_Management"
                }
            },
            error: function () {
                alert("程序异常！");
            }
        })
    }
})