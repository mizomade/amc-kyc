<template>
  <div>
    <h2 class="text-xl font-bold mb-4">Step 3: Children & Grandchildren</h2>

    <div
      v-for="(child, index) in children"
      :key="index"
      class="mb-6 p-4 border rounded space-y-4 relative"
      
    >
      
      <h3 class="font-semibold text-lg">Child {{ index + 1 }}</h3>
      <button 
      @click="removeChild(index)" 
      class="absolute top-2 right-2 text-red-500 text-2xl font-bold"
>
  &times;
</button>
 
<input
  type="file"
  @change="onPhotoSelected($event, index, 'child')"
  accept="image/*"
  class="w-full px-3 py-2 border rounded"
/>

      <!-- FATHER SEARCH -->
<div class="relative">
  <input
    v-model="child.searchFather"
    @input="searchFather(index)"
    placeholder="Search Father"
    class="w-full px-3 py-2 border rounded"
  />
  <div
    v-if="child.fatherOptions.length"
    class="absolute z-10 bg-white border w-full rounded shadow max-h-48 overflow-auto"
  >
    <div
      v-for="p in child.fatherOptions"
      :key="p.id"
      @click="selectFather(index, p)"
      class="px-3 py-2 hover:bg-blue-100 cursor-pointer"
    >
      {{ p.first_name }} {{ p.hnam_hming }}
    </div>
  </div>
  <div v-if="child.father_id" class="text-sm text-gray-600 mt-1">
    Selected: {{ child.selectedFather?.first_name }} {{ child.selectedFather?.hnam_hming }}
    <button @click="clearFather(index)" class="text-red-500 ml-2 text-xs">Clear</button>
  </div>
</div>

<!-- MOTHER SEARCH -->
<div class="relative">
  <input
    v-model="child.searchMother"
    @input="searchMother(index)"
    placeholder="Search Mother"
    class="w-full px-3 py-2 border rounded"
  />
  <div
    v-if="child.motherOptions.length"
    class="absolute z-10 bg-white border w-full rounded shadow max-h-48 overflow-auto"
  >
    <div
      v-for="p in child.motherOptions"
      :key="p.id"
      @click="selectMother(index, p)"
      class="px-3 py-2 hover:bg-blue-100 cursor-pointer"
    >
      {{ p.first_name }} {{ p.hnam_hming }}
    </div>
  </div>
  <div v-if="child.mother_id" class="text-sm text-gray-600 mt-1">
    Selected: {{ child.selectedMother?.first_name }} {{ child.selectedMother?.hnam_hming }}
    <button @click="clearMother(index)" class="text-red-500 ml-2 text-xs">Clear</button>
  </div>
</div>

      <input v-model="child.first_name" class="w-full px-3 py-2 border rounded" placeholder="First Name" />
      <input v-model="child.hnam_hming" class="w-full px-3 py-2 border rounded" placeholder="Surname (optional)" />
      <select v-model="child.gender" class="w-full px-3 py-2 border rounded">
        <option disabled value="">Select Gender</option>
        <option>Male</option>
        <option>Female</option>
        <option>Transgender</option>
        <option>Other</option>
      </select>
      <input v-model="child.dob" type="date" class="w-full px-3 py-2 border rounded" placeholder="DOB" />
      <input v-model="child.blood_group" class="w-full px-3 py-2 border rounded" placeholder="Blood Group" />
      <input v-model="child.epic_number" class="w-full px-3 py-2 border rounded" placeholder="EPIC Number" />
      <input v-model="child.aadhar_number" class="w-full px-3 py-2 border rounded" placeholder="Aadhar Number" />
      <select v-model="child.religion_id" class="w-full px-3 py-2 border rounded">
        <option value="">Select Religion</option>
        <option v-for="r in religions" :key="r.id" :value="r.id">{{ r.name }}</option>
      </select>
<select
  v-model="child.denomination_id"
  :disabled="getDenominationsForReligion(child.religion_id).length === 0"
  @change="onDenominationChanged(child)"
  class="w-full px-3 py-2 border rounded"
>
  <option value="">Select Denomination</option>
  <option
    v-for="d in getDenominationsForReligion(child.religion_id)"
    :key="d.id"
    :value="d.id"
  >
    {{ d.name }}
  </option>
</select>



      <!-- SPOUSE TOGGLE -->
      <label class="flex items-center space-x-2">
        <input type="checkbox" v-model="child.hasSpouse" />
        <span>Add Spouse</span>
      </label>

      <!-- SPOUSE FORM -->
      <div v-if="child.hasSpouse" class="pl-4 border-l-2 space-y-2 ">
          <div class="relative">
    <h4 class="text-sm font-medium">Spouse Details</h4>
    <button
      @click="clearSpouse(index)"
      class="absolute top-0 right-0 text-red-500 text-2xl font-bold"
    >
      &times;
    </button>
  </div>
        
                <input
          type="file"
          @change="onPhotoSelected($event, index, 'spouse')"
          accept="image/*"
          class="w-full px-3 py-2 border rounded"
        />

        <input v-model="child.spouse.first_name" class="w-full px-3 py-2 border rounded" placeholder="First Name" />
        <input v-model="child.spouse.hnam_hming" class="w-full px-3 py-2 border rounded" placeholder="Surname (optional)" />
        <select v-model="child.spouse.gender" class="w-full px-3 py-2 border rounded">
          <option disabled value="">Select Gender</option>
          <option>Male</option>
          <option>Female</option>
          <option>Transgender</option>
          <option>Other</option>
        </select>
        <input v-model="child.spouse.dob" type="date" class="w-full px-3 py-2 border rounded" placeholder="DOB" />
        <input v-model="child.spouse.blood_group" class="w-full px-3 py-2 border rounded" placeholder="Blood Group" />
        <input v-model="child.spouse.epic_number" class="w-full px-3 py-2 border rounded" placeholder="EPIC Number" />
        <input v-model="child.spouse.aadhar_number" class="w-full px-3 py-2 border rounded" placeholder="Aadhar Number" />
        <select v-model="child.spouse.religion_id" class="w-full px-3 py-2 border rounded">
          <option  value="">Select Religion</option>
          <option v-for="r in religions" :key="r.id" :value="r.id">{{ r.name }}</option>
        </select>
<select
  v-model="child.spouse.denomination_id"
  :disabled="getDenominationsForReligion(child.spouse.religion_id).length === 0"
  @change="onDenominationChanged(child.spouse)"
  class="w-full px-3 py-2 border rounded"
>
  <option value="">Select Denomination</option>
  <option
    v-for="d in getDenominationsForReligion(child.spouse.religion_id)"
    :key="d.id"
    :value="d.id"
  >
    {{ d.name }}
  </option>
</select>



        <!-- GRANDCHILDREN -->
        <div class="space-y-3">
          <h5 class="text-sm font-semibold">Grandchildren</h5>
          
          <div
            v-for="(g, gIndex) in child.grandchildren"
            :key="gIndex"
            class="pl-4 border-l space-y-2 relative bg-white p-4 rounded"
          >
            <h3 class="font-semibold text-lg">Grandchildren {{ gIndex + 1 }}</h3>
          <button
            @click="removeGrandchild(index, gIndex)"
            class="absolute top-0 right-0 text-red-500 text-xl font-bold"
          >
            &times;
          </button>


          
                <input
        type="file"
        @change="onPhotoSelected($event, index, 'grandchild', gIndex)"
        accept="image/*"
        class="w-full px-3 py-2 border rounded"
      />

        <!-- FATHER SEARCH -->
<div class="relative">
  <input
    v-model="child.searchFather"
    @input="searchFather(index)"
    placeholder="Search Father"
    class="w-full px-3 py-2 border rounded"
  />
  <div
    v-if="child.fatherOptions.length"
    class="absolute z-10 bg-white border w-full rounded shadow max-h-48 overflow-auto"
  >
    <div
      v-for="p in child.fatherOptions"
      :key="p.id"
      @click="selectFather(index, p)"
      class="px-3 py-2 hover:bg-blue-100 cursor-pointer"
    >
      {{ p.first_name }} {{ p.hnam_hming }}
    </div>
  </div>
  <div v-if="child.father_id" class="text-sm text-gray-600 mt-1">
    Selected: {{ child.selectedFather?.first_name }} {{ child.selectedFather?.hnam_hming }}
    <button @click="clearFather(index)" class="text-red-500 ml-2 text-xs">Clear</button>
  </div>
</div>

<!-- MOTHER SEARCH -->
<div class="relative">
  <input
    v-model="child.searchMother"
    @input="searchMother(index)"
    placeholder="Search Mother"
    class="w-full px-3 py-2 border rounded"
  />
  <div
    v-if="child.motherOptions.length"
    class="absolute z-10 bg-white border w-full rounded shadow max-h-48 overflow-auto"
  >
    <div
      v-for="p in child.motherOptions"
      :key="p.id"
      @click="selectMother(index, p)"
      class="px-3 py-2 hover:bg-blue-100 cursor-pointer"
    >
      {{ p.first_name }} {{ p.hnam_hming }}
    </div>
  </div>
  <div v-if="child.mother_id" class="text-sm text-gray-600 mt-1">
    Selected: {{ child.selectedMother?.first_name }} {{ child.selectedMother?.hnam_hming }}
    <button @click="clearMother(index)" class="text-red-500 ml-2 text-xs">Clear</button>
  </div>
</div>

            <input v-model="g.first_name" class="w-full px-3 py-2 border rounded" placeholder="First Name" />
            <input v-model="g.hnam_hming" class="w-full px-3 py-2 border rounded" placeholder="Surname (optional)" />
            <select v-model="g.gender" class="w-full px-3 py-2 border rounded">
              <option disabled value="">Select Gender</option>
              <option>Male</option>
              <option>Female</option>
              <option>Transgender</option>
              <option>Other</option>
            </select>
            <input v-model="g.dob" type="date" class="w-full px-3 py-2 border rounded" placeholder="DOB" />
            <input v-model="g.blood_group" class="w-full px-3 py-2 border rounded" placeholder="Blood Group" />
            <input v-model="g.epic_number" class="w-full px-3 py-2 border rounded" placeholder="EPIC Number" />
            <input v-model="g.aadhar_number" class="w-full px-3 py-2 border rounded" placeholder="Aadhar Number" />
            <select v-model="g.religion_id" class="w-full px-3 py-2 border rounded">
              <option value="">Select Religion</option>
              <option v-for="r in religions" :key="r.id" :value="r.id">{{ r.name }}</option>
            </select>
    <select
      v-model="g.denomination_id"
      :disabled="getDenominationsForReligion(g.religion_id).length === 0"
      @change="onDenominationChanged(g)"
      class="w-full px-3 py-2 border rounded"
    >
      <option value="">Select Denomination</option>
      <option
        v-for="d in getDenominationsForReligion(g.religion_id)"
        :key="d.id"
        :value="d.id"
      >
        {{ d.name }}
      </option>
    </select>


          </div>
          <button @click="addGrandchild(index)" class="text-blue-500 text-sm">+ Add Grandchild</button>
        </div>
      </div>
    </div>

    <button @click="addChild" class="mb-4 bg-green-600 text-white px-4 py-2 rounded">+ Add Child</button>

    <div class="flex justify-end">
      <button @click="submitChildren" class="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700">
        Submit Family
      </button>
    </div>
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

const children = ref([])
const religions = ref([])
const denominations = ref([])
const childPhotos = ref({})
const spousePhotos = ref({})
const grandchildPhotos = ref({})

const addChild = () => {
  children.value.push({
    first_name: '',
    hnam_hming: '',
    gender: '',
    dob: '',
    blood_group: '',
    epic_number: '',
    aadhar_number: '',
    religion_id: '',
    denomination_id: '',
    hasSpouse: false,
    spouse: {
      first_name: '',
      hnam_hming: '',
      gender: '',
      dob: '',
      blood_group: '',
      epic_number: '',
      aadhar_number: '',
      religion_id: '',
      denomination_id: ''
    },
    grandchildren: [],
    searchFather: '',
    searchMother: '',
    fatherOptions: [],
    motherOptions: [],
    selectedFather: null,
    selectedMother: null,
    father_id: null,
    mother_id: null,
  })
}
const removeChild = (index) => {
  children.value.splice(index, 1)
}



const addGrandchild = (childIndex) => {
  children.value[childIndex].grandchildren.push({
    first_name: '',
    hnam_hming: '',
    gender: '',
    dob: '',
    blood_group: '',
    epic_number: '',
    aadhar_number: '',
    religion_id: '',
    denomination_id: ''
  })
}


const fetchMeta = async () => {
  const [rel, den] = await Promise.all([
    $axios.get('/meta/religions/'),
    $axios.get('/meta/denominations/')
  ])
  religions.value = rel.data
  denominations.value = den.data
}
const getDenominationsForReligion = (religionId) => {
  if (!religionId) return []
  return denominations.value.filter(d => d.religion_id === religionId)
}

const onDenominationChanged = (person) => {
  const denoms = getDenominationsForReligion(person.religion_id)
  if (!denoms.length) {
    person.denomination_id = null
  }
}



const searchFather = async (index) => {
  const query = children.value[index].searchFather
  if (!query) return
  const res = await $axios.get('/search/father/', {
    params: {
      house_id: store.house_id,
      name: query
    }
  })
  children.value[index].fatherOptions = res.data
}

const selectFather = (index, person) => {
  children.value[index].father_id = person.id
  children.value[index].selectedFather = person
  children.value[index].searchFather = `${person.first_name} ${person.hnam_hming}`
  children.value[index].fatherOptions = []
}

const clearFather = (index) => {
  children.value[index].father_id = null
  children.value[index].selectedFather = null
  children.value[index].searchFather = ''
  children.value[index].fatherOptions = []
}

const searchMother = async (index) => {
  const query = children.value[index].searchMother
  if (!query) return
  const res = await $axios.get('/search/mother/', {
    params: {
      house_id: store.house_id,
      name: query
    }
  })
  children.value[index].motherOptions = res.data
}

const selectMother = (index, person) => {
  children.value[index].mother_id = person.id
  children.value[index].selectedMother = person
  children.value[index].searchMother = `${person.first_name} ${person.hnam_hming}`
  children.value[index].motherOptions = []
}

const clearMother = (index) => {
  children.value[index].mother_id = null
  children.value[index].selectedMother = null
  children.value[index].searchMother = ''
  children.value[index].motherOptions = []
}
const clearSpouse = (index) => {
  children.value[index].hasSpouse = false
  children.value[index].spouse = {
    first_name: '',
    hnam_hming: '',
    gender: '',
    dob: '',
    blood_group: '',
    epic_number: '',
    aadhar_number: '',
    religion_id: '',
    denomination_id: ''
  }
}
const removeGrandchild = (childIndex, grandchildIndex) => {
  children.value[childIndex].grandchildren.splice(grandchildIndex, 1)
}



const onPhotoSelected = (event, index, type, gIndex = null) => {
  const file = event.target.files[0]
  if (!file) return

  if (type === 'child') {
    childPhotos.value[index] = file
  } else if (type === 'spouse') {
    spousePhotos.value[index] = file
  } else if (type === 'grandchild') {
    if (!grandchildPhotos.value[index]) grandchildPhotos.value[index] = {}
    grandchildPhotos.value[index][gIndex] = file
  }
}
const buildFormData = (data, photoFile) => {
  const form = new FormData()
  for (const [key, value] of Object.entries(data)) {
    form.append(key, value ?? '')
  }
  if (photoFile) form.append('photo', photoFile)
  return form
}



const submitChildren = async () => {
  try {
    for (const child of children.value) {
      if (child.denomination_id === '') child.denomination_id = null
      if (child.religion_id === '') child.religion_id = null

      const childRes = await $axios.post('/person/', {
        ...child,
        house_id: store.house_id,
        father_id: child.father_id,
        mother_id: child.mother_id,
      })
      const childId = childRes.data.id

      if (child.hasSpouse) {
        if (child.spouse.denomination_id === '') child.spouse.denomination_id = null
        if (child.spouse.religion_id === '') child.spouse.religion_id = null

        const spouseRes = await $axios.post('/person/', {
          ...child.spouse,
          house_id: store.house_id,
          spouse_id: childId
        })
        await $axios.patch(`/person/${childId}/`, {
          spouse_id: spouseRes.data.id
        })
      }

      for (const grandchild of child.grandchildren) {
        if (grandchild.denomination_id === '') grandchild.denomination_id = null
        if (grandchild.religion_id === '') grandchild.religion_id = null

        await $axios.post('/person/', {
          ...grandchild,
          house_id: store.house_id,
          father_id: child.gender === 'Male' ? childId : null,
          mother_id: child.gender === 'Female' ? childId : null
        })
      }

      store.addMember(childRes.data)
    }

    alert('Family created successfully!')
    router.push('/family-entry/complete')
  } catch (err) {
    console.error(err)
    alert('Something went wrong while saving the family.')
  }
}


onMounted(fetchMeta)
</script>
