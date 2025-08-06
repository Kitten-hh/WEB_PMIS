$(function () {
    // 模擬 Vue 的 data 函數
    var state = {
        isFullScreen: false,
        InputVal: "",
        predefinedData: [],
        predefinedData_master: { 'master': [], 'detail': [] },
        defaultOptionSelected: [],
        questionType:'meeting',
        iframe_src: "http://183.63.205.83:3000/aiChat"
        //iframe_src: "http://222.118.20.236:3002/aiChat"
        
    };

    // 方法對象來模擬 Vue 的方法
    var methods = {
        sendDataToReact: function(sendtype = "") {
            var iframeWindow = document.getElementById("ChatAI_iframe").contentWindow;
            var message = {
                type: "updateData",
                sendData: "This is data to analyze. You don't have to do anything, okay:" + JSON.stringify(state.predefinedData)
            };

            if (sendtype === "InputVal") {
                message = {
                    type: "InputVal",
                    sendData: state.InputVal
                };
            }

            if (sendtype === "predefinedData_master") {
                message = {
                    type: "updateData",
                    sendData: "For the following master and detail data that you need to analyze, you don't need to do anything at the moment:" + JSON.stringify(state.predefinedData)
                };
            }
            iframeWindow.postMessage(message, state.iframe_src);
        },

        toggleAIBox: function(e) {
            e.preventDefault();
            var chatAI = document.getElementById("ChatAI");
            chatAI.classList.toggle("fullScreen");
            state.isFullScreen = !state.isFullScreen;
        }
    };

    // 模擬掛載生命週期鉤子
    function mounted() {
        //配置iframe加載時動作和加載網址
        function calculateIframeHeight() {
            var iframeWrapper = window.innerHeight/5*3
            $("#ChatAI_iframe").height(iframeWrapper);
        }
        $('#ChatAI_iframe').on("load", function () {
            calculateIframeHeight();
        }).attr('src', state.iframe_src);
        init_aiPresetQuestion()
    }


    function init_aiPresetQuestion(){
        var sessionid = '11580-520'
        var url = `/looper/task/get_requirement_task?sessionid=${sessionid}`
        if(state.questionType=='session') {
            url = `/PMIS/public/get_syspara?ftype=ProjectStatusQuestion`
        }
        $.ajax({
            url:url,
            type:"GET",
            beforeSend: function(request){
                request.setRequestHeader("X-CSRFToken", self.getCookie('csrftoken'));
            },                
            success:function(response) {
                if (response.status) {
                    var resultdata = []
                    if(state.questionType=='meeting'){
                        for(var item of response.data){
                          if(item['taskid']!='10'){
                            resultdata.push(item['task'])
                          }
                        }
                    }
                    if(state.questionType=='session'){
                        for(var item of response.data){
                            resultdata.push(item['fvalue'])
                        }
                    }
                    state.defaultOptionSelected = resultdata
                    init_QuestionSelect()
                }
            }
        })
    }


    function init_QuestionSelect() {
        var questionSelectContainer = $('#chatAI_modal .questionSelect');
        questionSelectContainer.empty(); // 更直接的清空方法
    
        var strhtml = '';
        for (var item of state.defaultOptionSelected) {
            strhtml += '<div class="custom-control custom-radio dropdown-item"><label class="custom-control-label d-flex justify-content-between">' + item + '</label></div>';
        }
        questionSelectContainer.html(strhtml); // 一次性添加所有選項
    
        questionSelectContainer.on('click', '.custom-control-label', function(e) { // 事件委派
            state['InputVal'] = $(this).text();
            methods.sendDataToReact('InputVal');
        });
    }
    

    window.init_AI = function(val,field_name='',show_modal=true) {
        state[field_name] = val;
        if(field_name=='questionType')
            init_aiPresetQuestion();
        else
            methods.sendDataToReact(field_name);
        if(show_modal)
            $('#chatAI_modal').modal("show");  
    }

    mounted()
});