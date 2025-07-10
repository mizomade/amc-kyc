<template>
    <div class="tree-node flex flex-col items-center">
      <div
        :class="[
          'node-content px-4 py-2 rounded-lg shadow-md cursor-pointer transition duration-300',
          isSelected ? 'bg-green-600 text-white' : 'bg-blue-500 text-white hover:bg-blue-600'
        ]"
        @click="handleClick"
      >
        {{ node.name }}
      </div>
  
      <div
        v-if="hasChildren"
        class="node-children flex mt-4"
      >
        <div
          v-for="child in node.children"
          :key="child.id"
          class="flex flex-col items-center mx-4 relative"
        >
          <!-- <div class="line-vertical"></div>
          <div class="line-horizontal"></div> -->
          <TreeNode
            :node="child"
            :onSelect="onSelect"
            :search="search"
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
  search: String,
  selectedId: Number,
})

const hasChildren = computed(() => props.node.children && props.node.children.length)
const isSelected = computed(() => props.node.id === props.selectedId)

const handleClick = () => {
  props.onSelect(props.node)
}
</script>

  
  <style scoped>
  /* Reuse same lines if needed, or leave empty if parent handles */
  </style>
  