<script setup lang="ts">
import { Smartphone } from 'lucide-vue-next'
</script>

<template>
  <div class="mobile-blocker">
    <div class="content">
      <div class="icon-wrapper">
        <Smartphone :size="64" class="phone-icon" />
      </div>
      <h2 class="title">W A R N I N G !</h2>
      <p class="subtitle">// 请旋转设备以接入终端</p>
      <div class="decor-line"></div>
      <p class="info">Rotate display for optimal viewing experience.</p>
    </div>
  </div>
</template>