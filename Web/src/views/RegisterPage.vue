<template>
  <div class="box">
    <div class="zhuce">
      <el-form
        :model="ruleForm"
        :rules="rules"
        ref="ruleForm"
        label-width="100px"
        class="demo-ruleForm"
      >
        <el-form-item label="账号名称" prop="user">
          <el-input v-model="ruleForm.name" clearable></el-input>
        </el-form-item>
        <el-form-item label="手机号码" prop="mobile">
          <el-input v-model="ruleForm.telephone" clearable></el-input>
        </el-form-item>
        <el-form-item label="账号密码" prop="pass">
          <el-input
            type="password"
            v-model="ruleForm.password"
            clearable
          ></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="checkPass">
          <el-input
            type="password"
            v-model="ruleForm.checkPass"
            clearable
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm2')"
            >注册</el-button
          >
          <el-button @click="returnForm">取消</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>
<script>
import baseUrl from "../network/config.js";
export default {
  name: "RegisitorPage",
  data() {
    var checkUser = (rule, value, callback) => {
      console.log(rule);
      const regUser = /^[a-zA-Z0-9_-]{3,16}$/;
      if (regUser.test(value)) {
        return callback();
      }
      callback(new Error("用户名不能为空"));
    };
    var checkMobile = (rule, value, callback) => {
      console.log(rule);
      const regUser = /^((0\d{2,3}-\d{7,8})|(1[34578]\d{9}))$/;
      if (regUser.test(value)) {
        return callback();
      }
      callback(new Error("手机号码不能为空"));
    };
    // var checkEmail = (rule, value, callback) => {
    //   console.log(rule);
    //   const regUser = /^([a-zA-Z0-9]+[-_]?)+@[a-zA-Z0-9]+\.[a-z]+$/;
    //   if (regUser.test(value)) {
    //     return callback();
    //   }
    //   callback(new Error("邮箱不能为空"));
    // };
    var validatePass = (rule, value, callback) => {
      console.log(rule);
      if (value === "") {
        callback(new Error("请输入密码"));
      } else {
        if (this.ruleForm.checkPass !== "") {
          this.$refs.ruleForm.validateField("checkPass");
        }
        callback();
      }
    };
    var validatePass2 = (rule, value, callback) => {
      console.log(rule);
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.ruleForm.password) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      }
    };
    return {
      base_url: baseUrl,
      //base_url: "http://localhost:10164/",
      grouplist: undefined,
      ruleForm: {
        name: "",
        telephone: "",
        // email: "",
        password: "",
        checkPass: "",
      },
      rules: {
        name: [{ validator: checkUser, trigger: "blur" }],
        telephone: [{ validator: checkMobile, trigger: "blur" }],
        // email: [{ validator: checkEmail, trigger: "blur" }],
        password: [{ validator: validatePass, trigger: "blur" }],
        checkPass: [{ validator: validatePass2, trigger: "blur" }],
      },
    };
  },
  methods: {
    returnForm() {
      // 返回login界面
      this.$router.push("/login");
    },
    submitForm() {
      console.log(this.ruleForm);
      var data = this.ruleForm;
      delete data.checkPass;
      data = JSON.stringify(data);
      console.log(data);
      this.$http({
        url: this.base_url + "/register",
        method: "post",
        headers: {
          "content-type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
        data: data,
      }).then(
        (response) => {
          console.log(response.body);
          this.grouplist = response.body;
          this.$message.success("注册成功！");
          this.$router.push("/login");
        },
        (response) => {
          console.log(response);
          this.$message.error("出问题啦！！！");
        }
      );
    },
  },
  mounted() {},
};
</script>
<style lang="less" scoped>
.box {
  height: 100%;
}
.zhuce {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 450px;
  height: 400px;
  background-color: #fff;
  border-radius: 3px;
}
.el-form-item {
  margin-top: 30px;
  width: 400px;
}
</style>

