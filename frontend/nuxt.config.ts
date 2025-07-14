export default defineNuxtConfig({
  modules: [
    '@pinia/nuxt',
    '@nuxtjs/tailwindcss',
  ],
  css: [
    '~/assets/css/main.css',
  ],
  plugins: [
    '~/plugins/axios.js',
    '~/plugins/pinia.client.js',
  ],
})

