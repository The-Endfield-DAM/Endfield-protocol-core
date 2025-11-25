<script setup lang="ts">
import { Check, ChevronLeft, ChevronRight, UserPlus } from 'lucide-vue-next'

const config = useRuntimeConfig()
const session = useSupabaseSession()
const { success, error: showError } = useToast()

// 分页参数
const page = ref(1)
const pageSize = 10 // 🟢 设定每页 10 条

// 数据获取
const { data: auditData, pending, refresh } = await useFetch<any>('/admin/applications', {
  baseURL: config.public.apiBase,
  onRequest({ options }) {
    const token = session.value?.access_token
    if (token) options.headers = { Authorization: `Bearer ${token}` } as any
  },
  query: computed(() => ({ page: page.value, size: pageSize })),
  watch: [page], // 翻页自动刷新
  server: false,
  lazy: true
})

// 审批动作状态
const showConfirmModal = ref(false)
const targetUser = ref<any>(null)
const isProcessing = ref(false)

// 1. 打开确认框
const openApproveModal = (user: any) => {
  targetUser.value = user
  showConfirmModal.value = true
}

// 2. 执行批准
const confirmApprove = async () => {
  if (!targetUser.value) return
  isProcessing.value = true
  
  try {
    await $fetch(`${config.public.apiBase}/admin/approve/${targetUser.value.id}`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${session.value?.access_token}` }
    })
    
    success(`OPERATOR ${targetUser.value.code} APPROVED // 已归入基建工程部`)
    refresh() // 刷新列表
  } catch (err) {
    console.error(err)
    showError('APPROVAL FAILED // 操作失败')
  } finally {
    isProcessing.value = false
    showConfirmModal.value = false
    targetUser.value = null
  }
}

// 分页计算
const totalPages = computed(() => auditData.value?.pages || 1)
const prevPage = () => { if (page.value > 1) page.value-- }
const nextPage = () => { if (page.value < totalPages.value) page.value++ }
</script>

<template>
  <div class="audit-panel">
    <div class="audit-header">
      <div>APPLICATION CODE</div>
      <div>CONTACT EMAIL</div>
      <div>APPLIED AT</div>
      <div style="text-align: right">ACTION</div>
    </div>

    <div v-if="pending" class="empty-list">
      SCANNING DATABASE...
    </div>

    <div v-else-if="!auditData?.items || auditData.items.length === 0" class="empty-list">
      [ NO PENDING APPLICATIONS ]
    </div>

    <div v-else class="audit-list">
      <div v-for="item in auditData.items" :key="item.id" class="audit-item">
        <div class="col-code">{{ item.code }}</div>
        <div class="col-email">{{ item.email }}</div>
        <div class="col-date">{{ new Date(item.applied_at).toLocaleDateString() }}</div>
        <div class="col-action">
          <button class="approve-btn" @click="openApproveModal(item)">
            <UserPlus :size="14" />
            APPROVE
          </button>
        </div>
      </div>
    </div>

    <div class="pagination" v-if="totalPages > 1">
      <button class="page-btn" @click="prevPage" :disabled="page === 1">
        <ChevronLeft :size="16" />
      </button>
      <span>PAGE {{ page }} / {{ totalPages }}</span>
      <button class="page-btn" @click="nextPage" :disabled="page === totalPages">
        <ChevronRight :size="16" />
      </button>
    </div>

    <ActionModal 
      v-model="showConfirmModal"
      title="确认审批"
      message="高危操作：确认要同意此用户成为后台管理员吗？"
      :sub-message="targetUser ? `CODE: ${targetUser.code}` : ''"
      @confirm="confirmApprove"
    />
  </div>
</template>