import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import ProductManagement from '../views/ProductManagement.vue'
import StockManagement from '../views/StockManagement.vue'
import Orders from '../views/Orders.vue'
import Reports from '../views/Reports.vue'
import Login from '../views/Login.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { requiresAuth: false }
    },
    {
      path: '/',
      name: 'dashboard',
      component: Dashboard,
      meta: { requiresAuth: true }
    },
    {
      path: '/products',
      name: 'products',
      component: ProductManagement,
      meta: { requiresAuth: true }
    },
    {
      path: '/stock',
      name: 'stock',
      component: StockManagement,
      meta: { requiresAuth: true }
    },
    {
      path: '/orders',
      name: 'orders',
      component: Orders,
      meta: { requiresAuth: true }
    },
    {
      path: '/reports',
      name: 'reports',
      component: Reports,
      meta: { requiresAuth: true }
    }
  ]
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    // If route requires auth and user is not authenticated, redirect to login
    next({ name: 'login' })
  } else if (to.name === 'login' && isAuthenticated) {
    // If already logged in and trying to access login page, redirect to dashboard
    next({ name: 'dashboard' })
  } else {
    // Otherwise, proceed as normal
    next()
  }
})

export default router
