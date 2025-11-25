<script setup lang="ts">
import { Check, X, AlertTriangle } from 'lucide-vue-next'

const props = defineProps<{
  title?: string
  message?: string
  subMessage?: string
}>()

// 双向绑定显示状态
const isOpen = defineModel<boolean>({ default: false })
const emit = defineEmits(['confirm'])

const confirm = () => {
  emit('confirm')
  isOpen.value = false
}
const close = () => { isOpen.value = false }
</script>

<template>
  <Teleport to="body">
    <Transition name="pop">
      <div v-if="isOpen" class="delete-overlay">
        <div class="delete-box">
          <AlertTriangle :size="48" color="#FF4D4F" style="margin: 0 auto 15px;" />
          
          <div class="delete-title">{{ title || 'SYSTEM WARNING' }}</div>
          <div class="delete-info">
            {{ message }}<br>
            <span style="color: #FF4D4F; font-weight: bold;">{{ subMessage }}</span>
          </div>

          <div class="delete-actions">
            <button class="symbol-btn cancel" @click="close">
              <X :size="28" stroke-width="3" />
            </button>
            
            <button class="symbol-btn confirm" @click="confirm">
              <Check :size="28" stroke-width="3" />
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>