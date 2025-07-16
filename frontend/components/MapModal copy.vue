<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-xl p-6 w-11/12 md:w-2/3 lg:w-1/2 relative">
      <button @click="$emit('close')" class="absolute top-3 right-3 text-gray-600 hover:text-gray-900 text-2xl font-bold">&times;</button>
      <h2 class="text-2xl font-bold mb-4">House Location: {{ houseNumber }}</h2>
      <div id="map" class="w-full" style="height: 500px;"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick, onUnmounted } from 'vue';
import { useNuxtApp } from '#app';

const props = defineProps({
  show: {
    type: Boolean,
    default: false,
  },
  latitude: {
    type: Number,
    default: 20.5937, // Default to India center
  },
  longitude: {
    type: Number,
    default: 78.9629, // Default to India center
  },
  houseNumber: {
    type: String,
    default: 'Unknown',
  },
});

const emit = defineEmits(['close']);

const { $leaflet: L } = useNuxtApp();
let map = null;

const initMap = () => {
  if (map) {
    map.remove();
  }

  map = L.map('map', {
    center: [props.latitude, props.longitude],
    zoom: 15,
    maxZoom: 17
  });

  L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
      maxZoom: 19,
      attribution: "&copy; OpenStreetMap contributors",
    }
  ).addTo(map);

  if (props.latitude && props.longitude) {
    L.marker([props.latitude, props.longitude]).addTo(map)
      .bindPopup(`<b>${props.houseNumber}</b><br>Location.`).openPopup();
  }
};

watch(() => props.show, (newValue) => {
  if (newValue) {
    nextTick(() => {
      initMap();
    });
  } else if (map) {
    map.remove(); // Clean up map when modal is closed
    map = null;
  }
});

onUnmounted(() => {
  if (map) {
    map.remove();
    map = null;
  }
});
</script>

<style scoped>
/* Add any component-specific styles here if needed */
</style>