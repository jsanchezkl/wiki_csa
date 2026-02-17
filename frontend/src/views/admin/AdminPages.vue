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
              <span class="material-symbols-outlined text-primary">article</span>
            </div>
            <div>
              <h1 class="text-xl font-bold text-slate-900 dark:text-white">Páginas del Wiki</h1>
              <p class="text-xs text-slate-500">Gestiona el contenido de tu Wiki</p>
            </div>
          </div>
        </div>
        <div class="flex items-center gap-4">
          <router-link 
            to="/admin/pages/new"
            class="flex items-center gap-2 bg-primary text-white px-4 py-2 rounded-lg hover:bg-primary/90 transition-colors font-medium"
          >
            <span class="material-symbols-outlined text-lg">add</span>
            Nueva Página
          </router-link>
        </div>
      </div>
    </header>

    <div class="p-8">
      <!-- Filters -->
      <div class="mb-6 flex items-center gap-4">
        <input 
          type="text" 
          v-model="searchQuery"
          placeholder="Buscar página..."
          class="flex-1 max-w-md px-4 py-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-sm"
        />
        <select 
          v-model="filterDepartment"
          class="px-4 py-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-sm"
        >
          <option value="">Todos los departamentos</option>
          <option v-for="dept in departments" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
        </select>
        <select 
          v-model="filterStatus"
          class="px-4 py-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-sm"
        >
          <option value="">Todos los estados</option>
          <option value="published">Publicadas</option>
          <option value="draft">Borradores</option>
        </select>
      </div>

      <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-slate-50 dark:bg-slate-800">
              <tr>
                <th class="text-left px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Página</th>
                <th class="text-left px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Departamento</th>
                <th class="text-left px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Estado</th>
                <th class="text-left px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Última actualización</th>
                <th class="text-right px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Acciones</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
              <tr v-for="page in filteredPages" :key="page.id" class="hover:bg-slate-50 dark:hover:bg-slate-800/50">
                <td class="px-6 py-4">
                  <div class="flex items-center gap-3">
                    <span class="material-symbols-outlined text-slate-400">{{ page.icon }}</span>
                    <div>
                      <p class="font-medium text-slate-900 dark:text-white">{{ page.title }}</p>
                      <code class="text-xs text-slate-400">/wiki/{{ page.slug }}</code>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <span class="text-sm text-slate-600 dark:text-slate-400">{{ page.department_name }}</span>
                </td>
                <td class="px-6 py-4">
                  <span 
                    class="text-xs px-2 py-1 rounded-full"
                    :class="page.is_published ? 'bg-emerald-100 text-emerald-600 dark:bg-emerald-900/30' : 'bg-amber-100 text-amber-600 dark:bg-amber-900/30'"
                  >
                    {{ page.is_published ? 'Publicada' : 'Borrador' }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <span class="text-sm text-slate-500">{{ formatDate(page.updated_at) }}</span>
                </td>
                <td class="px-6 py-4">
                  <div class="flex items-center justify-end gap-2">
                    <router-link 
                      :to="`/wiki/${page.slug}`"
                      class="p-2 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg transition-colors"
                      target="_blank"
                    >
                      <span class="material-symbols-outlined text-lg text-slate-500">visibility</span>
                    </router-link>
                    <router-link 
                      :to="`/admin/pages/${page.slug}/edit`"
                      class="p-2 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg transition-colors"
                    >
                      <span class="material-symbols-outlined text-lg text-slate-500">edit</span>
                    </router-link>
                    <button 
                      @click="confirmDelete(page)"
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
        
        <div v-if="filteredPages.length === 0" class="p-12 text-center">
          <span class="material-symbols-outlined text-5xl text-slate-300 mb-4">article</span>
          <p class="text-slate-500 mb-4">No se encontraron páginas</p>
          <router-link 
            to="/admin/pages/new"
            class="text-primary font-medium hover:underline"
          >
            Crear tu primera página
          </router-link>
        </div>
      </div>
    </div>

    <!-- Delete Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 z-50 flex items-center justify-center">
      <div class="absolute inset-0 bg-black/50" @click="showDeleteModal = false"></div>
      <div class="relative bg-white dark:bg-slate-900 rounded-2xl p-6 max-w-md w-full mx-4 shadow-2xl">
        <h3 class="text-lg font-bold text-slate-900 dark:text-white mb-2">Eliminar Página</h3>
        <p class="text-slate-500 mb-6">¿Estás seguro de que deseas eliminar "{{ pageToDelete?.title }}"? Esta acción no se puede deshacer.</p>
        <div class="flex items-center justify-end gap-3">
          <button 
            @click="showDeleteModal = false"
            class="px-4 py-2 text-slate-600 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors"
          >
            Cancelar
          </button>
          <button 
            @click="deletePageConfirmed"
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
import { getPages, getDepartments, deletePage } from '../../api'

const pages = ref([])
const departments = ref([])
const searchQuery = ref('')
const filterDepartment = ref('')
const filterStatus = ref('')
const showDeleteModal = ref(false)
const pageToDelete = ref(null)

const filteredPages = computed(() => {
  let result = pages.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(page => 
      page.title.toLowerCase().includes(query) ||
      page.slug.toLowerCase().includes(query)
    )
  }

  if (filterDepartment.value) {
    result = result.filter(page => page.department === parseInt(filterDepartment.value))
  }

  if (filterStatus.value) {
    result = result.filter(page => 
      filterStatus.value === 'published' ? page.is_published : !page.is_published
    )
  }

  return result
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', { 
    day: 'numeric', 
    month: 'short', 
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const confirmDelete = (page) => {
  pageToDelete.value = page
  showDeleteModal.value = true
}

const deletePageConfirmed = async () => {
  try {
    await deletePage(pageToDelete.value.slug)
    pages.value = pages.value.filter(p => p.id !== pageToDelete.value.id)
    showDeleteModal.value = false
    pageToDelete.value = null
  } catch (error) {
    console.error('Error deleting page:', error)
    alert('Error al eliminar la página')
  }
}

onMounted(async () => {
  try {
    const [pagesRes, deptsRes] = await Promise.all([
      getPages({ all: 'true' }),
      getDepartments(true)
    ])
    pages.value = pagesRes.data
    departments.value = deptsRes.data
  } catch (error) {
    console.error('Error loading data:', error)
  }
})
</script>




