<template>
  <nav class="bg-white  fixed w-full z-20">
    <div class="container mx-auto px-6 py-3 flex justify-between items-center">
      <NuxtLink to="/" class="text-xl font-bold text-blue-600">KYC</NuxtLink>
      <div class="flex items-center space-x-4">
        <!-- <NuxtLink to="/admin" class="text-gray-600 hover:text-blue-600">Admin</NuxtLink>
        <NuxtLink to="/local_council" class="text-gray-600 hover:text-blue-600">Local Council</NuxtLink>
        <NuxtLink to="/operator" class="text-gray-600 hover:text-blue-600">Operator</NuxtLink> -->
        <button v-if="!authStore.isAuthenticated" @click="goToLogin" class="bg-blue-600 text-white hover:bg-blue-700 transition duration-300 ease-in-out font-bold py-2 px-4 rounded-full">
          Login
        </button>
        <button v-if="authStore.isAuthenticated" @click="logout" class="bg-red-600 text-white hover:bg-red-700 transition duration-300 ease-in-out font-bold py-2 px-4 rounded-full">
          Logout
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '~/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const goToLogin = () => {
  router.push('/login');
};

const logout = () => {
  authStore.logout();
  router.push('/login');
};
</script>
