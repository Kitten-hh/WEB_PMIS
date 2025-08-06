<template>
    <div id="app" class="analysis_page page-inner">
        <div class="subheader dropdown">                 
            <div class="el-example task_search_tools">   
                <button class="btn btn-primary font-weight-bolder" @click="search('Bonus')"><i class="fa fa-search mr-2 d-none d-sm-inline"></i>{{$t("Search")}}</button>                
                <button class="btn btn-hover-text-primary font-weight-bolder btn-secondary" @click="bonusAnalysis('yesterday')">
                    <span class="d-block d-md-none">{{ $t("YDay") }}</span>
                    <span class="d-none d-md-inline">{{ $t("Yesterday") }}</span>
                </button>
                <button class="btn btn-hover-text-primary font-weight-bolder btn-secondary" @click="bonusAnalysis('today')">
                    <span class="d-block d-md-none">{{ $t("TDay") }}</span>
                    <span class="d-none d-md-inline">{{ $t("Today") }}</span>
                </button>  
                <button class="btn btn-hover-text-primary font-weight-bolder btn-secondary"
                    @click="bonusAnalysis('lastweek')">
                    <span class="d-block d-md-none">{{ $t("LW") }}</span>
                    <span class="d-none d-md-inline">{{ $t("Last Week") }}</span>
                </button> 
                <button class="btn btn-hover-text-primary font-weight-bolder btn-secondary"
                    @click="bonusAnalysis('week')">
                    <span class="d-block d-md-none">{{ $t("W") }}</span>
                    <span class="d-none d-md-inline">{{ $t("This Week") }}</span>
                </button>  
                <button class="btn btn-secondary btn-hover-text-primary font-weight-bolder d-none d-md-inline-block"
                    @click="bonusAnalysis('lastmonth')">{{$t("Last Month")}}
                </button>  
                <button class="btn btn-secondary btn-hover-text-primary font-weight-bolder d-none d-md-inline-block"
                    @click="bonusAnalysis('month')">{{$t("This Month")}}
                </button>  
                <button class="btn btn-secondary btn-hover-text-primary font-weight-bolder d-none d-md-inline-block"
                    @click="bonusAnalysis('lastquarter')">{{$t("Last Quarter")}}
                </button>  
                <button class="btn btn-secondary btn-hover-text-primary font-weight-bolder d-none d-md-inline-block"
                    @click="bonusAnalysis('quarter')">{{$t("This Quarter")}}
                </button>   
                <button class="btn btn-secondary btn-hover-text-primary font-weight-bolder d-none d-md-inline-block" @click="searchSummary">{{$t("Summary")}}
                </button>  
                <button class="btn btn-secondary btn-hover-text-primary font-weight-bolder d-none d-md-inline-block"
                    @click="refreshAonusAnalysis">{{$t("Refresh")}}
                </button> 


                <div class="form-check d-none">
                    <input class="form-check-input" type="checkbox" checked id="cb_calSat"/>
                    <label class="form-check-label" for="cb_calSat">
                        計算周六
                    </label>
                </div>
            </div>   
        </div>
        <div class="modal fade" id="editModal" tabindex="-1" role="dialog" aria-labelledby="editModalTitle"
            style="display: none;" aria-hidden="true">
            <div id="form-wapper"> <!--form將生成到這個div中，需要設置id-->
            </div>
        </div>


        <div class="modal fade tableModal" id="tasktypeModal" tabindex="-1" role="dialog" aria-labelledby="tasktypeModalTitle"
            aria-hidden="true">
            <div class="modal-dialog modal-dialog-scrollable modal-xl" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalCenterTitle">{{$t("Task Type Analysis")}}</h5>
                        <button type="button" class="close text-dark" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <!--Task Type Datatable-->
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary btn-cancel" data-dismiss="modal">{{$t("Close")}}</button>                    
                    </div>
                </div>
            </div>
        </div>   
        <div style="margin-top: 12px;">   
            <div class="row">
                <div class="col-12 col-lg-6 col-xl-5 col-xxl-3 mb-4 mb-sm-0 d-none d-md-block">
                    <!--begin::Card-->
                    <div class="wrapper_test" id="card_para">
                        <div class="col-12 px-0">
                            <h3 class="text-dark-75 trm-title-with-divider mb-0">
                                {{$t("Bonus Parameter")}}
                                <label name="lb_contact" class="m-0 text-warning"></label>
                                <span class="m-0"></span>
                            </h3>
                        </div>
                        <div class="card-body px-0 p-sm-3">
                            <div class="row pc_parameter px-0">
                                <div class="col-12 mb-3">
                                    <div class="box boxs">
                                        <div class="cs_content flex-row-fluid">
                                            <h4 class="flex-grow-1 text-dark">{{$t("Budget Allowance")}} %</h4>
                                            <!-- <p id="BudgetAllowance" class="mb-0 text-warning text-hover-danger">0</p> -->
                                            <input class="textEdit form-control" type="text" id="BudgetAllowance" v-model="BudgetAllowance" style="width: 40px;" @blur="budgetAllowance_blur">
                                        </div>
                                        <div class="cs_content flex-row-fluid">
                                            <h4 class="flex-grow-1 text-dark">{{$t("Price Per Score")}} ¥</h4>
                                            <input class="textEdit form-control" type="text" id="UnitPrice" v-model="UnitPrice" style="width: 40px;" @blur="unitprice_blur">                                              
                                        </div>                                        
                                    </div>
                                </div>

                                <div class="col-12 mb-3">
                                    <div class="box boxs">
                                        <div class="cs_content flex-row-fluid">
                                            <h4 class="flex-grow-1 text-dark">{{$t("Management S")}}</h4>
                                            <p id="ManagementS" class="mb-0 text-warning text-hover-danger">{{ManagementS}}</p>
                                        </div>
                                        <div class="cs_content flex-row-fluid">
                                            <h4 class="flex-grow-1 text-dark">{{$t("Performance. S")}}</h4>
                                            <p id="PerformanceS" class="mb-0 text-warning text-hover-danger">{{PerformanceS}}</p>
                                        </div>
                                        <div class="cs_content flex-row-fluid">
                                            <h4 class="flex-grow-1 text-dark">{{$t("Working Day")}}</h4>
                                            <p id="WorkingDay" class="mb-0 text-warning text-hover-danger">{{WorkingDay}}</p>
                                        </div>
                                        <div class="cs_content flex-row-fluid">
                                            <h4 class="flex-grow-1 text-dark">{{$t("Quarter Working Day")}}</h4>
                                            <p id="QuarterWorkingDay" class="mb-0 text-warning text-hover-danger">{{QuarterWorkingDay}}</p>
                                        </div>
                                        <div class="cs_content flex-row-fluid">
                                            <h4 class="flex-grow-1 text-dark">{{$t("Perfect Scoring")}}</h4>
                                            <p id="PerfectScoring" class="mb-0 text-warning text-hover-danger">{{PerfectScoring}}</p>
                                        </div>
                                    </div>
                                </div>
                            
                                <div class="col-12 mb-3">
                                    <div class="box flex-row inner-box">
                                        <div class="cs_content flex-row-fluid">
                                            <h4 class="flex-grow-1 text-dark">{{$t("Ratio of M:S:P")}}</h4>
                                            <div class="d-flex align-items-center">
                                                <!-- <p id="RatioOFM" class="mb-0 text-warning text-hover-danger">0</p> -->
                                                <input class="textEdit form-control" type="text" id="RatioOFM" v-model="RatioOFM" style="width: 40px;" @blur="ratioOFM_blur">
                                                <span class="mx-2">:</span>
                                                <!-- <p id="RatioOFS" class="mb-0 text-warning text-hover-danger">0</p> -->
                                                <input class="textEdit form-control" type="text" id="RatioOFS" v-model="RatioOFS" style="width: 40px;" @blur="ratioOFS_blur" disabled>
                                                <span class="mx-2">:</span>
                                                <!-- <p id="RatioOFP" class="mb-0 text-warning text-hover-danger">0</p> -->
                                                <input class="textEdit form-control" type="text" id="RatioOFP" v-model="RatioOFP" style="width: 40px;" @blur="ratioOFP_blur">
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="col-12 mb-3">
                                    <div class="box boxs">
                                        <div class="cs_content flex-row-fluid">
                                            <h4 class="flex-grow-1 text-dark">{{$t("Mag")}} %</h4>
                                            <!-- <p id="ManagementRatio" class="mb-0 text-warning text-hover-danger">0</p> -->
                                            <input class="textEdit form-control" type="text" id="ManagementRatio" v-model="ManagementRatio" style="width: 40px;" @blur="managementRatio_blur">
                                        </div>
                                        <div class="cs_content flex-row-fluid">
                                            <h4 class="flex-grow-1 text-dark">{{$t("Per")}} %</h4>
                                            <!-- <p id="PerformanaceRatio" class="mb-0 text-warning text-hover-danger">0</p> -->
                                            <input class="textEdit form-control" type="text" id="PerformanaceRatio" v-model="PerformanaceRatio" style="width: 40px;" @blur="performanaceRatio_blur">
                                        </div>
                                    </div>
                                </div>

                                <div class="col-12 mb-3 d-none">
                                    <div class="box flex-row inner-box" style="height: 100%;">
                                        <div class="cs_content flex-row-fluid">
                                            <h4 class="flex-grow-1 text-dark">{{$t("Salary")}} %</h4>
                                            <p id="Salary" class="mb-0 text-warning text-hover-danger" style="visibility: hidden;">0</p>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-12">
                                    <div class="box flex-row inner-box" style="height: 100%;">
                                        <div class="cs_content flex-row-fluid" style="justify-content: flex-end;">
                                            <button id="btn_saveParam" class="btn btn-subtle-primary mr-2" 
                                            style="font-weight: 900;font-size: larger;" @click="saveParam">{{$t("Save")}}</button>
                                            <button id="btn_restore" class="btn btn-subtle-primary" 
                                            style="font-weight: 900;font-size: larger;" @click="restore">{{$t("Cancel")}}</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!--end::Card--> 
                </div>
                <div class="col-12 col-lg-6 col-xl-7 col-xxl-9">
                    <div class="card card-custom gutter-b" style="display:none">
                            <div class="card-header">
                                <h3 class="card-title"><label name="lb_contact"></label><label>{{$t("Task Type Analysis")}}</label></h3>
                            </div>
                            <div class="card-body">
                                <div id="db_tasktype"></div>
                            </div>
                    </div>
                    <div id="search_card_accordion" class="card-expansion mb-2" ref="search_card_accordion">
                        <div id="query_wrapper" class="card card-custom gutter-b task_card bg-gray-100 card-expansion-item expanded" data-card="true">
                            <div class="card-header border-0 d-flex flex-wrap py-0">
                                <button
                                    :class="['btn btn-reset', isExpend ? 'd-none' : '']"
                                    data-toggle="collapse"
                                    data-target="#search_card_collapse"
                                    aria-expanded="true"
                                    aria-controls="search_card_collapse"
                                >
                                    <span class="collapse-indicator mr-2">
                                        <i class="fa fa-fw fa-chevron-down"></i>
                                    </span>                                                                   
                                </button>
                                <ul class="nav nav-tabs">
                                    <li class="nav-item">
                                        <a
                                            class="nav-link active"
                                            id="tab_tasks"
                                            data-toggle="tab"
                                            href="#content_tasks"
                                        >
                                            <h3 class="card-title"> 
                                                <!-- <label name="lb_contact"></label> -->
                                                <label class="text-dark-75 trm-title-with-divider mb-0">{{$t("Tasks")}}</label>     
                                            </h3> 
                                        </a>
                                    </li>
                                    <li class="nav-item" id="tab_Deductions">
                                        <a
                                            class="nav-link"
                                            id="tab_deduction"
                                            data-toggle="tab"
                                            ref="tab_deduction"
                                            href="#content_deduction"
                                        >
                                            <h3 class="card-title"> 
                                                <!-- <label name="lb_contact"></label> -->
                                                <label class="text-dark-75 trm-title-with-divider mb-0">{{$t("Deductions")}}</label>     
                                            </h3> 
                                        </a>
                                    </li>  
                                    <li class="nav-item" id="tab_TaskType">
                                        <a
                                            class="nav-link"
                                            id="tab_tasktype"
                                            data-toggle="tab"
                                            href="#content_tasktype"
                                        >
                                            <h3 class="card-title"> 
                                                <label class="text-dark-75 trm-title-with-divider mb-0">{{$t("Task Type")}}</label>     
                                            </h3> 
                                        </a>
                                    </li>               
                                </ul>
                                <div class="card-toolbar ml-auto ml-sm-0 ml-lg-auto">  
                                    <label id="lb_condition" class="mr-2" style="display:none"></label>
                                    <button id="btn_aibox" class="btn btn-primary font-weight-bolder font-size-sm px-2 mr-2" style="display:none" @click="AIOpen">{{$t("AI Box")}}
                                    </button> 
                                    <button id="btn_reportDesign" class="btn btn-primary font-weight-bolder font-size-sm px-2 mr-2" style="display:none" @click="design()">{{$t("Design")}}
                                    </button> 
                                    <button id="btn_reportPreview" class="btn btn-primary font-weight-bolder font-size-sm px-2 mr-2" style="display:none" @click="preview()">{{$t("Preview")}}
                                    </button> 
                                    <button id="btn_auditScore" class="btn btn-primary font-weight-bolder font-size-sm px-2 mr-2" style="display:none" @click="auditScore('Y')">{{$t("Post")}}
                                    </button>  
                                    <button id="btn_unauditScore" class="btn btn-primary font-weight-bolder font-size-sm px-2 mr-2" style="display:none" @click="auditScore('R')">{{$t("UnPost")}}
                                    </button>
                                    <button id="btn_expand" type="button" class="btn btn-secondary text-dark" data-toggle="task-expander" style="display:none" @click="taskExpander($event)">
                                        <i :class="[isExpend ? 'fas fa-compress-alt' : 'fas fa-expand-alt']"></i>
                                    </button>
                                     <!-- <button class="btn btn-secondary btn-hover-text-primary font-weight-bolder d-none d-md-inline-block"
                                        @click="AIOpen">{{$t("AI Box")}}
                                    </button>  -->
                                </div>
                            </div>       
                            <div id="search_card_collapse" class="collapse show" aria-labelledby="heading" data-parent="#search_card_accordion">  
                                <div class="tab-content pt-1">
                                    <div
                                        class="tab-pane fade show active"
                                        id="content_tasks"
                                        role="tabpanel"
                                    >
                                        <div class="card card-reflow mb-0">
                                            <div class="card-body no-drag grid-item-body py-0 pb-2">                           
                                                <LPDataTable
                                                    :paging_inline="true"
                                                    :paging="false"
                                                    :columns="taskColumns"
                                                    :datasource="[]"            
                                                    :custom_options="task_custom_options"
                                                    :searching="false"
                                                    :firstColSelected="true"
                                                    ref="dt_task"    
                                                    @on_dbclick="showTaskDetail"                       
                                                />                   
                                            </div>
                                        </div>
                                    </div>
                                    <div
                                        class="tab-pane fade"
                                        id="content_deduction"
                                        role="tabpanel"
                                    >
                                        <div class="card card-reflow mb-0">                                             
                                            <div class="form-inline task_search_tools mt-2 px-3">   
                                                <button class="btn btn-sm btn-primary font-weight-bolder mr-2" @click="search">
                                                    <i class="fa fa-search"></i>
                                                </button>
                                                <button id="btnNew" ref="btnNew" type="button" class="btn btn-sm btn-primary" @click="newDeductionItem">
                                                    <i class="fa fa-plus"></i>
                                                </button>
                                            </div>  
                                            <div class="card-body no-drag grid-item-body py-0 pb-2">          
                                                <LPDataTable
                                                    id="dt_userdeduction"
                                                    :paging_inline="true"
                                                    :paging="false"
                                                    :columns="userDeductionColumns"
                                                    datasource="/bonus/userdeduction/datatable"
                                                    :custom_options="userDeduction_custom_options"
                                                    :custom_params_fun="userDeduction_params_fun"
                                                    :searching="false"
                                                    :show_footer="true"
                                                    ref="dt_userdeduction"
                                                />
                                            </div>
                                        </div>
                                    </div>
                                    <div
                                        class="tab-pane fade"
                                        id="content_tasktype"
                                        role="tabpanel"
                                    >
                                        <div class="card card-reflow mb-0">                                             
                                            <div class="card-body no-drag grid-item-body py-0 pb-2">          
                                                <LPDataTable
                                                    :paging_inline="true"
                                                    :paging="false"
                                                    :columns="taskTypeColumns"
                                                    :datasource="[]"            
                                                    :custom_options="tasktype_custom_options"
                                                    :searching="false"
                                                    :show_footer="true"
                                                    ref="dt_tasktype"                           
                                                />
                                            </div>
                                        </div>
                                    </div>
                                </div>  
                            </div>
                        </div>
                    </div>
                    <!--begin::Card-->
                    <div id="card_result">
                        <div class="pc_parameter">
                            <div class="card-deck-xxl">
                                <div class="d-none d-md-flex flex-column">
                                    <h3 class="text-dark-75 trm-title-with-divider mt-2">
                                        {{$t("Bonus Analysis Result")}}
                                        <!-- <label name="lb_contact" class="m-0 text-warning"></label> -->
                                        <span></span>
                                    </h3>
                                    <div class="inner-box ad-info-card bg-gray-100">
                                        <div class="card-body p-0">
                                            <div class="table-responsive">
                                                <table class="table table-hover score_wrap">
                                                    <thead class="thead-">
                                                        <tr>
                                                            <th></th>
                                                            <th class="text-primary"> 
                                                                <div class="th_wrap light-primary">
                                                                    <span class="nav-icon d-none d-sm-block d-md-none d-lg-block mr-2"><i class="fas fa-star"></i></span>
                                                                    <span class="nav-text">{{$t("Score")}}</span>
                                                                </div>
                                                            </th>
                                                            <th class="text-danger">                                                    
                                                                <div class="th_wrap light-danger">
                                                                    <span class="nav-icon d-none d-sm-block d-md-none d-lg-block mr-2"><i class="fas fa-chart-line"></i></span>
                                                                    <span class="nav-text d-none d-xxxsl-block">{{$t("Lookup Score")}}</span>
                                                                    <span class="nav-text d-block d-xxxsl-none">{{$t("LScore")}}</span>
                                                                </div>
                                                            </th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        <tr>
                                                            <td> <span>{{$t("Total Tasks Score")}}</span> </td>
                                                            <td class="text-center text-primary"> <strong id="Score">{{Score}}</strong> </td>
                                                            <td class="text-center text-danger"> <strong id="LookupScore">{{LookupScore}}</strong> </td>
                                                        </tr>
                                                        <tr>
                                                            <td> <span>{{$t("Total Management Score")}}</span> </td>
                                                            <td class="text-center text-primary"> <strong id="ManagementScore">{{ManagementScore}}</strong> </td>
                                                            <td class="text-center text-danger"> <strong id="ManagementLookupScore">{{ManagementLookupScore}}</strong> </td>
                                                        </tr>                                                    
                                                        <tr>
                                                            <td> <span>{{$t("Final Score For The Quarter")}}</span> </td>
                                                            <td class="text-center text-primary"> <strong id="QuarterScore">{{QuarterScore}}</strong> </td>
                                                            <td class="text-center text-danger"> <strong id="QuarterLookupScore">{{QuarterLookupScore}}</strong> </td>
                                                        </tr>
                                                        <tr>
                                                            <td> <span>{{$t("Bonus Score")}}</span> </td>
                                                            <td class="text-center text-primary"> <strong id="ScoreBonus">{{ScoreBonus}}</strong> </td>
                                                            <td class="text-center text-danger"> <strong id="LookupScoreBonus">{{LookupScoreBonus}}</strong> </td>
                                                        </tr>
                                                        <!--
                                                        <tr>
                                                            <td> <span>S Actual Quarter</span> </td>
                                                            <td class="text-center text-primary"> <strong id="ScoreActualQuarter">{{ScoreActualQuarter}}</strong> </td>
                                                            <td class="text-center text-danger"> <strong id="LookupScoreActualQuarter">{{LookupScoreActualQuarter}}</strong> </td>
                                                        </tr>
                                                        -->
                                                        <tr>
                                                            <td> <span>{{$t("Actual Bonus $ For The Quarter")}}</span> </td>
                                                            <td class="text-center text-primary"> <strong id="ActQuarterBonusAmount">¥{{ActQuarterBonusAmount}}</strong> </td>
                                                            <td class="text-center text-danger"> <strong id="ActQuarterLookupBonusAmount">¥{{ActQuarterLookupBonusAmount}}</strong> </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="d-flex flex-column">
                                    <h3 class="text-dark-75 trm-title-with-divider mt-2">
                                        {{$t("Bonus Simulation Result")}}
                                        <!-- <label name="lb_contact" class="m-0 text-warning"></label> -->
                                        <span></span>
                                    </h3>
                                    <div class="inner-box ad-info-card bg-gray-100">
                                        <ul class="info-list other mt-5-0">                     
                                            <li><strong>{{$t("Deduction Score")}}</strong><span id="Deduction">{{DeductionScore}}</span></li>                       
                                            <li><strong>{{$t("Sugg.Avg")}}</strong><span id="SuggAvg">{{SuggAvg}}</span></li>
                                            <li><strong>{{$t("Simulate Score Base On Budget")}}</strong><span id="SimulateScore">{{SimulateScore}}</span></li>
                                            <li><strong>{{$t("Total Task on the period")}}</strong><span id="PeriodScore">{{PeriodScore}}</span></li>
                                            <li><strong>{{$t("Avg Daily on a period")}}</strong><span id="ScoreAvg">{{ScoreAvg}}</span></li>
                                            <li><strong>{{$t("Simulate Total Take In $Per Mth")}}</strong><span id="SimulatePerMth">¥{{SimulatePerMth}}</span></li>
                                            <li><strong>{{$t("Simulated bonus for the quarter")}}</strong><span id="ActInPerMth">¥{{ActInPerMth}}</span></li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!--end::Card-->
                </div>
            </div>  
        </div>        
        
        <!-- summaryModal -->
        <div class="modal fade summaryModal" id="summaryModal" tabindex="-1" role="dialog" aria-labelledby="summaryModalTitle"
            aria-hidden="true">
            <div class="modal-dialog modal-fullscreen p-3 p-md-1 p-xxl-9" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">{{$t("Summary")}}
                            <label id="lb_progress" class="m-0 text-warning"></label>
                        </h5>
                        <button type="button" class="close text-dark" data-dismiss="modal" aria-label="Close">
                            <i aria-hidden="true" class="fa fa-times"></i>
                        </button>
                    </div>
                    <div class="modal-body p-md-1 p-xl-2">
                        <div class="table-responsive">
                            <table id="dt_summary" class="table table-borderless table-hover table-vertical-center mb-0 table-row-dashed">
                                <thead>
                                    <tr class="text-center">
                                        <th class="p-0 w-50px"></th>
                                        <th class="p-0 min-w-110px w-90px-c"></th>
                                        <th class="p-0 min-w-110px w-50px-c"></th>
                                        <th class="p-0 min-w-110px w-50px-c"></th>
                                        <th colspan="4" class="px-0 pt-0 pb-2 min-w-150px text-left"><span
                                                class="badge badge-subtle badge-danger p-2 text-uppercase">{{$t("Calculation")}}</span>
                                        </th>
                                        <th colspan="5" class="px-0 pt-0 pb-2 min-w-140px text-left"><span
                                                class="badge badge-subtle badge-primary text-uppercase p-2">{{$t("Simulation")}}</span>
                                        </th>
                                        <th class="p-0 min-w-50px"></th>
                                    </tr>
                                    <tr class="text-center th_details">
                                        <th class="pl-0 w-50px text-dark-75">{{$t("User")}}</th>
                                        <th class="min-w-110px w-90px-c text-dark-75">{{$t("Ratio of M:S:P")}}</th>
                                        <th class="min-w-110px w-50px-c text-dark-75">{{$t("Mag")}} %</th>
                                        <th class="min-w-110px w-50px-c text-dark-75 border-right">{{$t("Per")}} %</th>
                                        <th class="min-w-110px w-90px-c text-dark-75">{{$t("Total Tasks Score")}}</th>
                                        <th class="min-w-110px w-90px-c text-dark-75">{{$t("Final Score For The Quarter")}}</th>
                                        <th class="min-w-110px w-90px-c text-dark-75">{{$t("Bonus Score")}}</th>
                                        <th class="min-w-110px w-90px-c text-dark-75 border-right">{{$t("Actual Bonus $ for the quarter")}}</th>
                                        <th class="min-w-110px w-90px-c text-dark-75">{{$t("Avg")}}</th>
                                        <th class="min-w-110px w-90px-c text-dark-75">{{$t("Sugg.Avg")}}</th>
                                        <th class="min-w-110px w-90px-c text-dark-75">{{$t("Simulate Score Base On Budget")}}</th>
                                        <th class="min-w-110px w-90px-c text-dark-75">
                                            <div class="d-flex align-items-center sorting" @click="doSort">
                                                {{$t("Simulate Total Take In $Per Mth")}}
                                                <span class="fa-stack ml-1">
                                                    <i class="fas fa-sort-up fa-stack-1x"></i>
                                                    <i class="fas fa-sort-down fa-stack-1x"></i>
                                                </span>
                                            </div>
                                        </th>
                                        <th class="min-w-110px w-90px-c text-dark-75">{{$t("Simulated bonus for the quarter")}}</th>
                                        <th class="pr-0 min-w-50px"></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(item,index) in bonusData" :key="index">
                                        <td>
                                            <div class="mr-2">
                                                <span
                                                    class="tile bg-info text-uppercase">{{item.contact}}</span>
                                            </div>
                                        </td>
                                        <td class="text-center">
                                            <div
                                                class="d-flex align-items-center justify-content-center font-weight-bold font-size-h5 font-size-h6-md font-size-h5-xl">
                                                <p class="mb-0 text-warning text-hover-danger">{{item.RatioOFM}}</p>
                                                <span class="mx-2">:</span>
                                                <p class="mb-0 text-warning text-hover-danger">{{item.RatioOFS}}</p>
                                                <span class="mx-2">:</span>
                                                <p class="mb-0 text-warning text-hover-danger">{{item.RatioOFP}}</p>
                                            </div>
                                        </td>
                                        <td class="text-center">
                                            <span class="font-weight-bold text-warning text-hover-danger font-size-h5 font-size-h6-md font-size-h5-xl">{{item.ManagementRatio}}</span>
                                        </td>
                                        <td class="text-center border-right">
                                            <span class="font-weight-bold text-warning text-hover-warning font-size-h5 font-size-h6-md font-size-h5-xl">{{item.PerformanaceRatio}}</span>
                                        </td>
                                        <td class="text-center">
                                            <span class="font-weight-bolder d-block font-size-h5 font-size-h6-md font-size-h5-xl text-danger text-hover-warning">{{item.Score}}</span>
                                        </td>
                                        <td class="text-center">
                                            <span class="font-weight-bolder d-block font-size-h5 font-size-h6-md font-size-h5-xl text-danger text-hover-warning">{{item.QuarterScore}}</span>
                                        </td>
                                        <td class="text-center">
                                            <span class="font-weight-bolder d-block font-size-h5 font-size-h6-md font-size-h5-xl text-danger text-hover-warning">{{item.ScoreBonus}}</span>
                                        </td>
                                        <td class="text-center border-right">
                                            <span class="font-weight-bolder d-block font-size-h5 font-size-h6-md font-size-h5-xl text-danger text-hover-warning">{{item.ActQuarterBonusAmount}}</span>
                                        </td>
                                        <!-- Simulate -->
                                        <td class="text-center">
                                            <span class="font-weight-bolder d-block font-size-h5 font-size-h6-md font-size-h5-xl text-primary text-hover-warning">{{item.ScoreAvg}}</span>
                                        </td>
                                        <td class="text-center">
                                            <span class="font-weight-bolder d-block font-size-h5 font-size-h6-md font-size-h5-xl text-primary text-hover-warning">{{item.SuggAvg}}</span>
                                        </td>
                                        <td class="text-center">
                                            <span class="font-weight-bolder d-block font-size-h5 font-size-h6-md font-size-h5-xl text-primary text-hover-warning">{{item.SimulateScore}}</span>
                                        </td>
                                        <td class="text-center">
                                            <span class="font-weight-bolder d-block font-size-h5 font-size-h6-md font-size-h5-xl text-primary text-hover-warning">{{item.SimulatePerMth}}</span>
                                        </td>
                                        <td class="text-center">
                                            <span class="font-weight-bolder d-block font-size-h5 font-size-h6-md font-size-h5-xl text-primary text-hover-warning">{{item.ActInPerMth}}</span>
                                        </td>
                                        <!--  -->
                                        <td class="text-center pr-0">
                                            <div class="d-flex align-items-center text-success font-size-h4 font-size-h5-md font-size-h4-lg" v-if="item.percent>=0"> 
                                                <i class="fas fa-caret-up text-success mr-2"></i> {{item.percent}}% 
                                            </div>
                                            <div class="d-flex align-items-center text-danger font-size-h4 font-size-h5-md font-size-h4-lg" v-else> 
                                                <i class="fas fa-caret-down text-danger mr-2"></i> {{item.percent}}% 
                                            </div>
                                        </td>                                      
                                    </tr>                                    
                                </tbody>
                            </table>
                        </div>
                    </div>            
                    <div class="modal-footer py-3">
                        <button type="button" class="btn btn-primary btn-cancel btn-tasktype-sl" data-target="#tasktypeSLModal" data-toggle="modal">{{$t("Task Type")}}</button>
                        <button type="button" class="btn btn-secondary btn-cancel" data-dismiss="modal">{{$t("Close")}}</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="modal fade tableModal" id="tasktypeSLModal" tabindex="-1" role="dialog" aria-labelledby="tasktypeModalTitle"
        aria-hidden="true">
        <div class="modal-dialog modal-dialog-scrollable modal-xl" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalCenterTitle">{{$t("Task Type Analysis")}}</h5>
                    <button type="button" class="close text-dark" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body taskTypeSL_body">
                    <LPDataTable
                        :paging_inline="true"
                        :paging="false"
                        :columns="taskTypeSLColumns"
                        :datasource="[]"            
                        :custom_options="tasktypeSL_custom_options"
                        :searching="false"
                        :show_footer="true"
                        ref="dt_tasktype_sl"                           
                    />
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary btn-cancel btn-bonus-simulation-undo" 
                    :disabled="!(TaskTypeSl_CurVerNo > 0 && TaskTypeSl_MaxVerNo > 0)" 
                    @click="resetSimulationTasktype(-1)">{{$t("Undo")}}</button>                            
                    <button type="button" class="btn btn-primary btn-cancel btn-bonus-simulation-redo" 
                    :disabled="!(TaskTypeSl_CurVerNo < TaskTypeSl_MaxVerNo + 1 && TaskTypeSl_MaxVerNo > 0)" 
                    @click="resetSimulationTasktype(1)">{{$t("Redo")}}</button>    
                    <button type="button" class="btn btn-primary btn-cancel btn-bonus-simulation" @click="bonusSimulationSL">{{$t("Bonus Simulation")}}</button>    
                    <button type="button" class="btn btn-primary btn-cancel btn-bonus-simulation" @click="bonusSimulationSA">{{$t("Save")}}</button>                 
                    <button type="button" class="btn btn-secondary btn-cancel" data-dismiss="modal">{{$t("Close")}}</button>  
                </div>
            </div>
        </div>
    </div> 
    <!--
    <div class="modal fade tableModal" id="deductionItemModal" tabindex="-1" role="dialog" aria-labelledby="deductionItemTitle"
        aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-xl" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">扣分明細</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <LPDataTable
                        id="dt_userdeduction"
                        :paging_inline="true"
                        :paging="false"
                        :columns="userDeductionColumns"
                        datasource="/bonus/userdeduction/datatable"            
                        :custom_options="userDeduction_custom_options"
                        :custom_params_fun="userDeduction_params_fun"
                        :searching="false"
                        :show_footer="true"
                        ref="dt_userdeduction"                           
                    />
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary btn-cancel" @click="newDeductionItem">New Item</button>                    
                    <button type="button" class="btn btn-secondary btn-cancel" data-dismiss="modal">Close</button>                    
                </div>
            </div>
        </div>
    </div>-->
    <div class="modal fade" id="selectDateModal" tabindex="-1" role="dialog" aria-labelledby="selectDateModalTitle"
        aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{$t("Please enter the date")}}</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <i class="fas fa-times text-dark" style="font-size: 20px;"></i>
                    </button>
                </div>
                <div class="modal-body">                                    
                    <div class="col">
                        <div class="row-container SWRow"><div class="col div-1"><div class="form-group SWDate" style="">
                            <label class="col-form-label caption">{{$t("From Date")}}</label>
                            <input class="form-control control" type="date" value="" id="summary_edatefrom" required>
                        </div></div><div class="col div-2"><div class="form-group SWDate" style="">
                            <label class="col-form-label caption">{{$t("To Date")}}</label>
                            <input class="form-control control" type="date" value="" id="summary_edateto" required>
                        </div></div></div>
                    </div>              
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary bonus_summary" @click="bonusSummary">{{$t("Search")}}</button>                    
                </div>
            </div>
        </div>
    </div>
    <div class="modal fade my-modal-parent" id="messageModal" tabindex="-1" role="dialog" aria-labelledby="messageModalTitle"
        aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{$t("Message")}}</h5>
                    <button type="button" class="close text-dark" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <p id="msg" class="font-weight-bolder text-dark"></p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary btn-cancel" data-dismiss="modal">{{$t("Close")}}</button>
                </div>
            </div>
        </div>
    </div>
    <LPModal ref="SearchModal" :title="$t('Filter')" class="col" id="SearchModal" show_part="bf">
      <template v-slot:body>
        <ul class="nav nav-tabs nav-tabs-line mb-1" style="font-size:14px;" id="tab_search">
            <li class="nav-item">
                <a class="nav-link show active" data-toggle="tab" href="#search_basic" id="nav_normal">{{$t("Normal Condition")}}</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" data-toggle="tab" href="#search_advanced" id="nav_pms">{{$t("PMIS Condition")}}</a>
            </li>
        </ul>
        <div class="tab-content mb-1">
            <div class="tab-pane fade active show" id="search_basic">
                <div class="row">
                    <div class="form-group col-12">
                        <label class="col-form-label caption">{{$t("Contact")}}</label>
                        <input class="form-control control" type="text" name="contact" id="contact">
                    </div>
                </div>
                <div class="row">
                    <div class="form-group col-6">
                        <label class="col-form-label caption">{{$t("ProjectID")}}</label>
                        <input class="form-control control" type="text" name="projectid" id="projectid">
                    </div>
                    <div class="form-group col-6">
                        <label class="col-form-label caption">{{$t("RecordID")}}</label>
                        <input class="form-control control" type="text" name="recordid" id="recordid">
                    </div>
                </div>
                <div class="row">
                    <div class="form-group col-6">
                        <label class="col-form-label caption">{{$t("From Date")}}</label>
                        <input class="form-control control" type="date" name="edatefrom" id="edatefrom" required>
                    </div>
                    <div class="form-group col-6">
                        <label class="col-form-label caption">{{$t("To Date")}}</label>
                        <input class="form-control control" type="date" name="edateto" id="edateto" required>
                    </div>
                </div>
            </div>
            <div class="tab-pane fade" id="search_advanced">
                <div class="form-inline mb-1 cust_filter align-items-center" style="flex-wrap: nowrap;">
                    <div class="input-group mr-3" style="flex:1 1 auto">
                        <input type="text" id="template-users" class="form-control"/>
                        <div class="input-group-append">
                            <button id="search_filter_btn" @click="searchFilter" class="btn btn-primary no-caret"><span class="fa fa-search"></span></button>
                        </div>                
                    </div>  
                              
                    <div class="checkbox-inline">
                        <label class="checkbox">
                            <input class="control enlarged-checkbox mr-2" id="IsDaily" type="checkbox" name="Checkboxes2" checked />
                            <span></span>
                            {{$t("Daily")}}
                        </label>
                    </div>                
                </div>
                <div class="pre-scrollable">

                </div>             
            </div>  
        </div>        
        <!-- :gsearch_placeholder="a" -->        
      </template>
      <template v-slot:footer>
        <button type="button" class="btn btn-danger" @click="clearHandle">{{$t("Clear")}}</button>
        <button type="button" class="btn btn-primary" @click="searchHandle">{{$t("Search")}}</button>
        <button type="button" class="btn btn-secondary" data-dismiss="modal">{{$t("Close")}}</button>
      </template>
    </LPModal>
    <LPModal ref="UserModal" :title="$t('Please enter the user name')" class="col noShadowModal" id="UserModal">
      <template v-slot:body>
        <!-- :gsearch_placeholder="a" -->
        <input type="text" class="form-control" name="contact" :placeholder="$t('UserName')" v-model="contact">
      </template>
      <template v-slot:footer>
        <button type="button" class="btn btn-primary" @click="bonusAnalysis_handle" data-dismiss="modal">{{$t("Search")}}</button>
      </template>
    </LPModal>
    <LPModalForm
        :novalidate="true"
        ref="deductionItemForm"
        :title="deductionItemFormTitle"
        @on_submit="submitModalForm"
    >  
        <LPLabelInput :label="$t('Area of Improvement')">
            <LPCombobox url='/looper/metting/get_Improvement' :labelFields="['tpdesc']"            
            valueField='tpdesc' @on_item_selected="manageChange"
            :value="currentDeductionItem.improvement" @on_Blur="(value) => { currentDeductionItem.improvement = value }"
            />            
        </LPLabelInput> 
        <LPLabelInput :label="$t('Description')">
          <LPCombobox url='/looper/metting/get_Improvement_item' ref="description_LPCasombobox" :labelFields="['tptname']"
            :filter="Improvement_item_filter"
            valueField='TptName' :value="currentDeductionItem.description" @on_item_selected="onDescriptionDesc_change"
            @on_Blur="(value) => { currentDeductionItem.description = value }" />
        </LPLabelInput> 
        <LPLabelInput :label="$t('PenaltyID')">
        <input
            type="text"
            class="form-control"
            v-model="currentDeductionItem.penaltyid"
        >
        </LPLabelInput> 
        <LPLabelInput :label="$t('Contact')">
        <input
            type="text"
            class="form-control"
            v-model="currentDeductionItem.username"
            @change="getUserPosition"
        >
        </LPLabelInput>     
        <LPLabelInput :label="$t('Category')">
            <LPCombobox url='/bonus/userdeduction/get_duction_category' :labelFields="['category']"
                valueField='category' :value="currentDeductionItem.category" @on_item_selected="(item) => { currentDeductionItem.category = item.category }"
                @on_Blur="(value) => { currentDeductionItem.category = value }" />
        </LPLabelInput>    
        <LPLabelInput :label="$t('Position')">            
        <input
            type="text"
            class="form-control"
            v-model="currentDeductionItem.position"            
        >
        </LPLabelInput>    
        <!-- <LPLabelInput :label="$t('Description')">
        <textarea
            class="form-control scrollbar"
            v-model="currentDeductionItem.description"
            rows="3"
        ></textarea>
        </LPLabelInput>  -->
        <LPLabelInput :label="$t('Deduct Score')">
        <input
            type="text"
            class="form-control"
            v-model="currentDeductionItem.score"
        >
        </LPLabelInput> 
        <LPLabelInput :label="$t('Date')">
        <input 
            type="date"
            class="form-control" 
            v-model="currentDeductionItem.deductiondate"
            required
        >
        </LPLabelInput> 
        </LPModalForm>
         <LPAIComBox ref="aicombox" 
          class="mb-0" 
          :iframe_src="'http://183.63.205.83:3000/aiChat'" 
          :aiPresetQuestion="aiPresetQuestion" 
          :predefinedData="this.sentAIData" />    
    <div id="SWListgroup" class="list-group list-group-bordered mb-3" style="display: none;">
        <a href="#" class="list-group-item list-group-item-action d-flex" pk="[[qf025]]">                                                                                                                                                                      
        <div class="pr-2">
            <div class="tile">
            <span class="">[[qf012 ]]</span>
            </div>
        </div>
        <div class="list-group-item-body">[[qf003]]</div>
        </a>
    </div>
</template>
<script>
import axios from "axios";
import LPModalForm from "@components/looper/layout/LPModalForm.vue";
import LPLabelInput from "@components/looper/forms/LPLabelInput.vue";
import LPModal from "@components/looper/layout/LPModal.vue";
import LPCombobox from "@components/looper/forms/LPCombobox.vue";
import LPAIComBox from "@components/looper/general/LPAIComBox.vue";
import LPDataTable, {
  DateRender
} from "@components/looper/tables/LPDataTable.vue";
import {
    formatDate,
    getToday,
    getWeekStartDate,
    getLastWeekStartDate,
    getLastWeekEndDate,
    getMonthStartDate,
    getMonthEndDate,
    getLastMonthStartDate,
    getLastMonthEndDate,
    getQuarterStartDate,
    getQuarterEndDate,
    getLastQuarterStartDate,
    getLastQuarterEndDate,
    get_quarterly_date
} from "/BonusApp/static/BonusApp/source/javascript/datatime_common.js";
export default {
  name: "bonus_analysis",
  components: {   
    LPDataTable,
    LPModalForm,
    LPModal,
    LPLabelInput,
    LPCombobox,
    LPAIComBox,
  },
  data() {
    var self = this;
    return {        
        taskColumns: [
            { field: "contact", label: this.$t("Contact") , width: "50px" , className: 'all'},  
            { field: "taskno", label: this.$t("TaskNo"), width: "120px" , className: 'min-phone-l'},
            { field: "progress", label: this.$t("Progress"), visible:false},
            { field: "task", label: this.$t("Description"), width: "270px" , className: 'min-tablet mw_custom'},
            //{field:"edate", label:"E Date", render:SWDataTable.DateRender},         
            {
                field: "planbdate", label: this.$t("PlanBDate"), width:"60px",
                className: 'desktop',
                visible:false,
                render: function ChangeDateFormat(value) {
                    var reg = /^\s*$/;
                    //返回值为true表示不是空字符串
                    if (value != null && value != undefined && !reg.test(value)) {
                        var orderdate = new Date(value);
                        var month = orderdate.getMonth() + 1;
                        var day = orderdate.getDate();
                        month = (month.toString().length == 1) ? ("0" + month) : month;
                        day = (day.toString().length == 1) ? ("0" + day) : day;
                        //当前日期 yyyy-MM-dd
                        return orderdate.getFullYear() + '-' + month + '-' + day;
                    } else
                        return '';
                }
            },   
            {
                field: "edate", label: this.$t("E Date"), width:"60px",
                className: 'desktop',
                render: function ChangeDateFormat(value) {
                    var reg = /^\s*$/;
                    //返回值为true表示不是空字符串
                    if (value != null && value != undefined && !reg.test(value)) {
                        var orderdate = new Date(value);
                        var month = orderdate.getMonth() + 1;
                        var day = orderdate.getDate();
                        month = (month.toString().length == 1) ? ("0" + month) : month;
                        day = (day.toString().length == 1) ? ("0" + day) : day;
                        //当前日期 yyyy-MM-dd
                        return orderdate.getFullYear() + '-' + month + '-' + day;
                    } else
                        return '';
                }
            },
            { field: "score", label: this.$t("S"),  className: "fontBlue" , className: 'desktop'},
            { field: "lookupscore", label: this.$t("LS"), className: "fontRed" , className: 'desktop'}, 
            { field: "realtasktype", label: this.$t("Task Type") , width: "80px", className: 'desktop'},
            { field: "tasktypedc", label: this.$t("TaskType Description") , className: 'desktop'}, 
        ],
        taskTypeColumns:[                               
            { field: "tasktype", label: this.$t("Task Type") , width: "130px"}, 
            { field: "description", label: this.$t("Description"), width: "400px"},  
            { field: "score", label: this.$t("Score"), width: "100px" },         
            { field: "count", label: this.$t("Count"), width: "100px" },   
            { field: "totalscore", label: this.$t("TotalScore"), width: "100px" },     
        ],
        taskTypeSLColumns:[
            { field: "tasktype", label: this.$t("Task Type") , width: "130px"}, 
            { field: "description", label: this.$t("Description"), width: "400px"},  
            { field: "oldscore", label: this.$t("Score") , width :"100px"},
            { field: "score", label: this.$t("New Score") , width :"100px", 
                render:function(data, type, row){
                    if (row['score'] == row['oldscore'])
                        return `<input class="textEdit form-control text-dark" type="text" value="${data}" inc_id="${row.inc_id}" oldvalue="${data}" oldscore="${row.oldscore}" style="width: 40px;">`;
                    else
                        return `<input class="textEdit form-control" type="text" value="${data}" inc_id="${row.inc_id}" oldvalue="${data}" oldscore="${row.oldscore}" style="width: 40px;">`;
                }
            },                                
            { field: "count", label: this.$t("Count") },   
            { field: "totalscore", label: this.$t("TotalScore") , width :"100px"},  
        ],
        userDeductionColumns:[
            { field: "inc_id", label: this.$t("ID"), visible:false}, 
            { field: "username", label: this.$t("UserName")}, 
            { field: "description", label: this.$t("Description"), width: "400px"},           
            { field: "score", label: this.$t("Score")},
            { field: "deductiondate", label: this.$t("Date"), render: DateRender},
            { field:'operate',label: this.$t('Operation'),width:"30",
                render:function(data, type, row){    
                    return `<div class="dropdown SWDropdown" inc_id="${row.inc_id}">
                    <button class="btn caption" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><i class="fas fa-ellipsis-v"></i></button>  
                        <div class="dropdown-menu control" aria-labelledby="dropdownMenuButton">
                            <a class="dropdown-item edit" href="#">{0}</a>
                            <a class="dropdown-item delete" href="#">{1}</a>
                        </div>
                    </div>`.format(self.$t("Edit"),self.$t("Delete"))
                }
            }   
        ],
        task_custom_options:{
            responsive: false,
            scrollX: true,
            scrollY: 380,
            deferLoading: 0,
            autoWidth: false,        
        },
        tasktype_custom_options:{
            responsive: false,
            scrollX: true,
            scrollY: 350,
            deferLoading: 0,
            autoWidth: false, 
            footerCallback: function( tfoot, data, start, end, display ) {                       
                var api = this.api();
                $( api.column( 0 ).footer() ).html("");
                $( api.column( 1 ).footer() ).html("");
                $( api.column( 2 ).footer() ).html(self.$t("Total:"));
                $( api.column( 3 ).footer() ).html(
                    api.column( 3 ).data().reduce( function ( a, b ) {
                        return a + b;
                    }, 0 )
                );
                $( api.column( 4 ).footer() ).html(
                    api.column( 4 ).data().reduce( function ( a, b ) {
                        return a + b;
                    }, 0 )
                ); 
            }       
        },
        tasktypeSL_custom_options:{
            responsive: false,
            scrollX: true,
            scrollY: "60vh",
            deferLoading: 0,
            autoWidth: false, 
            footerCallback: function( tfoot, data, start, end, display ) {                        
                var api = this.api();
                $( api.column( 0 ).footer() ).html("");
                $( api.column( 1 ).footer() ).html("");
                $( api.column( 2 ).footer() ).html("");
                $( api.column( 3 ).footer() ).html(self.$t("Total:"));
                $( api.column( 4 ).footer() ).html(
                    api.column( 4 ).data().reduce( function ( a, b ) {
                        return a + b;
                    }, 0 )
                );
                $( api.column( 5 ).footer() ).html(
                    api.column( 5 ).data().reduce( function ( a, b ) {
                        return a + b;
                    }, 0 )
                );            
            }
        },
        userDeduction_custom_options:{     
            responsive: false,
            scrollX: true,
            scrollY: 290,  
            deferLoading: 0,       
            autoWidth: false, 
            footerCallback: function( tfoot, data, start, end, display ) {                       
                var api = this.api();
                $( api.column( 0 ).footer() ).html("");  
                $( api.column( 1 ).footer() ).html("");       
                $( api.column( 2 ).footer() ).html(self.$t("Total:"));
                $( api.column( 3 ).footer() ).html(
                    api.column( 3 ).data().reduce( function ( a, b ) {
                        return a + b;
                    }, 0 )
                );           
            }             
        },
        global_edatefrom:'',
        global_edateto:'',
        contact:'',
        recordid:undefined,
        projectid:'',
        cloneBonusData:{},
        contactBonusData:{},
        taskData:[],
        BudgetAllowance:0,
        PerfectScoring:0,
        RatioOFM:0,
        RatioOFS:0,
        RatioOFP:0,
        ManagementS:0,
        PerformanceS:0,
        QuarterWorkingDay:0,
        UnitPrice:0,
        WorkingDay:0,
        ManagementRatio:0,
        PerformanaceRatio:0,
        Salary:0,
        Score:0,
        LookupScore:0,
        ManagementScore:0,
        ManagementLookupScore:0,
        ScoreAvg:0,
        SuggAvg:0,
        QuarterScore:0,
        QuarterLookupScore:0,
        SimulateScore:0,
        ScoreBonus:0,
        LookupScoreBonus:0,
        SimulatePerMth:0,
        ScoreActualQuarter:0,
        LookupScoreActualQuarter:0,
        ActInPerMth:0,
        ActQuarterBonusAmount:0,
        ActQuarterLookupBonusAmount:0,
        PeriodScore:0,
        isBounsSearch:false,
        bonusData:[],
        currentDeductionItem:{},
        deductionItemFormTitle:"",
        userDeduction_params_fun:undefined,
        searchType:"",        
        TaskTypeSl_MaxVerNo:0,
        TaskTypeSl_CurVerNo:undefined,
        TaskTypeSl_CurDirection:undefined,
        isMobile: false,
        isExpend: false,
        isSortState: 0,
        DeductionScore: 0,
        management_selected:[],
        Improvement_item_filter:'',
        aiPresetQuestion: [], 
        predefinedData: [],
        bonusResult: null,
        sentAIData:{},
    };
  },
  mounted() {
    //$.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
    $('.wrapper').on("shown.bs.tab","a[data-toggle='tab']", function (e) {
        $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
    });

    $('.tableModal').on('shown.bs.modal', function(e){
        $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
    });
    $(".taskTypeSL_body").on("blur", ".textEdit", function(){
        var value = $(this).val();
        var oldscore = $(this).attr("oldscore");
        var td_dom = $(this).closest("td");
        var count = parseInt(td_dom.next().text());
        td_dom.next().next().text(value * count);
        if (value != oldscore)
            $(this).removeClass("text-dark");
        else
            if (!$(this).hasClass("text-dark"))
                $(this).addClass("text-dark");
    });
    this.listenButtonEvent();
    this.get_tasktype_sl_history_maxver();
    this.isMobileStyle();
  },
  created() {          
     var self = this;
     self.$nextTick(function(){
        self.init_params();           
     })  
        
  },
  methods: {  
    AIOpen() {
        console.log("sentAIData ", this.sentAIData);
        this.$refs.aicombox.$refs.modal.show();
    },
    //檢驗參數penalty是否為Y
    init_params(){
        var self = this   
        var penalty =  this.$route.query.penalty;
        if(penalty=='Y'){
            this.$refs.tab_deduction.click();
            this.$refs.btnNew.click();                             
        }
    },
    //獲取模板選項源
    init_penalty(){
        var self = this
        axios.get("/looper/metting/get_Improvement",{
            params:{ "manager": '2', "tpdesc": 'AreasofImprovementfor'}
        })    
        .then((response)=>{
            var result = response.data;
            if(result.status){                 
                self.management_selected=result.data;                     
            }            
        });   

    },
    //模板變化事件
    manageChange(item){
        this.currentDeductionItem.management = item.tpmastid; 
        this.currentDeductionItem.improvement=item.tpdesc
        if (this.currentDeductionItem.management)
            this.Improvement_item_filter=`tpmastid=${this.currentDeductionItem.management}`
        else
            this.Improvement_item_filter=''
    },

    search(searchType){      
        this.searchType = searchType;
        if (this.searchType=="Bonus")
            $('#tab_search').show()
        else{
            $("#nav_normal").click();
            $('#tab_search').hide()
        }            
        this.$refs.SearchModal.show();        
    },
    searchHandle(){
        if(this.searchType=="Bonus")
            this.bonusSearch();
        else
            this.deductionSearch();
    },
    clearHandle(){
        $('#contact').val('');
        $('#edatefrom').val('');
        $('#edateto').val('');
        $('#projectid').val('');
        $('#recordid').val('');
    },
    bonusSearch(){  
        var id = $('#SearchModal .tab-content .active').attr('id');
        // 一般查詢
        if (id == "search_basic") {
            this.contact=$('#contact').val();
            this.global_edatefrom = $('#edatefrom').val();
            this.global_edateto = $('#edateto').val();
            this.projectid = $('#projectid').val();
            this.recordid = $('#recordid').val();
            if (this.global_edatefrom=="") {
                this.showMessage(this.$t("Please enter the from date")); //請輸入[從實際結束時間]                    
                return;
            }
            if (this.global_edateto=="") {        
                this.showMessage(this.$t("Please enter the to date")); //請輸入[到實際結束時間]          
                return;
            }        
            this.bonusAnalysis_handle();
        }else{
            // 按PMS 自定義條件查詢
            if ($("#search_advanced .list-group a.active").length == 0) {
                this.showMessage(this.$t("Please select a condition"));
                return false;
            }
            this.search_task()

        }       
        this.$refs.SearchModal.hide();
    },
    deductionSearch(){  
      var contact=$('#contact').val();
      var datefrom = $('#edatefrom').val();
      var dateto = $('#edateto').val();
      var self = this;
      this.userDeduction_params_fun = () => {  
        if (contact=='' && datefrom=='' && dateto==''){
            return null;
        }  
        let filter = "";
        if(contact!=''){
          filter+='{"id":"username","field":"username","type":"string","input":"text","operator":"equal","value":"{0}"},'.format(contact);
        }
        if(datefrom!=''){
          filter+='{"id":"deductiondate","field":"deductiondate","type":"string","input":"text","operator":"greater_or_equal","value":"{0}"},'.format(datefrom);
        }
        if(dateto!=''){
          filter+='{"id":"deductiondate","field":"deductiondate","type":"string","input":"text","operator":"less_or_equal","value":"{0}"},'.format(dateto);
        }
        filter=filter.substr(0,filter.length-1);
        return {  
          attach_query:
            `{"condition":"AND","rules":[{0}],"not":false,"valid":true}`.format(filter),
        };
      };
      this.$nextTick(() => {
        self.$refs.dt_userdeduction.datatable.draw();
      });
      this.$refs.SearchModal.hide();

    },
    bonusAnalysis(cycle){
        this.projectid = '';
        this.recordid = undefined;
        if(cycle=='today'){
            this.global_edatefrom = getToday();
            this.global_edateto = getToday();
        }
        else if(cycle=='yesterday'){
            var yesterday = new Date();
            yesterday.setDate(yesterday.getDate()-1); 
            this.global_edatefrom = formatDate(yesterday);
            this.global_edateto = formatDate(yesterday);
        }else if(cycle=='lastweek'){
            this.global_edatefrom = getLastWeekStartDate();
            this.global_edateto = getLastWeekEndDate();
        }else if(cycle=='week'){
            this.global_edatefrom = getWeekStartDate();
            this.global_edateto = getToday();
        }else if(cycle=='lastmonth'){
            this.global_edatefrom = getLastMonthStartDate();
            this.global_edateto = getLastMonthEndDate();
        }else if(cycle=='month'){
            this.global_edatefrom = getMonthStartDate();
            this.global_edateto = getToday();
        }else if(cycle=='lastquarter'){
            this.global_edatefrom = getLastQuarterStartDate();
            this.global_edateto = getLastQuarterEndDate();
        }else if(cycle=='quarter'){
            this.global_edatefrom = getQuarterStartDate();
            this.global_edateto = getToday();
        }
        this.$refs.UserModal.show();
    },
    refreshAonusAnalysis(){
        if(this.contact==''){
            this.showMessage(this.$t("Please enter the contact"));//聯繫人不能為空
            return;      
        }
        this.bonusAnalysis_handle();
    },
    bonusAnalysis_handle(){
        var quarterBegin = formatDate(get_quarterly_date(new Date(this.global_edatefrom))[0]);
        var quarterEnd = getToday();
        if (formatDate(get_quarterly_date(new Date(this.global_edatefrom))[1])<quarterEnd)
            quarterEnd = formatDate(get_quarterly_date(new Date(this.global_edatefrom))[1]);
        
        //alert(formatDate(get_quarterly_date(new Date(this.global_edatefrom))[0]));
        //alert(formatDate(get_quarterly_date(new Date(this.global_edatefrom))[1]));
        $('.dataTables_info').css('display','none');  
        axios.get("/bonus/bonus_analysis",{
            params: { "contact": this.contact, "edatefrom": this.global_edatefrom, "edateto": this.global_edateto , "calSat":false, "quarterbegin":quarterBegin, "quarterend":quarterEnd, "projectid":this.projectid, "recordid":this.recordid}
        })
        .then((response) => {
            $("#tab_tasks").click();
            this.$refs.UserModal.hide();
            var result = response.data;
            var message = result.errorMessage;
            if (message != '') {              
                this.showMessage(message);                  
                return;
            }
            if(this.contact!=""){
                this.cloneBonusData = JSON.parse(JSON.stringify(result.bonusResult));              
                this.showBonusResult(result.bonusResult);                                                   
                this.isBounsSearch = true;     
                this.setComponent('');                                           
                this.showTaskTypes(result.tasktypedata);


                // 给AI发送的数据
                this.sentAIData={
                    BonusParameter:{
                        'Budget Allowance %':result.bonusResult.BudgetAllowance,
                        'Price Per Score ¥':result.bonusResult.UnitPrice,
                        'Management S':result.bonusResult.ManagementS,
                        'Performance. S':result.bonusResult.PerformanceS,
                        'Working Day':result.bonusResult.PeriodWorkingDay,
                        'Quarter Working Day':result.bonusResult.QuarterWorkingDay,
                        'Perfect Scoring':result.bonusResult.PerfectScoring,
                        'Ratio of M:S:P':result.bonusResult.RatioOFM+':'+result.bonusResult.RatioOFS+':'+result.bonusResult.RatioOFP,
                        'Mag %':'',
                        'Per %':''
                    },
                    BonusAnalysisResult:{
                        Score:{
                            'Total Tasks Score':result.bonusResult.TotalScore,
                            'Total Management Score':result.bonusResult.ManagementScore,
                            'Final Score For The Quarter':result.bonusResult.QuarterScore,
                            'Bonus Score':result.bonusResult.ScoreBonus,
                            'Actual Bonus $ For The Quarter':'¥'+result.bonusResult.ActQuarterBonusAmount,
                        },
                        LookupScore:{
                            'Total Tasks Score':result.bonusResult.LookupScore,
                            'Total Management Score':result.bonusResult.ManagementLookupScore,
                            'Final Score For The Quarter':result.bonusResult.QuarterLookupScore,
                            'Bonus Score':result.bonusResult.LookupScoreBonus,
                            'Actual Bonus $ For The Quarter':'¥'+result.bonusResult.ActQuarterLookupBonusAmount,
                        }
                    },
                    BonusSimulationResult:{
                        'Deduction Score':result.bonusResult.DeductionScore,
                        'Sugg.Avg':result.bonusResult.SuggAvg,
                        'Simulate Score Base On Budget':result.bonusResult.SimulateScore,
                        'Total Task on the period':result.bonusResult.PeriodScore,
                        'Avg Daily on a period':result.bonusResult.ScoreAvg,
                        'Simulate Total Take In $Per Mth':'¥'+result.bonusResult.SimulatePerMth,
                        'Simulated bonus for the quarter':'¥'+result.bonusResult.ActInPerMth,
                    },
                    bonusResult:{
                        'Task List':result.data.map(({ contact, taskno, task ,score,edate,lookupscore,subtasktypedesc,pid,recordid,tiddesc,projectname,tasklistno,remark,class_field}) => ({
                                        'Contact':contact,
                                        'Record ID(项目编号)':recordid,  //項目編號  00188
                                        'Project Name(项目名称)':projectname, //項目名稱 *Knowledge based project
                                        'Session No(模组编号)':tasklistno,    //模組編號  00500-503
                                        'Session Describe(模组描述)':tiddesc,    //模塊名稱  IP - SALC Implementation
                                        'PID(工程编号)':pid,  //工程編號  00500 
                                        'TaskNo':taskno,
                                        'Description':task,
                                        'Score':score,
                                        'E Date':edate,
                                        'LookupScore':lookupscore,
                                        'TaskType Description':subtasktypedesc,
                                        'Remark':remark,
                                        'Class':class_field
                                    })),
                        'Task Type Data':result.tasktypedata.map(({ count, description, lookupscore ,score,tasktype,totallookupscore,totalscore}) => ({
                                        'Count':count,
                                        'Description':description,
                                        'Lookup Score':lookupscore,
                                        'Score':score,
                                        'Task Type':tasktype,
                                        'Total Lookup Score':totallookupscore,
                                        'Total Score':totalscore,
                                    })),
                    }
                }
                
            }else{
                this.isBounsSearch = false;
                var filter = "EDate Between {0} and {1}".format(this.global_edatefrom,this.global_edateto);
                this.setComponent(filter);  
            }
            this.showTasks(result.data);
             console.log("Data received from server: ", response.data);
        })
        .catch((error) => {
          console.log(error);
        });
        
    },
    showTaskTypes(data){
        this.$refs.dt_tasktype.datatable.clear();
        this.$refs.dt_tasktype.datatable.rows
        .add(data).columns.adjust()
        .draw();  
    }, 
    //顯示任務信息
    showTasks(data){        
        if(this.isBounsSearch){
            $('#query_wrapper').parent().parent().removeClass("fullscreen");
        }else {
            $('#query_wrapper').parent().parent().addClass("fullscreen");
        }

        var dataTable = this.$refs.dt_task.datatable;        
        dataTable.columns(this.$refs.dt_task.getColumnIndexByName("progress")+1).visible(!this.isBounsSearch);   
        dataTable.columns(this.$refs.dt_task.getColumnIndexByName("planbdate")+1).visible(!this.isBounsSearch);   
        dataTable.clear().rows.add(data).columns.adjust().draw();
        this.getBrowser();
    },     
    showBonusResult(data,isShowHint=true) {
        this.contactBonusData = data;
        this.BudgetAllowance=data["BudgetAllowance"];
        this.PerfectScoring=data["PerfectScoring"];
        this.RatioOFM=data["RatioOFM"];
        this.RatioOFS=data["RatioOFS"];
        this.RatioOFP=data["RatioOFP"];
        this.ManagementS=data["ManagementS"];
        this.PerformanceS=data["PerformanceS"];
        this.QuarterWorkingDay=data["QuarterWorkingDay"];
        this.WorkingDay=data["WorkingDay"];
        this.ManagementRatio=data["ManagementRatio"];
        this.PerformanaceRatio=data["PerformanaceRatio"];
        this.Salary=data["Salary"];
        this.Score=data["Score"];
        this.UnitPrice=data["UnitPrice"]
        this.LookupScore=data["LookupScore"];
        this.ManagementScore=data["ManagementScore"];
        this.ManagementLookupScore=data["ManagementLookupScore"];
        this.ScoreAvg=data["ScoreAvg"];
        this.SuggAvg=data["SuggAvg"];
        this.QuarterScore=data["QuarterScore"];
        this.QuarterLookupScore=data["QuarterLookupScore"];
        this.SimulateScore=data["SimulateScore"];
        this.ScoreBonus=data["ScoreBonus"];
        this.LookupScoreBonus=data["LookupScoreBonus"];
        this.SimulatePerMth=data["SimulatePerMth"];
        this.ScoreActualQuarter=data["ScoreActualQuarter"];
        this.LookupScoreActualQuarter=data["LookupScoreActualQuarter"];               
        this.ActInPerMth=data["ActInPerMth"];
        this.ActQuarterBonusAmount=data["ActQuarterBonusAmount"];
        this.ActQuarterLookupBonusAmount=data["ActQuarterLookupBonusAmount"]; 
        this.PeriodScore=data["PeriodScore"];  
        this.DeductionScore=data["DeductionScore"];
        var differ = data["SuggAvg"]-data["ScoreAvg"];
        //當每日實際得分比建議分少20時，則提示
        if (data["SuggAvg"]-data["ScoreAvg"]>20 && isShowHint)
            this.showMessage("周期: {0} 到 {1}<br/> Avg: {2} 比 Sugg.Avg: {3} 低 {4} （不達標）".format(this.global_edatefrom,this.global_edateto,data["ScoreAvg"],data["SuggAvg"],differ.toFixed(2)));
    },
    setComponent(Condition){
        $("#btn_expand").show();
        $("#btn_aibox").show();
        
        if(this.isBounsSearch){
            $("#tab_TaskType").show(); 
            //$('#card_task').removeClass("d-none");
            //$('#no_content').addClass("d-none");
            $("#tab_Deductions").show();

            $("#btn_auditScore").show();
            //$("#btn_reportDesign").show();
            $("#btn_reportPreview").show();
            $("#btn_unauditScore").show();
            
            $("#card_para").show();
            $("#card_result").show();
            $('#query_wrapper').removeClass("d-none");

            $("#lb_condition").hide();
        }
        else{
            //$("#btn_showTaskType").hide();
            $("#btn_auditScore").hide();
            //$("#btn_reportDesign").show();
            $("#btn_reportPreview").hide();
            $("#btn_unauditScore").hide();

            $("#tab_TaskType").hide(); 
            $("#tab_Deductions").hide();
            $("#card_para").hide();
            $("#card_result").hide();
            $("#lb_condition").show();
        }
        $("[name='lb_contact']").html("");
        $("#lb_condition").html("");
        if(this.contact!=""){
            $("[name='lb_contact']").html("（" + this.contact + "）");
            $("#contact").val(this.contact);
        }
        if(Condition!="")
            $("#lb_condition").html(Condition);
    },
    auditScore(state){
        var tasks = this.$refs.dt_task.getSelectedFlagData()["datas"];
        if(tasks && tasks.length==0){
            this.showMessage(this.$t("Please select task record"));//請選擇記錄！
            return;
        }
        axios.post("/bonus/audit_source",this.objectToFormData({"tasks":JSON.stringify(tasks),"audit":state})
        )
        .then((response) => {
            var result = response.data;
            if(result.status)
                if(state=='Y')
                    this.showMessage(this.$t("Post Success"));//審核成功！
                else
                    this.showMessage(this.$t("Un Post Success"));//反審核成功！
            else
                this.showMessage(result.msg);
        });        
    },
    searchSummary(){
        $("#summary_edatefrom").val(getQuarterStartDate());
        $("#summary_edateto").val(getQuarterEndDate());
        $('#selectDateModal').modal('show');  
    },
    bonusSummary() {
        var edatefrom = $("#summary_edatefrom").val();   
        var edateto= $("#summary_edateto").val();
        if ((edatefrom=='') || (edateto=='')){
            this.showMessage(this.$t("The date cannot be null"));//日期不能為空
        }
        $('#selectDateModal').modal('hide');  
        this.bonusData=[];
        $('#summaryModal').modal('show'); 
        //$("#dt_summary tbody").children().remove();
        $("#lb_progress").html(this.$t("Loading..."));//正在加載...
        var isChecked = $('#cb_calSat').prop('checked');  
        this.analyse_bar(edatefrom, edateto, isChecked);        
    },
    analyse_bar(edatefrom, edateto, cb_calSat, isSL=false) {
        axios.get("/bonus/analyse_bar",{
            params:{"edatefrom": edatefrom, "edateto": edateto, "calSat": cb_calSat,"isSL":isSL}
        })
        .then((response) => {  
            if(response.status == 200)                 
            this.bonusData = this.sortBonusData(response.data.bonusResult);
            this.showTaskTypesSL(response.data.taskTypeList);
            $("#lb_progress").html("");
        });        
    },
    sortBonusData(bonusData){
        var result=[];
        for(let contact in bonusData) {  
            let data =  bonusData[contact]
            let ScoreAvg = data["ScoreAvg"];
            let SuggAvg = data["SuggAvg"];
            //計算達到值
            let percent = parseInt((ScoreAvg-SuggAvg)/SuggAvg*100); 
            data["percent"] = percent;
            data["contact"]= contact;  
            result.push(data);          
        }
        //按達表值從小到大進行排序
        result = result.sort(function(a,b){
            return a.percent-b.percent;
        });
        return result;
    },
    showTaskTypesSL(data){
        this.$refs.dt_tasktype_sl.datatable.clear();
        axios.get("/bonus/get_tasktype_sl")
        .then((response) => {  
            if(response.status == 200)                 
            {
                var taskTypeList = response.data.data;
                var taskTypeListMap = taskTypeList.reduce(function(map, obj) {
                    map[obj.dtasktype] = obj;
                    return map;
                }, {});
                var list_data=[];
                for (var item of data) {
                    if (item.tasktype in taskTypeListMap) {
                        item['inc_id'] = taskTypeListMap[item.tasktype].inc_id;
                        item.score = taskTypeListMap[item.tasktype].score;
                        item['oldscore'] = taskTypeListMap[item.tasktype].oldscore;
                        item.totalscore = item.score * item.count;
                        list_data.push(item);
                    }
                }                
                this.$refs.dt_tasktype_sl.datatable.rows
                .add(list_data)
                .draw();  
            }else {
                this.showMessage(this.$t("Failed to read temp TaskType"));//讀取暫時TaskType失敗!
            }
        });  
    },
    bonusSimulationSL(){
        var taskTypeDomList = $(".taskTypeSL_body .textEdit");
        var changeList = []
        for (var taskTypeDom of taskTypeDomList) {
            if ($(taskTypeDom).val() != $(taskTypeDom).attr("oldvalue")) {
                changeList.push({inc_id:$(taskTypeDom).attr("inc_id"), score:$(taskTypeDom).val()})
            }
        }
        if (changeList.length > 0 ) {
            axios.post("/bonus/update_tasktype_sl",this.objectToFormData({"updateList":JSON.stringify(changeList)}))
            .then((response)=>{
                if (response.status==200) {
                    if (this.TaskTypeSl_MaxVerNo != response.data.max_verno) {
                        this.TaskTypeSl_MaxVerNo = response.data.max_verno;
                        this.TaskTypeSl_CurVerNo = this.TaskTypeSl_MaxVerNo == 0 ? 0 :this.TaskTypeSl_MaxVerNo + 1;
                        this.TaskTypeSl_CurDirection = undefined;
                    }
                    $("#tasktypeSLModal").modal("hide");
                    var edatefrom = $("#summary_edatefrom").val();   
                    var edateto= $("#summary_edateto").val();                    
                    $("#lb_progress").html(this.$t("Loading..."));
                    var isChecked = $('#cb_calSat').prop('checked');  
                    this.analyse_bar(edatefrom, edateto, isChecked, true);                        
                }else {
                    this.showMessage(this.$t("Failed to save temp TaskType"));//保存臨時TaskType失敗！
                }
            });                   
        }else {
            $("#tasktypeSLModal").modal("hide");
            var edatefrom = $("#summary_edatefrom").val();   
            var edateto= $("#summary_edateto").val();           
            $("#lb_progress").html(this.$t("Loading..."));
            var isChecked = $('#cb_calSat').prop('checked');  
            this.analyse_bar(edatefrom, edateto, isChecked, true);            
        }
    },
    bonusSimulationSA() {
        var taskTypeDomList = $(".taskTypeSL_body .textEdit");
        var changeList = []
        for (var taskTypeDom of taskTypeDomList) {
            if ($(taskTypeDom).val() != $(taskTypeDom).attr("oldvalue")) {
                changeList.push({inc_id:$(taskTypeDom).attr("inc_id"), score:$(taskTypeDom).val()})
            }
        }
        axios.post("/bonus/update_tasktype_sl?save=true",this.objectToFormData({"updateList":JSON.stringify(changeList)}))
        .then((response)=>{
            if (response.status==200) {
                if (response.data.status) {    
                    if (this.TaskTypeSl_MaxVerNo != response.data.max_verno) {
                        this.TaskTypeSl_MaxVerNo = response.data.max_verno;
                        this.TaskTypeSl_CurVerNo = this.TaskTypeSl_MaxVerNo == 0 ? 0 :this.TaskTypeSl_MaxVerNo + 1;
                        this.TaskTypeSl_CurDirection = undefined;
                    }
                    this.showMessage(this.$t("Save successfully"));//保存TaskType成功
                    $("#tasktypeSLModal").modal("hide"); 
                    var edatefrom = $("#summary_edatefrom").val();   
                    var edateto= $("#summary_edateto").val();                    
                    $("#lb_progress").html(this.$t("Loading..."));
                    var isChecked = $('#cb_calSat').prop('checked');  
                    this.analyse_bar(edatefrom, edateto, isChecked, false);                         
                }else {
                    this.showMessage(this.$t("Fail to save"));//保存TaskType失敗！
                }   
            }
        });                   
    },
    resetSimulationTasktype(direction) {
        var verno = this.TaskTypeSl_CurVerNo ? this.TaskTypeSl_CurVerNo + direction : 0;
        if (this.TaskTypeSl_CurVerNo > 1 && this.TaskTypeSl_CurVerNo < this.TaskTypeSl_MaxVerNo && direction != this.TaskTypeSl_CurDirection)
            verno = this.TaskTypeSl_CurVerNo;
        if (verno > this.TaskTypeSl_MaxVerNo)
            verno = this.TaskTypeSl_MaxVerNo;
        if (verno < 1)
            verno = 1;             
        if (verno > 0 && verno <= this.TaskTypeSl_MaxVerNo) {
            axios.post("/bonus/reset_tasktype_sl", this.objectToFormData({verno:verno,action:direction == -1 ? "undo" : "redo"}))
            .then((response)=>{
                if (response.status==200) {
                    if (response.data.status) {
                        this.TaskTypeSl_CurVerNo = response.data['TaskTypeSl_CurVerNo'];
                        this.TaskTypeSl_CurDirection = response.data['TaskTypeSl_CurDirection'];                        
                        /**
                        this.TaskTypeSl_CurVerNo = verno;
                        this.TaskTypeSl_CurDirection = direction;
                        if (verno == this.TaskTypeSl_MaxVerNo && direction == 1)
                            this.TaskTypeSl_CurVerNo = verno + 1;
                        if (verno == 1 && direction == -1)
                            this.TaskTypeSl_CurVerNo = 0;
                        */
                        this.refresh_tasktype_sl(response.data.data);
                    }else {
                        this.showMessage(this.$t("Fail to rest"));//Rest TaskType失敗！
                    }   
                }
            });        
        }
    },
    get_tasktype_sl_history_maxver() {
        axios.get("/bonus/get_tasktype_sl_history_maxver")
        .then((response)=>{
            if (response.status==200) {
                if (response.data.status) {   
                    this.TaskTypeSl_MaxVerNo = response.data.max_verno;
                    this.TaskTypeSl_CurVerNo = this.TaskTypeSl_MaxVerNo == 0 ? 0 :this.TaskTypeSl_MaxVerNo + 1;
                    if (response.data.TaskTypeSl_CurVerNo != -1) {
                        this.TaskTypeSl_CurVerNo = response.data.TaskTypeSl_CurVerNo;
                    }
                    if (response.data.TaskTypeSl_CurDirection != 0) {
                        this.TaskTypeSl_CurDirection = response.data.TaskTypeSl_CurDirection;
                    }
                }   
            }
        });        
    },
    refresh_tasktype_sl(data) {
        var table_data = this.$refs.dt_tasktype_sl.datatable.rows().data().toArray();
        var taskTypeListMap = data.reduce(function(map, obj) {
            map[obj.dtasktype] = obj;
            return map;
        }, {});
        var list_data=[];
        for (var item of table_data) {
            if (item.tasktype in taskTypeListMap) {
                item['inc_id'] = taskTypeListMap[item.tasktype].inc_id;
                item.score = taskTypeListMap[item.tasktype].score;
                item['oldscore'] = taskTypeListMap[item.tasktype].oldscore;
                item.totalscore = item.score * item.count;
                list_data.push(item);
            }
        }                
        this.$refs.dt_tasktype_sl.datatable.clear().rows
        .add(list_data)
        .draw();  
    },
    budgetAllowance_blur(){
        if(Number(this.BudgetAllowance) != this.contactBonusData["BudgetAllowance"]){
            this.contactBonusData["BudgetAllowance"] = Number(this.BudgetAllowance);
            this.calculate_bonus(this.contactBonusData,false);
        }   
    },
    ratioOFM_blur(){
        if(Number(this.RatioOFM) > 100){
            this.showMessage(this.$t("Ratio of M not more than 100"));//Ratio of M比例不能大於100
            this.RatioOFM = this.contactBonusData["RatioOFM"]; 
            return; 
        }
        if(Number(this.RatioOFM) != this.contactBonusData["RatioOFM"]){
            this.RatioOFS = 100 - Number(this.RatioOFM);
            this.contactBonusData["RatioOFM"] = Number(this.RatioOFM);
            this.contactBonusData["RatioOFS"] = Number(this.RatioOFS);
            this.calculate_bonus(this.contactBonusData,false);
        }           
    },
    ratioOFS_blur(){
        if(Number(this.RatioOFS) != this.contactBonusData["RatioOFS"]){
            this.contactBonusData["RatioOFS"] = Number(this.RatioOFS);
            this.calculate_bonus(this.contactBonusData,false);
        }          
    },
    ratioOFP_blur(){        
        if(Number(this.RatioOFP) != this.contactBonusData["RatioOFP"]){        
            this.contactBonusData["RatioOFP"] = Number(this.RatioOFP); 
            this.calculate_bonus(this.contactBonusData,false);
        } 
    },
    managementRatio_blur(){
        if(Number(this.ManagementRatio) != this.contactBonusData["ManagementRatio"]){
            this.contactBonusData["ManagementRatio"] = Number(this.ManagementRatio);
            this.calculate_bonus(this.contactBonusData,false);
        }       
    },
    unitprice_blur(){
        if(Number(this.UnitPrice) != this.contactBonusData["UnitPrice"]){
            this.contactBonusData["UnitPrice"] = Number(this.UnitPrice);
            this.calculate_bonus(this.contactBonusData,false);
        } 
    },
    performanaceRatio_blur(){
        if(Number(this.PerformanaceRatio) != this.contactBonusData["PerformanaceRatio"]){
            this.contactBonusData["PerformanaceRatio"] = Number(this.PerformanaceRatio);
            this.calculate_bonus(this.contactBonusData,false);
        }           
    },
    restore() { 
        this.contactBonusData = JSON.parse(JSON.stringify(this.cloneBonusData));        
        this.calculate_bonus(this.contactBonusData,false);                
    },
    calculate_bonus(bonusPara,isShowHint=true){   
        axios.get("/bonus/bonus_recalculate",{
            params:{"bonusPara":JSON.stringify(bonusPara)}
        })    
        .then((response)=>{
            var result = response.data;
            if(result.state =='OK'){                
                this.showBonusResult(result.data,isShowHint); 
            }            
        });     
    },
    saveParam(){ 
        var formData = new FormData();
        if (this.contact==""){
            this.showMessage(this.$t("The current user name is empty"));//當前參數用戶名為空
            return;
        }        
        formData.append('username', this.contact);
        formData.append('budgetallowance', this.BudgetAllowance);
        formData.append('managementratio', this.ManagementRatio);
        formData.append('performanaceratio', this.PerformanaceRatio);
        formData.append('unitprice', this.UnitPrice);
        formData.append('salary', this.Salary);
        formData.append('ratioofm', this.RatioOFM);
        formData.append('ratioofp', this.RatioOFP);
        formData.append('ratioofs', this.RatioOFS);

        axios.post("/bonus/bonus/update/{0}".format(contact),formData)
        .then((response)=>{
            if(response.data.status){
                this.showMessage(this.$t("Save successfully"));//保存成功
                this.cloneBonusData = JSON.parse(JSON.stringify(this.contactBonusData));
            }            
        });          
    },
    listenButtonEvent(){        
        var self = this;   
        //刪除扣分記錄
        $("#dt_userdeduction").on("click", ".delete", function(e){
            e.preventDefault(); //阻止按鈕默認動作
            e.stopPropagation();
            var pk = $(this).closest(".SWDropdown").attr("inc_id");
            self.deleteDeductionItem(pk);
        });
        //修改扣分記錄
        $("#dt_userdeduction").on("click", ".edit", function(e){
            e.preventDefault(); //阻止按鈕默認動作
            e.stopPropagation();
            var pk = $(this).closest(".SWDropdown").attr("inc_id");
            axios.get('/bonus/userdeduction/update?pk='+pk)
            .then((response)=>{
                var result = response.data;
                if(result.status){
                    self.currentDeductionItem = result.data;
                    self.deductionItemFormTitle = self.$t("Eidt Penalty");
                    self.$refs.deductionItemForm.$refs.modal.show();
                }
            })
        });
    },
    newDeductionItem(){
        this.currentDeductionItem = {};   
        this.currentDeductionItem['deductiondate']=new Date().toString('yyyy-MM-dd')
        this.deductionItemFormTitle= this.$t("Add Penalty");  
        this.$refs.deductionItemForm.$refs.modal.show();
    },
    submitModalForm() {
      var self = this;
      var url = "/bonus/userdeduction/add";
      if (self.currentDeductionItem.inc_id)
        url = "/bonus/userdeduction/update?pk=" + self.currentDeductionItem.inc_id;
      return new Promise((resolve, reject) => {
        if (!this.currentDeductionItem.deductiondate) {
          self.showMessage(this.$t("The date cannot be null"));//日期不能為空
          reject(false);
        }else if (!this.currentDeductionItem.description) {
          self.showMessage(this.$t("The description cannot be empty"));//描述不能為空
          reject(false);        
        }else if (!this.currentDeductionItem.username) {
          self.showMessage(this.$t("The user name cannot be empty"));//用戶名不能為空
          reject(false);        
        }else if (!this.currentDeductionItem.score) {
          self.showMessage(this.$t("The score cannot be empty"));//分數不能為空
          reject(false);        
        } else {
          axios
            .post(url, self.objectToFormData(self.currentDeductionItem))
            .then((response) => {
              if (!response.data.status) 
                return self.showMessage(response.data.msg.fail);               
              this.$nextTick(function () {
                self.$refs.dt_userdeduction.datatable.draw();
              });
              resolve(response);
            })
            .catch((error) => {
              console.log(error);
              reject(error);
            });
        }
      });
    },
    onDescriptionDesc_change(item){
        var array = item.tptname.split('-')
        if (array.length>1){
            this.currentDeductionItem.penaltyid = array[0];
            this.currentDeductionItem.description = array[1];            
        }else{
            this.currentDeductionItem.description = array[0];
        }
        this.currentDeductionItem.username = item.contact;
        this.getUserPosition();
        
    },
    deleteDeductionItem(pk) {
      //確定刪除嗎?
      if (!confirm(this.$t("Are you sure you want to delete it?"))) return;
      var self = this;
      axios
        .post("/bonus/userdeduction/delete/" + pk)
        .then((response) => {
          if (!response.data.status) return self.showMessage(response.data.msg);
          this.$nextTick(function () {
            self.$refs.dt_userdeduction.datatable.draw();
          });
        })
        .catch((error) => {
          console.log(ereror);
        });
    },
    getUserDeduction() {
      var self = this;
      this.userDeduction_params_fun = () => {       
        return {
          attach_query:
            `{"condition":"AND","rules":[
                {"id":"username","field":"username","type":"string","input":"text","operator":"equal","value":"{0}"},{"id":"deductiondate","field":"deductiondate","type":"string","input":"text","operator":"greater_or_equal","value":"{1}"},{"id":"deductiondate","field":"deductiondate","type":"string","input":"text","operator":"less_or_equal","value":"{2}"}],"not":false,"valid":true}`.format(self.contact,self.global_edatefrom,self.global_edateto),
        };
      };
      this.$nextTick(() => {
        self.$refs.dt_userdeduction.datatable.draw();
      });
    },

    showTaskDetail(task) {
      init_task(task.inc_id);      
    },
    showMessage(msg){
        $('#msg').html(msg);
        $('#messageModal').modal('show'); 
    },
    getBrowser(){
        var isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
        var isSafari = /Safari/.test(navigator.userAgent) && /Apple Computer/.test(navigator.vendor);
        if (isChrome) {
            console.log("Chrome!");
        }
        if (isSafari) {
            $(".col-checker .custom-checkbox .custom-control-label").addClass("iosCheckbox");
        }
    },
    isMobileStyle() {
        if (SWApp.os.isMobile) {
            this.isMobile = true;
        }
    },
    taskExpander(e) {
        e.preventDefault();
        $(".analysis_page").toggleClass("task-expanded");
        $(this.$refs.search_card_accordion).toggleClass("page-expanded");
        this.isExpend = !this.isExpend;
        $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
    },
    design() {
        var tasktypedata = this.$refs.dt_tasktype.datatable.rows().data().toArray();
        tasktypedata = tasktypedata.sort((a, b) => a.tasktype.localeCompare(b.tasktype));
        var data = {variables:{contact:this.contact}, datasource:{tasktypedata:tasktypedata}}

        this.design_report(`/static/PMISLooper/report/TaskTypeReport.mrt`, data);      
    },
    preview() {
        var tasktypedata = this.$refs.dt_tasktype.datatable.rows().data().toArray();
        tasktypedata = tasktypedata.sort((a, b) => a.tasktype.localeCompare(b.tasktype));
        var data = {variables:{contact:this.contact}, datasource:{tasktypedata:tasktypedata}}
        this.preview_report(`/static/PMISLooper/report/TaskTypeReport.mrt`, data);      
    },
    searchFilter(){
        var filter_val = $("#template-users").val();
        var is_dialy = $("#IsDaily").is(":checked") ? "Y" : "N";
        axios.get("/bonus/query/search/",{
            params:{ filter: filter_val, is_dialy: is_dialy }
        })    
        .then((response)=>{
            var result = response.data;
            if(result.state =='OK'){                
                //var result = eval(result.data);
                this.display_filter_list(result.data);
                //$('#no_content').addClass("d-none");
                //$('#card_task').removeClass("d-none");
            }            
        }); 
    },
    display_filter_list(data) {
        var dom = $("#SWListgroup").clone();
        dom.removeAttr("id");
        dom.addClass("SWListgroup");
        var item = dom.find("a");
        dom.empty();
        for(var d of data) {
            var local_item = item.clone();
            dom.append(local_item.prop("outerHTML").render(d));
        }
        $("#search_advanced .pre-scrollable").empty()
        dom.show();
        $("#search_advanced .pre-scrollable").append(dom);

        $('#search_advanced .list-group .list-group-item').on("click", function(e) {
            e.preventDefault()
            $(this).parent().find('.list-group-item').removeClass('active');
            $(this).addClass('active');
        });        
    },
    search_task(){ 
        var self = $("#search_advanced .list-group a.active")[0];
        var id = $(self).attr("pk");           
        //var filter_text = $("#template-users").val();
        var filter_text = $(self).children(".list-group-item-body").text()
        axios.get("/bonus/task_enquiry",{
            params:{ "query_filter_id": id, "sort": "Contact"}
        })    
        .then((response)=>{
            var result = response.data;
            if(result.state =='OK'){                 
                this.isBounsSearch = false; 
                this.setComponent(filter_text);
                this.showTasks(result.data);                
            }            
        });   
    },
    getUserPosition(){
        if(this.currentDeductionItem.username)   
            axios.get("/bonus/userdeduction/get_position",{
                params:{ "contact": this.currentDeductionItem.username}
            })    
            .then((response)=>{
                var result = response.data;
                if(result.status){                 
                    this.currentDeductionItem.position = result.data;         
                }            
            }); 
    },
    //字段排序
    doSort(e){
      var self = $(e.target);
      self.toggleClass("sorting_asc");
      if(self.hasClass("sorting_asc")) {  //升序
        if(self.hasClass("sorting_desc")) {
          self.removeClass("sorting_desc");
        }
        this.bonusData.sort(function(a,b){
            return a.SimulatePerMth - b.SimulatePerMth;
        });
      }else{  // 降序
        self.addClass("sorting_desc");
        this.bonusData.sort(function(a,b){
            return b.SimulatePerMth - a.SimulatePerMth;
        });
      }
    },     
  },
};

</script>
<style>
.dataTables_info {
  display: none;
}
.my-modal-parent {
  position: fixed; 
  z-index: 999999;
}

/* ios LPDataTable 多選樣式 */
.iosCheckbox::before,
.iosCheckbox::after {
    left: 0;
}

.mw_custom {
    max-width: 270px;
}

.enlarged-checkbox {
    transform: scale(2); /* 放大倍数，这里为2 */
}

.noShadowModal .modal-header,
.noShadowModal .modal-footer {
    box-shadow: none;
}

/* sorting */
.sorting {
    cursor: pointer;
}
.sorting .fa-stack {
    width: 1em;
}
.sorting .fa-stack i {
    opacity: .3;
}
.sorting .fa-stack i:last-child {
    top: 1px;
}
.sorting.sorting_asc .fa-stack i:first-child,
.sorting.sorting_desc .fa-stack i:last-child {
    opacity: 1;
}
</style>