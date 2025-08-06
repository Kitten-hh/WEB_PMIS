getCookie = (function(_super) {
    return function() {
        if (arguments != undefined && arguments.length > 0 && arguments[0] == 'csrftoken')
            arguments[0] = "csrftoken_WEB_PMIS";
        return _super.apply(this, arguments);
    };         
})(getCookie);
ah.proxy({
    //请求发起前进入
    onRequest: (config, handler) => {
        //console.log(config.url)
        var lang_code = $("#curr_language_code").val();
        if (lang_code != "" && config.url.length > 0) {
            var languages = $("#lang_menu a[lang_code]").map(function() {return "/" + $(this).attr("lang_code");}).get()
            var prefix_str = config.url.charAt(0) == "/" ? "/"+lang_code : lang_code;
            if (!config.url.startsWith(prefix_str) && languages.filter((x)=>config.url.startsWith(x)).length == 0 && !config.url.startsWith("/static"))
                config.url = prefix_str + config.url;
        }           
        handler.next(config);
    },
    //请求发生错误时进入，比如超时；注意，不包括http状态码错误，如404仍然会认为请求成功
    onError: (err, handler) => {
        //console.log(err.type)
        handler.next(err)
    },
    //请求成功后进入
    onResponse: (response, handler) => {
        //console.log(response.response)
        if (handler.xhr.responseURL != undefined && handler.xhr.responseURL.indexOf("/looper/login_page") != -1) {
            // check_login();
            alert("Please Login");
            window.open("/looper/login_page?next="+window.location.pathname)
        }else {
            handler.next(response);
        }
        handler.next(response);
        //console.log(handler.xhr.responseURL);
    }
});
function set_login_name(value) {
    $("#login_username").val(value);
}
function get_login_name() {
    return $("#login_username").val();
}
function get_username() {
    var username = getParamFromUrl("username");
    if (username == undefined)
        username = getParamFromUrl("contact");
    if (username == undefined)
        username = get_login_name();
    if (username == undefined || username == "")
        username = "sing";
    return username;
}
/**
window.winUUID = generateUUID();
const winChannel = new BroadcastChannel('win_operation_channel');

winChannel.onmessage = (event) => {
    const data = event.data;
    if (data.action == "getWin") {
        var lang_code = $("#curr_language_code").val();
        var urlPathName = window.location.pathname;
        if(lang_code != "")
            urlPathName = urlPathName.replace("/"+lang_code, "");
        winChannel.postMessage({ action: 'getWinResult', target:window.name, winUUID:window.winUUID, urlPathName:urlPathName });
    }else if (data.action == "closeWin" && data.uuid == window.winUUID) {
        window.close();
    }
    if (window.name == data.target) {
        if (data.action == "goHome") {
            var home = window.open("", "staff_dashboard");
            var interval = setInterval(() => {
                if(home.document.hidden) {
                    setTimeout(() => {
                        home = window.open("", "staff_dashboard");    
                    });
                }
                else
                    clearInterval(interval);
            }, 200);
        }
    }
    console.log('Received message:', event.data);
};
*/