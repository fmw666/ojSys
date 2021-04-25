<template>
  <div id="poster">
    <div>
      <el-form status-icon label-position="left" label-width="100px" class="login-container">
        <h3 class="login_title">竞赛发布用户注册</h3>

        <el-form-item label="单位名称（企业/学校）" prop="username">
          <el-input type="text" @blur="check_username" v-model="username" autocomplete="off"></el-input>
          <span v-show="error_name" class="error_tip" style="display: block">{{ error_name_message }}</span>
        </el-form-item>

        <el-form-item label="密码" prop="pass">
          <el-input type="password" @blur="check_pwd" v-model="password" autocomplete="off"></el-input>
          <span v-show="error_password" class="error_tip">密码最少8位，最长20位</span>
        </el-form-item>

        <el-form-item label="确认密码" prop="checkPass">
          <el-input type="password" @blur="check_cpwd" v-model="password2" autocomplete="off"></el-input>
          <span v-show="error_check_password" class="error_tip">两次输入的密码不一致</span>
        </el-form-item>

        <el-form-item label="手机号" prop="phone">
          <el-input type="tel" @blur="check_phone" v-model="mobile"></el-input>
          <span v-show="error_phone" class="error_tip">{{ error_phone_message }}</span>
        </el-form-item>

        <el-form-item label="短信验证码">
          <el-input @blur="check_sms_code" v-model="sms_code" type="tel"></el-input>
          <el-button type="primary" plain @click="send_sms_code()">{{ sms_code_tip }}</el-button>
          <span v-show="error_sms_code" class="error_tip">{{ error_sms_code_message }}</span>
        </el-form-item>

        <el-form-item>
          <el-checkbox v-model="allow">同意</el-checkbox>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submit">注册</el-button>
          <el-button>重置</el-button>
        </el-form-item>

        <el-row style="text-align: center; margin-top: -10px;;">
          <router-link to="/login"><el-link type="primary">用户登录</el-link></router-link>
        </el-row>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: "SRegister",
  data() {
    return {
      options: [{
          value: '1',
          label: '普通用户'
        }, {
          value: '2',
          label: '竞赛发布人员'
        }],
      value: '',

      error_name: false,
      error_password: false,
      error_check_password: false,
      error_phone: false,
      error_sms_code: false,
      sending_flag: false,

      username: '',
      password: '',
      password2: '',
      mobile: '',
      sms_code: '',
      allow: false,
      sms_code_tip: '获取短信验证码',
      error_sms_code_message: '',
      error_name_message: '',
      error_phone_message: '',
    };
  },
  methods: {
    // 检查用户名
    check_username() {
      const len = this.username.length;
      if (len<5 || len>20) {
        this.error_name_message = '请输入5-20个字符的用户名'
        this.error_name = true;
      } else {
        this.error_name = false;
      }
      // 检查重名
      if (this.error_name === false) {
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
    },
    // 检查密码
    check_pwd() {
      const len = this.password.length;
      if (len<8 || len>20) {
        this.error_password = true;
      } else {
        this.error_password = false;
      }
    },
    // 检查确认密码
    check_cpwd() {
      if (this.password != this.password2) {
        this.error_check_password = true;
      } else {
        this.error_check_password = false;
      }
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
            } else {
              this.error_phone = false;
            }
          })
          .catch(error => {
            console.log(error.response.data);
          })
      }
    },
    // 检查验证码
    check_sms_code() {
      if (!this.sms_code) {
        this.error_sms_code = true;
      } else {
        this.error_sms_code = false;
      }
    },
    // 检查允许
    check_allow() {
      if (!this.allow) {
        this.error_allow = true;
      } else {
        this.error_allow = false;
      }
    },
    submit() {
      this.check_username();
      this.check_pwd();
      this.check_cpwd();
      this.check_phone();
      this.check_sms_code();
      this.check_allow();

      if (this.error_name===false && this.error_password===false && this.error_check_password===false
        && this.error_phone===false && this.error_sms_code===false && this.error_allow===false) {
        this.$axios.post(this.$host + "/api/v1/users/", {
          username: this.username,
          password: this.password,
          mobile: this.mobile,
          sms_code: this.sms_code,
          allow: this.allow.toString()
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

            }
          })
      }
    },
    send_sms_code() {
      if (this.sending_flag === true) {
        return;
      }
      this.sending_flag = true;

      this.check_phone();

      // 向后端发送请求
      this.$axios.get(this.$host + '/api/v1' + '/sms_codes/' + this.mobile + '/', {
        responseType: 'json'
      }).then(response => {
        // 发送成功
        // 倒计时 60s，允许 60s 后用户可以再次点击获取验证码按钮
        let num = 60;
        let t = setInterval(() => {
          if (num === 1) {
            clearInterval(t);
            this.sms_code_tip = '获取短信验证码';
            this.sending_flag = false;
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