<template>
  <div
    v-if="show"
    class="fixed inset-0 z-50 bg-black bg-opacity-50 flex items-center justify-center"
  >
    <div class="bg-white w-full max-w-3xl p-4 rounded-xl relative shadow-lg">
      <button
        class="absolute top-2 right-2 text-gray-600 hover:text-red-500"
        @click="emit('close')"
      >
        ✕
      </button>

      <h2 class="text-xl font-bold mb-2">Location Map</h2>
      <p v-if="houseNumber" class="text-gray-600 mb-4">
        House No.: <span class="font-semibold">{{ houseNumber }}</span>
      </p>

  <LMap
  v-if="clientReady"
  v-model:zoom="zoom"
  :center="mapCenter"
  style="height: 400px; width: 100%"
  :use-global-leaflet="false"
  @click="onMapClick"
>
  <!-- Layer switch control -->
  <LControlLayers position="topright" />

  <!-- Base Layers -->
  <LTileLayer
    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    attribution="&copy; OpenStreetMap contributors"
    layer-type="base"
    name="OpenStreetMap"
  />
  <LTileLayer
    url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    attribution="Tiles © Esri"
    layer-type="base"
    name="Satellite"
  />

  <!-- Marker -->
  <LMarker v-if="marker" :lat-lng="marker" />
</LMap>


      <div class="mt-4 text-sm text-gray-700 space-y-1">
        <p v-if="marker">
          <strong>Latitude:</strong> {{ marker.lat }}<br />
          <strong>Longitude:</strong> {{ marker.lng }}
        </p>
        <p v-if="address"><strong>Address:</strong> {{ address }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'

// Props
const props = defineProps({
  show: Boolean,
  latitude: Number,
  longitude: Number,
  houseNumber: String,
  satellite: {
    type: Boolean,
    default: false,
  }
})

const emit = defineEmits(['close'])

const zoom = ref(15)
const marker = ref(null)
const address = ref('')
const clientReady = ref(false)

// Map center based on props
const mapCenter = computed(() =>
  props.latitude && props.longitude
    ? [props.latitude, props.longitude]
    : [23.7358, 92.7164]      // zarkawt
)


watch(
  () => props.show,
  (val) => {
    if (val && props.latitude && props.longitude) {
      marker.value = {
        lat: props.latitude,
        lng: props.longitude,
      }
      getAddress(props.latitude, props.longitude)
    }
  }
)

onMounted(() => {
  clientReady.value = true
})

function onMapClick(e) {
  marker.value = e.latlng
  getAddress(e.latlng.lat, e.latlng.lng)
  emit('selected', { lat: e.latlng.lat, lng: e.latlng.lng });     //coordinate for house entry
}

async function getAddress(lat, lng) {
  try {
    const res = await fetch(
      `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lng}`
    )
    const data = await res.json()
    address.value = data.display_name || ''
  } catch (err) {
    console.error('Address fetch failed', err)
  }
}
</script>
