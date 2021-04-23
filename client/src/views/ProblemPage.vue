<template>
<div>

  题目
  <textarea ref="textarea" v-model="code" style="resize: none" rows="40" cols="80" ></textarea>
  <el-button @click="execute">运行</el-button>
  <span>运行结果：{{msg}}</span>
</div>
</template>

<script>

export default {
  name: "ProblemPage",
  data() {
    return {
      code: '',
      user_id: sessionStorage.user_id || localStorage.user_id,
      token: sessionStorage.token || localStorage.token,
      result: '',
      msg: ''
    }
  },
  mounted() {
  },
  methods: {
    execute() {
      this.$axios.post("http://127.0.0.1:8000/api/v1/judge/", {
          user_id: this.user_id,
          id: this.$route.path.substring(10),
          code: this.code
        }).then(response => {
          this.result = response.data['code']
          this.msg = response.data['msg']
          console.log(response.data)
      })
    }
  }
}
</script>

<style scoped>

</style>