<template>
  <div class="layout-container">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <div class="logo-area">
        <div class="logo-text">END<span class="logo-highlight">FIELD</span></div>
      </div>
      
      <nav class="nav-menu">
        <NuxtLink to="/" class="nav-item active">/// 资产监控</NuxtLink>
        <NuxtLink to="/upload" class="nav-item">/// 协议上传</NuxtLink>
        <NuxtLink to="/editor" class="nav-item">/// 蓝图构建</NuxtLink>
        <NuxtLink to="/settings" class="nav-item">/// 系统设置</NuxtLink>
      </nav>
    </aside>

    <!-- 主内容区 -->
    <main class="main-content">
      <header class="top-header">
        <div class="breadcrumb">SYSTEM // ASSETS_MANAGEMENT</div>
        <div class="user-profile">ADMIN_001</div>
      </header>
      
      <div class="page-view">
        <!-- 这里显示具体的页面内容 -->
        <slot />
      </div>
    </main>
  </div>
</template>