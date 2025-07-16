<template>
  <form @submit.prevent="submitForm" class="space-y-6">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <label for="occupation_id" class="block text-sm font-medium text-gray-700">Occupation</label>
        <select
          id="occupation_id"
          v-model="occupationData.occupation_id"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        >
          <option
            v-for="occupation in occupations"
            :key="occupation.id"
            :value="occupation.id"
          >
            {{ occupation.name }}
          </option>
        </select>


      </div>

      <div>
        <label for="employer_name" class="block text-sm font-medium text-gray-700">Employer Name</label>
        <input
          type="text"
          id="employer_name"
          v-model="occupationData.employer_name"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
        />
      </div>

      <div>
        <label for="position_title" class="block text-sm font-medium text-gray-700">Position Title</label>
        <input
          type="text"
          id="position_title"
          v-model="occupationData.position_title"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
        />
      </div>

      <div>
        <label for="start_date" class="block text-sm font-medium text-gray-700">Start Date</label>
        <input
          type="date"
          id="start_date"
          v-model="occupationData.start_date"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
        />
      </div>

      <div>
        <label for="end_date" class="block text-sm font-medium text-gray-700">End Date</label>
        <input
          type="date"
          id="end_date"
          v-model="occupationData.end_date"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
        />
      </div>

      <div>
        <label for="remarks" class="block text-sm font-medium text-gray-700">Remarks</label>
        <input
          type="text"
          id="remarks"
          v-model="occupationData.remarks"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
        />
      </div>
    </div>

    <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
      <button
        type="submit"
        :disabled="disableSave"
        class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 disabled:opacity-50"
      >
        Save
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useNuxtApp } from '#app';
import { usePersonStore } from '@/stores/person';

const emit = defineEmits(['saved']);

const { $api } = useNuxtApp();
const personStore = usePersonStore();
const personId = computed(() => personStore.person_id);

const occupations = ref([]);

const occupationData = ref({
  occupation_id: null,
  employer_name: '',
  position_title: '',
  start_date: null,
  end_date: null,
  remarks: ''
});

const fetchOccupations = async () => {
  try {
    const response = await $api.get('/occupationlist/');  
    occupations.value = response.data;                 
  } catch (error) {
    console.error('Error fetching occupations:', error);
  }
};


const submitForm = async () => {
  if (!personId.value) {
    alert('Person ID missing. Please save personal details first.');
    return;
  }

  const payload = {
    ...occupationData.value,
    person_id: personId.value  // 🔥 Include person_id
  };

  try {
    await $api.post('/occupations/', payload);
    alert('Occupation saved successfully.');
    emit('saved');  // 🔥 Emit to move to document tab
  } catch (error) {
    console.error('Failed to save occupation:', error);
    alert('Failed to save occupation.');
  }
};

const props = defineProps({
  disableSave: {
    type: Boolean,
    default: false
  }
});

onMounted(fetchOccupations);
</script>
