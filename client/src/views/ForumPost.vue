<template>
  <div id="ForumPost">
    <div class="container">
      <el-card>
        <div class="title">发布帖子</div>
        <el-form>
          <el-form-item label="标题">
            <el-input v-model="title"></el-input>
          </el-form-item>

          <el-form-item label="内容">
            <el-input type="textarea" v-model="content"></el-input>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="publish">立即发布</el-button>
            <el-button @click="reset">重置</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script>
import {Base, Auth} from '../components/mixins'
import {ElMessage} from "element-plus";

export default {
  name: "ForumPost",
  mixins: [Base, Auth],
  data() {
    return {
      title: '',
      content: '',
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
          this.to_path('/login?next=/forum_post')
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消登录'
          });
        });
        return
      }

      // 登录了
      this.$axios.post(this.$host + "/api/v1/forums/post/" + this.user_id, {
          title: this.title,
          content: this.content
        }, {
          responseType: 'json'
        })
        .then(response => {
          if (response.data['code'] === 1) {
            ElMessage.success('发布成功！已为您跳转到您的帖子');
            this.to_path('/forum/' + response.data['fid'])
          } else {
            ElMessage.error('发布失败，请刷新网页重试~');
          }
      });
    },

    // 重置表单
    reset() {
      this.title = '';
      this.content = '';
    },
  }
}
</script>

<style scoped>
.container {
  /*width: 1130px;*/
  width: 66vw;
  margin: 0 auto;
  padding-top: 120px;
}
</style>