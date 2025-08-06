$(function() {      
    
    $('.modal').on('show.bs.modal', function (event) {
        $(this).removeClass("hide");
        var idx = $('.modal:visible').length;
        $(this).css('z-index', 1040 + (10 * idx));
    });

    $('.modal').on('hide.bs.modal', function (event) {
        $(this).addClass("hide");
    });

    $('.modal').on('shown.bs.modal', function (event) {
        var idx = ($('.modal:visible').length) - 1; // raise backdrop after animation.
        $('.modal-backdrop').not('.stacked').css('z-index', 1039 + (10 * idx));
        $('.modal-backdrop').not('.stacked').addClass('stacked');
    });    

    if (SWApp.os.isAndroid || SWApp.os.isPhone)
        $("#dataTables-example").addClass("w-150");
    $("#query_search").on("click", function(){
        $("#exampleModal").modal("show");
        var filter_val = $("#template-users").val();
        if (filter_val === "")
            $("#template-users").val("sing");
        $("#search_filter_btn").click();
    });

    function search_record_filter() {
        var filter_val = $("#template-users").val();
        var is_dialy = $("#IsDaily").is(":checked") ? "Y":"N";
        $.ajax({
            url:"/PMIS/query/search",
            data:{filter:filter_val,is_dialy:is_dialy},
            success:function(data){
                var result = eval(data);
                display_filter_list(result.data);
            },
            fail:function(data) {
                $("#queryfilter. .pre-scrollable").empty();
            }
        })
    }

    $("#search_filter_btn").on("click", function(){
        search_record_filter();
    });

    $("#template-users").on('keypress',function(e) {
        if(e.which == 13) {
            search_record_filter();
        }
    });

    function display_filter_list(data) {
        var dom = $("#SWListgroup").clone();
        dom.removeAttr("id");
        dom.addClass("SWListgroup");
        var item = dom.find("a");
        dom.empty();
        for(d of data) {
            var local_item = item.clone();
            dom.append(local_item.prop("outerHTML").render(d));
        }
        $("#queryfilter .pre-scrollable").empty()
        dom.show();
        $("#queryfilter .pre-scrollable").append(dom);
        $("#queryfilter .pre-scrollable .list-group .tile").css({"background-color":"#fff","color":"#1f3d9d","width":"auto"});
    }

    $("#queryfilter").on(
        {
            dblclick:function(e){
                e.preventDefault(); //阻止按鈕默認動作
                e.stopPropagation();        
                search_task(this);
            },
            longpress:function(e) {
                e.preventDefault(); //阻止按鈕默認動作
                e.stopPropagation();        
                search_task(this);
            }
        },
        ".list-group a"
    );

    
    
    function search_task(self){
        var id = $(self).attr("pk");
        $("input[name='queryFilterId']").val(id);
        $.ajax({
            url:"/PMIS/task/search_with_queryid/" + id,
            success:function(data){
                if (data.status) {
                    show_datatble(data.data);
                }
            },
            error:function(){
                $("#dataTables-example tbody").html('');
            }
        });
        $("#exampleModal").modal("hide");
        return false;
    }

    $("#show_mindmap").on("click", function(e){
        if ($("input[name='queryFilterId']").val() != '') {
            $("#show_mindmap_form").submit();
        }
    })

    function update_task(self) {
        var pk = $(self).find(".pk").text();
        init_task(pk);
    }

    $("#dataTables-example").on(
        {
            dblclick:function(){
                update_task(this);
            },
            longpress:function() {
                update_task(this);
            }
        },
        "tr"
    );

    function show_datatble(data) {
        /**$("#datatable-task").empty();
        var table = new SWDataTable("#datatable-task", "table1"); //創建SWDataTable對象
        table.pageLength = 20; //設置每頁顯示的數量為20
        table.paging = true; //設置分頁顯示
        table.searching = false; //設置不顯示查詢框
        //設置DataTable顯示5個字段，分別是taskno, task,contact, planbdate, planedate
        table.columns = [
        {field: "taskno", label: "TaskNo"},
        {field: "task", label: "Task"},
        {field:"contact", label:"Contact"},
        {field:"schpriority", label:"SchPriority"},
        {field:"planbdate", label:"PlanBDate"},
        {field:"edate", label:"EDate"},
        {field:"progress", label:"Progress"},
        ];
        table.init(data); //根據以上設置好的屬性，初始化table1，數據來源於/server/tasks這個地址    */
        var result = data;
        var html = "";
        for (var i = 0; i < result.length; i++) {
            var row = result[i];
            if (i%2 == 0)
                html += '<tr class="even">';
            else
                html += '<tr class="odd">';
            html += "<td style='color:#91a8f3'>" + row.taskno + "<span class='d-none pk'>" + row.inc_id + "</span></td>";
            html += "<td>" + row.task + "</td>";
            html += "<td>" + row.contact + "</td>";
            html += '<td class="center">' + (row.schpriority == null ? "":row.schpriority) + "</td>";
            if (row.planbdate != null && row.planbdate != undefined && row.planbdate != '') {
                var myDate = new Date(row.planbdate);
                //var month = myDate.getMonth()+1 < 10 ? '0' + (myDate.getMonth()+1) : "" + myDate.getMonth()+1;
                //var day = myDate.getDate() < 10 ? '0' + myDate.getDate() : "" + myDate.getDate();
                //html += '<td class="center">' + myDate.getFullYear() + month + day + "</td>";
                html += '<td class="center">' + myDate.toString("yyyy-MM-dd") + "</td>";
            }else
                html += '<td class="center"></td>';
            if (row.edate != null && row.edate != undefined && row.edate != '') {
                var myDate = new Date(row.edate);
                //var month = myDate.getMonth()+1 < 10 ? '0' + (myDate.getMonth()+1) : "" + myDate.getMonth()+1;
                //var day = myDate.getDate() < 10 ? '0' + myDate.getDate() : "" + myDate.getDate();
                //html += '<td class="center">' + myDate.getFullYear() + month + day + "</td>";                        
                html += '<td class="center">' + myDate.toString("yyyy-MM-dd") + "</td>";                        
            }else
                html += '<td class="center"></td>';
            html += '<td class="center">'
            html += `<span>${row.progress == null ? "": row.progress}</span>`;
            html += "</td></tr>";
        }
        $("#dataTables-example tbody").html(html);
    }
    if (getParamFromUrl("newtask") != null) {
        try {            
            var username = getParamFromUrl("username");
            var url = "/looper/dashboard/analysis_new_task?search_task=true"
            var data = {username:username}        
            $.get(url, data, function(result){
                if (result.status) {
                    show_datatble(result.data);
                }else {
                    alert("讀取數據失敗!");
                }
            });                
        } catch (error) {
            alert("讀取數據失敗!");
        }
    }else 
        show_datatble([])
  });