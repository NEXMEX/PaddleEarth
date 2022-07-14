<template>
  <div class="father-container">
    <div
      v-for="(option, index) in options"
      :key="index"
      class="analysing-charts"
      ref="analysingChart"
      v-show="index === indexOfOptions && isShowChart"
    >
      <v-chart
        class="chart"
        :option="option"
        :loading-options="loadingOptions"
        :autoresize="true"
        :loading="chartLoading"
      />
    </div>
  </div>
</template>

<script >
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { PieChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
} from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";

use([
  CanvasRenderer,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
]);

export default {
  name: "AnalysingChart",
  components: {
    VChart,
  },
  provide: {
    [THEME_KEY]: "dark",
  },
  data() {
    return {
        empty_data_0: {
        accessible_score: 0, //通达性
        cover_score: 0, //
        coverage: 0, //覆盖率
        matching_score: 0, //匹配度
        scale_score: 0, //规模
        totality_level: "", //总体评价
      }, //目标提取对应的空数据
      empty_data_1: {
        change: 0,
        early_coverage: 0,
        later_coverage: 0,
        scope: "",
        strength: "",
      }, //变化检测对应空的数据
      empty_data_2: {
        amount: 0,
        amount_score: 0,
        density_score: 0,
        name: "",
        rationality: "",
        scope_score: 0,
      }, //目标检测对应的空数据
      empty_data_3: {
        availability: "",
        building_coverage: 0,
        forest_coverage: 0,
        rationality: "",
        road_coverage: 0,
      }, //地物分类对应的空数据
      data_0: {
        accessible_score: 0, //通达性
        cover_score: 0, //
        coverage: 0, //覆盖率
        matching_score: 0, //匹配度
        scale_score: 0, //规模
        totality_level: "", //总体评价
      }, //目标提取对应的数据
      data_1: {
        change: 0,
        early_coverage: 0,
        later_coverage: 0,
        scope: "",
        strength: "",
      }, //变化检测对应的数据
      data_2: {
        amount: 0,
        amount_score: 0,
        density_score: 0,
        name: "",
        rationality: "",
        scope_score: 0,
      }, //目标检测对应的数据
      data_3: {
        availability: "",
        building_coverage: 0,
        forest_coverage: 0,
        rationality: "",
        road_coverage: 0,
      }, //地物分类对应的数据
      isShowChart: false,
      indexOfOptions: -1,
      //图表加载动画配置
      loadingOptions: {
        text: "loading",
        color: "#c23531",
        textColor: "#000",
        maskColor: "rgba(255, 255, 255, 0.8)",
        zlevel: 0,

        // 字体大小。从 `v4.8.0` 开始支持。
        fontSize: 12,
        // 是否显示旋转动画（spinner）。从 `v4.8.0` 开始支持。
        showSpinner: true,
        // 旋转动画（spinner）的半径。从 `v4.8.0` 开始支持。
        spinnerRadius: 10,
        // 旋转动画（spinner）的线宽。从 `v4.8.0` 开始支持。
        lineWidth: 5,
        // 字体粗细。从 `v5.0.1` 开始支持。
        fontWeight: "normal",
        // 字体风格。从 `v5.0.1` 开始支持。
        fontStyle: "normal",
        // 字体系列。从 `v5.0.1` 开始支持。
        fontFamily: "sans-serif",
      },
      chartLoading: true,
      modeCode: -1,
    };
  },
  computed: {
    options() {
      let self = this;
      return [
        // 雷达图
        {
          title: {
            text: "路网建设评价\n总体评价:"+self.data_0.totality_level,
          },
          tooltip: {
            trigger: "item",
          },
          legend: {
            data: ["检测地区"],
          },
          radar: {
            shape: "circle",
            indicator: [
              { name: "覆盖率得分", max: 10 },
              { name: "通达性", max: 10 },
              { name: "规模", max: 10 },
              { name: "匹配度", max: 10 },
            ],
          },

          series: [
            {
              name: "路网建设评价",
              type: "radar",
              areaStyle: {},
              
              data: [
                {
                  value: [
                    self.data_0.cover_score,
                    self.data_0.accessible_score,
                    self.data_0.scale_score,
                    self.data_0.matching_score,
                  ],
                  name: "检测地区",
                },
              ],
            },
          ],
        },
        //折线图
        {
          title: {
            text: "城市化\t"+"扩张范围:"+self.data_1.scope+"\t扩展强度:"+self.data_1.strength,
          },
          tooltip: {
            trigger: "item",
            formatter: "{b} : {c} ",
          },
          xAxis: {
            type: "category",
            data: ["阶段1覆盖率", "阶段2覆盖率"],
          },
          yAxis: {
            type: "value",
          },
          series: [
            {
              data: [self.data_1.early_coverage, self.data_1.later_coverage],
              type: "line",
              symbol: "rectangle",
              symbolSize: 20,
              lineStyle: {
                color: "#5470C6",
                width: 4,
              },
            
              itemStyle: {
                borderWidth: 3,
                borderColor: "#EE6666",
                color: "yellow",
              },
            },
          ],
        },
        //雷达图2
        {
          title: {
            text: "资源分配评价\n资源分配合理性:"+self.data_2.rationality,
          },
          tooltip: {
            trigger: "item",
          },
          label: {
            show: true,
            formatter: function (params) {
              return params.value;
            },
          },
          backgroundColor: {
            type: "radial",
            x: 0.3,
            y: 0.3,
            r: 0.8,
            colorStops: [
              {
                offset: 0,
                color: "#2C3740",
              },
              {
                offset: 1,
                color: "#2C3740",
              },
            ],
          },
          legend: {
            data: ["检测地区"],
          },
          radar: {
            shape: "circle",
            indicator: [
              { name: "数量", max: 10 },
              { name: "范围", max: 10 },
              { name: "密度", max: 10 },
            ],
          },
          series: [
            {
              name: "Budget vs spending",
              type: "radar",
              areaStyle: {},
           
              lineStyle: {
                color: "#7CECD7",
                width: 4,
                type: "dashed",
              },
              itemStyle: {
                borderWidth: 3,
                borderColor: "#EE6666",
                color: "green",
              },
              data: [
                {
                  value: [
                    self.data_2.amount,
                    self.data_2.scope_score,
                    self.data_2.density_score,
                  ],
                  name: "检测地区",
                },
              ],
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: "rgba(0, 0, 0, 0.5)",
                },
              },
            },
          ],
        },
        //饼状图
        {
          title: {
            text: "用地比例图\n"+"用地规划合理性:"+self.data_3.rationality+"\n土地利用率:"+self.data_3.availability,
            left: "center",
          },
   
          tooltip: {
            trigger: "item",
            formatter: "{a} <br/>{b} :  ({d}%)",
          },
          legend: {
            orient: "vertical",
            left: "left",
            data: ["林地", "建筑", "道路", "其他"],
          },
          series: [
            {
              name: "用地比例",
                
              type: "pie",
              radius: "55%",
              center: ["50%", "60%"],
              data: [
                { value: self.data_3.forest_coverage, name: "林地" },
                { value: self.data_3.building_coverage, name: "建筑" },
                { value: self.data_3.road_coverage, name: "道路" },
                {
                  value:
                  self.data_3.forest_coverage===0?0:
                    1 -
                    self.data_3.forest_coverage -
                    self.data_3.building_coverage -
                    self.data_3.road_coverage,
                  name: "其他",
                },
              ],
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: "rgba(0, 0, 0, 0.5)",
                },
              },
            },
          ],
        },
      ];
    },
  },
  mounted() {
    this.$bus.$on("sendModeCode", (mode) => {
      this.chartLoading = true;
      switch (mode) {
        case "目标提取":
          this.indexOfOptions = 0;
          break;
        case "变化检测":
          this.indexOfOptions = 1;
          break;
        case "目标检测":
          this.indexOfOptions = 2;
          break;
        case "地物分类":
          this.indexOfOptions = 3;
          break;
      }
      setTimeout(() => {
        this.chartLoading = false;
      }, 800);
    });
    this.$bus.$on("showAnaChart", (e) => {
      e == 1;
      this.isShowChart = !this.isShowChart;
    });
    this.$bus.$on("getLayers", (items) => {
      //this.isShowChart = true;

      switch (this.indexOfOptions) {
        case 0:
          this.data_0 = items.index;
          this.data_1=this.empty_data_1;
          this.data_2=this.empty_data_2;
          this.data_3=this.empty_data_3
          break;
        case 1:
          this.data_0=this.empty_data_0;
          this.data_1 = items.index;          
          this.data_2=this.empty_data_2;
          this.data_3=this.empty_data_3;
          break;
        case 2:
          this.data_0=this.empty_data_0;
          this.data_1=this.empty_data_1;
          this.data_2 = items.index;
          this.data_3=this.empty_data_3;
          
          break;
        case 3:
          this.data_0=this.empty_data_0;
          this.data_1=this.empty_data_1;
          this.data_2=this.empty_data_2;   
          this.data_3 = items.index;
          break;
      }
      console.log(items);
    });

    this.$bus.$on("destroyMap", (p) => {
      p == 1;
      this.isShowChart = false;
    });
  },
};
</script>

<style scoped lang="less">
.father-container {
  position: relative;
}
.analysing-charts {
  position: fixed;
  right: 7%;
  top: 10%;
  z-index: 100;
  height: 450px;
  width: 450px;
}
</style>