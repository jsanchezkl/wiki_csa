<template>
  <div class="min-h-screen bg-slate-50 dark:bg-background-dark">
    <!-- Header -->
    <header class="sticky top-0 z-30 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800">
      <div class="px-8 py-4 flex items-center justify-between">
        <div class="flex items-center gap-4">
          <router-link 
            to="/admin/departments" 
            class="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors"
          >
            <span class="material-symbols-outlined text-slate-600">arrow_back</span>
          </router-link>
          <div>
            <h1 class="text-xl font-bold text-slate-900 dark:text-white">
              {{ isEditing ? 'Editar Categoría' : 'Nueva Categoría' }}
            </h1>
            <p class="text-xs text-slate-500">{{ isEditing ? 'Modifica los datos de la categoría' : 'Crea una nueva categoría o subcategoría' }}</p>
          </div>
        </div>
        <div class="flex items-center gap-4">
          <button 
            @click="saveCategory"
            :disabled="saving"
            class="flex items-center gap-2 bg-primary text-white px-4 py-2 rounded-lg hover:bg-primary/90 transition-colors font-medium disabled:opacity-50"
          >
            <span v-if="saving" class="material-symbols-outlined animate-spin text-lg">sync</span>
            <span v-else class="material-symbols-outlined text-lg">save</span>
            {{ saving ? 'Guardando...' : 'Guardar' }}
          </button>
        </div>
      </div>
    </header>

    <div class="max-w-3xl mx-auto p-8">
      <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800">
        <div class="p-6 space-y-6">
          <!-- Parent Category (for subcategories) -->
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
              Categoría Padre (opcional)
            </label>
            <select 
              v-model="form.parent"
              class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/20 focus:border-primary transition-colors"
            >
              <option :value="null">— Categoría Principal (sin padre)</option>
              <option v-for="cat in parentCategories" :key="cat.id" :value="cat.id">
                {{ cat.name }}
              </option>
            </select>
            <p class="text-xs text-slate-500 mt-1">
              Deja vacío para crear una categoría principal. Selecciona una categoría para crear una subcategoría.
            </p>
          </div>

          <!-- Name -->
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
              Nombre de la Categoría *
            </label>
            <input 
              type="text" 
              v-model="form.name"
              placeholder="Ej: Human Resources"
              class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/20 focus:border-primary transition-colors"
            />
          </div>

          <!-- Slug -->
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
              Slug (URL)
            </label>
            <input 
              type="text" 
              v-model="form.slug"
              placeholder="Generado automáticamente"
              class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/20 focus:border-primary transition-colors"
            />
            <p class="text-xs text-slate-500 mt-1">Deja vacío para generar automáticamente desde el nombre</p>
          </div>

          <!-- Description -->
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
              Descripción
            </label>
            <textarea 
              v-model="form.description"
              rows="3"
              placeholder="Breve descripción de la categoría"
              class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/20 focus:border-primary transition-colors resize-none"
            ></textarea>
          </div>

          <!-- Icon and Color -->
          <div class="grid grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                Icono
              </label>
              <div class="relative">
                <input 
                  type="text" 
                  v-model="form.icon"
                  placeholder="Ej: groups, folder, settings"
                  class="w-full px-4 py-3 pl-12 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/20 focus:border-primary transition-colors"
                />
                <span class="absolute left-4 top-1/2 -translate-y-1/2 material-symbols-outlined text-slate-400">{{ form.icon }}</span>
              </div>
              <p class="text-xs text-slate-500 mt-1">
                <a href="https://fonts.google.com/icons" target="_blank" class="text-primary hover:underline">Ver iconos disponibles</a>
              </p>
            </div>

            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                Color
              </label>
              <div class="grid grid-cols-6 gap-2">
                <button 
                  v-for="color in colors" 
                  :key="color"
                  @click="form.color = color"
                  class="w-10 h-10 rounded-lg transition-all"
                  :class="[
                    `bg-${color}-500`,
                    form.color === color ? 'ring-2 ring-offset-2 ring-slate-900' : ''
                  ]"
                ></button>
              </div>
            </div>
          </div>

          <!-- Order -->
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
              Orden de visualización
            </label>
            <input 
              type="number" 
              v-model="form.order"
              min="0"
              class="w-24 px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/20 focus:border-primary transition-colors"
            />
            <p class="text-xs text-slate-500 mt-1">Número menor = aparece primero. Usa números únicos para un orden específico.</p>
          </div>

          <!-- Active -->
          <div class="flex items-center gap-3">
            <button 
              @click="form.is_active = !form.is_active"
              class="relative w-12 h-6 rounded-full transition-colors"
              :class="form.is_active ? 'bg-primary' : 'bg-slate-300 dark:bg-slate-700'"
            >
              <span 
                class="absolute top-1 w-4 h-4 bg-white rounded-full transition-transform shadow"
                :class="form.is_active ? 'left-7' : 'left-1'"
              ></span>
            </button>
            <span class="text-sm text-slate-700 dark:text-slate-300">
              {{ form.is_active ? 'Categoría activa' : 'Categoría inactiva' }}
            </span>
          </div>
        </div>
      </div>

      <!-- Preview -->
      <div class="mt-8 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6">
        <h3 class="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-4">Vista Previa</h3>
        <div class="flex items-center gap-4 p-4 rounded-xl bg-slate-50 dark:bg-slate-800">
          <span 
            class="p-3 rounded-xl"
            :class="`bg-${form.color}-100 dark:bg-${form.color}-900/30`"
          >
            <span :class="`material-symbols-outlined text-2xl text-${form.color}-600`">{{ form.icon }}</span>
          </span>
          <div>
            <p class="font-bold text-slate-900 dark:text-white">
              <span v-if="selectedParentName" class="text-slate-400 text-sm">{{ selectedParentName }} > </span>
              {{ form.name || 'Nombre de la Categoría' }}
            </p>
            <p class="text-sm text-slate-500">{{ form.description || 'Descripción de la categoría' }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { getCategory, getCategories, createCategory, updateCategory } from '../../api'

const router = useRouter()

const props = defineProps({
  id: String
})

const isEditing = !!props.id
const saving = ref(false)
const parentCategories = ref([])

const colors = ['blue', 'indigo', 'emerald', 'amber', 'rose', 'purple']

const form = ref({
  name: '',
  slug: '',
  description: '',
  icon: 'folder',
  color: 'blue',
  order: 0,
  is_active: true,
  parent: null
})

const selectedParentName = computed(() => {
  if (!form.value.parent) return null
  const parent = parentCategories.value.find(c => c.id === form.value.parent)
  return parent ? parent.name : null
})

const generateSlug = (name) => {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '')
}

watch(() => form.value.name, (newName) => {
  if (!isEditing && newName && !form.value.slug) {
    form.value.slug = generateSlug(newName)
  }
})

const saveCategory = async () => {
  if (!form.value.name) {
    alert('El nombre es requerido')
    return
  }

  saving.value = true
  try {
    const data = { ...form.value }
    // Convert null parent to undefined for API
    if (data.parent === null || data.parent === '') {
      delete data.parent
    }
    
    if (isEditing) {
      await updateCategory(props.id, data)
    } else {
      await createCategory(data)
    }
    router.push('/admin/departments')
  } catch (error) {
    console.error('Error saving category:', error)
    alert('Error al guardar la categoría: ' + (error.response?.data?.detail || error.message))
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  try {
    // Load parent categories (only main categories, not subcategories)
    const catsRes = await getCategories({ all: 'true', parent: 'null' })
    parentCategories.value = catsRes.data.filter(c => !c.parent)
    
    if (isEditing) {
      const response = await getCategory(props.id)
      form.value = { ...response.data }
      // Remove the current category from parent options to avoid circular reference
      parentCategories.value = parentCategories.value.filter(c => c.id !== parseInt(props.id))
    }
  } catch (error) {
    console.error('Error loading data:', error)
  }
})
</script>
