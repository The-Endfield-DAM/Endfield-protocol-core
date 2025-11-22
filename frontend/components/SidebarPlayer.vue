<script setup lang="ts">
import { Play, Pause, Disc } from 'lucide-vue-next'

const { currentTrack, isPlaying, toggle } = usePlayer()
const audioRef = ref<HTMLAudioElement | null>(null)

// 监听播放/暂停状态
watch(isPlaying, (val) => {
  if (!audioRef.value) return
  if (val) {
    audioRef.value.play().catch(e => {
      console.warn("Play interrupted:", e)
      isPlaying.value = false
    })
  } else {
    audioRef.value.pause()
  }
})

// 监听切歌 (核心修复)
watch(currentTrack, async () => {
  if (!audioRef.value) return
  
  // 1. 等待 DOM 更新 src
  await nextTick()
  
  // 2. 强制重载音频流 (这是解决切歌不响的关键)
  audioRef.value.load()
  
  // 3. 尝试播放
  try {
    await audioRef.value.play()
    isPlaying.value = true
  } catch (e) {
    console.warn("Autoplay blocked:", e)
    isPlaying.value = false
  }
})

// 初始化
onMounted(() => {
  if (audioRef.value) {
    audioRef.value.volume = 0.4
  }
})
</script>

<template>
  <div class="mini-player">
    <audio ref="audioRef" :src="currentTrack || ''" loop></audio>

    <div class="player-info">
      <div class="disk-icon" :class="{ spinning: isPlaying }">
        <Disc :size="18" />
      </div>
      <div class="track-status">
        <span class="label">Enjoy Music</span>
        <span class="status">{{ isPlaying ? 'PLAYING' : 'STANDBY' }}</span>
      </div>
    </div>

    <button class="control-btn" @click="toggle">
      <Pause v-if="isPlaying" :size="16" fill="currentColor" />
      <Play v-else :size="16" fill="currentColor" />
    </button>
  </div>
</template>