<script setup lang="ts">
const isOpen = defineModel<boolean>({ default: false })
const emit = defineEmits(['logout-confirmed'])

const isShuttingDown = ref(false)
const terminalLogs = ref<string[]>([])
const terminalRef = ref<HTMLElement | null>(null)

const SYSTEM_LOGS = [
  '[SYSTEM] SIGTERM received...',
  '[KERNEL] Unmounting file systems...',
  '[AUTH] Revoking tokens...',
  '[NET] Closing connection...',
  '[SYSTEM] Halted.'
]

const startShutdownSequence = async () => {
  isShuttingDown.value = true
  for (const log of SYSTEM_LOGS) {
    terminalLogs.value.push(log)
    await nextTick()
    if (terminalRef.value) terminalRef.value.scrollTop = terminalRef.value.scrollHeight
    await new Promise(r => setTimeout(r, 150))
  }
  await new Promise(r => setTimeout(r, 300))
  emit('logout-confirmed')
  isOpen.value = false
  isShuttingDown.value = false
  terminalLogs.value = []
}

const cancel = () => {
  isOpen.value = false
}
</script>

<template>
  <ClientOnly>
    <Teleport to="body">
      <div v-if="isOpen" class="logout-overlay">
        
        <div v-if="isShuttingDown" class="shutdown-terminal" ref="terminalRef">
          <div v-for="(log, index) in terminalLogs" :key="index" class="log-line">{{ log }}</div>
          <div class="cursor-line">_</div>
        </div>

        <Transition name="banner-pop" appear>
          <div v-if="!isShuttingDown" class="warning-banner">
            <div class="warning-text">是否确认关闭终末地集成工业系统？</div>
            <div class="warning-sub">Confirm Disconnect?</div>
            
            <div class="btn-group">
              <button class="text-btn confirm" @click="startShutdownSequence">YES</button>
              <div class="divider">|</div>
              <button class="text-btn cancel" @click="cancel">NO</button>
            </div>
          </div>
        </Transition>
        
      </div>
    </Teleport>
  </ClientOnly>
</template>