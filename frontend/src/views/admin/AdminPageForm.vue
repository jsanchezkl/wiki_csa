<template>
  <div class="min-h-screen bg-slate-50 dark:bg-background-dark">
    <!-- Header -->
    <header class="sticky top-0 z-30 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800">
      <div class="px-8 py-4 flex items-center justify-between">
        <div class="flex items-center gap-4">
          <router-link 
            to="/admin/pages" 
            class="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors"
          >
            <span class="material-symbols-outlined text-slate-600">arrow_back</span>
          </router-link>
          <div>
            <h1 class="text-xl font-bold text-slate-900 dark:text-white">
              {{ isEditing ? 'Editar Página' : 'Nueva Página' }}
            </h1>
            <p class="text-xs text-slate-500">{{ isEditing ? 'Modifica el contenido de la página' : 'Crea una nueva página para tu Wiki' }}</p>
          </div>
        </div>
        <div class="flex items-center gap-4">
          <button 
            @click="savePage(false)"
            :disabled="saving"
            class="flex items-center gap-2 px-4 py-2 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
          >
            <span class="material-symbols-outlined text-lg text-slate-500">save</span>
            Guardar Borrador
          </button>
          <button 
            @click="savePage(true)"
            :disabled="saving"
            class="flex items-center gap-2 bg-primary text-white px-4 py-2 rounded-lg hover:bg-primary/90 transition-colors font-medium disabled:opacity-50"
          >
            <span v-if="saving" class="material-symbols-outlined animate-spin text-lg">sync</span>
            <span v-else class="material-symbols-outlined text-lg">publish</span>
            {{ saving ? 'Publicando...' : 'Publicar' }}
          </button>
        </div>
      </div>
    </header>

    <div class="flex">
      <!-- Main Editor -->
      <div class="flex-1 p-8 max-w-4xl">
        <!-- Basic Info -->
        <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 mb-6">
          <div class="p-6 border-b border-slate-200 dark:border-slate-800">
            <h2 class="text-lg font-bold text-slate-900 dark:text-white">Información Básica</h2>
          </div>
          <div class="p-6 space-y-6">
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                Título de la Página *
              </label>
              <input 
                type="text" 
                v-model="form.title"
                placeholder="Ej: Employee Policies & Benefits"
                class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-lg font-semibold focus:ring-2 focus:ring-primary/20 focus:border-primary transition-colors"
              />
            </div>

            <div class="grid grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                  Slug (URL)
                </label>
                <div class="flex items-center gap-2">
                  <span class="text-slate-400 text-sm">/wiki/</span>
                  <input 
                    type="text" 
                    v-model="form.slug"
                    placeholder="policies-benefits"
                    class="flex-1 px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/20 focus:border-primary transition-colors"
                  />
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                  Categoría *
                </label>
                <select 
                  v-model="form.category"
                  class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/20 focus:border-primary transition-colors"
                >
                  <option value="">Selecciona una categoría</option>
                  <optgroup v-for="cat in mainCategories" :key="cat.id" :label="cat.name">
                    <option :value="cat.id">{{ cat.name }}</option>
                    <option v-for="subcat in getSubcategories(cat.id)" :key="subcat.id" :value="subcat.id">
                      &nbsp;&nbsp;└─ {{ subcat.name }}
                    </option>
                  </optgroup>
                </select>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                Encabezado
              </label>
              <input 
                type="text" 
                v-model="form.heading"
                placeholder="Ej: Employee Policies & Benefits"
                class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/20 focus:border-primary transition-colors"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                Descripción
              </label>
              <textarea 
                v-model="form.description"
                rows="3"
                placeholder="Breve descripción de la página que aparecerá debajo del título"
                class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/20 focus:border-primary transition-colors resize-none"
              ></textarea>
            </div>
          </div>
        </div>

        <!-- Content Editor -->
        <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 mb-6">
          <div class="p-6 border-b border-slate-200 dark:border-slate-800">
            <h2 class="text-lg font-bold text-slate-900 dark:text-white">Contenido</h2>
            <p class="text-sm text-slate-500">Usa el editor para crear tu contenido. Puedes añadir imágenes, enlaces, listas y más.</p>
          </div>
          <div class="p-6">
            <RichTextEditor v-model="form.content" placeholder="Escribe el contenido de tu página aquí..." />
          </div>
        </div>

        <!-- Sections -->
        <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800">
          <div class="p-6 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
            <div>
              <h2 class="text-lg font-bold text-slate-900 dark:text-white">Secciones</h2>
              <p class="text-sm text-slate-500">Añade secciones para organizar mejor el contenido</p>
            </div>
            <button 
              @click="addSection"
              class="flex items-center gap-2 text-primary font-medium hover:underline"
            >
              <span class="material-symbols-outlined text-lg">add</span>
              Añadir Sección
            </button>
          </div>
          <div class="p-6">
            <div v-if="form.sections.length === 0" class="text-center py-8">
              <span class="material-symbols-outlined text-4xl text-slate-300 mb-2">view_list</span>
              <p class="text-slate-500">No hay secciones aún</p>
              <button @click="addSection" class="text-primary font-medium hover:underline">
                Añadir primera sección
              </button>
            </div>
            
            <div v-else class="space-y-6">
              <div 
                v-for="(section, index) in form.sections" 
                :key="index"
                class="border border-slate-200 dark:border-slate-700 rounded-xl"
              >
                <div class="flex items-center gap-4 p-4 bg-slate-50 dark:bg-slate-800 rounded-t-xl">
                  <span class="material-symbols-outlined text-slate-400 cursor-move">drag_indicator</span>
                  <input 
                    type="text" 
                    v-model="section.title"
                    placeholder="Título de la sección"
                    class="flex-1 px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white font-medium"
                  />
                  <input 
                    type="text" 
                    v-model="section.icon"
                    placeholder="Icono"
                    class="w-32 px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white"
                  />
                  <button 
                    @click="removeSection(index)"
                    class="p-2 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                  >
                    <span class="material-symbols-outlined text-lg text-red-500">delete</span>
                  </button>
                </div>
                <div class="p-4">
                  <RichTextEditor v-model="section.content" placeholder="Contenido de la sección..." />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Sidebar Settings -->
      <div class="w-80 p-8 border-l border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 min-h-screen">
        <h3 class="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-6">Configuración</h3>
        
        <!-- Sidebar Help -->
        <div class="mb-6">
          <h4 class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-3">Sidebar de Ayuda</h4>
          <div class="space-y-4">
            <div>
              <label class="block text-xs text-slate-500 mb-1">Texto de ayuda</label>
              <input 
                type="text" 
                v-model="form.help_text"
                placeholder="Questions? Contact HR"
                class="w-full px-4 py-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-sm"
              />
            </div>
            <div>
              <label class="block text-xs text-slate-500 mb-1">Texto del botón</label>
              <input 
                type="text" 
                v-model="form.help_button_text"
                placeholder="Contact Support"
                class="w-full px-4 py-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-sm"
              />
            </div>
          </div>
        </div>

        <!-- Page Icon -->
        <div class="mb-6">
          <h4 class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-3">Icono de la Página</h4>
          <div class="relative">
            <input 
              type="text" 
              v-model="form.icon"
              placeholder="description"
              class="w-full px-4 py-2 pl-10 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-sm"
            />
            <span class="absolute left-3 top-1/2 -translate-y-1/2 material-symbols-outlined text-slate-400 text-sm">{{ form.icon }}</span>
          </div>
        </div>

        <!-- Options -->
        <div class="mb-6">
          <h4 class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-3">Opciones</h4>
          <div class="space-y-3">
            <label class="flex items-center gap-3 cursor-pointer">
              <input type="checkbox" v-model="form.is_featured" class="w-4 h-4 text-primary rounded" />
              <span class="text-sm text-slate-600 dark:text-slate-400">Página destacada</span>
            </label>
          </div>
        </div>

        <!-- Preview Card -->
        <div class="mt-8 pt-6 border-t border-slate-200 dark:border-slate-700">
          <h4 class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-3">Vista Previa</h4>
          <div class="rounded-xl overflow-hidden border border-slate-200 dark:border-slate-700 p-4 bg-white dark:bg-slate-800">
            <div class="flex items-center gap-3 mb-2">
              <span class="material-symbols-outlined text-primary">{{ form.icon }}</span>
              <p class="font-bold text-slate-900 dark:text-white text-sm">{{ form.title || 'Título de la página' }}</p>
            </div>
            <p class="text-xs text-slate-500">{{ form.description || 'Descripción de la página' }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getPage, createPage, updatePage, getCategories } from '../../api'
import RichTextEditor from '../../components/RichTextEditor.vue'

const router = useRouter()
const route = useRoute()

const props = defineProps({
  slug: String
})

const isEditing = !!props.slug
const saving = ref(false)
const categories = ref([])

const mainCategories = computed(() => {
  return categories.value.filter(c => !c.parent)
})

const getSubcategories = (parentId) => {
  return categories.value.filter(c => c.parent === parentId)
}

const form = ref({
  title: '',
  slug: '',
  category: '',
  heading: '',
  description: '',
  content: '',
  help_text: '',
  help_button_text: 'Contact Support',
  icon: 'description',
  is_published: false,
  is_featured: false,
  sections: []
})

const generateSlug = (name) => {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '')
}

watch(() => form.value.title, (newTitle) => {
  if (!isEditing && newTitle && !form.value.slug) {
    form.value.slug = generateSlug(newTitle)
  }
  if (!form.value.heading) {
    form.value.heading = newTitle
  }
})

const addSection = () => {
  form.value.sections.push({
    title: '',
    slug: '',
    icon: 'article',
    content: '',
    order: form.value.sections.length
  })
}

const removeSection = (index) => {
  form.value.sections.splice(index, 1)
}

const savePage = async (publish = false) => {
  if (!form.value.title || !form.value.category) {
    alert('El título y categoría son requeridos')
    return
  }

  saving.value = true
  
  const data = {
    ...form.value,
    is_published: publish,
    sections: form.value.sections.map((s, i) => ({
      ...s,
      slug: s.slug || generateSlug(s.title),
      order: i
    }))
  }

  try {
    if (isEditing) {
      await updatePage(props.slug, data)
    } else {
      await createPage(data)
    }
    router.push('/admin/pages')
  } catch (error) {
    console.error('Error saving page:', error)
    alert('Error al guardar la página: ' + (error.response?.data?.detail || error.message))
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  try {
    const catsRes = await getCategories({ all: 'true' })
    categories.value = catsRes.data

    if (isEditing) {
      const pageRes = await getPage(props.slug)
      const pageData = pageRes.data
      form.value = {
        ...pageData,
        category: pageData.category,
        sections: pageData.sections || []
      }
    }
  } catch (error) {
    console.error('Error loading data:', error)
  }
})
</script>

