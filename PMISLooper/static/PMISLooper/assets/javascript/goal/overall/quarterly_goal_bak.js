$(function(){

    var contact = getParamFromUrl("contact");
    var period = getParamFromUrl("period");

    function init_monthly() {
        var url = "/PMIS/goal/overall/monthly";
        var params = {contact:contact, period:period};
        $.get(url, params, function(data){
            if (data.status) {
                for (var i = 0; i < Object.keys(data.data).length; i++) {
                    $(".monthly_{0}".format(i + 1)).prev().find("h5").text(Date.parse(Object.keys(data.data)[i]).toString("MMMM"))
                    var monthly = data.data[Object.keys(data.data)[i]];
                    var content = $("<div class='col'></div>");
                    var item = $(`<div class='task' pk='[[inc_id]]'>[[task]]([[recordid]] [[projectname]])<i class="far fa-times-circle"></i></div>`);
                    for (task of monthly) {
                        var local_item = item.clone();
                        content.append(local_item.prop("outerHTML").render(task));
                    }
                    $(".monthly_{0}".format(i + 1)).find(".monthly").append(content);
                }
            }
        })
    }

    function init_weekly() {
        var url = "/PMIS/goal/overall/weekly_bak";
        var params = {contact:contact, period:period};
        $.get(url, params, function(data){
            if (data.status) {
                for (var i = 0; i < Object.keys(data.data).length; i++) {
                    var group = data.data[Object.keys(data.data)[i]];
                    for (var j = 0; j < Object.keys(group).length; j++) {
                        var weekly = group[Object.keys(group)[j]];
                        var weekly_content = $("<div><div>{0}</div></div>".format(Object.keys(group)[j]));
                        var item = $(`<div class='task' pk='[[inc_id]]'>[[task]]([[recordid]])<i class="far fa-times-circle"></i></div>`);
                        for (task of weekly) {
                            var local_item = item.clone();
                            weekly_content.append(local_item.prop("outerHTML").render(task));
                        }
                        if (j == 0 || j == 1)
                            $(".monthly_{0}".format(i+1)).find(".weekly_1").append(weekly_content);    
                        else
                            $(".monthly_{0}".format(i+1)).find(".weekly_2").append(weekly_content);    
                    }
                }
            }
        })
    }

    init_monthly();
    init_weekly();

    function update_task(self) {
        var pk = $(self).attr("pk")
        init_task(pk);
    }

    $(".quarterly").on(
        {
            dblclick:function(){
                update_task(this);
            },
            longpress:function() {
                update_task(this);
            }
        },
        ".task"
    );        
});