<template>
  <div id="login">
    <el-form status-icon label-position="left" label-width="100px" class="login-container">
      <h3 class="login_title">用户登录</h3>

      <el-form-item label="用户名或手机号" prop="username">
        <el-input type="text" @blur="check_username" v-model="username" autocomplete="off"></el-input>
        <span v-show="error_username" class="error_tip" style="display: block">{{ error_name_message }}</span>
      </el-form-item>

      <el-form-item label="密码" prop="pass">
        <el-input type="password" @blur="check_pwd" v-model="password" autocomplete="off"></el-input>
        <span v-show="error_pwd" class="error_tip">密码最少8位，最长20位</span>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submit">登录</el-button>
        <el-button>重置</el-button>
      </el-form-item>

      <el-row style="text-align: center; margin-top: -10px;;">
        <router-link to="/forget"><el-link type="primary">忘记密码</el-link></router-link>
        <router-link to="/register"><el-link type="primary">用户注册</el-link></router-link>
      </el-row>
    </el-form>
  </div>
</template>

<script>
  export default {
    name: "login",
    data() {
      return {
        username: '',
        password: '',
        error_username: false,
        error_pwd: false,
        remember: false,
      };
    },
    methods: {
      check_username() {

      },
      check_pwd() {

      },
      get_query_string(name) {
        const reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
        const r = window.location.search.substr(1).match(reg);
        if (r != null) {
            return decodeURI(r[2]);
        }
        return null;
      },
      submit() {
        this.check_username();
        this.check_pwd();

        if (this.error_username === false && this.error_pwd === false) {
          this.$axios.post("http://127.0.0.1:8000/api-token-auth/", {
            username: this.username,
            password: this.password
          }, {
            responseType: 'json',
            withCredentials: true
          })
          .then(response => {
            if (this.remember) {
              // 记住登录
              sessionStorage.clear();
              localStorage.token = response.data.token;
              localStorage.user_id = response.data.user_id;
              localStorage.username = response.data.username;
            } else {
              // 未记住登录
              localStorage.clear();
              sessionStorage.token = response.data.token;
              sessionStorage.user_id = response.data.user_id;
              sessionStorage.username = response.data.username;
            }
            // 跳转页面
            let return_url = this.get_query_string('next');
            if (!return_url) {
              return_url = '/';
            }
            location.href = return_url
          })
        }
      },
    }
  }
</script>

<style scoped>
  #login {
    /*background: url("../assets/code-bg.jpg") no-repeat center;*/
    height: 100%;
    width: 100%;
    background-size: cover;
    position: fixed;
  }

  .login-container {
    border-radius: 15px;
    background-clip: padding-box;
    margin: 90px auto;
    width: 350px;
    padding: 35px 35px 15px 35px;
    background: #fff;
    border: 1px solid #eaeaea;
    box-shadow: 0 0 25px #cac6c6;
  }

  .login_title {
    margin: 0px auto 40px auto;
    text-align: center;
    color: #505458;
  }
</style>