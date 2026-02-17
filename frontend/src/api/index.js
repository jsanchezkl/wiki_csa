import axios from 'axios'

// URL de la API - configurable via variable de entorno
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor para agregar token a las peticiones
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Interceptor para manejar errores de autenticación
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    
    // Si el token expiró y no hemos intentado refrescar
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (refreshToken) {
          const response = await axios.post('http://localhost:8001/api/auth/refresh/', {
            refresh: refreshToken
          })
          
          localStorage.setItem('access_token', response.data.access)
          originalRequest.headers.Authorization = `Bearer ${response.data.access}`
          
          return api(originalRequest)
        }
      } catch (refreshError) {
        // Si falla el refresh, limpiar y redirigir a login
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
        window.location.href = '/login'
      }
    }
    
    return Promise.reject(error)
  }
)

export default api

// Dashboard
export const getDashboard = () => api.get('/dashboard/')
export const getSidebar = () => api.get('/sidebar/')

// Search
export const search = (query) => api.get('/search/', { params: { q: query } })

// Categories (antes Departments)
export const getCategories = (params = {}) => api.get('/categories/', { params })
export const getCategory = (id) => api.get(`/categories/${id}/`)
export const createCategory = (data) => api.post('/categories/', data)
export const updateCategory = (id, data) => api.put(`/categories/${id}/`, data)
export const deleteCategory = (id) => api.delete(`/categories/${id}/`)
export const getCategoriesTree = () => api.get('/categories/tree/')

// Alias para compatibilidad (Departments -> Categories)
export const getDepartments = (all = false) => api.get('/categories/', { params: { all: all ? 'true' : '' } })
export const getDepartment = (id) => api.get(`/categories/${id}/`)
export const createDepartment = (data) => api.post('/categories/', data)
export const updateDepartment = (id, data) => api.put(`/categories/${id}/`, data)
export const deleteDepartment = (id) => api.delete(`/categories/${id}/`)

// Pages
export const getPages = (params = {}) => api.get('/pages/', { params })
export const getPage = (slug) => api.get(`/pages/${slug}/`)
export const createPage = (data) => api.post('/pages/', data)
export const updatePage = (slug, data) => api.put(`/pages/${slug}/`, data)
export const deletePage = (slug) => api.delete(`/pages/${slug}/`)

// Sections
export const getSections = (pageSlug) => api.get('/sections/', { params: { page: pageSlug } })
export const createSection = (data) => api.post('/sections/', data)
export const updateSection = (id, data) => api.put(`/sections/${id}/`, data)
export const deleteSection = (id) => api.delete(`/sections/${id}/`)
export const bulkUpdateSections = (sections) => api.post('/sections/bulk_update/', { sections })

// Media
export const getMedia = (type) => api.get('/media/', { params: { type } })
export const uploadMedia = (data) => api.post('/media/', data)
export const deleteMedia = (id) => api.delete(`/media/${id}/`)

// Updates
export const getUpdates = () => api.get('/updates/')
export const createUpdate = (data) => api.post('/updates/', data)

// Settings
export const getSettings = () => api.get('/settings/')
export const updateSettings = (data) => api.put('/settings/1/', data)

// Admin Stats
export const getAdminStats = () => api.get('/admin/stats/')

// Chat
export const sendChatMessage = (message, sessionId = null) => 
  api.post('/chat/', { message, session_id: sessionId })

export const getChatHistory = (sessionId) => 
  api.get('/chat/history/', { params: { session_id: sessionId } })

export const indexChatContent = () => 
  api.post('/chat/index/')

export const getChatStats = () => 
  api.get('/chat/stats/')

// Auth
export const login = (email, password) => 
  api.post('/auth/login/', { email, password })

export const refreshToken = (refresh) => 
  api.post('/auth/refresh/', { refresh })

export const logout = () => {
  const refresh = localStorage.getItem('refresh_token')
  return api.post('/auth/logout/', { refresh })
}

export const getMe = () => 
  api.get('/auth/me/')

export const checkAdmin = () => 
  api.get('/auth/check-admin/')

// Helper para verificar si está autenticado
export const isAuthenticated = () => {
  return !!localStorage.getItem('access_token')
}

// Helper para obtener usuario actual
export const getCurrentUser = () => {
  const user = localStorage.getItem('user')
  return user ? JSON.parse(user) : null
}

// Helper para verificar si es admin
export const isAdmin = () => {
  const user = getCurrentUser()
  return user?.is_admin || user?.role === 'admin'
}
