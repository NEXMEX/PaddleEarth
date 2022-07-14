<template>
  <header>
    <div class="l-content">薛定谔的炼丹炉</div>
    <div class="r-content">
      <el-button type="info " size="mini" class="tip" plain @click="Tip"
        >帮助
        <i class="el-icon-s-opportunity el-icon--right"></i>
      </el-button>
      <el-dropdown @command="handleCommand" trigger="click" v-if="refresh">
        <el-button type="info" size="small" class="charts" plain>
          <i class="el-icon-s-custom"></i>
        </el-button>
        <el-dropdown-menu slot="dropdown" v-show="false">
          <el-dropdown-item command="Login" v-show="!isLogin"
            >登录</el-dropdown-item
          >
          <el-dropdown-item command="Register" v-show="!isLogin"
            >注册</el-dropdown-item
          >
          <el-dropdown-item command="Logout" v-show="isLogin"
            >退出登录</el-dropdown-item
          >
          <el-dropdown-item command="SwitchAccount" v-show="isLogin"
            >切换账号</el-dropdown-item
          >
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </header>
</template>

<script>
export default {
  name: "CommonHeader",
  data() {
    return {
      isAnalysing: false,
      
      refresh: true,
      bg:require('../assets/background.png')
    };
  },
  computed:{
      isLogin:{
        get: function(){
          return typeof(this.$store.state.currDbSource)==='object'?false:this.$store.state.currDbSource
        },
        set: function(newval){
         this.$store.commit('saveCurrDbSource',newval)
         return newval
         
        }
      }
  },
  methods: {
    //用户点击提示按钮
    Tip(evt) {
      //使按钮失去焦点
      let target = evt.target;
      if (target.nodeName == "SPAN") {
        target = evt.target.parentNode;
      }
      target.blur();
      //显示引导页
      this.$bus.$emit("showHelper", 1);
    },
    handleCommand(command) {
     
      if (command === "Login") {
        if (!this.isLogin) {
          document.body.style.background = `url(${this.bg}) no-repeat`;
          this.$router.push("/login");
        } else {
          this.$message.error("您已登录");
        }
      } else if (command === "Register") {
        if (!this.isLogin) {
          document.body.style.background = `url(${this.bg}) no-repeat`;
          this.$router.push("/register");
        } else {
          this.$message.error("您已登录");
        }
      } else if (command === "Logout") {
        if (this.isLogin) {
          this.$message.success("退出成功");
          this.isLogin = false;
          window.sessionStorage.setItem("token","");
        } else {
          this.$message.error("您尚未登录");
        }
      } else {
        if (this.isLogin) {
          document.body.style.background = `url(${this.bg}) no-repeat`;
          this.$router.push("/login");
          this.isLogin = false;
        } else {
          this.$message.error("您尚未登录");
        }
      }
    },
  },
  mounted() {
    if(window.sessionStorage.getItem("token")){
     this.isLogin=true 
    }
    console.log(this.$store.state)
  },

};
</script>

<style lang="less" scoped>
header {
  margin-top:3px;
  display: flex;
  height: 100%;
  justify-content: space-between;
  align-items: center;
}
.l-content {
  display: flex;
  align-items: center;
  div {
    margin-right: 0px;
  }
}
.r-content {
  display: flex;
  align-items: center;
  div {
    margin-right: 0px;
  }
  .tip {
    color: #2c3740;
    background-color: #5c7373;
    width: 70px;
    height: 30px;
  }
  .charts {
    display: flex;
    align-items: center;
    margin-left: 10px;
    background-color: #5c7373;
    color: #2c3740;
    width: 40px;
    height: 30px;
  }
}
</style>