$(function () {

    var Contact = new SWText("contact", "hidden", "Contact", "");
    var InputDate = new SWText("inputdate", "hidden", "InputDate", "");
    var ItemNo = new SWText("itemno", "hidden", "ItemNo", "");
    var ImageNo = new SWText("imageno", "hidden", "imageno", "");
    var INC_ID = new SWText("inc_id", "hidden", "imageno", "");
    var TextName = new SWText("textname", "text", gettext("Name"), "");
    $("#thehidden").append(Contact.dom);
    $("#thehidden").append(InputDate.dom);
    $("#thehidden").append(ItemNo.dom);
    $("#thehidden").append(ImageNo.dom);
    $("#thehidden").append(INC_ID.dom);
    $("#thehidden").append(TextName.dom);


    // $(".page").addClass("has-sidebar has-sidebar-expand-xl sidebar_cust");
    // $(".app-main").css("padding-bottom", "0");

    //獲取路由的參數
    function getQueryString(name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
        var r = window.location.search.substr(1).match(reg);
        if (r != null) return decodeURI(r[2]);
        return '';
    }

    //獲取對應參數
    var contact = getQueryString('contact');
    var inputdate = getQueryString('inputdate');
    var itemno = getQueryString('itemno');
    var imageno = getQueryString('imageno');
    var inc_id = getQueryString('inc_id');


    //為表格主鍵字段賦值
    if (contact != '' && inputdate != '' && itemno != '') {
        $('input[name="contact"]').val(contact)
        $('input[name="inputdate"]').val(inputdate)
        $('input[name="itemno"]').val(itemno)
        $('input[name="imageno"]').val(imageno)
        $('input[name="inc_id"]').val(inc_id)
    }else if(inc_id !=''){
        $('input[name="inc_id"]').val(inc_id)
    }


    //向頁面創建富文本編輯器SWRichText對象
    var swrichtext = new SWRichText("editor_wrap");

    // 為控件綁定edit 事件
    $("#summernote-edit").on("click", function () {
        swrichtext.edit();
        // $(this).addClass('d-none');
        // $('#summernote-save').removeClass('d-none');
    });

    // 為控件綁定save 事件
    $('#summernote-save').on('click', function () {
        // $(this).addClass('d-none');
        // $('#summernote-edit').removeClass('d-none');
        $.ajax({
            type:'POST',
            url:'/looper/DailyPlanner/TecdailyplannerImageController',
            data:{'contact':$('input[name="contact"]').val(),'inputdate':$('input[name="inputdate"]').val(),'itemno':$('input[name="itemno"]').val(),
                'imageno':$('input[name="imageno"]').val(),'DetailText':swrichtext.save(),'text':$('input[name="textname"]').val()},
            beforeSend: function(request){
                request.setRequestHeader("X-CSRFToken", self.getCookie('csrftoken'));
            },          
            success:function(result){
                if(result.status){
                    jsondata = result.data[0];
                    $('input[name="contact"]').val(jsondata['contact'])
                    $('input[name="inputdate"]').val(jsondata['inputdate'])
                    $('input[name="itemno"]').val(jsondata['itemno'])
                    $('input[name="imageno"]').val(jsondata['imageno'])
                    $('input[name="textname"]').val(jsondata['text'])
                    $('input[name="inc_id"]').val(jsondata['inc_id'])
                    parent.selectDetailPlanner();
                }
            }
        })
    });

    // 為控件綁定load 事件
    // $('#summernote-load').on('click', function () {
    //     swrichtext.load("/looper/DailyPlanner/GetTecdailyplannerImageContent?contact="+contact+"&inputdate="+inputdate+"&itemno="+itemno+"&imageno="+$('input[name="imageno"]').val()+"&isrichtext=1");
    // });
    if (inc_id!=''){
        $.ajax({
            Type:'GET',
            url:'/looper/DailyPlanner/GetTecdailyplannerImageContent',
            data:{'inc_id':$('input[name="inc_id"]').val()},       
            success:function(result){
                if(result.status){
                    jsondata = result.data[0];
                    $('input[name="contact"]').val(jsondata['contact'])
                    $('input[name="inputdate"]').val(jsondata['inputdate'])
                    $('input[name="itemno"]').val(jsondata['itemno'])
                    $('input[name="imageno"]').val(jsondata['imageno'])
                    $('input[name="textname"]').val(jsondata['text'])
                    $('input[name="inc_id"]').val(jsondata['inc_id'])
                    swrichtext.load(jsondata['detailtext']);
                }
            }
        }) 
    }
});







