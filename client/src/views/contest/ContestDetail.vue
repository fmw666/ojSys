<template>
<div>
<!--  // 0未开始报名，1已开始报名，2比赛进行中，3已结束-->
  <div class="container">
    <el-card v-if="status === 1 || status === 3 || status === 0">
      <div class="header">
        <div style="margin-top: 0" class="title">{{name}}</div>
        <el-tag v-if="status === 0" style="margin-left: 20px;">报名开始时间：{{remain_hours}}:{{remain_minutes}}:{{remain_seconds}}</el-tag>
        <el-tag v-if="status === 1" style="margin-left: 20px;">报名剩余时间：{{remain_hours}}:{{remain_minutes}}:{{remain_seconds}}</el-tag>

        <span v-if="status === 1">
          <el-button v-if="identity === '管理员' || identity === '竞赛发布者'" style="float: right;" type="text" round>
            当前报名人数：{{sign_up_user.length}}
          </el-button>
          <span v-else-if="identity === '普通用户'">
            <el-button v-if="signed" @click="sign_up(2)" style="float: right;" type="success" round>取消报名</el-button>
            <el-button v-else @click="sign_up(1)" style="float: right;" type="primary" round>点击报名</el-button>
          </span>
          <el-tag v-else @click="to_path('/login?next=/contests/' + cid)" style="float: right;cursor:pointer;" type="text" round>您还未登录</el-tag>
        </span>
      </div>

      <div class="msg" style="margin: 0 0 30px 40px; font-size: 14px">——主办方：{{holder}}</div>

      <div class="msg" style="margin-top: 10px">
        开赛时间
        <span v-if="status === 3">（已结束）</span>
      </div>
      <el-tag>{{contest_start_date}}</el-tag>
      <span style="color: rgb(64,158,255);">--</span>
      <el-tag>{{contest_end_date}}</el-tag>

      <el-row v-if="status === 3">
        <el-col :span="12">
          <div class="msg">赛后情况</div>
          <div class="content">提交用户（排名不分先后）：</div>
          <div style="margin-bottom: 26px;">
            <el-button style="padding-bottom: 0; margin: 0 10px 0 0" type="text" v-for="cu in end_commit_users">
              {{cu[0]}}
            </el-button>
          </div>
          <div class="content">排名情况：</div>
          <div class="tables">
            <el-table
              :data="end_rankings_table"
              style="width: 100%">
              <el-table-column
                prop="rank"
                label="排名"
                min-width="16%">
              </el-table-column>
              <el-table-column
                prop="user"
                label="用户名"
                min-width="28%">
              </el-table-column>
              <el-table-column
                prop="cnt"
                label="完成题数"
                min-width="26%">
              </el-table-column>
              <el-table-column
                prop="spend_time"
                label="用时"
                min-width="30%">
              </el-table-column>
            </el-table>
          </div>
        </el-col>

        <el-col :span="12">
          <div class="msg">题目列表</div>
          <div style="margin-left: 30px; font-size: 15px; margin-bottom: 10px">题目总数：</div>
          <div style="margin-left: 30px">
            <div v-for="(p, index) in end_problems">
              {{index + 1}}、<el-button @click="to_path('/problems/' + p[1])" type="text" style="font-size: 16px; padding-bottom: 0">{{p[0]}}</el-button>
            </div>
          </div>
        </el-col>

        <el-divider></el-divider>
      </el-row>


      <div class="msg">描述</div>
      <div class="content" v-html="message"></div>

      <div class="msg">奖励</div>
      <div class="content" v-html="reward"></div>

      <div class="msg">比赛要求</div>
      <div v-if="require" class="content" v-html="require"></div>
      <div v-else class="content">无</div>

    </el-card>

    <el-card v-if="status === 2">
      <div style="margin: 0 0 30px 0; color: #3091f2; font-size: 14px">比赛进行中，请在截止时间前完成比赛，祝您有个好的成绩！</div>
      <div class="title">{{name}}</div>
      <el-tag style="margin-left: 20px;">剩余比赛时间：{{remain_hours}}:{{remain_minutes}}:{{remain_seconds}}</el-tag>

      <el-button type="primary" @click="dialogVisible = true" style="float: right">提交比赛</el-button>


      <el-dialog
        title="提示"
        v-model="dialogVisible"
        width="30%"
        center>
        <div>当前比赛题目总数：<b>{{problems_cnt}}</b>，您已完成题数：<b>{{pass_cnt}}</b></div>
        <br>
        <div>确定提交？提交后不可修改，等到比赛结束后可查询比赛结果。</div>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="dialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="commit">确 定</el-button>
          </span>
        </template>
      </el-dialog>


      <div class="msg" style="margin: 10px 0 30px 40px; font-size: 14px">——主办方：{{holder}}</div>
      <div style="margin-top: 20px">
        <div v-for="cp in contest_problems.slice((page-1), page)">
          <div class="description">
            <el-scrollbar native class="scrollbar">
              <div style="margin: 20px 30px 30px 30px; height: max-content">
                <div style="display: flex">
                  <div class="problems_header">{{page}}. {{cp['name']}}</div>
                  <div v-if="results[page-1] === '未通过'" style="color: #E37831"><b>未通过</b></div>
                  <div v-if="results[page-1] === '已通过'" style="color: #19be6b"><b>已通过</b></div>
                </div>
                <div class="problems_title">描述</div>
                <span class="problems_msg" v-html="cp['message']"></span>

                <div class="problems_title">输入样例</div>
                <el-tag v-if="cp['input_example']" class="problems_msg example" v-html="cp['input_example']"></el-tag>
                <span v-else class="msg">无</span>

                <div class="problems_title">输出样例</div>
                <el-tag v-if="cp['output_example']" class="problems_msg example" v-html="cp['output_example']"></el-tag>
                <span v-else class="msg">无</span>

              </div>
            </el-scrollbar>

            <div class="extra">
              <el-pagination
                layout="prev, pager, next"
                @current-change="handleCurrentChange"
                :page-size="1"
                :current-page="page"
                :total="problems_cnt">
              </el-pagination>
            </div>
          </div>


          <div class="text_input">
            <div class="code_text">
              <label>
                <textarea v-model="contest_problems[page-1]['init_code']" autofocus style="height: 100%; width: 100%; resize: none" id="code_input" ref="textarea" rows="40" cols="80"></textarea>
              </label>
            </div>
            <div class="extra">
              <el-button style="float: right" @click="execute" type="primary" icon="el-icon-edit">运行</el-button>
              <span style="line-height: 39px; width: 50px">
                <span class="status" style="font-size: 15px">运行结果：</span>
                <span class="status_code">
                  <span v-if="result === 'wa'">
                    <el-tag>
                      <i style="color: #ed3f14" class="el-icon-error"></i>&ensp;
                      <span style="color: #495060">Wrong Answer</span>
                    </el-tag>
                  </span>
                  <span v-if="result === 'ac'">
                    <el-tag>
                      <i style="color: #19be6b" class="el-icon-success"></i>&ensp;
                      <span style="color: #495060">Accepted</span>
                    </el-tag>
                  </span>
                  <span v-if="result === 'waiting'">
                    <el-tag>
                      <i style="color: rgb(255,153,0)" class="el-icon-remove"></i>&ensp;
                      <span style="color: #495060">Waiting</span>
                    </el-tag>
                  </span>
                </span>
              </span>
            </div>
            <div v-if="msg !== 'ac'" class="status" style="margin-top: 10px;">
              {{msg}}
            </div>
          </div>
        </div>

      </div>
    </el-card>


    <el-button style="margin-top: 10px" @click="to_path('/contests')">返回列表</el-button>
  </div>

  <el-backtop :visibility-height="0"></el-backtop>
</div>
</template>

<script>
import {Base, Auth} from '../../components/mixins'

import {defineComponent} from 'vue'
import {ElMessage} from "element-plus";

export default defineComponent({
  name: "ContestDetail",
  mixins: [Base, Auth],
  data() {
    return {
      // 比赛 id
      cid: '',
      // 主办方
      holder: '',
      name: '',
      title: '',
      message: '',
      reward: '',
      require: '',
      // 报名的人
      sign_up_user: [],

      // 判断自己报没报名
      signed: false,

      status: 0,  // 0未开始报名，1已开始报名，2比赛进行中，3已结束

      sign_up_start_date: '',
      sign_up_end_date: '',
      remain_hours: '',
      remain_minutes: '',
      remain_seconds: '',
      contest_start_date: '',
      contest_end_date: '',

      // 如果status==2，即比赛进行中，获取比赛所有题目
      contest_problems: [],
      // 题目分页
      page: 1,  // 当前页数
      ordering: 'id',  // 排序
      problems_cnt: 0,
      // 用户通过题目数
      pass_cnt: 0,

      result: '',
      msg: '',
      // 返回结果记录
      results: [],

      // 比赛进行中
      // 提交比赛的 dialog 确定框
      dialogVisible: false,
      // 进入比赛开始计时
      enter_time: new Date(),
      finish_time: new Date(),

      // 比赛结束数据
      end_commit_users: [],
      end_rankings: [],
      end_problems: [],
      end_rankings_table: [],
      end_rankings_detail: [],
    }
  },
  mounted() {
    this.init_data()
    this.login()
    // 仅在报名中，登录检查
    if (sessionStorage.getItem('login_flag') === 'true') {
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
          this.holder = response.data['author_username']
          this.name = response.data['name']
          this.message = response.data['message'].replace(/\r\n/g,"<br/>")
          this.reward = response.data['reward']
          this.require = response.data['require']
          this.sign_up_user = response.data['sign_up_user']

          this.sign_up_start_date = response.data['sign_up_start_date']
          this.sign_up_end_date = response.data['sign_up_end_date']
          this.contest_start_date = response.data['contest_start_date']
          this.contest_end_date = response.data['contest_end_date']

          // 题目总数量
          this.problems_cnt = response.data['problems'].length

          // 0未开始报名，1已开始报名，2比赛进行中，3已结束
          if (response.data['is_no']) {
            this.status = 0
          } else if (response.data['is_sign']) {
            this.status = 1
          } else if (response.data['is_start']) {
            this.status = 2
            // 设置题目结果
            for (let i=0; i<this.problems_cnt; i++) {
              this.results.push('未通过')
            }
            // 请求比赛题目数据
            this.get_contest_problems()
          } else if (response.data['is_end']) {
            this.status = 3
            // 等待中
          } else if (response.data['is_wait']) {
            this.status = 4
            ElMessage.warning('比赛未开始，等待中')
            this.to_path('/contests')
          }

          let time
          // 报名如果开始、如果结束、这类的时间提示
          let message

          // 未开始报名 status = 0
          if (this.status === 0) {
            let new_time = this.sign_up_start_date.replace('年', '-')
            new_time = new_time.replace('月', '-').replace('日', '')
            new_time += ':00'
            time = new Date(new_time)
            message = '报名已开始'
            this.difference(new Date(), time)
          }
          // 开始报名 status = 1
          else if (this.status === 1) {
            // 2021年05月06日  05:54
            let new_time = this.sign_up_end_date.replace('年', '-')
            new_time = new_time.replace('月', '-').replace('日', '')
            new_time += ':00'
            // date like: 2021-05-12 12:15:12
            time = new Date(new_time)
            message = '报名已结束'
            this.difference(new Date(), time)
          }
          // 开始比赛 status = 2
          else if (this.status === 2) {
            this.$message({
              type: 'success',
              duration: 10000,
              showClose: true,
              message: '，您最终完成的时间将作为您最后成绩的一部分（此消息存在 10s）'
            });
            this.$notify.info({
              title: '提示',
              message: '请勿刷新或中途退出（此消息不会自动关闭）',
              duration: 0
            });
            let new_time = this.contest_end_date.replace('年', '-')
            new_time = new_time.replace('月', '-').replace('日', '')
            new_time += ':00'
            time = new Date(new_time)
            message = '比赛已结束'

            this.difference(new Date(), time)
          }
          // 结束了的话，就不用了倒计时了 status = 3
          else if (this.status === 3) {
            // 但是要获得一些数据：报名用户（按报名时间排序）、排名情况、题目列表
            this.$axios.get(this.$host + "/api/v1/contests/" + this.cid + '/ranking', {
              responseType: 'json'
            }).then(response => {
              if (response.data['code'] === 1) {
                console.log(response.data)
                this.end_commit_users = response.data['commit_users']
                this.end_rankings = response.data['rankings']
                this.end_problems = response.data['problems']

                for (let index in this.end_rankings) {
                  this.end_rankings_table.push({
                    'user': this.end_rankings[index]['user'][0][1],
                    'uid': this.end_rankings[index]['user'][0][0],
                    'rank': parseInt(index,10) + 1,
                    'spend_time': this.end_rankings[index]['spend_time'][0],
                    'cnt': this.end_rankings[index]['pass_problems'][0].length,
                  })
                }
                console.log(this.end_rankings_table)
              } else {
                ElMessage.error('获取比赛排名情况失败！请检查您的地址是否正确')
              }
            })
            return
          }

          let timer = setInterval(() => {
            this.difference(new Date(), time)
            // 时间结束
            if (this.remain_hours < 0 || this.remain_minutes < 0 || this.remain_seconds < 0) {
              this.$axios.get(this.$host + "/api/v1/cron/contests")
              clearInterval(timer)
              // 提示，然后刷新
              ElMessage.info(message)
              if (this.status === 2) {
                // 强制提交
                this.commit()
              }
              this.$router.go(0)
            }
          }, 1000)

      }).catch(_ => {
        // 肯定是没有比赛
        ElMessage.error('没有该比赛，访问错误！')
        this.to_path('/contests')
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

    // 点击页数，切换到相应页
    handleCurrentChange(val) {
      this.page = val;
    },

    // 如果status==2，即比赛进行中，获取比赛所有题目
    get_contest_problems() {
      this.cid = this.$route.params && this.$route.params.id;
      this.$axios.get(this.$host + "/api/v1/contests/" + this.cid + '/problems/', {
          params: {
            // 检查一下是否有权限
            uid: this.user_id,
          },
          responseType: 'json'
        }).then(response => {
          this.contest_problems = response.data.results

          // 越界访问！
          if (this.contest_problems.length === 0) {
            this.to_path('/contests')
          }
        }).catch(_ => {
          // 肯定是没权限，偷偷跑进来的，赶出去！
          this.to_path('/contests')
        })
    },

    // 报名检查
    sign_up_check() {
      this.$axios.post(this.$host + "/api/v1/contest/" + this.cid + '/sign/', {
          uid: this.user_id,
          option: 0  // 0 是检查是否报名，不做其他处理
        }, {
          responseType: 'json'
        }).then(response => {
          // 已报名
          if (response.data['code'] === 1) {
            this.signed = true
            // ElMessage.success('您已报名该比赛~')
          }
          // 未报名
          else if (response.data['code'] === -1) {
            this.signed = false
            // ElMessage.info('您未报名该比赛，欢迎报名~')
          }
          // 失败
          else {
            ElMessage.error('失败，请刷新网页重试~');
          }
      })
    },

    // 点击报名
    sign_up(option) {
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

      // 进行报名
      if (option === 1) {
        this.$axios.post(this.$host + "/api/v1/contest/" + this.cid + '/sign/', {
            uid: this.user_id,
            option: option    // 1 未报名，进行报名操作
          }, {
            responseType: 'json'
          }).then(response => {
            // 报名成功
            if (response.data['code'] === 1) {
              ElMessage.success('报名成功，祝您有个好成绩！');
              this.signed = true
            }
            // 已报名
            else if (response.data['code'] === -1) {
              ElMessage.info('报名成功，祝您有个好成绩！');
              this.signed = true
            }
            // 失败
            else {
              ElMessage.error('报名失败，请刷新网页重试~');
            }
        })
      } else if (option === 2) {
        // 取消报名
        this.$axios.post(this.$host + "/api/v1/contest/" + this.cid + '/sign/', {
            uid: this.user_id,
            option: option    // 2 已报名，取消报名
          }, {
            responseType: 'json'
          }).then(response => {
            // 取消报名成功
            if (response.data['code'] === 1) {
              ElMessage.success('已取消报名！');
              this.signed = false
            }
            // 已报名
            else if (response.data['code'] === -1) {
              ElMessage.info('已取消报名！');
              this.signed = false
            }
            // 失败
            else {
              ElMessage.error('取消报名失败，请刷新网页重试~');
            }
        })
      }
    },

    // 执行代码
    execute() {
      // 改变运行结果状态为执行中
      this.result = 'waiting'
      this.$axios.post(this.$host + "/api/v1/judge/", {
        uid: this.user_id,
        id: this.contest_problems[this.page-1]['id'],
        code: this.contest_problems[this.page-1]['init_code']
      }).then(response => {
        this.compiler_version = response.data['version']
        this.result = response.data['code']
        this.msg = response.data['output']

        if (this.result === 'ac') {
          this.$message({
            type: 'success',
            message: '运行通过！'
          });
          this.results[this.page-1] = '已通过'
          this.pass_cnt++
          this.msg = 'ac'
        } else {
          this.$message({
            type: 'error',
            message: '运行失败！请仔细检查您的代码噢~'
          });
        }
      }).catch(error => {
        console.log(error)
      })
    },

    // 提交比赛
    commit() {
      if (this.identity !== '普通用户') {
        ElMessage.warning('只有报名的普通用户才能提交哦~')
      }
      // 完成比赛时间
      this.finish_time = new Date()
      this.difference(this.enter_time, this.finish_time)
      // 我需要传入，用户id，比赛id，用户完成了哪些题，用时情况，这样就能查询到这个比赛所有题目
      // 保存到比赛里（和用户多对多关系）,保存到 ContestInfoResult
      let pass_problems = []
      for (let index in this.results) {
        if (this.results[index] === '已通过') {
          pass_problems.push(this.contest_problems[index].id)
        }
      }
      this.$axios.post(this.$host + "/api/v1/contest/" + this.cid + '/info/', {
          uid: this.user_id,
          problems: pass_problems,
          spend_time: [this.remain_hours, this.remain_minutes, this.remain_seconds]
          // 排名情况后台 crontab 里自己计算，设置这个人已完成比赛，报名比赛取消该比赛
        }, {
          responseType: 'json'
        }).then(response => {
          if (response.data['code'] === 1) {
            ElMessage.success('提交成功，比赛结束后方可查看自己排名')
            this.$router.go(-1)
          }
      })

    },
  }
})
</script>

<style scoped>

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

.description {
  display: inline-block;
  width: 50%;
  /*height: 500px;*/
  height: 70vh;
}

.scrollbar {
  background: rgba(255,255,255,0.85);
  -webkit-box-shadow:0 3px 3px #c3c3c3 inset;
  -moz-box-shadow:0 3px 3px #c3c3c3 inset;
  box-shadow:0 0 8px 2px #c3c3c3 inset;
}

.problems_header {
  font-size: 21px;
  font-weight: bold;
  font-family: Helvetica Neue,Helvetica,PingFang SC,Hiragino Sans GB,Microsoft YaHei,\\5FAE\8F6F\96C5\9ED1,Arial,sans-serif;
  -webkit-font-smoothing: antialiased;
  color: #495060;
  flex: 1;
}

.tables  ::v-deep(.el-table__expanded-cell) {
  padding: 20px;
}

.tables  ::v-deep(.el-table__expanded-cell) div {
  margin-bottom: 10px;
}

.tags > span {
  margin-right: 20px;
}

.problems_title {
  font-size: 17px;
  font-weight: 600;
  margin: 25px 0 10px;
  color: #3091f2;
}

.problems_msg {
  font-size: 16px;
  color: #495060;
}

.example {
  font-size: 14px;
  height: max-content;
  width: 100%;
}

.extra {
  margin-top: 16px;
}

.text_input {

  display: inline-block;
  width: 45%;
  float: right;
  height: 100%;
}

.text_input > .code_text {
  height: 69.4vh;
  width: 100%;
}

.status {
  font-size: 14px;
  color: #495060;
}
</style>