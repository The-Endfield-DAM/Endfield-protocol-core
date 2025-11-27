<script setup lang="ts">
import { 
  Play, Pause, SkipBack, SkipForward, UploadCloud, 
  Music, Type, Languages, Repeat, Shuffle, List 
} from 'lucide-vue-next'
// 🟢 引入解析器 (确保 frontend/utils/lrcParser.ts 存在)
import { parseLrc, type LyricLine } from '~/utils/lrcParser'

const { 
  currentTrackObj, isPlaying, toggle, next, prev, playlist, playList,
  currentIndex, // 需要直接操作 index
  currentTime, duration, isSeeking, seek, playMode, toggleMode
} = usePlayer()

const config = useRuntimeConfig()
const session = useSupabaseSession()
const { success, error: showError } = useToast()

// --- 歌词核心逻辑 ---
const lyricsData = ref<LyricLine[]>([])   // 结构化歌词数据
const currentLineIndex = ref(-1)          // 当前高亮行
const lyricsContainerRef = ref<HTMLElement | null>(null) // 滚动容器
const showTranslation = ref(true)         // 翻译开关

// --- 播放列表与云端库逻辑 ---
const showPlaylist = ref(false)           // 列表显示开关
let refreshTimer: any = null

// 🟢 加载云端曲库 (支持静默刷新)
const loadCloudLibrary = async (silent = false) => {
  const token = session.value?.access_token
  
  const { data, error } = await useFetch<any[]>('/files/', {
    baseURL: config.public.apiBase,
    query: { mime_type_prefix: 'audio/' },
    headers: token ? { Authorization: `Bearer ${token}` } : {}
  })

  if (error.value) {
    if (!silent) showError('FAILED TO LOAD LIBRARY // 加载失败')
    return
  }
  
  if (data.value && data.value.length > 0) {
    const newTracks = data.value.map(f => ({
      id: f.id,
      title: f.filename.replace(/\.[^/.]+$/, ""), // 去掉扩展名
      artist: f.artist || 'Unknown Artist',
      url: f.url,
      cover: f.cover_r2_key,
      lyrics: f.lyrics_r2_key
    }))

    // 🟢 核心优化：无缝更新列表 (解决 R2 过期问题)
    // 如果当前已经在播放列表中的歌，我们需要保持播放状态，只更新 URL
    if (playlist.value.length > 1) {
      const currentId = currentTrackObj.value.id
      playlist.value = newTracks
      
      // 修正 currentIndex，防止切歌
      const newIndex = newTracks.findIndex(t => t.id === currentId)
      if (newIndex !== -1) {
        currentIndex.value = newIndex
      } else {
        // 如果当前歌被删了，重置到 0 (或者暂停)
        currentIndex.value = 0
      }
      // 注意：这里不调用 playList()，也不重置 isPlaying
      if (!silent) success(`LIBRARY REFRESHED // URL UPDATED`)
    } else {
      // 首次加载或单曲模式，直接覆盖
      playlist.value = newTracks
      currentIndex.value = 0
      if (!silent) success(`LIBRARY LOADED // ${newTracks.length} TRACKS`)
    }

    // 🟢 启动/重置定时器 (50分钟刷新一次)
    if (refreshTimer) clearInterval(refreshTimer)
    refreshTimer = setInterval(() => loadCloudLibrary(true), 50 * 60 * 1000)

  } else {
    if (!silent) showError('NO AUDIO FILES FOUND // 未找到音频文件')
  }
}

// 切换列表显示
const togglePlaylist = () => {
  showPlaylist.value = !showPlaylist.value
}

// 组件销毁时清理定时器
onUnmounted(() => {
  if (refreshTimer) clearInterval(refreshTimer)
})

// 组件挂载时自动加载云端R2数据库文件
onMounted(() => {
  loadCloudLibrary(true) //静默加载列表
  showPlaylist.value = false //确保列表默认关闭
})

// 1. 切歌时：加载并解析歌词
watch(() => currentTrackObj.value, async (newTrack) => {
  // 重置状态
  lyricsData.value = []
  currentLineIndex.value = -1
  
  // @ts-ignore
  const lyricUrl = newTrack.lyrics || newTrack.lyrics_r2_key
  
  if (lyricUrl && lyricUrl.startsWith('http')) {
    try {
      // 获取文本
      const text = await $fetch<string>(lyricUrl)
      // 🟢 解析为对象数组
      lyricsData.value = parseLrc(text)
    } catch (e) {
      // 构造一个伪造的错误行
      lyricsData.value = [{ time: 0, text: '[LYRICS LOAD ERROR]' }]
    }
  } else {
    lyricsData.value = [{ time: 0, text: '[NO LYRICS AVAILABLE]' }]
  }
}, { immediate: true })

// 2. 播放时：实时计算高亮行 & 滚动
watch(currentTime, (time) => {
  // 如果正在拖拽进度条，或者是空歌词，不滚动
  if (isSeeking.value || lyricsData.value.length === 0) return

  // 查找当前时间对应的最后一行
  const index = lyricsData.value.findIndex((line, i) => {
    const nextLine = lyricsData.value[i + 1]
    // 当前时间 >= 行时间 且 (下一行不存在 或 当前时间 < 下一行时间)
    return time >= line.time && (!nextLine || time < nextLine.time)
  })

  if (index !== -1 && index !== currentLineIndex.value) {
    currentLineIndex.value = index
    scrollToActiveLine()
  }
})

// 3. 滚动实现 (保持高亮行在中间)
const scrollToActiveLine = () => {
  if (!lyricsContainerRef.value) return
  
  const activeEl = lyricsContainerRef.value.querySelector('.lyric-line.active') as HTMLElement
  if (activeEl) {
    // 计算偏移：元素顶部 - 容器一半 + 元素一半
    const top = activeEl.offsetTop - lyricsContainerRef.value.clientHeight / 2 + activeEl.clientHeight / 2
    
    lyricsContainerRef.value.scrollTo({
      top,
      behavior: 'smooth'
    })
  }
}

// --- 其他逻辑 (保持不变) ---
const formatTime = (seconds: number) => {
  if (!seconds || isNaN(seconds)) return '00:00'
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

const onSeekStart = () => { isSeeking.value = true }
const onSeekEnd = (e: Event) => {
  const target = e.target as HTMLInputElement
  seek(Number(target.value))
  isSeeking.value = false
}

const goToUpload = () => navigateTo('/play/musicupload')

const coverUrl = computed(() => {
  // @ts-ignore
  return currentTrackObj.value.cover || currentTrackObj.value.cover_r2_key || '/images/deco.e59de0.png'
})

const modeIconColor = computed(() => 'var(--text-main)')
</script>

<template>
  <div class="play-page">
    <div class="player-container">
      
      <div class="visual-side">
        <div class="album-cover-box large">
          <img :src="coverUrl" class="album-img" alt="Cover" />
          <div class="cover-overlay">
            <Music :size="48" v-if="!coverUrl.includes('http')" />
          </div>
        </div>
      </div>

      <div class="control-side">
        
        <div class="header-row">
          <div class="track-info">
            <div class="track-title">{{ currentTrackObj.title }}</div>
            <div class="track-artist">{{ currentTrackObj.artist || 'Unknown Artist' }}</div>
          </div>
          <button class="upload-entry-btn" @click="goToUpload">
            <UploadCloud :size="16" />
          </button>
        </div>

        <div class="lyrics-box embedded">
          <div class="lyrics-content-wrapper" ref="lyricsContainerRef">
            <div 
              v-for="(line, index) in lyricsData" 
              :key="index" 
              class="lyric-line"
              :class="{ active: index === currentLineIndex }"
              @click="seek(line.time)" 
            >
              <div class="l-text">{{ line.text.split('\n')[0] }}</div>
              <div v-if="showTranslation && line.text.split('\n')[1]" class="l-trans">
                {{ line.text.split('\n')[1] }}
              </div>
            </div>
            
            <div style="height: 50%;"></div>
          </div>

          <button class="trans-btn floating" @click="showTranslation = !showTranslation" :class="{ active: showTranslation }">
            <Languages :size="14"/>
          </button>
        </div>

        <div class="progress-area">
          <div class="time-labels">
            <span>{{ formatTime(currentTime) }}</span>
            <span>{{ formatTime(duration) }}</span>
          </div>
          <input 
            type="range" min="0" :max="duration || 100" :value="currentTime" 
            @input="currentTime = Number(($event.target as HTMLInputElement).value)"
            @mousedown="onSeekStart" @mouseup="onSeekEnd"
            class="seek-slider"
          />
        </div>

        <div class="controls">
          <button class="ctrl-btn mode-btn" @click="toggleMode" :title="playMode.toUpperCase()">
            <Repeat v-if="playMode === 'sequence'" :size="20" />
            <Repeat v-else-if="playMode === 'loop'" :size="20" color="var(--c-brand)" />
            <Shuffle v-else-if="playMode === 'shuffle'" :size="20" color="var(--c-brand)" />
          </button>

          <button class="ctrl-btn" @click="prev"><SkipBack :size="24"/></button>
          
          <button class="ctrl-btn main" @click="toggle">
            <Pause v-if="isPlaying" :size="32" fill="black" stroke="black"/>
            <Play v-else :size="32" fill="black" stroke="black" style="margin-left: 4px;"/>
          </button>
          
          <button class="ctrl-btn" @click="next"><SkipForward :size="24"/></button>
          
          <button class="ctrl-btn mode-btn" @click="togglePlaylist" :class="{ active: showPlaylist }" title="Playlist">
            <List :size="20" />
          </button>
        </div>

        <div class="playlist compact" v-show="showPlaylist">
          <div 
            v-for="(track, index) in playlist" 
            :key="track.id" 
            class="playlist-item" 
            :class="{ active: currentTrackObj.id === track.id }"
            @click="playList(playlist, index)"
          >
            <div class="item-idx">{{ index + 1 }}</div>
            <div class="item-info">
              <div class="item-title">{{ track.title }}</div>
              <div class="item-artist">{{ track.artist || '-' }}</div>
            </div>
          </div>
        </div>

      </div>
      
    </div>
  </div>
</template>

<style scoped>
/* 补充歌词行内样式，确保 play.css 之外的细节正常显示 */
.lyric-line {
  padding: 10px 0;
  text-align: left; /* 改为左对齐或居中视设计而定，这里建议左对齐适合阅读 */
  color: var(--text-sub);
  opacity: 0.5;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  cursor: pointer;
  border-radius: 4px;
}

.lyric-line:hover {
  background: rgba(255, 255, 255, 0.05);
  opacity: 0.8;
}

/* 高亮态 */
.lyric-line.active {
  opacity: 1;
  transform: scale(1.02);
  transform-origin: left center;
}

.l-text {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 4px;
}

.lyric-line.active .l-text {
  color: var(--c-brand); /* 高亮变黄 */
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
}

.l-trans {
  font-size: 12px;
  font-family: var(--font-mono);
}

/* 列表激活态样式补充 */
.ctrl-btn.mode-btn.active {
  color: var(--c-brand);
  border-color: var(--c-brand);
}
</style>