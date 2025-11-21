<script setup lang="ts">
const config = useRuntimeConfig()

// --- 状态管理 ---
const fileInput = ref<HTMLInputElement | null>(null)
const isDragging = ref(false)
const isUploading = ref(false) // 仅代表正在传输中
const uploadStatus = ref<'idle' | 'signing' | 'uploading' | 'success' | 'error'>('idle')
const progress = ref(0)
const resultUrl = ref('')

// --- ⚡ 模拟进度动画 ---
const simulateProgress = () => {
  progress.value = 0
  const interval = setInterval(() => {
    if (uploadStatus.value === 'uploading') {
      if (progress.value < 95) {
        progress.value += Math.random() * 8
      }
    } else if (uploadStatus.value === 'success') {
      progress.value = 100
      clearInterval(interval)
    } else if (uploadStatus.value === 'error') {
      clearInterval(interval)
    }
  }, 150)
}

// --- 核心上传逻辑 ---
const handleFileSelect = async (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files?.[0]) await startUpload(input.files[0])
  // 重置 input 否则同一个文件不能选两次
  if (input) input.value = '' 
}

const onDrop = async (e: DragEvent) => {
  isDragging.value = false
  if (isUploading.value) return // 正在传的时候禁止拖拽
  if (e.dataTransfer?.files[0]) await startUpload(e.dataTransfer.files[0])
}

// 点击触发 (如果正在传则无效)
const triggerSelect = () => {
  if (!isUploading.value) fileInput.value?.click()
}

const startUpload = async (file: File) => {
  try {
    // 重置状态
    uploadStatus.value = 'signing'
    isUploading.value = true
    progress.value = 0
    simulateProgress()

    // 1. 获取签名
    const presignedData = await $fetch(`${config.public.apiBase}/upload/presigned`, {
      method: 'POST',
      body: { filename: file.name, content_type: file.type || 'application/octet-stream' }
    }) as any

    // 2. 直传
    uploadStatus.value = 'uploading'
    await $fetch(presignedData.upload_url, {
      method: 'PUT',
      body: file,
      headers: { 'Content-Type': file.type }
    })

    // 3. 成功
    uploadStatus.value = 'success'
    resultUrl.value = presignedData.public_url

  } catch (err) {
    console.error(err)
    uploadStatus.value = 'error'
  } finally {
    isUploading.value = false
  }
}
</script>

<template>
  <div class="upload-page">
    <div class="panel-header">
      <h1>PROTOCOL_UPLOAD <span class="sub">// 协议传输</span></h1>
    </div>

    <div class="upload-container">
      <!-- 左侧：拖拽区域 -->
      <div 
        class="drop-zone" 
        :class="{ 'dragging': isDragging, 'disabled': isUploading, 'success': uploadStatus === 'success' }"
        @dragover.prevent="isDragging = true"
        @dragleave.prevent="isDragging = false"
        @drop.prevent="onDrop"
        @click="triggerSelect"
      >
        <input type="file" ref="fileInput" @change="handleFileSelect" hidden />
        <div class="zone-content">
          <div class="upload-icon"></div>
          
          <!-- 状态：上传中 -->
          <template v-if="isUploading">
            <h3>SYSTEM BUSY</h3>
            <p>Transmitting Data...</p>
          </template>
          
          <!-- 状态：成功 (允许再次上传) -->
          <template v-else-if="uploadStatus === 'success'">
            <h3 style="color: var(--c-success)">UPLOAD COMPLETE</h3>
            <p>Click to upload another file</p>
          </template>

          <!-- 状态：空闲 -->
          <template v-else>
            <h3>INITIATE UPLOAD</h3>
            <p>Drop blueprint files or click to browse</p>
          </template>
        </div>
      </div>

      <!-- 右侧：PRTS 核心系统 -->
      <div class="monitor-wrapper">
        
        <!-- A. 待机状态 (呼吸菱形) -->
        <div v-if="uploadStatus === 'idle'" class="idle-monitor">
          <div class="idle-diamond-wrap">
            <div class="idle-diamond"></div>
            <div class="idle-diamond inner"></div>
          </div>
          <div class="idle-text">WAITING...</div>
        </div>

        <!-- B. 工作状态 (PRTS 动画) -->
        <transition name="fade-scale">
          <div v-if="uploadStatus !== 'idle'" class="prts-core">
            
            <!-- 背景巨大的水印字 -->
            <div class="bg-watermark">
              <span>P</span><span>R</span><span>T</span><span>S</span>
            </div>

            <!-- 旋转菱形容器 -->
            <div class="diamond-shifter">
              <svg class="diamond-svg" viewBox="0 0 300 300">
                <!-- 1. 先画内部填充 (放在底层) -->
                <!-- 调整了 x, y 和宽高，让它稍微缩进一点点，完全被边框包裹 -->
                <rect x="12" y="12" width="276" height="276" class="diamond-fill" 
                      :style="{ height: `${progress}%` }" />
                
                <!-- 2. 后画白色外框 (放在顶层，遮住填充边缘) -->
                <rect x="5" y="5" width="290" height="290" class="diamond-border" />
              </svg>
              
              <!-- 中心内容 -->
              <div class="core-text">
                <template v-if="uploadStatus === 'success'">
                  <div class="success-title">UPLOAD</div>
                  <div class="success-sub">SUCCESS</div>
                </template>
                <template v-else-if="uploadStatus === 'error'">
                  <div class="success-title" style="color: var(--c-danger)">ERROR</div>
                </template>
                <template v-else>
                  <div class="progress-val">{{ Math.floor(progress) }}%</div>
                  <div class="status-text">SYNCING...</div>
                </template>
              </div>
            </div>

            <div class="rhodes-label">RHODES ISLAND // NEURAL NETWORK</div>
          </div>
        </transition>
      </div>

    </div>
  </div>
</template>