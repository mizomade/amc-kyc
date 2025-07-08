<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900">Citizen List</h1>
      <NuxtLink to="/admin/newentry" class="bg-blue-600 text-white py-2 px-4 rounded-md shadow-md hover:bg-blue-700 transition duration-300">
        Add New Entry
      </NuxtLink>
    </div>

    <!-- Tabs for different lists (e.g., Persons, Houses) -->
    <div class="bg-white rounded-lg shadow-md p-6">
      <div class="border-b border-gray-200 mb-4">
        <nav class="-mb-px flex space-x-8" aria-label="Tabs">
          <button @click="activeTab = 'persons'" :class="[activeTab === 'persons' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300', 'whitespace-nowrap py-3 px-1 border-b-2 font-medium text-sm']">
            Persons
          </button>
          <button @click="activeTab = 'houses'" :class="[activeTab === 'houses' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300', 'whitespace-nowrap py-3 px-1 border-b-2 font-medium text-sm']">
            Houses
          </button>
          <!-- Add more tabs as needed -->
        </nav>
      </div>

      <div v-if="activeTab === 'persons'">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Persons</h2>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Age</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="person in persons" :key="person.id">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ person.name }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ person.age }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ person.role }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <a href="#" class="text-blue-600 hover:text-blue-900 mr-4">Edit</a>
                  <a href="#" class="text-red-600 hover:text-red-900">Delete</a>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div v-if="activeTab === 'houses'">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Houses</h2>
        <p class="text-gray-600">Content for houses list will go here.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const activeTab = ref('persons');

const persons = ref([
  { id: 1, name: 'Alice Smith', age: 30, role: 'Resident' },
  { id: 2, name: 'Bob Johnson', age: 45, role: 'Head of Household' },
  { id: 3, name: 'Charlie Brown', age: 22, role: 'Student' },
]);

definePageMeta({
  layout: 'admin',
  middleware: 'auth',
//   roles: ['admin'],
});
</script>

<style scoped>
/* Tailwind CSS handles most styling, no custom styles needed here */
</style>
