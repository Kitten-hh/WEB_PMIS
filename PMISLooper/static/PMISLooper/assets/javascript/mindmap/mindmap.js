var mindmap_type_form = undefined;
var mindmap_form = undefined;
var mindmap = undefined;
var pre_selected_node = undefined;
var curr_selected_node = undefined;
var jsonarray = undefined;
var params = undefined;
var hideMenu = getParamFromUrl("hideMenu") == "Y" ? true : false;
if (hideMenu) {
    $("#SWMindmap>.mindmap_wrapper").hide();
    $("#myDiagramDiv").attr("style", $("#myDiagramDiv").attr("style") + "height:calc(100vh - 3.5rem)");
    $("#phoneLeftPanel+.btn-floated").removeAttr("data-toggle");
}
// var self = this;
$(function () {
    $("body").addClass("technic_mindmap");
    if (!(hideMenu && (SWApp.os.isAndroid || SWApp.os.isPhone || SWApp.os.isTablet))) {
        $(".page").addClass("sidebar_cust");
        setTimeout(function() {
            $(".page.sidebar_cust").addClass("has-sidebar has-sidebar-fluid has-sidebar-expand-xl");
        }, 1000)
        $(".page.sidebar_cust").on("click", '.btn-floated', function(e) {
            e.stopPropagation();
            Looper.showSidebar();
        })
    }
    $(".app-main").css("padding-bottom", "0");

    //$(".top-bar-item-right ul li").slice(1,3).remove();
    var top_lenght = $(".top-bar").length;
    if (top_lenght) {
        if (SWApp.os.isAndroid || SWApp.os.isPhone || SWApp.os.isTablet) {
            $("#splitter").attr("id", "pc_sidebar").addClass("page-sidebar");
            $(".col_cust").addClass("ps-20");
            $(".sidebar-sec .card-header").addClass("d-none");
            $(".tree-demo").css("overflow", "hidden");
        } else {
            $("#pc_sidebar").attr("id", "splitter");
            // 分隔條插件
            var splitter = $('#splitter').split({
                orientation: 'vertical',
                position: hideMenu ? '100%' : '83%',
                onDrag: function(event) {
                    mindmap.gojs_layoutAll();
                }
            });
        }
    } else {
        var splitter = $("#splitter").split({
            orientation: 'vertical',
            limit: 1150,
        })
    }
    if (hideMenu)
        $("#splitter .vsplitter").hide();

    // 注釋樣式
    $(".note_wrap").click(function () {
        var toggle = $('.note_wrap');
        var noteT = $('.title_note');
        var note = $('.note');
        if (toggle.hasClass('toggled')) {
            toggle.removeClass('toggled');
            toggle.removeClass('code-on');
            noteT.addClass("d-none");
            note.removeClass("d-none");
            toggle.css("width", "178px");
        } else {
            toggle.addClass('code-on');
            toggle.addClass('toggled');
            noteT.removeClass("d-none");
            note.addClass("d-none");
            toggle.css("width", "0");
        }
    });

    // 版本2:修改按钮显示样式
    var mindmapBtn = `<li id="position" class="nav-item"><a class="nav-link" href="#" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><span class="fas fa-sitemap"></span></a>
    <div class="dropdown-menu dropdown-menu-rich dropdown-menu-right SWMindmap" style="position: absolute; top: 36px; left: -276px; will-change: top, left;" x-placement="bottom-end">
    <div class="dropdown-arrow"></div><div class="dropdown-sheets"></div></div></li>`

    $(".top-bar-item-right .header-nav").append(mindmapBtn);
    $("#position .dropdown-sheets").append($(".mindmap_wrapper .dropdown-sheet-item"));

    var menu_type = getParamFromUrl("type");
    // 初始化Form
    mindmap_type_form = new SWForm("#edit_mindmap_type .modal-body", gettext("Add Folder"), "", "", true);
    mindmap_type_form.dom.find(".page-inner").removeClass("page-inner");
    mindmap_type_form.dom.find(".card-header").hide();
    mindmap_type_form.dom.find(".btn-subtle-info").attr("data-dismiss", "modal");
    mindmap_type_form.addComponent(new SWText("inc_id", "hidden", ""));
    mindmap_type_form.addComponent(new SWText("parentid", "hidden", ""));
    mindmap_type_form.addComponent(new SWText("udf01", "hidden", ""));
    mindmap_type_form.addComponent(new SWText("sdesc", "text", gettext("Description")));
    mindmap_type_form.addComponent(new SWText("order", "number", gettext("Order")));
    mindmap_type_form.create_url = "/PMIS/mindmap/type_create";
    mindmap_type_form.update_url = "/PMIS/mindmap/type_update?pk=[[pk]]";
    mindmap_type_form.on_init_format = function (data) {
        if (menu_type != undefined && menu_type.length > 0)
            data.udf01 = menu_type;
    }
    mindmap_type_form.on_after_save = function (data) {
        $("#edit_mindmap_type").modal("hide");
        $('#techtree').jstree(true).refresh();
    }
    mindmap_type_form.pk_in_url = false;

    mindmap_form = new SWForm("#edit_mindmap .modal-body", gettext("Add Mindmap"), "", "", true);
    mindmap_form.dom.find(".page-inner").removeClass("page-inner");
    mindmap_form.dom.find(".card-header").hide();
    mindmap_form.dom.find(".btn-subtle-info").attr("data-dismiss", "modal");
    mindmap_form.addComponent(new SWText("inc_id", "hidden", ""));
    mindmap_form.addComponent(new SWText("typeid", "hidden", ""));
    mindmap_form.addComponent(new SWCombobox("map_type", gettext("Map Type"),
        [{ value: "1", label: "Tree Mindmap" }, { value: "2", label: "Course Mindmap" }, { value: "3", label: "Project Mindmap" }]));
    mindmap_form.addComponent(new SWText("sdesc", "text", gettext("Description")));
    mindmap_form.addComponent(new SWText("remark", "number", gettext("Remark")));
    mindmap_form.create_url = "/PMIS/mindmap/create";
    mindmap_form.update_url = "/PMIS/mindmap/update?pk=[[pk]]";
    mindmap_form.pk_in_url = false;
    mindmap_form.on_after_init = function (data) {
    }
    mindmap_form.on_after_save = function (data) {
        $("#edit_mindmap").modal("hide");
        $('#techtree').jstree(true).refresh();
    }

    window.select_session = new SWSelectquery("");  //設置Search按鈕為觸發標籤

    window.select_session.table.columns = [
        { field: "sessionid", label: gettext("sessionid") },
        { field: "sdesp", label: gettext("desc") },
    ];
    window.select_session.table.firstColSelected = true;
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
                var url = "/PMIS/mindmap/get_menu";
                if (menu_type != undefined && menu_type.length > 0)
                    url = url + "?type={0}".format(menu_type)
                $.ajax({
                    type: "GET",
                    url: url,
                    dataType: "json",
                    async: false,
                    success: function (result) {
                        var arrays = result.data;
                        for (var i = 0; i < arrays.length; i++) {
                            var arr = {
                                "id": arrays[i].id,
                                "data": { "inc_id": arrays[i].inc_id },
                                "parent": arrays[i].parentid == null ? "-1" : arrays[i].parentid,
                                "text": arrays[i].sdesc + ((!arrays[i].id.startsWith("M_") && arrays[i].order) ? "({0})".format(arrays[i].order) : ""),
                                "map_type": arrays[i].map_type,
                                "type": arrays[i].id.startsWith("M_") ? "file" : "",
                                'state': {
                                    'closed': true
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
            "state",
        ],
        "state": {
            "key": "jstree",
        },
        'contextmenu': {
            'select_node': true,
            'items': technicMenu
        },

    }).on('move_node.jstree', function (e, data) {
        // the move already happened
        moveNode(e, data);
    }).on('loaded.jstree', function (e, data) {
        var pk = getParamFromUrl('pk');
        if (pk != '' && pk != undefined) {
            $('#techtree').jstree(true).clear_state();
            $('#techtree').jstree(true).select_node($('#techtree').jstree(true).get_node(`M_${pk}`));
            $(`#M_${pk} a`).click();
        }else if (window.dynamic_mindmap_json != "") {
            show_dynamic_mindmap();
        }
    });

    //樹狀圖節點點擊事件
    $('#techtree').bind("activate_node.jstree", jstreenodeclick);
    //
    $("#techtree").bind("select_node.jstree", function (e, data) {
        if (curr_selected_node != undefined)
            pre_selected_node = curr_selected_node;
        curr_selected_node = data.node;
    });
    if (SWApp.os.isMobile || SWApp.os.isTablet)
        mindmap = new SWMindmap("#phoneLeftPanel");
    else
        mindmap = new SWMindmap("#leftPane");
    mindmap.tree_dom = $('#techtree').jstree(true);
    mindmap.on_after_save = mindmap_after_save
    // mindmap.on_save = save_mindmap;
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
    /**
    var pk = getParamFromUrl('pk');
    if (pk != '') 
        $(`#${pk}`).dblclick();
    */
    //layout_mindmap(pk)

    if ($('#techtree').jstree(true).get_selected(true).length !== 0)
        mindmap.mindmap_inc_id = $('#techtree').jstree(true).get_selected(true)[0].data.inc_id

    // 修改session明細信息
    window.CommonData = {
        PartUserNames:promiseGet("/PMIS/user/get_part_user_names"), //電腦部用戶
        TaskProgress:promiseGet("/PMIS/task/progresses"), //任務進度
    }

    edit_session_form = new SWForm("#edit_session_form", gettext("Edit Session"), "", "", true);
    edit_session_form.dom.find(".page-inner").removeClass("page-inner");
    edit_session_form.dom.find(".card-header").hide();
    edit_session_form.dom.find(".card-footer>.save").removeClass("btn-subtle-danger").addClass("btn-primary");
    edit_session_form.dom.find(".btn-subtle-info").attr("data-dismiss", "modal").removeClass("btn-subtle-info").addClass("btn-light");

    var sessionID_tmpl = `<div class="sessionWrap d-flex">
                    <label class="mr-2 mb-0">` + gettext("Session") + `:</label>
                    <p id="edit_session_sessionID" class="text-mute mb-0"></p>
                </div>`
    edit_session_form.dom.find(".card-body").append(sessionID_tmpl);

    edit_session_form.addComponent(new SWCombobox("edit_session_contact", gettext("Contact"), window.CommonData.PartUserNames));
    edit_session_form.addComponent(new SWCombobox("edit_session_progress", gettext('Progress'), window.CommonData.TaskProgress));
    edit_session_form.addComponent(new SWDate("edit_session_planbdate", "datetime-local", gettext("PlanBDate")));
    edit_session_form.addComponent(new SWDate("edit_session_planedate", "datetime-local", gettext("PlanEDate")));
    edit_session_form.addComponent(new SWText("edit_session_relationsession", "text", gettext("Relation Session")));
    edit_session_form.addComponent(new SWCombobox("edit_session_relationstatus", gettext('Relation Status'), [{label:"I:"+gettext("relation_status_I"),value:"I"},{label:"F:" + gettext("relation_status_F"), value:"F"}]));
    var relatonSession_tmpl = `<div class="parentSessionWrap d-flex">
    <i id="parentSessionIcon" class="fas fa-level-up-alt fa-rotate-by text-purple"></i>
    <p id="editSession_relationSession" class="text-mute mb-0 ml-3"></p></div></div>`
    edit_session_form.dom.find(".card-body").append(relatonSession_tmpl);
    edit_session_form.addComponent(new SWText("edit_session_parentSession", "text", gettext("Parent Session")));

    var parentSession_tmpl = `<div class="parentSessionWrap d-flex">
    <i id="parentSessionIcon" class="fas fa-level-up-alt fa-rotate-by text-purple"></i>
    <p id="editSession_parentSession" class="text-mute mb-0"></p></div></div>`
    edit_session_form.dom.find(".card-body").append(parentSession_tmpl);
    
    edit_session_form.pk_in_url = false;
    edit_session_form.save_data = (data) =>{ eidt_session_date('2', data) };
    edit_session_form.on_after_init = function (data) {
    }
    edit_session_form.on_after_save = function (data) {
        $("#show_edit_session").modal("hide");
    }

    // var parentSessionNameVal = $('#editSession_parentSession').text();
    // if (parentSessionNameVal === '') {
    //     $('#parentSessionIcon').hide();
    // }
    $("#show_edit_session").find('input[name="edit_session_parentSession"]').on('input', function(e){
        var parent = e.target.value.split('-');
        if (parent && parent.length != 2) return ;
        var purl = `/PMIS/session/update?pid=${parent[0]}&tid=${parent[1]}`
        $.get(purl, function (result) {
            if (result.status) {
                $('#editSession_parentSession').text(`${e.target.value} ${result.data.sdesp}`);
                $('#editSession_parentSession').attr('flag', '1');
            }
            else{
                $('#editSession_parentSession').text(gettext('no session'));
                $('#editSession_parentSession').attr('flag', '0')
            }
        })
    })
    $("#show_edit_session").find('input[name="edit_session_relationsession"]').on('input', function(e){
        var parent = e.target.value.split('-');
        if (parent && parent.length != 2) return ;
        var purl = `/PMIS/session/update?pid=${parent[0]}&tid=${parent[1]}`
        $.get(purl, function (result) {
            if (result.status) {
                $('#editSession_relationSession').text(`${e.target.value} ${result.data.sdesp}`);
                $('#editSession_relationSession').attr('flag', '1');
            }
            else{
                $('#editSession_relationSession').text(gettext('no session'));
                $('#editSession_relationSession').attr('flag', '0')
            }
        })
    })
    
});


function technicMenu(node) {
    return {
        createItem: {
            "label": gettext("Add Folder"),
            "action": function (obj, e) {
                // 获取节点
                var currentNode = obj.reference[0] //當前節點                
                if (currentNode.id.startsWith("M_"))
                    return;
                $("#edit_mindmap_type .modal-title").text(gettext("Add Folder"));
                $("#edit_mindmap_type").modal("show");

                var params = {}
                if (currentNode.id != "-1_anchor")
                    params['parentid'] = $('#techtree').jstree(true).get_node(currentNode.id).data.inc_id
                mindmap_type_form.set_pk(undefined);
                mindmap_type_form.init_data(params);
            },
            "_class": "class"
        },
        renameItem: {
            "label": gettext("Add Mindmap"),
            "action": function (obj) {
                // 获取节点
                var currentNode = obj.reference[0] //當前節點
                if (currentNode.id.startsWith("M_"))
                    return;
                if (currentNode.id == "-1_anchor")
                    return;
                $("#edit_mindmap .modal-title").text(gettext("Add Mindmap"));
                $("#edit_mindmap").modal("show");
                params = {}
                params['typeid'] = $('#techtree').jstree(true).get_node(currentNode.id).data.inc_id;
                params['parents'] = $('#techtree').jstree(true).get_node(currentNode.id).parents;

                for (key in params['parents']) {
                    if (params['parents'][key] == 1 || params['typeid'] == 1) {
                        params['map_type'] = "2";
                    } else if (params['parents'][key] == 2 || params['typeid'] == 2) {
                        params['map_type'] = "1";
                    } else if (params['parents'][key] == 38 || params['typeid'] == 38) {
                        params['map_type'] = "3";
                    }
                }
                delete params['parents'];
                mindmap_form.set_pk(undefined);
                mindmap_form.init_data(params);
            }
        },
        modifyItem: {
            "label": gettext("Modifly"),
            "action": function (obj) {
                var currentNode = obj.reference[0] //當前節點
                if (currentNode.id == "-1_anchor")
                    return;
                //如果是Mindmap
                if (currentNode.id.startsWith("M_")) {
                    $("#edit_mindmap .modal-title").text(gettext("Modifly Mindmap"));
                    $("#edit_mindmap").modal("show");
                    var pk = $('#techtree').jstree(true).get_node(currentNode.id).data.inc_id;
                    mindmap_form.set_pk(pk);
                    mindmap_form.init_data();
                } else {
                    $("#edit_mindmap_type .modal-title").text(gettext("Modifly Type"));
                    $("#edit_mindmap_type").modal("show");
                    var pk = $('#techtree').jstree(true).get_node(currentNode.id).data.inc_id;
                    mindmap_type_form.set_pk(pk);
                    mindmap_type_form.init_data();
                }
            }
        },
        deleteItem: {
            "label": gettext("Delete"),
            "action": function (obj, e, data) {
                var currentNode = obj.reference[0] //當前節點
                if (currentNode.id == "-1_anchor")
                    return;

                //如果是Mindmap
                var pk = $('#techtree').jstree(true).get_node(currentNode.id).data.inc_id;
                var url = "/PMIS/mindmap/type_del?pk=[[pk]]"
                if (currentNode.id.startsWith("M_")) {
                    url = "/PMIS/mindmap/del?pk=[[pk]]"
                };
                url = url.render({ pk: pk })
                var all_childid = $('#techtree').jstree("get_node", currentNode).children_d;
                var json_data = {};
                if (all_childid.length > 0) {
                    json_data['all_childid[]'] = all_childid;
                }
                var flag = confirm("點擊確定後將會刪除此選項及其子選項!");
                if (flag) {
                    $.ajax({
                        type: "POST",
                        url: url,
                        traditional: true,
                        dataType: "json",
                        data: json_data,
                        beforeSend: function (request) {
                            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                        },
                        success: function (result) {
                            if (result.status) {
                                $('#techtree').jstree(true).refresh();
                            } else {
                                alert("刪除失敗");
                            }
                        }
                    });
                }
            }
        },
        geturlItem: {
            "label": gettext("Get url"),
            "action": function (obj) {
                var currentNode = obj.reference[0] //當前節點
                if (currentNode.id == "-1_anchor")
                    return;
                //如果是Mindmap
                if (currentNode.id.startsWith("M_")) {
                    var id = currentNode.id.match(/\d+(.\d+)?/g)[0];
                    var origin = window.location.origin
                    var pathname = window.location.pathname
                    var menu_type = getParamFromUrl("type");
                    if (menu_type != "" && menu_type != null)
                        menu_type = "type={0}&".format(menu_type);
                    else
                        menu_type = "";
                    var url = origin + pathname + "?{0}pk={1}".format(menu_type, id);
                    function copyToClipboard(str) {
                        const el = document.createElement('textarea'); //创建input对象
                        el.value = str;
                        el.setAttribute('readonly', '');  //当前获得焦点的元素
                        el.style.position = 'absolute';
                        el.style.left = '-9999px';
                        document.body.appendChild(el); //添加元素
                        const selected = document.getSelection().rangeCount > 0 ? document.getSelection().getRangeAt(0) : false;
                        el.select();
                        document.execCommand('copy'); //执行复制
                        document.body.removeChild(el);//删除元素
                        if (selected) {
                            document.getSelection().removeAllRanges();
                            document.getSelection().addRange(selected);
                        }
                    };
                    copyToClipboard(url);
                    var selector = $("li[aria-selected='true']");
                    SWApp.popoverMsg(selector, "複製成功");
                } else {
                    return;
                }
            }
        },
        copyItem: {
            "label": gettext("Copy MindMap"),
            "action": function (obj) {
                var currentNode = obj.reference[0] //當前節點
                if (currentNode.id == "-1_anchor") return;
                if (!currentNode.id.startsWith("M_")) return alert('文件夾不能複製');
                $("#select_folder .modal-title").text(gettext("Please select a destination folder"));
                $("#select_folder").modal("show");
                var id = currentNode.id.match(/\d+(.\d+)?/g)[0];
                var folderNodes = [];
                $("#techtree").jstree("get_json", -1, { flat: true }).forEach(function (node) {
                    if (node.type === "default") { // 判断节点类型为文件夹
                        folderNodes.push({
                            value: node.id,
                            label: node.text
                        });
                    }
                });
                $("#select_folder .modal-body").empty()
                selectfolder_form = new SWForm("#select_folder .modal-body", gettext("Please select a destination folder"), "", "", true);
                selectfolder_form.dom.find(".page-inner").removeClass("page-inner");
                selectfolder_form.dom.find(".card-header").hide();
                selectfolder_form.dom.find(".btn-subtle-info").attr("data-dismiss", "modal");
                selectfolder_form.addComponent(new SWCombobox("target_id", gettext("Folder"),folderNodes));
                selectfolder_form.addComponent(new SWText("file_name", "text", gettext("Modified File Name")));
                selectfolder_form.create_url = `/PMIS/mindmap/copy_mindmap?id=${id}`;
                selectfolder_form.pk_in_url = false;
                selectfolder_form.on_after_save = function (data) {
                    $("#select_folder").modal("hide");
                    $('#techtree').jstree(true).refresh();
                }
            }
        }
    };
}


function jstreenodeclick(obj, e) {
    var attr_id = e.node.id.indexOf("M_");
    var map_name = e.node.original.map_type;
    if (map_name == undefined)
        map_name = 1;
    if (map_name !== null && map_name == 2) {
        if (SWApp.os.isMobile || SWApp.os.isTablet) {
            $("#phoneLeftPanel").empty();
            mindmap = new SWSolutionmap("#phoneLeftPanel");
            mindmap.tree_dom = $('#techtree').jstree(true);
            mindmap.on_after_save = mindmap_after_save
        }
        else {
            $("#leftPane").empty();
            mindmap = new SWSolutionmap("#leftPane");
            mindmap.tree_dom = $('#techtree').jstree(true);
            mindmap.on_after_save = mindmap_after_save

        }
    } else if (map_name !== null && map_name == 3) {
        if (SWApp.os.isMobile || SWApp.os.isTablet) {
            $("#phoneLeftPanel").empty();
            mindmap = new SWSessionmap("#phoneLeftPanel");
            mindmap.tree_dom = $('#techtree').jstree(true);
            mindmap.on_after_save = mindmap_after_save
            mindmap.add_session_event = add_session;
            mindmap.goto_project_event = goto_project_event;
            mindmap.add_task_event = add_task;
            mindmap.eidt_session_date_event = eidt_session_date;
            mindmap.update_session_event = update_session;
            mindmap.get_session_task = get_session_task;
            mindmap.add_exists_session_event = add_exists_session_event;
            mindmap.goto_development_event = goto_development_event;
            mindmap.gotoMilestoneActiviitesEvent = gotoMilestoneActiviitesEvent;
            mindmap.goto_project_event = goto_project_event;
            mindmap.show_session_tasks_event = show_session_tasks_event;
            mindmap.show_session_log_event = show_session_log_event;
            mindmap.get_week_active_session_event = get_week_active_session;
            mindmap.gotoGanttEvent = gotoGanttPage; 
        }
        else {
            $("#leftPane").empty();
            mindmap = new SWSessionmap("#leftPane");
            mindmap.tree_dom = $('#techtree').jstree(true);
            mindmap.on_after_save = mindmap_after_save
            mindmap.add_session_event = add_session;
            mindmap.goto_project_event = goto_project_event;
            mindmap.add_task_event = add_task;
            mindmap.eidt_session_date_event = eidt_session_date;
            mindmap.update_session_event = update_session;
            mindmap.get_session_task = get_session_task;
            mindmap.add_exists_session_event = add_exists_session_event;
            mindmap.goto_development_event = goto_development_event;
            mindmap.gotoMilestoneActiviitesEvent = gotoMilestoneActiviitesEvent;
            mindmap.show_session_tasks_event = show_session_tasks_event;
            mindmap.show_session_log_event = show_session_log_event;
            mindmap.get_week_active_session_event = get_week_active_session;
            mindmap.gotoGanttEvent = gotoGanttPage; 
        }
    } else {
        if (SWApp.os.isMobile || SWApp.os.isTablet) {
            $("#phoneLeftPanel").empty();
            mindmap = new SWMindmap("#phoneLeftPanel");
            mindmap.tree_dom = $('#techtree').jstree(true);
            mindmap.on_after_save = mindmap_after_save
        }
        else {
            $("#leftPane").empty();
            mindmap = new SWMindmap("#leftPane");
            mindmap.tree_dom = $('#techtree').jstree(true);
            mindmap.on_after_save = mindmap_after_save
        }
    }
    var dom = $(".SWMindmap .save").length
    if (dom) {
        var f = $(".SWMindmap .save").attr("disabled");
        if (attr_id != -1) {
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
            if (f) {
                $(".SWMindmap .save").attr("disabled", true);
                $(".SWMindmap .clear").click();
            } else {
                var fl = confirm("當前mindmap已更改,請先保存？");
                if (fl) {
                    if (pre_selected_node != undefined && pre_selected_node != curr_selected_node) {
                        $('#techtree').jstree(true).deselect_node(e.node);
                        $('#techtree').jstree(true).select_node(pre_selected_node);
                    }
                }
                else {
                    $(".SWMindmap .save").attr("disabled", true);
                    $(".SWMindmap .clear").click();
                }
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
    mindmap.mindmap_inc_id = pk;
    var url = "/PMIS/mindmap/get_data/" + pk;
    $.get(url, function (result) {
        if (result.status) {
            mindmap.node_data = result.data;
            mindmap.load(result.data);
            if (SWApp.os.isMobile || SWApp.os.isTablet) {
                Looper.toggleSidebar();
            }
        } else {
            alert("獲取MindMap數據失敗");
        }
    });
}

function show_dynamic_mindmap() {
    if (window.dynamic_mindmap_json != "") {
        if (SWApp.os.isMobile || SWApp.os.isTablet) {
            $("#phoneLeftPanel").empty();
            mindmap = new SWSessionmap("#phoneLeftPanel");        
        }
        else {
            $("#leftPane").empty();    
            mindmap = new SWSessionmap("#leftPane");
        }
        mindmap.tree_dom = $('#techtree').jstree(true);
        mindmap.on_after_save = mindmap_after_save
        mindmap.add_session_event = add_session;
        mindmap.goto_project_event = goto_project_event;
        mindmap.add_task_event = add_task;
        mindmap.eidt_session_date_event = eidt_session_date;
        mindmap.update_session_event = update_session;
        mindmap.get_session_task = get_session_task;
        mindmap.add_exists_session_event = add_exists_session_event;
        mindmap.goto_development_event = goto_development_event;
        mindmap.gotoMilestoneActiviitesEvent = gotoMilestoneActiviitesEvent;
        mindmap.show_session_tasks_event = show_session_tasks_event;
        mindmap.get_week_active_session_event = get_week_active_session;    
        mindmap.gotoGanttEvent = gotoGanttPage;    
        var data = JSON.parse(window.dynamic_mindmap_json);
        mindmap.node_data = data
        mindmap.load(data);
        if (SWApp.os.isMobile || SWApp.os.isTablet) {
            Looper.toggleSidebar();
        }        
    }
}
function mindmap_after_save() {
    var currentNode = $('#techtree').jstree("get_selected");
    if (currentNode.length == 0 || !currentNode[0].startsWith("M_")) {
        alert("請選擇一個Mindmap");
        return false;
    }
}


function layout_mindmap(pk) {
    var url = "/PMIS/mindmap/get_data/" + pk;
    if (pk == null || pk == undefined || pk == "") return;
    $.get(url, function (result) {
        if (result.status) {
            mindmap.node_data = result.data;
            mindmap.load(result.data);
            if (SWApp.os.isMobile || SWApp.os.isTablet) {
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
function goto_development_event(recordid, sessionid) {
    setTimeout(() => {
        window.open(`/devplat/sessions?recordid=${recordid}&menu_id=mi_${sessionid}#Requirements`, "_blank");
    });
}
function gotoMilestoneActiviitesEvent(user, recordid, sessionid) {
    window.open(`/looper/user/top5_projects?contact=${user}&recordid=${recordid}&sessions=${sessionid}`, "_blank");
}

function gotoGanttPage(recordid, sessionid) {
    if (sessionid !== '')
        window.open(`/project/project_milestone?recordid=${recordid}&sessionid=${sessionid}`, "_blank");
    else
        window.open(`/project/project_milestone?recordid=${recordid}`, "_blank");
}
function show_session_tasks_event(recordid, sessionid) {
    function showOriginalSessionTask() {
        setTimeout(() => {
            window.open(`/devplat/sessions?recordid=${recordid}&menu_id=mi_${sessionid}#Session_Tasks`, "_blank");   
        });                
    }
    $.get("/project/session/get_relation_info", {sessionid:sessionid}).then((result)=>{
        if (result.status) {
            var relation_recordid = result.data.recordid;
            var relationsessionid = result.data.relationsessionid;
            if (relation_recordid != null && relationsessionid != null) {            
                setTimeout(() => {
                    window.open(`/devplat/sessions?recordid=${relation_recordid}&menu_id=mi_${relationsessionid}#Session_Tasks`, "_blank");   
                });                
            }else 
                showOriginalSessionTask();
        }else 
            showOriginalSessionTask();
    }).catch((error)=>{
        showOriginalSessionTask();
    });            
}
function show_session_log_event(recordid, sessionid) {
    function showOriginalSessionLog() {
        setTimeout(() => {
            window.open(`/devplat/sessions?recordid=${recordid}&menu_id=mi_${sessionid}#Session_Log`, "_blank");   
        });                
    }
    $.get("/project/session/get_relation_info", {sessionid:sessionid}).then((result)=>{
        if (result.status) {
            var relation_recordid = result.data.recordid;
            var relationsessionid = result.data.relationsessionid;
            if (relation_recordid != null && relationsessionid != null) {            
                setTimeout(() => {
                    window.open(`/devplat/sessions?recordid=${relation_recordid}&menu_id=mi_${relationsessionid}#Session_Log`, "_blank");   
                });                
            }else 
                showOriginalSessionLog();
        }else 
            showOriginalSessionLog();
    }).catch((error)=>{
        showOriginalSessionLog();
    });            
}
function get_week_active_session(contact) {
    var url = '/PMIS/mindmap/active_session'
    return new Promise((resolve, reject) => {
        $.get(url, { username: contact }, function (result) {
            if (result.status) {
                resolve(result.data);
            }
        });
    });
}
function add_task(sessionid, contact) {
    var params = { sessionid: sessionid }
    if (contact != undefined)
        params['contact'] = contact;
    init_task(undefined, params);
    var id = "#add-task"
    if (SWApp.os.isAndroid || SWApp.os.isPhone || SWApp.os.isTablet)
        id = "#add-task-module"
    return new Promise((resolve, reject) => {
        var interval = setInterval(function () {
            var isShown = $(id).hasClass('in') || $(id).hasClass('show');
            if (!isShown) {
                resolve(true)
                clearInterval(interval);
            }
        }, 100);
    });
}

function update_session(recordid, session) {
    var url = "/PMIS/session/update?type=1&recordid=" + recordid
    $.ajax({
        type: "POST",
        url: url,
        data: session,
        datatype: "json",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function (result) {
            if (!result.status)
                alert("更新Session內容失敗");
        }
    });
}

function get_session_task(pid, tid, contact, top) {
    var url = "/PMIS/session/search_task"
    var params = { pid: pid, tid: tid, contact: contact, count: top, progress_ncf:true }
    return new Promise((resolve, reject) => {
        $.get(url, params, function (result) {
            if (result.status) {
                resolve(result.data);
            } else {
                reject(null);
            }
        })
    })
}

function add_exists_session_event(recordid) {
    if (SWApp.os.isMobile || SWApp.os.isTablet) {
        window.select_session.height($(window).height() - 236 - 10);
        window.select_session.width($(window).width() - 10);
    } else {
        window.select_session.height(600);
        window.select_session.width(800);
    }
    window.select_session.datasource = '/PMIS/session/session_list_all';
    var filter = { "condition": "OR", "rules": [], "not": false };
    filter.rules.push({ "id": "recordid", "field": "recordid", "type": "string", "input": "string", "operator": "equal", "value": recordid });
    return new Promise((resolve, reject) => {
        //window.select_session.custom_params = { category: 1, recordid: recordid }
        window.select_session.custom_params = { recordid: recordid }
        window.select_session.show();
        window.select_session.on_selected_event = function (data) {
            resolve(data);
        }
    })
}

function goto_project_event(recordid) {
    var url = "/devplat/project/overview?recordids={0}".format(recordid);
    setTimeout(() => {
        window.open(url, "project")
    });
}

function add_session(recordid, contact, sessionid) {
    var url = "/PMIS/session/create?type=1&recordid=" + recordid
    return new Promise((resolve, reject) => {
        $.get(url, function (result) {
            if (result.status) {
                var now = new Date();
                var quarter = Math.floor((now.getMonth() / 3));
                var firstDate = new Date(now.getFullYear(), quarter * 3, 1);
                var endDate = new Date(firstDate.getFullYear(), firstDate.getMonth() + 3, 0);
                var data = {
                    pid: result.data.pid, tid: result.data.tid, progress: "I",
                    planbdate: firstDate.toString('yyyy-MM-dd'), planedate: endDate.toString('yyyy-MM-dd'),
                    //sdesp: "session add in mindmap"
                }
                if (sessionid != undefined)
                    data['parent'] = sessionid;
                if (contact != undefined)
                    data['contact'] = contact;
                $.ajax({
                    type: "POST",
                    url: url,
                    data: data,
                    datatype: "json",
                    beforeSend: function (request) {
                        request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    },
                    success: function (result) {
                        if (result.status)
                            resolve(result.data.instance);
                        else
                            reject(null);
                    }
                });
            }
        })
    });
}

function eidt_session_date(type, datas){ // type=1是獲取獲取, type=2是將數據保存
    var planBeginDate = $('#show_edit_session').find('input[name="edit_session_planbdate"]');
    var planEndDate = $('#show_edit_session').find('input[name="edit_session_planedate"]');
    var contact = $('#show_edit_session').find('select[name="edit_session_contact"]');
    var progress = $('#show_edit_session').find('select[name="edit_session_progress"]');
    var parentSession = $('#show_edit_session').find('input[name="edit_session_parentSession"]');
    var relationSession = $('#show_edit_session').find('input[name="edit_session_relationsession"]');
    var relationStatus = $('#show_edit_session').find('select[name="edit_session_relationstatus"]');
    var parentDesc = $('#editSession_parentSession');
    var relatonDesc = $('#editSession_relationSession');
    if (type=='1'){
        var pid = datas[0];
        var tid = datas[1];
        var url = `/PMIS/session/update?pid=${pid}&tid=${tid}`
        $.get(url, function (result) {
            if (result.status) {
                var data = result.data;
                planBeginDate.val(data.planbdate);
                planEndDate.val(data.planedate);
                relationSession.val(data.relationsessionid);
                contact.val(data.contact).selectpicker('refresh');
                progress.val(data.progress).selectpicker('refresh');
                relationStatus.val(data.relationstatus).selectpicker('refresh');
                parentSession.val(data.parent);
                $("#edit_session_sessionID").text(`${pid}-${tid}  ${data.sdesp}`);
                $("#edit_session_sessionID").attr('pid', pid);
                $("#edit_session_sessionID").attr('tid', tid);
                if (data.parent){
                    var parent = data.parent.split('-');
                    var purl = `/PMIS/session/update?pid=${parent[0]}&tid=${parent[1]}`
                    $.get(purl, function (result) {
                        if (result.status) {
                            parentDesc.text(`${data.parent} ${result.data.sdesp}`)
                        }
                    })
                }
                if(data.relationsessionid) {
                    var relation = data.relationsessionid.split('-');
                    var purl = `/PMIS/session/update?pid=${relation[0]}&tid=${relation[1]}`
                    $.get(purl, function (result) {
                        if (result.status) {
                            relatonDesc.text(`${data.relationsessionid} ${result.data.sdesp}`)
                        }
                    })
                }
                $("#show_edit_session").modal("show");
            }
        })
    }
    if (type=='2') {
        var pid = $("#edit_session_sessionID").attr('pid');
        var tid = $("#edit_session_sessionID").attr('tid');
        var url = `/PMIS/session/update`;    
        var data = {
            pid: pid, tid: tid,
            planbdate: planBeginDate.val(), planedate: planEndDate.val(),
            contact: contact.val(), progress: progress.val(), parent: parentSession.val(),
            relationsessionid:relationSession.val(),
            relationstatus:relationStatus.val()
        }
        if ($('#editSession_parentSession').attr('flag') == '0') return alert(gettext('enter error parents Session'))
        $.ajax({
            type: "POST",
            url: url,
            data: data,
            datatype: "json",
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            success: function (result) {
                if (result.status)
                    alert(gettext('Success'))
                else
                    alert(gettext('Fail'))
                $("#show_edit_session").modal("hide");
            }
        });
    }
   
}
