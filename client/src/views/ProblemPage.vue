<template>
<div>

  题目
  {{message}}
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

      pid: '',
      name: '',
      message: '',
      header: '',
      alg_type: '',
      ds_type: '',

      result: '',
      msg: '',
    }
  },
  mounted() {
    this.init_data()
  },
  methods: {
    init_data() {
      this.pid = this.$route.params && this.$route.params.id;
      this.$axios.get("http://127.0.0.1:8000/api/v1/problems/" + this.pid, {
          responseType: 'json'
        })
        .then(response => {
          this.message = response.data['message']
          console.log(response.data)
      })
    },
    execute() {
      this.$axios.post("http://127.0.0.1:8000/api/v1/judge/", {
          user_id: this.user_id,
          id: this.id,
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