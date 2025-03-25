<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <img src="../assets/logo.png" alt="UIC Bookstore Logo" class="login-logo" />
        <div class="login-title">
          <h1><span class="text-uic">UIC</span> <span class="text-bookstore">BOOKSTORE</span></h1>
          <p>Inventory Management System</p>
        </div>
      </div>

      <form @submit.prevent="login" class="login-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input 
            type="text" 
            id="username" 
            v-model="form.username" 
            class="form-control" 
            required 
            placeholder="Enter username"
            autocomplete="username"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <div class="password-input">
            <input 
              :type="showPassword ? 'text' : 'password'" 
              id="password" 
              v-model="form.password" 
              class="form-control" 
              required 
              placeholder="Enter password"
              autocomplete="current-password"
            />
            <button 
              type="button" 
              class="toggle-password" 
              @click="showPassword = !showPassword"
            >
              {{ showPassword ? '👁️' : '👁️‍🗨️' }}
            </button>
          </div>
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <button type="submit" class="btn-primary login-btn" :disabled="isLoading">
          {{ isLoading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  username: '',
  password: ''
})

const error = ref('')
const isLoading = ref(false)
const showPassword = ref(false)

async function login() {
  error.value = ''
  isLoading.value = true
  
  try {
    const success = await authStore.login(form.username, form.password)
    if (success) {
      router.push('/')
    } else {
      error.value = 'Invalid username or password'
    }
  } catch (err) {
    console.error('Login error:', err)
    error.value = 'An error occurred during login. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  padding: 40px;
}

.login-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
  text-align: center;
}

.login-logo {
  width: 80px;
  height: auto;
  margin-bottom: 15px;
}

.login-title h1 {
  font-size: 24px;
  margin-bottom: 5px;
}

.login-title p {
  color: #666;
  margin: 0;
}

.text-uic {
  font-weight: 700;
  color: #2c3e50;
}

.text-bookstore {
  font-weight: 300;
  color: #3498db;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 600;
  font-size: 14px;
  color: #555;
}

.form-control {
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-control:focus {
  border-color: #3498db;
  outline: none;
}

.password-input {
  position: relative;
  display: flex;
}

.password-input input {
  flex: 1;
  padding-right: 40px;
}

.toggle-password {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  opacity: 0.6;
  transition: opacity 0.3s;
}

.toggle-password:hover {
  opacity: 1;
}

.login-btn {
  padding: 14px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s;
  margin-top: 10px;
}

.login-btn:hover {
  background-color: #2980b9;
}

.login-btn:disabled {
  background-color: #99c4e7;
  cursor: not-allowed;
}

.error-message {
  color: #e74c3c;
  font-size: 14px;
  background-color: rgba(231, 76, 60, 0.1);
  padding: 10px;
  border-radius: 6px;
  text-align: center;
}
</style>
