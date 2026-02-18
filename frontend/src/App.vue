<template>
  <!-- Login Layout (sin sidebar/header) -->
  <div v-if="hideLayout" class="min-h-screen">
    <router-view />
  </div>
  
  <!-- Main Layout -->
  <div v-else class="relative flex min-h-screen w-full bg-white dark:bg-background-dark overflow-x-hidden">
    <!-- Mobile Overlay -->
    <Transition
      enter-active-class="transition-opacity duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-300"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div 
        v-if="sidebarOpen" 
        @click="sidebarOpen = false"
        class="fixed inset-0 bg-black/50 z-30 lg:hidden"
      ></div>
    </Transition>
    
    <!-- SIDEBAR -->
    <Sidebar :isOpen="sidebarOpen" @close="sidebarOpen = false" />
    
    <!-- MAIN CONTENT WRAPPER -->
    <div class="flex-1 flex flex-col lg:ml-64 min-w-0">
      <!-- HEADER -->
      <Header :title="pageTitle" :showBack="showBackButton" @toggleSidebar="sidebarOpen = !sidebarOpen" />
      
      <!-- MAIN CONTENT -->
      <main class="flex-1 bg-background-light dark:bg-background-dark/50 w-full">
        <router-view />
      </main>
    </div>

    <!-- Chat Bot Assistant -->
    <ChatBot />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar from './components/Sidebar.vue'
import Header from './components/Header.vue'
import ChatBot from './components/ChatBot.vue'
import { getSettings, isAuthenticated } from './api'

const route = useRoute()

// Mobile sidebar state
const sidebarOpen = ref(false)

// Close sidebar on route change (mobile)
watch(() => route.path, () => {
  sidebarOpen.value = false
})

// Ocultar layout en login y otras páginas públicas
const hideLayout = computed(() => route.meta?.hideLayout === true)

const pageTitle = computed(() => {
  if (route.name === 'Home') return 'Dashboard'
  return route.meta?.title || 'Wiki'
})

const showBackButton = computed(() => route.name !== 'Home')

// Cargar configuración y actualizar título de la página
onMounted(async () => {
  if (!isAuthenticated()) return
  
  try {
    const response = await getSettings()
    if (response.data.site_name) {
      document.title = `${response.data.site_name} - Corporate Knowledge Base`
    }
  } catch (error) {
    console.error('Error loading settings:', error)
  }
})

// Actualizar título cuando cambia la ruta
watch(() => route.name, (name) => {
  // Podríamos actualizar el título según la página actual
})
</script>
