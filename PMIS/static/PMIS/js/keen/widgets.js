var Widgets = function () {

    var displayWidget1 = function (options) {
        if (!document.getElementById(options.elementId)) {
            return;
        }

        top.window.IndexClass.getDataFromRestAPI(options).then((data) => {
            var totalNum = 0;
            var maxNum = 0;
            for (var i = 0; i < data.length; i++) {
                totalNum = totalNum + data[i][options.displayField];
                if (maxNum < data[i][options.displayField])
                    maxNum = data[i][options.displayField]
            }
            for (var i = 0; i < data.length; i++) {
                var num = data[i][options.displayField];
                var ratio = parseInt(num / maxNum * 100);
                data[i].ratio = ratio;
            }
            var html = "<div class=\"k-widget-19__title\"> \r\n" +
                "    <div class=\"k-widget-19__label\">" + totalNum + "</div>\r\n" +
                "    <img class=\"k-widget-19__bg\" src=\"assets/media/misc/iconbox_bg.png\" alt=\"bg\">\r\n" +
                "</div>" +
                "<div class=\"k-widget-19__data\">\r\n" +
                "    <div class=\"k-widget-19__chart\">\r\n";
            for (var i = 0; i < data.length; i++) {
                html = html +
                    "        <div class=\"k-widget-19__bar\">\r\n" +
                    "              <div class=\"k-widget-19__bar-" + data[i].ratio + "\" data-toggle=\"k-tooltip\" data-skin=\"brand\" data-placement=\"top\" title=\"\" data-original-title=\"" +
                    data[i][options.displayField] + "\"></div>\r\n" +
                    "        </div>\r\n";
            }
            html = html + "</div>";
            $("#" + options.elementId).empty().html(html);
            KApp.initTooltips();
        });
    }

    var displayWidget2 = function (options) {
        if (!document.getElementById(options.elementId)) {
            return;
        }

        if ($("#" + options.elementId + " .k_widget_chart").length == 0)
            return;

        top.window.IndexClass.getDataFromRestAPI(options).then((data) => {
            var totalNum = 0;
            var dataA = {
                data: [],
                labels: [],
                colors: [],
                colorName: []
            }
            for (var i = 0; i < data.length; i++) {
                totalNum = totalNum + data[i][options.dataField]
                dataA.data.push(data[i][options.dataField]);
                dataA.labels.push(data[i][options.labelField]);
                if (i < 4) {
                    dataA.colors.push(KApp.getBaseColor("shape", i + 1));
                    dataA.colorName.push("k-shape-bg-color-" + (i + 1));
                }
                else if (i < 8)
                    dataA.colors.push(KApp.getBaseColor("label", i - 3))
                
                else
                    dataA.colors.push(KApp.getBaseColor("shape", (i + 1) % 4));
                
            }
            $("#" + options.elementId + " .k-widget-21__label").text(totalNum);
            var html = "";
            for (var j = 0; j < dataA.labels.length; j++) {
                html = html + "<div class=\"k-widget-21__legend\"> <i class=\"" + dataA.colorName[j] + "\"></i> <span>" + dataA.labels[j] + "</span> </div>\r\n";
            }
            $("#" + options.elementId + " .k-widget-21__legends").empty().html(html);
            var config = {
                type: 'doughnut',
                data: {
                    datasets: [{
                        data: dataA.data,
                        backgroundColor: dataA.colors
                    }],
                    labels: dataA.labels
                },
                options: {
                    cutoutPercentage: 75,
                    responsive: true,
                    maintainAspectRatio: false,
                    legend: {
                        display: false,
                        position: 'top',
                    },
                    title: {
                        display: false,
                        text: 'Technology'
                    },
                    animation: {
                        animateScale: true,
                        animateRotate: true
                    },
                    tooltips: {
                        enabled: true,
                        intersect: false,
                        mode: 'nearest',
                        bodySpacing: 5,
                        yPadding: 10,
                        xPadding: 10,
                        caretPadding: 0,
                        displayColors: false,
                        backgroundColor: KApp.getStateColor('brand'),
                        titleFontColor: '#ffffff',
                        cornerRadius: 4,
                        footerSpacing: 0,
                        titleSpacing: 0
                    }
                }
            };

            var ctx = $("#" + options.elementId + " .k_widget_chart").get(0).getContext('2d');
            var myDoughnut = new Chart(ctx, config);
        });
    }

    var displayWidget3 = function (options) {
        if (!document.getElementById(options.elementId)) {
            return;
        }

        if ($("#" + options.elementId + " .k_widget_chart").length == 0)
            return;

        top.window.IndexClass.getDataFromRestAPI(options).then((data) => {
            var max = 0;
            var totalNum = 0;
            var dataA = {
                data: [],
                labels: []
            }

            for (var i = 0; i < data.length; i++) {
                totalNum = totalNum + data[i][options.dataField]
                if (max < data[i][options.dataField])
                    max = data[i][options.dataField];
                dataA.data.push(data[i][options.dataField]);
                dataA.labels.push(data[i][options.labelField]);
            }
                      

            // Main chart
            var color = KApp.getStateColor('brand');
            var ctx = $("#" + options.elementId + " .k_widget_chart").get(0).getContext('2d');
            var gradient = ctx.createLinearGradient(0, 0, 0, 120);
            gradient.addColorStop(0, Chart.helpers.color(color).alpha(0.3).rgbString());
            gradient.addColorStop(1, Chart.helpers.color(color).alpha(0).rgbString());

            var data = dataA.data;
            $("#" + options.elementId + " .k-widget-20__label").text(totalNum);
            var mainConfig = {
                type: 'line',
                data: {
                    labels: dataA.labels,
                    datasets: [{
                        label: options.dataField,//'Task Qty',
                        borderColor: color,
                        borderWidth: 3,
                        backgroundColor: gradient,
                        pointBackgroundColor: KApp.getStateColor('brand'),
                        data: data,
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    title: {
                        display: false,
                        text: 'Stacked Area'
                    },
                    tooltips: {
                        enabled: true,
                        intersect: false,
                        mode: 'nearest',
                        bodySpacing: 5,
                        yPadding: 10,
                        xPadding: 10,
                        caretPadding: 0,
                        displayColors: false,
                        backgroundColor: KApp.getStateColor('brand'),
                        titleFontColor: '#ffffff',
                        cornerRadius: 4,
                        footerSpacing: 0,
                        titleSpacing: 0
                    },
                    legend: {
                        display: false,
                        labels: {
                            usePointStyle: false
                        }
                    },
                    hover: {
                        mode: 'index'
                    },
                    scales: {
                        xAxes: [{
                            display: false,
                            scaleLabel: {
                                display: false,
                                labelString: 'Month'
                            },
                            ticks: {
                                display: false,
                                beginAtZero: true,
                            }
                        }],
                        yAxes: [{
                            display: false,
                            scaleLabel: {
                                display: false,
                                labelString: 'Value'
                            },
                            gridLines: {
                                color: '#eef2f9',
                                drawBorder: false,
                                offsetGridLines: true,
                                drawTicks: false
                            },
                            ticks: {
                                max: max,
                                display: false,
                                beginAtZero: true
                            }
                        }]
                    },
                    elements: {
                        point: {
                            radius: 0,
                            borderWidth: 0,
                            hoverRadius: 0,
                            hoverBorderWidth: 0
                        }
                    },
                    layout: {
                        padding: {
                            left: 0,
                            right: 0,
                            top: 0,
                            bottom: 0
                        }
                    }
                }
            };

            var chart = new Chart(ctx, mainConfig);

            // Update chart on window resize
            KUtil.addResizeHandler(function () {
                chart.update();
            });
        });
    }

    var displayPlanningActual = function (options) {
        if (!document.getElementById(options.elementId)) {
            return;
        }

        top.window.IndexClass.getDataFromRestAPI(options).then((data) => {
            var color = Chart.helpers.color;
            var MaxNum = 0;
            //將數據分組
            var dataMap = new Map();
            for (var key in options.groups) {
                dataMap.set(key, {
                    label: key,
                    backgroundColor: color(KApp.getStateColor(top.window.IndexClass.getColor().replace("bg-", ""))).alpha(1).rgbString(),
                    borderWidth: 0,
                    data: []
                });
            }
            var labels = [];
            for (var i = 0; i < data.length; i++) {

                dataMap.forEach((value, key, dataMap) => {
                    value.data.push(data[i][options.groups[key]]);
                    if (MaxNum < data[i][options.groups[key]])
                        MaxNum = data[i][options.groups[key]];
                });
                labels.push(data[i][options.labelField]);
            }
            var barChartData = {
                labels: labels,
                datasets: Array.from(dataMap.values())
            }

            var html = "";
            for (var key in options.groups) {
                html +=
                    "<div class=\"k-widget-9__legend\">\r\n" +
                    "   <div class=\"k-widget-9__legend-bullet\"  style=\"background-color:"+dataMap.get(key).backgroundColor+" !important\"></div>\r\n" +
                    "   <div class=\"k-widget-9__legend-label\">" + key + "</div>\r\n" +
                    "</div>\r\n";
            }
            $("#"+options.elementId + " .k-widget-9__legends").empty().html(html);
            //生成圖表
            var canvas = $("#" + options.elementId + " .k_widget_chart");
            var ctx = canvas[0].getContext('2d');
            var oldBar = canvas.data("bar");
            if (oldBar != undefined)
                oldBar.destroy();            
            var myBar = new Chart(ctx, {
                type: 'bar',
                data: barChartData,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    legend: false,
                    scales: {
                        xAxes: [{
                            categoryPercentage: 0.35,
                            barPercentage: 0.70,
                            display: true,
                            scaleLabel: {
                                display: false,
                                labelString: 'Month'
                            },
                            gridLines: false,
                            ticks: {
                                display: true,
                                beginAtZero: true,
                                fontColor: KApp.getBaseColor('shape', 3),
                                fontSize: 13,
                                padding: 10
                            }
                        }],
                        yAxes: [{
                            categoryPercentage: 0.35,
                            barPercentage: 0.70,
                            display: true,
                            scaleLabel: {
                                display: false,
                                labelString: 'Value'
                            },
                            gridLines: {
                                color: KApp.getBaseColor('shape', 2),
                                drawBorder: false,
                                offsetGridLines: false,
                                drawTicks: false,
                                borderDash: [3, 4],
                                zeroLineWidth: 1,
                                zeroLineColor: KApp.getBaseColor('shape', 2),
                                zeroLineBorderDash: [3, 4]
                            },
                            ticks: {
                                max: MaxNum,
                                stepSize: 10000,
                                display: true,
                                beginAtZero: true,
                                fontColor: KApp.getBaseColor('shape', 3),
                                fontSize: 13,
                                padding: 10
                            }
                        }]
                    },
                    title: {
                        display: false
                    },
                    hover: {
                        mode: 'index'
                    },
                    tooltips: {
                        enabled: true,
                        intersect: false,
                        mode: 'nearest',
                        bodySpacing: 5,
                        yPadding: 10,
                        xPadding: 10,
                        caretPadding: 0,
                        displayColors: false,
                        backgroundColor: KApp.getStateColor('brand'),
                        titleFontColor: '#ffffff',
                        cornerRadius: 4,
                        footerSpacing: 0,
                        titleSpacing: 0
                    },
                    layout: {
                        padding: {
                            left: 0,
                            right: 0,
                            top: 5,
                            bottom: 5
                        }
                    }
                }
            });
            canvas.data("bar", myBar);
        });
    }

    return {
        init: function () {
            var options = {
                elementId: "oneAndHalfM_FTask",
                url: "http://www.cyber-access.com:3200/PMSService/M_PMS/V_Analysis_OneAndHalfM_FTask/_search",
                query: { "query": "['Weekly','<>',]" },
                displayField: "Task_Qty",
                sort: "Weekly"
            }
            var options2 = {
                elementId: "k-widget-21-staff-quarterly",
                url: "http://www.cyber-access.com:3200/PMSService/M_PMS/V_Analysis_MainStaffQNoFTask/_search",
                query: { "query": "['Contact','<>',]" },
                dataField: "Task_Qty",
                labelField: "Contact"
            }

            var options3 = {
                elementId: "quarterly_newTask",
                url: "http://www.cyber-access.com:3200/PMSService/M_PMS/V_Analysis_Quarterly_Weely_NewTask/_search",
                query: { "query": "['Weekly','<>',]" },
                dataField: "Task_Qty",
                labelField: "Weekly"
            }
            var optons4 = {
                elementId: "k_chart_PA_Task",
                url: "http://www.cyber-access.com:3200/PMSService/M_PMS/V_Analysis_PlanningActual/_search",
                query: { "query": "['RDate','<>',]" },
                groups: { Planning: "PTask_Qty", Actacl: "ATask_Qty" },
                labelField: "RDate",
                sort:"RDate"
            }
            var optons5 = {
                elementId: "k_chart_PY_Sales",
                url: "/PMIS/sale/sales_dashboard/getPastYearSales",
                query: { "query": "['Order_Month','<>',]" },
                displayField: "order_qty",
                sort: "order_month"
            }
            var options6 = {
                elementId: "k_chart_PY_Sales_Cust",
                url: "http://www.cyber-access.com:3200/VCAsiaSZService/VCAsia_db/V_Sales_PastYear_Cust/_search",
                query: { "query": "['CustNo','<>',]" },
                dataField: "Total_Qty",
                labelField: "CustNo"
            }
            var options7 = {
                elementId: "k_chart_PY_Sales_Quarter",
                url: "http://www.cyber-access.com:3200/VCAsiaSZService/VCAsia_db/V_Sales_Quarter/_search",
                query: { "query": "['Weekly','<>',]" },
                dataField: "Order_Qty",
                labelField: "Weekly", 
                sort:"Weekly" 
            }
            var optons8 = {
                elementId: "k_chart_PY_OrderState",
                url: "http://www.cyber-access.com:3200/VCAsiaSZService/VCAsia_db/V_Sales_PastYear/_search",
                query: { "query": "['Order_Month','<>',]" },
                groups: { Order: "Order_Qty", Shipment: "Ship_Qty" },
                labelField: "Order_Month",
                sort:"Order_Month"
            }
            displayWidget1(options);
            displayWidget2(options2);
            displayWidget3(options3);
            displayPlanningActual(optons4);
            
            displayWidget1(optons5);
            displayWidget2(options6);
            displayWidget3(options7);
            displayPlanningActual(optons8);
        }
    }
}();

jQuery(document).ready(function () {
    Widgets.init();
});