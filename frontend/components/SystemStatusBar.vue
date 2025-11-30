<script setup lang="ts">
const config = useRuntimeConfig()

interface SystemStats {
    fileCount: number
    trackCount: number
    userCount: number
    systemStatus: string
}

const { data: stats } = await useFetch<SystemStats>('/stats/', {
  baseURL: config.public.apiBase,
  lazy: true
})
</script>

<template>
  <div class="system-status-bar">
    <div class="status-item">
      <span class="indicator"></span>
      <span>SYS: ACTIVE</span>
    </div>
    <div class="status-item">
      <span>📊 Files: {{ stats?.fileCount || 0 }}</span>
    </div>
    <div class="status-item">
      <span>🎵 Tracks: {{ stats?.trackCount || 0 }}</span>
    </div>
    <div class="status-item">
      <span>👤 Operators: {{ stats?.userCount || 0 }}</span>
    </div>
  </div>
</template>