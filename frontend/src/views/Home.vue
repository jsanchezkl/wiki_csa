<template>
  <div class="px-8 py-8">
    <!-- Welcome Banner -->
    <div class="mb-10">
      <div class="bg-primary rounded-3xl p-8 text-white relative overflow-hidden">
        <div class="relative z-10">
          <h3 class="text-2xl font-bold mb-2">{{ settings.welcome_title || '' }}</h3>
          <p class="text-primary-100 text-sm opacity-90 mb-6 max-w-md">{{ settings.welcome_message || '' }}</p>
          
        </div>
        <div class="absolute -right-10 -bottom-10 size-64 bg-white/10 rounded-full blur-3xl"></div>
        <div class="absolute -right-20 -top-20 size-48 bg-white/5 rounded-full blur-2xl"></div>
      </div>
    </div>

    <!-- Browse Categories Section -->
    <div class="mb-10">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-slate-900 dark:text-white text-lg font-bold tracking-tight">Explorar Categorías</h2>
        <button class="text-primary text-xs font-bold uppercase tracking-wide hover:underline">Ver Todo</button>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div 
          v-for="cat in categories" 
          :key="cat.id"
          class="bg-white dark:bg-slate-800 rounded-2xl border border-slate-100 dark:border-slate-700 p-6 hover:shadow-md transition-shadow cursor-pointer"
        >
          <div 
            class="size-12 rounded-xl flex items-center justify-center mb-4"
            :class="`bg-${cat.color}-50 dark:bg-${cat.color}-900/20 text-${cat.color}-500`"
          >
            <span class="material-symbols-outlined text-2xl">{{ cat.icon }}</span>
          </div>
          <h3 class="text-sm font-bold text-slate-900 dark:text-white mb-1">{{ cat.name }}</h3>
          <p class="text-xs text-slate-500 dark:text-slate-400">{{ cat.description }}</p>
        </div>
      </div>
    </div>

    <!-- Recent Updates Section -->
    <div>
      <h2 class="text-slate-900 dark:text-white text-lg font-bold tracking-tight mb-6">Recent Updates</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <router-link 
          v-for="update in recentUpdates" 
          :key="update.id"
          :to="update.page_slug ? `/wiki/${update.page_slug}` : '#'" 
          class="flex items-center gap-4 p-4 bg-white dark:bg-slate-800 rounded-2xl border border-slate-100 dark:border-slate-700 hover:shadow-md transition-shadow cursor-pointer"
        >
          <div 
            class="size-10 rounded-xl flex items-center justify-center shrink-0"
            :class="update.icon_color === 'primary' ? 'bg-primary/10 text-primary' : `bg-${update.icon_color}-50 dark:bg-${update.icon_color}-900/20 text-${update.icon_color}-600`"
          >
            <span class="material-symbols-outlined text-xl">{{ update.icon }}</span>
          </div>
          <div class="flex-1 min-w-0">
            <h4 class="text-sm font-bold text-slate-900 dark:text-white mb-0.5">{{ update.title }}</h4>
            <p class="text-xs text-slate-500 dark:text-slate-400">{{ update.description }}</p>
          </div>
          <span class="material-symbols-outlined text-slate-300">chevron_right</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getDashboard } from '../api'

const settings = ref({
  welcome_title: 'Welcome back!',
  welcome_message: ''
})
const categories = ref([])
const recentUpdates = ref([])

onMounted(async () => {
  try {
    const response = await getDashboard()
    settings.value = response.data.settings || {}
    categories.value = response.data.categories || response.data.departments || []
    recentUpdates.value = response.data.recent_updates || []
  } catch (error) {
    console.error('Error loading dashboard:', error)
  }
})
</script>
