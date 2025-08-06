$(function(){
    var url = "/PMIS/goalmaster/show_treelist/{0}".format(getParamFromUrl("pk"));
    var calendar = new SWCalendar("#goal_calendar");
    calendar.events_url = url;
    calendar.start_field = "PlanBDate";
    calendar.end_field = "PlanEDate";
    calendar.title_field = "Task";
    calendar.extended_fields = ['INC_ID']
    calendar.eventClick = function(info) {
        var pk = info.event.extendedProps['INC_ID'];
        init_task(pk);        
    }
    calendar.init();
});