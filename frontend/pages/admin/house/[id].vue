<template>
  <div class="container mx-auto p-6 bg-gray-100 min-h-screen">
    <div class="relative mb-8">
      <button @click="goBack" class="absolute top-0 left-0  hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded-lg  flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
        </svg>
        Back
      </button>
      <h1 class="text-3xl font-extrabold text-gray-800 text-center">House Details</h1>
    </div>

    <div v-if="house" class="space-y-8">
      <!-- House Information Card -->
      <div class="bg-white shadow-lg rounded-xl p-8">
        <h2 class="text-2xl font-bold text-gray-700 mb-6 border-b pb-3">House Information</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-4">
          <DetailItem label="House Number" :value="house.house_number" />
          <DetailItem label="Veng" :value="house.veng ? house.veng.name : 'N/A'" />
          <DetailItem label="Street" :value="house.street" />
          <DetailItem label="Landmarks" :value="house.landmarks" />
          <DetailItem label="Is Owner" :value="house.is_owner ? 'Yes' : 'No'" />
          <DetailItem label="Have Tenant" :value="house.have_tenant ? 'Yes' : 'No'" />
          <DetailItem label="Is Tenant" :value="house.is_tenant ? 'Yes' : 'No'" />
          <DetailItem label="LSC Number" :value="house.lsc_number" />
          <DetailItem label="Awmtan Kum" :value="house.awmtan_kum" />
          <DetailItem label="Pem Luh Chhan" :value="house.pem_luh_chhan" />
          <DetailItem label="Household Size" :value="house.household_size" />
          <DetailItem label="Landlord Name" :value="house.landlord_name" />
          <DetailItem label="Landlord Phone" :value="house.landlord_phone" />
          <DetailItem label="Landlord Veng" :value="house.landlord_veng" />
          <DetailItem label="Latitude" :value="house.latitude" />
          <DetailItem label="Longitude" :value="house.longitude" />
          <DetailItem label="Parent House" :value="house.parent_house ? house.parent_house.house_number : 'N/A'" />
        </div>
        <div class="mt-6 text-center">
          <button @click="showMapModal = true" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg shadow-md transition duration-300 ease-in-out">
            Show Location on Map
          </button>
        </div>

      </div>

      <!-- Members Card -->
      <div v-if="house.members && house.members.length > 0" class="bg-white shadow-lg rounded-xl p-8">
        <h2 class="text-2xl font-bold text-gray-700 mb-6 border-b pb-3">House Members</h2>
        <ul class="space-y-3">
          <li v-for="member in house.members" :key="member.id" class="bg-gray-50 p-4 rounded-lg shadow-sm border border-gray-200 hover:bg-gray-100 transition duration-200 ease-in-out">
            <NuxtLink :to="`/admin/person/${member.id}`" class="block text-blue-600 hover:underline text-lg font-medium">
              {{ member.first_name }} {{ member.hnam_hming }}
            </NuxtLink>
          </li>
        </ul>
      </div>
      <div v-else class="bg-white shadow-lg rounded-xl p-8">
        <h2 class="text-2xl font-bold text-gray-700 mb-6 border-b pb-3">House Members</h2>
        <p class="text-gray-600">No members found for this house.</p>
      </div>

      <!-- Tenants Card -->
      <div v-if="house.tenants && house.tenants.length > 0" class="bg-white shadow-lg rounded-xl p-8">
        <h2 class="text-2xl font-bold text-gray-700 mb-6 border-b pb-3">Tenant Houses</h2>
        <ul class="space-y-3">
          <li v-for="tenant in house.tenants" :key="tenant.id" class="bg-gray-50 p-4 rounded-lg shadow-sm border border-gray-200 hover:bg-gray-100 transition duration-200 ease-in-out">
            <NuxtLink :to="`/admin/house/${tenant.id}`" class="block text-blue-600 hover:underline text-lg font-medium">
              {{ tenant.house_number }}
            </NuxtLink>
          </li>
        </ul>
      </div>
      <div v-else class="bg-white shadow-lg rounded-xl p-8">
        <h2 class="text-2xl font-bold text-gray-700 mb-6 border-b pb-3">Tenants</h2>
        <p class="text-gray-600">No tenants found for this house.</p>
      </div>

      <!-- Maids Card -->
      <div v-if="house.maids && house.maids.length > 0" class="bg-white shadow-lg rounded-xl p-8">
        <h2 class="text-2xl font-bold text-gray-700 mb-6 border-b pb-3">House Maids</h2>
        <ul class="space-y-3">
          <li v-for="maid in house.maids" :key="maid.id" class="bg-gray-50 p-4 rounded-lg shadow-sm border border-gray-200">
            <p class="text-lg font-medium">{{ maid.name }}</p>
            <p class="text-gray-600">Veng: {{ maid.veng }}</p>
            <p class="text-gray-600">Phone: {{ maid.phone_number || 'N/A' }}</p>
          </li>
        </ul>
      </div>
      <div v-else class="bg-white shadow-lg rounded-xl p-8">
        <h2 class="text-2xl font-bold text-gray-700 mb-6 border-b pb-3">House Maids</h2>
        <p class="text-gray-600">No maids found for this house.</p>
      </div>

      <!-- Verification Details Card -->
      <div class="bg-white shadow-lg rounded-xl p-8">
        <h2 class="text-2xl font-bold text-gray-700 mb-6 border-b pb-3">Verification Details</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-4">
          <DetailItem label="Is Verified" :value="house.is_verified ? 'Yes' : 'No'" />
          <DetailItem label="Verified By" :value="house.verified_by" />
          <DetailItem label="Verified At" :value="house.verified_at" />
          <DetailItem label="Verification Remarks" :value="house.verification_remarks" />
          <DetailItem label="Created At" :value="house.created_at" />
          <DetailItem label="Updated At" :value="house.updated_at" />
          <DetailItem label="Rent Start Date" :value="house.rent_start_date" />
          <DetailItem label="Rent End Date" :value="house.rent_end_date" />
        </div>
      </div>
    </div>

    <div v-else class="text-center text-gray-600 text-xl mt-16 p-8 bg-white shadow-lg rounded-xl">
      Loading house details or house not found...
    </div>

    <!-- Map Modal Component -->
    <MapModal
      :show="showMapModal"
      :latitude="house ? house.latitude : null"
      :longitude="house ? house.longitude : null"
      :houseNumber="house ? house.house_number : ''"
      @close="showMapModal = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter, useNuxtApp } from '#app';
import DetailItem from '~/components/DetailItem.vue';
import MapModal from '~/components/MapModal.vue';


const showMap = ref(false)

definePageMeta({
  layout: 'admin',
  middleware: 'auth',
});


const house = ref(null);
const route = useRoute();
const router = useRouter();
const { $api } = useNuxtApp();
const showMapModal = ref(false);

const goBack = () => {
  router.back();
};

onMounted(async () => {
  try {
    const houseId = route.params.id;
    const response = await $api.get(`/house/details/${houseId}`);
    house.value = response.data;
  } catch (error) {
    console.error('Error fetching house details:', error);
    house.value = null;
  }
});
</script>

<style scoped>
/* Add any component-specific styles here if needed */
</style>