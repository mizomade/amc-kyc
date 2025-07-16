<template>
  <div>
    <div
      v-for="(qualification, index) in qualifications"
      :key="index"
      class="mb-6 p-4 border rounded space-y-4 relative"
    >
      <h3 class="font-semibold text-lg">Qualification {{ index + 1 }}</h3>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

        <div>
          <label class="block text-sm font-medium text-gray-700">Education</label>
          <select
            v-model="qualification.education_id"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
          >
            <option v-for="education in educationOptions" :key="education.id" :value="education.id">
              {{ education.name }}
            </option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Year of Passing</label>
          <input
            type="number"
            v-model="qualification.year_of_passing"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Institution Name</label>
          <input
            type="text"
            v-model="qualification.institution_name"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Grade / Marks</label>
          <input
            type="text"
            v-model="qualification.grade_or_marks"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Certificate Number</label>
          <input
            type="text"
            v-model="qualification.certificate_number"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Remarks</label>
          <input
            type="text"
            v-model="qualification.remarks"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
          />
        </div>

      </div>
    </div>

    <div class="flex flex-col gap-4 mt-6">
      <button
        type="button"
        @click="addQualificationForm"
        class="w-full inline-flex justify-center rounded-md border border-dashed border-gray-400 px-4 py-2 text-gray-700 hover:bg-gray-100"
      >
        + Add More
      </button>

        <button
          type="button"
          @click="submitAllQualifications"
          :disabled="isSubmitDisabled"
          class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-white font-medium hover:bg-blue-700 disabled:opacity-50"
        >
          Save All Qualifications
        </button>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useNuxtApp } from '#app'
import { usePersonStore } from '@/stores/person'

const { $api } = useNuxtApp()
const personStore = usePersonStore()
const emit = defineEmits(['saved'])
// Get person_id directly from Pinia
const personId = computed(() => personStore.person_id)

// Disable the save button if person_id missing
const isSubmitDisabled = computed(() => !personId.value)

const educationOptions = ref([])
const qualifications = ref([createEmptyQualification()])

function createEmptyQualification() {
  return {
    education_id: null,
    year_of_passing: '',
    institution_name: '',
    grade_or_marks: '',
    certificate_number: '',
    remarks: ''
  }
}

const fetchEducationOptions = async () => {
  try {
    const response = await $api.get('/education/')
    educationOptions.value = response.data
  } catch (error) {
    console.error('Failed to fetch education options:', error)
  }
}

const addQualificationForm = () => {
  qualifications.value.push(createEmptyQualification())
}

const submitAllQualifications = async () => {
  if (!personId.value) {
    alert('Person ID missing. Please save personal details first.')
    return
  }

  const payload = {
    qualifications: qualifications.value.map((qualification) => ({
      person_id: personId.value,
      education_id: qualification.education_id,
      year_of_passing: qualification.year_of_passing,
      institution_name: qualification.institution_name,
      grade_or_marks: qualification.grade_or_marks,
      certificate_number: qualification.certificate_number,
      remarks: qualification.remarks
    }))
  }

  console.log('Payload:', payload)
  try {
    await $api.post('/qualifications/bulk/', payload)
    alert('All qualifications saved successfully.')

    emit('saved')  // 🔥 EMIT HERE after success

  } catch (error) {
    console.error('Bulk qualification save failed:', error)
    alert('Failed to save qualifications.')
  }
}


onMounted(fetchEducationOptions)

// Optional debug: watch personId changes
watch(personId, (newId) => {
  if (newId) {
    console.log('🟢 person_id available:', newId)
  }
})
</script>


