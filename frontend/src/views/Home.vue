<template>
  <div class="px-4 py-4 sm:px-6 sm:py-6 md:px-8 md:py-8">
    <!-- Welcome Banner -->
    <div class="mb-6 sm:mb-8 md:mb-10">
      <div 
        class="rounded-2xl sm:rounded-3xl p-4 sm:p-6 md:p-8 text-white relative overflow-hidden bg-cover bg-center bg-no-repeat min-h-[120px] sm:min-h-[140px] md:min-h-[160px]"
        :style="{ backgroundImage: 'url(/bg-servicios.webp)' }"
      >
        <div class="absolute inset-0 bg-black/40 rounded-2xl sm:rounded-3xl"></div>
        <div class="relative z-10">
          <h3 class="text-xl sm:text-2xl font-bold mb-1 sm:mb-2">{{ settings.welcome_title || '' }}</h3>
          <p class="text-white/90 text-xs sm:text-sm mb-4 sm:mb-6 max-w-full sm:max-w-md leading-relaxed">{{ settings.welcome_message || '' }}</p>
          
        </div>
      </div>
    </div>

    <!-- Browse Categories Section -->
    <div class="mb-6 sm:mb-8 md:mb-10">
      <div class="flex items-center justify-between mb-4 sm:mb-6 gap-2">
        <h2 class="text-slate-900 dark:text-white text-base sm:text-lg font-bold tracking-tight">Explorar Categorías</h2>
        <button class="text-primary text-xs font-bold uppercase tracking-wide hover:underline whitespace-nowrap">Ver Todo</button>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4">
        <div 
          v-for="cat in categories" 
          :key="cat.id"
          class="bg-white dark:bg-slate-800 rounded-xl sm:rounded-2xl border border-slate-100 dark:border-slate-700 p-4 sm:p-5 md:p-6 hover:shadow-md transition-shadow cursor-pointer active:scale-[0.98]"
        >
          <div 
            class="size-10 sm:size-12 rounded-lg sm:rounded-xl flex items-center justify-center mb-3 sm:mb-4"
            :class="`bg-${cat.color}-50 dark:bg-${cat.color}-900/20 text-${cat.color}-500`"
          >
            <span class="material-symbols-outlined text-xl sm:text-2xl">{{ cat.icon }}</span>
          </div>
          <h3 class="text-sm font-bold text-slate-900 dark:text-white mb-1">{{ cat.name }}</h3>
          <p class="text-xs text-slate-500 dark:text-slate-400 line-clamp-2">{{ cat.description }}</p>
        </div>
      </div>
    </div>

    <!-- Recent Updates Section -->
    <div>
      <h2 class="text-slate-900 dark:text-white text-base sm:text-lg font-bold tracking-tight mb-4 sm:mb-6">Recent Updates</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3 sm:gap-4">
        <router-link 
          v-for="update in recentUpdates" 
          :key="update.id"
          :to="update.page_slug ? `/wiki/${update.page_slug}` : '#'" 
          class="flex items-center gap-3 sm:gap-4 p-3 sm:p-4 bg-white dark:bg-slate-800 rounded-xl sm:rounded-2xl border border-slate-100 dark:border-slate-700 hover:shadow-md transition-shadow cursor-pointer active:scale-[0.98]"
        >
          <div 
            class="size-9 sm:size-10 rounded-lg sm:rounded-xl flex items-center justify-center shrink-0"
            :class="update.icon_color === 'primary' ? 'bg-primary/10 text-primary' : `bg-${update.icon_color}-50 dark:bg-${update.icon_color}-900/20 text-${update.icon_color}-600`"
          >
            <span class="material-symbols-outlined text-lg sm:text-xl">{{ update.icon }}</span>
          </div>
          <div class="flex-1 min-w-0">
            <h4 class="text-sm font-bold text-slate-900 dark:text-white mb-0.5 truncate">{{ update.title }}</h4>
            <p class="text-xs text-slate-500 dark:text-slate-400 truncate">{{ update.description }}</p>
          </div>
          <span class="material-symbols-outlined text-slate-300 text-lg sm:text-base">chevron_right</span>
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
