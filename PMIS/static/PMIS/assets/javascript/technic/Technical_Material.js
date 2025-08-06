var technic_data = {tecmb:{},steps:[],example:[],precaution:[]}
$(function () {
    var per_row1 = new SWRow();
    var Verifybtn = new SWButton("Verifybtn", "btn btn-primary", gettext('Confirm'));
    var Auditbtn = new SWButton("Auditbtn", "btn btn-primary",gettext('Audit'));
    var unVerifybtn = new SWButton("unVerifybtn", "btn btn-primary", gettext('UnConfirm'));
    var unAuditbtn = new SWButton("unAuditbtn", "btn btn-primary", gettext('UnAudit'));
    // var needEdit = new SWButton("needEdit", "btn btn-primary", "需修改");
    var DoEdit = new SWButton("DoEdit", "btn btn-primary", gettext('Edit'));

    var DoDesing = new SWButton("printReport", "btn btn-primary", gettext('Pring_Report'));
    var Download = new SWButton("Download", "btn btn-primary", gettext('Download'));//syl 20231013
    per_row1.addComponent(Verifybtn);
    per_row1.addComponent(Auditbtn);
    per_row1.addComponent(unVerifybtn);
    per_row1.addComponent(unAuditbtn);
    // per_row1.addComponent(needEdit);
    per_row1.addComponent(DoEdit);
    per_row1.addComponent(DoDesing);
    per_row1.addComponent(Download); //syl 20231013




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
            window.location.href='/PMIS/Technical_Material_update?pk=' + $('#tecmbid').val()
        }else if(btnid == 'printReport'){
            get_Technical($('#technicalid_input').val().replaceAll(' ',''),$('#technicalinc_id_input').val().replaceAll(' ',''))
            // design_report(`/static/PMIS/TechnicalReport.mrt`, reportdata);
            // preview_report(`/static/PMIS/TechnicalReport.mrt`,reportdata)
        }else if(btnid == 'Download'){ //syl 20231013
            window.location.href='/PMIS/download_tecnical_word?id=' + $('#tecmbid').val() //將概念轉為Word文檔下載查看
        }else{
            if(status!='' && param!=''){updateTechnical(param,status);}
        }
    });

    $("#expandedBtn").on('click',function(e){
        e.preventDefault();
        $(this).parent().closest(".conBox").toggleClass("page-expanded");
        var icon = $(this).find("i");
        if (icon.hasClass("fa-expand-alt")) {
            icon.removeClass("fa-expand-alt").addClass("fa-compress-alt");
        } else {
            icon.removeClass("fa-compress-alt").addClass("fa-expand-alt");
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

