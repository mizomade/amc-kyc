<template>
  <div class="container mx-auto p-4">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-extrabold text-gray-900">Issued Certificates</h1>
      <nuxt-link to="/admin/certificates/typeselection" class="px-6 py-3 bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition ease-in-out duration-150">
        Issue New Certificate
      </nuxt-link>
    </div>

    <div class="flex flex-col md:flex-row justify-between items-center mb-6 space-y-4 md:space-y-0 md:space-x-4">
      <div class="w-full md:w-1/3">
        <label for="search" class="sr-only">Search</label>
        <input type="text" id="search" v-model="searchQuery" @input="debouncedSearch" placeholder="Search by person or certificate number..." class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
      </div>
      <div class="w-full md:w-1/4">
        <label for="certificate-type-filter" class="sr-only">Filter by Type</label>
        <select id="certificate-type-filter" v-model="selectedCertificateType" @change="fetchCertificates" class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
          <option :value="null">All Certificate Types</option>
          <option v-for="type in certificateTypes" :key="type.id" :value="type.id">{{ type.name }}</option>
        </select>
      </div>
    </div>

    <div class="bg-white shadow-lg rounded-lg overflow-hidden py-6 px-4">
      <h3 class="text-lg font-semibold text-gray-800 p-4 text-center ">List of Issued Certificates</h3>
      <hr class="border-gray-200 mb-4">
      <table class="min-w-full leading-normal">
        <thead class="bg-red-100">
          <tr class="bg-white text-gray-600 uppercase text-sm font-semibold">
            <th class="py-3 px-6 text-left">Certificate No.</th>
            <th class="py-3 px-6 text-left">Person</th>
            <th class="py-3 px-6 text-center">Certificate Type</th>
            <th class="py-3 px-6 text-center">Issue Date</th>
            <th class="py-3 px-6 text-center">Actions</th>
          </tr>
        </thead>
        <tbody class="text-gray-700 text-sm">
          <tr v-for="cert in filteredCertificates" :key="cert.id" class="border-b border-gray-200 hover:bg-gray-50 transition duration-150 ease-in-out cursor-pointer" @click="goToDetails(cert.id)">
            <td class="py-4 px-6 whitespace-nowrap">{{ cert.certificate_number || 'N/A' }}</td>
            <td class="py-4 px-6 whitespace-nowrap">{{ cert.person_first_name }}</td>
            <td class="py-4 px-6 text-center">{{ cert.certificate_type }}</td>
            <td class="py-4 px-6 text-center">{{ cert.issue_date }}</td>
            <td class="py-4 px-6 text-center">
              <div class="flex items-center justify-center space-x-2">
                <button @click.stop="goToDetails(cert.id)" class="text-blue-600 hover:text-blue-900 transition duration-150 ease-in-out">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                    <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
                  </svg>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination (Placeholder) -->
    <div class="flex justify-center mt-6">
      <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
        <a href="#" class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
          <span class="sr-only">Previous</span>
          <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
        </a>
        <a href="#" aria-current="page" class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-blue-50 text-sm font-medium text-blue-600 hover:bg-blue-100">
          1
        </a>
        <a href="#" class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50">
          2
        </a>
        <a href="#" class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50">
          3
        </a>
        <a href="#" class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
          <span class="sr-only">Next</span>
          <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10l-3.293-3.293a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
          </svg>
        </a>
      </nav>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useNuxtApp } from '#app';
import { useRouter } from 'vue-router';

const { $api } = useNuxtApp();
const router = useRouter();

const certificates = ref([]);
const certificateTypes = ref([]);
const selectedCertificateType = ref(null);
const searchQuery = ref('');
let searchTimeout = null;

definePageMeta({
  layout: 'admin',
  middleware: 'auth',
});

const fetchCertificates = async () => {
  try {
    let url = '/certificates/issued/';
    if (selectedCertificateType.value) {
      url += `?certificate_type_id=${selectedCertificateType.value}`;
    }
    const response = await $api.get(url);
    certificates.value = response.data;
  } catch (error) {
    console.error('Error fetching issued certificates:', error);
  }
};

const fetchCertificateTypes = async () => {
  try {
    const response = await $api.get('/certificates/types/');
    certificateTypes.value = response.data;
  } catch (error) {
    console.error('Error fetching certificate types:', error);
  }
};

onMounted(() => {
  fetchCertificateTypes();
  fetchCertificates();
});

const filteredCertificates = computed(() => {
  if (!searchQuery.value) {
    return certificates.value;
  }
  const query = searchQuery.value.toLowerCase();
  return certificates.value.filter(cert => 
    cert.person_first_name.toLowerCase().includes(query) ||
    cert.certificate_number.toLowerCase().includes(query)
  );
});

const debouncedSearch = () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    // No need to re-fetch from API for search, as it's client-side filtered
  }, 300);
};

const goToDetails = (id) => {
  router.push(`/admin/certificates/details/${id}`);
};
</script>
