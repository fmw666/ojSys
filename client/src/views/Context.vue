<template>
  <div>
		<div class="sideBar">
			<el-tabs v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="已报名" name="first">已报名 |</el-tab-pane>
    <el-tab-pane label="进行中" name="second">进行中 |</el-tab-pane>
    <el-tab-pane label="已结束" name="third">已结束</el-tab-pane>
  </el-tabs>
		</div>
  </div>
</template>

<style>
  .el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
  }
</style>

<script>
  export default {
    data() {
      return {
				isCollapse: true,
				activeName: 'second'
      };
    },
    methods: {
      handleClick(tab, event) {
        console.log(tab, event);
      }
    }
	}
</script>