<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="login">
      <input type="text" v-model="username" placeholder="Username" />
      <input type="password" v-model="password" placeholder="Password" />
      <select v-model="selectedRole">
        <option value="">Select Role</option>
        <option value="admin">Admin</option>
        <option value="local_council">Local Council</option>
        <option value="operator">Operator</option>
        <option value="user">User</option>
      </select>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '~/stores/auth';

const username = ref('');
const password = ref('');
const selectedRole = ref(''); // New ref for selected role
const authStore = useAuthStore();

// Redirect to home if already authenticated
if (authStore.token) {
  navigateTo('/');
}

const login = async () => {
  // Simulate a successful login and set the token and user role
  authStore.setToken('simulated_token'); // Set a dummy token
  authStore.setUser({ username: username.value, role: selectedRole.value }); // Set user with selected role

  if (authStore.token) {
    navigateTo('/');
  }
};
</script>
