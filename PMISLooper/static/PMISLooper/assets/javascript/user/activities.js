$(function () {
    $("title").html(gettext('Activities'));
    var contact =  getParamFromUrl("contact");
    if (contact == null)
        contact = 'sing'
    else 
        update_tab_link();
    var all_user = new SWCombobox('user',gettext('User'),window.CommonData.PartUserNames, contact);
    all_user.dom.addClass("row");
    all_user.dom.find(".caption").css({"font-size":"16px","font-weight":"600"});
    all_user.dom.find("label").addClass("col-auto");
    all_user.dom.find("button").addClass("user_selected");
    all_user.dom.children(".control").css("width","100px");
    all_user.dom.children(".control").wrap('<div class="col-auto"></div>');
    var subtitle_tmpl = `<span class="timeline-date text-primary time">[[planbdate]]</span>
                        <span class="ml-4 timeline-date text-primary time" progress="[[progress]]">[[progress]]</span>
                        <span class="ml-4 timeline-date text-primary time">[[hoperation]]</span>
                        <span class="ml-4 timeline-date text-primary time">[[schpriority]]</span>
                        <span class="d-none pk">[[inc_id]]</span>`;
    var arrage_subtitle_tmpl = `<span class="timeline-date text-primary time">[[planbdate2]]</span>
                        <span class="ml-4 timeline-date text-primary time" arrageprogress="[[arrageprogress]]">[[arrageprogress]]</span>
                        <span class="ml-4 timeline-date text-primary time">[[hoperation]]</span>
                        <span class="ml-4 timeline-date text-primary time">[[schpriority]]</span>
                        <span class="d-none pk">[[inc_id]]</span>`;                        
    $(".page-inner .userlist").append(all_user.dom);
    var daily_tmpl = `<p class="font-weight-normal text-dark pt-1 mb-0 caption">[[task]]</p><span class="d-none pk">[[inc_id]]</span><i class="far fa-right"></i>`
    var daily_pattern = new SWTimeline2(gettext("Default Daily Pattern"), "/PMIS/task/default_dialy_pattern/"+contact,"planbdate","", daily_tmpl, "tasktid asc");
    $("#daily_pattern").append(daily_pattern.dom);
    var today_task = new SWTimeline2(gettext("Today's Tasks"), "/looper/user/activites/arrage_tasks?type=T&contact="+contact,"planbdate",subtitle_tmpl, "task", "planbdate asc", summary_today_arrage);
    $("#today_task").append(today_task.dom);
    var yesterday_task = new SWTimeline2(gettext("Yesterday's Tasks"), "/looper/user/activites/arrage_tasks?type=P&contact="+contact,"arrangedate",arrage_subtitle_tmpl,"task","arrangedate asc", summary_arrage);
    $("#yesterday_task").append(yesterday_task.dom);
    var comming_week_task = new SWTimeline2(gettext("Comming One Week Planing"), "/looper/user/activites/arrage_tasks?type=C&contact="+contact,"arrangedate",arrage_subtitle_tmpl,"task","arrangedate asc", summary_arrage);
    $("#comming_week_task").append(comming_week_task.dom);
    var schedule_task = new SWTimeline2(gettext("Schedule Priority Tasks"), "/PMIS/task/schedule_priority/"+contact,"planbdate",subtitle_tmpl,"task","planbdate asc");
    $("#activites_schedule_priority").append(schedule_task.dom);
    var class1_task = new SWTimeline2(gettext("Class1 Tasks"), "/PMIS/task/classone_tasks/"+contact,"planbdate",subtitle_tmpl,"task","planbdate asc");
    $("#class1_task").append(class1_task.dom);

    all_user.input_dom.on("change", function(){
        all_user.input_dom.selectpicker('refresh');
        today_task = new SWTimeline2(gettext("Today's Tasks"), "/looper/user/activites/arrage_tasks?type=T&contact="+all_user.input_dom.val(),"planbdate",subtitle_tmpl,"task","planbdate asc", summary_today_arrage);        
        var yesterday_task = new SWTimeline2(gettext("Yesterday's Tasks"), "/looper/user/activites/arrage_tasks?type=P&contact="+all_user.input_dom.val(),"arrangedate",arrage_subtitle_tmpl,"task","arrangedate asc", summary_arrage);
        var comming_week_task = new SWTimeline2(gettext("Comming One Week Planing"), "/looper/user/activites/arrage_tasks?type=C&contact="+all_user.input_dom.val(),"arrangedate",arrage_subtitle_tmpl,"task","arrangedate asc", summary_arrage);
        schedule_task = new SWTimeline2(gettext("Schedule Priority Tasks"), "/PMIS/task/schedule_priority/"+all_user.input_dom.val(),"planbdate",subtitle_tmpl,"task","planbdate asc");
        class1_task = new SWTimeline2(gettext("Class1 Tasks"), "/PMIS/task/classone_tasks/"+all_user.input_dom.val(),"planbdate",subtitle_tmpl,"task","planbdate asc");
        daily_pattern = new SWTimeline2(gettext("Default Daily Pattern"), "/PMIS/task/default_dialy_pattern/"+all_user.input_dom.val(),"planbdate","", daily_tmpl, "tasktid asc");
        $("#today_task").empty();
        $("#yesterday_task").empty();
        $("#comming_week_task").empty();
        $("#activites_schedule_priority").empty();
        $("#class1_task").empty();
        $("#daily_pattern").empty();
        $("#daily_pattern").append(daily_pattern.dom);        
        $("#today_task").append(today_task.dom);
        $("#yesterday_task").append(yesterday_task.dom);        
        $("#comming_week_task").append(comming_week_task.dom);            
        $("#activites_schedule_priority").append(schedule_task.dom);        
        $("#class1_task").append(class1_task.dom); 
        // 頂部顯示內容
        $(".activites_header .username").text($(".user_selected").attr('title'));
            init_task(pk);
        
    });
    function summary_arrage() {
        $(this.dom).find(".timeline.timeline2").each((index,item)=>{
            var arrage_tasks = $(item).children(".timeline-item").length;
            var finish_tasks = $(item).find(".timeline-item span[arrageprogress='C']").length + $(item).find(".timeline-item span[arrageprogress='F']").length;
            $(item).append(`
                <div class="d-flex flex-row cust_style" style="justify-content: space-evenly;align-items: center;border:1px dashed rgba(20, 20, 31, .12); border-radius: 0;">
                <div class="metric flex-row flex-lg-column flex-xl-row warn" style="border-right:1px dashed rgba(20, 20, 31, .12); border-radius: 0;text-align: center;flex-basis: 0;align-items: center;">                    
                <p class="metric-label mb-0 mr-2 mr-lg-0 mr-xl-2">`+gettext("Assign")+` </p>                    
                <h5 class="metric-value">${arrage_tasks}</h5>                                           
                </div>
                <div class="metric flex-row flex-lg-column flex-xl-row" style="text-align: center;flex-basis: 0;align-items: center;">                    
                <p class="metric-label mb-0 mr-2 mr-lg-0 mr-xl-2">`+gettext("Completed")+` </p>
                <h5 class="metric-value">${finish_tasks}</h5>                                            
                </div>
                </div>`);
        });
    }
    function summary_today_arrage() {
        var arrage_tasks = $(this.dom).find(".timeline.timeline2").children(".timeline-item").length;
        var finish_tasks = $(this.dom).find(".timeline.timeline2").find(".timeline-item span[progress='C']").length + $(item).find(".timeline-item span[progress='F']").length;
        $(this.dom).find(".timeline.timeline2").last().after(`
        <div class="d-flex flex-row cust_style" style="justify-content: space-evenly;align-items: center;border:1px dashed rgba(20, 20, 31, .12); border-radius: 0;">
        <div class="metric flex-row flex-lg-column flex-xl-row warn" style="border-right:1px dashed rgba(20, 20, 31, .12); border-radius: 0;text-align: center;flex-basis: 0;align-items: center;">                    
        <p class="metric-label mb-0 mr-2 mr-lg-0 mr-xl-2">`+gettext("Assign")+` </p>                    
        <h5 class="metric-value">${arrage_tasks}</h5>                                           
        </div>
        <div class="metric flex-row flex-lg-column flex-xl-row" style="text-align: center;flex-basis: 0;align-items: center;">                    
        <p class="metric-label mb-0 mr-2 mr-lg-0 mr-xl-2">`+gettext("Completed")+` </p>
        <h5 class="metric-value">${finish_tasks}</h5>                                            
        </div>
        </div>`);
    }    
    function update_tab_link() {
        $(".page-navs .nav-link").each((index, item)=>{
            var href = $(item).attr("href");
            if (href != "#") {
                if (href.indexOf("?") == -1)
                    $(item).attr("href", href + "?contact="+contact)
                else
                    $(item).attr("href", href + "&contact="+contact)
            }
        });
    }
    function update_task(self) {
        var pk = $(self).parent().find(".pk").text();
        init_task(pk);
    }

    $(".page-inner").on(
        {
            dblclick:function(){
                update_task(this);
            },
            longpress:function() {
                update_task(this);
            }
        },
        ".SWTimeline2 .caption"
    );
});