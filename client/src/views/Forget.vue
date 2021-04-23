<template>
  <div>
    <div>
      <el-steps :active="active" finish-status="success">
        <el-step title="选择验证方式"></el-step>
        <el-step title="进行验证"></el-step>
        <el-step title="重置密码"></el-step>
      </el-steps>

      <el-button style="margin-top: 12px;" @click="next">下一步</el-button>
    </div>
  </div>
</template>

<script>
export default {
  name: "Forget",
  data() {
    return {
      active: 0
    };
  },

  methods: {
    next() {
      if (this.active++ > 2) this.active = 0;
    }
  }
}
</script>

<style scoped>

</style>