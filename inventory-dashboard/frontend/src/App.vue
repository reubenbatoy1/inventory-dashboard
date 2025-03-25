<script setup>
import logo from './assets/logo.png'
import { useAuthStore } from './stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

function logout() {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <!-- Login page doesn't use the app layout -->
  <div v-if="!authStore.isAuthenticated" class="login-layout">
    <router-view />
  </div>
  
  <!-- Main app layout only shown when authenticated -->
  <div v-else class="app">
    <nav class="side-nav">
      <div class="logo-container">
        <div class="logo">
          <img :src="logo" alt="UIC Bookstore Logo" class="logo-image" />
          <div class="logo-text">
            <span class="text-uic">UIC</span>
            <span class="text-bookstore">BOOKSTORE</span>
          </div>
        </div>
      </div>
      <nav class="nav-links">
        <router-link to="/" class="nav-link">
          <span class="icon">📊</span>
          <span class="text">Dashboard</span>
        </router-link>
        <router-link to="/products" class="nav-link">
          <span class="icon">📦</span>
          <span class="text">Products</span>
        </router-link>
        <router-link to="/stock" class="nav-link">
          <span class="icon">🔄</span>
          <span class="text">Stock</span>
        </router-link>
        <router-link to="/orders" class="nav-link">
          <span class="icon">📝</span>
          <span class="text">Orders</span>
        </router-link>
        <router-link to="/reports" class="nav-link">
          <span class="icon">📈</span>
          <span class="text">Reports</span>
        </router-link>
      </nav>

      <!-- Logout at the bottom of sidebar -->
      <div class="logout-container">
        <button @click="logout" class="logout-button">
          <span class="icon">🚪</span>
          <span class="text">Logout</span>
        </button>
      </div>
    </nav>
    <main class="main-content">
      <header class="top-bar">
        <div class="search">
          <input type="text" placeholder="Search..." />
        </div>
        <div class="user-menu">
          <span class="notifications">🔔</span>
          <span class="profile">{{ authStore.username }}</span>
        </div>
      </header>
      <div class="page-content">
        <router-view />
      </div>
    </main>
  </div>
</template>

<style>
.app {
  display: flex;
  min-height: 100vh;
}

.side-nav {
  width: 250px;
  background: white;
  border-right: 1px solid #eee;
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  z-index: 100;
}

.logo-container {
  padding: 1.75rem 1.5rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: center;
  background: white;
}

.logo {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.logo-image {
  height: 65px;
  width: auto;
  object-fit: contain;
}

.logo-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  line-height: 1.1;
}

.text-uic {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2196F3;
  letter-spacing: 0.05em;
}

.text-bookstore {
  font-size: 0.875rem;
  font-weight: 500;
  color: #666;
  letter-spacing: 0.1em;
}

.nav-links {
  display: flex;
  flex-direction: column;
  padding: 0.5rem 0;
  overflow-y: auto;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: #666;
  text-decoration: none;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.nav-link:hover {
  background: #f5f5f5;
  color: #2196F3;
}

.nav-link.router-link-active {
  background: rgba(33, 150, 243, 0.1);
  color: #2196F3;
  font-weight: 500;
}

.nav-link .icon {
  font-size: 1.125rem;
  opacity: 0.8;
}

.nav-link.router-link-active .icon {
  opacity: 1;
}

.main-content {
  flex: 1;
  background: #f9fafb;
  display: flex;
  flex-direction: column;
  margin-left: 250px;
}

.top-bar {
  background: white;
  border-bottom: 1px solid #eee;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 90;
}

.page-content {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
}

/* Global Styles */
.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: #2196F3;
  color: white;
}

.btn-primary:hover {
  background: #1976D2;
}

.btn-secondary {
  background: #f5f5f5;
  color: #666;
}

.btn-secondary:hover {
  background: #e0e0e0;
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

/* Modal Styles */
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
  overflow: hidden;
}

.modal-content {
  background: white;
  border-radius: 8px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  margin: 1rem;
}

.modal-content.modal-lg {
  max-width: 800px;
}

.modal-header {
  padding: 1rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.125rem;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #666;
  cursor: pointer;
}

.close-btn:hover {
  color: #333;
}

.modal-actions {
  padding: 1rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.logout-container {
  margin-top: auto;
  padding: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.logout-button {
  width: 100%;
  display: flex;
  align-items: center;
  padding: 12px 15px;
  color: #e74c3c;
  background: none;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 14px;
}

.logout-button:hover {
  background-color: rgba(231, 76, 60, 0.1);
}

.logout-button .icon {
  margin-right: 10px;
  font-size: 18px;
}

.login-layout {
  min-height: 100vh;
  width: 100%;
}
</style>
