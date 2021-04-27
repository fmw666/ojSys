<template>
  <div id="contexts">

    <br><br><br><br><br><br>

    <router-link to="/sregister">机构注册？成为赛事方</router-link>

    <div class="left">
      <span v-if="id_sort">
        <a @click="on_sort('-id')" :class="ordering=='id'?'active':''">报名中 🔽</a>
      </span>
      <span v-else>
        <a @click="on_sort('id')" :class="ordering=='id'?'active':''">报名中 🔼</a>
      </span>
      |
      <span v-if="header_sort">
        <a @click="on_sort('-header')" :class="ordering=='header'?'active':''">进行中 🔽</a>
      </span>
      <span v-else>
        <a @click="on_sort('header')" :class="ordering=='header'?'active':''">进行中 🔼</a>
      </span>
      |
      <span v-if="header_sort">
        <a @click="on_sort('-header')" :class="ordering=='header'?'active':''">已结束 🔽</a>
      </span>
      <span v-else>
        <a @click="on_sort('header')" :class="ordering=='header'?'active':''">已结束 🔼</a>
      </span>
    </div>

    <div class="pagenation">
      <a v-show="previous" @click="on_page(previous)">上一页</a>
      <a v-for="num in page_nums" @click="on_page(num)" :class="num==page?'active':''">{{num}}</a>
      <a v-show="next" @click="on_page(next)">下一页></a>
    </div>

    <el-card class="box-card">
      <div v-for="context in contexts" :key="context.id" @click="enter(context.id)" class="items">
        <h4>{{context.name}}</h4>
        <div class="tips">
          <span class="tip">主办方：{{context.author_username}}</span>
          <span class="tip">| {{context.create_date}}</span>
        </div>
        <el-divider></el-divider>
      </div>
    </el-card>
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


      };
    },
    methods: {
      enter(cid) {
        this.$router.push('/contexts/' + cid)
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
      // 点击页数
      on_page(num) {
        if (num != this.page) {
          this.page = num
          this.get_problems()
        }
      },
      // 点击排序
      on_sort(ordering) {
        if (ordering == 'id' || ordering == '-id') {
          this.id_sort = ! this.id_sort
        }
        if (ordering == 'header' || ordering == '-header') {
          this.header_sort = ! this.header_sort
        }

        if (ordering != this.ordering) {
          this.page = 1
          this.ordering = ordering
          this.get_contexts()
        }
      }
    },
    computed: {
      // 总页数
      total_page: function() {
        return Math.ceil(this.count/this.page_size);
      },
      // 下一页
      next: function() {
        if (this.page >= this.total_page) {
          return 0;
        } else {
          return this.page + 1;
        }
      },
      // 上一页
      previous: function() {
        if (this.page <= 0 ) {
          return 0;
        } else {
          return this.page - 1;
        }
      },
      // 页码
      page_nums: function() {
        // 分页页数显示计算
        // 1.如果总页数<=5
        // 2.如果当前页是前3页
        // 3.如果当前页是后3页,
        // 4.既不是前3页，也不是后3页
        let i = 1;
        let nums = [];
        if (this.total_page <= 5) {
          for (i=1; i<=this.total_page; i++) {
            nums.push(i);
          }
        } else if (this.page <= 3) {
          nums = [1, 2, 3, 4, 5];
        } else if (this.total_page - this.page <= 2) {
          for (i=this.total_page; i>this.total_page-5; i--) {
            nums.push(i);
          }
        } else {
          for (i=this.page-2; i<this.page+3; i++){
            nums.push(i);
          }
        }
        return nums;
      }
    },
    mounted() {
      // this.cat = this.get_query_string('cat')

      this.get_contexts()
    }
  }
</script>

<style>
.left {
  width: 600px;
  height: 100%;
  border: black 1px solid;
}
#contexts {
  width: 1142px;
  margin: 0 auto;
}
#contexts .box-card {
  position: relative;
  top: 100px;
  box-shadow: rgb(0 0 0 / 17%) 13px 15px 13px 2px;
}
.items {
  cursor: pointer;
}
.items :hover {
  -webkit-box-shadow: #ccc 0px 10px 10px;
  -moz-box-shadow: #ccc 0px 10px 10px;
  box-shadow: #ccc 0px 10px 10px;
}
.tips {
  margin-top: 10px;
}
.tip {
  margin-right: 40px;
  font-size: 15px;
}
</style>