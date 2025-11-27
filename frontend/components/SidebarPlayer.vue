<script setup lang="ts">
import { Play, Pause, Disc } from 'lucide-vue-next'

const { 
  currentTrack, currentTrackObj, isPlaying, toggle, next, 
  currentTime, duration, isSeeking 
} = usePlayer()

const audioRef = ref<HTMLAudioElement | null>(null)

// 播放状态同步
watch(isPlaying, (val) => {
  if (!audioRef.value) return
  val ? audioRef.value.play().catch(() => isPlaying.value = false) : audioRef.value.pause()
})

// 切歌同步
watch(currentTrack, async () => {
  if (!audioRef.value) return
  await nextTick()
  audioRef.value.load()
  if (isPlaying.value) audioRef.value.play().catch(() => {})
})

// 🟢 进度条拖拽同步 (当用户在 /play 页面拖动时，这里执行跳转)
watch(currentTime, (newTime) => {
  // 只有当 isSeeking 为 true (正在拖拽中) 或者 偏差较大时才强制设置 currentTime
  // 避免由 timeupdate 事件引发的死循环
  if (audioRef.value && Math.abs(audioRef.value.currentTime - newTime) > 1) {
    audioRef.value.currentTime = newTime
  }
})

const onEnded = () => next()

// 🟢 新增：更新时间到全局状态
const onTimeUpdate = () => {
  if (audioRef.value && !isSeeking.value) {
    currentTime.value = audioRef.value.currentTime
  }
}

const onLoadedMetadata = () => {
  if (audioRef.value) {
    duration.value = audioRef.value.duration
  }
}

onMounted(() => {
  if (audioRef.value) audioRef.value.volume = 0.4
})

const openFullPlayer = () => navigateTo('/play')
</script>

<template>
  <div class="mini-player" @click="openFullPlayer" title="Open Music Terminal">
    
    <audio 
      ref="audioRef" 
      :src="currentTrack || ''" 
      @ended="onEnded"
      @timeupdate="onTimeUpdate"
      @loadedmetadata="onLoadedMetadata"
    ></audio>

    <div class="player-info">
      <div class="disk-icon" :class="{ spinning: isPlaying }">
        <Disc :size="18" />
      </div>
      <div class="track-status">
        <span class="label">{{ currentTrackObj.artist || 'Unknown Artist' }}</span>
        <span class="status">{{ currentTrackObj.title || 'BGM' }}</span>
      </div>
    </div>

    <button class="control-btn" @click.stop="toggle">
      <Pause v-if="isPlaying" :size="16" fill="currentColor" />
      <Play v-else :size="16" fill="currentColor" />
    </button>
  </div>
</template>