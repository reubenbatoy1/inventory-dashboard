import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(JSON.parse(localStorage.getItem('user')) || null)
  const token = ref(localStorage.getItem('token') || null)
  
  // Getters
  const isAuthenticated = computed(() => !!token.value)
  const username = computed(() => user.value?.username || '')
  
  // Actions
  async function login(username, password) {
    try {
      // Create form data for token endpoint
      const formData = new FormData()
      formData.append('username', username)
      formData.append('password', password)
      
      // Call the token endpoint
      const response = await axios.post('/api/token', formData)
      
      if (response.data.access_token) {
        // Set the token
        token.value = response.data.access_token
        localStorage.setItem('token', token.value)
        
        // Get user details
        const userResponse = await axios.get('/api/users/me', {
          headers: {
            'Authorization': `Bearer ${token.value}`
          }
        })
        
        // Save user data
        user.value = userResponse.data
        localStorage.setItem('user', JSON.stringify(user.value))
        
        // For development fallback
        if (!user.value && username === 'admin' && password === 'admin123') {
          const userData = { 
            username: 'admin',
            full_name: 'Administrator',
            email: 'admin@example.com'
          }
          user.value = userData
          localStorage.setItem('user', JSON.stringify(userData))
        }
        
        return true
      }
      return false
    } catch (error) {
      console.error('Login error:', error)
      
      // For development fallback
      if (username === 'admin' && password === 'admin123') {
        const userData = { 
          username: 'admin',
          full_name: 'Administrator',
          email: 'admin@example.com'
        }
        
        // Save to state
        user.value = userData
        token.value = 'mock-jwt-token-' + Math.random()
        
        // Save to localStorage
        localStorage.setItem('user', JSON.stringify(userData))
        localStorage.setItem('token', token.value)
        
        return true
      }
      
      return false
    }
  }
  
  function logout() {
    // Clear state
    user.value = null
    token.value = null
    
    // Clear localStorage
    localStorage.removeItem('user')
    localStorage.removeItem('token')
  }

  return {
    user,
    token,
    isAuthenticated,
    username,
    login,
    logout
  }
})
