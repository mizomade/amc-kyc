<template>
  <div v-if="show" class="fixed inset-0 z-50 bg-black bg-opacity-50 flex items-center justify-center">
    <div class="bg-white p-6 rounded-lg w-full max-w-md">
      <h2 class="text-xl font-semibold mb-4">Add New Parent</h2>

      <div class="mb-4">
        <label class="block mb-1">First Name</label>
        <input v-model="parentData.first_name" type="text"
          class="w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-500" />
      </div>

      <div class="mb-4">
        <label class="block mb-1">Hnam Hming</label>
        <input v-model="parentData.hnam_hming" type="text"
          class="w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-500" />
      </div>

      <div class="mb-4">
        <label class="block mb-1">Gender</label>
        <select v-model="parentData.gender"
          class="w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-500">
          <option disabled value="">Select Gender</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
          <option value="Transgender">Transgender</option>
          <option value="Other">Other</option>
        </select>
      </div>

      <div class="flex justify-end space-x-4">
        <button type="button" @click="$emit('close')" class="...">
        Cancel
        </button>

        <button type="button" @click="submit" class="...">
        Save
        </button>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useNuxtApp } from '#app'
import { useHouseStore } from '@/stores/house'

const { $api } = useNuxtApp()
const houseStore = useHouseStore()

const props = defineProps({
  show: Boolean
})

const emit = defineEmits(['close', 'added'])

const parentData = ref({
  first_name: '',
  hnam_hming: '',
  gender: ''
})

const submit = async () => {
  if (!parentData.value.first_name || !parentData.value.gender) {
    alert('First Name and Gender are required.')
    return
  }

  const formData = new FormData()
  formData.append('first_name', parentData.value.first_name)
  formData.append('hnam_hming', parentData.value.hnam_hming || '')
  formData.append('gender', parentData.value.gender)

  // Append house_id only if available
  if (houseStore.house_id) {
    formData.append('house_id', String(houseStore.house_id))
  }

  try {
    const response = await $api.post('/person/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    emit('added', response.data)
    emit('close')
    parentData.value = { first_name: '', hnam_hming: '', gender: '' }
  } catch (error) {
    console.error('Failed to save parent:', error)
    alert('Failed to add parent.')
  }
}


</script>
