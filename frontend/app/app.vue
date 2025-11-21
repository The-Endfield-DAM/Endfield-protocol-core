<script setup lang="ts">
// 1. 定义数据结构 (TypeScript 接口)
interface Asset {
  id: number
  name: string
  code: string
  type: string
  status: string
  location?: string
}

// 2. 请求后端数据
// useFetch 是 Nuxt 的核心函数，自动处理服务端渲染
// 注意：这里必须写后端地址 http://127.0.0.1:8000
const { data: assets, pending, error } = await useFetch<Asset[]>('http://127.0.0.1:8000/assets/')

// 3. 状态颜色逻辑
const getStatusColor = (status: string) => {
  if (status === 'Active') return '#4ade80' // 绿色
  if (status === 'Warning') return '#facc15' // 黄色
  return '#f87171' // 红色
}
</script>

<template>
  <div class="endfield-terminal">
    <!-- 顶部导航 -->
    <header class="header">
      <h1 class="title">ENDFIELD <span class="sub">PROTOCOL</span></h1>
      <div class="status-bar">SYSTEM ONLINE</div>
    </header>

    <!-- 加载中状态 -->
    <div v-if="pending" class="loading">
      Connecting to Industrial System...
    </div>

    <!-- 错误状态 -->
    <div v-else-if="error" class="error-box">
      <p>CONNECTION LOST</p>
      <small>{{ error }}</small>
    </div>

    <!-- 资产列表 (卡片流) -->
    <div v-else class="grid-container">
      <div v-for="asset in assets" :key="asset.id" class="asset-card">
        <div class="card-header">
          <span class="asset-code">{{ asset.code }}</span>
          <span class="indicator" :style="{ backgroundColor: getStatusColor(asset.status) }"></span>
        </div>
        <h2 class="asset-name">{{ asset.name }}</h2>
        <div class="card-meta">
          <p>TYPE: {{ asset.type }}</p>
          <p>LOC: {{ asset.location || 'Unknown' }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 终末地风格样式表 */
:global(body) {
  margin: 0;
  background-color: #0a0a0a;
  color: #e5e5e5;
  font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.endfield-terminal {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.header {
  border-bottom: 2px solid #ffd700; /* 终末地黄 */
  margin-bottom: 40px;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding-bottom: 10px;
}

.title {
  font-size: 2.5rem;
  font-weight: 900;
  letter-spacing: 2px;
  margin: 0;
}

.sub { font-weight: 300; opacity: 0.7; }
.status-bar { font-family: monospace; color: #4ade80; }

.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.asset-card {
  background: #1a1a1a;
  border: 1px solid #333;
  padding: 24px;
  transition: transform 0.2s, border-color 0.2s;
  position: relative;
  overflow: hidden;
}

.asset-card:hover {
  transform: translateY(-2px);
  border-color: #ffd700;
}

/* 装饰性左边框 */
.asset-card::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background-color: #333;
  transition: background-color 0.2s;
}
.asset-card:hover::before { background-color: #ffd700; }

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.asset-code {
  font-family: monospace;
  color: #666;
  font-size: 0.9rem;
}

.indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  box-shadow: 0 0 8px currentColor;
}

.asset-name { margin: 0 0 15px 0; font-size: 1.2rem; }

.card-meta {
  font-size: 0.85rem;
  color: #888;
  font-family: monospace;
  line-height: 1.5;
}
</style>