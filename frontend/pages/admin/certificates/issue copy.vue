<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Issue Certificate</h1>
    <div class="bg-white p-8 rounded-lg shadow-md">
      <div ref="editor"></div>
    </div>
    <div class="mt-6">
      <button @click="printCertificate" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded">
        Print Certificate
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import 'quill/dist/quill.snow.css';

const route = useRoute();
const editor = ref(null);
let quillInstance = null;

onMounted(async () => {
  if (process.client) {
    const Quill = (await import('quill')).default;
    
    let templateDelta = JSON.parse(route.query.template || '{}');
    const variables = { ...route.query };
    delete variables.template;

    // Auto-calculate issue_date
    const today = new Date();
    const issueDate = `${today.getDate()}/${today.getMonth() + 1}/${today.getFullYear()}`;
    variables['issue_date'] = issueDate;

    // Substitute variables in the Delta
    if (templateDelta.ops) {
      templateDelta.ops.forEach(op => {
        if (typeof op.insert === 'string') {
          for (const key in variables) {
            const placeholder = `{{ ${key} }}`;
            op.insert = op.insert.replace(new RegExp(placeholder, 'g'), variables[key]);
          }
          // Handle son/daughter
          if (variables['person.gender'] && variables['person.gender'].toLowerCase() === 'female') {
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
