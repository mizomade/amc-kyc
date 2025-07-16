<template>
  <NuxtLayout>
    <!-- <UApp> -->

    <NuxtPage />
  <!-- </UApp> -->
</NuxtLayout>

</template>

<script setup>
import { useAuthStore } from '~/stores/auth';
import { onMounted } from 'vue';

const authStore = useAuthStore();

onMounted(() => {
  authStore.init();
});
</script>



