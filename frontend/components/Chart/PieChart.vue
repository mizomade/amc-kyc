<template>
  <Pie v-if="chartData" :data="chartData" :options="chartOptions" />
</template>

<script setup lang="ts">
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale } from 'chart.js'
import type { ChartData, ChartOptions } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale)

defineProps<{
  chartData: ChartData<'pie'>,
  chartOptions?: ChartOptions<'pie'>
}>()
</script>