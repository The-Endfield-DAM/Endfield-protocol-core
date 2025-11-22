<script setup lang="ts">
import { 
  Activity, UploadCloud, Box, Settings, User, Volume2, Layers, LogOut 
} from 'lucide-vue-next'

const route = useRoute()
const user = useSupabaseUser() // 获取当前用户信息
const supabase = useSupabaseClient() // 获取操作客户端

// 判断是否是登录页 (如果是 /login，则不显示侧边栏)
const isAuthPage = computed(() => route.path === '/login')

// 退出登录逻辑
const handleLogout = async () => {
  const confirmLogout = confirm('CONFIRM DISCONNECT? // 确认断开神经连接？')
  if (!confirmLogout) return

  try {
    await supabase.auth.signOut()
    navigateTo('/login')
  } catch (error) {
    console.error('Logout failed:', error)
  }
}
</script>

<template>
  <div class="layout-container">
    <div v-if="!isAuthPage" class="bg-decoration">ENDFIELD</div>

    <aside v-if="!isAuthPage" class="sidebar desktop-only">
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
        <div v-if="user" class="nav-item" @click="handleLogout">
          <LogOut class="nav-icon" :size="20" />
          <span class="nav-label">断开连接</span>
        </div>
        
        <NuxtLink v-else to="/login" class="nav-item">
          <User class="nav-icon" :size="20" />
          <span class="nav-label">身份识别</span>
        </NuxtLink>
        
        <NuxtLink to="/settings" class="nav-item" active-class="active">
          <Settings class="nav-icon" :size="20" />
          <span class="nav-label">系统设置</span>
        </NuxtLink>
      </div>
    </aside>

    <header v-if="!isAuthPage" class="mobile-header mobile-only">
      <div class="logo-area">
        <div class="logo-icon" style="background: var(--c-brand);"></div>
        <div class="logo-text">END<span style="color: var(--c-brand)">FIELD</span></div>
      </div>
      
      <div v-if="user" class="mobile-user" @click="handleLogout">
        <LogOut :size="20" color="var(--text-main)" />
      </div>
      <NuxtLink v-else to="/login" class="mobile-user">
        <User :size="20" color="var(--text-main)" />
      </NuxtLink>
    </header>

    <main class="main-content">
      <slot />
    </main>

    <nav v-if="!isAuthPage" class="mobile-tab-bar mobile-only">
      <NuxtLink to="/" class="tab-item" active-class="active"><Activity :size="24" /></NuxtLink>
      <NuxtLink to="/upload" class="tab-item" active-class="active"><UploadCloud :size="24" /></NuxtLink>
      <NuxtLink to="/wiki" class="tab-item" active-class="active"><Layers :size="24" /></NuxtLink>
      <NuxtLink to="/settings" class="tab-item" active-class="active"><Settings :size="24" /></NuxtLink>
    </nav>
  </div>
</template>