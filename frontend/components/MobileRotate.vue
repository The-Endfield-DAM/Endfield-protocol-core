<script setup lang="ts">
import { Smartphone } from 'lucide-vue-next'

const isLoading = ref(false)
const progress = ref(0)
let progressInterval: NodeJS.Timeout | null = null

const startLoadingSequence = () => {
  // 🟢 调试日志：看看函数是否被调用
  console.log('⚡ 触发横屏加载动画')
  
  if (isLoading.value) return

  isLoading.value = true
  progress.value = 0
  
  if (progressInterval) clearInterval(progressInterval)

  progressInterval = setInterval(() => {
    const increment = Math.floor(Math.random() * 15) + 5
    progress.value = Math.min(progress.value + increment, 100)

    if (progress.value >= 100) {
      if (progressInterval) clearInterval(progressInterval)
      setTimeout(() => {
        isLoading.value = false
        progress.value = 0
        console.log('✅ 加载完成，显示主界面')
      }, 300)
    }
  }, 150)
}

onMounted(() => {
  const mql = window.matchMedia('(orientation: portrait)')
  let wasPortrait = mql.matches
  
  // 🟢 调试日志：初始状态
  console.log('当前是否竖屏:', wasPortrait)

  const handleOrientationChange = (e: MediaQueryListEvent) => {
    const isNowPortrait = e.matches
    
    // 🟢 调试日志：状态变化
    console.log('屏幕旋转 -> 新状态是否竖屏:', isNowPortrait)
    
    // 从“竖”变“横”
    if (wasPortrait && !isNowPortrait) {
      startLoadingSequence()
    }
    wasPortrait = isNowPortrait
  }

  mql.addEventListener('change', handleOrientationChange)

  onUnmounted(() => {
    mql.removeEventListener('change', handleOrientationChange)
    if (progressInterval) clearInterval(progressInterval)
  })
})
</script>

<template>
  <div class="mobile-blocker">
    <div class="content">
      <div class="icon-wrapper">
        <Smartphone :size="64" class="phone-icon" />
      </div>
      <h2 class="title">W A R N I N G !</h2>
      <p class="subtitle">// P R T S :请旋转设备以接入终端</p>
      <div class="decor-line"></div>
      <p class="info">Rotate display for optimal viewing experience.</p>
    </div>
  </div>

  <transition name="fade">
    <div v-if="isLoading" class="transition-loader">
      <div class="loader-content">
        <div class="loader-deco"></div>
        <div class="loader-text glitch" data-text="TERMINAL LOADING...">TERMINAL LOADING...</div>
        
        <div class="progress-container">
          <div class="progress-bar" :style="{ width: progress + '%' }"></div>
        </div>
        
        <div class="progress-info">
          <span>SYSTEM SYNCHRONIZING</span>
          <span class="percentage">{{ progress }}%</span>
        </div>
      </div>
    </div>
  </transition>
</template>