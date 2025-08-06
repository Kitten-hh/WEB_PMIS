
<template>
  <div :class="{ 'PmsSessionManager page': true, lang_en: lang_code_en }">
    <div ref="splitContainer" class="split-container page-inner">
      <TabBar :tabList="TopTabs" :Hasdropdown="false" :class="['split-pane cardShadow sessionSearchCard topPane scrollbar', isMobile ? 'card-expansion-item expanded' :'',]" :style="{ height: topPaneHeight + 'px' }">
        <template v-slot:session>
          <!-- <div> -->
            <div class="pt-1 search-scope session-search-scope pb-0 d-flex flex-wrap">
              <div class="form-group col-sm-6 col-md-6 col-lg-3 col-xl-2">
                <label class="col-form-label caption col-auto pl-0">{{
                  $t("Record ID")
                }}</label>
                <input class="form-control col" v-model="recordID" />
              </div>
              <div class="form-group col-sm-6 col-md-6 col-lg-3 col-xl-2">
                <label class="col-form-label caption col-auto pl-0">{{
                  $t("Contact")
                }}</label>
                <select class="col select2-contact noFirstVal">
                  <option v-for="(c, key) in contactOptions" :key="key" :value="c">
                    {{ c }}
                  </option>
                </select>
              </div>
              <div class="form-group col-sm col-md col-xl-4">
                <label class="col-form-label caption col-auto pl-0">{{
                  $t("All Contact")
                }}</label>
                <select multiple class="col select2-contact-mul noFirstVal">
                  <option v-for="(c, key) in contactOptions" :key="key" :value="c">
                    {{ c }}
                  </option>
                </select>
              </div>
              <div class="form-group col-auto">
                <button
                  class="btn btn-primary btn_search mr-2"
                  @click="queryClickHandler"
                >
                  <i class="oi oi-magnifying-glass d-xl-none"></i>
                  <span class="d-none d-xl-inline-block">{{ $t("Search") }}</span>
                </button>
                <button class="btn btn-secondary btn_clear" @click="clearHandler">
                  <i class="fa fa-broom d-xl-none"></i>
                  <span class="d-none d-xl-inline-block">{{ $t("Clear") }}</span>
                </button>
              </div>
            </div>
            <LPTreegrid
              ref="sessionTable"
              :datasource="sessionDataSource"
              :columns="sessionColumns"
              idField="sessionid"
              parentIdField="parentid"
              :custom_options="sessionOption"
            />
          <!-- </div> -->
        </template>
  
        <template v-slot:meetting>
          <!-- <div> -->
            <div class="pt-1 search-scope meetting-search-scope pb-0 d-flex flex-wrap">
              <div class="form-group col-12 col-sm col-md-9 col-lg-6 col-xxl-4">
                <label class="col-form-label caption col-auto pl-0">{{ $t('CreateDate') }}</label>
                <div class="input-group input-group-alt m-0">
                  <LPFlatpickerDate ref="topMeetingBDate" id="topMeetingBDate" v-model="search.startDate" />
                  <div class="input-group-append">
                    <span class="input-group-text custom-text">{{ $t('To') }}</span>
                  </div>
                  <LPFlatpickerDate ref="topMeetingEDate" id="topMeetingEDate" v-model="search.endDate" />
                </div>
              </div>

              <div class="form-group col-auto">
              <button class="btn btn-primary btn_search mr-2" @click="searchTopMeeting" >
                <i class="oi oi-magnifying-glass d-xl-none"></i>
                <span class="d-none d-xl-inline-block">{{ $t("Search") }}</span>
              </button>

              <button class="btn btn-secondary btn_clear" @click="clearTopMeeting">
                <i class="fa fa-broom d-xl-none"></i>
                <span class="d-none d-xl-inline-block">{{ $t("Clear") }}</span>
              </button>
            </div>
            </div>
            <LPDataTable 
              ref="meetingTable" 
              :columns="meetingColumns" 
              :datasource="meetingDataSource"
              @on_row_click="meeting_row_click"
              :paging_inline="true"
              :custom_options="taskOptions"
              /> 
          <!-- </div> -->
        </template>
  
        <template v-slot:goal>
          <!-- <div> -->
            <div class="pt-1 search-scope goal-search-scope pb-0 d-flex flex-wrap">

              <div class="form-group col-sm-6 col-md-7 col-lg-3 col-xl-2">
                <label class="col-form-label caption col-auto pl-0">{{
                  $t("Contact")
                }}</label>
                <select class="col select2-contact noFirstVal">
                  <option v-for="(c, key) in contactOptions" :key="key" :value="c">
                    {{ c }}
                  </option>
                </select>
              </div>
              
              <div class="form-group col-sm-6 col-md-5 col-lg-2 col-xl-2">
                <label class="col-form-label caption col-auto pl-0">{{ $t("Year") }}</label>
                <input type="text" class="form-control col" v-model="goalYear"  />
              </div>


              <div class="form-group col-sm col-md-5 col-lg-2 col-xl-2">
                <label class="col-form-label caption col-auto pl-0">{{
                  $t("Period")
                }}</label>
                <select class="select2-goalnumber form-control" v-model="goalNumberOptions"></select>
              </div>

              <div class="form-group col-sm col-md col-lg-3 col-xl-2">
                <label class="col-form-label caption col-auto pl-0">{{
                  $t("Category")
                }}</label>
                <select class="select2-goalcategory form-control" v-model="selectGoalCategory"></select>
              </div>

              <div class="form-group col-auto">
                <button class="btn btn-primary btn_search mr-2" @click="searchTopGoal" >
                  <i class="oi oi-magnifying-glass d-xl-none"></i>
                  <span class="d-none d-xl-inline-block">{{ $t("Search") }}</span>
                </button>
                <button class="btn btn-secondary btn_clear" @click="clearTopGoal">
                  <i class="fa fa-broom d-xl-none"></i>
                  <span class="d-none d-xl-inline-block">{{ $t("Clear") }}</span>
                </button>
              </div>
            </div>
            <LPDataTable 
              ref="goalTable" 
              :columns="goalColumns" 
              :datasource="goalDataSource"
              :paging_inline="true"
              :custom_options="taskOptions"
            /> 
          <!-- </div> -->
        </template>

        <template v-slot:technical>
          <!-- <div> -->
            <div class="pt-1 search-scope meetting-search-scope technical-search-scope pb-0 d-flex flex-wrap">
              <div class="form-group col-12 col-sm-8 col-md-8 col-lg-5 col-xl-4 col-xxl-4">
                <label class="col-form-label caption col-auto pl-0">{{ $t('CreateDate') }}</label>
                <div class="input-group input-group-alt m-0">
                  <LPFlatpickerDate ref="topTechnicalBDate" id="topTechnicalBDate" v-model="topTechnicalsearch.startDate" />
                  <div class="input-group-append">
                    <span class="input-group-text custom-text">{{ $t('To') }}</span>
                  </div>
                  <LPFlatpickerDate ref="topTechnicalEDate" id="topTechnicalEDate" v-model="topTechnicalsearch.endDate" />
                </div>
              </div>
              
              <div class="form-group col-sm-4 col-md-4 col-lg-3 col-xl-2">
                <label class="col-form-label caption col-auto pl-0">{{
                  $t("Contact")
                }}</label>
                <select class="col select2-contact-tech noFirstVal">
                  <option v-for="(c, key) in contactOptions" :key="key" :value="c">
                    {{ c }}
                  </option>
                </select>
              </div>

              <div class="form-group col-sm-6 col-md-6 col-lg-4 col-xl-2">
                <label class="col-form-label caption col-auto pl-0">{{ $t('Technical ID') }}</label>
                <input type="text" class="form-control col" v-model="topTechnicalsearch.technicalID"  />
              </div>

              <div class="form-group col-sm-6 col-md-6 col-lg-5 col-xl-2">
                <label class="col-form-label caption col-auto pl-0">{{ $t('Category') }}</label>
                <input type="text" class="form-control col" v-model="topTechnicalsearch.category"  />
              </div>
  
              
              <div class="form-group col-sm col-md col-lg col-xl-2">
                <label class="col-form-label caption col-auto pl-0">{{ $t('Area') }}</label>
                <input type="text" class="form-control col" v-model="topTechnicalsearch.area"  />
              </div>
              
              <div class="form-group col-auto">
                <button class="btn btn-primary btn_search mr-2" @click="searchTopTechnical" >
                  <i class="oi oi-magnifying-glass d-xl-none"></i>
                  <span class="d-none d-xl-inline-block">{{ $t("Search") }}</span>
                </button>

                <button class="btn btn-secondary btn_clear" @click="clearTopTechnical">
                  <i class="fa fa-broom d-xl-none"></i>
                  <span class="d-none d-xl-inline-block">{{ $t("Clear") }}</span>
                </button>
              </div>
            </div>
            <LPDataTable 
              ref="technicalTable" 
              @on_dbclick="technical_row_dbclick"
              :columns="technicalColumns" 
              :datasource="technicalSource"
              :paging_inline="true"
              :searching="false"
              :custom_options="taskOptions"
            /> 
          <!-- </div> -->
        </template>
      </TabBar>
      
      <div
        class="split-divider"
        @mousedown="startDrag"
        @touchstart="startDrag"
        @dblclick="maximizeBottomPane"
        @touchend="handleTouchEnd"
      ></div>
      <div
        class="split-pane bottomPane card cardShadow detailInfo mb-0"
        :style="{ height: bottomPaneHeight + 'px' }"
      >
        <ul class="nav nav-tabs skinableNavTab flex-shrink-0 scrollbar">
          <li class="nav-item">
            <a
              class="nav-link show active"
              data-toggle="tab"
              href="#task-list"
              @click="activeTab = 0"
              >{{ $t("Task list") }}</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" 
            data-toggle="tab"
             href="#task-list-all"
             @click="activeTab = 1"
             >{{$t("Task list(All)")}}</a>
          </li>
          <li class="nav-item">
            <a
              class="nav-link"
              id="tab_tasks"
              data-toggle="tab"
              href="#top-task"
              @click="activeTab = 2"
              >{{ $t("Prompt Tasks") }}</a>
          </li>
          <li class="nav-item">
            <a
              class="nav-link"
              id="tab_sql"
              data-toggle="tab"
              href="#sql-script"
              @click="activeTab = 3"
              >{{ $t("SQL Script") }}</a>
          </li>
        </ul>
        <div
          :class="{
            'card-body tab-content scrollbar': true,
            isSpecialTabCard: isTaskTabActive,
          }"
        >
          <fieldset class="col-12 taskSearch card-expansion-item expanded">
            <legend class="mb-0">
              <button
                class="btn btn-reset d-flex justify-content-between prevent-default pl-0"
                data-toggle="collapse"
                data-target="#sessionMgnTaskSearchCollapse"
                aria-expanded="true"
                aria-controls="sessionMgnTaskSearchCollapse"
              >
                <span class="collapse-indicator"
                  ><i class="fa fa-fw fa-caret-right mr-1"></i></span
                ><span>{{ $t("Task Query") }}</span>
              </button>
            </legend>
            <div
              id="sessionMgnTaskSearchCollapse"
              class="collapse show row search_list mx-0"
            >
              <div
                class="form-group col-sm-6 col-md-4 col-lg-3"
                v-show="!isTaskTabActive"
              >
                <!-- class裡去掉了 v-show="!isTaskTabActive"  -->

                <label class="col-form-label caption col-auto pl-0">{{
                  $t("Progress")
                }}</label>
                <select v-model="selectedProgress" class="select2-progress">
                  <option
                    v-for="(progress, key) in progressOptions"
                    :key="key"
                    :value="progress.data"
                  >
                    {{ progress.name }}
                  </option>
                </select>
              </div>
              <div
                class="form-group col-sm-6 col-md-4 col-lg-3"
                v-show="!isTaskTabActive"
              >
                <label class="col-form-label caption col-auto pl-0">{{
                  $t("Priority")
                }}</label>
                <select v-model="selectedPriority" class="select2-priority">
                  <option
                    v-for="(priority, key) in priorityOptions"
                    :key="key"
                    :value="priority"
                  >
                    {{ priority }}
                  </option>
                </select>
              </div>
              <div
                class="form-group col-sm-6 col-md-4 col-lg-3"
                v-show="!isTaskTabActive"
              >
                <label class="col-form-label caption col-auto pl-0">{{
                  $t("Class")
                }}</label>
                <select v-model="selectedClass" class="select2-class">
                  <option
                    v-for="(classOption, key) in classOptions"
                    :key="key"
                    :value="classOption.value"
                  >
                    {{ classOption.label }}
                  </option>
                </select>
              </div>
              <div
                class="form-group col-sm-6 col-md-8 col-lg-9"
                v-show="!isTaskTabActive"
              >
                <label class="col-form-label caption col-auto pl-0">{{
                  $t("Task desc")
                }}</label>
                <input
                  v-model="taskText"
                  class="form-control"
                  @keyup.enter="taskListChange"
                />
              </div>
              <!--
              <div class="form-group d-flex col-sm-6 col-md-4 col-lg">
                <label class="col-form-label caption col-auto pl-0">{{ $t("Condition") }}:</label>
                <select class="col ml-2 select2-condition-task" v-model="selectedCondition">
                  <option v-for="(option, key) in conditions" :key="key" :value="option.inc_id">{{ option.desc }}</option>
                </select>
              </div>
              -->
              <div
                :class="[
                  'form-group col-sm-6 col-md-4 col-lg-3'
                ]"
                v-show="!isTaskTabActive"
              >
                <label class="col-form-label caption col-auto pl-0">{{
                  $t("Contact")
                }}</label>
                <select
                  class="col ml-2 select2-contact-task"
                  v-model="selectedContact"
                >
                  <option
                    v-for="(c, key) in contactOptions"
                    :key="key"
                    :value="c"
                  >
                    {{ c }}
                  </option>
                </select>
              </div>
              <div class="form-group col-sm-6 col-md-4 col-lg-3"
              v-show="!isTaskTabActive">
                <label class="col-form-label caption col-auto pl-0">{{
                  $t("Record ID")
                }}</label>
                <input class="form-control" v-model="ai_recordID" />
              </div>

              <!-- 第三四標籤頁的表單框 -->
              <div
                class="prompt_sql_tab_show form-group col-sm-6 col-md-4 col-lg-3"
                v-show="activeTab === 2 || activeTab === 3"
              >

                <label class="col-form-label caption col-auto pl-0">{{
                  $t("Progress")
                }}</label>
                <select v-model="selectedPromptProgress" class="select2-promptprogress">
                  <option
                    v-for="(progress, key) in progressOptions"
                    :key="key"
                    :value="progress.data"
                  >
                    {{ progress.name }}
                  </option>
                </select>
              </div>
              <div
                class="prompt_sql_tab_show form-group col-sm-6 col-md-4 col-lg-3"
                v-show="activeTab === 2 || activeTab === 3"
              >
                <label class="col-form-label caption col-auto pl-0">{{
                  $t("Priority")
                }}</label>
                <select v-model="selectedPromptPriority" class="select2-promptpriority">
                  <option
                    v-for="(priority, key) in priorityOptions"
                    :key="key"
                    :value="priority"
                  >
                    {{ priority }}
                  </option>
                </select>
              </div>
              <div
                class="prompt_sql_tab_show form-group col-sm-6 col-md-4 col-lg-3"
                v-show="activeTab === 2 || activeTab === 3"
              >
                <label class="col-form-label caption col-auto pl-0">{{
                  $t("Class")
                }}</label>
                <select v-model="selectedPromptClass" class="select2-promptclass">
                  <option
                    v-for="(classOption, key) in classOptions"
                    :key="key"
                    :value="classOption.value"
                  >
                    {{ classOption.label }}
                  </option>
                </select>
              </div>
              <div
                class="prompt_sql_tab_show form-group col-sm-6 col-md-8 col-lg-9"
                v-show="activeTab === 2 || activeTab === 3"
              >
                <label class="col-form-label caption col-auto pl-0">{{
                  $t("Task desc")
                }}</label>
                <input
                  v-model="taskPromptText"
                  class="form-control"
                  
                />
                <!-- 注釋了input裡的@keyup.enter="taskListChange" -->
              </div>

              <div
                :class="[
                  'prompt_sql_tab_show form-group col-sm-6 col-md-4 col-lg-3',
                  
                ]" 
                v-show="activeTab === 2 || activeTab === 3"
              >
                <label class="col-form-label caption col-auto pl-0">{{
                  $t("Contact")
                }}</label>
                <select
                  class="col ml-2 select2-promptcontact-task"
                  v-model="selectedPromptContact"
                >
                  <option
                    v-for="(c, key) in contactOptions"
                    :key="key"
                    :value="c"
                  >
                    {{ c }}
                  </option>
                </select>
              </div>
              <div class="prompt_sql_tab_show form-group col-sm-6 col-md-4 col-lg-3"
              v-show="activeTab === 2 || activeTab === 3">
                <label class="col-form-label caption col-auto pl-0">{{
                  $t("Record ID")
                }}</label>
                <input class="form-control" v-model="ai_recordPromptID" />
              </div>

              <!-- 第三四標籤頁結束 -->
              
              <div class="form-group col-sm-12 col-md-8 col-lg">
                <label class="col-form-label caption col-auto pl-0">{{
                  $t("Category")
                }}</label>
                <LPCombobox
                  url="/looper/session_manager/get_category_data"
                  ref="category_LPCasombobox"
                  :labelFields="['category']"
                  valueField="category"
                  :value="category"
                  @on_item_selected="
                    (item) => {
                      this.category = item.category;
                    }
                  "
                  @on_Blur="
                    (value) => {
                      this.category = value;
                    }
                  "
                  showCount="20"
                  width="500px"
                  class="dropdownMenuScroll"
                />
              </div>
              <div class="form-group col-sm-12 col-md-8 col-lg query_condition">
                <label class="col-form-label caption col-auto pl-0">{{
                  $t("Prompt")
                }}</label>
                <LPCombobox
                  url="/looper/session_manager/get_conditon_data"
                  ref="condition_LPCasombobox"
                  :labelFields="['sname']"
                  valueField="sname"
                  :value="currentPrompt.sname"
                  @on_item_selected="onConditionSelected"
                  @on_Blur="onConditionBlur"
                  showCount="20"
                  width="500px"
                  :filter="prompt_filter"
                  class="dropdownMenuScroll"
                />
              </div>
              <div class="form-group col-auto">
                <div
                  class="custom-control custom-control-inline custom-checkbox mr-0"
                >
                  <input
                    type="checkbox"
                    class="custom-control-input"
                    id="approved"
                    v-model="isapproved"
                    @change="setPromptFilter"
                  />
                  <label
                    class="custom-control-label cursor-pointer"
                    for="approved"
                    >{{ $t("Approved") }}</label
                  >
                </div>
              </div>
              <div class="form-group col-auto">
                <button class="btn btn-primary mr-2" @click="getTasks">
                  {{ $t("Search") }}
                </button>
                <button class="btn btn-primary mr-2 btn_ai_analysis" @click="aiAnalysis">
                  {{ $t("AI Analysis") }}
                </button>
                <button
                  class="btn btn-secondary btn_clear"
                  @click="clearTasksHandler"
                >
                  {{ $t("Clear") }}
                </button>
              </div>
            </div>
          </fieldset>
          <div class="tab-pane fade active show" id="task-list" role="tabpanel">
            <LPDataTable
              ref="taskTable"
              :datasource="[]"
              :columns="taskColumns"
              :row_nowrap="true"
              :custom_options="taskOptions"
              :searching="false"
              :paging_inline="true"
              :custom_params_fun="taskParamsFun"
              @on_selectornot="taskTableRowSelected"
              :paging="false"
              @on_dbclick="showTaskDetail"
            />
          </div>
          <div class="tab-pane fade" id="task-list-all" role="tabpanel">
            <LPDataTable
              ref="taskAllTable"
              :datasource="[]"
              :columns="taskColumns"
              :row_nowrap="true"
              :custom_options="taskOptions"
              :searching="false"
              :paging_inline="true"
              :custom_params_fun="taskParamsFun"
              @on_selectornot="taskTableRowSelected"
              :paging="false"
              @on_dbclick="showTaskDetail"
            />
          </div>
          <div class="tab-pane fade" id="top-task" role="tabpanel">
            <div v-if="showTaskData">
              <LPDataTable
                ref="topTask"
                :datasource="[]"
                :columns="dataColumns"
                :row_nowrap="true"
                :custom_options="taskOptions"
                :searching="false"
                :paging_inline="true"
                :paging="false"
                @on_dbclick="showTaskDetail"
                @on_row_click="topTask_row_click"
              />
            </div>
          </div>
          <div class="tab-pane fade" id="sql-script" role="tabpanel">
            <div class="row mx-0 sqlScriptRow">
              <div class="form-group col-12">
                <label class="col-form-label caption" for="tf6">{{
                  $t("SQL Query")
                }}</label>
                <textarea
                  class="form-control control"
                  id="tf6"
                  rows="14"
                  name="q_sql"
                  v-model="currentPrompt.ssql"
                  @input="handleSsqlChange"
                ></textarea>
              </div>
              <div class="form-group d-flex col-12">
                <label class="col-form-label caption col-auto pl-0">{{
                  $t("Prompt By Ai")
                }}</label>
                <input
                  class="form-control mr-2"
                  v-model="currentPrompt.promptbyai"
                />
                <button
                  class="btn btn-primary text-nowrap"
                  @click="currentPrompt.ssql = historySsql"
                >
                  {{ $t("Restore") }}
                </button>
              </div>
              <div class="form-group d-flex col-12 col-sm">
                <label class="col-form-label caption col-auto pl-0">{{
                  $t("Category")
                }}</label>
                <LPCombobox
                  url="/looper/session_manager/get_category_data"
                  ref="category_LPCasombobox"
                  :labelFields="['category']"
                  valueField="category"
                  :value="currentPrompt.category"
                  @on_item_selected="
                    (item) => {
                      this.currentPrompt.category = item.category;
                    }
                  "
                  @on_Blur="
                    (value) => {
                      this.currentPrompt.category = value;
                    }
                  "
                  showCount="20"
                  width="500px"
                  class="dropdownMenuScroll"
                />
              </div>
              <div class="form-group col-auto">
                <div
                  class="custom-control custom-control-inline custom-checkbox"
                >
                  <input
                    type="checkbox"
                    class="custom-control-input"
                    id="isai"
                    v-model="currentPrompt.isai"
                    disabled
                  />
                  <label
                    class="custom-control-label cursor-pointer"
                    for="isai"
                    >{{ $t("IsAi") }}</label
                  >
                </div>
                <div
                  class="custom-control custom-control-inline custom-checkbox mr-0"
                >
                  <input
                    type="checkbox"
                    class="custom-control-input"
                    id="isapproved"
                    v-model="currentPrompt.isapproved"
                    :disabled="!canApprove"
                  />
                  <label
                    class="custom-control-label cursor-pointer"
                    for="isapproved"
                    >{{ $t("Approved") }}</label
                  >
                </div>
              </div>
              <div class="form-group col-auto">
                <button class="btn btn-primary mr-2 savePrompt" ref="saveButton" @click="savePrompt">
                  {{ $t("Save") }}
                </button>
                <button type="button" class="btn btn-primary executeSql" ref="sqlButton" @click="executeSql">
                  {{ $t("Execute SQL") }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <LPAIComBox ref="aicombox" :predefinedData="aiPredefinedData" />
</template>
<script>
import axios from "axios";
import LPTreegrid from "@components/looper/tables/LPTreegrid.vue";
import LPLabelInput from "@components/looper/forms/LPLabelInput.vue";
import LPCombobox from "@components/looper/forms/LPCombobox.vue";
import TabBar from "@components/looper/navigator/TabBar.vue";
import LPFlatpickerDate from "@components/looper/forms/LPFlatpickerDate.vue";
import LPDataTable, {
  DateRender,
} from "@components/looper/tables/LPDataTable.vue";
import LPAIComBox from "@components/looper/general/LPAIComBox.vue";
export default {
  name: "PmsSessionManager_vueFrm",
  components: { LPTreegrid, LPDataTable, LPLabelInput, LPCombobox, LPAIComBox,TabBar,LPFlatpickerDate },
  data() {
    return {
      search: {
        startDate: "", // 開始日期
        endDate: "",   // 結束日期
      },
      TopTabs: [
        { tabid: 'session', label: this.$t("Session"), bodyname: 'session' },
        { tabid: 'meetting', label: this.$t("Meeting"), bodyname: 'meetting' },
        { tabid: 'goal', label: this.$t("Goal"), bodyname: 'goal' },
        { tabid: 'technical', label: this.$t("Technical"), bodyname: 'technical' }
      ],
      meetingColumns:[
        { field: "id", label: this.$t("Meeting ID"), width: 150 },
        { field: "creator", label: this.$t("Creator") }, // 創建者
        { field: "topic", label: this.$t("Topic") }, // 主題
        { field: "discussprocess", label: this.$t("Discuss Process") }, // 討論過程
        { field: "summary", label: this.$t("Summary") }, // 總結
        { field: "state", label: this.$t("State") }, // 狀態
      ],
      meetingDataSource: [],
      meetingRowData:{},

      technicalColumns: [
        { field: "mb015c", label: this.$t("Category"), width: 150 }, // 類別
        { field: "mb004", label: this.$t("Technical Topic") }, // 主題
        { field: "mb016", label: this.$t("Area") , width: 150}, // 區域
        { field: "mb023", label: this.$t("Technical ID") }, // 技術編號
        { field: "creator", label: this.$t("Contact") }, // 聯繫人
        { field: "create_date", label: this.$t("Create Date") }, // 創建日期
        { field: "mb008", label: this.$t("Usage") }, // 作用
      ],
      topTechnicalsearch: {
        startDate: "", // 開始日期
        endDate: "",   // 結束日期
        // content: '',  // 内容
        category: "", // category
        area: "",
        technicalID: ''
      },
      goalColumns:[
        { field: "goalid", label: this.$t("Goal ID"), width: 150 },
        { field: "creator", label: this.$t("Creator") }, // 創建者
        { field: "period", label: this.$t("Period") }, // 季度
        // { field: "month", label: this.$t("Month") }, // 月份
        { field: "goaldesc", label: this.$t("Goal Desc") }, // 描述 
        { field: "goaltype", label: this.$t("Goal Type") }, // 類型
        { field: "goaltype", label: this.$t("Goal Type") }, // 類型
        { field: "recordid", label: this.$t("Recordid") }, // 類型
      ],
      goalDataSource: [],
      goalRecordID: "",
      goalYear: "",
      goalNumberOptions: [],
      goalRowData:{},
      technicalSource: [],
      selectGoalNumber:{},  // 存儲選中的數據
      goalCategoryOptions: [],
      selectGoalCategory:{},  // 存儲選中的數據

      

      splitContainerHeight: 0, // 用於存儲.split-container元素的高度
      topPaneHeight: 380, // 初始頂部面板的高度
      startY: 0,
      startHeight: 200,
      sessionColumns: [
        { field: "sessionid", label: this.$t("Session ID"), width: 150 }, // 模版編號
        { field: "parentid", label: "", visible: false }, // 模版編號
        { field: "recordid", label: this.$t("Record ID"), width: "250px" }, //子工程編號
        { field: "sdesp", label: this.$t("Description") }, // 任務描述
        { field: "contact", label: this.$t("Contact") }, // 聯繫人
        { field: "allcontact", label: this.$t("All Contact") }, // 所有聯繫人
        { field: "progress", label: this.$t("Progress") }, // 進度
        {
          field: "pschedule",
          label: this.$t("Plan schedule"),
          render: (value) => {
            return `<div style="width: 100%; height: 100%;">
              <div style="display: flex; width: 100%; height: 100%;">
                <div style="width: ${value}%; height: 100%; background-color: #0000FF;"></div>
                <div style="width: ${100 - value}%;"></div>
              </div>
              <div style="color: #FF3300; text-align: center;">${value}%</div>
            </div>`;
          },
        }, // 計劃進度
        { field: "aschedule", label: this.$t("Actual schedule") }, // 實際進度
        {
          field: "planbdate",
          label: this.$t("Plan begin date"),
          render: DateRender,
        }, // 計劃開始
        {
          field: "planedate",
          label: this.$t("Plan end date"),
          render: DateRender,
        }, // 計劃結束
        { field: "priority", label: this.$t("Priority") }, // 優先級
        {
          field: "projectscore",
          label: this.$t("Project scheduling priority"),
        }, // 工程排期優先級
        { field: "weight", label: this.$t("Scheduling priority") }, // 排期優先級
        { field: "capacity", label: this.$t("Capacity") }, // 產能
        { field: "djcapacity", label: this.$t("Day job capacity") }, // DayJob產能
        { field: "outstandday", label: this.$t("Outstand day") }, // 拖期天數
        { field: "outstandqty", label: this.$t("Outstand qty") }, // 拖期數量
        { field: "flowchartno", label: this.$t("Flowchart") }, // 流程圖
        { field: "type", label: this.$t("Type") }, // 類型
      ],
      sessionOption: {
        height: "auto",
        uniqueId: "sessionid",
      },
      sessionDataSource: [],
      taskColumns: [
        { field: "taskno", label: this.$t("Taskno") }, // 模版編號
        { field: "udf04", label: this.$t("Frame name") }, // 窗口名稱
        {
          field: "task",
          label: this.$t("Task Description"),
          width: "360px",
          className: "subLabelMB",
        }, // 任務描述
        { field: "contact", label: this.$t("Contact") }, // 聯繫人
        { field: "progress", label: this.$t("Progress") }, // 進度
        {
          field: "planbdate",
          label: this.$t("Plan begin date"),
          render: DateRender,
        }, // 計劃開始
        {
          field: "planedate",
          label: this.$t("Plan end date"),
          render: DateRender,
        }, // 計劃結束
        { field: "score", label: this.$t("Score") }, // 分數
        { field: "relationid", label: this.$t("Relation ID") }, // 關聯任務
        { field: "bdate", label: this.$t("BDate"), render: DateRender }, // 實際開始
        { field: "edate", label: this.$t("EDate"), render: DateRender }, // 實際結束
        { field: "priority", label: this.$t("Priority") }, // 優先權
        { field: "schpriority", label: this.$t("Scheduling priority") }, // 排期優先級
        { field: "dayjob", label: this.$t("Day task") }, // 當天任務
        { field: "remark", label: this.$t("Remark") }, // 備註
        { field: "revisedby", label: this.$t("Revised by") }, // 修改人
        { field: "subprojectid", label: this.$t("Subproject iD") }, // 序號
        { field: "projectname", label: this.$t("Project name") }, // 工程名稱
      ],
      sqlQuery: "", // 输入的SQL查询
      taskData: [], // 执行结果数据
      /*
      topTaskColumns: [
        { field: "taskno", label: "TaskNo" },
        { field: "task", label: "Task", width: '360px' },
        { field: "contact", label: "Contact" },
        { field: "planbdate", label: "Plan Begin Date", render: DateRender },
        { field: "planedate", label: "Plan End Date", render: DateRender },
        { field: "progress", label: "Progress" },
        { field: "class", label: "Class" },
        { field: "remark", label: "Remark", width: '360px' },
        { field: "schpriority", label: "Schedule Priority" },
        { field: "projectname", label: "Project Name" },        
        { field: "recordid", label: "RecordID" },
        { field: "sdesp", label: "Session Name", width: '200px' },
        { field: "tasklistcontact", label: "Session Contact" },
        { field: "tasklistplanbdate", label: "Session Plan Begin Date", render: DateRender },
        { field: "tasklistplanedate", label: "Session Plan End Date", render: DateRender },
        { field: "tasklistprogress", label: "Session Progress" },
        { field: "tasklistremark", label: "Session Remark" },
      ], 
      */
      dataColumns: [],
      taskOptions: {
        responsive: false,
        autoWidth: false,
        scrollX: true,
        scrollY: "auto",
        // scrollCollapse: true, // 啟用滾動折疊
        deferLoading: 0,
      },
      contact: "", // 聯繫人
      allContact: [], // 所有聯繫人
      recordID: "", // 記錄ID
      period: "", // 時間範圍
      selectedProgress: "",
      selectedPromptProgress: "",
      selectedPriority: "",
      selectedPromptPriority: "",
      selectedContact: "",
      selectedPromptContact: "",
      selectedCondition: null,
      selectedClass: "",
      selectedPromptClass: "",
      taskText: "",
      taskPromptText: "",
      progressOptions: [
        { name: "", data: "" },
        { name: "N:新工作", data: "N" },
        { name: "I:正在進行的工作", data: "I" },
        { name: "T:當天的工作", data: "T" },
        { name: "S:已經開始的工作", data: "S" },
        { name: "F:已完成工作", data: "F" },
        { name: "C:基本完成", data: "C" },
        { name: "NF:除F的工作", data: "NF" },
        { name: "H:被掛起的工作", data: "H" },
        { name: "R:復查", data: "R" },
      ],
      priorityOptions: ["", "888", "8888", "8889"],
      classOptions: [
        { label: "", value: "" },
        { label: "class1", value: "1" },
        { label: "class2", value: "2" },
        { label: "Other", value: "3" },
      ],
      contactOptions: [],
      selsectedTreeRow: {},
      allQuerySession: [],
      topTasks: [],
      filterTopTasks: [], // 篩選後的數據
      conditions: [],
      loading: false,
      currentPrompt: {
        inc_id: null,
        sname: "",
        isai: true,
        category: "",
        isapproved: false,
        ssql: "",
      },
      showTaskData: false,
      aiPredefinedData: [],
      ai_recordID: "",
      ai_recordPromptID: "",
      lang_code_en: true,
      isQueryCollapse: true,
      isTaskTabActive: false,
      sql_script: "", //查詢任務的SQL語句
      category: "",
      isapproved: false,
      prompt_filter: "",
      historySsql: "",
      canApprove: false,
      isMobile: false,
      isclearPane: false,
      lastTouchEnd: 0,
      topTaskData:{}, //提示任務對象
    };
  },
  mounted() {
    this.setGoalCategoryOptions();
    this.setGoalNumberOptions();

    // 在 Vue 组件挂载后调用初始化右键菜单的方法
    this.$nextTick(() => {
        this.initializeContextMenu();         // 初始化 top-task 表格的右键菜单
        this.initializeSessionContextMenu();  // 初始化 sessionTable 表格的右键菜单
    });

    this.get_lang_code();
    this.getPromptApprove();
    var _this = this;
    this.$nextTick(function () {
      _this.splitContainerHeight = _this.$refs.splitContainer.offsetHeight; // 獲取.split-container元素的高度
      _this.onResized();

      if ($(".fixed-table-toolbar").attr("class").indexOf("d-none") == -1)
        $(".fixed-table-toolbar").addClass("d-none");
      var table = $(this.$refs.sessionTable.$el).find("table.SWTreegrid"); //TreeTable元素
      table.attr("data-toggle", "table");
      table.attr("data-click-to-select", "true");
      table.on("click-row.bs.table", function (e, row, el) {
        var dt = _this.$refs.taskTable.datatable; //task table 對象
        if ($(el).attr("class").indexOf("selected") != -1) {
          $(el).removeClass("selected");
          dt.clear().rows.add([]).draw();
          _this.selsectedTreeRow = {};
          return;
        } else {
          $(el).siblings().removeClass("selected");
          $(el).addClass("selected");
          _this.selsectedTreeRow = row;
        }
        _this.getTopTaskData([row.sessionid], dt);

        _this.onResized();

        if (SWApp.os.isMobile) {
          _this.maximizeBottomPane();
        }
      });

      $(".taskSearch .btn-reset").on("click", function () {
        _this.isQueryCollapse = !_this.isQueryCollapse;
      });

      // ?听 select2:open 事件
      $(".noFirstVal").on("select2:open", () => {
        setTimeout(() => {
          $(
            ".select2-container.select2-container--open ul.select2-results__options>li.select2-results__option"
          ).each(function () {
            if ($(this).attr("id") === undefined) {
              $(this).addClass("d-none"); //當select2下拉選屬性中的id為空時,設置隱藏
            }
          });
        }, 0);
      });

      $('.PmsSessionManager .detailInfo a[data-toggle="tab"]').on(
        "shown.bs.tab",
        function (e) {
          if (
            $(e.currentTarget).attr("id") === "tab_tasks" ||
            $(e.currentTarget).attr("id") === "tab_sql"
          ) {
            _this.isTaskTabActive = true;
          } else {
            _this.isTaskTabActive = false;
          }
        }
      );

      _this.mobileUI();
      $(".PmsSessionManager .LPDataTable .dataTables_info")
        .closest(".row")
        .addClass("mx-0");

      // if (SWApp.os.isMobile) {
      //   _this.isMobile = true;
      // } else {
      //   $(".search-scope").unwrap();
      // }
    });

    window.addEventListener("resize", this.onResized);

    var recordid = getParamFromUrl("recordid");
    if (recordid) {
      this.recordID = recordid;
      this.ai_recordID = recordid;
      this.queryClickHandler();
    }
    // 聯繫人和全部聯繫人選擇框的處理
    $(".select2-contact")
      .select2()
      .on("select2:select", function (e) {
        _this.contact = e.params.data.text;
      });
    $(".select2-contact-tech")
      .select2()
      .on("select2:select", function (e) {
        _this.contact = e.params.data.text;
      });
    $(".select2-contact-mul")
      .select2()
      .on("select2:select", function (e) {
        var text = e.params.data.text;
        if (!_this.allContact.includes(text)) _this.allContact.push(text);
      })
      .on("select2:unselect", function (e) {
        var text = e.params.data.text;
        if (_this.allContact.includes(text)) {
          _this.allContact.splice(_this.allContact.indexOf(text), 1);
        }
      });
    $(".select2-progress")
      .select2()
      .on("select2:select", function (e) {
        _this.selectedProgress = e.params.data.id;
      });

    $(".select2-promptprogress")
      .select2()
      .on("select2:select", function (e) {
        _this.selectedPromptProgress = e.params.data.id;
      });

    $(".select2-priority")
      .select2()
      .on("select2:select", function (e) {
        _this.selectedPriority = e.params.data.id;
      });

    $(".select2-promptpriority")
      .select2()
      .on("select2:select", function (e) {
        _this.selectedPromptPriority = e.params.data.id;
      });

    $(".select2-contact-task")
      .select2()
      .on("select2:select", function (e) {
        _this.selectedContact = e.params.data.id;
      });

    $(".select2-promptcontact-task")
      .select2()
      .on("select2:select", function (e) {
        _this.selectedPromptContact = e.params.data.id;
      });
    //$('.select2-condition-task').select2().on("select2:select", function (e) { _this.selectedCondition = e.params.data.id });
    $(".select2-class")
      .select2()
      .on("select2:select", function (e) {
        _this.selectedClass = e.params.data.id;
      });

    $(".select2-promptclass")
      .select2()
      .on("select2:select", function (e) {
        _this.selectedPromptClass = e.params.data.id;
      });

    //
    $(".wrapper").on("shown.bs.modal", function (e) {
      $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
    });
    $(".wrapper").on("shown.bs.tab", "a[data-toggle='tab']", function (e) {
      $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
      _this.onResized();
    });
    $(this.$refs.sqlButton).popover({
      content: 'SQL 執行成功',
      placement: 'top',
      trigger: 'manual'
    });
    $(this.$refs.saveButton).popover({
      content: '保存成功',
      placement: 'top',
      trigger: 'manual'
    });
  },
  created() {
    this.getContacts();
    //this.fetchSqlscriptData();
  },
  computed: {
    bottomPaneHeight() {
      // return window.innerHeight - this.topPaneHeight;
      return this.splitContainerHeight - this.topPaneHeight;
    },
  },
  watch: {
        topTasks(newTasks) {
      // 當 topTasks 改變時，重置 filterTopTasks
      this.filterTopTasks = [...newTasks];
    },
  
    selectedProgress: function () {
      this.taskListChange();
    },
    selectedPriority: function () {
      this.taskListChange();
    },
    selectedContact: function () {
      this.taskListChange();
    },
    selectedClass: function () {
      this.taskListChange();
    },

    selectedPromptProgress: function (newVal) {
      this.filterTasks();
    },
    selectedPromptPriority: function (newVal) {
      this.filterTasks();
    },
    selectedPromptContact: function (newVal) {
      this.filterTasks(); 
    },
    selectedPromptClass: function (newVal) {
      this.filterTasks(); 
    },
    taskPromptText(newVal) {
      this.filterTasks();
    },
    ai_recordPromptID(newVal) {
      this.filterTasks();
    },

    isQueryCollapse() {
      this.$nextTick(() => {
        this.onResized();
      });
    },
    category: function () {
      this.setPromptFilter();
    },
  },
  methods: {
    // meeting選中行
    meeting_row_click(event, data){
      this.meetingRowData = data;
      const meetingId = this.meetingRowData.id;
      console.log(meetingId);
      
       axios.get('/looper/session_manager/get_meeting_detail', {
        params: {id: meetingId}
      })
      .then(response => {
        console.log(response.data); // 成功時的回應數據
        this.$refs.taskTable.datatable.clear().draw(); //清空列表信息
        this.$nextTick(function () {
        this.$refs.taskTable.datatable.rows.add(response.data.data).draw();
            })

      })
      .catch(error => {
        console.error("Error fetching meeting details:", error);
      });
    },

    filterTasks() {
        this.filterTopTasks = this.topTasks.filter(task => {
          console.log(task);
          console.log(task.class);
          return (
            (this.selectedPromptProgress ? task.progress === this.selectedPromptProgress : true) &&
            (this.selectedPromptPriority ? task.priority === this.selectedPromptPriority : true) &&
            (this.selectedPromptClass ? task.class === this.selectedPromptClass : true) &&
            (this.selectedPromptContact ? task.contact === this.selectedPromptContact : true)&&
            (this.taskPromptText ? task.task.includes(this.taskPromptText) : true) &&
            (this.ai_recordPromptID ? task.recordid.includes(this.ai_recordPromptID) : true)
          );
        });
      this.$nextTick(() => {
        // 假設你有表格引用（ref）
        this.$refs.topTask.datatable
          .clear()  // 清空表格
          .rows.add(this.filterTopTasks || [])  // 添加篩選後的數據
          .draw();  // 重繪表格
      });
      console.log(this.filterTopTasks);
    },

    // 清空功能
    clearTopMeeting() {
      this.search.startDate = "";
      this.search.endDate = "";
      this.meetingDataSource = [];
    },
    // 搜索功能
    searchTopMeeting() {
      if (!this.search.startDate || !this.search.endDate) {
        alert(this.$t("Please select both start and end dates"));
        return;
      }
      const params = {
        start_date: this.search.startDate,
        end_date: this.search.endDate,
      };
      console.log("Search Params:", params);
      try {
        axios
          .get("/looper/session_manager/get_meeting_master", { params })
          .then((res) => {
            // console.log(res);
            console.log(res.data.data);
            this.meetingDataSource = res.data.data;

             this.$refs.meetingTable.datatable.clear().draw(); //清空列表信息
              this.$nextTick(function () {
              this.$refs.meetingTable.datatable.rows.add(res.data.data).draw();
                  })
            
          })
          .catch((error) => {
            console.error("Error fetching meeting data:", error);
          });
      } catch (error) {
        console.error("Unexpected error in searchTopMeeting:", error);
      }
    },



    // 初始化 select2 並設置分類選項
    setGoalCategoryOptions() {
      const _this = this;
      _this.goalCategoryOptions=[
          { id: 'Q', text: 'Quarter' }, // Q 代表季度
          { id: 'M', text: 'Month' },    // M 代表月
          { id: 'W', text: 'Week' }      // W 代表周
        ],

          // 初始化 select2 插件
          $('select.select2-goalcategory').select2({
            data: _this.goalCategoryOptions,
            // placeholder: 'Select a category',
            allowClear: true,
          }).on('select2:select', function (e) {
            _this.selectGoalCategory = e.params.data;  // 將選中的整個對象存儲
          });

           // 當 selectGoalCategory 更新時，手動更新 select2 的選中值
          if (_this.selectGoalCategory) {
            $('select.select2-goalcategory').val(_this.selectGoalCategory).trigger('change');
            }

        },

    setGoalNumberOptions() {
      const _this = this;
      _this.goalNumberOptions=[
          { id: '1', text: '1' }, 
          { id: '2', text: '2' },   
          { id: '3', text: '3' },   
          { id: '4', text: '4' }      
        ],

          // 初始化 select2 插件
          $('select.select2-goalnumber').select2({
            data: _this.goalNumberOptions,
            // placeholder: 'Select a number',
            allowClear: true,
          }).on('select2:select', function (e) {
            _this.selectGoalNumber = e.params.data;  // 將選中的整個對象存儲
          });

           // 當 selectGoalNumber 更新時，手動更新 select2 的選中值
          if (_this.selectGoalNumber) {
            $('select.select2-goalnumber').val(_this.selectGoalNumber).trigger('change');
            }

        },

   
    clearTopGoal(){
      this.contact=''
      this.goalYear=''
      $("select.select2-goalnumber").val(null).trigger("change");
      $("select.select2-goalcategory").val(null).trigger("change");
    },
    searchTopGoal(){
        try {
          const contact = this.contact || ''; // 获取 contact
          const goaltype = this.selectGoalCategory.id || ''; // 获取 goaltype
          const year = this.goalYear || ''; // 获取 year
          const number = this.selectGoalNumber.id || ''; // 获取 number

          // 检查 year 是否为空
          if (!year) {
            // 如果 year 为空，弹出提示或处理逻辑
            alert("Year is required!");
            return;  // 结束函数执行，避免发起请求
          }

          axios
            .get("/looper/session_manager/get_Goal_master", {
              params: {
                contact: contact,
                goaltype: goaltype,
                year: year,
                number: number
              }
            })
          .then((res) => {
            // console.log(res);
            console.log(res.data.data);
            this.goalDataSource = res.data.data;

             this.$refs.goalTable.datatable.clear().draw(); //清空列表信息
              this.$nextTick(function () {
              this.$refs.goalTable.datatable.rows.add(res.data.data).draw();
                  })
            
          })
          .catch((error) => {
            console.error("Error fetching meeting data:", error);
          });
      } catch (error) {
        console.error("Unexpected error in searchTopMeeting:", error);
      }
    },

    formatDate(dateStr){
      return dateStr.replace(/-/g, '');
    },
    searchTopTechnical(){
      var params = {}
      if (this.topTechnicalsearch.endDate && this.topTechnicalsearch.startDate) {
        params['bdate'] = this.formatDate(this.topTechnicalsearch.startDate)
        params['edate'] = this.formatDate(this.topTechnicalsearch.endDate)
      }
      params = {
        ...params, 
        'category': this.topTechnicalsearch.category,
        'area': this.topTechnicalsearch.area,
        'technicalID': this.topTechnicalsearch.technicalID,
        'contact': this.contact
      }
      try {
        axios
            .get("/looper/session_manager/get_technical", {
              params,
            })
          .then((res) => {
            this.technicalSource = res.data.data;
             this.$refs.technicalTable.datatable.clear().draw(); //清空列表信息
              this.$nextTick(function () {
              this.$refs.technicalTable.datatable.rows.add(res.data.data).draw();
                  })
          })
          .catch((error) => {
            console.error("Error fetching technical data:", error);
          });
      } catch (error) {
        console.error("Unexpected error in searchTopTechnical:", error);
      }
    },
    clearTopTechnical(){
      this.topTechnicalsearch.endDate = ''
      this.topTechnicalsearch.startDate = ''
      this.topTechnicalsearch.context = ''
      this.topTechnicalsearch.category = ''
      this.topTechnicalsearch.technicalID = ''
      this.topTechnicalsearch.area = ''
      this.technicalSource = [];
      this.$refs.technicalTable.datatable.clear().draw();
      this.$nextTick(function () {
        $("select.select2-contact-tech").val(null).trigger("change");
      });
    },

    technical_row_dbclick(event, data){
      var url = `http://183.63.205.83:8000/zh-hans/PMIS/opportunity/Technical_Material?param={0}`.format(event.mb023)
      window.open(url)
    },
    //提示任務列表單擊事件
    topTask_row_click(event,data){
      if(data == undefined) return
      this.topTaskData = data;
    },
    // 执行SQL并显示结果
    executeSql() {
      // $("#tab_tasks").click();
      this.showTaskData = false;
      console.log('this.topTasks1',this.topTasks);
      const sql = this.currentPrompt.ssql;
      // 检查 SQL 查询是否为空
      if (!sql) {
        alert("SQL查询不能为空");
        return;
      }
      // 发送请求到后端执行 SQL
      axios.post("/looper/session_manager/execute_sql", { sql })
        .then((response) => {
          // console.log("后端响应数据:", response.data);
          if (response.data.status) {
            // 成功时将数据填充到表格
            // 将返回的数据的字段名全部转换为小写
            this.generateHeaders(response.data.columns);
            this.topTasks = response.data.data.map((item) => {
                let newItem = {};
                Object.keys(item).forEach((key) => {
                  newItem[key.toLowerCase()] = item[key];
                });
                return newItem;
            });
            // this.filterTopTasks = [...this.topTasks]; // 初始化 filterTopTasks
            // this.topTasks = response.data.data
            console.log('this.topTasks2',this.topTasks);
            this.showTaskData = true;
            this.$nextTick(function () {
              this.$nextTick(function () {
                this.$refs.topTask.datatable
                  .clear()
                  // .rows.add(this.topTasks || [])
                  .rows.add(this.filterTopTasks || [])
                  .draw();
              });
            });
            this.showSuccessExecuteSqlPopover();
          } else {
            // 处理后端返回的错误信息
            alert( `SQL 执行失败:  ${response.data.msg}`);
          }
        })
        .catch((error) => {
          // 捕获网络错误或其他请求错误
          console.error("执行 SQL 出错:", error);
          alert("执行 SQL 出错，请检查日志");
        });
    },
    showSuccessExecuteSqlPopover() {
      // 显示Popover
      $(this.$refs.sqlButton).popover('show');

      // 1秒后自动关闭
      setTimeout(() => {
        $(this.$refs.sqlButton).popover('hide');
      }, 2000);
    },
    initializeContextMenu() {
      const _this = this;
      $.contextMenu({
        selector: "#top-task .dataTables_scrollBody tbody tr",
        callback: function (key, options) {
          if (key === "group") {
            // 获取top-task表格的数据
            const topTaskTable = _this.$refs.topTask;
            const sessionList = topTaskTable.datatable.data().toArray();

            // POST 数据到后端并跳转到 React 页面
            axios
              .post(
                "/looper/session_manager/session_group_task",
                {
                  sessionList: sessionList, // 确保 sessionList 是一个有效的数组或对象
                },
                {
                  headers: {
                    "Content-Type": "application/json", // 明确指定 Content-Type
                  },
                }
              )
              .then((response) => {
                if (
                  response.status === 200 &&
                  response.data.message === "Data received successfully"
                ) {
                  // 成功后跳转到 React 项目页面，并传递 sessionList 数据
                  window.open(
                    // "http://222.118.20.236:8018/sessionmanager",
                    "http://183.63.205.83:8239/sessionmanager",
                    "_blank"
                  );
                } else {
                  alert("Failed to process the session list");
                }
              })
              .catch((error) => {
                console.error(error);
              });
          }
          /**
          if (key === "sysbug"){
            if(_this.topTaskData.taskno != undefined && _this.topTaskData.taskno.startsWith('11580-3738')){ //必須是上報任務
              axios.get(`/looper/session_manager/get_sysbugno`,{params:{taskno:_this.topTaskData.taskno}}).then(response =>{
                if(response.data.udf10 !== '' && response.data.udf01 != ''){
                  window.open(
                    `http://${window.location.host}/zh-hans/systembugrpt?rp016=${response.data.udf10}&rp017=${response.data.udf01}`,
                    "_blank"
                  );
                }

              })
              .catch(error =>{
                console.log(error);
              })
            }
          }*/
        },
        items: {
          group: {
            name: this.$t('Group Task'), // 任务分组
            icon: "fa-folder-open"

          },
          /**
          sysbug: {
            name: this.$t('View Reported Issues'), // 查看上報信息
            icon: "fa-eye"
          },
          */
        },
      });
    },

    initializeSessionContextMenu() {
        const _this = this;
        // 使用 Vue ref 获取 sessionTable 的 DOM 元素
        const sessionTableElement = this.$refs.sessionTable.$el;

        // 初始化 sessionTable 右键菜单
        $.contextMenu({
            selector: "[class^='treegrid-']", // 匹配所有以 "treegrid-" 开头的类名
            callback: function (key, options) {
                if (key === "addTask") {
                    // 获取当前行的数据
                    const rowData=_this.selsectedTreeRow;
                    if (rowData) {
                        _this.addTask(rowData); 
                    } else {
                        alert("未找到对应的行数据");
                    }
                }
            },
            items: {
                addTask: {
                    name: this.$t('Add Task'),  //添加任務
                    icon: "fa-plus-square",
                },
            },
        });
    },
    // 添加任务逻辑
    addTask(rowData) {
      console.log(rowData);
      window.init_task(undefined,{sessionid:rowData.sessionid})
    },

    startDrag(event) {
      event.preventDefault(); // 阻止默?事件，避免触???等行?
      this.startY = event.clientY || event.touches[0].clientY;
      this.startHeight = this.topPaneHeight;

      $(".topPane.split-pane")
        .removeClass("mb-0")
        .css("margin-bottom", ".5rem");
      if ("#tab_sql.active") {
        $('textarea[name="q_sql"]').attr("rows", 14);
      }

      document.addEventListener("mousemove", this.onDrag);
      document.addEventListener("touchmove", this.onDrag);
      document.addEventListener("mouseup", this.stopDrag);
      document.addEventListener("touchend", this.stopDrag);

      this.onResized();
    },
    onDrag(event) {
      const clientY =
        event.clientY || (event.touches && event.touches[0].clientY);
      if (clientY) {
        const dy = clientY - this.startY;
        this.topPaneHeight = this.startHeight + dy;

        // 更新bottomPaneHeight
        this.splitContainerHeight = this.$refs.splitContainer.offsetHeight;
        this.onResized();
      }
    },
    stopDrag() {
      document.removeEventListener("mousemove", this.onDrag);
      document.removeEventListener("touchmove", this.onDrag);
      document.removeEventListener("mouseup", this.stopDrag);
      document.removeEventListener("touchend", this.stopDrag);

      this.onResized();
    },
    taskListChange() {
      if (this.selsectedTreeRow.sessionid !== undefined) {
        this.getTopTaskData(
          [this.selsectedTreeRow.sessionid],
          this.$refs.taskTable.datatable
        );
      }
      this.getTopTaskData(
        this.allQuerySession,
        this.$refs.taskAllTable.datatable
      );
    },
    async getTopTaskData(sessionList, table) {
      const params = new URLSearchParams();
      params.append("selectedProgress", this.selectedProgress);
      params.append("selectedPriority", this.selectedPriority);
      params.append("selectedContact", this.selectedContact);
      params.append("taskText", this.taskText);
      params.append("selectedClass", this.selectedClass);
      params.append("sessionData", sessionList.join(","));

      try {
        const response = await axios.get(
          "/looper/session_manager/get_filtered_tasks",
          { params }
        );
        table
          .clear()
          .rows.add(response.data.tasks || [])
          .draw();
      } catch (error) {
        console.error(error);
      }
    },
    trim(str) {
      return str.replace(/^\s+|\s+$/g, "");
    },
    getTasks() {
      $("#tab_tasks").click();
      this.showTaskData = false;
      axios
        .get("/looper/session_manager/get_tasks", {
          params: {
            record_id: this.ai_recordID, // 替換為您的SubProjectID
            contact: this.selectedContact, // 替換為您的聯繫人
            condition: this.currentPrompt.inc_id, // 當前選中的條件
            question: this.currentPrompt.sname, //查詢的內容
          },
        })
        .then((response) => {
          // console.log(response);
          //this.sql_script = response.data.sql;
          //this.currentPrompt.ssql=response.data.sql;
          this.currentPrompt = response.data.promtsql;
          this.historySsql = this.currentPrompt.ssql;
          if (!response.data.status) return alert(response.data.msg);
          //const { columns, data } = response.data;
          this.topTasks = response.data.data;
          console.log('首次this.topTasks',this.topTasks);
          this.generateHeaders(response.data.columns);
          this.showTaskData = true;
          this.$nextTick(function () {
            this.$nextTick(function () {
              this.$refs.topTask.datatable
                .clear()
                // .rows.add(this.topTasks || [])
                .rows.add(this.filterTopTasks || [])
                .draw();
            });
          });
          this.filterTasks();//xuan
          console.log(this.filterTopTasks);
          
        })
        .catch((error) => {
          console.log(error);
        });
    },
    queryClickHandler() {
      const params = {
        contact: this.trim(this.contact),
        allContact: this.trim(this.allContact.join(",")),
        recordID: this.trim(this.recordID),
        period: this.trim(this.period),
      };
      try {
        axios
          .get("/looper/session_manager/get_vtask_list_tree", { params })
          .then((res) => {
            this.sessionDataSource = res.data;
            this.$nextTick(function () {
              this.$refs.sessionTable.reLoad();
              if (
                $(".fixed-table-toolbar").attr("class").indexOf("d-none") == -1
              )
                $(".fixed-table-toolbar").addClass("d-none");
            });
            this.allQuerySession = this.sessionDataSource.map(
              (v) => v.sessionid
            );
            if (this.allQuerySession.length !== 0)
              this.getTopTaskData(
                this.allQuerySession,
                this.$refs.taskAllTable.datatable
              );
            this.$refs.taskTable.datatable.clear().rows.add([]).draw();
            this.onResized();
            this.sessionEnquiryMobileUI();
          });
      } catch (error) {
        console.error(error);
      }
    },
    getContacts() {
      this.contactOptions.push("");
      axios.get(`/PMIS/user/get_part_user_names`).then((response) => {
        if (response.data.data.length > 0) {
          response.data.data.forEach((contact) => {
            this.contactOptions.push(contact);
          });
        }
      });
    },
    fetchSqlscriptData() {
      axios
        .get("/looper/session_manager/get_conditon_data")
        .then((response) => {
          this.conditions.push({ inc_id: null, sname: "" });
          if (response.data.length > 0) {
            response.data.forEach((condition) => {
              this.conditions.push(condition);
            });
          }
          var a = this.conditions;
        })
        .catch((error) => {
          //console.error(error);
        });
    },
    generateHeaders(columns) {
      console.log('columns',columns);
      const lowerCaseColumns = columns.map(column => column.toLowerCase());
      // console.log('lowerCaseColumns',lowerCaseColumns);
      this.dataColumns = lowerCaseColumns.map((column) => {
        let header = {
          label: column.toUpperCase(),
          field: column,
        };
        if (["TASK", "REMARK"].includes(column.toUpperCase())) {
          header.width = "360px";
        }
        if (column.toUpperCase().includes("DATE")) {
          header.render = DateRender;
        }
        if (column.toUpperCase().includes("INC_ID")) {
          header.visible = false;
        }
        return header;
      });
      console.log('頭',this.dataColumns);
    },
    showTaskDetail(task) {
      if (task.taskno && task.inc_id) init_task(task.inc_id);
    },
    onConditionSelected(item) {
      //this.currentPrompt = item;
      this.fetchPromtsql(item.inc_id);
      //this.selectedCondition=item.inc_id;
      //this.getTasks();
    },
    onConditionBlur(text) {
      this.currentPrompt.sname = text;
    },
    aiAnalysis() {
      this.aiPredefinedData = this.topTasks;
      this.$nextTick(function () {
        this.$refs.aicombox.$refs.modal.show();
      });
    },
    get_lang_code() {
      if ($("#curr_language_code").val() !== "en") {
        this.lang_code_en = false;
      }
    },
    clearHandler() {
      this.recordID = "";
      this.$nextTick(function () {
        $("select.select2-contact").val(null).trigger("change");
        $("select.select2-contact-mul")
          .val([])
          .trigger("change")
          .siblings("span.select2-container")
          .find("ul.select2-selection__rendered")
          .empty();
      });
    },
    clearTasksHandler() {
      // this.selectedPromptProgress = null;
      // this.selectedPromptPriority = null;
      // this.selectedPromptClass = null;
      // this.selectedPromptContact = null;
      this.taskPromptText = '';
      this.ai_recordPromptID = '';

      // 恢復 topTasks 原始數據到 filterTopTasks
      this.filterTopTasks = [...this.topTasks];


      this.taskText = "";
      this.ai_recordID = "";
      this.isapproved = false;
      this.currentPrompt = {
        inc_id: null,
        sname: "",
        isai: true,
        category: "",
        isapproved: false,
        ssql: "",
      };
      this.category = "";
      this.$nextTick(function () {
        $(
          "select.select2-progress, select.select2-priority, select.select2-class, select.select2-contact-task,select.select2-promptprogress,select.select2-promptclass,select.select2-promptpriority,select.select2-promptcontact-task"
        )
          .val(null)
          .trigger("change");
      });
    },
    onResized() {
      this.$nextTick(() => {
        setTimeout(() => {
          this.splitContainerHeight = this.$refs.splitContainer.offsetHeight; // 更新.split-container元素的高度

          const bottomPaneNavHeight = $(".bottomPane .nav-tabs").height();
          const bottomPaneEnquiryHeight = $(
            ".bottomPane .taskSearch"
          ).outerHeight(true);
          const bottomPaneHeaderHeight = $(
            ".bottomPane>.tab-content .tab-pane.active .LPDataTable .dataTables_scrollHead"
          ).height();
          const bottomPanePagingHeight = $(
            ".bottomPane>.tab-content .tab-pane.active .LPDataTable .dataTables_info"
          ).outerHeight(true);

          $(
            ".bottomPane>.tab-content .tab-pane.active .LPDataTable .dataTables_scrollBody"
          ).height(
            this.bottomPaneHeight -
              bottomPaneNavHeight -
              bottomPaneHeaderHeight -
              bottomPaneEnquiryHeight -
              bottomPanePagingHeight -
              38 +
              "px"
          );

          if ($("body").hasClass("dark-skin")) {
            $(
              ".bottomPane>.tab-content .tab-pane.active .LPDataTable .dataTables_scrollBody"
            ).height(
              this.bottomPaneHeight -
                bottomPaneNavHeight -
                bottomPaneHeaderHeight -
                bottomPaneEnquiryHeight -
                bottomPanePagingHeight -
                38 -
                15 +
                "px"
            );
          }
        }, 300);
      });
    },
    handleTouchEnd(event) {
      const currentTime = new Date().getTime();
      const tapLength = currentTime - this.lastTouchEnd;

      if (tapLength < 300 && tapLength > 0) {
        // 檢測到雙擊
        this.maximizeBottomPane();
      }

      this.lastTouchEnd = currentTime;
    },
    maximizeBottomPane() {
      this.topPaneHeight = 0; // 將頂部面板高度設置為0
      this.$nextTick(() => {
        $(".topPane.split-pane").addClass("mb-0");
        if ("#tab_sql.active") {
          $('textarea[name="q_sql"]').attr("rows", 25);
        }
        this.onResized(); // 刷新頁面布局
      });
    },
    mobileUI() {
      if (SWApp.os.isMobile || SWApp.os.isTablet) {
        $(".taskSearch").removeClass("expanded");
        $(".taskSearch .btn-reset").attr("aria-expanded", "false");
        $(".taskSearch #sessionMgnTaskSearchCollapse").removeClass("show");
      }
    },
    sessionEnquiryMobileUI() {
      if ($(".sessionSearchCard").hasClass("expanded")) {
        $(".sessionSearchCard").removeClass("expanded");
        $("#sessionSearchHeading>.btn-reset").attr("aria-expanded", "false");
        $(".sessionSearchCard #sessionSearchCollapse").removeClass("show");
      }
    },
    savePrompt() {
      if (this.currentPrompt.sname == "")
        return alert(this.$t("Prompt cannot be empty."));
      //this.currentPrompt.ssql = this.sql_script;
      axios
        .post("/looper/session_manager/approve_condition", this.currentPrompt)
        .then((response) => {
          if (response.data.status) {
            this.currentPrompt = response.data.data;
            // alert("保存成功");
            this.showSuccessSavePromptPopover()
          } else {
            alert(response.data.msg);
          }
        })
        .catch((error) => {
          console.error("保存失敗:", error);
        });
    },
    showSuccessSavePromptPopover() {
      // 显示Popover
      $(this.$refs.saveButton).popover('show');

      // 1秒后自动关闭
      setTimeout(() => {
        $(this.$refs.saveButton).popover('hide');
      }, 2000);
    },
    setPromptFilter() {
      const isap = this.isapproved ? 1 : 0;
      const filters = [];

      if (this.category) {
        filters.push(`category=${this.category}`);
      }
      if (this.isapproved) {
        filters.push(`isapproved=${isap}`);
      }

      this.prompt_filter = filters.join(";");
    },
    fetchPromtsql(inc_id) {
      axios
        .get(`/looper/session_manager/promtsql?id=${inc_id}`)
        .then((response) => {
          if (response.data.status) {
            this.currentPrompt = response.data.data;
            this.historySsql = this.currentPrompt.ssql;
          } else {
            alert(response.data.msg || "Failed to fetch Promtsql data.");
          }
        })
        .catch((error) => {
          alert("An error occurred while fetching Promtsql data.");
        });
    },
    getPromptApprove() {
      axios
        .get("/looper/session_manager/get_user_prompt_approve")
        .then((response) => {
          if (response.data.status) {
            this.canApprove = response.data.data;
          } else {
            this.canApprove = false;
          }
        })
        .catch((error) => {
          this.canApprove = false;
        });
    },
    handleSsqlChange() {
      // 當 ssql 的值發生變化時，將 isai 賦值為 false
      if (this.currentPrompt.ssql === this.historySsql) {
        this.currentPrompt.isai = true;
      } else {
        this.currentPrompt.isai = false;
      }
    },
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.onResized);
  },
};
</script>
<style>
/* dataTable 圖標 */
.LPDataTable table.dataTable thead .sorting:before {
  content: "\f0de" !important;
  right: 0.5em !important;
}

.LPDataTable table.dataTable thead .sorting:after {
  content: "\f0dd" !important;
}

.select2-container--open .select2-results__option {
  word-wrap: break-word;
}

.split-container {
  display: flex;
  flex-direction: column; /* ?方向改?列，以??上下分割 */
  height: 100vh;
}

.split-pane {
  overflow: auto;
  border: 1px solid #ddd;
  transition: height 0.2s ease-out;
}

.split-divider {
  height: 7px;
  min-height: 1px;
  cursor: row-resize;
  position: relative;
  flex-shrink: 0;
  touch-action: none;
  border-radius: 12px;
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
  margin: 0 5px -7px 5px;
}

.split-container .split-divider:before,
.split-container .split-divider:after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  transition: background-color 0.3s;
  transform: translate(-50%);
  width: 30px;
  margin-top: -2px;
  height: 2px;
}
.split-container .split-divider:before {
  margin-top: -2px;
}
.split-container .split-divider:after {
  margin-top: 1px;
}

.context-menu-icon.context-menu-icon-fas,
.context-menu-icon.context-menu-icon--fa {
  line-height: 1.5;
}
.context-menu-icon.context-menu-icon-fas::before,
.context-menu-icon.context-menu-icon--fa::before {
  font-family: "Font Awesome 5 Free";
  font-size: 1.1em;
}
</style>