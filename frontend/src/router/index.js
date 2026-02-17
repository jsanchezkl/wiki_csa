import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import WikiPage from '../views/WikiPage.vue'
import Login from '../views/Login.vue'
import { isAuthenticated, isAdmin } from '../api'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { public: true, hideLayout: true }
  },
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/wiki/:slug',
    name: 'WikiPage',
    component: WikiPage,
    props: true,
    meta: { requiresAuth: true }
  },
  // Admin routes
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/admin/AdminDashboard.vue'),
    meta: { title: 'Administración', requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/departments',
    name: 'AdminDepartments',
    component: () => import('../views/admin/AdminDepartments.vue'),
    meta: { title: 'Departamentos', requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/departments/new',
    name: 'AdminDepartmentNew',
    component: () => import('../views/admin/AdminDepartmentForm.vue'),
    meta: { title: 'Nuevo Departamento', requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/departments/:id/edit',
    name: 'AdminDepartmentEdit',
    component: () => import('../views/admin/AdminDepartmentForm.vue'),
    props: true,
    meta: { title: 'Editar Departamento', requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/pages',
    name: 'AdminPages',
    component: () => import('../views/admin/AdminPages.vue'),
    meta: { title: 'Páginas', requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/pages/new',
    name: 'AdminPageNew',
    component: () => import('../views/admin/AdminPageForm.vue'),
    meta: { title: 'Nueva Página', requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/pages/:slug/edit',
    name: 'AdminPageEdit',
    component: () => import('../views/admin/AdminPageForm.vue'),
    props: true,
    meta: { title: 'Editar Página', requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/settings',
    name: 'AdminSettings',
    component: () => import('../views/admin/AdminSettings.vue'),
    meta: { title: 'Configuración', requiresAuth: true, requiresAdmin: true }
  },
  // Catch all - redirect to home
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authenticated = isAuthenticated()
  const admin = isAdmin()

  // Ruta pública
  if (to.meta.public) {
    // Si ya está autenticado y va a login, redirigir a home
    if (to.name === 'Login' && authenticated) {
      return next('/')
    }
    return next()
  }

  // Requiere autenticación
  if (to.meta.requiresAuth && !authenticated) {
    return next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  }

  // Requiere admin
  if (to.meta.requiresAdmin && !admin) {
    return next('/')
  }

  next()
})

export default router
