var lead_menu = function() {
    
    return {
        init:function() {   
            $('title').html('BonusSimulationApp')
            //設置MenuItem
            SWNavigationBar.setMenuItem("mi_1","HOME","/bonus/bonus_analysis_page/");
            SWNavigationBar.setMenuItem("mi_2","Dash Board","/bonus/spectaculars/");
            SWNavigationBar.setMenuItem("mi_3","TaskType Management","/bonus/tasktype");
            SWNavigationBar.setMenuItem("mi_4","Bonus Parameter Setting ","/bonus/user_bonusparams_index");
            SWNavigationBar.setMenuItem("mi_5","Bonus Statistics","/bonus/get_bonus_stats/");
            SWNavigationBar.setMenuItem("mi_6","Task Search","/bonus/task_search");
            //SWNavigationBar.setMenuItem("mi_7","Layout Test","/bonus/test_page_layout/");
            SWNavigationBar.setLogoUrl("/looper");
        }
    }
 }();
 
 //自動加載
 jQuery(document).ready(function () {
    //調用以上定義的Init方法
    lead_menu.init();
    //base_menu.setKeenMeun();
 });