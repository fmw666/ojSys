<template>
  <div class="index">
    <el-container>
      <el-main>
        <el-row type="flex" class="row-bg" justify="space-around">
          <el-col :xs="16" :sm="7">
            <router-link to="/problems">刷题</router-link>
          </el-col>
          <el-col :xs="16" :sm="7">
            <router-link to="/contexts">竞赛</router-link>
          </el-col>
          <el-col :xs="16" :sm="7">
            <div v-if="username">
              用户头像，—— {{ username }}
              <br><router-link to="/account">个人中心</router-link>
              <el-link type="primary" @click="logout">退出登录</el-link>
            </div>
            <div v-else>
              <router-link to="/login">请登录</router-link>！
              <router-link to="/register">请注册</router-link>！
            </div>
            <br>刷题：3/1923<br>竞赛：0/123
          </el-col>
        </el-row>
        <!--  -->
        <!-- <el-button type="primary" round>el-button</el-button> -->
      </el-main>
    </el-container>
  </div>
</template>

<script>

export default {
  name: 'Index',
  data() {
    return {
      username: sessionStorage.username || localStorage.username,
      user_id: sessionStorage.user_id || localStorage.user_id,
      token: sessionStorage.token || localStorage.token,
    }
  },
  components: {
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

<style>
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