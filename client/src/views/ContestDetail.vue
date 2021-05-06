<template>
<div>
  <div class="container">
    <el-card>
      <div class="header">
        <div class="title">{{name}}</div>
        <el-tag style="margin-left: 20px;">报名剩余时间：{{remain_hours}}:{{remain_minutes}}:{{remain_seconds}}</el-tag>
        <el-button @click="sign_up" style="float: right;" type="primary" round>点击报名</el-button>
      </div>

      <div class="msg" style="margin-top: 10px">开赛时间</div>
      <el-tag>{{contest_start_date}}</el-tag>
      <span style="color: rgb(64,158,255);">--</span>
      <el-tag>{{contest_end_date}}</el-tag>

      <div class="msg">描述</div>
      <div class="content">{{message}}</div>

      <div class="msg">奖励</div>
      <div class="content">{{reward}}</div>

      <div class="msg">比赛要求</div>
      <div v-if="require" class="content">{{require}}</div>
      <div v-else class="content">无</div>

    </el-card>
  </div>

  <el-backtop :visibility-height="0"></el-backtop>
</div>
</template>

<script>
import {Base, Auth} from '../components/mixins'

import {defineComponent} from 'vue'
import {ElMessage} from "element-plus";

export default defineComponent({
  name: "ContestDetail",
  mixins: [Base, Auth],
  data() {
    return {

      cid: '',
      name: '',
      title: '',
      message: '',
      reward: '',
      require: '',

      sign_up_end_date: '',
      remain_hours: '',
      remain_minutes: '',
      remain_seconds: '',
      contest_start_date: '',
      contest_end_date: '',

      result: '',
      msg: '',
    }
  },
  mounted() {
    this.init_data()
    this.login()
    if (this.login_flag === true) {
      this.sign_up_check()
    }
  },
  methods: {

    init_data() {
      this.cid = this.$route.params && this.$route.params.id;
      this.$axios.get(this.$host + "/api/v1/contests/" + this.cid, {
          responseType: 'json'
        })
        .then(response => {
          this.name = response.data['name']
          this.message = response.data['message'].replace(/\r\n/g,"<br/>")
          this.reward = response.data['reward']
          this.require = response.data['require']

          this.sign_up_end_date = response.data['sign_up_end_date']
          this.contest_start_date = response.data['contest_start_date']
          this.contest_end_date = response.data['contest_end_date']

          // 2021年05月06日  05:54
          let new_time = this.sign_up_end_date.replace('年', '-')
          new_time = new_time.replace('月', '-').replace('日', '')
          new_time += ':00'
          // date like: 2021-05-12 12:15:12
          let end = new Date(new_time)

          this.difference(new Date(), end)

          let timer = setInterval(() => {
            this.difference(new Date(), end)
            if (this.remain_hours === 0 && this.remain_minutes === 0 && this.remain_seconds === 0) {
              // 如果结束报名
              clearInterval(timer)
            }
          }, 1000)

          console.log(response.data)
      });

    },
    // 获得时间差
    difference(beginTime, endTime) {
      const dateBegin = new Date(beginTime);
      const dateEnd = new Date(endTime);
      const dateDiff = dateEnd.getTime() - dateBegin.getTime();//时间差的毫秒数
      const dayDiff = Math.floor(dateDiff / (24 * 3600 * 1000));//计算出相差天数
      const leave1 = dateDiff % (24 * 3600 * 1000);    //计算天数后剩余的毫秒数
      let hours = Math.floor(leave1 / (3600 * 1000));//计算出小时数
      //计算相差分钟数
      const leave2 = leave1 % (3600 * 1000);   //计算小时数后剩余的毫秒数
      const minutes = Math.floor(leave2 / (60 * 1000)); //计算相差分钟数
      //计算相差秒数
      const leave3 = leave2 % (60 * 1000);     //计算分钟数后剩余的毫秒数
      const seconds = Math.round(leave3 / 1000);

      hours += dayDiff * 24
      this.remain_hours = hours
      this.remain_minutes = minutes
      this.remain_seconds = seconds
    },

    // 报名检查
    sign_up_check() {

    },

    // 点击报名
    sign_up() {
      // 未登录
      if (this.login_flag === false) {
        this.$confirm('您还未进行登录, 请先登录！', '提示', {
          confirmButtonText: '去登录',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.to_path('/login?next=/contests/' + this.cid)
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消登录'
          });
        });
        return
      }

      console.log('登录了')
    },
  }
})
</script>

<style scoped>

.container {
  /*width: 1130px;*/
  width: 66vw;
  margin: 0 auto;
  padding-top: 120px;
}
.container ::v-deep(.el-card) {
  padding: 10px 20px;
}
.header {
  height: 50px;
}
.title {
  display: inline-block;
  font-size: 19px;
  font-weight: 600;
}
.msg {
  color: #3091f2;
  font-size: 17px;
  font-weight: bold;
  margin: 30px 0 20px 0;
}
.content {
  word-wrap:break-word;
}
</style>