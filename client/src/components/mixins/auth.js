export default {
  data() {
    return {
      user_id: sessionStorage.user_id || localStorage.user_id,
      token: sessionStorage.token || localStorage.token,
      // 用户名
      username: '',
      // 身份
      identity: '',
      // 手机号
      mobile: '',
      // 邮箱
      email: '',
      // 邮箱激活状态
      email_active: '',
      // 是否登录
      login_flag: false,
      // 刷过的题
      problem_solved: [],
      // 刷题数
      problem_cnt: 0,
      // 发帖信息
      forum_post: [],
      // 获赞总数
      like_cnt: 0,

    }
  },
  methods: {
    // 退出登录
    logout() {
      if (this.login_flag === true) {
        sessionStorage.clear();
        localStorage.clear();
      }
    },
    // 登录判断，并获取信息
    login() {
      // 判断用户登录状态
      if (this.user_id && this.token) {
        this.$axios.get(this.$host + "/api/v1/user/", {
        // 向后端传递 JWT token 的方法
        headers: {
          'Authorization': 'JWT ' + this.token
        },
        responseType: 'json'
        }).then(response => {
          // 加载用户数据
          this.user_id = response.data.id;
          this.username = response.data.username;
          this.mobile = response.data.mobile;
          this.email = response.data.email;
          this.email_active = response.data['email_active'];
          this.login_flag = true

          if (response.data['is_p'] === false && response.data['is_oc'] === false) {
            this.identity = '管理员'
          } else if (response.data['is_p'] === true) {
            this.identity = '普通用户'
          } else if (response.data['is_oc'] === true) {
            this.identity = '竞赛发布者'
          }

          this.problem_solved = response.data['participant']['solved_problems']
          this.problem_cnt = response.data['participant']['solved_problems'].length
          this.forum_post = response.data['forum_author']

          for (let i=0; i<this.forum_post.length; i++) {
            this.like_cnt += this.forum_post[i]['like_cnt'].length
          }

          // this.contest_cnt = 1
          // this.total_contest_cnt = 2
        }).catch(error => {

        });
      } else {
        this.login_flag = false
      }
    }
  }
}