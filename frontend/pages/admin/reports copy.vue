<template>
  <div class="min-h-screen bg-gray-50 p-4 sm:p-6 lg:p-8">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-3xl font-bold tracking-tight text-gray-900 mb-8">Reports Dashboard</h1>

      <!-- Report Navigation -->
      <div class="bg-white rounded-lg shadow-sm mb-8">
        <nav class="flex space-x-1 p-1.5" aria-label="Tabs">
          <button @click="setActiveReport('summary')" :class="[activeReport === 'summary' ? 'bg-blue-600 text-white shadow-md' : 'text-gray-600 hover:bg-gray-200', 'px-4 py-2.5 font-medium text-sm rounded-md transition-all duration-200']">
            <Icon name="heroicons:chart-pie" class="w-5 h-5 mr-2 inline-block" />
            Summary
          </button>
          <button @click="setActiveReport('persons')" :class="[activeReport === 'persons' ? 'bg-blue-600 text-white shadow-md' : 'text-gray-600 hover:bg-gray-200', 'px-4 py-2.5 font-medium text-sm rounded-md transition-all duration-200']">
            <Icon name="heroicons:users" class="w-5 h-5 mr-2 inline-block" />
            Persons Report
          </button>
          <button @click="setActiveReport('houses')" :class="[activeReport === 'houses' ? 'bg-blue-600 text-white shadow-md' : 'text-gray-600 hover:bg-gray-200', 'px-4 py-2.5 font-medium text-sm rounded-md transition-all duration-200']">
            <Icon name="heroicons:home-modern" class="w-5 h-5 mr-2 inline-block" />
            Houses Report
          </button>
        </nav>
      </div>

      <!-- Report Content -->
      <div class="bg-white rounded-lg shadow-lg p-6 min-h-[500px]">
        <!-- Summary Report -->
        <div v-if="activeReport === 'summary'">
          <h2 class="text-2xl font-semibold text-gray-800 mb-6">Data Summary</h2>
          <div v-if="isLoading" class="flex justify-center items-center h-64">
            <Icon name="svg-spinners:3-dots-fade" class="w-12 h-12 text-blue-600" />
          </div>
          <div v-else-if="summaryData" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <div class="bg-blue-50 border-l-4 border-blue-500 p-6 rounded-lg">
              <h3 class="text-lg font-medium text-gray-700">Total Persons</h3>
              <p class="text-4xl font-bold text-blue-900 mt-2">{{ summaryData.persons }}</p>
            </div>
            <div class="bg-green-50 border-l-4 border-green-500 p-6 rounded-lg">
              <h3 class="text-lg font-medium text-gray-700">Total Houses</h3>
              <p class="text-4xl font-bold text-green-900 mt-2">{{ summaryData.houses }}</p>
            </div>
            <div class="bg-indigo-50 border-l-4 border-indigo-500 p-6 rounded-lg">
              <h3 class="text-lg font-medium text-gray-700">Total Families</h3>
              <p class="text-4xl font-bold text-indigo-900 mt-2">{{ summaryData.families }}</p>
            </div>
          </div>
        </div>

        <!-- Persons Report -->
        <div v-if="activeReport === 'persons'">
          <h2 class="text-2xl font-semibold text-gray-800 mb-6">Persons Report</h2>
          <!-- Filters -->
          <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 items-start">
            <!-- Geography -->
            <div>
              <h3 class="font-medium text-gray-800 mb-2">Geography</h3>
              <label for="veng" class="block text-sm font-medium text-gray-700">Veng</label>
              <select id="veng" v-model="personFilters.veng_id" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md">
                <option value="">All</option>
                <!-- Populate with API data -->
              </select>
              <label for="street" class="block text-sm font-medium text-gray-700 mt-2">Street</label>
              <input type="text" id="street" v-model="personFilters.street" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm" placeholder="Street name">
            </div>

            <!-- Demographics -->
            <div>
              <h3 class="font-medium text-gray-800 mb-2">Demographics</h3>
              <label for="gender" class="block text-sm font-medium text-gray-700">Gender</label>
              <select id="gender" v-model="personFilters.gender" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md">
                <option value="">All</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
              <label for="age_group" class="block text-sm font-medium text-gray-700 mt-2">Age Group</label>
              <div class="flex space-x-2">
                <input type="number" v-model.number="personFilters.min_age" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm sm:text-sm" placeholder="Min">
                <input type="number" v-model.number="personFilters.max_age" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm sm:text-sm" placeholder="Max">
              </div>
              <label for="marital_status" class="block text-sm font-medium text-gray-700 mt-2">Marital Status</label>
              <select id="marital_status" v-model="personFilters.marital_status" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md">
                <option value="">All</option>
                <!-- Populate with API data or fixed options -->
              </select>
              <label for="blood_group" class="block text-sm font-medium text-gray-700 mt-2">Blood Group</label>
              <select id="blood_group" v-model="personFilters.blood_group" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md">
                <option value="">All</option>
                <!-- Populate with API data or fixed options -->
              </select>
            </div>

            <!-- Religion -->
            <div>
              <h3 class="font-medium text-gray-800 mb-2">Religion</h3>
              <label for="religion" class="block text-sm font-medium text-gray-700">Religion</label>
              <select id="religion" v-model="personFilters.religion_id" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md">
                <option value="">All</option>
                <!-- Populate with API data -->
              </select>
              <label for="denomination" class="block text-sm font-medium text-gray-700 mt-2">Denomination</label>
              <select id="denomination" v-model="personFilters.denomination_id" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md">
                <option value="">All</option>
                <!-- Populate with API data -->
              </select>
            </div>

            <!-- Other -->
            <div>
              <h3 class="font-medium text-gray-800 mb-2">Other</h3>
              <label for="education" class="block text-sm font-medium text-gray-700">Education</label>
              <select id="education" v-model="personFilters.education_id" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md">
                <option value="">All</option>
                <!-- Populate with API data -->
              </select>
              <label for="occupation" class="block text-sm font-medium text-gray-700 mt-2">Occupation</label>
              <select id="occupation" v-model="personFilters.occupation_id" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md">
                <option value="">All</option>
                <!-- Populate with API data -->
              </select>
              <label class="block text-sm font-medium text-gray-700 mt-2">Verification Status</label>
              <select v-model="personFilters.is_verified" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md">
                <option :value="null">All</option>
                <option :value="true">Verified</option>
                <option :value="false">Not Verified</option>
              </select>
            </div>

            <div class="col-span-full flex justify-end items-center mt-4">
              <button @click="fetchPersonsReport" class="bg-blue-600 text-white px-6 py-2.5 rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 flex items-center">
                <Icon name="heroicons:magnifying-glass" class="w-5 h-5 mr-2" />
                Generate Report
              </button>
            </div>
          </div>
          <!-- Table -->
          <div v-if="isLoading" class="flex justify-center items-center h-64">
            <Icon name="svg-spinners:3-dots-fade" class="w-12 h-12 text-blue-600" />
          </div>
          <div v-else-if="personsReportData.length > 0" class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Gender</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">DOB</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Qualifications</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Occupations</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="person in personsReportData" :key="person.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ person.first_name }} {{ person.hnam_hming }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ person.gender }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ person.dob }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ person.qualifications.length }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ person.occupations.length }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="text-center py-16">
            <Icon name="heroicons:document-magnifying-glass" class="w-12 h-12 mx-auto text-gray-400" />
            <h3 class="mt-2 text-sm font-medium text-gray-900">No Data</h3>
            <p class="mt-1 text-sm text-gray-500">Adjust your filters or generate a new report.</p>
          </div>
        </div>

        <!-- Houses Report -->
        <div v-if="activeReport === 'houses'">
          <h2 class="text-2xl font-semibold text-gray-800 mb-6">Houses Report</h2>
          <!-- Filters -->
          <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-6 flex items-center gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Verification Status</label>
              <fieldset class="mt-2">
                <div class="flex items-center space-x-4">
                  <div class="flex items-center">
                    <input id="verified_all" v-model="houseFilters.is_verified" :value="null" type="radio" class="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300">
                    <label for="verified_all" class="ml-2 block text-sm text-gray-900">All</label>
                  </div>
                  <div class="flex items-center">
                    <input id="verified_true" v-model="houseFilters.is_verified" :value="true" type="radio" class="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300">
                    <label for="verified_true" class="ml-2 block text-sm text-gray-900">Verified</label>
                  </div>
                  <div class="flex items-center">
                    <input id="verified_false" v-model="houseFilters.is_verified" :value="false" type="radio" class="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300">
                    <label for="verified_false" class="ml-2 block text-sm text-gray-900">Not Verified</label>
                  </div>
                </div>
              </fieldset>
            </div>
            <div class="self-end">
              <button @click="fetchHousesReport" class="bg-blue-600 text-white px-4 py-2 rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 flex items-center">
                <Icon name="heroicons:magnifying-glass" class="w-5 h-5 mr-2" />
                Generate
              </button>
            </div>
          </div>
          <!-- Table -->
          <div v-if="isLoading" class="flex justify-center items-center h-64">
            <Icon name="svg-spinners:3-dots-fade" class="w-12 h-12 text-blue-600" />
          </div>
          <div v-else-if="housesReportData.length > 0" class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">House No.</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Veng</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Owner</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tenants</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="house in housesReportData" :key="house.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ house.house_number }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ house.veng }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <span :class="[house.is_verified ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800', 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium']">
                      {{ house.is_verified ? 'Verified' : 'Not Verified' }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ house.owner ? `${house.owner.first_name} ${house.owner.hnam_hming}` : 'N/A' }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ house.tenants.length }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="text-center py-16">
            <Icon name="heroicons:document-magnifying-glass" class="w-12 h-12 mx-auto text-gray-400" />
            <h3 class="mt-2 text-sm font-medium text-gray-900">No Data</h3>
            <p class="mt-1 text-sm text-gray-500">Adjust your filters or generate a new report.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
import { useNuxtApp } from '#app';

const { $api } = useNuxtApp()

definePageMeta({
  layout: 'admin',
  middleware: 'auth',
});

const activeReport = ref('summary');
const isLoading = ref(false);

// Data stores
const summaryData = ref(null);
const personsReportData = ref([]);
const housesReportData = ref([]);
const vengs = ref([]);
const religions = ref([]);
const denominations = ref([]);
const educations = ref([]);
const occupations = ref([]);

// Filter models
const personFilters = reactive({
  gender: '',
  min_age: null,
  max_age: null,
  street: '',
  marital_status: '',
  blood_group: '',
  religion_id: '',
  denomination_id: '',
  education_id: '',
  occupation_id: '',
  is_verified: null,
  veng_id: ''
});

const houseFilters = reactive({
  is_verified: null, // null for all, true for verified, false for not
});

const setActiveReport = (reportName) => {
  activeReport.value = reportName;
  // Reset data when switching tabs
  personsReportData.value = [];
  housesReportData.value = [];
  // Fetch summary data if that tab is selected
  if (reportName === 'summary' && !summaryData.value) {
    fetchSummaryReport();
  }
};

const fetchSummaryReport = async () => {
  isLoading.value = true;
  try {
    const response = await $api.get('/reports/summary');
    summaryData.value = response.data;
  } catch (error) {
    console.error('Failed to fetch summary report:', error);
    // Handle error display to user
  } finally {
    isLoading.value = false;
  }
};

const fetchPersonsReport = async () => {
  isLoading.value = true;
  personsReportData.value = [];
  try {
    const params = new URLSearchParams();
    Object.entries(personFilters).forEach(([key, value]) => {
      if (value !== null && value !== '') {
        params.append(key, value);
      }
    });
    
    const response = await $api.get(`/reports/persons?${params.toString()}`);
    personsReportData.value = response.data;
  } catch (error)
{
    console.error('Failed to fetch persons report:', error);
  } finally {
    isLoading.value = false;
  }
};

const fetchHousesReport = async () => {
  isLoading.value = true;
  housesReportData.value = [];
  try {
    const params = new URLSearchParams();
    if (houseFilters.is_verified !== null) {
      params.append('is_verified', houseFilters.is_verified);
    }

    const response = await $api.get(`/reports/houses?${params.toString()}`);
    housesReportData.value = response.data;
  } catch (error) {
    console.error('Failed to fetch houses report:', error);
  } finally {
    isLoading.value = false;
  }
};

const fetchDropdownData = async () => {
  try {
    const [vengRes, religionRes, denominationRes, educationRes, occupationRes] = await Promise.all([
      $api.get('/veng/'),
      $api.get('/religion/'),
      $api.get('/denomination/'),
      $api.get('/qualifications/'),
      $api.get('/occupations/')
    ]);
    vengs.value = vengRes.data;
    religions.value = religionRes.data;
    denominations.value = denominationRes.data;
    educations.value = educationRes.data;
    occupations.value = occupationRes.data;
  } catch (error) {
    console.error('Failed to fetch dropdown data:', error);
  }
};

// Fetch initial summary report on component mount
onMounted(() => {
  fetchSummaryReport();
  fetchDropdownData();
});
</script>

<style scoped>
/* Using Tailwind CSS utility classes, so limited custom CSS is needed. */
/* Minor tweaks for better form element alignment if necessary */
.self-end {
  align-self: flex-end;
}
</style>
