export default {
  data() {
    return {
      total_problem_cnt: 0,
      total_context_cnt: 0,
    }
  },
  mounted() {
    this.get_problem_cnt();
    this.get_context_cnt();

  },

  methods: {
    // 路由跳转
    to_path(path) {
      this.$router.push(path).then(r => console.log());
    },
    // 解析 URL
    get_query_string(name) {
      const reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
      const r = window.location.search.substr(1).match(reg);
      if (r != null) {
        return decodeURI(r[2])
      }
      return null
    },


    // 获取 problem cnt
    get_problem_cnt() {
      this.$axios.get(this.$host + "/api/v1/problems/", {
        responseType: 'json'
      }).then(response => {
        this.total_problem_cnt = response.data.count
      }).catch(error => {
        console.log(error.response.data)
      })
    },
    // 获取 context cnt
    get_context_cnt() {
      this.$axios.get(this.$host + "/api/v1/contexts/", {
        responseType: 'json'
      }).then(response => {
        this.total_context_cnt = response.data.count
      }).catch(error => {
        console.log(error.response.data)
      })
    }
  }

}