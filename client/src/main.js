import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import hosts from "./store/hosts"

import ElementPlus  from 'element-plus'
import '../node_modules/element-plus/lib/theme-chalk/index.css'
import '../node_modules/element-plus/lib/theme-chalk/display.css'
// import 'dayjs/locale/zh-cn'
import locale from 'element-plus/lib/locale/lang/zh-cn'

import VueCodemirror from 'vue-codemirror'
import '../node_modules/codemirror/lib/codemirror.css'
// import '../../../node_modules/codemirror/keymap/sublime' //sublime编辑器效果
// import "../../../node_modules/codemirror/theme/dracula.css"// 配置里面也需要theme设置为monokai
// import "../../../node_modules/codemirror/mode/vue/vue.js" // 配置里面也需要mode设置为vue
// import '../../../node_modules/codemirror/addon/selection/active-line' //光标行背景高亮，配置里面也需要styleActiveLine设置为true

// import '../node_modules/codemirror/mode/javascript/javascript.js'
// import '../node_modules/codemirror/theme/base16-dark.css'


// locale("zh-cn")
//
const app = createApp(App)
app.config.globalProperties.$axios = axios
app.config.globalProperties.$host = hosts.host
app.use(store).use(router).use(VueCodemirror, {
    options: {
        theme: "dracula",
        mode: "vue",
        keymap: "sublime"
    }
}).use(ElementPlus, {locale}).mount('#app')

