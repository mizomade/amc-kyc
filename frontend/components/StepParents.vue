<template>
  <div class="space-y-6">
    <h2 class="text-xl font-bold mb-4">Step 2: Father and Mother Details</h2>

    <!-- FATHER SECTION -->
    <div class="border p-4 rounded">
      <h3 class="text-lg font-semibold mb-2">Father</h3>
      <label class="block mb-2">Upload Photo</label>
        <input
          type="file"
          @change="onPhotoSelected($event, 'father')"
          accept="image/*"
          class="w-full mb-2 px-3 py-2 border rounded"
        />

      <input v-model="father.first_name" class="w-full mb-2 px-3 py-2 border rounded" placeholder="First Name" />
      <input v-model="father.hnam_hming" class="w-full mb-2 px-3 py-2 border rounded" placeholder="Surname (optional)" />
      <select v-model="father.gender" class="w-full mb-2 px-3 py-2 border rounded">
        <option value="">Select Gender</option>
        <option value="Male">Male</option>
        <option value="Female">Female</option>
        <option value="Transgender">Transgender</option>
        <option value="Other">Other</option>
      </select>

      <select v-model="father.religion_id" class="w-full mb-2 px-3 py-2 border rounded">
        <option value="">Religion</option>
        <option v-for="r in religions" :key="r.id" :value="r.id">{{ r.name }}</option>
      </select>

      <select v-model="father.denomination_id" class="w-full mb-2 px-3 py-2 border rounded">
        <option value="">Denomination</option>
        <option v-for="d in filteredDenominations(father.religion_id)" :key="d.id" :value="d.id">{{ d.name }}</option>
      </select>

      <input v-model="father.dob" type="date" class="w-full mb-2 px-3 py-2 border rounded" placeholder="Date of Birth" />
      <input v-model="father.blood_group" class="w-full mb-2 px-3 py-2 border rounded" placeholder="Blood Group" />
      <input v-model="father.epic_number" class="w-full mb-2 px-3 py-2 border rounded" placeholder="EPIC Number" />
      <input v-model="father.aadhar_number" class="w-full mb-2 px-3 py-2 border rounded" placeholder="Aadhar Number" />
      <input v-model="father.mobile" class="w-full mb-2 px-3 py-2 border rounded" placeholder="Mobile (optional)" />
    </div>

    <!-- MOTHER SECTION -->
    <div class="border p-4 rounded">
      <h3 class="text-lg font-semibold mb-2">Mother</h3>
      <label class="block mb-2">Upload Photo</label>
        <input
          type="file"
          @change="onPhotoSelected($event, 'mother')"
          accept="image/*"
          class="w-full mb-2 px-3 py-2 border rounded"
        />


      <input v-model="mother.first_name" class="w-full mb-2 px-3 py-2 border rounded" placeholder="First Name" />
      <input v-model="mother.hnam_hming" class="w-full mb-2 px-3 py-2 border rounded" placeholder="Surname (optional)" />
      <select v-model="mother.gender" class="w-full mb-2 px-3 py-2 border rounded">
        <option value="">Select Gender</option>
        <option value="Female">Female</option>
        <option value="Male">Male</option>
        <option value="Transgender">Transgender</option>
        <option value="Other">Other</option>
      </select>

      <select v-model="mother.religion_id" class="w-full mb-2 px-3 py-2 border rounded">
        <option value="">Religion</option>
        <option v-for="r in religions" :key="r.id" :value="r.id">{{ r.name }}</option>
      </select>

      <select v-model="mother.denomination_id" class="w-full mb-2 px-3 py-2 border rounded">
        <option value="">Denomination</option>
        <option v-for="d in filteredDenominations(mother.religion_id)" :key="d.id" :value="d.id">{{ d.name }}</option>
      </select>

      <input v-model="mother.dob" type="date" class="w-full mb-2 px-3 py-2 border rounded" placeholder="Date of Birth" />
      <input v-model="mother.blood_group" class="w-full mb-2 px-3 py-2 border rounded" placeholder="Blood Group" />
      <input v-model="mother.epic_number" class="w-full mb-2 px-3 py-2 border rounded" placeholder="EPIC Number" />
      <input v-model="mother.aadhar_number" class="w-full mb-2 px-3 py-2 border rounded" placeholder="Aadhar Number" />
      <input v-model="mother.mobile" class="w-full mb-2 px-3 py-2 border rounded" placeholder="Mobile (optional)" />
    </div>

    <!-- SUBMIT BUTTON -->
    <button
      @click="submitParents"
      class="mt-4 bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
    >
      Next
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useNuxtApp } from '#app'
import { useRouter } from 'vue-router'
import { useFamilyFormStore } from '@/stores/familyForm'

const { $axios } = useNuxtApp()
const store = useFamilyFormStore()
const router = useRouter()
const allDenominations = ref([])

const father = ref({
  first_name: '',
  hnam_hming: '',
  gender: 'Male',
  dob: '',
  blood_group: '',
  epic_number: '',
  aadhar_number: '',
  mobile: '',
  house_id: store.house_id,
  religion_id: '',
  denomination_id: '',
  photo: null,
})

const mother = ref({
  first_name: '',
  hnam_hming: '',
  gender: 'Female',
  dob: '',
  blood_group: '',
  epic_number: '',
  aadhar_number: '',
  mobile: '',
  house_id: store.house_id,
  religion_id: '',
  denomination_id: '',
  photo:null,
})
const fatherPhoto = ref(null)
const motherPhoto = ref(null)

const religions = ref([])

const onPhotoSelected = (event, type) => {
  const file = event.target.files[0]
  if (!file) return
  if (type === 'father') fatherPhoto.value = file
  if (type === 'mother') motherPhoto.value = file
}

const filteredDenominations = (religionId) => {
  if (!religionId) return []
  return allDenominations.value.filter(d => d.religion_id === religionId)
}

onMounted(async () => {
  const [religionRes, denomRes] = await Promise.all([
    $axios.get('/meta/religions/'),
    $axios.get('/meta/denominations/')
  ])
  religions.value = religionRes.data
  allDenominations.value = denomRes.data
})
const cleanPerson = (person) => {
  const cleaned = { ...person }
  if (!cleaned.denomination_id) {
    cleaned.denomination_id = null
  }
  if (!cleaned.religion_id) {
    cleaned.religion_id = null
  }
  return cleaned
}



const buildFormData = (person, photoFile) => {
  const formData = new FormData()
  for (const [key, value] of Object.entries(person)) {
    formData.append(key, value ?? '')
  }
  if (photoFile) {
    formData.append('photo', photoFile)
  }
  return formData
}

const submitParents = async () => {
  try {
    const fatherForm = buildFormData(father.value, fatherPhoto.value)
    const motherForm = buildFormData(mother.value, motherPhoto.value)

    const fatherRes = await $axios.post('/person/', fatherForm, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    const motherRes = await $axios.post('/person/', motherForm, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    store.setFatherId(fatherRes.data.id)
    store.setMotherId(motherRes.data.id)

    router.push('/family-entry/childrens')
  } catch (err) {
    console.error('Failed to save parents:', err)
    alert('Failed to submit parent info. Please check all fields.') //
  }
}


</script>
