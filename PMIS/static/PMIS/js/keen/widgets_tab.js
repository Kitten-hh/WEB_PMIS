var WidgetTab = function() {

    var displayWidgetTab2 = function(options) {
        if (!document.getElementById(options.elementId)) {
            return;
        }

        top.window.IndexClass.getDataFromRestAPI(options).then((data)=>{
            var html = "";
            for(var i = 0; i < data.length; i++) {
                html = html + 
                "<div class=\"carousel-item ";
                if (i == 0)
                    html = html + " active ";
                html = html + "k-slider__body\">\r\n"+
                "    <div class=\"k-widget-13\">\r\n"+
                "        <div class=\"k-widget-13__body\">\r\n"+
                "            <a class=\"k-widget-13__title\" href=\"#\">" + data[i][options.titleField] + "</a> \r\n"+
                "            <div class=\"k-widget-13__desc\">"+ data[i][options.descField] + "</div>\r\n"+
                "        </div>\r\n"+
                "        <div class=\"k-widget-13__foot\">\r\n"+
                "            <div class=\"k-widget-13__progress\">\r\n"+
                "                <div class=\"k-widget-13__progress-info\">\r\n"+
                "                    <div class=\"k-widget-13__progress-status\"> Progress </div>\r\n"+
                "                    <div class=\"k-widget-13__progress-value\">"+ data[i][options.progressField]+"%</div>\r\n"+
                "                </div>\r\n"+
                "                <div class=\"progress\">\r\n"+
                "                    <div class=\"progress-bar k-bg-brand\" role=\"progressbar\" style=\"width: "+ data[i][options.progressField]+"%\"  "+
                "                    aria-valuenow=\""+data[i][options.progressField]+"\" aria-valuemin=\"0\" aria-valuemax=\"100\"></div>\r\n"+
                "                </div>\r\n"+
                "            </div>\r\n"+
                "        </div>\r\n"+
                "    </div>\r\n"+
                "</div>\r\n";
            }

            $("#"+ options.elementId + " .carousel-inner").empty().html(html);
        });        
    }

    var displayWidgetTab3 = function(options) {
        if (!document.getElementById(options.elementId)) {
            return;
        }

        top.window.IndexClass.getDataFromRestAPI(options).then((data)=>{
            var html = "";
            for(var i = 0; i < data.length; i++) {
                var title = "", desc = "", footDesc = "";
                var titleFields = options.titleFields.split(",");
                var descFields = options.descFields.split(",");
                var footFields = options.footFields.split(",");

                for(var j = 0; j < titleFields.length; j++) 
                    title = title + data[i][titleFields[j]] +  "  ";
                for(var j = 0; j < descFields.length; j++) 
                    desc = desc + data[i][descFields[j]] + "  ";
                for(var j = 0; j < footFields.length; j++)
                    footDesc = footDesc + data[i][footFields[j]] + "  ";
                html = html + 
                "<div class=\"carousel-item ";
                if (i == 0)
                    html = html + " active ";
                html = html + "k-slider__body\">\r\n"+
                "    <div class=\"k-widget-13\">\r\n"+
                "        <div class=\"k-widget-13__body\">\r\n"+
                "            <a class=\"k-widget-13__title\" href=\"#\">" + title + "</a> \r\n"+
                "            <div class=\"k-widget-13__desc\">" + desc + "</div>\r\n"+
                "        </div>\r\n"+
                "        <div class=\"k-widget-13__foot\">\r\n"+
                "            <div class=\"k-widget-13__label\"> <span class=\"k-label-font-color-2\">" + footDesc + "</span> </div>\r\n"+
                "            <div class=\"k-widget-13__toolbar\"> <a href=\"#\" class=\"btn btn-default btn-sm btn-bold btn-upper\">View Detail</a> </div>\r\n"+
                "        </div>\r\n"+
                "    </div>\r\n"+
                "</div>\r\n";
            }

            $("#"+ options.elementId + " .carousel-inner").empty().html(html);
        });             
    }

    var displayWidgetTabTop = function(options) {
        if (!document.getElementById(options.elementId)) {
            return;
        }

        top.window.IndexClass.getDataFromRestAPI(options).then((data)=>{
            var tabData = new Map();
            for(var i = 0; i < data.length; i++) {
                var tab = data[i][options.tabField];
                if (!tabData.has(tab))
                    tabData.set(tab, []);
                tabData.get(tab).push(data[i]);
            }
            var navHtml = "";
            var contentHtml = "";
            var index = 0;
            tabData.forEach((value, key, tabData)=>{
                index++;
                var tabId = options.elementId + "_tab_" + index;
                navHtml = navHtml +
                "<li class=\"nav-item\">\r\n"+
                "<a class=\"nav-link "
                if (index == 1)
                    navHtml += "active ";
                navHtml += "\" data-toggle=\"tab\" href=\"#" + tabId + "\" role=\"tab\">\r\n"+
                "    <span class=\"nav-link-icon\"><i class=\"flaticon2-graphic\"></i></span>\r\n"+
                "    <span class=\"nav-link-title\">" + key + "</span> \r\n"+
                "</a>\r\n"+
                "</li>\r\n";
                contentHtml +=
                "<div class=\"tab-pane fade active show\" id=\"" + tabId +"\" role=\"tabpanel\">\r\n";
                for(var i = 0; i < value.length; i++) {
                    contentHtml +=
                    "<div class=\"k-widget-1__item\">\r\n"+
                    "    <div class=\"k-widget-1__item-info\">\r\n"+
                    "        <a href=\"#\" class=\"k-widget-1__item-title\">"+value[i][options.titleField] + "</a> \r\n"+
                    "        <div class=\"k-widget-1__item-desc\">" + value[i][options.descField]+ "</div>\r\n"+
                    "    </div>\r\n"+
                    "    <div class=\"k-widget-1__item-stats\">\r\n"+
                    "        <div class=\"k-widget-1__item-value\">"+ value[i][options.progressField] + "%</div>\r\n"+
                    "        <div class=\"k-widget-1__item-progress\">\r\n"+
                    "            <div class=\"progress\">\r\n"+
                    "                <div class=\"progress-bar "+top.window.IndexClass.getColor()+"\" role=\"progressbar\" style=\"width: "+ value[i][options.progressField] + "%;\" aria-valuenow=\""+ (100 - value[i][options.progressField]) + "\" aria-valuemin=\"0\" aria-valuemax=\"100\"></div>\r\n"+
                    "            </div>\r\n"+
                    "        </div>\r\n"+
                    "    </div>\r\n"+
                    "</div>\r\n";
                }
                contentHtml += "</div>\r\n";
            });
            $("#"+ options.elementId + " .nav").empty().html(navHtml);
            $("#"+ options.elementId + " .tab-content").empty().html(contentHtml);
        });         
    }
    var displayLatestTask = function(options) {
        if (!document.getElementById(options.elementId)) {
            return;
        }

        top.window.IndexClass.getDataFromRestAPI(options).then((data)=>{
            var tabData = new Map();        
            var tabFieldArr = options.tabSort.split(",");
            for(var tab of tabFieldArr)
                tabData.set(tab, []);
            for(var i = 0; i < data.length; i++) {
                var tab = data[i][options.tabField];
                if (tabData.has(tab))
                    tabData.get(tab).push(data[i]);
            }
            var navHtml = "";
            var contentHtml = "";
            var index = 0;
            tabData.forEach((value, key, tabData)=>{
                index++;
                var id = options.elementId + "_tab_" + index;
                navHtml +=
                "<li class=\"nav-item\"> <a class=\"nav-link "
                if (index == 1)
                    navHtml += " active show ";
                navHtml +=
                "\" data-toggle=\"tab\" href=\"#"+ id +
                "\" role=\"tab\" aria-selected=\"false\">" + key + "</a> </li>";

                contentHtml += "<div class=\"tab-pane fade "
                if (index == 1)
                    contentHtml += " active show "
                contentHtml += "\" id=\""+id+"\" role=\"tabpanel\">\r\n";
                //contentHtml += "<div data-scroll=\"true\" class=\"k-scroll ps ps--active-y\" style=\"height: 300px; overflow: hidden;\">";
                contentHtml += "    <div class=\"k-widget-5\">\r\n";
                for(var i = 0; i < value.length; i++) {
                    var descFieldArr = options.descFields.split(",");
                    var remarkFieldArr = options.remarkFields.split(",");
                    var desc = "", remark = "";
                    for(var field of descFieldArr)
                        desc += value[i][field] + " ";
                    for(var field of remarkFieldArr)
                        remark += value[i][field] + " ";
                    contentHtml +=
                        "        <div class=\"k-widget-5__item k-widget-5__item--info\">\r\n"+
                        "            <div class=\"k-widget-5__item-info\">\r\n"+
                        "                <a href=\"#\" class=\"k-widget-5__item-title\">" +desc+ "</a> \r\n"+
                        "                <div class=\"k-widget-5__item-datetime\">" +remark+ "</div>\r\n"+
                        "            </div>\r\n"+
                        "            <div class=\"k-widget-5__item-check\">\r\n"+
                        "                <a href=\"#\" class=\"btn btn-default btn-sm btn-bold btn-upper\">View Detail</a> "+
                        "            </div>\r\n"+
                        "        </div>\r\n"
                }
                contentHtml += "    </div>";
                //contentHtml += "</div>";
                contentHtml += "</div>";
            });

            $("#"+options.elementId + " .nav-tabs").empty().html(navHtml);
            $("#"+options.elementId + " .tab-content").empty().html(contentHtml);
        });
    }
    return {        
        init:function() {
            var options = {
                elementId:"k-widget-slider-project",
                url:"http://www.cyber-access.com:3200/PMSService/M_PMS/V_Analysis_Quarterly_Critical/_search",
                query:{"query": "['RecordId','<>',]"},
                titleField:"RecordId",
                descField:"ProjectName",
                progressField:"Progress"
            }    

            var options3 = {
                elementId:"k-widget-slider-today-schedule",
                url:"http://www.cyber-access.com:3200/PMSService/M_PMS/V_Analysis_Today_Schedule/_search",
                query:{"query": "['Contact','<>',]"},
                titleFields:"TaskNo,Contact,Progress,SchPriority",
                descFields:"Task",
                footFields:"PlanBDate,PlanEDate",
                sort:"SchPriority Desc"
            }               

            var options2 = {
                elementId:"k-widget-slider-yesterday-ftask",
                url:"http://www.cyber-access.com:3200/PMSService/M_PMS/V_Analysis_Yesterday_FTasks/_search",
                query:{"query": "['Contact','<>',]"},
                titleFields:"TaskNo,Contact,Progress,SchPriority",
                descFields:"Task",
                footFields:"PlanBDate,PlanEDate",
                sort:"SchPriority Desc"
            }               

            var options4 = {
                elementId:"k-widget-top-project",
                url:"http://www.cyber-access.com:3200/PMSService/M_PMS/V_Analysis_Top_Projects/_search",
                query:{"query": "['RecordId','<>',]"},
                tabField:"SType",
                titleField:"RecordId",
                descField:"ProjectName",
                progressField:"Progress"
            }               
            var options5 = {
                elementId:"display_latest_tasks",
                url:"http://www.cyber-access.com:3200/PMSService/M_PMS/V_Analysis_LatestTask/_search",
                query:{"query": "['Contact','<>',]"},
                tabField:"TabType",
                tabSort:"Today,Week,Month",
                descFields:"Task",
                remarkFields:"TaskNo,AddDate,Contact,Progress",
                sort:"AddDate Desc"
            }     
            var options6 = {
                elementId:"k-widget-slider-customer",
                url: "http://www.cyber-access.com:3200/VCAsiaSZService/VCAsia_db/V_Sales_Customer_ShipmentProgress/_search",
                query:{"query": "['CustNo','<>',]"},
                titleField:"CustNo",
                descField:"CustName",
                progressField:"Progress"
            } 
            var options7 = {
                elementId:"k-widget-slider-weekly-orders",
                url: "http://www.cyber-access.com:3200/VCAsiaSZService/VCAsia_db/V_Sales_Weekly_NewOrder/_search",
                query:{"query": "['CustNo','<>',]"},
                titleFields:"CustName",
                descFields:"OrderNo,CREATOR,Amount",
                footFields:"OrderDate,ReqDate", 
                sort:"OrderDate Desc"
            } 
            var options8 = {
                elementId:"k-widget-slider-weekly-shipment",
                url: "http://www.cyber-access.com:3200/VCAsiaSZService/VCAsia_db/V_Sales_Weekly_Shipment/_search",
                query:{"query": "['CustNo','<>',]"},
                titleFields:"CustName",
                descFields:"ShipNo,CREATOR,Amount",
                footFields:"Shipdate",  
                sort:"Shipdate Desc"
            } 
            var options9 = {
                elementId:"k-widget-top-customer",
                url: "http://www.cyber-access.com:3200/VCAsiaSZService/VCAsia_db/V_Sales_Cust_Analysis/_search",
                query:{"query": "['CustNo','<>',]"},
                tabField:"SType",
                titleField:"CustNo",
                descField:"CustName",
                progressField:"Increase"
            }  
            var options10 = {
                elementId:"display_latest_orders",
                url: "http://www.cyber-access.com:3200/VCAsiaSZService/VCAsia_db/V_Sales_OrderList/_search",
                query:{"query": "['OrderNo','<>',]"},
                tabField:"TabType",
                tabSort:"Today,Week,Month",
                descFields:"OrderNo,CustNo,CustName,Amount",
                remarkFields:"OrderDate",
                sort:"OrderDate Desc"
            }
            displayWidgetTab2(options);
            displayWidgetTab3(options2);
            displayWidgetTab3(options3);
            displayWidgetTabTop(options4);
            displayLatestTask(options5);
            
            displayWidgetTab2(options6);
            displayWidgetTab3(options7);
            displayWidgetTab3(options8);
            displayWidgetTabTop(options9);
            displayLatestTask(options10);
        }
    }
}();

jQuery(document).ready(function(){
    WidgetTab.init();
});