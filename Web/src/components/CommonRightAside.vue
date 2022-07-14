<template>
  <div class="common-aside">
    <div class="vertical-toolbar1">
      <!-- 展示数据 -->
      <!-- ramrif node_modules -->
      <div class="tool-btn-container" id="analyse-btn">
        <el-tooltip
          class="item"
          effect="dark"
          content="数据分析"
          placement="left"
        >
          <el-button
            @click="showChart"
            circle
            :disabled="isBeforeAnalysing"
            class="tool-btn"
            ><i class="el-icon-data-analysis" :style="iconColorSetter1"></i
          ></el-button>
        </el-tooltip>
      </div>
      <!-- 下载文件按钮 -->
      <div class="tool-btn-container" id="download-btn">
        <el-tooltip
          class="item"
          effect="dark"
          content="保存至本地"
          placement="left"
        >
          <el-button
            @click="downloadData"
            circle
            :disabled="isBeforeAnalysing"
            class="tool-btn"
            ><i class="el-icon-download" :style="iconColorSetter1"></i
          ></el-button>
        </el-tooltip>
      </div>
      <!-- 查询记录按钮 -->
      <div class="tool-btn-container" id="query-btn">
        <el-tooltip
          class="item"
          effect="dark"
          content="处理记录"
          placement="left"
        >
          <el-button @click="queryHistory" circle class="tool-btn"
            ><i class="el-icon-reading" :style="iconColorSetter"></i
          ></el-button>
        </el-tooltip>
      </div>
    </div>

    <div class="vertical-toolbar2">
      <!-- 刷新地图按钮 -->
      <div class="tool-btn-container" id="refresh-btn">
        <el-tooltip class="item" effect="dark" content="刷新" placement="left">
          <el-button @click="destroyMap" circle class="tool-btn"
            ><i class="el-icon-refresh" :style="iconColorSetter"></i
          ></el-button>
        </el-tooltip>
      </div>

      <!-- 处理按钮 -->
      <div class="tool-btn-container" id="process-btn">
        <el-tooltip
          class="item"
          effect="dark"
          content="开始处理"
          placement="left"
        >
          <el-button
            @click="StartAnalysing"
            class="tool-btn"
            circle
            v-loading.fullscreen.lock="fullscreenLoading"
            :disabled="isAfterUpload"
            ><i class="el-icon-coordinate" :style="iconColorSetter3"></i
          ></el-button>
        </el-tooltip>
      </div>
      <!-- 上传文件按钮 -->
      <div class="tool-btn-container" id="upload-btn">
        <el-tooltip
          class="item"
          effect="dark"
          content="上传文件"
          placement="left"
        >
          <el-button
            class="tool-btn"
            @click="uploadImg"
            circle
            :disabled="isBeforeUpload"
            ><i class="el-icon-upload2" :style="iconColorSetter2"></i
          ></el-button>
        </el-tooltip>
      </div>
    </div>
    <!-- 文件上传模块 "https://jsonplaceholder.typicode.com/posts/"-->
    <div>
      <el-dialog :title="`请上传图片  ${fileList.length}/${limit}`" :visible.sync="dialogFormVisible">
        <el-upload
          class="upload-demo"
          drag
          :action="base_url + `/upload`"
          ref="upload"
          
          :file-list="staticFileList"
          :headers="headers"
          :limit="limit"
          :auto-upload="false"
          :before-upload="handleBeforeUpload"
          :on-change="handleFileUploaderChange"
          :on-exceed="handleExceed"
          :on-success="handleSuccess"
          :on-progress="handleProgress"
          list-type="picture"
        >
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          <div class="el-upload__tip" slot="tip">只能上传jpg/png文件</div>
        </el-upload>

        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="UploadAll">确 定</el-button>
        </div>
      </el-dialog>
    </div>
    <el-dialog title="处理历史" :visible.sync="dialogTableVisible">
      <el-table :data="gridData" stripe border height="250">
        <el-table-column
          property="time"
          label="日期"
          width="150"
        ></el-table-column>
        <el-table-column
          property="type"
          label="类型"
          width="150"
        ></el-table-column>
        <el-table-column label="操作" width="100">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="LoadData(scope.row)"
              >加载</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script>
import { Message } from "element-ui";
import baseUrl from "../network/config.js";

export default {
  name: "CommonRightAside",
  data() {
    return {
      staticFileList:[],
      orgImgCount: 0,
      iconColorSetter: `color:white`,
      iconColorSetter1: `color:gray`,
      iconColorSetter2: `color:gray`,
      iconColorSetter3: `color:gray`,
      fullscreenLoading: false,
      gridData: [],
      dialogTableVisible: false,
      result_url: "", //结果图像url
      token: "",
      //  base_url: "http://localhost:10164/",
      base_url: baseUrl,
      processUrl: "",
      limit: undefined,
      headers: {
        //  "Content-Type": "application/x-www-form-urlencoded",
        "Access-Control-Allow-Origin": "*",
      },
      dialogFormVisible: false,
      dialogImageUrl: "",
      fileList: [],
      img_base64ARR: [],
      optionObj: {
        mode: "",
        coordinate: [],
      },
      //控制上方两个按钮
      isBeforeAnalysing: true,
      isBeforeUpload: true, //控制上传按钮
      isAfterUpload: true, //控制处理按钮
      orgImgUrlArr: [], //原始图像数组
      modeCode: -1, //当前处理模式
    };
  },
  computed: {},
  methods: {
    //加载用户数据
    LoadData(row) {
      if (this.orgImgCount === 3) {
        this.$message.error("工作区已满！");
        return;
      }
      console.log(row);
      this.result_url = row.result_url;
      switch (row.type) {
        case "目标提取":
          document.getElementById("target-extraction-btn").click();
          break;
        case "变化检测":
          document.getElementById("change-detection-btn").click();
          break;
        case "目标检测":
          document.getElementById("target-detection-btn").click();
          break;
        case "地物分类":
          document.getElementById("classification-btn").click();
          break;
      }
      console.log("row:", row);
      this.$bus.$emit("getOrgImg", row.image1_url);

      this.$bus.$emit("getQueryImg", row.image1_url, row);
      this.$bus.$emit("getLayers", row);
      this.$message.success("加载成功");
      this.dialogTableVisible = false;
      this.isBeforeAnalysing = false;
    },
    //查询历史记录
    queryHistory() {
      let token = window.sessionStorage.getItem("token");
      if (!token) {
        this.$message.warning("请先登录");
      } else {
        let data = {};
        let query_url = this.base_url + "/query";
        this.$http({
          url: query_url,
          method: "get",
          data: data,
          headers: {
            "content-type": "application/json",
            "Access-Control-Allow-Origin": "*",
            Authorization: "Bearer " + token,
          },
        }).then(
          (response) => {
            console.log(response.data.data);
            for (let i = 0; i < response.data.data.length; i++) {
              this.gridData[response.data.data.length - i - 1] =
                response.data.data[i];
            }
            this.gridData = this.gridData.map((item) => {
              switch (item.type) {
                case 0:
                  item.type = "目标提取";
                  break;
                case 1:
                  item.type = "变化检测";
                  break;
                case 2:
                  item.type = "目标检测";
                  break;
                case 3:
                  item.type = "地物分类";
                  break;
              }
              return item;
            });
            this.dialogTableVisible = true;
          },
          (err) => {
            console.log(err);
            this.$message.error("出问题啦");
          }
        );
      }
    },
    // 开始处理数据
    StartAnalysing(evt) {
      //使按钮失去焦点
      let target = evt.target;
      console.log(target.nodeName);
      if (target.nodeName == "I") {
        target = evt.target.parentNode;
      }
      target.blur();
      this.fullscreenLoading = true;
      console.log(JSON.stringify(this.optionObj));
      this.fileList.splice(0, this.fileList.length);
      // axios.get(`http://api.github.com/search/users?q=test`).then(
      //   (response) => {
      //     console.log("请求成功了");
      //     this.$bus.$emit("getLayers", response.data.items);
      //     this.isBeforeAnalysing=false;
      //   },
      //   (err) => {
      //     console.log("请求失败了", err);
      //   }
      // );
      console.log(this.orgImgUrlArr);
      var data = {
        type: this.modeCode,
        image1_url: this.orgImgUrlArr[0],
        image2_url: this.orgImgUrlArr[1] ? this.orgImgUrlArr[1] : "",
        coordinate: this.optionObj.coordinate,
      };
      this.orgImgUrlArr.splice(0, this.orgImgUrlArr.length);
      data = JSON.stringify(data);
      var request_url = this.base_url + "/interpret";
      let token = window.sessionStorage.getItem("token")
        ? "Bearer " + window.sessionStorage.getItem("token")
        : "";
      this.$http({
        url: request_url,
        method: "post",
        data: data,
        headers: {
          "content-type": "application/json",
          "Access-Control-Allow-Origin": "*",
          Authorization: token,
        },
      }).then(
        (response) => {
          this.isBeforeAnalysing = false;
          this.$message.success("处理结束");
          console.log(typeof response.data, response.data.data);
          this.$bus.$emit("getLayers", response.data.data);
          this.result_url = response.data.data.result_url;
          this.optionObj.coordinate=[]          
          this.fullscreenLoading = false;
        },
        (err) => {
          console.log(err);
          this.$message.error("出问题啦");
          this.fullscreenLoading = false;
        }
      );
    },
    //下载图片
    downloadIamge(imgsrc, name) {
      // 下载图片地址和图片名
      var image = new Image();
      // 解决跨域 Canvas 污染问题
      image.setAttribute("crossOrigin", "anonymous");
      image.onload = function () {
        var canvas = document.createElement("canvas");
        canvas.width = image.width;
        canvas.height = image.height;
        var context = canvas.getContext("2d");
        context.drawImage(image, 0, 0, image.width, image.height);
        var url = canvas.toDataURL("image/png"); // 得到图片的base64编码数据
        var a = document.createElement("a"); // 生成一个a元素
        var event = new MouseEvent("click"); // 创建一个单击事件
        a.download = name || "photo"; // 设置图片名称
        a.href = url; // 将生成的URL设置为a.href属性
        a.dispatchEvent(event); // 触发a的单击事件
      };
      image.src = imgsrc;
    },
    //下载文件
    downloadData(evt) {
      //使按钮失去焦点
      let target = evt.target;
      console.log(target.nodeName);
      if (target.nodeName == "I") {
        target = evt.target.parentNode;
      }
      target.blur();
      this.downloadIamge(this.result_url, "处理结果");
    },
    //显示图表
    showChart(evt) {
      //使按钮失去焦点
      let target = evt.target;
      if (target.nodeName == "I") {
        target = evt.target.parentNode;
      }
      target.blur();
      this.$bus.$emit("showAnaChart", 1);
    },
    //刷新地图
    destroyMap(evt) {
      //使按钮失去焦点
      let target = evt.target;
      if (target.nodeName == "I") {
        target = evt.target.parentNode;
      }
      target.blur();
      this.$bus.$emit("destroyMap", 1);
      this.fileList = [];
      this.isBeforeAnalysing = true;
      this.isBeforeUpload = true;
      this.isAfterUpload = true;
    },
    //上传按钮点击事件
    uploadImg() {
      if (this.orgImgCount === 3) {
        this.$message.error("工作区已满！");
        return;
      }
      if (this.orgImgCount === 2&&this.modeCode===1) {
        this.$message.error("工作区容量不足！");
        return;
      }
      this.dialogFormVisible = true;
      this.limit = this.optionObj.mode === "变化检测" ? 2 : 1;
    },
    //文件上传时
    // eslint-disable-next-line
    handleProgress(event,file,fileList){
        
    },
    //照片发送之前
    handleBeforeUpload(file) {
      if(file===undefined){
        return false;
      }
      console.log(this.fileList);
      if (this.fileList.length != 2 && this.modeCode === 1) {
        this.fileList.splice(0, this.fileList.length);
        this.$message({
          showClose: true,
          message: "请上传两张图片，第一张为变化前，第二张为变化后",
          type: "warning",
        });
        return false;
      }
      if (file.size <= 0) {
        return false;
      }
    },

    handleRemove() {},
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
    },
    //文件上传超过限制
    handleExceed() {
      Message({
        message: `最多上传${this.limit}张图片!`,
        type: "error",
      });
    },
    //上传所有文件
    UploadAll() {
      this.$refs.upload.submit();
    },
    //上传状态改变时的处理
    handleFileUploaderChange(file) {
      if(this.modeCode===1 && this.fileList.length===2){
        this.fileList.splice(1,1);
        this.fileList.unshift(file);
        this.orgImgUrlArr.push(file.response.data.image_url);
        return;
      }
      if(this.modeCode!==1&& this.fileList===1){
        return;
      }
      console.log("im in change!!!!!!!!!!!!", file);
      
      this.fileList.unshift(file);
      if(file.response!=undefined){
        this.orgImgUrlArr.push(file.response.data.image_url);
      }
      
    },
    //上传成功后的处理

    handleSuccess(response, file, fileList) {
      setTimeout(()=>{

      },3000)
      response == fileList;
      //让代码不报错
      file === file;
      this.fileList = fileList;
      // eslint-disable-next-line
      const self = this;   
      var flag = true;
      flag === flag;
      
      console.log("response",response)
      console.log("fileList",fileList)    
      this.fileList.forEach((file) => {
        console.log("file.response", file.response);
        let reader = new FileReader();
        reader.readAsDataURL(file.raw);
        reader.onload = function () {
          let img_base64 = this.result;
          self.img_base64ARR.push(img_base64);
          if (flag) {
            self.$bus.$emit("sendOrgImg", img_base64);
            flag = false;
          }
          self.$bus.$emit("getOrgImg", img_base64);
        };
        this.$refs.upload.clearFiles();
        
      });
      Message({
        message: `上传成功`,
        type: "success",
      });
      this.isAfterUpload = false;
      this.$bus.$emit("optionObj", this.optionObj.mode);
    },
  },
  mounted() {
    console.log(baseUrl);
    console.log(this.orgImgUrlArr);
    this.token =
      window.sessionStorage.getItem("token") === null
        ? this.token
        : window.sessionStorage.getItem("token");
    window.sessionStorage.getItem("token");
    console.log("token", this.token);
    this.$bus.$on("getDrawParam", (coordinates) => {
      this.optionObj.coordinate = coordinates[0].map((item) => {
        //  item[0]=item[0]/100;
        //  item[1]=item[1]/100;
        return item;
      });
      console.log(this.optionObj.coordinate);
    });
    this.$bus.$on("sendModeCode", (mode, processUrl) => {
      switch (mode) {
        case "目标提取":
          this.modeCode = 0;
          break;
        case "变化检测":
          this.modeCode = 1;
          break;
        case "目标检测":
          this.modeCode = 2;
          break;
        case "地物分类":
          this.modeCode = 3;
          break;
      }
      this.optionObj.mode = mode;
      this.isBeforeUpload = false;
      this.processUrl = processUrl;
    });
    this.$bus.$on("workAreaCount", (cnt) => {
      this.orgImgCount = cnt;
    });
  },
  watch: {
    dialogFormVisible(newval) {
      if (!newval) {
        this.fileList = [];
      }
    },
    isBeforeAnalysing(newval) {
      this.iconColorSetter1 = newval ? `color:gray` : `color:white`;
    },
    isBeforeUpload(newval) {
      this.iconColorSetter2 = newval ? `color:gray` : `color:white`;
    },
    isAfterUpload(newval) {
      this.iconColorSetter3 = newval ? `color:gray` : `color:white`;
    },
  },
};
</script>

<style scoped lang="less">
.vertical-toolbar1 {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #2c3740;
  border-radius: 10%;
}
.vertical-toolbar2 {
  margin-top: 600%;
  display: flex;
  flex-direction: column-reverse;
  align-items: center;
  background-color: #2c3740;
  border-radius: 10%;
  margin-bottom: 50px;
}
.tool-btn-container {
  margin: 3px;
  padding: 5px;
}
.tool-btn {
  background-color: #5C7373;
  border: 0;
}
.tool-btn-container :focus {
  background-color: #7cecd7;
}
.tool-btn-container :hover {
  background-color: gray;
}
</style>