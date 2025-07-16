<template>
  <div class="fixed z-50 inset-0 overflow-y-auto bg-gray-900 bg-opacity-50">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <span class="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>

      <div @click.stop class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full">
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Add New Member</h3>

          <!-- Tabs -->
          <div class="border-b border-gray-200">
            <nav class="-mb-px flex space-x-8">
              <button @click="activeTab = 'personal'" :class="activeTab === 'personal' ? activeTabClass : inactiveTabClass">Personal Details</button>
              <button @click="activeTab = 'qualifications'" :class="activeTab === 'qualifications' ? activeTabClass : inactiveTabClass">Qualifications</button>
              <button @click="activeTab = 'occupations'" :class="activeTab === 'occupations' ? activeTabClass : inactiveTabClass">Occupations</button>
              <button @click="activeTab = 'documents'" :class="activeTab === 'documents' ? activeTabClass : inactiveTabClass">Documents</button>
            </nav>
          </div>

          <div class="mt-6 h-[60vh] overflow-y-auto">

            <!-- Personal Details -->
            <div v-if="activeTab === 'personal'">
              <form @submit.prevent="submitPersonalDetails" class="space-y-6">

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

                  <!-- Static Fields -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700">First Name</label>
                    <input v-model="memberData.first_name" type="text"
                      class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700">Hnam Hming</label>
                    <input v-model="memberData.hnam_hming" type="text"
                      class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
                  </div>

                  <div>
                    <label for="gender" class="block text-sm font-medium text-gray-700">Gender</label>
                    <select
                      id="gender"
                      v-model="memberData.gender"
                      class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    >
                      <option disabled value="">Select Gender</option>
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                      <option value="Transgender">Transgender</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>


                  <div>
                    <label class="block text-sm font-medium text-gray-700">Date of Birth</label>
                    <input v-model="memberData.dob" type="date"
                      class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700">Blood Group</label>
                    <input v-model="memberData.blood_group" type="text"
                      class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700">Mobile</label>
                    <input v-model="memberData.mobile" type="text"
                      class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700">EPIC Number</label>
                    <input v-model="memberData.epic_number" type="text"
                      class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700">Aadhar Number</label>
                    <input v-model="memberData.aadhar_number" type="text"
                      class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700">Marital Status</label>
                    <input v-model="memberData.marital_status" type="text"
                      class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
                  </div>

                          <!-- Father Dropdown -->
                        <div>
                          <label class="block text-sm font-medium text-gray-700">Father</label>
                          <div class="flex space-x-2">
                            <input
                              type="text"
                              v-model="fatherSearchText"
                              @input="searchFather"
                              placeholder="Search Father..."
                              class="flex-1 mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm"
                            />
                            <button
                              @click="showAddFatherModal = true"
                              type="button"
                              class="inline-flex justify-center rounded-md border border-transparent shadow-sm px-3 py-2 bg-gray-500 text-white text-sm font-medium hover:bg-gray-600"
                          >
                              +
                            </button>
                          </div>

                          <div v-if="fatherOptions.length > 0" class="border rounded-md mt-1 max-h-40 overflow-y-auto bg-white">
                            <div
                              v-for="option in fatherOptions"
                              :key="option.id"
                              @click="selectFather(option)"
                              class="px-3 py-2 hover:bg-gray-100 cursor-pointer"
                            >
                              {{ option.first_name }} {{ option.hnam_hming }}
                            </div>
                          </div>
                        </div>


                      

                      <!-- Mother Dropdown -->
                      <div>
                        <label class="block text-sm font-medium text-gray-700">Mother</label>
                        <div class="flex space-x-2">
                          <input
                            type="text"
                            v-model="motherSearchText"
                            @input="searchMother"
                            placeholder="Search Mother..."
                            class="flex-1 mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm"
                          />
                          <button
                            @click="showAddMotherModal = true"
                            type="button"
                            class="inline-flex justify-center rounded-md border border-transparent shadow-sm px-3 py-2 bg-gray-500 text-white text-sm font-medium hover:bg-gray-600"
                          >
                            +
                          </button>

                        </div>

                        <div v-if="motherOptions.length > 0" class="border rounded-md mt-1 max-h-40 overflow-y-auto bg-white">
                          <div
                            v-for="option in motherOptions"
                            :key="option.id"
                            @click="selectMother(option)"
                            class="px-3 py-2 hover:bg-gray-100 cursor-pointer"
                          >
                            {{ option.first_name }} {{ option.hnam_hming }}
                          </div>
                        </div>
                      </div>





                  <!-- Religion Dropdown -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700">Religion</label>
                    <select v-model="memberData.religion_id"
                      class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm">
                      <option disabled value="">Select Religion</option>
                      <option v-for="religion in religions" :key="religion.id" :value="religion.id">
                        {{ religion.name }}
                      </option>
                    </select>
                  </div>

                  <!-- Denomination Dropdown -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700">Denomination</label>
                    <select v-model="memberData.denomination_id"
                      class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm">
                      <option disabled value="">Select Denomination</option>
                      <option v-for="denomination in denominations" :key="denomination.id" :value="denomination.id">
                        {{ denomination.name }}
                      </option>
                    </select>
                  </div>
                  <div>
                    <label for="rent_start_date" class="block text-sm font-medium text-gray-700">Rent Start Date</label>
                    <input
                      id="rent_start_date"
                      type="date"
                      v-model="memberData.rent_start_date"
                      class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    />
                  </div>

                  <div>
                    <label for="rent_end_date" class="block text-sm font-medium text-gray-700">Rent End Date</label>
                    <input
                      id="rent_end_date"
                      type="date"
                      v-model="memberData.rent_end_date"
                      class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    />
                  </div>
                  <div>
                  <label class="block text-sm font-medium text-gray-700">Photo</label>
                  <input
                    type="file"
                    accept="image/*"
                    @change="handlePhotoUpload"
                    class="mt-1 block w-full text-sm text-gray-700 border border-gray-300 rounded-md shadow-sm"
                  />
                </div>



                  <!-- Is Househead Checkbox -->
                  <div class="flex items-center mt-4">
                    <input id="is_househead" type="checkbox" v-model="memberData.is_househead"
                      class="mr-2 h-4 w-4 text-blue-600 border-gray-300 rounded" />
                    <label for="is_househead" class="text-sm text-gray-700">Is House Head?</label>
                  </div>

                </div>

                <!-- Buttons -->
                <div class="bg-gray-50 px-4 py-3 flex justify-between">
                  <button @click="$emit('close')" type="button"
                    class="inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-gray-500 text-base font-medium text-white hover:bg-gray-600">
                    Back
                  </button>
                  <button type="submit"
                    class="inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700">
                    Save Personal Details
                  </button>
                </div>

              </form>
            </div>

            <!-- Other Tabs -->
          <div v-show="activeTab === 'qualifications'">
            <QualificationForm :personId="personId" :disableSave="!personId" @saved='moveToOccupations'/>
          </div>

          <div v-show="activeTab === 'occupations'">
            <OccupationForm :personId="personId" :disableSave="!personId" @saved='moveToDocuments'/>
          </div>
          <div v-show="activeTab === 'documents'">
            <DocumentForm :personId="personId" :disableSave="!personId" @close="handleDocumentFormClose" />
          </div>

          </div>
        </div>
      </div>
    </div>
  </div>
                      <AddParentModal :show="showAddFatherModal" @close="showAddFatherModal = false" @added="handleNewFather" />
                        <!-- Mother Modal -->
                      <AddParentModal
                        :show="showAddMotherModal"
                        @close="showAddMotherModal = false"
                        @added="handleNewMother"
                      />

</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import QualificationForm from './QualificationForm.vue'
import OccupationForm from './OccupationForm.vue'
import DocumentForm from './DocumentForm.vue'
import { useNuxtApp } from '#app'
import { usePersonStore } from '@/stores/person'
const { $api } = useNuxtApp()
import { useHouseStore } from '@/stores/house'
import AddParentModal from './AddParentModal.vue'
const emit = defineEmits(['close'])
const showAddFatherModal = ref(false)
const personStore = usePersonStore()
const personId = computed(() => personStore.person_id)
const houseStore = useHouseStore()
const activeTab = ref('personal')
const religions = ref([])
const denominations = ref([])
const fatherSearchText = ref('')
const fatherOptions = ref([])
const showAddMotherModal = ref(false)
const motherSearchText = ref('')
const motherOptions = ref([])
const photoFile = ref(null)


const memberData = ref({
  first_name: '',
  hnam_hming: '',
  gender: '',
  dob: '',
  blood_group: '',
  mobile: '',
  epic_number: '',
  aadhar_number: '',
  marital_status: '',
  religion_id: '',
  denomination_id: '',
  father_id: '',
  mother_id: '',
  rent_start_date: '',   
  rent_end_date: '', 
  is_househead: false
})
const handlePhotoUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    photoFile.value = file
  }
}

const fetchReligions = async () => {
  const response = await $api.get('/religion/')
  religions.value = response.data
}

const fetchDenominations = async () => {
  const response = await $api.get('/denomination/')
  denominations.value = response.data
}


const searchFather = async () => {
  if (!fatherSearchText.value || !houseStore.house_id) {
    fatherOptions.value = []
    return
  }
  try {
    const response = await $api.get(
      `/search/father/?house_id=${houseStore.house_id}&name=${fatherSearchText.value}`
    )
    fatherOptions.value = response.data
  } catch (error) {
    console.error('Failed to search father:', error)
  }
}

const searchMother = async () => {
  if (!motherSearchText.value || !houseStore.house_id) {
    motherOptions.value = []
    return
  }
  try {
    const response = await $api.get(
      `/search/mother/?house_id=${houseStore.house_id}&name=${motherSearchText.value}`
    )
    motherOptions.value = response.data
  } catch (error) {
    console.error('Failed to search mother:', error)
  }
}

const selectFather = (option) => {
  memberData.value.father_id = option.id
  fatherSearchText.value = `${option.first_name} ${option.hnam_hming || ''}`.trim()
  fatherOptions.value = []  // Hide options after selection
}



const selectMother = (option) => {
  memberData.value.mother_id = option.id
  motherSearchText.value = `${option.first_name} ${option.hnam_hming || ''}`.trim()
  motherOptions.value = []  // Hide options after selection
}


const handleNewFather = (newParent) => {
  fatherOptions.value.unshift(newParent)
  memberData.value.father_id = newParent.id
fatherSearchText.value = `${newParent.first_name || ''} ${newParent.hnam_hming || ''}`.trim()

}

const handleNewMother = (newParent) => {
  motherOptions.value.unshift(newParent)
  memberData.value.mother_id = newParent.id
motherSearchText.value = `${newParent.first_name || ''} ${newParent.hnam_hming || ''}`.trim()

}

const submitPersonalDetails = async () => {
  console.log('🔴 submitPersonalDetails() called – CHILD FORM SENDING DATA')
  if (!houseStore.house_id) {
    alert('House ID missing.')
    return
  }

  const formData = new FormData()
  formData.append('first_name', memberData.value.first_name)
  formData.append('hnam_hming', memberData.value.hnam_hming || '')
  formData.append('gender', memberData.value.gender)
  formData.append('dob', memberData.value.dob || '')
  formData.append('blood_group', memberData.value.blood_group || '')
  formData.append('mobile', memberData.value.mobile || '')
  formData.append('epic_number', memberData.value.epic_number || '')
  formData.append('aadhar_number', memberData.value.aadhar_number || '')
  formData.append('marital_status', memberData.value.marital_status || '')

  // Append IDs only if valid
  if (memberData.value.father_id) {
    formData.append('father_id', memberData.value.father_id)
  }
  if (memberData.value.mother_id) {
    formData.append('mother_id', memberData.value.mother_id)
  }
  if (memberData.value.religion_id) {
    formData.append('religion_id', memberData.value.religion_id)
  }
  if (memberData.value.denomination_id) {
    formData.append('denomination_id', memberData.value.denomination_id)
  }
  if (photoFile.value) {
  formData.append('photo', photoFile.value)
}


  formData.append('house_id', houseStore.house_id)
  formData.append('rent_start_date', memberData.value.rent_start_date || '')
  formData.append('rent_end_date', memberData.value.rent_end_date || '')
  formData.append('is_househead', memberData.value.is_househead ? 'true' : 'false')

  try {
    const response = await $api.post('/person/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    personStore.setPersonId(response.data.id)
    fetchHouseMembers();
    activeTab.value = 'qualifications'

    alert('Personal details saved.')
  } catch (error) {
    console.error('Failed to save personal details:', error)
    alert('Failed to save personal details.')
  }
}
const moveToOccupations = () => {
  activeTab.value = 'occupations'
}
const moveToDocuments = () => {
  activeTab.value = 'documents'
}
const handleDocumentFormClose = () => {
  fetchHouseMembers(); 
  emit('close')                       // ✅ Close the AddMemberDialog
  personStore.clearPersonId()         // ✅ Reset person_id
}


const fetchHouseMembers = async () => {
  if (!houseStore.house_id) return;
  try {
    const response = await $api.get(`/house/${houseStore.house_id}/members/`);
    houseStore.members = response.data;   // ✅ Shared via Pinia
  } catch (error) {
    console.error('Failed to fetch members:', error);
  }
};


onMounted(() => {
  fetchReligions()
  fetchDenominations()
})

const activeTabClass = 'whitespace-nowrap py-4 px-1 border-b-2 border-blue-500 font-medium text-sm text-blue-600'
const inactiveTabClass = 'whitespace-nowrap py-4 px-1 border-b-2 border-transparent font-medium text-sm text-gray-500 hover:text-gray-700 hover:border-gray-300'
</script>
