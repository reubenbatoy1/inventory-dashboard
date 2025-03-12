<template>
  <div class="dashboard">
    <div class="grid-4">
      <!-- Overview Cards -->
      <div class="card">
        <h3>Total Sales</h3>
        <div class="stat">{{ metrics.sales.value }}</div>
        <div :class="['trend', metrics.sales.trend >= 0 ? 'positive' : 'negative']">
          {{ metrics.sales.trend >= 0 ? '+' : '' }}{{ metrics.sales.trend }}%
        </div>
        <div class="category-breakdown">
          <div v-for="(category, index) in metrics.sales.byCategory" :key="index">
            <span>{{ category.category }}</span>
            <span>{{ category.value }} ({{ category.trend >= 0 ? '+' : '' }}{{ category.trend }}%)</span>
          </div>
        </div>
      </div>
      <div class="card">
        <h3>Revenue</h3>
        <div class="stat">₱{{ metrics.revenue.value.toLocaleString() }}</div>
        <div :class="['trend', metrics.revenue.trend >= 0 ? 'positive' : 'negative']">
          {{ metrics.revenue.trend >= 0 ? '+' : '' }}{{ metrics.revenue.trend }}%
        </div>
        <div class="category-breakdown">
          <div v-for="(category, index) in metrics.revenue.byCategory" :key="index">
            <span>{{ category.category }}</span>
            <span>₱{{ category.value.toLocaleString() }} ({{ category.trend >= 0 ? '+' : '' }}{{ category.trend }}%)</span>
          </div>
        </div>
      </div>
      <div class="card">
        <h3>Profit</h3>
        <div class="stat">₱{{ metrics.profit.value.toLocaleString() }}</div>
        <div :class="['trend', metrics.profit.trend >= 0 ? 'positive' : 'negative']">
          {{ metrics.profit.trend >= 0 ? '+' : '' }}{{ metrics.profit.trend }}%
        </div>
        <div class="category-breakdown">
          <div v-for="(category, index) in metrics.profit.byCategory" :key="index">
            <span>{{ category.category }}</span>
            <span>₱{{ category.value.toLocaleString() }} ({{ category.trend >= 0 ? '+' : '' }}{{ category.trend }}%)</span>
          </div>
        </div>
      </div>
      <div class="card">
        <h3>Cost</h3>
        <div class="stat">₱{{ metrics.cost.value.toLocaleString() }}</div>
        <div :class="['trend', metrics.cost.trend >= 0 ? 'positive' : 'negative']">
          {{ metrics.cost.trend >= 0 ? '+' : '' }}{{ metrics.cost.trend }}%
        </div>
        <div class="category-breakdown">
          <div v-for="(category, index) in metrics.cost.byCategory" :key="index">
            <span>{{ category.category }}</span>
            <span>₱{{ category.value.toLocaleString() }} ({{ category.trend >= 0 ? '+' : '' }}{{ category.trend }}%)</span>
          </div>
        </div>
      </div>
    </div>

    <div class="grid-2 mt-4">
      <!-- Inventory Summary -->
      <div class="card">
        <h3>Inventory Summary</h3>
        <div class="inventory-stats">
          <div class="stat-item">
            <span class="label">Currently in Stock</span>
            <span class="value">{{ inventorySummary.inStock }} items</span>
          </div>
          <div class="stat-item">
            <span class="label">Low Stock Items</span>
            <span class="value">{{ inventorySummary.lowStock }} items</span>
          </div>
          <div class="stat-item">
            <span class="label">To be Received</span>
            <span class="value">{{ inventorySummary.toBeReceived }} items</span>
          </div>
          <div class="stat-item">
            <span class="label">Category Breakdown</span>
            <ul>
              <li v-for="(count, category) in inventorySummary.categoryBreakdown" :key="category">
                {{ category }}: {{ count.total }} items ({{ count.lowStock }} low stock)
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Purchase Overview -->
      <div class="card">
        <h3>Purchase Overview</h3>
        <div class="purchase-stats">
          <div class="stat-item">
            <span class="label">Purchase Orders</span>
            <span class="value">{{ purchaseOverview.totalOrders }}</span>
          </div>
          <div class="stat-item">
            <span class="label">Total Cost</span>
            <span class="value">₱{{ purchaseOverview.totalCost.toLocaleString() }}</span>
          </div>
          <div class="stat-item">
            <span class="label">Pending Delivery</span>
            <span class="value">{{ purchaseOverview.pendingDelivery }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Trends -->
    <div class="card mt-4" style="height: 220px;">
      <h3 class="chart-title">Weekly Sales by Category</h3>
      <div class="chart-container">
        <Line :data="chartData" :options="chartOptions" />
      </div>
    </div>

    <div class="grid-2 mt-4">
      <!-- Top Selling Products -->
      <div class="card">
        <h3>Top Selling Products</h3>
        <table class="table">
          <thead>
            <tr>
              <th>Product</th>
              <th>Category</th>
              <th>Sold</th>
              <th>Revenue</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in topProducts" :key="product.name">
              <td>{{ product.name }}</td>
              <td><span :class="['category-tag', product.category]">{{ product.category }}</span></td>
              <td>{{ product.sold }}</td>
              <td>₱{{ product.revenue }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Low Stock Alert -->
      <div class="card">
        <h3>Low Stock Items</h3>
        <table class="table">
          <thead>
            <tr>
              <th>Product</th>
              <th>Category</th>
              <th>Stock</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in lowStockItems" :key="item.id">
              <td>{{ item.name }}</td>
              <td><span :class="['category-tag', item.category]">{{ item.category }}</span></td>
              <td>{{ item.stock }}</td>
              <td>
                <span :class="['stock-badge', getStockClass(item.stock, item.reorderLevel)]">
                  {{ item.stock === 0 ? 'Out of Stock' : 'Low Stock' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js'
import { useInventoryStore } from '../stores/inventory'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

// Initialize store
const store = useInventoryStore()
const { products, orders, purchaseOrders } = store

// Calculate metrics for overview cards
const metrics = computed(() => {
  const today = new Date()
  const thirtyDaysAgo = new Date(today.getTime() - (30 * 24 * 60 * 60 * 1000))
  
  // Initialize category metrics
  const categoryMetrics = {
    Uniform: { sales: 0, revenue: 0, cost: 0 },
    Books: { sales: 0, revenue: 0, cost: 0 },
    Other: { sales: 0, revenue: 0, cost: 0 }
  }

  // Calculate current month metrics by category
  const currentMonthOrders = orders.value.filter(order => new Date(order.date) >= thirtyDaysAgo)
  currentMonthOrders.forEach(order => {
    order.items.forEach(item => {
      const product = products.value.find(p => p.id === item.id)
      if (product) {
        categoryMetrics[product.category].sales += item.quantity
        categoryMetrics[product.category].revenue += item.price * item.quantity
        categoryMetrics[product.category].cost += item.cost * item.quantity
      }
    })
  })

  // Calculate total metrics
  const currentMetrics = {
    sales: Object.values(categoryMetrics).reduce((total, cat) => total + cat.sales, 0),
    revenue: Object.values(categoryMetrics).reduce((total, cat) => total + cat.revenue, 0),
    cost: Object.values(categoryMetrics).reduce((total, cat) => total + cat.cost, 0)
  }
  currentMetrics.profit = currentMetrics.revenue - currentMetrics.cost

  // Calculate previous month metrics
  const sixtyDaysAgo = new Date(today.getTime() - (60 * 24 * 60 * 60 * 1000))
  const previousMonthOrders = orders.value.filter(order => {
    const orderDate = new Date(order.date)
    return orderDate >= sixtyDaysAgo && orderDate < thirtyDaysAgo
  })

  // Initialize previous category metrics
  const previousCategoryMetrics = {
    Uniform: { sales: 0, revenue: 0, cost: 0 },
    Books: { sales: 0, revenue: 0, cost: 0 },
    Other: { sales: 0, revenue: 0, cost: 0 }
  }

  // Calculate previous month metrics by category
  previousMonthOrders.forEach(order => {
    order.items.forEach(item => {
      const product = products.value.find(p => p.id === item.id)
      if (product) {
        previousCategoryMetrics[product.category].sales += item.quantity
        previousCategoryMetrics[product.category].revenue += item.price * item.quantity
        previousCategoryMetrics[product.category].cost += item.cost * item.quantity
      }
    })
  })

  const previousMetrics = {
    sales: Object.values(previousCategoryMetrics).reduce((total, cat) => total + cat.sales, 0),
    revenue: Object.values(previousCategoryMetrics).reduce((total, cat) => total + cat.revenue, 0),
    cost: Object.values(previousCategoryMetrics).reduce((total, cat) => total + cat.cost, 0)
  }
  previousMetrics.profit = previousMetrics.revenue - previousMetrics.cost

  return {
    sales: {
      value: currentMetrics.sales,
      trend: calculateTrend(currentMetrics.sales, previousMetrics.sales),
      byCategory: Object.entries(categoryMetrics).map(([category, metrics]) => ({
        category,
        value: metrics.sales,
        trend: calculateTrend(metrics.sales, previousCategoryMetrics[category].sales)
      }))
    },
    revenue: {
      value: currentMetrics.revenue,
      trend: calculateTrend(currentMetrics.revenue, previousMetrics.revenue),
      byCategory: Object.entries(categoryMetrics).map(([category, metrics]) => ({
        category,
        value: metrics.revenue,
        trend: calculateTrend(metrics.revenue, previousCategoryMetrics[category].revenue)
      }))
    },
    profit: {
      value: currentMetrics.profit,
      trend: calculateTrend(currentMetrics.profit, previousMetrics.profit),
      byCategory: Object.entries(categoryMetrics).map(([category, metrics]) => ({
        category,
        value: metrics.revenue - metrics.cost,
        trend: calculateTrend(
          metrics.revenue - metrics.cost,
          previousCategoryMetrics[category].revenue - previousCategoryMetrics[category].cost
        )
      }))
    },
    cost: {
      value: currentMetrics.cost,
      trend: calculateTrend(currentMetrics.cost, previousMetrics.cost),
      byCategory: Object.entries(categoryMetrics).map(([category, metrics]) => ({
        category,
        value: metrics.cost,
        trend: calculateTrend(metrics.cost, previousCategoryMetrics[category].cost)
      }))
    }
  }
})

// Calculate inventory summary
const inventorySummary = computed(() => {
  const categoryCounts = {
    Uniform: {
      total: products.value.filter(p => p.category === 'Uniform').reduce((total, p) => total + p.stock, 0),
      lowStock: products.value.filter(p => p.category === 'Uniform' && p.stock > 0 && p.stock < 10).length
    },
    Books: {
      total: products.value.filter(p => p.category === 'Books').reduce((total, p) => total + p.stock, 0),
      lowStock: products.value.filter(p => p.category === 'Books' && p.stock > 0 && p.stock < 5).length
    },
    Other: {
      total: products.value.filter(p => p.category === 'Other').reduce((total, p) => total + p.stock, 0),
      lowStock: products.value.filter(p => p.category === 'Other' && p.stock > 0 && p.stock < 50).length
    }
  }

  return {
    inStock: Object.values(categoryCounts).reduce((total, cat) => total + cat.total, 0),
    lowStock: Object.values(categoryCounts).reduce((total, cat) => total + cat.lowStock, 0),
    toBeReceived: purchaseOrders.value.reduce((total, po) => 
      total + po.items.reduce((sum, item) => sum + (po.status === 'pending' ? item.quantity : 0), 0), 0),
    categoryBreakdown: categoryCounts
  }
})

// Calculate purchase overview
const purchaseOverview = computed(() => {
  return {
    totalOrders: purchaseOrders.value.length,
    totalCost: purchaseOrders.value.reduce((total, po) => 
      total + po.items.reduce((sum, item) => sum + (item.cost * item.quantity), 0), 0),
    pendingDelivery: purchaseOrders.value.filter(po => po.status === 'pending').length
  }
})

// Calculate top selling products by category
const topProducts = computed(() => {
  const productSales = {}
  orders.value.forEach(order => {
    order.items.forEach(item => {
      if (!productSales[item.name]) {
        const product = products.value.find(p => p.id === item.id)
        productSales[item.name] = { 
          sold: 0, 
          revenue: 0,
          category: product ? product.category : 'Unknown'
        }
      }
      productSales[item.name].sold += item.quantity
      productSales[item.name].revenue += item.price * item.quantity
    })
  })
  
  return Object.entries(productSales)
    .map(([name, data]) => ({ 
      name, 
      category: data.category,
      sold: data.sold,
      revenue: data.revenue.toLocaleString()
    }))
    .sort((a, b) => parseInt(b.revenue.replace(/,/g, '')) - parseInt(a.revenue.replace(/,/g, '')))
    .slice(0, 5)
})

// Calculate low stock items with category-specific thresholds
const lowStockItems = computed(() => {
  const thresholds = {
    'Uniform': 10,
    'Books': 5,
    'Other': 50
  }

  return products.value
    .filter(product => product.stock < thresholds[product.category])
    .map(product => ({
      id: product.id,
      name: product.name,
      category: product.category,
      stock: product.stock,
      reorderLevel: thresholds[product.category]
    }))
    .sort((a, b) => {
      // Sort by severity (how far below threshold)
      const aPercentage = (a.stock / a.reorderLevel) * 100
      const bPercentage = (b.stock / b.reorderLevel) * 100
      return aPercentage - bPercentage
    })
    .slice(0, 5)
})

function calculateTrend(current, previous) {
  if (previous === 0) return current > 0 ? 100 : 0
  return Math.round(((current - previous) / previous) * 100)
}

function isLowStock(name) {
  const product = products.value.find(p => p.name === name)
  return product && product.stock < 10
}

function getStockClass(stock, reorderLevel) {
  return stock === 0 ? 'out-of-stock' : stock < reorderLevel ? 'low-stock' : 'in-stock'
}

// Chart data with real-time updates and category breakdown
const chartData = computed(() => {
  const labels = ['M', 'T', 'W', 'T', 'F', 'S', 'S']
  
  // Initialize category data arrays
  const categoryData = {
    Uniform: Array(7).fill(0),
    Books: Array(7).fill(0),
    Other: Array(7).fill(0)
  }

  // Calculate daily sales by category for the past week
  const today = new Date()
  const dailyData = Array(7).fill(null).map((_, index) => {
    const date = new Date(today)
    date.setDate(date.getDate() - (6 - index))
    
    const dayOrders = orders.value.filter(order => {
      const orderDate = new Date(order.date)
      return orderDate.toDateString() === date.toDateString()
    })

    // Calculate sales and revenue by category
    const dayCategoryData = {
      Uniform: { sales: 0, revenue: 0 },
      Books: { sales: 0, revenue: 0 },
      Other: { sales: 0, revenue: 0 }
    }

    dayOrders.forEach(order => {
      order.items.forEach(item => {
        const product = products.value.find(p => p.id === item.id)
        if (product) {
          dayCategoryData[product.category].sales += item.quantity
          dayCategoryData[product.category].revenue += item.price * item.quantity
          categoryData[product.category][index] = dayCategoryData[product.category].sales
        }
      })
    })

    return {
      sales: Object.values(dayCategoryData).reduce((total, cat) => total + cat.sales, 0),
      revenue: Object.values(dayCategoryData).reduce((total, cat) => total + cat.revenue, 0)
    }
  })

  return {
    labels,
    datasets: [
      {
        label: 'Uniform Sales',
        data: categoryData.Uniform,
        borderColor: '#4CAF50',
        backgroundColor: 'rgba(76, 175, 80, 0.1)',
        tension: 0.2,
        fill: true
      },
      {
        label: 'Book Sales',
        data: categoryData.Books,
        borderColor: '#2196F3',
        backgroundColor: 'rgba(33, 150, 243, 0.1)',
        tension: 0.2,
        fill: true
      },
      {
        label: 'Other Sales',
        data: categoryData.Other,
        borderColor: '#9C27B0',
        backgroundColor: 'rgba(156, 39, 176, 0.1)',
        tension: 0.2,
        fill: true
      }
    ]
  }
})

// Chart options following UI preferences
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      grid: {
        display: false
      },
      ticks: {
        font: {
          size: 11
        },
        color: '#666'
      }
    },
    x: {
      grid: {
        display: false
      },
      ticks: {
        font: {
          size: 11
        },
        color: '#666'
      }
    }
  },
  plugins: {
    legend: {
      position: 'top',
      align: 'end',
      labels: {
        boxWidth: 8,
        usePointStyle: true,
        pointStyle: 'circle',
        padding: 15,
        font: {
          size: 11
        },
        color: '#666'
      }
    },
    tooltip: {
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      titleColor: '#666',
      bodyColor: '#666',
      borderColor: '#ddd',
      borderWidth: 1,
      padding: 8,
      bodyFont: {
        size: 11
      },
      titleFont: {
        size: 11
      },
      displayColors: false,
      callbacks: {
        label: function(context) {
          const label = context.dataset.label || ''
          const value = context.parsed.y || 0
          return `${label}: ${value} units`
        }
      }
    }
  }
}

// Watch for changes in products and update metrics
watch([products, orders, purchaseOrders], () => {
  // The computed properties will automatically update
}, { deep: true })
</script>

<style scoped>
.dashboard {
  padding: 0.75rem;
}

.grid-4 {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.75rem;
}

.grid-2 {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

.card {
  background: #fff;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0.5rem 0;
}

.trend {
  font-size: 0.875rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  display: inline-block;
}

.trend.positive {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.trend.negative {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

.category-breakdown {
  margin-top: 0.75rem;
  font-size: 0.875rem;
  color: #666;
}

.category-breakdown div {
  padding: 0.25rem 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-title {
  margin-bottom: 0.75rem;
  color: #666;
  font-size: 0.875rem;
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

.table td {
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.stock-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  display: inline-block;
}

.out-of-stock {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

.low-stock {
  background: rgba(255, 152, 0, 0.1);
  color: #ff9800;
}

.in-stock {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.category-tag {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  display: inline-block;
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

.inventory-stats,
.purchase-stats {
  display: grid;
  gap: 0.75rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.stat-item:last-child {
  border-bottom: none;
}

.stat-item .label {
  color: #666;
  font-size: 0.875rem;
}

.stat-item .value {
  font-weight: 500;
  font-size: 0.875rem;
}

.mt-4 {
  margin-top: 0.75rem;
}

@media (max-width: 1024px) {
  .grid-4 {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .grid-2,
  .grid-4 {
    grid-template-columns: 1fr;
  }

  .chart-container {
    height: 160px;
  }

  .stat {
    font-size: 1.25rem;
  }
}
</style>
