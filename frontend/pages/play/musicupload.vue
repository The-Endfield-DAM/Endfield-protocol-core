<script setup lang="ts">
import { UploadCloud, Music, FileText, Disc, ChevronLeft } from 'lucide-vue-next'

const config = useRuntimeConfig()
const session = useSupabaseSession()
const { success, error: showError } = useToast()
const router = useRouter()

// --- 表单状态 ---
const artistName = ref('')
const audioFile = ref<File | null>(null)
const coverFile = ref<File | null>(null)
const lyricFile = ref<File | null>(null)

// 🟢 新增：封面预览链接 (解决 Template 中无法使用 URL.createObjectURL 的问题)
const coverPreview = ref('')

// --- UI 状态 ---
const isUploading = ref(false)
const uploadProgress = ref(0)

// --- 文件选择处理 ---
const handleAudioSelect = (e: Event) => {
  const files = (e.target as HTMLInputElement).files
  if (files?.[0]) audioFile.value = files[0]
}

const handleCoverSelect = (e: Event) => {
  const files = (e.target as HTMLInputElement).files
  if (files?.[0]) {
    const file = files[0]
    coverFile.value = file
    
    // 🟢 核心修复：在 Script 中生成预览链接
    if (coverPreview.value) URL.revokeObjectURL(coverPreview.value) // 释放旧内存
    coverPreview.value = URL.createObjectURL(file)
  }
}

const handleLyricSelect = (e: Event) => {
  const files = (e.target as HTMLInputElement).files
  if (files?.[0]) lyricFile.value = files[0]
}

// --- 核心上传逻辑 ---
const uploadSingle = async (file: File, prefix: string) => {
  const contentType = file.type || (prefix === 'lrc' ? 'text/plain' : 'application/octet-stream')
  
  const presignedData = await $fetch(`${config.public.apiBase}/upload/presigned`, {
    method: 'POST',
    body: { 
      filename: `${prefix}_${Date.now()}_${file.name}`, 
      content_type: contentType 
    }
  }) as any

  await $fetch(presignedData.upload_url, {
    method: 'PUT',
    body: file,
    headers: { 'Content-Type': contentType }
  })

  return {
    key: presignedData.file_key,
    url: presignedData.public_url
  }
}

const startMusicUpload = async () => {
  if (!audioFile.value) return showError('MISSING AUDIO // 必须上传音频文件')
  
  isUploading.value = true
  uploadProgress.value = 10
  
  try {
    const uploadTasks: Promise<{ key: string, url: string }>[] = []
    
    // Task A: Audio
    uploadTasks.push(uploadSingle(audioFile.value, 'audio'))
    
    // Task B: Cover
    let coverKey = null
    if (coverFile.value) {
      uploadTasks.push(uploadSingle(coverFile.value, 'cover').then(res => {
        coverKey = res.key
        return res
      }))
    }
    
    // Task C: Lyric
    let lyricKey = null
    if (lyricFile.value) {
      uploadTasks.push(uploadSingle(lyricFile.value, 'lrc').then(res => {
        lyricKey = res.key
        return res
      }))
    }
    
    uploadProgress.value = 50
    
    const results = await Promise.all(uploadTasks)
    const audioResult = results[0]
    if (!audioResult) {
      throw new Error ('AUDIO UPLOAD FAILED // 上传失败')
    }
    
    uploadProgress.value = 80

    // 写入数据库
    await $fetch(`${config.public.apiBase}/files/`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${session.value?.access_token}` },
      body: {
        filename: audioFile.value.name,
        r2_key: audioResult.key,
        url: audioResult.url,
        size: audioFile.value.size,
        mime_type: audioFile.value.type || 'audio/mpeg',
        
        artist: artistName.value || 'Unknown Artist',
        cover_r2_key: coverKey,
        lyrics_r2_key: lyricKey,
        
        asset_id: null
      }
    })

    uploadProgress.value = 100
    success('TRACK UPLOADED // 唱片已归档')
    
    setTimeout(() => router.push('/play'), 1000)

  } catch (err) {
    console.error(err)
    showError('UPLOAD FAILED // 传输中断')
  } finally {
    isUploading.value = false
  }
}

const goBack = () => router.push('/play')
</script>

<template>
  <div class="music-upload-page">
    
    <div class="page-header">
      <button class="back-btn" @click="goBack">
        <ChevronLeft :size="24" />
      </button>
      <div class="header-title">
        <h1>ENDFIELD RECORDS <span class="sub">// 唱片录入</span></h1>
      </div>
    </div>

    <div class="upload-container">
      
      <div class="form-panel">
        
        <div class="form-group">
          <label class="input-label">ARTIST NAME / 艺术家</label>
          <input type="text" v-model="artistName" class="industrial-input" placeholder="UNIDENTIFIED" />
        </div>

        <div class="form-group">
          <label class="input-label">AUDIO SOURCE / 音频母带 <span class="req">*</span></label>
          <div class="file-selector" :class="{ active: audioFile }">
            <input type="file" accept="audio/*" @change="handleAudioSelect" />
            <div class="selector-content">
              <Music :size="24" />
              <span class="filename">{{ audioFile ? audioFile.name : 'CLICK TO SELECT AUDIO' }}</span>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label class="input-label">LYRICS DATA / 歌词文本 (.lrc)</label>
          <div class="file-selector" :class="{ active: lyricFile }">
            <input type="file" accept=".lrc,.txt" @change="handleLyricSelect" />
            <div class="selector-content">
              <FileText :size="24" />
              <span class="filename">{{ lyricFile ? lyricFile.name : 'OPTIONAL LRC FILE' }}</span>
            </div>
          </div>
        </div>

      </div>

      <div class="visual-panel">
        <div class="cover-upload-box">
          <label class="input-label">ALBUM ART / 封面</label>
          <div class="cover-preview" :class="{ 'has-img': coverPreview }">
            <input type="file" accept="image/*" @change="handleCoverSelect" />
            
            <img v-if="coverPreview" :src="coverPreview" class="cover-img" />
            
            <div v-else class="placeholder">
              <Disc :size="48" opacity="0.5" />
              <span>DRAG OR CLICK</span>
            </div>
          </div>
        </div>

        <button class="upload-btn" @click="startMusicUpload" :disabled="isUploading || !audioFile">
          <template v-if="isUploading">
            UPLOADING... {{ uploadProgress }}%
          </template>
          <template v-else>
            <UploadCloud :size="20" />
            INITIATE TRANSFER
          </template>
        </button>
      </div>

    </div>
  </div>
</template>

<style scoped>
.music-upload-page {
  padding: 40px;
  height: 100%;
  overflow-y: auto;
  background: var(--bg-base);
}

.page-header {
  display: flex; align-items: center; gap: 20px;
  margin-bottom: 40px; border-bottom: 1px solid var(--border-light); padding-bottom: 15px;
}
.back-btn {
  background: transparent; border: 1px solid var(--border-light);
  color: var(--text-sub); width: 40px; height: 40px;
  display: flex; align-items: center; justify-content: center; cursor: pointer;
}
.back-btn:hover { border-color: var(--c-brand); color: var(--c-brand); }
.header-title h1 { font-size: 24px; color: var(--text-main); margin: 0; letter-spacing: 2px; }
.header-title .sub { font-size: 12px; color: var(--c-brand); margin-left: 10px; }

.upload-container {
  display: grid; grid-template-columns: 1.5fr 1fr; gap: 60px; max-width: 1200px;
}

/* 表单样式 */
.form-group { margin-bottom: 30px; }
.input-label { display: block; font-family: var(--font-mono); font-size: 12px; color: var(--text-sub); margin-bottom: 10px; }
.req { color: var(--c-danger); }

.industrial-input {
  width: 100%; background: rgba(255,255,255,0.03); border: 1px solid var(--border-light);
  padding: 15px; color: var(--text-main); font-family: var(--font-sans); outline: none;
}
.industrial-input:focus { border-color: var(--c-brand); background: rgba(0,0,0,0.3); }

.file-selector {
  position: relative; border: 1px dashed var(--border-light); background: rgba(0,0,0,0.2);
  padding: 20px; transition: all 0.3s; cursor: pointer;
}
.file-selector:hover { border-color: var(--c-brand); background: rgba(255,215,0,0.05); }
.file-selector.active { border-style: solid; border-color: var(--c-success); background: rgba(74,222,128,0.05); }
.file-selector input { position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; cursor: pointer; }
.selector-content { display: flex; align-items: center; gap: 15px; color: var(--text-sub); }
.active .selector-content { color: var(--c-success); }
.filename { font-family: var(--font-mono); font-size: 14px; }

/* 封面上传 */
.cover-preview {
  width: 100%; aspect-ratio: 1; background: #000; border: 1px solid var(--border-light);
  position: relative; display: flex; align-items: center; justify-content: center;
  overflow: hidden; transition: all 0.3s;
}
.cover-preview:hover { border-color: var(--c-brand); }
.cover-preview input { position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; cursor: pointer; z-index: 2; }
.cover-img { width: 100%; height: 100%; object-fit: cover; }
.placeholder { display: flex; flex-direction: column; align-items: center; gap: 10px; color: var(--text-sub); font-family: var(--font-mono); font-size: 12px; }

/* 提交按钮 */
.upload-btn {
  width: 100%; margin-top: 30px; padding: 20px;
  background: var(--c-brand); color: #000; border: none;
  font-family: var(--font-mono); font-weight: 900; font-size: 16px; letter-spacing: 2px;
  cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px;
  clip-path: polygon(20px 0, 100% 0, 100% calc(100% - 20px), calc(100% - 20px) 100%, 0 100%, 0 20px);
  transition: all 0.2s;
}
.upload-btn:hover:not(:disabled) { transform: translate(-2px, -2px); box-shadow: 5px 5px 0 rgba(255,255,255,0.1); }
.upload-btn:disabled { opacity: 0.5; cursor: wait; background: #555; color: #999; }

@media (max-width: 768px) {
  .upload-container { grid-template-columns: 1fr; gap: 30px; }
  .cover-preview { max-width: 300px; margin: 0 auto; }
}
</style>