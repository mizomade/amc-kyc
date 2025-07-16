<template>
  <div>
    <p class="text-sm font-medium text-gray-500">{{ label }}</p>
    <p class="text-lg text-gray-900">{{ value || 'N/A' }}<slot></slot></p>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

defineProps({
  label: String,
  value: [String, Number, Boolean, null],
});
</script>
