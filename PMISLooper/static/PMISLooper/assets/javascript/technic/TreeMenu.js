var Errorlist = new Array();
var statusdesclist = new Array()
$(function () {
    var row1 = new SWRow()
    var contact = new SWCombobox("selectcontact", gettext("Contact"), window.CommonData.PartUserNames);
    contact.setHorizontalDisplay();
    contact.setHorizontalDisplay();
    var combobox1 = new SWCombobox("selectMonthTime", gettext("Month"), "/looper/DailyPlanner/getRecentlyinMarchu", '', value_field = 'MonthTime', lable_field = 'MonthTime');
    combobox1.setHorizontalDisplay();
    var button1 = new SWButton("btnSelect", "btn-danger", "SELECT");
    row1.addComponent(contact);
    row1.addComponent(combobox1);
    //row1.addComponent(button1);
    $("#Optiondiv").append(row1.dom);

    

    $('body').tooltip({
        selector: '[data-toggle="tooltip"]'
    });

    if (SWApp.os.isAndroid || SWApp.os.isPhone) {
        $("#pciframe").remove();
        $("#pc_technic").attr("id", "mobile_technic");
    }
    else {
        $("#mobile_technic").attr("id", "pc_technic");
    }

    $("body").addClass("technic_daily_planner");


    $(".page").addClass("has-sidebar has-sidebar-expand-xl sidebar_cust");
    $(".app-main").css("padding-bottom", "0");

    if (SWApp.os.isAndroid || SWApp.os.isPhone) {
        $("#splitter").attr("id", "pc_sidebar").addClass("page-sidebar");
        $(".col_cust").addClass("ps-20");
        $(".sidebar-sec .card-header").addClass("d-none");
        $(".tree-demo").css("overflow", "hidden");
    }else {
        $("#pc_sidebar").attr("id", "splitter");
        // 分隔條插件
        var splitter = $('#splitter').split({
            orientation: 'vertical',
            position: '82%'
        });
    }
    // jsTree插件  
    $("#techtree").jstree({
        "core": {
            "themes": {
                "responsive": false,
                "dots": false,
            },
            "check_callback": true,
            'data': function (obj, callback) {
                var jsonarray = new Array();
                $.ajax({
                    type: "GET",
                    url: "/looper/DailyPlanner/selectTreeMenu",
                    dataType: "json",
                    async: false,
                    success: function (result) {
                        var arrays = result.data;
                        for (var i = 0; i < arrays.length; i++) {
                            var arr = {
                                "id": arrays[i].FolderID,
                                "parent": arrays[i].ParentID == 0 ? "#" : arrays[i].ParentID,
                                "text": arrays[i].FolderName,
                                'state': {
                                    'opened': true
                                },
                            }
                            jsonarray.push(arr);
                            if (arrays[i].dailyplannerstatus != 'N' && arrays[i].dailyplannerstatus != '' && arrays[i].dailyplannerstatus != null) {
                                Errorlist.push(arrays[i].FolderID)
                                statusdesclist.push(arrays[i].statusdesc)
                            }
                        }
                    }
                });
                callback.call(this, jsonarray);
            },
        },
        "types": {
            "default": {
                "icon": "fa fa-cloud text-warning"
            }
        },
        "plugins": [
            "contextmenu",
            "dnd",
            "types",
            "wholerow",
            "unique"
        ],
        'contextmenu': {
            'select_node': false,
            'items': technicMenu
        }
    });

    //聯繫人和用戶改變事件
    $("[name='selectcontact'] select").change(function () {
        if($("[name='selectcontact'] select").val()!='' && $("[name='selectMonthTime'] select").val()!=''){selectDetailPlanner()}
    })
    $("[name='selectMonthTime'] select").change(function () {
        if($("[name='selectcontact'] select").val()!='' && $("[name='selectMonthTime'] select").val()!=''){selectDetailPlanner()}
    })

    //新增Task點擊方法
    $("a").click(".card-header-item", function () { createTask(''); })

    //樹狀圖節點點擊事件
    $('#techtree').bind("activate_node.jstree", jstreenodeclick);

    //jstree加載完成後調用的方法
    $('#techtree').on('ready.jstree', jstreeRead);

    $('#techtree').on('dblclick','a',function(){
        if(this.id.slice(0, 10) == 'Technical_'){
            window.open('/PMIS/newOpportunity')
        }
    })

    $('#Optiondiv .col ').css("padding","0px");
    //$('#Optiondiv .col .SWCombobox ').css("padding","0px");
    $("#Optiondiv .col").width('50%');

});

//樹狀圖右鍵菜單
function technicMenu(node) {
    return {
        reportItem: {
            "label": gettext("Detail Technic Report"),
            "action": function (obj) {
                var currentNode = obj.reference[0] //當前節點
                //Task詳情
                if (currentNode.text.slice(0, 4) == 'Task') {
                    var inc_id = currentNode.id.slice(19,-7)
                    if (SWApp.os.isMobile) {
                        $('#phoneiframe').attr('src', "/looper/technic/technical_statement?pk="+inc_id,);
                        Looper.toggleSidebar()
                    } else {
                        $('#pciframe').attr('src', "/looper/technic/technical_statement?pk="+inc_id,);
                    }   
                }else{
                    alert('請選中Detail Planner再選擇該選項！')
                }
            }
        },   
        createItem: {
            "label": gettext("New Page"),
            "action": function (obj, e) {
                // 获取节点
                var currentNode = obj.reference[0] //當前節點
                var parentNode = obj.reference[0].parentElement.parentElement.parentElement  //父節點
                var thecontact = $("[name='selectcontact'] select").val()
                var theinputdate = ''
                var theitemno = ''
                if (currentNode.text.slice(0, 4) == 'Task') {
                    theinputdate = currentNode.id.slice(0, 8)
                    theitemno = currentNode.id.slice(8,13)
                }else  if(parentNode.id=='techtree'){
                    var childNode = currentNode.nextSibling.lastChild.children
                    theinputdate = currentNode.id.slice(3,11)
                    theitemno = childNode[2].id.slice(8,13)
                }else{
                    theinputdate = parentNode.id.slice(0, 8)
                    theitemno = parentNode.id.slice(8,13)
                }
                $('input[name="contact"]').val(thecontact)
                $('input[name="inputdate"]').val(theinputdate)
                $('input[name="itemno"]').val(theitemno)
                //window.location.href="/looper/technic/createUI?contact=" + thecontact+"&inputdate="+theinputdate+"&itemno="+theitemno;
                //$('#theiframe').attr('src',"/looper/technic/createUI?contact=" + thecontact+"&inputdate="+theinputdate+"&itemno="+theitemno);
                if (SWApp.os.isMobile) {
                    $('#phoneiframe').attr('src', "/looper/technic/createUI?contact=" + thecontact + "&inputdate=" + theinputdate + "&itemno=" + theitemno);
                    Looper.toggleSidebar()
                } else {
                    $('#pciframe').attr('src', "/looper/technic/createUI?contact=" + thecontact + "&inputdate=" + theinputdate + "&itemno=" + theitemno);
                }
            }
        },
        // renameItem: {
        //     "label": "Create Code",
        //     "action": function (obj) {
        //         // 获取节点
        //         var currentNode = obj.reference[0] //當前節點
        //         var parentNode = obj.reference[0].parentElement.parentElement.parentElement  //父節點
        //         var thecontact = parentNode.id.slice(0, -8)
        //         var theinputdate = currentNode.id.slice(0, 8)
        //         var theitemno = currentNode.id.slice(8, 13)
        //         $('input[name="contact"]').val(thecontact)
        //         $('input[name="inputdate"]').val(theinputdate)
        //         $('input[name="itemno"]').val(theitemno)
        //         //window.location.href="/looper/technic/createUI?contact=" + thecontact+"&inputdate="+theinputdate+"&itemno="+theitemno;
        //         // $('#theiframe').attr('src',"/looper/technic/createUI?contact=" + thecontact+"&inputdate="+theinputdate+"&itemno="+theitemno);
        //         if (SWApp.os.isMobile) {
        //             $('#phoneiframe').attr('src', "/looper/technic/createUI?contact=" + thecontact + "&inputdate=" + theinputdate + "&itemno=" + theitemno);
        //             Looper.toggleSidebar()
        //         } else {
        //             $('#pciframe').attr('src', "/looper/technic/createUI?contact=" + thecontact + "&inputdate=" + theinputdate + "&itemno=" + theitemno);
        //         }
        //     }
        // },
        updateItem: {
            "label": gettext("Create Task"),
            "action": function (obj) {
                var inputdate=''
                var currentNode = obj.reference[0] //當前節點
                var parentNode = obj.reference[0].parentElement.parentElement.parentElement.id  //父節點
                if(parentNode=='techtree'){
                    inputdate=currentNode.text
                }
                createTask(inputdate);
            }
        },
        deleteItem: {
            "label": gettext("Delete"),
            "action": function (obj) {
                var currentNode = obj.reference[0] //當前節點
                var parentNode = obj.reference[0].parentElement.parentElement.parentElement  //父節點
                //窗口文檔
                if (currentNode.id.slice(-10,-7) == 'Frm') {
                    alert('窗口文檔刪除請去除Task詳情中的Frame Specification輸入框值！')
                    return
                }
                //流程圖
                if (currentNode.text == 'Flowchart') {
                    alert('流程圖刪除請去除Task詳情中的Flowchart輸入框值！')
                    return
                }
                //技術文檔
                if (currentNode.id.slice(0, 10) == 'Technical_') {
                    var fl = confirm("確定要刪除該技術文檔？");
                    if (!fl) {return}
                    var pk = currentNode.id.split('_')[2]
                    var url = "/looper/DailyPlanner/SolutionDelete?pk=[[pk]]"
                    url = url.render({ pk: pk })
                    $.ajax({
                        type: "POST",
                        url: url,
                        traditional: true,
                        dataType: "json",
                        beforeSend: function (request) {
                            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                        },
                        success: function (result) {
                            if (result.status) {selectDetailPlanner()}
                        }
                    });
                    return
                }
                //Page詳情
                if (currentNode.id.slice(8,15)  == 'ThePage') {
                    var fl = confirm("確定要刪除該分頁？");
                    if (!fl) {return}
                    var theinc_id = currentNode.id.slice(20,-7)
                    var argument = {'inc_id':theinc_id}
                    $.ajax({
                        type: "GET",
                        url: "/looper/DailyPlanner/TaskCodeDelete",
                        dataType: "json",
                        data: argument,
                        async: false,
                        success: function (result) {
                            if (result.status) {selectDetailPlanner()}
                        }
                    })
                    return
                }
                //Task詳情
                if (currentNode.text.slice(0, 4) == 'Task') {
                    var fl = confirm("確定要刪除該DailyPlanner？");
                    if (!fl) {return}
                    var thecontact = $("[name='selectcontact'] select").val()
                    var theinputdate = currentNode.id.slice(0, 8)
                    var theitemno = currentNode.id.slice(8, 13)
                    var argument = {'contact':thecontact,'inputdate':theinputdate,'itemno':theitemno}
                    $.ajax({
                        type: "GET",
                        url: "/looper/DailyPlanner/DeletemoreDailyPlanner",
                        dataType: "json",
                        data: argument,
                        async: false,
                        success: function (result) {
                            if (result.status) {selectDetailPlanner()}
                        }
                    })
                    return
                }
                if(parentNode.id=='techtree'){
                    var fl = confirm("確定要刪除該日期下所有DailyPlanner和關聯文檔？");
                    if (!fl) {return}
                    var thecontact = $("[name='selectcontact'] select").val()
                    var theinputdate = currentNode.id.slice(3,11)
                    var argument = {'contact':thecontact,'inputdate':theinputdate,'itemno':''}
                    $.ajax({
                        type: "GET",
                        url: "/looper/DailyPlanner/DeletemoreDailyPlanner",
                        dataType: "json",
                        data: argument,
                        async: false,
                        success: function (result) {
                            if (result.status) {selectDetailPlanner()}
                        }
                    })
                    return
                }
            }
        },        
        gotoDevelopment: {
            "label": gettext("Goto Development"), 
            "action": function (obj) {
                var currentNode = obj.reference[0] //當前節點
                //Task詳情
                if (currentNode.text.slice(0, 4) == 'Task') {
                    var inc_id = currentNode.id.slice(19,-7)
                    var url = "/looper/DailyPlanner/get_development?pk="+inc_id;
                    $.get(url, function(result){
                        if (result.status) {
                            var recordid = result.data.recordid;
                            var sessionid = result.data.sessionid;
                            window.open(`/devplat/sessions?recordid=${recordid}&menu_id=mi_${sessionid}#Requirements`, "_blank");
                        }
                    });
                }else{
                    alert('請選中Detail Planner再選擇該選項！')
                }                
            }                   
        }
    }
}

//創建新Task功能按鈕點擊方法
function createTask(inputdate) {
    if (inputdate==''){
        if (SWApp.os.isMobile) {
            $('#phoneiframe').attr('src', '/looper/technic/createdailyplanner');
            Looper.toggleSidebar()
        } else {
            $('#pciframe').attr('src', '/looper/technic/createdailyplanner');
        }
    }else{
        if (SWApp.os.isMobile) {
            $('#phoneiframe').attr('src', '/looper/technic/createdailyplanner?inputdate='+inputdate);
            Looper.toggleSidebar()
        } else {
            $('#pciframe').attr('src', '/looper/technic/createdailyplanner?inputdate='+inputdate);
        }
    }
}

//樹狀圖節點點擊方法
function jstreenodeclick(obj, e) {
    // 获取当前节点
    var currentNode = e.node;
    //技術文檔
    if (currentNode.id.slice(0, 10) == 'Technical_') {
        var param = currentNode.text.slice(0, 14)
        var inc_id = currentNode.id.split('_')[1]
        //window.open("http://183.63.205.83:8000/PMIS/opportunity/Technical_Material?param=" + param);
        if (SWApp.os.isMobile) {
            $('#phoneiframe').attr('src', '/PMIS/opportunity/Technical_Material?detailplanner=Y&param=' + param+'&inc_id='+inc_id);
            Looper.toggleSidebar()
        } else {
            $('#pciframe').attr('src', '/PMIS/opportunity/Technical_Material?detailplanner=Y&param=' + param+'&inc_id='+inc_id);
        }
    }
    //Task詳情
    if (currentNode.text.slice(0, 4) == 'Task') {
        var pk = currentNode.id.slice(19)
        if (SWApp.os.isMobile) {
            $('#phoneiframe').attr('src', '/looper/technic/createdailyplanner?pk=' + pk);
            Looper.toggleSidebar()
        } else {
            $('#pciframe').attr('src', '/looper/technic/createdailyplanner?pk=' + pk);
        }
    }
    //窗口文檔
    if (currentNode.id.slice(-3) == 'Frm') {
        var framespecification = currentNode.text.trim()
        if (SWApp.os.isMobile) {
            window.open('http://192.168.2.111:8888/PMSApp/technicdoc.do?frmName=' + framespecification)
        } else {
            window.open('http://192.168.2.111:8888/PMSApp/technicdoc.do?frmName=' + framespecification)
        }
    }
    //流程圖
    if (currentNode.text == 'Flowchart') {
        var Flowchartid = currentNode.id.slice(9).trim()
        window.open('http://183.63.205.83:8888/WEBPMS/FlowChart/Main.html?username=qfq&no=' + Flowchartid+'&*#')
    }
    //Page詳情
    if (currentNode.id.slice(8,15)  == 'ThePage') {
        var theinc_id = currentNode.id.slice(20);
        if (SWApp.os.isMobile) {
            $('#phoneiframe').attr('src', "/looper/technic/createUI?inc_id=" + theinc_id);
            Looper.toggleSidebar()
        } else {
            $('#pciframe').attr('src', "/looper/technic/createUI?inc_id=" + theinc_id);
        }
    }
}


//獲取路由的參數
function getQueryString(name) {  
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");  
    var r = window.location.search.substr(1).match(reg);  
    if (r != null) return decodeURI(r[2]);
    return '';  
}


//樹狀圖加載後事件
function jstreeRead(event, obj) {
    // for (var i = 0; i < Errorlist.length; i++) {
    //     $("#" + Errorlist[i] + "_anchor").css("color", "#F00");
    //     $("#" + Errorlist[i] + "_anchor").attr({ "data-toggle": "tooltip", "data-placement": "right", "title": "", "data-original-title": statusdesclist[i] });
    // }
    // Errorlist = []
    // statusdesclist = []
    // $("#Optiondiv .div-1 .form-control").width('28%');

    //獲取對應參數




    var parameterinc_id = getQueryString('inc_id'); 
    var parametercontact = getQueryString('contact'); 
    var parameterinputdate = getQueryString('inputdate')==''?'': Date.parseExact(getQueryString('inputdate'), 'yyyyMMdd').toString("yyyy-MM");
    //當聯繫人和日期不為空時刷新樹狀圖數據
    if(parametercontact!='' && parameterinputdate!=''){
        $("[name='selectcontact'] select").val(parametercontact)
        $("[name='selectMonthTime'] select").val(parameterinputdate)
        $("[name='selectcontact'] select").siblings('button').find(".filter-option-inner-inner").html(parametercontact)
        $("[name='selectMonthTime'] select").siblings('button').find(".filter-option-inner-inner").html(parameterinputdate)
        selectDetailPlanner()
    }
    //當Daily Planner的INC_ID不為空時顯示對應報表
    if(parameterinc_id!=''){
        if (SWApp.os.isMobile) {
            $('#phoneiframe').attr('src', "/looper/technic/technical_statement?pk="+parameterinc_id,);
            Looper.toggleSidebar()
        } else {
            $('#pciframe').attr('src', "/looper/technic/technical_statement?pk="+parameterinc_id,);
        }  
    }
}

//查詢某人某月的DetailPlanner
function selectDetailPlanner() {
    $.ajax({
        type: "GET",
        url: "/looper/DailyPlanner/selectTreeMenu",
        dataType: "json",
        data: { "contact": $("[name='selectcontact'] select").val(), "monthday": $("[name='selectMonthTime'] select").val() },
        async: false,
        success: function (result) {
            var jsonarray = new Array();
            var arrays = result.data;
            var pk = getParamFromUrl('inc_id');
            for (var i = 0; i < arrays.length; i++) {
                var arr = {
                    "id": arrays[i].FolderID,
                    "parent": arrays[i].ParentID == 0 ? "#" : arrays[i].ParentID,
                    "text": arrays[i].FolderName,
                    'state': {
                        'opened': true,
                        'selected': arrays[i].FolderID.indexOf('inc_id'+pk)!=-1?true:false // 设置节点被选中
                    },
                }
                jsonarray.push(arr);
                if (arrays[i].dailyplannerstatus != 'N' && arrays[i].dailyplannerstatus != '' && arrays[i].dailyplannerstatus != null) {
                    Errorlist.push(arrays[i].FolderID)
                    statusdesclist.push(arrays[i].statusdesc)
                }
            }
            $('#techtree').jstree(true).destroy();// 清除树节点
            // 重新设置树的JSON数据集
            $('#techtree').jstree({
                "themes": {
                    "responsive": false,
                    "dots": false,
                },
                "check_callback": true,
                'core': { 'data': jsonarray },
                "types": {
                    "default": {
                        "icon": "fa fa-cloud text-warning"
                    }
                },
                "plugins": [
                    "contextmenu",
                    "types",
                    "wholerow",
                    "unique",
                ],
                'contextmenu': {
                    'select_node': false,
                    'items': technicMenu
                }
            }).on('ready.jstree', function(e, data) {
                window.setTimeout(function () {
                    var pk = getParamFromUrl('inc_id');
                    if (pk != '') {
                        var selected = $('#techtree').jstree(true).get_node(`[id$="inc_id${pk}_anchor`)
                        if (selected != false){
                            $('#techtree').jstree('select_node',selected['id']);
                        }
                    }
                }, 1000);
            }).on('select_node.jstree', function (e, data) {
                // 获取选中节点的 ID 或索引
                var nodeId = data.node.id;
                $('#' + nodeId).get(0).scrollIntoView({ behavior: 'smooth', block: 'center' });
              });
            $('#techtree').jstree(true).refresh(); // 刷新树
            $('#techtree').bind("activate_node.jstree", jstreenodeclick);
        }
    })


}



