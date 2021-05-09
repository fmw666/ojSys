<template>
  <div id="ContestPost">
    <div class="container">
      <el-card>
        <el-scrollbar native>
          <div style="height: 70vh; padding: 20px 40px 60px 20px">
            <div class="title">发布比赛</div>
            <el-form>
              <div style="display: flex">
                <div style="flex: 1; padding: 10px">
                  <el-form-item label="比赛标题">
                    <el-input v-model="name"></el-input>
                  </el-form-item>

                  <el-form-item label="描述信息">
                    <el-input resize="none" :autosize="{ minRows: 10, maxRows: 10}" type="textarea" v-model="message"></el-input>
                  </el-form-item>
                </div>

                <div style="width: 50%; padding: 10px">
                  <el-form-item label="奖励信息">
                    <el-input resize="none" :autosize="{ minRows: 6, maxRows: 6}" type="textarea" v-model="reward"></el-input>
                  </el-form-item>

                  <el-form-item label="比赛要求">
                    <el-input resize="none" :autosize="{ minRows: 5, maxRows: 5}" type="textarea" v-model="require"></el-input>
                  </el-form-item>
                </div>
              </div>


              <el-transfer
                v-model="my_problems"
                filterable
                :filter-method="filterMethod"
                filter-placeholder="请输入要查找的题目"
                :data="my_problems_data"
                :titles="['我的题目列表', '已选择题目']"
              />

              <el-transfer
                v-model="other_problems"
                filterable
                :filter-method="filterMethod"
                filter-placeholder="请输入要查找的题目"
                :data="other_problems_data"
                :titles="['其他题目列表', '已选择题目']"
              />

              <div>
                <el-date-picker
                  v-model="date_sign_up"
                  type="datetimerange"
                  align="right"
                  start-placeholder="开始日期"
                  end-placeholder="结束日期"
                  :default-time="defaultTime">
                </el-date-picker>
              </div>

              <div>
                <el-date-picker
                  v-model="date_contest"
                  type="datetimerange"
                  align="right"
                  start-placeholder="开始日期"
                  end-placeholder="结束日期"
                  :default-time="defaultTime">
                </el-date-picker>
              </div>

              <el-form-item>
                <el-button type="primary" @click="publish">立即发布</el-button>
                <el-button @click="reset">重置</el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-scrollbar>
      </el-card>
    </div>
  </div>
</template>

<script>
import {Base, Auth} from '../../components/mixins'
import {ElMessage} from "element-plus";

export default {
  name: "ContestPost",
  mixins: [Base, Auth],
  data() {
    return {
      name: '',
      message: '',
      reward: '',
      require: '',

      my_problems_data: [],
      my_problems: [],
      other_problems_data: [],
      other_problems: [],
      filterMethod(query, item) {
        return item.spell.indexOf(query) > -1;
      },

      defaultTime: [
          new Date(new Date().getFullYear(), new Date().getMonth(), new Date().getDate(), new Date().getHours(), new Date().getMinutes(), new Date().getSeconds()),
      ], // '12:00:00', '08:00:00'
      date_sign_up: '',
      date_contest: '',
    }
  },
  mounted() {
    this.login()
    this.get_my_problems()
    this.get_other_problems()
  },
  methods: {
    // 自己发布的题
    get_my_problems() {
      // 获取所有比赛数据
      this.$axios.get(this.$host + "/api/v1/problems/my/", {
          params: {
            uid: this.user_id,
          },
          responseType: 'json'
        }).then(response => {
          const data = [];
          response.data.results.forEach((problem) => {
            data.push({
              label: problem['name'],
              key: problem['id'],
              spell: problem['name']
            });
          });
          this.my_problems_data = data
        })
    },
    // 所有人发布的题
    get_other_problems() {
      // 获取所有比赛数据
      this.$axios.get(this.$host + "/api/v1/problems/", {
          params: {
            page_size: Number.MAX_SAFE_INTEGER,
            ordering: 'id',
          },
          responseType: 'json'
        }).then(response => {
          const data = [];
          response.data.results.forEach((problem) => {
            data.push({
              label: problem['name'],
              key: problem['id'],
              spell: problem['name']
            });
          });
          this.other_problems_data = data
        })
    },
    // 点击发布
    publish() {
      // 未登录
      if (this.login_flag === false) {
        this.$confirm('您还未进行登录, 请先登录！', '提示', {
          confirmButtonText: '去登录',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.to_path('/login?next=/contest_post')
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消登录'
          });
        });
        return
      }

      // 登录了
      this.$axios.post(this.$host + "/api/v1/contests/post/" + this.user_id, {
          name: this.name,
          message: this.message,
          reward: this.reward,
          require: this.require,
          problems: Array.from(new Set(this.other_problems.concat(this.my_problems))),
          date_sign_up: this.date_sign_up,
          date_contest: this.date_contest,
        }, {
          responseType: 'json'
        })
        .then(response => {
          if (response.data['code'] === 1) {
            ElMessage.success('发布成功！已为您跳转到您的帖子');
            this.to_path('/contests/' + response.data['cid'])
          } else {
            ElMessage.error('发布失败，请刷新网页重试~');
          }
      });
    },

    // 重置表单
    reset() {
      this.title = '';
      this.message = '';
      this.reward = ''
      this.require = ''
      this.my_problems = []
      this.other_problems = []
      this.date_sign_up = ''
      this.date_contest = ''
    },
  }
}
</script>


<style scoped>
.title {
  color: #3091f2;
  font-size: 17px;
  font-weight: bold;
  margin: 10px 0 20px 0;
}
</style>