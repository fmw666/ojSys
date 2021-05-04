<template>
  <div id="CodeMirror" style="margin: 0 0 15px 0">
    <div class="header" style="justify-content: space-between;">
      <div>
        <span>Language</span>
        <el-select class="adjust" v-model="language" @change="onLangChange" placeholder="请选择">
          <el-option
            v-for="item in languages"
            :key="item"
            :label="item"
            :value="item">
          </el-option>
        </el-select>

        <el-button style="margin-left: 10px" @click="onResetClick" type="primary" icon="el-icon-refresh-right"></el-button>

      </div>

      <div>
        <span>Theme:</span>
        <el-select v-model="theme" @change="onThemeChange" placeholder="请选择">
          <el-option
            v-for="item in themes"
            :key="item.label"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>

      </div>
    </div>
<!--    <codemirror :value="value" :options="options" @change="onEditorCodeChange" ref="myEditor">-->
<!--    </codemirror>-->
    <codemirror v-model="code" :options="options"></codemirror>
  </div>
</template>


<script>
import {codemirror} from 'vue-codemirror'
import 'codemirror/lib/codemirror.css'
import 'codemirror/keymap/sublime' //sublime编辑器效果
import "codemirror/theme/dracula.css"// 配置里面也需要theme设置为monokai
import "codemirror/mode/vue/vue.js" // 配置里面也需要mode设置为vue
import 'codemirror/addon/selection/active-line' //光标行背景高亮，配置里面也需要styleActiveLine设置为true

export default {
  name: 'CodeMirror',
  components: {
    codemirror
  },
  props: {
    value: {
      type: String,
      default: ''
    },
    languages: {
      type: Array,
      default: () => {
        return ['C', 'C++', 'Java', 'Python3']
      }
    },
    language: {
      type: String,
      default: 'C++'
    },
    theme: {
      type: String,
      default: 'solarized'
    }
  },
  data () {
    return {
      options: {
        tabSize: 4,    // tab的空格个数
        theme: 'solarized',    //主题样式dracula
        lineNumbers: true,    //是否显示行数
        lineWrapping: true,     //是否自动换行
        styleActiveLine: true,    //line选择是是否加亮
        matchBrackets: true,    //括号匹配
        mode: "text/x-csrc",  //实现javascript代码高亮
        readOnly: false,  //只读

        // codemirror options
        line: true,
        // 代码折叠
        foldGutter: true,
        gutters: ['CodeMirror-linenumbers', 'CodeMirror-foldgutter'],
        // 选中文本自动高亮，及高亮方式
        styleSelectedText: true,
        highlightSelectionMatches: {showToken: /\w/, annotateScrollbar: true}
      },
      mode: {
        'C++': 'text/x-csrc'
      },
      themes: [
        {label: 'm.Monokai', value: 'monokai'},
        {label: 'm.Solarized_Light', value: 'solarized'},
        {label: 'm.Material', value: 'material'}
      ]
    }
  },
  mounted () {

    this.mode = mode
    this.editor.setOption('mode', this.mode[this.language])

    this.editor.focus()
  },
  methods: {
    onEditorCodeChange (newCode) {
      this.$emit('update:value', newCode)
    },
    onLangChange (newVal) {
      this.editor.setOption('mode', this.mode[newVal])
      this.$emit('changeLang', newVal)
    },
    onThemeChange (newTheme) {
      this.editor.setOption('theme', newTheme)
      this.$emit('changeTheme', newTheme)
    },
    onResetClick () {
      this.$emit('resetCode')
    },

  },
  computed: {
    editor () {
      // get current editor object
      return this.$refs.myEditor.editor
    }
  },
  watch: {
    'theme' (newVal, oldVal) {
      this.editor.setOption('theme', newVal)
    }
  }
}
</script>

<style>
  .CodeMirror {
    height: auto !important;
  }
  .CodeMirror-scroll {
    min-height: 300px;
    max-height: 1000px;
  }
</style>