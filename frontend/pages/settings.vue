<script setup lang="ts">
const config = useRuntimeConfig()
const session = useSupabaseSession()

// 1. 获取当前用户信息
// 🟢 核心修复：在花括号里加上 refresh
const { data: userInfo, pending, error, refresh } = await useFetch<any>('/users/me', {
  baseURL: config.public.apiBase,
  onRequest({ options }) {
    const token = session.value?.access_token
    if (token) {
      options.headers = { Authorization: `Bearer ${token}` }
    }
  },
  lazy: true,
  server: false 
})

// 判断是否为管理员
const isAdmin = computed(() => userInfo.value?.role === 'admin')
</script>

<template>
  <div class="settings-page">
    <div class="page-header">
      <h1>SYSTEM_SETTINGS <span class="sub">// 个人终端</span></h1>
    </div>

    <div v-if="pending" class="loading">LOADING USER DATA...</div>
    <div v-else-if="error" class="error">DATA CORRUPTED: {{ error.message }}</div>

    <div v-else-if="userInfo" class="content-area">
      <ProfileCard :user="userInfo" @refresh="refresh()" />

      <PersonalDossier :user="userInfo" @refresh="refresh()" />

      <div class="admin-section">
        <template v-if="isAdmin">
          <div class="section-title">
            <h2>ADMIN_CONSOLE</h2>
            <span class="badge admin">LEVEL 5 CLEARANCE</span>
          </div>
          <div class="admin-panel active">
            <div class="panel-header-text">
              <span class="blink">●</span> SYSTEM ONLINE
            </div>
            <div class="welcome-text">
              Welcome, <span class="highlight">Endministrator.</span>
            </div>
            <div class="panel-desc">
              // 全舰防御系统与人事档案库已就绪<br>
              // 等待指令...
            </div>
          </div>
        </template>

        <template v-else>
          <div class="section-title">
            <h2>OPERATOR_STATUS</h2>
            <span class="badge pending">LEVEL 1 CLEARANCE</span>
          </div>
          <div class="admin-panel pending">
            <div class="panel-header-text">
              <span class="blink-slow">●</span> AWAITING APPROVAL
            </div>
            <div class="welcome-text">
              Status: <span class="highlight-pending">Pending...</span>
            </div>
            <div class="panel-desc">
              // 您的权限正在审批流程中<br>
              // 如需管理员认证，请联系基建工程部
            </div>
          </div>
        </template>
      </div>

    </div>
  </div>
</template>