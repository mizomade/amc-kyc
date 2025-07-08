<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <h1 class="text-3xl font-bold text-gray-900 mb-6">Add New User</h1>

    <div class="bg-white p-6 rounded-lg shadow-md">
      <form @submit.prevent="submitForm" class="space-y-6">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
          <input type="text" id="username" v-model="formData.username" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
        </div>
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
          <input type="email" id="email" v-model="formData.email" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
        </div>
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <input type="password" id="password" v-model="formData.password" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
        </div>
        <div>
          <label for="role" class="block text-sm font-medium text-gray-700">Role</label>
          <select id="role" v-model="formData.role" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
            <option value="">Select Role</option>
            <option value="admin">Admin</option>
            <option value="local_council">Local Council</option>
            <option value="operator">Operator</option>
            <option value="user">User</option>
          </select>
        </div>
        <div>
          <button type="submit" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
            Add User
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const formData = ref({
  username: '',
  email: '',
  password: '',
  role: '',
});

const submitForm = () => {
  console.log('Form submitted:', formData.value);
  // Here you would typically send this data to your backend API
  alert('User added! Check console for data.');
  // Optionally, redirect after submission
  // navigateTo('/admin/users');
};

definePageMeta({
  layout: 'admin',
  middleware: 'auth',
  roles: ['admin'],
});
</script>

<style scoped>
/* Tailwind CSS handles most styling, no custom styles needed here */
</style>
