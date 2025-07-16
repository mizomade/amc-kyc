<template>
  <div class="flex min-h-screen bg-gray-100">
    <Sidebar ref="sidebarRef" />
    <main :style="mainContentStyle" class="flex-1 p-6 transition-all duration-300">
      <slot />
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import Sidebar from '~/components/sidebar.vue';

const sidebarRef = ref(null);

const mainContentStyle = computed(() => {
  const sidebarWidthOpen = 256; // w-64 max-w-[16rem] = 16 * 16px = 256px
  const sidebarWidthClosed = 80; // w-20 max-w-[5rem] = 5 * 16px = 80px

  if (sidebarRef.value && sidebarRef.value.isOpen) {
    return { marginLeft: `${sidebarWidthOpen}px` };
  } else {
    return { marginLeft: `${sidebarWidthClosed}px` };
  }
});
</script>
