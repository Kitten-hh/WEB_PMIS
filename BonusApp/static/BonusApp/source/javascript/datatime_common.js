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
export function formatDate(date) {
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

export function getToday(){
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
export function getQuarterStartMonth(){
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

//獲得年的開端日期
export function getYearStartDate(year) {
    var thisYearStartDate = new Date(nowYear+year, 0, 1);
    return formatDate(thisYearStartDate);
}

//獲得年的停止日期
export function getYearEndDate(year) {
    var thisYearEndDate = new Date(nowYear+year, 11, 31);
    return formatDate(thisYearEndDate);
}

//獲得上週的開端日期
export function getLastWeekStartDate() {
    var weekStartDate = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek - 7);
    return formatDate(weekStartDate);
}
    
//獲得上週的停止日期
export function getLastWeekEndDate() {
    var weekEndDate = new Date(nowYear, nowMonth, nowDay + (6 - nowDayOfWeek)-7);
    return formatDate(weekEndDate);
}

//獲得本週的開端日期
export function getWeekStartDate() {
    var weekStartDate = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek);
    return formatDate(weekStartDate);
}
    
//獲得本週的停止日期
export function getWeekEndDate() {
    var weekEndDate = new Date(nowYear, nowMonth, nowDay + (6 - nowDayOfWeek));
    return formatDate(weekEndDate);
}
    
//獲得本月的開端日期
export function getMonthStartDate(){
    var monthStartDate = new Date(nowYear, nowMonth, 1);
    return formatDate(monthStartDate);
}
    
//獲得本月的停止日期
export function getMonthEndDate(){
    var monthEndDate = new Date(nowYear, nowMonth, getMonthDays(nowMonth));
    return formatDate(monthEndDate);
}
    
//獲得上月開端時候
export function getLastMonthStartDate(){
    var lastMonthStartDate = new Date(now.getFullYear(), now.getMonth() - 1, 1);
    return formatDate(lastMonthStartDate);
}
    
//獲得上月停止時候
export function getLastMonthEndDate(){
    //获得当前月份0-11
    var currentMonth = now.getMonth();
    //获得当前年份4位年
    var currentYear = now.getFullYear();
    var firstDay = new Date(currentYear, currentMonth, 1);

    if (currentMonth == 11) {
        currentYear++;
        currentMonth = 0; //就为
    } else {
        //否则只是月份增加,以便求的下一月的第一天
        currentMonth++;
    }
    //一天的毫秒数
    var millisecond = 1000 * 60 * 60 * 24;
    //求出上月的最后一天
    var lastMonthEndDate = new Date(firstDay - millisecond);
    return formatDate(lastMonthEndDate);
}
    
//獲得本季度的開端日期
export function getQuarterStartDate(){    
    var quarterStartDate = new Date(nowYear, getQuarterStartMonth(), 1);
    return formatDate(quarterStartDate);
}
    
//或的本季度的停止日期
export function getQuarterEndDate(){
    var quarterEndMonth = getQuarterStartMonth() + 2;
    var quarterStartDate = new Date(nowYear, quarterEndMonth, getMonthDays(quarterEndMonth));
    return formatDate(quarterStartDate);
}  


//獲得上季度的開端日期
export function getLastQuarterStartDate(){   
    /*
    var nowYear = now.getFullYear(); //当前年
    var qs = new Date(nowYear, getQuarterStartMonth() - 3, 1);   
    return formatDate(qs);*/
    return formatDate(get_last_quartely_date(Date.today())[0]); 
}
    
//或的上季度的停止日期
export function getLastQuarterEndDate(){ 
    /*
    var quarterEndMonth = getQuarterStartMonth() - 1;
    var now = new Date();
    now.setMonth(quarterEndMonth);
    var nowYear = now.getFullYear();
    var qe = new Date(nowYear, quarterEndMonth, getMonthDays(quarterEndMonth));
    */
    return formatDate(get_last_quartely_date(Date.today())[1]); 
}  


export function get_quarterly_date(currentDate) {
    var quarter = Math.ceil((currentDate.getMonth() + 1)/3)
    var qbdate = new Date(currentDate.getFullYear(), 3 * quarter - 3, 1);    
    var month = 3 * quarter
    var remaining = parseInt(month / 12)
    var qedate = new Date(currentDate.getFullYear() + remaining, month % 12, 1).addDays(-1);    
    return [qbdate, qedate]
}

export function get_last_quartely_date (currentDate) {
    var lastQuarterFirstDay = new Date(currentDate.getFullYear() , currentDate.getMonth() - 3 , 1);
    return get_quarterly_date(lastQuarterFirstDay)
}