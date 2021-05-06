<template>
  <div id="problems">
    <div class="container">

      <el-card>
        <div>
          <div class="tag-group">
            <span class="tag-group__title">算法&emsp;&emsp;</span>
            <el-tag
              v-for="item in algs"
              :key="item.label"
              :type="item.type"
              effect="light"
              class="tag_class alg"
              @click="get_problems_with_tag('alg', item.label)">
              {{ item.label }}
            </el-tag>
          </div>
          <div class="tag-group">
            <span class="tag-group__title">数据结构</span>
            <el-tag
              v-for="item in ds"
              :key="item.label"
              :type="item.type"
              class="tag_class ds"
              @click="get_problems_with_tag('ds', item.label)"
              effect="light">
              {{ item.label }}
            </el-tag>
          </div>
          <div class="tag-group">
            <span class="tag-group__title">企业&emsp;&emsp;</span>
            <el-tag
              v-for="item in firms"
              :key="item.label"
              :type="item.type"
              class="tag_class firm"
              @click="get_problems_with_tag('firm', item.label)"
              effect="light">
              {{ item.label }}
            </el-tag>
          </div>
          <div class="tag-group">
            <span class="tag-group__title">难度&emsp;&emsp;</span>
            <el-tag
              v-for="item in header"
              :key="item.label"
              :type="item.type"
              class="tag_class header"
              @click="get_problems_with_tag('header', item.label)"
              effect="light">
              {{ item.label }}
            </el-tag>
          </div>
        </div>
      </el-card>

      <el-card class="box-card">
        <div class="sort_bar">
          <span v-if="id_sort">
            <span class="demonstration order_tag" @click="on_sort('-id')" :class="ordering==='id'?'active':''">序号<i class="el-icon-arrow-down el-icon--right"></i></span>
          </span>
          <span v-else>
              <span class="demonstration order_tag" @click="on_sort('id')" :class="ordering==='id'?'active':''">序号<i class="el-icon-arrow-up el-icon--right"></i></span>
          </span>
          <el-divider direction="vertical" style="margin: 0 20px"></el-divider>
          <span v-if="header_sort">
            <span class="demonstration order_tag" @click="on_sort('-header')" :class="ordering==='header'?'active':''">难度<i class="el-icon-arrow-down el-icon--right"></i></span>
          </span>
          <span v-else>
            <span class="demonstration order_tag" @click="on_sort('header')" :class="ordering==='header'?'active':''">难度<i class="el-icon-arrow-up el-icon--right"></i></span>
          </span>

          <el-tag style="float: right; margin-top: -4px; background-color: white; cursor: pointer">题目总数：{{total_problem_cnt}}</el-tag>
        </div>

        <el-divider style="width: 160px; margin: 15px 0"></el-divider>

        <transition-group>
          <el-card v-if="count > 0" v-for="problem in problems" :key="problem.id" @click="to_path('/problems/' + problem.id)" class="items" shadow="hover">
            <h4 style="display: inline">{{ problem.id + ". " + problem.name }}</h4>
            <span class="headers">{{ problem.header }}</span>
            <div class="tips">
              <span class="tip">算法类型：{{ problem.alg_type }}</span>
              <span class="tip">数据结构：{{ problem.ds_type }}</span>
            </div>
          </el-card>
        </transition-group>
        <el-card v-if="count === 0" @click="reset_query" style="margin: 30px 0; font-size: 14px; cursor: pointer">没有数据，点击重置全部查询条件</el-card>

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
      </el-card>
      <el-card class="ranting">
        AC 排行榜
        <br>
        排名|用户名|通过数
        <br>
        <a>登录</a>后查看我的排名
      </el-card>
    </div>

    <el-backtop :visibility-height="0"></el-backtop>

  </div>
</template>

<script>
import {Base} from '../components/mixins'
import {ElMessage} from "element-plus";

export default {
  mixins: [Base],
  data() {
    return {
      page: 1,  // 当前页数
      page_size: 10,  // 每页数量
      ordering: 'id',  // 排序
      id_sort: true,  // true 代表顺序，false 代表反序
      header_sort: true, // true 代表顺序，false 代表反序
      count: 0,  // 总数量
      problems: [],  // 数据
      total_problems: [], // 所有数据，用于展示每个 tag 数目

      algs: [
        { type: 'info', label: '基础'},
        { type: 'success', label: '贪心算法'},
        { type: '', label: 'DFS/BFS'},
        { type: 'success', label: '动态规划'},
        { type: 'warning', label: '二分法'},
        { type: '', label: '最短路径算法'}
      ],

      ds: [
        { type: 'info', label: '基础'},
        { type: 'success', label: '数组'},
        { type: '', label: '链表'},
        { type: 'success', label: '栈'},
        { type: 'warning', label: '队列'},
        { type: '', label: '哈希表'},
        { type: 'warning', label: '树'},
        { type: 'success', label: '图'},
      ],

      firms: [
        { type: '', label: '浙江大学'},
        { type: 'success', label: '阿里巴巴集团'},
      ],

      header: [
        { type: 'info', label: '入门'},
        { type: 'success', label: '简单'},
        { type: '', label: '中等'},
        { type: 'warning', label: '困难'},
        { type: 'danger', label: '特难'},
      ],

      alg_choose: '', // 选中的名称
      ds_choose: '',
      firm_choose: '',
      header_choose: '',
    };
  },
  watch: {
    count: {
      handler(old_val, new_val) {
        if (this.count === 0) {
          this.tips_msg = ElMessage({
            message: '当前没有查询到匹配记录',
            duration: 0,
            type: 'info'
          })
        } else {
          this.tips_msg ? this.tips_msg.close() : ''
        }
      }
    }
  },
  methods: {
    // 选择算法标签
    get_problems_with_tag(type, tag) {
      let i;
      let elements = document.getElementsByClassName(type)
      // 循环所有标签，找到选中下标，和之前选择到的下标
      let index_now;
      let index_old = -1;
      for (i=0; i<elements.length; i++) {
        if (elements[i].className.indexOf('el-tag--dark') !== -1) {
          index_old = i
        }
        if (elements[i].innerHTML.replace('<!--v-if-->', '') === tag) {
          index_now = i
        }
      }

      // 如果选中的标签，之前就是被选择的那个，则重置自己的样式，然后全部重新获取
      if (index_now === index_old) {
        elements[index_now].classList.add('el-tag--light')
        elements[index_now].classList.remove('el-tag--dark')
        if (type === 'alg') {
          this.alg_choose = ''
        } else if (type === 'ds') {
          this.ds_choose = ''
        } else if (type === 'firm') {
          this.firm_choose = ''
        } else if (type === 'header') {
          this.header_choose = ''
        }
        this.get_problems()
        return;
      }
      // 更新现在的
      elements[index_now].classList.add('el-tag--dark')
      elements[index_now].classList.remove('el-tag--light')

      // 如果之前的没有选择过，flag 变为 现在的名称
      if (index_old === -1) {
        elements[index_now].classList.add('el-tag--dark')
        elements[index_now].classList.remove('el-tag--light')
      } else {
        // 之前的选择了，则重置以前的
        elements[index_old].classList.add('el-tag--light')
        elements[index_old].classList.remove('el-tag--dark')
      }
      // choose 改为现在的 名称
      let reg = RegExp(' · ')
      let str = elements[index_now].innerHTML.replace('<!--v-if-->', '')
      if (type === 'alg') {
        this.alg_choose = str.substr(0, reg.exec(str).index)
      } else if (type === 'ds') {
        this.ds_choose =  str.substr(0, reg.exec(str).index)
      } else if (type === 'firm') {
        this.firm_choose =  str
      } else if (type === 'header') {
        this.header_choose =  str.substr(0, reg.exec(str).index)
      }
      // 获取数据
      this.get_problems()
    },
    // 重置查询
    reset_query() {
      this.alg_choose = ''
      this.ds_choose = ''
      this.firm_choose = ''
      this.header_choose = ''
      let i;
      let elements = document.getElementsByClassName('el-tag')
      for (i=0; i<elements.length; i++) {
        elements.item(i).classList.add('el-tag--light')
        elements.item(i).classList.remove('el-tag--dark')
      }
      this.get_problems()
    },
    // 切换每页多少数据
    handleSizeChange(val) {
      this.page_size = val;
      this.get_problems()
    },
    // 点击页数，切换到相应页
    handleCurrentChange(val) {
      this.page = val;
      this.get_problems()
    },
    get_problems() {
      this.$axios.get(this.$host + "/api/v1/problems/", {
        params: {
          page: this.page,
          page_size: this.page_size,
          ordering: this.ordering,
          alg: this.alg_choose,
          ds: this.ds_choose,
          firm: this.firm_choose,
          header: this.header_choose
        },
        responseType: 'json'
      }).then(response => {
        this.count = response.data.count
        this.problems = response.data.results
      }).catch(error => {
        console.log(error.response.data)
      })
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
    },
    // 得到总的 problems
    get_total_problems() {
      // 先获取数据
      this.$axios.get(this.$host + "/api/v1/problems/", {
        params: {
          page_size: Number.MAX_SAFE_INTEGER,
        },
        responseType: 'json'
      }).then(response => {
        this.total_problems = response.data.results
        this.set_values()
      }).catch(error => {
        console.log(error.response.data)
      })

    },
    // 给每个 tag 设置值
    set_values() {
      let i;
      let lens = this.total_problems.length
      let alg_cnts = {'基础':0,'贪心算法':0,'DFS/BFS':0,'动态规划':0,'二分法':0,'最短路径算法':0}
      let ds_cnts = {'基础':0,'数组':0,'链表':0,'栈':0,'队列':0,'哈希表':0,'树':0,'图':0}
      let header_cnts = {'入门':0,'简单':0,'中等':0,'困难':0,'特难':0}
      for (i=0; i<lens; i++) {
        alg_cnts[this.total_problems[i].alg_type] += 1
        ds_cnts[this.total_problems[i].ds_type] += 1
        header_cnts[this.total_problems[i].header] += 1
      }

      for (i=0; i<this.algs.length; i++) {
        this.algs[i]["label"] = this.algs[i]["label"] + ' · ' + alg_cnts[this.algs[i]["label"]]
      }
      for (i=0; i<this.ds.length; i++) {
        this.ds[i]["label"] = this.ds[i]["label"] + ' · ' + ds_cnts[this.ds[i]["label"]]
      }
      for (i=0; i<this.header.length; i++) {
        this.header[i]["label"] = this.header[i]["label"] + ' · ' + header_cnts[this.header[i]["label"]]
      }
    },
  },
  computed: {

  },
  mounted() {
    this.get_problems();

    this.get_total_problems();
  },
  created() {
  }
}
</script>

<style scoped>

.container {
  /*width: 1142px;*/
  width: 66vw;
  margin: 0 auto;
  padding-top: 110px;
}

.container .box-card,
.container .ranting {
  margin-top: 20px;
  display: inline-block;
  box-shadow: rgba(0 0 0 .17) 13px 15px 13px 2px;
}

.container .box-card {
  width: 60%;
}

.container .ranting {
  width: 35%;
  float: right;
}

.tag-group__title {
  margin-right: 14px;
  margin-left: 10px;
}

.tag_class {
  margin: 6px 6px 10px 12px;
  cursor: pointer;
  user-select: none;
}


.sort_bar {
  margin: 3px 0 0 10px;
}

.items {
  cursor: pointer;
  margin: 10px 0;
}

.items ::v-deep(.el-card) > .el-card__body {
  padding: 12px 0 12px 20px;
}

.order_tag {
  cursor: pointer;
  user-select: none;
  font-size: 15px;
}

.headers {
  margin-left: 30px;
  font-size: 13px;
}

.tips {
  margin-top: 10px;
}

.tip {
  margin-right: 40px;
  font-size: 14px;
}

.pagination {
  margin: 20px 0 0 10px;
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
    transition: all 0.6s ease;
}
/*v-move 和 v-leave-active 配合使用，能够实现列表后续的元素，渐渐地漂上来的效果 */

.v-move{
    transition: all 0.6s ease;
}
.v-leave-active{
    position: absolute;
}
</style>