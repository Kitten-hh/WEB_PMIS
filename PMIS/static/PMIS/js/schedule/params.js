var Vue_Form = SimpleTemplateNoBar_Vue.extend({
    data() {
        return {
            sys_params:init_sys_param,
            curr_user_params:init_curr_user_params,
            next_user_params:init_next_user_params,
            user_list:user_list,
            cur_user:cur_user,
            periods:periods
        }
    },
    watch: {
        "MasterView_CurData.from_field": function(val, oldVal){
            this.MasterView_CurData.hour = this.computed_hour()
        },
        "MasterView_CurData.to": function(val, oldVal){
            this.MasterView_CurData.hour = this.computed_hour()
        },
        cur_user:function(val, oldVal){
            window.location.href = '/PMIS/schparams?user=' + val
        }
    },
    methods : {
        init_datatable() {
            var tables = datatableview.initializeWithPromise($('.datatable'),SingleDataTableStyle, {
                dom: `<'row ml-0 mr-0 justify-content-between'<'text-left'<"NewRecord">><'align-middle text-right'f>>
                 <'row'<'col-sm-12'tr>>`
            });
            return tables;
        },
        initBindEvent() {
            var self = this;
            this.$super(Vue_Form, this).initBindEvent();
              $('#period_dlg .builder-plugins').queryBuilder({
                plugins: [
                  'filter-description',
                  'unique-filter',
                  'bt-tooltip-errors',
                  'bt-selectpicker',
                  'bt-checkbox',
                  'not-group'
                ],
              
                filters: [
                  {
                    'id': 'TypeNo', 
                    'type': 'integer', 
                    'field': 'TypeNo', 
                    'label': 'TypeNo', 
                    'input': 'checkbox',
                    values: type_list,
                    'operators': ['in', 'not_in', 'equal', 'not_equal']}]
              });          
              $("#period_dlg .btn_ok").on('click', function(){
                  var result = $('#period_dlg .builder-plugins').queryBuilder('getSQL');
                  self.MasterView_CurData.logic = result.sql;
                  $("#period_dlg").modal('hide')
              });
              $("#type_dlg .builder-plugins").queryBuilder({
                plugins: [
                  'filter-description',
                  'unique-filter',
                  'bt-tooltip-errors',
                  'bt-selectpicker',
                  'bt-checkbox',
                  'not-group'
                ],
                filters: [{
                    'id': 'Hoperation',
                    'type': 'string',
                    'field': 'Hoperation',
                    'label': '操作',
                    'operators': ['is_null', 'is_not_null', 'equal', 'not_equal', 'less', 'less_or_equal', 'greater', 'greater_or_equal', 'between', 'not_between', 'begins_with', 'not_begins_with', 'ends_with', 'not_ends_with', 'in', 'not_in', 'is_empty', 'is_not_empty', 'contains', 'not_contains']
                }, {
                    'id': 'UDF09',
                    'type': 'string',
                    'field': 'UDF09',
                    'label': '上報人',
                    'operators': ['is_null', 'is_not_null', 'equal', 'not_equal', 'less', 'less_or_equal', 'greater', 'greater_or_equal', 'between', 'not_between', 'begins_with', 'not_begins_with', 'ends_with', 'not_ends_with', 'in', 'not_in', 'is_empty', 'is_not_empty', 'contains', 'not_contains']
                }, {
                    'id': 'CycleTask',
                    'type': 'string',
                    'field': 'CycleTask',
                    'label': '循環任務',
                    'operators': ['is_null', 'is_not_null', 'equal', 'not_equal', 'less', 'less_or_equal', 'greater', 'greater_or_equal', 'between', 'not_between', 'begins_with', 'not_begins_with', 'ends_with', 'not_ends_with', 'in', 'not_in', 'is_empty', 'is_not_empty', 'contains', 'not_contains']
                }, {
                    'id': 'DayJob',
                    'type': 'string',
                    'field': 'DayJob',
                    'label': 'DayJob',
                    'operators': ['is_null', 'is_not_null', 'equal', 'not_equal', 'less', 'less_or_equal', 'greater', 'greater_or_equal', 'between', 'not_between', 'begins_with', 'not_begins_with', 'ends_with', 'not_ends_with', 'in', 'not_in', 'is_empty', 'is_not_empty', 'contains', 'not_contains']
                }, {
                    'id': 'RealTaskType',
                    'type': 'string',
                    'field': 'RealTaskType',
                    'label': 'TaskCategory',
                    'operators': ['is_null', 'is_not_null', 'equal', 'not_equal', 'less', 'less_or_equal', 'greater', 'greater_or_equal', 'between', 'not_between', 'begins_with', 'not_begins_with', 'ends_with', 'not_ends_with', 'in', 'not_in', 'is_empty', 'is_not_empty', 'contains', 'not_contains']
                }, {
                    'id': 'Progress',
                    'type': 'string',
                    'field': 'Progress',
                    'label': '進度',
                    'operators': ['is_null', 'is_not_null', 'equal', 'not_equal', 'less', 'less_or_equal', 'greater', 'greater_or_equal', 'between', 'not_between', 'begins_with', 'not_begins_with', 'ends_with', 'not_ends_with', 'in', 'not_in', 'is_empty', 'is_not_empty', 'contains', 'not_contains']
                }, {
                    'id': 'PlanEDate',
                    'type': 'date',
                    'field': 'PlanEDate',
                    'label': '計畫結束',
                    validation: {
                        format: 'YYYY/MM/DD'
                    },
                    plugin: 'datepicker',
                    plugin_config: {
                        format: 'yyyy/mm/dd',
                        todayBtn: 'linked',
                        todayHighlight: true,
                        defaultViewDate:new Date(2000,06,01),
                        autoclose: true
                    },                    
                    'operators': ['is_null', 'is_not_null', 'equal', 'not_equal', 'less', 'less_or_equal', 'greater', 'greater_or_equal', 'between', 'not_between']
                },{
                    'id':'Is_Normal',
                    'type':'integer',
                    'label':'Is_Normal',
                    'input':'radio',
                    values:{
                        1:'Yes',
                        0:'No'
                    },
                    'operator':['equal']
                }]
              });
              $("#type_dlg .btn_ok").on('click', function(){
                var result = $('#type_dlg .builder-plugins').queryBuilder('getSQL');
                self.SchType_CurData.logic = result.sql;
                $("#type_dlg").modal('hide')
            });
        },
        computed_hour() {
            if (_.isEmpty(this.MasterView_CurData.from_field) || _.isEmpty(this.MasterView_CurData.to))
                return undefined
            else {
                start = this.MasterView_CurData.from_field.split(":");
                end = this.MasterView_CurData.to.split(":");
                var startDate = new Date(0, 0, 0, start[0], start[1], 0);
                var endDate = new Date(0, 0, 0, end[0], end[1], 0);
                return _.round(dateFns.differenceInMinutes(endDate, startDate)/60,2)
            }
        },
        save_params() {
            var self = this;
            data = {
                sys_params:JSON.stringify(this.sys_params),
                curr_user_params:JSON.stringify(this.curr_user_params),
                user:self.cur_user
            }
            $.ajax({
                url:"save_params",
                type:"POST",
                data:data,
                beforeSend: function(request){
                    request.setRequestHeader("X-CSRFToken", self.getCookie('csrftoken'));
                },                
                success:function(result) {
                    if (result.status) {
                        alert("保存成功!");
                        window.location.reload(true);
                    }
                    else
                        alert("保存失敗!");
                }
            })
        }
    }
})

var Form = new Vue_Form().$mount("#Main_Page");