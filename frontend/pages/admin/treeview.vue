<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <h1 class="text-3xl font-bold text-gray-900 mb-6">Family Tree View</h1>

    <div class="bg-white rounded-lg shadow-md p-6">
      <!-- Search Box with Dropdown -->
      <div class="mb-4 relative">
        <input
          v-model="searchQuery"
          @input="fetchSuggestions"
          type="text"
          placeholder="Search citizen by name..."
          class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <ul
          v-if="suggestions.length"
          class="absolute z-10 w-full bg-white border mt-1 rounded-md shadow-md"
        >
          <li
            v-for="person in suggestions"
            :key="person.id"
            @click="selectSuggestion(person)"
            class="px-4 py-2 hover:bg-blue-50 cursor-pointer"
          >
            {{ person.name }}
          </li>
        </ul>
      </div>

      <div class="overflow-x-auto py-4">
        <div class="flex justify-center items-start">
          <div class="tree-container" v-if="treeData">
            <TreeNode
              :node="treeData"
              :onSelect="selectNode"
              :selectedId="selectedNode?.id"
            />

            
          </div>
          <div v-else class="text-gray-500">Search and select a person to load the tree.</div>
        </div>
      </div>

      <!-- Selected Details -->
      <div v-if="selectedNode" class="mt-8 p-4 bg-gray-100 rounded">
        <h3 class="text-lg font-semibold mb-2">Person Details</h3>
        <p><strong>Name:</strong> {{ selectedNode.name }}</p>
        <p><strong>ID:</strong> {{ selectedNode.id }}</p>
        <!-- More details can go here -->
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useNuxtApp } from '#app'
import TreeNode from '~/components/TreeNode.vue'

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
    const response = await $api.get(`/tree-view/citizens/search?name=${encodeURIComponent(searchQuery.value)}`)
    suggestions.value = response.data
  } catch (error) {
    console.error('Error fetching suggestions:', error)
    suggestions.value = []
  }
}

const selectSuggestion = async (person) => {
  searchQuery.value = person.name
  suggestions.value = []

  try {
    const response = await $api.get(`/tree-view/citizens/${person.id}/tree`);
    treeData.value = response.data
  } catch (error) {
    console.error('Error fetching tree:', error)
    treeData.value = null
  }
}

const selectNode = (node) => {
  selectedNode.value = node
}
</script>

<style scoped>
.tree-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 20px;
}
</style>
