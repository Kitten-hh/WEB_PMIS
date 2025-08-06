var mindmap_type_form = undefined;
var mindmap_form = undefined;
var mindmap = undefined;
var pre_selected_node = undefined;
var curr_selected_node = undefined;
var jsonarray = undefined;
$(function () {
    $("body").addClass("technic_mindmap");
    $(".page").addClass("has-sidebar has-sidebar-expand-xl sidebar_cust");
    $(".app-main").css("padding-bottom", "0");
    var top_lenght = $(".top-bar").length
    if (top_lenght) {
        if (SWApp.os.isAndroid || SWApp.os.isPhone) {
            $("#splitter").attr("id", "pc_sidebar").addClass("page-sidebar");
            $(".col_cust").addClass("ps-20");
            $(".sidebar-sec .card-header").addClass("d-none");
            $(".tree-demo").css("overflow", "hidden");
        }
        else {
            $("#pc_sidebar").attr("id", "splitter");
            // 分隔條插件
            var splitter = $('#splitter').split({
                orientation: 'vertical',
                position: '83%'
            });
        }
    } else {
        var splitter = $("#splitter").split({
            orientation: 'vertical',
            limit: 1150,
        })
    }
    // 初始化Form
    // mindmap_type_form = new SWForm("#edit_mindmap_type .modal-body", "新增分類", "", "", true);
    // mindmap_type_form.dom.find(".page-inner").removeClass("page-inner");
    // mindmap_type_form.dom.find(".card-header").hide();
    // mindmap_type_form.dom.find(".btn-subtle-info").attr("data-dismiss", "modal");
    // mindmap_type_form.addComponent(new SWText("inc_id", "hidden", ""));
    // mindmap_type_form.addComponent(new SWText("parentid", "hidden", ""));
    // mindmap_type_form.addComponent(new SWText("sdesc", "text", "描述"));
    // mindmap_type_form.addComponent(new SWText("order", "number", "排序"));
    // mindmap_type_form.create_url = "/PMIS/mindmap/type_create";
    // mindmap_type_form.update_url = "/PMIS/mindmap/type_update?pk=[[pk]]";
    // mindmap_type_form.on_after_save = function (data) {
    //     $("#edit_mindmap_type").modal("hide");
    //     $('#techtree').jstree(true).refresh();
    // }
    // mindmap_type_form.pk_in_url = false;

    // mindmap_form = new SWForm("#edit_mindmap .modal-body", "新增Mindmap", "", "", true);
    // mindmap_form.dom.find(".page-inner").removeClass("page-inner");
    // mindmap_form.dom.find(".card-header").hide();
    // mindmap_form.dom.find(".btn-subtle-info").attr("data-dismiss", "modal");
    // mindmap_form.addComponent(new SWText("inc_id", "hidden", ""));
    // mindmap_form.addComponent(new SWText("typeid", "hidden", ""));
    // mindmap_form.addComponent(new SWText("sdesc", "text", "描述"));
    // mindmap_form.addComponent(new SWText("remark", "number", "備註"));
    // mindmap_form.create_url = "/PMIS/mindmap/create";
    // mindmap_form.update_url = "/PMIS/mindmap/update?pk=[[pk]]";
    // mindmap_form.pk_in_url = false;
    // mindmap_form.on_after_save = function (data) {
    //     $("#edit_mindmap").modal("hide");
    //     $('#techtree').jstree(true).refresh();
    // }


    // jsTree插件  
    $("#techtree").jstree({
        "core": {
            "themes": {
                "responsive": false,
                "dots": false,
            },
            "check_callback": true,
            'data': function (obj, callback) {
                jsonarray = new Array();
                jsonarray.push({ id: "-1", parent: "#", text: "MindMap", state: { opened: true } })
                $.ajax({
                    type: "GET",
                    url: "/PMIS/mindmap/get_menu",
                    dataType: "json",
                    async: false,
                    success: function (result) {
                        var arrays = result.data;
                        for (var i = 0; i < arrays.length; i++) {
                            var arr = {
                                "id": arrays[i].id,
                                "data": { "inc_id": arrays[i].inc_id },
                                "parent": arrays[i].parentid == null ? "-1" : arrays[i].parentid,
                                "text": arrays[i].sdesc,
                                "type": arrays[i].id.startsWith("M_") ? "file" : "",
                                'state': {
                                    'opened': true
                                },
                            }
                            jsonarray.push(arr);
                        }
                    }
                });
                callback.call(this, jsonarray);
            },
        },
        "types": {
            "default": {
                "icon": "fa fa-cloud text-warning"
            },
            'file': {
                'icon': 'fa fa-file'
            }
        },
        "plugins": [
            "contextmenu",
            "dnd",
            "types",
            "wholerow",
            "unique",
            "search",

        ],
        // 'contextmenu': {
        //     'select_node': true,
        //     'items': technicMenu
        // },

    }).on('move_node.jstree', function (e, data) {
        // the move already happened
        moveNode(e, data);
    });

    //樹狀圖節點點擊事件
    $('#techtree').bind("activate_node.jstree", jstreenodeclick);
    //
    $("#techtree").bind("select_node.jstree", function (e, data) {
        if (curr_selected_node != undefined)
            pre_selected_node = curr_selected_node;
        curr_selected_node = data.node;
    });
    if (SWApp.os.isMobile)
        mindmap = new SWMindmap("#phoneLeftPanel");
    else
        mindmap = new SWMindmap("#leftPane");
    mindmap.tree_dom = $('#techtree').jstree(true);
    mindmap.on_save = save_mindmap;
    $("#techtree").on("doubletap", ".jstree-anchor", function (e) {
        alert('hey!');
        $(e.currentTarget).trigger('contextmenu'); // either use this line
        $(e.currentTarget).closest('.jstree').jstree(true).show_contextmenu(e.currentTarget, e.pageX, e.pageY, e); // or this line
    });
    $('#techtree').on('longpress', '.jstree-anchor', function (e) {
        alert("aaab");
        $(e.currentTarget).trigger('contextmenu'); // either use this line
        $(e.currentTarget).closest('.jstree').jstree(true).show_contextmenu(e.currentTarget, e.pageX, e.pageY, e); // or this line
    });

});


// function technicMenu(node) {
//     return {
//         createItem: {
//             "label": "新增分類",
//             "action": function (obj, e) {
//                 // 获取节点
//                 var currentNode = obj.reference[0] //當前節點                
//                 if (currentNode.id.startsWith("M_"))
//                     return;
//                 $("#edit_mindmap_type .modal-title").text("新增分類");
//                 $("#edit_mindmap_type").modal("show");

//                 var params = {}
//                 if (currentNode.id != "-1_anchor")
//                     params['parentid'] = $('#techtree').jstree(true).get_node(currentNode.id).data.inc_id
//                 mindmap_type_form.set_pk(undefined);
//                 mindmap_type_form.init_data(params);
//             },
//             "_class": "class"
//         },
//         renameItem: {
//             "label": "新增Mindmap",
//             "action": function (obj) {
//                 // 获取节点
//                 var currentNode = obj.reference[0] //當前節點
//                 if (currentNode.id.startsWith("M_"))
//                     return;
//                 if (currentNode.id == "-1_anchor")
//                     return;
//                 $("#edit_mindmap .modal-title").text("新增Mindmap");
//                 $("#edit_mindmap").modal("show");
//                 var params = {}
//                 params['typeid'] = $('#techtree').jstree(true).get_node(currentNode.id).data.inc_id;
//                 mindmap_form.set_pk(undefined);
//                 mindmap_form.init_data(params);
//             }
//         },
//         modifyItem: {
//             "label": "修改",
//             "action": function (obj) {
//                 var currentNode = obj.reference[0] //當前節點
//                 if (currentNode.id == "-1_anchor")
//                     return;
//                 //如果是Mindmap
//                 if (currentNode.id.startsWith("M_")) {
//                     $("#edit_mindmap .modal-title").text("修改Mindmap");
//                     $("#edit_mindmap").modal("show");
//                     var pk = $('#techtree').jstree(true).get_node(currentNode.id).data.inc_id;
//                     mindmap_form.set_pk(pk);
//                     mindmap_form.init_data();
//                 } else {
//                     $("#edit_mindmap_type .modal-title").text("修改分類");
//                     $("#edit_mindmap_type").modal("show");
//                     var pk = $('#techtree').jstree(true).get_node(currentNode.id).data.inc_id;
//                     mindmap_type_form.set_pk(pk);
//                     mindmap_type_form.init_data();
//                 }
//             }
//         },
//         deleteItem: {
//             "label": "刪除",
//             "action": function (obj, e, data) {
//                 var currentNode = obj.reference[0] //當前節點
//                 if (currentNode.id == "-1_anchor")
//                     return;

//                 //如果是Mindmap
//                 var pk = $('#techtree').jstree(true).get_node(currentNode.id).data.inc_id;
//                 var url = "/PMIS/mindmap/type_del?pk=[[pk]]"
//                 if (currentNode.id.startsWith("M_")) {
//                     url = "/PMIS/mindmap/del?pk=[[pk]]"
//                 };
//                 url = url.render({ pk: pk })
//                 var all_childid = $('#techtree').jstree("get_node", currentNode).children_d;
//                 var flag = confirm("點擊確定後將會刪除此選項及其子選項!");
//                 if (flag) {
//                     $.ajax({
//                         type: "POST",
//                         url: url,
//                         traditional: true,
//                         dataType: "json",
//                         data: { 'all_childid[]': all_childid },
//                         beforeSend: function (request) {
//                             request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
//                         },
//                         success: function (result) {
//                             if (result.status) {
//                                 $('#techtree').jstree(true).refresh();
//                             } else {
//                                 alert("刪除失敗");
//                             }
//                         }
//                     });
//                 }
//             }
//         }
//     };
// }


function jstreenodeclick(obj, e) {
    var dom = $(".SWMindmap .save").length
    if (dom) {
        var f = $(".SWMindmap .save").attr("disabled");
        if (f) {
            load_jsondata(obj, e);
        } else {
            var fl = confirm("當前mindmap已更改,請先保存？");
            if (fl) {
                if (pre_selected_node != undefined && pre_selected_node != curr_selected_node) {
                    $('#techtree').jstree(true).deselect_node(e.node);
                    $('#techtree').jstree(true).select_node(pre_selected_node);
                }
            }
            else {
                load_jsondata(obj, e);
            }
        }
    } else {
        load_jsondata(obj, e);
    }
}

function load_jsondata(obj, e) {
    // 获取当前节点
    var currentNode = e.node;
    if (!currentNode.id.startsWith("M_"))
        return;
    var pk = $('#techtree').jstree(true).get_node(currentNode.id).data.inc_id;
    var url = "/PMIS/mindmap/get_data/" + pk;
    $.get(url, function (result) {
        if (result.status) {
            mindmap.node_data = result.data;
            mindmap.load(result.data);
            if (SWApp.os.isMobile) {
                Looper.toggleSidebar();
            }
        } else {
            alert("獲取MindMap數據失敗");
        }
    });
}

function moveNode(e, data) {
    if (data.parent != data.old_parent) {
        var id = data.node.id;
        var pk = data.node.data["inc_id"];
        var parent = data.parent;
        var url = "/PMIS/mindmap/type_update?pk=[[pk]]"
        var params = { parentid: parent };
        if (id.startsWith("M_")) {
            url = "/PMIS/mindmap/update?pk=[[pk]]"
            params = { typeid: parent };
        }
        url = url.render({ pk: pk });
        $.ajax({
            type: "POST",
            url: url,
            data: params,
            dataType: "json",
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            success: function (result) {
                if (result.status) {
                    $('#techtree').jstree(true).refresh();
                } else {
                    alert("保存失敗");
                }
            }
        });
        console.log("Node was moved to a different tree-instance");
    }
}


function save_mindmap(data) {
    var currentNode = $('#techtree').jstree("get_selected");
    if (currentNode.length == 0 || !currentNode[0].startsWith("M_")) {
        alert("請選擇一個Mindmap");
        return;
    }
    var url = "/PMIS/mindmap/update?pk=[[pk]]"
    var pk = $('#techtree').jstree(true).get_node(currentNode[0]).data.inc_id;
    url = url.render({ pk: pk });
    var def = $.Deferred();
    $.ajax({
        type: "POST",
        url: url,
        data: { data: data },
        dataType: "json",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function (result) {
            if (result.status) {
                alert("保存成功");
                def.resolve("保存成功");
            } else {
                alert("保存失敗");
                def.reject("保存失敗");
            }
        }
    });
    return def;
}

