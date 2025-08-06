   
    var Editname = ''
    var selected_node = {};
    var form1 = null
    $(function () {

        

        var scoredata = [{value_field:'0', label_field:'0'},{value_field:'1', label_field:'1'},{value_field:'2', label_field:'2'},
        {value_field:'3', label_field:'3'},{value_field:'4', label_field:'4'},{value_field:'5', label_field:'5'},{value_field:'6', label_field:'6'},
        {value_field:'7', label_field:'7'},{value_field:'8', label_field:'8'},{value_field:'9', label_field:'9'},{value_field:'10', label_field:'10'}];
        var score = new SWCombobox("mb027", "",scoredata,'0','value_field','label_field');
        $(".score #score").append(score.dom);
        $(".score #score").children().css({'height': '20px','margin': '0px','display': 'flex'})
        $(".score #score").children().children().find('button').css({'height': '150%'})

        form1 = new SWBaseForm("#stepper_from_div");
        form1.create_url = "/PMIS/TechnicalCreate";
        form1.init_data({});
        
        form1.on_init_format = function(data) {
            data.mb005 = get_username()//聯繫人
            data.mb015c = data.mb001
            data.mb001 = ''
            if(data.mb027==null){
                data.mb027='0'
            }
            $('input[name="mb015c"]').attr('readonly',true)
            $('input[name="mb015c"]').on('click',()=>{
                selected_node = {};
                $('#category_tree_q').val('');
                $('#category_tree_area').val('');
                $('#category_tree_subarea').val('');
                refresh_tree();
                $('#quick_category_tree').modal('show');
            })
            window.setTimeout(function () {
                getTechnicId()
            }, 100);
        }


        $("#stepper_from_div form").on("click", ".save", function(e){
            if($('#myModal').children().length>0){
                Enterclick()
            }
        });
        
    
        //確定選擇的樹狀圖節點
        $('#quick_category_Confirm').on("click", ()=>{
            var treeselected = $("#category_tree").jstree().get_selected()
            if(treeselected.length==0 || selected_node['inc_id']==undefined){
                var treedata =  $('#category_tree').jstree().get_json()
                var category = $('#category_tree_q').val()
                
                var hasrecord = false
                for(var item of treedata){
                    if(item['text'].replaceAll(' ','').toUpperCase()===category.replaceAll(' ','').toUpperCase()){
                        selected_node=item['data']
                        hasrecord = true
                        break
                    }
                }
                if(!hasrecord){
                    var msg = gettext('Please select category!')
                    alert(msg)   
                    return
                } 
            }
            $('input[name="mb015"]').val('');
            $('input[name="mb015c"]').val('');
            $('input[name="mb016"]').val('');
            $('input[name="mb026"]').val('');
            $('input[name="mb023"]').val('');
    
            $('input[name="mb015"]').val(selected_node['ma007'].replaceAll(' ','')); 
            $('input[name="mb015c"]').val(selected_node['ma003b']);
            if (selected_node['ma002'].replaceAll(' ','')!='' && selected_node['ma002'].replaceAll(' ','')==selected_node['ma007'].replaceAll(' ','')){
                $('input[name="mb016"]').val(selected_node['ma003']);
            }
            if(selected_node['ma002'].replaceAll(' ','')!='' && selected_node['ma002'].replaceAll(' ','')!=selected_node['ma007'].replaceAll(' ','')){
                $('input[name="mb016"]').val(selected_node['ma003c']);
                $('input[name="mb026"]').val(selected_node['ma003']);
            }
            getTechnicId()
            $('#quick_category_tree').modal('hide')    
            
        });
        
        // var test_search = new SWSelectquery("#Cataloguemodelbtn"); //設置Search按鈕為觸發標籤
        // test_search.table.columns = [
        //     // { field: "ma001", label: "分類編號" },
        //     // { field: "ma003", label: "分類描述" },
        //     // { field: "ma003c", label: "父分類描述" },
        //     // { field: "ma003b", label: "目錄" }
        //     { field: "ma001", label: gettext("catagoryno") },
        //     { field: "ma003", label: gettext("catagory_describe") },
        //     { field: "ma003c", label: gettext("parent_catagory_describe") },
        //     { field: "ma003b", label: gettext("general_catagory") },
        //     { field: "ma007", label: gettext("general_catagory_no"),visible:false },
        //     { field: "inc_id", label: gettext("inc_id"),visible:false},
        // ];

        // if (SWApp.os.isMobile) {
        //     test_search.height($(window).height() - 236 - 10);
        //     test_search.width($(window).width() - 10);      
        // }
        // else {
        //     test_search.height(500);
        //     test_search.width(1100);
        // }
        // test_search.datasource = '/PMIS/CatalogueDatatable';
    
        // test_search.on_selected_event = function (data) {
        //     $('input[name="mb015c"]').val(data['ma003b']);
        //     $('input[name="mb001"]').val(data['ma001']);
        //     $('input[name="mb003"]').val(data['ma001']);
        //     getTechnicId();
        //     form1.redirect_url = "/PMIS/opportunity/Technical_Material?param="+$('input[name="mb023"]').val();
        // }

        // $('input[name="mb015c"]').on('click',()=>{
        //      $('#Cataloguemodelbtn').click();
        // })
    
        
        $('input[name="mb016"]').on('change',()=>{
            getTechnicId();
            form1.redirect_url = "/PMIS/opportunity/Technical_Material?param="+$('#stepper_from_div input[name="mb023"]').val();
        })
        
        $('input[name="mb005"]').on('change',()=>{
            $('input[name="creator"]').val($('input[name="mb005"]').val())
        })
        
        //實現思路增加按鈕
        $('#stepsAddbtn').on('click',function(){
            addhtml('Stepstab','typefirst','Stepshidden')
        })
        //實際案例增加按鈕
        $('#exampleAddbtn').on('click',function(){
            addhtml('Exampletab','typesecond','Examplehidden')
        })
        //注意事項增加按鈕
        $('#precautionAddbtn').on('click',function(){
            addhtml('Precautiontab','typethird','Precautionhidden')
        })
        
        
        

        var edtMA002C = new SWText("parentdsc","text", gettext('Parent Category Name'))
        $("#quick_category #edtMA002C").append(edtMA002C.dom);
        
        var edtMA002 = new SWText("ma002","text", gettext('Parent Category ID'))
        $("#quick_category #edtMA002").append(edtMA002.dom);
        
        var edtMA003 = new SWTextarea("ma003", gettext('Category Name'),4)
        $("#quick_category #edtMA003").append(edtMA003.dom);
        
        var edtMA005 = new SWText("ma005","hidden", gettext('Sequence'))
        $("#edtMA005").append(edtMA005.dom);
        $('#quick_category_form input[name="ma001"]').attr('readonly',true)
        $('#quick_category_form input[name="ma002"]').attr('readonly',true)
        $('#quick_category_form input[name="parentdsc"]').attr('readonly',true)



        //分類表單
        form_Category = new SWBaseForm("#quick_category_form_div");
        form_Category.create_url = "/PMIS/TecmaCreateView";
        form_Category.update_url = "/PMIS/TecmaUpdateView?pk=[[pk]]";
        form_Category.pk_in_url = false;
        form_Category.on_init_format = function(data) {
            if(data.ma002==null || data.ma002.replaceAll(' ','')=='')
                data.ma002 = 'placeholder'
            if (data.inc_id==null){
                var treeselected = $("#category_tree").jstree().get_selected()
                if(treeselected.length==0 || selected_node['inc_id']==undefined){
                    return
                }
                data.parentdsc = selected_node['ma003']
                data.ma002 = selected_node['ma001']
                data.ma007 = selected_node['ma007']
            }else{
                data.parentdsc = selected_node['ma003c']
            }
        }
        form_Category.on_after_save = function(data) {
            refresh_tree()
            $('#quick_category').modal('hide')    
        }


        
        $("#addRoot").on('click',function(){
            append_Category(true)
        })


        $.ajax({
            type: "GET",
            url: "/PMIS/technical/categorytree",
            dataType: "json",
            async: false,
            success: function (result) {
                var arrays = result.data;
                var jsonarray = buildTree(arrays, "ma002", "ma001",'ma003', '');
                init_tree(jsonarray)
            }
        })


        $('#category_tree_q').on('focus',function () {
            tree_search_old['category']=$('#category_tree_q').val()
        }); 
        $('#category_tree_area').on('focus',function () {
            tree_search_old['area']=$('#category_tree_area').val()
        }); 
        $('#category_tree_subarea').on('focus',function () {
            tree_search_old['subarea']=$('#category_tree_subarea').val()
        }); 
        
        $('#category_tree_q').on('blur',function () {
            if(tree_search_old['category']!=$('#category_tree_q').val())
                refresh_tree()
        }); 
        $('#category_tree_area').on('blur',function () {
            if(tree_search_old['area']!=$('#category_tree_area').val())
                refresh_tree()
        }); 
        $('#category_tree_subarea').on('blur',function () {
            if(tree_search_old['subarea']!=$('#category_tree_subarea').val())
                refresh_tree()
        }); 
        
        $('#category_tree_q').on("keydown",function (event) {
            if (event.key === "Enter"){
                refresh_tree()
                 tree_search_old['category']=$('#category_tree_q').val()
            }
        }); 
        $('#category_tree_area').on("keydown",function (event) {
            if (event.key === "Enter"){
                refresh_tree()
                 tree_search_old['area']=$('#category_tree_area').val()
            }
        }); 
        $('#category_tree_subarea').on("keydown",function (event) {
            if (event.key === "Enter") {
                refresh_tree()
                 tree_search_old['subarea']=$('#category_tree_subarea').val()
            }
        }); 


    });

    //格式化int並補充字符
    function formatZero(num, len) {
        if(String(num).length > len) return num;
        return (Array(len).join(0) + num).slice(-len);
    }

    //打開modal
    function openmodal(strname,parentId){
        $("#myModal textarea[name='modaltextarea']").val($("#"+parentId+" textarea[name='"+strname+".mc005']").val());
        // $("#myModal input[name='modalimginput']").val($("#"+parentId+" input[name='"+strname+".imginput']").val())
        $("img[name='modalimg']").attr('src', '');
        if($("img[name='"+strname+".img']").attr('src')!=undefined){
            $("img[name='modalimg']").attr('src', $("img[name='"+strname+".img']").attr('src'));
        }
        Editname = strname
    }

    //雙擊事件
    function dbOpen(e){
        if($('#myModal').children().length>0){Enterclick()}
        var strhtml ='<div id="myModal"><div class="modal-body px-0">'+
                        '<textarea name="modaltextarea" cols="30" rows="10" class="col-12 formtextaret"></textarea>'+
                        '<span class="my-2 btn btn-outline-primary fileinput-button bg-primary" style="color:white;">'+
                        '<input class="getFile" name="modalimginput" type="file" onchange="imgChange(this)"  accept="image/jpg">'+gettext('Upload Photo')+'</span>'+
                        '<img name="modalimg" class="mw-100"></div><div class="modal-footer px-0">'+
                    '<button type="button" class="btn btn-primary" onclick="Deletedataclick()" id="Deletedatabtn">'+gettext('Delete this data')+'</button>'+
                    '<button type="button" class="btn btn-primary" onclick="Deleteimgclick()" id="Deleteimgbtn">'+gettext('Delete Photo')+'</button>'+
                    '<button type="button" class="btn btn-primary" onclick="Enterclick()" id="Enterbtn">'+gettext('Confirm')+'</button>'+
                    '<button type="button" class="btn btn-light technicmodelhidden" onclick="modalhidden()" id="modalhiddenbtn">'+gettext('Cancel')+'</button>'+
                    '</div></div>'
        var strname = e.id
        var parentId = e.parentElement.previousElementSibling.id
        $('div[name="'+strname+'"]').children().addClass('ishidden')
        $('div[name="'+strname+'"]').append(strhtml)
        openmodal(strname,parentId)
    }
    //增加記錄條數HTML文本
    function addhtml(divId,typeindex,hiddivid){
        if($('#myModal').children().length>0){Enterclick()}
        var strname = $('#'+divId+' .toUpdate').length+1
        strname = formatZero(strname,4)
        var strhtml = '<div id="'+typeindex+'['+strname+']" name="'+typeindex+'['+strname+']" ondblclick="dbOpen(this)" class="toUpdate">'+
        '<li><pre name="'+typeindex+'['+strname+'].pre"></pre></div>'
        $("#"+divId).append(strhtml);

        var strhtml2 ='<textarea name="'+typeindex+'['+strname+'].mc005" cols="30" rows="10" class="col-12 formtextaret"></textarea>'+
        '<input name="'+typeindex+'['+strname+'].imginput" type="text">'+
        '<input type="checkbox" class="" name="'+typeindex+'['+strname+'].deletedata" value="">'+
        '<input type="checkbox" class="" name="'+typeindex+'['+strname+'].deleteimg" value="">'
        $("#"+hiddivid).append(strhtml2);
        $('div[name="'+typeindex+'['+strname+']"').dblclick()
    }

    //模態框確認按鈕
    function Enterclick(){
        $("textarea[name='"+Editname+".mc005']").val($("#myModal textarea[name='modaltextarea']").val());
        $("pre[name='"+Editname+".pre']").text($("#myModal textarea[name='modaltextarea']").val());
        if($("img[name='"+Editname+".img']").attr('src')!=undefined){
            $("img[name='"+Editname+".img']").attr('src',$("img[name='modalimg']").attr('src'));
            $("input[name='"+Editname+".imginput']").val($("img[name='modalimg']").attr('src').substring($("img[name='modalimg']").attr('src').indexOf(',')+1))
        }else{
            if(($("img[name='modalimg']").attr('src')!='')){
                var strhtml ='<li><img src=""  alt="" name="'+Editname+'.img" class="mw-100"></li>'
                $("div[name='"+Editname+"']").append(strhtml)
                $("img[name='"+Editname+".img']").attr('src',$("img[name='modalimg']").attr('src'));
                $("input[name='"+Editname+".imginput']").val($("img[name='modalimg']").attr('src').substring($("img[name='modalimg']").attr('src').indexOf(',')+1))
                //$('input[name="file"]').val();
            }  
        }
        modalhidden()
    }

     //模態框刪除本條數據按鈕
     function Deletedataclick(){
        var fl = confirm(gettext('Are you sure you want to delete this data?'));
        if (!fl) {return}
        $("input[name='"+Editname+".deletedata']").attr('checked','true')
        $("div[name='"+Editname+"']").children().remove()
        modalhidden()
    }

     //模態框刪除圖片按鈕
     function Deleteimgclick(){
        if ($("img[name='"+Editname+".img']").attr('src')!=undefined){
            $("input[name='"+Editname+".deleteimg']").attr('checked','true')
            $("img[name='"+Editname+".img']").parent().remove();
            $("img[name='modalimg']").attr('src', '');
            $("input[name='"+Editname+".imginput']").val('')
        }
    }

     //模態框取消按鈕
     function modalhidden(){
        $('div[name="'+Editname+'"]').children().removeClass('ishidden');
        $('#myModal').remove();
        Editname = ''
    }

    //圖片改變事件
    function imgChange(e){
        const file = e.files[0];
        const fr = new FileReader();
        var strname = 'img[name="'+e.name.slice(0,-5)+'"]'
        fr.onload = function (e) {
            $(strname).attr('src', e.target.result);
        };    
        fr.readAsDataURL(file);
    }

    function getTechnicId(){
        if(($('#stepper_from_div input[name="mb016"]').val().trim() != '') && ($('#stepper_from_div input[name="mb015"]').val().trim() !='') ){
            var TechnicId = $('#stepper_from_div input[name="mb015c"]').val().slice(0,3).trim()+'-'+$('#stepper_from_div input[name="mb016"]').val().trim().slice(0,3)+'-'
            $.ajax({
                type: "GET",
                url: "/PMIS/opportunity/getTechnicid",
                dataType: "json",
                data: {'TechnicId':TechnicId},
                async: false,
                success: function (result) {
                    if (result.state) {
                        jsondata = result.data
                        if(jsondata.length>0){
                            $('#stepper_from_div input[name="mb023"]').val(jsondata[0]['theTechnicid']);
                        }else{
                            $('#stepper_from_div input[name="mb023"]').val(jsondata[0]['theTechnicid']);
                        }
                        form1.redirect_url = "/PMIS/opportunity/Technical_Material?param="+$('#stepper_from_div input[name="mb023"]').val();
                    }
                }
            })
        }
    }



    function init_tree(jsonarray){
        // jsTree插件  
        $("#category_tree").jstree({
            "core": {
                "themes": {
                    "responsive": false,
                    "dots": false,
                },
                "max_depth": 2,
                "check_callback": true,
                'data': jsonarray,
            },
            "types": {
                "#": {
                  icon: "fa fa-folder" // 根节点图标
                },
                "default": {
                  icon: "fa fa-file" // 默认节点图标
                },
                "level1": {
                  icon: "fa fa-star" // 第一层级节点图标
                },
                "level2": {
                  icon: "fa fa-flag" // 第二层级节点图标
                },
            },
            "plugins": [
                "contextmenu",
                "types",
                "wholerow",'state',
                "unique","search",
            ],
            'search':{
                'show_only_matches':true,
            },
            'contextmenu': {
                'select_node': true,
                'items': categoryMenu
            },
            'state': {
              'opened': false, // 设置所有节点默认关闭
            },
        });
        
        $('#category_tree').jstree(true).refresh(); // 刷新树
        //樹狀圖節點點擊事件
        $('#category_tree').bind("activate_node.jstree", (obj,e)=>{
            // 获取当前节点
            selected_node = e.node.data
        });
    
    }
    
    

    //新增分類
    function append_Category(isRoot=false){
        if(isRoot){$('#quick_category_form #edtMA002C').parent().attr('hidden',true);}else{$('#quick_category_form #edtMA002C').parent().attr('hidden',false);}
        $('#quick_category .modal-title').html(gettext('Create Category'));
        form_Category.set_pk(undefined);
        form_Category.init_data();
        $('#quick_category').modal('show')
    }

    //修改分類
    function update_Category(){
        var treeselected = $("#category_tree").jstree().get_selected()
        if(treeselected.length==0 || selected_node['inc_id']==undefined){
            alert(gettext('Please select a category!'))    
            return
        }
        if(selected_node['ma002'].replaceAll(' ','')==''){$('#quick_category_form #edtMA002C').parent().attr('hidden',true);}else{$('#quick_category_form #edtMA002C').parent().attr('hidden',false);}
        $('#quick_category .modal-title').html(gettext('Update Category'));
        form_Category.set_pk(selected_node['inc_id']);
        form_Category.init_data();
        $('#quick_category').modal('show')
    }




    //樹狀圖右鍵菜單
    function categoryMenu(node) {
        var path = node.parents.concat(node.id).reverse();
        var level = path.length - 1;
        var items = {
            updateItem: {
                "label": gettext('Update node'),
                "action": function (obj) {
                    update_Category()
                }
            },
        };

        // 根据节点层级生成不同的菜单项
        if (level === 1) {
            items.add = {
                "label": gettext('Add Area'),
                "action": function (obj) {
                    append_Category()
                }
            }; 
        } else if (level === 2) {
            items.add = {
                "label": gettext('Add Sub Area'),
                "action": function (obj) {
                    append_Category()
                }
            }; 
        }
        return items;
    }       
        


    
    //刷新樹狀圖
    function refresh_tree() {
        var category = $('#category_tree_q').val()
        var area = $('#category_tree_area').val()
        var subarea = $('#category_tree_subarea').val()
        $.ajax({
            type: "GET",
            url: "/PMIS/technical/categorytree?category={0}&area={1}&subarea={2}".format(category,area,subarea),
            dataType: "json",
            async: false,
            success: function (result) {
                var arrays = result.data;
                var jsonarray = buildTree(arrays, "ma002", "ma001",'ma003', '');
                $('#category_tree').jstree(true).destroy();// 清除树节点
                
                // $('#select_category_tree').jstree(true).destroy();// 清除树节点
                init_tree(jsonarray)
            }
        })


    }



    function buildTree(data, parentKey, idKey,textkey, parentValue, level = 1) {
        const result = [];
        for (const item of data) {
            var type = '#'
            if(item[parentKey].replaceAll(' ','') != '' && item[parentKey].replaceAll(' ','')==item['ma007'].replaceAll(' ',''))
                type='level1'
            if(item[parentKey].replaceAll(' ','') != '' && item[parentKey].replaceAll(' ','')!=item['ma007'].replaceAll(' ',''))
                type='level2'
          if (item[parentKey].replaceAll(' ','') === parentValue) {
            const newNode = {
              'id': item[idKey],
              'text': item[textkey],
              'children': level==3?[]: buildTree(data, parentKey, idKey,textkey, item[idKey],level+1),
              'data':item,
              'type':type
            };
            result.push(newNode);
          }
        }
        return result;
    }
    
