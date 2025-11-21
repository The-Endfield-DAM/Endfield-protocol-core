// 引入 Node.js 工具，用于获取绝对路径
import { fileURLToPath } from 'url'

export default defineNuxtConfig({
  compatibilityDate: '2025-11-21',
  devtools: { enabled: true },

  runtimeConfig: {
    public: {
      // 默认值是本地后端，部署时我们在后台改这个变量覆盖它
      apiBase: 'http://127.0.0.1:8000'
    }
  },
  
  // 注册全局 CSS
  css: [
    // 使用 fileURLToPath 强制解析为绝对路径 (例如 D:/Project/.../variables.css)
    fileURLToPath(new URL('./assets/css/variables.css', import.meta.url)),
    fileURLToPath(new URL('./assets/css/layout.css', import.meta.url)),
    fileURLToPath(new URL('./assets/css/component.css', import.meta.url)),
    fileURLToPath(new URL('./assets/css/upload.css', import.meta.url)),
    fileURLToPath(new URL('./assets/css/wiki.css', import.meta.url))
  ]
})