<script setup lang="ts">
const session = useSupabaseSession()
const config = useRuntimeConfig()

// --- 状态管理 ---
const fileInput = ref<HTMLInputElement | null>(null)
const isDragging = ref(false)
const isUploading = ref(false)
const uploadStatus = ref<'idle' | 'signing' | 'uploading' | 'processing' | 'success' | 'error'>('idle')
const progress = ref(0)
const resultUrl = ref('')

// 新增：批量上传状态
const totalFiles = ref(0)
const completedFiles = ref(0)

// --- ⚡ 批量任务调度器 (指挥官) ---
const handleBatchUpload = async (files: File[]) => {
  if (files.length === 0) return

  // 1. 初始化状态
  isUploading.value = true
  uploadStatus.value = 'signing' // 先进入准备态
  progress.value = 0
  totalFiles.value = files.length
  completedFiles.value = 0
  
  let successCount = 0
  let failCount = 0

  // 2. 开始循环上传 (串行执行，保证稳定性；如果想快可以用 Promise.all 并发)
  // 为了动画好看，我们用串行，让进度条慢慢涨
  uploadStatus.value = 'uploading'

  for (const file of files) {
    try {
      // 调用单文件上传逻辑
      await uploadSingleFile(file)
      successCount++
    } catch (e) {
      console.error(`File ${file.name} failed:`, e)
      failCount++
    } finally {
      completedFiles.value++
      // 更新总进度 (百分比)
      progress.value = (completedFiles.value / totalFiles.value) * 100
    }
  }

  // 3. 结算
  isUploading.value = false
  if (successCount > 0) {
    uploadStatus.value = 'success'
    // 如果有失败的，可以在这里提示，或者暂时只显示成功
    if (failCount > 0) {
      console.warn(`${failCount} files failed to upload.`)
    }
  } else {
    uploadStatus.value = 'error'
  }
}

// --- ⚡ 单文件执行者 (士兵) ---
// 从原来的 startUpload 改造而来，不再控制全局状态，只负责抛出异常或成功
const uploadSingleFile = async (file: File) => {
  const contentType = file.type || 'application/octet-stream'

  // 1. 获取签名
  const presignedData = await $fetch(`${config.public.apiBase}/upload/presigned`, {
    method: 'POST',
    body: { 
      filename: file.name, 
      content_type: contentType 
    }
  }) as any

  // 2. 直传 R2
  await $fetch(presignedData.upload_url, {
    method: 'PUT',
    body: file,
    headers: { 'Content-Type': contentType }
  })

  // 3. 录入数据库
  await $fetch(`${config.public.apiBase}/files/`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${session.value?.access_token}`
    },
    body: {
      filename: file.name,
      r2_key: presignedData.file_key,
      url: presignedData.public_url,
      size: file.size,
      mime_type: contentType,
      asset_id: null 
    }
  })
  
  // 记录最后一个文件的 URL 用于显示（可选）
  resultUrl.value = presignedData.public_url
}

// --- 交互事件处理 ---
const handleFileSelect = async (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files && input.files.length > 0) {
    // 将 FileList 转为数组
    const files = Array.from(input.files)
    await handleBatchUpload(files)
  }
  if (input) input.value = '' 
}

const onDrop = async (e: DragEvent) => {
  isDragging.value = false
  if (isUploading.value) return
  
  if (e.dataTransfer?.files && e.dataTransfer.files.length > 0) {
    const files = Array.from(e.dataTransfer.files)
    await handleBatchUpload(files)
  }
}

const triggerSelect = () => {
  if (!isUploading.value) fileInput.value?.click()
}
</script>

<template>
  <div class="upload-page">
    <div class="panel-header">
      <h1>UPLOAD <span class="sub">// 协议传输</span></h1>
    </div>

    <div class="upload-container">
      <div 
        class="drop-zone" 
        :class="{ 'dragging': isDragging, 'disabled': isUploading, 'success': uploadStatus === 'success' }"
        @dragover.prevent="isDragging = true"
        @dragleave.prevent="isDragging = false"
        @drop.prevent="onDrop"
        @click="triggerSelect"
      >
        <input type="file" ref="fileInput" @change="handleFileSelect" hidden multiple />
        
        <div class="zone-content">
          <div class="upload-icon"></div>
          
          <template v-if="isUploading">
            <h3>SYSTEM BUSY</h3>
            <p>正在上传...</p>
          </template>
          
          <template v-else-if="uploadStatus === 'success'">
            <h3 style="color: var(--c-success)">BATCH COMPLETE</h3>
            <p>Ready for next transmission</p>
          </template>

          <template v-else>
            <h3>INITIATE UPLOAD</h3>
            <p>拖拽或点击选择文件上传</p>
          </template>
        </div>
      </div>

      <div class="monitor-wrapper">
        
        <div v-if="uploadStatus === 'idle'" class="idle-monitor">
          <div class="idle-diamond-wrap">
            <div class="idle-diamond"></div>
            <div class="idle-diamond inner"></div>
          </div>
          <div class="idle-text">WAITING...</div>
        </div>

        <transition name="fade-scale">
          <div v-if="uploadStatus !== 'idle'" class="prts-core">
            
            <div class="bg-watermark">
              <span>P</span><span>R</span><span>T</span><span>S</span>
            </div>

            <div class="diamond-shifter">
              <svg class="diamond-svg" viewBox="0 0 300 300">
                <rect x="12" y="12" width="276" height="276" class="diamond-fill" 
                      :style="{ height: `${progress}%` }" />
                <rect x="5" y="5" width="290" height="290" class="diamond-border" />
              </svg>
              
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
                  <div class="status-text">
                    SYNCING ({{ completedFiles }}/{{ totalFiles }})...
                  </div>
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