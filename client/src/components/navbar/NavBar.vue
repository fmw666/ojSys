<template>
  <div id="nav_bar">
    <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      @select="handleSelect"
    >
      <el-menu-item index="/"
        ><img style="width: 50px" src="../../assets//ico.png" alt=""
      /></el-menu-item>
      <el-menu-item index="/problems">刷题区</el-menu-item>
      <el-menu-item index="/contexts">竞赛区</el-menu-item>
      <el-menu-item index="/account">个人中心</el-menu-item>
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
    };
  },
  created() {},
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
  z-index: 99999;
  box-shadow: rgb(0 0 0 / 17%) 13px 15px 13px 2px;
}
#nav_bar :hover {
}
#nav_bar /deep/ .el-menu--horizontal {
  border-radius: 8px;
  overflow: hidden;
}
#nav_bar /deep/ .el-menu--horizontal > .el-menu-item {
  height: 72px;
  line-height: 72px;
}
</style>
