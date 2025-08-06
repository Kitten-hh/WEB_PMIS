
    function getQueryString(name) {  
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");  
        var r = window.location.search.substr(1).match(reg);  
        if (r != null) return decodeURI(r[2]);
        return '';  
    }

    var TecVM = new Vue({
        el : '#TechnicReport',
        data : {
            DetaliPlanner:{},
            inc_id:'',
        },
        methods :{
            //獲取DailyPlanner詳情
            GetDetailPlanner: function(){
                this.inc_id = getQueryString('pk');
                if (this.inc_id==''){this.CreatedefaultGoal()} 
                $.ajax({  
                    url: '/looper/DailyPlanner/update?pk=' + this.inc_id,
                    type: 'GET',
                    dataType: 'json',
                    cache: false,
                    success: function (json) {
                        if(json.status){
                            json.data['inputdate']=Date.parseExact(json.data['inputdate'], 'yyyyMMdd').toString("yyyy-MM-dd");
                            json.data['startdate'] = new Date(json.data['startdate']).toString('yyyy-MM-dd');
                            json.data['enddate'] = new Date(json.data['enddate']).toString('yyyy-MM-dd');
                            TecVM.DetaliPlanner=json.data;
                            TecVM.GetSolutionType(json.data['contact'],json.data['inputdate'],json.data['itemno']);
                        }
                    }
                })
            },

            //獲取SolutionType詳情
            GetSolutionType:function(contact,inputdate,itemno){
                $.ajax({      
                    url: "/looper/DailyPlanner/displaysolutionType",
                    type: "GET",
                    dataType: 'json',
                    data: { "contact": contact, "inputdate": Date.parse(inputdate).toString("yyyyMMdd"), "itemno": itemno },
                    cache: false,
                    success: function (json) {
                        if(json.status){
                            var goalnum = 1;
                            var oldType = ''
                            for(var i=0;i<json.data.length;i++){
                                if(json.data[i].mindmapsdesc==oldType){
                                    TecVM.CreateTechnic(goalnum-1,json.data[i],i+1);
                                }
                                if(json.data[i].mindmapsdesc!=oldType){
                                    TecVM.CreateGoal(goalnum,json.data[i],i+1);
                                    oldType = json.data[i].mindmapsdesc;
                                    goalnum = goalnum+1
                                }
                            }
                            if(json.data.length==0){TecVM.CreatedefaultGoal()}
                        }else{
                            TecVM.CreatedefaultGoal()
                        }
                    }
                })
            },

            //增加Goal輸入框
            CreateGoal: function(goalnum,solutionType,indexno){                
                var thehtml ='<div class="t'+goalnum+'" id="Goal'+goalnum+'">'+
                            '<div class="row">'+
                                '<div class="col-4 col-md-2 technical_title">'+ "Solution Type" +'<span class="badge badge-danger ml-2">For Goal '+goalnum+'</span>'+
                                '</div>'+
                                '<div class="col-8 col-md-10 technical_content">'+solutionType.mindmapsdesc+'</div>'+
                            '</div>'+
                            '<div class="row">'+
                                '<div class="col-4 col-md-2 technical_title">'+ "Technical" +'</div>'+
                                '<div class="col-8 col-md-10 technical_content">'+solutionType.Technicalcode+'</div>'+
                            '</div>'+
                            '<div class="row">'+
                                '<div class="col-4 col-md-2 technical_title">'+ "Condition" +'</div>'+
                                '<div class="col-8 col-md-10 technical_content condition_wrap'+indexno+'">'+

                                '</div>'+
                            '</div>'+
                            '<div class="row">'+
                                '<div class="col-3 technical_title">'+ "ETime" +'</div>'+
                                '<div class="col-3 technical_content">'+solutionType.etime+'</div>'+
                                '<div class="col-3 technical_title">'+ "FTime" +'</div>'+
                                '<div class="col-3 technical_content">'+solutionType.ftime+'</div>'+
                            '</div>'+
                            '<div class="row">'+
                                '<div class="col-4 col-md-2 technical_title">'+ "Remark" +'</div>'+
                                '<div class="col-8 col-md-10 technical_content">'+solutionType.remark+'</div>'+
                            '</div>'+
                        '</div>'
                $('#technical_body').append(thehtml)
                TecVM.AppendChebox(indexno,solutionType.condition, solutionType.tis)
            },
            
            //增加Technic輸入框
            CreateTechnic: function(goalnum,solutionType,indexno){
                var thehtml ='<div class="row">'+
                                '<div class="col-4 col-md-2 technical_title">Technical</div>'+
                                '<div class="col-8 col-md-10 technical_content">'+solutionType.Technicalcode+'</div>'+
                            '</div>'+
                            '<div class="row">'+
                                '<div class="col-4 col-md-2 technical_title">Condition</div>'+
                                '<div class="col-8 col-md-10 technical_content condition_wrap'+indexno+'">'+

                                '</div>'+
                            '</div>'+
                            '<div class="row">'+
                                '<div class="col-3 technical_title">ETime</div>'+
                                '<div class="col-3 technical_content">'+solutionType.etime+'</div>'+
                                '<div class="col-3 technical_title">FTime</div>'+
                                '<div class="col-3 technical_content">'+solutionType.ftime+'</div>'+
                            '</div>'+
                            '<div class="row">'+
                                '<div class="col-4 col-md-2 technical_title">Remark</div>'+
                                '<div class="col-8 col-md-10 technical_content">'+solutionType.remark+'</div>'+
                            '</div>'
                $('#Goal'+goalnum).append(thehtml)
                TecVM.AppendChebox(indexno,solutionType.condition, solutionType.tis)
            
            },

            //創建默認框
            CreatedefaultGoal: function(){
                var thehtml ='<div class="t1">'+
                            '<div class="row">'+
                                '<div class="col-4 col-md-2 technical_title">Solution Type<span class="badge badge-danger ml-2">For Goal 1</span>'+
                                '</div>'+
                                '<div class="col-8 col-md-10 technical_content"></div>'+
                            '</div>'+
                            '<div class="row">'+
                                '<div class="col-4 col-md-2 technical_title">Technical</div>'+
                                '<div class="col-8 col-md-10 technical_content"></div>'+
                            '</div>'+
                            '<div class="row">'+
                                '<div class="col-4 col-md-2 technical_title">Condition</div>'+
                                '<div class="col-8 col-md-10 technical_content condition_wrap1">'+

                                '</div>'+
                            '</div>'+
                            '<div class="row">'+
                                '<div class="col-3 technical_title">ETime</div>'+
                                '<div class="col-3 technical_content"></div>'+
                                '<div class="col-3 technical_title">FTime</div>'+
                                '<div class="col-3 technical_content"></div>'+
                            '</div>'+
                            '<div class="row">'+
                                '<div class="col-4 col-md-2 technical_title">Remark</div>'+
                                '<div class="col-8 col-md-10 technical_content"></div>'+
                            '</div>'+
                        '</div>'
                $('#technical_body').append(thehtml)
                this.AppendChebox(1,'')
            },

            //增加condition勾選框
            AppendChebox: function(indexno,condition, tis){
                var satisfactory = false
                var refinement = false
                var ambiguous = false
                switch(condition) {
                    case 'S':
                        satisfactory = true
                        break;
                    case 'R':
                        refinement = true
                        break;
                    case 'A':
                        ambiguous = true
                        break;
                }
                var condition1 = new SWRow();
                var isc1 = new SWCheckbox("satisfactory"+indexno, "Satisfactory",satisfactory);
                condition1.addComponent(isc1);
                var isc2 = new SWCheckbox("refinement"+indexno, "Refinement",refinement);
                condition1.addComponent(isc2);
                var isc3 = new SWCheckbox("ambiguous"+indexno, "Ambiguous",ambiguous);
                condition1.addComponent(isc3);
                var tis = new SWCombobox("tis"+indexno, "TIS", ["R","Y"], tis)
                tis.dom.addClass("technical-tis");
                tis.setHorizontalDisplay()
                condition1.dom.find(".col_right").prepend(tis.dom);   
                $(".condition_wrap"+indexno).append(condition1.dom);
            },

        },
        //實體創建成功後調用
        created:function(){
            this.GetDetailPlanner();   

        }
        
    });

    $(function () {
        var contact = new SWText("contact", "hidden", "contact", "");
        $("#from_div").prepend(contact.dom);
        var inputdate = new SWText("inputdate", "hidden", "inputdate", "");
        $("#from_div").prepend(inputdate.dom);
        var taskno = new SWText("taskno", "hidden", "taskno", "");
        $("#from_div").prepend(taskno.dom);
        var itemno = new SWText("itemno", "hidden", "itemno", "");
        $("#from_div").prepend(itemno.dom);
        var taskdescription = new SWText("taskdescription", "hidden", "taskdescription", "");
        $("#from_div").prepend(taskdescription.dom);
        var framespecification = new SWText("framespecification", "hidden", "framespecification", "");
        $("#from_div").prepend(framespecification.dom);
        var tasktype = new SWText("tasktype", "hidden", "tasktype", "");
        $("#from_div").prepend(tasktype.dom);
        var status = new SWText("status", "hidden", "status", "");
        $("#from_div").prepend(status.dom);
        var goalachieve = new SWText("goalachieve", "hidden", "goalachieve", "");
        $("#from_div").prepend(goalachieve.dom);
        
        var form = new SWBaseForm("#detailplanner_from_div");
        form.create_url = "/looper/DailyPlanner/create";
        form.update_url = "/looper/DailyPlanner/update?pk=[[pk]]";
        form.redirect_url="/looper/technic/technical_statement?pk="+ getQueryString('pk');
        form.init_data({});

        $(".technical_statement").parents(".app-main").css("padding-top","0");

    })
