<template>
  <div class="login_container">
    <div class="login_box">
      <!--表单提交区域-->
      <h2>薛定谔的炼丹炉</h2>
      <el-form
        :rules="loginFormRules"
        ref="loginFormRef"
        label-width="0px"
        class="login_form"
        :model="loginForm"
      >
        <!--用户名-->
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            prefix-icon="iconfont icon-user"
            placeholder="请输入手机号"
            clearable
          ></el-input>
        </el-form-item>
        <!--密码-->
        <el-form-item prop="password">
          <el-input
            type="password"
            v-model="loginForm.password"
            prefix-icon="iconfont icon-3702mima"
            placeholder="请输入密码"
            show-password
            clearable
          ></el-input>
        </el-form-item>
        <!--按钮区-->
        <el-form-item class="btns">
          <el-button
            type="primary"
            @click="gotoHome"
            size="small"
            style="margin-right: 8px"
            >暂不登录</el-button
          >
          <el-checkbox class="remember" v-model="keepPassword"
            >记住密码</el-checkbox
          >
          <el-button type="primary" @click="login">登录</el-button>
          <el-button type="primary" @click="register">注册</el-button>
          <el-button type="info" @click="resetLoginForm">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import baseUrl from "../network/config.js";
export default {
  data() {
    return {
      base_url: baseUrl,
      //base_url: "http://localhost:5000/",
      success: true,
      keepPassword: false, // 记住密码
      loginForm: {
        // 登录的表单数据的绑定对象
        username: "",
        password: "",
      },
      loginFormRules: {
        // 验证用户名是否合法
        username: [
          { required: true, message: "请输入登录名称", trigger: "blur" },
          {
            min: 3,
            max: 11,
            message: "长度在 3 到 11 个字符",
            trigger: "blur",
          },
        ],
        // 验证密码是否合法
        password: [
          { required: true, message: "请输入登录密码", trigger: "blur" },
          {
            min: 5,
            max: 15,
            message: "长度在 5 到 15 个字符",
            trigger: "blur",
          },
        ],
      },
    };
  },
  created() {
    sessionStorage.clear();
  },
  mounted() {
    // 读取cookie
    this.getCookie();
  },
  methods: {
    //前往主页面
    gotoHome() {
      this.$router.push("/home");
    },
    // 记住密码保存数据
    setCookie(name, pwd, exdays) {
      var exdate = new Date(); // 获取时间
      exdate.setTime(exdate.getTime() + 24 * 60 * 60 * 1000 * exdays); // 保存的天数
      // 字符串拼接cookie
      window.document.cookie =
        "userName" + "=" + name + ";path=/;expires=" + exdate.toGMTString();
      window.document.cookie =
        "userPwd" + "=" + pwd + ";path=/;expires=" + exdate.toGMTString();
    },
    // 读取cookie
    getCookie() {
      if (document.cookie.length > 0) {
        this.keepPassword = true;
        var arr = document.cookie.split("; "); // 这里显示的格式需要切割一下自己可输出看下
        console.log(arr);
        for (var i = 0; i < arr.length; i++) {
          var arr2 = arr[i].split("="); // 再次切割
          // 判断查找相对应的值
          if (arr2[0] === "userName") {
            this.loginForm.username = arr2[1]; // 保存到保存数据的地方
          } else if (arr2[0] === "userPwd") {
            this.loginForm.password = arr2[1];
          }
        }
      }
    },
    // 清除cookie
    clearCookie: function () {
      this.setCookie("", "", -1); // 修改2值都为空，天数为负1天就好了
    },
    // 多层嵌套无法输入解决方法
    change() {
      this.$forceUpdate();
    },
    resetLoginForm() {
      // 点击重置按钮,重置登录表单
      console.log(this);
      this.$refs.loginFormRef.resetFields();
    },
    // login(){
    //      this.$store.commit('saveCurrDbSource',this.success)
    //      this.loginLoading = false
    //      document.body.style.background='black';
    //      this.$router.push('/home')
    //      this.$message.success('登录成功')

    // },
    login() {
      // 点击登录按钮，跳转到Home.vue
      this.$refs.loginFormRef.validate(async (valid) => {
        // 验证登录数据
        if (!valid) {
          // 根据登录结果判断是否发起登录请求
          return (this.loginLoading = false);
        }
        var request_data = {
          telephone: this.loginForm.username,
          password: this.loginForm.password,
        };
        request_data = JSON.stringify(request_data);
        const { data: res } = await this.$http.post(
          this.base_url + "/login",
          request_data,
          {
            headers: {
              "content-type": "application/json",
              "Access-Control-Allow-Origin": "*",
            },
          }
        );
        console.log("res", res);
        if (res.code !== 200) {
          this.loginLoading = false;
          return this.$message.error("登录失败 帐号或密码错误!");
        }
        this.$message.success("登录成功!");
        this.$store.commit("saveCurrDbSource", this.success);
        console.log(res.data);
        window.sessionStorage.clear();
        window.sessionStorage.setItem("token", res.data.token);
        if (this.keepPassword) {
          this.setCookie(this.loginForm.username, this.loginForm.password, 7);
        }

        this.$router.push("/home"); // 跳转到home.vue
        this.loginLoading = false;
      });
    },
    register() {
      // 跳转到注册界面
      this.$router.push("/register");
    },
  },
};
</script>
<style lang="less" scoped>
h2 {
  text-align: center;
}

.login_box {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 450px;
  height: 300px;
  background-color: #fff;
  border-radius: 3px;
  .login_form {
    box-sizing: border-box;
    position: absolute;
    bottom: 0;
    width: 100%;
    padding: 0 20px;
  }
  .btns {
    display: flex;
    justify-content: flex-end;
  }
  .remember {
    padding-right: 5px;
  }
}
</style>
