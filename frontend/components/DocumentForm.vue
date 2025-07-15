<template>
  <form @submit.prevent="submitForm" class="space-y-6">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <label for="document_type_id" class="block text-sm font-medium text-gray-700">Document Type</label>
        <select id="document_type_id" v-model="documentData.document_type_id"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
          <option v-for="docType in documentTypes" :key="docType.id" :value="docType.id">{{ docType.name }}</option>
        </select>
      </div>
      <div>
        <label for="remarks" class="block text-sm font-medium text-gray-700">Remarks</label>
        <input type="text" id="remarks" v-model="documentData.remarks"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
      </div>
    </div>
    <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
      <button type="submit" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm">
        Save
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const emit = defineEmits(['submit']);

const documentTypes = ref([]);
const documentData = ref({
  document_type_id: null,
  remarks: '',
});

const fetchDocumentTypes = async () => {
  try {
    const response = await $fetch('http://localhost:8000/api/attachments/document-types/');
    documentTypes.value = response;
  } catch (error) {
    console.error('Error fetching document types:', error);
  }
};

const submitForm = () => {
  emit('submit', documentData.value);
};

onMounted(() => {
  fetchDocumentTypes();
});
</script>
