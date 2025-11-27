// frontend/composables/usePlayer.ts

export interface Track {
  id: number | string
  title: string
  artist?: string
  url: string
  cover?: string
  mimeType?: string
  lyrics?: string
}

const DEFAULT_TRACK: Track = {
  id: 'bgm_001',
  title: 'Endfield OST',
  artist: 'System Audio',
  url: '/audio/storyteller.mp3',
  mimeType: 'audio/mpeg'
}

// 播放模式类型: 列表循环 | 单曲循环 | 随机播放
export type PlayMode = 'sequence' | 'loop' | 'shuffle'

export const usePlayer = () => {
  const playlist = useState<Track[]>('player_playlist', () => [DEFAULT_TRACK])
  const currentIndex = useState<number>('player_index', () => 0)
  const isPlaying = useState<boolean>('player_status', () => false)
  const volume = useState<number>('player_volume', () => 0.4)

  const currentTime = useState<number>('player_current_time', () => 0)
  const duration = useState<number>('player_duration', () => 0)
  const isSeeking = useState<boolean>('player_seeking', () => false)

  // 🟢 新增：播放模式状态 (默认顺序播放)
  const playMode = useState<PlayMode>('player_mode', () => 'sequence')

  const currentTrackObj = computed(() => playlist.value[currentIndex.value] || DEFAULT_TRACK)
  const currentTrack = computed(() => currentTrackObj.value.url)

  const play = (track: Track) => {
    if (currentTrack.value === track.url) {
      toggle()
      return
    }
    // 查找或新增逻辑保持不变...
    const existingIndex = playlist.value.findIndex(t => t.id === track.id)
    if (existingIndex !== -1) {
      currentIndex.value = existingIndex
    } else {
      playlist.value = [track]
      currentIndex.value = 0
    }
    isPlaying.value = true
  }

  const playList = (list: Track[], index: number = 0) => {
    playlist.value = list
    currentIndex.value = index
    isPlaying.value = true
  }

  // 🟢 核心修改：根据模式决定下一首
  const next = () => {
    const len = playlist.value.length
    if (len === 0) return

    if (playMode.value === 'loop') {
      // 单曲循环：重头开始
      seek(0)
      isPlaying.value = true
    } else if (playMode.value === 'shuffle') {
      // 随机播放：随机跳一个索引 (且不与当前相同)
      let randomIdx = Math.floor(Math.random() * len)
      if (len > 1) {
        while (randomIdx === currentIndex.value) {
          randomIdx = Math.floor(Math.random() * len)
        }
      }
      currentIndex.value = randomIdx
      isPlaying.value = true
    } else {
      // 顺序播放 (列表循环)
      if (currentIndex.value < len - 1) currentIndex.value++
      else currentIndex.value = 0
      isPlaying.value = true
    }
  }

  const prev = () => {
    if (currentIndex.value > 0) currentIndex.value--
    else currentIndex.value = playlist.value.length - 1
    isPlaying.value = true
  }

  const toggle = () => {
    isPlaying.value = !isPlaying.value
  }

  const seek = (time: number) => {
    currentTime.value = time
  }

  // 🟢 新增：切换播放模式
  const toggleMode = () => {
    const modes: PlayMode[] = ['sequence', 'loop', 'shuffle']
    const nextIndex = (modes.indexOf(playMode.value) + 1) % modes.length
    playMode.value = modes[nextIndex]
  }

  const resetPlayer = () => {
    playlist.value = [DEFAULT_TRACK]
    currentIndex.value = 0
    isPlaying.value = false
    currentTime.value = 0
    duration.value = 0
  }

  const initBGM = () => {
    if (playlist.value.length === 0) {
      playlist.value = [DEFAULT_TRACK]
      currentIndex.value = 0
    }
    isPlaying.value = true
  }

  return {
    playlist,
    currentIndex,
    currentTrack,
    currentTrackObj,
    isPlaying,
    volume,
    currentTime,
    duration,
    isSeeking,
    playMode, // 导出状态
    play,
    playList,
    next,
    prev,
    toggle,
    seek,
    toggleMode, // 导出切换方法
    resetPlayer,
    initBGM
  }
}