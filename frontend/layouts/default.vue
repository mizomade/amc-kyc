<template>
  <div>
    <Navbar />
    <main class="pt-16">
      <slot />
    </main>
  </div>
  <Footer />
</template>

<script setup>
import Navbar from '~/components/navbar.vue';
import Footer from '~/components/Footer.vue';
</script>