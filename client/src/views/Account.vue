<template>
  <div id="account">
    <div>
      个人信息页面<hr>
      用户名：<span>{{ username }}</span><br>
      手机号：<span>{{ mobile }}</span><br>
      <span>Email：</span>
      <div v-if="set_email">
          <input v-model="email" type="email" name="email">
          <input @click="save_email" type="button" name="" value="保 存">
          <input @click="set_email=false" type="reset" name="" value="取 消">
          <div v-if="email_error">邮箱格式错误</div>
      </div>
      <div v-else-if="email">
          {{ email }}
          <div v-if="email_active">已验证</div>
          <div v-else>
              待验证<input @click="save_email" :disabled="send_email_btn_disabled" type="button"
                        :value="send_email_tip">
          </div>
      </div>
      <div v-else>
          <input @click="set_email=true" type="button" name="" value="设 置">
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "account",
  data() {
    return {
      user_id: sessionStorage.user_id || localStorage.user_id,
      token: sessionStorage.token || localStorage.token,
      username: '',
      mobile: '',
      email: '',
      email_active: false,
      set_email: false,
      send_email_btn_disabled: false,
      send_email_tip: '重新发送验证邮件',
      email_error: false,
    }
  },
  mounted() {
    // 判断用户登录状态
    if (this.user_id && this.token) {
      this.$axios.get("http://127.0.0.1:8000/api/v1/user/", {
        // 向后端传递 JWT token 的方法
        headers: {
          'Authorization': 'JWT ' + this.token
        },
        responseType: 'json'
      }).then(response => {
        // 加载用户数据
        this.user_id = response.data.id;
        this.username = response.data.username;
        this.mobile = response.data.mobile;
        this.email = response.data.email;
        this.email_active = response.data.email_active;
      }).catch(error => {
        if (error.response.status==401 || error.response.status==403) {
          location.href = '/login?next=/account';
        }
      });
    } else {
      location.href = '/login?next=/account';
    }
  },
  methods: {
    // 退出登录
    logout() {
      sessionStorage.clear();
      localStorage.clear();
      location.href = '/login';
    },
    // 保存邮箱
    save_email() {
      const re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
      if (re.test(this.email)) {
        this.email_error = false;
      } else {
        this.email_error = true;
        return;
      }
      this.$axios.put('http://127.0.0.1:8000/api/v1/email/', {
        email: this.email
      }, {
        headers: {
          'Authorization': 'JWT ' + this.token
        },
        responseType: 'json'
      })
      .then(response => {
        this.set_email = false;
        this.send_email_btn_disabled = true;
        this.send_email_tip = '已发送验证邮箱'
      })
      .catch(error => {
        alert(error.data);
      });
    }
  }
}

</script>

<style scoped>

</style>