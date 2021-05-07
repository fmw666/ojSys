<template>
  <div id="contests">
    <div class="container">
      <div style="float: right">
        <router-link to="/sregister">
          <el-tag size="small">机构注册？成为赛事方</el-tag>
        </router-link>
      </div>

      <el-card style="width: 100%">
        <el-tabs style="margin: 0 20px" v-model="activeName" @tab-click="handleClick">

          <el-tab-pane v-for="tp in tabPanes" :label="tp.label" :name="tp.name">

            <transition-group>
              <el-card v-for="contest in contests" :key="contest.id" @click="to_path('/contests/' + contest.id)" class="items" shadow="always">
                <div class="card-left">
                  <h4 class="header">{{contest.name}}</h4>
                  <span class="holder">——主办方：{{contest['author_username']}}</span>
                  <div class="tips">
                    <div class="tip">正式比赛时间：</div>
                    <el-tag>{{contest['contest_start_date']}}</el-tag>
                    <span class="divider-line">--</span>
                    <el-tag>{{contest['contest_end_date']}}</el-tag>
                  </div>
                </div>

                <el-divider direction="vertical" style="height: 30px"></el-divider>

                <div class="card-right">
                  <span class="tip">报名开始时间：</span>
                  <el-button type="text" style="padding: 5px">{{contest['sign_up_start_date']}}</el-button>
                  <span class="tip">报名截至时间：</span>
                  <el-button type="text" style="padding: 5px">{{contest['sign_up_end_date']}}</el-button>

                  <span class="tip" style="margin-top: 7px">当前报名人数：3</span>
                </div>

              </el-card>
            </transition-group>

            <el-pagination
              v-if="count > 0"
              background
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
              :current-page="page"
              :page-sizes="[10, 20, 50, 100]"
              :page-size="10"
              layout="total, sizes, prev, pager, next, jumper"
              :total="count"
              class="pagination">
            </el-pagination>

            <el-card v-if="count === 0" style="margin: 30px 0; font-size: 14px; cursor: pointer">暂时还没有相关信息，请下次再来吧~</el-card>

          </el-tab-pane>
        </el-tabs>
      </el-card>

    </div>


    <el-backtop :visibility-height="0"></el-backtop>
  </div>
</template>

<script>
import {Base} from '../../components/mixins'
export default {
  mixins: [Base],
  data() {
    return {

      page: 1,  // 当前页数
      page_size: 20,  // 每页数量
      ordering: 'id',  // 排序
      id_sort: true,  // true 代表顺序，false 代表反序
      header_sort: true, // true 代表顺序，false 代表反序
      count: 0,  // 总数量
      contests: [],  // 数据

      activeName: 'sign',

      tabPanes: [
        { label: '⭐ 报名中', name: 'sign'},
        { label: '💬 未开始', name: 'no'},
        { label: '🎈 已结束', name: 'end'},
        { label: '🚀 进行中', name: 'start'},
      ]
    };
  },
  methods: {
    // 切换每页多少数据
    handleSizeChange(val) {
      this.page_size = val;
      this.get_contests();
    },
    // 点击页数，切换到相应页
    handleCurrentChange(val) {
      this.page = val;
      this.get_contests();
    },
    // 点击 Tabs 标签页触发事件
    handleClick() {
      // 设置为第一页
      this.page = 1
      this.get_contests();
    },

    get_contests() {
      this.$axios.get(this.$host + "/api/v1/contests/", {
        params: {
          page: this.page,
          page_size: this.page_size,
          ordering: this.ordering,
          status: this.activeName
        },
        responseType: 'json'
      }).then(response => {
        this.count = response.data.count
        this.contests = response.data.results
      }).catch(error => {
        console.log(error.response.data)
      })
    },

    // 点击排序
    on_sort(ordering) {
      if (ordering === 'id' || ordering === '-id') {
        this.id_sort = ! this.id_sort
      }
      if (ordering === 'header' || ordering === '-header') {
        this.header_sort = ! this.header_sort
      }

      if (ordering !== this.ordering) {
        this.page = 1
        this.ordering = ordering
        this.get_contests()
      }
    }
  },
  computed: {

  },
  mounted() {
    // this.cat = this.get_query_string('cat')

    this.get_contests()
  }
}
</script>

<style scoped>

.container .box-card {
  box-shadow: rgba(0 0 0 .17) 13px 15px 13px 2px;
}
.card-left {
  width: 62%;
  display: inline-block;

      vertical-align: middle;
}
.items ::v-deep(.el-card) .el-card__body {
  position: relative;
}
.card-right {
  float: right;
  width: 30%;
  position: absolute;
  top: 0;
  bottom: 0;
  right: 0;
  margin: auto;
  height: 82px;
}
.items {
  cursor: pointer;
  margin: 10px 0;
  width: 100%;
  height: 100%;
}

.header {
  display: inline;
  font-size: 18px;
  line-height: 30px;
}

.holder {
  margin-left: 20px;
  font-size: 16px;
  line-height: 30px;
}
.tips {
  margin-top: 16px;
}
.tip {
  display: inline-block;
  margin-right: 10px;
  font-size: 14px;
}
.divider-line {
  color: rgb(64,158,255);
}

.pagination {
  margin: 40px 0 0 10px;
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