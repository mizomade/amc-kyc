<template>
  <div class="tree-node flex flex-col items-center relative">
    <!-- Upward connections: Father + Mother -->
    <div v-if="hasParents" class="flex items-end justify-center relative mb-6">
      <!-- Vertical line to this node -->
      <div class="absolute top-full h-6 w-0.5 connection-line left-1/2 -translate-x-1/2 rounded-full"></div>
      
      <!-- Horizontal line between parents -->
      <div class="absolute top-1/2 w-full h-0.5 connection-line rounded-full"></div>
      
      <div v-if="node.father" class="flex flex-col items-center mx-6 relative">
        <!-- Vertical line from parent down -->
        <div class="absolute bottom-0 h-6 w-0.5 connection-line left-1/2 -translate-x-1/2 rounded-full"></div>
        <TreeNode
          :node="node.father"
          :onSelect="onSelect"
          :selectedId="selectedId"
          :generation="generation - 1"
        />
      </div>
      
      <div v-if="node.mother" class="flex flex-col items-center mx-6 relative">
        <!-- Vertical line from parent down -->
        <div class="absolute bottom-0 h-6 w-0.5 connection-line left-1/2 -translate-x-1/2 rounded-full"></div>
        <TreeNode
          :node="node.mother"
          :onSelect="onSelect"
          :selectedId="selectedId"
          :generation="generation - 1"
        />
      </div>
    </div>
    
    <!-- Current Generation Level - Siblings, This Node, and Spouse horizontally -->
    <div class="flex items-center justify-center relative">
      <!-- Siblings (to the left) -->
      <div v-if="hasSiblings" class="flex items-center mr-4">
        <div
          v-for="(sibling, index) in node.siblings"
          :key="sibling.id"
          class="flex items-center relative"
          :class="{ 'ml-4': index > 0 }"
        >
          <TreeNode
            :node="sibling"
            :onSelect="onSelect"
            :selectedId="selectedId"
            :generation="generation"
          />
        </div>
        <!-- Horizontal connector line from siblings to main node -->
        <div class="h-0.5 connection-line rounded-full w-8"></div>
      </div>
      
      <!-- This Node (center) -->
      <div
        :class="[
          'node-card px-6 py-3 rounded-xl shadow-lg cursor-pointer transition-all duration-300 relative z-10',
          isSelected ? 'node-selected' : 'node-default'
        ]"
        @click="handleClick"
      >
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 avatar-circle rounded-full flex items-center justify-center text-white text-sm font-bold">
            {{ node.name.charAt(0) }}
          </div>
          <div>
            <div class="font-semibold transition-colors duration-300" :class="isSelected ? 'text-white' : 'text-gray-800'">
              {{ node.name }}
            </div>
            <div class="text-xs transition-colors duration-300" :class="isSelected ? 'text-white/80' : 'text-gray-500'">
              Gen {{ generation }}
            </div>
          </div>
        </div>
      </div>
      
      <!-- Spouse (to the right) -->
      <div v-if="node.spouse" class="flex items-center ml-4 relative">
        <!-- Horizontal connector line from main node to spouse -->
        <div class="h-0.5 connection-line rounded-full w-8"></div>
        <div class="ml-4">
          <TreeNode
            :node="node.spouse"
            :onSelect="onSelect"
            :selectedId="selectedId"
            :generation="generation"
          />
        </div>
      </div>
    </div>
    
    <!-- Downward children (arranged horizontally) -->
    <div v-if="hasChildren" class="flex justify-center items-start mt-6 relative">
      <!-- Vertical line from this node -->
      <div class="absolute bottom-full h-6 w-0.5 connection-line left-1/2 -translate-x-1/2 rounded-full"></div>
      
      <!-- Horizontal line above children (spans across all children) -->
      <div 
        class="absolute top-0 h-0.5 connection-line rounded-full"
        :style="{ 
          left: `${100 / node.children.length / 2}%`, 
          right: `${100 / node.children.length / 2}%` 
        }"
      ></div>
      
      <!-- Children arranged horizontally -->
      <div
        v-for="(child, index) in node.children"
        :key="child.id"
        class="flex flex-col items-center relative"
        :class="{ 'ml-8': index > 0 }"
      >
        <!-- Vertical line from horizontal to child -->
        <div class="absolute top-0 h-6 w-0.5 connection-line left-1/2 -translate-x-1/2 rounded-full"></div>
        
        <TreeNode
          :node="child"
          :onSelect="onSelect"
          :selectedId="selectedId"
          :generation="generation + 1"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  node: {
    type: Object,
    required: true
  },
  onSelect: {
    type: Function,
    required: true
  },
  selectedId: {
    type: Number,
    default: null
  },
  generation: {
    type: Number,
    default: 0
  }
})

const hasChildren = computed(() => props.node.children && props.node.children.length)
const hasParents = computed(() => props.node.father || props.node.mother)
const hasSiblings = computed(() => props.node.siblings && props.node.siblings.length)
const isSelected = computed(() => props.node.id === props.selectedId)

const handleClick = () => {
  props.onSelect(props.node)
}
</script>

<style scoped>
.tree-node {
  position: relative;
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.node-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  position: relative;
  overflow: hidden;
}

.node-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  transition: left 0.5s;
}

.node-card:hover::before {
  left: 100%;
}

.node-default:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.node-selected {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: white;
  box-shadow: 0 8px 25px rgba(79, 70, 229, 0.4);
}

.connection-line {
  background: linear-gradient(45deg, #4f46e5, #7c3aed);
  box-shadow: 0 0 10px rgba(79, 70, 229, 0.3);
}

.avatar-circle {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
}

/* Responsive adjustments */
@media (max-width: 1024px) {
  .flex.items-center.ml-8 {
    margin-left: 1.5rem;
  }
  
  .flex.items-center.ml-4 {
    margin-left: 1rem;
  }
  
  .flex.items-center.mr-4 {
    margin-right: 1rem;
  }
}

@media (max-width: 768px) {
  .tree-node {
    font-size: 0.875rem;
  }
  
  .node-card {
    padding: 0.75rem 1rem;
  }
  
  .flex.items-center.ml-8 {
    margin-left: 1rem;
  }
  
  .flex.items-center.ml-4 {
    margin-left: 0.75rem;
  }
  
  .flex.items-center.mr-4 {
    margin-right: 0.75rem;
  }
}

@media (max-width: 640px) {
  .node-card {
    padding: 0.5rem 0.75rem;
  }
  
  .flex.items-center.space-x-3 {
    gap: 0.5rem;
  }
  
  .w-8.h-8 {
    width: 1.5rem;
    height: 1.5rem;
    font-size: 0.75rem;
  }
  
  .flex.items-center.ml-8 {
    margin-left: 0.75rem;
  }
  
  .flex.items-center.ml-4 {
    margin-left: 0.5rem;
  }
  
  .flex.items-center.mr-4 {
    margin-right: 0.5rem;
  }
}

/* Ensure proper horizontal spacing for large families */
.tree-node > div:last-child > div {
  min-width: fit-content;
}
</style>