<template>
<div id="ForumDetail">
  <div class="container">
    <el-card>
      <div class="header">
        <div class="title">{{forumDetail.title}}</div>
        <span style="margin-left: 30px;" class="date_tip">最后修改于：{{forumDetail['modify_date']}}</span>
      </div>
      <div class="date_tip" style="margin-bottom: 30px">创建于：{{forumDetail['publish_date']}}</div>

      <div class="content">{{forumDetail['content']}}</div>

      <el-divider></el-divider>

      <div class="bottom">
        <div class="bottom_left">
          <div class="msg">作者</div>
          <div class="content">
            <el-tag>
              <span v-if="forumDetail['author_is_admin'] === 'True'">管理员</span>
              <span v-if="forumDetail['author_is_p'] === 'True'">用户</span>
              <span v-if="forumDetail['author_is_oc'] === 'True'">机构</span> — {{forumDetail['author_username']}}
            </el-tag>
          </div>
        </div>

        <div class="bottom_right">
          <div v-if="is_like === false" class="no_like" @click="click_like">
            <i style="font-size: 20px" class="el-icon-star-off"></i> {{cnt}}人赞
          </div>
          <div v-else class="yes_like" @click="cancel_like">
            <i style="font-size: 22px" class="el-icon-star-on"></i> {{cnt}}人赞
          </div>
        </div>
      </div>

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
  name: "ForumDetail",
  mixins: [Base, Auth],
  data() {
    return {

      fid: '',
      forumDetail: {},

      // 是不是自己的帖子
      myself: false,
      // 点没点赞
      is_like: false,
      cnt: 0
    }
  },
  watch: {
    is_like: {
      handler(old_val, new_val) {
        this.init_data()
      }
    }
  },
  mounted() {
    this.init_data()
    this.login()
    if (this.login_flag === true) {
      this.init_data()
    }
  },
  methods: {

    init_data() {
      this.fid = this.$route.params && this.$route.params.id;
      this.$axios.get(this.$host + "/api/v1/forums/" + this.fid, {
          responseType: 'json'
        })
        .then(response => {
          this.forumDetail = response.data
          this.cnt = this.forumDetail['like_cnt'].length
          // 1. 检查文章是不是本人的
          if (this.user_id.toString() === response.data['author'].toString()) {
            this.myself = true
          }
          // 2. 如果不是本人的，那么自己点没点赞
          const array = new Array(response.data['like_cnt'])
          for (let i=0; i<array[0].length; i++) {
            if (array[0][i].toString() === this.user_id.toString()) {
              this.is_like = true
              break
            }
          }
      });

    },
    // 点赞
    click_like() {
      // 未登录
      if (this.login_flag === false) {
        this.$confirm('您还未进行登录, 请先登录！', '提示', {
          confirmButtonText: '去登录',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.to_path('/login?next=/forum/' + this.fid)
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消登录'
          });
        });
        return
      }

      // 登录了
      if (this.myself === true) {
        ElMessage.warning('不允许给自己的帖子点赞哦~');
        return
      }

      // 其他用户
      this.fid = this.$route.params && this.$route.params.id;
      this.$axios.post(this.$host + "/api/v1/forums/" + this.fid, {
          uid: this.user_id,
          option: 0
        }, {
          responseType: 'json'
        })
        .then(response => {
          if (response.data['code'] === 1) {
            this.is_like = true
            ElMessage.success('感谢您对这篇帖子的认可~');
          } else {
            ElMessage.error('点赞失败，请刷新网页重试~');
          }
      });

    },
    // 取消点赞
    cancel_like() {
      // 这个不用登录验证了，因为 is_like 前已经做了
      this.fid = this.$route.params && this.$route.params.id;
      this.$axios.post(this.$host + "/api/v1/forums/" + this.fid, {
          uid: this.user_id,
          option: 1
        }, {
          responseType: 'json'
        })
        .then(response => {
          if (response.data['code'] === 1) {
            this.is_like = false
            ElMessage.info('您取消了点赞~');
          } else {
            ElMessage.error('点赞失败，请刷新网页重试~');
          }
      });

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
  margin: 0 0 20px 0;
}
.title {
  display: inline;
  font-size: 19px;
  font-weight: 600;
}
.date_tip {
  font-size: 15px;
  color:rgb(202, 198, 198);
}
.msg {
  color: #3091f2;
  font-size: 17px;
  font-weight: bold;
  margin: 10px 0 12px 0;
}
.content {
  word-wrap:break-word;
}

.bottom {
  display: flex;
}
.bottom_left {
  flex: 1;
}
.bottom_right {
  width: 20%;
  align-self: flex-end;
  text-align: right;
  margin-bottom: 2px;
  font-size: 16px;
}

.no_like {
  cursor: pointer;
  float: right;
}
.no_like:hover {
  color: rgb(222, 104, 70);
}

.yes_like {
  cursor: pointer;
  float: right;
  color: rgb(238, 69, 21);
}
.yes_like i {
  font-size: 19px;
}
.no_like:hover {
  color: rgb(238, 91, 49);
}
</style>