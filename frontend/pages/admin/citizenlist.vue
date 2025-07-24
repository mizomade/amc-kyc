<template>
  <div class="min-h-screen bg-gray-100 p-6">
          <div class="flex justify-between items-center mb-6">
              <h1 class="text-3xl font-bold text-gray-900">Citizen List</h1>

              <div class="flex space-x-4 items-center">
                
                <!-- 👇 Persons Tab Filters -->
                <div v-if="activeTab === 'persons'" class="flex space-x-2 items-center">
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
                    <option value="new-voters">New Voters</option>
                  </select>

                  <!-- Occupation Filter -->
                  <select
                    v-model="selectedOccupation"
                    class="rounded-full border border-gray-300 px-4 py-1 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">All Occupations</option>
                    <option
                      v-for="occupation in occupations"
                      :key="occupation.id"
                      :value="occupation.name"
                    >
                      {{ occupation.name }}
                    </option>
                  </select>

                  <!-- Person Search -->
                  <input
                    v-model="searchTerm"
                    type="text"
                    placeholder="Search name..."
                    class="border border-gray-300 rounded-md px-3 py-2 text-sm shadow-sm"
                  />
                </div>

                <!--  Houses Tab Filters -->
                <div v-else-if="activeTab === 'houses'" class="flex space-x-2 items-center">
                  <select
                    v-model="houseVeng"
                    class="rounded-full border border-gray-300 px-4 py-1 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">All Locations</option>
                    <option
                      v-for="veng in vengs"
                      :key="veng.id"
                      :value="veng.id"
                    >
                      {{ veng.name }}
                    </option>
                  </select>

                  <select
                    v-model="houseOwnership"
                    class="rounded-full border border-gray-300 px-4 py-1 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">All Ownerships</option>
                    <option value="owned">Owned</option>
                    <option value="rented">Rented</option>
                  </select>


                  <input
                    v-model="houseSearchTerm"
                    type="text"
                    placeholder="Search house no..."
                    class="border border-gray-300 rounded-md px-3 py-2 text-sm shadow-sm"
                  />
                </div>

                <!-- Add New Entry Button (Always Visible) -->
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
        <h2 class="text-xl font-semibold text-gray-900 mb-4"></h2>
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
                
                >
                  <td class="px-6 py-4 text-sm font-medium text-gray-900 max-w-[200px] truncate"   @click="router.push(`/admin/person/${person.id}`)">
                    {{ person.first_name }}  {{ person.hnam_hming || '' }}
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
        <h2 class="text-xl font-semibold text-gray-900 mb-4"></h2>
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
                <tr v-for="house in houses" :key="house.id" class="hover:bg-blue-50 cursor-pointer transition" @click="router.push(`/admin/house/${house.id}`)">
                  <td class="px-6 py-4 text-sm text-gray-900">{{ house.house_number }} </td>
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

definePageMeta({
  layout: 'admin',
  middleware: 'auth',
})

const router = useRouter()
const { $api } = useNuxtApp()

// Tabs
const activeTab = ref('persons')

// Persons filters
const persons = ref([])
const selectedAge = ref('')
const selectedOccupation = ref('')
const searchTerm = ref('')
const occupations = ref([])

// Houses filters
const houses = ref([])
const houseOwnership = ref('')
const houseSearchTerm = ref('')
const vengs = ref([])         // stores list of locations
const houseVeng = ref('')  

// Fetch Data on Mount
onMounted(async () => {
  await fetchPersons()
  await fetchOccupations()
  await fetchHouses()
    await fetchVengs() 
})

/* === Persons Fetching === */
async function fetchPersons() {
  try {
    const params = {}

    if (searchTerm.value) params.search = searchTerm.value

    if (selectedOccupation.value) params.occupation = selectedOccupation.value

    if (selectedAge.value) {
      if (selectedAge.value === 'new-voters') {
        params.new_voters = true
      } else {
        params.age_group = selectedAge.value
      }
    }

    const res = await $api.get('/forentry/search/', { params })
    persons.value = res.data.reverse()
  } catch (err) {
    console.error('Failed to load persons:', err)
  }
}


// Filters Watchers (Persons)
watch([selectedAge, selectedOccupation], () => {
  fetchPersons()
})

// Search Watcher with Debounce (Persons)
const debouncedFetchPersons = debounce(() => {
  fetchPersons()
}, 300)

watch(searchTerm, () => {
  debouncedFetchPersons()
})


/* === Houses Fetching === */
async function fetchHouses() {
  try {
    const params = {}
    if (houseOwnership.value) params.ownership = houseOwnership.value
    if (houseSearchTerm.value) params.query = houseSearchTerm.value
    if (houseVeng.value) params.veng_id = houseVeng.value   // location filter

    const res = await $api.get('/forentry/houses/search/', { params })
    houses.value = res.data
  } catch (err) {
    console.error('Failed to search houses:', err)
    houses.value = []
  }
}


async function fetchVengs() {
  try {
    const res = await $api.get('/veng/')   // adjust endpoint if needed
    vengs.value = res.data
  } catch (err) {
    console.error('Failed to load locations (vengs):', err)
  }
}

watch(houseVeng, () => {
  fetchHouses()
})



// Filters Watchers (Houses)
watch([houseOwnership], () => {
  fetchHouses()
})

// Search Watcher with Debounce (Houses)
const debouncedFetchHouses = debounce(() => {
  fetchHouses()
}, 300)

watch(houseSearchTerm, () => {
  debouncedFetchHouses()
})


/* === Occupations Fetching === */
async function fetchOccupations() {
  try {
    const res = await $api.get('/occupations/')
    occupations.value = res.data
  } catch (err) {
    console.error('Failed to load occupations:', err)
  }
}


/* === Delete Person === */
async function confirmDelete(personId) {
  if (confirm('Are you sure you want to delete this person?')) {
    try {
      await $api.delete(`/forentry/delete/${personId}`)
      persons.value = persons.value.filter(p => p.id !== personId)
    } catch (err) {
      console.error('Failed to delete person:', err)
      alert('Failed to delete person.')
    }
  }
}
</script>


<style scoped>
/* Tailwind CSS handles most styling, no custom styles needed here */
</style>