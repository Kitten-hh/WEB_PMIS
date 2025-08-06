import { createApp } from 'vue'
import FlowChartMain from '../vue_page/main.vue'
import PublicPlugins from '@components/static/assets/javascript/PublicPlugins.js'
import moment from 'moment'     //格式化日期插件
import numeral from 'numeral'
import axios from 'axios'

window.app = createApp(FlowChartMain)
app = app.use(PublicPlugins)
app = app.use(moment)
app = app.use(numeral)
app.config.globalProperties.$moment = moment;
app.config.globalProperties.$numeral = numeral;

axios.interceptors.request.use(config => {
    var lang_code = $("#curr_language_code").val();
    if (lang_code != "" && config.method == "post" && config.url.length > 0) {
        var prefix_str = config.url.charAt(0) == "/" ? "/"+lang_code : lang_code;
        if (!config.url.startsWith(prefix_str))
            config.url = prefix_str + config.url;
    }    
    return config
  }, error => {
    return Promise.reject(error)
});
