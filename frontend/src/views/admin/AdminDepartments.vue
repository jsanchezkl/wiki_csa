<template>
  <div class="min-h-screen bg-slate-50 dark:bg-background-dark">
    <!-- Admin Header -->
    <header class="sticky top-0 z-30 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800">
      <div class="px-8 py-4 flex items-center justify-between">
        <div class="flex items-center gap-4">
          <router-link 
            to="/admin" 
            class="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors"
          >
            <span class="material-symbols-outlined text-slate-600">arrow_back</span>
          </router-link>
          <div class="flex items-center gap-3">
            <div class="p-2 bg-primary/10 rounded-lg">
              <span class="material-symbols-outlined text-primary">folder</span>
            </div>
            <div>
              <h1 class="text-xl font-bold text-slate-900 dark:text-white">Categorías</h1>
              <p class="text-xs text-slate-500">Gestiona las categorías y subcategorías del Wiki</p>
            </div>
          </div>
        </div>
        <div class="flex items-center gap-4">
          <router-link 
            to="/admin/departments/new"
            class="flex items-center gap-2 bg-primary text-white px-4 py-2 rounded-lg hover:bg-primary/90 transition-colors font-medium"
          >
            <span class="material-symbols-outlined text-lg">add</span>
            Nueva Categoría
          </router-link>
        </div>
      </div>
    </header>

    <div class="p-8">
      <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800">
        <div class="p-6 border-b border-slate-200 dark:border-slate-800">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-bold text-slate-900 dark:text-white">Todas las Categorías</h2>
            <div class="flex items-center gap-2">
              <input 
                type="text" 
                v-model="searchQuery"
                placeholder="Buscar categoría..."
                class="px-4 py-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-sm"
              />
            </div>
          </div>
        </div>
        
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-slate-50 dark:bg-slate-800">
              <tr>
                <th class="text-left px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Categoría</th>
                <th class="text-left px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Categoría Padre</th>
                <th class="text-left px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Slug</th>
                <th class="text-left px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Páginas</th>
                <th class="text-left px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Orden</th>
                <th class="text-left px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Estado</th>
                <th class="text-right px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Acciones</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
              <tr v-for="cat in filteredCategories" :key="cat.id" class="hover:bg-slate-50 dark:hover:bg-slate-800/50">
                <td class="px-6 py-4">
                  <div class="flex items-center gap-3">
                    <span 
                      class="p-2 rounded-lg"
                      :class="`bg-${cat.color}-100 dark:bg-${cat.color}-900/30`"
                    >
                      <span :class="`material-symbols-outlined text-${cat.color}-600`">{{ cat.icon }}</span>
                    </span>
                    <div>
                      <p class="font-medium text-slate-900 dark:text-white">
                        <span v-if="cat.parent_name" class="text-slate-400">└─ </span>
                        {{ cat.name }}
                      </p>
                      <p class="text-xs text-slate-500 truncate max-w-xs">{{ cat.description }}</p>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <span v-if="cat.parent_name" class="text-sm text-slate-600 dark:text-slate-400">{{ cat.parent_name }}</span>
                  <span v-else class="text-xs text-slate-400">— Principal</span>
                </td>
                <td class="px-6 py-4">
                  <code class="text-xs bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded text-slate-600 dark:text-slate-400">{{ cat.slug }}</code>
                </td>
                <td class="px-6 py-4">
                  <span class="text-sm text-slate-600 dark:text-slate-400">{{ cat.pages_count }} páginas</span>
                </td>
                <td class="px-6 py-4">
                  <span class="text-sm font-mono text-slate-600 dark:text-slate-400">{{ cat.order }}</span>
                </td>
                <td class="px-6 py-4">
                  <span 
                    class="text-xs px-2 py-1 rounded-full"
                    :class="cat.is_active ? 'bg-emerald-100 text-emerald-600 dark:bg-emerald-900/30' : 'bg-red-100 text-red-600 dark:bg-red-900/30'"
                  >
                    {{ cat.is_active ? 'Activa' : 'Inactiva' }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <div class="flex items-center justify-end gap-2">
                    <router-link 
                      :to="`/admin/departments/${cat.id}/edit`"
                      class="p-2 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg transition-colors"
                    >
                      <span class="material-symbols-outlined text-lg text-slate-500">edit</span>
                    </router-link>
                    <button 
                      @click="confirmDelete(cat)"
                      class="p-2 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                    >
                      <span class="material-symbols-outlined text-lg text-red-500">delete</span>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div v-if="filteredCategories.length === 0" class="p-12 text-center">
          <span class="material-symbols-outlined text-5xl text-slate-300 mb-4">folder_off</span>
          <p class="text-slate-500">No se encontraron categorías</p>
        </div>
      </div>
    </div>

    <!-- Delete Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 z-50 flex items-center justify-center">
      <div class="absolute inset-0 bg-black/50" @click="showDeleteModal = false"></div>
      <div class="relative bg-white dark:bg-slate-900 rounded-2xl p-6 max-w-md w-full mx-4 shadow-2xl">
        <h3 class="text-lg font-bold text-slate-900 dark:text-white mb-2">Eliminar Categoría</h3>
        <p class="text-slate-500 mb-6">¿Estás seguro de que deseas eliminar "{{ categoryToDelete?.name }}"? Esta acción no se puede deshacer.</p>
        <div class="flex items-center justify-end gap-3">
          <button 
            @click="showDeleteModal = false"
            class="px-4 py-2 text-slate-600 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors"
          >
            Cancelar
          </button>
          <button 
            @click="deleteCategoryConfirmed"
            class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
          >
            Eliminar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getCategories, deleteCategory } from '../../api'

const categories = ref([])
const searchQuery = ref('')
const showDeleteModal = ref(false)
const categoryToDelete = ref(null)

const filteredCategories = computed(() => {
  let result = [...categories.value]
  
  // Sort: main categories first, then subcategories grouped under their parents
  result.sort((a, b) => {
    // If both are main categories or both are subcategories
    if (!a.parent && !b.parent) {
      return a.order - b.order || a.name.localeCompare(b.name)
    }
    if (a.parent && b.parent) {
      if (a.parent === b.parent) {
        return a.order - b.order || a.name.localeCompare(b.name)
      }
      return a.parent - b.parent
    }
    // Main categories come before their subcategories
    if (!a.parent && b.parent === a.id) return -1
    if (!b.parent && a.parent === b.id) return 1
    // Otherwise sort by whether it has a parent
    if (!a.parent) return -1
    if (!b.parent) return 1
    return 0
  })
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(cat => 
      cat.name.toLowerCase().includes(query) ||
      cat.slug.toLowerCase().includes(query)
    )
  }
  
  return result
})

const confirmDelete = (cat) => {
  categoryToDelete.value = cat
  showDeleteModal.value = true
}

const deleteCategoryConfirmed = async () => {
  try {
    await deleteCategory(categoryToDelete.value.id)
    categories.value = categories.value.filter(c => c.id !== categoryToDelete.value.id)
    showDeleteModal.value = false
    categoryToDelete.value = null
  } catch (error) {
    console.error('Error deleting category:', error)
    alert('Error al eliminar la categoría')
  }
}

onMounted(async () => {
  try {
    const response = await getCategories({ all: 'true' })
    categories.value = response.data
  } catch (error) {
    console.error('Error loading categories:', error)
  }
})
</script>
