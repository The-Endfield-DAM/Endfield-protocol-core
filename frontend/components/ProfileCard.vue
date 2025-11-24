<script setup lang="ts">
import { User, Shield, Building, Hash, Edit2, Check, X, Camera } from 'lucide-vue-next'

const props = defineProps<{
  user: {
    code: string
    role: string
    department?: string
    avatar_url?: string
    type: string
  }
}>()

const emit = defineEmits(['refresh'])
const config = useRuntimeConfig()
const session = useSupabaseSession()

// 🟢 1. 引入 Toast 系统
const { success, error: showError } = useToast()

const isLoading = ref(false)

// --- 状态管理 (已精简) ---
// 仅保留代号编辑和裁剪相关的状态
const isEditingCode = ref(false)
const newCodeStr = ref('')
const showCropper = ref(false)
const cropperImgSrc = ref('')
const fileInput = ref<HTMLInputElement | null>(null)

// 🟢 监听器优化：只监听 code 变化
watch(() => props.user?.code, (newVal) => {
  if (newVal) newCodeStr.value = newVal
}, { immediate: true })

// 智能头像计算属性
const displayAvatar = computed(() => {
  if (!props.user) return ''
  if (props.user.avatar_url) return props.user.avatar_url
  
  const isAdmin = props.user.role === 'admin'
  const name = isAdmin ? 'AD' : 'TP'
  const bg = isAdmin ? 'FFD700' : '333333'
  const color = isAdmin ? '000000' : 'E5E5E5'
  return `https://ui-avatars.com/api/?name=${name}&background=${bg}&color=${color}&size=256&bold=true&length=2&font-size=0.4`
})

// --- 代号编辑逻辑 ---
const startEditCode = () => {
  newCodeStr.value = props.user?.code || ''
  isEditingCode.value = true
}
const cancelEditCode = () => { isEditingCode.value = false }

const saveCode = async () => {
  // 如果没变或是空的，直接关闭不请求
  if (!newCodeStr.value.trim() || newCodeStr.value === props.user.code) {
    isEditingCode.value = false
    return
  }

  isLoading.value = true
  try {
    await $fetch(`${config.public.apiBase}/users/me`, {
      method: 'PATCH',
      headers: { Authorization: `Bearer ${session.value?.access_token}` },
      body: { code: newCodeStr.value }
    })
    
    isEditingCode.value = false
    emit('refresh')
    // 🟢 替换 Alert：成功反馈
    success('CODENAME UPDATED // 代号已更新')
    
  } catch (err) {
    // 🟢 替换 Alert：错误反馈
    showError('UPDATE FAILED // 更新失败')
  } finally {
    isLoading.value = false
  }
}

// --- 头像上传逻辑 ---
const triggerFileSelect = () => { fileInput.value?.click() }

const onFileSelected = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (!input.files?.[0]) return
  const file = input.files[0]
  
  const reader = new FileReader()
  reader.onload = (e) => {
    if (typeof e.target?.result === 'string') {
      cropperImgSrc.value = e.target.result
      showCropper.value = true // 打开裁剪弹窗
    }
  }
  reader.readAsDataURL(file)
  input.value = ''
}

const onCropConfirmed = async (imageBlob: Blob) => {
  isLoading.value = true
  try {
    const filename = `avatar_${props.user.type}_${Date.now()}.jpg`

    // 1. 获取签名
    const presignedData = await $fetch(`${config.public.apiBase}/upload/presigned`, {
      method: 'POST',
      body: { filename, content_type: 'image/jpeg' }
    }) as any

    // 2. 直传 R2
    await $fetch(presignedData.upload_url, {
      method: 'PUT',
      body: imageBlob,
      headers: { 'Content-Type': 'image/jpeg' }
    })

    // 3. 更新后端 (存 Key)
    await $fetch(`${config.public.apiBase}/users/me`, {
      method: 'PATCH',
      headers: { Authorization: `Bearer ${session.value?.access_token}` },
      body: { avatar_url: presignedData.file_key } 
    })

    emit('refresh')
    // 🟢 替换 Alert：成功反馈
    success('UPDATED SUCCESS // 头像已更新')

  } catch (err) {
    console.error(err)
    // 🟢 替换 Alert：错误反馈
    showError('UPLOAD FAILED // 上传中断')
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="profile-card">
    <div class="card-left relative-container">
      <div class="avatar-frame">
        <img :src="displayAvatar" alt="AVATAR" class="avatar-img" />
        <div class="scan-line"></div>
      </div>
      
      <button class="camera-btn" @click="triggerFileSelect" :disabled="isLoading">
        <Camera :size="16" />
      </button>
      <input type="file" ref="fileInput" @change="onFileSelected" hidden accept="image/png,image/jpeg,image/webp" />
    </div>

    <div class="card-right">
      <div class="info-row main editable-row">
        <div class="code-wrapper">
          <span class="label">CODENAME</span>
          <div v-if="isEditingCode" class="inline-editor">
            <input v-model="newCodeStr" class="edit-input code-input" :disabled="isLoading" @keyup.enter="saveCode" />
            <div class="editor-actions">
               <button class="mini-btn save" @click="saveCode" :disabled="isLoading"><Check :size="14"/></button>
               <button class="mini-btn cancel" @click="cancelEditCode" :disabled="isLoading"><X :size="14"/></button>
            </div>
          </div>
          <div v-else class="code-display">
            <span class="value code">{{ user?.code || 'UNKNOWN' }}</span>
            <button class="mini-btn edit" @click="startEditCode"><Edit2 :size="14" /></button>
          </div>
        </div>
      </div>

      <div class="info-grid">
        <div class="info-item">
          <Shield :size="14" class="icon"/>
          <span class="label">CLEARANCE</span>
          <span class="value" :class="user?.role">{{ user?.role ? user.role.toUpperCase() : 'UNKNOWN' }}</span>
        </div>
        <div class="info-item">
          <Building :size="14" class="icon"/>
          <span class="label">DEPT</span>
          <span class="value">{{ user?.department || 'PENDING' }}</span>
        </div>
        <div class="info-item">
          <Hash :size="14" class="icon"/>
          <span class="label">TYPE</span>
          <span class="value">{{ user?.type ? user.type.toUpperCase() : 'UNKNOWN' }}</span>
        </div>
      </div>
    </div>
    
    <div class="bg-text">IDENTITY</div>

    <ImageCropperModal
      v-model:open="showCropper"
      :imgSrc="cropperImgSrc"
      @confirm="onCropConfirmed"
    />
  </div>
</template>