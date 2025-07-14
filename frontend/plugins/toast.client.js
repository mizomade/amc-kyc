// plugins/vue-toastification.client.js
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

export default defineNuxtPlugin((nuxtApp) => {
  const options = {
    // optional config
    timeout: 3000,
    position: 'top-right',
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
    showCloseButtonOnHover: false,
  }

  nuxtApp.vueApp.use(Toast, options)
})
