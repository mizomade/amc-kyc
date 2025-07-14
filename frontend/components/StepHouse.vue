<template>
  <div class="space-y-4">
    <h2 class="text-xl font-bold">Step 1: House Details</h2>

    <!-- House Number -->
    <input
      v-model="store.house.house_number"
      class="w-full px-3 py-2 border rounded"
      placeholder="House Number" required
    />
<!-- Parent House Search -->
<div class="relative">
  <input
    type="text"
    v-model="selectedParentHouseText"
    @input="fetchHouseOptions"
    placeholder="Search Parent House"
    class="w-full px-3 py-2 border rounded"
  />
  <div
    v-if="parentHouseOptions.length && !selectedParentHouse"
    class="absolute z-10 bg-white border w-full rounded shadow max-h-60 overflow-auto"
  >
    <div
      v-for="house in parentHouseOptions"
      :key="house.id"
      @click="selectParentHouse(house)"
      class="px-3 py-2 hover:bg-blue-100 cursor-pointer"
    >
      {{ house.house_number }}
    </div>
  </div>

  <!-- Clear Button inside input -->
  <div
    v-if="selectedParentHouse"
    class="absolute right-2 top-1/2 -translate-y-1/2 cursor-pointer text-red-500 text-sm"
    @click="clearParentHouse"
  >
    ✕
  </div>
</div>


    <!-- Veng Dropdown -->
    <select v-model="store.house.veng_id" class="w-full px-3 py-2 border rounded">
      <option :value="null" disabled>Select Veng</option>
      <option v-for="v in vengs" :key="v.id" :value="v.id">{{ v.name }}</option>
    </select>


    <!-- Street, Landmark -->
    <input v-model="store.house.street" class="w-full px-3 py-2 border rounded" placeholder="Street" />
    <input v-model="store.house.landmarks" class="w-full px-3 py-2 border rounded" placeholder="Landmarks" />
    <input v-model="store.house.lsc_number" class="w-full px-3 py-2 border rounded" placeholder="LSC Number" />
    <input v-model="store.house.awmtan_kum" type="number" class="w-full px-3 py-2 border rounded" placeholder="Awmtan Kum" />
    <input v-model="store.house.pem_luh_chhan" class="w-full px-3 py-2 border rounded" placeholder="Pem Luh Chhan" />
    <input v-model="store.house.household_size" type="number" class="w-full px-3 py-2 border rounded" placeholder="Household Size" />
    <!-- Coordinates (Moved Up) -->
    <input v-model="store.house.latitude" type="number" class="w-full px-3 py-2 border rounded" placeholder="Latitude" />
    <input v-model="store.house.longitude" type="number" class="w-full px-3 py-2 border rounded" placeholder="Longitude" />

    <!-- House Status Checkboxes -->
    <div class="flex flex-col gap-2 text-sm">
      <label class="flex items-center gap-2">
        <input type="checkbox" v-model="store.house.is_owner" @change="handleOwnerChange" />
        Is Owner?
      </label>
      <label class="flex items-center gap-2">
        <input type="checkbox" v-model="store.house.have_tenant" @change="handleTenantChange" />
        Have Tenant?
      </label>
      <label class="flex items-center gap-2">
        <input type="checkbox" v-model="store.house.is_tenant" @change="handleIsTenantChange" />
        Is Tenant?
      </label>
    </div>

    <!-- Conditional: Landlord Info if is_tenant is checked -->
    <div v-if="store.house.is_tenant" class="pt-2 space-y-2">
      <input v-model="store.house.landlord_name" class="w-full px-3 py-2 border rounded" placeholder="Landlord Name" />
      <input v-model="store.house.landlord_phone" class="w-full px-3 py-2 border rounded" placeholder="Landlord Phone" />
      <input v-model="store.house.landlord_veng" class="w-full px-3 py-2 border rounded" placeholder="Landlord Veng" />
    </div>

  
  </div>
  <!-- Next Button -->
<button
  @click="submitHouse"
  class="mt-6 bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
>
  Next
</button>
</template>

<script setup>
import { useFamilyFormStore } from '@/stores/familyForm'
import { onMounted, ref } from 'vue'
import { useNuxtApp } from '#app'
import { useRouter } from 'vue-router'
const router = useRouter()
const store = useFamilyFormStore()
const { $axios } = useNuxtApp()

const vengs = ref([])
const selectedParentHouse = ref(null)
const selectedParentHouseText = ref('')
const searchText = ref('')
const parentHouseOptions = ref([])

onMounted(async () => {
  const res = await $axios.get('/veng/')
  vengs.value = res.data
})

const fetchHouseOptions = async () => {
  const search = selectedParentHouseText.value
  if (search.length < 2) {
    parentHouseOptions.value = []
    return
  }
  const res = await $axios.get('/search/house/', {
    params: { search }
  })
  parentHouseOptions.value = res.data
}

const selectParentHouse = (house) => {
  store.house.parent_house_id = house.id
  selectedParentHouse.value = house
  selectedParentHouseText.value = house.house_number
  parentHouseOptions.value = []
}

const clearParentHouse = () => {
  store.house.parent_house_id = null
  selectedParentHouse.value = null
  selectedParentHouseText.value = ''
}

// 🧠 Checkbox Logic
const handleIsTenantChange = () => {
  if (store.house.is_tenant) {
    store.house.is_owner = false
    store.house.have_tenant = false
  }
}
const handleOwnerChange = () => {
  if (store.house.is_owner && store.house.is_tenant) {
    store.house.is_tenant = false
  }
}
const handleTenantChange = () => {
  if (store.house.have_tenant && store.house.is_tenant) {
    store.house.is_tenant = false
  }
}


const submitHouse = async () => {
  if (!store.house.house_number || store.house.house_number.trim()===''){
    
    return
  }
  try {
    const response = await $axios.post('/house/', store.house)
    store.setHouseId(response.data.id)
    router.push('/family-entry/parents') // Step 2 route
  } catch (error) {
    console.error('Failed to create house:', error)
    alert('Failed to submit house. Check all fields and try again.')
  }
}
</script>
