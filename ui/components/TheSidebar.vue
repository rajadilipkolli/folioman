<template>
  <div>
    <!-- Sidebar content here -->
  </div>
</template>

<script setup>
import { ref } from 'vue'

const menu = ref([
  { title: 'Dashboard', icon: 'pi pi-chart-bar', href: '/' },
  { title: 'Portfolio', icon: 'pi pi-list', href: '/portfolio' },
])

const onToggleCollapse = () => {
  console.log('Sidebar toggled')
}
</script>

<style scoped>
/* Add your styles here */
</style>
