export default defineNuxtConfig({

  app: {
    head: {
      script: [
        // { src: 'https://cdn.jsdelivr.net/npm/chart.js', defer: true }, // Example for Chart.js CDN
        // Add other global scripts here
      ],
    },
  },
  modules: ['@pinia/nuxt', '@nuxtjs/tailwindcss', '@nuxt/ui', '@nuxt/icon', 'nuxt-echarts', '@nuxtjs/leaflet'],
  css: [
    '~/assets/css/main.css',
  ],
  build: {
    transpile: ['vue-quill-editor'],
  },
  nitro: {
    alias: {
      'form-data': 'form-data/lib/form_data.js'
    }
  },
  plugins: [
    { src: '~/plugins/chart.js', mode: 'client' }
  ]
});