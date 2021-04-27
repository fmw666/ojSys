<template>
  <div id="account">
    <el-card class="box-card">
      <div class="account_title">
        <div class="account_title_text">个人信息页面</div>
        <el-link :underline="false" @click="logout">退出登录</el-link>
        <el-avatar> user </el-avatar>
      </div>

      <el-divider><i class="el-icon-mobile-phone"></i></el-divider>

      <el-form
        :disabled="disabled"
        :model="ruleForm"
        :rules="rules"
        ref="ruleForm"
        label-width="100px"
        class="demo-ruleForm"
      >
        <el-form-item label="用户名：" prop="username">
          <el-input v-model="ruleForm.username"></el-input>
        </el-form-item>
        <el-form-item label="手机号：" prop="phone">
          <el-input v-model="ruleForm.phone"></el-input>
        </el-form-item>
        <el-form-item prop="email" label="邮箱：">
          <el-input v-model="ruleForm.email"></el-input>
        </el-form-item>
      </el-form>
      <div class="isSubmit">
        <el-button type="primary" @click="onSubmit('ruleForm')" class="isChange"
          >修改</el-button
        >
        <el-button @click="onOpen">取消</el-button>
      </div>
    </el-card>
    <div>
      个人信息页面
      <hr />
      用户名：<span>{{ username }}</span
      ><br />
      手机号：<span>{{ mobile }}</span
      ><br />
      <span>Email：</span>
      <div v-if="set_email">
        <input v-model="email" type="email" name="email" />
        <input @click="save_email" type="button" name="" value="保 存" />
        <input @click="set_email = false" type="reset" name="" value="取 消" />
        <div v-if="email_error">邮箱格式错误</div>
      </div>
      <div v-else-if="email">
        {{ email }}
        <div v-if="email_active">已验证</div>
        <div v-else>
          待验证<input
            @click="save_email"
            :disabled="send_email_btn_disabled"
            type="button"
            :value="send_email_tip"
          />
        </div>
      </div>
      <div v-else>
        <input @click="set_email = true" type="button" name="" value="设 置" />
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

      ruleForm: {
        username: '',
        phone: '',
        email: '',
      },
      rules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
          { min: 3, max: 10, message: "长度在 3 到 10 个字符", trigger: "blur" },
        ],
        phone: [
          { required: true, message: "请输入手机号", trigger: "blur" },
          { min: 11, max: 11, trigger: "blur" },
        ],
        email: [
          { required: true, message: "请输入邮箱地址", trigger: "blur" },
          {
            type: "email",
            message: "请输入正确的邮箱地址",
            trigger: ["blur", "change"],
          },
        ],
      },

      disabled: true,
    }
  },
  mounted() {
    // 判断用户登录状态
    if (this.user_id && this.token) {
      this.$axios.get(this.$host + "/api/v1/user/", {
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

        this.ruleForm.username = this.username
        this.ruleForm.phone = this.mobile
        this.ruleForm.email = this.email
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
      this.$axios.put(this.$host + '/api/v1/email/', {
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
    },
    // 修改按钮
    onSubmit(formName) {
      if (this.disabled) {
        this.disabled = false;
        document.querySelector(".isChange").querySelector("span").innerHTML =
            "提交";
      } else {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            alert("修改成功!");
            document
                .querySelector(".isChange")
                .querySelector("span").innerHTML = "修改";
            this.disabled = true;
          } else {
            console.log("error submit!!");
            return false;
          }
        });
      }
    },
    // 取消按钮
    onOpen() {
      document.querySelector(".isChange").querySelector("span").innerHTML =
        "修改";
      this.disabled = true;
    }
  }
}

</script>

<style scoped>
#account {
  width: 1142px;
  margin: 0 auto;
}
#account .box-card {
  position: relative;
  top: 100px;
  box-shadow: rgb(0 0 0 / 17%) 13px 15px 13px 2px;
}
#account .box-card /deep/ .el-form .el-input .el-input__inner {
  width: 30%;
}
#account .box-card .isSubmit {
  width: 150px;
  margin: 60px auto 0px;
}
#account .box-card .account_title {
  display: flex;
  padding-right: 50px;
}
#account .box-card .account_title .account_title_text {
  flex: 1;
  line-height: 42px;
}
#account .box-card .account_title .el-link {
  width: 100px;
}
</style>