<script setup lang="ts">
import { CheckCircle, AlertTriangle, XCircle, Info } from 'lucide-vue-next'

const { toastState, hide } = useToast()

// 根据类型动态选择图标
const getIcon = () => {
  switch (toastState.value.type) {
    case 'success': return CheckCircle
    case 'error': return XCircle
    case 'warning': return AlertTriangle
    default: return Info
  }
}
</script>

<template>
  <Teleport to="body">
    <Transition name="toast-slide">
      <div 
        v-if="toastState.show" 
        class="system-toast" 
        :class="toastState.type"
        @click="hide"
      >
        <div class="toast-icon">
          <component :is="getIcon()" :size="20" />
        </div>
        
        <div class="toast-content">
          <div class="toast-title">SYSTEM NOTIFICATION //</div>
          <div class="toast-message">{{ toastState.message }}</div>
        </div>
        
        <div class="scan-line"></div>
      </div>
    </Transition>
  </Teleport>
</template>