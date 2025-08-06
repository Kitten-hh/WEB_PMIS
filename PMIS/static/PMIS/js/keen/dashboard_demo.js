var dashboard_demo = function() {
   return {
       init:function() {
           var optons5 = {
               elementId: "k_chart_PY_Sales",
               url: "/PMIS/sale/sales_dashboard/getPastYearSales",
               query: { "query": "['Order_Month','<>',]" },
               displayField: "order_qty",
               sort: "order_month"
           }           
           var options7 = {
                elementId: "k_chart_PY_Sales_Quarter",
                url: "/PMIS/sale/sales_dashboard/getQuarterSales",
                query: { "query": "['Weekly','<>',]" },
                dataField: "order_qty",
                labelField: "weekly", 
                sort:"weekly" 
            }           
            var options8 = {
                elementId:"k-widget-slider-weekly-shipment",
                url: "/PMIS/sale/sales_dashboard/getWeeklyShipment",
                query:{"query": "['CustNo','<>',]"},
                titleFields:"custname",
                descFields:"shipno,creator,amount",
                footFields:"shipdate",  
                sort:"shipdate Desc"
            } 
            var options9 = {
                elementId:"k-widget-top-customer",
                url: "/PMIS/sale/sales_dashboard/getSalesCustAnalysis",
                query:{"query": "['CustNo','<>',]"},
                tabField:"stype",
                titleField:"custno",
                descField:"custname",
                progressField:"increase"
            }  
            var optons10 = {
                elementId: "k_chart_PY_OrderState",
                url: "/PMIS/sale/sales_dashboard/getOrderState",
                query: { "query": "['Order_Month','<>',]" },
                groups: { Order: "order_qty", Shipment: "ship_qty" },
                labelField: "order_month",
                sort:"order_month"
            }            
            var options11 = {
                elementId:"display_latest_orders",
                url: "/PMIS/sale/sales_dashboard/getSaleOrderList",
                query:{"query": "['OrderNo','<>',]"},
                tabField:"tabtype",
                tabSort:"Today,Week,Month",
                showTab:"Month",
                descFields:"orderno,custno,custname,amount",
                remarkFields:"orderdate",
                sort:"orderdate desc"
            }            
            var options2 = {
                elementId: "k_top_product_search",                    
                url: "/PMIS/sale/sales_dashboard/product_search",
                query:{"query": "['PartNo','<>',]"},
                columns:[
                    {field:"partno", title:"產品編號",width:"120",textAlign:"left"},
                    {field:"orders", title:"數量",width:"60",textAlign:"left"},
                    {field:"description", title:"描述",width:"300",textAlign:"left"},
                    {field:"custpn",title:"客號",width:"150",textAlign:"left"},
                    {field:"bdate", title:"早期下單日期",width:"100",textAlign:"left"},
                    {field:"edate", title:"最後下單日期",width:"100",textAlign:"left"}
                ]
            }            
            var options12 = {
                elementId: "k-widget-slider-newproject",
                url: "/PMIS/sale/sales_dashboard/getNewProduct",
                query:{"query": "['PartNo','<>',]"},
                titleField:"partno",
                descField:"description",
                purchasesField:"orders",
                createDateField:"create_date"
            }            
           ComponentClass.displayWidget1(optons5);
           ComponentClass.displayWidget3(options7);
           ComponentClass.displayWidgetTab3(options8);
           ComponentClass.displayWidgetTabTop(options9);
           ComponentClass.displayPlanningActual(optons10);
           ComponentClass.displayLatestTask(options11);
           ComponentClass.displayBothTable(options2);
           ComponentClass.displayWidgetTabNew(options12);
       }
   }
}();

jQuery(document).ready(function () {
    dashboard_demo.init();
});