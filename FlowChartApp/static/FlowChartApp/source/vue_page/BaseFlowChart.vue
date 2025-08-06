<template>
</template>
<script>
import convertTool from "../javascript/ConvertTool"
import axios from 'axios';
export default {
    name: "BaseFlowChart_vueFrm",
    data() {
        return {
            flowChartInstance: undefined,
            history:[],
            currentFlowChart:undefined
        }
    },
    methods: {
        nodeDubleClick(node_data) {
            var childType = node_data.childType;
            var flowChartNo = node_data.flowChartNo;
            var url = node_data.url;
            //打開外部URL
            if (childType == "module" && url != undefined && url != "") {
                setTimeout(() => {
                    url = url.replace(/&amp;/g, '&');
                    window.open(url);
                });
            }

            //打開關聯流程圖
            if (childType == "system" && flowChartNo != undefined && flowChartNo != "") {
                this.show_flowchart(flowChartNo)
            }
        },
        diagramClick(modelData) {
            console.log(modelData);
        },
        show_flowchart(flowChartNo, sysid=undefined) {
            var self = this;
            if ((flowChartNo == undefined || flowChartNo == "") && (sysid ==undefined || sysid == "")) {
                return;
            }
            var url = '/flowchart/get_old_flowchart_data'
            if (sysid == undefined)
                url += `?flowChartNo=${flowChartNo}`
            else 
                url += `?sysid=${sysid}`
            url += "&format=json"
            var flowChartStr = "{0}:{1}".format((flowChartNo == undefined ? "" : flowChartNo), (sysid == undefined ? "":sysid));
            if (this.currentFlowChart != flowChartStr)
                    self.history.push(this.currentFlowChart);
                
            return new Promise((resolve, reject) => {
                axios.get(url).then((result) => {
                    if (result.data.status) {
                        try {
                            var gojs_data = convertTool.convert(JSON.parse(result.data.data.flowchartdata));
                            var modelData = convertTool.convertModelData(result.data.data.flowchartinfo)
                            var model = go.Model.fromJson(gojs_data);
                            model.modelData = modelData;
                            self.flowChartInstance.getDiagram().model = model;
                            self.currentFlowChart = flowChartStr;
                        } catch (e) {
                            alert("轉換流程圖失敗!");
                        }
                    }
                }).catch(function (error) {
                    console.log(error);
                    resolve(false)
                });
            });
        },

        prevFlowChart() {
            if (this.history.length > 1) {
                this.currentFlowChart = this.history.pop();
                var flowchartno = this.currentFlowChart.split(":")[0]
                var sysid = this.currentFlowChart.split(":")[1]
                if (flowchartno != "")
                    this.show_flowchart(flowchartno);
                else if (sysid != "")
                    this.show_flowchart(undefined, sysid);
            }
            
        },
        show_doc_click(dataType, no) {
		    if(dataType == "2")
		        this.show_flowchart(no);
    	}

    }
}
</script>