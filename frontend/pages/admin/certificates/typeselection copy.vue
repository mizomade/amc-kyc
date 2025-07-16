<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Select Certificate Type</h1>
    <div class="mb-4">
      <label for="certificate-type" class="block text-sm font-medium text-gray-700">Certificate Type</label>
      <select id="certificate-type" v-model="selectedCertificate" @change="generateForm" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md">
        <option :value="null" disabled>Please select a certificate type</option>
        <option v-for="cert in certificateTypes" :key="cert.id" :value="cert">{{ cert.name }}</option>
      </select>
    </div>
 
    <div v-if="selectedCertificate && selectedCertificate.variables" class="mt-8">
      <h2 class="text-xl font-semibold mb-4">Certificate Details</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div v-for="(variable, index) in selectedCertificate.variables.variables" :key="index" class="mb-4">
          <label :for="variable.key" class="block text-sm font-medium text-gray-700">{{ variable.name }}</label>
          <input :type="variable.type" :id="variable.key" v-model="formValues[variable.variable]" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md">
        </div>
      </div>
      <div class="mt-6">
        <button @click="buildCertificate" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded">
          Build Certificate
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useNuxtApp } from '#app';

const router = useRouter();
const { $api } = useNuxtApp();

const certificateTypes = ref([]);
const selectedCertificate = ref(null);
const formValues = ref({});

onMounted(async () => {
  try {
    const response = await $api.get('/certificates/types/');
    certificateTypes.value = response.data;
  } catch (error) {
    console.error('Error fetching certificate types:', error);
  }
});

const generateForm = () => {
  if (selectedCertificate.value) {
    formValues.value = {};
    // You would typically fetch person data here based on some identifier
    // For now, we'll pre-fill with some dummy data
    // formValues.value = {
    //   'person.name': 'John Doe',
    //   'person.dob': '1990-01-01',
    //   'person.place_of_birth': 'Someplace',
    //   'veng.name': 'Someville'
    // };
  }
};

const buildCertificate = () => {
  if (selectedCertificate.value) {
    router.push({
      name: 'admin-certificates-issue',
      query: {
        template: JSON.stringify(selectedCertificate.value.template),
        ...formValues.value
      }
    });
  }
};
</script>
