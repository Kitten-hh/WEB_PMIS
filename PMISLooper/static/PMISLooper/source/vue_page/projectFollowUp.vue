<template>
  <div class="page-inner">
    <h3 class="section-title pt-0 mb-3"> Project Follow Up in WPMIS </h3>
    <div class="wrapper mb-4">
      <div class="rounded-circle text-center startBox font-weight-bold">start</div>
    </div>
    <div class="levelBox">
      <div class="task-header justify-content-center pt-3">
        <h3 class="task-title"> Menu Level</h3>
      </div>
      <div class="task-body p-4">
        <a target="_blank" href="/looper/staff_dashboard" class="task-issue text-center font-weight-bold">Check Dashboard</a>
        <a target="_blank" href="/looper/task/today_task" class="task-issue text-center font-weight-bold">Check Today’s Task</a>
        <a target="mindmap" href="/looper/mindmap?type=1" class="task-issue text-center font-weight-bold">Check Mindmap</a>
        <a target="_blank" href="#" id="linkGoal" class="task-issue text-center font-weight-bold">Check Goal</a>
        <a target="_blank" href="/devplat/project/overview" class="task-issue text-center font-weight-bold">Check Projects</a>
        <a target="_blank" href="/looper/user/sessions" class="task-issue text-center font-weight-bold">Check Session SDLC</a>
        <a target="_blank" href="/looper/task/enquiry" class="task-issue text-center font-weight-bold">Check Tasks</a>
      </div>
    </div>
    <div class="levelBox">
      <div class="task-header justify-content-center pt-3">
        <h3 class="task-title"> Second Level</h3>
      </div>
      <div class="task-body p-4">
        <a target="_blank" href="#" id="link_act_tasks" class="task-issue text-center font-weight-bold">Activity Tasks</a>
        <a target="_blank" href="" class="task-issue text-center font-weight-bold invisible"></a>
        <a target="_blank" href="" class="task-issue text-center font-weight-bold invisible"></a>
        <a target="_blank" href="" class="task-issue text-center font-weight-bold invisible"></a>
        <a target="_blank" href="/devplat/project/overview" class="task-issue text-center font-weight-bold">Project - Check priority, Project</a>
        <a target="_blank" href="" class="task-issue text-center font-weight-bold invisible"></a>
        <a target="_blank" href="" class="task-issue text-center font-weight-bold invisible"></a>
      </div>
    </div>
    <div class="levelBox level3 border-0">
      <div class="task-header justify-content-center pt-3 invisible">
        <h3 class="task-title"></h3>
      </div>
      <div class="task-body p-4">
        <a target="_blank" href="" class="task-issue text-center font-weight-bold invisible"></a>
        <a target="_blank" href="" class="task-issue text-center font-weight-bold"></a>
        <a target="_blank" href="" class="task-issue text-center font-weight-bold invisible"></a>
        <a target="_blank" href="" class="task-issue text-center font-weight-bold invisible"></a>
        <a target="_blank" href="" class="task-issue text-center font-weight-bold lineStyle">Check Milestone (Session) progress for completion status</a>
        <a target="_blank" href="" class="task-issue text-center font-weight-bold invisible"></a>
        <a target="_blank" href="" class="task-issue text-center font-weight-bold invisible"></a>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "onePage_vueFrm",
  data() {
    return {

    }
  },
  mounted() {
    var username = get_username();
    var quarterly = "{0}-{1}".format(new Date().toString("yyyy"), Math.ceil((new Date().getMonth() + 1)/3));
    $("#linkGoal").attr("href", `/looper/goal/overall/quarterly_goal?contact=${username}&period=${quarterly}`);
    $("#link_act_tasks").attr("href", `/looper/user/activites?contact=${username}`);
  },
  methods: {
  },
};
</script>
<style>
.wrapper .startBox {
  width: 20rem;
  height: 4rem;
  border: 2px solid #000;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.levelBox {
  display: inline-flex;
  flex-direction: column;
  width: 20rem;
  height: 100%;
  vertical-align: top;
  border-radius: 0.25rem;
  /* background-color: #fff; */
  border: 2px dashed #000;
  position: relative;
}

.levelBox:not(:last-child) {
  margin-right: 1.25rem;
}

.levelBox .task-body {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.levelBox .task-issue {
  color: #363642;
  border: 2px solid #000;
  width: 200px;
  height: 150px;
  padding: 1rem;
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-around;
  align-items: center;
  color: #363642;
}

.levelBox .task-issue:hover {
  cursor: pointer;
  border: 1px solid #346cb0;
  box-shadow: 1px 1px 0px 2px #346cb0;
  background-color: #f6f7f9;
  color: #346cb0;
  text-decoration: none
}

.levelBox .task-issue.lineStyle {
  align-self: end;
}

.lineStyle::after {
  position: absolute;
  left: -103px;
  bottom: -28%;
  top: 3px;
  margin: auto;
  width: 222px;
  height: 2px;
  background: #03030f;
  content: '';
  z-index: 9999;
  transform: rotate3d(1, 1, -1, 45deg);
}
</style>