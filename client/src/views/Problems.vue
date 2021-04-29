<template>
  <div id="problems">
    <div class="container">
      <div>
        <div>
          <div>算法：</div>
          <div>数据结构：</div>
        </div>
        <br>
        <div class="sort_bar">
          <span v-if="id_sort">
            <a @click="on_sort('-id')" :class="ordering==='id'?'active':''">序号 🔽</a>
          </span>
          <span v-else>
              <a @click="on_sort('id')" :class="ordering==='id'?'active':''">序号 🔼</a>
          </span>
          |
          <span v-if="header_sort">
            <a @click="on_sort('-header')" :class="ordering==='header'?'active':''">难度 🔽</a>
          </span>
          <span v-else>
            <a @click="on_sort('header')" :class="ordering==='header'?'active':''">难度 🔼</a>
          </span>
        </div>

        <div class="pagination">
          <a v-show="previous" @click="on_page(previous)">上一页</a>
          <a v-for="num in page_nums" @click="on_page(num)" :class="num===page?'active':''">{{ num }}</a>
          <a v-show="next" @click="on_page(next)">下一页></a>
        </div>
      </div>

      <el-card class="box-card">
        <el-card v-for="problem in problems" :key="problem.id" @click="enter(problem.id)" class="items" shadow="hover">
          <h4 style="display: inline">{{ problem.id + ". " + problem.name }}</h4>
          <span class="header">{{ problem.header }}</span>
          <div class="tips">
            <span class="tip">算法类型：{{ problem.alg_type }}</span>
            <span class="tip">数据结构：{{ problem.ds_type }}</span>
          </div>
        </el-card>
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
      problems: [],  // 数据


    };
  },
  methods: {
    enter(pid) {
      this.$router.push('/problems/' + pid)
    },
    filter(name) {
      this.$router.push({path: "/problems", query: {alg_type: name}});
    },
    get_query_string(name) {
      const reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
      const r = window.location.search.substr(1).match(reg);
      if (r != null) {
        return decodeURI(r[2])
      }
      return null
    },
    get_problems() {
      this.$axios.get(this.$host + "/api/v1/problems/", {
        params: {
          page: this.page,
          page_size: this.page_size,
          ordering: this.ordering
        },
        responseType: 'json'
      }).then(response => {
        this.count = response.data.count
        this.problems = response.data.results
      }).catch(error => {
        console.log(error.response.data)
      })
    },
    // 点击页数
    on_page(num) {
      if (num !== this.page) {
        this.page = num
        this.get_problems()
      }
    },
    // 点击排序
    on_sort(ordering) {
      if (ordering === 'id' || ordering === '-id') {
        this.id_sort = !this.id_sort
      }
      if (ordering === 'header' || ordering === '-header') {
        this.header_sort = !this.header_sort
      }

      if (ordering !== this.ordering) {
        this.page = 1
        this.ordering = ordering
        this.get_problems()
      }
    }
  },
  computed: {
    // 总页数
    total_page: function () {
      return Math.ceil(this.count / this.page_size);
    },
    // 下一页
    next: function () {
      if (this.page >= this.total_page) {
        return 0;
      } else {
        return this.page + 1;
      }
    },
    // 上一页
    previous: function () {
      if (this.page <= 0) {
        return 0;
      } else {
        return this.page - 1;
      }
    },
    // 页码
    page_nums: function () {
      // 分页页数显示计算
      // 1.如果总页数<=5
      // 2.如果当前页是前3页
      // 3.如果当前页是后3页,
      // 4.既不是前3页，也不是后3页
      let i;
      let nums = [];
      if (this.total_page <= 5) {
        for (i = 1; i <= this.total_page; i++) {
          nums.push(i);
        }
      } else if (this.page <= 3) {
        nums = [1, 2, 3, 4, 5];
      } else if (this.total_page - this.page <= 2) {
        for (i = this.total_page; i > this.total_page - 5; i--) {
          nums.push(i);
        }
      } else {
        for (i = this.page - 2; i < this.page + 3; i++) {
          nums.push(i);
        }
      }
      return nums;
    }
  },
  mounted() {
    // this.cat = this.get_query_string('cat')

    this.get_problems()
  }
}
</script>

<style scoped>

.container {
  width: 1142px;
  margin: 0 auto;
  padding-top: 150px;
}

.container .box-card {
  position: relative;
  top: 100px;
  box-shadow: rgba(0 0 0 .17) 13px 15px 13px 2px;
}

.items {
  cursor: pointer;
  margin: 10px 0;
}

.header {
  margin-left: 30px;
  font-size: 13px;
}

.tips {
  margin-top: 10px;
}

.tip {
  margin-right: 40px;
  font-size: 15px;
}
</style>