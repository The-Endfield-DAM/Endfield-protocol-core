// frontend/composables/useToast.ts

type ToastType = 'success' | 'error' | 'warning' | 'info'

interface ToastState {
  show: boolean
  message: string
  type: ToastType
}

export const useToast = () => {
  // 使用 useState 保证跨组件共享状态
  const toastState = useState<ToastState>('system_toast', () => ({
    show: false,
    message: '',
    type: 'info'
  }))

  let timer: NodeJS.Timeout | null = null

  // 核心触发函数
  const show = (message: string, type: ToastType = 'info', duration = 3000) => {
    // 如果已有弹窗，先强制重置（产生一种刷新感）
    if (toastState.value.show) {
      if (timer) clearTimeout(timer)
      toastState.value.show = false
      setTimeout(() => trigger(message, type, duration), 100)
    } else {
      trigger(message, type, duration)
    }
  }

  const trigger = (message: string, type: ToastType, duration: number) => {
    toastState.value = { show: true, message, type }
    
    if (duration > 0) {
      timer = setTimeout(() => {
        toastState.value.show = false
      }, duration)
    }
  }

  const hide = () => {
    toastState.value.show = false
  }

  return {
    toastState,
    hide,
    // 快捷调用方法
    success: (msg: string) => show(msg, 'success'),
    error: (msg: string) => show(msg, 'error'),
    warning: (msg: string) => show(msg, 'warning'),
    info: (msg: string) => show(msg, 'info')
  }
}