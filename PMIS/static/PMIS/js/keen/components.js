var ComponentClass = function() {
    var colors = ["bg-accent","bg-brand","bg-danger","bg-focus","bg-info","bg-light","bg-metal","bg-primary","bg-success","bg-warning"];

    var getColor = function() {
        var index = KUtil.getRandomInt(0,colors.length-1);
        return colors[index];
    }

    var getDataFromURL = function(options) {
        var localAjaxType = "get";
        if (options.ajaxType != undefined)
            localAjaxType = options.ajaxType;
        var deferred = $.Deferred();
        $.ajax({
            url: options.url,
            type: localAjaxType,    
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(options.query),
            success: function (resultData) {
                if (resultData.code == 0) {
                    //是否需要排序
                    if (options.sort != undefined) {
                        var arr = options.sort.split(" ");
                        var field = arr[0];
                        var isDesc = false;
                        if (arr.length == 2 && arr[1].toLowerCase() == "desc")
                            isDesc = true;
                        //對數據進行排序
                        resultData.data.sort(function (a, b) {
                            if (a[field] < b[field])
                                return isDesc ? 1 : -1;
                            if (a[field] > b[field])
                                return isDesc ? -1 : 1;
                            return 0;
                        });
                    }
                    deferred.resolve(resultData.data);
                } else {
                    alert("訪問數據失敗，請檢查傳入參數是否正確");
                }
            }
        });
        return deferred.promise();
    }    

    var numberDataType = ["numeric","float","int"];
    var initColumns = function(options) {
        var deferred = $.Deferred();
        if (!options.gen_columns && options.hasOwnProperty("columns"))
            return deferred.resolve(options.columns);
        var localOptions = $.extend(true, {}, options);
        localOptions.query = {};
        var columns = [];
        //判斷是否初始化字段信息
        var isInitColumn = $("#" + localOptions.elementId).attr("isInitColumn") == "Y"
        if (!isInitColumn) {
            var url = localOptions.url;
            if (url.endsWith("/"))
                url = url.substr(0, url.length - 2);
            url = url.substr(0, url.lastIndexOf("/")+1) + "_mappings";
            localOptions.url = url;
            localOptions.ajaxType = "get";
            getDataFromURL(localOptions).then((data)=>{
                var custColumns = localOptions.columns;
                var destColumns;
                if (options.query != undefined && options.query.source != undefined)
                    destColumns = options.query.source;
                for(var i = 0; i < data.length; i++) {
                    if (destColumns != undefined && destColumns.indexOf(data[i].ColumnName) == -1)
                        continue;
                    var title = data[i].Description;
                    var sortable = "asc";
                    var width =  80; //默認30;
                    var type = "string";
                    if (numberDataType.indexOf(data[i].DataType) >= 0) {
                        width = 80;
                        type = "number";
                    }
                    else if (data[i].DataType == "datetime") {
                        width = 80;
                        type = "date";
                    }
                    else
                        width = data[i].Length > 200 ? 200 : data[i].Length < 80 ? 80 : data[i].Length;
                    var textAlign = "center";
                    var template;
                    if (custColumns != undefined && custColumns[data[i].ColumnName] != undefined) {
                        var custCol = custColumns[data[i].ColumnName];
                        if (custCol.title != undefined)
                            title = custCol.title;
                        if (custCol.sortable != undefined)
                            sortable = custCol.sortable;
                        if (custCol.width != undefined)
                            width = custCol.width;
                        if (custCol.type != undefined)
                            type = custCol.type;
                        if (custCol.textAlign != undefined)
                            textAlign = custCol.textAlign;
                        if (custCol.template != undefined)
                            template = custCol.template;
                    }
                    var col = {
                        field: data[i].ColumnName,
                        title: title,
                        sortable: sortable,
                        width: width,
                        type: type,
                        selector: false,
                        textAlign: textAlign
                    }
                    if (type == "date") {
                        col.format = 'YYYYMMDD'
                        col.template = function(row) {
                            return moment(row[this.field]).format(this.format);
                        }
                    }
                    if (template != undefined) {
                        col.template = template;
                    }
                    columns.push(col);
                }

                $("#" + localOptions.elementId).attr("isInitColumn", "Y");
                $("#" + localOptions.elementId).data("columns", columns);
                deferred.resolve(columns);
            });
        }else 
            deferred.resolve($("#" + localOptions.elementId).data("columns"));
        return deferred.promise();
    }


    var displayWidget1 = function (options) {
        if (!document.getElementById(options.elementId)) {
            return;
        }

        getDataFromURL(options).then((data) => {
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

        getDataFromURL(options).then((data) => {
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

        getDataFromURL(options).then((data) => {
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

        getDataFromURL(options).then((data) => {
            var color = Chart.helpers.color;
            var MaxNum = 0;
            //將數據分組
            var dataMap = new Map();
            for (var key in options.groups) {
                dataMap.set(key, {
                    label: key,
                    backgroundColor: color(KApp.getStateColor(getColor().replace("bg-", ""))).alpha(1).rgbString(),
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

    var displayWidgetTab2 = function(options) {
        if (!document.getElementById(options.elementId)) {
            return;
        }

        getDataFromURL(options).then((data)=>{
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

        getDataFromURL(options).then((data)=>{
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

    var displayWidgetTabNew = function(options) {
        if (!document.getElementById(options.elementId)) {
            return;
        }

        getDataFromURL(options).then((data)=>{
            var html = "";
            for(var i = 0; i < data.length; i++) {
                html = html + 
                "<div class=\"carousel-item ";
                if (i == 0)
                    html = html + " active ";
                html = html + `">
                <div class="k-widget-14__body">
                    <div class="k-widget-14__product">
                        <div class="k-widget-14__thumb">
                            <a href="#">
                                <img src="assets/media/blog/1.jpg" class="k-widget-14__image--landscape" alt="" title="">
                            </a>
                        </div>
                        <div class="k-widget-14__content">
                            <a href="#">
                                <h3 class="k-widget-14__title">
                                `+ data[i][options.titleField] +`
                                </h3>
                            </a>
                            <div class="k-widget-14__desc"> `+ data[i][options.descField] +`</div>
                        </div>
                    </div>
                    <div class="k-widget-14__data">
                        <div class="k-widget-14__info">
                            <div class="k-widget-14__info-title k-font-brand">`+ data[i][options.purchasesField] +`</div>
                            <div class="k-widget-14__desc">Purchases</div>
                        </div>
                        <div class="k-widget-14__info">
                            <div class="k-widget-14__info-title">37</div>
                            <div class="k-widget-14__desc">Reviews</div>
                        </div>
                    </div>
                </div>
                <div class="k-widget-14__foot">
                    <div class="k-widget-14__foot-info">
                        <div class="k-widget-14__foot-label btn btn-sm btn-label-brand btn-bold"> `+data[i][options.createDateField]+` </div>
                        <div class="k-widget-14__foot-desc">Date of Release</div>
                    </div>
                    <div class="k-widget-14__foot-toolbar"> <a href="#" class="btn btn-default btn-sm btn-bold btn-upper">Preview</a> <a href="#" class="btn btn-default btn-sm btn-bold btn-upper">Details</a> </div>
                </div>
            </div>`;
            }
            $("#"+ options.elementId + " .carousel-inner").empty().html(html);
        });        
    }    

    var displayWidgetTabTop = function(options) {
        if (!document.getElementById(options.elementId)) {
            return;
        }

        getDataFromURL(options).then((data)=>{
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
                    "                <div class=\"progress-bar "+getColor()+"\" role=\"progressbar\" style=\"width: "+ value[i][options.progressField] + "%;\" aria-valuenow=\""+ (100 - value[i][options.progressField]) + "\" aria-valuemin=\"0\" aria-valuemax=\"100\"></div>\r\n"+
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

        getDataFromURL(options).then((data)=>{
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
                if ((options.hasOwnProperty('showTab') && key == options.showTab) || (!options.hasOwnProperty('showTab') && index == 1))
                    navHtml += " active show ";
                navHtml +=
                "\" data-toggle=\"tab\" href=\"#"+ id +
                "\" role=\"tab\" aria-selected=\"false\">" + key + "</a> </li>";

                contentHtml += "<div class=\"tab-pane fade "
                if ((options.hasOwnProperty('showTab') && key == options.showTab) || (!options.hasOwnProperty('showTab') && index == 1))
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

    var displayBothTable = function (options) {
        if (!document.getElementById(options.elementId)) {
            return;
        }

        initColumns(options).then((columns) => {
            getDataFromURL(options).then((data) => {
                var datatable = $("#"+options.elementId).KDatatable({
                    // datasource definition
                    data: {
                        type: 'local',
                        source: data,
                        pageSize: 10,
                    },

                    layout: {
                        theme: 'default',
                        class: '',
                        scroll: true,
                        height: 350,
                        footer: false
                    },
                    sortable: true,

                    filterable: false,

                    pagination: true,

                    search: {
                        input: $('#generalSearch')
                    },

                    rows: {
                        // disable responsive auto hide columns in row for horizontal scrollbar
                        autoHide: false
                    },
                    columns:columns
                });
            });
        });
    }    

    return {
        init:function() {
        },
        getDataFromRestAPI:getDataFromURL,
        getColor:getColor,
        initColumns:initColumns,
        displayWidget1:displayWidget1,
        displayWidget2:displayWidget2,
        displayWidget3:displayWidget3,
        displayPlanningActual:displayPlanningActual,
        displayWidgetTab2:displayWidgetTab2,
        displayWidgetTab3:displayWidgetTab3,
        displayWidgetTabTop:displayWidgetTabTop,
        displayLatestTask:displayLatestTask,
        displayBothTable:displayBothTable,
        displayWidgetTabNew:displayWidgetTabNew
    }    
}();

jQuery(document).ready(function () {
    ComponentClass.init();
});