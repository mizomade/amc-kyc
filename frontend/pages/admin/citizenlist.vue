<template>
  <div class="min-h-screen bg-gray-100 p-6">
          <div class="flex justify-between items-center mb-6">
              <h1 class="text-3xl font-bold text-gray-900">Citizen List</h1>
              <div class="flex space-x-2 items-center">
                
                <!-- Filter Dropdown Buttons -->
                    <div class="flex space-x-2">
                      <!-- Age Filter -->
                      <select
                      v-model="selectedAge"
                      class="rounded-full border border-gray-300 px-4 py-1 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="">All Ages</option>
                      <option value="0-18">0-18</option>
                      <option value="18-35">18-35</option>
                      <option value="35-60">35-60</option>
                      <option value="60 above">60 above</option>
                    </select>


                      <!-- Occupation Filter -->
                      <select
                      v-model="selectedOccupation"
                      class="rounded-full border border-gray-300 px-4 py-1 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="">All Occupations</option>
                      <option value="Business">Business</option>
                      <option value="Government">Government</option>
                      <option value="Unemployed">Unemployed</option>
                    </select>

                    </div>


                <!-- Search Input -->
                <input
                  v-model="searchTerm"
                  type="text"
                  placeholder="Search name..."
                  class="border border-gray-300 rounded-md px-3 py-2 text-sm shadow-sm"
                />

                <!-- Add New Entry Button -->
                <NuxtLink
                  to="/admin/newentry/"
                  class="bg-blue-600 text-white py-2 px-4 rounded-md shadow-md hover:bg-blue-700 transition duration-300"
                >
                  Add New Entry
                </NuxtLink>
              </div>
            </div>




    <!-- Tabs for different lists (e.g., Persons, Houses) -->
    <div class="bg-white rounded-lg shadow-md p-6">
      <div class="border-b border-gray-200 mb-4">
        <nav class="-mb-px flex space-x-8" aria-label="Tabs">
          <button @click="activeTab = 'persons'" :class="[activeTab === 'persons' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300', 'whitespace-nowrap py-3 px-1 border-b-2 font-medium text-sm']">
            Persons
          </button>
          <button @click="activeTab = 'houses'" :class="[activeTab === 'houses' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300', 'whitespace-nowrap py-3 px-1 border-b-2 font-medium text-sm']">
            Houses
          </button>
          <!-- Add more tabs as needed -->
        </nav>
      </div>

      <div v-if="activeTab === 'persons'">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Persons</h2>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Age</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">EPIC</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Aadhar</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Mobile</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                </tr>
              </thead>

              <tbody class="bg-white divide-y divide-gray-200">
                <tr
                  v-for="person in persons"
                  :key="person.id"
                  class="hover:bg-blue-50 cursor-pointer transition"
                  @click="router.push(`/profile/${person.id}`)"
                >
                  <td class="px-6 py-4 text-sm font-medium text-gray-900 max-w-[200px] truncate">
                    {{ person.first_name }} {{ person.hnam_hming || '' }}
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-500">
                  {{ person.age || '-' }}
                  </td>

                  <td class="px-6 py-4 text-sm text-gray-500">
                    {{ person.epic_number || '-' }}
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-500">
                    {{ person.aadhar_number || '-' }}
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-500">
                    {{ person.mobile || '-' }}
                  </td>
                  <td
                    class="px-6 py-4 text-sm font-medium text-red-600 hover:text-red-800"
                    @click.stop="confirmDelete(person.id)"
                  >
                    Delete
                  </td>
                </tr>
              </tbody>


          </table>
        </div>
      </div>

      <div v-if="activeTab === 'houses'">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Houses</h2>
        <table class="min-w-full divide-y divide-gray-200">
  <thead class="bg-gray-50">
    <tr>
      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">House No</th>
      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Head of Family</th>
      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Location</th>
      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ownership</th>
    </tr>
  </thead>
  <tbody class="bg-white divide-y divide-gray-200">
    <tr v-for="house in houses" :key="house.id">
      <td class="px-6 py-4 text-sm text-gray-900">{{ house.house_number }}</td>
      <td class="px-6 py-4 text-sm text-gray-500">{{ house.head_name || '—' }}</td>
      <td class="px-6 py-4 text-sm text-gray-500">{{ house.veng_name }}</td>
        <td class="px-6 py-4 text-sm text-gray-500">
        {{ house.is_owner ? 'Owned' : 'Rented' }}
        </td>

    </tr>
  </tbody>
</table>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useNuxtApp } from '#app'
import debounce from 'lodash/debounce'
import { useRouter } from 'vue-router'

const router = useRouter()

const activeTab = ref('persons')
const persons = ref([])
const houses = ref([])
const selectedAge = ref('')
const selectedOccupation = ref('')
const searchTerm = ref('')  // new: search input binding

const { $api } = useNuxtApp()

onMounted(async () => {
  await fetchPersons()
  await fetchHouses()
})

async function fetchPersons() {
  try {
    const params = {}
    if (searchTerm.value) params.search = searchTerm.value
    if (selectedAge.value) params.age_group = selectedAge.value
    if (selectedOccupation.value) params.occupation = selectedOccupation.value

    const res = await $api.get('/search/person/', { params })
    persons.value = res.data.reverse()
  } catch (err) {
    console.error('Failed to load persons:', err)
  }
}

watch([selectedAge, selectedOccupation], () => {
  fetchPersons()
})

watch(searchTerm, () => {
  debouncedFetch()
})







async function fetchHouses() {
  try {
    const res = await $api.get('/person/houses/')
    houses.value = res.data
  } catch (err) {
    console.error('Failed to load houses:', err)
  }
}

// new: debounce search watcher
const debouncedFetch = debounce((val) => {
  fetchPersons(val)
}, 300)

watch(searchTerm, (val) => {
  debouncedFetch(val)
})

async function confirmDelete(personId) {
  if (confirm("Are you sure you want to delete this person?")) {
    try {
      await $api.delete(`/person/delete/${personId}`)
    
      persons.value = persons.value.filter(p => p.id !== personId)
    } catch (err) {
      console.error("Failed to delete person:", err)

      alert("Failed to delete person.")
    }
  }
}




</script>


<style scoped>
/* Tailwind CSS handles most styling, no custom styles needed here */
</style>
