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
    
    <!-- This Node and its horizontal relatives -->
    <div class="flex items-center justify-center">
      <!-- Siblings -->
      <div v-if="hasSiblings" class="flex items-center">
        <div
          v-for="sibling in node.siblings"
          :key="sibling.id"
          class="flex items-center mx-4 relative"
        >
          <TreeNode
            :node="sibling"
            :onSelect="onSelect"
            :selectedId="selectedId"
            :generation="generation"
          />
          <!-- Connector to main node -->
          <div class="absolute top-1/2 h-0.5 connection-line rounded-full w-full left-1/2"></div>
        </div>
      </div>
      
      <!-- This Node -->
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
      
      <!-- Spouse -->
      <div v-if="node.spouse" class="flex items-center mx-6 relative">
        <TreeNode
          :node="node.spouse"
          :onSelect="onSelect"
          :selectedId="selectedId"
          :generation="generation"
        />
        <!-- Connector to main node -->
        <div class="absolute top-1/2 h-0.5 connection-line rounded-full w-full right-1/2"></div>
      </div>
    </div>
    
    <!-- Downward children -->
    <div v-if="hasChildren" class="flex justify-center items-start mt-6 relative">
      <!-- Vertical line from this node -->
      <div class="absolute bottom-full h-6 w-0.5 connection-line left-1/2 -translate-x-1/2 rounded-full"></div>
      
      <!-- Horizontal line above children -->
      <div class="absolute top-0 w-full h-0.5 connection-line rounded-full"></div>
      
      <div
        v-for="child in node.children"
        :key="child.id"
        class="flex flex-col items-center mx-6 relative"
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
@media (max-width: 768px) {
  .tree-node {
    font-size: 0.875rem;
  }
  
  .node-card {
    padding: 0.75rem 1rem;
  }
  
  .flex.items-center.mx-6 {
    margin-left: 1rem;
    margin-right: 1rem;
  }
  
  .flex.items-center.mx-4 {
    margin-left: 0.5rem;
    margin-right: 0.5rem;
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
}
</style>