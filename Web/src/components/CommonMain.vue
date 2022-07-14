<template>
  <div class="common-main">
    <!-- 显示处理之后的图像 -->
    <!-- <div
      v-for="(layer, index) in layers"
      :key="index"
      v-show="indexOfLayer === index"
    >
      <el-image :src="layer.avatar_url" />
    </div> -->
    <!-- 显示原始图像 -->
    <static-map v-show="showOrgImg"></static-map>
    <!-- drawleaflet -->
    <analysing-chart></analysing-chart>
  </div>
</template>

<script>
import StaticMap from "./StaticMap.vue";
import AnalysingChart from "./AnalysingChart.vue";

export default {
  name: "CommonMain",
  data() {
    return {
      layers: [],
      indexOfLayer: -1,
      // indexOfOrgImg: 0,
      // //图像urlBase64
      // imgBase64Array: [],
      //是否显示原始图像
      showOrgImg: true,
      //显示处理之后的图像
      showAnalysedImg: false,
      //刷新地图组件
      refreshMap:true,
      bg:require("../assets/background_dark.png")
    };
  },
  methods: {
    //闪烁效果
    go() {
      setInterval(() => {
        this.indexOfLayer =
          this.indexOfLayer < this.layers.length ? this.indexOfLayer + 1 : 0;
      }, 300);
    },


  },
  mounted() {

    //显示处理之后的图像
    this.$bus.$on("getLayers", (layers) => {
      // this.showOrgImg = false;
      this.showAnalysedImg = true
      this.layers.push(layers);
    });
    // this.go();
    this.$bus.$on('destroyMap',(e)=>{
      e===1;//没有意义的一句话
      this.layers=[]
      this.indexOfLayer=-1;
      this.showOrgImg = true;
    })
  },
  beforeCreate(){
  let bg=require("../assets/background_dark.png")
    document.body.background="transparent"
    document.getElementById("app").style.background=`url(${bg}) no-repeat`;
    document.getElementById("app").style.backgroundSize=`100% 100%`;
   
  },
  beforeDestroy(){

    let bg=require("../assets/background.png")
    document.getElementById("app").style.background="transparent";
     document.body.background=`url(${bg}) no-repeat`
    document.body.style.backgroundSize=`100% 100%`;
  },
  components:{ StaticMap, AnalysingChart },
};
  
</script>

<style scoped lang="less">
div {
  width: 100%;
  height: 100vh;
  padding: 0;
  margin: 0;
}
div img {
 
  width: 100%;
  height: 100vh;
  padding:0;
}
</style>