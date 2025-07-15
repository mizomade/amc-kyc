<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <h1 class="text-3xl font-bold text-gray-900 mb-6">Add New Entry</h1>

    <div class="bg-white p-6 rounded-lg shadow-md">
      <div class="border-b border-gray-200">
        <nav class="-mb-px flex space-x-8" aria-label="Tabs">
          <button @click="activeTab = 'house'"
            :class="['whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm', activeTab === 'house' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300']">
            House Details
          </button>
          <button @click="activeTab = 'members'"
            :class="['whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm', activeTab === 'members' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300']">
            Member List
          </button>
        </nav>
      </div>

      <div class="mt-6">
        <div v-if="activeTab === 'house'">
          <form @submit.prevent="submitHouseForm" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label for="house_number" class="block text-sm font-medium text-gray-700">House Number</label>
                <input type="text" id="house_number" v-model="houseData.house_number"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
              </div>
              <div>
                <label for="veng_id" class="block text-sm font-medium text-gray-700">Veng</label>
                <select id="veng_id" v-model="houseData.veng_id"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                  <option v-for="veng in vengs" :key="veng.id" :value="veng.id">{{ veng.name }}</option>
                </select>
              </div>
              <div>
                <label for="street" class="block text-sm font-medium text-gray-700">Street</label>
                <input type="text" id="street" v-model="houseData.street"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
              </div>
              <div>
                <label for="landmarks" class="block text-sm font-medium text-gray-700">Landmarks</label>
                <input type="text" id="landmarks" v-model="houseData.landmarks"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
              </div>
              <div>
                <label for="lsc_number" class="block text-sm font-medium text-gray-700">LSC Number</label>
                <input type="text" id="lsc_number" v-model="houseData.lsc_number"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
              </div>
              <div>
                <label for="awmtan_kum" class="block text-sm font-medium text-gray-700">Awm Tan Kum</label>
                <input type="number" id="awmtan_kum" v-model="houseData.awmtan_kum"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
              </div>
              <div>
                <label for="pem_luh_chhan" class="block text-sm font-medium text-gray-700">Pem Luh Chhan</label>
                <input type="text" id="pem_luh_chhan" v-model="houseData.pem_luh_chhan"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
              </div>
              <div>
                <label for="household_size" class="block text-sm font-medium text-gray-700">Household Size</label>
                <input type="number" id="household_size" v-model="houseData.household_size"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
              </div>
              <div>
                <label for="landlord_name" class="block text-sm font-medium text-gray-700">Landlord Name</label>
                <input type="text" id="landlord_name" v-model="houseData.landlord_name"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
              </div>
              <div>
                <label for="landlord_phone" class="block text-sm font-medium text-gray-700">Landlord Phone</label>
                <input type="text" id="landlord_phone" v-model="houseData.landlord_phone"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
              </div>
              <div>
                <label for="landlord_veng" class="block text-sm font-medium text-gray-700">Landlord Veng</label>
                <input type="text" id="landlord_veng" v-model="houseData.landlord_veng"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
              </div>
              <div>
                <label for="latitude" class="block text-sm font-medium text-gray-700">Latitude</label>
                <input type="number" step="any" id="latitude" v-model="houseData.latitude"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
              </div>
              <div>
                <label for="longitude" class="block text-sm font-medium text-gray-700">Longitude</label>
                <input type="number" step="any" id="longitude" v-model="houseData.longitude"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
              </div>
              <div v-if="houseData.is_tenant">
                <label for="parent_house_id" class="block text-sm font-medium text-gray-700">Parent House</label>
                <select id="parent_house_id" v-model="houseData.parent_house_id"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                  <option v-for="house in houses" :key="house.id" :value="house.id">{{ house.house_number }}</option>
                </select>
              </div>
               <div class="flex items-center">
                <input type="checkbox" id="is_owner" v-model="houseData.is_owner" class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500" />
                <label for="is_owner" class="ml-2 block text-sm text-gray-900">Is Owner</label>
              </div>
              <div class="flex items-center">
                <input type="checkbox" id="have_tenant" v-model="houseData.have_tenant" class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500" />
                <label for="have_tenant" class="ml-2 block text-sm text-gray-900">Have Tenant</label>
              </div>
              <div class="flex items-center">
                <input type="checkbox" id="is_tenant" v-model="houseData.is_tenant" class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500" />
                <label for="is_tenant" class="ml-2 block text-sm text-gray-900">Is Tenant</label>
              </div>
            </div>
            <div>
              <button type="submit"
                class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                Save House
              </button>
            </div>
          </form>
        </div>

        <div v-if="activeTab === 'members'">
          <div class="flex justify-end mb-4">
            <button @click="showAddMemberForm = true"
              class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
              Add New Member
            </button>
          </div>
          <div v-if="houseStore.members.length > 0">
            <ul class="divide-y divide-gray-200">
              <li v-for="member in houseStore.members" :key="member.id" class="py-4 flex">
                <div class="ml-3">
                  <p class="text-sm font-medium text-gray-900">{{ member.first_name }}</p>
                  <p class="text-sm text-gray-500">{{ member.hnam_hming }}</p>
                </div>
              </li>
            </ul>
          </div>
          <p v-else class="text-gray-700">No members found for this house.</p>
        </div>
      </div>
    </div>
    <AddMemberDialog v-if="showAddMemberForm" @close="showAddMemberForm = false" @submit="submitMemberForm" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useHouseStore } from '~/stores/house';
import AddMemberDialog from '~/components/AddMemberDialog.vue';

const activeTab = ref('house');
const showAddMemberForm = ref(false);
const vengs = ref([]);
const houses = ref([]);
const houseStore = useHouseStore();

const houseData = ref({
  house_number: '',
  parent_house_id: null,
  veng_id: null,
  street: '',
  landmarks: '',
  is_owner: true,
  lsc_number: '',
  awmtan_kum: null,
  pem_luh_chhan: '',
  have_tenant: false,
  household_size: null,
  is_tenant: false,
  landlord_name: '',
  landlord_phone: '',
  landlord_veng: '',
  latitude: null,
  longitude: null,
  household_head_id: null,
});

const fetchVengs = async () => {
  try {
    const response = await $fetch('http://localhost:8000/api/veng/');
    vengs.value = response;
  } catch (error) {
    console.error('Error fetching vengs:', error);
  }
};

const fetchHouses = async () => {
  try {
    const response = await $fetch('http://localhost:8000/api/house/');
    houses.value = response;
  } catch (error) {
    console.error('Error fetching houses:', error);
  }
};

const submitHouseForm = async () => {
  try {
    const response = await $fetch('http://localhost:8000/api/house/', {
      method: 'POST',
      body: houseData.value,
    });
    houseStore.setHouse(response);
    await houseStore.fetchMembers(response.id);
    console.log('House form submitted:', response);
    alert('House details saved!');
  } catch (error) {
    console.error('Error submitting house form:', error);
    alert('Failed to save house details.');
  }
};

const submitMemberForm = async (memberData) => {
  try {
    memberData.house_id = houseStore.house.id;
    const response = await $fetch('http://localhost:8000/api/person/', {
      method: 'POST',
      body: memberData,
    });
    houseStore.addMember(response);
    console.log('Member form submitted:', response);
    alert('Member added!');
    showAddMemberForm.value = false;
  } catch (error) {
    console.error('Error submitting member form:', error);
    alert('Failed to add member.');
  }
};

onMounted(() => {
  fetchVengs();
  fetchHouses();
});

definePageMeta({
  layout: 'admin',
  middleware: 'auth',
});
</script>

<style scoped>
/* Tailwind CSS handles most styling, no custom styles needed here */
</style>

