// frontend/middleware/auth.global.ts

export default defineNuxtRouteMiddleware((to, from) => {
  // 获取当前 Supabase 用户状态
  const user = useSupabaseUser()

  // 1. 针对登录页的特殊逻辑
  if (to.path === '/login') {
    // 如果用户已经登录了，还想去登录页 -> 踢回首页
    if (user.value) {
      return navigateTo('/')
    }
    // 否则允许访问登录页
    return
  }

  // 2. 针对其他所有页面 (首页、Wiki、Upload等)
  // 如果用户没登录 -> 踢回登录页
  if (!user.value) {
    return navigateTo('/login')
  }
})