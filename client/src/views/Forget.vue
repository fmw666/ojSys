<template>
  <div id="forget">
    <el-form status-icon label-position="top" label-width="10px" class="container">
      <h3 class="title">找回密码</h3>

      <div>
        <el-steps :active="active" finish-status="success" simple style="margin-top: 20px">
          <el-step v-bind:title="step1" ></el-step>
          <el-step v-bind:title="step2" ></el-step>
          <el-step v-bind:title="step3" ></el-step>
        </el-steps>
      </div>

      <el-form-item v-if="active===0" style="text-align: center; margin: 40px 0">
        <el-select v-model="ways" placeholder="请选择验证方式" style="margin-right: 20px; width: 200px">
          <el-option label="手机号" value="1"></el-option>
          <el-option label="邮箱号" value="2"></el-option>
        </el-select>
        <el-button type="primary" v-bind:disabled="is_choose" round @click="next">确定<i class="el-icon-caret-right el-icon--right"></i></el-button>
      </el-form-item>

      <el-form-item v-if="active===1" style="margin: 40px 0">
        <el-input v-if="ways==='1'" placeholder="请输入手机号" v-model="mobile" maxlength="11" style="width: 200px; margin: 0 20px 0 70px" clearable show-word-limit></el-input>
        <el-input v-if="ways==='2'" placeholder="请输入邮箱号" v-model="mobile" style="width: 250px; margin-right: 20px" clearable></el-input>
        <el-button round v-bind:disabled="btn_disabled" @click="send_sms_code">{{sms_code_tip}}</el-button>
      </el-form-item>

      <el-form-item v-if="active===1" style="text-align: center; margin: 40px 0">
        <el-input placeholder="请输入验证码" v-model="sms_code" style="width: 120px;margin: 0 20px 0 54px"></el-input>
        <el-button type="primary" round @click="verify">验证<i class="el-icon-caret-right el-icon--right"></i></el-button>
      </el-form-item>

      <el-form-item v-if="active===1">
        <el-button round @click="prev"><i class="el-icon-caret-left el-icon--right"></i>上一步</el-button>
      </el-form-item>

      <el-form-item v-if="active===2"  label="密码" prop="pass" style="margin: 2px 0 0 120px">
        <el-input type="password" maxlength="20" style="width: 250px" clearable show-word-limit v-model="password" autocomplete="off"></el-input>
        <el-alert style="width: 220px" v-show="error_password" title="密码最少8位，最长20位" type="warning" ></el-alert>
      </el-form-item>

      <el-form-item v-if="active===2" label="确认密码" prop="checkPass" style="margin: 10px 0 0 120px">
        <el-input type="password" maxlength="20" style="width: 250px" clearable show-word-limit v-model="password2" autocomplete="off"></el-input>
        <el-alert style="width: 220px" v-show="error_check_password" title="两次输入的密码不一致" type="warning" ></el-alert>
      </el-form-item>

      <el-form-item v-if="active===2" style="margin: 30px 0 0 200px">
        <el-button type="primary" @click="reset_pwd">重置</el-button>
      </el-form-item>

      <el-form-item v-if="active===3" style="text-align: center; margin: 40px 0">
        <el-link @click="to_path('/login')">已重置密码，快去登录吧~</el-link>
      </el-form-item>


      <el-divider></el-divider>

      <el-row style="margin-top: 5px; position: relative;">
        <el-link @click="to_path('/login')" type="primary">不找了，想起来了</el-link>
        <span class="set_center">&emsp;|&emsp;</span>
        <el-link @click="to_path('/register')" type="primary">我还是再注册一个吧</el-link>
      </el-row>
    </el-form>
  </div>
</template>

<script>
import {Base} from '../components/mixins'

import {ElMessage} from "element-plus";
export default {
  mixins: [Base],
  name: "Forget",
  data() {
    return {
      active: 0,

      step1: '验证方式',
      step2: '进行验证',
      step3: '重置密码',

      ways: '',  // 验证方式
      is_choose: true,


      error_password: false,
      error_check_password: false,
      password: '',
      password2: '',

      mobile: '',
      sms_code_tip: '获取验证码',
      not_exist: false,
      error_phone: false,
      error_phone_message: '',
      sending_flag: false,
      btn_disabled: false,
      email: '',
      sms_code: '',
    };
  },
  watch: {
    ways: {
      handler(old_val, new_val) {
        this.is_choose = this.ways === ''
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
  },
  methods: {
    // 检查手机号
    check_phone() {
      const re = /^1[3-9]\d{9}$/;
      if (re.test(this.mobile)) {
        this.error_phone = false;
      } else {
        this.error_phone_message = '您输入的手机号格式不正确';
        ElMessage.error(this.error_phone_message);
        this.error_phone = true;
      }
      if (this.error_phone === false) {
        this.$axios.get(this.$host + "/api/v1/users/mobile/" + this.mobile + '/count/', {
          responseType: 'json'
        })
          .then(response => {
            if (response.data.count === 0) {
              this.error_phone_message = '手机号不存在';
              ElMessage.error(this.error_phone_message);
              this.error_phone = true;
              this.not_exist = true;
            } else {
              this.error_phone = false;
              this.not_exist = false;
            }
          })
          .catch(error => {
            console.log(error.response.data);
          })
      }
    },
    // 发送验证码
    send_sms_code() {
      this.check_phone();
      if (this.error_phone === true || this.not_exist === true) {
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
        ElMessage.success("发送成功");
        // 倒计时 60s，允许 60s 后用户可以再次点击获取验证码按钮
        let num = 60;
        this.btn_disabled = true;
        let t = setInterval(() => {
          if (num === 1) {
            clearInterval(t);
            this.sending_flag = false;
            this.btn_disabled = false;
            this.sms_code_tip = '获取验证码';
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
    },
    // 验证验证码
    verify () {
      if (this.sms_code.length !== 6) {
        ElMessage.error('请输入正确格式的验证码');
        return;
      }
      if (this.error_phone === false) {
        this.$axios.post(this.$host + "/api/v1/user/forget/", {
          mobile: this.mobile,
          sms_code: this.sms_code,
        }, {
          responseType: 'json'
        }). then(response => {
          if (response.data['code'] === 1) {
            ElMessage.success('验证成功，请重置您的密码');
            this.step2 = '验证成功'
            this.active ++;
          } else {
            ElMessage.error('验证码错误');
          }
        })
      } else {
        ElMessage.error('请检查您的手机号');
      }
    },
    // 重置密码
    reset_pwd() {
      this.error_check_password = this.password !== this.password2;
      if (this.error_password === false && this.error_check_password === false && this.password !== '' && this.password2 !== '') {
        this.$axios.post(this.$host + "/api/v1/user/password/reset/", {
          mobile: this.mobile,
          password: this.password
        }, {
          responseType: 'json'
        }). then(response => {
          ElMessage.success('重置密码完成，马上去登录吧~');
          this.step3 = '重置完成'
          this.active ++;
        })
      } else {
        ElMessage.info('请检查您的输入');
      }
    },
    next() {
      // 判断
      if (this.active === 0) {
        if (this.ways === '') {
          ElMessage.error('请选择验证方式');
        }
        else if (this.ways === '1') {
          this.step1 = '已选手机'
          this.active ++;
        } else {
          ElMessage.info('暂不支持其他验证方式');
        }
      }
    },
    prev() {
      this.step1 = '验证方式';
      this.active --;
    },
  }
}
</script>

<style scoped>
#forget {
  /*background: url("../assets/code-bg.jpg") no-repeat center;*/
  height: 100%;
  width: 100%;
  background-size: cover;
  position: fixed;
}

.container {
  border-radius: 15px;
  background-clip: padding-box;
  margin: 10% auto;
  width: 480px;
  padding: 35px 35px 15px 35px;
  background: #fff;
  border: 1px solid #eaeaea;
  box-shadow: 0 0 25px #cac6c6;
}

.title {
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