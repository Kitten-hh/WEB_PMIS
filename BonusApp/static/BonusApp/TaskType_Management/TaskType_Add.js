$("#app-footer").on('click', '#cencel', function () {
    window.location.href = '/bonus/tasktype'
})

$("#app-footer").on('click', '#save', function () {
    var taskType_Id = $("#taskType_Id").val()
    if (confirm("確定添加？")) {
        $.ajax({
            type: "POST",
            url: "/en/bonus/tasktype/add/save/",
            data: $(".myForm").serialize(),
            datatype: "json",
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", getCookie('csrftoken_WEB_PMIS'));
            },
            success: function (result) {
                if (result.status) {
                    alert("保存成功！");
                    window.location.href = "/bonus/tasktype"
                }
            },
            error: function () {
                alert("程序异常！");
            }
        })
    }
})