var ComponentClass = function () {
    function getRandomInt(min, max) {
        min = Math.ceil(min);
        max = Math.floor(max);
        return Math.floor(Math.random() * (max - min + 1)) + min; //含最大值，含最小值 
    }    

    var colors = ['blue','indigo','purple','pink','red','orange','yellow','green','teal','cyan'];

    var getColor = function() {
        var index = getRandomInt(0,colors.length-1);
        return colors[index];
    }    

    var getDataFromURL = function (options) {
        var localAjaxType = "get";
        if (options.ajaxType != undefined)
            localAjaxType = options.ajaxType;
        var deferred = $.Deferred();
        var param = JSON.stringify(options.query);
        if (localAjaxType == "get")
            param = options.query
        $.ajax({
            url: options.url,
            type: localAjaxType,
            dataType: "json",
            contentType: "application/json",
            data: param,
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


    var displayCompletionTasksControl = function (options) {
        if (!document.getElementById(options.elementId)) {
            return;
        }
        function handle(data) {
            var MaxNum = 0;
            //將數據分組
            var dataMap = new Map();
            for (var key in options.groups) {
                var color = Looper.getColors('brand')[getColor()]
                if (options.groups[key].hasOwnProperty("looper_color"))
                    color = Looper.getColors('brand')[options.groups[key]['looper_color']]
                if (options.groups[key].hasOwnProperty("color"))
                    color = options.groups[key]['color']
                dataMap.set(key, {
                    label: key,
                    backgroundColor: color,
                    borderColor: color,                    
                    data: []
                });
            }
            var labels = [];
            for (var i = 0; i < data.length; i++) {
                dataMap.forEach((value, key, dataMap) => {
                    value.data.push(data[i][options.groups[key]['field']]);
                    if (MaxNum < data[i][options.groups[key]['field']])
                        MaxNum = data[i][options.groups[key]['field']];
                });
                labels.push(data[i][options.labelField]);
            }
            var barChartData = {
                labels: labels,
                datasets: Array.from(dataMap.values())
            }

            var canvas = $('#' + options.elementId)[0].getContext('2d');
            var chart = new Chart(canvas, {
                type: 'bar',
                data: barChartData,
                options: {
                    responsive: true,
                    legend: {
                        display: false
                    },
                    title: {
                        display: false
                    },
                    scales: {
                        xAxes: [{
                            gridLines: {
                                display: true,
                                drawBorder: false,
                                drawOnChartArea: false
                            },
                            ticks: {
                                maxRotation: 0,
                                maxTicksLimit: 3
                            }
                        }],
                        yAxes: [{
                            gridLines: {
                                display: true,
                                drawBorder: false
                            },
                            ticks: {
                                beginAtZero: true,
                                stepSize: 100
                            }
                        }]
                    }
                }
            });
        }
        if (options.hasOwnProperty("data"))
            handle(options.data)
        else
            getDataFromURL(options).then((data)=>{
                handle(data)
            });
    }



    return {
        init: function () {
        },
        getDataFromRestAPI: getDataFromURL,
        displayCompletionTasksControl:displayCompletionTasksControl
    }
}();

jQuery(document).ready(function () {
    ComponentClass.init();
});