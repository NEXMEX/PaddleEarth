<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script >
import "animate.css";

export default {
  name: "App",
  data() {
    return {
      base_url: "http://172.22.27.65:9090",
    };
  },
  methods: {},
  components: {},
  mounted() {
    this.$router.push("/welcome");
  },
  beforeDestroy() {
    this.$bus.$off("showRightAside");
    this.$bus.$off("getLayers");
    this.$bus.$off("sendOrgImg");
    this.$bus.$off("optionObj");
    this.$bus.$off("getDrawParam");
    this.$bus.$off("sendModeCode");
    this.$bus.$off("showAnaChart");
    this.$bus.$off("destroyMap");
    this.$bus.$off("workAreaCount");
    this.$bus.$off("getQueryImg");
  },
};
</script>

<style lang="less">
html,
body {
  margin: 0;
  padding: 0;
  background-color: transparent;
  overflow: hidden;
}
#app {
  height: 100vh;
  width: 100vw;
  font-family: "Microsoft YaHei";

  background-size: 100% 100%;
}
#common-aside {
  background-color: transparent;
}
.ol-zoomslider {
  top: 120px;
}

/* 修改鹰眼图控件的样式 */
.ol-overviewmap {
  bottom: 40px;
}

/* 修改坐标拾取控件的样式 */
.ol-mouse-position {
  top: initial;
  bottom: 0px;
  right: 200px;
}

/* 修改旋转控件的样式 */
.ol-rotate {
  right: 40px;
}
</style>
