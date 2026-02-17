<template>
  <div class="min-h-screen bg-slate-50 dark:bg-background-dark">
    <!-- Header -->
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
              <span class="material-symbols-outlined text-primary">settings</span>
            </div>
            <div>
              <h1 class="text-xl font-bold text-slate-900 dark:text-white">Configuración</h1>
              <p class="text-xs text-slate-500">Personaliza tu Wiki corporativo</p>
            </div>
          </div>
        </div>
        <div class="flex items-center gap-4">
          <button 
            @click="saveSettings"
            :disabled="saving"
            class="flex items-center gap-2 bg-primary text-white px-4 py-2 rounded-lg hover:bg-primary/90 transition-colors font-medium disabled:opacity-50"
          >
            <span v-if="saving" class="material-symbols-outlined animate-spin text-lg">sync</span>
            <span v-else class="material-symbols-outlined text-lg">save</span>
            {{ saving ? 'Guardando...' : 'Guardar Cambios' }}
          </button>
        </div>
      </div>
    </header>

    <div class="max-w-3xl mx-auto p-8">
      <!-- Site Info -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 mb-6">
        <div class="p-6 border-b border-slate-200 dark:border-slate-800">
          <h2 class="text-lg font-bold text-slate-900 dark:text-white">Información del Sitio</h2>
        </div>
        <div class="p-6 space-y-6">
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
              Nombre del Sitio
            </label>
            <input 
              type="text" 
              v-model="form.site_name"
              placeholder="EWiki"
              class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/20 focus:border-primary transition-colors"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
              Descripción del Sitio
            </label>
            <textarea 
              v-model="form.site_description"
              rows="3"
              placeholder="Base de conocimiento corporativa"
              class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/20 focus:border-primary transition-colors resize-none"
            ></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
              Logo del Sitio
            </label>
            <div class="flex items-start gap-4">
              <!-- Logo Preview -->
              <div class="shrink-0">
                <div 
                  class="w-24 h-24 rounded-xl border-2 border-dashed border-slate-300 dark:border-slate-600 flex items-center justify-center bg-slate-50 dark:bg-slate-800 overflow-hidden"
                >
                  <img 
                    v-if="form.logo_url" 
                    :src="form.logo_url" 
                    alt="Logo Preview"
                    class="max-w-full max-h-full object-contain"
                    @error="handleLogoError"
                  />
                  <span v-else class="material-symbols-outlined text-3xl text-slate-400">image</span>
                </div>
              </div>
              
              <!-- URL Input -->
              <div class="flex-1">
                <input 
                  type="text" 
                  v-model="form.logo_url"
                  placeholder="/logo_csa.png"
                  class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/20 focus:border-primary transition-colors"
                />
                <p class="mt-2 text-xs text-slate-500">
                  Puedes usar una URL completa o una ruta local como <code class="bg-slate-100 dark:bg-slate-700 px-1 rounded">/logo_csa.png</code>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Welcome Message -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 mb-6">
        <div class="p-6 border-b border-slate-200 dark:border-slate-800">
          <h2 class="text-lg font-bold text-slate-900 dark:text-white">Mensaje de Bienvenida</h2>
          <p class="text-sm text-slate-500">Personaliza el mensaje que aparece en el Dashboard</p>
        </div>
        <div class="p-6 space-y-6">
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
              Título de Bienvenida
            </label>
            <input 
              type="text" 
              v-model="form.welcome_title"
              placeholder="Welcome back, Alex!"
              class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/20 focus:border-primary transition-colors"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
              Mensaje de Bienvenida
            </label>
            <textarea 
              v-model="form.welcome_message"
              rows="3"
              placeholder="You have 3 new updates in the HR department..."
              class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/20 focus:border-primary transition-colors resize-none"
            ></textarea>
          </div>
        </div>
      </div>

      <!-- Preview -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800">
        <div class="p-6 border-b border-slate-200 dark:border-slate-800">
          <h2 class="text-lg font-bold text-slate-900 dark:text-white">Vista Previa del Dashboard</h2>
        </div>
        <div class="p-6">
          <div class="bg-gradient-to-br from-blue-500 via-primary to-indigo-600 rounded-2xl p-8 text-white">
            <div class="flex items-center gap-4 mb-4" v-if="form.logo_url">
              <img :src="form.logo_url" alt="Logo" class="h-12 w-auto object-contain" />
            </div>
            <h2 class="text-2xl font-bold mb-2">{{ form.welcome_title || 'Welcome back!' }}</h2>
            <p class="text-blue-100 text-sm">{{ form.welcome_message || 'Your personalized wiki experience awaits.' }}</p>
          </div>
        </div>
      </div>

      <!-- Success Message -->
      <div v-if="showSuccess" class="fixed bottom-8 right-8 bg-emerald-500 text-white px-6 py-3 rounded-xl shadow-lg flex items-center gap-3 animate-pulse">
        <span class="material-symbols-outlined">check_circle</span>
        <span>Configuración guardada correctamente</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getSettings, updateSettings } from '../../api'

const saving = ref(false)
const showSuccess = ref(false)
const logoError = ref(false)

const form = ref({
  site_name: '',
  site_description: '',
  logo_url: '',
  welcome_title: '',
  welcome_message: ''
})

const handleLogoError = () => {
  logoError.value = true
}

const saveSettings = async () => {
  saving.value = true
  try {
    await updateSettings(form.value)
    showSuccess.value = true
    setTimeout(() => {
      showSuccess.value = false
    }, 3000)
  } catch (error) {
    console.error('Error saving settings:', error)
    alert('Error al guardar la configuración')
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  try {
    const response = await getSettings()
    form.value = response.data
  } catch (error) {
    console.error('Error loading settings:', error)
  }
})
</script>

