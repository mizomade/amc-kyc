<!-- components/DoughnutChart.vue -->
<template>
    <Doughnut v-if="chartData" :data="chartData" :options="chartOptions" :style="chartStyles" />
  </template>
  
  <script setup lang="ts">
  import type { PropType } from 'vue'
  import { Doughnut } from 'vue-chartjs'
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    ArcElement, // <-- Different from Bar chart!
    type ChartData,
    type ChartOptions
  } from 'chart.js'
  
  // Register the necessary components for a Doughnut chart
  ChartJS.register(Title, Tooltip, Legend, ArcElement) // <-- Note the different elements
  
  defineProps({
    chartData: {
      type: Object as PropType<ChartData<'doughnut'>>,
      required: true
    },
    chartOptions: {
      type: Object as PropType<ChartOptions<'doughnut'>>,
      default: () => ({
        responsive: true,
        maintainAspectRatio: false
      })
    },
    chartStyles: {
      type: Object as PropType<Partial<CSSStyleDeclaration>>,
      default: () => ({
        height: '400px',
        position: 'relative'
      })
    }
  })
  </script>