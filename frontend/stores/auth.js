// stores/auth.js
import { defineStore } from 'pinia'
import { useNuxtApp } from '#app'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
    refresh_token: null,
    user: null
  }),
  actions: {
    setToken(token, refresh) {
      this.token = token
      this.refresh_token = refresh
    },
    setUser(user) {
      this.user = user
    },
    async login(credentials) {
      const { $axios } = useNuxtApp()
      try {
        const response = await $axios.post('/token/', credentials)
        this.setToken(response.data.access, response.data.refresh)
        await this.fetchUser()
      } catch (error) {
        console.error('Login failed:', error)
      }
    },
    async fetchUser() {
      const { $axios } = useNuxtApp()
      try {
        const response = await $axios.get('/user/me/')
        this.setUser(response.data)
      } catch (error) {
        console.error('Failed to fetch user:', error)
        this.logout()
      }
    },
    logout() {
      this.token = null
      this.refresh_token = null
      this.user = null
    }
  }
})
