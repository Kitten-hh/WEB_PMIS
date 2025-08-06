var IndexClass = function() {    
    $("a.k-menu__link").on("click", function() {
        $("#mainweb").attr("src", $(this).attr("dest"));
    });    

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
            top.window.IndexClass.getDataFromRestAPI(localOptions).then((data)=>{
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

    return {
        init:function() {
        },
        getDataFromRestAPI:getDataFromURL,
        getColor:getColor,
        initColumns:initColumns
    }
}();

jQuery(document).ready(function () {
    IndexClass.init();
});