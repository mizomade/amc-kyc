<template>
  <div class="container mx-auto py-6 pt-10 px-4 bg-gray-100  min-h-screen">
    <div class="relative mb-8">
      <button @click="goBack" class="absolute top-0 left-0 bg-transparent hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded-lg  flex items-center cursor-pointer">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
        </svg>
        Back
      </button>
      <h1 class="text-3xl font-extrabold text-gray-800 text-center">Citizen Details</h1>
    </div>

    <div v-if="person" class="space-y-8">
      <!-- Personal Details Card -->
      <div class="bg-white shadow-lg rounded-xl p-8">
        <h2 class="text-2xl font-bold text-gray-700 mb-6 border-b pb-3">Personal Information</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-4">
          <div class="flex items-center space-x-4" v-if="person.photo">
            <img :src="person.photo" alt="Person Photo" class="w-24 h-24 object-cover rounded-full shadow-md border-2 border-blue-300" />
            <p class="text-lg font-semibold text-gray-800">Photo</p>
          </div>
          <DetailItem label="First Name" :value="person.first_name" />
          <DetailItem label="Hnam Hming" :value="person.hnam_hming" />
          <DetailItem label="Gender" :value="person.gender" />
          <DetailItem label="Date of Birth" :value="person.dob" />
          <DetailItem label="Blood Group" :value="person.blood_group" />
          <DetailItem label="Mobile" :value="person.mobile" />
          <DetailItem label="EPIC Number" :value="person.epic_number" />
          <DetailItem label="Aadhar Number" :value="person.aadhar_number" />
          <DetailItem label="Marital Status" :value="person.marital_status" />
          <DetailItem label="Is Househead" :value="person.is_househead ? 'Yes' : 'No'" />
        </div>
      </div>

      <!-- Family Relations Card -->
      <div class="bg-white shadow-lg rounded-xl p-8">
        <h2 class="text-2xl font-bold text-gray-700 mb-6 border-b pb-3">Family Relations</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-4">
          <DetailItem label="Father" :value="person.father ? person.father.first_name + ' ' + (person.father.hnam_hming || '') : 'N/A'" />
          <DetailItem label="Mother" :value="person.mother ? person.mother.first_name + ' ' + (person.mother.hnam_hming || '') : 'N/A'" />
          <DetailItem label="Spouse" :value="person.spouse ? person.spouse.first_name + ' ' + (person.spouse.hnam_hming || '') : 'N/A'" />
        </div>
        <button  class="mt-4 inline-flex items-center px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700">
          Show Family Tree
        </button>
      </div>

      <!-- House Details Card -->
      <div v-if="person.house" class="bg-white shadow-lg rounded-xl p-8">
        <h2 class="text-2xl font-bold text-gray-700 mb-6 border-b pb-3">House Details</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-4">
          <DetailItem label="House Number" :value="person.house.house_number" />
          <DetailItem label="Veng" :value="person.house.veng ? person.house.veng.name : 'N/A'" />
          <DetailItem label="Street" :value="person.house.street" />
          <DetailItem label="Landmarks" :value="person.house.landmarks" />
          <DetailItem label="Is Owner" :value="person.house.is_owner ? 'Yes' : 'No'" />
          <DetailItem label="Have Tenant" :value="person.house.have_tenant ? 'Yes' : 'No'" />
          <DetailItem label="Is Tenant" :value="person.house.is_tenant ? 'Yes' : 'No'" />
          <DetailItem label="LSC Number" :value="person.house.lsc_number" />
          <DetailItem label="Awmtan Kum" :value="person.house.awmtan_kum" />
          <DetailItem label="Pem Luh Chhan" :value="person.house.pem_luh_chhan" />
          <DetailItem label="Household Size" :value="person.house.household_size" />
          <DetailItem label="Landlord Name" :value="person.house.landlord_name" />
          <DetailItem label="Landlord Phone" :value="person.house.landlord_phone" />
          <DetailItem label="Landlord Veng" :value="person.house.landlord_veng" />
          <DetailItem label="Latitude" :value="person.house.latitude" />
          <DetailItem label="Longitude" :value="person.house.longitude" />
        </div>
      </div>

      <!-- Other Details Card -->
      <div class="bg-white shadow-lg rounded-xl p-8">
        <h2 class="text-2xl font-bold text-gray-700 mb-6 border-b pb-3">Other Details</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-4">
          <DetailItem label="Religion" :value="person.religion ? person.religion.name : 'N/A'" />
          <DetailItem label="Denomination" :value="person.denomination ? person.denomination.name : 'N/A'" />
          <DetailItem label="Role" :value="person.role ? person.role.name : 'N/A'" />
        </div>
      </div>

      <!-- Qualifications Card -->
      <div v-if="person.qualifications && person.qualifications.length > 0" class="bg-white shadow-lg rounded-xl p-8">
        <h2 class="text-2xl font-bold text-gray-700 mb-6 border-b pb-3">Qualifications</h2>
        <div class="space-y-6">
          <div v-for="(qualification, index) in person.qualifications" :key="index" class="bg-gray-50 p-6 rounded-lg shadow-sm border border-gray-200">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-4">
              <DetailItem label="Education" :value="qualification.education.name" />
              <DetailItem label="Year of Passing" :value="qualification.year_of_passing" />
              <DetailItem label="Institution" :value="qualification.institution_name" />
              <DetailItem label="Grade/Marks" :value="qualification.grade_or_marks" />
              <DetailItem label="Certificate Number" :value="qualification.certificate_number" />
              <DetailItem label="Remarks" :value="qualification.remarks" />
            </div>
          </div>
        </div>
      </div>
      <div v-else class="bg-white shadow-lg rounded-xl p-8">
        <h2 class="text-2xl font-bold text-gray-700 mb-6 border-b pb-3">Qualifications</h2>
        <p class="text-gray-600">No qualifications available.</p>
      </div>

      <!-- Occupations Card -->
      <div v-if="person.occupations && person.occupations.length > 0" class="bg-white shadow-lg rounded-xl p-8">
        <h2 class="text-2xl font-bold text-gray-700 mb-6 border-b pb-3">Occupations</h2>
        <div class="space-y-6">
          <div v-for="(occupation, index) in person.occupations" :key="index" class="bg-gray-50 p-6 rounded-lg shadow-sm border border-gray-200">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-4">
              <DetailItem label="Occupation" :value="occupation.occupation.name" />
              <DetailItem label="Employer" :value="occupation.employer_name" />
              <DetailItem label="Position" :value="occupation.position_title" />
              <DetailItem label="Start Date" :value="occupation.start_date" />
              <DetailItem label="End Date" :value="occupation.end_date" />
              <DetailItem label="Remarks" :value="occupation.remarks" />
            </div>
          </div>
        </div>
      </div>
      <div v-else class="bg-white shadow-lg rounded-xl p-8">
        <h2 class="text-2xl font-bold text-gray-700 mb-6 border-b pb-3">Occupations</h2>
        <p class="text-gray-600">No occupations available.</p>
      </div>

      <!-- Attachments Card -->
      <div v-if="person.attachments && person.attachments.length > 0" class="bg-white shadow-lg rounded-xl p-8">
        <h2 class="text-2xl font-bold text-gray-700 mb-6 border-b pb-3">Attachments</h2>
        <div class="space-y-6">
          <div v-for="(attachment, index) in person.attachments" :key="index" class="bg-gray-50 p-6 rounded-lg shadow-sm border border-gray-200">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-4">
              <DetailItem label="Document Type" :value="attachment.document_type.name" />
              <DetailItem label="File">
<a
  :href="`http://localhost:8000${attachment.file}`"
  target="_blank"
  class="text-blue-600 hover:underline font-medium"
>
  View Document
</a>              </DetailItem>
              <DetailItem label="Remarks" :value="attachment.remarks" />
              <DetailItem label="Uploaded At" :value="attachment.uploaded_at" />
            </div>
          </div>
        </div>
      </div>
      <div v-else class="bg-white shadow-lg rounded-xl p-8">
        <h2 class="text-2xl font-bold text-gray-700 mb-6 border-b pb-3">Attachments</h2>
        <p class="text-gray-600">No attachments available.</p>
      </div>

      <!-- Verification Details Card -->
      <div class="bg-white shadow-lg rounded-xl p-8">
        <h2 class="text-2xl font-bold text-gray-700 mb-6 border-b pb-3">Verification Details</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-4">
          <DetailItem label="Is Verified" :value="person.is_verified ? 'Yes' : 'No'" />
          <DetailItem label="Verified By" :value="person.verified_by" />
          <DetailItem label="Verified At" :value="person.verified_at" />
          <DetailItem label="Verification Remarks" :value="person.verification_remarks" />
          <DetailItem label="Created At" :value="person.created_at" />
          <DetailItem label="Updated At" :value="person.updated_at" />
        </div>
      </div>
    </div>

    <div v-else class="text-center text-gray-600 text-xl mt-16 p-8 bg-white shadow-lg rounded-xl">
      Loading person details or person not found...
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter, useNuxtApp } from '#app';
import DetailItem from '~/components/DetailItem.vue';
definePageMeta({
  layout: 'admin',
  middleware: 'auth',
});

const person = ref(null);
const route = useRoute();
const router = useRouter();
const { $api } = useNuxtApp();

const goBack = () => {
  router.back();
};

onMounted(async () => {
  try {
    const personId = route.params.id;
    const response = await $api.get(`/person/${personId}`);
    person.value = response.data;
  } catch (error) {
    console.error('Error fetching person details:', error);
    person.value = null;
  }
});
</script>

<style scoped>
/* No component-specific styles needed as Tailwind CSS is used */
</style>