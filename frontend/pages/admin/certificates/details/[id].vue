<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Certificate Details</h1>
    <div v-if="certificate" class="bg-white p-8 rounded-lg shadow-md">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <p class="text-gray-600">Certificate Number:</p>
          <p class="font-semibold">{{ certificate.certificate_number || 'N/A' }}</p>
        </div>
        <div>
          <p class="text-gray-600">Person:</p>
          <p class="font-semibold">{{ certificate.person_first_name }}</p>
        </div>
        <div>
          <p class="text-gray-600">Certificate Type:</p>
          <p class="font-semibold">{{ certificate.certificate_type }}</p>
        </div>
        <div>
          <p class="text-gray-600">Application Date:</p>
          <p class="font-semibold">{{ certificate.application_date }}</p>
        </div>
        <div>
          <p class="text-gray-600">Issue Date:</p>
          <p class="font-semibold">{{ certificate.issue_date || 'N/A' }}</p>
        </div>
        <div>
          <p class="text-gray-600">Issued By:</p>
          <p class="font-semibold">{{ certificate.issued_by || 'N/A' }}</p>
        </div>
        <div>
          <p class="text-gray-600">Approved:</p>
          <p class="font-semibold">{{ certificate.is_approved ? 'Yes' : 'No' }}</p>
        </div>
        <div v-if="certificate.approved_at">
          <p class="text-gray-600">Approved At:</p>
          <p class="font-semibold">{{ certificate.approved_at }}</p>
        </div>
      </div>

      <h2 class="text-xl font-semibold mb-2">Certificate Content</h2>
      <div class="border p-4 rounded-md bg-gray-50">
        <div ref="contentEditor"></div>
      </div>

      <div class="mt-6">
        <button @click="printCertificate" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded">
          Print Certificate
        </button>
      </div>
    </div>
    <div v-else>
      <p>Loading certificate details...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import { useNuxtApp } from '#app';
import Quill from 'quill';
import 'quill/dist/quill.snow.css';

const route = useRoute();
const { $api } = useNuxtApp();
const certificate = ref(null);
const contentEditor = ref(null);
let quillInstance = null;

definePageMeta({
  layout: 'admin',
  middleware: 'auth',
});

onMounted(async () => {
  const certificateId = route.params.id;
  try {
    const response = await $api.get(`/certificates/issued/${certificateId}/`);
    certificate.value = response.data;

    if (process.client && certificate.value && certificate.value.content) {
      nextTick(() => {
        if (contentEditor.value) {
          quillInstance = new Quill(contentEditor.value, {
            theme: 'bubble', // Use 'bubble' theme for read-only display
            readOnly: true,
          });
          quillInstance.setContents(certificate.value.content);
        }
      });
    }
  } catch (error) {
    console.error('Error fetching certificate details:', error);
  }
});

const printCertificate = () => {
  if (quillInstance) {
    const printWindow = window.open('', '', 'height=600,width=800');
    const stylesheets = Array.from(document.styleSheets)
      .map(sheet => sheet.href ? `<link rel="stylesheet" href="${sheet.href}">` : `<style>${Array.from(sheet.cssRules).map(rule => rule.cssText).join('')}</style>`)
      .join('\n');

    printWindow.document.write(`
      <html>
        <head>
          <title>Print Certificate</title>
          ${stylesheets}
        </head>
        <body>
          ${quillInstance.root.innerHTML}
        </body>
      </html>
    `);
    printWindow.document.close();
    printWindow.focus();
    setTimeout(() => { printWindow.print(); }, 500);
  }
};
</script>
