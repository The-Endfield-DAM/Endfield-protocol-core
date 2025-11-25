<script setup lang="ts">
import { ChevronLeft } from 'lucide-vue-next'

const config = useRuntimeConfig()
const session = useSupabaseSession()

// 路由守卫：防止普通用户通过 URL 强行进入
const { data: userInfo, pending } = await useFetch<any>('/users/me', {
  baseURL: config.public.apiBase,
  onRequest({ options }) {
    const token = session.value?.access_token
    if (token) options.headers = { Authorization: `Bearer ${token}` } as any
  },
  server: false
})

// 监听权限，如果不是管理员直接踢回设置页
watch(userInfo, (user) => {
  if (user && user.role !== 'admin') {
    navigateTo('/settings')
  }
})

const goBack = () => navigateTo('/settings')
</script>

<template>
  <div class="settings-page">
    <div class="page-header">
      <div class="header-left">
        <button class="back-btn" @click="goBack">
          <ChevronLeft :size="24" />
        </button>
        <div>
          <h1>ADMIN_CONSOLE</h1>
          <div class="sub">// 干员审批中心</div>
        </div>
      </div>
      
      <div class="badge admin">LEVEL 5 RESTRICTED</div>
    </div>

    <div class="content-area">
      <AdminAuditList />
    </div>
    
  </div>
</template>

<style scoped>
/* 复用 settings.css 的基础样式 */
.settings-page { padding: 40px; height: 100%; overflow-y: auto; }

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.back-btn {
  background: transparent;
  border: 1px solid var(--border-light);
  color: var(--text-sub);
  width: 40px; height: 40px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}
.back-btn:hover {
  border-color: var(--c-brand);
  color: var(--c-brand);
}

.badge.admin {
  background: var(--c-success);
  color: #000;
  padding: 4px 12px;
  font-family: var(--font-mono);
  font-weight: bold;
  font-size: 12px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  border-bottom: 1px solid var(--border-light);
  margin-bottom: 30px;
  padding-bottom: 10px;
}

.page-header h1 { font-size: 24px; color: var(--text-main); letter-spacing: 2px; margin: 0; }
.sub { font-size: 12px; color: var(--c-brand); margin-top: 4px; }

@media (max-width: 768px) { 
  .settings-page { padding: 20px; }
}
</style>