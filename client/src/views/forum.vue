<template>
  <div id="Forum">
    <div class="container">
      <el-card>
        <div class="main">
          <el-tabs v-model="activeName" @tab-click="handleClick">
            <el-tab-pane label="🚩 全部主题" name="first">

            </el-tab-pane>

            <el-tab-pane label="🔥 热门" name="second">

            </el-tab-pane>

            <el-tab-pane label="👀 来自用户" name="third">

            </el-tab-pane>

            <el-tab-pane label="🎯 来自机构" name="forth">

            </el-tab-pane>

            <el-tab-pane label="🎈 来自管理员" name="fifth">

            </el-tab-pane>
          </el-tabs>
        </div>

        <div class="side">
          <div v-if="login_flag">
            <span style="font-size: 14px; padding-top: 10px;">您的身份：</span><el-tag>{{identity}}</el-tag>
            <el-divider style="margin: 10px 0"></el-divider>
            发帖数：
          </div>
          <div v-else style="float: right; margin: 10px 20px 0 0">
            <el-tag>您还未登录</el-tag>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import {Auth} from '../components/mixins'
export default {
  name: "forum",
  mixins: [Auth],
  data() {
    return {
      activeName: 'first',
    }
  },
  methods: {
    // 切换每页多少数据
    handleSizeChange(val) {
      //
    },
    // 点击页数，切换到相应页
    handleCurrentChange(val) {
      //
    },
    handleClick() {

    },
  },
  mounted() {
    this.login()
  }
}
</script>

<style scoped>
.container {
  width: 1142px;
  margin: 0 auto;
  padding-top: 110px;
}

.main {
  margin-left: 10px;
  display: inline-block;
  width: 70%;
}

.side {
  display: inline-block;
  width: 20%;
  float: right;
}

</style>