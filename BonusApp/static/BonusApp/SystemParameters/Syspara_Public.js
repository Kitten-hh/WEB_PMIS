$(function(){
    var form =new SWForm("#form-wapper","SystemParameters","/bonus/get_Syspara_Add_Page/","POST",false)
    form.addComponent(new SWText("ftype","text","用户名",""));
    form.addComponent(new SWText("inc_id","hidden",""));
    form.addComponent(new SWText("desp","text","所选系统", "BonusApp"));
    form.addComponent(new SWCombobox("nfield","参数名称",["RatioOFM","RatioOFS","RatioOFP","ManagementRatio","PerformanaceRatio","Salary","BudgetAllowance"],""));
    form.addComponent(new SWText("fvalue","text","参数值", ""));

    form.init_data(undefined, "/bonus/update_Syspara/[[pk]]"); 
    form.save_data("/bonus/Add_Syspara/", "/bonus/update_Syspara/[[pk]]", "/bonus/get_systemParameters/");
})

$("#form-wapper").on('click','.btn-danger', function(e){
    e.preventDefault();
    var self = $(this)
    GenericDelete($(this), "/bonus/delete_Syspara/[[pk]]", "/bonus/get_systemParameters/", function(){
        return $("form input[name='inc_id']").val();
    })
})

$("#form-wapper").on('click', '.btn-secondary', function () {
    window.location.href = '/bonus/get_systemParameters/'
})

$("#prev_page").click(function () {
    history.go(-1);
})
