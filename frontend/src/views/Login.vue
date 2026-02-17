<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 relative overflow-hidden">
    <!-- Animated Background -->
    <div class="absolute inset-0">
      <!-- Gradient Orbs -->
      <div class="absolute top-1/4 -left-20 w-96 h-96 bg-indigo-500/20 rounded-full blur-3xl animate-pulse"></div>
      <div class="absolute bottom-1/4 -right-20 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse" style="animation-delay: 1s;"></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary/10 rounded-full blur-3xl"></div>
      
      <!-- Grid Pattern -->
      <div class="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:64px_64px]"></div>
    </div>

    <!-- Login Card -->
    <div class="relative z-10 w-full max-w-md mx-4">
      <!-- Logo & Title -->
      <div class="text-center mb-8">
        <div v-if="logoUrl" class="mb-6">
          <img 
            :src="logoUrl" 
            :alt="siteName"
            class="h-16 w-auto mx-auto object-contain"
          />
        </div>
        <div v-else class="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-primary to-indigo-600 rounded-2xl shadow-2xl shadow-primary/30 mb-6">
          <span class="material-symbols-outlined text-white text-4xl">auto_stories</span>
        </div>
        <h1 class="text-3xl font-bold text-white mb-2">{{ siteName }}</h1>
        <p class="text-slate-400">Base de Conocimiento Corporativa</p>
      </div>

      <!-- Login Form Card -->
      <div class="bg-white/5 backdrop-blur-xl rounded-3xl p-8 border border-white/10 shadow-2xl">
        <h2 class="text-xl font-semibold text-white mb-6">Iniciar Sesión</h2>
        
        <!-- Error Alert -->
        <Transition
          enter-active-class="transition-all duration-300"
          enter-from-class="opacity-0 -translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition-all duration-200"
          leave-from-class="opacity-100"
          leave-to-class="opacity-0"
        >
          <div 
            v-if="error"
            class="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-xl flex items-start gap-3"
          >
            <span class="material-symbols-outlined text-red-400">error</span>
            <div>
              <p class="text-red-400 font-medium">{{ error }}</p>
              <p v-if="errorDetail" class="text-red-400/70 text-sm mt-1">{{ errorDetail }}</p>
            </div>
          </div>
        </Transition>

        <form @submit.prevent="handleLogin" class="space-y-5">
          <!-- Email Field -->
          <div>
            <label class="block text-sm font-medium text-slate-300 mb-2">
              Correo electrónico
            </label>
            <div class="relative">
              <span class="absolute left-4 top-1/2 -translate-y-1/2 material-symbols-outlined text-slate-400">
                mail
              </span>
              <input 
                v-model="email"
                type="email"
                placeholder="tu@correo.com"
                required
                class="w-full pl-12 pr-4 py-4 bg-white/5 border border-white/10 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary/50 transition-all"
                :class="{ 'border-red-500/50': error }"
              />
            </div>
          </div>

          <!-- Password Field -->
          <div>
            <label class="block text-sm font-medium text-slate-300 mb-2">
              Contraseña
            </label>
            <div class="relative">
              <span class="absolute left-4 top-1/2 -translate-y-1/2 material-symbols-outlined text-slate-400">
                lock
              </span>
              <input 
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="••••••••"
                required
                class="w-full pl-12 pr-12 py-4 bg-white/5 border border-white/10 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary/50 transition-all"
                :class="{ 'border-red-500/50': error }"
              />
              <button 
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white transition-colors"
              >
                <span class="material-symbols-outlined">
                  {{ showPassword ? 'visibility_off' : 'visibility' }}
                </span>
              </button>
            </div>
          </div>

          <!-- Remember Me -->
          <div class="flex items-center justify-between">
            <label class="flex items-center gap-2 cursor-pointer">
              <input 
                type="checkbox" 
                v-model="rememberMe"
                class="w-4 h-4 rounded border-white/20 bg-white/5 text-primary focus:ring-primary/50"
              />
              <span class="text-sm text-slate-400">Recordarme</span>
            </label>
          </div>

          <!-- Submit Button -->
          <button 
            type="submit"
            :disabled="isLoading"
            class="w-full py-4 bg-gradient-to-r from-primary to-indigo-600 text-white font-semibold rounded-xl hover:from-primary/90 hover:to-indigo-600/90 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:ring-offset-2 focus:ring-offset-slate-900 transition-all disabled:opacity-70 disabled:cursor-wait flex items-center justify-center gap-2"
          >
            <span 
              v-if="isLoading" 
              class="material-symbols-outlined animate-spin"
            >
              progress_activity
            </span>
            <span>{{ isLoading ? 'Ingresando...' : 'Ingresar' }}</span>
          </button>
        </form>
      </div>

      <!-- Footer -->
      <p class="text-center text-slate-500 text-sm mt-8">
        © {{ new Date().getFullYear() }} {{ siteName }}. Todos los derechos reservados.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { login, getSettings } from '../api'

const router = useRouter()
const route = useRoute()

const email = ref('')
const password = ref('')
const showPassword = ref(false)
const rememberMe = ref(true)
const isLoading = ref(false)
const error = ref('')
const errorDetail = ref('')
const siteName = ref('EWiki')
const logoUrl = ref('')

// Cargar nombre del sitio y logo
onMounted(async () => {
  try {
    const res = await getSettings()
    if (res.data.site_name) {
      siteName.value = res.data.site_name
    }
    if (res.data.logo_url) {
      logoUrl.value = res.data.logo_url
    }
  } catch (e) {
    // Ignorar error
  }
  
  // Verificar si ya está autenticado
  const token = localStorage.getItem('access_token')
  if (token) {
    router.push(route.query.redirect || '/')
  }
})

const handleLogin = async () => {
  error.value = ''
  errorDetail.value = ''
  isLoading.value = true

  try {
    const response = await login(email.value, password.value)
    
    // Guardar tokens
    localStorage.setItem('access_token', response.data.access)
    localStorage.setItem('refresh_token', response.data.refresh)
    localStorage.setItem('user', JSON.stringify(response.data.user))
    
    // Redirigir
    const redirect = route.query.redirect || '/'
    router.push(redirect)
    
  } catch (err) {
    if (err.response?.data) {
      error.value = err.response.data.error || 'Error de autenticación'
      errorDetail.value = err.response.data.detail || ''
    } else {
      error.value = 'Error de conexión'
      errorDetail.value = 'No se pudo conectar con el servidor'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* Custom checkbox styling */
input[type="checkbox"] {
  appearance: none;
  -webkit-appearance: none;
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.05);
  cursor: pointer;
  position: relative;
  transition: all 0.2s;
}

input[type="checkbox"]:checked {
  background: var(--color-primary, #6366f1);
  border-color: var(--color-primary, #6366f1);
}

input[type="checkbox"]:checked::after {
  content: '';
  position: absolute;
  left: 5px;
  top: 2px;
  width: 5px;
  height: 9px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}
</style>

