// frontend/nuxt.config.ts
import { fileURLToPath } from 'url'

export default defineNuxtConfig({
  compatibilityDate: '2025-11-21',
  devtools: { enabled: true },

  // 🔴 关键检查点：这一行必须存在！
  modules: ['@nuxtjs/supabase'],

  // Supabase 配置
  supabase: {
    redirect: true,
    redirectOptions: {
      login: '/login',
      callback: '/',
      exclude: [],
    }
  },

  runtimeConfig: {
    public: {
      apiBase: 'http://127.0.0.1:8000'
    }
  },
  
  css: [
    fileURLToPath(new URL('./assets/css/variables.css', import.meta.url)),
    fileURLToPath(new URL('./assets/css/layout.css', import.meta.url)),
    fileURLToPath(new URL('./assets/css/component.css', import.meta.url)),
    fileURLToPath(new URL('./assets/css/upload.css', import.meta.url)),
    fileURLToPath(new URL('./assets/css/wiki.css', import.meta.url)),
    fileURLToPath(new URL('./assets/css/login.css', import.meta.url))
  ]
})