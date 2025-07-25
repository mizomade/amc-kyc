<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <h1 class="text-3xl font-bold text-gray-900 mb-6">Family Tree View</h1>

    <div class="bg-white rounded-lg shadow-md p-6">
      <!-- Search Box -->
      <div class="mb-6 relative">
        <input
          v-model="searchQuery"
          @input="fetchSuggestions"
          type="text"
          placeholder="Search citizen by name..."
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <ul
          v-if="suggestions.length"
          class="absolute z-10 w-full bg-white border mt-1 rounded-md shadow-lg"
        >
          <li
            v-for="person in suggestions"
            :key="person.id"
            @click="selectSuggestion(person)"
            class="px-4 py-2 hover:bg-blue-100 cursor-pointer"
          >
            {{ person.name }}
          </li>
        </ul>
      </div>

      <!-- Family Tree Graph or Intro Info -->
      <div class="overflow-x-auto py-4">
        <div class="flex justify-center">
          <VGraphFamily
            v-if="treeData"
            :person-id="treeData.personId"
            :data="treeData"
            @node-selected="selectNode"
          />
          <div
            v-else
            class="text-center text-gray-600 py-20 px-6 max-w-2xl mx-auto"
          >
            <!-- <h2 class="text-2xl font-semibold text-gray-800 mb-4">Explore Your Family Heritage</h2>
            <p class="text-gray-700 mb-4">
              This portal allows you to explore the family trees of citizens across Mizoram.
              Simply type a person's name above to get started. You can view parents, spouses,
              children, and even navigate through generations.
            </p> -->
            <img
              src="/images/family-tree-placeholder.png"
              alt="Family Tree Illustration"
              class="w-full h-auto mx-auto mt-6 opacity-70"
            />
          </div>
        </div>
      </div>

      <!-- Selected Person Details -->
      <div
        v-if="selectedNode"
        class="mt-8 p-6 bg-gray-50 border border-gray-200 rounded-lg shadow"
      >
        <h3 class="text-xl font-semibold text-gray-700 mb-4">Person Details</h3>
        <p class="text-gray-800 mb-1"><strong>Name:</strong> {{ selectedNode.name }}</p>

        <div class="mt-4 flex gap-4">
          <NuxtLink
            :to="`/admin/person/${selectedNode.id}`"
            class="inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            See Personal Details
          </NuxtLink>

          <button
            @click="loadTreeFromSelectedNode"
            class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
          >
            Load Tree from this Person
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useNuxtApp } from '#app'
import { useRoute, useRouter } from 'vue-router'
import FamilyTreeGraph from '~/components/VGraphFamily.vue'


const route = useRoute();
const userId = route.query.id || '';

definePageMeta({
  layout: 'admin',
  middleware: 'auth',
})

const { $api } = useNuxtApp()
const searchQuery = ref('')
const suggestions = ref([])
const selectedNode = ref(null)
const treeData = ref(null)

const fetchSuggestions = async () => {
  if (searchQuery.value.length < 2) {
    suggestions.value = []
    return
  }

  try {
    const response = await $api.get(
      `/tree-view/citizens/search?name=${encodeURIComponent(searchQuery.value)}`
    )
    suggestions.value = response.data
  } catch (error) {
    console.error('Error fetching suggestions:', error)
    suggestions.value = []
  }
}

const selectSuggestion = async (person) => {
  searchQuery.value = person.name
  suggestions.value = []
  selectedNode.value = null

  try {
    const response = await $api.get(`/family-tree-v3/tree/${person.id}`)
    treeData.value = response.data
  } catch (error) {
    console.error('Error fetching tree:', error)
    treeData.value = null
  }
}

const selectNode = (node) => {
  if (node.isUnion) return
  selectedNode.value = node
}

const loadTreeFromSelectedNode = async () => {
  if (!selectedNode.value?.id) return
  try {
    const response = await $api.get(`/family-tree-v3/tree/${selectedNode.value.id}`)
    treeData.value = response.data
    selectedNode.value = null
  } catch (error) {
    console.error('Error loading tree from selected node:', error)
  }
}

onMounted(async () => {
  if (userId) {
    try {
      const response = await $api.get(`/family-tree-v3/tree/${userId}`)
      treeData.value = response.data
    } catch (error) {
      // console.error('Error fetching initial tree data:', error)
    }
  }
})  
</script>
