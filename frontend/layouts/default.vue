<script setup lang="ts">
import { 
  Activity, 
  UploadCloud, 
  Box, 
  Settings, 
  User, 
  Volume2,
  Layers,
  Menu // 新增 Menu 图标
} from 'lucide-vue-next'
</script>

<template>
  <div class="layout-container">
    <div class="bg-decoration">ENDFIELD</div>

    <aside class="sidebar desktop-only">
      <div class="logo-area">
        <div class="logo-icon" style="background: var(--c-brand);"></div>
        <div class="logo-text">END<span style="color: var(--c-brand)">FIELD</span></div>
      </div>
      
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

      <div class="bottom-actions">
        <NuxtLink to="/settings" class="nav-item" active-class="active">
          <Settings class="nav-icon" :size="20" />
          <span class="nav-label">系统设置</span>
        </NuxtLink>
      </div>
    </aside>

    <header class="mobile-header mobile-only">
      <div class="logo-area">
        <div class="logo-icon" style="background: var(--c-brand);"></div>
        <div class="logo-text">END<span style="color: var(--c-brand)">FIELD</span></div>
      </div>
      <div class="mobile-user">
        <User :size="20" />
      </div>
    </header>

    <main class="main-content">
      <slot />
    </main>

    <nav class="mobile-tab-bar mobile-only">
      <NuxtLink to="/" class="tab-item" active-class="active">
        <Activity :size="24" />
      </NuxtLink>
      <NuxtLink to="/upload" class="tab-item" active-class="active">
        <UploadCloud :size="24" />
      </NuxtLink>
      <NuxtLink to="/wiki" class="tab-item" active-class="active">
        <Layers :size="24" />
      </NuxtLink>
      <NuxtLink to="/settings" class="tab-item" active-class="active">
        <Settings :size="24" />
      </NuxtLink>
    </nav>
  </div>
</template>