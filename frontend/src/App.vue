<template>
  <!-- Login Layout (sin sidebar/header) -->
  <div v-if="hideLayout" class="min-h-screen">
    <router-view />
  </div>
  
  <!-- Main Layout -->
  <div v-else class="relative flex min-h-screen w-full bg-white dark:bg-background-dark overflow-x-hidden">
    <!-- SIDEBAR -->
    <Sidebar />
    
    <!-- MAIN CONTENT WRAPPER -->
    <div class="flex-1 flex flex-col ml-64 min-w-0">
      <!-- HEADER -->
      <Header :title="pageTitle" :showBack="showBackButton" />
      
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
import { computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar from './components/Sidebar.vue'
import Header from './components/Header.vue'
import ChatBot from './components/ChatBot.vue'
import { getSettings, isAuthenticated } from './api'

const route = useRoute()

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
