<script setup lang="ts">
import { Check, X, AlertTriangle } from 'lucide-vue-next'

const props = defineProps<{
  fileName?: string
}>()

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
          
          <div class="delete-title">CONFIRM DELETION</div>
          <div class="delete-info">
            确认删除文件吗？<br>
            <span style="color: #FF4D4F; font-weight: bold;">{{ fileName }}</span>
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