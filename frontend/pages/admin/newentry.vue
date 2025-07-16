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
                <!-- Parent House Search -->
                      <div>
                        <label for="parent_house_id" class="block text-sm font-medium text-gray-700">Parent House</label>
                        <div class="relative">
                          <input
                            type="text"
                            v-model="selectedParentHouseText"
                            @input="fetchHouseOptions"
                            placeholder="Search Parent House"
                            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                          />

                          <!-- Dropdown List -->
                          <div
                            v-if="parentHouseOptions.length && !selectedParentHouse"
                            class="absolute z-10 bg-white border w-full rounded-md shadow max-h-60 overflow-auto mt-1"
                          >
                            <div
                              v-for="house in parentHouseOptions"
                              :key="house.id"
                              @click="selectParentHouse(house)"
                              class="px-4 py-2 hover:bg-blue-100 cursor-pointer text-sm"
                            >
                              {{ house.house_number }}
                            </div>
                          </div>

                          <!-- Clear Button -->
                          <div
                            v-if="selectedParentHouse"
                            class="absolute right-3 top-1/2 -translate-y-1/2 cursor-pointer text-red-500 text-lg"
                            @click="clearParentHouse"
                          >
                            ×
                          </div>
                        </div>
                      </div>


              </div>
                 <!-- Is Owner -->
<div class="flex items-center">
  <input
    type="checkbox"
    id="is_owner"
    :checked="houseData.is_owner"
    @change="toggleOwner"
    class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
  />
  <label for="is_owner" class="ml-2 block text-sm text-gray-900">Is Owner</label>
</div>

<!-- Have Tenant -->
<div class="flex items-center">
  <input
    type="checkbox"
    id="have_tenant"
    :checked="houseData.have_tenant"
    @change="toggleHaveTenant"
    class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
  />
  <label for="have_tenant" class="ml-2 block text-sm text-gray-900">Have Tenant</label>
</div>

<!-- Is Tenant -->
<div class="flex items-center">
  <input
    type="checkbox"
    id="is_tenant"
    :checked="houseData.is_tenant"
    @change="toggleTenant"
    class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
  />
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

              <!-- Set max height with overflow scroll -->
              <div class="max-h-80 overflow-y-auto border rounded-lg">
                <div v-if="houseStore.members.length > 0">
                  <ul class="divide-y divide-gray-200">
                    <li v-for="member in houseStore.members" :key="member.id" class="py-2 px-4 flex items-center">
                      <p class="text-sm font-medium text-gray-900 truncate">
                        {{ member.first_name }} {{ member.hnam_hming }}
                      </p>
                    </li>
                  </ul>
                </div>
                <p v-else class="text-gray-700 p-4">No members found for this house.</p>
              </div>
            </div>

      </div>
    </div>
    <AddMemberDialog v-if="showAddMemberForm" @close="handleAddMemberClose"   />
  </div>
</template>

<script setup>
import { useNuxtApp } from '#app';
import { useHouseStore } from '@/stores/house';  
import { ref } from 'vue';
import { usePersonStore } from '@/stores/person'
const vengs = ref([]);
const houses = ref([]);
const activeTab = ref('house');          
const showAddMemberForm = ref(false); 
const selectedParentHouseText = ref('');
const selectedParentHouse = ref(null);
const parentHouseOptions = ref([]);

const { $api } = useNuxtApp();
const houseStore = useHouseStore();

const personStore = usePersonStore()
const houseData = ref({
  house_number: '',
  parent_house_id: null,
  veng_id: null,
  street: '',
  landmarks: '',
  is_owner: false,
  lsc_number: null,
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
  household_head_id: null,  // In case you're using it
});

const submitHouseForm = async () => {
  try {
    const response = await $api.post('/house/', houseData.value);

    houseStore.house_id = response.data.id;

    console.log('House created successfully, ID:', response.data.id);

    await fetchMembers();  // <-- fetch members after saving house

  } catch (error) {
    console.error('Failed to create house:', error);
  }
};

// Fetch members for the current house
const fetchMembers = async () => {
  if (!houseStore.house_id) return;

  try {
    const response = await $api.get(`/house/${houseStore.house_id}/members/`);
    houseStore.members = response.data;  // Update members in Pinia store
  } catch (error) {
    console.error('Failed to fetch members:', error);
    houseStore.members = [];
  }
};

const fetchVengs = async () => {
  try {
    const response = await $api.get('/veng/');
    vengs.value = response.data;
  } catch (error) {
    console.error('Failed to fetch vengs:', error);
  }
};
function fetchHouseOptions() {
  if (selectedParentHouseText.value.trim() === '') {
    parentHouseOptions.value = [];
    return;
  }

  $api.get('/search/house/', {
    params: { search: selectedParentHouseText.value }
  })
    .then((response) => {
      parentHouseOptions.value = response.data;
    })
    .catch(() => {
      parentHouseOptions.value = [];
    });
}

// Select House
function selectParentHouse(house) {
  selectedParentHouse.value = house;
  selectedParentHouseText.value = house.house_number;
  houseData.value.parent_house_id = house.id;
  parentHouseOptions.value = [];
}

// Clear Selection
function clearParentHouse() {
  selectedParentHouse.value = null;
  selectedParentHouseText.value = '';
  houseData.value.parent_house_id = null;
}

function toggleOwner() {
  houseData.value.is_owner = !houseData.value.is_owner;
  if (houseData.value.is_owner) {
    houseData.value.is_tenant = false;
  }
}

function toggleHaveTenant() {
  houseData.value.have_tenant = !houseData.value.have_tenant;
  if (houseData.value.have_tenant) {
    houseData.value.is_tenant = false;
  }
}

function toggleTenant() {
  houseData.value.is_tenant = !houseData.value.is_tenant;
  if (houseData.value.is_tenant) {
    houseData.value.is_owner = false;
    houseData.value.have_tenant = false;
  }
}
const handleAddMemberClose = () => {
  showAddMemberForm.value = false;
  personStore.clearPersonId();
  fetchHouseMembers();
}


watch(activeTab, (newTab) => {
  if (newTab === 'members' && houseStore.house_id) {
    fetchMembers();
  }
});
onMounted(() => {
  fetchVengs();
  fetchHouseOptions();

});
definePageMeta({
  layout: 'admin',
  middleware: 'auth',
});
</script>




<style scoped>
/* Tailwind CSS handles most styling, no custom styles needed here */
</style>

