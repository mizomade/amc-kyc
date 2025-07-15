<template>
  <form @submit.prevent="submitForm" class="space-y-6">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <label for="education_id" class="block text-sm font-medium text-gray-700">Education</label>
        <select id="education_id" v-model="qualificationData.education_id"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
          <option v-for="education in educations" :key="education.id" :value="education.id">{{ education.name }}</option>
        </select>
      </div>
      <div>
        <label for="year_of_passing" class="block text-sm font-medium text-gray-700">Year of Passing</label>
        <input type="number" id="year_of_passing" v-model="qualificationData.year_of_passing"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
      </div>
      <div>
        <label for="institution_name" class="block text-sm font-medium text-gray-700">Institution Name</label>
        <input type="text" id="institution_name" v-model="qualificationData.institution_name"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
      </div>
      <div>
        <label for="grade_or_marks" class="block text-sm font-medium text-gray-700">Grade/Marks</label>
        <input type="text" id="grade_or_marks" v-model="qualificationData.grade_or_marks"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
      </div>
      <div>
        <label for="certificate_number" class="block text-sm font-medium text-gray-700">Certificate Number</label>
        <input type="text" id="certificate_number" v-model="qualificationData.certificate_number"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
      </div>
      <div>
        <label for="remarks" class="block text-sm font-medium text-gray-700">Remarks</label>
        <input type="text" id="remarks" v-model="qualificationData.remarks"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
      </div>
    </div>
    <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
      <button type="submit" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm">
        Save
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const emit = defineEmits(['submit']);

const educations = ref([]);
const qualificationData = ref({
  education_id: null,
  year_of_passing: null,
  institution_name: '',
  grade_or_marks: '',
  certificate_number: '',
  remarks: '',
});

const fetchEducations = async () => {
  try {
    const response = await $fetch('http://localhost:8000/api/qualifications/');
    educations.value = response;
  } catch (error) {
    console.error('Error fetching educations:', error);
  }
};

const submitForm = () => {
  emit('submit', qualificationData.value);
};

onMounted(() => {
  fetchEducations();
});
</script>
