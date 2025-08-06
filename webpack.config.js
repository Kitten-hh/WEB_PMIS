const HtmlWebpackPlugin = require('html-webpack-plugin');
const { VueLoaderPlugin } = require('vue-loader')
var BundleTracker = require('webpack-bundle-tracker');
const { CleanWebpackPlugin } = require('clean-webpack-plugin'); // installed via npm
const WebpackShellPluginNext = require('webpack-shell-plugin-next');
const SingleEntryPlugin = require("webpack/lib/SingleEntryPlugin");
const webpack = require('webpack')
const path = require('path');
var fs = require('fs');
const glob = require("glob");
//讀取本項目settings.py文件
var test = fs.readFileSync('./manage.py', 'utf8');
var main_app_name = test.match(/('|")([^'"]+)[.]settings('|")/)[2];
var settings = fs.readFileSync('./' + main_app_name + '/settings.py', 'utf8');
var Pro_ENV = true
if (settings.match(/DEVELOPMENT\s*=\s*(\w+)/))
  Pro_ENV = settings.match(/DEVELOPMENT\s*=\s*(\w+)/)[1] == "False"  //以Django中的DEVELOPMENT=False表示開發環境，否則為生產環境
var Debug = settings.match(/DEBUG\s*=\s*(\w+)/)[1] == "True"  //以Django中的DEBUG=False表示開發環境，否則為生產環境  

//讀取本項目所有含有source
var watch_dirs = []
var app_names = glob.sync("./**/source").filter((dir)=>{
    var app_name = dir.substring(dir.indexOf("/") + 1, dir.indexOf("/static"))
    var check = new RegExp(app_name + "/static/" + app_name)
    return dir.match(check);
  }).map((dir)=>{
    watch_dirs.push(dir);
    var app_name = dir.substring(dir.indexOf("/") + 1, dir.indexOf("/static"))
    return app_name
});
watch_dirs = [...new Set(watch_dirs)];
app_names = [...new Set(app_names)]
console.log(app_names.join(","));
var files_regex = "./{"+app_names.join(",")+"}/**/source/**/*.js"
if (app_names.length == 1) 
  files_regex = "./"+app_names+"/**/source/**/*.js"
module.exports =  {
    mode: Debug ? 'development' : 'production',
    entry: glob.sync(files_regex).reduce((acc, item) => {
      const path = item.split("/");
      path[path.findIndex(p => p == "source")] = "dist"
      path[path.length-1] = path[path.length - 1].replace(".js", "");
      const name = path.join('/');
      acc[name] = item;
      return acc;
    }, {}),  
    output: {
      path: path.resolve(__dirname, ""),
      filename: (pathData) => {
        if (pathData.chunk.name.indexOf("BaseApp/static/BaseApp") != -1)
          return '[name].js'
        else
          return '[name]-[hash].js'
      }
    },
    module: {
      rules: [
        { test: /\.js$/, use: 'babel-loader' },
        { test: /\.vue$/, use: 'vue-loader' },
        { test: /\.css$/, use: ['vue-style-loader', 'css-loader']}
      ]
    },
    resolve: {
      // 别名，可以直接使用别名来代表设定的路径以及其他，在这个项目中没用到
      alias: {
        '@components': path.resolve(__dirname, 'BaseApp/static/BaseApp/assets/vue_components')
      },
      symlinks:false // 使用npm link
    },    
    plugins: [
      new webpack.DefinePlugin({
        Pro_ENV: JSON.stringify(Pro_ENV),  //設置是否生產環境，以Django中的Debug=False表示開發環境，否則為生產環境
      }),
      new VueLoaderPlugin(),
      //new AddWatchWebpackPlugin(watch_dirs),
      //默認是刪除配置中的output.path目錄下的所有文件，當前配置文件output.path配置為根目錄
      //必須設置需要刪除哪些文件，不然將刪除整個根目錄內的內容
      new CleanWebpackPlugin(  
        {
          root:__dirname,
          verbose:true, //開啟控制臺輸出
          dry:false, //啟用刪除文件
          cleanOnceBeforeBuildPatterns:[files_regex.replace("**/source/**","**/dist/**"), "!"+files_regex.replace("**/source/**","**/dist/**").replace("*.js","vendor.js")] //需要刪除的文件
        }
      ),
      new webpack.DllReferencePlugin({
        // 注意: DllReferencePlugin 的 context 必须和 package.json 的同级目录，要不然会链接失败
        context: path.resolve(__dirname, ''),
        manifest: path.resolve(__dirname, './vendor.manifest.json'),
      }),      
      new BundleTracker({filename: './webpack-stats.json'}),
      new WebpackShellPluginNext({
        onAfterDone:{
          scripts: ["sed -i 's\/\"\\.\\/[^/]\\+\\/static\\//\"/g' ./webpack-stats.json"],
          blocking: false,
          parallel: true
        }
      }),
    ]
}

