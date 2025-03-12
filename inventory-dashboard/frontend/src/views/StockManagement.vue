<template>
  <div class="stock-container">
    <div class="header">
      <h2>Stock Management</h2>
      <button class="btn btn-primary" @click="showAdjustmentModal = true">
        + Stock Adjustment
      </button>
    </div>

    <div class="filters">
      <div class="search-box">
        <input 
          type="text" 
          v-model="filters.search" 
          placeholder="Search products..." 
          class="form-control"
        />
      </div>
      <div class="category-filter">
        <select v-model="filters.category" class="form-control">
          <option value="">All Categories</option>
          <option value="Uniform">Uniform</option>
          <option value="Books">Books</option>
          <option value="Other">Other</option>
        </select>
      </div>
    </div>

    <div class="table-container">
      <table class="stock-table">
        <thead>
          <tr>
            <th>Product</th>
            <th>Category</th>
            <th>Current Stock</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in filteredProducts" :key="product.id">
            <td>{{ product.name }}</td>
            <td>
              <span :class="['category-tag', product.category]">
                {{ product.category }}
              </span>
            </td>
            <td>{{ product.stock }}</td>
            <td>
              <span :class="['status', product.statusClass]">
                {{ product.status }}
              </span>
            </td>
            <td class="actions-column">
              <button class="action-btn view" @click="openStockHistory(product)">
                <span class="icon">📋</span>
                <span class="text">History</span>
              </button>
              <button class="action-btn edit" @click="openStockAdjustment(product)">
                <span class="icon">📦</span>
                <span class="text">Adjust</span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- Stock Adjustment Modal -->
  <div class="modal" v-if="showAdjustmentModal">
    <div class="modal-content modal-sm">
      <div class="modal-header">
        <h3>Stock Adjustment</h3>
        <button class="close-btn" @click="closeModal">&times;</button>
      </div>
      <form @submit.prevent="saveStockAdjustment" class="compact-form">
        <div class="form-grid">
          <div class="form-row">
            <div class="form-group">
              <label>Product</label>
              <select v-model="adjustmentForm.productId" required class="form-control">
                <option value="" disabled selected>Select product</option>
                <option v-for="product in products" :key="product.id" :value="product.id">
                  {{ product.name }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>Type</label>
              <select v-model="adjustmentForm.type" required class="form-control">
                <option value="" disabled selected>Select type</option>
                <option value="add">Add Stock</option>
                <option value="remove">Remove Stock</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Quantity</label>
              <input 
                type="number" 
                v-model="adjustmentForm.quantity" 
                required 
                class="form-control" 
                min="1"
                placeholder="Enter quantity"
              />
            </div>
            <div class="form-group">
              <label>Reason</label>
              <select v-model="adjustmentForm.reason" required class="form-control">
                <option value="" disabled selected>Select reason</option>
                <option value="purchase">New Purchase</option>
                <option value="sale">Sale</option>
                <option value="return">Return</option>
                <option value="damage">Damage/Loss</option>
                <option value="correction">Stock Correction</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label>Notes</label>
            <input
              type="text"
              v-model="adjustmentForm.notes"
              class="form-control"
              placeholder="Additional notes (optional)"
            />
          </div>
          <div v-if="selectedProduct" class="stock-info">
            <div class="info-row">
              <span>Current Stock:</span>
              <span :class="getStockLevelClass(selectedProduct)">
                {{ selectedProduct.stockLevel }} units
              </span>
            </div>
            <div class="info-row">
              <span>Low Stock Alert:</span>
              <span>{{ getThreshold(selectedProduct.category) }} units</span>
            </div>
          </div>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-secondary btn-sm" @click="closeModal">Cancel</button>
          <button type="submit" class="btn btn-primary btn-sm">Save</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Stock History Modal -->
  <div class="modal" v-if="selectedProduct">
    <div class="modal-content modal-lg">
      <div class="modal-header">
        <h3>Stock History - {{ selectedProduct.name }}</h3>
        <button class="close-btn" @click="selectedProduct = null">&times;</button>
      </div>
      <div class="history-details">
        <div class="info-grid">
          <div class="info-group">
            <label>Current Stock</label>
            <div class="info-value">{{ selectedProduct.stock }}</div>
          </div>
          <div class="info-group">
            <label>Category</label>
            <div class="info-value">
              <span :class="['category-tag', selectedProduct.category]">
                {{ selectedProduct.category }}
              </span>
            </div>
          </div>
          <div class="info-group">
            <label>Status</label>
            <div class="info-value">
              <span :class="['status', selectedProduct.statusClass]">
                {{ selectedProduct.status }}
              </span>
            </div>
          </div>
        </div>
        
        <div class="history-section">
          <h4>Stock Movements</h4>
          <table class="history-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Type</th>
                <th>Quantity</th>
                <th>Notes</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="movement in selectedProduct.history" :key="movement.id">
                <td>{{ formatDate(movement.date) }}</td>
                <td>
                  <span :class="['movement-type', movement.type]">
                    {{ formatType(movement.type) }}
                  </span>
                </td>
                <td :class="getQuantityClass(movement.type)">
                  {{ getQuantityPrefix(movement.type) }}{{ movement.quantity }}
                </td>
                <td>{{ movement.notes }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useInventoryStore } from '../stores/inventory'

const store = useInventoryStore()
const { products } = store

const showAdjustmentModal = ref(false)
const selectedProduct = ref(null)

const filters = ref({
  search: '',
  category: ''
})

const adjustmentForm = ref({
  productId: '',
  type: '',
  quantity: 1,
  reason: '',
  notes: ''
})

// Group products by category
const groupedProducts = computed(() => {
  const groups = {
    Uniform: products.value.filter(p => p.category === 'Uniform'),
    Books: products.value.filter(p => p.category === 'Books'),
    Other: products.value.filter(p => p.category === 'Other')
  }
  return groups
})

const filteredProducts = computed(() => {
  return products.value.filter(product => {
    const matchesSearch = !filters.value.search || 
      product.name.toLowerCase().includes(filters.value.search.toLowerCase())
    const matchesCategory = !filters.value.category || product.category === filters.value.category
    return matchesSearch && matchesCategory
  })
})

function openStockHistory(product) {
  selectedProduct.value = product
}

function openStockAdjustment(product) {
  adjustmentForm.value.productId = product.id
  showAdjustmentModal.value = true
}

function saveStockAdjustment() {
  const adjustment = {
    id: Date.now(),
    date: new Date().toISOString(),
    type: adjustmentForm.value.type,
    quantity: adjustmentForm.value.quantity,
    reason: adjustmentForm.value.reason,
    notes: adjustmentForm.value.notes
  }

  // Add to product history
  if (!selectedProduct.value.history) {
    selectedProduct.value.history = []
  }
  selectedProduct.value.history.unshift(adjustment)

  // Update stock quantity
  const product = selectedProduct.value
  if (adjustmentForm.value.type === 'add') {
    product.stock += adjustmentForm.value.quantity
  } else {
    product.stock = Math.max(0, product.stock - adjustmentForm.value.quantity)
  }

  // Update product status
  updateProductStatus(product)
  
  // Update store
  store.updateProduct(product)
  closeModal()
}

function updateProductStatus(product) {
  const threshold = product.category === 'Uniform' ? 10 : 
                   product.category === 'Books' ? 5 : 50

  if (product.stock === 0) {
    product.status = 'Out of Stock'
    product.statusClass = 'out-of-stock'
  } else if (product.stock <= threshold) {
    product.status = 'Low Stock'
    product.statusClass = 'low-stock'
  } else {
    product.status = 'In Stock'
    product.statusClass = 'in-stock'
  }
}

function closeModal() {
  showAdjustmentModal.value = false
  adjustmentForm.value = {
    productId: '',
    type: '',
    quantity: 1,
    reason: '',
    notes: ''
  }
}

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function formatType(type) {
  return type.split('_').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ')
}

function getQuantityClass(type) {
  return type === 'stock_in' ? 'positive' : 'negative'
}

function getQuantityPrefix(type) {
  return type === 'stock_in' ? '+' : '-'
}

function getStockLevelClass(product) {
  const threshold = product.category === 'Uniform' ? 10 : 
                   product.category === 'Books' ? 5 : 50

  if (product.stockLevel <= threshold) {
    return 'stock-warning'
  } else {
    return 'stock-normal'
  }
}

function getThreshold(category) {
  return category === 'Uniform' ? 10 : 
         category === 'Books' ? 5 : 50
}
</script>

<style scoped>
.stock-container {
  padding: 1rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.filters {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.stock-table {
  width: 100%;
  border-collapse: collapse;
}

.stock-table th,
.stock-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #eee;
  font-size: 0.875rem;
}

.stock-table th {
  background: #f9fafb;
  font-weight: 500;
  color: #666;
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

.status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
}

.status.in-stock {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.status.low-stock {
  background: rgba(255, 152, 0, 0.1);
  color: #ff9800;
}

.status.out-of-stock {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

.actions-column {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  border: none;
  border-radius: 4px;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn.view {
  background: rgba(33, 150, 243, 0.1);
  color: #2196F3;
}

.action-btn.edit {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.action-btn:hover {
  filter: brightness(0.95);
}

.modal-sm {
  width: 90%;
  max-width: 400px;
}

.modal-content {
  transform: translateY(0);
  transition: transform 0.2s;
  max-height: none;
  overflow: visible;
}

.compact-form {
  padding: 1rem;
}

.form-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  margin-bottom: 0;
}

.form-group label {
  font-size: 0.75rem;
  color: #666;
  margin-bottom: 0.25rem;
  display: block;
}

.form-control {
  font-size: 0.75rem;
  padding: 0.375rem 0.5rem;
  height: 32px;
}

.stock-info {
  background: #f8f9fa;
  border-radius: 4px;
  padding: 0.75rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #666;
}

.info-row:not(:last-child) {
  margin-bottom: 0.5rem;
}

.stock-level {
  font-weight: 500;
}

.stock-normal {
  color: #4CAF50;
}

.stock-warning {
  color: #FFC107;
}

.stock-critical {
  color: #f44336;
}

.modal-actions {
  margin-top: 1rem;
  padding-top: 0.75rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

.btn-sm {
  font-size: 0.75rem;
  padding: 0.375rem 0.75rem;
  height: 32px;
}

.history-details {
  padding: 1rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.info-group label {
  font-size: 0.75rem;
  color: #666;
  margin-bottom: 0.25rem;
  display: block;
}

.info-value {
  font-size: 0.875rem;
  font-weight: 500;
}

.history-section {
  margin-top: 1.5rem;
}

.history-section h4 {
  margin-bottom: 1rem;
  color: #333;
  font-size: 1rem;
}

.history-table {
  width: 100%;
  border-collapse: collapse;
}

.history-table th,
.history-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #eee;
  font-size: 0.875rem;
}

.movement-type {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  text-transform: capitalize;
}

.movement-type.stock_in {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.movement-type.stock_out,
.movement-type.damaged,
.movement-type.expired,
.movement-type.lost,
.movement-type.phase_out {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

.positive {
  color: #4CAF50;
}

.negative {
  color: #f44336;
}

.form-control {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.875rem;
}

.form-control:focus {
  border-color: #2196F3;
  outline: none;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.1);
}

textarea.form-control {
  resize: vertical;
  min-height: 80px;
}
</style>
