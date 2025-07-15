<template>
  <div :class="bgClass + ' border-l-4 p-6 rounded-lg'">
    <h3 class="text-lg font-medium text-gray-700">{{ title }}</h3>
    <p :class="countClass + ' text-4xl font-bold mt-2'">{{ count }}</p>
  </div>
</template>

<script setup>
const props = defineProps({
  title: String,
  count: Number,
  color: {
    type: String,
    default: 'blue'
  }
})

const bgClass = `bg-${props.color}-50 border-${props.color}-500`
const countClass = `text-${props.color}-900`
</script>
