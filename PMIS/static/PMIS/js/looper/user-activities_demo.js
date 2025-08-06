var UserActivites = Vue.extend({
    data() {
        return {
            endDate:'',
            TaskData:{}
        }
    },
    created() {
        this.getData()
    },
    methods : {
        getData() {
            var self = this;
            var query = {}
            if (self.endDate != '')
                query['endDate'] = self.endDate;
            $.get("/PMIS/user/getUserActivites", query, function(data){
                var taskData = $.extend({},self.TaskData);
                if (data.code == 0) {
                    self.endDate = data.endDate
                    data.data.forEach(task => {
                        var title = self.getTitle(new Date(task.planbdate));
                        if (!taskData.hasOwnProperty(title))
                            taskData[title] = []
                        item = {      
                            task:task.task,
                            contact:task.contact,
                            sessionDesc:task.sessionDesc,
                            timeago:$.timeago(task.planbdate)
                        }
                        taskData[title].push(item);
                    })
                    self.TaskData = taskData;
                }
            })
        },
        getTitle(date) {
            const today = new Date()
            const yesterday = new Date(new Date().setDate(new Date().getDate()-1));
            if (date.getDate() == today.getDate() && date.getMonth() == today.getMonth() && date.getFullYear() == today.getFullYear())
                return 'Today';
            else if (date.getDate() == yesterday.getDate() && date.getMonth() == yesterday.getMonth() && date.getFullYear() == yesterday.getFullYear())
                return 'Yesterday';
            else
                return '' + date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate();
        }
    }
})

var activites = new UserActivites().$mount("#user-timeline");