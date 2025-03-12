import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'

// Import Chart.js components
import { Chart as ChartJS, registerables } from 'chart.js'
ChartJS.register(...registerables)

// Create app instance
const app = createApp(App)

// Use router
app.use(router)

// Mount app
app.mount('#app')
