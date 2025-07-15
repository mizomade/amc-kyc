<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Issued Certificates</h1>
      <nuxt-link to="/admin/certificates/issue" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
        Issue New Certificate
      </nuxt-link>
    </div>
    <div class="bg-white shadow-md rounded my-6">
      <table class="min-w-full table-auto">
        <thead>
          <tr class="bg-gray-200 text-gray-600 uppercase text-sm leading-normal">
            <th class="py-3 px-6 text-left">Certificate No.</th>
            <th class="py-3 px-6 text-left">Person</th>
            <th class="py-3 px-6 text-center">Certificate Type</th>
            <th class="py-3 px-6 text-center">Issue Date</th>
            <th class="py-3 px-6 text-center">Actions</th>
          </tr>
        </thead>
        <tbody class="text-gray-600 text-sm font-light">
          <tr v-for="cert in certificates" :key="cert.id" class="border-b border-gray-200 hover:bg-gray-100">
            <td class="py-3 px-6 text-left whitespace-nowrap">{{ cert.certificate_number }}</td>
            <td class="py-3 px-6 text-left">{{ cert.person_first_name }}</td>
            <td class="py-3 px-6 text-center">{{ cert.certificate_type }}</td>
            <td class="py-3 px-6 text-center">{{ cert.issue_date }}</td>
            <td class="py-3 px-6 text-center">
              <div class="flex item-center justify-center">
                <div class="w-4 mr-2 transform hover:text-purple-500 hover:scale-110">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
const { $api } = useNuxtApp();

const certificates = ref([]);

definePageMeta({
  layout: 'admin',
  middleware: 'auth',
//   roles: ['admin'],
});

onMounted(async () => {
  try {
    const response = await $api.get('/certificates/issued/');
    certificates.value = response.data;
  } catch (error) {
    console.error('Error fetching issued certificates:', error);
  }
});
</script>
