// frontend/nuxt.config.ts
import { fileURLToPath } from 'url'

export default defineNuxtConfig({
  compatibilityDate: '2025-11-21',
  devtools: { enabled: true },

  // 🔴 关键检查点：这一行必须存在！
  modules: ['@nuxtjs/supabase'],

  // Supabase 配置
  supabase: {
    redirect: false,
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
    fileURLToPath(new URL('./assets/css/login.css', import.meta.url)),
    fileURLToPath(new URL('./assets/css/dashboard.css', import.meta.url)),
    fileURLToPath(new URL('./assets/css/mobile-rotate.css', import.meta.url)),
    fileURLToPath(new URL('./assets/css/logout-modal.css', import.meta.url)),
    fileURLToPath(new URL('./assets/css/settings.css', import.meta.url)),
    fileURLToPath(new URL('./assets/css/profile-card.css', import.meta.url)),
    fileURLToPath(new URL('./assets/css/toast.css', import.meta.url)),
    fileURLToPath(new URL('./assets/css/delete-modal.css', import.meta.url)),
    fileURLToPath(new URL('./assets/css/personal-dossier.css', import.meta.url)),
    fileURLToPath(new URL('./assets/css/admin-audit.css', import.meta.url)),
    fileURLToPath(new URL('./assets/css/safety.css', import.meta.url)),
    fileURLToPath(new URL('./assets/css/play.css', import.meta.url))
  ]
})