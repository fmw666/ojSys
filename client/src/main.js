import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import hosts from "./store/hosts"

import ElementPlus from 'element-plus'
import '../node_modules/element-plus/lib/theme-chalk/index.css'
import '../node_modules/element-plus/lib/theme-chalk/display.css'
// import '../node_modules/dayjs/locale/zh-cn'
// import locale from '../node_modules/element-plus/lib/locale/lang/zh-cn'


const app = createApp(App)
app.config.globalProperties.$axios = axios
app.config.globalProperties.$host = hosts.host
app.use(store).use(router).use(ElementPlus).mount('#app')
