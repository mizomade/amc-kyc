<template>
  <div class="min-h-screen bg-gray-100 p-6">
        <div class="flex justify-between items-center mb-6">
        <h1 class="text-3xl font-bold text-gray-900">Citizen List</h1>
        <div class="flex space-x-4">
            <input
            v-model="searchTerm"
            type="text"
            placeholder="Search name..."
            class="border border-gray-300 rounded-md px-3 py-2 text-sm shadow-sm"
            />
            <NuxtLink
            to="/house-entry/"
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
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Age</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Father's Name</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Mother's Name</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
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
                    <td class="px-6 py-4 text-sm text-gray-500">{{ person.age }}</td>
                    <td class="px-6 py-4 text-sm text-gray-500">{{ person.father_name }}</td>
                    <td class="px-6 py-4 text-sm text-gray-500">{{ person.mother_name }}</td>
                    <td class="px-6 py-4 text-sm font-medium text-red-600 hover:text-red-800"@click.stop="confirmDelete(person.id)">Delete</td>


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
import { useToast } from 'vue-toastification'

const toast = useToast()

const router = useRouter()

const activeTab = ref('persons')
const persons = ref([])
const houses = ref([])

const searchTerm = ref('')  // new: search input binding

const { $axios } = useNuxtApp()

onMounted(async () => {
  await fetchPersons()
  await fetchHouses()
})

// modified: support optional search
async function fetchPersons(search = '') {
  try {
    const res = await $axios.get('/person/persons/', {
      params: search ? { search } : {}
    })
    persons.value = res.data
  } catch (err) {
    console.error('Failed to load persons:', err)
  }
}

async function fetchHouses() {
  try {
    const res = await $axios.get('/person/houses/')
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
      await $axios.delete(`/person/delete/${personId}`)
      toast.success('Person deleted successfully!')
      persons.value = persons.value.filter(p => p.id !== personId)
    } catch (err) {
      console.error("Failed to delete person:", err)
      toast.error('Failed to delete person.')
      alert("Failed to delete person.")
    }
  }
}




</script>


<style scoped>
/* Tailwind CSS handles most styling, no custom styles needed here */
</style>
