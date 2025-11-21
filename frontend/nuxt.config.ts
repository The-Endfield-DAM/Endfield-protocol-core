// 引入 Node.js 工具，用于获取绝对路径
import { fileURLToPath } from 'url'

export default defineNuxtConfig({
  devtools: { enabled: true },
  
  // 注册全局 CSS
  css: [
    // 使用 fileURLToPath 强制解析为绝对路径 (例如 D:/Project/.../variables.css)
    fileURLToPath(new URL('./assets/css/variables.css', import.meta.url)),
    fileURLToPath(new URL('./assets/css/layout.css', import.meta.url)),
    
    // ⚠️ 注意：你的截图里文件名是单数 component.css (没有s)
    // 请务必确认这里写的和左边文件栏里的名字一模一样！
    fileURLToPath(new URL('./assets/css/component.css', import.meta.url))
  ]
})