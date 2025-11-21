<script setup lang="ts">
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
const { data: files, pending, refresh } = await useFetch<FileRecord[]>('/files/', {
  baseURL: config.public.apiBase
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