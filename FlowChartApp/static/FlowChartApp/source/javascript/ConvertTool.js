class ConvertTool {
    convertModelData(flowchartinfo) {
        var match_diagram_propertys = this.get_diagram_match_property()
        var data = {}
        if (flowchartinfo) {
            for(var [type, value] of Object.entries(flowchartinfo)) {
                if (match_diagram_propertys.hasOwnProperty(type)) {
                    data[match_diagram_propertys[type]] = value;
                }
            }            
        }
        return data;
    }
    convert(flash_json) {
        var data = { "class": "go.GraphLinksModel",
            "linkFromPortIdProperty": "fromPort",
            "linkToPortIdProperty": "toPort",
            "nodeDataArray": [
            ],
            "linkDataArray": [

        ]};
        var match_propertys = this.get_match_property();
        var line_match_propertys = this.get_line_match_property();
        //var json = xml2json(flash_xml);
        //var json = this.convertXmlToJson(flash_xml);
        var json = flash_json;
        if (json.flowchart.hasOwnProperty("chart")) {
        if (Object.prototype.toString.apply(json.flowchart.chart) != '[object Array]')
        json.flowchart.chart = [json.flowchart.chart];
        for(var item of json.flowchart.chart) {
            var type = item.type;
            if (match_propertys.hasOwnProperty(type)) {
            var chart = this.convert_category(match_propertys[type], item)
            data.nodeDataArray.push(chart);
            }
        }
        }
        if (json.flowchart.hasOwnProperty("line")) {
        if (Object.prototype.toString.apply(json.flowchart.line) != '[object Array]')
        json.flowchart.line = [json.flowchart.line];
        for (var item of json.flowchart.line) {
            var type = item.type;
            if (line_match_propertys.hasOwnProperty(type)) {
            var line = this.convert_line_category(line_match_propertys[type], item)
            data.linkDataArray.push(line);
            }
        }
        }
        return JSON.stringify(data)
    }
    convert_category(match_property, item) {
        var chart = {}
        for(const [key, value] of Object.entries(match_property)) {
        if (key == "category")
            chart["category"] = value;
        else if (['width','height'].indexOf(key) != -1)
            chart[value] = parseFloat(item[key]);
        else if (key == "text" && item[key] != undefined)
            chart[value] = item[key].replaceAll("&#xD;","\n");
        else if (key == "align" && item[key] != undefined) {
            chart[value] = {alignCenter:"center",alignLeft:"left", alignRight:"right"}[item[key]];
        }
        else if (['fillcolor','bordercolor','fontcolor'].indexOf(key) != -1 && item[key] != undefined) {
            if (key == "fontcolor" && item[key] == "0")
                chart[value] = "#000"
            else if(key == 'fillcolor' && item[key] == "0")
                chart[value] = "#fff";
            else if (key=="bordercolor" && item[key] == "0")
                chart[value] = "#000";
            else
                chart[value] = "#" + parseInt(item[key]).toString(16).padStart(6, '0')
        }
        else
            chart[value] = item[key];
        }
        var loc_x = parseFloat(item.x) + chart.width/2;
        var loc_y = parseFloat(item.y) + chart.height/2;
        chart["loc"] = `${loc_x} ${loc_y}`;
        chart['bordersize'] = 1;
        if (['Start','End'].indexOf(match_property.category) != -1)
        chart["fillcolor"] = "#000";
        return chart;
    }
    convert_line_category(match_property, item) {
        var line = {}
        for(const [key, value] of Object.entries(match_property)) {
        if (key == "category")
            continue;
        else if (['fontsize'].indexOf(key) != -1)
            line[value] = parseFloat(item[key]);
        else if (key == "corners" && item[key] != undefined) {
            var corners = item[key].replaceAll("|", ",");
            var corners_arry = corners.split(",").map(d=>parseFloat(d));
            var fromPos_arry = item['fromPos'].split(",").map(d=>parseFloat(d))
            var toPos_arry = item['toPos'].split(",").map(d=>parseFloat(d))
            var corners_start = [(fromPos_arry[0] + corners_arry[0])/2, (fromPos_arry[1] + corners_arry[1])/2]
            var corners_end = [(toPos_arry[0] + corners_arry[corners_arry.length - 2])/2, 
            (toPos_arry[1] + corners_arry[corners_arry.length -1 ])/2]
            line[value] = fromPos_arry.concat(corners_start).concat(corners_arry).concat(corners_end).concat(toPos_arry);
        }
        else if (key == "text" && item[key] != undefined)
            line[value] = item[key].replaceAll("&#xD;","\n");
        else if (['fromPort','toPort'].indexOf(key) != -1 && item[key] != undefined) {
            line[value] = {1:"T",2:"R",3:"B",4:"L"}[parseInt(item[key])];
        }
        else if (['fillcolor','bordercolor','fontcolor'].indexOf(key) != -1 && item[key] != undefined) {
            if (key == "fontcolor" && item[key] == "0")
                line[value] = "#000";
            else if(key == 'fillcolor' && item[key] == "0")
                line[value] = "#000";
            else if (key == 'bordercolor' && item[key] == "0")
                line[value] = "#000";
            else
                line[value] = "#" + parseInt(item[key]).toString(16).padStart(6, '0')
        }
        else if (key == "isHideArrowhead") {
            line[value] = !(item[key] != undefined && item[key] == "1");
        }
        else if (key == "bordersize") {
            line[value] = item[key] == undefined || parseInt(item[key]) == 0 ? 1 : parseInt(item[key])
        }
        else
            line[value] = item[key];
        
        if (match_property.category == "default" && item['corners'] == undefined) {
            line["routing"] = "normal";
            line["points"] = (item['fromPos'] + "," + item['toPos'])
                .split(",").map(d=>parseFloat(d));
        }else if (match_property.category == "arcline") {
            line["routing"] = "normal";
            line["curve"] = "bezier";
            line["points"] = (item['fromPos'] + "," + item['corners'] + "," + item['corners'] + "," + item['toPos'])
                .split(",").map(d=>parseFloat(d));
        }
        }
        return line;
    }
    get_line_match_property() {
        var base_convert = {
        fromChart:"from",
        toChart:"to",
        fromPort:"fromPort",
        toPort:"toPort",
        corners:"points",
        text:"text",
        fontcolor:"fontColor",
        fontsize:"fontSize",
        bordercolor:"bordercolor",
        fillcolor:"fillcolor",
        isHideArrowhead:"showArrow",
        isDasned:"isDasned",
        bordersize:"bordersize"
        }
        var arcline = Object.assign({category:"arcline"}, base_convert);
        delete arcline['fromPort'];
        delete arcline['toPort'];
        return {
        bevelline:Object.assign({category:"default"}, base_convert),
        arcline:arcline
        }
    }
    get_diagram_match_property() {
        var base_convert = {
            'flowchartno':'flowchartno',
            'title':'name',
            'description':'desc',
            'parentno':'parentno',
            'version':'version',
            'fc050':'systemormodule',
            'fc051':'flowcharttype',
            'fc057':'system',
            'modifier':'modifier',
            'modi_date':'modi_date'
        }
        return Object.assign({}, base_convert)
    }
    get_match_property() {
        var base_convert = {
        id:"key",
        flowChartNo:"flowChartNo",
        childType:"childType",
        align:"textAlign",
        width:"width",
        height:"height",
        text:"text",
        bordercolor:"bordercolor",
        bordersize:"bordersize",
        fontcolor:"fontColor",
        fontsize:"fontSize",
        fillcolor:"fillcolor",
        url:"url"
        }
        return {
        port:Object.assign({category:"Activity"}, base_convert),
        program:Object.assign({category:"Program"}, base_convert),
        defaultprogram:Object.assign({category:"Procedure"}, base_convert),
        file:Object.assign({category:"Document"}, base_convert),
        store:Object.assign({category:"Store"}, base_convert),
        database:Object.assign({category:"Database"}, base_convert),
        handinput:Object.assign({category:"Manualinput"}, base_convert),
        table:Object.assign({category:"DbTable"}, base_convert),
        if:Object.assign({category:"Conditional"}, base_convert),
        annotation:Object.assign({category:"Comment"}, base_convert),        
        start:Object.assign({category:"Start"}, base_convert),
        end:Object.assign({category:"End"}, base_convert),
        case:Object.assign({category:"Usecase"}, base_convert),
        node:Object.assign({category:"Node"}, base_convert),
        component:Object.assign({category:"Component"}, base_convert),
        swimlane:Object.assign({category:"Swimlane"}, base_convert),
        "class":Object.assign({category:"Class"}, base_convert),
        package:Object.assign({category:"Package"}, base_convert),
        people:Object.assign({category:"User"}, base_convert),
        storage:Object.assign({category:"Storage"}, base_convert),
        computer:Object.assign({category:"Client"}, base_convert),
        server:Object.assign({category:"Server"}, base_convert),
        }
    }    
}

const convertTool = new ConvertTool()
export default convertTool