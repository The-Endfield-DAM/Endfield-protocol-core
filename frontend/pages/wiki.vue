<script setup lang="ts">
// 🟢 必须加上 lang="ts"，否则无法识别 <FileRecord[]> 泛型语法！

// 引入 Session 钩子，用于获取 Token
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

// 获取数据 (整合了鉴权和懒加载)
const { data: files, pending, refresh, error } = await useFetch<FileRecord[]>('/files/', {
  baseURL: config.public.apiBase,
  // 注入 Token
  headers: computed(() => ({
    Authorization: `Bearer ${session.value?.access_token}`
  })) as any,
  // 监听 Session 变化自动刷新
  watch: [session],
  
  // 开启懒加载，防止页面卡死
  lazy: true,
  timeout: 60000
})

// 错误监控
watch(error, (newErr) => {
  if (newErr) {
    console.error('Wiki 数据加载失败:', newErr)
  }
})
</script>

<template>
  <div class="wiki-page">
    <div class="page-header">
      <div class="header-title">
        <h1>ARCHIVE_DATABASE</h1>
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