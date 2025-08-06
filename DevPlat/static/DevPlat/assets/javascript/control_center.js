
function ControlCenter() {
    this.edit_form = undefined;
    this.CommonData = {
        'UpdateType':[{value:"DataBase", label:"數據庫"},{value:"Installation", label:"安裝"},{value:"UpdateInstallation", label:"更新程序"}]
    }
    var self = this;
    this.init = function() {
        var strhtml = '<form class="form-2 form" action="url" method="GET"><div class="page-inner"><div class="container"><div class="row"><div class="col-lg-12"><div class="card card-custom gutter-b example example-compact">\
            <div class="card-header card-title">' + gettext("VMs Control Systems Centre") + '</div><div class="card-body">\
            <div class="row"><div class="col-12 col-sm-4"><div id="ccenter_VM"></div></div>\
            <div class="col-12 col-sm-4"><div id="ccenter_IP"></div></div><div class="col-12 col-sm-4"><div id="ccenter_UpdateType"></div></div>\
            <div class="col-12 col-sm-4"><div id="ccenter_RecordID"></div></div><div class="col-12 col-sm-4"><div id="ccenter_SName"></div></div>\
            <div class="col-12 col-sm-4"><div id="ccenter_SID"></div></div><div class="col-12 col-sm-4"><div id="ccenter_ServerIP"></div></div>\
            <div class="col-12 col-sm-4"><div id="ccenter_DBName"></div></div><div class="col-12 col-sm-4"><div id="ccenter_SyncDays"></div></div>\
            <div class="col-12 col-sm-6"><div id="ccenter_SessionId"></div></div><div class="col-12 col-sm-6"><div id="ccenter_SyncRecords"></div></div>\
            <div class="col-12 col-sm-12"><div id="ccenter_SessionName"></div></div><div class="col-12 col-sm-12"><div id="ccenter_DestPath"></div></div>\
            <div class="col-12 col-sm-12"><div id="ccenter_Desp"></div></div><div class="col-12 col-sm-12"><div id="ccenter_Remark"></div></div></div>\
            </div></div></div></div></div></div></form>'
        $('#control_center_edit').append(strhtml)

        var recordid = getParamFromUrl("recordid");
        var menu_id = getParamFromUrl("menu_id");
        if(menu_id!=null && menu_id!=''){
            menu_id=menu_id.split('mi_')
            menu_id=menu_id[menu_id.length-1]
        }
        $.ajax({
            url: `/devplat/ccenter/search_ControlCentre?SessionId=${menu_id}&&RecordID=${recordid}`,
            type: "GET",
            dataType: 'json',
            cache: false,
            success: function (json) {
                if (json.status && json.data.length > 0) {
                    var jsondata = json.data[0];
                    self.setData(jsondata);
                }else{
                    self.setData({})
                }
            }
        })
    }

    this.setData = function(Data){
        var vm = new SWText("vm", "text",gettext('VMName'),Data['VM']==undefined?'':Data['VM']);
        $("#control_center_edit #ccenter_VM").append(vm.dom);
        var ip = new SWText("ip", "text",gettext('VMIPLocation'),Data['IP']==undefined?'':Data['IP']);
        $("#control_center_edit #ccenter_IP").append(ip.dom);
        
        var updatetype = new SWCombobox("updatetype", gettext('UpdateType'),self.CommonData['UpdateType'], Data['UpdateType']==undefined?'':Data['UpdateType'], 'value', 'label');
        $("#control_center_edit #ccenter_UpdateType").append(updatetype.dom);

        var recordid = new SWText("recordid", "text",gettext('RecordID'),Data['RecordID']==undefined?'':Data['RecordID']);
        $("#control_center_edit #ccenter_RecordID").append(recordid.dom);
        var sname = new SWText("sname", "text",gettext('SystemName'),Data['SName']==undefined?'':Data['SName']);
        $("#control_center_edit #ccenter_SName").append(sname.dom);
        var sid = new SWText("sid", "text",gettext('SystemID'),Data['SID']==undefined?'':Data['SID']);
        $("#control_center_edit #ccenter_SID").append(sid.dom);
        
        var serverip = new SWText("serverip", "text",gettext('ServerIP'),Data['ServerIP']==undefined?'':Data['ServerIP']);
        $("#control_center_edit #ccenter_ServerIP").append(serverip.dom);
        var dbname = new SWText("dbname", "text",gettext('DBName'),Data['DBName']==undefined?'':Data['DBName']);
        $("#control_center_edit #ccenter_DBName").append(dbname.dom);
        var syncdays = new SWText("syncdays", "text",gettext('SyncDays'),Data['SyncDays']==undefined?'':Data['SyncDays']);
        $("#control_center_edit #ccenter_SyncDays").append(syncdays.dom);
        
        var sessionid = new SWText("sessionid", "text",gettext('SessionId'),Data['SessionId']==undefined?'':Data['SessionId']);
        $("#control_center_edit #ccenter_SessionId").append(sessionid.dom);
        var syncrecords = new SWText("syncrecords", "text",gettext('SyncRecords'),Data['SyncRecords']==undefined?'':Data['SyncRecords']);
        $("#control_center_edit #ccenter_SyncRecords").append(syncrecords.dom);
        
        var sessionname = new SWText("sessionname", "text",gettext('SessionName'),Data['SessionName']==undefined?'':Data['SessionName']);
        $("#control_center_edit #ccenter_SessionName").append(sessionname.dom);
        var destpath = new SWText("destpath", "text",gettext('Attachment'),Data['DestPath']==undefined?'':Data['DestPath']);
        $("#control_center_edit #ccenter_DestPath").append(destpath.dom);
        var desp = new SWTextarea("desp",gettext('Desp'),5, Data['Desp']==undefined?'':Data['Desp']);
        $("#control_center_edit #ccenter_Desp").append(desp.dom);
        var remark = new SWTextarea("remark",gettext('Remark'), 5, Data['Remark']==undefined?'':Data['Remark']);
        $("#control_center_edit #ccenter_Remark").append(remark.dom);

        $('#control_center_edit input').prop('readOnly', true);
    }
    
    

    
}