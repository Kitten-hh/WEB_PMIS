$(function () {
    //用戶下拉框組件
    var user = get_username()
    var all_user = new SWCombobox('user',gettext('User'),window.CommonData.PartUserNames, user);
    all_user.dom.addClass("row");
    all_user.dom.find(".caption").css({"font-size":"16px","font-weight":"600"});
    all_user.dom.find("label").addClass("col-auto");
    all_user.dom.find("button").addClass("user_selected");
    all_user.dom.children(".control").css("width","100px");
    all_user.dom.children(".control").wrap('<div class="col-auto"></div>');
    $(".page-inner .userlist").append(all_user.dom);
    
    //獲取對應聯繫人優先級最高的5個Project及其任務
    function get_Projects(user){
        var url = '/en/looper/user/AnalyseProjects'
        if (user != undefined){
            url = url + "?contact="+user
        }else{
            url = url + '?contact=sing'
        }
        //移除原有的TopProject框
        $('#projectList').find('.top_wrap').remove()
        //獲取對應用戶前五的Project和其任務數據
        $.get(url, function(result){
            if (result.status){
                //Project必做任務數據
                var projectdata = result.data[0].projectdata
                //優先級前五的Project
                var projects = result.data[0].projects
                //優先級前五的Project的所有鍵
                var keyList = Object.keys(projects)
                // console.log(projectdata)
                // console.log(projects)
                keyList.forEach((strkey, index)=>{
                    //子標題
                    var child_info = `<p class="mb-0 timeline-date text-black font-weight-normal" inc_id="[[inc_id]]">[[pid]]-[[tid]]-[[taskid]]</p>`
                    //詳細內容
                    var daily_tmpl = `<p class="font-weight-bolder text-dark py-2 mb-0 caption"><i class="fas fa-bullhorn text-primary mr-2"></i>[[task]]</p>
                    <div class="mustFinish[[process]]">
                    <span class="text-purple"><i class="far fa-calendar-alt mr-2"></i>[[planbdate]]</span>
                    <span class="ml-3 text-purple"><i class="far fa-list-alt mr-2"></i>[[schpriority]]</span>
                    <span class="ml-3 text-purple"><i class="far fa-file mr-2"></i>[[progress]]</span>
                    </div>`
                    var title_tmpl = `<div class="d-flex justify-content-between align-items-center">
                    <h4 class="card-title mb-0">[[title]]</h4>
                    <div class="dropdown">
                        <button type="button" class="btn btn-sm btn-icon btn-light" data-toggle="dropdown" aria-haspopup="true"
                            aria-expanded="false"><i class="fas fa-filter"></i></button>
                        <div class="dropdown-menu dropdown-menu-right task_filter">
                            <div class="dropdown-arrow"></div>
                            <a href="#" class="dropdown-item" name="mf">Must Finish</a> 
                            <a href="#" class="dropdown-item" name="mh">Must Have</a> 
                            <a href="#" class="dropdown-item" name="all">All</a> 
                        </div>
                        </div>
                    </div>`
                    var sindex = index+1
                    var strid = 'top'+sindex
                    //SWTimeline2組件的容器
                    var strhtml = `<div class="col-12 col-xl-6 col-xxl-4 top_wrap" id="[[id]]"></div>`.replace('[[id]]',strid);
                    $("#projectList").append(strhtml);
                    var top = new SWTimeline2('G'+sindex+'.'+projects[strkey].desc, projectdata[strkey], "planbdate", child_info, daily_tmpl, "tasktid asc");
                    top.dom.children(".card-header").html(title_tmpl.render({title:'G'+sindex+'.'+projects[strkey].desc}));
                    $("#"+strid).append(top.dom);
                    //SWTimeline2組件下的統計數據顯示模塊
                    var analysehtml =`
                            <div id="summary_wrap" class="card-body pt-0">
                            <h4 class="card-title sum_title pb-2 mb-0">
                            <i class="fas fa-thumbtack mr-2"></i>Summary </h4>
                            <div class="d-flex justify-content-between align-items-center mb-2 pl-2 pt-2">
                                <div class="text-left left-date-title" data-toggle="tooltip" data-placement="top"
                                    data-original-title="Actual completion time">
                                    <span class="sr-only">Actual completion time</span>
                                    <i class="far fa-calendar-check text-dark mr-2"></i>[[planedate]]</div>
                                <div class="text-dark"><strong class="text-primary">[[Completed_Qty]]</strong> / <span>[[All_Qty]]</span></div>
                            </div>
                            <div class="d-flex flex-column pl-2">
                                <div class="row justify-content-start mb-2">
                                    <div class="col-auto">
                                        <span class="oi oi-media-record text-au mark_icon"></span>
                                        Actual Uncomplete (10)
                                    </div>
                                    <div class="col-auto">
                                        <span class="oi oi-media-record text-complete mark_icon"></span>
                                        Completed (8)
                                    </div>
                                    <div class="col-auto">
                                        <span class="oi oi-media-record text-uc mark_icon"></span>
                                        Unassign Complete (6)
                                    </div>
                                </div>
                                <div class="progress progress-sm mb-2">
                                    <div class="progress-bar bg-au progress-bar-striped progress-bar-animated" role="progressbar" style="width: 40%" aria-valuenow="40"
                                        aria-valuemin="0" aria-valuemax="100"></div>
                                    <div class="progress-bar bg-complete progress-bar-striped progress-bar-animated" role="progressbar" style="width: 30%" aria-valuenow="30"
                                        aria-valuemin="0" aria-valuemax="100"></div>
                                    <div class="progress-bar bg-uc progress-bar-striped progress-bar-animated" role="progressbar" style="width: 20%" aria-valuenow="20"
                                        aria-valuemin="0" aria-valuemax="100"></div>
                                </div>
                            </div>
                        </div>`
                    //對統計數據顯示模塊內容進行替換    
                    if(projectdata[strkey].length>0){
                        analysehtml = analysehtml.replace("[[Completed_Qty]]",projects[strkey].Completed_Qty).replace("[[All_Qty]]",projects[strkey].All_Qty)
                        .replace('[[planedate]]',new Date(projectdata[strkey][projectdata[strkey].length-1].planedate).toString("yyyy-MM-dd"))
                    }else{
                        analysehtml = analysehtml.replace("[[Completed_Qty]]",'0').replace("[[All_Qty]]",'0').replace('[[planedate]]','')
                    }
                    $("#"+strid).find(".SWTimeline2").append(analysehtml)
                })
                
                $('.mustFinishF').parent().parent().parent().addClass('priorityTask')
                $(".top5_mustHave").find(".SWTimeline2 span.tile").removeClass("bg-primary");
                $(".top5_mustHave").find(".SWTimeline2 span.tile i").remove();
                $(".top5_mustHave").find("span.int").removeClass("d-none");
            }
        });  
    }
    //獲取登陸者優先級最高的5個Project及其任務
    get_Projects(user)
    //User改變方法
    $("select[name='user']").on("change", function(){
        get_Projects($("select[name='user']").val())
    })
    //任務雙擊事件顯示該任務詳情
    $('#projectList').on('dblclick','.timeline-item',function(){
        var inc_id = $(this).find('.font-weight-normal').attr('inc_id')
        init_task(inc_id);
    })
});