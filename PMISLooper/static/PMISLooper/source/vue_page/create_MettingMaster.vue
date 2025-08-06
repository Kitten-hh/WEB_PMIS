<template>
  <div :class="['message flex-grow-1',collapse ?  'messageWidth' : 'messageFullWidth']">
    <div :class="['message-header shadow-sm', collapse ? 'custom_p' : '', lang_code_en ? 'eng_code' : '']">
      <h6 class="mb-0 title d-flex align-items-center mr-md-2">
        <button class="hamburger" type="button" data-original-title="顯示/隱藏" @click="toggleClick()">
          <i class="fas fa-exchange-alt"></i>
        </button>
        <button class="hamburger" type="button" data-original-title="刷新會議" @click="refreshClick()">
          <i class="fas fa-redo-alt"></i>
        </button>
        <ul class="nav nav-tabs border-bottom-0 meeting-header-tabs">
          <li class="nav-item">
            <a class="nav-link font-weight-bold active" data-toggle="tab" ref="meeting_allDetails_a"
              href="#meeting_allDetails"><span class="">{{ $t('Meetings') }}</span> </a>
          </li>
          <li class="nav-item">
            <a class="nav-link font-weight-bold show" data-toggle="tab" href="#meeting_query"><span class="">{{ $t('Query')
            }}</span> </a>
          </li>
          <li class="nav-item">
            <a class="nav-link font-weight-bold show" data-toggle="tab" href="#meeting_manager">
              <span class="d-none d-xl-inline">{{$t('Management Procedure')}}</span> 
              <span class="d-inline d-xl-none">{{$t('Mgn Proc')}}</span> 
            </a>
          </li>
          <!-- <li class="nav-item">
            <a class="nav-link font-weight-bold show" data-toggle="tab" href="#topic_meeting">議題查詢結論</a>
          </li> -->
        </ul>
      </h6>
      <div class="tools ml-1 ml-sm-auto">
        <button type="button" class="btn btn-sm btn-primary mr-sm-2" ref="save_meeting" @click="addMeetingInfo">{{
            $t('Save')
        }}</button>
        <button type="button" class="btn btn-sm btn-light" @click="noDisplay">{{ $t('Cancel') }}</button>
      </div>
    </div>
    <div class="message-body" ref="messageBody">
      <div id="myTabContent" class="tab-content">
        <div class="tab-pane fade active show" id="meeting_allDetails" :style="meetingDetailsStyle">
          <div class="row mx-0 h-100">
            <div class="col-12 col-xl-5 col-xxl-6 col-xxxl-4 left_pane scrollbar">
              <div id="meeting_info_accordion" class="card-expansion">
                <div class="card meeting_info_card card-expansion-item expanded">
                  <div class="card-header border-0" id="meeting_info_heading">
                    <button class="btn btn-reset d-flex justify-content-between w-100" data-toggle="collapse"
                      data-target="#meeting_info_collapse" aria-expanded="true" aria-controls="meeting_info_collapse">
                      <span class="font-weight-bold">{{ $t('Meeting Info') }}</span>
                      <span class="collapse-indicator">
                        <i class="fa fa-fw fa-chevron-down"></i>
                      </span>
                    </button>
                  </div>
                  <div id="meeting_info_collapse" class="collapse show" aria-labelledby="meeting_info_heading"
                    data-parent="#meeting_info_accordion">
                    <div class="card-body pt-0">
                      <form name="mettingform" @submit.prevent="submitMettingForm(metting)">
                        <div class="row">
                          <div class="form-group d-flex meeting-info col-6 mb-2">
                            <label class="col-form-label caption col-auto text-darkblue pl-0" for="tf1">
                              <i class="fas fa-flag fa-fw"></i>
                            </label>
                            <input type="text" v-model="metting.topic" @focus="onprocessFocus" @blur="onprocessBlur"  @input="autoSave" class="form-control col">
                          </div>
                          <div class="form-group d-flex members col-6 mb-2">
                            <label class="col-form-label caption text-darkblue col-auto pl-0">
                              <i class="fas fa-user-friends fa-fw"></i>
                            </label>
                            <LPMultipleSelect2 ref="parSelect2" :selectedItem="metting.participants" :deficiency_add="true" :options="options" @options_change="options_change" @NoResult="NoResult" @input="selected">
                              <option disabled value="0">Select one</option>
                            </LPMultipleSelect2>
                          </div>
                        </div>
                        <div class="form-group mb-2">
                          <label class="col-form-label caption pt-0 text-darkblue" for="summary">
                            <i class="fas fa-comment-dots fa-fw mr-2"></i>{{ $t('Agenda') }}
                          </label>
                          <textarea class="form-control scrollbar" @focus="onprocessFocus" @blur="onprocessBlur"  @input="autoSave" v-model="metting.summary" id="summary"
                            rows="10"></textarea>
                        </div>
                        <div class="form-group mb-0 meetingDiscussion">
                          <div class="d-flex align-items-center justify-content-between pb-2">
                              <label class="col-form-label caption py-0 text-darkblue mr-2" for="process">
                                <i class="fas fa-comment-dots fa-fw mr-2"></i>{{ $t('Discussion') }}
                              </label>
                              <button type="button" class="btn btn-sm btn-light btn-icon text-darkblue" @click="toggleDiscussion($event)">
                                <i :class="[isExpend ? 'fas fa-compress-alt' : 'fas fa-expand-alt']" style="font-size: 15px;"></i>
                              </button>
                          </div>
                          <textarea class="form-control scrollbar" v-model="metting.discussprocess" id="process"
                            rows="8" ref="DiscussionArea" style="resize:none;"
                            @focus="onprocessFocus" @blur="onprocessBlur" @input="autoSave"></textarea>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>
              </div>
              <div id="meeting_topic_accordion" class="card-expansion">
                <LPCard :class_str="'meeting_topics card-expansion-item expanded'" v-for="(subject, index) in subjects"
                  :key="index">
                  <template v-slot:header>
                    <div class="add-subject mr-2" type="button" data-toggle="tooltip" data-placement="bottom"
                      :data-original-title="$t('Add Topic')" @click="addtoolClick()"><i class="fas fa-comment-medical"></i></div>

                    <div class="add-subject mr-2" type="button" data-toggle="tooltip" data-placement="bottom"
                      :data-original-title="$t('Set Topic Results')" @click="show_create_met_items()"><i class="fas fa-file-signature"></i></div>
                      
                    <div class="add-subject mr-2" type="button" data-toggle="tooltip" data-placement="bottom"
                      :data-original-title="$t('View Meeting Topics')" @click="show_meeting_topics()"><i class="fas fa-file"></i></div>


                    <button class="btn btn-reset d-flex justify-content-between w-100" data-toggle="collapse"
                      data-target="#meeting_topic_collapse" aria-expanded="true" aria-controls="meeting_topic_collapse">
                      <span class="font-weight-bold">{{ $t('Topic') }}</span>
                      <span class="collapse-indicator">
                        <i class="fa fa-fw fa-chevron-down"></i>
                      </span>
                    </button>
                  </template>
                  <template v-slot:body>
                    <div id="meeting_topic_collapse" class="collapse show" aria-labelledby="meeting_topic_heading"
                      data-parent="#meeting_topic_accordion">
                      <form name="mettingform" class="px-3 pb-3 pt-0"
                        v-for="(subject_item, index_sub) in subject.subjects" :key="index_sub"
                        @submit.prevent="submitMettingItemForm(subject_item, index, index_sub, 'subjects')">
                        <div class="publisher publisher-alt">
                          <div class="publisher-input mb-0">
                            <LPCombobox url='/looper/metting/get_combobox_topic' ref="topic_LPCombobox"
                              :labelFields="['topic']" valueField='Task' :value="subject_item.task"
                              @on_item_selected="OnTopicChang" @on_Blur="(value) => { subject_item.task = value }" />
                          </div>
                        </div>
                      </form>
                      <form class="px-3 pb-3 pt-0">
                        <div class="form-group">
                          <label class="col-form-label caption text-comblue" for="com_input">{{ $t('Topic Results') }}</label>
                          <input type="hidden" name="com_input">
                          <ol class="conclusion-list pl-4">
                            <form name="mettingform" v-for="(conclusion, index_con) in subject.conclusions"
                              :key="index_con"
                              @submit.prevent="submitMettingItemForm(conclusion, index, index_con, 'conclusions')">
                              <li class="conclusion-list-item" v-bind:title="conclusion.task"
                                :name='"con_li_" + index_con'>
                                <div class="conclusions_item">
                                  <input type="text" v-model="conclusion.task" :name="'con_input_' + index_con" hidden
                                    @blur="DoEdit('conclusions', index, index_con)" class="form-control col">
                                  <div class="conclusions_wrap d-flex align-items-center"
                                    @dblclick="turn_to_task(conclusion)">
                                    <div class="conclusions_content" :name="'con_label_' + index_con">{{ conclusion.task
                                    }}</div>
                                  </div>
                                  <div class="conclusion-actions ml-2">
                                    <span class="badge badge-subtle badge-primary hoperation mr-2">{{ conclusion.hoperation ? conclusion.hoperation.trim() : '' }}</span>
                                    <span class="badge badge-subtle badge-primary taskstatus mr-2">{{ conclusion.progress ? conclusion.progress.trim() : '' }}</span>
                                    <div class="btn btn-sm btn-secondary btn-icon uploadFile" data-toggle="modal"
                                      data-target="#uploadFileDetails" @click="get_file(conclusion.uploadList)"
                                      v-show="conclusion.uploadList.length > 0"><i class="far fa-image"></i></div>
                                    <div class="dropdown ml-2">
                                      <button type="button" class="btn btn-sm btn-icon btn-secondary"
                                        data-toggle="dropdown" aria-expanded="false" aria-haspopup="true">
                                        <i class="fa fa-ellipsis-h"></i>
                                        <span class="sr-only">{{ $t('HOperation') }}</span>
                                      </button>
                                      <div class="dropdown-menu dropdown-menu-right dropdown-scroll scrollbar" style>
                                        <div class="dropdown-arrow mr-n1"></div>
                                        <button type="button" class="dropdown-item" ref="task_switch"
                                          @click="turn_to_task(conclusion)">
                                          <i class="fas fa-file-signature fa-fw mr-2"></i>{{ $t('Task Transfer') }}
                                        </button>
                                        <button class="dropdown-item" type="button"
                                          @click="DoEdit('conclusions', index, index_con)">
                                          <i class="fa fa-pencil-alt fa-fw mr-2"></i>{{ $t('Edit') }}
                                        </button>
                                        <button class="dropdown-item" type="button"
                                          @click="deleteTask(conclusion, index, index_con, 'conclusions')">
                                          <i class="far fa-trash-alt fa-fw mr-2"></i>{{ $t('Delete') }}
                                        </button>
                                        <button class="dropdown-item" type="button" @click="push_data(conclusion)">
                                          <i class="fas fa-cloud-upload-alt fa-fw mr-2"></i>{{ $t('Upload') }}
                                        </button>
                                        <button class="dropdown-item" type="button" @click="turn_topic(conclusion)">
                                          <i class="fas fa-file-signature fa-fw mr-2"></i>{{ $t('Topic Transfer') }}
                                        </button>
                                        <button class="dropdown-item" type="button"
                                          v-for="(hoperations, index_hopselect) in hoperation_select"
                                          :key="index_hopselect"
                                          @click="priority_processing(conclusion, hoperations.value, index, index_con, 'conclusions')">
                                          <i class="fas fa-cloud-upload-alt fa-fw mr-2"></i>{{ hoperations.label.trim() }}
                                        </button>
                                      </div>
                                    </div>
                                  </div>
                                </div>
                              </li>
                            </form>
                          </ol>
                          <div class="publisher">
                            <div class="publisher-input has-clearable pr-0">
                              <button type="button" class="close" @click="clear_data('conclusions')">
                                <span aria-hidden="true">
                                  <i class="fa fa-times-circle"></i>
                                </span>
                              </button>
                              <input id="new-conclusion" ref="conclusions_input" v-model="new_conclusion"
                                @keyup.enter="add_defaultData(index, 'conclusions', false)" class="form-control"
                                :placeholder="$t('Add New Results')" autocomplete="off">
                            </div>
                            <div class="publisher-actions">
                              <div class="publisher-tools pb-0">
                                <button type="button" class="btn btn-secondary" ref="new_conclusion" id="new_conclusion_btn"
                                  @click="add_defaultData(index, 'conclusions', false)">{{ $t('Add') }}</button>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="col-form-label caption text-comblue" for="vtTodos">{{ $t('Further Allocations') }}</label>
                          <input type="hidden" name="vtTodos">
                          <div id="vtTodos" class="todo-list">
                            <form name="mettingform" v-for="(arrange, index_arr) in subject.arranges" :key="index_arr"
                              @submit.prevent="submitMettingItemForm(arrange, index, index_arr, 'arranges')">
                              <div class="todo" :name="'arr_li_' + index_arr" v-bind:title="arrange.task">
                                <div class="custom-control custom-checkbox">
                                  <input type="checkbox" class="custom-control-input" :id="arrange.inc_id"
                                    :value="arrange.task" :checked="false">
                                  <label class="custom-control-label" :for="arrange.inc_id">{{ arrange.task }}</label>

                                </div>
                                <div class="todo-actions pr-1">
                                  <button type="button" class="btn btn-sm btn-light"
                                    @click="deleteTask(arrange, index, index_arr, 'arranges')">{{ $t('Delete') }}</button>
                                </div>
                              </div>
                            </form>
                          </div>
                          <div class="publisher">
                            <div class="publisher-input has-clearable pr-0">
                              <button type="button" class="close" @click="clear_data('arranges')">
                                <span aria-hidden="true">
                                  <i class="fa fa-times-circle"></i>
                                </span>
                              </button>
                              <input id="new-todo" v-model="new_arrange"
                                @keyup.enter="add_defaultData(index, 'arranges', false)"
                                class="form-control form-control-reflow" :placeholder="$t('Add New To Dos')" autocomplete="off">
                            </div>
                            <div class="publisher-actions">
                              <div class="publisher-tools pb-0">
                                <button type="button" class="btn btn-secondary" ref="new_arrange"
                                  @click="add_defaultData(index, 'arranges', false)">{{ $t('Add') }}</button>
                              </div>
                            </div>
                          </div>
                        </div>
                      </form>
                    </div>
                  </template>
                </LPCard>
              </div>
              <div class="card">
                <div class="summary_wrap card-body">
                  <div class="d-flex justify-content-between align-items-center">
                    <h4 class="card-title sum_title py-2 mb-0 font-weight-bold" style="font-size: 15px;">{{ $t('Meeting Summary')
                    }}</h4>
                    <!-- <div class="text-dark"><strong class="text-primary">{{analysis_meeting_notOUL.finish_con}}</strong> / <span>{{analysis_meeting_notOUL.conclusion_con}}</span></div> -->
                  </div>
                  <hr class="my-2">
                  <div class="d-flex flex-column pl-2">
                    <div class="row justify-content-start mb-2">
                      {{ $t('Allocated') }}:
                      <div class="col-auto">
                        <span class="oi oi-media-record text-au mark_icon"></span>
                        {{ $t('Assigned') }} {{ analysis_meeting_notOUL.assigning_con }}
                      </div>
                      <div class="col-auto">
                        <span class="oi oi-media-record text-complete mark_icon"></span>
                        {{ $t('Completed') }} {{ analysis_meeting_notOUL.finish_con }}
                      </div>
                      <div class="col-auto">
                        <span class="oi oi-media-record text-uc mark_icon"></span>
                        {{ $t('Uncomplete') }} {{ analysis_meeting_notOUL.unfinish_con }}
                      </div>
                    </div>
                    <div class="progress progress-sm mb-2">
                      <div class="progress-bar bg-au" role="progressbar"
                        :style="'width: ' + analysis_meeting_notOUL.assigning_ratio + '%;'"
                        :aria-valuetext="analysis_meeting_notOUL.assigning_ratio" aria-valuemin="0" aria-valuemax="100">
                      </div>
                      <div class="progress-bar bg-complete" role="progressbar"
                        :style="'width: ' + analysis_meeting_notOUL.finish_task_ratio + '%;'"
                        :aria-valuetext="analysis_meeting_notOUL.finish_task_ratio" aria-valuemin="0"
                        aria-valuemax="100"></div>
                      <div class="progress-bar bg-uc" role="progressbar"
                        :style="'width: ' + analysis_meeting_notOUL.unfinish_task_ratio + '%;'"
                        :aria-valuetext="analysis_meeting_notOUL.unfinish_task_ratio" aria-valuemin="0"
                        aria-valuemax="100"></div>
                    </div>
                  </div>
                  <hr class="my-2">
                  <div class="row justify-content-start mb-2">
                    <div class="col-auto">
                      <span class=""></span>
                      {{ $t('Void') }}: {{ analysis_meeting_OUL.conclusion_con }}
                    </div>
                  </div>
                </div>
              </div>
              <div id="meeting_accessoryList" class="card-expansion" v-show="accessoryList.length > 0">
                <LPCard :class_str="'meeting_topics card-expansion-item expanded'">
                  <template v-slot:header>
                    <button class="btn btn-reset d-flex justify-content-between w-100" data-toggle="collapse"
                      data-target="#meeting_accessoryList_collapse" aria-expanded="true"
                      aria-controls="meeting_accessoryList_collapse">
                      <span class="font-weight-bold">{{ $t('Attachm List') }}</span>
                      <span class="collapse-indicator">
                        <i class="fa fa-fw fa-chevron-down"></i>
                      </span>
                    </button>
                  </template>
                  <template v-slot:body>
                    <div
                      class="list-group list-group-messages list-group-flush list-group-bordered uploadList collapse show"
                      id="meeting_accessoryList_collapse" aria-labelledby="meeting_accessoryList_heading"
                      data-parent="#meeting_accessoryList">
                      <div class="list-group-item" v-for="(uploadItem, index) in accessoryList" :key="index">
                        <div class="list-group-item-figure pl-0">
                          <span
                            :class="[uploadItem.fileurl == null || uploadItem.fileurl == '' ? 'fa-stack' : 'tile tile-img']"
                            v-if="uploadItem.docname.lastIndexOf('.pdf') >= 0 || uploadItem.docname.lastIndexOf('.jpg') >= 0 || uploadItem.docname.lastIndexOf('.png') >= 0">
                            <template v-if="uploadItem.fileurl == null || uploadItem.fileurl == ''">
                              <i class="fa fa-square fa-stack-2x text-primary"></i>
                              <i class="fa fa-file-image fa-stack-1x fa-inverse"></i>
                            </template>
                            <img :src="uploadItem.fileurl" alt="" v-else>
                          </span>
                          <span v-else class="fa-stack"><i class="fa fa-square fa-stack-2x text-primary"></i> <i
                              class="fa fa-file-pdf fa-stack-1x fa-inverse"></i></span>
                        </div>
                        <div class="list-group-item-body">
                          <h4 class="list-group-item-title text-truncate">
                            <a target="_blank" :href="uploadItem.fileurl"
                              v-if="uploadItem.docname.lastIndexOf('.pdf') >= 0 || uploadItem.docname.lastIndexOf('.jpg') >= 0 || uploadItem.docname.lastIndexOf('.png') >= 0">{{ uploadItem.docname }}</a>
                            <a v-else href="javascript:;">{{ uploadItem.docname }}</a>
                          </h4>
                        </div>
                        <div class="list-group-item-figure pr-0">
                          <button type="button" class="btn btn-sm btn-icon btn-light text-dark"
                            @click="download_task_file(uploadItem)"><i
                              class="oi oi-data-transfer-download"></i></button>
                          <button type="button" class="btn btn-sm btn-icon btn-light text-dark"
                            @click="delete_task_file(uploadItem, index, '1')"><i class="far fa-trash-alt"></i></button>
                        </div>
                      </div>
                    </div>
                  </template>
                </LPCard>
              </div>
            </div>
            <div class="col-12 col-xl-7 col-xxl-6 col-xxxl-8 meeting-full h-100">
              <div class="card mb-3 mb-sm-0 h-100 meetingsDetailsCard">
                <div class="card-header">
                  <ul class="nav nav-tabs card-header-tabs scrollbar">
                    <li class="nav-item">
                      <a class="nav-link font-weight-bold active show meetingsDetailsCardTab1" data-toggle="tab" href="#meeting_details">{{ $t('Details') }}</a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link font-weight-bold meetingsDetailsCardTab2" data-toggle="tab" href="#past_raisedtasks">{{ $t('Past 8 days tasks') }}</a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link font-weight-bold meetingsDetailsCardTab3" data-toggle="tab" href="#yesterday_raisedtasks">{{ $t('Yesterday Unfinished task')
                      }}</a>
                    </li>
                  </ul>
                </div>
                <div class="card-body scrollbar right_pane pt-0">
                  <div id="raisedtasks_MeetingContent" class="tab-content">
                    <div class="tab-pane fade active show" id="meeting_details">
                      <div class="card-expansion mt-3">
                        <LPCard :class_str="'allMeeting_topics card-expansion-item expanded'"
                          v-for="(all_subject, index) in all_subjects" :key="index">
                          <template v-slot:header>
                            <button v-for="(subject, index_sub) in all_subject.subjects" :key="index_sub"
                              class="btn btn-reset d-flex justify-content-between w-100" data-toggle="collapse"
                              :data-target="'#all_subject-' + index" aria-expanded="true"
                              :aria-controls="'#all_subject-' + index">
                              <span class="font-weight-bold text-truncate"><i
                                  class="oi oi-chat text-dark mr-2"></i>{{ subject.task }}</span>
                              <span class="collapse-indicator"> <i class="fa fa-fw fa-chevron-down"></i> </span>
                            </button>
                          </template>
                          <template v-slot:body>
                            <div :id="'all_subject-' + index" class="collapse show">
                              <div class="px-3 pb-3">
                                <div class="log-divider my-1">
                                  <span class="text-darkblue"><i class="far fa-fw fa-comment-alt mr-1"></i>{{ $t('Topic Results')
                                  }}</span>
                                </div>
                                <div class="list-group list-group-messages list-group-flush list-group-bordered topicList">
                                  <div class="list-group-item" v-for="(conclusion, index_con) in all_subject.conclusions"
                                    :key="index_con" @dblclick="turn_to_task(conclusion)">
                                    <div class="list-group-item-figure">
                                      <div class="tile tile-circle bg-blue">{{ conclusion.contact }}</div>
                                    </div>
                                    <div class="list-group-item-body">
                                      <div class="row">
                                        <div class="d-none d-sm-block col-sm-3">
                                          <h4 class="list-group-item-title text-truncate">
                                            {{ conclusion.pid }}-{{ conclusion.tid }}-{{ conclusion.taskid }}</h4>
                                        </div>
                                        <div class="col-12 col-sm-9">
                                          <h4 class="list-group-item-title text-truncate">{{ conclusion.task }}</h4>
                                        </div>
                                      </div>
                                    </div>
                                    <div class="list-group-item-figure">
                                      <span class="badge badge-subtle badge-primary hoperation mr-2">{{ conclusion.hoperation ? conclusion.hoperation.trim() : '' }}</span>
                                      <span class="badge badge-subtle badge-primary taskstatus mr-2">{{ conclusion.progress ? conclusion.progress.trim() : '' }}</span>
                                      <div class="btn btn-sm btn-secondary btn-icon uploadFile" data-toggle="modal"
                                        data-target="#uploadFileDetails" @click="get_file(conclusion.uploadList)"
                                        v-show="conclusion.uploadList.length > 0"><i class="far fa-image"></i></div>
                                    </div>
                                  </div>
                                </div>

                              </div>
                            </div>
                          </template>
                        </LPCard>
                      </div>
                    </div>
                    <div class="tab-pane fade" id="past_raisedtasks">
                      <LPDataTable :paging="false" :paging_inline="true" :searching="1 != 1" :columns="past_raisedtaskscolumns" :datasource="past_raisedtasksdatasource" :custom_options="masterTable.custom_options" @on_row_click="row_click" @on_dbclick="masterTable.dbclick" ref="past_raisedtasksTable" />
                    </div>
                    <div class="tab-pane fade" id="yesterday_raisedtasks">
                      <LPDataTable :paging="false" :paging_inline="true" :searching="1 != 1" :columns="past_raisedtaskscolumns" :datasource="yesterday_raisedtasksdatasource" :custom_options="masterTable.custom_options" @on_row_click="row_click" @on_dbclick="masterTable.dbclick" ref="yesterday_raisedtasksTable" />
                    </div>
                      <AIComBOX v-show="meetingsDetailsCardTab !== 1"  style="height: 300px;"  id="ChatAI" :iframe_src="'http://183.63.205.83:3000/aiChat'"   class="mb-0" :aiPresetQuestion="aiPresetQuestion" :predefinedData="predefinedData"/>
                    
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="tab-pane fade meeting-full" id="meeting_query" ref="meeting_query" :style="{ 'height': meetingQueryHeight + 'px' }">
          <splitpanes class="default-theme" horizontal ref="splitPanes" @resized="onPaneResized" @dblclick="onSplitterDoubleClick">
            <pane class="topPane" size="41">
              <div :class="['pt-1 queryWrap scrollbar', collapse ? '' : 'col_custom', lang_code_en ? 'lang_en' : '']">
                <fieldset class="col-12 meetSearch mb-3 mb-xl-2 card-expansion-item expanded">
                  <legend class="mb-0">
                    <button class="btn btn-reset d-flex justify-content-between prevent-default pl-0" data-toggle="collapse" data-target="#meetingQueryCollapse" aria-expanded="true" aria-controls="meetingQueryCollapse"><span class="collapse-indicator"><i class="fa fa-fw fa-caret-right mr-1"></i></span><span>{{ $t('Meeting Query') }}</span>
                    </button>
                  </legend>
                  <div id="meetingQueryCollapse" class="collapse show form-row">
                    <div :class="['form-group d-flex query_meetingid col-12 col-xxl-2', collapse ? 'order-lg-first order-xl-0 col-lg-4' : 'col-sm-6 order-md-first col-lg-3 order-xl-0 col-xl-2']">
                      <label class="col-form-label caption col-auto pl-0" for="meetingId">{{ $t('Meeting ID') }}</label>
                      <input type="meetingId" class="form-control col" v-model="search.meetingid">
                    </div>

                    <div
                      :class="['form-group d-flex query_meetingTopic col-12 col-xxxl-3', collapse ? 'col-lg-6 col-xl-4' : 'col-sm-6 col-xl-3']">
                      <label class="col-form-label caption col-auto pl-0">{{ $t('Meeting Topic') }}</label>
                      <LPCombobox url='/looper/metting/get_combobox_mettopic' ref="mettopic_LPCombobox" :labelFields="['topic']"
                        valueField='topic' :value="search.meetingtopic" @on_item_selected="(value) => { search.meetingtopic = value.topic }"
                        @on_Blur="(value) => { search.meetingtopic = value }" />
                    </div>
                    
                    <div :class="['form-group d-flex query_agenda col-12 col-xxl-3', collapse ? 'col-lg-6 col-xl-4' : 'col-sm-6 col-xl-3']">
                      <label class="col-form-label caption col-auto pl-0" for="agenda">{{ $t('Agenda') }}</label>
                      <input id="agenda" type="text" class="form-control col" v-model="search.summary">
                    </div>

                    <div
                      :class="['form-group d-flex query_topic col-12 col-xxl-4', collapse ? 'order-lg-first order-xl-0 col-lg-8 col-xl-4' : 'col-sm-6 col-xl-4']">
                      <label class="col-form-label caption col-auto pl-0">{{ $t('Topic') }}</label>
                      <LPCombobox url='/looper/metting/get_combobox_topic' ref="topic_LPCombobox" :labelFields="['topic']"
                        valueField='Task' :value="search.topic" @on_item_selected="(value) => { search.topic = value.topic }"
                        @on_Blur="(value) => { search.topic = value }" />
                    </div>
                    
                    <div :class="['form-group d-flex query_participants col-12 col-xxl-2', collapse ? 'order-lg-first order-xl-0 col-lg-4' : 'col-sm-6 order-md-first col-lg-3 order-xl-0 col-xl-2']">
                      <label class="col-form-label caption col-auto pl-0" for="meetingId">{{ $t('Participants') }}</label>
                      <input type="meetingId" class="form-control col" v-model="search.participants">
                    </div>
                    
                    <div :class="['form-group d-flex query_discussion col-12 col-xxxl-6', collapse ? 'col-xl-12 order-xl-1 order-xxxl-0' : 'order-sm-1 order-lg-0 col-lg-6']">
                      <label class="col-form-label caption col-auto pl-0" for="discussion">{{ $t('Discussion') }}</label>
                      <input id="discussion" type="text" class="form-control col" v-model="search.discussprocess">
                    </div>

                    <div :class="['form-group query_planbdate d-flex col-12 col-xxl-4 col-xxxl-4', collapse ? 'order-lg-first order-xl-0 col-md-12 col-lg-8 col-xl-4' : 'col-sm-6 col-lg-6 col-xl-4']">
                      <label class="col-form-label caption col-auto pl-0" for="planBDates">{{ $t('PlanDate') }}</label>
                      <div class="input-group input-group-alt m-0">
                        <!-- <input id="planBDates" type="text" class="form-control col" data-toggle="flatpickr"
                      v-model="search.plandates" /> -->
                        <LPFlatpickerDate ref="planBDates" id="planBDates" v-model="search.plandates"/>
                        <div class="input-group-append">
                          <span class="input-group-text custom-text">{{ $t('To') }}</span>
                        </div>
                        <!-- <input id="planBDatee" type="text" class="form-control col" data-toggle="flatpickr"
                      v-model="search.plandatee" /> -->
                      <LPFlatpickerDate ref="planBDatee" id="planBDatee" v-model="search.plandatee"/>
                      </div>
                    </div>
                  </div>
                </fieldset>
                  <!-- <div
                    :class="['form-group d-flex col']">
                    <label class="col-form-label caption col-auto pl-0" for="tf1">{{ $t('Meeting State') }}</label>
                    <select class="status_select" data-toggle="selectpicker" data-width="100%" data-none-selected-text
                      v-model="search.meetingstate">
                      <option value=""></option>
                      <option value="N">N:未開始</option>
                      <option value="I">I:正在進行</option>
                      <option value="F">F:已經完成</option>
                    </select>
                  </div> -->
                  <!-- <div
                    :class="['form-group d-flex col-xxl-2 col-xxxl-1-5', collapse ? 'col-sm-6 col-md-6 col-lg-3 col-xl-3' : 'col-sm-4 col-md-4 col-lg-3 col-xl-2']">
                    <label class="col-form-label caption col-auto pl-0">{{ $t('Contact') }}</label>
                    <select class="status_select control" data-toggle="selectpicker" data-width="100%" data-size="5"
                      data-none-selected-text v-model="search.contact">
                      <option></option>
                      <option v-for="(option, inx) in options" :key="inx" :value="option.text">{{ option.text }}</option>
                    </select>
                  </div> -->
                  <fieldset class="col-12 taskSearch card-expansion-item expanded">
                    <legend class="mb-0">
                      <button class="btn btn-reset d-flex justify-content-between prevent-default pl-0" data-toggle="collapse" data-target="#meetingTaskSearchCollapse" aria-expanded="true" aria-controls="meetingTaskSearchCollapse"><span class="collapse-indicator"><i class="fa fa-fw fa-caret-right mr-1"></i></span><span>{{ $t('Task Query') }}</span></button>
                    </legend>
                    <div id="meetingTaskSearchCollapse" class="collapse show form-row">
                      <div :class="['form-group query_req d-flex col-xxxl-4', collapse ? 'order-sm-first order-xxxl-0 col-sm-12 col-md-12 col-lg-8 col-xl-6' : 'order-sm-first col-sm-8 col-md-8 col-lg-6 col-xl-5 col-xxl-4']">
                        <label class="col-form-label caption col-auto pl-0">{{ $t('CreateDate') }}</label>
                        <div class="input-group input-group-alt m-0">
                          <!-- <input id="requestDates" type="text" class="form-control col" data-toggle="flatpickr" v-model="search.createdates"/> -->
                          <LPFlatpickerDate ref="requestDates" id="requestDates" v-model="search.createdates"/>
                          <div class="input-group-append">
                              <span class="input-group-text custom-text">{{ $t('To') }}</span>
                            </div>
                            <!-- <input id="requestDatee" type="text" class="form-control col" data-toggle="flatpickr" v-model="search.createdatee"/> -->
                            <LPFlatpickerDate ref="requestDatee" id="requestDatee" v-model="search.createdatee"/>
                        </div>
                      </div>

                      <div :class="['form-group d-flex query_desc col-xxxl-8', collapse ? 'order-sm_2 order-md-3 order-xl-4 order-xxl-0 col-sm col-md col-lg col-xxl' : 'order-sm-4 col-sm order-lg-4 order-xl-0 col-lg col-xl']">
                        <label class="col-form-label caption col-auto pl-0" for="description">{{ $t('Description') }}</label>
                        <input id="description" type="text" class="form-control col" v-model="search.description">
                      </div>

                      <div :class="['form-group query_planbdate d-flex col-xxxl-4', collapse ? 'order-sm-first order-lg-0 col-sm-12 col-md-12 col-lg-8 col-xl-6' : 'col-sm-8 col-md-8 col-lg-6 col-xl-5 col-xxl-4']">
                        <label class="col-form-label caption col-auto pl-0" for="planBDates">{{ $t('PlanBDate') }}</label>
                        <div class="input-group input-group-alt m-0">
                          <!-- <input id="planBDates" type="text" class="form-control col" data-toggle="flatpickr"
                        v-model="search.planbs" /> -->
                        <LPFlatpickerDate  v-model="search.planbs"/>
                          <div class="input-group-append">
                            <span class="input-group-text custom-text">{{ $t('To') }}</span>
                          </div>
                          <!-- <input id="planBDatee" type="text" class="form-control col" data-toggle="flatpickr"
                        v-model="search.planbe" /> -->
                        <LPFlatpickerDate v-model="search.planbe"/>
                        </div>
                      </div>

                      <div :class="['form-group query_bdate d-flex col-xxxl-4', collapse ? 'col-sm-12 col-md-12 order-lg-2 order-xl-1 col-lg-8 col-xl-6 order-xxxl-0' : 'order-sm-2 col-sm-8 col-md-8 order-lg-0 col-lg-6 col-xl-5 col-xxl-4']">
                        <label class="col-form-label caption col-auto pl-0" for="bDates">{{ $t('BDate') }}</label>
                        <div class="input-group input-group-alt m-0">
                          <!-- <input id="bDates" type="text" class="form-control col" data-toggle="flatpickr" v-model="search.bdatebs" /> -->
                          <LPFlatpickerDate ref="bDates" id="bDates" v-model="search.bdatebs"/>
                          <div class="input-group-append">
                            <span class="input-group-text custom-text">{{ $t('To') }}</span>
                          </div>
                          <!-- <input id="bDates" type="text" class="form-control col" data-toggle="flatpickr" v-model="search.bdatebe"/> -->
                          <LPFlatpickerDate v-model="search.bdatebe"/>
                        </div>
                      </div>
                    
                      <div
                        :class="['form-group d-flex query_contact col-xs-6 col-xxl-2 col-xxxl-1-5', collapse ? 'order-sm-1 col-sm-6 col-md-6 order-lg-first col-lg-4 col-xl-3 order-xxxl-0 ' : 'order-sm-first col-sm-4 col-md-4 col-lg-3 col-xl-2']">
                        <label class="col-form-label caption col-auto pl-0">{{ $t('Contact') }}</label>
                        <select class="status_select control" data-toggle="selectpicker" data-width="100%" data-size="5"
                          data-none-selected-text v-model="search.contact" data-container="body">
                          <option></option>
                          <option v-for="(option, inx) in options" :key="inx" :value="option.text">{{ option.text }}</option>
                        </select>
                      </div> 

                      <div
                        :class="['form-group d-flex query_hoperation col-xs-6 col-12 col-xxl', collapse ? 'order-sm-1 col-sm-6 order-lg-0 col-lg-4 col-xl-3 order-xl-first order-xxl-0' : 'col-sm-4 col-lg-3 col-xl-3']">
                        <label class="col-form-label caption col-auto pl-0" for="tf1">{{ $t('HOperation') }}</label>
                        <select class="status_select" data-toggle="selectpicker" data-width="100%" data-size="5"
                          data-none-selected-text v-model="search.hoperation" data-container="body">
                          <option value=""></option>
                          <option value="empty">空</option>
                          <option v-for="(hoperations, index_hopselect) in hoperation_select" :key="index_hopselect"
                            :value="hoperations.value">{{ hoperations.label }}</option>
                        </select>
                      </div>

                      <div
                        :class="['form-group d-flex query_type col-xs-6 col-12 col-xxl', collapse ? 'order-sm-2 col-sm-6 order-lg-1 col-lg-4 order-xl-2 order-xxl-0' : 'order-sm-1 col-sm-4 col-lg-4  col-xl-2']">
                        <label class="col-form-label caption col-auto pl-0">{{ $t('Type') }}</label>
                        <select class="status_select" data-toggle="selectpicker" data-width="100%" data-none-selected-text
                          v-model="search.classif" data-container="body">
                          <option value=""></option>
                          <option value="0">轉後任務</option>
                          <option value="1">議題結論</option>
                        </select>
                      </div>

                      <div :class="['form-group d-flex query_planedate col-12 col-xxxl-4', collapse ? 'order-sm-first order-lg-3 order-xl-0 col-lg-8 col-xl-6' : 'order-sm-0 col-sm-8 col-lg-6 col-xl-5 col-xxl-4']">
                        <label class="col-form-label caption col-auto pl-0" for="planEDates">{{ $t('PlanEDate') }}</label>
                        <div class="input-group input-group-alt m-0">
                          <!-- <input id="planEDates" type="text" class="form-control col" data-toggle="flatpickr" v-model="search.planes" /> -->
                          <LPFlatpickerDate ref="planEDates" id="planEDates" v-model="search.planes"/>
                          <div class="input-group-append">
                            <span class="input-group-text custom-text">{{ $t('To') }}</span>
                          </div>
                          <!-- <input id="planEDatee" type="text" class="form-control col" data-toggle="flatpickr" v-model="search.planee" /> -->
                          <LPFlatpickerDate ref="planEDatee" id="planEDatee" v-model="search.planee"/>
                        </div>
                      </div>

                      <div :class="['form-group query_edate d-flex col-xxxl-4', collapse ? 'col-sm-12 col-md-12 col-lg-8 col-xl-6 order-xl-1 order-xxxl-0' : 'order-sm-3 col-sm-8 col-md-8 order-lg-0 col-lg-6 col-xl-5 col-xxl-4']">
                        <label class="col-form-label caption col-auto pl-0" for="eDates">{{ $t('EDate') }}</label>
                        <div class="input-group input-group-alt m-0">
                          <!-- <input id="eDates" type="text" class="form-control col" data-toggle="flatpickr" v-model="search.edatees" /> -->
                          <LPFlatpickerDate ref="eDates" id="eDates" v-model="search.edatees"/>
                          <div class="input-group-append">
                            <span class="input-group-text custom-text">{{ $t('To') }}</span>
                          </div>
                          <!-- <input id="eDates" type="text" class="form-control col" data-toggle="flatpickr" v-model="search.edateee" /> -->
                          <LPFlatpickerDate v-model="search.edateee"/>
                        </div>
                      </div>

                      <div
                        :class="['form-group d-flex query_allocation col-xs-6 col-12 col-xxxl-1-5', collapse ? 'order-sm-1 col-sm-6 order-md-2 col-lg-4 order-xl-2 order-xxl-0' : 'order-sm-2 col-sm-4 col-lg-4 col-xl-2']">
                        <label class="col-form-label caption col-auto pl-0" for="tf1">{{ $t('Allocation') }}</label>
                        <select class="status_select" data-toggle="selectpicker" data-width="100%" data-none-selected-text
                          v-model="search.allocation" data-container="body">
                          <option value=""></option>
                          <option value="0">沒有轉</option>
                          <option value="1">有轉</option>
                        </select>
                      </div>
                      <div
                        :class="['form-group d-flex query_progress col-xs-6 col-12 col-xxl', collapse ? 'order-sm-1 col-sm-6 order-lg-3 col-lg-4 order-xl-2 order-xxl-0' : 'order-sm-3 col-sm-4 col-xl-2']">
                        <label class="col-form-label caption col-auto pl-0" for="tf1">{{ $t('Progress') }}</label>
                        <select class="status_select" data-toggle="selectpicker" data-width="100%" data-none-selected-text
                          v-model="search.progress" data-container="body">
                          <option value=""></option>
                          <option value="I">I:正在進行</option>
                          <option value="T">T:當天必須完成任務</option>
                          <option value="N">N:未開始</option>
                          <option value="S">S:已經開始的工作</option>
                          <option value="C">C:基本完成</option>
                          <option value="F">F:已經完成</option>
                          <option value="H">H:此工作被掛起</option>
                          <option value="R">R:要檢測的任務</option>
                          <option value="NF">NF:除F的工作</option>
                          <option value="NFH">NFH:除FH的工作</option>
                        </select>
                      </div>

                      <div :class="['col-auto query_tools order-sm-5', collapse ? 'query_tools_col' : '']">
                        <button type="button" class="btn btn-primary mr-2" @click="clear_search()">{{ $t('Clear') }}</button>
                        <button class="btn btn-primary" type="button" @click="search_Metting()">{{ $t('Search') }}</button>
                      </div>
                  </div>
                  </fieldset>
              </div>
            </pane>
            <pane class="bottomPane" size="59" min-size="30">                  
              <div class="meeting-tasks">
                <div class="queryTaskWrapper scrollbar">
                  <div class="card mb-0">
                    <div class="card-header">
                      <ul class="nav nav-tabs card-header-tabs scrollbar">
                        <li class="nav-item">
                          <a class="nav-link font-weight-bold show" data-toggle="tab" href="#meeting_master">{{ $t('Meeting')
                          }}</a>
                        </li>
                        <li class="nav-item">
                          <a class="nav-link font-weight-bold active meetingDetail" data-toggle="tab" href="#meeting_detail">{{ $t('Meeting Items')
                          }}</a>
                        </li>
                        <li class="nav-item">
                          <a class="nav-link font-weight-bold" data-toggle="tab" href="#meeting_summary">{{ $t('Meeting Summary')
                          }}</a>
                        </li>
                        <li class="nav-item dropdown ml-auto">
                          <a class="nav-link" data-toggle="dropdown" href="#" role="button" aria-expanded="false">
                            <span class="font-weight-bold mr-2">{{ $t('Pre-condition')}}</span>
                            <span v-html="search_selected"></span> 
                            <span class="caret"></span>
                          </a>
                          <div class="dropdown-menu" style="">
                            <div class="dropdown-arrow"></div>
                            <div class="custom-control custom-radio">
                              <input type="radio" class="custom-control-input" checked name="rdGroup1" id="isnull"
                                @click="search_Metting('null', true)">
                              <label class="custom-control-label d-flex justify-content-between" for="isnull">
                                &nbsp;
                              </label>
                            </div>
                            <div class="custom-control custom-radio">
                              <input type="radio" class="custom-control-input" name="rdGroup1" id="eago"
                                @click="search_Metting('5', true)"> <label
                                class="custom-control-label d-flex justify-content-between" for="eago">{{ $t('Past 8 days Meeting')
                                }}</label>
                            </div>
                            <div class="custom-control custom-radio">
                              <input type="radio" class="custom-control-input" name="rdGroup1" id="ncm"
                                @click="search_Metting('3', true)"> <label
                                class="custom-control-label d-flex justify-content-between" for="ncm">{{ $t('Not Complete Meeting')
                                }}</label>
                            </div>
                            <div class="custom-control custom-radio">
                              <input type="radio" class="custom-control-input" name="rdGroup1" id="na"
                                @click="search_Metting('0', true)"> <label
                                class="custom-control-label d-flex justify-content-between" for="na">{{ $t('Not Allocation Tasks')
                                }}</label>
                            </div>
                            <div class="custom-control custom-radio">
                              <input type="radio" class="custom-control-input" name="rdGroup1" id="nd"
                                @click="search_Metting('1', true)"> <label
                                class="custom-control-label d-flex justify-content-between" for="nd">{{ $t('Actual Uncomplete')
                                }}</label>
                            </div>
                            <div class="custom-control custom-radio">
                              <input type="radio" class="custom-control-input" name="rdGroup1" id="fd"
                                @click="search_Metting('4', true)"> <label
                                class="custom-control-label d-flex justify-content-between" for="fd">{{ $t('Prioritized Tasks')
                                }}</label>
                            </div>
                          </div>
                        </li>
                      </ul>
                    </div>
                    <div :class="['card-body meetingMasterDetail scrollbar', isMeetingDetail ? 'py-0' : '']">
                      <div id="myMeetingContent" class="tab-content">
                        <div class="tab-pane fade" id="meeting_master">
                          <div class="masterDetailsCard row">
                            <div :class="[search_meeting.length > 1 ? 'col-6' : 'col-12']"
                              v-for="(meeting, index_search) in search_meeting" :key="index_search">
                              <div class="card mb-0">
                                <div class="card-body">
                                  <div class="media align-items-center justify-content-between flex-wrap">
                                    <h3 class="card-title mb-0 mr-2"><span
                                        class="fa fa-flag mr-2"></span>{{ meeting.meetingData.topic }}</h3>
                                    <span class="meeting_date"><i
                                        class="fas fa-calendar-alt mr-2"></i>{{ meeting.meetingData.id.trim().slice(0, -2).replace(/(.{2})/g, '$1-').substr(0, meeting.meetingData.create_date.trim().length) }}</span>
                                  </div>
                                  <div class="avatar-group avatar-group-sm flex-wrap mt-1"
                                    v-if="meeting.meetingData.participants.length > 0">
                                    <!-- <figure class="user-avatar avatar avatar-circle"
                                      v-for="(participant, index_part) in meeting.meetingData.participants"
                                      :key="index_part">
                                      <span class="avatar-initials">{{ participant }}</span>
                                    </figure> -->
                                    <figure class="user-avatar avatar avatar-circle" data-toggle="tooltip" title="" data-original-title="Andrew Kim" data-container="body"
                                      v-for="(participant, index_part) in meeting.meetingData.participants"
                                        :key="index_part">
                                      <span class="avatar-initials">{{ participant }}</span>
                                    </figure>
                                  </div>
                                  <div class="card shadow-none mb-0">
                                    <div class="log-divider my-1"><span class="text-darkblue"><i
                                          class="far fa-comment-dots fa-fw mr-2"></i>{{ $t('Agenda') }}</span></div>
                                    <div class="card-body query_meetingItem scrollbar">
                                      <div class="conclusions_content" name="con_label_0">{{ meeting.meetingData.summary }}
                                      </div>
                                    </div>
                                  </div>
                                  <div class="card shadow-none mb-0">
                                    <div class="log-divider my-1"><span class="text-darkblue"><i
                                          class="far fa-comment-dots fa-fw mr-2"></i>{{ $t('Discussion') }}</span></div>
                                    <div class="card-body query_discussProcess scrollbar">
                                      <div class="conclusions_content" name="con_label_0">
                                        {{ meeting.meetingData.discussprocess }}</div>
                                    </div>
                                  </div>
                                </div>
                                <div class="card-footer">
                                  <div class="card-footer-item card-footer-item-bordered p-2"><span
                                      class="oi oi-media-record text-au mark_icon fa-fw"></span><strong>{{ meeting.analysisData.assigning_con }}</strong>
                                  </div>
                                  <div class="card-footer-item card-footer-item-bordered p-2"><span
                                      class="oi oi-media-record text-complete mark_icon fa-fw"></span><strong>{{ meeting.analysisData.finish_con }}</strong>
                                  </div>
                                  <div class="card-footer-item card-footer-item-bordered p-2"><span
                                      class="oi oi-media-record text-uc mark_icon fa-fw"></span><strong>{{ meeting.analysisData.unfinish_con }}</strong>
                                  </div>
                                  <div class="card-footer-item card-footer-item-bordered p-2"><span
                                      class="oi oi-media-record text-normal mark_icon fa-fw"></span><strong>{{ meeting.analysisData.undistributed_con }}</strong>
                                  </div>
                                  <div class="card-footer-item card-footer-item-bordered p-2"><span
                                      class="oi oi-media-record text-normal mark_icon fa-fw"></span><strong>{{ meeting.analysisData.unfinishP_con }}</strong>
                                  </div>
                                </div>
                                <div class="card-progress-wrap">
                                  <div class="progress card-progress">
                                    <div class="progress-bar" role="progressbar" style="width: 59%" aria-valuenow="59"
                                      aria-valuemin="0" aria-valuemax="100"></div>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div class="tab-pane fade active show" id="meeting_detail">
                          <LPDataTable :paging="false" :paging_inline="true" :searching="1 != 1" :columns="masterTable.columns" :datasource="masterTable.datasource" :custom_options="masterTable.custom_options" @on_row_click="row_click" @on_dbclick="masterTable.dbclick" ref="meetingDetailTable" />
                        </div>
                        <div class="tab-pane fade" id="meeting_summary">
                          <div class="summary_wrapper">
                            <div class="card-body p-0 meeting_summaryCard">
                              <div class="row mx-0">
                                <div class="col-6 col-sm col-md-6 col-lg-4 col-xxl" v-for="(summarys, index) in summary_list" :key="index">
                                  <div class="metric py-2">
                                    <p class="metric-label"> {{ summarys.title }} </p>
                                    <h5 :class="['metric-value d-flex align-items-center text-primary', index == 2 ? 'text-purple' : '', index == 3 ? 'text-success' : '', index == 4 ? 'text-danger' : '']">
                                      <span class="far fa-check-circle"></span>{{ summarys.statistical }}</h5>
                                  </div>
                                </div>
                              </div>
                            </div>
                            <hr class="sumline">
                            <div class="details_wrapper">
                              <div class="row mx-0">
                                <div class="col-sm-6 col-xl-4 col-xxxl-3" v-for="(summarys, index) in summary_topic" :key="index">
                                  <div class="card card-fluid summaryDetailCard">
                                    <div class="card-header">
                                      <h3 class="card-title mb-0 d-flex align-items-center" style="color: #2e609c;">
                                        <span class="fa fa-flag mr-2"></span>
                                        <span class="text-truncate">{{ summarys.topic }}</span>
                                      </h3>
                                    </div>
                                    <div class="card-body innerBox pt-0">
                                      <ul class="task-inner">
                                        <li class="d-flex align-items-center justify-content-between">
                                          <span class="mr-2">議題結論</span>
                                          <span class="badge badge-subtle badge-primary align-self-start">{{ summarys.taskqty }}</span>
                                        </li>
                                        <li class="d-flex align-items-center justify-content-between">
                                          <span class="mr-2">完成議題結論</span>
                                          <span class="badge badge-subtle badge-primary align-self-start">{{ summarys.taskqty_f }}</span>
                                        </li>
                                        <li class="d-flex align-items-center justify-content-between">
                                          <span class="mr-2">馬上處理議題結論</span>
                                          <span class="badge badge-subtle badge-primary align-self-start">{{ summarys.p_taskqty }}</span>
                                        </li>
                                        <li class="d-flex align-items-center justify-content-between">
                                          <span class="mr-2">完成馬上處理議題結論</span>
                                          <span class="badge badge-subtle badge-primary align-self-start">{{ summarys.p_taskqty_f }}</span>
                                        </li>
                                        <li class="d-flex align-items-center justify-content-between">
                                          <span class="mr-2">未分配任務議題結論</span>
                                          <span class="badge badge-subtle badge-primary align-self-start">{{ summarys.un_taskqty }}</span>
                                        </li>
                                      </ul>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </div>
                            
                            <button ref="btn_expand" type="button" class="btn btn-sm btn-primary btn-floated position-absolute" @click="taskExpander($event)">
                              <i :class="[isExpend ? 'fas fa-compress-alt' : 'fas fa-expand-alt']"></i>
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
    
                </div>
              </div>
            </pane>
          </splitpanes>
        </div>

        <div class="tab-pane fade meeting-full" id="meeting_manager" ref="meeting_manager">
          <div class="row mx-0">
            <div class="col-12 col-xl-12 col-xxl-12 col-xxxl-12 meeting-full">
              <div class="card managerMasterCard">
                <div class="card-body scrollHeight scrollbar">
                  <div class="card-expansion mb-0">
                    <LPDataTable :paging="false" :paging_inline="true" :searching="true" :columns="MMaster_columns" :key="num1"
                      :datasource="MettingmasterView" :pageLength="10" @on_row_click="on_row_click"
                      ref="managerMasterTable" />
                  </div>
                </div>
              </div>
              <div class="card">
                <div class="card-body scrollHeight scrollbar">
                  <div class="card-expansion mb-0" id="managerDetail">
                    <LPDataTable :paging_inline="true" :searching="false" :columns="MDetail_columns"
                      :datasource="MettingdetailView" :pageLength="10" ref="managerDetailTable" :key="num" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <input id="fiAttachment" ref="fiAttachment" type="file" class="custom-file-input" multiple=""
      @change="upload_input_change" hidden>

    <LPModal ref="uploadFileDetails" :title="$t('View File Details')" id="uploadFileDetails">
      <template v-slot:body>
        <div class="list-group list-group-flush list-group-divider uploadList">
          <div class="list-group-item" v-for="(uploadItem, index) in uploadList" :key="index">
            <div class="list-group-item-figure pl-0">
              <span :class="[uploadItem.fileurl == null || uploadItem.fileurl == '' ? 'fa-stack' : 'tile tile-img']"
                v-if="uploadItem.docname.lastIndexOf('.pdf') >= 0 || uploadItem.docname.lastIndexOf('.jpg') >= 0 || uploadItem.docname.lastIndexOf('.png') >= 0">
                <template v-if="uploadItem.fileurl == null || uploadItem.fileurl == ''">
                  <i class="fa fa-square fa-stack-2x text-primary"></i>
                  <i class="fa fa-file-image fa-stack-1x fa-inverse"></i>
                </template>
                <img :src="uploadItem.fileurl" alt="" v-else>
              </span>
              <span v-else class="fa-stack"><i class="fa fa-square fa-stack-2x text-primary"></i> <i
                  class="fa fa-file-pdf fa-stack-1x fa-inverse"></i></span>
            </div>
            <div class="list-group-item-body">
              <h4 class="list-group-item-title text-truncate">
                <a target="_blank" :href="uploadItem.fileurl"
                  v-if="uploadItem.docname.lastIndexOf('.pdf') >= 0 || uploadItem.docname.lastIndexOf('.jpg') >= 0 || uploadItem.docname.lastIndexOf('.png') >= 0">{{ uploadItem.docname }}</a>
                <a v-else href="javascript:;">{{ uploadItem.docname }}</a>
              </h4>
            </div>
            <div class="list-group-item-figure pr-0">
              <button type="button" class="btn btn-sm btn-icon btn-light text-dark"
                @click="download_task_file(uploadItem)"><i class="oi oi-data-transfer-download"></i></button>
              <button type="button" class="btn btn-sm btn-icon btn-light text-dark"
                @click="delete_task_file(uploadItem, index, '0')"><i class="far fa-trash-alt"></i></button>
            </div>
          </div>
        </div>
      </template>
    </LPModal>


    <LPModal ref="ConclusionToTopic" :title="$t('Topic Transfer')" id="ConclusionToTopic">
      <template v-slot:body>
        <div class="form-group row">
          <div class="col">
            <input type="text" class="form-control" id="search_metting" v-model="searchMeeting"
              @keyup.enter="init_tree(searchMeeting)" :placeholder="$t('Meeting ID')">
          </div>
          <button type="button" class="btn btn-primary col-auto" @click="init_tree(searchMeeting)">
            {{ $t('Search') }}
          </button>
        </div>
        <fieldset>
          <legend class="mb-0">{{ $t('Topic Lists') }}</legend>
          <div class="mt-2 mb-3 scrollbar">
            <LPTree ref="lpTree" :data="treeData" @selectNode="nodeSelect" />
          </div>
        </fieldset>
      </template>
      <template v-slot:footer>
        <button type="button" class="btn btn-primary" @click="turn_to_topic()">{{ $t('Confirm') }}</button>
        <button type="button" class="btn btn-light" data-dismiss="modal">{{ $t('Cancel') }}</button>
      </template>
    </LPModal>



    <LPModal ref="create_met_items" :title="$t('Set Topic Results')" id="create_met_items">
      <template v-slot:body>
        <div class="card mt-2">
          <div class="card-header">
            <ul class="nav nav-tabs card-header-tabs border-bottom-0">
              <li class="nav-item">
                <a class="nav-link font-weight-bold active" data-toggle="tab" @click="()=>{create_met_show=true}"
                  href="#tab_create_met_form">
                  <span class="">{{ $t('Discussion Set Results') }}</span>
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link font-weight-bold" data-toggle="tab" @click="()=>{create_met_show=false}"
                  href="#tab_temple_create_met">
                  <span class="">{{ $t('Temp Set Results') }}</span>
                </a>
              </li>
            </ul>
          </div>
          <div class="card-body">
            <div class="tab-content">
              <div class="tab-pane fade meeting-full active show" id="tab_create_met_form" ref="tab_create_met_form">
                <form id="create_met_form">
                  <div class="row flex-column justify-content-center">
                    <div class="col-md-12 form-group d-flex met_items_topic mb-2">
                      <label class="col-form-label caption col-auto pl-0">{{ $t('Topic') }}</label>
                      <LPCombobox url='/looper/metting/get_combobox_topic' ref="topic_LPCombobox" :labelFields="['topic']"
                        valueField='Task' :value="create_met_topic"
                        @on_item_selected="(value) => { create_met_topic = value.topic }"
                        @on_Blur="(value) => { create_met_topic = value }" />
                    </div>
        
                    <div class="col-md-12" id="create_met">
                      <div class="row">
                        <div class="col-12 col-md-2" id="users"></div>
                        <div class="col-12 col-md-2" id="priority_p"></div>
                        <div class="col-12 col-md-2" id="process"></div>
                      </div>
                    </div>
                  </div>
                </form>
              </div>
        
        
              <div class="tab-pane fade meeting-full" id="tab_temple_create_met" ref="tab_temple_create_met">
                <div class="card managerMasterCard">
                  <div class="card-body scrollHeight scrollbar">
                    <div class="card-expansion mb-0">
                      <LPDataTable :paging="false" :paging_inline="true" :searching="true"
                        :columns="MMaster_columns_tab" :key="num1" :datasource="'/looper/metting/MeetingmanagerMastView'"
                        :pageLength="10" @on_row_click="on_row_click_tab" ref="managerMasterTable_tab" />
                    </div>
                  </div>
                </div>
                <div class="card mb-0">
                  <div class="card-body scrollHeight scrollbar">
                    <LPDataTable :paging_inline="true" :searching="false" :columns="MDetail_columns"
                      :datasource="MettingdetailView_tab" :pageLength="10" ref="managerDetailTable_tab" :key="num" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

      </template>
      <template v-slot:footer>
        <div name="tab_create_met_form" v-if="create_met_show" class="d-flex flex-wrap align-items-center justify-content-end m-0">
          <div class="SWCheckbox mr-2">
            <label class="custom-control custom-checkbox mb-0">
                <input type="checkbox" class="custom-control-input control" @click="ischeck_all()" name="ischeck_All" checked="checked">
                <span class="custom-control-label">
                  {{ $t('Select All') }}
                </span>
            </label>    
          </div>
          <button type="button" class="btn btn-primary mr-2" @click="create_met_items()">{{ $t('Confirm') }}</button>
          <button type="button" class="btn btn-light" data-dismiss="modal">{{ $t('Cancel') }}</button>
        </div>
        <div name="tab_temple_create_met m-0" v-else>
          <button type="button" class="btn btn-primary mr-2" @click="create_met_items_temp()">{{ $t('Confirm') }}</button>
          <button type="button" class="btn btn-light" data-dismiss="modal">{{ $t('Cancel') }}</button>
        </div>
      </template>
    </LPModal>



    <LPModal ref="meetingTopic_modal" :title="$t('View Meeting Topic')" id="meetingTopic_modal">
      <template v-slot:body>
        <div class="card mt-2">
          <LPDataTable :paging="false" :paging_inline="true" :searching="true"
            :columns="meetingTopic_columns" :datasource="meetingTopicSource"
            :pageLength="10" ref="meetingTopic_Table" />
        </div>

      </template>
      <template v-slot:footer>
        <div name="tab_temple_create_met m-0">
          <button type="button" class="btn btn-primary mr-2" @click="set_metTopic()">{{ $t('Confirm') }}</button>
          <button type="button" class="btn btn-light" data-dismiss="modal">{{ $t('Close') }}</button>
        </div>
      </template>
    </LPModal>



    <LPModalForm
        id="deductionItemModalForm"
        ref="deductionItemForm"
        :title="deductionItemFormTitle"
        @on_submit="submitModalForm"
    >  
        <LPLabelInput :label="$t('Management Procedure')">
          <LPCombobox url='/looper/metting/get_combobox_topic' ref="topic_LPComdfsbobox" :labelFields="['topic']"
            valueField='Task' :value="search.topic" @on_item_selected="(value) => { search.topic = value.topic }"
            @on_Blur="(value) => { search.topic = value }" />
        </LPLabelInput> 
        <LPLabelInput :label="$t('UserName')">
        <input
            type="text"
            class="form-control"
            v-model="currentDeductionItem.username"
        >
        </LPLabelInput> 
        <LPLabelInput :label="$t('Score')">
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

    <LPMessageModal ref="messageModal" @confirm="onMsgConfirm"/>
  </div>
</template>
    
<script>
import axios from "axios";
import LPMultipleSelect2 from "@components/looper/forms/LPMultipleSelect2.vue";
import LPCard from "@components/looper/layout/LPCard.vue";
import LPModal from "@components/looper/layout/LPModal.vue";
import LPCombobox from "@components/looper/forms/LPCombobox.vue";
import LPTree from "@components/looper/general/LPTree.vue";
import LPDataTable, {DateRender} from "@components/looper/tables/LPDataTable.vue";
import LPFlatpickerDate from "@components/looper/forms/LPFlatpickerDate.vue";
import LPModalForm from "@components/looper/layout/LPModalForm.vue";
import LPLabelInput from "@components/looper/forms/LPLabelInput.vue";
import LPMessageModal from "@components/looper/general/LPMessageModal.vue";
import { Splitpanes, Pane } from 'splitpanes';  // 導入Splitpanes元件和Pane元件
import AIComBOX from './Components/AIComBOX.vue';  
import 'splitpanes/dist/splitpanes.css';

export default {
  //定義頁面控件的名稱為index
  name: "create_MettingMaster",
  components: {
    LPMultipleSelect2,
    LPCard,
    LPModal,
    LPCombobox,
    LPTree,
    LPDataTable,
    LPFlatpickerDate,
    LPModalForm,
    LPLabelInput,
    LPMessageModal,
    Splitpanes,
    Pane,
    AIComBOX,
  },
  props: {
    collapse: Boolean
  },
  data() {
    var self =this;
    return {
      username: get_username(), //登錄用戶名
      strid: "", //會議ID
      met_inc_id: "", //會議inc_id
      sub_inc_id: "", //議題inc_id
      new_conclusion: "", //新結論
      new_arrange: "", //新後續安排
      relationID: "", //
      options: [], //參考人員下拉選擇
      metting: {}, //會議單頭信息
      subjects: [{ 'subjects': [] }], //會議詳細數據
      default_task: {},  //用於
      all_subjects: [{}], //會議詳細數據
      undone_subjects: [], //會議未完成任務數據
      default_session: '', //會議記錄默認session
      search : {
        'contact':'',//記錄聯繫人
        'description':'',//描述查詢輸入框
        'meetingid':'',//會議id查詢輸入框
        'progress':'',//記錄狀態
        'hoperation':'',//操作查詢
        'planbs':'',//計劃開始時間
        'planbe':'',//計劃開始時間
        'planes':'',//計劃開始時間
        'planee':'',//計劃開始時間
        'bdatebs':'',//計劃結束時間
        'bdatebe':'',//計劃結束時間
        'edatees':'',//計劃結束時間
        'edateee':'',//計劃結束時間
        'topic':'',//議題查詢
        'classif':'',//查詢類型
        'allocation':'',//記錄是否分配任務
        'createdates':'',
        'createdatee':'',
        'discussprocess':'',
        'summary':'',
        'meetingtopic':'',
        'participants':'',
        'plandates':'',
        'plandatee':'',
        'meetingstate':''
      },
      search_dec: '', //描述查詢輸入框
      search_metid: '', //會議id查詢輸入框
      search_pro: '',  //記錄狀態
      search_dis: '',//記錄是否分配任務
      search_con: '', //記錄聯繫人
      search_hop: '',//操作查詢
      search_plbs: '',//計劃開始時間
      search_plbe: '',//計劃開始時間
      search_ples: '',//計劃結束時間
      search_plee: '',//計劃結束時間
      search_bs: '',//計劃開始時間
      search_be: '',//計劃開始時間
      search_es: '',//計劃結束時間
      search_ee: '',//計劃結束時間
      search_topic: '',//議題查詢
      search_classif: '',//查詢類型
      file_mes: {},//文件
      task_inc_id: '',
      analysis_meeting_notOUL: {},//分析需要處理會議數據
      analysis_meeting_OUL: {},//分析無需處理會議數據
      accessoryList: [],//本議題所有附件
      metting_old: {},
      search_selected: '', //過去八天下拉選項顯示文本
      search_meeting: [],  //查詢的meeting單頭數據
      hoperation_select: [],//操作查詢下拉列表
      uploadList: [],//上傳文件或圖片
      flagMore: false,
      treeData: [], //樹狀圖數據
      turntopic: {},//轉議題存儲
      searchMeeting: '',//查詢輸入值
      MMaster_columns: [
        { field: "inc_id", label: this.$t('inc_id'), visible: false },
        { field: "tpmastid", label: "序號", visible: false },
        { field: "deptid", label: "部門編號", visible: false },
        { field: "deptname", label: "部門名稱", visible: false },
        { field: "tpno", label: "模板編號", visible: false },
        { field: "tpname", label: "模板名稱", visible: false },
        { field: "category", label: "模板類型", visible: false },
        { field: "t_stamp", label: "更新事件", visible: false },
        { field: "tpdesc", label: "模板描述", visible: false },
        {
          field: "tpdesc", label: "",
          render: function (data, type, full, meta) {
            if (data == null || data == undefined || data == '') return "";
            return String(meta.row + 1) + '.' + data
          }
        },
      ],
      
      MMaster_columns_tab: [
        { field: "inc_id", label: 'inc_id', visible: false },
        { field: "tpmastid", label: "序號", visible: false },
        { field: "deptid", label: "部門編號", visible: false },
        { field: "deptname", label: "部門名稱", visible: false },
        { field: "tpno", label: "模板編號", visible: false },
        { field: "tpname", label: "模板名稱", visible: false },
        { field: "category", label: "模板類型", visible: false },
        { field: "t_stamp", label: "更新事件", visible: false },
        { field: "tpdesc", label: "模板描述", visible: false },
        { field: "tpdesc", label: this.$t("Temp Description") },
      ],
      MettingmasterView: '/looper/metting/MeetingmanagerMastView?manager=2',
      MDetail_columns: [
        // { field: "inc_id", label: "inc_id", visible: false },
        { field: "tpdetailid", label: "序號", visible: false },
        { field: "tpmastid", label: "主表序號", visible: false },
        // { field: "tptname", label: "工作名稱", visible: false },
        { field: "contact", label: "聯繫人", visible: false },
        { field: "priority", label: "優先級", visible: false },
        { field: "status", label: "狀態", visible: false },
        { field: "remark", label: "備註", visible: false },
        { field: "revisedby", label: "創建人", visible: false },
        { field: "t_stamp", label: "更新時間", visible: false },
        { field: "operate", label: "操作", visible: false },
        { field: "cycletime", label: "循環時間", visible: false },
        { field: "cycleperiod", label: "循環週期", visible: false },
        { field: "day", label: "天數", visible: false },
        { field: "invalid", label: "是否作廢", visible: false },
        { field: "sessionid", label: "模板編號", visible: false },
        { field: "tasktype", label: "任務分類", visible: false },
        { field: "subtasktype", label: "子任務分類", visible: false },
        { field: "diff", label: "難度", visible: false },
        {
          field: "tptname", label: "",
          render: function (data, type, full, meta) {
            if (data == null || data == undefined || data == '') return "";
            return String(meta.row + 1) + '.' + data
          }
        },
      ],
      MettingdetailView: [],
      MettingdetailView_tab: [],
      num: 0,
      num1: 0,
      num2: 0,
      topic_search: '',
      topic_columns: [
        { field: "inc_id", label: this.$t('inc_id'), visible: false },
        { field: "pid", label: "pid", visible: false },
        { field: "tid", label: "tid", visible: false },
        { field: "taskid", label: "taskid", visible: false },
        { field: "docpath", label: "會議ID" },
        { field: "task", label: "結論" },
      ],
      topic_Datasoure: [],
      lang_code_en: true,
      create_met_topic:'Mr. Chan Task of the day',
      create_met_show:true,
      summary_list:[],
      summary_topic:[],
      isExpend: false,
      isMeetingDetail: true,
      masterTable:{
        datasource: [],
        columns:[
            { field: "contact", label: gettext('Contact'), 
              render: function(data, type, row) {
                if (data) {
                  return `<div class="tile tile-circle bg-blue">${data}</div>`;
                } else {
                  return "";
                }
              } 
            },
            { field: "taskno", label: gettext('TaskNo'), width: '18%',
              render: function(data, type, row) {
                if (data !== null) {
                  data = row.pid + '-' + row.tid + '-' + row.taskid;
                }
                return data;
              }
            },
            { field: "task", label: gettext('Task'), width: '60%', },
            { field: "planbdate", label: gettext('PlanBDate'), width: '75px', render:DateRender},
            { field: "planedate", label: gettext('PlanEDate'), width: '75px', render:DateRender},
            { field: "hoperation", label: gettext('Hoperation'),
              render: function(data, type, row) {
                if (data) {
                  return `<span class="badge badge-subtle badge-primary hoperation mr-2">${data.trim()}</span>`;
                } else {
                  return "";
                }
              }
            },          
            { field: "progress", label: gettext('Progress'),
              render: function(data, type, row) {
                if (data) {
                  return `<span class="badge badge-subtle badge-primary hoperation mr-2">${data}</span>`;
                } else {
                  return "";
                }
              }
            },
            {
              field: null,
              label: "",
              orderable: false,
              render: function(data, type, row) {
                var id = data.inc_id;  //得當前行的ID
                if(data.uploadList.length > 0){
                  return `<div class="d-flex flex-nowrap"><a href="#" class="btn btn-sm btn-secondary btn-icon uploadFile mr-1" data-toggle="modal"
          data-target="#uploadFileDetails"><i class="fas fa-image"></i></a><a class="btn btn-transfer btn-sm btn-icon btn-secondary mr-1" href="#" id="btnTrans_${id}"><i class="fas fa-file-signature"></i></a><a class="btn btn-delete btn-sm btn-icon btn-secondary" href="#" id="btnDel_${id}"><i class="fas fa-trash-alt"></i></a></div>`;
                }else {
                  return `<div class="d-flex flex-nowrap"><a class="btn btn-transfer btn-sm btn-icon btn-secondary mr-1" href="#" id="btnTrans_${id}"><i class="fas fa-file-signature"></i></a><a class="btn btn-delete btn-sm btn-icon btn-secondary" href="#" id="btnDel_${id}"><i class="fas fa-trash-alt"></i></a></div>`;
                }
              }
            }          
        ],
        custom_options:{
          deferLoading: 0,
          scrollY: true,
          scrollX: true,
          autoWidth: false,
          responsive: false,       
        },
        dbclick:function(data) {
          self.turn_to_task(data);
        },
        ChartAI_input:'',
      },
      //陳生過去八天提問列
      past_raisedtaskscolumns:[
            { field: "contact", label: gettext('Contact'), 
              render: function(data, type, row) {
                if (data) {
                  return `<div class="tile tile-circle bg-blue">${data}</div>`;
                } else {
                  return "";
                }
              } 
            },
            { field: "taskno", label: gettext('TaskNo'), width: '25%',
              render: function(data, type, row) {
                if (data !== null) {
                  data = row.pid + '-' + row.tid + '-' + row.taskid;
                }
                return data;
              }
            },
            { field: "task", label: gettext('Task'), width: '60%', },
            { field: "planbdate", label: gettext('PlanBDate'), width: '75px', render:DateRender},
            // { field: "planedate", label: gettext('PlanEDate'), width: '75px', render:DateRender},
            { field: "hoperation", label: gettext('Hoperation'),
              render: function(data, type, row) {
                if (data) {
                  return `<span class="badge badge-subtle badge-primary hoperation mr-2">${data.trim()}</span>`;
                } else {
                  return "";
                }
              }
            },          
            { field: "progress", label: gettext('Progress'),
              render: function(data, type, row) {
                if (data) {
                  return `<span class="badge badge-subtle badge-primary hoperation mr-2">${data}</span>`;
                } else {
                  return "";
                }
              }
            },      
        ],
      //陳生過去八天提問數據源
      past_raisedtasksdatasource:[],
      //陳生過去昨天提問未完成數據源
      yesterday_raisedtasksdatasource:[],
      //扣分數據
      currentDeductionItem:{},
      //扣分模態框標題
      deductionItemFormTitle:'',
      selected_manager:{},

      meetingTopicSource:[],
      meetingTopic_columns: [
        { field: "task", label: this.$t("Topic") },
      ],
      meetingQueryHeight: '',
      screenWidth: window.innerWidth,
      meetingsDetailsCardTab: 1,
      themeMode: '',
      predefinedData:[], //發給AI的數據
      aiPresetQuestion:[],
      refreshTimer:null,
      saveTimer:null,

    };
  },
  computed: {
    meetingDetailsStyle() {
      if (this.screenWidth >= 1200) {
        return { height: this.meetingQueryHeight + 'px' };
      } else {
        return {}; // 当屏幕宽度小于1200px时不应用任何样式
      }
    }
  },
  mounted() {
    //tooltip 提示工具显示
    $('[data-toggle="tooltip"]').tooltip();
    $('[data-toggle="tooltip"]').on("click", function () {
      $(this).tooltip("hide");
    });
    $('[data-toggle="flatpickr"]').flatpickr();

    this.get_lang_code();

    $('body').on("shown.bs.tab click", "a[data-toggle='tab'], [data-toggle='aside-menu']", function() {
      $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
    });

    var self = this
    this.$nextTick(function () {
      $('.queryTaskWrapper a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        if ($(e.currentTarget).hasClass("meetingDetail")) {
          self.isMeetingDetail = true
        } else {
          self.isMeetingDetail = false
        }

      });
      
      $('.meetingsDetailsCard .card-header-tabs a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        if ($(e.currentTarget).hasClass("meetingsDetailsCardTab2")) {
          self.meetingsDetailsCardTab = 2
          console.log($(e.currentTarget))
        } else if ($(e.currentTarget).hasClass("meetingsDetailsCardTab3")) {
          self.meetingsDetailsCardTab = 3
        } else if ($(e.currentTarget).hasClass("meetingsDetailsCardTab1")) {
          self.meetingsDetailsCardTab = 1
        }
      });

      this.getMeetingQueryHeight();
      $('.meeting-header-tabs a[data-toggle="tab"]').on("shown.bs.tab", function (e) {
        self.getMeetingQueryHeight();
      })

      var penalty_btn = '<div class="input-group-append"><button class="btn btn-primary" data-toggle="modal"  id="Penalty_btn">' + this.$t("Penalty") + '</button></div>'

      $('#meeting_manager .managerMasterCard .LPDataTable .input-group-alt').append(penalty_btn)
      $('#meeting_manager #Penalty_btn').on('click', function () {
        window.open('/bonus/main_page#/?penalty=Y')
      })
  })

    window.addEventListener('resize', this.getMeetingQueryHeight);
    this.refreshTimer = setInterval(() => {
      this.fetchMeetingData();
    }, 10000);

    $(window).on('resize', function () {
      $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
    });
  },
  created() {
    var self = this
    self.init_params();
    self.init_metting();
    self.init_contact();
    self.init_hoperation_select();
    self.init_subjects();
    self.init_all_subject();
    self.get_past_raisedtasks();
    self.get_yesterday_raisedtasks()
    window.setTimeout(function () {
      self.init_undone_subject();
      self.init_analysis_meeting();
      self.init_tree('-8')
      self.get_MeetingTopicSource()
      self.init_aiPresetQuestion()
      // $('[data-toggle="flatpickr"]').flatpickr();
    }, 1000);
    window.setTimeout(function () {
      $(".status_select").selectpicker('refresh');
      self.sendDataToReact();
    }, 2000);
  },
  beforeDestroy() {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer);
    }
  },
  methods: {
    autoSave() {
      // 1. 清空之前的計時器
      clearTimeout(this.saveTimer);
      // 2. 重新設置 10 秒的延時計時器
      this.saveTimer = setTimeout(() => {
        this.addMeetingInfo();
        clearTimeout(this.saveTimer);
      }, 10000);
    },
    fetchMeetingData() {
      var self = this
      self.init_metting();
      // self.init_subjects();
    },
    //初始化獲取參數
    init_params() {
      //获取參數會議ID和參會人員
      this.strid = this.$route.query.id;
      this.met_inc_id = this.$route.query.inc_id;
      this.sub_inc_id = this.$route.query.sub_inc_id;
      axios
        .get("/PMIS/global/get_typelist?type_name=mettingsession")
        .then(response => {
          if (response.data.status) {
            this.default_session = response.data.data[0]['value']
            axios
              .get("/PMIS/task/add_task", {
                params: { contact: this.username, sessionid: this.default_session }
              })
              .then(response => {
                if (response.data.status) {
                  response.data.data['uploadList'] = []
                  this.default_task = response.data.data
                }
              });
          }
        });
    },
    onprocessFocus() {
      this.isprocessFocused = true;
      // 如果需要的話，這裡可以做一些額外操作
    },
    onprocessBlur() {
      this.isprocessFocused = false;
      // 如果需要的話，這裡可以做一些額外操作
    },
    //初始化Metting單頭
    init_metting() {
      //當參數met_inc_id不為空時表示修改某會議信息
      if (this.met_inc_id != null) {
        axios
          .get(`/looper/metting/MettingmasterUpdateView?pk=${this.met_inc_id}`)
          .then(response => {
            // 處理成功後的返回數據
            if (response.data.status) {
              // if (response.data.data.participants != null) {
              //   //重構參會人員信息將其改為下拉框選擇對應id的數組
              //   var participant = response.data.data.participants.split(",");
              //   var values = [];
              //   for (var strkey of participant) {
              //     if (strkey != "") {
              //       for (var option of this.options) {
              //         if (option.text == strkey) {
              //           values.push(String(option.id));
              //           break;
              //         }
              //       }
              //     }
              //   }
              //   console.log(values)
              //   $(this.$refs.parSelect2.$refs.multipleSelect)
              //     .val(values)
              //     .trigger("change");
              // }

              if(this.metting.inc_id!==response.data.data.inc_id || 
                this.metting.modi_date==undefined || this.metting.modi_date.trim()<response.data.data.modi_date.trim()){
                if(!this.isprocessFocused){
                  this.metting = response.data.data;
                  this.metting_old = JSON.parse(JSON.stringify(this.metting));
                }
              }
            }
          });
      } else {
        axios
          .get(
            `/looper/metting/MettingmasterCreateView?contact=${get_username()}`
          )
          .then(response => {
            if (response.data.status) {
              if(!this.isprocessFocused){
                if(this.strid!=undefined && this.strid!=null && this.strid!='' && response.data.data.id!=this.strid)
                  response.data.data.id = this.strid
                this.metting = response.data.data;
                this.$emit("create_meeting", response.data.data);
                this.metting_old = JSON.parse(JSON.stringify(this.metting));
              }
            }
          });
      }
    },
    //初始化參會人員選項
    init_contact() {
      axios.get(`/PMIS/user/get_part_user_names`)
        .then(response => {
          if (response.data.data.length > 0) {
            var contacts = [];
            response.data.data.forEach((strkey, index) => {
              contacts.push({ id: index, text: strkey });
            });
            this.options = contacts;
          }
        });
    },
    //初始化會議詳細信息
    init_subjects() {
      //獲取用戶會議記錄信息
      axios
        .get(`/looper/metting/get_metting_item`, {
          params: { id: this.strid, subject: this.sub_inc_id }
        })
        .then(response => {
          var keys = ["subjects"];
          //若存在會議記錄則顯示，否則默認創建三條會議記錄輸入框
          if (response.data.status) {
            this.subjects = response.data.data;
          }
          for (var strkey of keys) {
            if ((this.subjects[0][strkey] === undefined) || (this.subjects[0][strkey].length==0)){
              this.add_defaultData(0, strkey, true);
            }
          }
        });
    },
    //初始化會議所有議題及相關信息
    init_all_subject() {
      //獲取用戶會議記錄信息
      axios
        .get(`/looper/metting/get_metting_item`, {
          params: { id: this.strid, status: 'Browse' }
        })
        .then(response => {
          //若存在會議記錄則顯示，否則默認創建三條會議記錄輸入框
          if (response.data.status) {
            this.all_subjects = response.data.data;
          }
        });
    },
    //初始化前八天未完成會議信息
    init_undone_subject() {
      this.search_Metting('null', true)
    },
    //初始化meeting統計數據
    init_analysis_meeting() {
      axios
        .get(`/looper/metting/analysis_meeting`, {
          params: { id: this.strid }
        })
        .then(response => {
          //若存在會議記錄則顯示，否則默認創建三條會議記錄輸入框
          if (response.data.status) {
            if (response.data.data.length > 0) {
              this.analysis_meeting_notOUL = response.data.data[0]['analysisData_hastask'];
              this.analysis_meeting_OUL = response.data.data[0]['analysisData_nottask'];
              this.accessoryList = response.data.data[0]['accessoryList'];
            }
          }
        });
    },
    //初始化操作查詢下拉列表
    init_hoperation_select() {
      axios
        .get(`/PMIS/global/get_typelist?type_name=HOperation_Type`)
        .then(response => {
          //若存在會議記錄則顯示，否則默認創建三條會議記錄輸入框
          if (response.data.status) {
            this.hoperation_select = response.data.data;
          }
        });
    },
    init_aiPresetQuestion(sessionid='11580-520'){
      axios
        .get(`/looper/task/get_requirement_task?sessionid=${sessionid}`)
        .then(response => {
          //若存在會議記錄則顯示，否則默認創建三條會議記錄輸入框
          if (response.data.status) {
            var result = []
            for(var item of response.data.data){
              if(item['taskid']!='10'){
                // result.push({
                //   message: item['task'],
                //   sender: "System",
                //   direction: "incoming"
                // })
                
                result.push(item['task'])
              }
            }
            this.aiPresetQuestion = result
          }
        });
    },
    //保存按鈕點擊方法
    async addMeetingInfo() {
      this.$refs.save_meeting.setAttribute('disabled', true);
      //當結論或後續安排輸入框存在內容時將其寫入對應列表中
      if (this.new_conclusion != '') {
        var newconclusion = this.default_task
        newconclusion.editionid = "3";
        newconclusion.task = this.new_conclusion;
        if (this.subjects[0]["conclusions"] == undefined) { this.subjects[0]["conclusions"] = []; }
        this.subjects[0]["conclusions"].push(newconclusion);
        this.new_conclusion = "";
      }
      if (this.new_arrange != '') {
        var newarrange = this.default_task
        newarrange.editionid = "4";
        newarrange.task = this.new_arrange;
        if (this.subjects[0]["arranges"] == undefined) { this.subjects[0]["arranges"] = []; }
        this.subjects[0]["arranges"].push(newarrange);
        this.new_arrange = "";
      }
      //當會議摘要或討論過程沒改變時設置其值為null(後台將不修改該字段內容)
      if (this.metting_old['discussprocess'] === this.metting['discussprocess']) this.metting['discussprocess'] = null
      if (this.metting_old['summary'] === this.metting['summary']) this.metting['summary'] = null
      var self = this;
      var keys = ["conclusions", "arranges"];
      //設置結���和後續安排的關聯議題和關聯會議，並設置序號
      for (var i = 0; i < this.subjects.length; i++) {
        var strkey_sub = self.subjects[i];
        this.submitMettingItemForm(strkey_sub["subjects"][0], i, 0, "subjects")
        for (var skey of keys) {
          if (strkey_sub[skey] != undefined) {
            for (var j = 0; j < strkey_sub[skey].length; j++) {
              self.submitMettingItemForm(strkey_sub[skey][j], i, j, skey);
            }
          }
        }
      }
      //格式化參會人員字段並生成數據的對象
      this.submitMettingForm(this.metting);
    },
    //格式化參會人員字段並生成數據的對象
    submitMettingForm(metting) {
      //格式化參會人員字段
      var participant = "";
      var participants = $(".select2-hidden-accessible").val();
      if (participants.length > 0) {
        participants.forEach((strkey, index) => {
          var strtext = "";
          for (var item of this.options) {
            if (String(item.id) === strkey) {
              strtext = item.text;
              break;
            }
          }
          participant = index == participants.length - 1 ? (participant += strtext) : (participant += strtext + ",");
        });
      }
      metting.participants = participant;
      var metid=metting.id
      //生成數據的對象
      let data = this.objectToFormData(metting);

      //當存在議題結論等信息時將其寫入數據對象中
      if (this.subjects[0]['subjects'][0].task != null || this.subjects[0]['conclusions'] != undefined || this.subjects[0]['arranges'] != undefined) {
        data.append("details", JSON.stringify(this.subjects));
      }
      //當會議記錄存在inc_id字段值時表示該數據已保存過
      if (metting.inc_id != "" && metting.inc_id != null && metting.inc_id != undefined) {
        this.update_Metting(data, metting.inc_id);
      } else {
        this.Create_check(metid,data);
      }
    },
    Create_check(metid,mitdata){
        axios
          .get(`/looper/metting/get_Mettingma?metid=${metid}`)
          .then(response => {
            if (response.data.status) {
              this.$refs.save_meeting.removeAttribute('disabled');
              if(response.data.data.length==0)
                this.create_Metting(mitdata);
              else{
                this.$refs.messageModal.message = this.$t('upgrade the ID of an existing conference') 
                this.$refs.messageModal.type = 1 
                this.$refs.messageModal.data = mitdata
                this.$refs.messageModal.operate = "create_met"
                $('#messageModal').modal('show')
              }
            }
          });
    },
    //新增會議單頭記錄
    create_Metting(data) {
      // 使用axios的post方式調用以上發布的CreateView
      axios
        .post(`/looper/metting/MettingmasterCreateView`, data)
        .then(response => {
          // 處理成功後的返回數據
          if (response.data.status) {
            this.metting = response.data.data.instance;
            this.metting_old = JSON.parse(JSON.stringify(this.metting));
            if (response.data.other != undefined) {
              if (this.subjects[0]['conclusions'] == undefined || this.subjects[0]['conclusions'] == null) this.subjects[0]['conclusions'] = []
              if (response.data.other['conclusions'] == undefined || response.data.other['conclusions'] == null) response.data.other['conclusions'] = []
              response.data.other['conclusions'] = this.uploadList_format(this.subjects[0]['conclusions'], response.data.other['conclusions'])
              this.subjects = [response.data.other]
            }
            if(!this.saveTimer)
              alert("新增成功！");
            this.$emit("refresh_tree", '-8');
            if (this.$route.query.sub_inc_id == null || this.$route.query.sub_inc_id == undefined) {
              var sub_inc_id = ''
              if (this.subjects[0]['subjects'] != undefined) { sub_inc_id = this.subjects[0]['subjects'][0].inc_id }
              this.$router.push({ path: '/create', query: { 'status': "edit", 'id': this.metting.id, 'inc_id': this.metting.inc_id, 'sub_inc_id': sub_inc_id } });
            }
            this.init_all_subject();
            this.init_analysis_meeting();
          }
        })
        .catch(error => {
          console.log(error);
        })
        .finally(() => {
          this.$refs.save_meeting.removeAttribute('disabled');
        });
    },
    //修改會議單頭記錄
    update_Metting(data, inc_id) {
      // 使用axios的post方式調用以上發布的UpdateView
      axios
        .post(`/looper/metting/MettingmasterUpdateView?pk=${inc_id}`, data)
        .then(response => {
          // 處理成功後的返回數據
          if (response.data.status) {
            // if(response.data.data.instance['summary'] == null || response.data.data.instance['summary'] =='')response.data.data.instance['summary'] = this.metting_old['summary']
            // if(response.data.data.instance['discussprocess'] == null || response.data.data.instance['discussprocess'] =='')response.data.data.instance['discussprocess'] = this.metting_old['discussprocess']
            this.metting = response.data.data.instance;
            this.metting_old = JSON.parse(JSON.stringify(this.metting));
            if (response.data.other != undefined) {
              if (this.subjects[0]['conclusions'] == undefined || this.subjects[0]['conclusions'] == null) this.subjects[0]['conclusions'] = []
              if (response.data.other['conclusions'] == undefined || response.data.other['conclusions'] == null) response.data.other['conclusions'] = []
              response.data.other['conclusions'] = this.uploadList_format(this.subjects[0]['conclusions'], response.data.other['conclusions'])
              this.subjects = [response.data.other]
            }
            if(!this.saveTimer)
              alert("修改成功！");
            this.$emit("refresh_tree", '-8');
            if (this.$route.query.sub_inc_id == null || this.$route.query.sub_inc_id == undefined) {
              var sub_inc_id = ''
              if (this.subjects[0]['subjects'] != undefined) { sub_inc_id = this.subjects[0]['subjects'][0].inc_id }
              this.$router.push({ path: '/create', query: { 'status': "edit", 'id': this.metting.id, 'inc_id': this.metting.inc_id, 'sub_inc_id': sub_inc_id } });
            }
            this.init_all_subject();
            this.init_analysis_meeting();
          }
        })
        .catch(error => {
          console.log(error);
        })
        .finally(() => {
          this.$refs.save_meeting.removeAttribute('disabled');
        });
    },
    //設置結論和後續安排的關聯議題和關聯會議，並設置序號
    submitMettingItemForm(subject_item, index, index_sub, strkey) {
      if (strkey != "subjects") {
        var subject = this.subjects[index].subjects[0];
        subject_item.relationid = subject.pid + "-" + String(subject.tid) + "-" + String(subject.taskid);
      }
      if (subject_item.contact == null)
        subject_item.contact = this.username;
      if (subject_item.docpath == null)
        subject_item.docpath = this.metting.id;
      if (subject_item.rank == null)
        subject_item.rank = index_sub;
    },
    //保存後獲取原文件列表
    uploadList_format(old_subjects, new_subjects) {
      var result = []
      for (var old_subject of old_subjects) {
        for (var i = 0; i < new_subjects.length; i++) {
          if (new_subjects[i]['inc_id'] == old_subject['inc_id']) {
            new_subjects[i]['uploadList'] = old_subject['uploadList']
            result.push(new_subjects[i])
            new_subjects.splice(i, 1)
            break;
          }
        }
      }
      if (new_subjects.length > 0) {
        for (var new_subject of new_subjects) {
          new_subject['uploadList'] = []
          result.push(new_subject)
        }
      }
      return result
    },
    //增加默認值
    add_defaultData(index, strkey, Isdefault) {
      axios
        .get("/PMIS/task/add_task", {
          params: { contact: this.username, sessionid: this.default_session }
        })
        .then(response => {
          if (response.data.status) {
            switch (strkey) {
              case "subjects":
                response.data.data.editionid = "1";
                break;
              case "conclusions":
                response.data.data.editionid = "3";
                response.data.data.task = this.new_conclusion;
                response.data.data['uploadList'] = [];
                this.new_conclusion = "";
                break
              case "arranges":
                response.data.data.editionid = "4";
                response.data.data.task = this.new_arrange;
                this.new_arrange = "";
                break
            }
            if (this.subjects[index][strkey] == undefined) {
              this.subjects[index][strkey] = [];
              this.subjects[index][strkey].push(response.data.data);
            }else if (this.subjects[index][strkey].length==0){
              this.subjects[index][strkey].push(response.data.data);
            } else {
              if (!Isdefault) {
                this.subjects[index][strkey].push(response.data.data);
              }
            }
          }
        });
    },
    //清除增加輸入框內容
    clear_data(strkey) {
      switch (strkey) {
        case "conclusions":
          this.new_conclusion = "";
          break;
        case "arranges":
          this.new_arrange = "";
          break;
      }
    },
    //議題結論修改
    DoEdit(strkey, index, index_con) {
            switch (strkey) {
        // case "subjects":
        //   response.data.data.editionid = "1";
        //   break;
        case "conclusions":
          if ($("[name='con_input_" + index_con + "']").is(':hidden')) {
            $("[name='con_label_" + index_con + "']").prop("hidden", "hidden");
            $("[name='con_input_" + index_con + "']").removeAttr("hidden");
            setTimeout(function () {
              $("[name='con_input_" + index_con + "']").focus();
            }, 50)
          } else {
            $("[name='con_label_" + index_con + "']").removeAttr("hidden");
            $("[name='con_input_" + index_con + "']").prop("hidden", "hidden");
                      }
          break
        case "arranges":
          if ($("[name='arr_input_" + index_con + "']").is(':hidden')) {
            $("[name='arr_label_" + index_con + "']").prop("hidden", "hidden");
            $("[name='arr_input_" + index_con + "']").removeAttr("hidden");
          } else {
            $("[name='arr_label_" + index_con + "']").removeAttr("hidden");
            $("[name='arr_input_" + index_con + "']").prop("hidden", "hidden");
          }
          break
      }
    },
    //刪除議題記錄或安排
    deleteTask(data, index, index_sub, strkey) {
      if (confirm("你確定要刪除該結論?")) {
        if (data.inc_id != null) {
          axios
            .post(`/PMIS/task/delete_task/${data.inc_id}`)
            .then(response => {
              if (response.data.status) {
                if (strkey === 'undone_subject') {
                  this.undone_subjects.splice(index_sub, 1)
                } else {
                  this.subjects[index][strkey].splice(index_sub, 1)
                }
              }
            })
            .catch(error => {
              console.log(error);
            });
        } else {
          if (strkey === 'undone_subject') {
            this.undone_subjects.splice(index_sub, 1)
          } else {
            this.subjects[index][strkey].splice(index_sub, 1)
          }
        }
      }
    },
    //顯示隱藏按鈕點擊方法
    toggleClick() {
      this.$emit('toggleClick');
      window.setTimeout(function () {
        $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
      }, 200);
    },
    //新增議題
    addtoolClick() {
      if (this.metting.inc_id != null) {
        var status = this.$route.query.status == 'add' ? 'edit' : 'add'
        this.$router.push({ path: '/create', query: { 'status': status, 'id': this.metting.id, 'inc_id': this.metting.inc_id } });
      } else {
        alert('請先選擇會議！')
      }
    },
    //查詢summery
    search_Metting(search_dis = '', isClick = false) {
      //初始化查詢字段值字典
      var search = {'contact':'','description':'','meetingid':'','progress':'','hoperation':'','planbs':'','planbe':'',
                    'planes':'','planee':'','bdatebs':'','bdatebe':'','edatees':'','edateee':'','topic':'',
                    'classif':'','allocation':search_dis,'createdates':'','createdatee':'',
                    'discussprocess':'','summary':'','meetingtopic':'','participants':'','plandates':'','plandatee':'','meetingstate':''}
      //判定是否為預查詢，若不是則將輸入框內字段值寫入字典search中
      if (search_dis != '' && isClick) {
        this.search_dis = search_dis
        var search_keys = Object.keys(search)
        //檢驗查詢條件是否存在內容
        for(var key of search_keys){
          search[key] = search[key]==''?this.search[key]:search[key]
        }
      } else {
        var search_keys = Object.keys(search)
        //檢驗查詢條件是否存在內容
        for(var key of search_keys){
          search[key] = this.search[key]
        }
        search['allocation'] = search_dis
      }
      if(isClick==false)search['allocation']=this.search['allocation']=='null'?'':this.search['allocation']
      //當是預查詢選項時根據選中的選項顯示不同的選項翻譯並設置部分字段值
      if(isClick){
        switch(search_dis){
          case 'null':
            this.search_selected = this.$t('Null')
            break
          case '0':
            this.search_selected = this.$t('Not Allocation Tasks')
            break
          case '1':
            this.search_selected = this.$t('Actual Uncomplete')
            search['progress'] = '0'
            break
          case '3':
            this.search_selected = this.$t('Not Complete Meeting')
            search['progress'] = '0'
            break
          case '4':
            this.search_selected = this.$t('Prioritized Tasks')
            break
          case '5':
            this.search_selected = this.$t('Past 8 days Meeting')
            break
        }
      }
      //獲取用戶會議記錄信息
      axios
        .get(`/looper/metting/get_metting_undone`, {
          params:search
        })
        .then(response => {
          //若存在會議記錄則顯示，否則默認創建三條會議記錄輸入框
          if (response.data.status) {
            var detail = response.data.data[0]['detail']
            //格式化計劃時間格式
            for (var subject of detail) {
              subject.planbdate = new Date(subject.planbdate).format('yyyy-MM-dd')
              subject.planedate = new Date(subject.planedate).format('yyyy-MM-dd')
            }
            this.undone_subjects = detail;
            this.search_meeting = response.data.data[0]['master'];
            this.summary_list = response.data.data[0]['summary'];
            this.summary_topic = response.data.data[0]['summary_topic'];
            this.$refs.meetingDetailTable.datatable.clear().rows.add(this.undone_subjects).draw();
            $(this.$refs.meetingDetailTable.table).removeClass("table-striped");
          }
        });
    },
    //設置結論優先處理
    priority_processing(conclusion, priority, index, index_sub, strkey) {
      if (conclusion.hoperation == priority) {
        alert('該結論已設置為該操作，無需重複設置!')
        return
      }
      conclusion.hoperation = priority
      if (priority == 'P') conclusion.class_field = 1
      this.updateTask(conclusion, index, index_sub, strkey)
    },
    //更新Task表
    updateTask(task, index, index_sub, strkey) {
      //獲取該結論的附件內容
      var uploadList = this.subjects[index][strkey][index_sub]['uploadList']
      axios
        .post(`/PMIS/task/update_task?pk=${task.inc_id}`, this.objectToFormData(task))
        .then(response => {
          // 處理成功後的返回數據
          if (response.data.status) {
            //重新賦值該結論的附件內容
            response.data.data.instance['uploadList'] = uploadList
            this.subjects[index][strkey][index_sub] = response.data.data.instance
            alert('更新數據成功！');
          }
        })
        .catch(error => {
          console.log(error);
        });
    },
    //刷新數據
    refreshClick() {
      var self = this
      var search_keys = Object.keys(self.search)
      var checkresult = false
      //檢驗查詢條件是否存在內容
      for(var key of search_keys){
          if(self.search[key] !=''){
            checkresult=true
            break
          }
      }
      if (checkresult)
        self.search_Metting()
      else
        $('input[name="rdGroup1"]:checked').click()
      self.subjects = [{}];
      self.init_metting();
      self.init_subjects();
      self.init_all_subject();
      self.get_past_raisedtasks();
      self.get_yesterday_raisedtasks()
      self.get_MeetingTopicSource()
      window.setTimeout(function () {
        self.init_analysis_meeting();
        self.num1 += 1
      }, 1000);
    },
    //上傳
    push_data(conclusion) {
      this.task_inc_id = conclusion.inc_id
      this.$refs.fiAttachment.click()
    },
    async upload_input_change(e) {
      var self = this;
      const file = e.target.files[0];
      //文件信息
      self.file_mes = { 'task_inc_id': self.task_inc_id, 'file': file }
      var data = self.objectToFormData(self.file_mes)
      self.file_mes = {}
      self.task_inc_id = null
      self.save_file(data)
      $('#fiAttachment').val('')
    },
    save_file(data) {
      axios
        .post(`/looper/metting/save_met_file`, data)
        .then(response => {
          // 處理成功後的返回數據
          if (response.data.status) {
            this.init_subjects();
            alert('上傳文件成功！');
          } else {
            alert('上傳文件失敗！');
          }
        })
        .catch(error => {
          console.log(error);
        });
    },
    //轉任務
    turn_to_task(conclusion) {
      if (conclusion.inc_id == null) {
        alert('請先保存該數據！')
        return
      }
      var self = this;
      init_task(conclusion.inc_id);
      $(self.$refs.task_switch).attr("data-toggle", "modal");
      if (SWApp.os.isAndroid || SWApp.os.isPhone)
        $(self.$refs.task_switch).attr("data-target", "#add-task-module");
      else $(self.$refs.task_switch).attr("data-target", "#add-task");
    },
    //清空查詢條件
    clear_search() {
      this.search = {
        'contact':'',//記錄聯繫人
        'description':'',//描述查詢輸入框
        'meetingid':'',//會議id查詢輸入框
        'progress':'',//記錄狀態
        'hoperation':'',//操作查詢
        'planbs':'',//計劃開始時間
        'planbe':'',//計劃開始時間
        'planes':'',//計劃開始時間
        'planee':'',//計劃開始時間
        'bdatebs':'',//計劃結束時間
        'bdatebe':'',//計劃結束時間
        'edatees':'',//計劃結束時間
        'edateee':'',//計劃結束時間
        'topic':'',//議題查詢
        'classif':'',//查詢類型
        'allocation':'',//記錄是否分配任務
        'createdates':'',
        'createdatee':'',
        'discussprocess':'',
        'summary':'',
        'meetingtopic':'',
        'participants':'',
        'plandates':'',
        'plandatee':'',
        'meetingstate':''
      }
      window.setTimeout(function () {
        $(".status_select").selectpicker('refresh');
      }, 100);

      Object.values(this.$refs).forEach((ref) => {
        if (ref && ref.clearDate) {
          ref.clearDate();
        }
      });
    },
    //切換顯示文件詳情模態框的文件信息
    get_file(uploadList) {
      this.uploadList = uploadList
    },
    //刪除文件
    delete_task_file(uploadItem, index, classif) {
      if (confirm("你確定要刪除該文件?")) {
        axios
          .post(`/looper/metting/DocumentDeleteView/${uploadItem.inc_id}`)
          .then(response => {
            if (response.data.status) {
              switch (classif) {
                case '0':
                  this.uploadList.splice(index, 1)
                  if (!this.uploadList.length > 0) this.$refs.uploadFileDetails.hide()
                  this.init_analysis_meeting();
                  break
                case '1':
                  this.accessoryList.splice(index, 1)
                  break
              }
            }
          })
          .catch(error => {
            console.log(error);
          });
      }
    },
    //下載文件
    download_task_file(uploadItem) {
      window.location.replace(uploadItem.fileurl + '&state=download')
    },
    //議題輸入框改變事件
    OnTopicChang(item) {
      this.subjects[0].subjects[0].task = item.topic;
    },
    //轉議題
    turn_topic(data) {
      this.turntopic = {}
      this.searchMeeting = ''
      this.init_tree('-8')
      this.turntopic['data'] = data
      this.$refs.ConclusionToTopic.show()
    },
    //會議行點擊方法
    nodeSelect(value) {
      this.turntopic['selected'] = value
    },
    //結論轉議題樹狀圖初始化
    init_tree(date) {
      if (isNaN(date)) {
        alert('只能查詢會議ID(ID為年份後兩位+月份+日期+序號組成)！')
        return
      }
      var searchMet = this.searchMeeting
      if ((searchMet != '') && (!isNaN(searchMet))) {
        date = searchMet
      }
      axios
        .get(`/looper/metting/get_metting_tree?date=${date}&isModal=Y`)
        .then(response => {
          // 處理成功後的返回數據
          if (response.data.status) {
            this.treeData = response.data.data
          }
        })
    },
    //結論轉議題
    turn_to_topic() {
      if (this.turntopic['data'] == undefined) {
        alert('空結論，請重試！')
        return
      }
      if (this.turntopic['selected'] == undefined || this.turntopic['selected']['tier'] == '0') {
        alert('請選擇議題！')
        return
      }
      this.turntopic['data']['relationid'] = this.turntopic['selected']['session_id']
      this.turntopic['data']['docpath'] = this.turntopic['selected']['strid']
      axios
        .post(`/PMIS/task/update_task?pk=${this.turntopic['data'].inc_id}`, this.objectToFormData(this.turntopic['data']))
        .then(response => {
          // 處理成功後的返回數據
          if (response.data.status) {
            this.refreshClick()
            this.$emit("refresh_tree", '-8');
            alert('轉議題成功！');
            this.turntopic = {}
            this.searchMeeting = ''
            this.$refs.ConclusionToTopic.hide()
          }
        })
        .catch(error => {
          console.log(error);
        });
    },
    //Management行點擊事件
    on_row_click(event, data) {
      // this.selected_manager = data
      var tpmastid = data['tpmastid']
      var url = `/looper/metting/MeetingmanagerDetailView?tpmastid=${tpmastid}`
      if (this.MettingdetailView != url) {
        this.MettingdetailView = url
        this.num += 1
      }
      window.setTimeout(function () {
        $('#managerDetail').find('th').html(data['tpdesc']).css("padding-top","0")
      }, 200);
    },
    //Management行點擊事件
    on_row_click_tab(event, data) {
      var tpmastid = data['tpmastid']
      var url = `/looper/metting/MeetingmanagerDetailView?tpmastid=${tpmastid}`
      if (this.MettingdetailView_tab != url) {
        this.MettingdetailView_tab = url
        this.num += 1
      }
      window.setTimeout(function () {
        $('#managerDetail').find('th').html(data['tpdesc']).css("padding-top","0")
      }, 200);
    },
    topic_search_meeting() {
      if (this.topic_search == '')
        return
      axios
        .get(`/looper/metting/topic_get_metting?topic=${this.topic_search}`)
        .then(response => {
          if (response.data.status) {
            this.topic_Datasoure = response.data.data
            this.num2 += 1
          }
        });
    },
    // 獲取當前語言
    get_lang_code() {
      if($("#curr_language_code").val() !== "en") {
          this.lang_code_en = false;
      }
    },
    toggleDiscussion(e) {
      e.preventDefault();
      $(".meeting-page").toggleClass("task-expanded");
      $(".meetingDiscussion").toggleClass("page-expanded");
      this.isExpend = !this.isExpend;
    },
    //顯示生成會議結論嚮導模態框
    show_create_met_items(){
      var data = $('#process').val().replace(/\r\n/g, "\r").replace(/\n/g, "\r").split(/\r/)
      var shtml = ``
      for(var i =0;i<data.length;i++){
        var strhtml = `<div class="row mb-2 align-items-center"><div class="col-12 col-md-auto" id="ischeck_${i}"></div><div class="col-12 col-md-6" id="task_${i}"></div><div class="col-12 col-md-2" id="tasktype_${i}">
                          </div><div class="col-12 col-md-2" id="subtasktype_${i}"></div><div class="col-12 col-md" id="diff_${i}"></div></div>`
        shtml+=strhtml
      }
      $('#create_met').html(shtml)
      for(var i =0;i<data.length;i++){
        var task_pc = new SWText("task_"+i, "text",this.$t('Task'),data[i]);
        $("#task_"+i).append(task_pc.dom);
        var tasktype_pc = new SWCombobox("tasktype_"+i, this.$t('Task Type'), "/PMIS/tasktype/tasktype_list", undefined, 'tasktype', 'description');
        $("#tasktype_"+i).append(tasktype_pc.dom);
        var subtasktype_pc = new SWCombobox("subtasktype_"+i, this.$t('Sub TaskType'), []);
        $("#subtasktype_"+i).append(subtasktype_pc.dom);
        var diff_pc = new SWCombobox("diff_"+i, this.$t('Diff'), ["1", "2", "3"])
        $("#diff_"+i).append(diff_pc.dom);   
        var ischeck_pc = new SWCheckbox("ischeck_"+i, this.$t('Select'), true)
        $("#ischeck_"+i).append(ischeck_pc.dom); 

        tasktype_pc.input_dom.on("change", function () {
            var tasktype = $(this).val();
            if (tasktype == "")
                return;
            var indx = String($(this).attr('name').split('_').pop())
            var init_data = subtasktype_pc.input_dom.data("init-data");
            subtasktype_pc = new SWCombobox("subtasktype_"+indx, this.$t('Sub TaskType'), "/PMIS/tasktype/subtasktype_list/" + tasktype, init_data, 'tasktype', 'description');
            $("#subtasktype_"+indx).empty();
            $("#subtasktype_"+indx).append(subtasktype_pc.dom);
        });
      }
      $('input[name="ischeck_All"]').prop("checked",true)
      this.$refs.create_met_items.width('auto')
      this.$refs.create_met_items.show()
    },
    //將選中的討論過程生成會議結論
    create_met_items(){
      var datas = $('#create_met_form').serializeObject()
      if($("#create_met_form input:checkbox").length==0){
        alert('至少選擇一條數據生成會議結論！')
        return
      }
      if($("#create_met_form input:checkbox").length==1 && $("#create_met_form .SWCheckbox input").length==1 && datas['task_0'].replace(' ','')==''){
        alert('討論過程無數據進行生成會議結論！')
        return
      }
      
      var data = {'met_items':JSON.stringify($('#create_met_form').serializeObject()),'topic':this.create_met_topic,'docpath':this.strid}
      axios
        .post(`/looper/metting/create_met_item`,this.objectToFormData(data))
        .then(response => {
          if (response.data.status) {
            alert('討論過程生成議題結論成功！')
            this.refreshClick();
            this.$emit("refresh_tree", '-8');
            this.$refs.create_met_items.hide()
          }else{
            var msg = '討論過程生成議題結論失敗！'
            if(response.data.msg.length>0)
              msg = response.data.msg
            alert(msg)
          }
        });
    },
    //全選討論過程
    ischeck_all(self){
      $('#create_met_form .SWCheckbox input').prop("checked", $('input[name="ischeck_All"]').prop("checked"));
    },
    create_met_items_temp(){
      var self = this
      var templates = this.$refs.managerMasterTable_tab.datatable.rows(['.selected']).data()[0];
      if(templates!=undefined)
        templates=[templates]
      if(templates==undefined || templates.length==0){
        alert('請選擇一條模板')
        return
      }
      for(var item of templates){
        var tpmastid = item['tpmastid']
        var url = `/looper/metting/MeetingmanagerDetailView?tpmastid=${tpmastid}`
        if (this.MettingdetailView_tab != url) {
          this.MettingdetailView_tab = url
          this.num += 1
        }
        var detaildata = this.$refs.managerDetailTable_tab.datatable.data()
        for(var i=0;i<detaildata.length;i++){
          // self.new_conclusion = detaildata[i]['tptname']
          var task =  JSON.parse(JSON.stringify(self.default_task))
          task['editionid'] = "3";
          task['task'] = detaildata[i]['tptname'];
          task['uploadList'] = [];
          var index=$('#meeting_topic_collapse .conclusion-list-item').length
          if (self.subjects[0]['conclusions'] == undefined) {
            self.subjects[0]['conclusions'] = [];
            self.subjects[0]['conclusions'].push(task);
          }else{
            self.subjects[0]['conclusions'].push(task);
          }
          this.$refs.create_met_items.hide()
          self.num+=1
          self.num1+=1
          // self.subjects[index]['conclusions'] = [];
          // self.subjects[index]['conclusions'].push(task);
          // $('#new_conclusion_btn').click()
        }
        // axios
        //   .get(url,{'content-type': 'application/json','headers':{"X-CSRFToken":getCookie('csrftoken')}})
        //   .then(response => {
        //     if (response.data.status) {
        //       for(var i of response.data.data){
        //         self.new_arrange=i['tptname']
        //         self.$refs.new_conclusion.click()
        //       }
        //     }
        //   });
      }
    },
    // 會議統計數據
    taskExpander(e) {
      e.preventDefault();
      $(".meeting-page").toggleClass("task-expanded");
      $("#meeting_summary").toggleClass("page-expanded");
      this.isExpend = !this.isExpend;
    },
    
    //不存在數據時的方法
    NoResult(value,selectedList){
      var contacts = [];
      var hasItem = false
      //獲取已存在的選項信息
      if(selectedList.length>0){
        var old_value = ''
        selectedList.forEach((item, index) => {
          for(var n=0;n<this.options.length;n++){
            var option=this.options[n]
            if(String(option['id'])==item){
              old_value=old_value==''?option['text']:old_value+','+option['text']
              break
            }
          }
        })
        old_value=old_value+','+value
      }
      //判斷是否輸入數據是否存在選項列表中，若存在則設置變量hasItem為true
      this.options.forEach((strkey, index) => {
        if(value==strkey['text']){
          hasItem=true
          return
        }
        contacts.push({ id: index, text: strkey['text'] });
      });
      if(hasItem==false){
        contacts.push({ id: this.options.length, text: value })
        this.options = contacts
        this.metting.participants = old_value
      }
    },
    //參會人員options改變事件
    options_change(value){
      var contacts = [];
      value.forEach((item, index) => {
        contacts.push(item);
      });
      this.options = contacts
    },
    row_click(event, data) {
      var Element = event.target.tagName;
      var target = event.target.className;
      if (Element == "A" || Element == "I") {
          event.preventDefault();
          if (target.includes("fa-image") || target.includes("uploadFile")) {
            this.get_file(data.uploadList);
          }
          if (target.includes("fa-file-signature") || target.includes("btn-transfer")) {
            this.turn_to_task(data);
          }
          if (target.includes("fa-trash-alt") || target.includes("btn-delete")) {
            this.deleteTask(data, 0, index, 'undone_subject');
          }
      }
    },

    //獲取過去八天陳生提出的問題
    get_past_raisedtasks(){
      var self = this
      self.past_raisedtasksdatasource=[]
      var Tempsearch = {
        'contact':'',//記錄聯繫人
        'description':'',//描述查詢輸入框
        'meetingid':'',//會議id查詢輸入框
        'progress':'',//記錄狀態
        'hoperation':'',//操作查詢
        'planbs':'',//計劃開始時間
        'planbe':'',//計劃開始時間
        'planes':'',//計劃開始時間
        'planee':'',//計劃開始時間
        'bdatebs':'',//計劃結束時間
        'bdatebe':'',//計劃結束時間
        'edatees':'',//計劃結束時間
        'edateee':'',//計劃結束時間
        'topic':'',//議題查詢
        'classif':'1',//查詢類型
        'allocation':'',//記錄是否分配任務
        'createdates':'',
        'createdatee':'',
        'discussprocess':'',
        'summary':'',
        'meetingtopic':'',
        'participants':'',
        'plandates':'-8',
        'plandatee':'',
        'meetingstate':''
      }
      axios
        .get(`/looper/metting/get_metting_undone`, {
          params:Tempsearch
        })
        .then(response => {
          //若存在會議記錄則顯示，否則默認創建三條會議記錄輸入框
          if (response.data.status) {
            var detail = response.data.data[0]['detail']
            for(var item of detail)
              self.past_raisedtasksdatasource.push(item)
            self.$refs.past_raisedtasksTable.datatable.clear().rows.add(this.past_raisedtasksdatasource).draw();
          }
        });
    },
    //獲取過去昨天未完成議題結論
    get_yesterday_raisedtasks(){
      var self = this
      var TempData = []
      var yesterday = []
      var today = new Date(); // 获取当前日期
      var yesterday = new Date(today); 
      yesterday.setDate(yesterday.getDate() - 1); 
      var yesterdayYear = yesterday.getFullYear().toString(); 
      var yesterdayMonth = (yesterday.getMonth() + 1).toString().padStart(2, '0');
      var yesterdayDay = yesterday.getDate().toString().padStart(2, '0'); 
      yesterday = yesterdayYear.substring(2) + yesterdayMonth + yesterdayDay

      
      //初始化查詢字段值字典
      var search = {'contact':'','description':'','meetingid':yesterday,'progress':'N','hoperation':'','planbs':'','planbe':'',
                    'planes':'','planee':'','bdatebs':'','bdatebe':'','edatees':'','edateee':'','topic':'',
                    'classif':'','allocation':'','createdates':'','createdatee':'',
                    'discussprocess':'','summary':'','meetingtopic':'','participants':'','plandates':'','plandatee':'','meetingstate':''}
      //獲取用戶會議記錄信息
      axios
        .get(`/looper/metting/get_metting_undone`, {
          params:search
        })
        .then(response => {
          //若存在會議記錄則顯示，否則默認創建三條會議記錄輸入框
          if (response.data.status) {
            var detail = response.data.data[0]['detail']
            self.yesterday_raisedtasksdatasource = detail
            self.$refs.yesterday_raisedtasksTable.datatable.clear().rows.add(self.yesterday_raisedtasksdatasource).draw();
          }
        });
        
    },
    //扣分按鈕點擊事件
    penalty_click(){
        // if(this.selected_manager['inc_id']==undefined || this.selected_manager['inc_id']==null || this.selected_manager['inc_id']==''){
        //   return
        // }
        // var tpdesc = this.selected_manager['tpdesc']
        // if(tpdesc.includes('Areas of Improvement for')){
        //   var concate = tpdesc.split('Areas of Improvement for')
        //   concate = concate[concate.length-1]
        //   this.currentDeductionItem = {};   
          // this.currentDeductionItem['username']=concate.replaceAll(' ','')
          // this.currentDeductionItem['description']=data['tptname']
          // this.currentDeductionItem['deductiondate']=new Date().toString('yyyy-MM-dd')
          // this.deductionItemFormTitle= this.$t("Add Penalty");  
          // this.$refs.deductionItemForm.$refs.modal.show();
        // }
    },
    //保存扣分數據
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
              self.currentDeductionItem = response.data.data.instance

              return self.showMessage(this.$t("Save Success"));    
            })
            .catch((error) => {
              console.log(error);
              reject(error);
            });
        }
      });
    },
    //扣分數據提示
    showMessage(msg){
      $('#deductionItemModalForm').find('.modal-footer').find('button[type="submit"]').popover({
          content: msg,
          container: "body",
          placement: "top",
          title: ''
      });
      $('#deductionItemModalForm').find('.modal-footer').find('button[type="submit"]').popover("show");
      setTimeout(function () {
          $('#deductionItemModalForm').find('.modal-footer').find('button[type="submit"]').popover('dispose');
          $('#deductionItemModalForm').find('.modal-footer').find('button[type="submit"]').removeAttr("data-original-title");
      }, 2500); 
    },

    //獲取所有會議主題
    get_MeetingTopicSource(){
      var self = this
      axios
        .get(`/looper/metting/MeetingTopicView?draw=1&start=1&length=-1&modal=dis_topic`)
        .then(response => {
          if (response.status==200) {
            var detail = response.data.data
            var meetingTopic = []
            var Topiclist = []
            //去除重複會議主題
            for(var item of detail){
              if(item['task']!=null && item['task']!='' && Topiclist.indexOf(item['task'].trim())==-1){
                  Topiclist.push(item['task'].trim())
                  meetingTopic.push(item)
              }
            }
            self.meetingTopicSource = meetingTopic
            self.$refs.meetingTopic_Table.datatable.clear().rows.add(self.meetingTopicSource).draw();
          }
        });
        
    },
    show_meeting_topics(){
      // this.$refs.meetingTopic_modal.width('800px')
      this.$refs.meetingTopic_modal.show()
    },
    set_metTopic(){
      var self = this
      var selectedItem = self.$refs.meetingTopic_Table.datatable.rows(['.selected']).data();
      if(selectedItem==undefined || selectedItem.length==0){
        alert('請選擇一條模板')
        return
      }
      self.subjects[0].subjects[0].task=selectedItem[0]['task']
      self.$refs.meetingTopic_modal.hide()
    },
    async onMsgConfirm(operate){
      //當Type為2時，直接關閉提示框
      if(this.$refs.messageModal.type==2){
        $('#messageModal').modal('hide')    
        return;
      }
     //當Type為1時，並處理operate="deleteShipment" 的操作
      if(operate=="create_met"){
        $('#messageModal').modal('hide')
        this.$refs.save_meeting.setAttribute('disabled', true);
        this.create_Metting(this.$refs.messageModal.data );
      }        
    },

    objectToFormData(obj) {
        let fd = new FormData();
        for (let o in obj) {
            if(obj[o]!=null){
                fd.append(o, obj[o]);
            }          
        }
        return fd;
    },
    getMeetingQueryHeight() {
      let element = this.$refs.messageBody;
      let computedStyle = window.getComputedStyle(element);
      let elementHeight = element.clientHeight -
        parseFloat(computedStyle.paddingTop) -
        parseFloat(computedStyle.paddingBottom);

      this.meetingQueryHeight = elementHeight;

      this.screenWidth = window.innerWidth; // 更新屏幕宽度
    },    
    sendDataToReact() {
      var self = this
      switch(self.meetingsDetailsCardTab){
        // case 1:{
        //   self.predefinedData = self.all_subjects
        //   break;
        // };
        case 2:{
          self.predefinedData = self.past_raisedtasksdatasource
          break;
        };
        case 3:{
          self.predefinedData = self.yesterday_raisedtasksdatasource
          break;
        };
      }
    },
    onPaneResized() {
      this.onSplitterAction();
    },
    onSplitterDoubleClick() {
      this.onSplitterAction();
    },
    onSplitterAction() {
      this.$nextTick(() => {
        this.$forceUpdate();
        setTimeout(() => {
          this.adjustPaneHeight();
        }, 200);
      });
    },
    adjustPaneHeight() {
      this.$nextTick(() => {
        const topPane = document.querySelector('.splitpanes__pane.topPane');
        const bottomPane = document.querySelector('.splitpanes__pane.bottomPane');

        if (topPane && bottomPane) {
          const totalHeight = topPane.parentNode ? topPane.parentNode.clientHeight : 0;

          if (totalHeight > 0) {
            const topPaneHeightPercentage = (topPane.offsetHeight / totalHeight) * 100;
            const bottomPaneHeightPercentage = 100 - topPaneHeightPercentage;

            topPane.style.height = `${topPaneHeightPercentage}%`;
            bottomPane.style.height = `${bottomPaneHeightPercentage}%`;
          }
        }
      });

    }
  },
  watch: {
    "$route.query.id": function (val) {
      var self = this
      self.$refs.save_meeting.removeAttribute('disabled');
      self.subjects = [{}];
      self.init_contact()
      self.init_params();
      self.init_metting();
      self.init_subjects();
      self.init_all_subject();
      self.$refs.meeting_allDetails_a.click()
      window.setTimeout(function () {
        self.init_analysis_meeting();
      }, 500);
    },
    "$route.query.status": function (val) {
      var self = this
      self.$refs.save_meeting.removeAttribute('disabled');
      self.subjects = [{}];
      self.init_contact()
      self.init_params();
      self.init_metting();
      self.init_subjects();
    },
    "$route.query.inc_id": function (val) {
      var self = this
      self.$refs.save_meeting.removeAttribute('disabled');
      self.subjects = [{}];
      self.init_params();
      self.init_metting();
      self.init_subjects();
      self.$refs.meeting_allDetails_a.click()
    },
    "$route.query.sub_inc_id": function (val) {
      var self = this
      self.$refs.save_meeting.removeAttribute('disabled');
      self.subjects = [{}];
      self.init_params();
      self.init_subjects();
      self.$refs.meeting_allDetails_a.click()
    },
    // "all_subjects": function (val) {
    //   var self = this
    //   self.sendDataToReact();
    // },
    "past_raisedtasksdatasource": function (val) {
      var self = this
      self.sendDataToReact();
    },
    "yesterday_raisedtasksdatasource": function (val) {
      var self = this
      self.sendDataToReact();
    },
    "meetingsDetailsCardTab": function (val) {
      var self = this
      self.sendDataToReact();
    },
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.getMeetingQueryHeight);
  },
};
</script>
<style>
/* 會議統計數據放大显示的样式 */
.task-expanded .meetingDiscussion.page-expanded,
.task-expanded #meeting_summary {
  height: 100vh;
}

.task-expanded .summary_wrapper {
  height: calc(100vh - 1rem);
  overflow-y: auto;
}

.task-expanded .summary_wrapper .sumline {
  margin-top: .25rem;
}

.query_meetingTopic>.dropdown{
  width: inherit;
}

@media (min-width: 768px) and (max-width: 1199.98px) {
  .task-expanded .summary_wrapper .meeting_summaryCard>.row>div,
  .task-expanded .summary_wrapper .details_wrapper>.row>div {
    flex: 0 0 33.333333%;
    max-width: 33.333333%
  }
}

@media (min-width: 1200px) {
  .task-expanded .summary_wrapper .meeting_summaryCard>.row>div {
    flex: 0 0 16.666667%;
    max-width: 16.666667%
  }
  
  .task-expanded .summary_wrapper .details_wrapper>.row>div {
    flex: 0 0 20%;
    max-width: 20%
  }
}

@media (min-width: 1800px) {
  .task-expanded .summary_wrapper .details_wrapper>.row>div {
    flex: 0 0 16.666667%;
    max-width: 16.666667%
  }
}

/* 討論過程全屏顯示樣式 */
.task-expanded.meeting-page .left_pane {
  -webkit-mask-image: none;
}
.task-expanded .meetingDiscussion.page-expanded {
  padding: .5rem 1rem 1.5rem 1rem;
}
.task-expanded .meetingDiscussion.page-expanded>textarea {
  height: calc(100% - 37px);
  font-size: 1.35rem;
}
</style>