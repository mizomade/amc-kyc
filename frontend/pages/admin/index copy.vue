<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <h1 class="text-3xl font-bold text-gray-900 mb-6">Admin Dashboard</h1>

    <!-- Stats Section -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white p-6 rounded-lg shadow-md flex items-center justify-between">
        <div>
          <p class="text-gray-500 text-sm">Total Users</p>
          <p class="text-3xl font-bold text-gray-900">1,234</p>
        </div>
        <div class="text-blue-500 text-4xl">
          <i class="fas fa-users"></i>
        </div>
      </div>
      <div class="bg-white p-6 rounded-lg shadow-md flex items-center justify-between">
        <div>
          <p class="text-gray-500 text-sm">New Registrations</p>
          <p class="text-3xl font-bold text-gray-900">125</p>
        </div>
        <div class="text-green-500 text-4xl">
          <i class="fas fa-user-plus"></i>
        </div>
      </div>
      <div class="bg-white p-6 rounded-lg shadow-md flex items-center justify-between">
        <div>
          <p class="text-gray-500 text-sm">Pending Approvals</p>
          <p class="text-3xl font-bold text-gray-900">45</p>
        </div>
        <div class="text-yellow-500 text-4xl">
          <i class="fas fa-hourglass-half"></i>
        </div>
      </div>
      <div class="bg-white p-6 rounded-lg shadow-md flex items-center justify-between">
        <div>
          <p class="text-gray-500 text-sm">Active Sessions</p>
          <p class="text-3xl font-bold text-gray-900">87</p>
        </div>
        <div class="text-purple-500 text-4xl">
          <i class="fas fa-chart-line"></i>
        </div>
      </div>
    </div>

    <!-- Recent Activity & Quick Links Section -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2 bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Recent Activity</h2>
        <ul class="divide-y divide-gray-200">
          <li class="py-3 flex justify-between items-center">
            <p class="text-gray-700">User <span class="font-medium">John Doe</span> registered.</p>
            <span class="text-gray-500 text-sm">2 hours ago</span>
          </li>
          <li class="py-3 flex justify-between items-center">
            <p class="text-gray-700">Admin <span class="font-medium">Jane Smith</span> approved a user.</p>
            <span class="text-gray-500 text-sm">Yesterday</span>
          </li>
          <li class="py-3 flex justify-between items-center">
            <p class="text-gray-700">New document uploaded by <span class="font-medium">User A</span>.</p>
            <span class="text-gray-500 text-sm">3 days ago</span>
          </li>
        </ul>
      </div>

      <div class="bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Quick Links</h2>
        <div class="grid grid-cols-1 gap-3">
          <NuxtLink to="/admin/users" class="bg-blue-500 text-white py-3 px-4 rounded-md text-center hover:bg-blue-600 transition duration-300">
            Manage Users
          </NuxtLink>
          <NuxtLink to="/admin/settings" class="bg-green-500 text-white py-3 px-4 rounded-md text-center hover:bg-green-600 transition duration-300">
            System Settings
          </NuxtLink>
          <NuxtLink to="/admin/reports" class="bg-purple-500 text-white py-3 px-4 rounded-md text-center hover:bg-purple-600 transition duration-300">
            View Reports
          </NuxtLink>
          <NuxtLink to="/admin/citizenlist" class="bg-purple-500 text-white py-3 px-4 rounded-md text-center hover:bg-purple-600 transition duration-300">
            List
          </NuxtLink>
          <NuxtLink to="/admin/newentry" class="bg-purple-500 text-white py-3 px-4 rounded-md text-center hover:bg-purple-600 transition duration-300">
            New Entry
        </NuxtLink>
        <NuxtLink to="/admin/treeview" class="bg-purple-500 text-white py-3 px-4 rounded-md text-center hover:bg-purple-600 transition duration-300">
            Tree View
        </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'admin',
  middleware: 'auth',
//   roles: ['admin'],
});
</script>

<style scoped>
/* No custom styles needed, Tailwind handles everything */
</style>
