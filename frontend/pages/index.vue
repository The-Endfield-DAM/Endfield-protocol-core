<script setup lang="ts">
// 1. 先定义接口
interface Asset {
  id: number
  name: string
  code: string
  type: string
  status: string
}

// 2. 再请求数据 (只留这一行！)
// 加入了 { lazy: true } 参数，防止后端没启动时前端卡死
const { data: assets, pending, error } = await useFetch<Asset[]>('http://127.0.0.1:8000/assets/', {
  lazy: true
})
</script>

<template>
  <div class="dashboard-page">
    <!-- 模仿官网的 Hero 区域 -->
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">INTEGRATED<br>INDUSTRIAL<br>SYSTEM</h1>
        <div class="hero-subtitle"> // 终末地集成工业协议 v1.0</div>
        <div class="hero-stats">
          <div class="stat-item">
            <div class="stat-val">Online</div>
            <div class="stat-label">System Status</div>
          </div>
          <div class="stat-item">
            <div class="stat-val">42ms</div>
            <div class="stat-label">Latency</div>
          </div>
        </div>
      </div>
      <!-- 这是一个装饰用的斜线背景 -->
      <div class="hero-overlay"></div>
    </div>

    <!-- 下方的内容区域 -->
    <div class="content-wrapper">
      <div class="section-header">
        <h2>ASSETS_OVERVIEW</h2>
        <div class="filter-tabs">
          <span class="tab active">ALL</span>
          <span class="tab">ACTIVE</span>
          <span class="tab">OFFLINE</span>
        </div>
      </div>

      <div v-if="pending" class="loading">SYSTEM SYNC...</div>
      
      <div v-else class="asset-grid">
        <AssetCard 
          v-for="asset in assets" 
          :key="asset.id"
          :code="asset.code"
          :name="asset.name"
          :type="asset.type"
          :status="asset.status"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-page {
  /* 页面不再有 padding，而是全屏 */
  min-height: 100%;
}

.hero-section {
  height: 300px; /* 顶部大图区域 */
  background: linear-gradient(45deg, #111 0%, #222 100%);
  position: relative;
  display: flex;
  align-items: center;
  padding: 0 40px;
  overflow: hidden;
  border-bottom: 2px solid var(--c-brand);
}

.hero-content { z-index: 2; }

.hero-title {
  font-size: 48px;
  font-weight: 900;
  line-height: 1;
  margin: 0;
  color: #fff;
  letter-spacing: 2px;
}

.hero-subtitle {
  color: var(--c-brand);
  font-family: var(--font-mono);
  margin-top: 10px;
  font-size: 14px;
}

.hero-overlay {
  position: absolute;
  top: 0; right: 0; bottom: 0; left: 0;
  background-image: repeating-linear-gradient(
    45deg,
    transparent,
    transparent 10px,
    rgba(255, 215, 0, 0.05) 10px,
    rgba(255, 215, 0, 0.05) 11px
  );
  z-index: 1;
}

.content-wrapper {
  padding: 40px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  border-bottom: 1px solid var(--border-light);
  padding-bottom: 10px;
}

.section-header h2 {
  font-weight: 300;
  font-size: 20px;
  letter-spacing: 1px;
}

.filter-tabs {
  display: flex;
  gap: 20px;
  font-size: 12px;
  font-family: var(--font-mono);
  color: var(--text-sub);
}

.tab.active { color: var(--c-brand); text-decoration: underline; }
.loading { color: var(--c-brand); font-family: var(--font-mono); animation: blink 1s infinite; }

@keyframes blink { 50% { opacity: 0.5; } }
</style>