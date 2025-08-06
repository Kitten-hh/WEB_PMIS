$(function(){      
    $("#kt_footer").remove();
    var table = new SWDataTable("#db_wapper", "db_tasktype");                            
    table.paging = false; 
    table.searching = true;//不显示查询框

    table.columns = [          
        { field: "id", label: "IndexNo",width: "80px"},                     
        { field: "tasktype", label: "Task Type" , width: "130px"} ,
        { field: "description", label: "Description",width: "350px"},  
        { field: "score", label: "Score",width: "100px"},                        
    ];    
    //把RestApi返回來的JSON數據顯示在DataTable中    
    table.setOptions(
        {                        
            responsive: true,
            scrollY: "650px",
            scrollCollapse: true, 
            drawCallback: function (settings) {
                var api = this.api();
                $("#db_tasktype tbody tr").dblclick(function(e){               
                    //var table = $('#dt_task').DataTable();
                    //得到當前行的id
                    var id = api.row(this).data()['id'];   
                    window.location.href = '/bonus/tasktype/detail?taskType_Id=' + id;                            
                });                
            }
        });  
    //table.setOptions({"columnDefs": [{"targets": [2],"visible": false}]});
    table.init('/bonus/tasktype/datatable');
});


$("#btnImport").on('click', function () {
     var fileobj = $("#excelFile")[0].files[0];
     var formdata = new FormData();
     formdata.append("excelFile", fileobj);     
     $.ajax({
        url: '/bonus/tasktype/import', 
        //傳到服務端的參數
        data: formdata, 
        //使用Post方式提交，必須傳送X-CSRFToken
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },             
        type: 'POST',
        processData: false, 
        contentType: false, 
        success: function(data){            
            alert(data.msg);
        },
        error: function(xhr, textStatus, errorThrown){
            alert("错误信息:"+xhr.statusText );
        }
     })
 });

 $("#btnDownload").on('click', function () {    
    $.ajax({
       url: '/bonus/tasktype/download',
       type: 'GET',
       success: function(data){            
          
       },       
    })
});
 