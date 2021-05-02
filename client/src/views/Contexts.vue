<template>
  <div id="contexts">
    <div class="container">
      <router-link to="/sregister">机构注册？成为赛事方</router-link>

      <el-card>
        <el-tabs v-model="activeName" @tab-click="handleClick">
          <el-tab-pane label="报名中" name="first">
            <el-card v-for="context in contexts" :key="context.id" @click="to_path(context.id)" class="items" shadow="always">
              <h4 style="display: inline">{{context.name}}</h4>
              <div class="tips">
                <span class="tip">主办方：{{context.author_username}}</span>
                <span class="tip">| {{context.create_date}}</span>
                <span class="tip">报名人数 3</span>
              </div>
            </el-card>

            <el-pagination
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
          </el-tab-pane>

          <el-tab-pane label="未开始" name="second">
            <el-card v-for="context in contexts" :key="context.id" @click="to_path(context.id)" class="items" shadow="always">
              <h4 style="display: inline">{{context.name}}</h4>
              <div class="tips">
                <span class="tip">主办方：{{context.author_username}}</span>
                <span class="tip">| {{context.create_date}}</span>
              </div>
            </el-card>

            <el-pagination
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
          </el-tab-pane>

          <el-tab-pane label="已结束" name="third">
            <el-card v-for="context in contexts" :key="context.id" @click="to_path(context.id)" class="items" shadow="always">
              <h4 style="display: inline">{{context.name}}</h4>
              <div class="tips">
                <span class="tip">主办方：{{context.author_username}}</span>
                <span class="tip">| {{context.create_date}}</span>
              </div>
            </el-card>

            <el-pagination
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
          </el-tab-pane>
        </el-tabs>
      </el-card>

    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        page: 1,  // 当前页数
        page_size: 20,  // 每页数量
        ordering: 'id',  // 排序
        id_sort: true,  // true 代表顺序，false 代表反序
        header_sort: true, // true 代表顺序，false 代表反序
        count: 0,  // 总数量
        contexts: [],  // 数据

        activeName: 'second',

      };
    },
    methods: {
      // 切换每页多少数据
      handleSizeChange(val) {
        this.page_size = val;
        this.get_contexts();
      },
      // 点击页数，切换到相应页
      handleCurrentChange(val) {
        this.page = val;
        this.get_contexts();
      },
      // 路由跳转
      to_path(cid) {
        this.$router.push('/contexts/' + cid)
      },
      // 点击 Tabs 标签页触发事件
      handleClick(tab, event) {
        console.log(tab, event);
      },
      filter(name) {
        this.$router.push({ path: "/contexts", query: { alg_type: name } });
      },
      get_query_string(name) {
        const reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
        const r = window.location.search.substr(1).match(reg);
        if (r != null) {
          return decodeURI(r[2])
        }
        return null
      },
      get_contexts() {
        this.$axios.get(this.$host + "/api/v1/contexts/", {
          params: {
            page: this.page,
            page_size: this.page_size,
            ordering: this.ordering
          },
          responseType: 'json'
        }).then(response => {
          this.count = response.data.count
          this.contexts = response.data.results
          console.log(response.data)
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
          this.get_contexts()
        }
      }
    },
    computed: {

    },
    mounted() {
      // this.cat = this.get_query_string('cat')

      this.get_contexts()
    }
  }
</script>

<style scoped>
.container {
  width: 1142px;
  margin: 0 auto;
  padding-top: 140px;
}
.container .box-card {
  box-shadow: rgba(0 0 0 .17) 13px 15px 13px 2px;
}
.items {
  cursor: pointer;
  margin: 10px 0;
}
.tips {
  margin-top: 10px;
}
.tip {
  margin-right: 40px;
  font-size: 15px;
}

.pagination {
  margin: 40px 0 0 10px;
}
</style>