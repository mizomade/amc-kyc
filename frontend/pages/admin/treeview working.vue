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
      <!-- Family Tree Graph -->
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
            class="text-center text-gray-500 py-20 w-full"
          >
            Search and select a person to load the family tree.
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
        <p class="text-gray-800 mb-1"><strong>ID:</strong> {{ selectedNode.id }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useNuxtApp } from '#app'
import FamilyTreeGraph from '~/components/VGraphFamily.vue'

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
  console.log('Selected node:', node)
  if (node.isUnion) return
  selectedNode.value = node
}
</script>
