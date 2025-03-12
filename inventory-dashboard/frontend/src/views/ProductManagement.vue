<template>
<div class="product-management">
  <!-- Header -->
  <div class="header">
    <h2>Product Management</h2>
    <button class="btn btn-primary" @click="showAddProductModal = true">
      + Add Product
    </button>
  </div>

  <!-- Filters -->
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

  <!-- Products Table -->
  <div class="table-container">
    <table class="products-table">
      <thead>
        <tr>
          <th>Product</th>
          <th>Category</th>
          <th>Price</th>
          <th>Stock</th>
          <th>Description</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in filteredProducts" :key="product.id">
          <td>
            <div class="product-info">
              <div class="product-image">
                <img v-if="product.image" :src="product.image" alt="Product" />
                <div v-else class="no-image">No Image</div>
              </div>
              <span class="product-name">{{ product.name }}</span>
            </div>
          </td>
          <td>
            <span :class="['category-tag', product.category]">
              {{ product.category }}
            </span>
          </td>
          <td>₱{{ product.price }}</td>
          <td>
            <span :class="['stock-status', getStockStatus(product)]">
              {{ product.stock }}
              <span v-if="getStockMessage(product)" class="stock-warning">
                {{ getStockMessage(product) }}
              </span>
            </span>
          </td>
          <td class="description-cell">{{ product.description }}</td>
          <td class="actions-column">
            <button class="action-btn view" @click="viewProductDetails(product)">
              <span class="icon">👁️</span>
            </button>
            <button class="action-btn edit" @click="editProduct(product)">
              <span class="icon">✏️</span>
            </button>
            <button class="action-btn delete" @click="confirmDelete(product)">
              <span class="icon">🗑️</span>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- Add/Edit Product Modal -->
  <div class="modal" v-if="showAddProductModal">
    <div class="modal-overlay" @click="closeModal"></div>
    <div class="modal-container">
      <div class="modal-header">
        <h3>{{ editingProduct ? 'Edit Product' : 'Add New Product' }}</h3>
        <button class="close-btn" @click="closeModal">&times;</button>
      </div>
      <form @submit.prevent="saveProduct" class="modal-form">
        <div class="form-grid">
          <div class="form-group full-width">
            <div class="image-upload">
              <input 
                type="file" 
                accept="image/*" 
                @change="handleImageUpload" 
                class="file-input"
                ref="fileInput"
              />
              <div class="image-preview" @click="triggerFileInput">
                <img v-if="imagePreview" :src="imagePreview" alt="Preview" />
                <div v-else class="upload-placeholder">
                  <span class="icon">📷</span>
                  <span class="text">Upload Image</span>
                </div>
              </div>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Name</label>
              <div class="input-group">
                <input 
                  type="text"
                  v-model="productForm.name"
                  required
                  class="form-control"
                  placeholder="Enter product name"
                />
              </div>
            </div>
            <div class="form-group">
              <label>Category</label>
              <select 
                v-model="productForm.category" 
                required 
                class="form-control"
                @change="handleCategoryChange"
              >
                <option value="" disabled selected>Select category</option>
                <option value="Uniform">Uniform</option>
                <option value="Books">Books</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Price (₱)</label>
              <input 
                type="number" 
                v-model="productForm.price" 
                required 
                class="form-control"
                min="0"
                step="0.01"
                placeholder="0.00"
              />
            </div>
            <div class="form-group">
              <label>Initial Stock</label>
              <input 
                type="number" 
                v-model="productForm.stock" 
                required 
                class="form-control"
                min="0"
                step="1"
                placeholder="0"
              />
              <div class="stock-hint" v-if="productForm.category">
                <div class="stock-info">
                  <span class="threshold">
                    {{ productForm.category === 'Other' ? '50 sheets' : 
                       productForm.category === 'Uniform' ? '10 units' : 
                       '5 units' }}
                  </span>
                  <span class="warning" v-if="isLowStock">
                    ⚠️ Low stock warning will show below this threshold
                  </span>
                </div>
              </div>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group full-width">
              <label>Description</label>
              <input 
                type="text"
                v-model="productForm.description" 
                class="form-control" 
                placeholder="Brief description"
              />
            </div>
          </div>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-secondary btn-sm" @click="closeModal">Cancel</button>
          <button type="submit" class="btn btn-primary btn-sm">{{ editingProduct ? 'Save Changes' : 'Add Product' }}</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Product Details Modal -->
  <div class="modal" v-if="selectedProduct">
    <div class="modal-content modal-lg">
      <div class="modal-header">
        <h3>Product Details</h3>
        <button class="close-btn" @click="selectedProduct = null">&times;</button>
      </div>
      <div class="product-details">
        <div class="details-layout">
          <div class="product-image-large">
            <img v-if="selectedProduct.image" :src="selectedProduct.image" alt="Product" />
            <div v-else class="no-image">
              <span class="icon">📷</span>
              <span class="text">No Image Available</span>
            </div>
          </div>
          <div class="details-grid">
            <div class="info-group">
              <label>Name</label>
              <div class="info-value">{{ selectedProduct.name }}</div>
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
              <label>Price</label>
              <div class="info-value price">₱{{ selectedProduct.price }}</div>
            </div>
            <div class="info-group">
              <label>Stock</label>
              <div class="info-value">
                {{ selectedProduct.stock }}
                <span v-if="getStockMessage(selectedProduct)" class="stock-warning">
                  {{ getStockMessage(selectedProduct) }}
                </span>
              </div>
            </div>
            <div class="info-group full-width">
              <label>Description</label>
              <div class="info-value description">
                {{ selectedProduct.description || 'No description available' }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Delete Confirmation Modal -->
  <div class="modal" v-if="showDeleteModal">
    <div class="modal-content">
      <div class="modal-header">
        <h3>Delete Product</h3>
        <button class="close-btn" @click="showDeleteModal = false">&times;</button>
      </div>
      <div class="modal-body">
        <p>Are you sure you want to delete <strong>{{ productToDelete?.name }}</strong>?</p>
        <p class="warning">This action cannot be undone.</p>
      </div>
      <div class="modal-actions">
        <button class="btn btn-secondary" @click="showDeleteModal = false">Cancel</button>
        <button class="btn btn-danger" @click="deleteProduct">Delete</button>
      </div>
    </div>
  </div>
</div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useInventoryStore } from '../stores/inventory'

const store = useInventoryStore()
const { products } = store

// Stock thresholds based on category
const stockThresholds = {
  'Uniform': 10, // Alert when any uniform item falls below 10 pieces
  'Books': 5,    // Alert when any book falls below 5 copies
  'Other': 50    // Alert when Scantron sheets fall below 50 pieces
}

function getStockStatus(product) {
  const threshold = stockThresholds[product.category]
  if (!threshold) return 'normal'
  
  return product.stock < threshold ? 'low' : 'normal'
}

function getStockMessage(product) {
  const threshold = stockThresholds[product.category]
  if (!threshold) return ''
  
  const unit = product.category === 'Other' ? 'sheets' : 'units'
  return product.stock < threshold ? `Low stock: ${product.stock} ${unit} (min: ${threshold})` : ''
}

// State
const showAddProductModal = ref(false)
const selectedProduct = ref(null)
const editingProduct = ref(null)
const showDeleteModal = ref(false)
const productToDelete = ref(null)

const filters = ref({
  search: '',
  category: ''
})

const productForm = ref({
  name: '',
  category: '',
  price: null,
  description: '',
  stock: 0
})

// Image upload state
const imagePreview = ref(null)
const fileInput = ref(null)

const isLowStock = computed(() => {
  if (!productForm.value.category || !productForm.value.stock) return false
  
  const threshold = stockThresholds[productForm.value.category]
  return productForm.value.stock < threshold
})

function handleCategoryChange() {
  productForm.value.price = null
  productForm.value.description = ''
  productForm.value.stock = 0
}

async function saveProduct() {
  const product = {
    id: editingProduct.value?.id || Date.now(),
    name: productForm.value.name.trim(),
    category: productForm.value.category,
    price: Number(productForm.value.price),
    description: productForm.value.description,
    stock: Number(productForm.value.stock),
    image: imagePreview.value
  }

  if (editingProduct.value) {
    store.updateProduct(product)
  } else {
    store.addProduct(product)
  }

  closeModal()
}

// Computed
const filteredProducts = computed(() => {
  return products.value.filter(product => {
    const matchesSearch = !filters.value.search || 
      product.name.toLowerCase().includes(filters.value.search.toLowerCase()) ||
      product.description.toLowerCase().includes(filters.value.search.toLowerCase())
    const matchesCategory = !filters.value.category || product.category === filters.value.category
    return matchesSearch && matchesCategory
  })
})

// Methods
function viewProductDetails(product) {
  selectedProduct.value = product
}

function editProduct(product) {
  editingProduct.value = product
  productForm.value = {
    name: product.name,
    category: product.category,
    price: product.price,
    description: product.description,
    stock: product.stock
  }
  imagePreview.value = product.image
  showAddProductModal.value = true
}

function confirmDelete(product) {
  productToDelete.value = product
  showDeleteModal.value = true
}

function deleteProduct() {
  if (productToDelete.value) {
    store.deleteProduct(productToDelete.value.id)
    showDeleteModal.value = false
    productToDelete.value = null
  }
}

function triggerFileInput() {
  fileInput.value.click()
}

function handleImageUpload(event) {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = e => {
      imagePreview.value = e.target.result
      productForm.value.image = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

function closeModal() {
  showAddProductModal.value = false
  editingProduct.value = null
  imagePreview.value = null
  productForm.value = {
    name: '',
    category: '',
    price: null,
    description: '',
    stock: 0
  }
}
</script>

<style scoped>
.product-management {
  min-height: calc(100vh - 4rem);
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.header h2 {
  font-size: 1.125rem;
  color: #333;
  margin: 0;
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

.products-table {
  width: 100%;
  border-collapse: collapse;
}

.products-table th,
.products-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #eee;
  font-size: 0.875rem;
}

.products-table th {
  background: #f9fafb;
  font-weight: 500;
  color: #666;
}

.description-cell {
  max-width: 300px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
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

.actions-column {
  display: flex;
  gap: 0.5rem;
}

.product-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.product-image {
  width: 40px;
  height: 40px;
  border-radius: 4px;
  overflow: hidden;
  background: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #eee;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  font-size: 0.75rem;
  color: #666;
  text-align: center;
}

.product-name {
  font-size: 0.875rem;
  color: #333;
}

.action-btn {
  width: 28px;
  height: 28px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn .icon {
  font-size: 1rem;
}

.action-btn.view {
  background: rgba(33, 150, 243, 0.1);
  color: #2196F3;
}

.action-btn.edit {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.action-btn.delete {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
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
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
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

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.product-select {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stock-hint {
  margin-top: 0.25rem;
}

.stock-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  color: #666;
}

.stock-info .threshold {
  background: #e3f2fd;
  color: #1976d2;
  padding: 0.125rem 0.375rem;
  border-radius: 4px;
  font-weight: 500;
}

.stock-info .warning {
  color: #f44336;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.stock-status {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stock-status.low {
  color: #f44336;
}

.stock-warning {
  font-size: 0.75rem;
  color: #f44336;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.btn-sm {
  font-size: 0.75rem;
  padding: 0.375rem 0.75rem;
  height: 32px;
}

.modal-lg {
  width: 90%;
  max-width: 600px;
}

.modal-content {
  transform: translateY(0);
  transition: transform 0.2s;
}

.compact-form {
  padding: 1rem;
}

.modal-header {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  position: sticky;
  top: 0;
  z-index: 10;
}

.modal-header h3 {
  font-size: 0.875rem;
  font-weight: 500;
  color: #333;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.25rem;
  color: #666;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #f5f5f5;
  color: #f44336;
}

.details-layout {
  padding: 1rem;
  overflow-y: auto;
}

.product-image-large {
  width: 100%;
  height: 240px;
  border-radius: 8px;
  overflow: hidden;
  background: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  border: 1px solid #eee;
}

.product-image-large img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.product-image-large .no-image {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.product-image-large .no-image .icon {
  font-size: 2rem;
  color: #ccc;
}

.product-image-large .no-image .text {
  font-size: 0.875rem;
  color: #666;
}

.info-value.price {
  font-size: 1rem;
  color: #2196F3;
  font-weight: 500;
}

.info-value.description {
  font-size: 0.875rem;
  color: #666;
  line-height: 1.5;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.product-select {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stock-hint {
  font-size: 0.75rem;
  color: #666;
  margin-top: 0.25rem;
}

.modal-actions {
  margin-top: 1rem;
  padding-top: 0.75rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

.warning {
  color: #f44336;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

.btn-danger {
  background: #f44336;
  color: white;
}

.btn-danger:hover {
  background: #d32f2f;
}

.btn-link {
  color: #2196F3;
  text-decoration: none;
  padding: 0;
  font-size: 0.875rem;
}

.btn-link:hover {
  text-decoration: underline;
}

.image-upload {
  width: 100%;
  margin-bottom: 1rem;
}

.image-preview {
  width: 100%;
  height: 120px;
  border: 2px dashed #ddd;
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  transition: all 0.2s;
}

.image-preview:hover {
  border-color: #2196F3;
  background: #e3f2fd;
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  color: #666;
}

.upload-placeholder .icon {
  font-size: 2rem;
}

.upload-placeholder .text {
  font-size: 0.875rem;
}

.file-input {
  display: none;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1001;
}

.modal-container {
  position: relative;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1002;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 1rem;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #666;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}

.close-btn:hover {
  background: #f5f5f5;
  color: #333;
}

.modal-form {
  padding: 1rem;
  overflow-y: auto;
  flex: 1;
  min-height: 0;
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
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-control {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.875rem;
  width: 100%;
  transition: border-color 0.2s;
}

.form-control:focus {
  border-color: #2196F3;
  outline: none;
}

.image-upload {
  width: 100%;
  margin-bottom: 1rem;
}

.image-preview {
  width: 100%;
  height: 120px;
  border: 2px dashed #ddd;
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  transition: all 0.2s;
}

.image-preview:hover {
  border-color: #2196F3;
  background: #e3f2fd;
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  color: #666;
}

.upload-placeholder .icon {
  font-size: 2rem;
}

.upload-placeholder .text {
  font-size: 0.875rem;
}

.file-input {
  display: none;
}

.stock-hint {
  margin-top: 0.25rem;
}

.stock-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  color: #666;
}

.stock-info .threshold {
  background: #e3f2fd;
  color: #1976d2;
  padding: 0.125rem 0.375rem;
  border-radius: 4px;
  font-weight: 500;
}

.stock-info .warning {
  color: #f44336;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.modal-actions {
  padding: 1rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  background: #fff;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  height: 32px;
}

.btn-primary {
  background: #2196F3;
  color: #fff;
}

.btn-primary:hover {
  background: #1976d2;
}

.btn-secondary {
  background: #f5f5f5;
  color: #333;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

.btn-sm {
  font-size: 0.75rem;
  padding: 0.375rem 0.75rem;
  height: 32px;
}
</style>
