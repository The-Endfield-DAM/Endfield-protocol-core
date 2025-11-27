<script setup lang="ts">
import { FileText, Image, Box, Download, PlayCircle, Trash2, CheckSquare, Square } from 'lucide-vue-next'

const props = defineProps<{
  id: number
  filename: string
  mimeType: string
  size: number
  url: string
  date: string
  selected: boolean
  // 🟢 新增：接收音乐专属元数据
  artist?: string
  coverUrl?: string
  lyricUrl?: string
}>()

const emit = defineEmits(['delete', 'toggle-select'])

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

// 仅允许音频文件显示播放按钮
const isMedia = computed(() => props.mimeType?.startsWith('audio/'))
const isCurrentPlaying = computed(() => isMedia.value && currentTrack.value === props.url && isPlaying.value)

// 🟢 核心修改：构造包含完整元数据的 Track 对象并播放
const handlePlay = () => {
  play({
    id: props.id,
    title: props.filename,
    artist: props.artist || 'Unknown Operator', // 使用传入的歌手名
    url: props.url,
    mimeType: props.mimeType,
    cover: props.coverUrl, // 传入封面链接
    // @ts-ignore: 临时扩展字段，确保 usePlayer 能存 (需确保 usePlayer.ts 的 Track 接口已更新或忽略类型检查)
    lyrics: props.lyricUrl 
  })
}
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
      <img v-if="coverUrl" :src="coverUrl" class="file-thumb" alt="cover" />
      <component v-else :is="getIcon()" :size="20" />
    </div>
    
    <div class="file-info">
      <div class="file-name">{{ filename }}</div>
      <div class="file-meta">
        <span v-if="artist" class="meta-tag artist">{{ artist }}</span>
        <span v-if="artist" class="meta-divider">/</span>

        <span class="meta-tag">{{ mimeType || 'UNKNOWN' }}</span>
        <span class="meta-divider">/</span>
        <span>{{ formatSize(size) }}</span>
        <span class="meta-divider desktop-only">/</span>
        <span class="desktop-only">{{ new Date(date).toLocaleDateString() }}</span>
      </div>
    </div>

    <div class="actions" @click.stop>
      <button v-if="isMedia" class="action-btn play-btn" @click="handlePlay">
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
.checkbox-area {
  margin-right: 15px;
  display: flex;
  align-items: center;
  color: var(--text-sub);
  transition: color 0.2s;
}
.checkbox-icon.checked { color: var(--c-brand); }

.file-item.selected {
  background: rgba(255, 215, 0, 0.08);
  border-color: var(--c-brand);
}

.action-btn.delete-btn:hover {
  color: var(--c-danger); border-color: var(--c-danger); background: rgba(255, 77, 79, 0.1);
}

/* 🟢 新增样式 */
.file-thumb {
  width: 32px; height: 32px; object-fit: cover; border-radius: 2px; border: 1px solid var(--border-light);
}
.artist {
  color: var(--c-brand); font-weight: bold;
}
</style>