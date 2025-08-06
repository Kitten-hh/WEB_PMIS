/**
import axios from 'axios'

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
*/

const setPermissionAxiosInterceptor = (instance) => {
  const interceptor = instance.interceptors.response.use(
      response => response,
      async (error) => {
          const originalRequest = error.config;

          // 如果服务器返回403错误
          if (error.response && error.response.status === 403 && !originalRequest._retry) {
              originalRequest._retry = true;
              alert(gettext("You do not have permission to perform this action."));
          }

          return Promise.reject(error);
      }
  );

  if (!instance.hasOwnProperty("interceptorIds")) {
      instance.interceptorIds = {};
  }
  instance.interceptorIds["permissionInterceptor"] = interceptor;
  return interceptor;
}

import axios from 'axios';
setPermissionAxiosInterceptor(axios);

import ReportPlugins from '/BaseReportApp/static/BaseReportApp/assets/javascript/ReportPlugins.js'
app = app.use(ReportPlugins)