<template>
<div class="inventory">
  <!-- Filters and Add Button -->
  <div class="filters">
    <div class="search-filters">
      <input 
        type="text" 
        v-model="filters.search" 
        placeholder="Search..." 
        class="form-control"
      />
      <select v-model="filters.category" class="form-control">
        <option value="">All Categories</option>
        <option v-for="category in categories" :key="category" :value="category">
          {{ category }}
        </option>
      </select>
      <select v-model="filters.stock" class="form-control">
        <option value="">All Stock</option>
        <option value="In Stock">In Stock</option>
        <option value="Low Stock">Low Stock</option>
        <option value="Out of Stock">Out of Stock</option>
      </select>
    </div>
    <button class="btn btn-primary" @click="showAddProductModal = true">
      Add Product
    </button>
  </div>

  <!-- Products Table -->
  <div class="card mt-4">
    <table class="table">
      <thead>
        <tr>
          <th>Product Name</th>
          <th>Category</th>
          <th>Stock</th>
          <th>Unit Price</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in filteredProducts" :key="product.id">
          <td style="min-width: 200px;">
            <div class="product-info" @click="viewProductDetails(product)">
              <div class="product-image">
                <img v-if="product.image" :src="product.image" alt="Product" style="width: 50px; height: 50px; object-fit: cover;" />
                <div v-else class="no-image">No Image</div>
              </div>
              <span class="product-name">{{ product.name }}</span>
            </div>
          </td>
          <td>{{ product.category }}</td>
          <td>{{ product.stock }}</td>
          <td>₱{{ product.price }}</td>
          <td>
            <span :class="['status', product.statusClass]">{{ product.status }}</span>
          </td>
          <td>
            <button class="btn-icon" @click="editProduct(product)">✏️</button>
            <button class="btn-icon" @click="deleteProduct(product.id)">🗑️</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- Add/Edit Product Modal -->
  <div class="modal" v-if="showAddProductModal">
    <div class="modal-content">
      <div class="modal-header">
        <h3>{{ editingProduct ? 'Edit Product' : 'Add New Product' }}</h3>
        <button class="close-btn" @click="closeModal">&times;</button>
      </div>
      <form @submit.prevent="saveProduct">
        <div class="form-grid">
          <div class="form-group full-width">
            <label>Product Image</label>
            <div class="image-upload">
              <input 
                type="file" 
                accept="image/*" 
                @change="handleImageUpload" 
                class="file-input"
                :id="'file-input-' + (editingProduct?.id || 'new')"
              />
              <label :for="'file-input-' + (editingProduct?.id || 'new')" class="file-label">
                <div v-if="imagePreview" class="preview">
                  <img :src="imagePreview" alt="Preview" />
                </div>
                <div v-else class="upload-placeholder">
                  <span>📷 Click to upload image</span>
                </div>
              </label>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Product Name</label>
              <input type="text" v-model="productForm.name" required class="form-control" placeholder="Enter product name" />
            </div>
            <div class="form-group">
              <label>Category</label>
              <select v-model="productForm.category" required class="form-control">
                <option value="" disabled selected>Select category</option>
                <option v-for="category in categories" :key="category" :value="category">
                  {{ category }}
                </option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Stock</label>
              <input type="number" v-model="productForm.stock" required class="form-control" min="0" placeholder="0" />
            </div>
            <div class="form-group">
              <label>Unit Price</label>
              <div class="price-input">
                <span class="currency">₱</span>
                <input type="number" v-model="productForm.price" required class="form-control" min="0" step="0.01" placeholder="0.00" />
              </div>
            </div>
          </div>
          <div class="form-group full-width">
            <label>Description</label>
            <textarea 
              v-model="productForm.description" 
              class="form-control" 
              rows="2" 
              placeholder="Enter product description"
            ></textarea>
          </div>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
          <button type="submit" class="btn btn-primary">{{ editingProduct ? 'Update' : 'Add' }} Product</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Product Details Modal -->
  <div class="modal" v-if="showProductDetailsModal">
    <div class="modal-content modal-lg">
      <div class="modal-header">
        <h3>Product Details</h3>
        <button class="close-btn" @click="closeModal">&times;</button>
      </div>
      <div class="product-details" v-if="selectedProduct">
        <div class="details-layout">
          <div class="product-image-large">
            <img v-if="selectedProduct.image" :src="selectedProduct.image" alt="Product" style="width: 100%; height: 300px; object-fit: contain;" />
            <div v-else class="no-image">No Image Available</div>
          </div>
          <div class="product-info-grid">
            <div class="info-row">
              <div class="info-group">
                <label>Name</label>
                <div class="info-value">{{ selectedProduct.name }}</div>
              </div>
              <div class="info-group">
                <label>Category</label>
                <div class="info-value">{{ selectedProduct.category }}</div>
              </div>
            </div>
            <div class="info-row">
              <div class="info-group">
                <label>Stock</label>
                <div class="info-value">
                  <span :class="['status', selectedProduct.statusClass]">
                    {{ selectedProduct.stock }}
                  </span>
                </div>
              </div>
              <div class="info-group">
                <label>Price</label>
                <div class="info-value price">₱{{ selectedProduct.price }}</div>
              </div>
            </div>
            <div class="info-group description-group">
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
</div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useInventoryStore } from '../stores/inventory'

// Initialize store
const store = useInventoryStore()
const products = store.products

// Local state
const showAddProductModal = ref(false)
const showProductDetailsModal = ref(false)
const editingProduct = ref(null)
const selectedProduct = ref(null)
const imagePreview = ref(null)

const filters = ref({
  search: '',
  category: '',
  stock: ''
})

const categories = ['Uniform', 'Books', 'Other']

const productForm = ref({
  name: '',
  category: '',
  stock: 0,
  price: 0,
  description: '',
  image: null
})

function updateProductStatus(product) {
  // Different thresholds for each category
  const thresholds = {
    'Uniform': 10,  // Low stock if less than 10 uniforms
    'Books': 5,     // Low stock if less than 5 books
    'Other': 50     // Low stock if less than 50 scantron sheets
  }
  
  const threshold = thresholds[product.category]
  
  if (product.stock <= 0) {
    product.status = 'Out of Stock'
    product.statusClass = 'out-of-stock'
  } else if (product.stock < threshold) {
    product.status = 'Low Stock'
    product.statusClass = 'low-stock'
  } else {
    product.status = 'In Stock'
    product.statusClass = 'in-stock'
  }
}

// Call updateProductStatus for each product on mount
onMounted(() => {
  products.value.forEach(updateProductStatus)
})

// Computed property for filtered products
const filteredProducts = computed(() => {
  return products.value.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(filters.value.search.toLowerCase())
    const matchesCategory = !filters.value.category || product.category === filters.value.category
    const matchesStock = !filters.value.stock || product.status === filters.value.stock
    return matchesSearch && matchesCategory && matchesStock
  })
})

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

function viewProductDetails(product) {
  selectedProduct.value = { ...product }
  showProductDetailsModal.value = true
}

function editProduct(product) {
  editingProduct.value = { ...product }
  productForm.value = { ...product }
  imagePreview.value = product.image
  showAddProductModal.value = true
}

function deleteProduct(id) {
  if (confirm('Are you sure you want to delete this product?')) {
    store.deleteProduct(id)
  }
}

function saveProduct() {
  const formData = { ...productForm.value }
  if (editingProduct.value) {
    store.updateProduct({ ...formData, id: editingProduct.value.id })
    const product = products.value.find(p => p.id === editingProduct.value.id)
    if (product) {
      updateProductStatus(product)
    }
  } else {
    formData.id = products.value.length + 1
    formData.status = 'In Stock'
    formData.statusClass = 'in-stock'
    store.addProduct(formData)
    updateProductStatus(formData)
  }
  closeModal()
}

function closeModal() {
  showAddProductModal.value = false
  showProductDetailsModal.value = false
  editingProduct.value = null
  selectedProduct.value = null
  productForm.value = {
    name: '',
    category: '',
    stock: 0,
    price: 0,
    description: '',
    image: null
  }
  imagePreview.value = null
}
</script>

<style scoped>
.inventory {
  padding: 0.75rem;
}

.filters {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
}

.search-filters {
  display: flex;
  gap: 0.75rem;
  flex: 1;
  max-width: 600px;
}

.form-control {
  font-size: 11px;
  padding: 0.35rem 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  color: #666;
}

.form-control:focus {
  outline: none;
  border-color: #2196F3;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.1);
}

.table {
  width: 100%;
  border-collapse: collapse;
  font-size: 11px;
}

.table th {
  text-align: left;
  padding: 0.75rem;
  font-weight: 500;
  color: #666;
  border-bottom: 1px solid #ddd;
}

.table td {
  padding: 0.75rem;
  border-bottom: 1px solid #ddd;
  color: #666;
}

.product-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
}

.product-image {
  width: 50px;
  height: 50px;
  border-radius: 4px;
  overflow: hidden;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-image-large {
  width: 100%;
  height: 300px;
  border-radius: 8px;
  overflow: hidden;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.no-image {
  font-size: 12px;
  color: #999;
  text-align: center;
}

.status {
  padding: 0.35rem 0.75rem;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
}

.status.in-stock {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.status.low-stock {
  background: rgba(255, 152, 0, 0.1);
  color: #FF9800;
}

.status.out-of-stock {
  background: rgba(255, 0, 0, 0.1);
  color: #FF0000;
}

.btn-icon {
  padding: 0.35rem;
  border: none;
  background: none;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.btn-icon:hover {
  opacity: 1;
}

/* Modal styles updated to match UI preferences */
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
  background: white;
  border-radius: 4px;
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  padding: 0.75rem;
  border-bottom: 1px solid #ddd;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-header h3 {
  font-size: 11px;
  font-weight: 500;
  color: #666;
  margin: 0;
}

.form-grid {
  padding: 0.75rem;
  display: grid;
  gap: 0.75rem;
}

.form-group label {
  display: block;
  font-size: 11px;
  color: #666;
  margin-bottom: 0.35rem;
}

.modal-actions {
  padding: 0.75rem;
  border-top: 1px solid #ddd;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.product-details {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.details-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  align-items: start;
}

.info-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.info-group {
  background: #f8f9fa;
  padding: 0.75rem;
  border-radius: 6px;
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
  font-size: 11px;
  color: #2c3e50;
  font-weight: 500;
}

.info-value.price {
  color: #2196F3;
  font-size: 1rem;
}

.description-group {
  grid-column: 1 / -1;
}

.info-value.description {
  font-weight: normal;
  white-space: pre-line;
  line-height: 1.5;
  color: #444;
}
</style>
