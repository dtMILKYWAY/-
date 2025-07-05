import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

const app = createApp(App)
const pinia = createPinia() // 创建 Pinia 实例

app.use(router)
app.use(pinia) // 使用 Pinia

app.mount('#app')