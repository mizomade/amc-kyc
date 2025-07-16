<template>
  <div class="min-h-screen bg-gray-50 p-4 sm:p-6 lg:p-8">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-3xl font-extrabold tracking-tight text-gray-900 mb-8">Dashboard Overview</h1>

      <div v-if="isLoading" class="flex justify-center items-center h-64">
        <Icon name="svg-spinners:3-dots-fade" class="w-12 h-12 text-blue-600" />
      </div>

      <div v-else-if="dashboardData" class="space-y-8">
        <!-- Section: Key Metrics -->
        <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="bg-gradient-to-r from-blue-500 to-blue-600 text-white p-6 rounded-xl shadow-lg transform hover:scale-105 transition duration-300">
            <h3 class="text-lg font-semibold mb-2">Total Houses</h3>
            <p class="text-4xl font-bold">{{ dashboardData.total_houses }}</p>
          </div>
          <div class="bg-gradient-to-r from-green-500 to-green-600 text-white p-6 rounded-xl shadow-lg transform hover:scale-105 transition duration-300">
            <h3 class="text-lg font-semibold mb-2">Total Citizens</h3>
            <p class="text-4xl font-bold">{{ dashboardData.total_citizens }}</p>
          </div>
          <div class="bg-gradient-to-r from-purple-500 to-purple-600 text-white p-6 rounded-xl shadow-lg transform hover:scale-105 transition duration-300">
            <h3 class="text-lg font-semibold mb-2">Verified Citizens</h3>
            <p class="text-4xl font-bold">{{ dashboardData.verified_citizens_percentage }}%</p>
          </div>
          <div class="bg-gradient-to-r from-yellow-500 to-yellow-600 text-white p-6 rounded-xl shadow-lg transform hover:scale-105 transition duration-300">
            <h3 class="text-lg font-semibold mb-2">Avg. Household Size</h3>
            <p class="text-4xl font-bold">{{ dashboardData.average_household_size }}</p>
          </div>
        </section>

        <!-- Section: House Statistics Charts -->
        <section class="bg-white p-6 rounded-xl shadow-lg">
          <h2 class="text-2xl font-bold text-gray-800 mb-6">House Statistics</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div class="chart-container">
              <h3 class="text-lg font-semibold text-gray-700 mb-4">Owned vs Rented Houses</h3>
              <canvas id="ownedRentedChart"></canvas>
            </div>
            <div class="chart-container">
              <h3 class="text-lg font-semibold text-gray-700 mb-4">Verified vs Unverified Houses</h3>
              <canvas id="verifiedUnverifiedHousesChart"></canvas>
            </div>
            <div class="chart-container">
              <h3 class="text-lg font-semibold text-gray-700 mb-4">Houses with/without Tenants</h3>
              <canvas id="housesTenantStatusChart"></canvas>
            </div>
          </div>
          <div class="mt-8 chart-container lg:col-span-3">
            <h3 class="text-lg font-semibold text-gray-700 mb-4">House Rent Start Dates Over Time</h3>
            <canvas id="rentStartTimeseriesChart"></canvas>
          </div>
        </section>

        <!-- Section: Citizen Statistics Charts -->
        <section class="bg-white p-6 rounded-xl shadow-lg">
          <h2 class="text-2xl font-bold text-gray-800 mb-6">Citizen Statistics</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="chart-container">
              <h3 class="text-lg font-semibold text-gray-700 mb-4">Gender Distribution</h3>
              <canvas id="genderDistributionChart"></canvas>
            </div>
            <div class="chart-container">
              <h3 class="text-lg font-semibold text-gray-700 mb-4">Age Group Breakdown</h3>
              <canvas id="ageGroupChart"></canvas>
            </div>
          </div>
        </section>

        <!-- Section: Religion & Demographics Charts -->
        <section class="bg-white p-6 rounded-xl shadow-lg">
          <h2 class="text-2xl font-bold text-gray-800 mb-6">Religion & Demographics</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="chart-container">
              <h3 class="text-lg font-semibold text-gray-700 mb-4">Religion Distribution</h3>
              <canvas id="religionDistributionChart"></canvas>
            </div>
            <div class="chart-container">
              <h3 class="text-lg font-semibold text-gray-700 mb-4">Top 5 Denominations</h3>
              <canvas id="topDenominationsChart"></canvas>
            </div>
          </div>
        </section>

        <!-- Section: Education & Occupation Charts -->
        <section class="bg-white p-6 rounded-xl shadow-lg">
          <h2 class="text-2xl font-bold text-gray-800 mb-6">Education & Occupation</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="chart-container">
              <h3 class="text-lg font-semibold text-gray-700 mb-4">Top 5 Occupations</h3>
              <canvas id="topOccupationsChart"></canvas>
            </div>
            <div class="chart-container">
              <h3 class="text-lg font-semibold text-gray-700 mb-4">Top 5 Education Levels</h3>
              <canvas id="topEducationLevelsChart"></canvas>
            </div>
          </div>
          <div class="mt-8 chart-container lg:col-span-2">
            <h3 class="text-lg font-semibold text-gray-700 mb-4">Graduation Trends by Year</h3>
            <canvas id="graduationTrendsChart"></canvas>
          </div>
        </section>
      </div>

      <div v-else class="text-center py-16">
        <p class="text-gray-500 text-lg">No dashboard data available.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, watch } from 'vue';
import { useNuxtApp } from '#app';
import { Chart, registerables } from 'chart.js';


Chart.register(...registerables);

const { $api } = useNuxtApp();

definePageMeta({
  layout: 'admin',
  middleware: 'auth',
});

const dashboardData = ref(null);
const isLoading = ref(true);

// Chart data and options refs
const ownedRentedChartData = ref({ labels: [], datasets: [] });
const verifiedUnverifiedHousesChartData = ref({ labels: [], datasets: [] });
const housesTenantStatusChartData = ref({ labels: [], datasets: [] });
const rentStartTimeseriesChartData = ref({ labels: [], datasets: [] });
const genderDistributionChartData = ref({ labels: [], datasets: [] });
const ageGroupChartData = ref({ labels: [], datasets: [] });
const religionDistributionChartData = ref({ labels: [], datasets: [] });
const topDenominationsChartData = ref({ labels: [], datasets: [] });
const topOccupationsChartData = ref({ labels: [], datasets: [] });
const topEducationLevelsChartData = ref({ labels: [], datasets: [] });
const graduationTrendsChartData = ref({ labels: [], datasets: [] });

const defaultChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: false,
    },
  },
};

const fetchDashboardData = async () => {
  isLoading.value = true;
  try {
    const response = await $api.get('/reports/dashboard');
    dashboardData.value = response.data;
  } catch (error) {
    console.error('Failed to fetch dashboard data:', error);
  } finally {
    isLoading.value = false;
  }
};

const updateChartData = () => {
  if (!dashboardData.value) return;

  const data = dashboardData.value;

  // House Stats Charts
  ownedRentedChartData.value = {
    labels: ['Owned', 'Rented'],
    datasets: [
      {
        backgroundColor: ['#42A5F5', '#FFA726'],
        data: [data.owned_houses, data.rented_houses],
      },
    ],
  };

  verifiedUnverifiedHousesChartData.value = {
    labels: ['Verified', 'Unverified'],
    datasets: [
      {
        backgroundColor: ['#66BB6A', '#EF5350'],
        data: [data.verified_houses_count, data.unverified_houses_count],
      },
    ],
  };

  housesTenantStatusChartData.value = {
    labels: ['With Tenants', 'Without Tenants'],
    datasets: [
      {
        backgroundColor: ['#AB47BC', '#7E57C2'],
        data: [data.houses_with_tenants, data.houses_without_tenants],
      },
    ],
  };

  rentStartTimeseriesChartData.value = {
    labels: Object.keys(data.timeseries_rent_start),
    datasets: [
      {
        label: 'Houses Established',
        backgroundColor: '#26A69A',
        borderColor: '#26A69A',
        data: Object.values(data.timeseries_rent_start),
        fill: false,
      },
    ],
  };

  // Citizen Stats Charts
  genderDistributionChartData.value = {
    labels: ['Male', 'Female', 'Other'],
    datasets: [
      {
        backgroundColor: ['#42A5F5', '#FF6384', '#FFCE56'],
        data: [data.male_citizens, data.female_citizens, data.other_gender_citizens],
      },
    ],
  };

  ageGroupChartData.value = {
    labels: ['0-18', '18-35', '35-60', '60+'],
    datasets: [
      {
        label: 'Number of Citizens',
        backgroundColor: '#7E57C2',
        data: [data.age_group_0_18, data.age_group_18_35, data.age_group_35_60, data.age_60_plus],
      },
    ],
  };

  // Religion Charts
  religionDistributionChartData.value = {
    labels: data.religion_distribution.map(item => item.label),
    datasets: [
      {
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9900'],
        data: data.religion_distribution.map(item => item.value),
      },
    ],
  };

  topDenominationsChartData.value = {
    labels: data.top_5_denominations.map(item => item.label),
    datasets: [
      {
        label: 'Number of People',
        backgroundColor: '#FF9900',
        data: data.top_5_denominations.map(item => item.value),
      },
    ],
  };

  // Education/Occupation Charts
  topOccupationsChartData.value = {
    labels: data.top_5_occupations.map(item => item.label),
    datasets: [
      {
        label: 'Number of People',
        backgroundColor: '#4BC0C0',
        data: data.top_5_occupations.map(item => item.value),
      },
    ],
  };

  topEducationLevelsChartData.value = {
    labels: data.top_5_education_levels.map(item => item.label),
    datasets: [
      {
        label: 'Number of People',
        backgroundColor: '#9966FF',
        data: data.top_5_education_levels.map(item => item.value),
      },
    ],
  };

  graduationTrendsChartData.value = {
    labels: Object.keys(data.graduation_trends),
    datasets: [
      {
        label: 'Graduations',
        backgroundColor: '#36A2EB',
        borderColor: '#36A2EB',
        data: Object.values(data.graduation_trends),
        fill: false,
      },
    ],
  };
};

watch(dashboardData, (newValue) => {
  if (newValue) {
    initCharts();
  }
});

let ownedRentedChart = null;
let verifiedUnverifiedHousesChart = null;
let housesTenantStatusChart = null;
let rentStartTimeseriesChart = null;
let genderDistributionChart = null;
let ageGroupChart = null;
let religionDistributionChart = null;
let topDenominationsChart = null;
let topOccupationsChart = null;
let topEducationLevelsChart = null;
let graduationTrendsChart = null;

const initCharts = () => {
  // House Stats Charts
  const ownedRentedCtx = document.getElementById('ownedRentedChart');
  if (ownedRentedCtx) {
    if (ownedRentedChart) ownedRentedChart.destroy();
    ownedRentedChart = new Chart(ownedRentedCtx, {
      type: 'pie',
      data: ownedRentedChartData.value,
      options: defaultChartOptions,
    });
  }

  const verifiedUnverifiedHousesCtx = document.getElementById('verifiedUnverifiedHousesChart');
  if (verifiedUnverifiedHousesCtx) {
    if (verifiedUnverifiedHousesChart) verifiedUnverifiedHousesChart.destroy();
    verifiedUnverifiedHousesChart = new Chart(verifiedUnverifiedHousesCtx, {
      type: 'pie',
      data: verifiedUnverifiedHousesChartData.value,
      options: defaultChartOptions,
    });
  }

  const housesTenantStatusCtx = document.getElementById('housesTenantStatusChart');
  if (housesTenantStatusCtx) {
    if (housesTenantStatusChart) housesTenantStatusChart.destroy();
    housesTenantStatusChart = new Chart(housesTenantStatusCtx, {
      type: 'pie',
      data: housesTenantStatusChartData.value,
      options: defaultChartOptions,
    });
  }

  const rentStartTimeseriesCtx = document.getElementById('rentStartTimeseriesChart');
  if (rentStartTimeseriesCtx) {
    if (rentStartTimeseriesChart) rentStartTimeseriesChart.destroy();
    rentStartTimeseriesChart = new Chart(rentStartTimeseriesCtx, {
      type: 'line',
      data: rentStartTimeseriesChartData.value,
      options: {
        ...defaultChartOptions,
        scales: {
          x: {
            type: 'category',
            title: {
              display: true,
              text: 'Year',
            },
          },
          y: {
            title: {
              display: true,
              text: 'Number of Houses',
            },
          },
        },
      },
    });
  }

  // Citizen Stats Charts
  const genderDistributionCtx = document.getElementById('genderDistributionChart');
  if (genderDistributionCtx) {
    if (genderDistributionChart) genderDistributionChart.destroy();
    genderDistributionChart = new Chart(genderDistributionCtx, {
      type: 'pie',
      data: genderDistributionChartData.value,
      options: defaultChartOptions,
    });
  }

  const ageGroupCtx = document.getElementById('ageGroupChart');
  if (ageGroupCtx) {
    if (ageGroupChart) ageGroupChart.destroy();
    ageGroupChart = new Chart(ageGroupCtx, {
      type: 'bar',
      data: ageGroupChartData.value,
      options: {
        ...defaultChartOptions,
        scales: {
          x: {
            title: {
              display: true,
              text: 'Age Group',
            },
          },
          y: {
            title: {
              display: true,
              text: 'Number of Citizens',
            },
          },
        },
      },
    });
  }

  // Religion Charts
  const religionDistributionCtx = document.getElementById('religionDistributionChart');
  if (religionDistributionCtx) {
    if (religionDistributionChart) religionDistributionChart.destroy();
    religionDistributionChart = new Chart(religionDistributionCtx, {
      type: 'pie',
      data: religionDistributionChartData.value,
      options: defaultChartOptions,
    });
  }

  const topDenominationsCtx = document.getElementById('topDenominationsChart');
  if (topDenominationsCtx) {
    if (topDenominationsChart) topDenominationsChart.destroy();
    topDenominationsChart = new Chart(topDenominationsCtx, {
      type: 'bar',
      data: topDenominationsChartData.value,
      options: {
        ...defaultChartOptions,
        scales: {
          x: {
            title: {
              display: true,
              text: 'Denomination',
            },
          },
          y: {
            title: {
              display: true,
              text: 'Number of People',
            },
          },
        },
      },
    });
  }

  // Education/Occupation Charts
  const topOccupationsCtx = document.getElementById('topOccupationsChart');
  if (topOccupationsCtx) {
    if (topOccupationsChart) topOccupationsChart.destroy();
    topOccupationsChart = new Chart(topOccupationsCtx, {
      type: 'bar',
      data: topOccupationsChartData.value,
      options: {
        ...defaultChartOptions,
        scales: {
          x: {
            title: {
              display: true,
              text: 'Occupation',
            },
          },
          y: {
            title: {
              display: true,
              text: 'Number of People',
            },
          },
        },
      },
    });
  }

  const topEducationLevelsCtx = document.getElementById('topEducationLevelsChart');
  if (topEducationLevelsCtx) {
    if (topEducationLevelsChart) topEducationLevelsChart.destroy();
    topEducationLevelsChart = new Chart(topEducationLevelsCtx, {
      type: 'bar',
      data: topEducationLevelsChartData.value,
      options: {
        ...defaultChartOptions,
        scales: {
          x: {
            title: {
              display: true,
              text: 'Education Level',
            },
          },
          y: {
            title: {
              display: true,
              text: 'Number of People',
            },
          },
        },
      },
    });
  }

  const graduationTrendsCtx = document.getElementById('graduationTrendsChart');
  if (graduationTrendsCtx) {
    if (graduationTrendsChart) graduationTrendsChart.destroy();
    graduationTrendsChart = new Chart(graduationTrendsCtx, {
      type: 'line',
      data: graduationTrendsChartData.value,
      options: {
        ...defaultChartOptions,
        scales: {
          x: {
            type: 'category',
            title: {
              display: true,
              text: 'Year',
            },
          },
          y: {
            title: {
              display: true,
              text: 'Number of Graduations',
            },
          },
        },
      },
    });
  }
};

const resizeCharts = () => {
  ownedRentedChart?.resize();
  verifiedUnverifiedHousesChart?.resize();
  housesTenantStatusChart?.resize();
  rentStartTimeseriesChart?.resize();
  genderDistributionChart?.resize();
  ageGroupChart?.resize();
  religionDistributionChart?.resize();
  topDenominationsChart?.resize();
  topOccupationsChart?.resize();
  topEducationLevelsChart?.resize();
  graduationTrendsChart?.resize();
};

onMounted(() => {
  fetchDashboardData();
  window.addEventListener('resize', resizeCharts);
});

onUnmounted(() => {
  window.removeEventListener('resize', resizeCharts);
  ownedRentedChart?.destroy();
  verifiedUnverifiedHousesChart?.destroy();
  housesTenantStatusChart?.destroy();
  rentStartTimeseriesChart?.destroy();
  genderDistributionChart?.destroy();
  ageGroupChart?.destroy();
  religionDistributionChart?.destroy();
  topDenominationsChart?.destroy();
  topOccupationsChart?.destroy();
  topEducationLevelsChart?.destroy();
  graduationTrendsChart?.destroy();
});
</script>

<style scoped>
/* No custom styles needed, Tailwind handles everything */
</style>
