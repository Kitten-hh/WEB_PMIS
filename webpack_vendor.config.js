const path = require('path');
const webpack = require('webpack');

var test = require('fs').readFileSync('./manage.py', 'utf8');
var main_app_name = test.match(/('|")([^'"]+)[.]settings('|")/)[2]

module.exports = {
    mode: 'production',
    entry: {
        vendor: ['vue', 'vue-router','axios'],
    },
    // 这个是输出 dll 文件
    output: {
        path: path.resolve(__dirname, './'+ main_app_name +'/static/' + main_app_name + '/dist/javascript'),
        filename: '[name].js',
        library: '[name]',
    },
    // 这个是输出映射表
    plugins: [
        new webpack.DllPlugin({ 
            name: '[name]', // name === output.library
            path: path.resolve(__dirname, '[name].manifest.json'),
        })
    ]
};
