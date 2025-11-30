<script setup lang="ts">
// 暂留（待改动）
// Asset 相关逻辑保留以备未来扩展
// const { data: assets, pending, error } = await useFetch<Asset[]>('/assets/', {
//   baseURL: config.public.apiBase,
//   lazy: true
// })

useHead({
  title: 'Endfield Industrial Operating System'
})
</script>

<template>
  <div class="dashboard-page">
    <!-- Hero 区域 -->
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          ENDFIELD<br>
          INDUSTRIAL<br>
          SYSTEM
        </h1>
        <div class="hero-subtitle">// 终末地集成工业系统</div>
        
        <!-- 系统状态栏 -->
        <SystemStatusBar />
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="content-wrapper">
      <!-- 核心模块入口 -->
      <div class="module-grid">
        <ModuleCard
          icon="📁"
          title="PROTOCOL ARCHIVE"
          subtitle="协议档案库"
          status="● Online"
          meta="Cloud Storage"
          route="/wiki"
          :disabled="false"
        />
        
        <ModuleCard
          icon="🎵"
          title="AUDIO TERMINAL"
          subtitle="音频终端"
          status="● Streaming"
          meta="Music Player"
          route="/play"
          :disabled="false"
        />
        
        <ModuleCard
          icon="📐"
          title="EDITOR MODULE"
          subtitle="蓝图模块"
          status="🔧 Building"
          meta="Coming Soon"
          route="/editor"
          :disabled="true"
        />
      </div>

      <!-- 实时活动流 -->
      <div class="activity-section">
        <ActivityLog />
      </div>
    </div>
  </div>
</template>

<style>
@import '@/assets/css/dashboard.css';
</style>