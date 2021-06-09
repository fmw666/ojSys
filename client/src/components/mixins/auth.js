export default {
  data() {
    return {
      user_id: sessionStorage.user_id || localStorage.user_id,
      token: sessionStorage.token || localStorage.token,
      // 是否登录
      login_flag: false,
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
  mounted() {
    this.login()
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
        }).then(res => {
          // 加载用户数据
          this.user_id = res.data.id;
          this.username = res.data.username;
          this.mobile = res.data.mobile;
          this.email = res.data.email;
          this.email_active = res.data['email_active'];
          this.login_flag = true

          if (res.data['is_p'] === false && res.data['is_oc'] === false) {
            this.identity = '管理员'
          } else if (res.data['is_p'] === true) {
            this.identity = '普通用户'
          } else if (res.data['is_oc'] === true) {
            this.identity = '竞赛发布者'
          }

          this.problem_solved = res.data['participant']['solved_problems']
          this.problem_cnt = res.data['participant']['solved_problems'].length
          this.forum_post = res.data['forum_author']

          for (let i=0; i<this.forum_post.length; i++) {
            this.like_cnt += this.forum_post[i]['like_cnt'].length
          }

          // this.contest_cnt = 1
          // this.total_contest_cnt = 2

          this.store_in_session()
        }).catch(error => {

        });
      } else {
        this.login_flag = false
      }
    },

    store_in_session() {
      // 用户名
      sessionStorage.setItem('username', this.username)
      // 身份
      sessionStorage.setItem('identity', this.identity)
      // 手机号
      sessionStorage.setItem('mobile', this.mobile)
      // 邮箱
      sessionStorage.setItem('email', this.email)
      // 邮箱激活状态
      sessionStorage.setItem('email_active', this.email_active)
      // 是否登录
      sessionStorage.setItem('login_flag', this.login_flag)
      // 刷过的题
      sessionStorage.setItem('problem_solved', this.problem_solved)
      // 刷题数
      sessionStorage.setItem('problem_cnt', this.problem_cnt)
      // 发帖信息
      sessionStorage.setItem('forum_post', this.forum_post)
      // 获赞总数
      sessionStorage.setItem('like_cnt', this.like_cnt)
    }
  }
}