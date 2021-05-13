<template>
<div id="ProblemList">
  <div class="container">
    <el-card>
      <div class="title">题库管理中心</div>

      <div class="content">
        <el-row :gutter="20" style="font-weight: bold; color: #505458">
          <el-col :span="2">序号</el-col>
          <el-col :span="6">题目名称</el-col>
          <el-col :span="4">报名时间</el-col>
          <el-col :span="4">比赛时间</el-col>
          <el-col :span="4">状态</el-col>
          <el-col :span="4">题目</el-col>
        </el-row>
        <el-divider style="margin: 10px 0 10px 0"></el-divider>

        <el-row v-for="(contest, index) in contests" :gutter="20">
          <el-col :span="2">{{index + 1}}</el-col>
          <el-col :span="6">{{contest['name']}}</el-col>
          <el-col :span="4">
            {{contest['sign_up_start_date'].replace('年', '-').replace('月', '-').replace('日', '')}}
            <br>
            --
            <br>
            {{contest['sign_up_end_date'].replace('年', '-').replace('月', '-').replace('日', '')}}
          </el-col>
          <el-col :span="4">
            {{contest['contest_start_date'].replace('年', '-').replace('月', '-').replace('日', '')}}
            <br>
            --
            <br>
            {{contest['contest_end_date'].replace('年', '-').replace('月', '-').replace('日', '')}}
          </el-col>
          <el-col :span="4">
            <el-tag v-if="contest['is_no']">未开始</el-tag>
            <el-tag v-if="contest['is_sign']">报名中</el-tag>
            <el-tag v-if="contest['is_wait']">等待中</el-tag>
            <el-tag v-if="contest['is_start']">已开始</el-tag>
            <el-tag v-if="contest['is_end']">已结束</el-tag>
          </el-col>
          <el-col :span="4">
<!--            <div v-for="p in contest['problems']">-->
<!--              {{p}}-->
<!--            </div>-->
          </el-col>
          <el-divider style="margin: 10px 0 10px 0"></el-divider>
        </el-row>
      </div>
    </el-card>
  </div>
</div>
</template>

<script>
export default {
  name: "ProblemList"
}
</script>

<style scoped>
.title {
  color: #3091f2;
  font-size: 18px;
  font-weight: bold;
  margin: 10px 0 20px 20px;
}

.content {
  margin: 40px 0 0 20px;
}
</style>