<script setup lang="ts">
// 引入 Supabase 客户端
const supabase = useSupabaseClient()
const user = useSupabaseUser()

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
const handleAuth = async () => {
  // 1. 数据清洗：去除首尾空格，防止复制粘贴带入的不可见字符导致格式错误
  const cleanEmail = username.value.trim()
  const cleanPassword = password.value.trim()

  // 2. 空值校验
  if (!cleanEmail || !cleanPassword) return alert('MISSING DATA // 请输入完整信息')
  
  isLoading.value = true
  try {
    if (isLoginMode.value) {
      // --- 登录模式 ---
      const { error } = await supabase.auth.signInWithPassword({
        email: cleanEmail,
        password: cleanPassword
      })
      if (error) throw error
      
      console.log('Login Success')
      // 注意：登录成功后，页面顶部的 watchEffect 会自动监测到 user 变化并跳转首页
      
    } else {
      // --- 注册模式 ---
      const { error, data } = await supabase.auth.signUp({
        email: cleanEmail,
        password: cleanPassword
      })
      if (error) throw error
      
      // 3. 注册后状态判断
      // 如果你在 Supabase 关闭了 "Confirm email"，这里会直接返回 session，视为自动登录
      if (data.session) {
        alert('PROFILE CREATED // 档案已建立，正在自动登入...')
      } else {
        // 如果开启了邮箱验证，提示查收邮件
        alert('VERIFICATION REQUIRED // 请前往邮箱查收验证信件')
        isLoginMode.value = true // 自动切回登录界面方便操作
      }
    }
  } catch (error: any) {
    console.error(error)
    
    // 4. 错误信息汉化/人性化处理
    let msg = error.message
    if (msg.includes('Invalid login credentials')) msg = '身份验证失败 (账号或密码错误)'
    if (msg.includes('User already registered')) msg = '该身份已存在 (请直接登录)'
    if (msg.includes('invalid claim')) msg = '会话已过期，请刷新页面'
    
    alert(`ACCESS DENIED // ${msg}`)
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
        <label class="input-label">IDENTITY (EMAIL)/</label>
        <input 
          type="text" 
          v-model="username"
          class="input-field" 
          spellcheck="false"
          @keyup.enter="handleAuth"
        >
      </div>
      <div class="input-group">
        <label class="input-label">Rb_SECRET/</label>
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