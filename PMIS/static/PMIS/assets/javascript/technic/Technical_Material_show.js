var technic_data = {tecmb:{},steps:[],example:[],precaution:[]}
$(function () {
    var per_row1 = new SWRow();
    var Verifybtn = new SWButton("Verifybtn", "btn btn-primary", "確認");
    var Auditbtn = new SWButton("Auditbtn", "btn btn-primary", "審核");
    var unVerifybtn = new SWButton("unVerifybtn", "btn btn-primary", "反確認");
    var unAuditbtn = new SWButton("unAuditbtn", "btn btn-primary", "反審核");
    // var needEdit = new SWButton("needEdit", "btn btn-primary", "需修改");
    var DoEdit = new SWButton("DoEdit", "btn btn-primary", "修改");

    var DoDesing = new SWButton("printReport", "btn btn-primary", "打印報表");
    per_row1.addComponent(Verifybtn);
    per_row1.addComponent(Auditbtn);
    per_row1.addComponent(unVerifybtn);
    per_row1.addComponent(unAuditbtn);
    // per_row1.addComponent(needEdit);
    per_row1.addComponent(DoEdit);
    per_row1.addComponent(DoDesing);




    $("#btnVessel").append(per_row1.dom);
    $("#btnVessel").children().css({'justify-content': 'flex-end'})
    //獲取路由的參數
    function getQueryString(name) {  
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");  
        var r = window.location.search.substr(1).match(reg);  
        if (r != null) return decodeURI(r[2]);
        return '';  
    }

    $("#btnVessel button").on('click',function(){
        var param = getQueryString('param'); 
        var status = ''
        var btnid = this.id;
        switch(btnid){
            case 'Verifybtn': 
                status='C';
                break; 
            case 'Auditbtn': 
                status='Y';
                break;    
            case 'unVerifybtn': 
                status='U';
                break;
            case 'unAuditbtn': 
                status='R';
                break;    
            case 'needEdit': 
                status='E';
                break;
        }
        if(btnid == 'DoEdit'){
            window.location.href='/PMIS/Technical_Material_update_show?pk=' + $('#tecmbid').val()
        }else if(btnid == 'printReport'){
            get_Technical($('#technicalid_input').val().replaceAll(' ',''),$('#technicalinc_id_input').val().replaceAll(' ',''))
            // design_report(`/static/PMIS/TechnicalReport.mrt`, reportdata);
            // preview_report(`/static/PMIS/TechnicalReport.mrt`,reportdata)
        }else{
            if(status!='' && param!=''){updateTechnical(param,status);}
        }
    });

    

})


function updateTechnical(Technicalno,status){
    $.ajax({
        type:'POST',
        url:'/PMIS/opportunity/updateTechnical',
        data:{'status':status,'Technicalno':Technicalno},
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", self.getCookie('csrftoken'));
        },          
        success:function(result){
            if(result.status){location.reload()}
        }
    })
}



function get_Technical(param,inc_id){
    $.ajax({
        type: "GET",
        url: "/PMIS/opportunity/Get_technical?get_img=y&param="+param+'&inc_id='+inc_id,
        dataType: "json",
        async: false,
        success: function (result) {
            if (result.state==200) {
                technic_data['tecmb'] = result.data.tecmb;
                technic_data['steps'] = result.data.steps;
                technic_data['example'] = result.data.example;
                technic_data['precaution'] = result.data.precaution;
                var reportdata = {
                    datasource:technic_data
                }
                preview_report(`/static/PMIS/TechnicalReport.mrt`,reportdata)
            }
        }
    })
}

function design_report(report_name, datasource) {
    localStorage.setItem("report_name", report_name);
    localStorage.setItem("report_data", JSON.stringify(datasource));
    window.open("/base_report/design", "_blank")
}     

function preview_report(report_name, datasource) {
    localStorage.setItem("report_name", report_name);
    localStorage.setItem("report_data", JSON.stringify(datasource));
    window.open("/base_report/preview", "_blank")
}

