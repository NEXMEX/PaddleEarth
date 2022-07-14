<template>
  <div id="map" v-if="refreshMap">
    <div
      clsss="draw-tool-bar"
      v-show="refreshMap"
      style="
        background-color: #2c3740;
        padding: 3px;
        display: flex;
        flex-direction: row;
      "
    >
      &nbsp; &nbsp; &nbsp; &nbsp;
      <div class="draw-tool-container">
        <el-tooltip class="item" effect="dark" placement="bottom">
          <div slot="content">绘制区域<br />双击结束</div>
          <el-button
            @click="drawFeature('Polygon')"
            circle
            :disabled="dontShowButton"
            id="draw-tools"
            class="draw-btn"
            ><i class="el-icon-edit" :style="iconColorSetter"></i
          ></el-button>
        </el-tooltip>
      </div>
      <div class="draw-tool-container">
        <el-tooltip
          class="item"
          effect="dark"
          content="撤销绘制"
          placement="bottom"
        >
          <el-button
            @click="draw.removeLastPoint()"
            circle
            :disabled="dontShowButton"
            class="draw-btn"
            ><i class="el-icon-back" :style="iconColorSetter"></i
          ></el-button>
        </el-tooltip>
      </div>
      <div class="draw-tool-container">
        <el-tooltip
          class="item"
          effect="dark"
          content="取消绘制"
          placement="bottom"
        >
          <el-button
            @click="map.removeInteraction(draw)"
            circle
            :disabled="dontShowButton"
            class="draw-btn"
            ><i class="el-icon-close" :style="iconColorSetter"></i
          ></el-button>
        </el-tooltip>
      </div>
      <div class="draw-tool-container">
        <el-tooltip
          class="item"
          effect="dark"
          content="清除绘制"
          placement="bottom"
        >
          <el-button
            @click="clearDrawLayer()"
            circle
            :disabled="dontShowButton"
            class="draw-btn"
            ><i class="el-icon-refresh-left" :style="iconColorSetter"></i
          ></el-button>
        </el-tooltip>
      </div>

      <el-radio-group
        v-model="radio"
        @change="changeLayer"
        style="margin-top: 10px; margin-bottom: 10px"
      >
        <el-radio
          label="showOrg"
          border
          style="margin-left: 600px; color: white"
          id="show-org-img"
          >原始图像</el-radio
        >
        <el-radio
          label="dontShow"
          border
          style="color: white"
          id="after-analyse"
          >处理后图像</el-radio
        >
      </el-radio-group>
    </div>
    <div id="popup" class="ol-popup" v-show="showPopup">
      <a href="#" id="popup-closer" class="ol-popup-closer"></a>
      <div id="popup-content"></div>
    </div>
  </div>
</template>

<script>
import "ol/ol.css";
import { Map, View } from "ol";
import { Vector as VectorLayer, Image as ImageLayer } from "ol/layer";
import { ImageStatic } from "ol/source";
import { getCenter } from "ol/extent";
import { Projection, transform } from "ol/proj";
import { createStringXY } from "ol/coordinate";
import Draw from "ol/interaction/Draw";
import { Fill, Stroke, Style, Circle } from "ol/style";
import { Vector as VectorSource } from "ol/source";
import { GeoJSON } from "ol/format";
// import { toLonLat } from "ol/proj";
// import { toStringHDMS } from "ol/coordinate";
import Overlay from "ol/Overlay";
import { defaults, MousePosition, ZoomSlider, ZoomToExtent } from "ol/control";

export default {
  name: "StaticMap",
  data() {
    return {
      radio: 1,
      map: null, // 地图
      imgx: 0, // 当前地图宽
      imgy: 0, // 当前地图高
      imgURL: "", //底图URL
      result_url: "", //结果url
      refreshMap: true, //是否刷新地图
      draw_source: new VectorSource(),
      draw_vector: undefined,
      draw: undefined,
      extent: [], //当前矩形左下角坐标和右上角左边
      resCoordinates: [[], []],
      state: "Before Analyse", //是否显示图块信息
      showPopup: false, //是否显示popup
      // highlightStyleARR: [
      //   new Style({
      //     fill: new Fill({
      //       color: "yellow",
      //     }),
      //     stroke: new Stroke({
      //       color: "#eeeeee",
      //       width: 2,
      //     }),
      //   }),
      //   new Style({
      //     fill: new Fill({
      //       color: "green",
      //     }),
      //     stroke: new Stroke({
      //       color: "#eeeeee",
      //       width: 2,
      //     }),
      //   }),
      // ], //渲染样式
      popupAttr: [{}], //瓦片属性
      dontShowButton: true, //是否禁用绘制按钮
      layers: [],
      iconColorSetter: `color:gray`,
    };
  },
  methods: {
    // 初始化地图
    initMap(flag, layers) {
      // let extent = [0, 0, 418, 600];
      return new Promise(() => {
        console.log("im in map");
        let center = transform([0, 0], "EPSG:4326", "EPSG:3857");
        console.log("center:", center);
        let extent = [
          center[0] - (this.imgx * 1) / 2,
          center[1] - (this.imgy * 1) / 2,
          center[0] + (this.imgx * 1) / 2,
          center[1] + (this.imgy * 1) / 2,
          // center[0] - this.imgx/10 / 2,
          // center[1] - this.imgy/10 / 2,
          // center[0] + this.imgx/10 / 2,
          // center[1] + this.imgy/10 / 2,
        ]; // 获取图片的宽高
        this.extent = extent;
        console.log("extent:", extent);
        let projection = new Projection({
          code: "xkcd-image",
          units: "pixels",
          extent: extent,
        });
        let $this = this;
        console.log($this);
        var orgLayer = new ImageLayer({
          source: new ImageStatic({
            url: this.imgURL, // 静态地图
            projection: projection,
            imageExtent: extent,
          }),
        });
        orgLayer.name = "OrgImg";
        this.map = new Map({
          target: "map",
          layers: [orgLayer],
          view: new View({
            projection: projection,
            center: getCenter(extent),
            zoom: 2,
            maxZoom: 18,
          }),
          controls: defaults({}).extend([
            // 添加坐标拾取控件
            new MousePosition({
              // 设置数据格式
              coordinateFormat: createStringXY(6),
              // 设置空间参考系统为'EPSG:4326'
              projection: "EPSG:3857",
            }),

            // 滑块缩放控件
            new ZoomSlider(),
            // 缩放至特定位置控件
            new ZoomToExtent({
              extent: this.extent,
              // extent: [
              //   // 位置矩形的左下角坐标
              //   0, 25,
              //   // 位置矩形的右上角坐标
              //   125, 110,
              // ],
            }),
          ]),
        });
        if (flag) {
          this.state = "After Analysing";
          this.layers.push(layers);
          this.result_url = layers.result_url;
          let projection = new Projection({
            code: "xkcd-image",
            units: "pixels",
            extent: this.extent,
          });
          let result_Layer = new ImageLayer({
            source: new ImageStatic({
              url: this.result_url, // 静态地图
              projection: projection,
              imageExtent: this.extent,
            }),
          });
          result_Layer.name = "resultImg";
          if (this.map !== null) {
            // try{
            // this.map.removeLayer(this.draw_vector)
            // }catch(err){
            //   console.log(err)
            // }
            this.map.addLayer(result_Layer);
            console.log(
              "im in layers hahhaha",
              this.map.getLayers(),
              this.draw_vector
            );
          } else {
            console.log("出错啦");
          }
        }
      });
    },
    //改变图层
    changeLayer(choice) {
      console.log(choice);
      let layers = this.map.getLayers();
      layers.forEach((layer) => {
        if (layer.name === "resultImg") {
          layer.setVisible(choice === "showOrg" ? false : true);
        }
        if (layer.name === "orgImg") {
          layer.setVisible(choice === "showOrg" ? true : false);
        }
        console.log(layer.name, layers);
      });
    },
    //添加绘画图层
    addDrawLayer() {
      this.draw_vector = new VectorLayer({
        source: this.draw_source,
        //绘制好后，在地图上呈现的样式
        style: new Style({
          fill: new Fill({
            color: "rgba(255, 255, 255, 0.2)",
          }),
          stroke: new Stroke({
            //边界样式
            color: "#ffcc33",
            width: 3,
          }),
          //点样式继承image
          image: new Circle({
            radius: 7,
            fill: new Fill({
              color: "#ffcc33",
            }),
          }),
        }),
      });
      this.map.addLayer(this.draw_vector);
    },
    //清除绘制图层
    clearDrawLayer() {
      if (this.draw) {
        this.map.removeInteraction(this.draw); //移除交互
      }
      if (this.draw_vector) {
        this.draw_vector.getSource().clear(); //清除图层上的所有要素
      }
    },
    //绘制点线面
    drawFeature(featureType = "") {
      this.map.on("pointermove", function () {});
      this.map.removeInteraction(this.draw);

      this.draw = new Draw({
        source: this.draw_source,
        type: featureType,
        //绘制时，在地图上呈现的样式
        style: new Style({
          fill: new Fill({
            color: "rgba(255, 255, 255, 0.2)",
          }),
          stroke: new Stroke({
            color: "#ffcc33",
            width: 2,
          }),
          image: new Circle({
            radius: 7,
            fill: new Fill({
              color: "#ffcc33",
            }),
          }),
        }),
      });
      this.map.addInteraction(this.draw);
      this.draw.on("drawend", (e) => {
        console.log(
          " e.feature.getGeometry().getCoordinates():",
          e.feature.getGeometry().getCoordinates()
        );
        //传输用户绘制图形的坐标
        this.$bus.$emit(
          "getDrawParam",
          e.feature.getGeometry().getCoordinates()
        );
      });
    },
    //根据坐标绘制图形
    drawByCoordinate() {
      console.log(GeoJSON);
      var styles = {
        Polygon: [
          new Style({
            stroke: new Stroke({
              color: "#ffcc33",
              lineDash: [0],
              width: 1,
            }),
            fill: new Fill({
              color: "#ffcc33",
            }),
          }),
        ],
      };

      var styleFunction = function (feature) {
        console.log(feature);
        return styles[feature.getGeometry().getType()];
      };
      console.log(styleFunction);

      var geojsonObject = {
        type: "FeatureCollection",
        crs: {
          type: "name",
          properties: {
            name: "EPSG:3857",
          },
        },
        features: [
          {
            //区域
            type: "Feature",
            geometry: {
              type: "Polygon",
              coordinates: this.resCoordinates,
            },
          },
        ],
      };
      /*11111111111111111111111*/
      //       var geojsonObject = {
      //  "type"    : "FeatureCollection",
      //  "creator" : "svg2geojson v0.7.1",
      //  "features": [
      //   {"type":"Feature","properties":{"svgID":"path @ M1023,1"},"geometry":{"type":"Polygon","coordinates":[[[0.319688,0.000406],[0.000312,0.000406],[0.000312,0.415594],[0.319688,0.415594],[0.319688,0.000406]],[[0.320000,0],[0.320000,0],[0.320000,0.416000],[0,0.416000],[0,0],[0.320000,0]]]}},
      //   {"type":"Feature","properties":{"svgID":"#[object Object]"},"geometry":{"type":"Polygon","coordinates":[[[0.155938,0.230750],[0.155938,0.230750],[0.183241,0.167103],[0.154491,0.104540],[0.098437,0.105625],[0.071134,0.169272],[0.099884,0.231835],[0.155938,0.230750]]]}},
      //   {"type":"Feature","properties":{"svgID":"polygon @ 726,629,726,629"},"geometry":{"type":"Polygon","coordinates":[[[0.226875,0.255531],[0.226875,0.255531],[0.253084,0.234922],[0.252459,0.195110],[0.225625,0.175906],[0.199416,0.196515],[0.200041,0.236328],[0.226875,0.255531]]]}},
      //   {"type":"Feature","properties":{"svgID":"polygon @ 526,782,526,782"},"geometry":{"type":"Polygon","coordinates":[[[0.164375,0.317687],[0.164375,0.317687],[0.162534,0.289985],[0.143159,0.278204],[0.125625,0.294125],[0.127466,0.321827],[0.146841,0.333608],[0.164375,0.317687]]]}},
      //   {"type":"Feature","properties":{"svgID":"polygon @ 177,718,177,718"},"geometry":{"type":"Polygon","coordinates":[[[0.055312,0.291687],[0.055312,0.291687],[0.073172,0.266086],[0.065047,0.233179],[0.039063,0.225875],[0.021203,0.251477],[0.029328,0.284383],[0.055312,0.291687]]]}},
      //   {"type":"Feature","properties":{"svgID":"polygon @ 82,200,82,200"},"geometry":{"type":"Polygon","coordinates":[[[0.025625,0.081250],[0.025625,0.081250],[0.038250,0.066613],[0.034813,0.045082],[0.018750,0.038187],[0.006125,0.052825],[0.009563,0.074356],[0.025625,0.081250]]]}},
      //   {"type":"Feature","properties":{"svgID":"polygon @ 89,346,89,346"},"geometry":{"type":"Polygon","coordinates":[[[0.027812,0.140562],[0.027812,0.140562],[0.044322,0.128172],[0.044322,0.103391],[0.027812,0.091000],[0.011303,0.103391],[0.011303,0.128172],[0.027812,0.140562]]]}},
      //   {"type":"Feature","properties":{"svgID":"polygon @ 288,776,288,776"},"geometry":{"type":"Polygon","coordinates":[[[0.090000,0.315250],[0.090000,0.315250],[0.090000,0.315250],[0.081069,0.321953],[0.081069,0.335359],[0.090000,0.342062],[0.098931,0.335359],[0.098931,0.321953],[0.090000,0.315250]]]}}
      //  ]
      // }
      /*坐标转换*/
      // geojsonObject.features = geojsonObject.features.map((feature) => {
      //   return {
      //     type: "Feature",
      //     coordinates: feature.geometry.coordinates.map((coordinates) => {
      //       return coordinates.map((coordinate) => {
      //         return transform(coordinate, "EPSG:4326", "EPSG:3857");
      //       });
      //     }),
      //   };
      // });

      console.log("geojsonObject", geojsonObject);
      var vectorSource = new VectorSource({
        features: new GeoJSON().readFeatures(geojsonObject),
      });
      var vectorLayer = new VectorLayer({
        source: vectorSource,
        style: new Style({
          fill: new Fill({
            color: "red",
          }),
          stroke: new Stroke({
            //边界样式
            color: "#ffcc33",
            width: 3,
          }),
          //点样式继承image
          image: new Circle({
            radius: 7,
            fill: new Fill({
              color: "#ffcc33",
            }),
          }),
        }),
        format: new GeoJSON(),
      });
      // vectorLayer.setZIndex(2)
      console.log("VectorLayer", vectorLayer);
      this.map.addLayer(vectorLayer);
    },
    //点击显示图块信息
    showTilesInfo() {
      //绑定点击图块事件
      this.map.on("singleclick", this.showInfoHandler);
      //如果当前状态为处理之前，则不显示图块信息
      if (this.state == "Before Analyse")
        this.map.un("singleclick", this.showInfoHandler);
    },
    //显示图块信息实现
    showInfoHandler(e) {
      this.showPopup = true;
      const highlightStyle = new Style({
        fill: new Fill({
          color: "green",
        }),
        stroke: new Stroke({
          color: "#eeeeee",
          width: 2,
        }),
      });
      /**
       * Elements that make up the popup.
       */
      const container = document.getElementById("popup");
      const content = document.getElementById("popup-content");
      const closer = document.getElementById("popup-closer");
      /**
       * Create an overlay to anchor the popup to the map.
       */
      const popup = new Overlay({
        element: container,
        autoPan: {
          animation: {
            duration: 250,
          },
        },
      });
      this.map.addOverlay(popup);
      /**
       * Add a click handler to hide the popup.
       * Don't follow the href.
       */
      closer.onclick = () => {
        console.log("im in closer");
        this.showPopup = false;
        popup.setPosition(undefined);
        closer.blur();
        return false;
      };
      const selected = [];
      //改变图块颜色
      const coordinate = e.coordinate;
      this.map.forEachFeatureAtPixel(e.pixel, function (feature) {
        const selIndex = selected.indexOf(feature);
        if (selIndex < 0) {
          selected.push(feature);
          feature.setStyle(highlightStyle);
        } else {
          selected.splice(selIndex, 1);
          feature.setStyle(undefined);
        }
        content === coordinate;
        if (feature) {
          // // 清空html
          // content.innerHTML = "";
          // // popup属性
          // feature.set("attr1", "attr1");
          // var attr1 = document.createElement("p");
          // attr1.innerText = "属性1：" + feature.get("attr1");
          // content.appendChild(attr1);
          // // 弹出popup
          // popup.setPosition(coordinate);
        }
      });
    },
    //将url地址转为base64
    toBase64(imgUrl) {
      this.imgURL = imgUrl;
      // 一定要设置为let，不然图片不显示
      let self = this;
      let image = new Image();
      // 解决跨域问题
      image.setAttribute("crossOrigin", "anonymous");
      const imageUrl = imgUrl;

      image.src = imageUrl;
      // image.onload为异步加载
      image.onload = () => {
        var canvas = document.createElement("canvas");
        canvas.width = image.width;
        canvas.height = image.height;
        var context = canvas.getContext("2d");
        context.drawImage(image, 0, 0, image.width, image.height);
        var quality = 0.8;
        // 这里的dataurl就是base64类型
        // 使用toDataUrl将图片转换成jpeg的格式,不要把图片压缩成png，因为压缩成png后base64的字符串可能比不转换前的长！
        console.log("lalallaaimg", canvas.toDataURL("image/jpeg", quality));
        var dataurl = canvas.toDataURL("image/jpeg", quality);
        self.imgURL = dataurl;
      };
    },
    /**
     * getLayer事件
     */
    getLayersHandler(layers) {
      console.log("im in getLayers");
      this.state = "After Analysing";
      this.layers.push(layers);
      this.result_url = layers.result_url;
      let projection = new Projection({
        code: "xkcd-image",
        units: "pixels",
        extent: this.extent,
      });

      let result_Layer = new ImageLayer({
        source: new ImageStatic({
          url: this.result_url, // 静态地图
          projection: projection,
          imageExtent: this.extent,
        }),
      });
      result_Layer.name = "resultImg";
      if (this.map !== null) {
        // try{
        // this.map.removeLayer(this.draw_vector)
        // }catch(err){
        //   console.log(err)
        // }
        if (this.draw_vector != undefined) {
          this.map.removeLayer(this.draw_vector);
          this.map.addLayer(result_Layer);
          this.map.addLayer(this.draw_vector);
        } else {
          this.map.addLayer(result_Layer);
        }

        console.log("draw", this.draw_vector);
        // try{
        //   this.map.addLayer(this.draw_vector)
        // }catch(err){
        //   console.log(err)
        // }

        console.log(
          "im in layers hahhaha",
          this.map.getLayers(),
          this.draw_vector
        );
        document.getElementById("after-analyse").click();
      } else {
        console.log("出错啦");
      }
    },
    /**
     * sendOrgImg事件
     */
    sendOrgImgHandler(img_base64) {
      return new Promise(() => {
        console.log("im in sendimg");
        this.imgURL = img_base64;
        this.clearDrawLayer();
        document.getElementById("show-org-img").click();
        this.dontShowButton = false;
      });
    },
    /**
     * getQueryImg事件
     */
    getQueryImgHandler(img_base64, layers) {
      this.imgURL = img_base64;
      this.clearDrawLayer();
      this.dontShowButton = false;
      //初始化原始图像
      this.imgURL = img_base64;
      let img = new Image();
      img.src = this.imgURL;
      // let that = this;
      img.onload = (res) => {
        this.imgx = res.target.width;
        this.imgy = res.target.height;
        console.log("imgx:", this.imgx);
        this.initMap(true, layers);
      };
      //强制刷新组件
      this.refreshMap = false;
      this.$nextTick(() => {
        this.refreshMap = true;
      });
    },
  },
  mounted() {
    //初始化原始图像
    let img = new Image();
    img.src = this.imgURL;
    let that = this;
    img.onload = function (res) {
      that.imgx = res.target.width;
      that.imgy = res.target.height;
      that.initMap(false);
    };

    //显示原始图像
    this.$bus.$on("sendOrgImg", (img_base64) => {
      this.sendOrgImgHandler(img_base64);
    });
    //显示处理之后的图像
    this.$bus.$on("getLayers", (layers) => {
      this.getLayersHandler(layers);
    });
    this.$bus.$on("getQueryImg", (img_base64, layers) => {
      this.getQueryImgHandler(img_base64, layers);
    });
    this.$bus.$on("destroyMap", (param) => {
      param == 1;
      this.imgURL = "";
      this.showPopup = false;
      this.dontShowButton = true;
      this.clearDrawLayer();
    });
  },
  created() {},
  watch: {
    imgURL: {
      handler(value) {
        //初始化原始图像
        this.imgURL = value;
        let img = new Image();
        img.src = this.imgURL;
        // let that = this;
        img.onload = async (res) => {
          this.imgx = res.target.width;
          this.imgy = res.target.height;
          console.log("imgx:", this.imgx);
          await this.initMap(false);
        };
        //强制刷新组件
        this.refreshMap = false;
        this.$nextTick(() => {
          this.refreshMap = true;
        });
      },
      immediate: false,
    },

    draw_source: {
      handler() {
        this.addDrawLayer();
      },
      deep: true,
    },
    dontShowButton(newval) {
      this.iconColorSetter = newval ? `color:gray` : `color:white`;
    },
  },
};
</script>

<style lang="less" scoped>
.map {
  //border-radius: 3%;
  border: 1px dashed;
  width: 100vw;
  height: 100vh;
  margin: 15%;
  background-color: transparent;
  /* 修改滑块缩放控件的样式 */
}
.draw-tool-container {
  margin-top: 10px;
  margin-bottom: 10px;
  padding-left: 10px;
  padding-right: 5px;
}
.draw-btn {
  background-color: #5C7373;
  border: 0;
}
.draw-tool-container :focus {
  background-color: #7cecd7;
}
.draw-tool-container :hover {
  background-color: gray;
}
.draw-tool-bar {
  display: flex;
  flex-direction: row;
  align-items: center;
  background-color: #2c3740;
  z-index: 500;
}
.ol-popup {
  position: absolute;
  background-color: white;
  -webkit-filter: drop-shadow(0 1px 4px rgba(0, 0, 0, 0.2));
  filter: drop-shadow(0 1px 4px #ffc125);
  padding: 15px;
  border-radius: 5px;
  border: 1px solid #cccccc;
  bottom: 12px;
  left: -50px;
  min-width: 200px;
  color: black;
}

.ol-popup:after,
.ol-popup:before {
  top: 100%;
  border: solid transparent;
  content: " ";
  height: 0;
  width: 0;
  position: absolute;
  pointer-events: none;
}

.ol-popup:after {
  border-top-color: white;
  border-width: 10px;
  left: 48px;
  margin-left: -10px;
}

.ol-popup:before {
  border-top-color: #cccccc;
  border-width: 11px;
  left: 48px;
  margin-left: -11px;
}

.ol-popup-closer {
  text-decoration: none;
  position: absolute;
  top: 2px;
  right: 8px;
  color: red;
}

.ol-popup-closer:after {
  content: "✖";
}
</style>