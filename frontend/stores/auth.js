import { defineStore } from 'pinia';
import { useNuxtApp } from '#app';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
    user: null,
    refresh_token: null,
  }),
  actions: {
    setToken(token, refresh) {
      this.token = token;
      this.refresh_token = refresh;
      if (process.client) {
        localStorage.setItem('auth_token', token);
        localStorage.setItem('auth_refresh_token', refresh);
      }
    },
    setUser(user) {
      this.user = user;
    },
    async login(credentials) {
      const { $api } = useNuxtApp();
      try {
        const response = await $api.post('/token/', credentials);
        this.setToken(response.data.access, response.data.refresh);
        await this.fetchUser();
      } catch (error) {
        console.error('Login failed:', error);
        // Handle login error (e.g., show a notification)
      }
    },
    async fetchUser() {
      const { $api } = useNuxtApp();
      try {
        const response = await $api.get('/user/getch/me/'); // Assuming this endpoint exists
        this.setUser(response.data);
      } catch (error) {
        console.error('Failed to fetch user:', error);
        this.logout(); // Log out if user data cannot be fetched
      }
    },
    logout() {
      this.token = null;
      this.refresh_token = null;
      this.user = null;
      if (process.client) {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('auth_refresh_token');
      }
    },
    init() {
      if (process.client) {
        const token = localStorage.getItem('auth_token');
        const refreshToken = localStorage.getItem('auth_refresh_token');
        if (token && refreshToken) {
          this.setToken(token, refreshToken);
          this.fetchUser();
        }
      }
    },
  },
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
});
