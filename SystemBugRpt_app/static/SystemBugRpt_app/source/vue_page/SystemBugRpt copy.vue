<template>
  <header class="page-title-bar px-3 py-2 mb-2">
    <div class="d-flex justify-content-between">
      <h1 class="page-title mb-0 d-none d-md-block">{{$t('SystemBugRptWindow')}}</h1><!--公司問題處理查看窗口-->
      <h1 class="page-title mb-0 d-block d-md-none">{{$t('Issue Reporting')}}</h1><!--問題上報-->
    </div>
</header>
<div :class="['card systemBugRptCard', masterState == 1 ? 'isNewSIR' : '']">
  <div class="card-header">
  <!-- 功能按鈕以及nav -->
    <ul class="nav nav-tabs card-header-tabs">
      <li class="nav-item">
        <a
          ref="Admrp_details"
          class="nav-link"
          data-toggle="tab"
          href="#Admrp_detail"
        >{{$t('Detail Information')}}</a><!--詳細資料-->
      </li>
      <li class="nav-item">
        <a
          class="nav-link active infoBrowse"
          data-toggle="tab"
          href="#Admrp_list"
          :style="state!==0 ? 'pointer-events: none;' : ''"
        >{{$t('Information Browse')}}</a><!--信息預覽-->
      </li>
      <li class="nav-item">
        <a
          class="nav-link"
          data-toggle="tab"
          href="#Admrp_01"
        >{{$t('Manage Member Info')}}</a><!--信息管理部 Manage Member Info-->
      </li>
      <li class="nav-item">
        <a
          class="nav-link"
          data-toggle="tab"
          href="#Admrp_ai"
          >{{ $t("AI Query") }}</a><!--AI查詢-->
      </li>
      <li class="tools_wrap d-flex align-items-center ml-auto">
        <button type="button" class="btn btn-secondary order-button" data-v-8ec5118a="" @click="openAiRequirementAnalysis">
          <i class="oi oi-document m-0 mr-xl-1" data-v-8ec5118a=""></i>
          <span class="d-none d-xl-inline" data-v-8ec5118a="">需求分析</span><!--需求分析 Requirement Analysis-->
        </button>
        <button type="button" class="btn btn-secondary order-button" data-v-8ec5118a="" @click="refresh_info">
          <i class="oi oi-reload m-0 mr-xl-1" data-v-8ec5118a=""></i>
          <span class="d-none d-xl-inline" data-v-8ec5118a="">{{$t('refresh')}}</span><!--刷新-->
        </button>
        <OperationBar
          ref="buttonBar"
          module_power="65535"
          :function_items="functionArray"
          @on-add="addMaster"
          @on-edit="updateMaster"
          @on-delete="deleteMaster"
          @on-save="saveMasters"
          @on-undo="undoMaster"
          @on-search="masterSearch" 
          button_show="111111000"
          @onFun1="terminateProblem"
          @onFun2="transferProblem"
          @onFun3="showArrangeTaskModel"
        />
      </li>
    </ul>
  <!-- end -->
  </div>
  <div :class="['card-body', isInfoBrowse ? 'py-0' : '']">
    <div class="tab-content">
      <!-- 編輯資料主體 -->
      <div
        class="tab-pane fade"
        id="Admrp_detail"
        role="tabpanel"
      >
        <div class = "row admrpDetail">
          <!--系統問題-->
          <div class="col-12 col-lg-6 leftPane">
            <h5 class="text_deepblue">{{$t('System Issue')}}</h5> <!--系統問題 System Issue-->
              <div :class="['form-group row search_list mb-2', lang_code_en ? 'lang_en' : '']" name="search_list">

                <div class="form-group d-flex align-items-center col-12 col-sm-4 col-lg-6 col-xxl-4 col-xxxxl-3">
                  <label class="col-form-label col-auto">{{$t("ADMRP_rp017")}}</label><!--問題單號 ADMRP_rp017-->
                  <input
                    type="text"
                    v-model="currentMaster.rp017"
                    class="form-control col"
                    disabled
                  />
                </div>
                <div :class="['form-group align-items-center col-12 col-sm-4 col-lg-6 col-xxl-4 col-xxxxl-3', masterState == 1 ? 'd-none d-md-flex' : 'd-flex']">
                  <label class="col-form-label col-auto">{{$t("ADMRP_rp004")}}</label><!--提出人 ADMRP_rp004-->
                  <input
                    type="text"
                    v-model="currentMaster.rp004"
                    class="form-control col"
                    disabled
                  />
                </div>
                <div :class="['form-group align-items-center col-12 col-sm-4 col-lg-6 col-xxl-4 col-xxxxl-3', masterState == 1 ? 'd-none d-md-flex' : 'd-flex']">
                  <label class="col-form-label col-auto">{{$t("ADMRP_rp002")}}</label><!--提出日期 ADMRP_rp002-->
                  <input
                    type="date"
                    v-model="currentMaster.rp002"
                    :class="{'form-control col': true, 'date-hidden': !currentMaster.rp002}" 
                    style="width:133px"
                    disabled
                    required
                  />
                </div>
                <div class="form-group d-flex align-items-center col-12 col-sm-4 col-lg-6 col-xxl-4 col-xxxxl-3">
                  <label class="col-form-label col-auto">{{$t("ADMRP_rp003")}}</label><!--所屬部門 ADMRP_rp003-->
                  <select
                    class="select2-type noFirstVal"
                    v-model="currentMaster.rp003"
                    :disabled="([0].indexOf(state) > -1)"
                  >
                  </select>
                </div>
                <div class="form-group d-flex align-items-center col-12 col-sm-4 col-lg-6 col-xxl-4 col-xxxxl-3 query_issueType mb_xxxxl_2">
                  <label class="col-form-label col-auto">{{$t("ADMRP_rp044")}}</label><!--上報類型 ADMRP_rp044-->
                  <select
                    class="form-control col"
                    v-model="currentMaster.rp044"
                    :disabled="([0].indexOf(state) > -1)"
                  >
                    <option value="1">需求</option>
                    <option value="2">維護</option>
                    <option value="3">維修</option>
                    <option value="4">穩定性</option>
                    <option value="5">添加字段</option>
                    <option value="6">邏輯增強</option>
                    <option value="7">邏輯變更</option>
                  </select>
                </div>

                <div class="form-group d-flex align-items-center col-12 col-sm-4 col-lg-6 col-xxl-4 col-xxxxl-3 mb_xxxxl_2">
                  <label class="col-form-label col-auto">{{$t("ADMRP_rp011")}}</label><!--處理狀態 ADMRP_rp011-->
                  <select
                    class="form-control col"
                    v-model="currentMaster.rp011"
                    :disabled="([0].indexOf(state) > -1)"
                  >
                    <option value="N">未處理</option>
                    <option value="I">處理中</option>
                    <option value="F">已處理</option>
                    <option value="T">暫時處理</option>
                  </select>
                </div>
                <div class="form-group d-flex align-items-center col-12 col-sm-4 col-lg-6 col-xxl-4 col-xxxxl-3 mb_xxxxl_2">
                  <label class="col-form-label col-auto">{{$t("ADMRP_rp043")}}</label><!--原始提出人 ADMRP_rp043-->
                  <input
                    type="text"
                    v-model="currentMaster.rp043"
                    :disabled="([0].indexOf(state) > -1)"
                    class="form-control col"
                  />
                </div>
                <div :class="['form-group flex-wrap align-items-center col-12 mb-1', masterState == 1 ? 'd-none d-md-flex' : 'd-flex']">
                  <label class="col-form-label text_deepblue col-auto">{{$t('Notice')}}: {{$t('Notice_1')}}</label><!--提示: 1.只有問題的創建者才能修改問題描述和提交附件.-->
                  <label class="col-form-label text_deepblue col-auto">{{$t('Notice_2')}}</label><!--2.硬件問題請直接轉交給電腦部網絡組處理,軟件問題先提交給信管部處理.-->
                </div>
                <div class="form-group d-flex align-items-center col-12 mb-1 admrp_addAttachment">
                  <label class="col-form-label col-auto">{{$t("AddAttachment")}}</label><!--添加附件 AddAttachment-->
                  <div :class="['btn btn-sm btn-secondary fileinput-button mb-0', !([1].indexOf(state) > -1) ? 'disabled' : '']">
                    <i class="fa fa-plus fa-fw"></i> <span>{{$t('Choose files')}}</span>
                    <input ref="fileInput" type="file" name="files[]" @change="uploadFile($event,'F')" :disabled="!([1].indexOf(state) > -1)" multiple>
                  </div>
                  <!--Attached files 附件-->
                </div>

                <!--附件列表-->
                <div class="modal-body" v-show="fileArray_left.length!==0">
                  <div class="list-group list-group-flush list-group-divider filelist">
                    <div class="list-group-item" v-for="(item,index) in fileArray_left" :key="index">
                      <div class="list-group-item-body py-2">
                        <h4 class="list-group-item-title text-truncate">{{item.rq005}}</h4>
                      </div>
                      <div class="list-group-item-figure pr-0 py-2">
                        <a class="btn btn-sm btn-icon btn-light text-dark" @click="previewFile(item.inc_id)" ><i class="oi oi-eye"></i></a>
                        <a class="btn btn-sm btn-icon btn-light text-dark" :href="'/systembugrpt/download_file?inc_id=' + item.inc_id" v-show="([0].indexOf(state) > -1)" ><i class="oi oi-data-transfer-download"></i></a>
                        <button class="btn btn-sm btn-icon btn-light text-dark" @click="admrqDelete(index)" v-show="([1].indexOf(state) > -1)"><i class="far fa-trash-alt"></i></button>
                      </div>
                    </div>
                  </div>
                </div>
                <!--附件列表-->

                <div class="form-group col-12 query_issueDescp">
                  <label :class="['col-form-label col-auto', masterState == 1 ? 'd-none d-md-inline-block': 'd-inline-block']">{{$t("ADMRP_rp005")}}</label><!--問題描述 ADMRP_rp005-->
                  <textarea type="text" class="form-control col" :rows="textareaRows" v-model="currentMaster.rp005" :disabled="!([1].indexOf(state) > -1)"></textarea>
                </div>

                <div class="form-group col-12 query_issueDescp">
                  <label :class="['col-form-label col-auto', masterState == 1 ? 'd-none d-md-inline-block': 'd-inline-block']"> {{ $t('Handler Description') }} </label><!--處理者描述 Mô tả người xử lý-->
                  <textarea type="text" class="form-control col" :rows="textareaRows" v-model="currentMaster.task" :disabled="!([1].indexOf(state) > -1)"></textarea>
                </div>
              </div>
              <p class="text_deepblue mb-2 mx_5">{{$t('Related Pictures')}}</p><!--Related Pictures 相關圖片-->
            <div :class="['card mx_5', bugImgArray.length !==0 || masterState !== 0 ? 'card-reflow' : 'cardWrap']">
              <UploadImage ref="admrp_img_ref" :multiple="true" :enabled="([1,2].indexOf(masterState) > -1)" :acceptImagesOnly="1==1" @duplicate_file_detected="duplicate_file_detected"/>
            </div>
          </div>

          <!--處理結果 TheResults-->
          <div class="col-12 col-lg-6 rightPane">
            <h5 style="color:red">{{$t('TheResults')}}</h5>

              <!-- .nav-tabs -->
              <ul class="nav nav-tabs">
                <li class="nav-item">
                  <a class="nav-link active show" data-toggle="tab" href="#otherDept">{{$t('OtherDept')}}</a> <!--其它部門 OtherDept-->
                </li>
                <li class="nav-item">
                  <a class="nav-link" data-toggle="tab" href="#computerDept">{{$t('ComputerDept')}}</a><!--電腦部 ComputerDept-->
                </li>         
              </ul>
              <!-- /.nav-tabs -->
            <div class="tab-content pt-3">
              <div
                class="tab-pane fade active show"
                id="otherDept"
                role="tabpanel"
              >
              <!--其它部門-->
                <div :class="['form-group row search_list mb-0', lang_code_en ? 'lang_en' : '']" name="search_list">
                  <!--其它部門-->
                  <div class="form-group d-flex align-items-center col-12 col-sm-4 col-lg-6 col-xxl-4 col-xxxl-3">
                    <label class="col-form-label col-auto">{{$t("ADMRP_rp010")}}</label><!--跟進人 ADMRP_rp010-->
                    <input
                      type="text"
                      v-model="currentMaster.rp010"
                      :disabled="([0].indexOf(state) > -1)"
                      class="form-control col"
                    />
                  </div>
                  <div class="form-group d-flex align-items-center col-12 col-sm-4 col-lg-6 col-xxl-4 col-xxxl-3" >
                    <label class="col-form-label col-auto">{{$t("ADMRP_rp009")}}</label><!--跟進部門 ADMRP_rp009-->
                    <select class="select2-genjin noFirstVal" :disabled="([0].indexOf(state) > -1)" v-model="currentMaster.rp009"></select>
                  </div>
                  <div class="form-group d-flex align-items-center col-12 col-sm-4 col-lg-6 col-xxl-4 col-xxxl-3" >
                    <label class="col-form-label col-auto">{{$t("ADMRP_rp021")}}</label><!--問題類型 ADMRP_rp021-->
                    <select
                      class="form-control col"
                      v-model="currentMaster.rp021"
                      :disabled="([0].indexOf(state) > -1)"
                    >
                      <option value=""></option>
                      <option value="A">A.系統流程問題</option>
                      <option value="B">B.程序報錯</option>
                      <option value="C">C.數據錯誤</option>
                      <option value="D">D.用戶需求</option>
                      <option value="E">E.部門協助</option>
                      <option value="F">F.其它問題(開發)</option>
                      <option value="G">G.電腦軟件</option>
                      <option value="H">H.打印機</option>
                      <option value="J">J.操作系統</option>
                      <option value="K">K.網絡問題</option>
                      <option value="L">L.Email問題</option>
                      <option value="M">M.其它電腦問題</option>
                    </select>
                  </div>
                  <div class="form-group d-flex align-items-center col-12 col-sm-4 col-lg-6 col-xxl-4 col-xxxl-3" >
                    <label class="col-form-label col-auto">{{$t("ADMRP_rp049")}}</label><!--預計時間 ADMRP_rp049-->
                    <input
                      type="number"
                      v-model="currentMaster.rp049"
                      :disabled="([0].indexOf(state) > -1)"
                      class="form-control col"
                    />
                  </div>
                  <div class="form-group d-flex align-items-center col-12 col-sm-4 col-lg-6 col-xxl-4 col-xxxl-3" >
                    <label class="col-form-label col-auto">{{$t("ADMRP_rp031")}}</label><!--計劃開始 ADMRP_rp031-->
                    <input
                      type="date"
                      :disabled="([0].indexOf(state) > -1)"
                      :class="{'form-control col': true, 'date-hidden': !currentMaster.rp031}" 
                      v-model="currentMaster.rp031"
                      required
                      style="width:133px"
                    />
                  </div>
                  <div class="form-group d-flex align-items-center  col-12 col-sm-4 col-lg-6 col-xxl-4 col-xxxl-3" >
                    <label class="col-form-label col-auto">{{$t("ADMRP_rp032")}}</label><!--計劃結束 ADMRP_rp032-->
                    <input
                      type="date"
                      v-model="currentMaster.rp032"
                      :disabled="([0].indexOf(state) > -1)"
                      :class="{'form-control col': true, 'date-hidden': !currentMaster.rp032}" 
                      required
                      style="width:133px"
                    />
                  </div>
                  <div class="form-group d-flex align-items-center  col-12 col-sm-4 col-lg-6 col-xxl-4 col-xxxl-3" >
                    <label class="col-form-label col-auto">{{$t("ADMRP_rp029")}}</label><!--問題級別 ADMRP_rp029-->
                    <select
                      class="form-control col"
                      v-model="currentMaster.rp029"
                      :disabled="([0].indexOf(state) > -1)"
                    >
                      <option value=""></option>
                      <option value="1">Class 1</option>
                      <option value="2">Class 2</option>
                      <option value="3">Other</option>
                    </select>
                  </div>
                  <div class="form-group d-flex align-items-center  col-12 col-sm-4 col-lg-6 col-xxl-4 col-xxxl-3" >
                    <label class="col-form-label col-auto">{{$t("ADMRP_rp033")}}</label><!--優先級 ADMRP_rp033-->
                    <select
                      class="form-control col"
                      v-model="currentMaster.rp033"
                      :disabled="([0].indexOf(state) > -1)"
                    >
                      <option value=""></option>
                      <option value="888">888</option>
                      <option value="8888">8888</option>
                      <option value="8889">8889</option>
                    </select>
                  </div>
                  <div class="form-group d-flex align-items-center col-12 col-sm-4 col-lg-6 col-xxl-4 col-xxxl-3" >
                    <label class="col-form-label col-auto">{{$t("ADMRP_rp045")}}</label><!--規則 ADMRP_rp045-->
                    <input
                      type="text"
                      v-model="currentMaster.rp045"
                      :disabled="([0].indexOf(state) > -1)"
                      class="form-control col"
                    />
                  </div>
                  <div class="form-group d-flex align-items-center col col-sm-4 col-lg col-xxl-4 col-xxxl-3 query_relationTask" >
                    <label class="col-form-label col-auto">{{$t("ADMRP_rp024")}}</label><!--關聯任務 ADMRP_rp024-->
                    <input
                      type="text"
                      v-model="currentMaster.rp024"
                      :disabled="([0].indexOf(state) > -1)"
                      class="form-control col"
                    />
                  <div class="tile bg-success query_relationTaskTile" style="cursor: pointer;" @click="showReadRelationTaskModel">
                    <span class="oi oi-chat"></span>
                  </div>
                  </div>
                  <div class="form-group d-flex align-items-center col-12 col-sm-8 col-lg-12 col-xxl-8 col-xxxl-6 problemCategory">
                    <label class="col-form-label caption col-auto pl-0"><span class="required">*</span>{{ $t('Problem Category') }}</label> <!--問題類別-->
                    <select class="select2-problemcategory form-control" name="problemcategory" v-model="currentMaster.problemcategory" :disabled="([0].indexOf(state) > -1)"></select>
                  </div>
                  <div class="form-group d-flex align-items-center  col-12 col-sm-4 col-lg-6 col-xxl-4 col-xxxl-3" >
                    <label class="col-form-label col-auto">{{ $t('Result') }}</label><!--處理結果 ADMRP_processtype-->
                    <select
                      class="form-control col"
                      :disabled="([0].indexOf(state) > -1)"
                      v-model="currentMaster.processtype"
                    >
                      <option value=""></option>
                      <option value="S">S:Satisfied</option><!--滿意-->
                      <option value="A">A:Alternative</option><!--替換-->
                      <option value="N">N:UnKnown</option><!--未知的-->
                      <!--需要測試-->
                      <!-- <option value="T">T:Need to Test</option> -->
                      <option value="T">T:Temporary </option><!--臨時的-->
                      <option value="I">I:Checking</option><!--校驗-->
                      <option value="C">C:Confirmed</option><!--確認的-->
                    </select>
                  </div>
                  <div class="form-group d-flex align-items-center col-12 col-sm-4 col-lg-6 col-xxl-4 col-xxxl-3" >
                    <label class="col-form-label col-auto"><span class="required">*</span>{{$t("ADMRP_rp020")}}</label><!--系統名稱 ADMRP_rp020-->
                    <input
                      type="text"
                      class="form-control col"
                      v-model="currentMaster.rp020"
                      @click="showSystemModal"
                      :disabled="([0].indexOf(state) > -1)"
                    />
                  </div>
                  <div class="form-group d-flex align-items-center col-12 col-sm-4 col-lg-6 col-xxl-4 col-xxxl-3" >
                    <label class="col-form-label col-auto"><span class="required">*</span>{{$t("ADMRP_rp027")}}</label><!--功能描述 ADMRP_rp027-->
                    <textarea type="text" class="form-control col" v-model="currentMaster.rp027c" :disabled="([0].indexOf(state) > -1)" style="flex: 1;" @click="showDocmhModal"></textarea>
                    <input
                      type="text"
                      class="form-control col"
                      v-model="currentMaster.rp027"
                      v-show="false"
                      :disabled="([0].indexOf(state) > -1)"
                    />
                  </div>
                  <div class="form-group d-flex align-items-center col-12 col-sm-4 col-lg-6 col-xxl-4 col-xxxl-3" >
                    <label class="col-form-label col-auto">{{$t("SessionPriority")}}</label><!--模塊優先級 SessionPriority-->
                    <input
                      type="text"
                      class="form-control col"
                      v-model="currentMaster.sessionpriority"
                      :disabled="([0].indexOf(state) > -1)"
                    />
                  </div>
                  <!-- <div class="form-group d-flex align-items-center col-12 col-sm-4 col-lg-6 col-xxl-4 col-xxxl-3" >
                    <label class="col-form-label col-auto">{{'Rule'}}</label>
                    <input
                      type="text"
                      class="form-control col"
                      v-model="currentMaster.rule"
                      :disabled="([0].indexOf(state) > -1)"
                    />
                  </div>
                  <div class="form-group d-flex align-items-center col-12 col-sm-4 col-lg-6 col-xxl-4 col-xxxl-3" >
                    <label class="col-form-label col-auto">{{'Logic'}}</label>
                    <input
                      type="text"
                      class="form-control col"
                      v-model="currentMaster.logic"
                      :disabled="([0].indexOf(state) > -1)"
                    />
                  </div>
                  <div class="form-group d-flex align-items-center col-12 col-sm-4 col-lg-6 col-xxl-4 col-xxxl-3" >
                    <label class="col-form-label col-auto">{{'Policy'}}</label>
                    <input
                      type="text"
                      class="form-control col"
                      v-model="currentMaster.policy"
                      :disabled="([0].indexOf(state) > -1)"
                    />
                  </div> -->

                  <div class="form-group d-flex align-items-center col-12 col-xxxl-6">
                    <label class="col-form-label col-auto">{{ $t('RelationId') }}</label><!--關聯上報單號-->
                    <textarea type="text" class="form-control col" v-model="currentMaster.relationid" :disabled="([0].indexOf(state) > -1)" style="flex: 1;"></textarea>
                    <div class="tile bg-success query_relationTaskTile" style="cursor: pointer;" @click="searchSysBugNoModal">
                      <span class="oi oi-chat"></span>
                    </div>
                  </div>

                  <div class="form-group d-flex align-items-center col-12 mb-2" >
                    <label class="col-form-label col-auto">{{$t("AddAttachment")}}</label><!--添加附件 AddAttachment-->
                    <div :class="['btn btn-sm btn-secondary fileinput-button mb-0 mr-3', !([1].indexOf(state) > -1) ? 'disabled' : '']">
                      <i class="fa fa-plus fa-fw"></i> <span>{{$t('Choose files')}}</span>
                      <input ref="fileInput2" type="file" name="files[]" @change="uploadFile($event,'R')" :disabled="!([1].indexOf(state) > -1)" multiple>
                    </div>
                    <!--Attached files 附件-->
                  </div>
                  <!--附件列表-->
                  <div class="modal-body">
                    <div class="list-group list-group-flush list-group-divider filelist">
                      <div class="list-group-item" v-for="(item,index) in fileArray_right" :key="index">
                        <div class="list-group-item-body py-2">
                          <h4 class="list-group-item-title text-truncate">{{item.rq005}}</h4>
                        </div>
                        <div class="list-group-item-figure pr-0 py-2">
                          <a class="btn btn-sm btn-icon btn-light text-dark" @click="previewFile(item.inc_id)" ><i class="oi oi-eye"></i></a>
                          <a class="btn btn-sm btn-icon btn-light text-dark" :href="'/systembugrpt/download_file?inc_id=' + item.inc_id" v-show="([0].indexOf(state) > -1)"><i class="oi oi-data-transfer-download"></i></a>
                          <button class="btn btn-sm btn-icon btn-light text-dark" @click="admrqRightDelete(index)" v-show="([1].indexOf(state) > -1)"><i class="far fa-trash-alt"></i></button>
                        </div>
                      </div>
                    </div>
                  </div>
                  <!--附件列表-->
                </div>
              <!--其它部門-->
              </div>
              <div
                class="tab-pane fade"
                id="computerDept"
                role="tabpanel"
              >
              <!--電腦部-->
                <div :class="['form-group row search_list mb-1', lang_code_en ? 'lang_en' : '']" name="search_list">
                  <div class="form-group d-flex align-items-center col-12 col-sm-6 col-xxl-4" >
                    <label class="col-form-label col-auto"><span class="required">*</span>{{$t("ADMRP_rp020")}}</label><!--系統名稱 ADMRP_rp020-->
                    <input
                      type="text"
                      class="form-control col"
                      v-model="currentMaster.rp020"
                      @click="showSystemModal"
                      :disabled="([0].indexOf(state) > -1)"
                    />
                  </div>
                  <div class="form-group d-flex align-items-center col-12 col-sm-6 col-xxl-4" >
                    <label class="col-form-label col-auto"><span class="required">*</span>{{$t("ADMRP_rp027")}}</label><!--功能描述 ADMRP_rp027-->
                    <textarea type="text" class="form-control col" v-model="currentMaster.rp027c" :disabled="([0].indexOf(state) > -1)" style="flex: 1;" @click="showDocmhModal"></textarea>
                    <input
                      type="text"
                      class="form-control col"
                      v-model="currentMaster.rp027"
                      v-show="false"
                      :disabled="([0].indexOf(state) > -1)"
                    />
                  </div>
                  <div class="form-group d-flex align-items-center col-12 col-sm-6 col-xxl-4" >
                    <label class="col-form-label col-auto">{{$t("ADMRP_rp022")}}</label><!--窗體名稱 ADMRP_rp022-->
                    <input
                      type="text"
                      class="form-control col"
                      v-model="currentMaster.rp022"
                      @click="showModuleModal"
                      :disabled="([0].indexOf(state) > -1)"
                    />
                  </div>
                  <div class="form-group d-flex align-items-center col-12 col-sm-6 col-xxl-4" >
                    <label class="col-form-label col-auto">{{$t("ADMRP_rp028")}}</label><!--功能依賴對象 ADMRP_rp028-->
                    <input
                      type="text"
                      class="form-control col"
                      v-model="currentMaster.rp028"
                      @click="showModuleObjectModal"
                      :disabled="([0].indexOf(state) > -1)"
                    />
                  </div>
                  <div class="form-group d-flex align-items-center col-12 col-sm-6 col-xxl-4" >
                    <label class="col-form-label col-auto">{{$t("ADMRP_rp023")}}</label><!--問題所屬項目 ADMRP_rp023-->
                    <input
                      type="text"
                      class="form-control col"
                      v-model="currentMaster.rp023"
                      disabled
                    />
                  </div>
                  <div class="form-group d-flex align-items-center col-12 col-sm-6 col-xxl-4" >
                    <label class="col-form-label col-auto">{{$t("ADMRP_rp001")}}</label><!--版本 ADMRP_rp001-->
                    <input
                      type="text"
                      class="form-control col"
                      v-model="currentMaster.rp001"
                      disabled
                    />
                  </div>
                  <div class="form-group d-flex align-items-center col-12 col-sm-6 col-xxl-4" >
                    <label class="col-form-label col-auto">{{$t("ADMRP_rp012")}}</label><!--實際開始 ADMRP_rp012-->
                    <input
                      type="date"
                      required
                      style="width:133px"
                      v-model="currentMaster.rp012"
                      :class="{'form-control col': true, 'date-hidden': !currentMaster.rp012}" 
                      :disabled="([0].indexOf(state) > -1)"
                    />
                  </div>
                  <div class="form-group d-flex align-items-center col-12 col-sm-6 col-xxl-4" >
                    <label class="col-form-label col-auto">{{$t("ADMRP_rp013")}}</label><!--實際完成 ADMRP_rp013-->
                    <input
                      type="date"
                      required
                      style="width:133px"
                      v-model="currentMaster.rp013"
                      :class="{'form-control col': true, 'date-hidden': !currentMaster.rp013}"
                      :disabled="([0].indexOf(state) > -1)"
                    />
                  </div>
                  <div class="form-group d-flex align-items-center col-12 col-sm-6 col-xxl-4" >
                    <label class="col-form-label col-auto">{{$t("ADMRP_rp026")}}</label><!--更新開發版 ADMRP_rp026-->
                    <select
                      class="form-control col"
                      v-model="currentMaster.rp026"
                      :disabled="([0].indexOf(state) > -1)"
                    >
                      <option value="Y">Yes</option>
                      <option value="N">No</option>
                    </select>
                  </div>
                  <div class="form-group d-flex align-items-center col-12 col-sm-6 col-xxl-4" >
                    <label class="col-form-label col-auto">{{$t("ADMRP_rp025")}}</label><!--更新穩定版 ADMRP_rp025-->
                    <select
                      class="form-control col"
                      v-model="currentMaster.rp025"
                      :disabled="([0].indexOf(state) > -1)"
                    >
                      <option value="Y">Yes</option>
                      <option value="N">No</option>
                    </select>
                  </div>
                  <div class="form-group d-flex align-items-center col-12 col-sm-6 col-xxl-4" >
                    <label class="col-form-label col-auto">{{$t("ADMRP_rp030")}}</label><!--是否重要窗口 ADMRP_rp030-->
                    <select
                      class="form-control col"
                      v-model="currentMaster.rp030"
                      :disabled="([0].indexOf(state) > -1)"
                    >
                      <option value="Y">Yes</option>
                      <option value="N">No</option>
                    </select>
                  </div>
                  <div class="form-group d-flex align-items-center col-12 col-xxxl-6">
                    <label class="col-form-label col-auto">{{ $t('RelationId') }}</label><!--關聯上報單號-->
                    <textarea type="text" class="form-control col" v-model="currentMaster.relationid" :disabled="([0].indexOf(state) > -1)" style="flex: 1;"></textarea>
                    <div class="tile bg-success query_relationTaskTile" style="cursor: pointer;" @click="searchSysBugNoModal">
                      <span class="oi oi-chat"></span>
                    </div>
                  </div>
                </div>
              <!--電腦部-->
              </div>

              <div :class="['form-group row search_list results_otherDept mb-1', lang_code_en ? 'lang_en' : '']" name="search_list">
                <div class="form-group d-flex align-items-center col-12 col-xxxl-6">
                  <label class="col-form-label col-auto"><span class="required">*</span>{{$t("SolutionType")}}</label><!--SolutionType 解決方案類型-->
                  <textarea type="text" class="form-control col" v-model="currentMaster.solutiontype" :disabled="([0].indexOf(state) > -1)" style="flex: 1;"></textarea>
                  <div class="tile bg-success query_relationTaskTile" style="cursor: pointer;" @click="showSolutionTypeModel">
                    <span class="oi oi-chat"></span>
                  </div>
                </div>
                <div class="form-group d-flex align-items-center col-12 col-xxxl-6">
                  <label class="col-form-label col-auto">{{ $t('ADMRP_description') }}</label><!--Description 說明-->
                  <textarea type="text" class="form-control col" v-model="currentMaster.description" :disabled="([0].indexOf(state) > -1)"></textarea>
                </div>
                <div class="form-group d-flex align-items-center col-12 col-xxxl-6">
                  <label class="col-form-label col-auto"><span class="required">*</span>{{$t("ADMRP_rp007")}}</label><!--處理方式 ADMRP_rp007-->
                  <textarea type="text" class="form-control col mr_40" v-model="currentMaster.rp007" :disabled="([0].indexOf(state) > -1)"></textarea>
                </div>
                <div class="form-group d-flex align-items-center col-12 col-xxxl-6">
                  <label class="col-form-label col-auto">{{$t("ADMRP_rp008")}}</label><!--問題原因 ADMRP_rp008-->
                  <textarea type="text" class="form-control col" v-model="currentMaster.rp008" :disabled="([0].indexOf(state) > -1)"></textarea>
                </div>
                <div class="form-group d-flex align-items-center col-12 col-xxxl-6">
                  <label class="col-form-label col-auto">{{$t("ADMRP_rp046")}}</label><!--影響的表 ADMRP_rp046-->
                  <textarea type="text" class="form-control col mr_40" v-model="currentMaster.rp046" :disabled="([0].indexOf(state) > -1)"></textarea>
                </div>
                <div class="form-group d-flex align-items-center col-12 col-xxxl-6">
                  <label class="col-form-label col-auto">{{$t("ADMRP_rp048")}}</label><!--預計結果 ADMRP_rp048-->
                  <textarea type="text" class="form-control col" v-model="currentMaster.rp048" :disabled="([0].indexOf(state) > -1)"></textarea>
                </div>
                <div class="form-group d-flex align-items-center col-12 col-xxxl-6">
                  <label class="col-form-label col-auto">{{$t("Remark")}}</label><!--備註-->
                  <textarea type="text" class="form-control col mr_40" v-model="currentMaster.remark" :disabled="([0].indexOf(state) > -1)"></textarea>
                </div>
              </div>

              <!--流程圖列表-->
              <div class="d-flex justify-content-end mb-2 flowChartWrap">
                <button 
                  type="button"
                  class="btn btn-sm btn-primary mr-1"
                  @click="show_flowChartModel('1')"
                >
                  <i class="fa fa-plus m-0"></i
                  >
                </button>
              </div>

              <LPDataTable
                :paging="false"
                :paging_inline="true"
                :searching="false"
                :columns="flowChartColumns"
                :custom_options="flowChartOptions"
                :custom_params_fun="flowChart_params_fun"
                @on_row_click="flowChart_row_click"
                :datasource="[]"
                ref="flowChartTable"
              />
              <br/>
              <!--流程圖列表-->

              <!--問題跟進狀態-->
              <p class="text_deepblue mb-0 mx_5">{{$t('Question follow up state')}}:<label class="col-form-label text-lg-right col-auto" v-html="currentMaster.rp024"></label></p> <!--問題跟進狀態 Question follow up state-->
              <LPDataTable
                ref="taskItemTable"
                :columns="taskItemColumns"
                datasource="/systembugrpt/taskitem_table?format=datatables"
                :custom_params_fun="taskItemParamsFun"
                :custom_options="taskItemOptions"
                :paging_inline="true"
                :searching="false"
                :pageLength="25"
              />
              <!--問題跟進狀態-->

            </div>
          </div>
        </div>
        
        <!-- end -->
      </div>
      <!-- end -->
        
      <!-- Master列表-->
      <div
        class="tab-pane fade active show"
        id="Admrp_list"
        role="tabpanel"                
      >
        <LPDataTable
          ref="AdmrpTable"
          :columns="masterColumns"
          datasource="/systembugrpt/admrp_table?format=datatables"
          :custom_params_fun="masterParamsFun"
          :custom_options="masterOptions"
          :orderBy="masterTable_order_by"
          :paging_inline="true"
          :searching="false"
          :pageLength="25"
          @on_row_click="master_row_click"
          @on_dbclick="master_db_click"
        />
      </div>

      <!--信息管理部-->
      <div
        class="tab-pane fade"
        id="Admrp_01"
        role="tabpanel"                
      >
        <div class = "row manageMemberInfo">
          <!--系統問題 System Issue-->
          <div class="col-12 col-lg-6 leftPane">
            <h5 class="text_deepblue">{{$t('System Issue')}}</h5>
            <div :class="['form-group row search_list mb-0', lang_code_en ? 'lang_en' : '']" name="search_list">

              <div class="form-group d-flex align-items-center col-12 col-sm-6 col-lg-12 col-xl-6 col-xxl-4 col-xxxxl-3">
                <label class="col-form-label col-auto">{{$t("ADMRP_rp017")}}</label><!--單號 ADMRP_rp017-->
                <input
                  type="text"
                  v-model="currentMaster.rp017"
                  class="form-control col"
                  disabled
                />
              </div>
              <div class="form-group d-flex align-items-center col-12 col-sm-6 col-lg-12 col-xl-6 col-xxl-4 col-xxxxl-3">
                <label class="col-form-label col-auto">{{$t("ADMRP_rp004")}}</label><!--提出人 ADMRP_rp004-->
                <input
                  type="text"
                  v-model="currentMaster.rp004"
                  class="form-control col"
                  disabled
                />
              </div>
              <div class="form-group d-flex align-items-center col-12 col-sm-6 col-lg-12 col-xl-6 col-xxl-4 col-xxxxl-3">
                <label class="col-form-label col-auto">{{$t("ADMRP_rp002")}}</label><!--提出日期 ADMRP_rp002-->
                <input
                  type="date"
                  v-model="currentMaster.rp002"
                  required
                  style="width:133px"
                  disabled
                  :class="{'form-control col': true, 'date-hidden': !currentMaster.rp002}"
                />
              </div>
              <div class="form-group d-flex align-items-center col-12 col-sm-6 col-lg-12 col-xl-6 col-xxl-4 col-xxxxl-3">
                <label class="col-form-label col-auto">{{$t("ADMRP_modifier")}}</label><!--修改者 ADMRP_modifier-->
                <input
                  type="text"
                  v-model="currentMaster.modifier"
                  class="form-control col"
                  disabled
                />
              </div>
              <div class="form-group d-flex align-items-center col-12 col-sm-6 col-lg-12 col-xl-6 col-xxl-4 col-xxxxl-3">
                <label class="col-form-label col-auto">{{$t("ADMRP_modi_date")}}</label><!--修改日期 ADMRP_modi_date-->
                <input
                  type="text"
                  v-model="currentMaster.modi_date"
                  class="form-control col"
                  disabled
                />
              </div>
              <div class="form-group d-flex align-items-center col-12 col-sm-6 col-lg-12 col-xl-6 col-xxl-4 col-xxxxl-3">
                <label class="col-form-label col-auto">{{$t("ADMRP_rp011")}}</label><!--處理狀態 ADMRP_rp011-->
                <select
                  class="form-control col"
                  v-model="currentMaster.rp011"
                  :disabled="([0].indexOf(state) > -1)"
                >
                  <option value="N">未處理</option>
                  <option value="I">處理中</option>
                  <option value="F">已處理</option>
                  <option value="T">暫時處理</option>
                </select>
              </div>
              <div class="form-group d-flex align-items-center col-12 col-sm-6 col-lg-12 col-xl-6 col-xxl-4 col-xxxxl-3">
                <label class="col-form-label col-auto">{{$t("ADMRP_rp043")}}</label><!--原始提出人 ADMRP_rp043-->
                <input
                  type="text"
                  v-model="currentMaster.rp043"
                  :disabled="([0].indexOf(state) > -1)"
                  class="form-control col"
                />
              </div>
              <div class="form-group d-flex align-items-center col-12 col-sm-6 col-lg-12 col-xl-6 col-xxl-4 col-xxxxl-3">
                <label class="col-form-label col-auto">{{$t("ADMRP_rp044")}}</label><!--上報類型 ADMRP_rp044-->
                <select
                  class="form-control col"
                  v-model="currentMaster.rp044"
                  :disabled="([0].indexOf(state) > -1)"
                >
                  <option value="1">需求</option>
                  <option value="2">維護</option>
                  <option value="3">維修</option>
                  <option value="4">穩定性</option>
                  <option value="5">添加字段</option>
                  <option value="6">邏輯增強</option>
                  <option value="7">邏輯變更</option>
                </select>
              </div>
              <div class="form-group d-flex align-items-center col-12 col-sm-6 col-lg-12 col-xl-6 col-xxl-4 col-xxxxl-3">
                <label class="col-form-label col-auto">{{$t("ADMRP_rp003")}}</label><!--部門 ADMRP_rp003-->
              <select class="select2-type2 noFirstVal" :disabled="([0].indexOf(state) > -1)" v-model="currentMaster.rp003"></select>
              </div>
              <div class="form-group d-flex align-items-center col-12 col-sm-6 col-lg-12 col-xl-6 col-xxl-4 col-xxxxl-3">
                <label class="col-form-label col-auto">{{$t("ADMRP_rp050")}}</label><!--功能性需求 ADMRP_rp050-->
                <select
                  class="form-control col"
                  v-model="currentMaster.rp050"
                  :disabled="([0].indexOf(state) > -1)"
                >
                  <option value="Y">是</option>
                  <option value="N">否</option>
                </select>
              </div>
              <div class="form-group d-flex align-items-center col-12 col-sm-6 col-lg-12 col-xl-6 col-xxl-4 col-xxxxl-3">
                <label class="col-form-label col-auto">{{$t("ADMRP_rp051")}}</label><!--後台處理 ADMRP_rp051-->
                <select
                  class="form-control col"
                  v-model="currentMaster.rp051"
                  :disabled="([0].indexOf(state) > -1)"
                >
                  <option value="Y">是</option>
                  <option value="N">否</option>
                </select>
              </div>
              <div class="form-group d-flex align-items-center col-12 col-sm-6 col-lg-12 col-xl-6 col-xxl-4 col-xxxxl-3">
                <label class="col-form-label col-auto">{{$t("ADMRP_rp052")}}</label><!--需求優先級 ADMRP_rp052-->
                <select
                  class="form-control col"
                  v-model="currentMaster.rp052"
                  :disabled="([0].indexOf(state) > -1)"
                >
                  <option value="1">緊急,影響到系統正常運作</option>
                  <option value="2">重要需求</option>
                  <option value="3">現有系統某一個優化</option>
                  <option value="4">想優化功能(需新增功能優化現有功能)</option>
                </select>
              </div>
              <div class="form-group d-flex align-items-center col-12 col-sm-6 col-lg-12 col-xl-6 col-xxl-4 col-xxxxl-3">
                <label class="col-form-label col-auto">{{$t("ADMRP_rp041")}}</label><!--固定資產編號 ADMRP_rp041-->
                <input
                  type="text"
                  v-model="currentMaster.rp041"
                  :disabled="([0].indexOf(state) > -1)"
                  class="form-control col"
                />
              </div>
              <div class="form-group col-12">
                <label class="col-form-label col-auto">{{$t("ADMRP_rp053")}}</label><!--需求描述及邏輯 ADMRP_rp053-->
                <textarea
                  type="text"
                  class="form-control col"
                  v-model="currentMaster.rp053"
                  :disabled="([0].indexOf(state) > -1)"
                  rows="7"
                ></textarea>
              </div>



          </div>
          <!--用戶界面/應用流程圖-->
            <!-- .nav-tabs -->
            <ul class="nav nav-tabs">
              <li class="nav-item">
                <a class="nav-link active show" data-toggle="tab" href="#userPage">{{$t('UserPage')}}</a> <!--用戶界面 UserPage-->
              </li>
              <li class="nav-item">
                <a class="nav-link" data-toggle="tab" href="#flowChartPage">{{$t('FlowChartPage')}}</a><!--應用流程圖 FlowChartPage-->
              </li>         
            </ul>
            <!-- /.nav-tabs -->
          <div class="tab-content pt-2">
            <div
              class="tab-pane fade active show"
              id="userPage"
              role="tabpanel"
            >
              <UploadImage ref="userPageImg_ref" :multiple="true" :enabled="([2].indexOf(masterState) > -1)" @on_files_change="userPageImgChange"/><!--用戶界面-->
            </div>
            <div
              class="tab-pane fade"
              id="flowChartPage"
              role="tabpanel"
            >
              <UploadImage ref="appFlowChart_ref" :multiple="true" :enabled="([2].indexOf(masterState) > -1)" @on_files_change="appFlowChartChange"/><!--應用流程圖-->
            </div>
          </div>
          <!--用戶界面/應用流程圖-->



          </div>
          <!--處理結果 TheResults-->
          <div class="col-12 col-lg-6 rightPane">
            <h5 style="color:red">{{$t('TheResults')}}</h5>
            <div :class="['form-group row search_list mb-0', lang_code_en ? 'lang_en' : '']" name="search_list">
              <div class="form-group d-flex align-items-center col-12 col-sm-4 col-lg-6 col-xl-4 col-xxxl-3">
                <label class="col-form-label col-auto">{{$t("ADMRP_rp010")}}</label><!--跟進人 ADMRP_rp010-->
                <input
                  type="text"
                  v-model="currentMaster.rp010"
                  class="form-control col"
                  :disabled="([0].indexOf(state) > -1)"
                />
              </div>
              <div class="form-group d-flex align-items-center col-12 col-sm-4 col-lg-12 order-lg-1 order-xl-0 col-xl-4">
                <label class="col-form-label col-auto">{{$t("ADMRP_rp009")}}</label><!--跟進部門 ADMRP_rp009-->
                <select class="select2-genjin2 noFirstVal" :disabled="([0].indexOf(state) > -1)" v-model="currentMaster.rp009"></select>
              </div>
              <div class="form-group d-flex align-items-center col-12 col-sm-4 col-lg-6 col-xl-4">
                <label class="col-form-label col-auto">{{$t("ADMRP_rp024")}}</label><!--關聯任務 ADMRP_rp024-->
                <input
                  type="text"
                  v-model="currentMaster.rp024"
                  class="form-control col"
                  :disabled="([0].indexOf(state) > -1)"
                />
              </div>
            </div>
            <!--添加流程圖/快速設計用戶界面-->
              <!-- .nav-tabs -->
              <ul class="nav nav-tabs">
                <li class="nav-item">
                  <a class="nav-link active show" data-toggle="tab" href="#addFlowChart">{{$t('Add Flowchart')}}</a> <!--添加流程圖 Add Flowchart-->
                </li>
                <li class="nav-item">
                  <a class="nav-link" data-toggle="tab" href="#designPage">{{$t('Design User Page')}}</a><!--快速設計用戶界面 Design User Page-->
                </li>         
              </ul>
              <!-- /.nav-tabs -->
            <div class="tab-content pt-2 mb-3">
              <div
                class="tab-pane fade active show"
                id="addFlowChart"
                role="tabpanel"
              >
                <UploadImage ref="flowChart_ref" :multiple="true" :enabled="([2].indexOf(masterState) > -1)" @on_files_change="flowChartChange"/><!--添加流程圖-->
              </div>
              <div
                class="tab-pane fade"
                id="designPage"
                role="tabpanel"
              >
              <UploadImage ref="designPage_ref" :multiple="true" :enabled="([2].indexOf(masterState) > -1)" @on_files_change="designPageChange"/><!--快速設計用戶界面-->
              </div>
            </div>
            <!--功能列表整理-->
            <p class="mx_5">{{$t('Function list organizing')}}</p> <!--功能列表整理 Function list organizing-->
            <div class="card mb-3 mx_5">
              <div class="card-body p-0">
                <div
                  class="detail-operate align-items-center pt-2 px-2"
                  v-show="masterState == 2"
                >
                  <button
                    type="button"
                    class="btn btn-sm btn-primary mr-1"
                    @click="addAdmrf"
                  >
                    <i class="fa fa-plus m-0"></i>
                  </button>
                  <button
                    type="button"
                    class="btn btn-sm btn-warning mr-1"
                    @click="updateAdmrf"
                  >
                    <i class="fa fa-edit m-0"></i>
                  </button>
                  <button
                    type="button"
                    class="btn btn-sm btn-danger"
                    @click="deleteAdmrf"
                  >
                    <i class="fa fa-trash-alt m-0"></i>
                  </button>
                </div>
                <LPDataTable
                  ref="AdmrfTable"
                  :paging_inline="true"
                  :searching="false"
                  :pageLength="25"
                  :columns="admrfColumns"
                  datasource="/systembugrpt/admrf_table?format=datatables"
                  :custom_params_fun="admrfParamsFun"
                  :custom_options="admrfOptions"
                  @on_row_click="admrf_row_click"
                />
              </div>
            </div>
            <!--功能列表整理-->
            <!--非典型功能-->
            <div class="mb-3 mx_5">
              <p>{{$t('Atypical function')}}</p> <!--非典型功能 Atypical function-->
              <textarea
                type="text"
                class="form-control col"
                v-model="currentMaster.rp058"
                :disabled="([0].indexOf(state) > -1)"
              ></textarea>
            </div>
            <!--非典型功能 ADMRP_rp058-->
            <!--進度-->
            <p class="mx_5">{{$t('Progress')}}:</p> <!--進度 Progress-->
            <div class="card mb-3 mx_5">
              <div class="card-body p-0">
                <LPDataTable
                  ref="TaskProgressTable"
                  :paging_inline="true"
                  :searching="false"
                  :pageLength="25"
                  :columns="taskProgressColumns"
                  datasource="/systembugrpt/vtask_table?format=datatables"
                  :custom_params_fun="taskProgressParamsFun"
                  :custom_options="taskProgressOptions"
                />
              </div>
            </div>
            <!--進度-->
            <!--反饋意見-->
            <div class="mb-2 mx_5">
              <p>{{$t('Feedback')}}</p> <!--反饋意見 Feedback-->
              <textarea
                type="text"
                class="form-control col"
                v-model="currentMaster.rp056"
                :disabled="([0].indexOf(state) > -1)"
              ></textarea>
            </div>
            <!--反饋意見 ADMRP_rp056-->


          </div>
        </div>


      </div>
      <!-- end -->

      <!--AI查詢-->
      <div
        class="tab-pane fade"
        id="Admrp_ai"
        role="tabpanel"                
      >
      <div :class="['card cardShadow detailInfo', lang_code_en ? 'lang_en' : '']">
        <!--菜單欄-->
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
        <div :class="{
            'card-body tab-content scrollbar': true,
            isSpecialTabCard: isTaskTabActive,
          }">
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
                <label class="prompt_sql_tab_show col-form-label caption col-auto pl-0">{{
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
                <button class="btn btn-primary mr-2" @click="fetchSysBugTable">
                  {{ $t("Search") }}
                </button>
                <button class="btn btn-primary mr-2" @click="aiAnalysis">
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
          <!--任務列表-->
          <div
            class="tab-pane fade active show"
            id="task-list"
            role="tabpanel"                
          >
            <!-- <LPDataTable
              ref="bugTable"
              :datasource="[]"
              :columns="dataColumns"
              :row_nowrap="true"
              :custom_options="bugAiOptions"
              :searching="false"
              :paging_inline="true"
              :paging="false"
            /> -->
          </div>
          <!--任務列表(所有)-->
          <div
            class="tab-pane fade"
            id="task-list-all"
            role="tabpanel"                
          >
            <!-- <LPDataTable
              ref="bugTable"
              :datasource="[]"
              :columns="dataColumns"
              :row_nowrap="true"
              :custom_options="bugAiOptions"
              :searching="false"
              :paging_inline="true"
              :paging="false"
            /> -->
          </div>
          <!--提示任務-->
          <div
            class="tab-pane fade"
            id="top-task"
            role="tabpanel"                
          >
            <div v-if="showTaskData">
              <LPDataTable
                ref="bugTable"
                :datasource="[]"
                :columns="dataColumns"
                :row_nowrap="true"
                :custom_options="bugAiOptions"
                :searching="false"
                :paging_inline="true"
                :paging="false"
              />
              </div>
          </div>
          <!--SQL腳本-->
          <div
            class="tab-pane fade"
            id="sql-script"
            role="tabpanel"                
          >
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
      <!--AI查詢-->

    </div>
  </div>
</div>

<!--選擇系統編號-->
<LPModal ref="systemModal_ref" class="customModal">
  <template v-slot:body>
    <LPDataTable
      :paging="true"
      :pageLength="25"
      :paging_inline="true"
      :searching="true"
      :columns="systemColumns"
      :custom_options="systemOptions"
      @on_row_click="system_row_click"
      datasource="/systembugrpt/system_table?format=datatables"
      ref="SystemTable"
    />
  </template>
  <template v-slot:footer>
      <button type="button" class="btn btn-primary"  @click="systemClick">{{$t('Confirm')}}</button>
      <button type="button" class="btn btn-light" data-dismiss="modal">{{$t('Cancel')}}</button>
  </template>
</LPModal>
<!--選擇系統編號-->
<!--選擇窗體名稱-->
<LPModal ref="moduleModal_ref" class="customModal">
  <template v-slot:body>
    <LPDataTable
      :paging="true"
      :pageLength="25"
      :paging_inline="true"
      :searching="true"
      :columns="moduleColumns"
      :custom_options="moduleOptions"
      @on_row_click="module_row_click"
      :datasource="[]"
      ref="ModuleTable"
    />
  </template>
  <template v-slot:footer>
      <button type="button" class="btn btn-primary"  @click="moduleClick">{{$t('Confirm')}}</button>
      <button type="button" class="btn btn-light" data-dismiss="modal">{{$t('Cancel')}}</button>
  </template>
</LPModal>
<!--選擇窗體名稱-->
<!--選擇功能依賴對象-->
<LPModal ref="moduleObjectModal_ref" class="customModal">
  <template v-slot:body>
    <LPDataTable
      :paging="true"
      :pageLength="25"
      :paging_inline="true"
      :searching="true"
      :columns="moduleObjectColumns"
      :custom_options="moduleObjectOptions"
      @on_row_click="moduleObject_row_click"
      :datasource="[]"
      ref="ModuleObjectTable"
    />
  </template>
  <template v-slot:footer>
      <button type="button" class="btn btn-primary"  @click="moduleObjectClick">{{$t('Confirm')}}</button>
      <button type="button" class="btn btn-light" data-dismiss="modal">{{$t('Cancel')}}</button>
  </template>
</LPModal>
<!--選擇功能依賴對象-->
<!--新增和修改系統問題上報功能彈框-->
<LPModalForm
  ref="admrf_modalForm"
  :title="Modal_title"
  @on_submit="admrfSave"
>
  <div class="form-row">
    <div class="col-12">
      <LPLabelInput :label="$t('ADMRF_rf002')"><!--單號 ADMRF_rf002-->
        <em style="color: red">*</em>
        <input type="text" class="form-control" v-model="currentAdmrf.rf002" disabled />
      </LPLabelInput>
    </div>
    <div class="col-12">
      <LPLabelInput :label="$t('ADMRF_rf003')"><!--序號 ADMRF_rf003-->
        <em style="color: red">*</em>
        <input type="text" class="form-control" v-model="currentAdmrf.rf003" disabled/>
      </LPLabelInput>
    </div>
    <div class="col-12">
      <LPLabelInput :label="$t('ADMRF_rf004')"><!--功能列表 ADMRF_rf004-->
        <em style="color: red">*</em>
        <textarea type="text" class="form-control" v-model="currentAdmrf.rf004"></textarea>
      </LPLabelInput>
    </div>
    <div class="col-12">
      <LPLabelInput :label="$t('ADMRF_rf005')"><!--功能重要性 ADMRF_rf005-->
        <select
          class="form-control"
          v-model="currentAdmrf.rf005"
        >
          <option value="A">需要的,對系統至關重要</option>
          <option value="B">應該有可以省略</option>
          <option value="C">可以有,可選的功能</option>
          <option value="D">想有,可以繼續添加</option>
        </select>
      </LPLabelInput>
    </div>
  </div>
</LPModalForm>
<!--新增和修改系統問題上報功能彈框-->
<!--新增和修改系統問題上報功能彈框-->
<LPModalForm
  ref="deliverDept_modalForm"
  :title="Modal_title"
  @on_submit="deliverDeptSave"
>
  <div class="form-row">
    <div class="col-12">
      <LPLabelInput :label="$t('ADMRF_rf009')"><!--部門 ADMRF_rf009-->
      <select
        class="form-control"
        v-model="deptNo"
        required
      >
        <option
          v-for="(item,index) in cmsmeArray"
          :key="index"
          :value="item.me001"
        >{{ item.me002 }}</option>
      </select>
      </LPLabelInput>
    </div>
  </div>
</LPModalForm>
<!--新增和修改系統問題上報功能彈框-->

<!--安排Task功能彈框-->
<LPModalForm
  ref="arrangeTask_modalForm"
  :title="Modal_title"
  @on_submit="arrangeTaskSave"
>
  <!-- .nav-scroller -->
  <div class="nav-scroller border-bottom">
    <!-- .nav-tabs -->
    <ul class="nav nav-tabs">
      <li class="nav-item">
        <a class="nav-link"  data-toggle="tab" @click="userDefaultProjectClick" href="#userDefaultProject">{{$t('userDefaultProject')}}</a><!--用戶默認工程 userDefaultProject-->
      </li> 
      <li class="nav-item">
        <a class="nav-link"  data-toggle="tab" @click="getDefaultProClick" href="#formOwnershipProject">{{$t('formOwnershipProject')}}</a><!--窗體所屬工程 formOwnershipProject-->
      </li> 
      <li class="nav-item">
        <a class="nav-link active show" data-toggle="tab" ref="taskSimpleSetup_ref" @click="this.taskState=false" v-show="taskState" href="#taskSimpleSetup">{{$t('taskDetailSetting')}}</a> <!--任務詳細設置 taskDetailSetting-->
      </li>
      <li class="nav-item">
        <a class="nav-link" data-toggle="tab" @click="this.taskState=true" v-show="!taskState" href="#taskDetailSetting">{{$t('taskSimpleSetup')}}</a><!--任務簡單設置 taskSimpleSetup-->
      </li>
      <li class="nav-item">
        <a class="nav-link" data-toggle="tab" @click="setDefaultProjectClick" href="#setDefaultProject">{{$t('setDefaultProject')}}</a><!-- 設置默認工程 setDefaultProject-->
      </li>         
      <li class="nav-item">
        <a class="nav-link" data-toggle="tab" @click="showTaskTableClick" href="#viewProblemLog">{{$t('viewProblemLog')}}</a><!--查看問題記錄 viewProblemLog-->
      </li>         
    </ul>
    <!-- /.nav-tabs -->
  </div>
  <!-- .nav-scroller -->    
  <div class="tab-content pt-1" style="height:600px">
    <!--查看問題記錄-->
    <div
      class="tab-pane fade"
      id="viewProblemLog"
      role="tabpanel"
    >
      <LPDataTable
        :paging="true"
        :pageLength="25"
        :paging_inline="true"
        :searching="false"
        :columns="taskColumns"
        :custom_options="taskOptions"
        :custom_params_fun="task_params_fun"
        datasource="/systembugrpt/task_table?format=datatables"
        ref="systemBugRpt_taskTable_ref"
      />
    </div>
    <!--查看問題記錄-->
    <!--設置默認工程-->
    <div
      class="tab-pane fade"
      id="setDefaultProject"
      role="tabpanel"
    >
      <div style="height:15px"></div>
      <div :class="['form-group row search_list', lang_code_en ? 'lang_en' : '']" name="search_list">
      <div class="form-group d-flex align-items-center col-4">
        <label class="col-form-label text-lg-right col-auto">{{$t("V_Task_pid")}}</label><!--工程編號 V_Task_pid-->
        <input type="text" class="form-control" v-model="ut002"/>
        <div class="tile bg-success" style="cursor: pointer;" @click="showPidModel('1')">
          <span class="oi oi-chat"></span>
        </div>
      </div>
      <div class="form-group d-flex align-items-center col-4">
        <label class="col-form-label text-lg-right col-auto">{{$t("V_Task_tid")}}</label><!--工作類別 V_Task_tid-->
        <input type="text" class="form-control" v-model="ut003" />
        <div class="tile bg-success" style="cursor: pointer;" @click="showTidModel('1')">
          <span class="oi oi-chat"></span>
        </div>
      </div>
      <button type="button" class="btn btn-light"  style="background-color: #0066FF;" @click="setDefaultProjectSave">{{$t('Confirm')}}</button>
      </div>
    </div>
    <!--設置默認工程-->
    <!--任務簡單設置-->
    <div
      class="tab-pane fade active show"
      id="taskSimpleSetup"
      role="tabpanel"
    >
      <div style="height:15px"></div>
      <div :class="['form-group row search_list', lang_code_en ? 'lang_en' : '']" name="search_list">

        <div class="form-group d-flex align-items-center col-12">
          <label class="col-form-label text-lg-right col-auto" v-html="currentTask.taskno"></label>
        </div>
        <div class="form-group d-flex align-items-center col-6">
          <label class="col-form-label text-lg-right col-auto">{{$t("V_Task_task")}}</label><!--任務描述 V_Task_task-->
          <textarea type="text" class="form-control" v-model="currentTask.task"></textarea>
        </div>
        <div class="form-group d-flex align-items-center col-6"></div>
        <div class="form-group d-flex align-items-center col-3">
          <label class="col-form-label text-lg-right col-auto">{{$t("V_Task_contact")}}</label><!--聯繫人 V_Task_contact-->
            <input type="text" class="form-control" v-model="currentTask.contact" />
            <div class="tile bg-success" style="cursor: pointer;" @click="showUsersModel">
              <span class="oi oi-chat"></span>
            </div>
        </div>
        <div class="form-group d-flex align-items-center col-3" >
          <label class="col-form-label text-lg-right col-auto">{{$t("V_Task_priority")}}</label><!--優先級 V_Task_priority-->
            <input type="number" class="form-control" v-model="currentTask.priority"/>
        </div>
        <div class="form-group d-flex align-items-center col-6"></div>
        <div class="form-group d-flex align-items-center col-3" >
          <label class="col-form-label text-lg-right col-auto">{{$t("Send text message")}}</label><!--發送短信(暫不設置) Send text message-->
          <select
            class="form-control col"
          >
            <option value="N">No</option>
            <option value="Y">Yes</option>
          </select>
        </div>
        <div class="form-group d-flex align-items-center col-3" >
          <label class="col-form-label text-lg-right col-auto">{{$t("Delay delivery")}}</label><!--推遲發送(暫不設置) Delay delivery-->
          <select
            class="form-control col"
          >
            <option value="N">No</option>
            <option value="Y">Yes</option>
          </select>
        </div>
        <div class="form-group d-flex align-items-center col-6"></div>
      </div>

    </div>
    <!--任務簡單設置-->
    <!--任務詳細設置-->
    <div
      class="tab-pane fade"
      id="taskDetailSetting"
      role="tabpanel"
    >
      <div style="height:15px"></div>
      <div :class="['form-group row search_list', lang_code_en ? 'lang_en' : '']" name="search_list">
        <div class="form-group d-flex align-items-center col-3">
          <label class="col-form-label text-lg-right col-auto">{{$t("V_Task_pid")}}</label><!--項目編號 V_Task_pid-->
            <input type="text" class="form-control" v-model="currentTask.pid" @change="checkPidExist"/>
            <div class="tile bg-success" style="cursor: pointer;" @click="showPidModel('2')" >
              <span class="oi oi-chat"></span>
            </div>
        </div>
        <div class="form-group d-flex align-items-center col-3" >
          <label class="col-form-label text-lg-right col-auto">{{$t("V_Task_pname")}}</label><!--項目名稱 V_Task_pname-->
            <input type="text" class="form-control" v-model="currentTask.projectname"/>
        </div>
        <div class="form-group d-flex align-items-center col-3">
          <label class="col-form-label text-lg-right col-auto">{{$t("V_Task_tid")}}</label><!--工作編號 V_Task_tid-->
            <input type="text" class="form-control" v-model="currentTask.tid" @change="checkTidExist"/>
            <div class="tile bg-success" style="cursor: pointer;" @click="showTidModel('2')">
              <span class="oi oi-chat"></span>
            </div>
        </div>
        <div class="form-group d-flex align-items-center col-3" >
          <label class="col-form-label text-lg-right col-auto">{{$t("V_Task_taskid")}}</label><!--任務編號 V_Task_taskid-->
            <input type="text" class="form-control" v-model="currentTask.taskid"/>
        </div>
        <div class="form-group d-flex align-items-center col-6">
          <label class="col-form-label text-lg-right col-auto">{{$t("V_Task_tasklistdesp")}}</label><!--工作描述 V_Task_tasklistdesp-->
          <textarea type="text" class="form-control" v-model="currentTask.tasklistdesp"></textarea>
        </div>
        <div class="form-group d-flex align-items-center col-3" >
          <label class="col-form-label text-lg-right col-auto">{{$t("V_Task_priority")}}</label><!--優先級 V_Task_priority-->
            <input type="number" class="form-control" v-model="currentTask.priority"/>
        </div>
        <div class="form-group d-flex align-items-center col-3" >
          <label class="col-form-label text-lg-right col-auto">{{$t("V_Task_progress")}}</label><!--任務進度 V_Task_progress-->
          <select
            class="form-control col"
            v-model="currentTask.progress"
          >
            <option value="I">I</option>
            <option value="N">N</option>
            <option value="S">S</option>
            <option value="H">H</option>
          </select>
        </div>
        <div class="form-group d-flex align-items-center col-3">
          <label class="col-form-label text-lg-right col-auto">{{$t("V_Task_contact")}}</label><!--聯繫人 V_Task_contact-->
            <input type="text" class="form-control" v-model="currentTask.contact" />
            <div class="tile bg-success" style="cursor: pointer;" @click="showUsersModel">
              <span class="oi oi-chat"></span>
            </div>
        </div>
        <div class="form-group d-flex align-items-center col-3">
          <label class="col-form-label text-lg-right col-auto">{{$t("V_Task_udf04")}}</label><!--窗口名稱 V_Task_udf04-->
            <input type="text" class="form-control" v-model="currentTask.udf04" />
            <div class="tile bg-success" style="cursor: pointer;" @click="showModuleModals">
              <span class="oi oi-chat"></span>
            </div>
        </div>
        <div class="form-group d-flex align-items-center col-3" >
          <label class="col-form-label text-lg-right col-auto">{{$t("V_Task_planbdate")}}</label><!--計劃開始 V_Task_planbdate-->
            <input type="date" class="form-control" v-model="currentTask.planbdate" @change="taskDateChange"/>
        </div>
        <div class="form-group d-flex align-items-center col-3" >
          <label class="col-form-label text-lg-right col-auto">{{$t("All day long")}}</label><!--全天(未綁定值) All day long-->
          <select
            class="form-control col"
          >
            <option value="N">No</option>
            <option value="Y">Yes</option>
          </select>
        </div>
        <div class="form-group d-flex align-items-center col-6">
          <label class="col-form-label text-lg-right col-auto">{{$t("V_Task_task")}}</label><!--任務描述 V_Task_task-->
          <textarea type="text" class="form-control" v-model="currentTask.task"></textarea>
        </div>
        <div class="form-group d-flex align-items-center col-3" >
          <label class="col-form-label text-lg-right col-auto">{{$t("V_Task_planedate")}}</label><!--計劃結束 V_Task_planedate-->
            <input type="date" class="form-control" v-model="currentTask.planedate" @change="taskDateChange"/>
        </div>
        <div class="form-group d-flex align-items-center col-3" >
          <label class="col-form-label text-lg-right col-auto">{{$t("V_Task_etime")}}</label><!--計劃天數 V_Task_etime-->
            <input type="number" class="form-control" v-model="currentTask.etime"/>
        </div>
        <div class="form-group d-flex align-items-center col-6">
          <label class="col-form-label text-lg-right col-auto">{{$t("V_Task_remark")}}</label><!--備註 V_Task_remark-->
          <textarea type="text" class="form-control" v-model="currentTask.remark"></textarea>
        </div>

        <div class="form-group d-flex align-items-center col-3" >
          <label class="col-form-label text-lg-right col-auto">{{$t("Send text message")}}</label><!--發送短信(暫不設置)  Send text message-->
          <select
            class="form-control col"
          >
            <option value="N">No</option>
            <option value="Y">Yes</option>
          </select>
        </div>
        <div class="form-group d-flex align-items-center col-3" >
          <label class="col-form-label text-lg-right col-auto">{{$t("Delay delivery")}}</label><!--推遲發送(暫不設置) Delay delivery-->
          <select
            class="form-control col"
          >
            <option value="N">No</option>
            <option value="Y">Yes</option>
          </select>
        </div>
      </div>

    </div>
    <!--任務詳細設置-->
  </div>

</LPModalForm>
<!--安排Task功能彈框-->
<!--選擇工程編號-->
<LPModal ref="pidModal_ref" class="customModal">
  <template v-slot:body>
    <LPDataTable
      :paging="true"
      :pageLength="25"
      :paging_inline="true"
      :searching="true"
      :columns="pidColumns"
      :custom_options="pidOptions"
      @on_row_click="pid_row_click"
      :custom_params_fun="pid_params_fun"
      datasource="/systembugrpt/project_table?format=datatables"
      ref="projectPidTable_ref"
    />
  </template>
  <template v-slot:footer>
      <button type="button" class="btn btn-primary"  @click="setPidClick">{{$t('Confirm')}}</button>
      <button type="button" class="btn btn-light" data-dismiss="modal">{{$t('Cancel')}}</button>
  </template>
</LPModal>
<!--選擇工程編號-->
<!--選擇工作類別-->
<LPModal ref="tidModal_ref" class="customModal">
  <template v-slot:body>
    <LPDataTable
      :paging="true"
      :pageLength="25"
      :paging_inline="true"
      :searching="true"
      :columns="tidColumns"
      :custom_options="tidOptions"
      @on_row_click="tid_row_click"
      :custom_params_fun="tid_params_fun"
      datasource="/systembugrpt/tasklist_table?format=datatables"
      ref="projectTidTable_ref"
    />
  </template>
  <template v-slot:footer>
      <button type="button" class="btn btn-primary"  @click="setTidClick">{{$t('Confirm')}}</button>
      <button type="button" class="btn btn-light" data-dismiss="modal">{{$t('Cancel')}}</button>
  </template>
</LPModal>
<!--選擇工作類別-->
<!--選擇联系人-->
<LPModal ref="userModal_ref" class="customModal">
  <template v-slot:body>
    <LPDataTable
      :paging="true"
      :pageLength="25"
      :paging_inline="true"
      :searching="true"
      :columns="userColumns"
      @on_row_click="user_row_click"
      datasource="/systembugrpt/user_table?format=datatables"
      ref="userModalTable_ref"
    />
  </template>
  <template v-slot:footer>
      <button type="button" class="btn btn-primary"  @click="setUserClick">{{$t('Confirm')}}</button>
      <button type="button" class="btn btn-light" data-dismiss="modal">{{$t('Cancel')}}</button>
  </template>
</LPModal>
<!--選擇工作類別-->
<!--選擇窗體名稱-->
<LPModal ref="moduleModals_ref" class="customModal">
  <template v-slot:body>
    <LPDataTable
      :paging="true"
      :pageLength="25"
      :paging_inline="true"
      :searching="true"
      :columns="moduleColumns"
      :custom_options="moduleOptions"
      @on_row_click="module_row_click"
      :datasource="[]"
      ref="ModuleTable"
    />
  </template>
  <template v-slot:footer>
      <button type="button" class="btn btn-primary"  @click="modulesClick">{{$t('Confirm')}}</button>
      <button type="button" class="btn btn-light" data-dismiss="modal">{{$t('Cancel')}}</button>
  </template>
</LPModal>
<!--選擇窗體名稱-->
<!--查看關聯任務明細信息 關聯任務-->
<LPModal ref="associatedTaskModals_ref" class="associatedTaskModals" show_part="hb" :title="$t('ADMRP_rp024')">
  <template v-slot:body>
    <LPDataTable
      :paging="true"
      :pageLength="25"
      :paging_inline="true"
      :searching="false"
      :columns="associatedTaskColumns"
      :custom_options="associatedTaskOptions"
      :custom_params_fun="associatedTask_params_fun"
      @on_dbclick="associatedTaskDbClick"
      :datasource="[]"
      ref="AssociatedTaskTable"
    />
  </template>
</LPModal>
<!--查看關聯任務明細信息 datasource="/systembugrpt/vtask_table?format=datatables"-->

<!--打開彈窗選擇SolutionType-->
<LPModal ref="solutiontypeModals_ref" class="solutiontypeModal" :title="$t('Solution Type List')">
  <template v-slot:body>
    <LPDataTable
      :paging="false"
      :pageLength="50"
      :firstColSelected="true"
      :paging_inline="true"
      :searching="true"
      :columns="solutionTypeColumns"
      :custom_options="solutionTypeOptions"
      datasource="/systembugrpt/get_solutiontype_table?format=datatables"
      ref="solutionTypeTable"
    />
  </template>
  <template v-slot:footer>
      <button type="button" class="btn btn-primary"  @click="solutionTypeClick">{{$t('Confirm')}}</button>
      <button type="button" class="btn btn-light" data-dismiss="modal">{{$t('Cancel')}}</button>
  </template>
</LPModal>

<LPModalForm
  ref="flowChart_modalForm"
  :title="flowChartModal_title"
  @on_submit="flowChartSave"
>
  <div class="form-row">
    <div class="col-12">
      <LPLabelInput label="">
        <label>
          {{ $t('Flowchart ID/URL') }} <span class="required" style="color: red;">*</span><!--流程圖編號/URL-->
        </label>
        <input type="text" class="form-control" v-model="flowChart.flowchartno" @change="flowchartnoChange(flowChart.flowchartno)">
      </LPLabelInput>
      <LPLabelInput label="">
        <label>
          {{ $t('Type') }} <span class="required" style="color: red;">*</span><!--類型-->
        </label>
        <select
          class="form-control"
          v-model="flowChart.charttype"
        >
          <option value="url">url</option>
          <option value="flowchart">flowchart</option>
        </select>
      </LPLabelInput>
      <LPLabelInput :label="$t('Description')"><!--描述-->
        <input type="text" class="form-control" v-model="flowChart.description">
      </LPLabelInput>
    </div>
  </div>
</LPModalForm>

<!--打開彈窗選擇上報單號信息-->
<LPModal ref="sysBugModals_ref" class="sysBugModal" :title="$t('Report Information List')"> <!--上報信息列表-->
  <template v-slot:body>
    <br/>
    <button type="button" class="btn btn-secondary order-button" data-v-8ec5118a="" @click="searchSysBugNoClick">
      <i class="fas fa-search m-0 mr-xl-1" data-v-8ec5118a=""></i><span class="d-none d-xl-inline" data-v-8ec5118a="">{{$t('query')}}</span>
    </button>
    <LPDataTable
      ref="admrp_table"
      :columns="masterColumns"
      datasource="/systembugrpt/admrp_table?format=datatables"
      :firstColSelected="true"
      :custom_params_fun="admrpParamsFun"
      :custom_options="admrpOptions"
      :paging_inline="true"
      :searching="false"
      :pageLength="100"
    />
  </template>
  <template v-slot:footer>
      <button type="button" class="btn btn-primary"  @click="searchSysBugClick">{{$t('Confirm')}}</button>
      <button type="button" class="btn btn-light" data-dismiss="modal">{{$t('Cancel')}}</button>
  </template>
</LPModal>

<!--選擇功能描述-->
<LPModal ref="docmhModal_ref" class="docmhModal" :title="$t('Window Function Information List')"><!--窗口功能信息列表-->
  <template v-slot:body>
    <br/>
    <button type="button" class="btn btn-secondary order-button" data-v-8ec5118a="" @click="searchDocmhClick">
      <i class="fas fa-search m-0 mr-xl-1" data-v-8ec5118a=""></i>
      <span class="d-none d-xl-inline" data-v-8ec5118a="">{{$t('query')}}</span>
    </button>
    <LPDataTable
      :paging="true"
      :pageLength="100"
      :paging_inline="true"
      :firstColSelected="true"
      :searching="false"
      :columns="docmhColumns"
      :custom_options="docmhOptions"
      :custom_params_fun="docmhParamsFun"
      datasource="/systembugrpt/get_docmhTable?format=datatables"
      ref="docmhTable"
    />
  </template>
  <template v-slot:footer>
      <button type="button" class="btn btn-primary"  @click="docmhClick">{{$t('Confirm')}}</button>
      <button type="button" class="btn btn-light" data-dismiss="modal">{{$t('Cancel')}}</button>
  </template>
</LPModal>
<!--選擇系統編號-->

<!--用戶反饋-->
<LPModal ref="feedbackModal_ref" class="feedbackModal" title="用戶反饋"><!--用戶反饋-->
  <template v-slot:body>
    <div class="form-row">
      <div class="col-12">
        <LPLabelInput :label="$t('ADMRP_rp017')"><!--上報號-->
          <input type="text" class="form-control" v-model="currentMaster.rp017" disabled>
        </LPLabelInput>
        <LPLabelInput :label="$t('ADMRP_rp005')"><!--描述-->
          <textarea type="text" class="form-control" v-model="currentMaster.rp005" disabled></textarea>
        </LPLabelInput>
        <LPLabelInput :label="$t('ADMRP_rp002')"><!--提出日期-->
          <input
            type="date"
            v-model="currentMaster.rp002"
            disabled
            :class="{'form-control col': true, 'date-hidden': !currentMaster.rp002}"
          />
        </LPLabelInput>
        <LPLabelInput :label="$t('ADMRP_rp013')"><!--處理結束日期-->
          <input
            type="date"
            v-model="currentMaster.rp013"
            disabled
            :class="{'form-control col': true, 'date-hidden': !currentMaster.rp013}"
          />
        </LPLabelInput>
        <LPLabelInput label="">
          <label> 反饋用戶 <span class="required" style="color: red;">*</span></label><!--反饋用戶-->
          <input type="text" class="form-control" v-model="username" disabled>
        </LPLabelInput>
        <LPLabelInput label="">
          <label> 所屬部門 <span class="required" style="color: red;">*</span></label><!--所屬部門-->
          <select class="select2-type noFirstVal"></select>
        </LPLabelInput>
        <LPLabelInput label="">
          <label> 您的問題解決了嗎? <span class="required" style="color: red;">*</span></label><!--您的問題解決了嗎?-->
          <select
            class="form-control"
          >
            <option value="1">永久解決</option>
            <option value="2">臨時解決</option>
            <option value="3">尚未解決</option>
          </select>
        </LPLabelInput>
        <LPLabelInput label="">
          <label> 您對解決速度與結果的評價：<span class="required" style="color: red;">*</span></label><!--您對解決速度與結果的評價：-->
          <select
            class="form-control"
          >
            <option value="1">解決速度非常快</option>
            <option value="2">解決速度一般，但結果滿意</option>
            <option value="3">解決速度慢，結果不滿意</option>
            <option value="4">沒有解決問題</option>
          </select>
        </LPLabelInput>
        <LPLabelInput label="">
          <label> 請對處理過程的整體滿意度進行評分(1-5分): <span class="required" style="color: red;">*</span></label><!--請對處理過程的整體滿意度進行評分(1-5分):-->
          <select
            class="form-control"
          >
            <option value="1">1分:非常不滿意</option>
            <option value="2">2分:不滿意</option>
            <option value="3">3分:一般</option>
            <option value="4">4分:滿意</option>
            <option value="5">5分:非常滿意</option>
          </select>
        </LPLabelInput>
        <LPLabelInput label="不滿意原因"><!--不滿意原因-->
          <textarea type="text" class="form-control" ></textarea>
        </LPLabelInput>
        <LPLabelInput label="改進建議"><!--改進建議-->
          <textarea type="text" class="form-control" ></textarea>
        </LPLabelInput>
        <LPLabelInput label="備註"><!--備註-->
          <textarea type="text" class="form-control" ></textarea>
        </LPLabelInput>
      </div>
    </div>
  </template>
  <template v-slot:footer>
      <button type="button" class="btn btn-primary">提交反饋</button>
      <button type="button" class="btn btn-light" data-dismiss="modal">{{$t('Cancel')}}</button>
  </template>
</LPModal>
<!--用戶反饋-->

<LPAIComBox v-if="showLPAIComBox" ref="aicombox" :predefinedData="aiPredefinedData" />

<LPAIComBox
  v-if="showLPAIAnalysisComBox"
  ref="aicombox_to"
  :iframe_src="'http://183.63.205.83:3000/aiChat'"
  :predefinedData="aiProblemData"
/>

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

<div class="UploadImage">
    <!-- 加载指示器 -->
    <div v-if="isLoading" class="loading-overlay">
        <div class="loading-spinner">
            <i class="fas fa-spinner fa-spin"></i> {{$t('Saving')}}...
        </div><!--Saving 正在保存-->
    </div>
    <!-- 其他内容 -->
</div>
</template>
<script>
import axios from "axios";
import LPModal from "@components/looper/layout/LPModal.vue";
import LPDataTable,{DateRender} from "@components/looper/tables/LPDataTable.vue";
import LPModalForm from "@components/looper/layout/LPModalForm.vue";
import LPLabelInput from "@components/looper/forms/LPLabelInput.vue";
import OperationBar from "@components/looper/navigator/OperationBar.vue";
import UploadImage from "@components/looper/general/UploadImage.vue";
import LPCombobox from "@components/looper/forms/LPCombobox.vue";
import LPAIComBox from "@components/looper/general/LPAIComBox.vue";
export default {
name: "SystemBugRpt_vueFrm",
components: {
  LPAIComBox,
  LPModal,
  LPCombobox,
  UploadImage,
  LPDataTable,
  LPModalForm,
  LPLabelInput,
  OperationBar,
},
data() {
  var self = this
  return {
    docmhColumns:[ //窗口文檔功能描述列表
      { field: "mh001", label: this.$t('Program Number'), width: "120px"}, //程序編號
      { field: "mh002", label: this.$t('Version Number'), width: "120px"}, //版本號
      { field: "mh003", label: this.$t('Sequence Number'), width: "120px"}, //序號
      { field: "mh004", label: this.$t("ADMRP_rp027"), width: "30%"}, //功能描述
      { field: "mh005", label: this.$t('Category'), width: "120px"}, //類別
    ],
    docmhOptions:{
      deferLoading: 0,
      scrollY: 660,
      responsive: false,
      autoWidth: false,
      scrollX: true,
      columnDefs: [
        {
          targets: [3],
          render: function (data, type, full, meta) {
            if (data) {
              if (data.length > 15) {
                return (
                  "<label title='" +
                  data +
                  "' style='text-decoration: none;'>" +
                  data.trim().substr(0, 15) +
                  "..." +
                  "</label>"
                );
              } else {
                return data;
              }
            } else {
              return "";
            }
          },
        },
      ],
    },
    admrpOptions:{
      deferLoading: 0,
      scrollY: 660,
      responsive: false,
      autoWidth: false,
      scrollX: true,
      columnDefs: [
        {
          targets: [5,9,10,17],
          render: function (data, type, full, meta) {
            if (data) {
              if (data.length > 15) {
                return (
                  "<label title='" +
                  data +
                  "' style='text-decoration: none;'>" +
                  data.trim().substr(0, 15) +
                  "..." +
                  "</label>"
                );
              } else {
                return data;
              }
            } else {
              return "";
            }
          },
        },
      ],
    },
    flowChartColumns:[
      { field: "flowchartno", label: this.$t("Flowchart ID/URL"), width: "30%"}, //流程圖編號/URL
      { field: "charttype", label: this.$t("Type"), width: "10%"}, //類型
      { field: "description", label: this.$t("Description"), width: "40%"}, //描述
      {
        field: null,
        label: this.$t("Action"),
        render: function (data, type, row) {
          var id = row.DT_RowId;
          // return `
          //     <a class="btn view-diagram btn-sm btn-icon btn-secondary" href="#" id="${id}">
          //       <i class="fas fa-eye"></i>
          //     </a>
          //     <a class="btn btn-edit btn-sm btn-icon btn-secondary" href="#" id="${id}">
          //       <i class="fa fa-pencil-alt"></i>
          //     </a> 
          //     <a class="btn del-btn btn-sm btn-icon btn-secondary" href="#" id="${id}">
          //       <i class="far fa-trash-alt"></i>
          //     </a>
          // `
          return `
            <button 
              type="button"
              class="btn btn-sm btn-success mr-1"
            >
            <i class="fa fa-eye m-0"></i
            >
            </button>
            <button 
              type="button"
              class="btn btn-sm btn-warning mr-1"
            >
            <i class="fa fa-edit m-0"></i
            >
            </button>
            <button 
              type="button"
              class="btn btn-sm btn-danger"
            >
            <i class="fa fa-trash-alt m-0"></i
            >
            </button>
          `
        }, width: "20%"
      },
      { field: "inc_id", label: "inc_id", visible: false },
    ],
    solutionTypeColumns:[
      { field: "category", label: this.$t("Category"), width: "30%" }, //分類
      { field: "remark", label: this.$t("Remark"), width: "70%" }, // 描述
    ],
    solutionTypeOptions:{
      scrollY: 500,
      responsive: false,
      autoWidth: false,
      scrollX: true,
    },
    taskItemColumns:[ //問題跟進狀態列表信息 TaskItem -> V_Task
      { field: "taskno", label: this.$t("TaskNo"), width: "150px" }, //任務編號
      { field: "task", label: this.$t("V_Task_task"), width: "60%" }, //任務描述
      { field: "contact", label: this.$t("V_Task_contact"), width: "70px" }, //聯繫人
      { field: "planbdate", label: this.$t("V_Task_planbdate"), width: "150px",
        render: function (data, type, row) {
          if (typeof data == "string") {
            data = data.slice(0, 10);
          }
          return data;
        },
      }, //計劃開始日期
      { field: "planedate", label: this.$t("V_Task_planedate"), width: "150px",
        render: function (data, type, row) {
          if (typeof data == "string") {
            data = data.slice(0, 10);
          }
          return data;
        },
      }, //計劃結束日期
      { field: "progress", label: this.$t("V_Task_progress"), width: "70px" }, //任務進度
    ],
    associatedTaskColumns:[//關聯任務明細列表
      { field: "pid", label: this.$t("V_Task_pid"), className: "all",width: "70px" }, //工程編號
      { field: "tid", label: this.$t("V_Task_tid"), className: "all",width: "70px" }, //類別
      { field: "taskid", label: this.$t("V_Task_taskid"), className: "all",width: "70px" }, //任務編號
      { field: "task", label: this.$t("V_Task_task"), className: "all",width: "300px" }, //任務描述
      { field: "contact", label: this.$t("V_Task_contact"), className: "all",width: "70px" }, //聯繫人
      { field: "planbdate", label: this.$t("V_Task_planbdate"), className: "all",width: "150px",
        render: function (data, type, row) {
          if (typeof data == "string") {
            data = data.slice(0, 10);
          }
          return data;
        },
      }, //計劃開始
      { field: "etime", label: this.$t("V_Task_etime"), className: "all",width: "70px" }, //天數
      { field: "planedate", label: this.$t("V_Task_planedate"), className: "all",width: "150px",
        render: function (data, type, row) {
          if (typeof data == "string") {
            data = data.slice(0, 10);
          }
          return data;
        },
      }, //計劃結束
      { field: "atime", label: this.$t("V_Task_atime"), className: "all",width: "70px" }, //實際天數
      { field: "bdate", label: this.$t("V_Task_bdate"), className: "all",width: "150px",
        render: function (data, type, row) {
          if (typeof data == "string") {
            data = data.slice(0, 10);
          }
          return data;
        },
      }, //實際開始
      { field: "edate", label: this.$t("V_Task_edate"), className: "all",width: "150px",
        render: function (data, type, row) {
          if (typeof data == "string") {
            data = data.slice(0, 10);
          }
          return data;
        },
      }, //實際結束
      { field: "priority", label: this.$t("V_Task_priority"), className: "all",width: "70px" }, //優先級
      { field: "remark", label: this.$t("V_Task_remark"), className: "all",width: "300px" }, //備註
      { field: "progress", label: this.$t("V_Task_progress"), className: "all",width: "70px" }, //進度
      { field: "revisedby", label: this.$t("V_Task_revisedby"), className: "all",width: "70px" }, //修改人
      { field: "relationid", label: this.$t("V_Task_relationid"), className: "all",width: "200px" }, //關聯編號
      { field: "",
        label: "",
        className: "none",
        render: function (data, type, row) {
          // 开始构建表格的字符串 
          /*
            序號,程序員,描述,開始日期,結束日期,天數,分數,質量,備註,修改人,進度
           */
          let tableHtml = `
              <table class="table table-bordered w-100" border="1">
                  <thead>
                      <tr>
                          <th>${self.$t('V_TaskItem_itemid')}</th>
                          <th>${self.$t('V_TaskItem_programmer')}</th>
                          <th>${self.$t('V_TaskItem_descriptions')}</th>
                          <th>${self.$t('V_TaskItem_startdate')}</th>
                          <th>${self.$t('V_TaskItem_enddate')}</th>
                          <th>${self.$t('V_TaskItem_time_used')}</th>
                          <th>${self.$t('V_TaskItem_score')}</th>
                          <th>${self.$t('V_TaskItem_quality')}</th>
                          <th>${self.$t('V_TaskItem_remark')}</th>
                          <th>${self.$t('V_TaskItem_revisedby')}</th>
                          <th>${self.$t('V_TaskItem_progress')}</th>
                      </tr>
                  </thead>
                  <tbody>`;

          // 遍历传入的 data 数组，为每个元素创建一个表格行
          row.item_array.forEach(item => {
              tableHtml += `
                  <tr>
                      <td>${item.itemid}</td>
                      <td>${item.programmer}</td>
                      <td class="text-truncate" title="${item.descriptions}" style="max-width:120px">${item.descriptions}</td>     
                      <td>${item.startdate}</td>
                      <td>${item.enddate}</td>
                      <td>${item.time_used}</td>
                      <td>${item.score}</td>
                      <td>${item.quality}</td>
                      <td class="text-truncate" title="${item.remark}"  style="max-width:120px">${item.remark}</td>
                      <td>${item.revisedby}</td>
                      <td>${item.progress}</td>
                  </tr>`;
          });

          // 完成表格的构建 共(Total) 條(items)
          tableHtml += `
                  </tbody>
                  <tfoot>
                    <tr>
                      <td colspan="11">${self.$t('total')}${row.item_array.length}${self.$t('entries')}</td>
                    </tr>
                  </tfoot>
              </table>`;

          return tableHtml;
        },
      },
      { field:"inc_id", label:"inc_id", visible:true}      
    ],
    taskProgressColumns:[ //任務進度列表
      { field: "taskno", label: this.$t("V_Task_pid_taskno"), width: "150px" }, // 任務編號
      { field: "task", label: this.$t("V_Task_pid_task"), width: "300px" }, // 任務描述
      { field: "progress", label: this.$t("V_Task_progress")}, // 進度
    ],
    userColumns:[ //用户列表
      { field: "username", label: this.$t("Users_username"), width: "90px" }, //Users_username 用户编号
      { field: "workno", label: this.$t("Users_workno"), width: "90px" }, //Users_workno 工号
    ],
    pidColumns:[ //在彈框中選擇數據獲取pid
      { field: "pid", label: this.$t("Project_pid"), width: "90px" },
      { field: "pname", label: this.$t("Project_pname"), width: "90px" },
    ],
    tidColumns:[ //在彈框中選擇數據獲取tid
      { field: "pid", label: this.$t("TaskList_pid"), width: "90px" },
      { field: "tid", label: this.$t("TaskList_tid"), width: "90px" },
      { field: "sdesp", label: this.$t("TaskList_sdesp"), width: "90px" },
    ],
    taskColumns:[ //任務列表
      { field: "pid", label: this.$t("V_Task_pid"), width: "90px" }, //工程編號 
      { field: "tid", label: this.$t("V_Task_tid") }, //類別編號 
      { field: "taskid", label: this.$t("V_Task_taskid") }, //任務編號 
      { field: "task", label: this.$t("V_Task_task"), width: "300px" }, //任務描述 
      { field: "contact", label: this.$t("V_Task_contact") }, //聯繫人 
      { field: "progress", label: this.$t("V_Task_progress") }, //進度 
      { field: "docpath", label: this.$t("V_Task_docpath"), width: "150px" }, //關聯文檔 
      { field: "relationid", label: this.$t("V_Task_relationid"), width: "300px" }, //關聯任務 
      { field: "quantity", label: this.$t("V_Task_quantity") }, //數量 
      { field: "planbdate", label: this.$t("V_Task_planbdate"),
        width: "150px",
        render: function (data, type, row) {
          if (typeof data == "string") {
            data = data.slice(0, 10);
          }
          return data;
        },
      }, //計劃開始 
      { field: "planedate", label: this.$t("V_Task_planedate"),
        width: "150px",
        render: function (data, type, row) {
          if (typeof data == "string") {
            data = data.slice(0, 10);
          }
          return data;
        },
      }, //計劃結束 
      { field: "etime", label: this.$t("V_Task_etime") }, //實際天數 
      { field: "bdate", label: this.$t("V_Task_bdate"),
        width: "150px",
        render: function (data, type, row) {
          if (typeof data == "string") {
            data = data.slice(0, 10);
          }
          return data;
        },
      }, //實際開始 
      { field: "edate", label: this.$t("V_Task_edate"),
        width: "150px",
        render: function (data, type, row) {
          if (typeof data == "string") {
            data = data.slice(0, 10);
          }
          return data;
        },
      }, //實際結束 
      { field: "priority", label: this.$t("V_Task_priority") }, //優先級 
      { field: "remark", label: this.$t("V_Task_remark"), width: "300px" }, //備註 
      { field: "revisedby", label: this.$t("V_Task_revisedby") }, //修改人 
    ],
    admrfColumns:[ //ADMRF
      { field: "inc_id", label: "inc_id", visible: false },
      { field: "rf002", label: "rf002", visible: false },
      { field: "rf003", label: this.$t("ADMRF_rf003") }, //序號 ADMRF_rf003
      { field: "rf004", label: this.$t("ADMRF_rf004") }, //功能列表 ADMRF_rf004
      { field: "rf005", label: this.$t("ADMRF_rf005") }, //功能重要性 ADMRF_rf005
    ],
    moduleObjectColumns:[ //功能列表 ModuleObject
      { field: "sys", label: this.$t('ModuleObject_sys')}, //主系統編號 ModuleObject_sys
      { field: "moduleid", label: this.$t('ModuleObject_moduleid')}, //模塊編號 ModuleObject_moduleid
      { field: "objectname", label: this.$t('ModuleObject_objectname')}, //對象名稱 取值 ModuleObject_objectname
      { field: "objecttype", label: this.$t('ModuleObject_objecttype')}, //對象類型 ModuleObject_objecttype
      { field: "description", label: this.$t('ModuleObject_description'), width: "300px"}, //對象的標籤 ModuleObject_description
    ],
    moduleColumns:[ //窗體列表 Module
      { field: "moduleid", label: this.$t('Module_moduleid')}, //程序編號 Module_moduleid
      { field: "modulename", label: this.$t('Module_modulename')}, //程序名稱 取值 Module_modulename
      { field: "sys", label: this.$t('Module_sys')}, //主系統編號 Module_sys
      { field: "description", label: this.$t('Module_description'), width: "300px"}, //程序描述 Module_description
      { field: "parentid", label: this.$t('Module_parentid')}, //父編號 Module_parentid
      { field: "moduletype", label: this.$t('Module_moduletype')}, //程序類型 Module_moduletype
    ],
    systemColumns:[ //系統列表 System
      { field: "sys", label: this.$t('System_sys')}, //系統名稱 取值 System_sys
      { field: "sysid", label: this.$t('System_sysid')}, //系統編號 System_sysid
      { field: "sysremark", label: this.$t('System_sysremark')}, //系統描述 System_sysremark
    ],
    masterColumns:[ //系統問題上報列表 ADMRP
      { field: "rp017", label: this.$t('ADMRP_rp017'), width: "150px"}, //單號 ADMRP_rp017
      { field: "rp002", label: this.$t('ADMRP_rp002'), width: "110px", //提出日期 ADMRP_rp002
        render: DateRender,type:'date'
      },
      { field: "rp003", label: this.$t('ADMRP_rp003')}, //提出部門 ADMRP_rp003
      { field: "rp004", label: this.$t('ADMRP_rp004'), width: "90px"}, //提出人員 ADMRP_rp004
      { field: "rp005", label: this.$t('ADMRP_rp005'), width: "300px"}, //問題描述 ADMRP_rp005
      { field: "rp023", label: this.$t('ADMRP_rp023'), width: "100px"}, //問題所屬項目 ADMRP_rp023
      { field: "problemcategory", label: this.$t('Problem Category'), width: "120px"}, //問題級別 ADMRP_rp023 
      { field: "sessionpriority", label: this.$t('SessionPriority'), width:"60px" }, //模塊優先級           
      { field: "rp010", label: this.$t('ADMRP_rp010'), width: "130px"}, //跟進人 ADMRP_rp010
      { field: "rp029", label: this.$t('ADMRP_rp029'), width: "60px"}, //問題級別 ADMRP_rp023
      { field: "rp033", label: this.$t('ADMRP_rp033'), width: "60px"}, //優先級 ADMRP_rp033
      { field: "rp024", label: this.$t('ADMRP_rp024'), width: "300px"}, //關聯Task ADMRP_rp024
      { field: "rp007", label: this.$t('ADMRP_rp007'), width: "300px"}, //處理方式&結果 ADMRP_rp007
      { field: "rp008", label: this.$t('ADMRP_rp008'), width: "300px"}, //發生問題的原因 ADMRP_rp008
      { field: "rp009", label: this.$t('ADMRP_rp009')}, //跟進部門 ADMRP_rp009
      { field: "rp011", label: this.$t('ADMRP_rp011')}, //狀態 ADMRP_rp011
      { field: "rp031", label: this.$t('ADMRP_rp031'), width: "110px", //計劃開始 ADMRP_rp031
        render: DateRender
      },
      { field: "rp032", label: this.$t('ADMRP_rp032'), width: "110px",
        render: DateRender
      },
      { field: "rp012", label: this.$t('ADMRP_rp012'), width: "110px",
        render: DateRender
      }, //處理開始日期 ADMRP_rp012
      { field: "rp013", label: this.$t('ADMRP_rp013'), width: "110px",
        render: DateRender
      }, //處理結束日期 ADMRP_rp013
      { field: "remark", label: this.$t('ADMRP_rp014'), width: "300px"}, //備註 ADMRP_rp014
      { field: "inc_id", label: "inc_id", visible: false },
    ],
    masterOptions:{
      scrollY: 660,
      responsive: false,
      autoWidth: false,
      scrollX: true,
      columnDefs: [
        {
          targets: [5,7,11,12,13,19],
          render: function (data, type, full, meta) {
            if (data) {
              if (data.length > 15) {
                return (
                  "<label title='" +
                  data +
                  "' style='text-decoration: none;'>" +
                  data.trim().substr(0, 15) +
                  "..." +
                  "</label>"
                );
              } else {
                return data;
              }
            } else {
              return "";
            }
          },
        },
      ],
    },
    systemOptions:{
      scrollY: 300,
    },
    moduleOptions:{
      scrollY: 300,
      responsive: false,
      autoWidth: false,
      scrollX: true,
      columnDefs: [
        {
          targets: [3],
          render: function (data, type, full, meta) {
            if (data) {
              if (data.length > 15) {
                return (
                  "<label title='" +
                  data +
                  "' style='text-decoration: none;'>" +
                  data.trim().substr(0, 15) +
                  "..." +
                  "</label>"
                );
              } else {
                return data;
              }
            } else {
              return "";
            }
          },
        },
      ],
    },
    moduleObjectOptions:{
      scrollY: 300,
      responsive: false,
      autoWidth: false,
      scrollX: true,
      columnDefs: [
        {
          targets: [4],
          render: function (data, type, full, meta) {
            if (data) {
              if (data.length > 15) {
                return (
                  "<label title='" +
                  data +
                  "' style='text-decoration: none;'>" +
                  data.trim().substr(0, 15) +
                  "..." +
                  "</label>"
                );
              } else {
                return data;
              }
            } else {
              return "";
            }
          },
        },
      ],
    },
    admrfOptions:{
      deferLoading: 0,
      scrollY: 173,
      responsive: false,
      autoWidth: false,
      scrollX: true,
      columnDefs: [
        {
          targets: [2],
          render: function (data, type, full, meta) {
            if (data) {
              if (data.length > 15) {
                return (
                  "<label title='" +
                  data +
                  "' style='text-decoration: none;'>" +
                  data.trim().substr(0, 15) +
                  "..." +
                  "</label>"
                );
              } else {
                return data;
              }
            } else {
              return "";
            }
          },
        },
      ],
    },
    taskOptions:{
      deferLoading: 0,
      scrollY: 500,
      responsive: false,
      autoWidth: false,
      scrollX: true,
      columnDefs: [
        {
          targets: [3,7,15],
          render: function (data, type, full, meta) {
            if (data) {
              if (data.length > 15) {
                return (
                  "<label title='" +
                  data +
                  "' style='text-decoration: none;'>" +
                  data.trim().substr(0, 15) +
                  "..." +
                  "</label>"
                );
              } else {
                return data;
              }
            } else {
              return "";
            }
          },
        },
      ],
    },
    tidOptions:{
      deferLoading: 0,
      scrollY: 500,
      responsive: false,
      autoWidth: false,
      scrollX: true,
      columnDefs: [
        {
          targets: [2],
          render: function (data, type, full, meta) {
            if (data) {
              if (data.length > 15) {
                return (
                  "<label title='" +
                  data +
                  "' style='text-decoration: none;'>" +
                  data.trim().substr(0, 15) +
                  "..." +
                  "</label>"
                );
              } else {
                return data;
              }
            } else {
              return "";
            }
          },
        },
      ],
    },
    pidOptions:{
      deferLoading: 0,
      scrollY: 500,
      responsive: false,
      autoWidth: false,
      scrollX: true,
    },
    taskProgressOptions:{
      deferLoading: 0,
      scrollY: 300,
      responsive: false,
      autoWidth: false,
      scrollX: true,
      columnDefs: [
        {
          targets: [1],
          render: function (data, type, full, meta) {
            if (data) {
              if (data.length > 15) {
                return (
                  "<label title='" +
                  data +
                  "' style='text-decoration: none;'>" +
                  data.trim().substr(0, 15) +
                  "..." +
                  "</label>"
                );
              } else {
                return data;
              }
            } else {
              return "";
            }
          },
        },
      ],
    },
    associatedTaskOptions:{
      deferLoading: 0,
      scrollY: 600,
      responsive: false,
      autoWidth: false,
      scrollX: true,
      columnDefs: [
        {
          targets: [3,12],
          render: function (data, type, full, meta) {
            if (data) {
              if (data.length > 15) {
                return (
                  "<label title='" +
                  data +
                  "' style='text-decoration: none;'>" +
                  data.trim().substr(0, 15) +
                  "..." +
                  "</label>"
                );
              } else {
                return data;
              }
            } else {
              return "";
            }
          },
        },
      ],
      responsive:{
        // 立即在子行中顯示信息,無需等待用戶請求
        // details: { display: $.fn.dataTable.Responsive.display.childRowImmediate, } 
      }
    },
    taskItemOptions:{
      deferLoading: 0,
      scrollY: 300,
      responsive: false,
      autoWidth: false,
      scrollX: true,
    },
    flowChartOptions:{
      deferLoading: 0,
      scrollY: 150,
      responsive: false,
      autoWidth: false,
      scrollX: true,
      processing: true,
    },
    masterTable_order_by:[
      ["rp002", "desc"],
      // ["rp002", "asc"],
    ],
    functionArray:[
      { label: this.$t('Terminate problem'), event: "onFun1" }, //結束問題 Terminate problem
      { label: this.$t('Transfer problem'), event: "onFun2" }, //轉交問題 Transfer problem
      { label: this.$t('ArrangeTask'), event: "onFun3" }, //安排任務 ArrangeTask
    ],
    //AI查詢相關
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
    docmhParamsFun: undefined,
    admrpParamsFun: undefined,
    masterParamsFun: undefined,
    admrfParamsFun: undefined,
    task_params_fun: undefined,
    tid_params_fun: undefined,
    pid_params_fun: undefined,
    taskProgressParamsFun:undefined,
    associatedTask_params_fun:undefined,
    taskItemParamsFun:undefined,
    flowChart_params_fun:undefined,
    currentMaster:{}, //單頭對象
    currentMasterClone:{}, //單頭克隆對象
    currentTamp:{}, //臨時對象
    currentAdmrf:{}, //功能對象
    defaultProject:{}, //默認工程對象
    currentTask:{}, //任務對象
    cmsmeArray:[], //部門信息列表
    username: $("#login_username").val(), //獲取當前登錄用戶
    state: 0, //狀態標識對象 0:不可編輯,1:可編輯,2:附件不可編輯
    masterState: 0, //狀態標識對象 0:默認狀態 1:新增,2:修改
    admrqNo:'', //附件ID
    image:'', //詳細資料頁面上傳相關圖片
    Modal_title:'',//form表單標題
    deptNo:'',
    //以下為安排Task功能引用相關屬性
    ut002:'', //pid
    ut003:'', //tid
    taskState:true,//状态标识对象 true:显示简单设置任务,false:显示详细设置任务
    lang_code_en:true,
    bugImgArray: [], //存放系統問題上報圖片
    fileArray_left:[], //存放系統問題上報附件(左)
    fileArray_right: [], //存放系統問題上報附件(右)
    file : {}, //文件對象
    isInfoBrowse: true,
    isLoading: false,  // 添加加载状态
    flowChart: {}, // 流程圖對象
    flowChartModal_title:'',
    flowChartState: '1', // 狀態標識對象 1:新增,2:修改
    category: "",
    currentPrompt: {},
    prompt_filter: "",
    showTaskData: false,
    dataColumns: [],
    bugAiOptions: {
      responsive: false,
      autoWidth: false,
      scrollX: true,
      // scrollY: "auto",
      // scrollCollapse: true, // 啟用滾動折疊
      deferLoading: 0,
      scrollY: '62vh',
    },
    topSysBugs: [],
    aiPredefinedData: [],
    isapproved: false,
    historySsql: "",
    // activeTab:2,
    isTaskTabActive: false,
    selectedProgress: "",
    selectedPromptProgress: "",
    selectedPriority: "",
    selectedPromptPriority: "",
    selectedContact: "",
    selectedPromptContact: "",
    selectedCondition: null,
    selectedClass: "",
    selectedPromptClass: "",
    aiProblemData: "", //發送給Ai分析的數據
    showLPAIComBox: true, // 控制LPAIComBox顯示
    showLPAIAnalysisComBox: true, // 控制LPAIAnalysisComBox顯示
    messageSent: false, //狀態標識對象,判斷有沒有發送過消息給GPT
    messageNo: '', //消息記錄對象,判斷打開Ai分析時是否為同一條數據,當數據不同時重新發送消息給GPT
  }
},
computed: {
  textareaRows() {
    // 根據屏幕寬度動態計算行數
    return window.innerWidth < 576 && this.masterState == 1 ? 15 : 7;
  }
},
mounted() {
  this.get_fetchUrlParams();
  this.get_cmsmeArray();
  this.getProblemCategoryData();
  this.getContacts();
  $('.wrapper').on('shown.bs.modal', function (e) {
    $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
  });
  $('.wrapper').on("shown.bs.tab", "a[data-toggle='tab']", function (e) {
    $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
  });

  var self = this
  this.$nextTick(function () {
    self.get_lang_code();
    $('.systemBugRptCard a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
      if ($(e.currentTarget).hasClass("infoBrowse")) {
        self.isInfoBrowse = true
      } else {
        self.isInfoBrowse = false
      }
    });

    // 监听 select2:open 事件
    $(".noFirstVal").on('select2:open', () => {
      setTimeout(() => {
        $(".select2-container.select2-container--open ul.select2-results__options>li.select2-results__option").each(function() {
          if ($(this).attr("id") === undefined) {
            $(this).addClass("d-none"); //當select2下拉選屬性中的id為空時,設置隱藏
          }
        });
      }, 0);
    });

    // 聯繫人和全部聯繫人選擇框的處理
    $(".select2-contact")
      .select2()
      .on("select2:select", function (e) {
        self.contact = e.params.data.text;
      });
    $(".select2-contact-mul")
      .select2()
      .on("select2:select", function (e) {
        var text = e.params.data.text;
        if (!self.allContact.includes(text)) self.allContact.push(text);
      })
      .on("select2:unselect", function (e) {
        var text = e.params.data.text;
        if (self.allContact.includes(text)) {
          self.allContact.splice(self.allContact.indexOf(text), 1);
        }
      });
    $(".select2-progress")
      .select2()
      .on("select2:select", function (e) {
        self.selectedProgress = e.params.data.id;
      });

    $(".select2-promptprogress")
      .select2()
      .on("select2:select", function (e) {
        self.selectedPromptProgress = e.params.data.id;
      });

    $(".select2-priority")
      .select2()
      .on("select2:select", function (e) {
        self.selectedPriority = e.params.data.id;
      });

    $(".select2-promptpriority")
      .select2()
      .on("select2:select", function (e) {
        self.selectedPromptPriority = e.params.data.id;
      });

    $(".select2-contact-task")
      .select2()
      .on("select2:select", function (e) {
        self.selectedContact = e.params.data.id;
      });

    $(".select2-promptcontact-task")
      .select2()
      .on("select2:select", function (e) {
        self.selectedPromptContact = e.params.data.id;
      });
    //$('.select2-condition-task').select2().on("select2:select", function (e) { _this.selectedCondition = e.params.data.id });
    $(".select2-class")
      .select2()
      .on("select2:select", function (e) {
        self.selectedClass = e.params.data.id;
      });

    $(".select2-promptclass")
      .select2()
      .on("select2:select", function (e) {
        self.selectedPromptClass = e.params.data.id;
      });


    $("title").html(this.$t("System Issue Reporting"));
    $(this.$refs.sqlButton).popover({
      content: this.$t('SQL Execution Successful'), //SQL 執行成功
      placement: 'top',
      trigger: 'manual'
    });
    $(this.$refs.saveButton).popover({
      content: this.$t('Save Successful'), //保存成功
      placement: 'top',
      trigger: 'manual'
    });
  })

  this.setModelBackdrop('docmhModal_ref');
  this.setModelBackdrop('sysBugModals_ref');
  this.setModelBackdrop('solutiontypeModals_ref');
  this.$refs.flowChart_modalForm.$refs.modal.show = function() { 
    $(this.$refs.modal).modal({
      backdrop: 'static', // 防止點擊背景關閉
      keyboard: false // 禁用 Esc 關閉
    });
  };

  $('.systemBugRptCard .detailInfo a[data-toggle="tab"]').on(
        "shown.bs.tab",
        function (e) {
          if (
            $(e.currentTarget).attr("id") === "tab_tasks" ||
            $(e.currentTarget).attr("id") === "tab_sql"
          ) {
            self.isTaskTabActive = true;
          } else {
            self.isTaskTabActive = false;
          }
        }
      );

  // 在 Vue 组件挂载后调用初始化右键菜单的方法
  this.$nextTick(() => {
    this.initializeContextMenu(); //; 初始化 上報數據 表格的右键菜单
  });
  window.addEventListener('resize', ()=>{$.fn.dataTable.tables({ visible: true, api: true }).columns.adjust()});
},
watch:{
  "currentMaster.rp003":function(){
      this.$nextTick(function () {
        $('select.select2-type').trigger('change');
        $('select.select2-type2').trigger('change');
      });
  },
  "currentMaster.rp009":function(){
      this.$nextTick(function () {
        $('select.select2-genjin').trigger('change');
        $('select.select2-genjin2').trigger('change');
      });
  },
  category: function () {
    this.setPromptFilter();
  },
},
methods: {
  //需求分析按鈕點擊事件(通過Ai去問清用戶的需求)
  openAiRequirementAnalysis() {
    var self = this;
    // 设置发送给 GPT 的数据，并将段落标签添加到 aiProblemData 中
    this.aiProblemData = `
    You are a user and want to pass my requirement to a programmer to help create a program for me 
    
    2. Your response will include 3 sections.
    a) Iterated prompt (This is the prompt that you will rewrite each time I answer more questions . It should be clear, concise, and easily understood by the student). 
    c) Questions( 
    Options: 1. Let the programmer to ask any questions. 2. Inform users what resources are available, such as tables, diagrams, or similar existing program, etc
    )
    
    This is the system issue report submitted by the user: '{0}'

    Ask the above question one by one for each Iterated prompt.
    `.format(JSON.stringify(this.currentMaster.rp005));

    this.showLPAIComBox = false;  // 隐藏LPAIComBox
    // this.showLPAIAnalysisComBox = false;  // 隱藏LPAIAnalysisComBox
    this.showLPAIAnalysisComBox = true;  // 显示LPAIAnalysisComBox

    $(this.$refs.aicombox_to.$refs.modal).modal('hidden.bs.modal', function(e) {
      //重新v-if=false一下可以清空聊天記錄
    })
    
    // 显示弹窗并发送数据
    this.$nextTick(() => {
      self.showLPAIAnalysisComBox = true;  // 显示LPAIAnalysisComBox
      self.$refs.aicombox_to.$refs.modal.show(); // 显示弹窗
      if(self.currentMaster.rp017 === undefined) return
      // if(self.messageSent && self.messageNo === this.currentMaster.rp017) return // 如果已经发送过消息，则只打开弹窗

      self.$refs.aicombox_to.InputVal = this.aiProblemData; // 设置 InputVal
      // 加入 setTimeout，确保 InputVal 被设置后再发送数据
      setTimeout(() => {
        self.$refs.aicombox_to.sendDataToReact("InputVal"); // 发送数据给 GPT
        // self.messageSent = true;
        // self.messageNo = this.currentMaster.rp017;
      }, 100); // 延迟一点时间，确保数据已经设置完成
    });
  },

  // openAiRequirementAnalysis() {
  //   var self = this;
  //   // 设置发送给 GPT 的数据，并将段落标签添加到 aiProblemData 中
  //   this.aiProblemData = `
  //     You are a programmer to help to program from a user's requirement to form a functional requirement.
  //     The functional requirement needs to have at least the technical involved and what tables or fields involved. If possible help to generate the necessary UML diagrams.
  //     1. Your answer might be very specific or choose one of your suggested options.
  //     2. Your response will include 3 sections. 
  //     a) Iterated prompt (This is the prompt that you will rewrite each time I answer more questions. 
  //     It should be clear, concise, and easily understood by the student).
  //     c) Questions (Options:) Ask the above question one by one for each Iterated prompt.

  //     The following is the user's requirement: '{0}'

  //     Please continue to provide more detailed information on the above.
  //   `.format(JSON.stringify(this.currentMaster.rp005));

  //   this.showLPAIComBox = false;  // 隐藏LPAIComBox
  //   this.showLPAIAnalysisComBox = true;  // 显示LPAIAnalysisComBox

  //   // 显示弹窗并发送数据
  //   this.$nextTick(() => {
  //     self.$refs.aicombox_to.$refs.modal.show(); // 显示弹窗

  //     if(self.messageSent) return // 如果已经发送过消息，则只打开弹窗

  //     self.$refs.aicombox_to.InputVal = this.aiProblemData; // 设置 InputVal
  //     // 加入 setTimeout，确保 InputVal 被设置后再发送数据
  //     setTimeout(() => {
  //       self.$refs.aicombox_to.sendDataToReact("InputVal"); // 发送数据给 GPT
  //       self.messageSent = true
  //     }, 100); // 延迟一点时间，确保数据已经设置完成
  //   });
  // },

  //獲取聯繫人
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
  handleSsqlChange() {
    // 當 ssql 的值發生變化時，將 isai 賦值為 false
    if (this.currentPrompt.ssql === this.historySsql) {
      this.currentPrompt.isai = true;
    } else {
      this.currentPrompt.isai = false;
    }
  },
  //系統問題上報列表單擊事件
  master_row_click(event, data){
    if(data == undefined) return
    // this.getMasterInfo(data.inc_id,'');
  },
  initializeContextMenu() {
      const _this = this;
      $.contextMenu({
        // selector: "#top-task .dataTables_scrollBody tbody tr",
        selector: "#Admrp_list tbody tr",
        callback: function (key, options) {
          if(key === "feedback"){
            _this.$refs.feedbackModal_ref.width("30%");
            _this.$refs.feedbackModal_ref.show();
          }
        },
        items: {
          // feedback: {
          //   name: "用戶反饋", // 用戶反饋
          //   // icon: "bi bi-chat-dots"
          // },

          /**
           * 添加子菜單選項
          sysbug: {
            name: this.$t('View Reported Issues'), // 查看上報信息
            icon: "fa-eye"
          },
          */
        },
      });
    },

  //保存查詢sql
  savePrompt() {
    if (this.currentPrompt.sname == "")
      return this.showMessage(this.$t("Prompt cannot be empty.")); //提示不能為空.
    axios
      .post("/looper/session_manager/approve_condition", this.currentPrompt)
      .then((response) => {
        if (response.data.status) {
          this.currentPrompt = response.data.data;
          // this.showMessage("保存成功");
          this.showSuccessSavePromptPopover()
        } else {
          this.showMessage(response.data.msg);
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
  // 执行SQL并显示结果
  executeSql() {
    // $("#tab_tasks").click();
    this.showTaskData = false;
    // console.log('this.topTasks1',this.topSysBugs);
    const sql = this.currentPrompt.ssql;
    // 检查 SQL 查询是否为空
    if (!sql) {
      this.showMessage(this.$t("SQL Query Cannot Be Empty")); //SQL查询不能为空
      return;
    }
    // 发送请求到后端执行 SQL
    axios.post("/systembugrpt/execute_sql", { sql })
      .then((response) => {
        // console.log("后端响应数据:", response.data);
        if (response.data.status) {
          // 成功时将数据填充到表格
          // 将返回的数据的字段名全部转换为小写
          this.generateHeaders(response.data.columns);
          this.topSysBugs = response.data.data.map((item) => {
              let newItem = {};
              Object.keys(item).forEach((key) => {
                newItem[key.toLowerCase()] = item[key];
              });
              return newItem;
          });
          // this.topSysBugs = response.data.data
          // console.log('this.topTasks2',this.topSysBugs);
          this.showTaskData = true;
          this.$nextTick(function () {
            this.$nextTick(function () {
              this.$refs.bugTable.datatable
                .clear()
                .rows.add(this.topSysBugs || [])
                .draw();
            });
          });
          this.showSuccessExecuteSqlPopover();
        } else {
          // 处理后端返回的错误信息
          this.showMessage(`${this.$t('SQL Execution Failed')}:  ${response.data.msg}`) //SQL 執行失敗: 
        }
      })
      .catch((error) => {
        // 捕获网络错误或其他请求错误
        console.error("执行 SQL 出错:", error);
        // this.showMessage("执行 SQL 出错，请检查日志");
        this.showMessage(this.$t("Error Executing SQL, Please Check the Logs")); //执行 SQL 出错，请检查日志
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
  //AI分析按鈕點擊事件
  aiAnalysis() {
    this.aiPredefinedData = this.topSysBugs;
    this.showLPAIComBox = true;  // 隱藏LPAIComBox
    this.showLPAIAnalysisComBox = false;  // 顯示LPAIAnalysisComBox
    this.$nextTick(function () {
      this.$refs.aicombox.$refs.modal.show();
    });
  },
  //將用戶錄入的自然語言提交給AI,用AI生成SQL查詢上報信息
  fetchSysBugTable() {
    if (!this.currentPrompt.sname) return //用戶沒有錄入數據時不進行查詢
    $("#tab_tasks").click();
    this.showTaskData = false;
    axios
      .get("/systembugrpt/fetch_sysbug_table", {
        params: {
          // record_id: this.ai_recordID, // 替換為您的SubProjectID
          // contact: this.selectedContact, // 替換為您的聯繫人
          condition: this.currentPrompt.inc_id || '', // 當前選中的條件
          question: this.currentPrompt.sname, //查詢的內容
        },
      })
      .then((response) => {
        if(response.data.status){
          this.currentPrompt = response.data.promtsql;
          this.historySsql = this.currentPrompt.ssql;
          this.topSysBugs = response.data.data;
          // console.log('首次this.topSysBugs',this.topSysBugs);
          this.generateHeaders(response.data.columns);
          this.showTaskData = true;
          this.$nextTick(function () {
            this.$nextTick(function () {
              this.$refs.bugTable.datatable
                .clear()
                .rows.add(this.topSysBugs || [])
                .draw();
            });
          });
        }else{
          this.showMessage(this.$t("Data query failure")); //查詢數據失敗
        }
        
      })
      .catch((error) => {
        console.log(error);
      });
  },
  //清空按鈕點擊事件
  clearTasksHandler() {
    // this.taskText = "";
    // this.ai_recordID = "";
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
        "select.select2-progress, select.select2-priority, select.select2-class, select.select2-contact-task"
      )
        .val(null)
        .trigger("change");
    });
  },
  generateHeaders(columns) {
    const lowerCaseColumns = columns.map(column => column.toLowerCase());

    // 字段名与字段描述的映射关系
    const fieldDescriptions = [
      { rp016: this.$t('ADMRP_rp016') }, //單別
      { rp017: this.$t('ADMRP_rp017') }, //單號
      { rp001: this.$t('Version Number') }, //版本號
      { rp002: this.$t('ADMRP_rp002') }, //提出日期
      { rp003: this.$t('ADMRP_rp003') }, //提出部門
      { rp004: this.$t('ADMRP_rp004') }, //提出人員
      { rp005: this.$t('ADMRP_rp005') }, //問題描述
      { rp007: this.$t('ADMRP_rp007') }, //處理方式&結果
      { rp008: this.$t('ADMRP_rp008') }, //發生問題的原因
      { rp009: this.$t('ADMRP_rp009') }, //跟進部門
      { rp010: this.$t('ADMRP_rp010') }, //跟進人
      { rp011: this.$t('ADMRP_rp011') }, //狀態
      { rp012: this.$t('ADMRP_rp012') }, //處理開始日期
      { rp013: this.$t('ADMRP_rp013') }, //處理結束日期
      { rp014: this.$t('Remark')}, //備注
      { rp015: this.$t('Transfer to Computer Department') }, //轉電腦部處理
      { rp018: this.$t('Mark Issue Report Conversion Status') }, //標記問題上報轉換狀態
      { rp019: this.$t('Custom Field') }, //自定義字段
      { rp006: this.$t('Attachment') }, //附件
      { rp020: this.$t('ADMRP_rp020') }, //系統名稱 
      { rp021: this.$t('ADMRP_rp021') }, //問題類型 
      { rp022: this.$t('ADMRP_rp022') }, //窗體名稱
      { rp023: this.$t('ADMRP_rp023') }, //問題所屬項目
      { rp024: this.$t('ADMRP_rp024') }, //關聯Task
      { rp025: this.$t('ADMRP_rp025') }, //更新穩定版 
      { rp026: this.$t('ADMRP_rp026') }, //更新開發版 
      { rp027: this.$t('ADMRP_rp027') }, //功能名稱
      { rp028: this.$t('ADMRP_rp028') }, //功能依賴對象 
      { rp029: this.$t('ADMRP_rp029') }, //問題級別
      { rp030: this.$t('ADMRP_rp030') }, //是否重要窗口 
      { rp031: this.$t('Planned Start Time') }, //計划開始時間
      { rp032: this.$t('Planned End Time') }, //計划結束時間
      { rp033: this.$t('ADMRP_rp033') }, //優先級
      { rp034: this.$t("Previous Issue's RP017 Property") }, //前一問題的rp017屬性
      { rp035: this.$t('Export Mark') }, //導出標記
      { rp036: this.$t('Session ID') }, //會話ID
      { rp037: this.$t('Handling Category') }, //處理分類
      { rp038: this.$t('Handling Method') }, //處理方式(1:維護,2:換配件)
      { rp039: this.$t('Report Time') }, //上報時間
      { rp040: this.$t('Equipment Number') }, //設備編號
      { rp041: this.$t('ADMRP_rp041') }, //固定資產編號 
      { rp043: this.$t('ADMRP_rp043') }, //原始提出人 
      { rp044: this.$t('ADMRP_rp044') }, //上報類型 
      { rp045: this.$t('ADMRP_rp045') }, //規則 
      { rp046: this.$t('ADMRP_rp046') }, //影響的表 
      { rp047: this.$t('Flowchart') }, //流程圖
      { rp048: this.$t('Expected Outcome') }, //預期結果
      { rp049: this.$t('ADMRP_rp049') }, //預計時間 
      { rp050: this.$t('ADMRP_rp050') }, //功能性需求 
      { rp051: this.$t('ADMRP_rp051') }, //後台處理 
      { rp052: this.$t('ADMRP_rp052') }, //需求優先級 
      { rp053: this.$t('ADMRP_rp053') }, //需求描述及邏輯 
      { rp054: this.$t('Function list organizing') }, //功能列表整理 
      { rp055: this.$t('Progress') }, //進度 
      { rp056: this.$t('Feedback Comments') }, //反餽意見
      { rp057: this.$t('Reserved Field') }, //備用字段
      { rp058: this.$t('Atypical function') }, //非典型功能 
      { rp059: this.$t('Selected Field') }, //勾選字段
      { solutiontype: this.$t('SolutionType') }, //解決方案類型 
      { remark: this.$t('Remark') }, //備注
      { description: this.$t('ADMRP_description') }, //說明 
      { problemcategory: this.$t('Problem Category') }, //問題類別
      { processtype: this.$t('Process Type')}, //處理結果
      { relationid: this.$t('RelationId') }, //關聯上報單號
      { sessionpriority: this.$t('SessionPriority') }, //模塊優先級
      // 继续添加其他字段与描述的映射关系
    ];

    this.dataColumns = lowerCaseColumns.map((column) => {
      let header = {
        label: column.toUpperCase(), // 默认label为字段名
        field: column,
      };

      // 查找字段描述
      const fieldDescription = fieldDescriptions.find(item => item[column.toLowerCase()]);
      if (fieldDescription) {
        header.label = fieldDescription[column.toLowerCase()]; // 用对应的描述替换label
      }

      // 如果没有找到描述，则保持字段名为label
      if (!fieldDescription) {
        header.label = column.toUpperCase(); // 如果没有匹配的描述，使用字段名作为label
      }

      // 设置宽度、渲染方式等
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

    // 打印输出生成的列头
    // console.log('Headers:', this.dataColumns);
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
  onConditionBlur(text) {
    this.currentPrompt.sname = text;
  },
  onConditionSelected(item) {
    this.fetchPromtsql(item.inc_id);
  },
  fetchPromtsql(inc_id) {
    axios
      .get(`/looper/session_manager/promtsql?id=${inc_id}`)
      .then((response) => {
        if (response.data.status) {
          this.currentPrompt = response.data.data;
          this.historySsql = this.currentPrompt.ssql;
        } else {
          this.showMessage(response.data.msg || "Failed to fetch Promtsql data.");
        }
      })
      .catch((error) => {
        this.showMessage("An error occurred while fetching Promtsql data.");
      });
  },
  //選擇窗口功能
  docmhClick(){
    const dataArray = this.$refs.docmhTable.getSelectedFlagData()["datas"];
    if (dataArray.length === 0) return this.showMessage(this.$t('Unselected data')); // 沒有選擇數據
    /* 檢測是否為同一窗口的數據 */
    // 獲取所有 mh001 的值
    const mh001Set = new Set(dataArray.map(item => item.mh001));
    // 如果 mh001 的值不一致，提示用戶並返回
    if (mh001Set.size > 1) {
      return this.showMessage(this.$t('Only one window function can be selected')); // 只能選擇一個窗口的功能
    }
    /* 給對應字段賦值 */
    const firstItem = dataArray[0];
    this.currentMaster.rp022 = firstItem.mh001; // 窗體名稱(編號)
    this.currentMaster.rp001 = firstItem.mh002; // 版本

    // rp027 取每一條數據的 mh003，並以 ";" 分隔
    this.currentMaster.rp027 = dataArray.map(item => item.mh003).join(";");

    // rp027c 取每一條數據的功能描述，格式為 "序號. 功能描述;"
    // 第二條數據開始換行顯示
    this.currentMaster.rp027c = dataArray
    .map((item, index) => `${index + 1}. ${item.mh004 || ''}`) // 為空值提供默認描述
    .join("\n"); // 使用 "\n" 表示換行

    this.$refs.docmhModal_ref.hide(); // 關閉彈窗
  },
  //窗口功能查詢按鈕點擊事件
  searchDocmhClick(){
    var self = this;
    var columns = [];
    for (let item of self.docmhColumns) {
        // if (["", "inc_id"].indexOf(item.field) != -1) continue;
        columns.push(item);
    }
    var query = self
    .GetQueryExp(
        "SystemBugRpt_vueFrm_docmhTable",
        columns
    )
    query.then((query) => {
      var query_value = {}
      if (query.master != undefined)
        query_value["attach_query"] = JSON.stringify(query.master);
        self.docmhParamsFun = function () {
            return query_value;
        };
        self.$nextTick(function () {
            self.$refs.docmhTable.datatable.column(0).search("").draw();
        });
    });
  },
  //功能描述輸入框點擊事件
  showDocmhModal(){
    $('#DataTables_Table_16_wrapper .dataTables_scrollBody').find('input.select-flag[type="checkbox"]').prop('checked', false);
    $('#DataTables_Table_16_wrapper .dataTables_scrollHead table tr th').eq(0).find('input:checkbox').prop('checked', false); //移除明細表格勾選信息
    $('.selected-row-info').text(''); //移除明細選擇顯示信息
    this.currentTamp = {};
    this.docmhParamsFun = undefined;
    this.$nextTick(function () {
      this.$refs.docmhTable.getSelectedInfo(); //刷新勾選狀態
      this.$refs.docmhTable.datatable.column(0).search("").draw();
    });
    this.$refs.docmhModal_ref.width("50%");
    this.$refs.docmhModal_ref.show();
  },
  //用戶選擇上報單號信息
  searchSysBugClick(){
    const dataArray = this.$refs.admrp_table.getSelectedFlagData()["datas"];
    if (dataArray.length === 0) return this.showMessage(this.$t('Unselected data')); //沒有選擇數據
    // 检查 currentMaster.relationid 是否为 null 或 undefined，若是，则初始化为空字符串
    if (!this.currentMaster.relationid) {
      this.currentMaster.relationid = '';
    }
    // 将选中的单号添加到 this.currentMaster.relationid 字段
    dataArray.forEach(order => {
      // 如果 currentMaster.relationid 为空，则初始化为当前选中的单号
      if (!this.currentMaster.relationid) {
        this.currentMaster.relationid = order.rp017;
      } else {
          // 如果 currentMaster.relationid 已经有值，检查是否存在重复的单号
          let orderArray = this.currentMaster.relationid.split(';');  // 将原来的单号字符串分割为数组
          if (!orderArray.includes(order.rp017)) {  // 如果不存在该单号
              // 拼接新单号，确保末尾有分号
              this.currentMaster.relationid = this.currentMaster.relationid + (this.currentMaster.relationid.endsWith(';') ? '' : ';') + order.rp017;
          }
      }
    })
    this.$refs.sysBugModals_ref.hide();
  },
  //查詢系統問題上報信息
  searchSysBugNoClick(){
    var self = this;
    var columns = [];
    for (let item of self.masterColumns) {
        // if (["", "inc_id"].indexOf(item.field) != -1) continue;
        columns.push(item);
    }
    var query = self
    .GetQueryExp(
        "SystemBugRpt_vueFrm_admrp_table",
        columns
    )
    query.then((query) => {
      var query_value = {}
      if (query.master != undefined)
        query_value["attach_query"] = JSON.stringify(query.master);
        self.admrpParamsFun = function () {
            return query_value;
        };
        self.$nextTick(function () {
            self.$refs.admrp_table.datatable.column(0).search("").draw();
        });
    });
  },
  //打開彈窗查詢系統問題上報單號
  searchSysBugNoModal(){
    if(this.masterState == 0) return //不為新增和修改狀態時退出
    // 取消所有行勾選框的勾選狀態
    $('#DataTables_Table_15_wrapper .dataTables_scrollBody').find('input.select-flag[type="checkbox"]').prop('checked', false);
    $('#DataTables_Table_15_wrapper .dataTables_scrollHead table tr th').eq(0).find('input:checkbox').prop('checked', false); //移除明細表格勾選信息
    $('.selected-row-info').text(''); //移除明細選擇顯示信息
    this.admrpParamsFun = undefined;
    this.$nextTick(function () {
      this.$refs.admrp_table.getSelectedInfo(); //刷新單頭勾選狀態
      this.$refs.admrp_table.datatable.column(0).search("").draw();
    })
    this.$refs.sysBugModals_ref.width("70%");
    this.$refs.sysBugModals_ref.show();
  },
  //刪除流程圖
  deleteFlowChart(){
    axios.post(`/systembugrpt/flowchart/delete`,this.objectToFormData(this.flowChart)).then((response) => {
      this.getflowchart(this.currentMaster.inc_id); //獲取流程圖列表
    })
    .catch((error) => {
      console.log(error);
    });
  },
  //設置彈出框不會點擊空白處關閉
  setModelBackdrop(ref){
    this.$refs[ref].show = function() { 
    $(this.$refs.modal).modal({
      backdrop: 'static', // 防止點擊背景關閉
      keyboard: false // 禁用 Esc 關閉
    });
  };
  },
  //保存流程圖
  flowChartSave(){
    return new Promise((resolve, reject) => {
      if(this.flowChart.flowchartno.trim() == '' || this.flowChart.charttype == ''){
        this.showMessage(this.$t('The required field cannot be empty!')); //必填項不能為空!
        reject(false);
        return 
      }
      if(this.flowChartState == '1'){//新增時檢測流程圖是否已在列表中存在
        var dataArray = this.$refs.flowChartTable.datatable.rows().data().toArray(); //獲取流程圖列表
        // 檢查 flowchartno 是否已存在
        const isExisting = dataArray.some(item => item.flowchartno === this.flowChart.flowchartno.trim());
        if (isExisting) {
          this.showMessage("This flowchart already exists!"); //對應的流程圖已存在
          reject(false);
          return;
        }
      }
      if(this.flowChartState == '1'){ //新增
        axios
          .post(`/systembugrpt/flowchart/create`, this.objectToFormData(this.flowChart))
          .then(response => {
            if(response.data.inc_id != undefined){
              this.flowChart.inc_id = response.data.inc_id;
              this.getflowchart(this.currentMaster.inc_id); //獲取流程圖列表
            }
          })
          .catch(error => {
            console.log(error);
          });
      }else{ //修改
        axios
          .post(
            `/systembugrpt/flowchart/update`,
            this.objectToFormData(this.flowChart))
          .then(response => {
            if(response.data.inc_id != undefined){
              this.getflowchart(this.currentMaster.inc_id); //獲取流程圖列表
            }
          })
          .catch(error => {
            console.log(error);
          });
      }
      this.$refs.flowChart_modalForm.$refs.modal.hide(); //關閉視窗
    });
  },
  //流程圖字段變更事件
  flowchartnoChange(val){
    if(val == ''){
      this.flowChart.description = ''
      return
    } 
    axios.get(`/systembugrpt/get_flowChartInfo`,{params:{id:val}}).then(response =>{ //根據流程圖編號獲取名稱
      this.flowChart.description = response.data.data;
    })
    .catch(error =>{
      console.log(error);
    })
  },
  //打開編輯彈窗 type == '1':操作為新增, type == '2':操作為修改
  show_flowChartModel(type){
    if(this.masterState != 2) return //不為修改狀態時退出
    if(type == '1'){
      this.flowChartModal_title = this.$t('Add Flowchart');
      this.flowChart = {};
      this.flowChart.flowchartno = '';
      this.flowChart.charttype = '';
      this.flowChart.description = '';
      this.flowChart.admrpid = this.currentMaster.inc_id;
      this.flowChartState = '1';
    }else{
      this.flowChartModal_title = this.$t('Edit Flowchart');
      this.flowChart.admrpid = this.currentMaster.inc_id;
      this.flowChartState = '2';
    }
    this.$refs.flowChart_modalForm.$refs.modal.width("500px");
    this.$refs.flowChart_modalForm.$refs.modal.show();
  },
  //流程圖列表點擊事件
  flowChart_row_click(e, data) {
    if(data == undefined) return
    this.flowChart = data;
    
    // 確認點擊的元素是按鈕或包含在按鈕內的圖標 <i>
    const buttonElement = e.target.closest("button");
    if (!buttonElement) return;

    // 獲取 <i> 標籤內的 class，用於判斷按鈕功能
    const iconElement = buttonElement.querySelector("i");
    if (!iconElement) return;

    const iconClassList = iconElement.className.split(" ");
    if (iconClassList.includes("fa-eye")){ //查看流程圖
      if(data.charttype ==='url'){
        window.open(data.flowchartno,'blank');//类型为 URL，直接跳转
      }else{
        window.open(
          `http://${window.location.host}/zh-hans/flowchart/preview_diagram?hidetm=true#/?flowChartNo=${data.flowchartno}`,
          "_blank"
        ); //類型為flowchart, 跳轉到預覽頁面
      }
    }else if(iconClassList.includes("fa-edit")) { //修改流程圖
      this.show_flowChartModel('2')
    } else { //刪除流程圖
      if(this.masterState != 2) return //不為修改狀態時退出
      let flag = confirm(this.$t("Are you sure you want to delete it")); 
      if (flag) { //給用戶確認操作
        this.deleteFlowChart();
      }
    }
  },
  //獲取系統問題上報流程圖信息
  getflowchart(admrpid){
    axios.get(`/systembugrpt/get_flowchart`,{params:{admrpid:admrpid}}).then(response =>{
      if(response.data.status){
        this.$refs.flowChartTable.datatable.clear().rows.add(response.data.data).draw();
      }else{
        this.$refs.flowChartTable.datatable.clear().rows.add([]).draw();
      }
    })
    .catch(error =>{
      console.log(error);
    })
  },
  //獲取問題類別(Problem Category)數據源
  getProblemCategoryData() {
    var _this = this;
    axios.get('/systembugrpt/get_problemcategory').then(res => {
      if (res.data.status) {
        var data = res.data.data;
        data = ['', ...data];
        $('select.select2-problemcategory[name="problemcategory"]').select2({ tags: true, data: data }).on("select2:select", function (e) {
          _this.currentMaster.problemcategory = e.params.data.text;
        });
      }
    })
  },
  // 選擇 solutionType 點擊事件
  solutionTypeClick() {
      const dataArray = this.$refs.solutionTypeTable.getSelectedFlagData()["datas"];
      if (dataArray.length === 0) return this.showMessage(this.$t('Unselected data')); //沒有選擇數據

      // 將當前頁面的 solutiontype 內容轉換為列表，處理 solutiontype 為 null 或 '' 的情況
      const currentSolutionList = (this.currentMaster.solutiontype || '')
          .split('\n')
          .map(line => line.replace(/^\d+\.\s*/, '').trim())  // 移除編號部分並去除多餘空白
          .filter(line => line !== '');  // 過濾掉空行

      // 過濾出新選中的數據中不重複的項目
      const newItems = dataArray
          .map(item => item.remark ? item.remark.trim() : '') // 去除新選項的空白
          .filter(item => item && !currentSolutionList.includes(item)); // 過濾掉 null 和空字符串

      // 如果沒有新項目，直接關閉彈窗
      if (newItems.length === 0) {
          this.$refs.solutiontypeModals_ref.hide();
          return;
      }

      // 合併現有的和新添加的項目，並清除空白行
      const combinedItems = [...currentSolutionList, ...newItems].filter(item => item !== '');

      // 對合併後的項目重新編號
      const updatedSolutionType = combinedItems
          .map((item, index) => `${index + 1}. ${item}`) // 重新編號
          .join('\n');

      // 更新 solutiontype 字段
      this.currentMaster.solutiontype = updatedSolutionType;
      this.$refs.solutiontypeModals_ref.hide();
  },
  //打開SolutionType選擇彈窗
  showSolutionTypeModel(){
    if(this.masterState == 0) return //不為新增和修改狀態時退出

    // 取消所有行勾選框的勾選狀態
    $('#DataTables_Table_14_wrapper .dataTables_scrollBody')
      .find('input.select-flag[type="checkbox"]')
      .prop('checked', false);

    $('#DataTables_Table_14_wrapper .dataTables_scrollHead table tr th').eq(0).find('input:checkbox').prop('checked', false); //移除明細表格勾選信息
    $('.selected-row-info').text(''); //移除明細選擇顯示信息
    this.$nextTick(function () {
      this.$refs.solutionTypeTable.getSelectedInfo(); //刷新單頭勾選狀態
    })
    this.$refs.solutiontypeModals_ref.width("700px");
    this.$refs.solutiontypeModals_ref.show();
  },
  //刷新按鈕點擊事件
  refresh_info(){
    if(String(this.currentMaster.inc_id || "") != ""){
      this.getMasterInfo(this.currentMaster.inc_id,'');
    }
  },
  //用戶上傳圖片已存在時提示用戶:文件已存在
  duplicate_file_detected(){
    this.showMessage(this.$t("File already exists"));
  },
  //預覽文件
  previewFile(inc_id){
    const url = `/systembugrpt/preview_file?inc_id=${inc_id}`;
    window.open(url, '_blank');  // 在新标签页中打开
  },
  //獲取系統問題上報窗口URL路徑上攜帶的參數
  get_fetchUrlParams(){
    var url_string = window.location.href;  //頁面的URL
    const url = new URL(url_string);
    // const searchParams = new URLSearchParams(url.hash.substring(url.hash.indexOf('?')));
    const searchParams = new URLSearchParams(url.search);  // 使用 search 而不是 hash
    const inc_id = searchParams.get('inc_id');//獲取系統問題上報主鍵
    const rp017 = searchParams.get('rp017');//系統問題上報單號
    if(inc_id != null && inc_id != undefined){
      this.$refs.Admrp_details.click();
      this.getMasterInfo(inc_id,'');
    }
    if(rp017 != null && rp017 != undefined){
      this.$refs.Admrp_details.click();
      this.getMasterInfo('',rp017);
    }
  },
  showMessage(msg){
    $('#msg').html(msg);
    $('#messageModal').modal('show'); 
  },
  get_lang_code() {
    if($("#curr_language_code").val() !== "en") {
      this.lang_code_en = false;
    }
  },
  masterSearch(){
    var self = this;
    var columns = [];
    for (let item of self.masterColumns) {
        // if (["", "inc_id"].indexOf(item.field) != -1) continue;
        columns.push(item);
    }
    var query = self
    .GetQueryExp(
        "SystemBugRpt_vueFrm_AdmrpTable",
        columns
    )
    query.then((query) => {
        var query_value = {}
        if (query.master != undefined)
            query_value["attach_query"] = JSON.stringify(query.master);
            self.masterParamsFun = function () {
                return query_value;
            };
            self.$nextTick(function () {
                self.$refs.AdmrpTable.datatable.column(0).search("").draw();
            });
    });
  }, 
  //刪除系統問題上報附件信息
  admrqDelete(id){
    let flag = confirm(this.$t("Are you sure you want to delete it"));
    if (flag) {
      this.fileArray_left.splice(id, 1);
    }
  },
  //刪除系統問題上報附件信息(右)
  admrqRightDelete(id){
    let flag = confirm(this.$t("Are you sure you want to delete it"));
    if (flag) {
      this.fileArray_right.splice(id, 1);
    }
  },

  //查詢關聯任務進度
  getTaskItemTable(){
    this.$refs.taskItemTable.filter_column_params_fun = undefined;
    this.taskItemParamsFun = () => {
      return { taskno: this.currentMaster.rp024};
    };
    this.refresh_Table("taskItemTable");
  },
  //讀取關聯任務信息(打開彈窗)
  showReadRelationTaskModel(){
    if(String(this.currentMaster.rp024 || "") == "") return
    axios.get(`/systembugrpt/get_taskrelation`,{params:{rp024:this.currentMaster.rp024}}).then(response =>{
      if(response.data.status){
        this.$nextTick(function () {
          this.$refs.AssociatedTaskTable.datatable.clear().rows.add(response.data.data).draw();
        })
        // this.$refs.associatedTaskModals_ref.width("70%");
        this.$refs.associatedTaskModals_ref.show();
      }else{
        this.showMessage(response.data.msg);
      }
    })
    .catch(error =>{
      console.log(error);
    })
  },
  //查詢關聯任務進度
  getTaskProgressTable(){
    this.$refs.TaskProgressTable.filter_column_params_fun = undefined;
    this.taskProgressParamsFun = () => {
      return { rp024: this.currentMaster.rp024};
    };
    this.refresh_Table("TaskProgressTable");
  },
  //安排Task保存事件
  arrangeTaskSave(){
    if(typeof this.currentTask.contact != 'string' || this.currentTask.contact == ''){
      this.currentTask.contact = this.username; //任务联系人为空时,默认设置当前用户为联系人
    }
    axios.post(`/systembugrpt/task/create`,this.objectToFormData(this.currentTask)).then(response =>{
      if(response.status != 200){
        return this.showMessage(this.$t('the new failure')); //新增失敗
      } 
      this.currentMaster.rp023 = this.currentTask.projectname; //问题所属项目
      this.currentMaster.rp031 = this.currentTask.planbdate; //计划开始
      this.currentMaster.rp032 = this.currentTask.planedate; //计划结束
      this.currentMaster.rp024 = this.currentTask.pid + '-' + this.currentTask.tid + '-' +this.currentTask.taskid; //关联TaskID
      this.masterState = 2;
      this.saveMaster(); //修改系统问题上报信息
    })
    .catch(error =>{
      console.log(error);
    })
  },
  //选择窗口名称并关闭弹框
  modulesClick(){
    if(this.currentTamp.rp022 == undefined) return this.showMessage(this.$t('Unselected data'));
    this.currentTask.udf04 = this.currentTamp.rp022;
    this.$refs.moduleModals_ref.hide();
  },
  //选择窗口名称(打开弹框)
  showModuleModals(){
    this.currentTamp = {};
    this.currentTamp.state = '2';
    this.getModuleArray('2');
    this.$refs.moduleModals_ref.width("900px");
    this.$refs.moduleModals_ref.show();
  },
  //弹框选中联系人
  setUserClick(){
    if(this.currentTamp.username == undefined) return this.showMessage(this.$t('Unselected data')); //沒有選擇數據
    this.currentTask.contact = this.currentTamp.username;
    this.$refs.userModal_ref.hide();
  },
  //联系人列表单击事件
  user_row_click(event,data){
    this.currentTamp.username = data.username;
  },
  //選擇聯繫人(打开弹框)
  showUsersModel(){
    $('.input-group-append').hide() //隱藏高級查詢
    this.currentTamp.username = undefined;
    this.$refs.userModal_ref.width("500px");
    this.$refs.userModal_ref.show();
  },
  //查詢窗體所屬工程
  async getDefaultProClick(){
    await axios.get(`/systembugrpt/get_defaultpro`,{params:{formname:this.currentTask.udf04}}).then(response =>{
      if(response.data.sc008 == '') return this.showMessage("窗體["+this.currentTask.udf04+"]沒有設置默認工程");
      this.currentTask.pid = response.data.sc008;
      this.currentTask.tid = response.data.sc005;
      this.checkPidExist(); //檢驗Pid是否合法
      this.checkTidExist(); //检验Tid是否合法
    })
    .catch(error =>{
      console.log(error);
    })
  },
  //設置用戶默認工程提交方法
  async setDefaultProjectSave(){
    if(typeof this.ut002 != 'string' || this.ut002 == '') return this.showMessage(this.$t('SystemBugRpt_multi_language_2')); //工程編號不能為空 SystemBugRpt_multi_language_2
    if(typeof this.ut003 != 'string' || this.ut003 == '') return this.showMessage(this.$t('SystemBugRpt_multi_language_3')); //工程類別不能為空 SystemBugRpt_multi_language_3
    await axios.get(`/systembugrpt/pmsut_save`,{params:{ut001:this.username,ut002:this.ut002,ut003:this.ut003}}).then(response =>{
      if(!response.data.status) return this.showMessage(this.$t('SystemBugRpt_multi_language_4')); //設置默認工程失敗 SystemBugRpt_multi_language_4
      //設置成功後賦值
      this.currentTask.pid = this.ut002;
      this.currentTask.tid = this.ut003;
      this.checkPidExist(); //检验Pid是否合法
      this.checkTidExist(); //检验Tid是否合法
      this.showMessage(this.$t('SystemBugRpt_multi_language_5')); // 設置默認工程失敗 Setting the default project succeeded
    })
    .catch(error =>{
      console.log(error);
    })
  },
  //選中tid並關閉彈框
  setTidClick(){
    if(this.currentTamp.ut003 == undefined) return this.showMessage(this.$t('Unselected data')); //沒有選擇數據
    if(this.currentTamp.state == '1'){
      this.ut003 = this.currentTamp.ut003;
    }else{
      this.currentTask.tid = this.currentTamp.ut003;
      this.getTaskID(this.currentTask.pid,this.currentTask.tid);
    }
    this.$refs.tidModal_ref.hide();
  },
  //工程類別列表單擊事件
  tid_row_click(event,data){
    this.currentTamp.ut003 = data.tid;
  },
  //打開工程類別(TID)彈框列表
  showTidModel(type){
    this.currentTamp.state = type;
    if(type == '1'){
      if(typeof this.ut002 != 'string' || this.ut002 == '') return this.showMessage(this.$t('SystemBugRpt_multi_language_2')); //工程編號不能為空
    }else{
      if(typeof this.currentTask.pid != 'string' || this.currentTask.pid == '') return this.showMessage(this.$t('SystemBugRpt_multi_language_2')); //工程編號不能為空
    }
    $('.input-group-append').hide() //隱藏高級查詢
    this.currentTamp.ut003 = undefined;
    this.$refs.projectTidTable_ref.filter_column_params_fun = undefined;
    var args = type=='1' ? this.ut002 : this.currentTask.pid; //从不同地方打开窗体需要按对应地方的参数查询
    this.tid_params_fun = () => {
      return {pid:args};
    };
    this.refresh_Table("projectTidTable_ref");
    this.$refs.tidModal_ref.width("700px");
    this.$refs.tidModal_ref.show();
  },
  //選中pid並關閉彈框
  setPidClick(){
    if(this.currentTamp.ut002 == undefined) return this.showMessage(this.$t('Unselected data')); //沒有選擇數據
    if(this.currentTamp.state == '1'){ //状态标识对象,有两个地方用的同一个弹框,值为1时表示是从设置默认对象窗口打开窗体,值为2时表示是在添加任务信息时打开窗体
      this.ut002 = this.currentTamp.ut002;
    }else{
      this.currentTask.pid = this.currentTamp.ut002;
      this.checkPidExist();
    }
    this.$refs.pidModal_ref.hide();
  },
  //工程列表單擊事件
  pid_row_click(event,data){
    this.currentTamp.ut002 = data.pid;
  },
  //打開工程(PID)列表彈框
  showPidModel(type){
    $('.input-group-append').hide() //隱藏高級查詢
    this.currentTamp.state = type;
    this.currentTamp.ut002 = undefined;
    this.$refs.projectPidTable_ref.filter_column_params_fun = undefined;
    this.pid_params_fun = () => {
      return {username: this.username};
    };
    this.refresh_Table("projectPidTable_ref");
    this.$refs.pidModal_ref.width("700px");
    this.$refs.pidModal_ref.show();
  },
  //檢驗任務類別編號準確性
  async checkTidExist(){
    if(this.currentTask.pid == '') return
    await axios.get(`/systembugrpt/checktidexist`,{params:{pid:this.currentTask.pid,tid:this.currentTask.tid}}).then(response =>{ //返回sdesp字段值
      if(response.data.data == ''){
        this.currentTask.tid = "";
        this.currentTask.taskid = "";
        this.currentTask.tasklistdesp = "";
        return this.showMessage(this.currentTask.pid+"工程"+this.currentTask.tid+"類別不存在");
      }
      this.currentTask.tasklistdesp = response.data.data;
    })
    .catch(error =>{
      console.log(error);
    })
  },
  //獲取TaskID
  async getTaskID(pid,tid){
    if(pid == '' || tid == '') return
    this.checkTidExist();
    await axios.get(`/systembugrpt/gettaskno`,{params:{pid:pid,tid:tid}}).then(response =>{
      if(!response.data.status) return this.showMessage(this.$t('SystemBugRpt_multi_language_6')); //获取TaskID失败 SystemBugRpt_multi_language_6
      this.currentTask.taskid = response.data.taskid;
      this.currentTask.taskno= response.data.taskno;
    })
    .catch(error =>{
      console.log(error);
    })
  },
  //檢驗PID數據是否合法(同時獲取TaskNo)
  async checkPidExist(){
    if(this.currentTask.pid == '') return
    await axios.get(`/systembugrpt/checkpidexist`,{params:{pid:this.currentTask.pid}}).then(response =>{
      if(response.data.data == ''){
        this.currentTask.projectname = '';
        return this.showMessage("工程編號"+this.currentTask.pid+"不存在"); //pid does not exist
      }
      this.currentTask.projectname = response.data.data; //獲取pname 
      if(this.currentTask.tid != ''){
        this.getTaskID(this.currentTask.pid,this.currentTask.tid);
      }
    })
    .catch(error =>{
      console.log(error);
    })
  },
  //用戶默認工程選項點擊事件(根據用戶名讀取默认工程)
  userDefaultProjectClick(){
    axios.get(`/systembugrpt/get_userdefaultproject`,{params:{ut001:this.username}}).then(response =>{
      if(response.data.msg != "") return this.showMessage(this.$t('SystemBugRpt_multi_language_7')); //SystemBugRpt_multi_language_7 用戶沒有設置默認工程
      this.ut002 = response.data.data.ut002;
      this.ut003 = response.data.data.ut003;
      this.currentTask.pid = this.ut002;
      this.currentTask.tid = this.ut003;
      this.checkPidExist(); //檢驗Pid是否合法
      this.checkTidExist(); //检验Tid是否合法
    })
    .catch(error =>{
      console.log(error);
    })
  },

  //設置默認工程按鈕點擊事件
  setDefaultProjectClick(){
    this.userDefaultProjectClick();
  },
  
  //查看問題記錄(参数:窗体名称:udf04)
  showTaskTableClick(){
    this.$refs.systemBugRpt_taskTable_ref.filter_column_params_fun = undefined;
    this.task_params_fun = () => {
      return { udf04: this.currentTask.udf04};
    };
    this.refresh_Table("systemBugRpt_taskTable_ref");
  },
  //计划开始日期和结束日期字段变更事件,日期值改变时检验数据是否合法,自动算出计划天数
  taskDateChange(){
    var bdate = this.$moment(this.currentTask.planbdate).format("YYYYMMDD");
    var edate = this.$moment(this.currentTask.planedate).format("YYYYMMDD");
    // if(bdate == "Invalid date") return this.showMessage('计划开始日期不能为空'); //The schedule start date cannot be empty
    if(bdate == 'Invalid date' || edate == 'Invalid date') return
    if(bdate > edate) return this.showMessage(this.$t('SystemBugRpt_multi_language_8')) //SystemBugRpt_multi_language_8 计划完成日期不能小于计划开始日期
    if(bdate == edate){
      this.currentTask.etime = 1;
    }else{
      this.currentTask.etime = Number(edate) - Number(bdate); //计划天数 = 计划结束日期 - 计划开始日期
    }
  },
  //安排任務彈框打開方法
  showArrangeTaskModel(){
    if(this.currentMaster.inc_id == undefined) return this.showMessage(this.$t('Unselected data')); //沒有選擇數據
    this.Modal_title = this.$t('ArrangeTask'); //安排任務 ArrangeTask
    this.currentTask = {};
    this.currentTask.udf04 = 'SystemBugRpt_Frm'; //默认窗口为系统问题上报窗口
    this.currentTask.progress = 'N';//任务进度
    this.currentTask.task = this.currentMaster.rp005;//问题描述
    this.currentTask.udf09 = this.currentMaster.rp004; //上报人
    this.currentTask.udf01 = this.currentMaster.rp017; //问题单号
    this.currentTask.planbdate = this.$moment(new Date()).format("YYYY-MM-DD");;//计划开始
    this.currentTask.planedate = this.$moment(new Date()).format("YYYY-MM-DD");;//计划结束
    this.currentTask.etime = 1; //计划天数
    if(this.currentMaster.rp033==888 || this.currentMaster.rp033==8){
      this.currentTask.priority = this.currentMaster.rp033; //优先级
    };
    this.getDefaultProClick();
    this.$refs.taskSimpleSetup_ref.click();
    this.$refs.arrangeTask_modalForm.$refs.modal.width("1300px");
    this.$refs.arrangeTask_modalForm.$refs.modal.show();
  },
  //轉交問題提交方法
  deliverDeptSave(){
    var date = this.$moment(new Date()).format("YYYY-MM-DD hh:mm");
    var remark = this.currentMaster.rp014;
    this.currentMaster.rp009 = this.deptNo; //轉交部門
    this.currentMaster.rp010 = '';
    this.currentMaster.rp015 = 'Y'; //提交給其它部門,默認為'N'
    var deptName = '';
    for(item of this.cmsmeArray){
      if(this.deptNo == item.me001){ //根據部門編號獲取部門名稱
        deptName = item.me002; 
      }
    }
    if(typeof remark == 'string' && remark != ''){ 
      this.currentMaster.rp014 = '---'+date+' 轉交到'+deptName+'處理---'+remark
    }else{
      this.currentMaster.rp014 = '---'+date+' 轉交到'+deptName+'處理---'
    }
    this.masterState = 2;
    this.saveMaster();
  },
  //轉交問題
  transferProblem(){
    if(this.currentMaster.inc_id == undefined) return this.showMessage(this.$t('Unselected data')); //沒有選擇數據
    this.deptNo = '';
    this.Modal_title = this.$t('SystemBugRpt_multi_language_9'); //選擇轉交部門 SystemBugRpt_multi_language_9
    this.$refs.deliverDept_modalForm.$refs.modal.width("300px");
    this.$refs.deliverDept_modalForm.$refs.modal.show();
  },
  //結束問題
  terminateProblem(){
    if(this.currentMaster.inc_id == undefined) return this.showMessage(this.$t('Unselected data')); //沒有選擇數據
    if(this.currentMaster.rp004 != this.username) return this.showMessage(this.$t('SystemBugRpt_multi_language_10')); //只有問題上報者才能結束 SystemBugRpt_multi_language_10
    if(this.currentMaster.rp011 == "F") return this.showMessage(this.$t('SystemBugRpt_multi_language_11')); //該問題已結束 SystemBugRpt_multi_language_11
    if(typeof this.currentMaster.rp010 != 'string' || this.currentMaster.rp010 == '') return this.showMessage(this.$t('SystemBugRpt_multi_language_12')) //跟進人不能為空 SystemBugRpt_multi_language_12
    if(typeof this.currentMaster.rp009 != 'string' || this.currentMaster.rp009 == '') return this.showMessage(this.$t('SystemBugRpt_multi_language_13')) //跟進部門不能為空 SystemBugRpt_multi_language_13
    if(typeof this.currentMaster.rp031 != 'string' || this.currentMaster.rp031 == '' || typeof this.currentMaster.rp032 != 'string'|| this.currentMaster.rp032 == '') return this.showMessage(this.$t('SystemBugRpt_multi_language_14')) //計劃開始日期和計劃結束日期不能為空 SystemBugRpt_multi_language_14
    if(typeof this.currentMaster.rp012 != 'string' || typeof this.currentMaster.rp013 != 'string'){
      this.currentMaster.rp012 = this.currentMaster.rp031; //默認為計劃開始日期 
      this.currentMaster.rp013 = this.currentMaster.rp032; //默認為計劃結束日期
    }
    var rp012 = this.$moment(this.currentMaster.rp012).format("YYYYMMDD");
    var rp013 = this.$moment(this.currentMaster.rp013).format("YYYYMMDD");
    if(rp013 < rp012) return this.this.showMessage(this.$t('SystemBugRpt_multi_language_15')); //實際完成日期不能小於實際開始日期 SystemBugRpt_multi_language_15
    this.masterState = 2;
    this.currentMaster.rp011 = 'F'; //更改狀態為F
    this.saveMaster();
  },
  //系統問題上報功能列表單擊事件
  admrf_row_click(event,data){
    this.currentAdmrf = data;
  },
  //刪除系統問題上報功能信息
  deleteAdmrf(){
    if (this.currentAdmrf.inc_id == undefined) return this.showMessage(this.$t("Please select the information you want to delete")); //請選擇要刪除的信息
    let flag = confirm(this.$t("Are you sure you want to delete it"));
    if (flag) {
      axios.post(`/systembugrpt/admrf/delete`,this.objectToFormData(this.currentAdmrf)).then((response) => {
        if (response.status) {
          this.currentAdmrf = {};
          this.$refs.AdmrfTable.datatable.search("").draw();
          return this.showMessage(this.$t("deleted successfully")); //刪除成功
        }
        return this.showMessage(this.$t("deleted failed")); //刪除失敗
      })
      .catch((error) => {
        console.log(error);
      });
    }
  },
  //系統問題上報功能信息表單提交方法
  admrfSave(){
    if(this.currentAdmrf.inc_id == undefined){ //新增
      axios.post(`/systembugrpt/admrf/create`,this.objectToFormData(this.currentAdmrf)).then(response =>{
        if(response.data.inc_id){
          this.currentAdmrf.inc_id = response.data.inc_id;
          this.$refs.AdmrfTable.datatable.search("").draw();
          return this.showMessage(this.$t('new success')); //新增成功
        }
          return this.showMessage(this.$t('the new failure')); //新增失敗
      })
      .catch(error =>{
        console.log(error);
      })
    }else{ //修改
      axios.post(`/systembugrpt/admrf/update`,this.objectToFormData(this.currentAdmrf))
      .then((response) => {
        if(response.status == 200){
          this.$refs.AdmrfTable.datatable.search("").draw();
          return this.showMessage(this.$t("change successfully"));
        }
        return this.showMessage(this.$t("change failed"));
      })
      .catch((error) => {
        console.log(error);
      });
    }
  },
  //修改系統問題上報功能信息
  updateAdmrf(){
    if(this.currentAdmrf.inc_id == undefined) return this.showMessage(this.$t('Select the data you want to modify'));//选择要修改的数据
    this.Modal_title = this.$t('SystemBugRpt_multi_language_16'); //修改功能信息 SystemBugRpt_multi_language_16
    this.$refs.admrf_modalForm.$refs.modal.width("300px");
    this.$refs.admrf_modalForm.$refs.modal.show();
  },
  //新增系統問題上報功能列表時獲取序號
  getAdmrfNo(){
    axios.get(`/systembugrpt/get_admrfno`,{params:{rf002:this.currentMaster.rp017}}).then(response =>{
      this.currentAdmrf.rf003 = response.data.data;
      console.log(this.currentAdmrf.rf003);
    })
    .catch(error =>{
      console.log(error);
    })
  },
  //新增系統問題上報功能信息
  addAdmrf(){
    this.Modal_title = this.$t("SystemBugRpt_multi_language_17"); //新增功能信息 SystemBugRpt_multi_language_17
    this.currentAdmrf = {},
    this.currentAdmrf.rf002 = this.currentMaster.rp017;
    this.getAdmrfNo();
    this.$refs.admrf_modalForm.$refs.modal.width("300px");
    this.$refs.admrf_modalForm.$refs.modal.show();
  },
  //刷新DataTable列表信息
  refresh_Table(table) {
    let self = this;
    this.$nextTick(function () {
      self.$refs[table].datatable.search("").draw();
    });
  },
  //根據單別單號獲取功能列表
  getAdmrfArray(){
    this.$refs.AdmrfTable.filter_column_params_fun = undefined;
    this.admrfParamsFun = () => {
      return { rf002:this.currentMaster.rp017};
    };
    this.refresh_Table("AdmrfTable");
  },
  //快速設計用戶界面 
  designPageChange(files,files_base64){
    if(files.length > 4) return this.showMessage(this.$t('SystemBugRpt_multi_language_18')); //SystemBugRpt_multi_language_18 上傳失敗,只能上傳4張圖片
    if(this.masterState == 2){ //只有處於修改狀態才會執行
      var args = {};
      args.rq002 = this.currentMaster.rp017; //單號
      args.rq007 = 'RI'; //類型
      var index = 1;
      for(item of files){
        args[`img${index}`] = item
        index++
      }
      this.uploadImgArray(args);
    }
  },
  //添加流程圖
  flowChartChange(files,files_base64){
    if(files.length > 4) return this.showMessage(this.$t('SystemBugRpt_multi_language_18')); //SystemBugRpt_multi_language_18 上傳失敗,只能上傳4張圖片
    if(this.masterState == 2){ //只有處於修改狀態才會執行
      var args = {};
      args.rq002 = this.currentMaster.rp017; //單號
      args.rq007 = 'RR'; //類型
      var index = 1;
      for(item of files){
        args[`img${index}`] = item
        index++
      }
      this.uploadImgArray(args);
    }
  },
  //上傳多張圖片通用請求方法(多張)
  uploadImgArray(args){
    axios.post(`/systembugrpt/upload_imgarray`,this.objectToFormData(args)).then(response =>{
      if(response.data.status){
        return this.showMessage(this.$t('upload successful')); //上傳成功
      }
      return this.showMessage(this.$t('fail to upload')); //上傳失敗
    })  
    .catch(error =>{
      console.log(error);
    })
  },
  //上傳應用流程圖 rq008 I
  appFlowChartChange(files,files_base64){
    if(files.length > 4) return this.showMessage(this.$t('SystemBugRpt_multi_language_18')); //SystemBugRpt_multi_language_18 上傳失敗,只能上傳4張圖片
    if(this.masterState == 2){ //只有處於修改狀態才會執行
      var args = {};
      args.rq002 = this.currentMaster.rp017; //單號
      args.rq007 = 'I'; //類型
      var index = 1
      for(item of files){
        args[`img${index}`] = item
        index++
      }
      this.uploadImgArray(args);
    }
  },
  //獲取圖片(多張)
  getUserPageImg(args,ref){
    axios.get(`/systembugrpt/get_imgarray`,{params:args}).then(response =>{
      this.$refs[ref].loadImage(response.data.data);
      if(ref == 'admrp_img_ref'){
        this.bugImgArray = this.$refs.admrp_img_ref.files;
      }
      // console.log(response.data.data);
    })
    .catch(error =>{
      console.log(error);
    })
  },

  //用戶界面圖片控件Change事件
  userPageImgChange(files,files_base64){
    if(files.length > 4) return this.showMessage(this.$t('SystemBugRpt_multi_language_18')); //SystemBugRpt_multi_language_18 上傳失敗,只能上傳4張圖片
    if(this.masterState == 2){ //只有處於修改狀態才會執行
      var args = {};
      args.rq002 = this.currentMaster.rp017; //單號
      args.rq007 = 'LI'; //類型
      var index = 1
      for(item of files){
        args[`img${index}`] = item
        index++
      }
      this.uploadImgArray(args);
    }
  },

  // 添加附件
  uploadFile(event, type) {
    const files = event.target.files;
    if (!files.length) return;

    // 遍歷所有選擇的文件
    Array.from(files).forEach(file => {
      let fileArray = type === 'F' ? this.fileArray_left : this.fileArray_right;

      // 检查文件名长度
      if (file.name.length > 150) {
          this.showMessage(this.$t("File name is too long. Max 150 characters")); //文件名过长。最多150个字符
          return; // 终止这个文件的处理
      }

      // 检查是否选择了相同的文件
      const fileExists = fileArray.some(item => item.rq005 === file.name);
      if (fileExists) {
        this.showMessage(this.$t("File already exists")); // 文件已存在
      } else {
        let newFile = {
          rq002: this.currentMaster.rp017, // 單號
          rq005: file.name, // 文件名
          rq006: file, // 文件內容
          rq007: type // 類型
        };

        fileArray.push(newFile);
      }
    });

    // 重置input，以确保下次相同文件选择时触发change事件
    event.target.value = '';
  },

  //選擇功能依賴對象
  moduleObjectClick(){
    if(this.currentTamp.rp028 == undefined) return this.showMessage(this.$t('Unselected data'));
    this.currentMaster.rp028 = this.currentTamp.rp028;
    this.$refs.moduleObjectModal_ref.hide();
  },
  //功能依賴對象列表單擊事件
  moduleObject_row_click(event,data){
    this.currentTamp.rp028 = data.objectname;
  },
  //查詢功能依賴對象列表
  getModuleObjectArray(){
    axios.get(`/systembugrpt/moduleobject_array`,{params:{moduleid:this.currentMaster.rp022}}).then(response =>{
      this.$refs.ModuleObjectTable.datatable.clear().rows.add(response.data.data).draw();
    })
    .catch(error =>{
      console.log(error);
    })
  },
  //用戶選擇功能依賴對象(打開彈框)
  showModuleObjectModal(){
    this.currentTamp = {};
    this.getModuleObjectArray();
    this.$refs.moduleObjectModal_ref.width("900px");
    this.$refs.moduleObjectModal_ref.show();
  },
  //選擇窗體名稱
  moduleClick(){
    if(this.currentTamp.rp022 == undefined) return this.showMessage(this.$t('Unselected data'));
    this.currentMaster.rp022 = this.currentTamp.rp022;
    this.$refs.moduleModal_ref.hide();
  },
  //窗體列表單擊事件
  module_row_click(event,data){
    this.currentTamp.rp022 = data.modulename;
  },
  //查詢窗體信息
  getModuleArray(type){
    var args = '';
    if(type == '1'){
      args = this.currentMaster.rp020;
    }
    axios.get(`/systembugrpt/module_array`,{params:{parentid:args}}).then(response =>{
      this.$refs.ModuleTable.datatable.clear().rows.add(response.data.data).draw();
    })
    .catch(error =>{
      console.log(error);
    })
  }, 
  //用戶選擇窗體名稱(打開彈框)
  showModuleModal(){
    this.currentTamp = {};
    this.currentTamp.state = '1';
    this.getModuleArray('1');
    this.$refs.moduleModal_ref.width("900px");
    this.$refs.moduleModal_ref.show();
  },
  //系統列表單擊事件 
  system_row_click(event,data){
    this.currentTamp.rp020 = data.sys;
  },
  //用戶選擇系統編號
  systemClick(){
    if(this.currentTamp.rp020 == undefined) return this.showMessage(this.$t('Unselected data'));
    this.currentMaster.rp020 = this.currentTamp.rp020;
    this.$refs.systemModal_ref.hide();
  },
  //用戶選擇系統名稱(打開彈框)
  showSystemModal(){
    this.currentTamp = {};
    this.$refs.systemModal_ref.width("900px");
    this.$refs.systemModal_ref.show();
  },
  //取消按鈕
  undoMaster(){
    this.currentMaster = this.cloneObject(this.currentMasterClone);
    this.setDateStr(this.currentMaster);
    this.$nextTick(function () {
      $('select.select2-type').trigger('change');
      $('select.select2-type2').trigger('change');
      $('select.select2-genjin').trigger('change');
      $('select.select2-genjin2').trigger('change');
      $('select.select2-problemcategory').trigger('change');
    });
    this.state = 0;
    this.masterState = 0;
    if(String(this.currentMaster.rp017 || "") != ""){
      this.getImgArray();
      this.getFileArray('F'); //獲取附件列表
      this.getFileArray('R'); //獲取附件列表(右)
      this.getflowchart(this.currentMaster.inc_id); //獲取流程圖列表
    }else{ //表示用戶在此之前沒有選擇過任何數據,直接進行新增
      this.fileArray_left = []; //清空附件列表
      this.fileArray_right = []; //清空附件列表
      this.$refs['userPageImg_ref'].loadImage([]);//清空用戶界面圖片
      this.$refs['appFlowChart_ref'].loadImage([]);//清空應用流程圖圖片
      this.$refs['flowChart_ref'].loadImage([]);//清空添加流程圖圖片
      this.$refs['designPage_ref'].loadImage([]);//清空快速設計用戶界面圖片
      this.$refs['admrp_img_ref'].loadImage([]);//清空系統問題上報圖片
    }
  },
  //修改系統問題上報信息
  updateMaster(){
    if(this.currentMaster.inc_id == undefined || this.currentMaster.inc_id == ''){
      this.$refs.buttonBar.setToolButtonState();
      return this.showMessage(this.$t('Select the data you want to modify'));//选择要修改的数据
    }
    if(this.currentMaster.rp011 == 'F'){
      this.$refs.buttonBar.setToolButtonState();
      return this.showMessage(this.$t('SystemBugRpt_multi_language_19'));//已結束問題不可修改 SystemBugRpt_multi_language_19
    }
    this.state = 1;
    if(this.currentMaster.rp004 != this.username){ //判斷當前修改者是否為上報者(只有問題上報者才可以修改附件和描述信息)
      this.state = 2;
    }
    this.masterState = 2;
    this.$refs.Admrp_details.click();
  },
  //獲取信息管理部界面對應圖片(多張)
  getImgArray(){
    var args = {rq002:this.currentMaster.rp017,rq007:"LI"}
    this.getUserPageImg(args,'userPageImg_ref');//獲取用戶界面圖片
    args.rq007 = "I";
    this.getUserPageImg(args,'appFlowChart_ref');//獲取應用流程圖圖片
    args.rq007 = "RR";
    this.getUserPageImg(args,'flowChart_ref');//獲取添加流程圖圖片
    args.rq007 = "RI";
    this.getUserPageImg(args,'designPage_ref');//獲取快速設計用戶界面圖片
    args.rq007 = "IMG";
    this.getUserPageImg(args,'admrp_img_ref');//獲取系統問題上報圖片
  },

  //單擊時獲取系統問題上報信息
  getMasterInfo(inc_id,rp017){
    axios.get(`/systembugrpt/admrp/get`,{params:{id:inc_id,rp017:rp017}}).then(response =>{
      if(response.data.status){
        this.currentMaster = response.data.data;
        this.currentMasterClone = this.cloneObject(this.currentMaster);
        this.getProblemCategoryData(); //重新獲取問題類別列表
        this.$nextTick(function () {
          $('select.select2-type').trigger('change');
          $('select.select2-type2').trigger('change');
          $('select.select2-genjin').trigger('change');
          $('select.select2-genjin2').trigger('change');
          $('select.select2-problemcategory').trigger('change');
        });

        this.setDateStr(this.currentMaster);
        // this.getAdmrqImg();//獲取相關圖片(單張)
        this.getImgArray();//獲取信息管理部界面對應圖片(多張)
        this.getAdmrfArray();//獲取功能列表
        this.getTaskProgressTable();//獲取關聯任務進度列表信息
        this.getTaskItemTable(); //獲取問題跟進狀態列表信息
        this.getFileArray('F'); //獲取附件列表
        this.getFileArray('R'); //獲取附件列表(右)
        this.getflowchart(this.currentMaster.inc_id); //獲取流程圖列表
      }else{
        console.log(response.data.msg);
        return this.showMessage(this.$t("Data query failure")); //查詢數據失敗
      }
    })
    .catch(error =>{
      console.log(error);
    })
  },
  //獲取附件列表
  getFileArray(type){
    axios.get(`/systembugrpt/get_systembugfile`,{params:{rq002:this.currentMaster.rp017,rq007:type}}).then(response =>{
      if(!response.data.status) return this.showMessage(this.$t('SystemBugRpt_multi_language_1')); //查詢附件信息失敗 SystemBugRpt_multi_language_1
      if(type == 'F'){
        this.fileArray_left = response.data.data;
      }else{
        this.fileArray_right = response.data.data;
      }
    })
    .catch(error =>{
      console.log(error);
    })
  },
  //系統問題上報列表雙擊事件
  master_db_click(data){
    if(data == undefined) return
    this.getMasterInfo(data.inc_id,'');
    this.$refs.Admrp_details.click();
  },
  //刪除系統問題上報信息
  deleteMaster(){
    if (this.currentMaster.inc_id == undefined) return this.showMessage(this.$t("Please select the information you want to delete")); //請選擇要刪除的信息
    let flag = confirm(this.$t("Are you sure you want to delete it"));
    if (flag) {
      axios.post(`/systembugrpt/admrp/delete`,this.objectToFormData(this.currentMaster)).then((response) => {
        if (response.status) {
          // this.getAdmrqImg();
          this.getImgArray();
          this.currentMaster = {};
          this.currentMasterClone = {};
          this.$nextTick(function () {
            this.$refs.AdmrpTable.datatable.search("").draw();
            $('select.select2-type').trigger('change');
            $('select.select2-type2').trigger('change');
            $('select.select2-genjin').trigger('change');
            $('select.select2-genjin2').trigger('change');
            $('select.select2-problemcategory').trigger('change');
          });
          this.fileArray_left = [];
          this.fileArray_right = [];
          this.$refs.flowChartTable.datatable.clear().rows.add([]).draw();
          return this.showMessage(this.$t("deleted successfully")); //刪除成功
        }
        return this.showMessage(this.$t("deleted failed")); //刪除失敗
      })
      .catch((error) => {
        console.log(error);
      });
    }
  },
  //把對象轉成FormData
  objectToFormData(obj){
    let fd = new FormData();
    for (let filedname in obj) {
      if(obj[filedname]!=null){   
        if (["rp012","rp013","rp031","rp032","planbdate","planedate"].indexOf(filedname) > -1) {
          obj[filedname] = this.$moment(obj[filedname]).format("YYYY-MM-DD");
          obj[filedname] = obj[filedname] + ' 00:00:00.000';
        }     
        fd.append(filedname, obj[filedname]); 
      }          
    }
    return fd;
  },
  //日期格式化
  setDateStr(data){
    if(typeof data.rp002 == 'string' && data.rp002 != ''){
      this.currentMaster.rp002 = data.rp002.slice(0,10);
    }
    if(typeof data.rp012 == 'string' && data.rp012 != ''){
      this.currentMaster.rp012 = data.rp012.slice(0,10);
    }
    if(typeof data.rp013 == 'string' && data.rp013 != ''){
      this.currentMaster.rp013 = data.rp013.slice(0,10);
    }
    if(typeof data.rp031 == 'string' && data.rp031 != ''){
      this.currentMaster.rp031 = data.rp031.slice(0,10);
    }
    if(typeof data.rp032 == 'string' && data.rp032 != ''){
      this.currentMaster.rp032 = data.rp032.slice(0,10);
    }
  },
  //form表單提交方法
  saveMasters(){
    if(String(this.currentMaster.rp003 || "") == ""){
      this.$refs.buttonBar.setToolButtonState(true);
      return this.showMessage(this.$t('SystemBugRpt_multi_language_20')); //提交部門不能為空,請重新輸入 SystemBugRpt_multi_language_20
    }
    if(String(this.currentMaster.rp009 || "") == ""){
      this.$refs.buttonBar.setToolButtonState(true);
      return this.showMessage(this.$t('SystemBugRpt_multi_language_13')); //跟進部門不能為空,請重新輸入
    }

    if(this.username != 'hb'){ //考慮到波哥要設置優先級信息,如下檢驗不方便他操作,先暫時設置賬戶跳過檢測
      //檢查是否有一個字段有值
      if (
        this.currentMaster.problemcategory ||
        this.currentMaster.rp007 ||
        this.currentMaster.solutiontype ||
        this.currentMaster.rp020 ||
        this.currentMaster.rp027
      ) {
        // 處理方式,解決方案類型,系統名稱,功能描述,問題類別任意一個字段不為空時,所有字段值都不能為空
        if(!this.currentMaster.problemcategory){
          this.$refs.buttonBar.setToolButtonState(true);
          return this.showMessage(this.$t('Issue Category Cannot Be Empty!')); // 問題類別不能為空!
        }
        if(!this.currentMaster.rp020){
          this.$refs.buttonBar.setToolButtonState(true);
          return this.showMessage(this.$t(this.$t('System Name Cannot Be Empty!'))); // 系統名稱不能為空!
        } 
        if(!this.currentMaster.rp027){
          this.$refs.buttonBar.setToolButtonState(true);
          return this.showMessage(this.$t(this.$t('Function Description Cannot Be Empty!'))); // 功能描述不能為空!
        }
        if(!this.currentMaster.solutiontype){
          this.$refs.buttonBar.setToolButtonState(true);
          return this.showMessage(this.$t(this.$t('Solution Type Cannot Be Empty!'))); // 解決方案類型不能為空!
        }
        if(!this.currentMaster.rp007){
          this.$refs.buttonBar.setToolButtonState(true);
          return this.showMessage(this.$t(this.$t('Handling Method Cannot Be Empty!'))); // 處理方式不能為空!
        }
      }
    }

    this.isLoading = true; // 开始加载

    var form = new FormData();
    var obj = this.currentMaster;

    var index = 1
    this.bugImgArray = this.$refs.admrp_img_ref.files;
    for(let i of this.bugImgArray){
      form.append(`img${index}`,i); //添加圖片
      index++
    }

    index = 1
    for(let file of this.fileArray_left){
      form.append(`file_rq005_${index}`,file.rq005) //文件名
      form.append(`file_rq006_${index}`,file.rq006) //文件內容
      form.append(`file_rq007_${index}`,file.rq007) //類型
      form.append(`file_incid_${index}`,(file.inc_id || ""))
      index++
    }

    for(let file of this.fileArray_right){
      form.append(`file_rq005_${index}`,file.rq005) //文件名
      form.append(`file_rq006_${index}`,file.rq006) //文件內容
      form.append(`file_rq007_${index}`,file.rq007) //類型
      form.append(`file_incid_${index}`,(file.inc_id || ""))
      index++
    }

    for (let filedname in obj) {
      if(obj[filedname]!=null){   
        if (["rp012","rp013","rp031","rp032","planbdate","planedate"].indexOf(filedname) > -1) {
          obj[filedname] = this.$moment(obj[filedname]).format("YYYY-MM-DD");
          obj[filedname] = obj[filedname] + ' 00:00:00.000';
        }     
        form.append(filedname, obj[filedname]); 
      }          
    }

    if(this.masterState == 1){ //新增
      axios.post(`/systembugrpt/admrp/create`,form).then(response =>{
        this.isLoading = false; // 停止加载
        if(response.data.inc_id){
          this.state = 0;
          this.masterState = 0;
          this.currentMaster = response.data;
          this.currentMasterClone = this.cloneObject(this.currentMaster);
          this.setDateStr(this.currentMaster);
          this.$nextTick(function () {
            this.$refs.AdmrpTable.datatable.search("").draw();
          })
          this.getFileArray('F'); //獲取附件列表
          this.getFileArray('R'); //獲取附件列表(右)
          this.showMessage(this.$t('new success')); //新增成功
        }else{
          this.showMessage(this.$t('the new failure')); //新增失敗
          this.$refs.buttonBar.setToolButtonState(true);
        }
        this.$nextTick(function () {
          $('select.select2-problemcategory').trigger('change');
        })
      })
      .catch(error =>{
        this.isLoading = false; // 停止加载
        this.$refs.buttonBar.setToolButtonState(true);
        this.showMessage(this.$t('the new failure')); //新增失敗
        console.log(error);
      })
    }else{ //修改
      axios.post(`/systembugrpt/admrp/update`,form)
      .then((response) => {
        this.isLoading = false; // 停止加载
        if(response.status == 200){
          this.state = 0;
          this.masterState = 0;
          // this.currentMaster = response.data.data;
          this.currentMasterClone = this.cloneObject(this.currentMaster);
          this.setDateStr(this.currentMaster);
          this.$nextTick(function () {
            this.$refs.AdmrpTable.datatable.search("").draw();
          })
          this.getFileArray('F'); //獲取附件列表
          this.getFileArray('R'); //獲取附件列表(右)
          this.$nextTick(function () {
            $('select.select2-problemcategory').trigger('change');
          })
          return this.showMessage(this.$t("change successfully"));
        }
        this.showMessage(this.$t("change failed"));
        this.$refs.buttonBar.setToolButtonState(true);
        this.$nextTick(function () {
          $('select.select2-problemcategory').trigger('change');
        })
      })
      .catch((error) => {
        this.isLoading = false; // 停止加载
        this.$refs.buttonBar.setToolButtonState(true);
        this.showMessage(this.$t("change failed"));
        console.log(error);
      });
    }
  },
  saveMaster(){
    if(String(this.currentMaster.rp003 || "") == ""){
      this.$refs.buttonBar.setToolButtonState(true);
      return this.showMessage(this.$t('SystemBugRpt_multi_language_20')); //提交部門不能為空,請重新輸入 SystemBugRpt_multi_language_20
    }
    //新增前的校驗未加
    if(this.masterState == 1){ //新增
      axios.post(`/systembugrpt/admrp/create`,this.objectToFormData(this.currentMaster)).then(response =>{
        if(response.data.inc_id){
          this.state = 0;
          this.masterState = 0;
          this.currentMaster = response.data;
          this.currentMasterClone = this.cloneObject(this.currentMaster);
          this.setDateStr(this.currentMaster);
          this.$refs.AdmrpTable.datatable.search("").draw();
          this.showMessage(this.$t('new success')); //新增成功
        }else{
          this.showMessage(this.$t('the new failure')); //新增失敗
        }
      })
      .catch(error =>{
        console.log(error);
      })
    }else{ //修改
      axios.post(`/systembugrpt/admrp/update`,this.objectToFormData(this.currentMaster))
      .then((response) => {
        if(response.status == 200){
          this.state = 0;
          this.masterState = 0;
          this.currentMaster = response.data;
          this.currentMasterClone = this.cloneObject(this.currentMaster);
          this.setDateStr(this.currentMaster);
          this.$refs.AdmrpTable.datatable.search("").draw();
          return this.showMessage(this.$t("change successfully"));
        }
        return this.showMessage(this.$t("change failed"));
      })
      .catch((error) => {
        console.log(error);
      });
    }
  },
  //新增時獲取系統問題上報單號(通過今天日期yyyymmdd和單別進行模糊查詢)
  getAdmrpNo(){
    var id = this.$moment(new Date()).format("YYYYMMDD");
    axios.get(`/systembugrpt/get_admrpno`,{params:{id:id}}).then(response =>{
      this.currentMaster.rp017 = response.data.data; //單號
      this.getImgArray();
    })
    .catch(error =>{
      console.log(error);
    })
  },
  //新增按鈕點擊事件
  addMaster(){
    this.state = 1;
    this.masterState = 1;
    this.currentMaster = {};
    var date = this.$moment(new Date()).format('yyyy-MM-DD');
    this.getAdmrpNo();
    this.fileArray_left = [];
    this.fileArray_right = [];
    this.currentMaster.rp004 = this.username; //提出人
    this.currentMaster.rp043 = this.username; //原始提出人
    this.currentMaster.rp002 = date; //提出日期
    this.currentMaster.rp011 ='N'; //處理狀態
    // this.set_image("");
    this.$nextTick(function () {
      $('select.select2-type').trigger('change');
      $('select.select2-type2').trigger('change');
      $('select.select2-genjin').trigger('change');
      $('select.select2-genjin2').trigger('change');
      $('select.select2-problemcategory').trigger('change');
    });
    this.$refs.flowChartTable.datatable.clear().rows.add([]).draw(); //獲取流程圖列表
    this.$refs.Admrp_details.click();
  },
  //獲取部門列表
  get_cmsmeArray(){
    function matchCustom(params, data) {
      if ($.trim(params.term) === '') {
          return data;
      }
      if (typeof data.text === 'undefined' || data.id === undefined) {
          return null;
      }
      let term = params.term.toLowerCase();
      let text = data.text.toLowerCase();
      let id = data.id.toString().toLowerCase();
      if (text.indexOf(term) > -1 || id.indexOf(term) > -1) {
          return data;
      }
      return null;
    }
    var _this = this;
    axios.get(`/systembugrpt/cmsme_table`).then(response =>{
      if(response.data.status){
        this.cmsmeArray = this.remove_blank(response.data.data);
        // var selectData = [{'id': '', 'text': '', 'me002': ''}]
        var selectData = [{'id': '', 'text': ''}]
        for (let d of response.data.data){
          // selectData.push({'id': d.me001, 'text': `${d.me001}: ${d.me002}`,'me002':d.me002})
          selectData.push({'id': d.me001, 'text': `${d.me001}: ${d.me002}`})
        }
        $('select.select2-type').select2({data: selectData,matcher: matchCustom}).on("select2:select", function(e){
          _this.currentMaster.rp003 = e.params.data.id;
          // $(this).val(e.params.data.text.split(':')[1]).trigger("change");
        });
        $('select.select2-type2').select2({data: selectData,matcher: matchCustom}).on("select2:select", function(e){
          _this.currentMaster.rp003 = e.params.data.id;
        });
        $('select.select2-genjin').select2({data: selectData,matcher: matchCustom}).on("select2:select", function(e){
          _this.currentMaster.rp009 = e.params.data.id;
        });
        $('select.select2-genjin2').select2({data: selectData,matcher: matchCustom}).on("select2:select", function(e){
          _this.currentMaster.rp009 = e.params.data.id;
        });
      }
    })
    .catch(error =>{
      console.log(error);
    })
  },
  //去除字符串末尾空格(列表中的所有對象)
  remove_blank(data) {
    let list = data;
    for (let item of list) {
      for (let key in item) {
        if (typeof item[key] === "string") {
          item[key] = item[key].trim();
        }
      }
    }
    return list;
  },
  //克隆對象
  cloneObject(obj) {
    if (typeof obj != "object") return;
    return JSON.parse(JSON.stringify(obj));
  },
  associatedTaskDbClick(data) {
    var pk = data.inc_id;
    window.init_task(pk);
  }  
},
}
</script>
<style>
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
}

.loading-spinner {
    text-align: center;
    color: white;
}

.required {
  color: red;
}

.detailInfo.card .dropdownMenuScroll.dropdown {
    width: 100%;
}

.detailInfo.card .tab-content .sqlScriptRow>.form-group:not(:first-child) {
    display: flex;
    align-items: center;
}
</style>