<template>
  <div id="login">
    <el-form status-icon label-position="left" label-width="105px" class="login-container">
      <h3 class="login_title">用户登录</h3>

      <el-form-item label="用户名/手机号" prop="username">
        <el-input type="text" v-model="username" autocomplete="off"></el-input>
        <el-alert v-show="error_username" title="请输入3-20个字符的用户名" type="warning" ></el-alert>
      </el-form-item>

      <el-form-item label="密码" prop="pass">
        <el-input type="password" v-model="password" autocomplete="off"></el-input>
        <el-alert v-show="error_password" title="密码最少8位，最长20位" type="warning"></el-alert>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submit">登录</el-button>
        <el-button @click="reset">重置</el-button>
      </el-form-item>

      <el-divider></el-divider>

      <el-row style="margin-top: 5px; position: relative;">
        <el-link @click="to_path('/forget')" type="primary">忘记密码</el-link>
        <span class="set_center">&emsp;|&emsp;</span>
        <el-link @click="to_path('/register')" type="primary">用户注册</el-link>
        <span class="set_center" style="position: absolute; right: 0">
          <el-checkbox v-model="remember">记住账户？</el-checkbox>
        </span>
      </el-row>
    </el-form>
  </div>
</template>

<script>
import {Base, Auth} from '../../components/mixins'

import {ElMessage} from "element-plus";

export default {
  name: "login",
  mixins: [Base, Auth],
  data() {
    return {
      password: '',
      error_username: false,
      error_password: false,
      remember: false,
    };
  },
  watch: {
    username: {
      handler(old_val, new_val) {
        const len = this.username.length;
        if (len > 0) {
          this.error_username = len < 3 || len > 20;
        } else if (len === 0) {
          this.error_username = false
        }
      }
    },
    password: {
      handler(old_val, new_val) {
        const len = this.password.length;
        if (len > 0) {
          this.error_password = len < 8 || len > 20;
        } else if (len === 0) {
          this.error_password = false
        }
      }
    }
  },
  created() {
    // 判断用户登录状态
    if (this.user_id && this.token) {
      this.$axios.get(this.$host + "/api/v1/user/", {
      // 向后端传递 JWT token 的方法
      headers: {
        'Authorization': 'JWT ' + this.token
      },
      responseType: 'json'
      }).then(response => {
        console.log(response.data)
        this.username = response.data.username
        ElMessage.warning('请在退出登录后再访问')
        this.$router.push('/')
      }).catch(error => {

      });
    }
  },
  methods: {
    submit() {
      if (this.error_username === false && this.error_password === false && this.username !== '' && this.password !== '') {
        this.$axios.post(this.$host + "/api-token-auth/", {
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
        .catch(error => {
          ElMessage.error('用户名/手机号 或 密码 有误');
        })
      } else {
        ElMessage.error('请检查您的输入');
      }
    },
    // 重置表单
    reset() {
      this.username = ''
      this.password = ''
      this.error_username = false
      this.error_password = false
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
    margin: 10% auto;
    width: 350px;
    padding: 35px 35px 15px 35px;
    background: #fff;
    border: 1px solid #eaeaea;
    box-shadow: 0 0 25px #cac6c6;
  }

  .login_title {
    margin: 0 auto 40px auto;
    text-align: center;
    color: #505458;
  }

  .set_center {
    vertical-align: middle;
    height: 25px;
    line-height: 25px;
  }
</style>