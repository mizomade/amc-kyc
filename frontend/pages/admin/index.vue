'''<template>
  <div class="page-container">
    <h1 class="text-3xl font-bold text-gray-800 mb-8 text-center">Admin Dashboard</h1>

    <ClientOnly>
      <div v-if="dashboardData">
        <!-- Summary Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
          <SummaryCard title="Total Houses" :count="dashboardData?.total_houses" color="blue" />
          <SummaryCard title="Verified Houses" :count="dashboardData?.verified_houses_count" color="green" />
          <SummaryCard title="Total Citizens" :count="dashboardData?.total_citizens" color="purple" />
          <SummaryCard title="Verified Citizens (%)" :count="dashboardData?.verified_citizens_percentage" color="yellow" />
        </div>

        <!-- House Stats -->
        <h2 class="text-2xl font-semibold text-gray-700 mb-6 text-center">House Statistics</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
          <div class="chart-wrapper">
            <h3 class="text-xl font-medium text-gray-700 mb-4">House Ownership</h3>
            <PieChart :chart-data="houseOwnershipData" :chart-options="chartOptions" />
          </div>
          <div class="chart-wrapper">
            <h3 class="text-xl font-medium text-gray-700 mb-4">Houses with Tenants</h3>
            <DoughnutChart :chart-data="houseTenantData" :chart-options="chartOptions" />
          </div>
          <div class="chart-wrapper col-span-full">
            <h3 class="text-xl font-medium text-gray-700 mb-4">House Establishment Trends</h3>
            <LineChart :chart-data="rentStartTrendData" :chart-options="chartOptions" />
          </div>
        </div>

        <!-- Citizen Stats -->
        <h2 class="text-2xl font-semibold text-gray-700 mb-6 text-center">Citizen Statistics</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
          <div class="chart-wrapper">
            <h3 class="text-xl font-medium text-gray-700 mb-4">Gender Distribution</h3>
            <PieChart :chart-data="genderDistributionData" :chart-options="chartOptions" />
          </div>
          <div class="chart-wrapper">
            <h3 class="text-xl font-medium text-gray-700 mb-4">Age Group Distribution</h3>
            <BarChart :chart-data="ageGroupData" :chart-options="chartOptions" />
          </div>
        </div>

        <!-- Religion, Education & Occupation Stats -->
        <h2 class="text-2xl font-semibold text-gray-700 mb-6 text-center">Demographic Insights</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
          <div class="chart-wrapper">
            <h3 class="text-xl font-medium text-gray-700 mb-4">Religion Distribution</h3>
            <PieChart :chart-data="religionDistributionData" :chart-options="chartOptions" />
          </div>
          <div class="chart-wrapper">
            <h3 class="text-xl font-medium text-gray-700 mb-4">Top 5 Denominations</h3>
            <BarChart :chart-data="topDenominationsData" :chart-options="chartOptions" />
          </div>
          <div class="chart-wrapper">
            <h3 class="text-xl font-medium text-gray-700 mb-4">Top 5 Occupations</h3>
            <BarChart :chart-data="topOccupationsData" :chart-options="chartOptions" />
          </div>
          <div class="chart-wrapper">
            <h3 class="text-xl font-medium text-gray-700 mb-4">Top 5 Education Levels</h3>
            <BarChart :chart-data="topEducationLevelsData" :chart-options="chartOptions" />
          </div>
          <div class="chart-wrapper col-span-full">
            <h3 class="text-xl font-medium text-gray-700 mb-4">Graduation Trends</h3>
            <LineChart :chart-data="graduationTrendsData" :chart-options="chartOptions" />
          </div>
        </div>
      </div>
      <div v-else-if="pending" class="text-center text-gray-500 text-xl">Loading dashboard data...</div>
      <div v-else-if="error" class="text-center text-red-500 text-xl">Error loading dashboard data: {{ error.message }}</div>
    </ClientOnly>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import type { ChartData, ChartOptions } from 'chart.js';
import { useNuxtApp } from '#app';
// Add these imports to your <script setup> block
import BarChart from '~/components/Chart/BarChart.vue';
import PieChart from '~/components/Chart/PieChart.vue';
import DoughnutChart from '~/components/Chart/DoughnutChart.vue';
import LineChart from '~/components/Chart/LineChart.vue';

// Import components
import SummaryCard from '~/components/SummaryCard.vue';

definePageMeta({
  layout: 'admin',
  middleware: 'auth',
});

const { $api } = useNuxtApp();

interface DashboardData {
  total_houses: number;
  owned_houses: number;
  rented_houses: number;
  verified_houses_count: number;
  unverified_houses_count: number;
  houses_with_tenants: number;
  houses_without_tenants: number;
  timeseries_rent_start: { [year: string]: number };
  average_household_size: number | null;
  total_citizens: number;
  gender_distribution: Array<{ label: string; value: number }>;
  age_group_distribution: Array<{ label: string; value: number }>;
  verified_citizens_percentage: number;
  religion_distribution: Array<{ label: string; value: number }>;
  top_5_denominations: Array<{ label: string; value: number }>;
  top_5_occupations: Array<{ label: string; value: number }>;
  top_5_education_levels: Array<{ label: string; value: number }>;
  graduation_trends: { [year: string]: number };
}

const dashboardData = ref<DashboardData | null>(null);
const pending = ref(true);
const error = ref<Error | null>(null);

onMounted(async () => {
  try {
    const response = await $api.get('/reports/dashboard');
    dashboardData.value = response.data;
  } catch (e) {
    error.value = e as Error;
  } finally {
    pending.value = false;
  }
});

const chartOptions = ref<ChartOptions>({ 
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
    },
    tooltip: {
      mode: 'index',
      intersect: false,
    },
  },
});

// Computed properties for chart data
const houseOwnershipData = computed<ChartData<'pie'>>(() => {
  if (!dashboardData.value) return { labels: [], datasets: [] };
  const owned = dashboardData.value.owned_houses || 0;
  const rented = dashboardData.value.rented_houses || 0;
  return {
    labels: ['Owned Houses', 'Rented Houses'],
    datasets: [{
      data: [owned, rented],
      backgroundColor: ['#4CAF50', '#FFC107'],
    }]
  };
});

const houseTenantData = computed<ChartData<'doughnut'>>(() => {
  if (!dashboardData.value) return { labels: [], datasets: [] };
  const withTenants = dashboardData.value.houses_with_tenants || 0;
  const withoutTenants = dashboardData.value.houses_without_tenants || 0;
  return {
    labels: ['Houses with Tenants', 'Houses without Tenants'],
    datasets: [{
      data: [withTenants, withoutTenants],
      backgroundColor: ['#2196F3', '#F44336'],
    }]
  };
});

const rentStartTrendData = computed<ChartData<'line'>>(() => {
  if (!dashboardData.value || !dashboardData.value.timeseries_rent_start) return { labels: [], datasets: [] };
  const labels = Object.keys(dashboardData.value.timeseries_rent_start).sort();
  const data = labels.map(year => dashboardData.value.timeseries_rent_start[year] || 0);
  return {
    labels: labels,
    datasets: [{
      label: 'Awm tan kum',
      data: data,
      fill: false,
      borderColor: '#9C27B0',
      tension: 0.1
    }]
  };
});

const genderDistributionData = computed<ChartData<'pie'>>(() => {
  if (!dashboardData.value || !dashboardData.value.gender_distribution) return { labels: [], datasets: [] };
  const labels = dashboardData.value.gender_distribution.map(item => item.label);
  const data = dashboardData.value.gender_distribution.map(item => item.value);
  return {
    labels: labels,
    datasets: [{
      data: data,
      backgroundColor: ['#03A9F4', '#E91E63', '#607D8B'],
    }]
  };
});

const ageGroupData = computed<ChartData<'bar'>>(() => {
  if (!dashboardData.value || !dashboardData.value.age_group_distribution) return { labels: [], datasets: [] };
  const labels = dashboardData.value.age_group_distribution.map(item => item.label);
  const data = dashboardData.value.age_group_distribution.map(item => item.value);
  return {
    labels: labels,
    datasets: [{
      label: 'Number of Citizens',
      data: data,
      backgroundColor: ['#FF5722', '#FF9800', '#CDDC39', '#8BC34A'],
    }]
  };
});

const religionDistributionData = computed<ChartData<'pie'>>(() => {
  if (!dashboardData.value || !dashboardData.value.religion_distribution) return { labels: [], datasets: [] };
  const labels = dashboardData.value.religion_distribution.map(item => item.label);
  const data = dashboardData.value.religion_distribution.map(item => item.value);
  return {
    labels: labels,
    datasets: [{
      data: data,
      backgroundColor: ['#F44336', '#E91E63', '#9C27B0', '#673AB7', '#3F51B5', '#2196F3', '#03A9F4', '#00BCD4', '#009688', '#4CAF50'],
    }]
  };
});

const topDenominationsData = computed<ChartData<'bar'>>(() => {
  if (!dashboardData.value || !dashboardData.value.top_5_denominations) return { labels: [], datasets: [] };
  const labels = dashboardData.value.top_5_denominations.map(item => item.label);
  const data = dashboardData.value.top_5_denominations.map(item => item.value);
  return {
    labels: labels,
    datasets: [{
      label: 'Number of Citizens',
      data: data,
      backgroundColor: ['#FFEB3B'],
    }]
  };
});

const topOccupationsData = computed<ChartData<'bar'>>(() => {
  if (!dashboardData.value || !dashboardData.value.top_5_occupations) return { labels: [], datasets: [] };
  const labels = dashboardData.value.top_5_occupations.map(item => item.label);
  const data = dashboardData.value.top_5_occupations.map(item => item.value);
  return {
    labels: labels,
    datasets: [{
      label: 'Number of Citizens',
      data: data,
      backgroundColor: ['#795548'],
    }]
  };
});

const topEducationLevelsData = computed<ChartData<'bar'>>(() => {
  if (!dashboardData.value || !dashboardData.value.top_5_education_levels) return { labels: [], datasets: [] };
  const labels = dashboardData.value.top_5_education_levels.map(item => item.label);
  const data = dashboardData.value.top_5_education_levels.map(item => item.value);
  return {
    labels: labels,
    datasets: [{
      label: 'Number of Citizens',
      data: data,
      backgroundColor: ['#607D8B'],
    }]
  };
});

const graduationTrendsData = computed<ChartData<'line'>>(() => {
  if (!dashboardData.value || !dashboardData.value.graduation_trends) return { labels: [], datasets: [] };
  const labels = Object.keys(dashboardData.value.graduation_trends).sort();
  const data = labels.map(year => dashboardData.value.graduation_trends[year] || 0);
  return {
    labels: labels,
    datasets: [{
      label: 'Graduations',
      data: data,
      fill: false,
      borderColor: '#FF9800',
      tension: 0.1
    }]
  };
});

</script>

<style>
.page-container {
  max-width: 1600px;
  margin: 2rem auto;
  padding: 1rem;
  font-family: sans-serif;
}
h1, h2 {
  text-align: center;
  margin-bottom: 1rem;
}
.chart-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.chart-wrapper {
  position: relative;
  height: 400px;
  width: 100%;
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  background-color: #fff;
}
</style>
''