<template>
<div id="test">

  <div class="container">

    <el-card>

<!--      <span>Language</span>-->
<!--      <el-select class="adjust" v-model="language" @change="onLangChange" placeholder="请选择">-->
<!--        <el-option-->
<!--          v-for="item in languages"-->
<!--          :key="item"-->
<!--          :label="item"-->
<!--          :value="item">-->
<!--        </el-option>-->
<!--      </el-select>-->

<!--      <el-button style="margin-left: 10px" @click="onResetClick" type="primary" icon="el-icon-refresh-right"></el-button>-->

<!--      <span>Theme:</span>-->
<!--      <el-select v-model="theme" @change="onThemeChange" placeholder="请选择">-->
<!--        <el-option-->
<!--          v-for="item in themes"-->
<!--          :key="item.label"-->
<!--          :label="item.label"-->
<!--          :value="item.value">-->
<!--        </el-option>-->
<!--      </el-select>-->

<!--    <codemirror :value="value" :options="options" @change="onEditorCodeChange" ref="myEditor">-->
<!--    </codemirror>-->

      <codemirror v-model="code" :options="cmOptions" />

    </el-card>
  </div>

</div>
</template>

<script>
export default {
  components: {
  },
  name: "test",
  data() {
    return {
      code: 'const a = 10',
      cmOptions: {
        tabSize: 4,
        mode: 'text/javascript',
        theme: 'base16-dark',
        lineNumbers: true,
        line: true,
        // more CodeMirror options...
      }
    }
  },
  methods: {
    onCmReady3() {
      this.$refs.myCmGenerate.codemirror.setSize('400px', '400px')
    },
    onCmFocus(instance, event) {
      console.log(instance)
      console.log(event)
    },
    onCmCodeChange(instance, obj) {
      console.log(instance)
      console.log(obj)
    }
  },
  computed: {
    codemirror() {
      return this.$refs.cmEditor.codemirror
    }
  },
  mounted() {
    console.log('the current CodeMirror instance object:', this.codemirror)
    // you can use this.codemirror to do something...
  }
}
</script>

<style scoped>

</style>