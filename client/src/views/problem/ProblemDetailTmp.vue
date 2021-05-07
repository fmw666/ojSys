<template>
<div>
  <div class="container">
    <!--problem main end-->
    <div>
      <CodeMirror :value.sync="code"
                  :languages="problem.languages"
                  :language="language"
                  :theme="theme"
                  @resetCode="onResetToTemplate"
                  @changeTheme="onChangeTheme"
                  @changeLang="onChangeLang"></CodeMirror>
    </div>
<!--      <Row type="flex" justify="space-between">-->
<!--        <Col :span="10">-->
<!--          <div class="status" v-if="statusVisible">-->
<!--            <template v-if="!this.contestID || (this.contestID && OIContestRealTimePermission)">-->
<!--              <span>{{$t('m.Status')}}</span>-->
<!--              <Tag type="dot" :color="submissionStatus.color" @click.native="handleRoute('/status/'+submissionId)">-->
<!--                {{$t('m.' + submissionStatus.text.replace(/ /g, "_"))}}-->
<!--              </Tag>-->
<!--            </template>-->
<!--            <template v-else-if="this.contestID && !OIContestRealTimePermission">-->
<!--              <Alert type="success" show-icon>{{$t('m.Submitted_successfully')}}</Alert>-->
<!--            </template>-->
<!--          </div>-->
<!--          <div v-else-if="problem.my_status === 0">-->
<!--            <Alert type="success" show-icon>{{$t('m.You_have_solved_the_problem')}}</Alert>-->
<!--          </div>-->
<!--          <div v-else-if="this.contestID && !OIContestRealTimePermission && submissionExists">-->
<!--            <Alert type="success" show-icon>{{$t('m.You_have_submitted_a_solution')}}</Alert>-->
<!--          </div>-->
<!--          <div v-if="contestEnded">-->
<!--            <Alert type="warning" show-icon>{{$t('m.Contest_has_ended')}}</Alert>-->
<!--          </div>-->
<!--        </Col>-->

<!--        <Col :span="12">-->
<!--          <template v-if="captchaRequired">-->
<!--            <div class="captcha-container">-->
<!--              <Tooltip v-if="captchaRequired" content="Click to refresh" placement="top">-->
<!--                <img :src="captchaSrc" @click="getCaptchaSrc"/>-->
<!--              </Tooltip>-->
<!--              <Input v-model="captchaCode" class="captcha-code"/>-->
<!--            </div>-->
<!--          </template>-->
<!--          <Button type="warning" icon="edit" :loading="submitting" @click="submitCode"-->
<!--                  :disabled="problemSubmitDisabled || submitted"-->
<!--                  class="fl-right">-->
<!--            <span v-if="submitting">{{$t('m.Submitting')}}</span>-->
<!--            <span v-else>{{$t('m.Submit')}}</span>-->
<!--          </Button>-->
<!--        </Col>-->
<!--      </Row>-->

<!--    <el-drawer-->
<!--      v-bind:title="title"-->
<!--      v-model="drawer"-->
<!--      :direction="direction"-->
<!--      :modal="false"-->
<!--      :size="'30%'"-->
<!--      :close-on-press-escape="true"-->
<!--      :before-close="handleClose" destroy-on-close>-->

<!--      <div style="margin-left: 20px">-->
<!--        <span>难度：{{header}}</span>-->
<!--        <br><br>-->
<!--        <span>算法类型：{{alg_type}}</span>-->
<!--        &emsp;&emsp;-->
<!--        <span>数据结构：{{ds_type}}</span>-->
<!--        <br><br>-->
<!--        <h3>描述</h3>-->
<!--        <span v-html="message"></span>-->
<!--        <br><br>-->
<!--        <el-button>上一题</el-button>-->
<!--        <el-button>下一题</el-button>-->
<!--      </div>-->
<!--    </el-drawer>-->

<!--    <div style="width: 68%; float: right">-->
<!--      <el-button @click="drawer = true" type="" style="margin-left: 16px;">-->
<!--        题目详情-->
<!--      </el-button>-->
<!--      <br>-->
<!--      <textarea id="code_input" ref="textarea" v-model="code" style="resize: none" rows="40" cols="80" autofocus></textarea>-->

<!--      <br><br>-->
<!--      <el-button @click="execute">运行</el-button>-->
<!--      <span>&emsp;&emsp;运行结果：{{msg}}</span>-->
<!--    </div>-->
  </div>
</div>
</template>

<script>
// import CodeMirror from "../components/CodeMirror.vue";

import {Auth} from '../../components/mixins'

import { defineComponent } from 'vue'
import { ElMessage } from 'element-plus'
export default defineComponent({
  name: "ProblemPage",
  mixins: [Auth],
  components: {
    // CodeMirror
  },
  data() {
    return {
      code: '',

      drawer: false,
      direction: 'ltr',

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

      // 以下是 OnlineJudgeFE
      problem: {
        title: '',
        description: '',
        hint: '',
        my_status: '',
        template: {},
        languages: [],
        created_by: {
          username: ''
        },
        tags: [],
        io_mode: {'io_mode': 'Standard IO'}
      },
      language: 'C++',
    }
  },
  mounted() {
    this.login_tip(true)
    this.init_data()

  },
  methods: {
    go_login() {
      this.$router.push('/login?next=/problems/' + this.pid)
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
          this.login_flag = true
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
        this.login_flag = false
      }
    },
    handleClose(done) {
      done()
      document.getElementById('code_input').focus()
    },
    init_data() {
      this.pid = this.$route.params && this.$route.params.id;
      this.$axios.get(this.$host + "/api/v1/problems/" + this.pid, {
          responseType: 'json'
        })
        .then(response => {
          this.name = response.data['name']
          this.message = response.data['message'].replace(/\r\n/g,"<br/>")
          this.header = response.data['header']
          this.alg_type = response.data['alg_type']
          this.ds_type = response.data['ds_type']
          this.code = response.data['init_code']

          this.title = this.pid + '. ' + this.name
          console.log(response.data)
      });

    },
    execute() {
      this.login_tip(false)
      if (this.login_flag === true) {
        this.$axios.post(this.$host + "/api/v1/judge/", {
          user_id: this.user_id,
          id: this.pid,
          code: this.code
        }).then(response => {
          this.compiler_version = response.data['version']
          this.result = response.data['code']
          this.msg = response.data['output']
          console.log(response.data)

          if (this.result === 'ac') {
            this.$message({
              type: 'success',
              message: '运行通过！'
            });
            this.msg = 'ac'
          } else {
            this.$message({
              type: 'error',
              message: '运行失败！请仔细检查您的代码噢~'
            });
          }
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
    // 以下是 OnlineJudgeFE
    onChangeLang (newLang) {
      if (this.problem.template[newLang]) {
        if (this.code.trim() === '') {
          this.code = this.problem.template[newLang]
        }
      }
      this.language = newLang
    },
    onChangeTheme (newTheme) {
      this.theme = newTheme
    },
    onResetToTemplate () {
      this.$Modal.confirm({
        content: this.$i18n.t('m.Are_you_sure_you_want_to_reset_your_code'),
        onOk: () => {
          let template = this.problem.template
          if (template && template[this.language]) {
            this.code = template[this.language]
          } else {
            this.code = ''
          }
        }
      })
    },
  }
})
</script>

<style scoped>

.container {
  width: 100%;
  margin: 0 auto;
  padding-top: 150px;
}

.tip_login {
  text-underline: black;
  cursor: pointer;
}

</style>