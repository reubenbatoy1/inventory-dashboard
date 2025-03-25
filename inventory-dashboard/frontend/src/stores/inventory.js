import { ref } from 'vue'

// Create a singleton store instance
const products = ref([
  {
    id: 1,
    name: 'Polo',
    category: 'Uniform',
    stock: 30,
    price: 450,
    status: 'In Stock',
    statusClass: 'in-stock',
    description: 'School polo uniform',
    history: []
  },
  {
    id: 2,
    name: 'Jogging Pants',
    category: 'Uniform',
    stock: 25,
    price: 400,
    status: 'In Stock',
    statusClass: 'in-stock',
    description: 'School jogging pants',
    history: []
  },
  {
    id: 3,
    name: 'Blouse',
    category: 'Uniform',
    stock: 8,
    price: 425,
    status: 'Low Stock',
    statusClass: 'low-stock',
    description: 'School blouse uniform',
    history: []
  },
  {
    id: 4,
    name: 'Physics Book',
    category: 'Books',
    stock: 15,
    price: 750,
    status: 'In Stock',
    statusClass: 'in-stock',
    description: 'Physics textbook',
    history: []
  },
  {
    id: 5,
    name: 'Chemistry Book',
    category: 'Books',
    stock: 12,
    price: 750,
    status: 'In Stock',
    statusClass: 'in-stock',
    description: 'Chemistry textbook',
    history: []
  },
  {
    id: 6,
    name: 'PE Book',
    category: 'Books',
    stock: 3,
    price: 500,
    status: 'Low Stock',
    statusClass: 'low-stock',
    description: 'Physical Education textbook',
    history: []
  },
  {
    id: 7,
    name: 'Scantron',
    category: 'Other',
    stock: 45,
    price: 5,
    status: 'Low Stock',
    statusClass: 'low-stock',
    description: 'Scantron answer sheets',
    history: []
  }
])

const orders = ref([
  {
    id: 1,
    customer: 'John Doe',
    date: '2025-03-11',
    status: 'pending',
    items: [
      { id: 1, name: 'Polo', quantity: 2, price: 450, cost: 350 },
      { id: 2, name: 'Jogging Pants', quantity: 1, price: 400, cost: 300 }
    ]
  },
  {
    id: 2,
    customer: 'Jane Smith',
    date: '2025-03-10',
    status: 'completed',
    items: [
      { id: 4, name: 'Physics Book', quantity: 1, price: 750, cost: 600 },
      { id: 5, name: 'Chemistry Book', quantity: 1, price: 750, cost: 600 }
    ]
  },
  {
    id: 3,
    customer: 'Alice Brown',
    date: '2025-03-12',
    status: 'pending',
    items: [
      { id: 7, name: 'Scantron', quantity: 20, price: 5, cost: 3 },
      { id: 3, name: 'Blouse', quantity: 1, price: 425, cost: 325 }
    ]
  }
])

const purchaseOrders = ref([
  {
    id: 1,
    supplier: 'Uniform Supplier',
    date: '2025-03-11',
    status: 'pending',
    items: [
      { id: 1, name: 'Polo', quantity: 50, cost: 350 }
    ]
  },
  {
    id: 2,
    supplier: 'Book Store',
    date: '2025-03-10',
    status: 'processing',
    items: [
      { id: 4, name: 'Physics Book', quantity: 20, cost: 600 }
    ]
  }
])

// Stock thresholds
const stockThresholds = {
  'Uniform': 10,
  'Books': 5,
  'Other': 50
}

// Update product status based on stock level
const updateProductStatus = (product) => {
  if (product.stock === 0) {
    product.status = 'Out of Stock'
    product.statusClass = 'out-of-stock'
  } else {
    const threshold = stockThresholds[product.category]
    if (product.stock < threshold) {
      product.status = 'Low Stock'
      product.statusClass = 'low-stock'
    } else {
      product.status = 'In Stock'
      product.statusClass = 'in-stock'
    }
  }
}

// Stock adjustment function
const adjustStock = (adjustment) => {
  const product = products.value.find(p => p.id === adjustment.productId)
  if (!product) return false

  const newStock = adjustment.type === 'add' 
    ? product.stock + adjustment.quantity 
    : product.stock - adjustment.quantity

  if (newStock < 0) return false

  // Add to history
  const historyEntry = {
    id: Date.now(),
    date: new Date().toISOString(),
    type: adjustment.type,
    quantity: adjustment.quantity,
    reason: adjustment.reason,
    notes: adjustment.notes
  }

  product.stock = newStock
  product.history.unshift(historyEntry)
  updateProductStatus(product)

  return true
}

// Product management functions
const addProduct = (product) => {
  products.value.push(product)
}

const updateProduct = (updatedProduct) => {
  const index = products.value.findIndex(p => p.id === updatedProduct.id)
  if (index !== -1) {
    products.value[index] = { ...updatedProduct }
  }
}

const deleteProduct = (id) => {
  products.value = products.value.filter(p => p.id !== id)
}

// Order management
const addOrder = (order) => {
  orders.value.push(order)
}

const updateOrder = (updatedOrder) => {
  const index = orders.value.findIndex(o => o.id === updatedOrder.id)
  if (index !== -1) {
    orders.value[index] = { ...updatedOrder }
  }
}

// Purchase order management
const addPurchaseOrder = (order) => {
  purchaseOrders.value.push(order)
}

// Export a singleton store
export const useInventoryStore = () => {
  return {
    products,
    orders,
    purchaseOrders,
    addProduct,
    updateProduct,
    deleteProduct,
    addOrder,
    updateOrder,
    addPurchaseOrder,
    adjustStock,
    stockThresholds
  }
}
