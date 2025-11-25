<script setup lang="ts">
import { ChevronLeft, Key, Mail, AlertTriangle, Save } from 'lucide-vue-next'

const goBack = () => navigateTo('/settings')
const supabase = useSupabaseClient()
const user = useSupabaseUser()
const { success, error: showError } = useToast()

const isLoading = ref(false)

// --- 密码修改逻辑 ---
const passwordForm = ref({ newPassword: '', confirmPassword: '' })

const updatePassword = async () => {
  const { newPassword, confirmPassword } = passwordForm.value
  
  if (!newPassword || newPassword.length < 6) {
    return showError('INVALID PASSWORD // 密码长度需大于6位')
  }
  if (newPassword !== confirmPassword) {
    return showError('MISMATCH // 两次输入不一致')
  }

  isLoading.value = true
  try {
    const { error } = await supabase.auth.updateUser({ password: newPassword })
    if (error) throw error
    
    success('PASSWORD UPDATED // 密钥已重置')
    passwordForm.value = { newPassword: '', confirmPassword: '' }
  } catch (err: any) {
    showError(`UPDATE FAILED // ${err.message}`)
  } finally {
    isLoading.value = false
  }
}

// --- 邮箱修改逻辑 ---
const emailForm = ref({ newEmail: '' })

const updateEmail = async () => {
  const email = emailForm.value.newEmail.trim()
  if (!email || !email.includes('@')) return showError('INVALID EMAIL // 格式错误')
  
  if (!confirm(`WARNING: Changing email to [${email}] will require re-verification. Proceed?`)) return

  isLoading.value = true
  try {
    const { error } = await supabase.auth.updateUser({ email: email })
    if (error) throw error
    
    success('CONFIRMATION SENT // 请前往新邮箱查收验证链接')
    emailForm.value.newEmail = ''
  } catch (err: any) {
    showError(`UPDATE FAILED // ${err.message}`)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="settings-page">
    <div class="page-header">
      <div class="header-left">
        <button class="back-btn" @click="goBack">
          <ChevronLeft :size="24" />
        </button>
        <div>
          <h1>SECURITY_PROTOCOL</h1>
          <div class="sub">// 终端安全设置</div>
        </div>
      </div>
      <div class="badge security">SECURE MODE</div>
    </div>

    <div class="content-area">
      <div class="safety-panel">
        
        <div class="panel-section">
          <div class="section-header">
            <Key :size="24" class="section-icon" />
            <div class="section-title">
              <h2>ACCESS KEY RESET</h2>
              <p>重置登录密钥</p>
            </div>
          </div>
          
          <div class="form-group">
            <label class="input-label">NEW PASSCODE / 新密码</label>
            <input type="password" v-model="passwordForm.newPassword" class="safety-input" placeholder="••••••" />
          </div>
          <div class="form-group">
            <label class="input-label">CONFIRM PASSCODE / 确认密码</label>
            <input type="password" v-model="passwordForm.confirmPassword" class="safety-input" placeholder="••••••" />
          </div>
          
          <div class="action-row">
            <button class="cyber-btn" @click="updatePassword" :disabled="isLoading">
              <Save :size="16" />
              UPDATE KEY
            </button>
          </div>
        </div>

        <div class="panel-section">
          <div class="section-header">
            <Mail :size="24" class="section-icon" />
            <div class="section-title">
              <h2>COMMUNICATION CHANNEL</h2>
              <p>通讯频段重定向 (当前: {{ user?.email }})</p>
            </div>
          </div>

          <div class="info-box">
            <AlertTriangle :size="14" style="display:inline; vertical-align:middle; margin-right:5px;"/>
            注意：修改邮箱后，系统将发送验证邮件至新邮箱。在验证完成前，旧邮箱依然有效。
          </div>
          
          <div class="form-group" style="margin-top: 20px;">
            <label class="input-label">NEW FREQUENCY / 新邮箱地址</label>
            <input type="text" v-model="emailForm.newEmail" class="safety-input" placeholder="operator@endfield.com" />
          </div>
          
          <div class="action-row">
            <button class="cyber-btn danger" @click="updateEmail" :disabled="isLoading">
              <Save :size="16" />
              RE-BIND EMAIL
            </button>
          </div>
        </div>

      </div>
    </div>
    
  </div>
</template>

<style scoped>
/* 复用部分通用样式 */
.settings-page { padding: 40px; height: 100%; overflow-y: auto; }
.header-left { display: flex; align-items: center; gap: 20px; }
.back-btn {
  background: transparent; border: 1px solid var(--border-light);
  color: var(--text-sub); width: 40px; height: 40px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; transition: all 0.2s;
}
.back-btn:hover { border-color: var(--c-brand); color: var(--c-brand); }
.badge.security { background: #00BCD4; color: #000; padding: 4px 12px; font-family: var(--font-mono); font-weight: bold; font-size: 12px; }
.page-header { display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 1px solid var(--border-light); margin-bottom: 30px; padding-bottom: 10px; }
.page-header h1 { font-size: 24px; color: var(--text-main); letter-spacing: 2px; margin: 0; }
.sub { font-size: 12px; color: var(--c-brand); margin-top: 4px; }

@media (max-width: 768px) { .settings-page { padding: 20px; } }
</style>