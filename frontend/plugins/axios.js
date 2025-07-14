import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

export default defineNuxtPlugin((nuxtApp) => {
  console.log('✅ Axios plugin loaded')

  const api = axios.create({
    baseURL: 'http://localhost:8000/api',
  })

  api.interceptors.request.use((config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  })


  nuxtApp.provide('axios', api) 
})
