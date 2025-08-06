/**
* 獲取本週、本季度、本月、上月的開端日期、停止日期
*/
var now = new Date(); //當前日期
var nowDayOfWeek = now.getDay(); //今天本週的第幾天
var nowDay = now.getDate(); //當前日
var nowMonth = now.getMonth(); //當前月
var nowYear = now.getYear(); //當前年
nowYear += (nowYear < 2000) ? 1900 : 0; //

var lastMonthDate = new Date(); //上月日期
lastMonthDate.setDate(1);
lastMonthDate.setMonth(lastMonthDate.getMonth()-1);
var lastYear = lastMonthDate.getYear();
var lastMonth = lastMonthDate.getMonth();

//格局化日期：yyyy-MM-dd
function formatDate(date) {
    var myyear = date.getFullYear();
    var mymonth = date.getMonth()+1;
    var myweekday = date.getDate();
    
    if(mymonth < 10){
    mymonth = "0" + mymonth;
    }
    if(myweekday < 10){
    myweekday = "0" + myweekday;
    }
    return (myyear+"-"+mymonth + "-" + myweekday);
}

function getToday(){
    return formatDate(now);
}

//獲得某月的天數
function getMonthDays(myMonth){
    var monthStartDate = new Date(nowYear, myMonth, 1);
    var monthEndDate = new Date(nowYear, myMonth + 1, 1);
    var days = (monthEndDate - monthStartDate)/(1000 * 60 * 60 * 24);
    return days;
}
    
//獲得本季度的開端月份
function getQuarterStartMonth(){
    var quarterStartMonth = 0;
    if(nowMonth<3){
        quarterStartMonth = 0;
    }
    if(2<nowMonth && nowMonth<6){
        quarterStartMonth = 3;
    }
    if(5<nowMonth && nowMonth<9){
        quarterStartMonth = 6;
    }
    if(nowMonth>8){
        quarterStartMonth = 9;
    }
    return quarterStartMonth;
}

//獲得上週的開端日期
function getLastWeekStartDate() {
    var weekStartDate = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek - 7);
    return formatDate(weekStartDate);
}
    
//獲得上週的停止日期
function getLastWeekEndDate() {
    var weekEndDate = new Date(nowYear, nowMonth, nowDay + (6 - nowDayOfWeek)-7);
    return formatDate(weekEndDate);
}

//獲得本週的開端日期
function getWeekStartDate() {
    var weekStartDate = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek);
    return formatDate(weekStartDate);
}
    
//獲得本週的停止日期
function getWeekEndDate() {
    var weekEndDate = new Date(nowYear, nowMonth, nowDay + (6 - nowDayOfWeek));
    return formatDate(weekEndDate);
}
    
//獲得本月的開端日期
function getMonthStartDate(){
    var monthStartDate = new Date(nowYear, nowMonth, 1);
    return formatDate(monthStartDate);
}
    
//獲得本月的停止日期
function getMonthEndDate(){
    var monthEndDate = new Date(nowYear, nowMonth, getMonthDays(nowMonth));
    return formatDate(monthEndDate);
}
    
//獲得上月開端時候
function getLastMonthStartDate(){
    var lastMonthStartDate = new Date(nowYear, lastMonth, 1);
    return formatDate(lastMonthStartDate);
}
    
//獲得上月停止時候
function getLastMonthEndDate(){
    var lastMonthEndDate = new Date(nowYear, lastMonth, getMonthDays(lastMonth));
    return formatDate(lastMonthEndDate);
}
    
//獲得本季度的開端日期
function getQuarterStartDate(){    
    var quarterStartDate = new Date(nowYear, getQuarterStartMonth(), 1);
    return formatDate(quarterStartDate);
}
    
//或的本季度的停止日期
function getQuarterEndDate(){
    var quarterEndMonth = getQuarterStartMonth() + 2;
    var quarterStartDate = new Date(nowYear, quarterEndMonth, getMonthDays(quarterEndMonth));
    return formatDate(quarterStartDate);
}  


//獲得上季度的開端日期
function getLastQuarterStartDate(){    
    var nowYear = now.getFullYear(); //当前年
    var qs = new Date(nowYear, getQuarterStartMonth() - 3, 1);   
    return formatDate(qs);
}
    
//或的上季度的停止日期
function getLastQuarterEndDate(){
    var quarterEndMonth = getQuarterStartMonth() - 1;
    var now = new Date();
    now.setMonth(quarterEndMonth);
    var nowYear = now.getFullYear();
    var qe = new Date(nowYear, quarterEndMonth, getMonthDays(quarterEndMonth));
    return formatDate(qe); 
}  