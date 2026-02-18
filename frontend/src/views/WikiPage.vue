<template>
  <div class="flex flex-col lg:flex-row gap-4 sm:gap-6 lg:gap-8 p-4 sm:p-6 lg:p-8">
    <!-- Loading State -->
    <div v-if="loading" class="flex-1 flex items-center justify-center py-12 sm:py-20">
      <div class="text-center">
        <span class="material-symbols-outlined text-4xl sm:text-5xl text-primary animate-spin">sync</span>
        <p class="text-slate-500 mt-3 sm:mt-4 text-sm sm:text-base">Cargando contenido...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="flex-1 flex items-center justify-center py-12 sm:py-20">
      <div class="text-center px-4">
        <span class="material-symbols-outlined text-4xl sm:text-5xl text-red-400">error</span>
        <p class="text-slate-700 dark:text-slate-300 font-semibold mt-3 sm:mt-4 text-sm sm:text-base">Página no encontrada</p>
        <p class="text-slate-500 mt-2 text-xs sm:text-sm">{{ error }}</p>
        <router-link to="/" class="text-primary font-medium hover:underline mt-4 inline-block text-sm">
          Volver al inicio
        </router-link>
      </div>
    </div>

    <template v-else>
      <!-- Mobile TOC (collapsible) -->
      <div class="lg:hidden mb-4">
        <button 
          @click="showMobileToc = !showMobileToc"
          class="w-full flex items-center justify-between px-4 py-3 bg-slate-100 dark:bg-slate-800 rounded-xl text-sm font-medium text-slate-700 dark:text-slate-300"
        >
          <span class="flex items-center gap-2">
            <span class="material-symbols-outlined text-lg">list</span>
            En esta página
          </span>
          <span 
            class="material-symbols-outlined text-lg transition-transform duration-200"
            :class="{ 'rotate-180': showMobileToc }"
          >expand_more</span>
        </button>
        <Transition
          enter-active-class="transition-all duration-200"
          enter-from-class="opacity-0 -translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition-all duration-150"
          leave-from-class="opacity-100"
          leave-to-class="opacity-0"
        >
          <nav v-show="showMobileToc" class="mt-2 p-3 bg-slate-50 dark:bg-slate-800/50 rounded-xl flex flex-col gap-1">
            <a 
              href="#overview"
              @click="showMobileToc = false"
              class="flex items-center gap-3 px-3 py-2 rounded-lg font-medium text-sm bg-primary/5 text-primary"
            >
              <span class="material-symbols-outlined text-lg">info</span>
              Descripción
            </a>
            <a 
              v-for="section in page.sections" 
              :key="section.id"
              :href="'#' + section.slug"
              @click="showMobileToc = false"
              class="flex items-center gap-3 px-3 py-2 rounded-lg font-medium text-sm text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700"
            >
              <span class="material-symbols-outlined text-lg">{{ section.icon || 'article' }}</span>
              {{ section.title }}
            </a>
          </nav>
        </Transition>
      </div>

      <!-- Desktop Sidebar TOC -->
      <aside class="w-56 flex-shrink-0 sticky top-24 h-fit hidden lg:block">
        <nav class="flex flex-col gap-1">
          <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4 px-3">En esta página</p>
          <a 
            href="#overview"
            :class="[
              'flex items-center gap-3 px-3 py-2 rounded-lg font-medium text-sm transition-colors',
              'bg-primary/5 text-primary font-semibold'
            ]"
          >
            <span class="material-symbols-outlined text-lg">info</span>
            Descripción
          </a>
          <a 
            v-for="section in page.sections" 
            :key="section.id"
            :href="'#' + section.slug"
            class="flex items-center gap-3 px-3 py-2 rounded-lg font-medium text-sm transition-colors text-slate-600 hover:bg-slate-50 dark:hover:bg-slate-800"
          >
            <span class="material-symbols-outlined text-lg">{{ section.icon || 'article' }}</span>
            {{ section.title }}
          </a>
        </nav>
      </aside>

      <!-- Main Article -->
      <article class="flex-1 min-w-0">
        <!-- Breadcrumb & Title -->
        <div class="mb-6 sm:mb-8" id="overview">
          <div class="flex items-center gap-1 sm:gap-2 text-primary font-semibold text-[10px] sm:text-xs mb-3 sm:mb-4 flex-wrap">
            <span class="truncate max-w-[120px] sm:max-w-none">{{ page.department_name }}</span>
            <span class="material-symbols-outlined text-[10px] sm:text-xs">chevron_right</span>
            <span class="truncate max-w-[120px] sm:max-w-none">{{ page.title }}</span>
          </div>
          <h1 class="text-slate-900 dark:text-white text-2xl sm:text-3xl md:text-4xl font-extrabold leading-tight mb-3 sm:mb-4">
            {{ page.heading || page.title }}
          </h1>
          <p class="text-slate-600 dark:text-slate-400 text-sm sm:text-base leading-relaxed mb-6 sm:mb-8">{{ page.description }}</p>
        </div>

        <!-- Main Content -->
        <div v-if="page.content" class="prose prose-sm sm:prose prose-slate dark:prose-invert max-w-none mb-8 sm:mb-12" v-html="page.content"></div>

        <!-- Sections -->
        <div v-for="section in page.sections" :key="section.id" :id="section.slug" class="mb-8 sm:mb-12 scroll-mt-20">
          <div class="flex items-center gap-2 sm:gap-3 mb-4 sm:mb-6">
            <span :class="`material-symbols-outlined text-xl sm:text-2xl text-${section.icon_color || 'primary'}`">{{ section.icon || 'article' }}</span>
            <h2 class="text-slate-900 dark:text-white text-xl sm:text-2xl font-bold">{{ section.title }}</h2>
          </div>
          <div class="prose prose-sm sm:prose prose-slate dark:prose-invert max-w-none" v-html="section.content"></div>
        </div>
      </article>
    </template>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { getPage } from '../api'

const props = defineProps({
  slug: {
    type: String,
    required: true
  }
})

// Mobile TOC toggle
const showMobileToc = ref(false)

const page = ref({
  title: '',
  heading: '',
  description: '',
  content: '',
  sections: [],
  department_name: '',
  banner_gradient: '',
  banner_icon: '',
  banner_text: '',
  help_text: '',
  help_button_text: ''
})
const loading = ref(true)
const error = ref(null)

const loadPage = async (slug) => {
  loading.value = true
  error.value = null
  
  try {
    const response = await getPage(slug)
    page.value = response.data
  } catch (err) {
    console.error('Error loading page:', err)
    error.value = err.response?.status === 404 
      ? 'La página solicitada no existe.' 
      : 'Error al cargar la página.'
  } finally {
    loading.value = false
  }
}

watch(() => props.slug, (newSlug) => {
  loadPage(newSlug)
}, { immediate: true })
</script>
