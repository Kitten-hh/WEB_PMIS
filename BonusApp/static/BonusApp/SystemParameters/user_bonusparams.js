$('title').html('Bonus Simulation')
$(function(){      
    $("#kt_footer").remove();
    var table = new SWDataTable("#db_wapper","bonusparam_datatable");
    //table.pageLength = 7; //设置每页显示的数量
    table.paging = false; //设置分页显示
    table.searching = true;//不显示查询框
    //table.groupBy = 'inc_id'; //设置按照什么分类
    //table.orderBy = [['inc_id','asc']];
    table.columns = [
        { field: "username", label: "User Name" },
        { field: "budgetallowance", label: "Budget Allowance %" },
        { field: "managementratio", label: "Mag %" },
        { field: "performanaceratio", label:"Per %" },
        { field: "ratioofm", label: "Ratio of M" },
        { field: "ratioofp", label: "Ratio of P" },
        { field: "ratioofs", label: "Ratio of S" },
        { field: "salary", label: "Salary" },
        
    ]; 
    table.setOptions(
        {                        
            responsive: true,
            //scrollY: "600px",
            scrollCollapse: true, 
            drawCallback: function (settings) {
                var api = this.api();
                $("#bonusparam_datatable tbody tr").dblclick(function(e){               
                    //var table = $('#dt_task').DataTable();
                    //得到當前行的id
                    var id = api.row(this).data()['username'];   
                    form.set_pk(id);
                    form.init_data();     
                    $("#editModal").modal("show");                             
                });                
            }
        });  
    //table.setOptions({"columnDefs": [{"targets": [2],"visible": false}]});
    table.init('/bonus/user_bonusparams')  
});

var form = new SWBaseForm("#editModal")
    form.pk_in_url = false; //這種情況必須設置pk_in_url = false
    form.update_url = "bonus/update/[[pk]]"; //更新動作url
    form.on_after_save = function(data) {
        $("#editModal").modal("hide"); //保存成功後，隱藏該modal
        var _table = $("#bonusparam_datatable").DataTable();
        _table.draw(true);
    }

$("#db_wapper").on('click','#sys_datatable tr', function () {
    var inc_id = $(this).find("td").eq(0).text();
    window.location.href = '/bonus/get_Syspara_Details/?inc_id=' + inc_id;
});

// 输入框回车事件
$("#sys_datatable_filter input").keyup(function(){
    if(event.keyCode == 13){ 
        search(); 
    }
});

//function search()

