<template>
  <div class="tree-node flex flex-col items-center relative">

    <!-- Upward connections: Father + Mother -->
    <div v-if="hasParents" class="flex items-end justify-center relative mb-4">
      <!-- Horizontal line between parents -->
      <div class="absolute top-1/2 w-full h-0.5 bg-gray-400"></div>

      <div class="flex flex-col items-center mx-4 relative">
        <!-- Vertical line from parent down -->
        <div class="absolute bottom-0 h-4 w-0.5 bg-gray-400"></div>
        <TreeNode
          v-if="node.father"
          :node="node.father"
          :onSelect="onSelect"
          :selectedId="selectedId"
        />
      </div>

      <div class="flex flex-col items-center mx-4 relative">
        <div class="absolute bottom-0 h-4 w-0.5 bg-gray-400"></div>
        <TreeNode
          v-if="node.mother"
          :node="node.mother"
          :onSelect="onSelect"
          :selectedId="selectedId"
        />
      </div>
    </div>

    <!-- This Node -->
    <div
      :class="[
        'node-content px-4 py-2 rounded-lg shadow-md cursor-pointer transition duration-300',
        isSelected ? 'bg-green-600 text-white' : 'bg-blue-500 text-white hover:bg-blue-600'
      ]"
      @click="handleClick"
    >
      {{ node.name }}
    </div>

    <!-- Downward children -->
    <div v-if="hasChildren" class="flex justify-center items-start mt-4 relative">
      <!-- Horizontal line above children -->
      <div class="absolute top-0 w-full h-0.5 bg-gray-400"></div>

      <div
        v-for="child in node.children"
        :key="child.id"
        class="flex flex-col items-center mx-4 relative"
      >
        <!-- Vertical line from horizontal to child -->
        <div class="absolute top-0 h-4 w-0.5 bg-gray-400"></div>

        <TreeNode
          :node="child"
          :onSelect="onSelect"
          :selectedId="selectedId"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  node: Object,
  onSelect: Function,
  selectedId: Number,
})

const hasChildren = computed(() => props.node.children && props.node.children.length)
const hasParents = computed(() => props.node.father || props.node.mother)
const isSelected = computed(() => props.node.id === props.selectedId)

const handleClick = () => {
  props.onSelect(props.node)
}
</script>

<style scoped>
.tree-node {
  position: relative;
}
</style>
