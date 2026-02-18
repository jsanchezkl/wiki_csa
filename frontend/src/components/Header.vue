<template>
  <header class="sticky top-0 z-30 bg-white/80 dark:bg-background-dark/80 backdrop-blur-md border-b border-slate-100 dark:border-slate-800">
    <div class="px-4 sm:px-6 md:px-8 py-3 sm:py-4 flex items-center gap-3 sm:gap-6 md:gap-8">
      <div class="flex-1 flex items-center gap-2 sm:gap-4">
        <!-- Mobile menu button -->
        <button 
          @click="$emit('toggleSidebar')"
          class="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors lg:hidden"
        >
          <span class="material-symbols-outlined text-slate-600 dark:text-slate-400">menu</span>
        </button>
        <router-link 
          v-if="showBack" 
          to="/" 
          class="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors hidden sm:flex"
        >
          <span class="material-symbols-outlined text-slate-600">arrow_back</span>
        </router-link>
        <h2 class="text-slate-900 dark:text-white text-base sm:text-lg md:text-xl font-bold tracking-tight truncate">{{ title }}</h2>
      </div>
      <div class="flex items-center gap-2 sm:gap-4 md:gap-6">
        <button class="p-2 text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors hidden sm:flex">
          <span class="material-symbols-outlined">notifications</span>
        </button>
        
        <!-- User dropdown -->
        <div class="relative" ref="dropdownRef">
          <button 
            @click="toggleDropdown"
            class="flex items-center gap-1 sm:gap-3 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-lg p-1.5 sm:p-2 transition-colors"
          >
            <div class="text-right hidden md:block">
              <p class="text-xs font-bold text-slate-900 dark:text-white">{{ userName }}</p>
              <p class="text-[10px] text-slate-500">{{ userRole }}</p>
            </div>
            <div class="size-8 sm:size-10 flex items-center justify-center rounded-full overflow-hidden ring-2 ring-white dark:ring-slate-700"
                 :class="userIsAdmin ? 'bg-gradient-to-br from-primary to-indigo-600' : 'bg-slate-200 dark:bg-slate-700'">
              <span class="material-symbols-outlined text-white text-lg sm:text-xl">person</span>
            </div>
            <span class="material-symbols-outlined text-slate-400 text-base sm:text-lg hidden sm:block">expand_more</span>
          </button>
          
          <!-- Dropdown menu -->
          <Transition
            enter-active-class="transition-all duration-200"
            enter-from-class="opacity-0 scale-95 -translate-y-2"
            enter-to-class="opacity-100 scale-100 translate-y-0"
            leave-active-class="transition-all duration-150"
            leave-from-class="opacity-100 scale-100"
            leave-to-class="opacity-0 scale-95"
          >
            <div 
              v-show="showDropdown"
              class="absolute right-0 mt-2 w-56 sm:w-64 bg-white dark:bg-slate-800 rounded-xl shadow-xl border border-slate-100 dark:border-slate-700 py-2 z-50"
            >
              <div class="px-4 py-3 border-b border-slate-100 dark:border-slate-700">
                <p class="text-sm font-bold text-slate-900 dark:text-white">{{ userName }}</p>
                <p class="text-xs text-slate-500">{{ userEmail }}</p>
                <span 
                  class="inline-flex items-center gap-1 mt-2 px-2 py-1 rounded-full text-xs font-medium"
                  :class="userIsAdmin ? 'bg-primary/10 text-primary' : 'bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-400'"
                >
                  <span class="material-symbols-outlined text-sm">{{ userIsAdmin ? 'shield_person' : 'person' }}</span>
                  {{ userIsAdmin ? 'Administrador' : 'Lector' }}
                </span>
              </div>
              
              <!-- Admin link (solo para admins) -->
              <div v-if="userIsAdmin" class="py-1 border-b border-slate-100 dark:border-slate-700">
                <router-link 
                  to="/admin" 
                  @click="showDropdown = false"
                  class="flex items-center gap-3 px-4 py-2 text-sm text-primary font-semibold hover:bg-primary/5 transition-colors"
                >
                  <span class="material-symbols-outlined text-lg">admin_panel_settings</span>
                  Panel de Administración
                </router-link>
              </div>
              
              <div class="py-1">
                <button 
                  @click="handleLogout"
                  class="w-full flex items-center gap-3 px-4 py-2 text-sm text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
                >
                  <span class="material-symbols-outlined text-lg">logout</span>
                  Cerrar Sesión
                </button>
              </div>
            </div>
          </Transition>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { logout, getCurrentUser, isAdmin } from '../api'

defineProps({
  title: {
    type: String,
    default: 'Dashboard'
  },
  showBack: {
    type: Boolean,
    default: false
  }
})

defineEmits(['toggleSidebar'])

const router = useRouter()
const showDropdown = ref(false)
const dropdownRef = ref(null)

// User info
const user = computed(() => getCurrentUser())
const userName = computed(() => {
  const u = user.value
  if (!u) return 'Usuario'
  return u.first_name && u.last_name 
    ? `${u.first_name} ${u.last_name}` 
    : u.email?.split('@')[0] || 'Usuario'
})
const userEmail = computed(() => user.value?.email || '')
const userRole = computed(() => user.value?.is_admin ? 'Administrador' : 'Lector')
const userIsAdmin = computed(() => isAdmin())

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
}

const handleLogout = async () => {
  try {
    await logout()
  } catch (e) {
    // Ignorar errores de logout
  }
  
  // Limpiar storage
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user')
  
  // Redirigir a login
  router.push('/login')
}

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    showDropdown.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
