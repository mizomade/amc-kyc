<template>
  <div>
    <Navbar />
    <main class="pt-16">
      <slot />
    </main>
    <footer class="bg-gray-800 text-gray-300 py-8 mt-8">
      <div class="container mx-auto px-6 text-center">
        <p>&copy; 2025 AMC Citizen Management System. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import Navbar from '~/components/navbar.vue';
</script>