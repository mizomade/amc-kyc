export default defineNuxtConfig({
  modules: [
    '@pinia/nuxt',
    '@nuxtjs/tailwindcss',
    '@nuxt/ui',
    '@nuxt/icon',
  ],
  css: [
    '~/assets/css/main.css',
  ],
  nitro: {
    alias: {
      'form-data': 'form-data/lib/form_data.js'
    }
  }
});