var StepsAry = []
var technicTable_q = undefined
var technicTable_datatable_q = undefined
var search_skip_txt_arr = ['I','can','and','as','to','with','How'].map((a)=>a.toLowerCase());
var search_skip_txt_arr_cn = ["的","地"];
var form_Category = undefined
var catagory_search =undefined
var selected_node = {}
var tree_search_old = {'category':'','area':'','subarea':''}
var technic_data = {tecmb:{},steps:[],example:[],precaution:[]}
$(function () {
    var Editname = ''
    // var nav_links = $(".top-bar-item-right .header-nav .nav-link")
    // var nav = $(nav_links[3])
    // nav.attr("data-toggle", "modal");
    // nav.attr("data-target", "#quick-add-technic");enquiryInput
    var enquiry_cmpt = new SWTextarea("q_search", "", '5');
    $("#enquiryInput").prepend(enquiry_cmpt.dom);

    var technicid_cmpt = new SWText("mb023","text", gettext('Technical ID'))
    $("#technicid").append(technicid_cmpt.dom);
    $('#quick_techinc_form input[name="mb023"]').attr('readonly',true)

    var date_cmpt = new SWDate("mb006","date",gettext('Date'));
    $("#technicDate").prepend(date_cmpt.dom);

    var contact_cmpt = new SWCombobox("mb005", gettext('Contact'), window.CommonData.PartUserNames,get_username())
    $("#technicContact").append(contact_cmpt.dom);

    var reference_cmpt = new SWTextarea("mb017", gettext('Reference'), 4)
    $("#technicReference").append(reference_cmpt.dom);

    var topic_cmpt = new SWTextarea("mb004", gettext('Technical Topic'), 4)
    $("#technicTopic").append(topic_cmpt.dom);

    

    var theory = new SWTextarea("mb007", gettext('Concept/Theory'),4)
    $("#theory").append(theory.dom);
    
    var category = new SWText("mb015c","text", gettext('Category'))
    $("#category").append(category.dom);

    var area = new SWText("mb016","text", gettext('Area'))
    $("#area").append(area.dom);

    var subarea = new SWText("mb026","text", gettext('Sub Area'))
    $("#subarea").append(subarea.dom);

    var video = new SWText("mb018","text", gettext('Video'))
    $("#video").append(video.dom);



    var edtMA002C = new SWText("parentdsc","text", gettext('Parent Category Name'))
    $("#quick_category_mini #edtMA002C").append(edtMA002C.dom);
    
    var edtMA002 = new SWText("ma002","text", gettext('Parent Category ID'))
    $("#quick_category_mini #edtMA002").append(edtMA002.dom);
    
    var edtMA003 = new SWTextarea("ma003", gettext('Category Name'),4)
    $("#quick_category_mini #edtMA003").append(edtMA003.dom);
    
    var edtMA005 = new SWText("ma005","hidden", gettext('Sequence'))
    $("#edtMA005").append(edtMA005.dom);
    $('#quick_category_form input[name="ma001"]').attr('readonly',true)
    $('#quick_category_form input[name="ma002"]').attr('readonly',true)
    $('#quick_category_form input[name="parentdsc"]').attr('readonly',true)

    var form1 = new SWBaseForm("#quick_techinc_form_div");
    form1.create_url = "/PMIS/TechnicalCreate";
    form1.update_url = "/PMIS/TechnicalUpdate?pk=[[pk]]";
    form1.pk_in_url = false;
    form1.init_data({});
    form1.on_init_format = function(data) {
        StepsAry = [{'typefirst[0001].mc005':''}]
        $('#Stepstab_quick .imgcontainer').addClass('ishidden')
        $("#quick_techinc_form img[name='modalimg']").attr('src', '');
        data.mb006 = data.mb006==null?'':data.mb006.replace(/^(\d{4})(\d{2})(\d{2})$/, "$1-$2-$3")//創建日期
        data.mb005 = get_username()//聯繫人
        data.mb015c = data.mb001
        data.mb001 = ''
        $('#quick_techinc_form input[name="mb015c"]').attr('readonly',true)
        $('#quick_techinc_form input[name="mb015c"]').on('click',()=>{
            selected_node = {};
            $('#category_tree_q').val('');
            $('#category_tree_area').val('');
            $('#category_tree_subarea').val('');
            refresh_tree();
            $('#quick_category_tree').modal('show');
            // $('#Cataloguemodelbtn').click();
        })
    
        window.setTimeout(function () {
            getTechnicId()
        }, 100);
    }
    form1.on_save_format = function(data){
        $("#quick_techinc_form_div #quick_techinc_form_submit").attr('disabled', true);   
        window.setTimeout(function(){
            $("#quick_techinc_form_div #quick_techinc_form_submit").removeAttr('disabled');
        },4000)        
        //格式日期，去除符合-
        data.mb006 = data.mb006.replaceAll('-','')
        //將實現思路明細寫入要提交的字典中
        // for(var item of StepsAry){
        //     var keys = Object.keys(item);
        //     for(key of keys){
        //         data[key] = item[key]
        //     }
        // }
        if(($("#quick_techinc_form img[name='modalimg']").attr('src')!='') && ($("#quick_techinc_form img[name='modalimg']").attr('src')!=undefined)){
            data['typefirst[0001].imginput'] = $("#quick_techinc_form img[name='modalimg']").attr('src').substring($("#quick_techinc_form img[name='modalimg']").attr('src').indexOf(',')+1)
        }
        //格式化
        data = objectToFormData(data)
        // data.mb023 = $('input[name="mb023"]').val();
    }

    form1.on_after_save = function(data) {
        $("#quick_techinc_form_div #quick_techinc_form_submit").removeAttr('disabled');
    }


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
        $('#quick_category_mini').modal('hide')    
    }

    //點擊保存按鈕後先將未提交的數據提交
    $("#quick_techinc_form_submit").on("click", function(e){
        if($('#myModal').children().length>0){
            $('#myModal').find('#Enterbtn').click()
        }
    });

    // $('select[name="mb005"').val(get_username())


    //增加下一步按鈕點擊方法
    $('#addStep').on('click',function(){
        //先提交數據
        if($('#myModal').children().length>0){
            $('#myModal').find('#Enterbtn').click()
        }
        //$('#Stepstab').children().last()[0].id
        //獲取總共有多少條任務
        var indexno = formatZero($('#Stepstab').children().length+1,4)

        //獲取html並處發對應雙擊事件
        var data = {}
        data['typefirst['+indexno+'].mc005'] = ''
        var divhtml = gethtml(data,indexno,true)
        $('#Stepstab').append(divhtml);
        StepsAry.push(data)
        $('div[name="typefirst['+indexno+']"]').dblclick()
    })

    
    //格式化數據方法
    function objectToFormData(obj){
        let fd = new FormData();
        for (let o in obj) {
            if(obj[o]){
                fd.append(o, obj[o]);
            }          
        }
        return fd;
    }
    
    promiseGet("/PMIS/global/get_typelist?type_name=search_skip").then((result)=>{
        if(result.status && result.data.length > 0) {
            for(var row of result.data) {
                var nfield = row.value;
                if (nfield == "search_skip_txt")
                    self.search_skip_txt_arr = row.label.split(",").map((a)=>a.toLowerCase());
                else if (nfield == "search_skip_txt")
                    self.search_skip_txt_arr_cn = row.label.split(",").map((a)=>a.toLowerCase());
            }
        }
    })

    
    $("a[data-target='#quick-add-technic']").on("click", function () {
        form1.set_pk(undefined);
        form1.init_data();
        init_technical_table();
    });

    
    
    enquiry_cmpt.input_dom.on("input", function (e) {
        if (self.technicTable_datatable_q != undefined) {
            var search_val = self.get_real_search_value($(this).val())
            if (search_val)
                self.technicTable_datatable_q.search(search_val).draw();
        }
    });

    $('input[name="bmb006"]').on('change',function(e){
        if (technicTable_datatable_q != undefined) {
            var search_val = $('#techEnquiryCollapse textarea[name="q_search"]').val()
            search_val = self.get_real_search_value(search_val)
            self.technicTable_datatable_q.search(search_val).draw();
        }
    })
    
    $('#print_technic').on('click',function(){
        var selected_master = self.technicTable_datatable_q.rows(['.selected']).data()
        if(selected_master==undefined || selected_master.length==0){
            alert('請要打印的文檔')
            return
        }
        var strmb023 = selected_master[0]['mb023'];
        var inc_id = selected_master[0]['inc_id'];
        get_Technical(strmb023,inc_id)
    })

    $('input[name="emb006"]').on('change',function(e){
        if (technicTable_datatable_q != undefined) {
            var search_val = $('#techEnquiryCollapse textarea[name="q_search"]').val()
            search_val = self.get_real_search_value(search_val)
            self.technicTable_datatable_q.search(search_val).draw();
        }
    })

    $('.wrapper').on('shown.bs.modal', function (e) {
        $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
        $.fn.DataTable.ext.pager.numbers_length = 5; //更改分頁欄上顯示的頁碼數量
    });

    get_lang_code();

    //技術文檔表格行雙擊事件    
    $('#techEnquiryTable').on('dblclick', 'tbody tr', function () {
        var strmb023 = technicTable_datatable_q.row(this).data()['mb023'];
        var inc_id = technicTable_datatable_q.row(this).data()['inc_id'];
        if(strmb023!=undefined && strmb023!=null && strmb023!='')
            window.open('/PMIS/opportunity/Technical_Material?param=' + strmb023.trim())
        else
            window.open('/PMIS/opportunity/Technical_Material?inc_id=' + inc_id)
    })

    // $('#techEnquiryTable').on('click', 'tbody tr', function () {
    //     var strmb023 = technicTable_datatable_q.row(this).data()['mb023'];
    //     var inc_id = technicTable_datatable_q.row(this).data()['inc_id'];
    //     get_Technical(strmb023,inc_id)
    // })


    


    //確定選擇的樹狀圖節點
    $('#quick_category_tree_div').on("click", '#quick_category_Confirm', function(event){
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
        $('#quick_techinc_form input[name="mb015"]').val('');
        $('#quick_techinc_form input[name="mb015c"]').val('');
        $('#quick_techinc_form input[name="mb016"]').val('');
        $('#quick_techinc_form input[name="mb026"]').val('');
        $('#quick_techinc_form input[name="mb023"]').val('');

        $('#quick_techinc_form input[name="mb015"]').val(selected_node['ma007'].replaceAll(' ','')); 
        $('#quick_techinc_form input[name="mb015c"]').val(selected_node['ma003b']);
        if (selected_node['ma002'].replaceAll(' ','')!='' && selected_node['ma002'].replaceAll(' ','')==selected_node['ma007'].replaceAll(' ','')){
            $('#quick_techinc_form input[name="mb016"]').val(selected_node['ma003']);
        }
        if(selected_node['ma002'].replaceAll(' ','')!='' && selected_node['ma002'].replaceAll(' ','')!=selected_node['ma007'].replaceAll(' ','')){
            $('#quick_techinc_form input[name="mb016"]').val(selected_node['ma003c']);
            $('#quick_techinc_form input[name="mb026"]').val(selected_node['ma003']);
        }
        getTechnicId()
        $('#quick_category_tree').modal('hide')    
    });

    
    

    //Area改變重新獲取TechnicalID
    $('input[name="mb016"]').on('change',()=>{
        getTechnicId();
    })




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

/**
 * 遞迴生成 jsTree 所需的樹狀結構。
 * @param {Array} data - 資料陣列。
 * @param {string} parentKey - 表示父級的鍵名。
 * @param {string} idKey - 節點 ID 的鍵名。
 * @param {string} textKey - 節點顯示文字的鍵名。
 * @param {string} parentValue - 當前遞迴中應匹配的父值。
 * @param {number} level - 當前層級（預設從 1 開始）。
 * @returns {Array} - 組裝好的樹狀節點陣列。
 */
function buildTree(data, parentKey, idKey, textKey, parentValue = '', level = 1) {
    var trimmedParentValue = parentValue.replaceAll(' ', '');
    return data.reduce((result, item) => {
        var currentParent = item[parentKey]?.replaceAll(' ', '') || '';
        var currentId = item[idKey]?.replaceAll(' ', '') || '';
        var ma007 = item['ma007']?.replaceAll(' ', '') || '';

        // 判斷節點類型
        let type = '#';
        if (currentParent && currentParent === ma007) {
            type = 'level1';
        } else if (currentParent && currentParent !== ma007) {
            type = 'level2';
        }

        // 若父鍵與當前傳入的 parentValue 相符，則生成節點
        if (currentParent === trimmedParentValue) {
            result.push({
                id: currentId,
                text: item[textKey],
                children: level < 3 ? buildTree(data, parentKey, idKey, textKey, currentId, level + 1) : [],
                data: item,
                type: type
            });
        }
        return result;
    }, []);
}

/**
 * 初始化 jsTree 樹狀圖，並綁定節點點擊事件。
 * @param {Array} jsonarray - 用於初始化 jsTree 的樹狀資料。
 */
function init_tree(jsonarray) {
    $("#category_tree").jstree({
        "core": {
            "themes": {
                "responsive": false,
                "dots": false
            },
            "check_callback": true,
            "data": jsonarray
        },
        "types": {
            "#": { icon: "fa fa-folder" },    // 根節點圖標
            "level1": { icon: "fa fa-star" },   // 第一層級節點圖標
            "level2": { icon: "fa fa-flag" }    // 第二層級節點圖標
        },
        "plugins": [
            "contextmenu",
            "types",
            "wholerow",
            "state",
            "unique",
            "search"
        ],
        "search": {
            "show_only_matches": true
        },
        "contextmenu": {
            "select_node": true,
            "items": categoryMenu
        },
        "state": {
            "opened": false
        }
    });

    // 綁定節點激活事件
    $('#category_tree').on("activate_node.jstree", (event, data) => {
        selected_node = data.node.data;
    });
}




// }

// 定义自定义搜索函数
function customSearch(queryText, level) {

    var tree = $('#category_tree').jstree(true);
    var results = [];

    // 获取所有节点数据
    var allNodes = tree.get_json('#', { flat: true });

    // 遍历节点数据
    allNodes.forEach(function(node) {
        // 仅对指定层级进行查询
        if (node.type === level && node.text.includes(queryText)) {
            results.push(node.id);
        }
    });

    // 重新加载 jstree，显示搜索结果
    // tree.settings.core.data = allNodes;
    // tree.refresh();
    // tree.open_node(queryText);
    return results;
}




//雙擊事件
function dbOpen(e){
    //提交數據
    if($('#myModal').children().length>0){
        $('#myModal').find('#Enterbtn').click()
    }
    var strname = e.id
    var begin = strname.indexOf('[')+1
    var end = strname.indexOf(']')
    //輸入框html代碼
    var strhtml ='<div id="myModal"><div class="modal-body" style="padding: inherit;"><div class="publisher publisher-alt focus active">'+
        '<div class="publisher-input"><textarea id="technic_steps" name="modaltextarea" class="form-control h-auto" rows="5"></textarea>'+
        '<img name="modalimg" class="mw-100"></div><div class="publisher-actions flex-wrap">'+
        '<div class="publisher-tools mr-auto"><div class="btn btn-light btn-icon fileinput-button"><i class="far fa-image"></i>'+
        '<input type="file" id="attachment3" class="getFile" name="modalimginput" onchange="imgChange(this)"  accept="image/jpg" multiple=""></div></div>'+
        '<button type="button" class="btn btn-sm btn-subtle-danger" onclick="Deletedataclick('+strname.substring(begin,end)+')" id="Deletedatabtn">'+gettext('Delete Data')+'</button>'+
        '<button type="button" class="btn btn-sm btn-subtle-info ml-2" onclick="Deleteimgclick('+strname.substring(begin,end)+')" id="Deleteimgbtn">'+gettext('Delete Image')+'</button>'+
        '<button type="button" class="btn btn-sm btn-subtle-primary ml-2" onclick="Enterclick('+strname.substring(begin,end)+')" id="Enterbtn">'+gettext('Confirm')+'</button>'+
        '<button type="button" class="btn btn-sm btn-secondary ml-2" onclick="modalhidden('+strname.substring(begin,end)+')" id="modalhiddenbtn">'+gettext('Cancel')+'</button>'+
        '</div></div></div></div>' 
    //隱藏li列表
    $('div[name="'+strname+'"]').children().addClass('ishidden')
    //將輸入框顯示在對應容器下
    $('div[name="'+strname+'"]').append(strhtml)
    $('#myModal .publisher').addClass('focus active')
    //設置輸入框的值
    openmodal(strname)
}


//根據對應字典值設置輸入框內容
function openmodal(strname){
    var indexno = strname.substring(strname.indexOf('[')+1,strname.indexOf(']'))
    indexno = parseInt(indexno)-1
    if (StepsAry[indexno]==undefined)return
    $("#myModal textarea[name='modaltextarea']").val(StepsAry[indexno][strname+'.mc005']);
    $("#myModal input[name='modalimginput']").val(StepsAry[indexno][+strname+'.imginput'])
    $("img[name='modalimg']").attr('src', '');
    if(StepsAry[indexno][strname+'.imgsrc']!=''){
        $("img[name='modalimg']").attr('src', StepsAry[indexno][strname+'.imgsrc']);
    }
}

//模態框確認按鈕
function Enterclick(indexno){
    var typefirst = {}
    indexno = formatZero(indexno,4)
    Stepsindex = parseInt(indexno)-1
    typefirst['typefirst['+indexno+'].mc005'] = $("#myModal textarea[name='modaltextarea']").val()
    // typefirst['typefirst['+indexno+'].pre'] = $("#myModal textarea[name='modaltextarea']").val()
    // if($("img[name='typefirst["+indexno+"].img']").attr('src')!=undefined){
    //     typefirst['typefirst['+indexno+'].img'] = $("img[name='modalimg']").attr('src')
    // }else{
    typefirst['typefirst['+indexno+'].imginput'] =  ''
    typefirst['typefirst['+indexno+'].imgsrc']  =''
        if(($("img[name='modalimg']").attr('src')!='') && ($("img[name='modalimg']").attr('src')!=undefined)){
            typefirst['typefirst['+indexno+'].imginput'] = $("img[name='modalimg']").attr('src').substring($("img[name='modalimg']").attr('src').indexOf(',')+1)
            typefirst['typefirst['+indexno+'].imgsrc'] = $("img[name='modalimg']").attr('src')

            // var strhtml ='<li><img src=""  alt="" name="'+Editname+'.img" class="mw-100"></li>'
            // $("div[name='"+Editname+"']").append(strhtml)
            // $("img[name='"+Editname+".img']").attr('src',$("img[name='modalimg']").attr('src'));
            // $("input[name='"+Editname+".imginput']").val($("img[name='modalimg']").attr('src').substring($("img[name='modalimg']").attr('src').indexOf(',')+1))
            //$('input[name="file"]').val();
        }  
    // }

    var divhtml = gethtml(typefirst,indexno,StepsAry[Stepsindex]==undefined)
    if(StepsAry[Stepsindex]==undefined && parseInt(indexno)>$('#Stepstab').children().length){
        StepsAry.push(typefirst)
        $('#Stepstab').append(divhtml);
    }else{
        StepsAry[Stepsindex] = typefirst
        $('div[name="typefirst['+indexno+']"]').html(divhtml);
    }
    //移除模態框
    modalhidden(indexno)
}

//生成html
function gethtml(data,indexno,isPush){
    var prehtml = '<li><pre name="typefirst['+indexno+'].mc005">'+data['typefirst['+indexno+'].mc005']+'</pre></li>'
    var imghtml = '<li><img src="'+data['typefirst['+indexno+'].imgsrc']+'"  alt="" name="typefirst['+indexno+'].imginput" class="mw-100"></li>'
    var divhtml = '<div name="typefirst['+indexno+']" id="typefirst['+indexno+']" ondblclick="dbOpen(this)"  class="toUpdate mh-20">{0}{1}</div>'
    if(isPush){
        if(data['typefirst['+indexno+'].imginput']==undefined || data['typefirst['+indexno+'].imginput']=='')
            divhtml = divhtml.format(prehtml,'')
        else
            divhtml = divhtml.format(prehtml,imghtml)
    }else{
        if(data['typefirst['+indexno+'].imginput']==undefined || data['typefirst['+indexno+'].imginput']=='')
            divhtml = '{0}{1}'.format(prehtml,'')
        else
            divhtml = '{0}{1}'.format(prehtml,imghtml)
    }
    return divhtml
}


//模態框取消按鈕
function modalhidden(indexno){
    indexno = formatZero(indexno,4)
    $('div[name="typefirst['+indexno+']"]').children().removeClass('ishidden');
    $('#myModal').remove();
}



//模態框刪除本條數據按鈕
function Deletedataclick(indexno){
    var fl = confirm("確定要刪除本條數據？");
    if (!fl) {return}
    indexno = formatZero(indexno,4)
    Stepsindex = parseInt(indexno)-1
    StepsAry[Stepsindex]['typefirst['+indexno+'].deletedata'] = 'on'
    $("div[name='typefirst["+indexno+"]").children().remove()
    modalhidden()
}

//模態框刪除圖片按鈕
function Deleteimgclick(indexno){
    indexno = formatZero(indexno,4)
    Stepsindex = parseInt(indexno)-1
    //清空圖片明細並設置刪除圖片
    if(StepsAry.length >= Stepsindex+1){
        StepsAry[Stepsindex]['typefirst['+indexno+'].imginput'] = ''
        StepsAry[Stepsindex]['typefirst['+indexno+'].imgsrc'] = ''
        StepsAry[Stepsindex]['typefirst['+indexno+'].deleteimg'] = 'on'
    }
    //去除img標籤圖片內容
    $('.getFile').val('')
    $("img[name='typefirst["+indexno+"].imginput']").parent().remove();
    $("img[name='modalimg']").attr('src', '');
    $('#Stepstab_quick .imgcontainer').addClass('ishidden')
}


//圖片改變事件
function imgChange(e){
    const file = e.files[0];
    if(file.size>2621440){
        alert('圖片不可大於2.5M！');
        return
    }
    if(file.size=0)
        return
    const fr = new FileReader();
    var strname = '#quick_techinc_form img[name="'+e.name.slice(0,-5)+'"]'
    fr.onload = function (e) {
        $(strname).attr('src', e.target.result);
    };    
    fr.readAsDataURL(file);
    $('#Stepstab_quick .imgcontainer').removeClass('ishidden')
}


//格式化int並補充字符
function formatZero(num, len) {
    if(String(num).length > len) return num;
    return (Array(len).join(0) + num).slice(-len);
}

//初始化技術文檔表格
function init_technical_table () {
    $('#techEnquiryTable').children().remove()
    var technicTable = new SWDataTable("#techEnquiryTable", "Technicaltable"); //創建SWDataTable對象
    technicTable.pageLength = 10; //設置每頁顯示的數量為20
    technicTable.paging = true; //設置分頁顯示
    technicTable.searching = false; //設置不顯示查詢框

    technicTable.orderBy = [['mb023', 'desc']]; //設置按taskno 升序排序
    //設置顯示字段
    technicTable.columns = [
        { field: "mb015c", label: gettext('Category')},
        { field: "mb023", label: gettext('Technic Id'), visible:false},
        { field: "mb004", label: gettext('Technical Topic') },
        { field: "mb016", label: gettext('Area') },
        { field: "mb001", label: gettext('Type Id') },
        { field: "mb005", label: gettext('Contact') },
        {
            field: "mb006", label: gettext('Create Date'), render: function (data) {
                if (data === null) return "";
                return data.replace(/^(\d{4})(\d{2})(\d{2})$/, "$1-$2-$3");
            }
        },
        { field: "mb008", label: gettext('Usage') },
    ];
    var mb004_width = SWApp.os.isMobile ? "60%" : "40%"
    var scrollY_height = SWApp.os.isMobile ? "300px" : "380px"
    technicTable.setOptions({
        responsive: true,
        colReorder: true, 
        scrollY: scrollY_height,
        columnDefs: [
            { "responsivePriority": 2, "className": "min-tablet-p", "targets": 0 },
            { "responsivePriority": 1, width: mb004_width, "className": "all test", "targets": 2 },
            { "responsivePriority": 2, "className": "none", "targets": 3 },
            { "responsivePriority": 3, "className": "none", "targets": 4 },
            { "responsivePriority": 5, "className": "min-tablet-p", "targets": 5 },
            { "responsivePriority": 3, "className": "none", "targets": 6 },
            { "responsivePriority": 5, width: "30%", "className": "min-tablet-p", "targets": 7 },
        ],
        deferLoading: 0,
    });
    technicTable.custom_params_fun = function () {
        var bmb006 = $('#techEnquiryCollapse input[name="bmb006"]').val()
        var emb006 = $('#techEnquiryCollapse input[name="emb006"]').val()
        var quictfilter = {"condition":"AND","rules":[],"not":false,"valid":true}
        if(bmb006!=''){
            quictfilter['rules'].push({"id": "mb006","field": "mb006","type": "string","input": "text",
            "operator": "greater_or_equal","value":bmb006.replaceAll('-','')})
        }
        if(emb006!=''){
            quictfilter['rules'].push({"id": "mb006","field": "mb006","type": "string","input": "text",
            "operator": "less_or_equal","value":emb006.replaceAll('-','')})
        }
        if (quictfilter['rules'].length>0) {
            return {attach_query: JSON.stringify(quictfilter)};
        }
        else
            return {};
    } 
    technicTable_q = technicTable
    technicTable_datatable_q = technicTable.init('/PMIS/TechnicalDatatable');
    if(SWApp.os.isMobile){
        technicTable_datatable_q.colReorder.move( 2, 0 )
    }






}

//綁定事件
function bind_event() {
    $.contextMenu({
        selector: '#category_tree li',
        callback: function(key, options) {
            if (key == "add") {
                append_Category()
            }else if(key == "update"){
                update_Category()
            }
        },
        items: {
            "add": {name: gettext("Create Category"), icon: "add"},
            "update": {name: gettext("Update Category"), icon: "add"},
        }
    });

}

function get_real_search_value(search_txt) {
    if (!search_txt)
        return ""
    search_txt = search_txt.trim();
    var chinese_match = search_txt.match(/[\u4e00-\u9fa5]+/g)
    var english_match = search_txt.match(/[^\u4e00-\u9fa5]+/g)
    var chinese_txt = chinese_match == null ? "" : chinese_match.join("");
    var english_txt = english_match == null ? "" : english_match.join("");
    var skip_txt = this.search_skip_txt_arr
    var english_txt = english_txt.trim().split(/\s+/).map((a)=>a.toLowerCase()).filter((x)=>x != "");
    var new_word = []
    for(var word of english_txt) {
        if (skip_txt.indexOf(word) == -1)
            new_word.push(word);
    }
    var chinese_txt = chinese_txt.trim().split("").filter((x)=>x != "");
    for(var word of chinese_txt) {
        if (this.search_skip_txt_arr_cn.indexOf(word) == -1)
            new_word.push(word);
    }
    if (new_word.length > 0)
        return new_word.join("+")
    else
        return ""
}

function get_lang_code() {
    var lang_code_en = $("#curr_language_code").val();
    if( lang_code_en == "en") {
        $(".page").addClass("lang_en")
    }
}

//新增分類
function append_Category(isRoot=false){
    if(isRoot){$('#quick_category_form #edtMA002C').parent().attr('hidden',true);}else{$('#quick_category_form #edtMA002C').parent().attr('hidden',false);}
    $('#quick_category_mini .modal-title').html(gettext('Create Category'));
    form_Category.set_pk(undefined);
    form_Category.init_data();
    $('#quick_category_mini').modal('show')
}

//修改分類
function update_Category(){
    // var up_category = $('#miniSelectquery_table').DataTable().rows(['.selected']).data();
    // if (up_category==undefined || up_category.length==0){
    //     alert('請選擇需要修改的分類！')
    //     return
    // }
    var treeselected = $("#category_tree").jstree().get_selected()
    if(treeselected.length==0 || selected_node['inc_id']==undefined){
        return alert('請選擇分類！')    
    }
    if(selected_node['ma002'].replaceAll(' ','')==''){$('#quick_category_form #edtMA002C').parent().attr('hidden',true);}else{$('#quick_category_form #edtMA002C').parent().attr('hidden',false);}
    $('#quick_category_mini .modal-title').html(gettext('Update Category'));
    form_Category.set_pk(selected_node['inc_id']);
    form_Category.init_data();
    $('#quick_category_mini').modal('show')
}

//新增分類時底下的Modal模糊化
$('#quick_category_tree').on('shown.bs.modal', function() {
    $('#quick-add-technic').addClass('blur');
}).on('hidden.bs.modal', function() {
    $('#quick-add-technic').removeClass('blur');
});


//獲取技術文檔編號
function getTechnicId(){
    if(($('input[name="mb016"]').val().trim() != '') && ($('input[name="mb015"]').val().trim() !='') ){
        var TechnicId = $('input[name="mb015c"]').val().slice(0,3).trim()+'-'+$('input[name="mb016"]').val().trim().slice(0,3)+'-'
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
                        if ($('input[name="mb023"]').val().slice(0,8).trim()!=jsondata[0]['theTechnicid'].slice(0,8).trim()){
                            $('input[name="mb023"]').val(jsondata[0]['theTechnicid']);
                        }
                    }
                }
            }
        })
    }
}





//樹狀圖右鍵菜單
function categoryMenu(node) {
    var path = node.parents.concat(node.id).reverse();
    var level = path.length - 1;
    var items = {
        updateItem: {
            "label": gettext("Update node"),
            "action": function (obj) {
                update_Category()
            }
        },
    };

    // 根据节点层级生成不同的菜单项
    if (level === 1) {
        items.add = {
            "label": gettext("Add Area"),
            "action": function (obj) {
                append_Category()
            }
        }; 
    } else if (level === 2) {
        items.add = {
            "label": gettext("Add Sub Area"),
            "action": function (obj) {
                append_Category()
            }
        }; 
    }
    return items;
}     
    


/**
 * 刷新樹狀圖：從伺服器取得資料後重新初始化 jsTree。
 */
function refresh_tree() {
    var category = $('#category_tree_q').val();
    var area = $('#category_tree_area').val();
    var subarea = $('#category_tree_subarea').val();
    var url = `/PMIS/technical/categorytree?category=${encodeURIComponent(category)}&area=${encodeURIComponent(area)}&subarea=${encodeURIComponent(subarea)}`;

    $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        success: (result) => {
            var arrays = result.data;
            var jsonarray = buildTree(arrays, "ma002", "ma001", "ma003", "");
            var treeInstance = $('#category_tree').jstree(true);
            if (treeInstance) {
                treeInstance.destroy();
            }
            init_tree(jsonarray);
        },
        error: (err) => {
            console.error("獲取樹狀資料失敗:", err);
        }
    });
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




function preview_report(report_name, datasource) {
    localStorage.setItem("report_name", report_name);
    localStorage.setItem("report_data", JSON.stringify(datasource));
    window.open("/base_report/preview", "_blank")
}