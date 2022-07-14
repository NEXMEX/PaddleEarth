<template>
  <div class="common-aside">
    <!-- 功能选择模块 -->
    <div class="select-bar" id="mode-selector">
      <el-row :gutter="20">
        <span><i class="bar-chart"></i>解译算法</span>

        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

        <span>当前模式：{{ mode }}</span>
      </el-row>
      <el-row class="mode-bar" :gutter="24">
        <el-col :span="6"
          ><div class="grid-content bg-purple">
            <el-tooltip
              class="item"
              effect="dark"
              content="目标提取"
              placement="bottom"
            >
              <div class="left-button-container">
                <el-button
                  id="target-extraction-btn"
                  @click="setMode(0)"
                  circle
                  plain
                  icon="road"
                  class="left-button"
                  ><i class="road"></i
                ></el-button>
              </div>
            </el-tooltip></div
        ></el-col>
        <el-col :span="6"
          ><div class="grid-content bg-purple">
            <el-tooltip
              class="item"
              effect="dark"
              content="变化检测"
              placement="bottom"
            >
              <div class="left-button-container">
                <el-button
                  id="change-detection-btn"
                  type="info"
                  @click="setMode(1)"
                  circle
                  plain
                  class="left-button"
                  ><i class="house"></i
                ></el-button>
              </div>
            </el-tooltip></div
        ></el-col>
        <el-col :span="6"
          ><div class="grid-content bg-purple">
            <el-tooltip
              class="item"
              effect="dark"
              content="目标检测"
              placement="bottom"
            >
              <div class="left-button-container">
                <el-button
                  id="target-detection-btn"
                  type="info"
                  @click="setMode(2)"
                  circle
                  plain
                  class="left-button"
                  ><i class="court"></i
                ></el-button>
              </div>
            </el-tooltip></div
        ></el-col>
        <el-col :span="6"
          ><div class="grid-content bg-purple">
            <el-tooltip
              class="item"
              effect="dark"
              content="地物分类"
              placement="bottom"
            >
              <div class="left-button-container">
                <el-button
                  id="classification-btn"
                  type="info"
                  @click="setMode(3)"
                  circle
                  plain
                  class="left-button"
                  ><i class="pine-tree"></i
                ></el-button>
              </div>
            </el-tooltip></div
        ></el-col>
      </el-row>
    </div>
    <div id="user-data-box">
      <div class="user-data-header">
        <i class="user-data"></i><span>我的数据</span>
        <span style="margin-left: 85px"
          >工作区{{ img_base64ARR.length }}/3</span
        >
      </div>

      <div class="orgImgsBox">
        <div
          class="OrgImgs"
          v-for="(img_base64, index) in img_base64ARR"
          :key="index"
        >
          <el-image
            :src="img_base64"
            :fit="fit"
            :preview-src-list="img_base64ARR"
            style="margin-left: 25%; margin-right: 25%"
          ></el-image>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CommonLeftAside",
  data() {
    return {
      data_box_height: 500,
      //   选择要使用的功能
      options: [
        {
          mode: "TargetExtraction",
          label: "目标提取",
        },
        {
          mode: "ChangeDetection",
          label: "变化检测",
        },
        {
          mode: "TargetDetection",
          label: "目标检测",
        },
        {
          mode: "Classificaton",
          label: "地物分类",
        },
      ],
      optionObj: {
        mode: "",
        coordinate: undefined,
      },
      limit: 1,
      dialogFormVisible: false,
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      isShowChart: false,
      orginalImg: {},
      processUrl: "",
      fileList: [],
      img_base64ARR: [],
      fit: "contain",
      mode: "",
    };
  },
  methods: {
    // 设置发送处理请求的url
    setMode(modeNum) {
      switch (modeNum) {
        case 0:
          this.processUrl = "http://xxx/objectextraction";
          this.mode = "目标提取";
          break;
        case 1:
          this.processUrl = "http://xxx/changedetection";
          this.mode = "变化检测";
          break;
        case 2:
          this.processUrl = "http://xxx/objectdetection";
          this.mode = "目标检测";
          break;
        case 3:
          this.processUrl = "http://xxx/classifiction";
          this.mode = "地物分类";
          break;
      }
      this.$bus.$emit("sendModeCode", this.mode, this.processUrl);
    },
  },
  mounted() {
    //设置该次请求的坐标
    this.$bus.$on("getDrawParam", (coordinates) => {
      this.optionObj.coordinate = coordinates[0];
    });
    this.$bus.$on("getOrgImg", (img_base64) => {
      this.img_base64ARR.push(img_base64);
      if (this.img_base64ARR.length > 3) {
        this.data_box_height += 80;
        document.getElementById("user-data-box").style.height =
          this.data_box_height + "px";
      }
    });
    this.$bus.$on("destroyMap", (p) => {
      p === 1;
      this.mode = "";
      this.img_base64ARR.splice(0, this.img_base64ARR.length);
      this.data_box_height = 500;
      document.getElementById("user-data-box").style.height =
        this.data_box_height + "px";
    });
  },
  watch: {
    img_base64ARR: {
      handler(newval) {
        this.$bus.$emit("workAreaCount", newval.length);
      },
      deep: true,
    },
  },
};
</script>

<style lang="less" scoped>
.common-aside {
  overflow-x: hidden;
  position: relative;
}
#user-data-header {
  display: flex;
  align-items: center;
  margin-left: 10px;
}

#user-data-box {
  background-color: #2c3740;
  width: 100%;
  border-radius: 5%;
  // height:100%;
  height: 500px;
  margin-top: 10px;
}
.left-button {
  background-color: #5C7373;
  border: 0;
}
.left-button-container :focus {
  background-color: #7cecd7;
}
.left-button-container :hover {
  background-color: gray;
}
h4 {
  padding-top: 3px;
}
.orgImgsBox {
  width: 280px;
  border-radius: 5%;
}
.OrgImgs {
  background-color: transparent;
  width: 80%;
  border-radius: 5%;
  margin-left: 10%;
  margin-top: 10px;
  border: 1px dashed;
}
.mode-bar {
  padding-top: 15px;
  padding-bottom: 15px;
}
.user-data {
  display: inline-block;
  width: 25px;
  height: 25px;
  margin-left: 10px;
  background-image: url(../assets/user-data.png);
  background-position: center center;
  background-size: 25px 25px;
  padding: 5px;
  background-repeat: no-repeat;
}
.road {
  display: inline-block;
  width: 20px;
  height: 20px;
  margin-left: 2px;
  margin-right: 2px;
  background-image: url(../assets/road.svg);
  background-position: center center;
  background-size: 20px 20px;
  background-repeat: no-repeat;
  border-radius: 50%;
}
.house {
  display: inline-block;
  width: 20px;
  height: 20px;
  margin-left: 2px;
  margin-right: 2px;
  background-image: url(../assets/house.png);
  background-position: center center;
  background-size: 20px 20px;
  background-repeat: no-repeat;
}
.court {
  display: inline-block;
  width: 20px;
  height: 20px;
  margin-left: 2px;
  margin-right: 2px;
  background-image: url(../assets/court.png);
  background-position: center center;
  background-size: 20px 20px;
  background-repeat: no-repeat;
}
.pine-tree {
  display: inline-block;
  width: 20px;
  height: 20px;
  margin-left: 2px;
  margin-right: 2px;
  background-image: url(../assets/pine-tree.png);
  background-position: center center;
  background-size: 20px 20px;
  background-repeat: no-repeat;
}
.bar-chart {
  display: inline-block;
  width: 30px;
  height: 30px;
  margin-left: 5px;
  margin-right: 5px;
  background-image: url(../assets/bar-chart.png);
  background-position: center center;
  background-size: 30px 30px;
  background-repeat: no-repeat;
}
.select-bar {
  border-radius: 15px;
  background-color: #2c3740;
  padding: 10px;
  padding-bottom: 20px;
  margin-top: 10px;
}
.select-box {
  // 未选中任何选项的时候 placeholder的样式 需要先选中父元素 增加权重
  /deep/ input::-webkit-input-placeholder {
    color: #fff;
  }
  /deep/ input::-moz-input-placeholder {
    color: #fff;
  }
  /deep/ input::-ms-input-placeholder {
    color: rgb(171, 30, 30);
  }

  //修改的是el-input的样式
  //一种方法是设置最里层el-input__inner的背景色 外层的两级父元素设置为透明色
  //另一种方法是从el-select到el-input__inenr的背景色都设置为需要的颜色
  /deep/ .el-select,
  /deep/ .el-input,
  /deep/ .el-input__inner {
    background-color: #030510;
    color: #fff;
    border: 0px;
    border-radius: 5px;
    text-align: center;
  }

  //el-input聚焦的时候 外层的border会有一个样式
  /deep/ .el-select .el-input.is-focus .el-input__inner {
    border: 0px;
  }
  //修改总体选项的样式 最外层
  /deep/ .el-select-dropdown {
    background-color: #4c5885;
    margin: 0px;
    border: 0px;
    border-radius: 0px;
  }

  //修改单个的选项的样式
  /deep/ .el-select-dropdown__item {
    background-color: #409eff;
    color: rgb(197, 128, 128);
  }

  //item选项的hover样式

  /deep/ .el-select-dropdown__item:hover {
    color: #409eff;
  }

  //修改的是下拉框选项内容上方的尖角
  /deep/ .el-popper .popper__arrow,
  .el-popper .popper__arrow::after {
    display: none;
  }
}
</style>