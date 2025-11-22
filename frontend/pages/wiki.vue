<script setup lang="ts">
// 🟢 必须加上 lang="ts"

// 引入 Session 钩子
const session = useSupabaseSession()
const config = useRuntimeConfig()

// 定义接口类型
interface FileRecord {
  id: number
  filename: string
  mime_type: string
  size: number
  url: string
  created_at: string
}

// 获取数据
const { data: files, pending, refresh, error } = await useFetch<FileRecord[]>('/files/', {
  baseURL: config.public.apiBase,
  
  // 🟢 修复核心 1：使用 onRequest 动态注入 Token
  // 这比 headers: computed(...) 更稳定，确保在请求发出的那一刻拿到最新的 Token
  onRequest({ options }) {
    const token = session.value?.access_token
    if (token) {
      options.headers = {
        ...options.headers,
        Authorization: `Bearer ${token}`
      }
    }
  },
  
  // 监听 Session 变化自动刷新 (例如 Token 刷新时)
  watch: [session],
  
  // 🟢 修复核心 2：关闭服务端渲染请求
  // 既然是鉴权接口，完全交给客户端处理，彻底解决 401/403 和水合不匹配问题
  server: false,
  
  // 懒加载，不阻塞页面显示
  lazy: true,
  
  // 增加超时时间 (防止冷启动超时)
  timeout: 60000
})

// 错误监控
watch(error, (newErr) => {
  if (newErr) {
    console.error('Wiki 数据加载异常:', newErr)
    if (newErr.statusCode === 403) {
      // 权限不足时的静默处理或提示
      console.warn('ACCESS DENIED // 请检查登录状态')
    }
  }
})
</script>

<template>
  <div class="wiki-page">
    <div class="page-header">
      <div class="header-title">
        <h1>DATABASE</h1>
        <div class="subtitle">// 协议档案库</div>
      </div>
      <button class="refresh-btn" @click="refresh()">
        REFRESH_SIGNAL
      </button>
    </div>

    <div v-if="pending" class="loading-state">
      [ CONNECTING TO NEURAL NETWORK... ]
    </div>

    <div v-else-if="!files || files.length === 0" class="empty-state">
      [ NO DATA ENTRIES FOUND ]
    </div>

    <div v-else class="file-list">
      <FileListItem
        v-for="file in files"
        :key="file.id"
        :filename="file.filename"
        :mimeType="file.mime_type"
        :size="file.size"
        :url="file.url"
        :date="file.created_at"
      />
    </div>
  </div>
</template>