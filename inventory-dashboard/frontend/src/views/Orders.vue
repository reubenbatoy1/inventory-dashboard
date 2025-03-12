<template>
  <div class="orders-container">
    <div class="header">
      <h2>Order History</h2>
      <button class="btn btn-primary" @click="showAddOrderModal = true">
        + Add Order
      </button>
    </div>

    <div class="filters">
      <div class="search-box">
        <input 
          type="text" 
          v-model="filters.search" 
          placeholder="Search orders..." 
          class="form-control"
        />
      </div>
      <div class="status-filter">
        <select v-model="filters.status" class="form-control">
          <option value="">All Status</option>
          <option value="pending">Pending</option>
          <option value="completed">Completed</option>
          <option value="cancelled">Cancelled</option>
        </select>
      </div>
    </div>

    <div class="table-container">
      <table class="orders-table">
        <thead>
          <tr>
            <th>Order ID</th>
            <th>Customer</th>
            <th>Date</th>
            <th>Total</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in filteredOrders" :key="order.id">
            <td>#{{ order.id }}</td>
            <td>{{ order.customer }}</td>
            <td>{{ formatDate(order.date) }}</td>
            <td>₱{{ order.total }}</td>
            <td>
              <span :class="['status', order.status]">{{ order.status }}</span>
            </td>
            <td class="actions-column">
              <button class="action-btn view" @click="openViewOrder(order)">
                <span class="icon">👁️</span>
                <span class="text">View</span>
              </button>
              <button class="action-btn edit" @click="openUpdateStatus(order)">
                <span class="icon">📝</span>
                <span class="text">Edit</span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- View Order Modal -->
  <div class="modal" v-if="selectedOrder">
    <div class="modal-content modal-lg">
      <div class="modal-header">
        <h3>Order Details #{{ selectedOrder.id }}</h3>
        <button class="close-btn" @click="selectedOrder = null">&times;</button>
      </div>
      <div class="order-details">
        <div class="details-grid">
          <div class="info-group">
            <label>Customer</label>
            <div class="info-value">{{ selectedOrder.customer }}</div>
          </div>
          <div class="info-group">
            <label>Date</label>
            <div class="info-value">{{ formatDate(selectedOrder.date) }}</div>
          </div>
          <div class="info-group">
            <label>Status</label>
            <div class="info-value">
              <span :class="['status', selectedOrder.status]">
                {{ selectedOrder.status }}
              </span>
            </div>
          </div>
        </div>
        
        <div class="items-section">
          <h4>Order Items</h4>
          <table class="items-table">
            <thead>
              <tr>
                <th>Product</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in selectedOrder.items" :key="item.id">
                <td>{{ item.name }}</td>
                <td>{{ item.quantity }}</td>
                <td>₱{{ item.price }}</td>
                <td class="total">₱{{ item.quantity * item.price }}</td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <td colspan="3" class="text-right"><strong>Total Amount</strong></td>
                <td class="total"><strong>₱{{ selectedOrder.total }}</strong></td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>
    </div>
  </div>

  <!-- Add Order Modal -->
  <div class="modal" v-if="showAddOrderModal">
    <div class="modal-content">
      <div class="modal-header">
        <h3>Create New Order</h3>
        <button class="close-btn" @click="closeAddOrderModal">&times;</button>
      </div>
      <form @submit.prevent="saveOrder">
        <div class="form-grid">
          <div class="form-group full-width">
            <label>Customer Name</label>
            <input type="text" v-model="orderForm.customer" required class="form-control" placeholder="Enter customer name" />
          </div>
          <div class="form-group full-width">
            <label>Items</label>
            <div class="items-container">
              <div v-for="(item, index) in orderForm.items" :key="index" class="order-item">
                <div class="item-grid">
                  <select v-model="item.product" class="form-control" required>
                    <option value="" disabled selected>Select product</option>
                    <optgroup label="Uniforms">
                      <option v-for="product in groupedProducts.Uniform" :key="product.id" :value="product">
                        {{ product.name }} - ₱{{ product.price }}
                      </option>
                    </optgroup>
                    <optgroup label="Books">
                      <option v-for="product in groupedProducts.Books" :key="product.id" :value="product">
                        {{ product.name }} - ₱{{ product.price }}
                      </option>
                    </optgroup>
                    <optgroup label="Other">
                      <option v-for="product in groupedProducts.Other" :key="product.id" :value="product">
                        {{ product.name }} - ₱{{ product.price }}
                      </option>
                    </optgroup>
                  </select>
                  <div class="quantity-input">
                    <input type="number" v-model="item.quantity" min="1" class="form-control" required placeholder="Qty" />
                    <button type="button" class="remove-btn" @click="removeItem(index)" v-if="orderForm.items.length > 1">&times;</button>
                  </div>
                </div>
                <div class="item-total" v-if="item.product">
                  <span class="category-tag" :class="[item.product.category]">{{ item.product.category }}</span>
                  Total: ₱{{ (item.quantity * item.product.price).toLocaleString() }}
                </div>
              </div>
            </div>
            <button type="button" class="btn-outline" @click="addItem">
              + Add Item
            </button>
          </div>
          <div class="form-group full-width">
            <div class="order-summary">
              <div class="summary-row">
                <span>Total Items:</span>
                <span>{{ orderForm.items.length }}</span>
              </div>
              <div class="summary-row">
                <span>Total Amount:</span>
                <span class="total-amount">₱{{ calculateTotal().toLocaleString() }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-secondary" @click="closeAddOrderModal">Cancel</button>
          <button type="submit" class="btn btn-primary">Create Order</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Update Status Modal -->
  <div class="modal" v-if="showUpdateStatusModal">
    <div class="modal-content">
      <div class="modal-header">
        <h3>Update Order Status #{{ editingOrder.id }}</h3>
        <button class="close-btn" @click="showUpdateStatusModal = false">&times;</button>
      </div>
      <form @submit.prevent="updateOrderStatus">
        <div class="form-grid">
          <div class="form-group full-width">
            <label>Status</label>
            <select v-model="selectedStatus" class="form-control" required>
              <option value="pending">Pending</option>
              <option value="completed">Completed</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-secondary" @click="showUpdateStatusModal = false">Cancel</button>
          <button type="submit" class="btn btn-primary">Update Status</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useInventoryStore } from '../stores/inventory'

const store = useInventoryStore()
const { products, orders } = store

const showAddOrderModal = ref(false)
const showUpdateStatusModal = ref(false)
const selectedOrder = ref(null)
const editingOrder = ref(null)
const selectedStatus = ref('')

const filters = ref({
  search: '',
  status: ''
})

const orderForm = ref({
  customer: '',
  date: new Date().toISOString(),
  items: [{ product: '', quantity: 1 }],
  status: 'pending'
})

const groupedProducts = computed(() => {
  const groups = {
    Uniform: products.value.filter(p => p.category === 'Uniform'),
    Books: products.value.filter(p => p.category === 'Books'),
    Other: products.value.filter(p => p.category === 'Other')
  }
  return groups
})

const filteredOrders = computed(() => {
  return orders.value.filter(order => {
    const matchesSearch = !filters.value.search || 
      order.customer.toLowerCase().includes(filters.value.search.toLowerCase()) ||
      order.id.toString().includes(filters.value.search)
    const matchesStatus = !filters.value.status || order.status === filters.value.status
    return matchesSearch && matchesStatus
  })
})

function openViewOrder(order) {
  selectedOrder.value = order
}

function updateOrderStatus() {
  if (editingOrder.value) {
    editingOrder.value.status = selectedStatus.value
    store.updateOrder(editingOrder.value)
    showUpdateStatusModal.value = false
    editingOrder.value = null
  }
}

function openUpdateStatus(order) {
  editingOrder.value = order
  selectedStatus.value = order.status
  showUpdateStatusModal.value = true
}

function addItem() {
  orderForm.value.items.push({ product: '', quantity: 1 })
}

function removeItem(index) {
  orderForm.value.items.splice(index, 1)
}

function saveOrder() {
  const newOrder = {
    id: orders.value.length + 1,
    customer: orderForm.value.customer,
    date: orderForm.value.date,
    status: orderForm.value.status,
    items: orderForm.value.items.map(item => ({
      id: item.product.id,
      name: item.product.name,
      quantity: item.quantity,
      price: item.product.price,
      cost: item.product.cost,
      category: item.product.category
    })),
    total: calculateTotal()
  }

  store.addOrder(newOrder)
  closeAddOrderModal()
}

function closeAddOrderModal() {
  showAddOrderModal.value = false
  orderForm.value = {
    customer: '',
    date: new Date().toISOString(),
    items: [{ product: '', quantity: 1 }],
    status: 'pending'
  }
}

function calculateTotal() {
  return orderForm.value.items.reduce((total, item) => {
    if (item.product && item.quantity) {
      return total + (item.product.price * item.quantity)
    }
    return total
  }, 0)
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

const getStatusColor = (status) => {
  switch (status) {
    case 'pending':
      return '#ff9800' // Orange for pending
    case 'completed':
      return '#4CAF50' // Green for completed
    case 'cancelled':
      return '#f44336' // Red for cancelled
    default:
      return '#666'
  }
}
</script>

<style scoped>
.orders-container {
  padding: 1rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.header h2 {
  font-size: 1rem;
  font-weight: 500;
  color: #666;
  margin: 0;
}

.filters {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.search-box {
  flex: 1;
}

.search-box .form-control {
  width: 100%;
  padding: 0.35rem 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 11px;
  color: #2c3e50;
}

.status-filter {
  min-width: 100px;
}

.status-filter .form-control {
  padding: 0.35rem 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 11px;
  color: #666;
  background: #fff;
  cursor: pointer;
}

.table-container {
  margin-bottom: 1rem;
}

.orders-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.orders-table th {
  background: #f8f9fa;
  color: #666;
  font-size: 11px;
  font-weight: 500;
  text-align: left;
  padding: 0.75rem;
  border-bottom: 1px solid #e9ecef;
}

.orders-table td {
  padding: 0.75rem;
  border-bottom: 1px solid #e9ecef;
  vertical-align: middle;
  font-size: 0.875rem;
  color: #2c3e50;
}

.status {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  text-transform: capitalize;
}

.status.pending {
  background: rgba(255, 152, 0, 0.1);
  color: #ff9800;
}

.status.completed {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.status.cancelled {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

.actions-column {
  text-align: right;
  min-width: 120px;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 0.35rem 0.5rem;
  margin-left: 0.5rem;
  color: #666;
  font-size: 11px;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn .icon {
  margin-right: 0.25rem;
  font-size: 0.875rem;
}

.action-btn.view:hover {
  background: rgba(33, 150, 243, 0.1);
  border-color: #2196F3;
  color: #2196F3;
}

.action-btn.edit:hover {
  background: rgba(0, 0, 0, 0.05);
  border-color: #666;
  color: #2c3e50;
}

/* Modal Base */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: #fff;
  border-radius: 8px;
  width: 480px;
  max-width: 90vw;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-lg {
  width: 800px;
}

.modal-header {
  padding: 0.75rem;
  border-bottom: 1px solid #e9ecef;
  position: relative;
}

.modal-header h3 {
  margin: 0;
  font-size: 11px;
  font-weight: 500;
  color: #666;
  padding-right: 2rem;
}

.close-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  font-size: 1.25rem;
  color: #666;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.2s;
}

.close-btn:hover {
  background: rgba(0, 0, 0, 0.05);
}

/* Order Details */
.order-details {
  padding: 0.75rem;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.info-group {
  background: #f8f9fa;
  padding: 0.75rem;
  border-radius: 4px;
  border: 1px solid #e9ecef;
}

.info-group label {
  font-size: 11px;
  font-weight: 500;
  color: #666;
  margin-bottom: 0.25rem;
  display: block;
}

.info-value {
  font-size: 0.875rem;
  color: #2c3e50;
  font-weight: 500;
}

.items-section {
  background: #fff;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.items-section h4 {
  margin: 0;
  padding: 0.5rem 0.75rem;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  color: #666;
  font-size: 11px;
  font-weight: 500;
}

.items-table {
  width: 100%;
  border-collapse: collapse;
}

.items-table th {
  background: #fff;
  padding: 0.5rem 0.75rem;
  border-bottom: 1px solid #e9ecef;
  font-weight: 500;
  color: #666;
  font-size: 11px;
  text-align: left;
}

.items-table td {
  padding: 0.5rem 0.75rem;
  border-bottom: 1px solid #e9ecef;
  font-size: 0.875rem;
  color: #2c3e50;
}

.items-table tfoot {
  background: #f8f9fa;
}

.items-table tfoot td {
  padding: 0.5rem 0.75rem;
  color: #2c3e50;
  font-weight: 500;
}

.text-right {
  text-align: right;
}

/* Form Styles */
.form-grid {
  display: grid;
  gap: 0.75rem;
  padding: 0.75rem;
}

.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  display: block;
  font-size: 11px;
  font-weight: 500;
  color: #666;
  margin-bottom: 0.25rem;
}

.form-control {
  width: 100%;
  padding: 0.35rem 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 11px;
  color: #2c3e50;
  background: #fff;
}

.form-control:focus {
  border-color: #2196F3;
  outline: none;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.1);
}

.items-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.order-item {
  background: #f8f9fa;
  border-radius: 4px;
  padding: 0.75rem;
  border: 1px solid #e9ecef;
}

.item-grid {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 0.75rem;
  align-items: start;
}

.quantity-input {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.quantity-input .form-control {
  width: 80px;
}

.remove-btn {
  background: none;
  border: none;
  color: #f44336;
  font-size: 1rem;
  cursor: pointer;
  padding: 0.25rem;
  line-height: 1;
  border-radius: 4px;
  transition: all 0.2s;
}

.remove-btn:hover {
  background: rgba(244, 67, 54, 0.1);
}

.item-total {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: #666;
  display: flex;
  align-items: center;
}

.category-tag {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  margin-right: 0.5rem;
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

.order-summary {
  background: #f8f9fa;
  border-radius: 4px;
  padding: 0.75rem;
  border: 1px solid #e9ecef;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  padding: 0.25rem 0;
  color: #666;
}

.summary-row:last-child {
  margin-top: 0.25rem;
  padding-top: 0.5rem;
  border-top: 1px solid #e9ecef;
  font-weight: 500;
}

.total-amount {
  color: #4CAF50;
  font-weight: 500;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.35rem 0.75rem;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.btn-primary {
  background: #2196F3;
  color: #fff;
}

.btn-primary:hover {
  background: #1976D2;
}

.btn-secondary {
  background: #fff;
  border-color: #ddd;
  color: #666;
}

.btn-secondary:hover {
  background: #f8f9fa;
  border-color: #666;
  color: #2c3e50;
}
</style>
