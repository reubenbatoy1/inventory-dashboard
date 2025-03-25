import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css'
import './plugins/axios' // Import axios configuration

// Import Chart.js components
import { Chart as ChartJS, registerables } from 'chart.js'
ChartJS.register(...registerables)

// Create Pinia instance
const pinia = createPinia()

// Create app instance
const app = createApp(App)

// Use plugins
app.use(pinia)
app.use(router)

// Mount app
app.mount('#app')
