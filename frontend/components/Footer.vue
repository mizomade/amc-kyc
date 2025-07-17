<template>
  <footer class="bg-gray-800 text-white py-6 px-4  md:px-8">
    <div class="container mx-auto flex flex-col md:flex-row justify-center items-start gap-9">
      <div class="text-center md:text-left mb-4 md:mb-0">
        <p>&copy; {{ currentYear }} AMC KYC. All rights reserved.</p>
        <p class="text-sm">Designed with <span class="text-red-500">&hearts;</span> </p>
      </div>
      <nav class="flex space-x-4">
        <a href="#" class="hover:text-gray-400 transition-colors duration-300">Privacy Policy</a>
        <a href="#" class="hover:text-gray-400 transition-colors duration-300">Terms of Service</a>
        <a href="#" class="hover:text-gray-400 transition-colors duration-300">Contact Us</a>
      </nav>
    </div>
  </footer>
</template>

<script setup>
import { ref } from 'vue';

const currentYear = ref(new Date().getFullYear());
</script>

<style scoped>
/* Add any custom styles here if needed, though Tailwind should cover most. */
</style>
