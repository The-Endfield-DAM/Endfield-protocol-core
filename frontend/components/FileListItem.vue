<script setup lang="ts">
import { FileText, Image, Box, Download } from 'lucide-vue-next'

const props = defineProps<{
  filename: string
  mimeType: string
  size: number
  url: string
  date: string
}>()

// 格式化文件大小
const formatSize = (bytes: number) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 根据类型显示图标
const getIcon = () => {
  if (props.mimeType?.includes('image')) return Image
  if (props.mimeType?.includes('model')) return Box
  return FileText
}
</script>

<template>
  <div class="file-item">
    <div class="file-icon">
      <component :is="getIcon()" :size="20" />
    </div>
    
    <div class="file-info">
      <div class="file-name">{{ filename }}</div>
      <div class="file-meta">
        <span class="meta-tag">{{ mimeType || 'UNKNOWN' }}</span>
        <span class="meta-divider">/</span>
        <span>{{ formatSize(size) }}</span>
        <span class="meta-divider">/</span>
        <span>{{ new Date(date).toLocaleDateString() }}</span>
      </div>
    </div>

    <a :href="url" target="_blank" class="download-btn">
      <Download :size="18" />
      <span>ACCESS</span>
    </a>
  </div>
</template>