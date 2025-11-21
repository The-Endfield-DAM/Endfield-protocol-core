<script setup lang="ts">
// 接收父组件传来的数据 props
defineProps<{
  code: string
  name: string
  type: string
  status: string
}>()

// 状态颜色逻辑
const getStatusColor = (s: string) => {
  if (s === 'Active') return 'var(--c-success)'
  if (s === 'Warning') return 'var(--c-brand)'
  return 'var(--c-danger)'
}
</script>

<template>
  <div class="asset-card">
    <div class="card-header">
      <span>{{ code }}</span>
      <span class="status-dot" :style="{ color: getStatusColor(status), backgroundColor: getStatusColor(status) }"></span>
    </div>
    <h3 class="card-title">{{ name }}</h3>
    <div class="card-type">{{ type }}</div>
  </div>
</template>