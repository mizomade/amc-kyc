<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-100 to-gray-200 p-8">
    <h1 class="text-4xl font-bold text-gray-800 mb-10">Admin Dashboard</h1>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
      <div class="bg-white rounded-xl shadow-md p-6 flex items-center justify-between">
        <div>
          <p class="text-sm text-gray-500">Total Users</p>
          <p class="text-3xl font-bold text-blue-600">1,234</p>
        </div>
        <div class="text-blue-500 text-4xl">
          <i class="fas fa-users"></i>
        </div>
      </div>
      <div class="bg-white rounded-xl shadow-md p-6 flex items-center justify-between">
        <div>
          <p class="text-sm text-gray-500">New Registrations</p>
          <p class="text-3xl font-bold text-green-600">125</p>
        </div>
        <div class="text-green-500 text-4xl">
          <i class="fas fa-user-plus"></i>
        </div>
      </div>
      <div class="bg-white rounded-xl shadow-md p-6 flex items-center justify-between">
        <div>
          <p class="text-sm text-gray-500">Pending Approvals</p>
          <p class="text-3xl font-bold text-yellow-600">45</p>
        </div>
        <div class="text-yellow-500 text-4xl">
          <i class="fas fa-hourglass-half"></i>
        </div>
      </div>
      <div class="bg-white rounded-xl shadow-md p-6 flex items-center justify-between">
        <div>
          <p class="text-sm text-gray-500">Active Sessions</p>
          <p class="text-3xl font-bold text-purple-600">87</p>
        </div>
        <div class="text-purple-500 text-4xl">
          <i class="fas fa-chart-line"></i>
        </div>
      </div>
    </div>

    <!-- Bottom Section: Activity + Quick Links -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Recent Activity -->
      <div class="lg:col-span-2 bg-white rounded-xl shadow-md p-6">
        <h2 class="text-xl font-semibold text-gray-800 mb-4">Recent Activity</h2>
        <ul class="divide-y divide-gray-200">
          <li class="py-4 flex justify-between items-center">
            <p class="text-gray-700">
              <span class="font-medium text-blue-600">John Doe</span> registered.
            </p>
            <span class="text-gray-500 text-sm">2 hours ago</span>
          </li>
          <li class="py-4 flex justify-between items-center">
            <p class="text-gray-700">
              <span class="font-medium text-green-600">Jane Smith</span> approved a user.
            </p>
            <span class="text-gray-500 text-sm">Yesterday</span>
          </li>
          <li class="py-4 flex justify-between items-center">
            <p class="text-gray-700">
              New document uploaded by <span class="font-medium text-purple-600">User A</span>.
            </p>
            <span class="text-gray-500 text-sm">3 days ago</span>
          </li>
        </ul>
      </div>

      <!-- Quick Links -->
      <div class="bg-white rounded-xl shadow-md p-6">
        <h2 class="text-xl font-semibold text-gray-800 mb-4">Quick Links</h2>
        <div class="space-y-3">
          <NuxtLink to="/admin/users" class="block bg-blue-600 text-white text-center py-3 rounded-lg hover:bg-blue-700 transition">
            Manage Users
          </NuxtLink>
          <NuxtLink to="/admin/settings" class="block bg-green-600 text-white text-center py-3 rounded-lg hover:bg-green-700 transition">
            System Settings
          </NuxtLink>
          <NuxtLink to="/admin/reports" class="block bg-purple-600 text-white text-center py-3 rounded-lg hover:bg-purple-700 transition">
            View Reports
          </NuxtLink>
          <NuxtLink to="/admin/citizenlist" class="block bg-indigo-600 text-white text-center py-3 rounded-lg hover:bg-indigo-700 transition">
            Citizen List
          </NuxtLink>
          <NuxtLink to="/house-entry/" class="block bg-pink-600 text-white text-center py-3 rounded-lg hover:bg-pink-700 transition">
            New Entry
          </NuxtLink>
          <NuxtLink to="/admin/treeview" class="block bg-yellow-600 text-white text-center py-3 rounded-lg hover:bg-yellow-700 transition">
            Tree View
          </NuxtLink>
          <NuxtLink to="/search/" class="block bg-gray-800 text-white text-center py-3 rounded-lg hover:bg-gray-900 transition">
            Search
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
