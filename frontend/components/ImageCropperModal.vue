<script setup lang="ts">
import VueCropper from 'vue-cropperjs';
import 'cropperjs/dist/cropper.css';
import { X, Check } from 'lucide-vue-next';

const props = defineProps<{
  imgSrc: string // 接收原始图片 base64 或 url
}>()

// 使用 defineModel 来实现双向绑定显示状态
const isOpen = defineModel<boolean>('open', { default: false })
const emit = defineEmits(['confirm'])

const cropper = ref()
const isLoading = ref(false)

// 确认裁剪
const handleConfirm = () => {
  if (!cropper.value) return
  isLoading.value = true
  
  // 获取裁剪后的 Canvas (正方形，宽高 512px)
  cropper.value.getCroppedCanvas({
    width: 512,
    height: 512,
    imageSmoothingQuality: 'high'
  }).toBlob((blob: Blob) => {
    // 将 blob 传回父组件进行上传
    emit('confirm', blob)
    isLoading.value = false
    isOpen.value = false
  }, 'image/jpeg', 0.9) // 输出 90% 质量的 JPG
}

const close = () => { isOpen.value = false }
</script>

<template>
  <Teleport to="body">
    <div v-if="isOpen" class="cropper-modal-overlay">
      <div class="cropper-container">
        <div class="cropper-header">
          <span>ADJUST AVATAR // 调整图像</span>
          <button class="close-btn" @click="close"><X :size="20"/></button>
        </div>
        
        <div class="cropper-wrapper">
          <vue-cropper
            ref="cropper"
            :src="imgSrc"
            alt="Source Image"
            :aspect-ratio="1 / 1" 
            :view-mode="1"
            drag-mode="move"
            :guides="true"
            :background="false"
            preview=".cropper-preview"
          />
        </div>

        <div class="cropper-footer">
          <div class="preview-box">
            <span>PREVIEW:</span>
            <div class="cropper-preview"></div>
          </div>
          <div class="actions">
            <button class="btn cancel" @click="close">CANCEL</button>
            <button class="btn confirm" @click="handleConfirm" :disabled="isLoading">
              <Check :size="16" class="mr-1"/>
              {{ isLoading ? 'PROCESSING...' : 'CONFIRM' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
/* 独立的模态框样式 */
.cropper-modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.85); z-index: 10000;
  display: flex; align-items: center; justify-content: center;
  backdrop-filter: blur(5px);
}

.cropper-container {
  width: 90%; 
  max-width: 500px;
  /* 🟢 核心修复 1: 限制最大高度，防止弹窗超出屏幕 */
  max-height: 90vh; 
  background: var(--bg-card); border: 1px solid var(--border-light);
  display: flex; flex-direction: column;
}

.cropper-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 15px 20px; border-bottom: 1px solid var(--border-light);
  font-family: var(--font-mono); color: var(--text-main);
  flex-shrink: 0; /* 防止头部被压缩 */
}
.close-btn { background: none; border: none; color: var(--text-sub); cursor: pointer; }
.close-btn:hover { color: var(--c-danger); }

.cropper-wrapper {
  /* 🟢 核心修复 2: 使用 Flex 自适应高度，而不是固定高度 */
  flex: 1; 
  min-height: 300px; /* 保证最小可视区 */
  background: #000; 
  position: relative;
  overflow: hidden; /* 防止 Canvas 溢出 */
}

/* 覆盖 cropperjs 默认样式以匹配主题 */
:deep(.cropper-view-box), :deep(.cropper-face) {
  border-radius: 50%; /* 圆形裁剪框预览 */
  outline: 2px solid var(--c-brand);
}

.cropper-footer {
  padding: 15px 20px; border-top: 1px solid var(--border-light);
  display: flex; justify-content: space-between; align-items: center;
  flex-shrink: 0; /* 防止底部被压缩 */
  background: var(--bg-card); /* 确保背景不透明，防止穿透 */
  z-index: 10;
}

.preview-box { display: flex; align-items: center; gap: 10px; font-family: var(--font-mono); font-size: 12px; color: var(--text-sub); }
/* 圆形预览 */
.cropper-preview { width: 40px; height: 40px; border-radius: 50%; overflow: hidden; border: 1px solid var(--c-brand); }

.actions { display: flex; gap: 10px; }
.btn { padding: 8px 16px; font-family: var(--font-mono); font-weight: bold; cursor: pointer; border: 1px solid; transition: all 0.2s; display: flex; align-items: center; }
.mr-1 { margin-right: 4px; }
.btn.cancel { background: transparent; border-color: var(--text-sub); color: var(--text-sub); }
.btn.cancel:hover { border-color: var(--text-main); color: var(--text-main); }
.btn.confirm { background: var(--c-brand); border-color: var(--c-brand); color: #000; }
.btn.confirm:hover:not(:disabled) { box-shadow: 0 0 15px rgba(255, 215, 0, 0.3); }
.btn.confirm:disabled { opacity: 0.5; cursor: not-allowed; }
</style>