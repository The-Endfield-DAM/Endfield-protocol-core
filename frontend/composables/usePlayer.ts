// frontend/composables/usePlayer.ts

// 你的默认音乐路径
const DEFAULT_BGM = '/audio/storyteller.mp3' 

export const usePlayer = () => {
  const currentTrack = useState<string | null>('player_track', () => DEFAULT_BGM)
  const isPlaying = useState<boolean>('player_status', () => false)
  const volume = useState<number>('player_volume', () => 0.4)

  const play = (url: string) => {
    if (currentTrack.value === url) {
      isPlaying.value = !isPlaying.value
    } else {
      currentTrack.value = url
      isPlaying.value = true
    }
  }

  const toggle = () => {
    isPlaying.value = !isPlaying.value
  }

  // 🟢 核心修复：重置播放器状态
  const resetPlayer = () => {
    currentTrack.value = DEFAULT_BGM
    isPlaying.value = false
  }

  // 🟢 逻辑升级：强制初始化 BGM
  const initBGM = () => {
    // 无论之前在播什么，登录成功后都切回默认背景音乐，防止旧链接过期导致 403
    currentTrack.value = DEFAULT_BGM 
    isPlaying.value = true
  }

  return {
    currentTrack,
    isPlaying,
    volume,
    play,
    toggle,
    resetPlayer, // 导出新方法
    initBGM
  }
}