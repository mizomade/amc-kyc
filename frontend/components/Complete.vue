<template>
  <div class="text-center py-16">
    <h1 class="text-3xl font-bold text-green-600 mb-6">Family Successfully Registered! ✨</h1>
    <p class="text-lg text-gray-700 mb-8">
      Thank you for completing the family registration process. All data has been saved successfully.
    </p>

    <div class="flex justify-center space-x-4">
      <NuxtLink to="/house-entry" class="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700">
        Register Another Family
      </NuxtLink>
      <NuxtLink to="/dashboard" class="bg-gray-200 text-gray-800 px-6 py-2 rounded hover:bg-gray-300">
        Go to Dashboard
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
// No script needed for now.
</script>

<style scoped>
/* Optional custom styles */
</style>
