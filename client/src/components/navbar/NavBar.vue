<template>
  <div id="nav_bar">
    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
      <el-menu-item index="/"><img style="width: 50px" src="../../assets//ico.png" alt=""/></el-menu-item>
      <el-menu-item index="/problems">刷题区</el-menu-item>
      <el-menu-item index="/contexts">竞赛区</el-menu-item>
      <el-submenu v-if="login_flag" class="sub_menu" index="/account">
        <template #title>您好，{{username}}</template>
        <el-menu-item index="/account">个人中心</el-menu-item>
        <el-menu-item index="/login" @click="logout()"> 退出登录</el-menu-item>
      </el-submenu>
      <el-menu-item v-else index="/login">您还未登录，马上去登录</el-menu-item>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: "NavBar",
  props: {
    msg: String,
  },
  data() {
    return {
      activeIndex: "/problems",
      user_id: sessionStorage.user_id || localStorage.user_id,
      token: sessionStorage.token || localStorage.token,

      username: '',

      login_flag: false,
    };
  },
  created() {
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

        // this.context_cnt = 1
        // this.total_context_cnt = 2
      }).catch(error => {

      });
    } else {
      this.login_flag = false
    }
  },
  watch: {
    $route(to, from) {
      // 对路由变化作出响应..
      if (to.path === "/login" || this.$route.path === '/login' || this.$route.path ==='/register' || this.$route.path === '/sregister' || this.$route.path==='/forget'){
        document.querySelector("#nav_bar").style.display = "none";
      } else {
        this.activeIndex = this.$route.path
        document.querySelector("#nav_bar").style.display = "block";
      }
    },
  },

  methods: {
    handleSelect(key, keyPath) {
      this.$router.push(key);
    },
    // 退出登录
    logout() {
      if (this.login_flag === true) {
        sessionStorage.clear();
        localStorage.clear();
      }
    }
  },
};
</script>

<style scoped>
#nav_bar {
  /*display: none !important;*/
  width: 1140px;
  left: 50%;
  transform: translateX(-50%);
  position: fixed;
  z-index: 99;
  box-shadow: rgb(0 0 0 / 17%) 13px 15px 13px 2px;
}
#nav_bar :hover {
}
#nav_bar ::v-deep(.el-menu--horizontal) {
  border-radius: 8px;
  overflow: hidden;
}

#nav_bar ::v-deep(.el-menu--horizontal) > .el-menu-item {
  height: 72px;
  line-height: 72px;
}
#nav_bar ::v-deep(.el-menu--horizontal) > .el-submenu {
  height: 72px;
  line-height: 72px;
}
#nav_bar ::v-deep(.el-menu--horizontal) > .el-submenu  .el-submenu__title{
  line-height: 72px;
  height: 72px;
}
</style>
