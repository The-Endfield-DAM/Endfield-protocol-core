<script setup lang="ts">
import { FileText, Image, Box, Download, PlayCircle, Trash2, CheckSquare, Square } from 'lucide-vue-next'

const props = defineProps<{
  id: number // 🟢 新增 ID 传入，方便回传
  filename: string
  mimeType: string
  size: number
  url: string
  date: string
  selected: boolean // 🟢 新增选中状态
}>()

const emit = defineEmits(['delete', 'toggle-select']) // 🟢 新增选择事件

const formatSize = (bytes: number) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const getIcon = () => {
  if (props.mimeType?.includes('image')) return Image
  if (props.mimeType?.includes('model')) return Box
  return FileText
}

const { play, currentTrack, isPlaying } = usePlayer()

const isMedia = computed(() => props.mimeType?.startsWith('audio/') || props.mimeType?.startsWith('video/'))
const isCurrentPlaying = computed(() => isMedia.value && currentTrack.value === props.url && isPlaying.value)
</script>

<template>
  <div 
    class="file-item" 
    :class="{ 'playing': isCurrentPlaying, 'selected': selected }"
    @click="emit('toggle-select')"
  >
    
    <div class="checkbox-area">
      <div class="checkbox-icon" :class="{ 'checked': selected }">
        <CheckSquare v-if="selected" :size="20" />
        <Square v-else :size="20" />
      </div>
    </div>

    <div class="file-icon">
      <component :is="getIcon()" :size="20" />
    </div>
    
    <div class="file-info">
      <div class="file-name">{{ filename }}</div>
      <div class="file-meta">
        <span class="meta-tag">{{ mimeType || 'UNKNOWN' }}</span>
        <span class="meta-divider">/</span>
        <span>{{ formatSize(size) }}</span>
        <span class="meta-divider desktop-only">/</span>
        <span class="desktop-only">{{ new Date(date).toLocaleDateString() }}</span>
      </div>
    </div>

    <div class="actions" @click.stop>
      <button v-if="isMedia" class="action-btn play-btn" @click="play(url)">
        <PlayCircle :size="18" :fill="isCurrentPlaying ? 'var(--c-brand)' : 'none'" />
      </button>
      <a :href="url" target="_blank" class="action-btn download-btn">
        <Download :size="18" />
      </a>
      <button class="action-btn delete-btn" @click="emit('delete')">
        <Trash2 :size="18" />
      </button>
    </div>
  </div>
</template>

<style scoped>
/* 复选框样式 */
.checkbox-area {
  margin-right: 15px;
  display: flex;
  align-items: center;
  color: var(--text-sub);
  transition: color 0.2s;
}
.checkbox-icon.checked { color: var(--c-brand); }

/* 选中高亮 */
.file-item.selected {
  background: rgba(255, 215, 0, 0.08); /* 淡淡的黄色背景 */
  border-color: var(--c-brand);
}

/* ... (其他样式与 component.css 复用，此处只需补充特有的) ... */
.action-btn.delete-btn:hover {
  color: var(--c-danger); border-color: var(--c-danger); background: rgba(255, 77, 79, 0.1);
}
</style>