$(document).ready(function() {
  //以下注解是在header下面添加一行用於過濾每個字段內容的，
  //但當前與 colResize(column拖動調整長度 第三方插件)有沖突
  /**$('#dataTables-example thead tr').clone(true).appendTo( '#dataTables-example thead' );
  $('#dataTables-example thead tr:eq(1) th').each( function (i) {
      var title = $(this).text();
      $(this).html( '<input type="text" placeholder="Search '+title+'" />' );

      $( 'input', this ).on( 'keyup change', function () {
          if ( table.column(i).search() !== this.value ) {
              table
                  .column(i)
                  .search( this.value )
                  .draw();
          }
      } );
  } );*/
  //在初始化數據前，設置Search 輸入框的搜索圖標
  $("#dataTables-example").one("preInit.dt", function () {
    $('#dataTables-example_filter .form-control').css("background-image", "url(data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+PHN2ZyAgIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgICB4bWxuczpjYz0iaHR0cDovL2NyZWF0aXZlY29tbW9ucy5vcmcvbnMjIiAgIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyIgICB4bWxuczpzdmc9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiAgIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgICB2ZXJzaW9uPSIxLjEiICAgaWQ9InN2ZzQ0ODUiICAgdmlld0JveD0iMCAwIDIxLjk5OTk5OSAyMS45OTk5OTkiICAgaGVpZ2h0PSIyMiIgICB3aWR0aD0iMjIiPiAgPGRlZnMgICAgIGlkPSJkZWZzNDQ4NyIgLz4gIDxtZXRhZGF0YSAgICAgaWQ9Im1ldGFkYXRhNDQ5MCI+ICAgIDxyZGY6UkRGPiAgICAgIDxjYzpXb3JrICAgICAgICAgcmRmOmFib3V0PSIiPiAgICAgICAgPGRjOmZvcm1hdD5pbWFnZS9zdmcreG1sPC9kYzpmb3JtYXQ+ICAgICAgICA8ZGM6dHlwZSAgICAgICAgICAgcmRmOnJlc291cmNlPSJodHRwOi8vcHVybC5vcmcvZGMvZGNtaXR5cGUvU3RpbGxJbWFnZSIgLz4gICAgICAgIDxkYzp0aXRsZT48L2RjOnRpdGxlPiAgICAgIDwvY2M6V29yaz4gICAgPC9yZGY6UkRGPiAgPC9tZXRhZGF0YT4gIDxnICAgICB0cmFuc2Zvcm09InRyYW5zbGF0ZSgwLC0xMDMwLjM2MjIpIiAgICAgaWQ9ImxheWVyMSI+ICAgIDxnICAgICAgIHN0eWxlPSJvcGFjaXR5OjAuNSIgICAgICAgaWQ9ImcxNyIgICAgICAgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNjAuNCw4NjYuMjQxMzQpIj4gICAgICA8cGF0aCAgICAgICAgIGlkPSJwYXRoMTkiICAgICAgICAgZD0ibSAtNTAuNSwxNzkuMSBjIC0yLjcsMCAtNC45LC0yLjIgLTQuOSwtNC45IDAsLTIuNyAyLjIsLTQuOSA0LjksLTQuOSAyLjcsMCA0LjksMi4yIDQuOSw0LjkgMCwyLjcgLTIuMiw0LjkgLTQuOSw0LjkgeiBtIDAsLTguOCBjIC0yLjIsMCAtMy45LDEuNyAtMy45LDMuOSAwLDIuMiAxLjcsMy45IDMuOSwzLjkgMi4yLDAgMy45LC0xLjcgMy45LC0zLjkgMCwtMi4yIC0xLjcsLTMuOSAtMy45LC0zLjkgeiIgICAgICAgICBjbGFzcz0ic3Q0IiAvPiAgICAgIDxyZWN0ICAgICAgICAgaWQ9InJlY3QyMSIgICAgICAgICBoZWlnaHQ9IjUiICAgICAgICAgd2lkdGg9IjAuODk5OTk5OTgiICAgICAgICAgY2xhc3M9InN0NCIgICAgICAgICB0cmFuc2Zvcm09Im1hdHJpeCgwLjY5NjQsLTAuNzE3NiwwLjcxNzYsMC42OTY0LC0xNDIuMzkzOCwyMS41MDE1KSIgICAgICAgICB5PSIxNzYuNjAwMDEiICAgICAgICAgeD0iLTQ2LjIwMDAwMSIgLz4gICAgPC9nPiAgPC9nPjwvc3ZnPg==)");
    $('#dataTables-example_filter .form-control').css("background-repeat", "no-repeat");
    $('#dataTables-example_filter .form-control').css("background-color", "#fff");
    $('#dataTables-example_filter .form-control').css("backgroundPositionX", "0px");
    $('#dataTables-example_filter .form-control').css("backgroundPositionY", "3px");
    $('#dataTables-example_filter .form-control').css("padding-left", "1.5rem");
  });

  var table = $("#dataTables-example").DataTable({
    initComplete: function(settings) {
      //以下注解的代碼的功能為:
      //在column header添加一個下拉選擇框 用於過濾該字段內容
      //還沒有處理好
      /**this.api().columns().every( function () {
        var column = this;
        var select = $(`<button type="button" class="btn btn-danger dropdown-toggle dropdown-toggle-split" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        <span class="sr-only">Toggle Dropdown</span>
                        </button>
                        <div class="dropdown-menu">
                        </div>`)
            .appendTo( $(column.header()))
            .on('click', function () {
                var val = $.fn.dataTable.util.escapeRegex(
                    $(this).val()
                );
                column
                    .search( val ? '^'+val+'$' : '', true, false )
                    .draw();
            } );

        column.data().unique().sort().each( function ( d, j ) {
            $('<a class="dropdown-item" href="#">'+d+'</a>').appendTo(select[2]);
        });
      });*/
    },
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
    scrollY:        400, //垂直滾動高度
    scrollX:         true,
    //scrollCollapse: true, //當顯示有限的行數時，允許表格降低高度
    //scroller:       true,  //啟用和配置DataTables的Scroller擴展
    select: {       //啟用和配置DataTables的select擴展, 支持選擇一行或多行
        style:'os' //api 只能api選擇， single 單行， multi 多行,  os 不按ctrl時是單選 按住時是多先 multi+shift 按住shift 選擇範圍
    },
    orderCellsTop: true  //顯示排序
    //fixedHeader: true
  });

  //因為選擇字段顯示與否的下拉列表的樣式與keen默認樣式有沖突，這裏需要清除keen的樣式
  table.on( 'buttons-action', function ( e, buttonApi, dataTable, node, config ) {
      $('#dataTables-example_wrapper .buttons-columnVisibility').css({'color':'#212529','background-color':'transparent'});  
      $('#dataTables-example_wrapper .buttons-columnVisibility.active').css({'color':'#fff','background-color':'#5867dd'});  
  });
});

