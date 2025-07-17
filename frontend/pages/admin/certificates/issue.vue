<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <div class="max-w-5xl mx-auto bg-white p-8 rounded-lg shadow-xl relative">
      <!-- Back Button -->
      <button @click="goBack" class="absolute top-4 left-4 text-gray-600 hover:text-gray-900 transition duration-150 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded-full p-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
      </button>

      <h1 class="text-4xl font-extrabold text-gray-900 mb-8 text-center">Issue Certificate</h1>

      <div class="bg-gray-50 p-6 rounded-lg border border-gray-200 mb-8">
        <div ref="editor" class="min-h-[400px] border border-gray-300 rounded-md overflow-hidden"></div>
      </div>

      <div class="flex justify-center space-x-6">
        <button @click="printCertificate" class="px-8 py-3 bg-indigo-600 text-white rounded-lg shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition ease-in-out duration-150">
          Print Certificate
        </button>
        <button @click="issueAndPrintCertificate" class="px-8 py-3 bg-green-600 text-white rounded-lg shadow-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition ease-in-out duration-150">
          Issue & Print Certificate
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { useRoute ,useRouter} from 'vue-router';
import { useNuxtApp } from '#app';
import 'quill/dist/quill.snow.css';
const router = useRouter();


definePageMeta({
  layout: 'admin',
  middleware: 'auth',
});

const route = useRoute();
const { $api } = useNuxtApp();
const editor = ref(null);
let quillInstance = null;

const formValues = ref({});

const goBack = () => {
  router.back();
};

onMounted(async () => {
  if (process.client) {
    const Quill = (await import('quill')).default;
    
    const certificateTypeId = route.query.certificateTypeId;
    formValues.value = JSON.parse(route.query.formValues || '{}');

    let templateDelta = {};

    try {
      const response = await $api.get(`/certificates/types/${certificateTypeId}/`);
      templateDelta = response.data.template;
    } catch (error) {
      console.error('Error fetching certificate template:', error);
      // Handle error, maybe redirect or show a message
      return;
    }

    // Auto-calculate issue_date
    const today = new Date();
    const issueDate = `${today.getDate()}/${today.getMonth() + 1}/${today.getFullYear()}`;
    formValues.value['issue_date'] = issueDate;

    // Substitute variables in the Delta
    if (templateDelta.ops) {
      templateDelta.ops.forEach(op => {
        if (typeof op.insert === 'string') {
          for (const key in formValues.value) {
            const placeholder = `{{ ${key} }}`;
            op.insert = op.insert.replace(new RegExp(placeholder, 'g'), formValues.value[key]);
          }
          // Handle son/daughter
          if (formValues.value['person.gender'] && formValues.value['person.gender'].toLowerCase() === 'female') {
            op.insert = op.insert.replace('son/daughter of', 'daughter of');
          } else {
            op.insert = op.insert.replace('son/daughter of', 'son of');
          }
          // Replace any remaining placeholders
          op.insert = op.insert.replace(/\{\{.*?\}\}/g, '[N/A]');
        }
      });
    }

    nextTick(() => {
      if (editor.value) {
        quillInstance = new Quill(editor.value, {
          theme: 'snow',
          modules: {
            toolbar: [
              ['bold', 'italic', 'underline'],
              [{ 'list': 'ordered'}, { 'list': 'bullet' }],
              [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
              ['clean']
            ]
          }
        });

        quillInstance.setContents(templateDelta);
      }
    });
  }
});

const issueAndPrintCertificate = async () => {
  if (quillInstance) {
    const certificateTypeId = route.query.certificateTypeId;
    const personId = formValues.value['person.id']; // Assuming person.id is available in formValues
    const content = quillInstance.getContents(); // Get content as Delta

    if (!personId) {
      alert('Person ID is required to issue a certificate.');
      return;
    }

    try {
      await $api.post('/certificates/issue/', {
        person_id: personId,
        certificate_type_id: certificateTypeId,
        content: content // Pass the full Delta object
      });
      alert('Certificate issued successfully!');
      printCertificate();
    } catch (error) {
      console.error('Error issuing certificate:', error);
      alert('Failed to issue certificate.');
    }
  }
};

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
