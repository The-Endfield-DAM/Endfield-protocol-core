<script setup lang="ts">
import { Trash2, Download, CheckSquare, XSquare } from 'lucide-vue-next'

const session = useSupabaseSession()
const config = useRuntimeConfig()
const { success, error: showError } = useToast()

interface FileRecord {
  id: number
  filename: string
  mime_type: string
  size: number
  url: string
  created_at: string
}

// --- 数据获取 ---
const { data: files, pending, refresh, error } = await useFetch<FileRecord[]>('/files/', {
  baseURL: config.public.apiBase,
  onRequest({ options }) {
    const token = session.value?.access_token
    if (token) options.headers = { ...options.headers, Authorization: `Bearer ${token}` }
  },
  watch: [session],
  server: false,
  lazy: true,
  timeout: 60000
})

watch(error, (newErr) => {
  if (newErr) {
    console.error('Wiki 数据加载异常:', newErr)
    if (newErr.statusCode === 403) console.warn('ACCESS DENIED // 请检查登录状态')
  }
})

// --- 多选逻辑 ---
const selectedIds = ref<Set<number>>(new Set())

const toggleSelect = (id: number) => {
  if (selectedIds.value.has(id)) selectedIds.value.delete(id)
  else selectedIds.value.add(id)
}

const toggleSelectAll = () => {
  if (!files.value) return
  if (selectedIds.value.size === files.value.length) selectedIds.value.clear()
  else files.value.forEach(f => selectedIds.value.add(f.id))
}

// --- 删除与弹窗状态管理 ---
const showDeleteModal = ref(false)
const targetFile = ref<FileRecord | null>(null)
const isBatchMode = ref(false) // 🟢 新增：标记当前弹窗是否为批量模式

// 1. 打开单删确认框
const openDeleteModal = (file: FileRecord) => {
  isBatchMode.value = false
  targetFile.value = file
  showDeleteModal.value = true
}

// 2. 打开批删确认框 (替换了原来的 confirmBatchDelete)
const triggerBatchDelete = () => {
  if (selectedIds.value.size === 0) return
  isBatchMode.value = true
  showDeleteModal.value = true
}

// 3. 统一确认入口 (弹窗回调)
const handleDeleteConfirm = async () => {
  if (isBatchMode.value) {
    await executeBatchDelete()
  } else {
    await executeSingleDelete()
  }
}

// --- 执行逻辑 ---

// 执行单删
const executeSingleDelete = async () => {
  if (!targetFile.value) return
  try {
    await $fetch(`${config.public.apiBase}/files/${targetFile.value.id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${session.value?.access_token}` }
    })
    success(`ASSET DELETED // ${targetFile.value.filename}`)
    refresh()
  } catch (err) {
    showError('DELETE FAILED // 权限不足或系统错误')
  }
}

// 执行批删
const executeBatchDelete = async () => {
  try {
    await $fetch(`${config.public.apiBase}/files/batch-delete`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${session.value?.access_token}` },
      body: Array.from(selectedIds.value)
    })
    
    success(`BATCH DELETE COMPLETE // 已销毁 ${selectedIds.value.size} 个文件`)
    selectedIds.value.clear()
    refresh()
  } catch (err) {
    showError('BATCH DELETE FAILED // 批量删除失败')
  }
}

// 批量下载
const batchDownload = () => {
  if (!files.value) return
  const targets = files.value.filter(f => selectedIds.value.has(f.id))
  targets.forEach((file, index) => {
    setTimeout(() => {
      const link = document.createElement('a')
      link.href = file.url
      link.download = file.filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }, index * 500)
  })
  success(`STARTING DOWNLOAD // ${targets.length} FILES`)
}
</script>

<template>
  <div class="wiki-page">
    <div class="page-header">
      <div class="header-title">
        <h1>ARCHIVE_DATABASE</h1>
        <div class="subtitle">// 协议档案库</div>
      </div>
      
      <div class="header-actions">
        <button class="refresh-btn" @click="toggleSelectAll">
          {{ selectedIds.size === files?.length && files?.length > 0 ? '[ DESELECT ALL ]' : '[ SELECT ALL ]' }}
        </button>
        <button class="refresh-btn" @click="refresh()">REFRESH</button>
      </div>
    </div>

    <div v-if="pending" class="loading-state">[ CONNECTING TO NEURAL NETWORK... ]</div>
    <div v-else-if="!files || files.length === 0" class="empty-state">[ NO DATA ENTRIES FOUND ]</div>

    <div v-else class="file-list">
      <FileListItem
        v-for="file in files"
        :key="file.id"
        :id="file.id"
        :filename="file.filename"
        :mimeType="file.mime_type"
        :size="file.size"
        :url="file.url"
        :date="file.created_at"
        :selected="selectedIds.has(file.id)"
        @toggle-select="toggleSelect(file.id)"
        @delete="openDeleteModal(file)" 
      />
    </div>

    <Transition name="slide-up">
      <div v-if="selectedIds.size > 0" class="batch-bar">
        <div class="batch-info">
          <CheckSquare :size="20" />
          <span>SELECTED: <span class="highlight">{{ selectedIds.size }}</span> ASSETS</span>
        </div>
        <div class="batch-actions">
          <button class="batch-btn download" @click="batchDownload">
            <Download :size="16" /> DOWNLOAD
          </button>
          
          <button class="batch-btn delete" @click="triggerBatchDelete">
            <Trash2 :size="16" /> DELETE
          </button>
          
          <button class="batch-btn close" @click="selectedIds.clear()">
            <XSquare :size="20" />
          </button>
        </div>
      </div>
    </Transition>

    <DeleteModal 
      v-model="showDeleteModal" 
      :file-name="isBatchMode ? `[ ${selectedIds.size} SELECTED ASSETS ]` : targetFile?.filename"
      @confirm="handleDeleteConfirm"
    />
  </div>
</template>

<style scoped>
.header-actions { display: flex; gap: 10px; }

.batch-bar {
  position: fixed;
  bottom: 30px; left: 50%; transform: translateX(-50%);
  z-index: 1000;
  
  display: flex; align-items: center; gap: 30px;
  padding: 15px 30px;
  
  background: rgba(0, 0, 0, 0.9);
  border: 1px solid var(--c-brand);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8), 0 0 20px rgba(255, 215, 0, 0.2);
  border-radius: 4px;
  backdrop-filter: blur(10px);
}

.batch-info {
  display: flex; align-items: center; gap: 10px;
  font-family: var(--font-mono); color: var(--text-main); font-size: 14px;
}
.highlight { color: var(--c-brand); font-weight: bold; font-size: 18px; margin: 0 5px; }

.batch-actions { display: flex; align-items: center; gap: 15px; }

.batch-btn {
  display: flex; align-items: center; gap: 8px;
  background: transparent; border: 1px solid var(--text-sub);
  color: var(--text-main); padding: 8px 16px;
  font-family: var(--font-mono); font-size: 12px; cursor: pointer;
  transition: all 0.2s;
}
.batch-btn:hover { border-color: #FFF; background: rgba(255,255,255,0.1); }

.batch-btn.delete { border-color: var(--c-danger); color: var(--c-danger); }
.batch-btn.delete:hover { background: var(--c-danger); color: #000; }

.batch-btn.download { border-color: var(--c-success); color: var(--c-success); }
.batch-btn.download:hover { background: var(--c-success); color: #000; }

.batch-btn.close { border: none; padding: 0; color: var(--text-sub); }
.batch-btn.close:hover { color: var(--c-brand); transform: scale(1.1); background: none; }

.slide-up-enter-active, .slide-up-leave-active { transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
.slide-up-enter-from, .slide-up-leave-to { opacity: 0; transform: translate(-50%, 50px); }

@media (max-width: 768px) {
  .batch-bar { 
    width: 90%; bottom: 80px;
    flex-direction: column; gap: 15px; padding: 15px;
  }
  .batch-actions { width: 100%; justify-content: space-between; }
  .batch-btn { flex: 1; justify-content: center; }
  .batch-btn.close { flex: 0; }
}
</style>