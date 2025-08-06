
function Overview() {
    this.Requirement = undefined;
    this.edit_form = undefined;
    var self = this;
    this.init = function() {
        var projectName = getCookie("projects_cur_name");
        var title = "User Requirement";
        if (projectName != undefined && projectName != "null" && projectName != "undefined")
            title = title + " - " + projectName;
        let form1 = new SWForm("#Overview",title,"url","GET",false);
        form1.addComponent(new SWText("rid","text",gettext('Requirement ID')));
        $("#Overview input[name='rid']").attr("readonly","readonly");
        form1.addComponent(new SWTextarea("purpose",gettext('Purpose'), 3).setAutoSize(true));
        form1.addComponent(new SWTextarea("feature",gettext('Feature'), 3).setAutoSize(true));
        form1.addComponent(new SWTextarea("fr",gettext('Functional Requirement'), 5).setAutoSize(true));
        form1.addComponent(new SWTextarea("gh",gettext('Good to Have'), 5).setAutoSize(true));
        form1.addComponent(new SWTextarea("mh",gettext('Must Have'), 5).setAutoSize(true));
        form1.addComponent(new SWTextarea("uc",gettext('Under Consideration'), 5).setAutoSize(true));
        form1.addComponent(new SWTextarea("nr",gettext('Non-Functional Requirement'), 5).setAutoSize(true));
        form1.addComponent(new SWText("sessionid","hidden","Session id"));
        form1.addComponent(new SWTextarea("attributes",gettext('Requirement attributes'), 3).setAutoSize(true));
        form1.addComponent(new SWCombobox("rt",gettext('Requirement Type'), "/devplat/requement/gettypes"));
        form1.create_url = "/devplat/requement/create";  
        form1.update_url = "/devplat/requement/update?pk=[[pk]]";  
        form1.pk_in_url = false;
        form1.auto_save(true);
        form1.on_after_save = function(data) {
        }
        form1.on_after_init = function(data) {
            $("#Overview textarea").trigger("change");
        }
        self.edit_form = form1;
        var recordid = getParamFromUrl("recordid");
        //如果recordid不為空則顯示Overview的 User Requirement
        if (recordid != undefined ) {
            self.Requirement.get_pk_with_rid(recordid).then((pk)=>{
                if (pk == "") {
                    self.edit_form.set_pk(undefined);       
                    self.edit_form.init_data({recordid:recordid});     
                }else {
                    self.edit_form.set_pk(pk);
                    self.edit_form.init_data();        
                }
            });
        }
    }
}