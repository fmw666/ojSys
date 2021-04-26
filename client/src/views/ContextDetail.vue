<template>
<div>
  <div>


    <el-button>报名参加</el-button>
  </div>
</div>
</template>

<script>
import { defineComponent } from 'vue'
import { ElMessage } from 'element-plus'
export default defineComponent({
  name: "ContextDetail",
  data() {
    return {
      user_id: sessionStorage.user_id || localStorage.user_id,
      token: sessionStorage.token || localStorage.token,

      is_login: false,

      pid: '',
      name: '',
      title: '',
      message: '',
      header: '',
      alg_type: '',
      ds_type: '',

      compiler_version: '',
      result: '',
      msg: '',
    }
  },
  mounted() {
    this.login_tip(true)
    this.init_data()

  },
  methods: {
    go_login() {
      this.$router.push('/login?next=/contexts/' + this.pid)
    },
    login_tip(flag) {
      // 判断用户登录状态
      if (this.user_id && this.token) {
        this.$axios.get(this.$host + "/api/v1/user/", {
        // 向后端传递 JWT token 的方法
        headers: {
          'Authorization': 'JWT ' + this.token
        },
        responseType: 'json'
        }).then(response => {
          let username = response.data.username
          if (flag) {
            this.$message({
              type: 'success',
              message: '已登录，欢迎您！' + username
            });
          }
          this.is_login = true
        }).catch(error => {

        });
      } else {
        if (flag) {
          ElMessage({
            dangerouslyUseHTMLString: true,
            message: '未登录，请先 <i><strong>登录</strong></i> &emsp;&emsp;<a @click="go_login" class="tip_login">去登录</a>',
            duration: 0
          });
        }
        this.is_login = false
      }
    },
    handleClose(done) {
      done()
      document.getElementById('code_input').focus()
    },
    init_data() {
      this.cid = this.$route.params && this.$route.params.id;
      this.$axios.get(this.$host + "/api/v1/contexts/" + this.cid, {
          responseType: 'json'
        })
        .then(response => {
          this.name = response.data['name']
          this.message = response.data['message'].replace(/\r\n/g,"<br/>")
          this.header = response.data['header']
          this.alg_type = response.data['alg_type']
          this.ds_type = response.data['ds_type']

          this.title = this.cid + '. ' + this.name
          console.log(response.data)
      });

    },
    execute() {
      this.login_tip(false)
      if (this.is_login === true) {
        this.$axios.post(this.$host + "/api/v1/judge/", {
          user_id: this.user_id,
          id: this.pid,
          code: this.code
        }).then(response => {
          this.compiler_version = response.data['version']
          this.result = response.data['code']
          this.msg = response.data['output']
          console.log(response.data)
        }).catch(error => {

        })
      } else {
        this.$confirm('您还未进行登录, 请先登录！', '提示', {
          confirmButtonText: '去登录',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.go_login()
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消登录'
          });
        });
      }
    },
    go_list() {
      this.$router.push('/problems')
    }
  }
})
</script>

<style scoped>
.tip_login {
  text-underline: black;
  cursor: pointer;
}
</style>