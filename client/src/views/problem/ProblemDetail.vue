<template>
<div>
  <div class="container">

    <div class="description">
      <el-scrollbar native class="scrollbar">
        <div style="margin: 20px 30px 30px 30px; height: max-content">
          <div class="header">{{pid}}. {{name}}</div>
          <div class="tags">
            <el-tag>难度：<b>{{header}}</b></el-tag>
            <el-tag>算法类型：<b>{{alg_type}}</b></el-tag>
            <el-tag>数据结构：<b>{{ds_type}}</b></el-tag>
          </div>
          <div class="title">描述</div>
          <span class="msg" v-html="message"></span>

          <div class="title">输入样例</div>
          <el-tag v-if="input_example" class="msg example" v-html="input_example"></el-tag>
          <span v-else class="msg">无</span>

          <div class="title">输出样例</div>
          <el-tag v-if="output_example" class="msg example" v-html="output_example"></el-tag>
          <span v-else class="msg">无</span>

          <div v-if="challenge" class="title">挑战</div>
          <span v-if="challenge" class="msg" v-html="challenge"></span>

        </div>

      </el-scrollbar>
      <div class="extra">
        <el-button @click="to_path('/problems')" size="medium" icon="el-icon-back" round>返回列表</el-button>
        <el-button-group style="float: right">
          <el-button size="medium" round icon="el-icon-arrow-left">上一题</el-button>
          <el-button size="medium" round>下一题<i class="el-icon-arrow-right el-icon--right"></i></el-button>
        </el-button-group>
      </div>
    </div>


    <div class="text_input">
      <div class="code_text">

        <textarea style="height: 100%; width: 100%; resize: none" id="code_input" ref="textarea" v-model="code" rows="40" cols="80" autofocus></textarea>
      </div>
      <div class="extra">
        <el-button style="float: right" @click="execute" type="primary" icon="el-icon-edit">运行</el-button>
        <span style="line-height: 39px; width: 50px">
          <span class="status" style="font-size: 15px">运行结果：</span>
          <span class="status_code">
            <span v-if="result === 'wa'">
              <el-tag>
                <i style="color: #ed3f14" class="el-icon-error"></i>&ensp;
                <span style="color: #495060">Wrong Answer</span>
              </el-tag>
            </span>
            <span v-if="result === 'ac'">
              <el-tag>
                <i style="color: #19be6b" class="el-icon-success"></i>&ensp;
                <span style="color: #495060">Accepted</span>
              </el-tag>
            </span>
          </span>
        </span>
      </div>
      <div v-if="msg !== 'ac'" class="status" style="margin-top: 10px;">
        {{msg}}
      </div>
    </div>

  </div>
</div>
</template>

<script>
import {Base, Auth} from '../../components/mixins'

import { defineComponent } from 'vue'
import { ElMessage } from 'element-plus'
export default defineComponent({
  name: "ProblemPage",
  mixins: [Base, Auth],

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
      input_example: '',
      output_example: '',
      challenge: '',

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
    onEditorCodeChange (newCode) {
      this.$emit('update:value', newCode)
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
            showClose: true,
            dangerouslyUseHTMLString: true,
            message: '未登录，请先 <b>登录</b> 才能提交代码',
            duration: 5000
          });
        }
        this.login_flag = false
      }
    },
    // 获取 题目 信息
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
          this.input_example = response.data['input_example']
          this.output_example = response.data['output_example']
          this.challenge = response.data['challenge']

          this.title = this.pid + '. ' + this.name
          console.log(response.data)
      });

    },
    // 执行程序
    execute() {
      this.login_tip(false)
      if (this.login_flag === true) {
        this.$axios.post(this.$host + "/api/v1/judge/", {
          uid: this.user_id,
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
          console.log(error)
        })
      } else {
        this.$confirm('您还未进行登录, 请先登录！', '提示', {
          confirmButtonText: '去登录',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.to_path('/login?next=/problems/' + this.pid)
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消登录'
          });
        });
      }
    },


  },
  computed: {
  },
})
</script>

<style scoped>
/*body .el-scrollbar__wrap {*/
/*  overflow-x: hidden;*/
/*}*/

/*css设置默认显示滚动条*/
.el-scrollbar__bar {
  opacity: 1;
}


.description {
  display: inline-block;
  width: 50%;
  /*height: 500px;*/
  height: 70vh;
}

.scrollbar {
  background: rgba(255,255,255,0.85);
  -webkit-box-shadow:0 3px 3px #c3c3c3 inset;
  -moz-box-shadow:0 3px 3px #c3c3c3 inset;
  box-shadow:0 0 8px 2px #c3c3c3 inset;
}

.header {
  font-size: 21px;
  font-weight: bold;
  font-family: Helvetica Neue,Helvetica,PingFang SC,Hiragino Sans GB,Microsoft YaHei,\\5FAE\8F6F\96C5\9ED1,Arial,sans-serif;
  -webkit-font-smoothing: antialiased;
  color: #495060;
}

.tags {
  margin: 16px 0;
}

.tags > span {
  margin-right: 20px;
}

.title {
  font-size: 17px;
  font-weight: 600;
  margin: 25px 0 10px;
  color: #3091f2;
}

.msg {
  font-size: 16px;
  color: #495060;
}

.example {
  font-size: 14px;
  height: max-content;
  width: 100%;
}

.extra {
  margin-top: 16px;
}

.text_input {

  display: inline-block;
  width: 45%;
  float: right;
  height: 100%;
}

.text_input > .code_text {
  height: 69.4vh;
  width: 100%;
}

.status {
  font-size: 14px;
  color: #495060;
}

</style>