<template>
  <div>
    <div
      v-for="(document, index) in documents"
      :key="index"
      class="space-y-6 mb-6 border-b pb-6"
    >
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label for="document_type_id" class="block text-sm font-medium text-gray-700">Document Type</label>
          <select
            v-model="document.document_type_id"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          >
            <option v-for="docType in documentTypes" :key="docType.id" :value="docType.id">
              {{ docType.name }}
            </option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Remarks</label>
          <input
            type="text"
            v-model="document.remarks"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Upload File</label>
          <input
            type="file"
            accept="image/*"
            @change="e => handleFileUpload(e, index)"
            class="mt-1 block w-full px-3 py-2 text-sm border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />

        </div>
      </div>
    </div>

    <div class="flex flex-col gap-4">
      <button
        type="button"
        @click="addMoreDocument"
        class="w-full inline-flex justify-center rounded-md border border-dashed border-gray-400 px-4 py-2 text-gray-700 hover:bg-gray-100"
      >
        + Add More Document
      </button>
      <button
        type="button"
        @click="submitAllDocuments"
        :disabled="disableSave"
        class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-white font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Save All Documents
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useNuxtApp } from '#app';
import { usePersonStore } from '@/stores/person';

const { $api } = useNuxtApp();
const personStore = usePersonStore();
const documentTypes = ref([]);
const documents = ref([createEmptyDocument()]);

const emit = defineEmits(['close']);

function createEmptyDocument() {
  return {
    document_type_id: null,
    remarks: '',
    file: null,  // File per document
  };
}

const fetchDocumentTypes = async () => {
  try {
    const response = await $api.get('/documentypelist/');
    documentTypes.value = response.data;
  } catch (error) {
    console.error('Error fetching document types:', error);
  }
};

const handleFileUpload = (e, index) => {
  documents.value[index].file = e.target.files[0];
};

const addMoreDocument = () => {
  documents.value.push(createEmptyDocument());
};

const submitAllDocuments = async () => {
  for (const document of documents.value) {
    const formData = new FormData();
    formData.append('person_id', personStore.person_id);
    formData.append('document_type_id', document.document_type_id);
    formData.append('remarks', document.remarks || '');

    if (document.file) {
      formData.append('file', document.file);
    }

    try {
      await $api.post('/attachments/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
    } catch (error) {
      console.error('Upload failed:', error);
      alert('Failed to upload one of the documents.');
      return;
    }
  }

  alert('All documents uploaded successfully.');

  resetDocuments();  

  emit('close');  
};
const props = defineProps({
  disableSave: {
    type: Boolean,
    default: false,
  },
});
const resetDocuments = () => {
  documents.value = [createEmptyDocument()];
};

onMounted(fetchDocumentTypes);
</script>