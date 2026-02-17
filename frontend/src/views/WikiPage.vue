<template>
  <div class="flex gap-8 p-8">
    <!-- Loading State -->
    <div v-if="loading" class="flex-1 flex items-center justify-center py-20">
      <div class="text-center">
        <span class="material-symbols-outlined text-5xl text-primary animate-spin">sync</span>
        <p class="text-slate-500 mt-4">Cargando contenido...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="flex-1 flex items-center justify-center py-20">
      <div class="text-center">
        <span class="material-symbols-outlined text-5xl text-red-400">error</span>
        <p class="text-slate-700 dark:text-slate-300 font-semibold mt-4">Página no encontrada</p>
        <p class="text-slate-500 mt-2">{{ error }}</p>
        <router-link to="/" class="text-primary font-medium hover:underline mt-4 inline-block">
          Volver al inicio
        </router-link>
      </div>
    </div>

    <template v-else>
      <!-- Sidebar TOC -->
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
      <article class="flex-1">
        <!-- Breadcrumb & Title -->
        <div class="mb-8" id="overview">
          <div class="flex items-center gap-2 text-primary font-semibold text-xs mb-4">
            <span>{{ page.department_name }}</span>
            <span class="material-symbols-outlined text-xs">chevron_right</span>
            <span>{{ page.title }}</span>
          </div>
          <h1 class="text-slate-900 dark:text-white text-3xl md:text-4xl font-extrabold leading-tight mb-4">
            {{ page.heading || page.title }}
          </h1>
          <p class="text-slate-600 dark:text-slate-400 text-base leading-relaxed mb-8">{{ page.description }}</p>
        </div>

        <!-- Main Content -->
        <div v-if="page.content" class="prose prose-slate dark:prose-invert max-w-none mb-12" v-html="page.content"></div>

        <!-- Sections -->
        <div v-for="section in page.sections" :key="section.id" :id="section.slug" class="mb-12">
          <div class="flex items-center gap-3 mb-6">
            <span :class="`material-symbols-outlined text-2xl text-${section.icon_color || 'primary'}`">{{ section.icon || 'article' }}</span>
            <h2 class="text-slate-900 dark:text-white text-2xl font-bold">{{ section.title }}</h2>
          </div>
          <div class="prose prose-slate dark:prose-invert max-w-none" v-html="section.content"></div>
        </div>
      </article>
    </template>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { getPage } from '../api'

const props = defineProps({
  slug: {
    type: String,
    required: true
  }
})

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
