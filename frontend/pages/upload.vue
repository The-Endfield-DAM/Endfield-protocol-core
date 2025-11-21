<script setup lang="ts">
const config = useRuntimeConfig()

// --- 状态管理 ---
const fileInput = ref<HTMLInputElement | null>(null)
const isDragging = ref(false)
const isUploading = ref(false) // 仅代表正在传输中
const uploadStatus = ref<'idle' | 'signing' | 'uploading' | 'processing' | 'success' | 'error'>('idle')
const progress = ref(0)
const resultUrl = ref('')

// --- ⚡ 模拟进度动画 ---
const simulateProgress = () => {
  progress.value = 0
  const interval = setInterval(() => {
    // 1. 签名阶段 (Signing): 慢速走到 20%
    if (uploadStatus.value === 'signing') {
      if (progress.value < 20) {
        progress.value += 1
      }
    } 
    // 2. 上传阶段 (Uploading): 正常走到 90%
    else if (uploadStatus.value === 'uploading') {
      if (progress.value < 90) {
        progress.value += Math.random() * 5 // 稍微调慢一点，避免大文件一下子这就跑满了
      }
    }
    // 3. 处理阶段 (Processing/Database): 走到 99%
    else if (uploadStatus.value === 'processing') {
      if (progress.value < 99) {
        progress.value += 0.5
      }
    }
    // 4. 成功或失败
    else if (uploadStatus.value === 'success') {
      progress.value = 100
      clearInterval(interval)
    } else if (uploadStatus.value === 'error') {
      clearInterval(interval)
    }
  }, 100) // 稍微加快刷新频率，看起来更丝滑
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
    // --- 阶段 1: 签名 ---
    uploadStatus.value = 'signing'
    isUploading.value = true
    progress.value = 0
    simulateProgress() // 启动动画

    const presignedData = await $fetch(`${config.public.apiBase}/upload/presigned`, {
      method: 'POST',
      body: { filename: file.name, content_type: file.type || 'application/octet-stream' }
    }) as any

    // --- 阶段 2: 直传 R2 ---
    uploadStatus.value = 'uploading' // 进度条开始主跑
    
    await $fetch(presignedData.upload_url, {
      method: 'PUT',
      body: file,
      headers: { 'Content-Type': file.type }
    })

    // --- 阶段 3: 录入数据库 (新增状态) ---
    uploadStatus.value = 'processing' // 进度条进入最后冲刺
    
    await $fetch(`${config.public.apiBase}/files/`, {
      method: 'POST',
      body: {
        filename: file.name,
        r2_key: presignedData.file_key,
        url: presignedData.public_url,
        size: file.size,
        mime_type: file.type,
        asset_id: null 
      }
    })

    // --- 阶段 4: 完成 ---
    uploadStatus.value = 'success' // 进度条直接满 100%
    resultUrl.value = presignedData.public_url

  } catch (err) {
    console.error("上传流程崩溃:", err) // 打印详细错误
    
    // 🔴 强制切换为错误状态，这会触发 simulateProgress 里的 clearInterval
    uploadStatus.value = 'error' 
    
    // 🔴 (可选) 如果你想在界面上显示具体错误，可以加一个 alert
    // alert("上传失败，请检查控制台日志") 
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