// Function to initialize the paraphrase list with textarea
function initParaphraseList(paraphrases, listId) {
    var listGroup = document.getElementById(listId);
    paraphrases.forEach(function(paraphrase, index) {
        addParaphrase(listId,index, paraphrase);
    });
}

// Function to add a paraphrase to the list
function addParaphrase(listId,index, paraphraseText = '') {
    var listGroup = document.getElementById(listId);
    var li = document.createElement('li');
    li.className = 'list-group-item d-flex align-items-center py-1';

    li.innerHTML = `
        <label class="font-weight-bold">${index + 1}.</label>
        <textarea class="form-control paraphrase-input ml-1" rows="2">${paraphraseText}</textarea>
        <a href="javascript:void(0);" class="px-2" onclick="this.parentElement.remove();"><i class="fa fa-trash-alt"></i></a>
    `;

    listGroup.appendChild(li);
} 

// 初始化 paraphrases 的数据到弹出框
window.init_paraphrase_modal = function(id) {
    const modal = $("#paraphrase-modal");

    // 清除上次打开 modal 的残留数据
    $("#paraphrase-topic").val('');
    $('#paraphrase-topic').removeData('id');
    $("#english-paraphrase-list").empty();
    $("#chinese-paraphrase-list").empty();

    // AJAX 请求从后端获取数据
    $.ajax({
        url: `/PMIS/technical/get_paraphrase?id=${id}`,  // 后端 API，替换为你的实际 URL
        type: 'GET',
        success: function(result) {
            // 检查是否返回数据
            if (result.status) {
                var paraphrase = result.data[0]
                // 初始化 topic 字段
                $("#paraphrase-topic").val(paraphrase.topic);
                $('#paraphrase-topic').data('id',  id)


                // Initialize English and Chinese paraphrase lists
                if (paraphrase.topic_paraphrases_english && paraphrase.topic_paraphrases_english.length > 0)
                    initParaphraseList(paraphrase.topic_paraphrases_english, 'english-paraphrase-list');
                if (paraphrase.topic_paraphrases_chinese && paraphrase.topic_paraphrases_chinese.length > 0)
                    initParaphraseList(paraphrase.topic_paraphrases_chinese, 'chinese-paraphrase-list');                

            }

            // 显示 modal
            modal.modal("show");
        },
        error: function(error) {
            console.error('Error fetching paraphrase data:', error);
            alert("{% trans 'Error fetching paraphrase data.' %}");
        }
    });    

    // 添加英文 paraphrase 按钮
    $("#add-english-paraphrase").off("click").on("click", function() {
        var index = $("#english-paraphrase-list .list-group-item").length + 1;
        addParaphrase('english-paraphrase-list', index);
        var paraphraseList = $("#english-paraphrase-list");
        paraphraseList.scrollTop(paraphraseList.prop("scrollHeight"));        
    });

    // 添加中文 paraphrase 按钮
    $("#add-chinese-paraphrase").off("click").on("click", function() {
        var index = $("#chinese-paraphrase-list .list-group-item").length + 1;
        addParaphrase('chinese-paraphrase-list', index);
        var paraphraseList = $("#chinese-paraphrase-list");
        paraphraseList.scrollTop(paraphraseList.prop("scrollHeight"));        
    });

    // 显示 modal
    modal.modal("show");
};

// 点击生成 paraphrases 按钮，获取输入内容并发送到后端
$('#generate-paraphrases-btn').click(function() {
    const id = $('#paraphrase-topic').data('id');  // 获取 id
    const gpt_model = $("#gpt_model").val();
    const paraphraseCount = $("#paraphrase-count").val();
    const custom_paraphrases = $("#paraphrase_method").val() === "paraphrase_method_custom";
    const topic = $("#paraphrase-topic").val();  // 获取 topic 字段

    // 获取所有 paraphrases 英文
    const englishParaphrases = [];
    $("#english-paraphrase-list .paraphrase-input").each(function() {
        const paraphrase = $(this).val().trim();
        if (paraphrase) {
            englishParaphrases.push(paraphrase);
        }
    });

    // 获取所有 paraphrases 中文
    const chineseParaphrases = [];
    $("#chinese-paraphrase-list .paraphrase-input").each(function() {
        const paraphrase = $(this).val().trim();
        if (paraphrase) {
            chineseParaphrases.push(paraphrase);
        }
    });

    const requestData = {
        id: id,
        gpt_model: gpt_model,
        paraphrase_count: paraphraseCount,
        custom_paraphrases: custom_paraphrases,
        paraphrases_english: englishParaphrases,
        paraphrases_chinese: chineseParaphrases
    };
    // 显示“生成中”的提示信息
    $("#loadingMessage").show();

    // 发送请求到后端生成 paraphrases
    $.ajax({
        url: '/PMIS/technical/update_embeddings',  // 替换为你的后端 URL
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(requestData),
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(result) {
            // 隐藏“生成中”的提示信息
            $("#loadingMessage").hide();
            if (result.status) {

                // 清空之前的 paraphrase 列表
                $("#english-paraphrase-list").empty();
                $("#chinese-paraphrase-list").empty();

                // 将后端生成的新 paraphrases 更新到页面中
                var newEnglishParaphrases = result.data[0].topic_paraphrases_english || [];
                var newChineseParaphrases = result.data[0].topic_paraphrases_chinese || [];

                // 添加新的英文 paraphrases
                newEnglishParaphrases.forEach(function(paraphrase, index) {
                    addParaphrase('english-paraphrase-list', index, paraphrase);
                });

                // 添加新的中文 paraphrases
                newChineseParaphrases.forEach(function(paraphrase, index) {
                    addParaphrase('chinese-paraphrase-list', index, paraphrase);
                });

                // 将列表滚动到最底部
                var englishParaphraseList = $("#english-paraphrase-list");
                englishParaphraseList.scrollTop(0);  // 将滚动条设置为顶部

                var chineseParaphraseList = $("#chinese-paraphrase-list");
                chineseParaphraseList.scrollTop(0);  // 将滚动条设置为顶部

                alert("Generate paraphrases successfully!");
            }else {
                alert("Generate paraphrases fail!");
            }
        },
        error: function(error) {
            // 隐藏“生成中”的提示信息
            $("#loadingMessage").hide();
            console.error('Error generating paraphrases:', error);
            alert("{% trans 'Error generating paraphrases.' %}");
        }
    });
});
