<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <h1 class="text-3xl font-bold text-gray-900 mb-6">Reports Dashboard</h1>

    <!-- Report Categories/Navigation -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 class="text-xl font-semibold text-gray-900 mb-4">Report Categories</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <button @click="activeReport = 'citizen_statistics'" :class="[activeReport === 'citizen_statistics' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-800 hover:bg-gray-300', 'py-3 px-4 rounded-md font-medium transition duration-300']">
          Citizen Statistics
        </button>
        <button @click="activeReport = 'house_demographics'" :class="[activeReport === 'house_demographics' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-800 hover:bg-gray-300', 'py-3 px-4 rounded-md font-medium transition duration-300']">
          House Demographics
        </button>
        <button @click="activeReport = 'activity_logs'" :class="[activeReport === 'activity_logs' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-800 hover:bg-gray-300', 'py-3 px-4 rounded-md font-medium transition duration-300']">
          Activity Logs
        </button>
        <button @click="activeReport = 'custom_reports'" :class="[activeReport === 'custom_reports' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-800 hover:bg-gray-300', 'py-3 px-4 rounded-md font-medium transition duration-300']">
          Custom Reports
        </button>
      </div>
    </div>

    <!-- Report Content Area -->
    <div class="bg-white rounded-lg shadow-md p-6">
      <div v-if="activeReport === 'citizen_statistics'">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Citizen Statistics Report</h2>
        <p class="text-gray-600">Detailed statistics about user registrations, active users, roles, etc. (e.g., charts, graphs).</p>
        <!-- Placeholder for charts/tables -->
        <div class="mt-4 p-4 bg-gray-50 border border-gray-200 rounded-md">
          <p class="text-gray-500">[Chart/Table for User Statistics]</p>
        </div>
      </div>

      <div v-if="activeReport === 'house_demographics'">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">House Demographics Report</h2>
        <p class="text-gray-600">Demographic breakdown of houses, family sizes, locations, etc.</p>
        <!-- Placeholder for charts/tables -->
        <div class="mt-4 p-4 bg-gray-50 border border-gray-200 rounded-md">
          <p class="text-gray-500">[Chart/Table for House Demographics]</p>
        </div>
      </div>

      <div v-if="activeReport === 'activity_logs'">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Activity Logs Report</h2>
        <p class="text-gray-600">Logs of system activities, user actions, and administrative changes.</p>
        <!-- Placeholder for tables -->
        <div class="mt-4 p-4 bg-gray-50 border border-gray-200 rounded-md">
          <p class="text-gray-500">[Table for Activity Logs]</p>
        </div>
      </div>

      <div v-if="activeReport === 'custom_reports'">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Custom Report Builder</h2>
        <p class="text-gray-600">Interface for building and generating custom reports based on selected criteria.</p>
        <!-- Placeholder for form/builder -->
        <div class="mt-4 p-4 bg-gray-50 border border-gray-200 rounded-md">
          <p class="text-gray-500">[Form/Builder for Custom Reports]</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const activeReport = ref('citizen_statistics'); // Default active report

definePageMeta({
  layout: 'admin',
  middleware: 'auth',
  // roles: ['admin'],
});
</script>

<style scoped>
/* Tailwind CSS handles most styling, no custom styles needed here */
</style>
