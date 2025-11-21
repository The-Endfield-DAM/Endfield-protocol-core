<script setup lang="ts">
interface Asset {
  id: number
  name: string
  code: string
  type: string
  status: string
}

// 请求后端
const { data: assets, pending, error } = await useFetch<Asset[]>('http://127.0.0.1:8000/assets/')
</script>

<template>
  <div>
    <h1 style="font-size: 24px; margin-bottom: 24px; font-weight: 300;">
      DASHBOARD <span style="color: var(--text-sub)">// OVERVIEW</span>
    </h1>

    <div v-if="pending">Loading Protocol...</div>
    <div v-else-if="error" style="color: var(--c-danger)">Signal Lost.</div>
    
    <div v-else class="asset-grid">
      <!-- 使用刚才封装的组件 -->
      <AssetCard 
        v-for="asset in assets" 
        :key="asset.id"
        :code="asset.code"
        :name="asset.name"
        :type="asset.type"
        :status="asset.status"
      />
    </div>
  </div>
</template>