<script setup lang="ts">
// 设置页面元数据
useHead({
  title: 'Editor Module - Under Construction'
})
</script>

<template>
  <div class="editor-placeholder">
    <div class="construction-notice">
      <div class="icon">🔧</div>
      <h1 class="module-title">EDITOR MODULE</h1>
      <h2 class="module-subtitle">编辑器模块</h2>
      <p class="status-text">[ UNDER CONSTRUCTION ]</p>
      <p class="desc-text">此功能正在开发中，敬请期待</p>
      <button class="back-btn" @click="$router.push('/')">
        ← 返回主页
      </button>
    </div>
  </div>
</template>

<style scoped>
.editor-placeholder {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0a0a0a;
  background-image: 
    linear-gradient(0deg, rgba(255,215,0,0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,215,0,0.02) 1px, transparent 1px);
  background-size: 20px 20px;
}

.construction-notice {
  text-align: center;
  padding: 60px 40px;
  max-width: 600px;
}

.icon {
  font-size: 120px;
  margin-bottom: 30px;
  animation: rotate 4s linear infinite;
  filter: grayscale(0.3);
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.module-title {
  font-size: 42px;
  font-weight: 900;
  font-family: var(--font-mono);
  letter-spacing: 4px;
  color: var(--text-main);
  margin-bottom: 10px;
}

.module-subtitle {
  font-size: 20px;
  color: var(--text-sub);
  font-weight: 300;
  margin-bottom: 40px;
}

.status-text {
  color: var(--c-brand);
  font-family: var(--font-mono);
  font-size: 16px;
  margin: 30px 0;
  letter-spacing: 2px;
}

.desc-text {
  color: var(--text-sub);
  font-size: 14px;
  margin-bottom: 40px;
}

.back-btn {
  background: transparent;
  border: 1px solid var(--c-brand);
  color: var(--c-brand);
  padding: 12px 30px;
  font-family: var(--font-mono);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.back-btn:hover {
  background: var(--c-brand);
  color: #000;
  box-shadow: 0 0 20px rgba(255,215,0,0.3);
}
</style>