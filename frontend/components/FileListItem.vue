<script setup lang="ts">
import { FileText, Image, Box, Download, PlayCircle } from 'lucide-vue-next'

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

const { play, currentTrack, isPlaying } = usePlayer()

// 判断是否为媒体文件
const isMedia = computed(() => {
  return props.mimeType?.startsWith('audio/') || props.mimeType?.startsWith('video/')
})

// 判断是否正在播放当前文件
const isCurrentPlaying = computed(() => {
  return isMedia.value && currentTrack.value === props.url && isPlaying.value
})
</script>

<template>
  <div class="file-item" :class="{ 'playing': isCurrentPlaying }">
    
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

    <div class="actions">
      <button 
        v-if="isMedia" 
        class="action-btn play-btn" 
        @click="play(url)"
        :title="isCurrentPlaying ? 'Pause' : 'Play BGM'"
      >
        <PlayCircle :size="18" :fill="isCurrentPlaying ? 'var(--c-brand)' : 'none'" />
      </button>

      <a :href="url" target="_blank" class="action-btn download-btn">
        <Download :size="18" />
        <span>ACCESS</span>
      </a>
    </div>
  </div>
</template>