<script setup lang="ts">
import { 
  Activity, 
  UploadCloud, 
  Box, 
  Settings, 
  User, 
  Volume2,
  Layers 
} from 'lucide-vue-next'
</script>

<template>
  <div class="layout-container">
    <!-- 背景装饰字 -->
    <div class="bg-decoration">ENDFIELD</div>

    <!-- 侧边栏 -->
    <aside class="sidebar">
      <!-- 1. 顶部 Logo -->
      <div class="logo-area">
        <div class="logo-icon" style="background: var(--c-brand);"></div> <!-- 用黄色方块模拟Logo -->
        <div class="logo-text">END<span style="color: var(--c-brand)">FIELD</span></div>
      </div>
      
      <!-- 2. 中间导航 -->
      <nav class="nav-menu">
        <NuxtLink to="/" class="nav-item" active-class="active">
          <Activity class="nav-icon" :size="20" />
          <span class="nav-label">资产监控</span>
        </NuxtLink>
        
        <NuxtLink to="/upload" class="nav-item" active-class="active">
          <UploadCloud class="nav-icon" :size="20" />
          <span class="nav-label">协议上传</span>
        </NuxtLink>
        
        <NuxtLink to="/editor" class="nav-item" active-class="active">
          <Box class="nav-icon" :size="20" />
          <span class="nav-label">蓝图构建</span>
        </NuxtLink>

        <NuxtLink to="/wiki" class="nav-item" active-class="active">
          <Layers class="nav-icon" :size="20" />
          <span class="nav-label">工业知识库</span>
        </NuxtLink>
      </nav>

      <!-- 3. 底部功能区 (模仿截图) -->
      <div class="bottom-actions">
        <div class="nav-item">
          <User class="nav-icon" :size="20" />
          <span class="nav-label">ADMIN_001</span>
        </div>
        <div class="nav-item">
          <Volume2 class="nav-icon" :size="20" />
          <span class="nav-label">声音: 开启</span>
        </div>
        
        <NuxtLink to="/settings" class="nav-item" active-class="active">
          <Settings class="nav-icon" :size="20" />
          <span class="nav-label">系统设置</span>
        </NuxtLink>
      </div>
    </aside>

    <!-- 主内容区 -->
    <main class="main-content">
      <!-- 删掉了 TopHeader，让视野更开阔，内容直接顶到头 -->
      <slot />
    </main>
  </div>
</template>