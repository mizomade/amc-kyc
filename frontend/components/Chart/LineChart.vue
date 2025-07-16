<template>
    <Line v-if="chartData" :data="chartData" :options="chartOptions" :style="chartStyles" />
  </template>
  
  <script setup lang="ts">
  import type { PropType } from 'vue'
  import { Line } from 'vue-chartjs'
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    CategoryScale,
    type ChartData,
    type ChartOptions
  } from 'chart.js'
  
  // A line chart requires all these elements.
  ChartJS.register(
    Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    CategoryScale
  )
  
  defineProps({
    chartData: {
      type: Object as PropType<ChartData<'line'>>,
      required: true
    },
    chartOptions: {
      type: Object as PropType<ChartOptions<'line'>>,
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