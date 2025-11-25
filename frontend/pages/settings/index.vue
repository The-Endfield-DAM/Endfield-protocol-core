<script setup lang="ts">
import { Lock, ChevronRight } from 'lucide-vue-next' // 🟢 引入新图标

const config = useRuntimeConfig()
const session = useSupabaseSession()

// 1. 获取当前用户信息
const { data: userInfo, pending, error, refresh } = await useFetch<any>('/users/me', {
  baseURL: config.public.apiBase,
  onRequest({ options }) {
    const token = session.value?.access_token
    if (token) {
      options.headers = { Authorization: `Bearer ${token}` } as any
    }
  },
  lazy: true,
  server: false 
})

// 判断是否为管理员
const isAdmin = computed(() => userInfo.value?.role === 'admin')

// 跳转
const enterAdminConsole = () => navigateTo('/settings/admin')
const enterSecurity = () => navigateTo('/settings/safety') // 🟢 新增跳转
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

      <div class="security-section">
        <div class="security-card" @click="enterSecurity">
          <div class="sec-icon">
            <Lock :size="24" />
          </div>
          <div class="sec-info">
            <div class="sec-title">SECURITY_PROTOCOL // 安全协议</div>
            <div class="sec-desc">密码修改 / 邮箱换绑 / 账户安全</div>
          </div>
          <div class="sec-action">
            <ChevronRight :size="20" />
          </div>
        </div>
      </div>

      <div class="admin-section">
        <template v-if="isAdmin">
          <div class="section-title">
            <h2>SYSTEM_STATUS</h2>
            <button class="badge admin clickable" @click="enterAdminConsole" title="Access Admin Console">
              LEVEL 5 CLEARANCE <span class="arrow">➜</span>
            </button>
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
              // 点击上方权限徽章进入审批中心
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

<style scoped>
/* 复用 settings.css 基础样式 */

/* 🟢 新增：安全入口样式 */
.security-section {
  margin-top: 40px;
}

.security-card {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  padding: 20px 30px;
  display: flex;
  align-items: center;
  gap: 20px;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  overflow: hidden;
}

.security-card:hover {
  border-color: var(--c-brand);
  background: rgba(255, 215, 0, 0.05);
  transform: translateX(5px);
}

.sec-icon {
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-main);
  transition: color 0.2s;
}
.security-card:hover .sec-icon { color: var(--c-brand); }

.sec-info { flex: 1; }

.sec-title {
  font-family: var(--font-mono);
  font-weight: bold;
  font-size: 16px;
  color: var(--text-main);
  margin-bottom: 5px;
}

.sec-desc {
  font-size: 12px;
  color: var(--text-sub);
}

.sec-action { color: var(--text-sub); transition: transform 0.2s; }
.security-card:hover .sec-action { 
  color: var(--c-brand); 
  transform: translateX(5px); 
}

/* 徽章交互样式 (Admin) */
.badge.clickable {
  cursor: pointer; border: none; transition: all 0.3s;
  display: flex; align-items: center; gap: 6px;
}
.badge.clickable:hover {
  background: var(--c-success); color: #000;
  box-shadow: 0 0 15px rgba(74, 222, 128, 0.4);
  transform: translateY(-1px); padding-right: 12px;
}
.arrow { display: inline-block; font-size: 10px; opacity: 0; transform: translateX(-5px); transition: all 0.3s; }
.badge.clickable:hover .arrow { opacity: 1; transform: translateX(0); }
</style>