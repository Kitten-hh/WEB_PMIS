$(function(){
    /**
    var user_li = $(".app .top-bar-item-right li:eq(1)");
    user_li.children("a").attr({"data-toggle":"dropdown","aria-haspopup":"true","aria-expanded":"false"});
    user_li.addClass("dropdown header-nav-dropdown").append($("#User_menu").html());
    var form_container = user_li.find("form");
    form_container.find(".login").on("click", login);
    */

    var account = $("header.aside-header");
    var account_phone = $("#auth-info-phone");
    account.find(".btn-account").replaceWith(account_phone.find(".btn-account"));
    account.find("#dropdown-aside").replaceWith(account_phone.find("#dropdown-aside"));
    // user_li.addClass("d-none d-md-block");
    var loginModal =  $("#userLogin");
    loginModal.find(".modal-body").append($("#User_menu .auth-page").html());
    loginModal.find(".login").replaceWith(`<button class="btn btn-lg btn-primary btn-block users-login" type="submit">登錄</button>`);
    loginModal.find(".custom-checkbox input").attr("id","remember-me-phone");
    loginModal.find(".custom-checkbox label").attr("for","remember-me-phone");
    /**
    //處理彈出登錄框
    var popopLoginModal = $("#login_modal");
    popopLoginModal.find(".modal-body").append($("#User_menu .auth-page").html());
    popopLoginModal.find(".login").replaceWith(`<button class="btn btn-lg btn-primary btn-block users-login" type="submit">登錄</button>`);
    popopLoginModal.find(".custom-checkbox input").attr("id","remember-me-phone");
    popopLoginModal.find(".custom-checkbox label").attr("for","remember-me-phone");
    popopLoginModal.find(".auth-page-title").remove();

    $('#userLogin').on('show.bs.modal', function (e) {
        $("aside.app-aside, .aside-backdrop").removeClass("show");
        $(".top-bar-list .hamburger.hamburger-squeeze").removeClass("active");
      })
    $("#userLogin").find(".users-login").on("click", login);

    function login(e) {
        e.preventDefault();
        var username = $(this).parents("form.auth-form").find("input[name='username']").val();
        var password = $(this).parents("form.auth-form").find("input[name='password']").val();
        var remeber_me = $(this).parents("form.auth-form").find("input[name='remeber-me']").prop('checked');
        if(username==''||password==''){// 或密碼
            SWHintMsg.showToast(form_container[0], "用戶名或密碼不能為空!","info", {position_class:"toast-top-center"});
            return;
        }
        $.ajax({  
            url: '/looper/login',
            data: {'username':username,'password':password},
            type: 'POST',
            dataType: 'json',
            cache: false,
            "beforeSend": function(request){
                request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            success: function(result){
                if(result.status){
                    SWHintMsg.showToast(form_container[0], "登錄成功！","info", {position_class:"toast-top-center"});
                    user_li.children("a").dropdown("toggle");
                    if($("aside.app-aside .hamburger").hasClass("active"))
                        $("#userLogin").modal('toggle');
                    set_login_name(result['data'].username);                        
                    showauth(false);
                }else{
                    if (result.msg != undefined && result.msg != "")
                        SWHintMsg.showToast(form_container[0], result.msg,"error", {position_class:"toast-top-center"});
                    else
                        SWHintMsg.showToast(form_container[0], "登錄失敗!","error", {position_class:"toast-top-center"});
                    set_login_name("");
                }
            }
        });
    }*/
    function islogin() {
        $.get("/looper/is_login", function(result){
            showauth(!result.status);
        });
    }
    function logout(e) {
        e.preventDefault();
        $.ajax({
            url:"/looper/logout",
            type: 'POST',
            dataType: 'json',
            cache: false,            
            "beforeSend": function(request){
                request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },           
            success:function(result) {
                //var lang_code = $("#curr_language_code").val();
                window.location.href = "/looper/login_page?next=/looper/staff_dashboard";
                //set_login_name("");
                //showauth(result.status);
            }
        });
    }
    $(".logout").on("click", logout);
    $(".userLogout").on("click", logout);
    islogin();
})

function showauth(status) {
    var account = $("header.aside-header"); 
    var user_li = $(".app .top-bar-item-right li:eq(1)");   
    var dev_link = $(".top-bar-list .devplat_link");
    if (dev_link.length > 0) {
        var link = dev_link.attr("href");
        var username = get_login_name();
        if (username == "")
            username = "sing";
        link = link.replace(/contact=[^&]+/g, "contact="+username)
        dev_link.attr("href", link);
    }
    if (status) {
        account.find(".btn-account-islogin").addClass("d-none");
        account.find("#dropdown-aside").removeClass("show");
        account.find(".btn-account-login").removeClass("d-none");
        user_li.removeClass("d-none").addClass("d-block"); 
        $(".auth-info").removeClass("d-md-block"); 
    }else {
        account.find(".btn-account-login").addClass("d-none");
        account.find(".btn-account-islogin, .account-icon").removeClass("d-none");
        user_li.removeClass("d-block").addClass("d-none");
        account.find(".account-name").text(get_login_name());
        $(".app .top-bar-item-right .auth-info .account-name").text(get_login_name());
        $(".auth-info").addClass("d-md-block");
    }
}
/**
*功能描述:檢查用戶是否登錄，
*如果沒有登錄彈出登錄框給用戶登錄後，再進行其他操作
**/
function check_login() {
    return new Promise((resolve, reject)=>{
        if (get_login_name() != "") {
            resolve(true);
            return;
        }
        $("#login_modal .users-login").on("click", function(e){
            e.preventDefault();
            var username = $("#login_modal").find("input[name='username']").val();
            var password = $("#login_modal").find("input[name='password']").val();
            var remeber_me = $("#login_modal").find("input[name='remeber-me']").prop('checked');
            if(username==''||password==''){// 或密碼
                SWHintMsg.showToast("#login_modal .modal-body", "用戶名或密碼不能為空!","info", {position_class:"toast-top-center"});
                return;
            }
            $.ajax({  
                url: '/looper/login',
                data: {'username':username,'password':password},
                type: 'POST',
                dataType: 'json',
                cache: false,
                "beforeSend": function(request){
                    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                },
                success: function(result){
                    if(result.status){
                        SWHintMsg.showToast("#login_modal .modal-body", "登錄成功！","info", {position_class:"toast-top-center"});
                        if (remeber_me)
                            setCookie('csrftoken', result['csrftoken'], {expires:Date.today().addDays(30)})
                        else
                            setCookie('csrftoken', result['csrftoken'], {expires:Date.today().addDays(7)})
                        $("#login_modal").modal("hide"); 
                        set_login_name(result['data'].username);
                        showauth(false);
                        resolve(true)
                    }else{
                        if (result.msg != undefined && result.msg != "")
                            SWHintMsg.showToast("#login_modal .modal-body", result.msg,"error", {position_class:"toast-top-center"});
                        else
                            SWHintMsg.showToast("#login_modal .modal-body", "登錄失敗!","error", {position_class:"toast-top-center"});
                        set_login_name("");
                    }
                }
            });        
        });
        $.get("/looper/is_login", function(result){
            if(result.status)
                resolve(true);
            else {
                $("#login_modal").modal("show");
            }
        });
    });
} 