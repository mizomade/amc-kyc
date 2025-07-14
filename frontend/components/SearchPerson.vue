<template>
  <div class="max-w-5xl mx-auto p-8">
    <h2 class="text-2xl font-bold mb-9 text-center"> Search for a Person</h2>

    <!-- Search Form -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-x-12">
      <!-- Left Column -->
      <div class="space-y-6">
        <div>
          <label class="block text-sm font-medium mb-1">Name</label>
          <div class="relative">
            <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></span>
            <input
              v-model="name"
              type="text"
              placeholder="Enter name"
              class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-400"
            />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Hnam Hming</label>
          <div class="relative">
            <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></span>
            <input
              v-model="hnam_hming"
              type="text"
              placeholder="Enter hnam hming"
              class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-400"
            />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Mobile Number</label>
          <div class="relative">
            <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></span>
            <input
              v-model="mobile"
              type="text"
              placeholder="Enter mobile number"
              class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-400"
            />
          </div>
        </div>
      </div>

      <!-- Right Column -->
      <div class="space-y-6 mt-6 md:mt-0">
        <div>
          <label class="block text-sm font-medium mb-1">EPIC Number</label>
          <div class="relative">
            <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></span>
            <input
              v-model="epic"
              type="text"
              placeholder="Enter EPIC number"
              class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-400"
            />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Aadhar Number</label>
          <div class="relative">
            <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></span>
            <input
              v-model="aadhar"
              type="text"
              placeholder="Enter Aadhar number"
              class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-400"
            />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">House Number</label>
          <div class="relative">
            <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></span>
            <input
              v-model="house_number"
              type="text"
              placeholder="Enter house number"
              class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-400"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Buttons -->
    <div class="flex justify-center gap-6 my-12">
      <button
        @click="search"
        :disabled="loading"
        class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-3 rounded-lg shadow disabled:opacity-50"
      >
        <span v-if="loading" class="animate-spin mr-2 inline-block w-5 h-5 border-2 border-white border-t-transparent rounded-full"></span>
        Search
      </button>
      <button
        @click="reset"
        class="bg-gray-200 hover:bg-gray-300 text-gray-800 px-8 py-3 rounded-lg shadow"
      >
        Reset
      </button>
    </div>

    <!-- Search Results -->
    <div v-if="results.length" class="bg-white rounded-lg shadow p-6 space-y-4">
      <h3 class="text-xl font-semibold mb-2">Results ({{ results.length }})</h3>
      <ul class="divide-y divide-gray-200">
        <li v-for="person in results" :key="person.id">
  <NuxtLink
    :to="`/profile/${person.id}`"
    class="block py-4 px-3 rounded hover:bg-blue-50 transition focus:outline-none focus:ring-2 focus:ring-blue-400"
  >
    <div class="flex gap-4 items-center">
      <!-- 📸 Photo -->
      <div class="w-14 h-14 rounded-full overflow-hidden border-2 border-blue-400 shadow-md">
        <img
          v-if="person.photo"
          :src="person.photo"
          alt="Profile"
          class="w-full h-full object-cover"
        />
        <div v-else class="w-full h-full flex items-center justify-center text-xs text-gray-400 bg-gray-100">
          No Photo
        </div>
      </div>

      <!-- 📝 Details -->
      <div class="flex-1 flex flex-col md:flex-row md:justify-between">
        <div>
          <p class="font-semibold text-gray-900">
            {{ person.first_name }} {{ person.hnam_hming }}
          </p>
          <p class="text-sm text-gray-600">
            EPIC: {{ person.epic_number }} |
            Aadhar: {{ person.aadhar_number }} |
            Mobile: {{ person.mobile }}
          </p>
        </div>
        <div class="text-sm text-gray-500 mt-2 md:mt-0 text-right">
          House: {{ person.house_number }}<br />
          Father: {{ person.father_name || '-' }}<br />
          Mother: {{ person.mother_name || '-' }}
        </div>
      </div>
    </div>
  </NuxtLink>
</li>

      </ul>
    </div>

    <!-- No Results -->
    <p v-else-if="searchedOnce && !loading" class="text-gray-500 italic text-center mt-10">
      No results found.
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useNuxtApp } from '#app'

const { $axios } = useNuxtApp()

const name = ref('')
const hnam_hming = ref('')
const mobile = ref('')
const epic = ref('')
const aadhar = ref('')
const house_number = ref('')
const results = ref([])
const searchedOnce = ref(false)
const loading = ref(false)

const search = async () => {
  loading.value = true
  const params = {}
  if (name.value) params.name = name.value
  if (hnam_hming.value) params.hnam_hming = hnam_hming.value
  if (mobile.value) params.mobile = mobile.value
  if (epic.value) params.epic = epic.value
  if (aadhar.value) params.aadhar = aadhar.value
  if (house_number.value) params.house_number = house_number.value

  try {
    const res = await $axios.get('/search/person/', { params })
    results.value = res.data
  } catch (err) {
    console.error('Search failed:', err)
    results.value = []
  } finally {
    searchedOnce.value = true
    loading.value = false
  }
}

const reset = () => {
  name.value = ''
  hnam_hming.value = ''
  mobile.value = ''
  epic.value = ''
  aadhar.value = ''
  house_number.value = ''
  results.value = []
  searchedOnce.value = false
}
</script>
