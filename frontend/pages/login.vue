<script setup lang="ts">
// 引入 Supabase 客户端
const supabase = useSupabaseClient()
const user = useSupabaseUser()
const { initBGM } = usePlayer()

// --- 逻辑层 ---
const username = ref('') // 这里输入的是邮箱，如 admin@endfield.com
const password = ref('')
const isLoginMode = ref(true) // true=登录, false=注册
const isLoading = ref(false)

// 如果用户已登录，自动踢回首页
watchEffect(() => {
  if (user.value) {
    navigateTo('/')
  }
})

// 切换模式
const toggleMode = () => {
  isLoginMode.value = !isLoginMode.value
  password.value = ''
}

// 核心鉴权处理
// 核心鉴权处理
const handleAuth = async () => {
  const cleanEmail = username.value.trim()
  const cleanPassword = password.value.trim()

  if (!cleanEmail || !cleanPassword) return alert('MISSING DATA // 请输入完整信息')
  
  isLoading.value = true
  try {
    if (isLoginMode.value) {
      // --- 登录 ---
      const { error } = await supabase.auth.signInWithPassword({
        email: cleanEmail,
        password: cleanPassword
      })
      if (error) throw error
      
      console.log('Login Success')
      
      // 🟢 1. 立即启动 BGM (此时播放器组件已在后台待命，会立即响应)
      initBGM()
      
      // 🟢 2. 移除 alert，直接跳转
      // alert('ACCESS GRANTED') <--- 删除这行
      navigateTo('/') 
      
    } else {
      // --- 注册 ---
      const { error, data } = await supabase.auth.signUp({
        email: cleanEmail,
        password: cleanPassword
      })
      if (error) throw error
      
      if (data.session) {
        // 🟢 注册并自动登录同理
        initBGM()
        // alert('PROFILE CREATED...') <--- 删除这行，或改成非阻塞的 Toast
        // watchEffect 会处理跳转
      } else {
        alert('VERIFICATION REQUIRED // 请前往邮箱查收验证信件')
        isLoginMode.value = true 
      }
    }
  } catch (error: any) {
    // ... 错误处理保持不变
    alert(`ACCESS DENIED // ${error.message}`)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="bg-watermark">ENDFIELD</div>
    
    <div class="logo-area">
      <div class="industrial-logo"></div>
    </div>

    <div class="login-card">
      <div class="input-group">
        <label class="input-label">U S E R N A M E/</label>
        <input 
          type="text" 
          v-model="username"
          class="input-field" 
          spellcheck="false"
          @keyup.enter="handleAuth"
        >
      </div>
      <div class="input-group">
        <label class="input-label">P A S S W O R D/</label>
        <input 
          type="password" 
          v-model="password"
          class="input-field"
          @keyup.enter="handleAuth"
        >
      </div>

      <div class="card-fade-overlay"></div>

      <div class="btn-container">
        <button class="diamond-btn" @click="handleAuth" :disabled="isLoading">
          <span class="btn-text" v-if="!isLoading">{{ isLoginMode ? 'ACCESS' : 'APPLY' }}</span>
          <span class="btn-text blink" v-else>WAIT...</span>
        </button>
      </div>
    </div>

    <div class="switch-mode" @click="toggleMode">
      {{ isLoginMode ? '申请新干员档案 // REGISTER' : '已有通行证 // LOGIN' }}
    </div>
  </div>
</template>