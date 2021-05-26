<template>
  <div class="index">
    <div class="content">

      <div @click="to_path('/problems')" class="card">
        <div class="shoebox">
          <img src="../assets/img/题库.png" alt="" />
        </div>
        <div class="selector">
          <h2>算法题库</h2>
          <div class="shoes">
            题库现有题：
            <span style="color: whitesmoke; font-weight: bold">{{total_problem_cnt}}</span>
          </div>
<!--          <a href="#" class="by-btn">Let's go</a>-->
        </div>
      </div>

      <div class="card" @click="to_path('/contests')" style="background-color:rgb(	250,128,114)">
        <div class="shoebox">
          <img src="../assets/img/竞赛.png" style="width: 200px" alt="" />
        </div>
        <div class="selector">
          <h2>算法竞赛区</h2>
          <div class="shoes-size">
            举办方：
            <span>浙江大学、阿里巴巴有限公司等</span>
          </div>
          <a href="#" class="by-btn">Let's go</a>
        </div>
      </div>
      <div class="card" style="background-color:rgb(255,215,0)">
        <div class="shoebox">
          <img
            src="../assets/img/个人中心 活动.png"
            style="width: 200px"
            alt=""
          />
        </div>
        <div v-if="login_flag" class="selector">
          <h2>欢迎登录，{{username}}</h2>
          <div style="margin: 15px 0">
            <span class="shoes-size">
            刷题：
            <span>{{problem_cnt}} / {{total_problem_cnt}}</span>
              &emsp;
            </span>
            <span class="shoes-size">
              比赛：
              <span>{{problem_cnt}} / 8</span>
            </span>
          </div>
          <a href="#" @click="to_path('/account')" class="by-btn">个人中心</a>
        </div>
        <div v-else class="selector">
          <h2>个人中心</h2>
          <a href="#" @click="to_path('/login')" class="by-btn">Sign in</a>
          <a href="#" @click="to_path('/register')" class="by-btn">Sign up</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {Base} from '../components/mixins'

export default {
  mixins: [Base],
  name: 'Index',
  data() {
    return {
      username: sessionStorage.username || localStorage.username,
      user_id: sessionStorage.user_id || localStorage.user_id,
      token: sessionStorage.token || localStorage.token,

      login_flag: false,
      problem_cnt: 0,
    }
  },
  components: {
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
        console.log(response.data)
        this.username = response.data.username
        this.login_flag = true

        // 设置值
        this.problem_cnt = response.data['participant']['solved_problems'].length

        // this.contest_cnt = 1
        // this.total_contest_cnt = 2
      }).catch(error => {

      });
    } else {
      this.login_flag = false
    }
  },
  methods: {
    // 退出登录
    logout() {
      sessionStorage.clear();
      localStorage.clear();
      location.href = '/login';
    },

  }
}
</script>

<style scoped>
@import "../assets/css/index.css";

.index {
  height: 100vh;
}
.el-main {
  border: 1px black solid;
  text-align: center; /*让div内部文字居中*/
  background-color: #fff;
  border-radius: 20px;
  width: 80%;
  height: 400px;
  margin: auto;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.el-row {
  height: 100%;
  align-items: center;
  justify-content: center;
}

.el-col {
  border: 1px red solid;
  height: 200px;
}

.el-col > div {
  text-align: justify;
}
</style>