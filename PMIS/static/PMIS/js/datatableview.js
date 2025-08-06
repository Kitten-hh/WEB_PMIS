/* For datatable view */

var datatableview = (function(){
    var defaultDataTableOptions = {
        "serverSide": true,
        "paging": true
    }
    var optionsNameMap = {
        'name': 'name',
        'config-sortable': 'orderable',
        'config-sorting': 'order',
        'config-visible': 'visible',
        'config-searchable': 'searchable'
    };

    var checkGlobalConfirmHook = true;
    var autoInitialize = false;

    function initialize($$, dataTableStyle, opts) {
        $$.each(function(){
            var datatable = $(this);
            var styleOptions = opts;
            if(dataTableStyle != null) {
                dataTableStyle.initialize(datatable);
                styleOptions = dataTableStyle.getOptions(opts);
            }
            var options = datatableview.getOptions(datatable, styleOptions);
            var table = datatable.DataTable(options);
            if(dataTableStyle != null)
                dataTableStyle.defaultHandleStyle(table);
        });
        return $$;
    }

    function getOptions(datatable, opts) {
        /* Reads the options found on the datatable DOM into an object ready to be sent to the
           actual DataTable() constructor.  Is also responsible for calling the finalizeOptions()
           hook to process what is found.
        */
        var columnOptions = [];
        var sortingOptions = [];

        datatable.find('thead th').each(function(){
            var header = $(this);
            var options = {};
            for (var i = 0; i < header[0].attributes.length; i++) {
                var attr = header[0].attributes[i];
                if (attr.specified && /^data-/.test(attr.name)) {
                    var name = attr.name.replace(/^data-/, '');
                    var value = attr.value;

                    // Typecasting out of string
                    name = optionsNameMap[name];
                    if (/^(true|false)/.test(value.toLowerCase())) {
                        value = (value === 'true');
                    }

                    if (name == 'order') {
                        // This doesn't go in the columnOptions
                        var sort_info = value.split(',');
                        sort_info[1] = parseInt(sort_info[1]);
                        sortingOptions.push(sort_info);
                        continue;
                    }

                    options[name] = value;
                }
            }
            columnOptions.push(options);
        });
        var hasOperation = false;
        if (opts != null && opts.columns != null)
            for(var i = 0; i < opts.columns.length; i++) {
                if (opts.columns[i].hasOwnProperty("mRender")) {
                    columnOptions.push(opts.columns[i])
                    hasOperation = true;
                }
            }
        if(hasOperation)
            datatable.find('thead tr').append("<th>Operation</th>")

        // Arrange the sorting column requests and strip the priority information
        sortingOptions.sort(function(a, b){ return a[0] - b[0] });
        for (var i = 0; i < sortingOptions.length; i++) {
            sortingOptions[i] = sortingOptions[i].slice(1);
        }


        options = $.extend({}, datatableview.defaults, opts, {
            "order": sortingOptions,
            "columns": columnOptions,
            "pageLength": datatable.attr('data-page-length'),
            "infoCallback": function(oSettings, iStart, iEnd, iMax, iTotal, sPre){
                $("#" + datatable.attr('data-result-counter-id')).html(parseInt(iTotal).toLocaleString());
                var infoString = oSettings.oLanguage.sInfo.replace('_START_',iStart).replace('_END_',iEnd).replace('_TOTAL_',iTotal);
                if (iMax != iTotal) {
                    infoString += oSettings.oLanguage.sInfoFiltered.replace('_MAX_',iMax);
                }
                return infoString;
            }
        });
        options.ajax = $.extend(options.ajax, {
            "url": datatable.attr('data-source-url'),
            "type": datatable.attr('data-ajax-method') || 'GET',
            "beforeSend": function(request){
                request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        });

        options = datatableview.finalizeOptions(datatable, options);
        return options;
    }

    function finalizeOptions(datatable, options) {
        /* Hook for processing all options before sent to actual DataTable() constructor. */

        // Legacy behavior, will be removed in favor of user providing their own finalizeOptions()
        if (datatableview.checkGlobalConfirmHook) {
            if (window.confirm_datatable_options !== undefined) {
                options = window.confirm_datatable_options(options, datatable);
            }
        }
        return options;
    }

    function makeXEditable(options) {
        var options = $.extend({}, options);
        if (!options.ajaxOptions) {
            options.ajaxOptions = {}
        }
        if (!options.ajaxOptions.headers) {
            options.ajaxOptions.headers = {}
        }
        options.ajaxOptions.headers['X-CSRFToken'] = getCookie('csrftoken');
        options.error = function (data) {
            var response = data.responseJSON;
            if (response.status == 'error') {
                var errors = $.map(response.form_errors, function(errors, field){
                    return errors.join('\n');
                });
                return errors.join('\n');
            }
        };
        return function(nRow, mData, iDisplayIndex) {
            $('td a[data-xeditable]', nRow).editable(options);
            return nRow;
        }
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var api = {
        // values
        autoInitialize: autoInitialize,
        auto_initialize: undefined,  // Legacy name
        checkGlobalConfirmHook: checkGlobalConfirmHook,
        defaults: defaultDataTableOptions,

        // functions
        initialize: initialize,
        getOptions: getOptions,
        finalizeOptions: finalizeOptions,
        makeXEditable: makeXEditable,
        make_xeditable: makeXEditable  // Legacy name
    }
    return api;
})();

$(function(){
    var shouldInit = null;
    if (datatableview.auto_initialize === undefined) {
        shouldInit = datatableview.autoInitialize;
    } else {
        shouldInit = datatableview.auto_initialize
    }

    if (shouldInit) {
        datatableview.initialize($('.datatable'));
    }
});


/**以下為自己定義的不同表格的風格 */
var baseDataTableStyle = (function(){
    defaultDataTableOptions = {}
    datatable = {}
    function initialize($$) {
        $$.addClass("table table-striped- table-bordered table-hover table-checkable dt-responsive");        
    }
    function defaultHandleStyle($$) {
    }
    function getOptions(opts) {    
    }
    var api = {
        // functions
        initialize:initialize,
        getOptions: getOptions,
        defaultHandleStyle: defaultHandleStyle
    }
    return api;
})();


var basicDataTableStyle = $.extend({}, baseDataTableStyle, {
    defaultDataTableOptions:{
          //responsive: true,    
          oLanguage: { "sSearch": ``},
          dom: `Z<'row'<'col-sm-6 text-left'f><'col-sm-6 text-right'B>>
          <'row'<'col-sm-12'tr>>
          <'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 dataTables_pager'lp>>`,
          buttons: [
            'print',
            'copyHtml5',
            'excelHtml5',
            'csvHtml5',
            'pdfHtml5',
            'colvis'
          ],
          colReorder: true,  //為資料表啟用和配置ColReorder擴展, 列可以拖動位置
          colResize: {   //設置列可以拖動調整寬度
            //"tableWidthFixed": true,
              },    
          deferRender:    true, //功能控制延遲渲染以提高初始化速度, 渲染用戶看到的部分
          paging: true,
          autoWidth: false,
          scrollY:        600, //垂直滾動高度
          scrollX:         true,          
          //scrollCollapse: true, //當顯示有限的行數時，允許表格降低高度
          //scroller:       true,  //啟用和配置DataTables的Scroller擴展
          select: {       //啟用和配置DataTables的select擴展, 支持選擇一行或多行
              style:'os' //api 只能api選擇， single 單行， multi 多行,  os 不按ctrl時是單選 按住時是多先 multi+shift 按住shift 選擇範圍
          },
          orderCellsTop: true,  //顯示排序
          //fixedHeader: true
    },
    getOptions:function(opts) {
        options = $.extend(basicDataTableStyle.defaultDataTableOptions, opts);
        return options;
    },
    defaultHandleStyle:function(table) {
        var id = table.tables().nodes().to$().attr('id');
        //在初始化數據前，設置Search 輸入框的搜索圖標
        $("#" + id + "_filter .form-control").css("background-image", "url(data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+PHN2ZyAgIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgICB4bWxuczpjYz0iaHR0cDovL2NyZWF0aXZlY29tbW9ucy5vcmcvbnMjIiAgIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyIgICB4bWxuczpzdmc9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiAgIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgICB2ZXJzaW9uPSIxLjEiICAgaWQ9InN2ZzQ0ODUiICAgdmlld0JveD0iMCAwIDIxLjk5OTk5OSAyMS45OTk5OTkiICAgaGVpZ2h0PSIyMiIgICB3aWR0aD0iMjIiPiAgPGRlZnMgICAgIGlkPSJkZWZzNDQ4NyIgLz4gIDxtZXRhZGF0YSAgICAgaWQ9Im1ldGFkYXRhNDQ5MCI+ICAgIDxyZGY6UkRGPiAgICAgIDxjYzpXb3JrICAgICAgICAgcmRmOmFib3V0PSIiPiAgICAgICAgPGRjOmZvcm1hdD5pbWFnZS9zdmcreG1sPC9kYzpmb3JtYXQ+ICAgICAgICA8ZGM6dHlwZSAgICAgICAgICAgcmRmOnJlc291cmNlPSJodHRwOi8vcHVybC5vcmcvZGMvZGNtaXR5cGUvU3RpbGxJbWFnZSIgLz4gICAgICAgIDxkYzp0aXRsZT48L2RjOnRpdGxlPiAgICAgIDwvY2M6V29yaz4gICAgPC9yZGY6UkRGPiAgPC9tZXRhZGF0YT4gIDxnICAgICB0cmFuc2Zvcm09InRyYW5zbGF0ZSgwLC0xMDMwLjM2MjIpIiAgICAgaWQ9ImxheWVyMSI+ICAgIDxnICAgICAgIHN0eWxlPSJvcGFjaXR5OjAuNSIgICAgICAgaWQ9ImcxNyIgICAgICAgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNjAuNCw4NjYuMjQxMzQpIj4gICAgICA8cGF0aCAgICAgICAgIGlkPSJwYXRoMTkiICAgICAgICAgZD0ibSAtNTAuNSwxNzkuMSBjIC0yLjcsMCAtNC45LC0yLjIgLTQuOSwtNC45IDAsLTIuNyAyLjIsLTQuOSA0LjksLTQuOSAyLjcsMCA0LjksMi4yIDQuOSw0LjkgMCwyLjcgLTIuMiw0LjkgLTQuOSw0LjkgeiBtIDAsLTguOCBjIC0yLjIsMCAtMy45LDEuNyAtMy45LDMuOSAwLDIuMiAxLjcsMy45IDMuOSwzLjkgMi4yLDAgMy45LC0xLjcgMy45LC0zLjkgMCwtMi4yIC0xLjcsLTMuOSAtMy45LC0zLjkgeiIgICAgICAgICBjbGFzcz0ic3Q0IiAvPiAgICAgIDxyZWN0ICAgICAgICAgaWQ9InJlY3QyMSIgICAgICAgICBoZWlnaHQ9IjUiICAgICAgICAgd2lkdGg9IjAuODk5OTk5OTgiICAgICAgICAgY2xhc3M9InN0NCIgICAgICAgICB0cmFuc2Zvcm09Im1hdHJpeCgwLjY5NjQsLTAuNzE3NiwwLjcxNzYsMC42OTY0LC0xNDIuMzkzOCwyMS41MDE1KSIgICAgICAgICB5PSIxNzYuNjAwMDEiICAgICAgICAgeD0iLTQ2LjIwMDAwMSIgLz4gICAgPC9nPiAgPC9nPjwvc3ZnPg==)");
        $("#" + id + "_filter .form-control").css("background-repeat", "no-repeat");
        $("#" + id + "_filter .form-control").css("background-color", "#fff");
        $("#" + id + "_filter .form-control").css("backgroundPositionX", "0px");
        $("#" + id + "_filter .form-control").css("backgroundPositionY", "3px");
        $("#" + id + "_filter .form-control").css("padding-left", "1.5rem");
        $("#" + id + "_wrapper .dataTables_pager").css("text-align", "right");
        $("#" + id + "_wrapper .dataTables_pager .dataTables_length").css("display", "inline-block");
        $("#" + id + "_wrapper .dataTables_pager .dataTables_paginate").css("display", "inline-block");
        $("#" + id + "_wrapper .text-right .dataTables_filter").css("display","inline-block");
        $("#" + id + "_wrapper .text-left .dataTables_filter").css("display","inline-block");
        //因為選擇字段顯示與否的下拉列表的樣式與keen默認樣式有沖突，這裏需要清除keen的樣式
        table.on( 'buttons-action', function ( e, buttonApi, dataTable, node, config ) {
            $("#" + id + "_wrapper .buttons-columnVisibility").css({'color':'#212529','background-color':'transparent'});  
            $("#" + id + "_wrapper .buttons-columnVisibility.active").css({'color':'#fff','background-color':'#5867dd'});  
        });  
        table.columns.adjust();
    }
});


var OnlyTableDataTableStyle = $.extend({}, baseDataTableStyle, {
    defaultDataTableOptions:{
          responsive: true,    
          oLanguage: { "sSearch": ``},
          dom: `Z<'row'<'col-sm-12'tr>>`,
          buttons: [
            'print',
            'copyHtml5',
            'excelHtml5',
            'csvHtml5',
            'pdfHtml5',
            'colvis'
          ],
          colReorder: true,  //為資料表啟用和配置ColReorder擴展, 列可以拖動位置
          colResize: {   //設置列可以拖動調整寬度
            //"tableWidthFixed": true,
              },    
          deferRender:    true, //功能控制延遲渲染以提高初始化速度, 渲染用戶看到的部分
          paging: false,
          //scrollY:        400, //垂直滾動高度
          scrollX:         true,          
          //scrollCollapse: true, //當顯示有限的行數時，允許表格降低高度
          //scroller:       true,  //啟用和配置DataTables的Scroller擴展
          select: {       //啟用和配置DataTables的select擴展, 支持選擇一行或多行
              style:'os' //api 只能api選擇， single 單行， multi 多行,  os 不按ctrl時是單選 按住時是多先 multi+shift 按住shift 選擇範圍
          },
          orderCellsTop: true,  //顯示排序
          //fixedHeader: true
    },
    getOptions:function(opts) {
        options = $.extend(OnlyTableDataTableStyle.defaultDataTableOptions, opts);
        return options;
    },
});


var SimpleDataTableStyle = $.extend({}, baseDataTableStyle, {
    defaultDataTableOptions:{
          //responsive: true,    
          oLanguage: { "sSearch": ``},
          dom: `Z<'row'<'col-sm-12'tr>>
               <'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 dataTables_pager'lp>>`,
          buttons: [
            'print',
            'copyHtml5',
            'excelHtml5',
            'csvHtml5',
            'pdfHtml5',
            'colvis'
          ],
          colReorder: true,  //為資料表啟用和配置ColReorder擴展, 列可以拖動位置
          colResize: {   //設置列可以拖動調整寬度
            //"tableWidthFixed": true,
              },    
          deferRender:    true, //功能控制延遲渲染以提高初始化速度, 渲染用戶看到的部分
          paging: true,
          autoWidth: false,
          scrollY:        600, //垂直滾動高度
          scrollX:         true,          
          //scrollCollapse: true, //當顯示有限的行數時，允許表格降低高度
          //scroller:true,
          /**scroller: { //啟用和配置DataTables的Scroller擴展
            //loadingIndicator: true          
          },*/
          select: {       //啟用和配置DataTables的select擴展, 支持選擇一行或多行
              style:'os' //api 只能api選擇， single 單行， multi 多行,  os 不按ctrl時是單選 按住時是多先 multi+shift 按住shift 選擇範圍
          },
          orderCellsTop: true,  //顯示排序
          //fixedHeader: true
    },
    getOptions:function(opts) {
        options = $.extend(SimpleDataTableStyle.defaultDataTableOptions, opts);
        return options;
    },
    defaultHandleStyle:function(table) {
        var id = table.tables().nodes().to$().attr('id');
        //在初始化數據前，設置Search 輸入框的搜索圖標
        $("#" + id + "_filter .form-control").css("background-image", "url(data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+PHN2ZyAgIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgICB4bWxuczpjYz0iaHR0cDovL2NyZWF0aXZlY29tbW9ucy5vcmcvbnMjIiAgIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyIgICB4bWxuczpzdmc9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiAgIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgICB2ZXJzaW9uPSIxLjEiICAgaWQ9InN2ZzQ0ODUiICAgdmlld0JveD0iMCAwIDIxLjk5OTk5OSAyMS45OTk5OTkiICAgaGVpZ2h0PSIyMiIgICB3aWR0aD0iMjIiPiAgPGRlZnMgICAgIGlkPSJkZWZzNDQ4NyIgLz4gIDxtZXRhZGF0YSAgICAgaWQ9Im1ldGFkYXRhNDQ5MCI+ICAgIDxyZGY6UkRGPiAgICAgIDxjYzpXb3JrICAgICAgICAgcmRmOmFib3V0PSIiPiAgICAgICAgPGRjOmZvcm1hdD5pbWFnZS9zdmcreG1sPC9kYzpmb3JtYXQ+ICAgICAgICA8ZGM6dHlwZSAgICAgICAgICAgcmRmOnJlc291cmNlPSJodHRwOi8vcHVybC5vcmcvZGMvZGNtaXR5cGUvU3RpbGxJbWFnZSIgLz4gICAgICAgIDxkYzp0aXRsZT48L2RjOnRpdGxlPiAgICAgIDwvY2M6V29yaz4gICAgPC9yZGY6UkRGPiAgPC9tZXRhZGF0YT4gIDxnICAgICB0cmFuc2Zvcm09InRyYW5zbGF0ZSgwLC0xMDMwLjM2MjIpIiAgICAgaWQ9ImxheWVyMSI+ICAgIDxnICAgICAgIHN0eWxlPSJvcGFjaXR5OjAuNSIgICAgICAgaWQ9ImcxNyIgICAgICAgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNjAuNCw4NjYuMjQxMzQpIj4gICAgICA8cGF0aCAgICAgICAgIGlkPSJwYXRoMTkiICAgICAgICAgZD0ibSAtNTAuNSwxNzkuMSBjIC0yLjcsMCAtNC45LC0yLjIgLTQuOSwtNC45IDAsLTIuNyAyLjIsLTQuOSA0LjksLTQuOSAyLjcsMCA0LjksMi4yIDQuOSw0LjkgMCwyLjcgLTIuMiw0LjkgLTQuOSw0LjkgeiBtIDAsLTguOCBjIC0yLjIsMCAtMy45LDEuNyAtMy45LDMuOSAwLDIuMiAxLjcsMy45IDMuOSwzLjkgMi4yLDAgMy45LC0xLjcgMy45LC0zLjkgMCwtMi4yIC0xLjcsLTMuOSAtMy45LC0zLjkgeiIgICAgICAgICBjbGFzcz0ic3Q0IiAvPiAgICAgIDxyZWN0ICAgICAgICAgaWQ9InJlY3QyMSIgICAgICAgICBoZWlnaHQ9IjUiICAgICAgICAgd2lkdGg9IjAuODk5OTk5OTgiICAgICAgICAgY2xhc3M9InN0NCIgICAgICAgICB0cmFuc2Zvcm09Im1hdHJpeCgwLjY5NjQsLTAuNzE3NiwwLjcxNzYsMC42OTY0LC0xNDIuMzkzOCwyMS41MDE1KSIgICAgICAgICB5PSIxNzYuNjAwMDEiICAgICAgICAgeD0iLTQ2LjIwMDAwMSIgLz4gICAgPC9nPiAgPC9nPjwvc3ZnPg==)");
        $("#" + id + "_filter .form-control").css("background-repeat", "no-repeat");
        $("#" + id + "_filter .form-control").css("background-color", "#fff");
        $("#" + id + "_filter .form-control").css("backgroundPositionX", "0px");
        $("#" + id + "_filter .form-control").css("backgroundPositionY", "3px");
        $("#" + id + "_filter .form-control").css("padding-left", "1.5rem");
        $("#" + id + "_wrapper .dataTables_pager").css("text-align", "right");
        $("#" + id + "_wrapper .dataTables_pager .dataTables_length").css("display", "inline-block");
        $("#" + id + "_wrapper .dataTables_pager .dataTables_paginate").css("display", "inline-block");
        $("#" + id + "_wrapper .text-right .dataTables_filter").css("display","inline-block");
        $("#" + id + "_wrapper .text-left .dataTables_filter").css("display","inline-block");
        //因為選擇字段顯示與否的下拉列表的樣式與keen默認樣式有沖突，這裏需要清除keen的樣式
        table.on( 'buttons-action', function ( e, buttonApi, dataTable, node, config ) {
            $("#" + id + "_wrapper .buttons-columnVisibility").css({'color':'#212529','background-color':'transparent'});  
            $("#" + id + "_wrapper .buttons-columnVisibility.active").css({'color':'#fff','background-color':'#5867dd'});  
        });  
        table.columns.adjust();
    }
});
