var TableClass = function () {

    var displayBothTable = function (options) {
        if (!document.getElementById(options.elementId)) {
            return;
        }

        top.window.IndexClass.initColumns(options).then((columns) => {
            top.window.IndexClass.getDataFromRestAPI(options).then((data) => {
                var datatable = $("#"+options.elementId).KDatatable({
                    // datasource definition
                    data: {
                        type: 'local',
                        source: data,
                        pageSize: 10,
                    },

                    layout: {
                        theme: 'default',
                        class: '',
                        scroll: true,
                        height: 350,
                        footer: false
                    },
                    sortable: true,

                    filterable: false,

                    pagination: true,

                    search: {
                        input: $('#generalSearch')
                    },

                    rows: {
                        // disable responsive auto hide columns in row for horizontal scrollbar
                        autoHide: false
                    },
                    columns:columns
                });
            });
        });
    }

    return {
            init: function () {
                var options = {
                    elementId: "k_task_search",
                    url: "http://www.cyber-access.com:3200/PMSService/M_PMS/V_Task/_search",
                    query: {
                        "query": "[['SubProjectID','<>','00319'],'and', ['Progress','=','T'], 'and', ['PlanBDate','>=','20191001'],'and',['PlanEDate','<=','20191231'],'and',['!', ['Pid','startswith','C']]]",
                        "source":["TaskNo","Task","Contact","Progress","PlanBDate","PlanEDate"]
                    },
                    columns:{
                        TaskNo:{title:"任務編號",width:"120",textAlign:"left"},
                        Task:{width:400, textAlign:"left"}
                    }
                }    
                
                var options2 = {
                    elementId: "k_top_product_search",                    
                    url: "http://www.cyber-access.com:3200/VCAsiaSZService/VCAsia_db/V_Sales_Top_Product/_search",
                	query:{"query": "['PartNo','<>',]"},
                    columns:{
                        PartNo:{title:"產品編號",width:"120",textAlign:"left"},
                        Orders:{title:"數量",width:"60",textAlign:"left"},
                        Description:{title:"描述",width:"300",textAlign:"left"},
                        CustPn:{title:"客號",width:"150",textAlign:"left"},
                        Bdate:{title:"早期下單日期",width:"100",textAlign:"left"},
                        Edate:{title:"最後下單日期",width:"100",textAlign:"left"}
                    }
                }
                displayBothTable(options);
                displayBothTable(options2);
            }
        }
    }();

    jQuery(document).ready(function () {
        TableClass.init();
    });