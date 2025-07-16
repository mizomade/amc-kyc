<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <div class="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow-xl">
      <h1 class="text-4xl font-extrabold text-gray-900 mb-8 text-center">Generate Certificate</h1>

      <!-- Person Search Section -->
      <div class="mb-8 p-6 border border-gray-200 rounded-lg bg-gray-50">
        <label for="person-search" class="block text-lg font-semibold text-gray-800 mb-2">Search Person</label>
        <input
          type="text"
          id="person-search"
          v-model="searchQuery"
          @input="debouncedSearchPersons"
          class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-500"
          placeholder="Search by name, EPIC, Aadhar..."
        />
        <ul v-if="searchResults.length" class="mt-3 border border-gray-300 rounded-md shadow-lg bg-white max-h-60 overflow-y-auto z-10 relative">
          <li
            v-for="person in searchResults"
            :key="person.id"
            @click="selectPerson(person.id)"
            class="px-4 py-3 cursor-pointer hover:bg-blue-50 transition duration-150 ease-in-out text-gray-800"
          >
            {{ person.name }}
          </li>
        </ul>
        <p v-if="selectedPersonName" class="mt-3 text-green-600 font-medium">Selected Person: {{ selectedPersonName }}</p>
      </div>

      <!-- Certificate Type Selection Section -->
      <div class="mb-8 p-6 border border-gray-200 rounded-lg bg-gray-50">
        <label for="certificate-type" class="block text-lg font-semibold text-gray-800 mb-2">Select Certificate Type</label>
        <select
          id="certificate-type"
          v-model="selectedCertificate"
          @change="generateForm"
          class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 text-gray-900"
        >
          <option :value="null" disabled>Please select a certificate type</option>
          <option v-for="cert in certificateTypes" :key="cert.id" :value="cert">{{ cert.name }}</option>
        </select>
      </div>

      <!-- Certificate Details Form Section -->
      <div v-if="selectedCertificate && selectedCertificate.variables && selectedCertificate.variables.variables" class="p-6 border border-gray-200 rounded-lg bg-gray-50">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">Certificate Details</h2>
        <form @submit.prevent="buildCertificate">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div v-for="(variable, index) in selectedCertificate.variables.variables" :key="index" class="relative">
              <label :for="variable.key" class="block text-sm font-medium text-gray-700 mb-1">
                {{ variable.name }}
                <span v-if="variable.required" class="text-red-500">*</span>
              </label>
              <input
                :type="variable.type"
                :id="variable.key"
                v-model="formValues[variable.variable]"
                :required="variable.required"
                class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 text-gray-900"
              />
            </div>
          </div>
          <div class="text-center">
            <button type="submit" class="px-8 py-3 bg-indigo-600 text-white rounded-lg shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition ease-in-out duration-150">
              Build Certificate
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useNuxtApp } from '#app';
import { form } from '#build/ui';

definePageMeta({
  layout: 'admin',
  middleware: 'auth',
});

const router = useRouter();
const { $api } = useNuxtApp();

const certificateTypes = ref([]);
const selectedCertificate = ref(null);
const formValues = ref({});
const selectedPersonName = ref('');

const searchQuery = ref('');
const searchResults = ref([]);
let searchTimeout = null;

onMounted(async () => {
  try {
    const response = await $api.get('/certificates/types/');
    certificateTypes.value = response.data;
  } catch (error) {
    console.error('Error fetching certificate types:', error);
  }
});

const debouncedSearchPersons = () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(async () => {
    if (searchQuery.value.length > 2) { // Only search if query is at least 3 characters
      try {
        const response = await $api.get(`/search/person/?name=${searchQuery.value}`);
        searchResults.value = response.data;
      } catch (error) {
        console.error('Error searching persons:', error);
        searchResults.value = [];
      }
    } else {
      searchResults.value = [];
    }
  }, 300); // 300ms debounce time
};

const selectPerson = async (personId) => {
  try {
    const response = await $api.get(`/person/${personId}`);
    const personData = response.data;

    // Populate formValues with person data
    formValues.value['person.id'] = personData.id;
    formValues.value['person.name'] = `${personData.first_name} ${personData.hnam_hming || ''}`.trim();
    formValues.value['person.father_name'] = personData.father_name?.father.first_name.value || '';
    formValues.value['person.permanent_address'] = personData.house_number || ''; 
    formValues.value['person.dob'] = personData.dob || '';
    formValues.value['person.place_of_birth'] = personData.place_of_birth || ''; 
    formValues.value['person.gender'] = personData.gender || '';
    formValues.value['veng.name'] = personData.veng_name || ''; // Assuming veng_name exists

    // Set selected person name for display
    selectedPersonName.value = formValues.value['person.name'];

    // Clear search results and query
    searchResults.value = [];
    searchQuery.value = '';

  } catch (error) {
    console.error('Error fetching person details:', error);
  }
};

const generateForm = () => {
  if (selectedCertificate.value) {
    // Preserve person data if already selected
    const currentPersonId = formValues.value['person.id'];
    const currentPersonName = formValues.value['person.name'];
    const currentPersonFatherName = formValues.value['person.father?.first_name?'] || '';
    const currentPersonPermanentAddress = formValues.value['person.permanent_address'];
    const currentPersonDob = formValues.value['person.dob'];
    const currentPersonPlaceOfBirth = formValues.value['person.place_of_birth'];
    const currentPersonGender = formValues.value['person.gender'];
    const currentVengName = formValues.value['veng.name'];

    formValues.value = {}; // Clear other form values

    if (currentPersonId) {
      formValues.value['person.id'] = currentPersonId;
      formValues.value['person.name'] = currentPersonName;
      formValues.value['person.father_name'] = currentPersonFatherName;
      formValues.value['person.permanent_address'] = currentPersonPermanentAddress;
      formValues.value['person.dob'] = currentPersonDob;
      formValues.value['person.place_of_birth'] = currentPersonPlaceOfBirth;
      formValues.value['person.gender'] = currentPersonGender;
      formValues.value['veng.name'] = currentVengName;
    }
  }
};

const buildCertificate = () => {
  if (!selectedCertificate.value) {
    alert('Please select a certificate type.');
    return;
  }

  if (!formValues.value['person.id']) {
    alert('Please select a person.');
    return;
  }

  // Client-side validation for required fields
  const requiredFields = selectedCertificate.value.variables.variables.filter(v => v.required);
  for (const field of requiredFields) {
    if (!formValues.value[field.variable]) {
      alert(`Please fill in the required field: ${field.name}`);
      return;
    }
  }

  router.push({
    name: 'admin-certificates-issue',
    query: {
      certificateTypeId: selectedCertificate.value.id,
      formValues: JSON.stringify(formValues.value)
    }
  });
};
</script>
