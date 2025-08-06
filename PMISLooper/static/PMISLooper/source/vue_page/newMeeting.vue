<template>
  <div :class="['meeting-page', collapse ? 'd-flex aside-expand-sm has-sidebar-open' : '']">
    <div class="aside-backdrop" @click="handleALL"></div>
    <div class="meeting-sidebar border-right" v-show="collapse">
      <header class="page-navs bg-light shadow-sm">
        <div class="input-group has-clearable">
          <button type="button" class="close" aria-label="Close" @click="clear_input">
            <span aria-hidden="true">
              <i class="fa fa-times-circle"></i>
            </span>
          </button>
          <label class="input-group-prepend" for="searchMeeting">
            <span class="input-group-text">
              <span class="oi oi-magnifying-glass"></span>
            </span>
          </label>
          <input type="text" class="form-control" id="searchMeeting" v-model="searchMeeting" @keyup.enter="init_tree(searchMeeting)" :placeholder="$t('Meeting ID')">
        </div>
        <div class="col-auto px-0 d-flex align-items-center">
          <div class="btn btn-light p-2 fileinput-button meetingDateIcon">
            <i class="oi oi-calendar"></i>
            <span class="sr-only">日期會議查詢</span><input type="text" class="" ref="cal_search" @change="calendar_search" data-toggle="flatpickr" data-date-format="Y-m-d">
          </div>
          <button
            type="button"
            class="hamburger"
            data-toggle="tooltip"
            data-placement="bottom"
            :data-original-title="$t('Add Meeting')"
            @click="displayMeetingInfo"
          >
            <i class="fas fa-plus"></i>
            <span class="sr-only">添加会议信息</span>
          </button>
           <button 
            type="button"
            class="hamburger" 
            data-toggle="tooltip"
            data-placement="bottom"
            :data-original-title="$t('Refresh Treeview')"
            @click="init_tree('-8')"
            style="font-size: 15px;"
           >
             <i class="fas fa-redo-alt"></i>
              <span class="sr-only">刷新樹狀圖</span>
          </button>
        </div>
      </header>
      <div class="board meeting_tree py-2 px-3 scrollbar">
        <LPTree ref="lpTree" :data="treeData" @selectNode="nodeSelect" @dblclickNode="Nodedblclick" :set_menus="set_menus" :key="treeKey"/>
      </div>
    </div>
    <router-view @refresh_tree="init_tree" :collapse="collapse" @create_meeting="create_meeting" @toggleClick='toggleClick' :key="viewKey"></router-view>
  </div>
  <div>
    <LPModal
    :title="$t('Edit Meeting ID')"
    ref="updateMeetingID"
    id="updateMeetingID"
    >
      <template v-slot:body>
        <div class="form-row m-0">
          <div class="form-group d-flex col-12">
            <label class="col-form-label col-auto pl-0">{{ $t("Meeting ID") }}</label>
            <input type="text" class="form-control col" v-model="MeetingData.new_meetingid" />
          </div>
        </div>
      </template>
      <template v-slot:footer>
          <button type="button" class="btn btn-primary mr-sm-2" @click="updateMetID">{{ $t("Confirm") }}</button>
          <button type="button" class="btn btn-secondary" data-dismiss="modal">{{ $t('Cancel') }}</button>
      </template>
    </LPModal>
  </div>
</template>


<script>
import axios from "axios";
import LPMultipleSelect2 from "@components/looper/forms/LPMultipleSelect2.vue";
import LPTree from "@components/looper/general/LPTree.vue";
import LPCard from "@components/looper/layout/LPCard.vue";
import LPModal from "@components/looper/layout/LPModal.vue";

export default {
  name: "newMeeting",
  components: {
    LPMultipleSelect2,
    LPTree,
    LPCard,
    LPModal,
  },
  props: { meeting_conclusion: String },
  data() {
    return {
      treeData: [],
      collapse: true,
      defOpen:false,
      searchMeeting:'',
      todayId:'',
      dataid : '',
      MeetingData:{},
      treeKey:0,
      viewKey:0,
    };
  },
  mounted() {
    //tooltip 提示工具显示
    $('[data-toggle="tooltip"]').tooltip();
    $('[data-toggle="tooltip"]').on("click", function() {
      $(this).tooltip("hide");
    });
  },
  created(){
    var self = this
    this.todayId=new Date().format("yyMMdd")
    this.init_tree('-8')
  },
  methods: { 
    set_menus(data) {
        return [
        {
          label: this.$t('Delete'),
          hidden:["metting_acc"].indexOf(data.tier) != -1,
          click: (menus, args) => {
            this.delete_topic(args)
            return true;
          }
        },
        {
          label: this.$t('Edit Meeting ID'),
          hidden:data.tier != '0',
          click: (menus, args) => {
            this.Nodedblclick(args)
            return true;
          }
        }]
    },    
    init_tree(date){
      if(isNaN(date)){
        alert('只能查詢會議ID(ID為年份後兩位+月份+日期+序號組成)！')
        return
      }
      var searchMet = this.searchMeeting
      if((searchMet!='') && (!isNaN(searchMet))){
        date = searchMet
      }
      axios
        .get(`/looper/metting/get_metting_tree?date=${date}`)
        .then(response => {
            // 處理成功後的返回數據
            if(response.data.status){
                var self = this
                if(this.$route.query.status=='add'){
                  for(var tree of this.treeData){
                    if(tree['strid']==this.dataid && tree['inc_id']==null){
                      response.data.data.push({'icon': "fas fa-star-of-life",'name': this.dataid+'(0/0)','children': [],'inc_id':null,'strid':this.dataid,'sub_inc_id':'','tier':'0'})  
                      break;
                    }
                  }
                }
                this.treeData = response.data.data
                var no = '01'
                for(var i of response.data.data){
                  if(this.todayId == i.strid.slice(0,6)){
                    if(parseInt(i.strid.slice(6))>parseInt(no) || parseInt(i.strid.slice(6))==1)
                      no = String(parseInt(i.strid.slice(6))+1)
                  }
                }
                this.dataid = this.todayId+no.padStart(2, '0')
                if(self.defOpen==false){
                  window.setTimeout(function () {
                    if(self.dataid.substring (7)=='1')
                      self.displayMeetingInfo()
                    else
                      self.nodeSelect(self.treeData[self.treeData.length-1])
                  }, 500);
                  self.defOpen=true
                }
            }
        })
    },

    create_meeting(data){
      this.dataid = data.id
      if(this.checkTreeData()){
        this.treeData.push({'icon': "fas fa-star-of-life",'name': data.id+'(0/0)','children': [],'inc_id':null,'strid':data.id,'sub_inc_id':'','tier':'0'})  
        this.treeScroll();
        if (SWApp.os.isAndroid || SWApp.os.isPhone)
          this.toggleClick();
      } 
    },
    //增加新增會議
    displayMeetingInfo() {
      if(this.$route.query.status=='add' && this.checkTreeData()){
        this.treeData.push({'icon': "fas fa-star-of-life",'name': this.dataid+'(0/0)','children': [],'inc_id':null,'strid':this.dataid,'sub_inc_id':'','tier':'0'})  
        this.nodeSelect(this.treeData[this.treeData.length-1])
      }else
        this.$router.push( {path: '/create', query: {'status': "add"} });
      // this.checkToday()
      // if (this.checkTreeData()){
      //   var node = {'icon': "",'name': this.dataid+'(0/0)','children': [],'inc_id':null,'strid':this.dataid,'sub_inc_id':'','tier':'0'}
      //   this.treeData.push(node);
      //   //this.$refs.lpTree.$data.current_data = node;
      //   this.treeScroll();
      // }
      // if (SWApp.os.isAndroid || SWApp.os.isPhone)
      //   this.toggleClick();
    },
    //檢驗樹狀圖是否存在空節點
    checkTreeData(){
      for(var tree of this.treeData){
        if(tree['strid']==this.dataid && tree['inc_id']!=null)this.dataid = String(parseInt(this.dataid)+1)
        if(tree['strid']==this.dataid && tree['inc_id']==null)
          return false
        else if (tree['inc_id']==null){
          return false
        }
      }
      return true
    },
    treeScroll(){
      $('.meeting_tree').stop().animate({
        scrollTop: $('.meeting_tree')[0].scrollHeight
      }, 800);
    },
    //會議行點擊方法
    nodeSelect(value){
      console.log(value);
      var strid = null
      var inc_id = null
      var sub_inc_id = null
      switch(value.tier){
        case '2':
          strid = value.strid
          inc_id = value.inc_id
          sub_inc_id = value.sub_inc_id
          break
        default:  
          strid = value.strid
          inc_id = value.inc_id
          break
      }
      this.$router.push( {path: '/create', query: {'status': "edit",'id':strid,'inc_id':inc_id,'sub_inc_id':sub_inc_id} });
      if (SWApp.os.isAndroid || SWApp.os.isPhone)
        this.toggleClick();
    },
    //顯示隱藏樹狀圖
    toggleClick(){
      this.collapse = !this.collapse
      console.log(this.collapse)
    },
    //清除樹狀圖查詢輸入框
    clear_input(){
      this.searchMeeting = '';
    },
    handleALL(event) {
      this.collapse = false;
    },
    delete_topic(args){
      if(confirm("你確定要刪除該議題及相關下層信息?")){
        var url = `/looper/metting/MettingmasterDeleteView/${args['inc_id']}`
        if(args['sub_inc_id']!='')
          url = `/looper/metting/delete_met_project?id=${args['sub_inc_id']}`
        axios
          .post(url)
          .then(response => {
            if (response.data.status) {
              alert('刪除成功')
              this.init_tree('-8')
              this.init_all_subject();
              this.init_analysis_meeting();
            }else{
              alert('刪除失敗')
            }
          })
          .catch(error => {
            console.log(error);
          });
      }
    },
    //樹狀圖節點雙擊方法
    Nodedblclick(data){
      this.MeetingData['inc_id']=data.inc_id
      this.MeetingData['old_meetingid']=data.strid
      this.MeetingData['new_meetingid']=data.strid
      this.MeetingData['sub_inc_id']=this.$route.query.sub_inc_id
      if(this.MeetingData.inc_id==undefined || this.MeetingData.inc_id==null || this.MeetingData.inc_id=='')
        this.MeetingData['checked']='true'
      else
        this.MeetingData['checked']='false'
      if (SWApp.os.isMobile) 
        this.$refs.updateMeetingID.width("380px");
      else
        this.$refs.updateMeetingID.width("500px");
      this.$refs.updateMeetingID.show();
      // console.log(data)
    },
    updateMeetingIDhide(){
      this.$refs.updateMeetingID.hide();
      this.MeetingData = {};
    },
    //修改會議ID
    updateMetID(){
      if (confirm("你確定要修改該會議ID?")){
        axios
          .post(`/looper/metting/update_meetingid`, this.objectToFormData(this.MeetingData))
          .then(response => {
            if (response.data.status) {
              if(this.MeetingData.inc_id==undefined || this.MeetingData.inc_id==null || this.MeetingData.inc_id==''){
                this.$router.push({path: '/create', query: {'status': "edit",'id':this.MeetingData.new_meetingid,'inc_id':'','sub_inc_id':''} });
                for(var i=0;i<this.treeData.length;i++){
                  if((this.treeData[i].strid == this.MeetingData.old_meetingid) && (this.treeData[i].inc_id==undefined || this.treeData[i].inc_id==null || this.treeData[i].inc_id=='')){
                    this.treeData[i]={'icon': "",'name': this.MeetingData.new_meetingid+'(0/0)','children': [],'inc_id':null,'strid':this.MeetingData.new_meetingid,'sub_inc_id':'','tier':'0'}
                    this.treeKey+=1
                    this.viewKey+=1
                    break
                  }
                }
                this.updateMeetingIDhide();
              }else{
                console.log(response)
                this.$router.push( {path: '/create', query: {'status': "edit",'id':this.MeetingData.new_meetingid,'inc_id':this.MeetingData.inc_id,'sub_inc_id':this.MeetingData.sub_inc_id} });
                this.updateMeetingIDhide();
                this.init_tree('-8')
              }
              alert('修改會議ID成功！')
            }else{
              if(response.data.msg.length>0)
                alert(response.data.msg)
              else
                alert('修改會議ID失敗！')
            }
          })
          .catch(error => {
            console.log(error);
          });
        
      }
    },
    //根據日期日期查詢對應日期的會議
    calendar_search(){
      if(this.$refs.cal_search.value!=''){
        var cal_date = new Date(this.$refs.cal_search.value).format("yyMMdd")
        this.init_tree(cal_date)
      }
    },

    checkToday(){
      var today = new Date()
      today = today.toString('yyMMdd')
      if(this.dataid!='' && this.dataid.substring(0,6)!=today){
        this.dataid = '{0}{1}'.format(today,this.dataid.substring(6))
      }
    }

  }
};
</script>
<style>
.fa-star-of-life{
  color:#757b81 !important;
  font-size: 10px !important;
}
</style>