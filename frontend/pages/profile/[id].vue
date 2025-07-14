<template>
  <div class="max-w-6xl mx-auto py-10 px-6 sm:px-10 bg-gray-50 min-h-screen">
    <div v-if="loading" class="text-center text-gray-500 py-24 text-lg">
      Loading profile...
    </div>

    <div v-else-if="person" class="bg-white rounded-2xl shadow-lg p-10 space-y-10">
      <!-- Top: Avatar + Editable Name -->
      <div class="flex flex-col sm:flex-row items-center sm:items-start gap-8">
        <div class="w-36 h-36 rounded-full bg-gray-200 overflow-hidden border-4 border-blue-500 shadow-md">
          <img
            v-if="person.photo"
            :src="person.photo"
            alt="Profile"
            class="w-full h-full object-cover"
          />
          <div
            v-else
            class="w-full h-full flex items-center justify-center text-sm text-gray-400"
          >
            No Photo
          </div>
        </div>

        <div class="w-full sm:w-auto flex-1 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-600">First Name</label>
            <input
              v-model="person.first_name"
              type="text"
              class="mt-1 w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none text-gray-800"
              placeholder="First name"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-600">Hnam Hming</label>
            <input
              v-model="person.hnam_hming"
              type="text"
              class="mt-1 w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none text-gray-800"
              placeholder="Hnam Hming"
            />
          </div>

          <p class="text-sm text-gray-500 mt-2">
            House No: <strong>{{ person.house_number || '-' }}</strong>
          </p>
        </div>
      </div>

      <!-- Personal Info -->
      <div class="space-y-6">
            <h2 class="text-xl font-semibold text-gray-800 border-b pb-2">Personal Information</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

                <div>
                <label class="block text-sm font-medium text-gray-600">EPIC Number</label>
                <input
                    v-model="person.epic_number"
                    type="text"
                    class="mt-1 w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 text-gray-800"
                    placeholder="EPIC number"
                />
                </div>

                <div>
                <label class="block text-sm font-medium text-gray-600">Aadhar Number</label>
                <input
                    v-model="person.aadhar_number"
                    type="text"
                    class="mt-1 w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 text-gray-800"
                    placeholder="Aadhar number"
                />
                </div>

                <div>
                <label class="block text-sm font-medium text-gray-600">Mobile</label>
                <input
                    v-model="person.mobile"
                    type="text"
                    class="mt-1 w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 text-gray-800"
                    placeholder="Mobile"
                />
                </div>

                <div>
                <label class="block text-sm font-medium text-gray-600">Date of Birth</label>
                <input
                    v-model="person.dob"
                    type="date"
                    class="mt-1 w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 text-gray-800"
                />
                </div>

            </div>
            </div>

      <!-- Save Button -->
      <div class="text-center pt-6">
        <button
          @click="saveChanges"
          class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-3 rounded-lg shadow transition duration-300"
        >
          Save Changes
        </button>
      </div>
    </div>

    <div v-else class="text-center py-20 text-gray-500 text-lg">
      Person not found.
    </div>
  </div>
</template>





<script setup>
import { useRoute, useNuxtApp } from '#app'
import { ref, onMounted } from 'vue'

const route = useRoute()
const { $axios } = useNuxtApp()

const person = ref(null)
const loading = ref(true)
const saving = ref(false)




onMounted(async () => {
  const id = route.params.id
  try {
    const res = await $axios.get('/search/person/', { params: { id } })
    if (res.data.length) {
      person.value = res.data[0]
    }
  } catch (error) {
    console.error('Failed to load profile:', error)
  } finally {
    loading.value = false
  }
})

async function saveChanges() {
  if (!person.value?.id) return

  saving.value = true

  try {
    const payload = {
      first_name: person.value.first_name,
      hnam_hming: person.value.hnam_hming,
      gender: person.value.gender,
      dob: person.value.dob,
      blood_group: person.value.blood_group,
      mobile: person.value.mobile,
      epic_number: person.value.epic_number,
      aadhar_number: person.value.aadhar_number,
      marital_status: person.value.marital_status,
    }

    // Only include FK if it exists
    if (person.value.father?.id) payload.father = person.value.father.id
    if (person.value.mother?.id) payload.mother = person.value.mother.id
    if (person.value.spouse?.id) payload.spouse = person.value.spouse.id
    if (person.value.house?.id) payload.house = person.value.house.id
    if (person.value.religion?.id) payload.religion = person.value.religion.id
    if (person.value.denomination?.id) payload.denomination = person.value.denomination.id
    if (person.value.role?.id) payload.role = person.value.role.id

    await $axios.put(`/person/update/${person.value.id}`, payload)
  } catch (error) {
    console.error('Failed to save profile:', error)
  } finally {
    saving.value = false
  }
}
</script>


