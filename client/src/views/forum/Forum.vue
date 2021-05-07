<template>
  <div id="Forum">
    <div class="container">
      <el-card>
        <div class="main">
          <el-tabs v-model="activeName" @tab-click="handleClick">

            <el-tab-pane v-for="tp in tabPanes" :label="tp.label" :name="tp.name">

              <transition-group>
                <el-card v-for="forum in forums" :key="forum.id" @click="to_path('/forum/' + forum.id)" class="items" shadow="always" title="点击查看详情">
                  <div class="header">
                    <div class="title">{{forum.title}}</div>
<!--                    <div class="watch">浏览次数：50</div>-->
                    <div class="watch">获赞次数：{{forum['like_cnt'].length}}</div>
                  </div>
                  <div class="content">{{forum.content}}</div>
                  <el-divider style="margin: 18px 0 0 0"></el-divider>
                  <div class="tip">
                    发布于：<el-button type="text">{{forum['publish_date']}}</el-button>

                    <el-divider v-if="~forum['modified']" style="margin: 0 20px" direction="vertical"></el-divider>

                    <span v-if="forum['modified']">最后修改于：<el-button type="text">{{forum['publish_date']}}</el-button></span>

                    <el-divider v-if="forum['modified']" style="margin: 0 20px" direction="vertical"></el-divider>

                    <span class="tip">来自 <el-button type="text" class="identity">
                      <span v-if="forum['author_is_admin'] === 'True'">管理员</span>
                      <span v-if="forum['author_is_p'] === 'True'">用户</span>
                      <span v-if="forum['author_is_oc'] === 'True'">机构</span>
                    </el-button>：<el-tag>{{forum['author_username']}}</el-tag></span>
                  </div>
                </el-card>
              </transition-group>

              <el-pagination
                v-if="count > 0"
                background
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                :current-page="page"
                :page-sizes="[5, 10, 20, 50]"
                :page-size="5"
                layout="total, sizes, prev, pager, next, jumper"
                :total="count"
                class="pagination">
              </el-pagination>

              <el-card v-if="count === 0" @click="to_path('forum_post')" style="margin: 30px 0; font-size: 14px; cursor: pointer">暂时还没有帖子，快去发表第一篇吧~</el-card>

            </el-tab-pane>

          </el-tabs>
        </div>

        <div class="side">
          <div style="position: relative" v-if="login_flag">
            <span style="font-size: 14px; padding-top: 10px;">您的身份：</span><el-tag>{{identity}}</el-tag>
            <el-divider style="margin: 10px 0"></el-divider>

            <div class="under">
              <div class="statistics">
                <span>发帖总数：{{forum_post.length}}</span>
                <span style="margin-left: 20px">获赞总数：{{like_cnt}}</span>
              </div>
              <el-button class="publish_btn" @click="to_path('forum_post')" size="small" round type="primary">发布帖子<i class="el-icon-s-promotion el-icon--right"></i></el-button>
            </div>
          </div>
          <div v-else style="float: right; margin: 10px 20px 0 0">
            <el-tag style="cursor:pointer;" @click="to_path('/login?next=/forum')">您还未登录</el-tag>
          </div>

          <div v-if="login_flag" class="history">
            💬 您的历史发帖

            <div class="example">
              <div class="example_title">标题</div>
              <div class="example_bottom">
                <div class="example_date">发布日期</div>
                <div class="example_like">获赞数</div>
              </div>
            </div>
            <el-divider style="margin: 0"></el-divider>


            <div @click="to_path('/forum/' + data.id)" class="show" v-for="data in forum_post.slice(0, 10)">
              <div style="font-size: 14px; font-weight: bold">{{data.title}}</div>
              <div class="example_bottom">
                <div style="color: rgb(64,188,255);font-size: 13px" class="example_date">{{data['publish_date']}}</div>
                <div class="example_like">{{data['like_cnt'].length}}</div>
              </div>

              <el-divider style="margin: 0"></el-divider>
            </div>
            <div class="show_tips" v-if="forum_post.length > 10">
              仅展示最近十条，剩余可在个人中心查看
            </div>

          </div>
        </div>
      </el-card>
    </div>


    <el-backtop :visibility-height="0"></el-backtop>
  </div>
</template>

<script>
import {Base, Auth} from '../../components/mixins'
export default {
  name: "forum",
  mixins: [Base, Auth],
  data() {
    return {
      activeName: 'all',

      page: 1,  // 当前页数
      page_size: 10,  // 每页数量
      ordering: '-publish_date',  // 排序

      count: 0,  // 总数量
      forums: [],  // 数据

      tabPanes: [
        { label: '🚩 全部主题', name: 'all'},
        { label: '🔥 热门', name: 'hot'},
        { label: '👀 来自用户', name: 'user'},
        { label: '🎯 来自机构', name: 'og'},
        { label: '🎈 来自管理员', name: 'admin'},
      ]
    }
  },
  methods: {
    // 切换每页多少数据
    handleSizeChange(val) {
      this.page_size = val;
      this.get_forums();
    },
    // 点击页数，切换到相应页
    handleCurrentChange(val) {
      this.page = val;
      this.get_forums();
    },
    // tab 切换事件
    handleClick() {
      // 设置为第一页
      this.page = 1
      //
      if (this.activeName === 'hot') {
        this.ordering = ''
      } else {
        this.ordering = '-publish_date'
      }
      this.get_forums()
    },

    // 获取数据
    get_forums() {
      this.$axios.get(this.$host + "/api/v1/forums/", {
        params: {
          page: this.page,
          page_size: this.page_size,
          ordering: this.ordering,
          from: this.activeName
        },
        responseType: 'json'
      }).then(response => {
        this.count = response.data.count
        this.forums = response.data.results
      }).catch(error => {
        console.log(error.response.data)
      })
    },

  },
  mounted() {
    this.get_forums()
    this.login()
  }
}
</script>

<style scoped>

.main {
  margin-left: 10px;
  display: inline-block;
  width: 65%;
}

.side {
  display: inline-block;
  float: right;
  width: 28%;
  margin-bottom: 20px;
}

.items {
  cursor: pointer;
  margin: 10px 0 20px 0;
}

.items ::v-deep(.el-card) > .el-card__body {
  padding: 12px 25px 8px 25px;
}

.header {
  width: 100%;
  margin: 5px 0 15px;

  display: flex;
}
.title {
  flex: 1;
  font-size: 17px;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.watch {
  font-size: 13px;
  color: #cac6c6;
  width: 20%;
  /*line-height: 23px;*/
  text-align: right;
}

.content {
  width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 16px;
  color: rgb(73, 80, 96);
  margin: 0 0 5px;
}

.tip {
  margin-top: 3px;
  font-size: 14px;
}

.tip ::v-deep(.el-tag) {
  height: 30px;
  line-height: 30px;
}

.tip .identity {
  border-radius: 0;
  font-weight: 600;
  padding: 0;
  border-bottom: 1px solid rgb(64,158,255);
}
.pagination {
  margin: 40px 0 0 10px;
}

.history {
  margin: 60px 0 20px 0;
}

.under {
  display: flex;
}
.statistics {
  font-size: 14px;
  margin-top: 5px;
  flex: 1;
  text-overflow: ellipsis;
  white-space: normal;
  word-break: break-all;
  height: 22px;
  vertical-align: center;
}


.example {
  margin: 20px 0 10px;
  font-size: 14px;
  color: rgb(144, 147, 153);
  font-weight: bold;
}
.example_bottom {
  display: flex;
}
.example_date {
  flex: 1;
}

.show {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: normal;
  word-break: break-all;
  line-height: 23px;
  font-size: 14px;
  color: rgb(96, 98, 102);
  cursor: pointer;
  margin: 20px 0;
}
.show:hover {

}
.show_tips {
  margin-top: 30px;
  color: rgb(64, 158, 255);
  font-size: 14px;
  text-align: center;;
  /*border-bottom: 1px solid rgb(64, 158, 255);*/
}

/* 列表加载动画 */
.v-enter-from {
  opacity: 0;
  transform: translateY(30px);
}
.v-enter-to {
  opacity: 1;
  transform: translateY(0);
}
.v-enter,.v-leave-to{
    opacity: 0;
    transform: translateY(30px);
}

.v-enter-active,.v-leave-active{
    transition: all 0.8s ease;
}
/*v-move 和 v-leave-active 配合使用，能够实现列表后续的元素，渐渐地漂上来的效果 */

.v-move{
    transition: all 0.8s ease;
}
.v-leave-active{
    position: absolute;
}
</style>