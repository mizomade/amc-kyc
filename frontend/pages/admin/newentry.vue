<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <h1 class="text-3xl font-bold text-gray-900 mb-6">Add New Entry</h1>

    <div class="bg-white p-6 rounded-lg shadow-md">
      <form @submit.prevent="submitForm" class="space-y-6">
        <div>
          <label for="name" class="block text-sm font-medium text-gray-700">Name</label>
          <input type="text" id="name" v-model="formData.name" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
        </div>
        <div>
          <label for="age" class="block text-sm font-medium text-gray-700">Age</label>
          <input type="number" id="age" v-model="formData.age" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
        </div>
        <div>
          <label for="role" class="block text-sm font-medium text-gray-700">Role</label>
          <input type="text" id="role" v-model="formData.role" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
        </div>
        <div>
          <button type="submit" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
            Submit
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const formData = ref({
  name: '',
  age: null,
  role: '',
});

const submitForm = () => {
  console.log('Form submitted:', formData.value);
  // Here you would typically send this data to your backend API
  alert('Form submitted! Check console for data.');
  // Optionally, redirect after submission
  // navigateTo('/admin/citizenlist');
};

definePageMeta({
  layout: 'admin',
  middleware: 'auth',
//   roles: ['admin'],
});
</script>

<style scoped>
/* Tailwind CSS handles most styling, no custom styles needed here */
</style>
