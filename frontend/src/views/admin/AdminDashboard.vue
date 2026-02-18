<template>
  <div class="min-h-screen bg-slate-50 dark:bg-background-dark">
    <!-- Admin Header -->
    <header class="sticky top-0 z-30 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800">
      <div class="px-4 sm:px-6 lg:px-8 py-3 sm:py-4 flex items-center justify-between gap-2">
        <div class="flex items-center gap-2 sm:gap-4 min-w-0">
          <button 
            @click="showMobileMenu = !showMobileMenu"
            class="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors lg:hidden"
          >
            <span class="material-symbols-outlined text-slate-600 dark:text-slate-400">menu</span>
          </button>
          <router-link 
            to="/" 
            class="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors hidden sm:flex"
          >
            <span class="material-symbols-outlined text-slate-600">arrow_back</span>
          </router-link>
          <div class="flex items-center gap-2 sm:gap-3 min-w-0">
            <div class="p-1.5 sm:p-2 bg-primary/10 rounded-lg shrink-0">
              <span class="material-symbols-outlined text-primary text-lg sm:text-2xl">admin_panel_settings</span>
            </div>
            <div class="min-w-0">
              <h1 class="text-base sm:text-xl font-bold text-slate-900 dark:text-white truncate">Panel de Administración</h1>
              <p class="text-[10px] sm:text-xs text-slate-500 hidden sm:block">Gestiona tu Wiki corporativo</p>
            </div>
          </div>
        </div>
        <div class="flex items-center gap-2 sm:gap-4 shrink-0">
          <router-link 
            to="/admin/pages/new"
            class="flex items-center gap-1 sm:gap-2 bg-primary text-white px-3 sm:px-4 py-2 rounded-lg hover:bg-primary/90 transition-colors font-medium text-sm"
          >
            <span class="material-symbols-outlined text-lg">add</span>
            <span class="hidden sm:inline">Nueva Página</span>
          </router-link>
        </div>
      </div>
    </header>

    <!-- Mobile Menu Overlay -->
    <Transition
      enter-active-class="transition-opacity duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-300"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div 
        v-if="showMobileMenu" 
        @click="showMobileMenu = false"
        class="fixed inset-0 bg-black/50 z-40 lg:hidden"
      ></div>
    </Transition>

    <div class="flex">
      <!-- Admin Sidebar -->
      <aside 
        :class="[
          'w-64 min-h-screen bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 transition-transform duration-300 ease-in-out',
          'fixed lg:static top-0 left-0 z-50 lg:z-auto pt-16 lg:pt-0',
          showMobileMenu ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        ]"
      >
        <!-- Mobile close button -->
        <button 
          @click="showMobileMenu = false"
          class="absolute top-4 right-4 p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 lg:hidden"
        >
          <span class="material-symbols-outlined text-slate-600 dark:text-slate-400">close</span>
        </button>
        <nav class="p-4">
          <div class="space-y-1">
            <router-link 
              to="/admin" 
              class="flex items-center gap-3 px-4 py-3 rounded-xl transition-colors"
              :class="isActive('/admin', true) ? 'bg-primary/10 text-primary' : 'text-slate-600 hover:bg-slate-50 dark:hover:bg-slate-800'"
            >
              <span class="material-symbols-outlined">dashboard</span>
              <span class="font-medium">Dashboard</span>
            </router-link>
            
            <router-link 
              to="/admin/departments" 
              class="flex items-center gap-3 px-4 py-3 rounded-xl transition-colors"
              :class="isActive('/admin/departments') ? 'bg-primary/10 text-primary' : 'text-slate-600 hover:bg-slate-50 dark:hover:bg-slate-800'"
            >
              <span class="material-symbols-outlined">folder</span>
              <span class="font-medium">Categorías</span>
            </router-link>
            
            <router-link 
              to="/admin/pages" 
              class="flex items-center gap-3 px-4 py-3 rounded-xl transition-colors"
              :class="isActive('/admin/pages') ? 'bg-primary/10 text-primary' : 'text-slate-600 hover:bg-slate-50 dark:hover:bg-slate-800'"
            >
              <span class="material-symbols-outlined">article</span>
              <span class="font-medium">Páginas</span>
            </router-link>
            
            <router-link 
              to="/admin/settings" 
              class="flex items-center gap-3 px-4 py-3 rounded-xl transition-colors"
              :class="isActive('/admin/settings') ? 'bg-primary/10 text-primary' : 'text-slate-600 hover:bg-slate-50 dark:hover:bg-slate-800'"
            >
              <span class="material-symbols-outlined">settings</span>
              <span class="font-medium">Configuración</span>
            </router-link>
          </div>
        </nav>
      </aside>

      <!-- Main Content -->
      <main class="flex-1 p-4 sm:p-6 lg:p-8">
        <!-- Stats Grid -->
        <div class="grid grid-cols-2 md:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 lg:gap-6 mb-6 sm:mb-8">
          <div class="bg-white dark:bg-slate-900 rounded-xl sm:rounded-2xl p-3 sm:p-4 lg:p-6 border border-slate-200 dark:border-slate-800">
            <div class="flex items-center justify-between mb-2 sm:mb-4">
              <span class="p-2 sm:p-3 bg-blue-100 dark:bg-blue-900/30 rounded-lg sm:rounded-xl">
                <span class="material-symbols-outlined text-blue-600 text-lg sm:text-2xl">folder</span>
              </span>
              <span class="text-[10px] sm:text-xs px-1.5 sm:px-2 py-0.5 sm:py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-600 rounded-full hidden sm:block">+2</span>
            </div>
            <p class="text-xl sm:text-2xl lg:text-3xl font-bold text-slate-900 dark:text-white mb-0.5 sm:mb-1">{{ stats.active_categories }}</p>
            <p class="text-[10px] sm:text-xs lg:text-sm text-slate-500">Categorías</p>
          </div>
          
          <div class="bg-white dark:bg-slate-900 rounded-xl sm:rounded-2xl p-3 sm:p-4 lg:p-6 border border-slate-200 dark:border-slate-800">
            <div class="flex items-center justify-between mb-2 sm:mb-4">
              <span class="p-2 sm:p-3 bg-emerald-100 dark:bg-emerald-900/30 rounded-lg sm:rounded-xl">
                <span class="material-symbols-outlined text-emerald-600 text-lg sm:text-2xl">article</span>
              </span>
              <span class="text-[10px] sm:text-xs px-1.5 sm:px-2 py-0.5 sm:py-1 bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 rounded-full hidden sm:block">{{ stats.published_pages }} pub</span>
            </div>
            <p class="text-xl sm:text-2xl lg:text-3xl font-bold text-slate-900 dark:text-white mb-0.5 sm:mb-1">{{ stats.total_pages }}</p>
            <p class="text-[10px] sm:text-xs lg:text-sm text-slate-500">Páginas</p>
          </div>
          
          <div class="bg-white dark:bg-slate-900 rounded-xl sm:rounded-2xl p-3 sm:p-4 lg:p-6 border border-slate-200 dark:border-slate-800">
            <div class="flex items-center justify-between mb-2 sm:mb-4">
              <span class="p-2 sm:p-3 bg-amber-100 dark:bg-amber-900/30 rounded-lg sm:rounded-xl">
                <span class="material-symbols-outlined text-amber-600 text-lg sm:text-2xl">edit_note</span>
              </span>
              <span class="text-[10px] sm:text-xs px-1.5 sm:px-2 py-0.5 sm:py-1 bg-amber-100 dark:bg-amber-900/30 text-amber-600 rounded-full hidden sm:block">Borrador</span>
            </div>
            <p class="text-xl sm:text-2xl lg:text-3xl font-bold text-slate-900 dark:text-white mb-0.5 sm:mb-1">{{ stats.draft_pages }}</p>
            <p class="text-[10px] sm:text-xs lg:text-sm text-slate-500">Borradores</p>
          </div>
          
          <div class="bg-white dark:bg-slate-900 rounded-xl sm:rounded-2xl p-3 sm:p-4 lg:p-6 border border-slate-200 dark:border-slate-800">
            <div class="flex items-center justify-between mb-2 sm:mb-4">
              <span class="p-2 sm:p-3 bg-purple-100 dark:bg-purple-900/30 rounded-lg sm:rounded-xl">
                <span class="material-symbols-outlined text-purple-600 text-lg sm:text-2xl">visibility</span>
              </span>
            </div>
            <p class="text-xl sm:text-2xl lg:text-3xl font-bold text-slate-900 dark:text-white mb-0.5 sm:mb-1">{{ stats.total_views }}</p>
            <p class="text-[10px] sm:text-xs lg:text-sm text-slate-500">Vistas</p>
          </div>
        </div>

        <!-- Chat AI / RAG Indexing Module -->
        <div class="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl sm:rounded-2xl p-4 sm:p-6 mb-6 sm:mb-8 text-white">
          <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3 sm:gap-0">
            <div class="flex items-center gap-3 sm:gap-4">
              <div class="p-2 sm:p-3 bg-white/20 rounded-lg sm:rounded-xl shrink-0">
                <span class="material-symbols-outlined text-2xl sm:text-3xl">psychology</span>
              </div>
              <div>
                <h2 class="text-lg sm:text-xl font-bold mb-0.5 sm:mb-1">Wiki Assistant AI</h2>
                <p class="text-white/80 text-xs sm:text-sm">Base de conocimiento para el chatbot</p>
              </div>
            </div>
            <div class="flex items-center gap-2 self-start">
              <span 
                class="px-2 sm:px-3 py-1 rounded-full text-xs sm:text-sm font-medium"
                :class="chatStats.enabled ? 'bg-emerald-400/20 text-emerald-200' : 'bg-red-400/20 text-red-200'"
              >
                <span class="inline-block w-1.5 sm:w-2 h-1.5 sm:h-2 rounded-full mr-1.5 sm:mr-2" :class="chatStats.enabled ? 'bg-emerald-400' : 'bg-red-400'"></span>
                {{ chatStats.enabled ? 'Activo' : 'Inactivo' }}
              </span>
            </div>
          </div>
          
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-4 mt-4 sm:mt-6">
            <!-- Stats -->
            <div class="bg-white/10 rounded-lg sm:rounded-xl p-3 sm:p-4">
              <div class="flex items-center gap-2 sm:gap-3 mb-1.5 sm:mb-2">
                <span class="material-symbols-outlined text-white/60 text-lg sm:text-2xl">description</span>
                <span class="text-white/60 text-xs sm:text-sm">Docs Indexados</span>
              </div>
              <p class="text-2xl sm:text-3xl font-bold">{{ chatStats.indexed_documents }}</p>
            </div>
            
            <div class="bg-white/10 rounded-lg sm:rounded-xl p-3 sm:p-4">
              <div class="flex items-center gap-2 sm:gap-3 mb-1.5 sm:mb-2">
                <span class="material-symbols-outlined text-white/60 text-lg sm:text-2xl">smart_toy</span>
                <span class="text-white/60 text-xs sm:text-sm">Modelo Chat</span>
              </div>
              <p class="text-sm sm:text-lg font-semibold truncate">{{ chatStats.model || 'N/A' }}</p>
            </div>
            
            <div class="bg-white/10 rounded-lg sm:rounded-xl p-3 sm:p-4">
              <div class="flex items-center gap-2 sm:gap-3 mb-1.5 sm:mb-2">
                <span class="material-symbols-outlined text-white/60 text-lg sm:text-2xl">data_array</span>
                <span class="text-white/60 text-xs sm:text-sm">Embeddings</span>
              </div>
              <p class="text-sm sm:text-lg font-semibold truncate">{{ chatStats.embedding_model || 'N/A' }}</p>
            </div>
          </div>
          
          <div class="mt-4 sm:mt-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 sm:gap-4">
            <p class="text-white/60 text-xs sm:text-sm hidden sm:block">
              <span class="material-symbols-outlined text-sm align-middle mr-1">info</span>
              Indexa el contenido cuando agregues o elimines páginas
            </p>
            <button 
              @click="indexContent"
              :disabled="isIndexing"
              class="flex items-center justify-center gap-2 bg-white text-indigo-600 px-4 sm:px-6 py-2.5 sm:py-3 rounded-lg sm:rounded-xl font-semibold hover:bg-white/90 transition-all disabled:opacity-70 disabled:cursor-wait w-full sm:w-auto text-sm sm:text-base"
            >
              <span 
                class="material-symbols-outlined"
                :class="{ 'animate-spin': isIndexing }"
              >
                {{ isIndexing ? 'sync' : 'refresh' }}
              </span>
              {{ isIndexing ? 'Indexando...' : 'Indexar Contenido' }}
            </button>
          </div>
          
          <!-- Indexing Result Toast -->
          <Transition
            enter-active-class="transition-all duration-300"
            enter-from-class="opacity-0 translate-y-2"
            enter-to-class="opacity-100 translate-y-0"
            leave-active-class="transition-all duration-200"
            leave-from-class="opacity-100 translate-y-0"
            leave-to-class="opacity-0 translate-y-2"
          >
            <div 
              v-if="indexResult"
              class="mt-4 p-4 rounded-xl flex items-center gap-3"
              :class="indexResult.success ? 'bg-emerald-400/20' : 'bg-red-400/20'"
            >
              <span class="material-symbols-outlined">
                {{ indexResult.success ? 'check_circle' : 'error' }}
              </span>
              <span>{{ indexResult.message }}</span>
            </div>
          </Transition>
        </div>

        <!-- Quick Actions -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 lg:gap-8">
          <!-- Recent Pages -->
          <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800">
            <div class="p-6 border-b border-slate-200 dark:border-slate-800">
              <h2 class="text-lg font-bold text-slate-900 dark:text-white">Páginas Recientes</h2>
            </div>
            <div class="p-6">
              <div v-if="pages.length === 0" class="text-center py-8">
                <span class="material-symbols-outlined text-4xl text-slate-300 mb-2">article</span>
                <p class="text-slate-500">No hay páginas aún</p>
                <router-link to="/admin/pages/new" class="text-primary font-medium hover:underline">
                  Crear primera página
                </router-link>
              </div>
              <div v-else class="space-y-3">
                <div 
                  v-for="page in pages.slice(0, 5)" 
                  :key="page.id"
                  class="flex items-center justify-between p-4 rounded-xl hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
                >
                  <div class="flex items-center gap-3">
                    <span class="material-symbols-outlined text-slate-400">{{ page.icon }}</span>
                    <div>
                      <p class="font-medium text-slate-900 dark:text-white">{{ page.title }}</p>
                      <p class="text-xs text-slate-500">{{ page.department_name }}</p>
                    </div>
                  </div>
                  <div class="flex items-center gap-2">
                    <span 
                      class="text-xs px-2 py-1 rounded-full"
                      :class="page.is_published ? 'bg-emerald-100 text-emerald-600' : 'bg-amber-100 text-amber-600'"
                    >
                      {{ page.is_published ? 'Publicada' : 'Borrador' }}
                    </span>
                    <router-link 
                      :to="`/admin/pages/${page.slug}/edit`"
                      class="p-2 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg transition-colors"
                    >
                      <span class="material-symbols-outlined text-lg text-slate-500">edit</span>
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Categories -->
          <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800">
            <div class="p-6 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
              <h2 class="text-lg font-bold text-slate-900 dark:text-white">Categorías</h2>
              <router-link 
                to="/admin/departments/new"
                class="text-sm text-primary font-medium hover:underline"
              >
                + Nueva
              </router-link>
            </div>
            <div class="p-6">
              <div v-if="categories.length === 0" class="text-center py-8">
                <span class="material-symbols-outlined text-4xl text-slate-300 mb-2">folder</span>
                <p class="text-slate-500">No hay categorías aún</p>
              </div>
              <div v-else class="space-y-3">
                <div 
                  v-for="cat in categories" 
                  :key="cat.id"
                  class="flex items-center justify-between p-4 rounded-xl hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
                >
                  <div class="flex items-center gap-3">
                    <span 
                      class="p-2 rounded-lg"
                      :class="`bg-${cat.color}-100 dark:bg-${cat.color}-900/30`"
                    >
                      <span :class="`material-symbols-outlined text-${cat.color}-600`">{{ cat.icon }}</span>
                    </span>
                    <div>
                      <p class="font-medium text-slate-900 dark:text-white">{{ cat.name }}</p>
                      <p class="text-xs text-slate-500">{{ cat.pages_count }} páginas</p>
                    </div>
                  </div>
                  <router-link 
                    :to="`/admin/departments/${cat.id}/edit`"
                    class="p-2 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg transition-colors"
                  >
                    <span class="material-symbols-outlined text-lg text-slate-500">edit</span>
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getAdminStats, getCategories, getPages, getChatStats, indexChatContent } from '../../api'

const route = useRoute()

// Mobile menu state
const showMobileMenu = ref(false)

const stats = ref({
  total_categories: 0,
  active_categories: 0,
  total_pages: 0,
  published_pages: 0,
  draft_pages: 0,
  total_views: 0
})

const categories = ref([])
const pages = ref([])

// Chat AI / RAG
const chatStats = ref({
  enabled: false,
  indexed_documents: 0,
  model: '',
  embedding_model: ''
})
const isIndexing = ref(false)
const indexResult = ref(null)

const isActive = (path, exact = false) => {
  if (exact) {
    return route.path === path
  }
  return route.path.startsWith(path)
}

const loadChatStats = async () => {
  try {
    const res = await getChatStats()
    chatStats.value = res.data
  } catch (error) {
    console.error('Error loading chat stats:', error)
  }
}

const indexContent = async () => {
  isIndexing.value = true
  indexResult.value = null
  
  try {
    const res = await indexChatContent()
    
    if (res.data.success) {
      indexResult.value = {
        success: true,
        message: `✅ ¡Indexación completada! ${res.data.indexed_pages} páginas indexadas correctamente.`
      }
      // Actualizar stats
      await loadChatStats()
    } else {
      indexResult.value = {
        success: false,
        message: `❌ Error al indexar: ${res.data.error || 'Error desconocido'}`
      }
    }
  } catch (error) {
    indexResult.value = {
      success: false,
      message: `❌ Error de conexión: ${error.message}`
    }
  } finally {
    isIndexing.value = false
    
    // Ocultar mensaje después de 5 segundos
    setTimeout(() => {
      indexResult.value = null
    }, 5000)
  }
}

onMounted(async () => {
  try {
    const [statsRes, catsRes, pagesRes] = await Promise.all([
      getAdminStats(),
      getCategories({ all: 'true' }),
      getPages({ all: 'true' }),
      loadChatStats()
    ])
    stats.value = statsRes.data
    categories.value = catsRes.data
    pages.value = pagesRes.data
  } catch (error) {
    console.error('Error loading admin data:', error)
  }
})
</script>

