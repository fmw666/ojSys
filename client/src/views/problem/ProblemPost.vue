<template>
<div id="ProblemPost">
  <div class="container">
    <el-card>
        <el-scrollbar native>
          <div style="height: 70vh; padding: 20px 40px 60px 20px">
            <div class="title">创建题目</div>
            <el-form>
              <el-form-item label="题目名称">
                <el-input v-model="name"></el-input>
              </el-form-item>

              <el-form-item label="题目描述信息">
                <el-input type="textarea" v-model="message"></el-input>
              </el-form-item>

              <el-form-item label="输入样例">
                <el-input type="textarea" v-model="input_example"></el-input>
              </el-form-item>

              <el-form-item label="输出样例">
                <el-input type="textarea" v-model="output_example"></el-input>
              </el-form-item>

              <el-form-item label="挑战（非必须）">
                <el-input type="textarea" v-model="challenge"></el-input>
              </el-form-item>

              <el-select v-model="alg_type" placeholder="算法类型">
                <el-option
                  v-for="item in alg_types"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>

              <el-select v-model="ds_type" placeholder="数据结构类型">
                <el-option
                  v-for="item in ds_types"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>

              <el-select v-model="header" placeholder="难度">
                <el-option
                  v-for="item in headers"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>

              <el-form-item label="题目初始化显示">
                <el-input type="textarea" v-model="init_code"></el-input>
              </el-form-item>

              <el-form-item label="题目测试代码文本部分">
                <el-input type="textarea" v-model="test_code"></el-input>
              </el-form-item>


              <el-form-item label="是否公开">
                <el-radio v-model="open" label="no">不公开</el-radio>
                <el-radio v-model="open" label="yes">公开</el-radio>
              </el-form-item>

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
  name: "ProblemPost",
  mixins: [Base, Auth],
  data() {
    return {
      name: '',
      message: '',
      input_example: '',
      output_example: '',
      challenge: '',
      alg_type: '',
      alg_types: ['基础', '贪心算法', 'DFS/BFS', '动态规划', '二分法', '最短路径算法'],
      ds_type: '',
      ds_types: ['基础', '数组', '链表', '栈', '队列', '哈希表', '树', '图'],
      header: '',
      headers: ['入门', '简单', '中等', '困难', '特难'],
      open: 'no',
      init_code: 'class Solution:\n' +
          '    """\n' +
          '    @param a: An integer\n' +
          '    @param b: An integer\n' +
          '    @return: The sum of a and b \n' +
          '    """\n' +
          '    def aplusb(self, a, b):\n' +
          '        # write your code here',
      test_code: 'inputs = [[1,2],[100,200],[-3,-1],[0,3]]\n' +
          'corrects= [3,300,-4,3]\n' +
          '\n' +
          'if len(inputs) != len(corrects):\n' +
          '    raise Exception(\'题目测试集错误，请联系管理员进行重修审核\')\n' +
          '\n' +
          's = Solution()\n' +
          'for i in range(len(inputs)):\n' +
          '    params = inputs[i]\n' +
          '    if s.aplusb(params[0], params[1]) != corrects[i]:\n' +
          '        raise Exception(\'输入值:{0}, {1}. 不等于正确值:{2}\'.format(params[0],params[1],corrects[i]))',
    }
  },
  mounted() {
    this.login()
  },
  methods: {
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
          problems: this.value,
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
      this.name = ''
      this.message = ''
      this.input_example = ''
      this.output_example = ''
      this.challenge = ''
      this.alg_type = ''
      this.ds_type = ''
      this.open = 'no'

      this.init_code = 'class Solution:\n' +
          '    """\n' +
          '    @param a: An integer\n' +
          '    @param b: An integer\n' +
          '    @return: The sum of a and b \n' +
          '    """\n' +
          '    def aplusb(self, a, b):\n' +
          '        # write your code here'
      this.test_code = 'inputs = [[1,2],[100,200],[-3,-1],[0,3]]\n' +
          'corrects= [3,300,-4,3]\n' +
          '\n' +
          'if len(inputs) != len(corrects):\n' +
          '    raise Exception(\'题目测试集错误，请联系管理员进行重修审核\')\n' +
          '\n' +
          's = Solution()\n' +
          'for i in range(len(inputs)):\n' +
          '    params = inputs[i]\n' +
          '    if s.aplusb(params[0], params[1]) != corrects[i]:\n' +
          '        raise Exception(\'输入值:{0}, {1}. 不等于正确值:{2}\'.format(params[0],params[1],corrects[i]))'
    },
  }
}
</script>

<style scoped>

</style>