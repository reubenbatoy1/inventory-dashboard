import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import ProductManagement from '../views/ProductManagement.vue'
import StockManagement from '../views/StockManagement.vue'
import Orders from '../views/Orders.vue'
import Reports from '../views/Reports.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: Dashboard
    },
    {
      path: '/products',
      name: 'products',
      component: ProductManagement
    },
    {
      path: '/stock',
      name: 'stock',
      component: StockManagement
    },
    {
      path: '/orders',
      name: 'orders',
      component: Orders
    },
    {
      path: '/reports',
      name: 'reports',
      component: Reports
    }
  ]
})

export default router
