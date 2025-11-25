<script setup lang="ts">
import { Edit2, Check, X, FileText, ChevronDown } from 'lucide-vue-next'

const props = defineProps<{
  user: {
    gender?: string
    age?: number
    address?: string
    bio?: string
  }
}>()

const emit = defineEmits(['refresh'])
const config = useRuntimeConfig()
const session = useSupabaseSession()
const { success, error: showError } = useToast()

const isEditing = ref(false)
const isLoading = ref(false)

// 🟢 新增：下拉菜单状态
const isGenderDropdownOpen = ref(false)
const genderOptions = ['男', '女']

// 表单数据
const formData = ref({
  gender: '',
  age: null as number | null,
  address: '',
  bio: ''
})

const initForm = () => {
  formData.value = {
    gender: props.user?.gender || '',
    age: props.user?.age || null,
    address: props.user?.address || '',
    bio: props.user?.bio || ''
  }
  isGenderDropdownOpen.value = false // 重置下拉状态
}

watch(() => props.user, initForm, { immediate: true, deep: true })

const startEdit = () => {
  initForm()
  isEditing.value = true
}

const cancelEdit = () => {
  isEditing.value = false
  initForm()
}

// 🟢 新增：切换下拉菜单
const toggleGenderDropdown = () => {
  if (!isEditing.value) return
  isGenderDropdownOpen.value = !isGenderDropdownOpen.value
}

// 🟢 新增：选择性别
const selectGender = (val: string) => {
  formData.value.gender = val
  isGenderDropdownOpen.value = false
}

const saveDossier = async () => {
  isLoading.value = true
  try {
    await $fetch(`${config.public.apiBase}/users/me`, {
      method: 'PATCH',
      headers: { Authorization: `Bearer ${session.value?.access_token}` },
      body: {
        gender: formData.value.gender,
        age: formData.value.age,
        address: formData.value.address,
        bio: formData.value.bio
      }
    })
    
    success('ARCHIVE UPDATED // 档案已归档')
    isEditing.value = false
    isGenderDropdownOpen.value = false
    emit('refresh')
  } catch (err) {
    showError('UPDATE FAILED // 数据写入错误')
    console.error(err)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="dossier-panel">
    <div class="dossier-header">
      <div class="dossier-title">
        <FileText :size="16" />
        PERSONAL ARCHIVE // 基础资料
      </div>
      
      <div class="actions">
        <div v-if="isEditing" class="edit-actions">
          <button class="action-btn save" @click="saveDossier" :disabled="isLoading">
            <Check :size="16" />
          </button>
          <button class="action-btn cancel" @click="cancelEdit" :disabled="isLoading">
            <X :size="16" />
          </button>
        </div>
        <button v-else class="action-btn" @click="startEdit">
          <Edit2 :size="16" />
        </button>
      </div>
    </div>

    <div class="dossier-body">
      <div class="form-item">
        <span class="label">GENDER / 性别</span>
        <div v-if="isEditing" class="custom-select-container" @click.stop="toggleGenderDropdown">
          <div class="edit-input select-trigger">
            <span>{{ formData.gender || 'SELECT GENDER' }}</span>
            <ChevronDown 
              :size="16" 
              class="dropdown-icon" 
              :class="{ 'rotate': isGenderDropdownOpen }" 
            />
          </div>
          
          <Transition name="dropdown-slide">
            <div v-if="isGenderDropdownOpen" class="select-options">
              <div 
                v-for="opt in genderOptions" 
                :key="opt" 
                class="select-option"
                :class="{ 'active': formData.gender === opt }"
                @click.stop="selectGender(opt)"
              >
                {{ opt }}
              </div>
            </div>
          </Transition>
        </div>
        
        <div v-else class="value-display" :class="{ empty: !user?.gender }">
          {{ user?.gender || 'NOT RECORDED' }}
        </div>
      </div>

      <div class="form-item">
        <span class="label">AGE / 年龄</span>
        <div v-if="isEditing">
          <input v-model.number="formData.age" type="number" class="edit-input" placeholder="0" />
        </div>
        <div v-else class="value-display" :class="{ empty: !user?.age }">
          {{ user?.age ? `${user.age} YEARS` : 'UNKNOWN' }}
        </div>
      </div>

      <div class="form-item">
        <span class="label">LOCATION / 归属地</span>
        <div v-if="isEditing">
          <input v-model="formData.address" class="edit-input" placeholder="NO DATA" />
        </div>
        <div v-else class="value-display" :class="{ empty: !user?.address }">
          {{ user?.address || 'NO DATA' }}
        </div>
      </div>

      <div class="form-item full-width">
        <span class="label">BIOGRAPHY / 个人简介</span>
        <div v-if="isEditing">
          <textarea v-model="formData.bio" class="edit-textarea" placeholder="在这里输入履历摘要或个人信条..."></textarea>
        </div>
        <div v-else class="value-display" :class="{ empty: !user?.bio }">
          {{ user?.bio || 'NO ENTRY' }}
        </div>
      </div>
    </div>
  </div>
</template>