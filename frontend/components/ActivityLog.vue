<script setup lang="ts">
const config = useRuntimeConfig()

interface Activity {
    time: string
    type: string
    message: string
}

const { data: activities, refresh } = await useFetch<Activity[]>('/activities/', {
  baseURL: config.public.apiBase,
  lazy: true
})

// 每1小时刷新一次
const refreshInterval = 60 * 60 * 1000
let timer: any = null

onMounted(() => {
  timer = setInterval(() => {
    refresh()
  }, refreshInterval)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

// 获取最后更新时间
const lastUpdate = computed(() => {
  const now = new Date()
  return now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
})
</script>

<template>
  <div class="activity-log">
    <div class="log-header">
      <span class="log-title">// RECENT ACTIVITY</span>
      <span class="log-update">Last Update: {{ lastUpdate }}</span>
    </div>
    <div class="log-content">
      <div 
        v-for="(act, idx) in activities" 
        :key="idx" 
        class="log-line"
      >
        <span class="log-prompt">&gt;</span>
        <span class="log-time">[{{ act.time }}]</span>
        <span class="log-msg">{{ act.message }}</span>
      </div>
      <div v-if="!activities || activities.length === 0" class="log-line">
        <span class="log-prompt">&gt;</span>
        <span class="log-msg">No recent activities</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.activity-log {
  background: #000;
  border: 1px solid #333;
  padding: 20px;
  font-family: 'Courier New', monospace;
}

.log-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #333;
}

.log-title {
  color: var(--c-brand);
  font-size: 12px;
  font-weight: bold;
}

.log-update {
  color: var(--text-sub);
  font-size: 10px;
}

.log-content {
  max-height: 200px;
  overflow-y: auto;
}

.log-content::-webkit-scrollbar {
  width: 6px;
}

.log-content::-webkit-scrollbar-track {
  background: #111;
}

.log-content::-webkit-scrollbar-thumb {
  background: #333;
}

.log-line {
  color: #0f0;
  font-size: 13px;
  margin-bottom: 8px;
  line-height: 1.6;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from { 
    opacity: 0; 
    transform: translateX(-10px); 
  }
  to { 
    opacity: 1; 
    transform: translateX(0); 
  }
}

.log-prompt {
  color: #0f0;
  margin-right: 8px;
}

.log-time {
  color: #888;
  margin-right: 8px;
}

.log-msg {
  color: #0f0;
}
</style>