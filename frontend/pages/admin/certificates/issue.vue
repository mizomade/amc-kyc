<template>
  <div class="p-8 bg-gray-100 min-h-screen">
    <div class="max-w-6xl mx-auto">
      <header class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-800">Issue New Certificate</h1>
          <p class="text-gray-500">Create and issue a new certificate for a person.</p>
        </div>
        <div class="flex items-center space-x-4">
          <button v-if="step === 2" @click="step = 1" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white rounded-md border border-gray-300 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            Back to Selection
          </button>
          <button @click="handleAction" :class="['px-6 py-2 text-sm font-medium text-white rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2', step === 1 ? 'bg-indigo-600 hover:bg-indigo-700 focus:ring-indigo-500' : 'bg-green-600 hover:bg-green-700 focus:ring-green-500']">
            {{ step === 1 ? 'Proceed to Editor' : 'Issue Certificate' }}
          </button>
        </div>
      </header>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Left Column: Form or Editor -->
        <div class="bg-white p-6 rounded-lg shadow-md">
          <!-- Step 1: Selection Form -->
          <div v-if="step === 1">
            <h2 class="text-xl font-semibold mb-4">1. Select Details</h2>
            <div class="space-y-6">
              <div>
                <label for="person" class="block text-sm font-medium text-gray-700">Person</label>
                <select v-model="selectedPerson" id="person" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md">
                  <option disabled value="">Please select a person</option>
                  <option v-for="person in people" :key="person.id" :value="person.id">{{ person.first_name }}</option>
                </select>
              </div>
              <div>
                <label for="cert-type" class="block text-sm font-medium text-gray-700">Certificate Type</label>
                <select v-model="selectedCertType" id="cert-type" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md">
                  <option disabled value="">Please select a type</option>
                  <option v-for="certType in certTypes" :key="certType.id" :value="certType.id">{{ certType.name }}</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Step 2: Rich Text Editor -->
          <div v-else>
            <h2 class="text-xl font-semibold mb-4">2. Edit Certificate Content</h2>
            <div ref="editor" style="height: 400px;"></div>
          </div>
        </div>

        <!-- Right Column: Live Preview -->
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h2 class="text-xl font-semibold mb-4">Live Preview</h2>
          <div class="prose prose-sm max-w-none border p-4 rounded-md h-full" v-html="certificateContent"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import axios from '~/plugins/axios.js';
import Quill from 'quill';
import 'quill/dist/quill.snow.css';

const { $api } = useNuxtApp();
definePageMeta({
  layout: 'admin',
  middleware: 'auth',
//   roles: ['admin'],
});

const step = ref(1);
const people = ref([]);
const certTypes = ref([]);
const selectedPerson = ref('');
const selectedCertType = ref('');
const certificateContent = ref('<p>Select a person and certificate type to generate a preview.</p>');
const editor = ref(null);
let quillInstance = null;
const router = useRouter();

onMounted(async () => {
  try {
    const [peopleRes, certTypesRes] = await Promise.all([
        $api.get('/person/'),
      $api.get('/certificates/types/')
    ]);
    people.value = peopleRes.data.persons;
    certTypes.value = certTypesRes.data;
  } catch (error) {
    console.error('Error fetching initial data:', error);
  }
});

const initializeQuill = () => {
  if (editor.value) {
    quillInstance = new Quill(editor.value, {
      theme: 'snow',
      modules: {
        toolbar: [
          ['bold', 'italic', 'underline', 'strike'],
          ['blockquote', 'code-block'],
          [{ 'header': 1 }, { 'header': 2 }],
          [{ 'list': 'ordered'}, { 'list': 'bullet' }],
          [{ 'script': 'sub'}, { 'script': 'super' }],
          [{ 'indent': '-1'}, { 'indent': '+1' }],
          [{ 'direction': 'rtl' }],
          [{ 'size': ['small', false, 'large', 'huge'] }],
          [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
          [{ 'color': [] }, { 'background': [] }],
          [{ 'font': [] }],
          [{ 'align': [] }],
          ['clean']
        ]
      }
    });
    quillInstance.on('text-change', () => {
      certificateContent.value = quillInstance.root.innerHTML;
    });
  }
};

watch(step, (newStep) => {
  if (newStep === 2 && !quillInstance) {
    setTimeout(initializeQuill, 0);
  }
});

const handleAction = async () => {
  if (step.value === 1) {
    if (!selectedPerson.value || !selectedCertType.value) {
      alert('Please select both a person and a certificate type.');
      return;
    }
    try {
      const response = await $api.post('/certificates/issue/', {
        person_id: selectedPerson.value,
        certificate_type_id: selectedCertType.value
      });
      certificateContent.value = response.data.content;
      if (quillInstance) {
        quillInstance.root.innerHTML = certificateContent.value;
      }
      step.value = 2;
    } catch (error) {
      console.error('Error generating certificate preview:', error);
    }
  } else {
    // In a real app, you'd likely save the final, edited `certificateContent`.
    // This example assumes the initial generation is what's saved.
    alert('Certificate issued successfully!');
    router.push('/admin/certificates');
  }
};
</script>

<style>
.ql-editor {
  min-height: 300px;
}
</style>