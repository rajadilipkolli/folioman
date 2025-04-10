<template>
  <div>
    <!-- Header content here -->
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRuntimeConfig, useState } from '#app'

const dropdownOpen = ref(false)
const profileIcon = computed(() => (dropdownOpen.value ? 'pi pi-angle-up' : 'pi pi-angle-down'))

// Replace $auth with a state-based approach
const user = useState('user', () => ({ firstname: 'John', username: 'johndoe' }))
const displayName = computed(() => user.value.firstname || user.value.username)

// Replace $bus with a custom event emitter
import mitt from 'mitt'
const emitter = mitt()
const onMenuToggle = () => {
  emitter.emit('menu-toggle')
}

const logout = async () => {
  console.log('Logging out...')
  window.location.href = '/login'
}
</script>

<style scoped>
/* Add your styles here */
</style>
