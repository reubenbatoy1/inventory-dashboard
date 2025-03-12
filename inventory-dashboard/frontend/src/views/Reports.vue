<template>
  <div class="reports">
    <div class="header">
      <h2>Reports & Analytics</h2>
      <div class="date-range">
        <input type="date" v-model="dateRange.start" class="form-control" />
        <span>to</span>
        <input type="date" v-model="dateRange.end" class="form-control" />
        <button class="btn btn-primary" @click="generateReport">
          Generate Report
        </button>
      </div>
    </div>

    <div class="grid-2">
      <!-- Sales Overview -->
      <div class="card">
        <h3>Sales Overview</h3>
        <div class="chart-container">
          <Line :data="salesData" :options="chartOptions" />
        </div>
      </div>

      <!-- Top Products -->
      <div class="card">
        <h3>Top Selling Products</h3>
        <table class="table">
          <thead>
            <tr>
              <th>Product</th>
              <th>Category</th>
              <th>Units</th>
              <th>Revenue</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in topProducts.slice(0, 5)" :key="product.name">
              <td>{{ product.name }}</td>
              <td><span :class="['category-tag', product.category]">{{ product.category }}</span></td>
              <td>{{ product.unitsSold }}</td>
              <td>
                <span :class="['trend', parseFloat(product.profit) > 0 ? 'positive' : 'negative']">
                  ₱{{ product.revenue }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="grid-2 mt-4">
      <!-- Category Performance -->
      <div class="card">
        <h3>Category Performance</h3>
        <div class="category-stats">
          <div v-for="(data, category) in metrics.categories" :key="category" class="stat-card">
            <h4><span :class="['category-tag', category]">{{ category }}</span></h4>
            <div class="metrics">
              <div class="metric">
                <span class="label">Sales</span>
                <span class="value">{{ data.sales }}</span>
              </div>
              <div class="metric">
                <span class="label">Revenue</span>
                <span class="value">₱{{ data.revenue.toLocaleString() }}</span>
              </div>
              <div class="metric">
                <span class="label">Profit</span>
                <span :class="['value', data.revenue - data.cost > 0 ? 'positive' : 'negative']">
                  ₱{{ (data.revenue - data.cost).toLocaleString() }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Category Distribution -->
      <div class="card">
        <h3>Sales Distribution by Category</h3>
        <div class="chart-container">
          <Pie :data="categoryData" :options="chartOptions" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Line, Pie } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, ArcElement, Title, Tooltip, Legend } from 'chart.js'
import { useInventoryStore } from '../stores/inventory'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, ArcElement, Title, Tooltip, Legend)

const store = useInventoryStore()
const { products, orders } = store

// Initialize with current date
const today = new Date('2025-03-11T21:56:30+08:00')
const thirtyDaysAgo = new Date(today.getTime() - (30 * 24 * 60 * 60 * 1000))

const dateRange = ref({
  start: thirtyDaysAgo.toISOString().split('T')[0],
  end: today.toISOString().split('T')[0]
})

// Real-time metrics computation
const metrics = computed(() => {
  const start = new Date(dateRange.value.start)
  const end = new Date(dateRange.value.end)
  
  const filteredOrders = orders.value.filter(order => {
    const orderDate = new Date(order.date)
    return orderDate >= start && orderDate <= end
  })

  const categoryMetrics = {
    Uniform: { sales: 0, revenue: 0, cost: 0 },
    Books: { sales: 0, revenue: 0, cost: 0 },
    Other: { sales: 0, revenue: 0, cost: 0 }
  }

  filteredOrders.forEach(order => {
    order.items.forEach(item => {
      const product = products.value.find(p => p.id === item.id)
      if (product) {
        categoryMetrics[product.category].sales += item.quantity
        categoryMetrics[product.category].revenue += item.price * item.quantity
        categoryMetrics[product.category].cost += item.cost * item.quantity
      }
    })
  })

  return {
    total: {
      sales: Object.values(categoryMetrics).reduce((total, cat) => total + cat.sales, 0),
      revenue: Object.values(categoryMetrics).reduce((total, cat) => total + cat.revenue, 0),
      cost: Object.values(categoryMetrics).reduce((total, cat) => total + cat.cost, 0)
    },
    categories: categoryMetrics
  }
})

// Real-time sales data
const salesData = computed(() => {
  const days = []
  const categorySales = {
    Uniform: [],
    Books: [],
    Other: []
  }

  // Generate last 7 days
  for (let i = 6; i >= 0; i--) {
    const date = new Date(today)
    date.setDate(date.getDate() - i)
    days.push(date.toLocaleDateString('en-US', { weekday: 'short' }).charAt(0))

    const dayOrders = orders.value.filter(order => {
      const orderDate = new Date(order.date)
      return orderDate.toDateString() === date.toDateString()
    })

    // Initialize daily sales
    const daySales = {
      Uniform: 0,
      Books: 0,
      Other: 0
    }

    dayOrders.forEach(order => {
      order.items.forEach(item => {
        const product = products.value.find(p => p.id === item.id)
        if (product) {
          daySales[product.category] += item.quantity
        }
      })
    })

    Object.entries(daySales).forEach(([category, sales]) => {
      categorySales[category].push(sales)
    })
  }

  return {
    labels: days,
    datasets: [
      {
        label: 'Uniform',
        data: categorySales.Uniform,
        borderColor: '#4CAF50',
        backgroundColor: 'rgba(76, 175, 80, 0.1)',
        tension: 0.2,
        fill: true
      },
      {
        label: 'Books',
        data: categorySales.Books,
        borderColor: '#2196F3',
        backgroundColor: 'rgba(33, 150, 243, 0.1)',
        tension: 0.2,
        fill: true
      },
      {
        label: 'Other',
        data: categorySales.Other,
        borderColor: '#9C27B0',
        backgroundColor: 'rgba(156, 39, 176, 0.1)',
        tension: 0.2,
        fill: true
      }
    ]
  }
})

// Real-time category distribution
const categoryData = computed(() => {
  const categoryTotals = {
    Uniform: 0,
    Books: 0,
    Other: 0
  }

  orders.value.forEach(order => {
    order.items.forEach(item => {
      const product = products.value.find(p => p.id === item.id)
      if (product) {
        categoryTotals[product.category] += item.quantity
      }
    })
  })

  return {
    labels: Object.keys(categoryTotals),
    datasets: [{
      data: Object.values(categoryTotals),
      backgroundColor: [
        'rgba(76, 175, 80, 0.7)',  // Uniform - Green
        'rgba(33, 150, 243, 0.7)', // Books - Blue
        'rgba(156, 39, 176, 0.7)'  // Other - Purple
      ]
    }]
  }
})

// Real-time top products
const topProducts = computed(() => {
  const productSales = {}
  
  orders.value.forEach(order => {
    order.items.forEach(item => {
      if (!productSales[item.id]) {
        const product = products.value.find(p => p.id === item.id)
        if (product) {
          productSales[item.id] = {
            name: product.name,
            category: product.category,
            unitsSold: 0,
            revenue: 0,
            profit: 0
          }
        }
      }
      if (productSales[item.id]) {
        productSales[item.id].unitsSold += item.quantity
        productSales[item.id].revenue += item.price * item.quantity
        productSales[item.id].profit += (item.price - item.cost) * item.quantity
      }
    })
  })

  return Object.values(productSales)
    .sort((a, b) => b.revenue - a.revenue)
    .map(product => ({
      ...product,
      revenue: product.revenue.toLocaleString(),
      profit: product.profit.toLocaleString()
    }))
})

// Chart options following UI preferences
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  height: 180,
  plugins: {
    legend: {
      position: 'right',
      align: 'start',
      labels: {
        padding: 8,
        font: { size: 11 },
        boxWidth: 8,
        usePointStyle: true,
        pointStyle: 'circle',
        color: '#666'
      }
    },
    tooltip: {
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      borderColor: '#ddd',
      borderWidth: 1,
      padding: 8,
      titleFont: { size: 11 },
      bodyFont: { size: 11 },
      titleColor: '#666',
      bodyColor: '#666',
      displayColors: false
    }
  },
  scales: {
    x: {
      grid: { display: false },
      ticks: {
        font: { size: 11 },
        color: '#666'
      }
    },
    y: {
      grid: { display: false },
      ticks: {
        font: { size: 11 },
        color: '#666',
        padding: 8
      }
    }
  }
}

// Auto-refresh every minute
let refreshInterval
onMounted(() => {
  refreshInterval = setInterval(() => {
    store.$patch(state => {
      // Refresh store data
    })
  }, 60000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})

function generateReport() {
  // Update date range and metrics will automatically recompute
  const start = new Date(dateRange.value.start)
  const end = new Date(dateRange.value.end)
  
  // Additional report generation logic if needed
}
</script>

<style scoped>
.reports {
  padding: 0.75rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.date-range {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-control {
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.btn {
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}

.btn-primary {
  background: #2196F3;
  color: white;
}

.grid-2 {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.card {
  background: white;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chart-container {
  height: 180px;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  padding: 0.5rem;
  text-align: left;
  font-size: 0.875rem;
  color: #666;
}

.table th {
  font-weight: 500;
}

.category-tag {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
}

.category-tag.Uniform {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.category-tag.Books {
  background: rgba(33, 150, 243, 0.1);
  color: #2196F3;
}

.category-tag.Other {
  background: rgba(156, 39, 176, 0.1);
  color: #9C27B0;
}

.trend {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
}

.trend.positive {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.trend.negative {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

.category-stats {
  display: grid;
  gap: 0.75rem;
}

.stat-card {
  padding: 0.75rem;
  border-radius: 4px;
  background: rgba(0, 0, 0, 0.02);
}

.metrics {
  display: grid;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.metric {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
}

.metric .label {
  color: #666;
}

.metric .value {
  font-weight: 500;
}

.metric .value.positive {
  color: #4CAF50;
}

.metric .value.negative {
  color: #f44336;
}

.mt-4 {
  margin-top: 0.75rem;
}

@media (max-width: 1024px) {
  .grid-2 {
    grid-template-columns: 1fr;
  }
}
</style>
