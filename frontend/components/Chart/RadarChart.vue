<template>
    <Radar :data="chartData" :options="chartOptions" :style="chartStyles" />
  </template>
  
  <script setup lang="ts">
  import type { PropType } from 'vue'
  import { Radar } from 'vue-chartjs'
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    PointElement,
    LineElement,
    RadialLinearScale, // Note the specific scale for radar charts
    Filler,
    type ChartData,
    type ChartOptions
  } from 'chart.js'
  
  // Radar charts have their own unique scale and require the Filler plugin to fill the area.
  ChartJS.register(
    Title,
    Tooltip,
    Legend,
    PointElement,
    LineElement,
    RadialLinearScale,
    Filler
  )
  
  defineProps({
    chartData: {
      type: Object as PropType<ChartData<'radar'>>,
      required: true
    },
    chartOptions: {
      type: Object as PropType<ChartOptions<'radar'>>,
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