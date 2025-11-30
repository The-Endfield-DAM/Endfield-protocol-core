<script setup lang="ts">
defineProps<{
  icon: string
  title: string
  subtitle: string
  status: string
  meta: string
  route: string
  disabled?: boolean
}>()
</script>

<template>
  <NuxtLink 
    :to="route" 
    class="module-card" 
    :class="{ disabled: disabled }"
  >
    <div class="card-icon">{{ icon }}</div>
    <div class="card-title">{{ title }}</div>
    <div class="card-subtitle">{{ subtitle }}</div>
    <div class="card-footer">
      <span class="status-badge">{{ status }}</span>
      <span class="meta-info">{{ meta }}</span>
    </div>
  </NuxtLink>
</template>

<style scoped>
.module-card {
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid var(--border-light);
  padding: 40px 30px;
  text-align: center;
  text-decoration: none;
  color: var(--text-main);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.module-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: linear-gradient(135deg, rgba(255,215,0,0.05) 0%, transparent 50%);
  opacity: 0;
  transition: opacity 0.3s;
}

.module-card:hover {
  transform: translateY(-8px);
  border-color: var(--c-brand);
  box-shadow: 
    0 20px 40px rgba(0,0,0,0.8),
    0 0 30px rgba(255,215,0,0.3);
}

.module-card:hover::before {
  opacity: 1;
}

.module-card.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.module-card.disabled:hover {
  transform: none;
  border-color: var(--border-light);
  box-shadow: none;
}

.card-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.card-title {
  font-size: 18px;
  font-weight: 700;
  font-family: var(--font-mono);
  letter-spacing: 2px;
  margin-bottom: 8px;
  color: var(--text-main);
}

.card-subtitle {
  font-size: 12px;
  color: var(--text-sub);
  margin-bottom: 24px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 20px;
  border-top: 1px solid var(--border-light);
  font-size: 11px;
}

.status-badge {
  color: var(--c-success);
  font-family: var(--font-mono);
}

.module-card.disabled .status-badge {
  color: var(--c-brand);
}

.meta-info {
  color: var(--text-sub);
  font-family: var(--font-mono);
}
</style>