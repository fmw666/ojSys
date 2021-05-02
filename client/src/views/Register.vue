<template>
  <div id="poster">
    <div>
      <el-form status-icon label-position="left" label-width="100px" class="login-container">
        <h3 class="login_title">用户注册</h3>

        <el-form-item label="用户名" prop="username">
          <el-input type="text" v-model="username" autocomplete="off"></el-input>
          <el-alert v-show="error_name" v-bind:title="error_name_message" type="warning" ></el-alert>
        </el-form-item>

        <el-form-item label="密码" prop="pass">
          <el-input type="password" v-model="password" autocomplete="off"></el-input>
          <el-alert v-show="error_password" title="密码最少8位，最长20位" type="warning" ></el-alert>
        </el-form-item>

        <el-form-item label="确认密码" prop="checkPass">
          <el-input type="password" v-model="password2" autocomplete="off"></el-input>
          <el-alert v-show="error_check_password" title="两次输入的密码不一致" type="warning" ></el-alert>
        </el-form-item>

        <el-form-item label="手机号" prop="phone">
          <el-input type="tel" v-model="mobile"></el-input>
          <el-alert v-show="error_phone" v-bind:title="error_phone_message" type="warning" ></el-alert>
        </el-form-item>

        <el-form-item label="短信验证码">
          <el-input style="width: 100px; margin-right: 10px" v-model="sms_code" type="tel"></el-input>
          <el-button type="primary" v-bind:disabled=btn_disabled @click="send_sms_code()">{{ sms_code_tip }}</el-button>
        </el-form-item>


        <el-form-item>
          <el-button type="primary" @click="submit">注册</el-button>
          <el-button @click="reset">重置</el-button>
        </el-form-item>

        <el-divider></el-divider>

        <el-row style="text-align: center; margin-top: 5px;">
          <el-link class="set_center" @click="toPath('/login')" type="primary">已有帐户？马上登录</el-link>
        </el-row>
      </el-form>
    </div>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus'
export default {
  name: "Register",
  data() {
    return {

      error_name: false,
      error_password: false,
      error_check_password: false,
      error_phone: false,
      phone_exist: false,
      error_sms_code: false,
      sending_flag: false,

      username: '',
      password: '',
      password2: '',
      mobile: '',
      sms_code: '',
      sms_code_tip: '获取短信验证码',
      btn_disabled: false,
      error_sms_code_message: '',
      error_name_message: '',
      error_phone_message: '',
    };
  },
  watch: {
    // 检查用户名
    username: {
      handler(old_val, new_val) {
        const len = this.username.length;
        if (len > 0) {
          if (len<5 || len>20) {
            this.error_name_message = '请输入5-20个字符的用户名'
            this.error_name = true;
          } else {
            this.error_name = false;
          }
        } else if (len === 0) {
          this.error_name = false
        }
        // 检查重名
        if (this.error_name === false && len > 0) {
          this.$axios.get(this.$host + "/api/v1/users/username/" + this.username + '/count/', {
            responseType: 'json'
          })
          .then(response => {
            if (response.data.count > 0) {
              this.error_name_message = '用户名已存在';
              this.error_name = true;
            } else {
              this.error_name = false;
            }
          })
          .catch(error => {
            console.log(error.response.data);
          })
        }
      }
    },
    // 检查密码
    password: {
      handler(old_val, new_val) {
        const len = this.password.length;
        if (len > 0) {
          this.error_password = len < 8 || len > 20;
        } else if (len === 0) {
          this.error_password = false
        }
      }
    },
    // 检查确认密码
    password2: {
      handler(old_val, new_val) {
        this.error_check_password = this.password !== this.password2;
      }
    },
    // 检查手机号
    mobile: {
      handler(old_val, new_val) {
        this.check_phone()
      }
    },
  },
  methods: {
    // 路由跳转
    toPath(isPath) {
      this.$router.push(isPath);
    },
    // 重置表单
    reset() {
      this.username = ''
      this.password = ''
      this.password2 = ''
      this.mobile = ''
      this.sms_code = ''
      this.error_name = false
      this.error_password = false
      this.error_check_password = false
      this.error_phone = false
      this.phone_exist = false
      this.error_sms_code = false
    },
    // 检查手机号
    check_phone() {
      const re = /^1[3-9]\d{9}$/;
      if (re.test(this.mobile)) {
        this.error_phone = false;
      } else {
        this.error_phone_message = '您输入的手机号格式不正确';
        this.error_phone = true;
      }
      if (this.error_phone === false) {
        this.$axios.get(this.$host + "/api/v1/users/mobile/" + this.mobile + '/count/', {
          responseType: 'json'
        })
          .then(response => {
            if (response.data.count > 0) {
              this.error_phone_message = '手机号已存在';
              this.error_phone = true;
              this.phone_exist = true;
            } else {
              this.error_phone = false;
              this.phone_exist = false;
            }
          })
          .catch(error => {
            console.log(error.response.data);
          })
      }
    },
    // 检查验证码
    check_sms_code() {
      this.error_sms_code = !this.sms_code;
    },
    submit() {
      this.check_sms_code();

      if (this.error_name===false && this.error_password===false && this.error_check_password===false
        && this.error_phone===false && this.error_sms_code===false) {
        this.$axios.post(this.$host + "/api/v1/users/", {
          username: this.username,
          password: this.password,
          mobile: this.mobile,
          sms_code: this.sms_code,
          allow: 1
        }, {
          responseType: 'json'
        })
          .then(response => {
            // 记录用户的登录状态
            sessionStorage.clear();
            localStorage.clear();
            localStorage.token = response.data.token;
            localStorage.username = response.data.username;
            localStorage.user_id = response.data.id;
            location.href = '/';
          })
          .catch(error => {
            if (error.response.status === 400) {
              ElMessage.error('请检查您的短信验证码');
            }
          })
      } else {
        ElMessage.error('请检查您的短信验证码');
      }
    },
    send_sms_code() {
      this.check_phone();
      if (this.error_phone === true || this.phone_exist === true) {
        return;
      }
      if (this.sending_flag === true) {
        return;
      }
      this.sending_flag = true;

      // 向后端发送请求
      this.$axios.get(this.$host + '/api/v1' + '/sms_codes/' + this.mobile + '/', {
        responseType: 'json'
      }).then(response => {
        // 发送成功
        // 倒计时 60s，允许 60s 后用户可以再次点击获取验证码按钮
        let num = 60;
        this.btn_disabled = true;
        let t = setInterval(() => {
          if (num === 1) {
            clearInterval(t);
            this.sms_code_tip = '获取短信验证码';
            this.sending_flag = false;
            this.btn_disabled = false;
          } else {
            num -= 1;
            this.sms_code_tip = num + '秒';
          }
        }, 1000, 60)
      })
      .catch(error => {
        if (error.response.status === 400) {

        }
        this.sending_flag = false;
      })
    }
  }
}
</script>

<style scoped>
  #poster {
    /*background: url("../assets/code-bg.jpg") no-repeat center;*/
    height: 100%;
    width: 100%;
    background-size: cover;
    position: fixed;
  }

  .login-container {
    border-radius: 15px;
    background-clip: padding-box;
    margin: 7% auto;

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