<template>
  <div class="fixed z-50 inset-0 overflow-y-auto">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- <div class="fixed inset-0 transition-opacity" aria-hidden="true" @click="$emit('close')">
        <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
      </div> -->

      <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

      <div @click.stop class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full">
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <h3 class="text-lg leading-6 font-medium text-gray-900">Add New Member</h3>
          <div class="mt-2">
            <div class="border-b border-gray-200">
              <nav class="-mb-px flex space-x-8" aria-label="Tabs">
                <button @click="activeTab = 'personal'"
                  :class="['whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm', activeTab === 'personal' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300']">
                  Personal Details
                </button>
                <button @click="activeTab = 'qualifications'"
                  :class="['whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm', activeTab === 'qualifications' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300']">
                  Qualifications
                </button>
                <button @click="activeTab = 'occupations'"
                  :class="['whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm', activeTab === 'occupations' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300']">
                  Occupations
                </button>
                <button @click="activeTab = 'documents'"
                  :class="['whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm', activeTab === 'documents' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300']">
                  Documents
                </button>
              </nav>
            </div>

            <div class="mt-6 h-[60vh] overflow-y-auto">
              <div v-if="activeTab === 'personal'">
                <form @submit.prevent="submitForm" class="space-y-6">
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label for="first_name" class="block text-sm font-medium text-gray-700">First Name</label>
                      <input type="text" id="first_name" v-model="memberData.first_name"
                        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
                    </div>
                    <div>
                      <label for="hnam_hming" class="block text-sm font-medium text-gray-700">Hnam Hming</label>
                      <input type="text" id="hnam_hming" v-model="memberData.hnam_hming"
                        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
                    </div>
                    <div>
                      <label for="gender" class="block text-sm font-medium text-gray-700">Gender</label>
                      <input type="text" id="gender" v-model="memberData.gender"
                        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
                    </div>
                    <div>
                      <label for="dob" class="block text-sm font-medium text-gray-700">Date of Birth</label>
                      <input type="date" id="dob" v-model="memberData.dob"
                        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
                    </div>
                    <div>
                      <label for="blood_group" class="block text-sm font-medium text-gray-700">Blood Group</label>
                      <input type="text" id="blood_group" v-model="memberData.blood_group"
                        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
                    </div>
                    <div>
                      <label for="mobile" class="block text-sm font-medium text-gray-700">Mobile</label>
                      <input type="text" id="mobile" v-model="memberData.mobile"
                        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
                    </div>
                    <div>
                      <label for="epic_number" class="block text-sm font-medium text-gray-700">EPIC Number</label>
                      <input type="text" id="epic_number" v-model="memberData.epic_number"
                        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
                    </div>
                    <div>
                      <label for="aadhar_number" class="block text-sm font-medium text-gray-700">Aadhar Number</label>
                      <input type="text" id="aadhar_number" v-model="memberData.aadhar_number"
                        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
                    </div>
                    <div>
                      <label for="marital_status" class="block text-sm font-medium text-gray-700">Marital Status</label>
                      <input type="text" id="marital_status" v-model="memberData.marital_status"
                        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
                    </div>
                    <div>
                      <label for="religion_id" class="block text-sm font-medium text-gray-700">Religion</label>
                      <select id="religion_id" v-model="memberData.religion_id"
                        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                        <option v-for="religion in religions" :key="religion.id" :value="religion.id">{{ religion.name }}</option>
                      </select>
                    </div>
                    <div>
                      <label for="denomination_id" class="block text-sm font-medium text-gray-700">Denomination</label>
                      <select id="denomination_id" v-model="memberData.denomination_id"
                        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                        <option v-for="denomination in denominations" :key="denomination.id" :value="denomination.id">{{ denomination.name }}</option>
                      </select>
                    </div>
                    <div>
                      <label for="role_id" class="block text-sm font-medium text-gray-700">Role</label>
                      <select id="role_id" v-model="memberData.role_id"
                        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                        <option v-for="role in roles" :key="role.id" :value="role.id">{{ role.name }}</option>
                      </select>
                    </div>
                  </div>
                  <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                    <button type="submit" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm">
                      Save
                    </button>
                    <button @click="$emit('close')" type="button" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
                      Cancel
                    </button>
                  </div>
                </form>
              </div>
              <div v-if="activeTab === 'qualifications'">
                <QualificationForm @submit="submitQualificationForm" />
              </div>
              <div v-if="activeTab === 'occupations'">
                <OccupationForm @submit="submitOccupationForm" />
              </div>
              <div v-if="activeTab === 'documents'">
                <DocumentForm @submit="submitDocumentForm" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import QualificationForm from './QualificationForm.vue';
import OccupationForm from './OccupationForm.vue';
import DocumentForm from './DocumentForm.vue';

const emit = defineEmits(['close', 'submit']);

const activeTab = ref('personal');
const religions = ref([]);
const denominations = ref([]);
const roles = ref([]);

const memberData = ref({
  first_name: '',
  hnam_hming: '',
  gender: '',
  dob: null,
  blood_group: '',
  mobile: '',
  epic_number: '',
  aadhar_number: '',
  marital_status: '',
  father_id: null,
  mother_id: null,
  spouse_id: null,
  religion_id: null,
  denomination_id: null,
  role_id: null,
});

const fetchReligions = async () => {
  try {
    const response = await $fetch('http://localhost:8000/api/religion/');
    religions.value = response;
  } catch (error) {
    console.error('Error fetching religions:', error);
  }
};

const fetchDenominations = async () => {
  try {
    const response = await $fetch('http://localhost:8000/api/denomination/');
    denominations.value = response;
  } catch (error) {
    console.error('Error fetching denominations:', error);
  }
};

const fetchRoles = async () => {
  try {
    const response = await $fetch('http://localhost:8000/api/role/');
    roles.value = response;
  } catch (error) {
    console.error('Error fetching roles:', error);
  }
};

const submitForm = () => {
  emit('submit', memberData.value);
};

const submitQualificationForm = async (qualificationData) => {
  try {
    qualificationData.person_id = memberData.value.id;
    const response = await $fetch('http://localhost:8000/api/qualifications/', {
      method: 'POST',
      body: qualificationData,
    });
    console.log('Qualification form submitted:', response);
    alert('Qualification details saved!');
  } catch (error) {
    console.error('Error submitting qualification form:', error);
    alert('Failed to save qualification details.');
  }
};

const submitOccupationForm = async (occupationData) => {
  try {
    occupationData.person_id = memberData.value.id;
    const response = await $fetch('http://localhost:8000/api/occupations/', {
      method: 'POST',
      body: occupationData,
    });
    console.log('Occupation form submitted:', response);
    alert('Occupation details saved!');
  } catch (error) {
    console.error('Error submitting occupation form:', error);
    alert('Failed to save occupation details.');
  }
};

const submitDocumentForm = async (documentData) => {
  try {
    documentData.person_id = memberData.value.id;
    const response = await $fetch('http://localhost:8000/api/attachments/', {
      method: 'POST',
      body: documentData,
    });
    console.log('Document form submitted:', response);
    alert('Document details saved!');
  } catch (error) {
    console.error('Error submitting document form:', error);
    alert('Failed to save document details.');
  }
};

onMounted(() => {
  fetchReligions();
  fetchDenominations();
  fetchRoles();
});
</script>
