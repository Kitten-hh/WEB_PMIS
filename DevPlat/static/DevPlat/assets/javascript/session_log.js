loadCss('/static/BaseApp/vendor/Looper/assets/vendor/select2/css/select2.min.css');
loadJs(['/static/BaseApp/vendor/Looper/assets/vendor/select2/js/select2.min.js'], false)
var gettext_operationLog = gettext("Operation Log");
function SessionLog() {
  var container = $('#Session_log');

  var sessionid = ''
  var contact = ''
  var log = ''
  var exeTime = ''

  this.init = function () {
    initPageUI();
    eventListener();
  }

  this.sessionChange = function (id) {
    if (sessionid === id) return;
    sessionid = id || '00500-6';
    initPageData(); //session和tab切換時進行log的初始化
  }

  function initPageUI() {
    contact = get_username() || ''; // 獲取默認的登陸者
    var Username = gettext("Username"); // 人員
    var Type = gettext("Type"); // log類型
    var ExeTime = gettext("ExeTime"); // 執行時間
    var Save = gettext("Save"); // 保存
    var logDesc = gettext("Log desc"); // 日誌描述
    var logInfoList = gettext("Log info list"); // 日誌信息列表
    var TypeManager = gettext("Type Manager") // 類型管理
    var template = `
    <div class="card card-fluid m-0">
      <div class="card-body">
        <div class="log-add">
          <div class="row mb-2">
            <div class="d-flex align-items-center col col-xl-2">
              <label for="logPerson" class='mr-2'>${Username}</label>
              <select class="log-contact form-control select-long" id="logPerson" data-none-selected-text>
                <!-- 人員选项 -->
              </select>
            </div>
            <div class="d-flex align-items-center col col-xl-2">
              <label for="logType">${Type}</label>
              <select class="select2-type form-control select-long" id="logType" data-none-selected-text>
                <!-- 类型选项 -->
              </select>
            </div>
            <div class="d-flex align-items-center col col-xl-2">
              <label for="logExeTime">${ExeTime}</label>
              <input type='text' class="form-control flatpickr" id="logExeTime" />
            </div>
            <div class="d-flex align-items-center col col-xl-2">
              <div class="action-buttons">
                <button class="btn btn-primary save">${Save}</button>
              </div>
            </div>
            <div class="col-auto ml-auto">
              <div class="action-buttons">
                <button class="btn btn-primary type-manager">${TypeManager}</button>
              </div>
            </div>
          </div>
          <div class="form-group">
            <label for="logMessage" class='mr-2'>${logDesc}</label>
            <textarea class="form-control" id="logMessage" rows="5"></textarea>
          </div>
        </div>
        <hr/>
        <h5 class="card-title">${logInfoList}</h5>
        <div class="log-list" style="height: 53vh;"></div>
        <h5 class="card-title d-flex justify-content-end mb-0"><strong class="totalNum"></strong></h5>
      </div>
    </div>`;
    container.html(template);
    setContactOptions();
    setCss();
    initPageData();
    typeManagerModal();
  }

  function typeManagerModal(){
    var TypeManager = gettext("Type Manager") // 類型管理 
    var template = `
    <div class="modal fade" id="type-manager-modal" tabindex="-1" role="dialog" aria-hidden="true">
      <div class="modal-dialog modal-dialog-scrollable " role="document">
        <div class="modal-content">
          <div v-show="show_header" class="modal-header">
            <h5 class="modal-title">
              ${TypeManager}
            </h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">×</span>
            </button>
          </div>
          <div class="modal-body"> 
            <div class="list-group shadow-none"> 
            
            </div>
          </div>
          <div class="modal-footer"> </div>
        </div>
      </div>
    </div>` 
    $('body').append(template);
  }

  async function setContactOptions() {
    var template = '';
    await window.CommonData.PartUserNames.then(res => {
      for (let v of res.data)
        if (v === contact) template += `<option value="${v}" selected>${v}</option>`;
        else template += `<option value="${v}">${v}</option>`
    });
    $('#logPerson').html(template);
    $('#logPerson').selectpicker('refresh');
  }

  function setCss() {
    var style = document.createElement('style');
    style.type = 'text/css';
    var cssContent = `
      #Session_log .log-add .form-group {
        display: flex;
        margin-bottom: 0.5rem;
      }
      #Session_log .log-add .form-inline {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      #Session_log .log-add .form-inline > label {
        flex: 0 0 auto;
        margin-right: 1rem; /* Spacing between label and select */
      }
      #Session_log .log-add label {
        min-width: 65px;
        margin-bottom: 0;
      }
      #Session_log .log-add .action-buttons {
        display: flex;
        justify-content: flex-end;
      }
      #Session_log .log-add .save {
        margin-left: 1rem;
      }
      #Session_log .log-list {
        overflow-y: scroll;
        margin-bottom: 1rem;
      }
      #Session_log .log-add #logType+.select2-container {
        width: 100% !important
      }
      .flatpickr-day {
        padding: 0 !important
      }
    `;
    if (style.styleSheet) {
      style.styleSheet.cssText = cssContent;
    } else {
      style.appendChild(document.createTextNode(cssContent));
    }
    document.head.appendChild(style);
  }

  function sessionLogList(logArray) {
    function formatDate(date) { return new Date(date).format('yyyy-MM-dd hh:mm') }
    function formatType(type) {
      if (type === undefined || type === null) return ''
      return type
    }
    var template = logArray.map(item => `
      <div class="card mb-1 log-message-row">
        <div class="list-group list-group-messages list-group-flush list-group-bordered">
          <div class="list-group-item unread p-1">
            <div class="list-group-item-figure" style="align-self: center;">
                <div class="tile tile-circle bg-blue" style="font-size: 12px; text-transform: uppercase;">${item.username}</div>
            </div>
            <div class="list-group-item-body pl-md-2" style="align-self: center;">
                <div class="row mx-0">
                    <div class="col-12 col-lg-3 d-flex align-items-center">
                        <span class="list-group-item-text text-dark mr-3"> ${formatDate(item.exetime)} </span>
                        <h4 class="list-group-item-title text-truncate" style="color: #222230;">${formatType(item.actiontype)}</h4>
                    </div>
                    <div class="col-12 col-lg-9">
                        <h4 class="list-group-item-title text-truncate">${item.action}</h4>
                    </div>
                </div>
            </div>
          </div>
        </div>
      </div>
        `).join('');
    container.find('.log-list').empty().append(template);
  }

  function eventListener() {
    $('select.select2-type').select2({ tags: true }).on("select2:select", function (e) {
      // var inputValue = e.params.data.text;
      // console.log(inputValue)
    });
    // container.find("textarea#logMessage").donetyping(function () { saveSessionLog() }, 2000);

    container.find('button.save').click(function () { saveSessionLog() });
    container.find('button.type-manager').click(function () { 
      var typeList = [];
      $.ajax({
        url: '/devplat/log/get',
        type: 'GET',
        data: {sessionid: sessionid},
        dataType: 'json',
        async: false,
        success: function (res) {
          if (res.status) {
            typeList = res.type_list;
          }
        }
      });
      var modalBody = typeList.map(item => `
          <div class="list-group-item list-group-item-action custom_listGroupItem">
            <div class="list-group-item-body">
              <span class="list-group-item-text">${item}</span>
            </div>
            <div class="list-group-item-figure">
              <button class="btn btn-sm btn-icon btn-light"><i class="far fa-trash-alt"></i></button>
            </div>
          </div>
        `).join('');
      $("#type-manager-modal").find(".modal-body .list-group").empty().append(modalBody)
      $("#type-manager-modal").find(".modal-dialog").width('25%').css("max-width","none")
      $("#type-manager-modal").modal('show') 
    });
    // container.find('.log-list').on('dblclick', '.log-message-row', function() {
    //   var itemData = JSON.parse($(this).attr('data-item'));
    //   logMessageRowDblclick(itemData);
    // });
    // 時間日期格式的初始化
    exeTime = new Date().format('yyyy-MM-dd hh:mm');
    var options = {
      defaultDate: new Date(),
      enableTime: true, // 启用时间选择
      dateFormat: "Y-m-d H:i", // 设置日期和时间的格式
      onChange: (selectedDates, dateStr, instance) => {
        exeTime = dateStr;
      },
      onReady: (selectedDates, dateStr, instance) => {
        const clearBtn = $('<button class="btn btn-sm btn-link flatpickr-clear">' + gettext('Clear') + '</button>')
          .on('click', () => {
            instance.clear();
            instance.close();
          });
        const todayBtn = $('<button class="btn btn-sm btn-link flatpickr-today">' + gettext('Today') + '</button>')
          .on('click', () => {
            instance.setDate(new Date(), true);
            instance.close();
          });
        const btnContainer = $('<div class="flatpickr-buttons d-flex align-items-center justify-content-between p-2"></div>');
        $(todayBtn).appendTo(btnContainer);
        $(clearBtn).appendTo(btnContainer);
        btnContainer.appendTo($(instance.calendarContainer));
      },
    }
    flatpickr($('input.flatpickr')[0], options);
    //instance.setDate(text).setDate(new Date());
    // 時間日期格式的初始化 end
  }

  // function logMessageRowDblclick(itemData) {
  //   console.log(itemData)
  // }

  function initPageData() {
    var data = {
      sessionid: sessionid,
    };
    $.ajax({
      url: '/devplat/log/get',
      type: 'GET',
      data: data,
      dataType: 'json',
      success: function (res) {
        if (res.status) {
          sessionLogList(res.data);
          $('select.select2-type').empty();
          res.type_list.forEach(function (item) {
            if (item != '') {
              var option = new Option(item, item, false, false);
              $('select.select2-type').append(option);
            }
          });
          $('select.select2-type').trigger('change');
          container.find('h5.card-title strong.totalNum').empty().append('  Total: ' + parseInt(res.total || 0));
        }
        else
          sessionLogList([])
      }
    })
  }

  function saveSessionLog() {
    log = $('#logMessage').val();
    contact = $('#logPerson').val();
    type = $('#logType').val();
    if (String(contact || '') === '')
      return alert(gettext('username is empty')); //'沒有選擇用戶名'
    if (String(type || '') === '')
      return alert(gettext('type is empty')); //'沒有選擇類型'
    if (String(log || '') === '')
      return alert(gettext('log info is empty')); //'日誌信息不能為空'
    if (String(exeTime || '') === '')
      return alert(gettext('exe time is empty')); //'執行時間不能為空'
    var postData = {
      contact: contact,
      sessionid: sessionid,
      log: log,
      type: type,
      exeTime: exeTime,
    }
    $.ajax({
      url: '/devplat/log/save',
      type: 'POST',
      data: postData,
      dataType: 'json',
      beforeSend: function (request) {
        request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      },
      success: function (res) {
        var text = ''
        if (res.status) {
          text = gettext('success'); //'保存成功'
          $('#logMessage').val('');
        }
        else
          text = gettext('fail'); //'保存失敗'
        SWApp.popoverMsg($('#Session_log button.save'), text);
        initPageData();
      },
    });
  }
}