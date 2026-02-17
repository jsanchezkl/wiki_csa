<template>
  <aside class="w-64 border-r border-slate-200 dark:border-slate-800 bg-white dark:bg-background-dark fixed top-0 left-0 h-screen flex flex-col z-40 shrink-0">
    <div class="p-6">
      <router-link to="/" class="flex items-center gap-3">
        <img 
          v-if="logoUrl" 
          :src="logoUrl" 
          :alt="siteName"
          class="h-10 w-auto object-contain"
        />
        <span v-else class="text-primary text-2xl font-bold tracking-tight">{{ siteName }}</span>
      </router-link>
    </div>
    
    <div class="px-4 mb-6 relative" ref="searchContainerRef">
      <label class="relative flex items-center">
        <span class="material-symbols-outlined absolute left-3 text-slate-400 text-sm">search</span>
        <input 
          v-model="searchQuery"
          @input="handleSearch"
          @focus="showSearchResults = searchResults.total > 0"
          class="w-full h-10 pl-10 pr-10 bg-slate-100 dark:bg-slate-800 border-none rounded-lg focus:ring-2 focus:ring-primary/20 transition-all text-xs font-medium text-slate-900 dark:text-white" 
          placeholder="Buscar páginas, categorías..." 
          type="text"
        />
        <span 
          v-if="isSearching" 
          class="material-symbols-outlined absolute right-3 text-slate-400 text-sm animate-spin"
        >
          progress_activity
        </span>
        <button 
          v-else-if="searchQuery" 
          @click="clearSearch"
          class="absolute right-3 text-slate-400 hover:text-slate-600 transition-colors"
        >
          <span class="material-symbols-outlined text-sm">close</span>
        </button>
      </label>
      
      <!-- Search Results Dropdown -->
      <Transition
        enter-active-class="transition-all duration-200"
        enter-from-class="opacity-0 -translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition-all duration-150"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div 
          v-if="showSearchResults && searchResults.total > 0"
          class="absolute left-4 right-4 top-12 bg-white dark:bg-slate-900 rounded-xl shadow-2xl border border-slate-200 dark:border-slate-700 max-h-80 overflow-y-auto z-50"
        >
          <!-- Pages -->
          <div v-if="searchResults.pages.length > 0">
            <p class="px-4 py-2 text-[10px] font-bold uppercase tracking-wider text-slate-400 bg-slate-50 dark:bg-slate-800 sticky top-0">
              Páginas
            </p>
            <router-link 
              v-for="page in searchResults.pages" 
              :key="'page-' + page.id"
              :to="`/wiki/${page.slug}`"
              @click="clearSearch"
              class="flex items-start gap-3 px-4 py-3 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
            >
              <span class="material-symbols-outlined text-lg text-primary mt-0.5">{{ page.icon || 'article' }}</span>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-slate-900 dark:text-white truncate">{{ page.title }}</p>
                <p class="text-xs text-slate-500 truncate">{{ page.category_name }}</p>
              </div>
            </router-link>
          </div>
          
          <!-- Categories -->
          <div v-if="searchResults.categories.length > 0">
            <p class="px-4 py-2 text-[10px] font-bold uppercase tracking-wider text-slate-400 bg-slate-50 dark:bg-slate-800 sticky top-0">
              Categorías
            </p>
            <div 
              v-for="cat in searchResults.categories" 
              :key="'cat-' + cat.id"
              @click="toggleSubmenu(cat.id); clearSearch();"
              class="flex items-center gap-3 px-4 py-3 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors cursor-pointer"
            >
              <span :class="`material-symbols-outlined text-lg text-${cat.color}-500`">{{ cat.icon }}</span>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-slate-900 dark:text-white truncate">{{ cat.name }}</p>
                <p v-if="cat.description" class="text-xs text-slate-500 truncate">{{ cat.description }}</p>
              </div>
            </div>
          </div>
          
          <!-- Sections -->
          <div v-if="searchResults.sections.length > 0">
            <p class="px-4 py-2 text-[10px] font-bold uppercase tracking-wider text-slate-400 bg-slate-50 dark:bg-slate-800 sticky top-0">
              Secciones
            </p>
            <router-link 
              v-for="section in searchResults.sections" 
              :key="'section-' + section.id"
              :to="`/wiki/${section.page_slug}#${section.slug}`"
              @click="clearSearch"
              class="flex items-start gap-3 px-4 py-3 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
            >
              <span class="material-symbols-outlined text-lg text-slate-400 mt-0.5">tag</span>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-slate-900 dark:text-white truncate">{{ section.title }}</p>
                <p class="text-xs text-slate-500 truncate">en {{ section.page_title }}</p>
              </div>
            </router-link>
          </div>
          
          <!-- No results message -->
          <div v-if="searchResults.total === 0 && searchQuery.length >= 2 && !isSearching" class="p-6 text-center">
            <span class="material-symbols-outlined text-3xl text-slate-300 mb-2">search_off</span>
            <p class="text-sm text-slate-500">No se encontraron resultados</p>
          </div>
        </div>
      </Transition>
      
      <!-- No results found after search -->
      <Transition
        enter-active-class="transition-all duration-200"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-all duration-150"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div 
          v-if="showSearchResults && searchQuery.length >= 2 && searchResults.total === 0 && !isSearching"
          class="absolute left-4 right-4 top-12 bg-white dark:bg-slate-900 rounded-xl shadow-2xl border border-slate-200 dark:border-slate-700 p-6 text-center z-50"
        >
          <span class="material-symbols-outlined text-3xl text-slate-300 mb-2">search_off</span>
          <p class="text-sm text-slate-500">No se encontraron resultados para "{{ searchQuery }}"</p>
        </div>
      </Transition>
    </div>
    
    <div class="flex-1 overflow-y-auto hide-scrollbar px-2 space-y-6">
      <nav class="space-y-1 px-2">
        <p class="px-3 text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-2">Menu</p>
        <router-link 
          to="/" 
          :class="[
            'flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors',
            isActive('/') ? 'text-primary bg-primary/5 font-semibold' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800'
          ]"
        >
          <span class="material-symbols-outlined text-xl">home</span>
          <span>Inicio</span>
        </router-link>
        <a class="flex items-center gap-3 px-3 py-2 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-lg text-sm transition-colors cursor-pointer">
          <span class="material-symbols-outlined text-xl">bookmark</span>
          <span>Guardados</span>
        </a>
        <a class="flex items-center gap-3 px-3 py-2 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-lg text-sm transition-colors cursor-pointer">
          <span class="material-symbols-outlined text-xl">history</span>
          <span>Actividad</span>
        </a>
      </nav>
      
      <div class="space-y-1 px-2">
        <div class="flex items-center justify-between px-3 mb-2">
          <p class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Categorías</p>
          <button class="text-primary text-[10px] font-bold">VER TODO</button>
        </div>
        
        <!-- Dynamic categories with subcategories -->
        <div v-for="cat in sortedCategories" :key="cat.id" class="relative">
          <!-- Category with pages or subcategories -->
          <button 
            v-if="(cat.pages && cat.pages.length > 0) || (cat.subcategories && cat.subcategories.length > 0)"
            @click="toggleSubmenu(cat.id)" 
            class="flex items-center justify-between w-full px-3 py-2 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-lg text-sm transition-colors"
          >
            <div class="flex items-center gap-3">
              <span :class="`material-symbols-outlined text-xl text-${cat.color}-500`">{{ cat.icon }}</span>
              <span>{{ cat.name }}</span>
            </div>
            <span 
              class="material-symbols-outlined text-lg transition-transform duration-200" 
              :class="{ 'rotate-180': openSubmenus[cat.id] }"
            >expand_more</span>
          </button>
          
          <!-- Category without pages or subcategories -->
          <a 
            v-else
            class="flex items-center gap-3 px-3 py-2 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-lg text-sm transition-colors cursor-pointer"
          >
            <span :class="`material-symbols-outlined text-xl text-${cat.color}-500`">{{ cat.icon }}</span>
            <span>{{ cat.name }}</span>
          </a>
          
          <!-- Submenu with subcategories and pages -->
          <div v-show="openSubmenus[cat.id]" class="pl-4 mt-1 space-y-1">
            <!-- Subcategories -->
            <div v-for="subcat in cat.subcategories" :key="'sub-' + subcat.id" class="relative">
              <button 
                v-if="subcat.pages && subcat.pages.length > 0"
                @click="toggleSubmenu('sub-' + subcat.id)" 
                class="flex items-center justify-between w-full px-3 py-1.5 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-lg text-xs transition-colors"
              >
                <div class="flex items-center gap-2">
                  <span :class="`material-symbols-outlined text-base text-${subcat.color}-400`">{{ subcat.icon }}</span>
                  <span>{{ subcat.name }}</span>
                </div>
                <span 
                  class="material-symbols-outlined text-sm transition-transform duration-200" 
                  :class="{ 'rotate-180': openSubmenus['sub-' + subcat.id] }"
                >expand_more</span>
              </button>
              
              <a 
                v-else
                class="flex items-center gap-2 px-3 py-1.5 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-lg text-xs transition-colors cursor-pointer"
              >
                <span :class="`material-symbols-outlined text-base text-${subcat.color}-400`">{{ subcat.icon }}</span>
                <span>{{ subcat.name }}</span>
              </a>
              
              <!-- Subcategory pages -->
              <div v-show="openSubmenus['sub-' + subcat.id]" class="pl-5 mt-1 space-y-0.5">
                <router-link 
                  v-for="page in subcat.pages" 
                  :key="page.id"
                  :to="`/wiki/${page.slug}`" 
                  :class="[
                    'flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs transition-colors',
                    isActive(`/wiki/${page.slug}`) ? 'text-primary bg-primary/5 font-semibold' : 'text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800'
                  ]"
                >
                  <span class="material-symbols-outlined text-sm">{{ page.icon }}</span>
                  <span>{{ page.title }}</span>
                </router-link>
              </div>
            </div>
            
            <!-- Direct pages under category -->
            <router-link 
              v-for="page in cat.pages" 
              :key="page.id"
              :to="`/wiki/${page.slug}`" 
              :class="[
                'flex items-center gap-3 px-3 py-2 rounded-lg text-xs transition-colors',
                isActive(`/wiki/${page.slug}`) ? 'text-primary bg-primary/5 font-semibold' : `text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800`
              ]"
            >
              <span :class="`material-symbols-outlined text-lg text-${cat.color}-400`">{{ page.icon }}</span>
              <span>{{ page.title }}</span>
            </router-link>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Admin section (solo para administradores) -->
    <div v-if="userIsAdmin" class="p-4 border-t border-slate-100 dark:border-slate-800 space-y-2">
      <router-link 
        to="/admin"
        class="flex w-full items-center justify-center gap-2 px-4 py-2.5 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-lg font-medium hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors text-sm"
      >
        <span class="material-symbols-outlined text-lg">admin_panel_settings</span>
        <span>Administración</span>
      </router-link>
      <router-link 
        to="/admin/pages/new"
        class="flex w-full items-center justify-center gap-2 px-4 py-2.5 bg-primary text-white rounded-lg font-bold shadow-lg shadow-primary/20 hover:opacity-90 transition-opacity text-sm"
      >
        <span class="material-symbols-outlined text-xl">add</span>
        <span>Crear Nuevo</span>
      </router-link>
    </div>
  </aside>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { getSidebar, getSettings, isAdmin, search } from '../api'

// User permissions
const userIsAdmin = computed(() => isAdmin())

const route = useRoute()
const categories = ref([])
const siteName = ref('EWiki')
const logoUrl = ref('')
const openSubmenus = reactive({})

// Search
const searchQuery = ref('')
const searchResults = ref({ pages: [], categories: [], sections: [], total: 0 })
const isSearching = ref(false)
const showSearchResults = ref(false)
const searchContainerRef = ref(null)
let searchTimeout = null

const handleSearch = () => {
  // Debounce search
  if (searchTimeout) clearTimeout(searchTimeout)
  
  if (searchQuery.value.length < 2) {
    searchResults.value = { pages: [], categories: [], sections: [], total: 0 }
    showSearchResults.value = false
    return
  }
  
  isSearching.value = true
  showSearchResults.value = true
  
  searchTimeout = setTimeout(async () => {
    try {
      const response = await search(searchQuery.value)
      searchResults.value = response.data
    } catch (error) {
      console.error('Error searching:', error)
      searchResults.value = { pages: [], categories: [], sections: [], total: 0 }
    } finally {
      isSearching.value = false
    }
  }, 300)
}

const clearSearch = () => {
  searchQuery.value = ''
  searchResults.value = { pages: [], categories: [], sections: [], total: 0 }
  showSearchResults.value = false
}

// Close search results when clicking outside
const handleClickOutside = (event) => {
  if (searchContainerRef.value && !searchContainerRef.value.contains(event.target)) {
    showSearchResults.value = false
  }
}

// Ordenar categorías por el campo order
const sortedCategories = computed(() => {
  return [...categories.value].sort((a, b) => {
    if (a.order !== b.order) {
      return a.order - b.order
    }
    return a.name.localeCompare(b.name)
  })
})

const isActive = (path) => {
  return route.path === path
}

const toggleSubmenu = (id) => {
  openSubmenus[id] = !openSubmenus[id]
}

// Auto-open submenu when on a page in that category
watch(() => route.path, (path) => {
  if (path.startsWith('/wiki/')) {
    const slug = path.replace('/wiki/', '')
    for (const cat of categories.value) {
      // Check direct pages
      if (cat.pages?.some(p => p.slug === slug)) {
        openSubmenus[cat.id] = true
        break
      }
      // Check subcategory pages
      for (const subcat of (cat.subcategories || [])) {
        if (subcat.pages?.some(p => p.slug === slug)) {
          openSubmenus[cat.id] = true
          openSubmenus['sub-' + subcat.id] = true
          break
        }
      }
    }
  }
}, { immediate: true })

onMounted(async () => {
  // Add click outside listener for search
  document.addEventListener('click', handleClickOutside)
  
  try {
    // Cargar configuración del sitio
    const settingsRes = await getSettings()
    if (settingsRes.data.site_name) {
      siteName.value = settingsRes.data.site_name
    }
    if (settingsRes.data.logo_url) {
      logoUrl.value = settingsRes.data.logo_url
    }
    
    // Cargar categorías
    const response = await getSidebar()
    categories.value = response.data
    
    // Auto-open current category submenu
    const path = route.path
    if (path.startsWith('/wiki/')) {
      const slug = path.replace('/wiki/', '')
      for (const cat of categories.value) {
        if (cat.pages?.some(p => p.slug === slug)) {
          openSubmenus[cat.id] = true
          break
        }
        for (const subcat of (cat.subcategories || [])) {
          if (subcat.pages?.some(p => p.slug === slug)) {
            openSubmenus[cat.id] = true
            openSubmenus['sub-' + subcat.id] = true
            break
          }
        }
      }
    }
  } catch (error) {
    console.error('Error loading sidebar:', error)
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  if (searchTimeout) clearTimeout(searchTimeout)
})
</script>
