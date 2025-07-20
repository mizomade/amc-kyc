<template>
  <div class="w-full h-[90vh] bg-white rounded-xl shadow p-4 overflow-auto border relative">
    <!-- Center Button -->
    <!-- <button
      @click="centerGraph"
      class="absolute top-2 right-2 z-10 px-3 py-1.5 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 shadow"
    >
      Center Tree View
    </button> -->
      <div class="flex justify-between items-center mb-4">
        <!-- <h1 class="text-2xl font-bold text-gray-800">Family Tree View</h1> -->
        <div class="flex items-center space-x-2">
          <button @click="graphRef?.panToCenter()" class="bg-blue-600 text-white px-3 rounded">To center</button>
          <button @click="graphRef?.fitToContents()" class="bg-blue-600 text-white px-3 rounded">Fit</button>
          <!-- <button @click="graphRef?.zoomIn()" class="bg-blue-600 text-white px-3 rounded">Zoom In</button> -->
          <!-- <button @click="graphRef?.zoomOut()" class="bg-blue-600 text-white px-3 rounded">Zoom Out</button> -->
          <!-- <el-slider-custom-zoom v-model="zoomLevel" /> -->
          <!-- Zoom Slider -->
<div class=" flex items-center gap-4">
  <label class="text-sm font-medium text-gray-700">Zoom</label>
  <input
    type="range"
    min="0.2"
    max="2"
    step="0.1"
    v-model="zoomLevel"
    class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
  />
  <!-- <span class="text-sm text-gray-600">{{ zoomLevel.toFixed(1) }}x</span> -->
</div>

        </div>
      </div>
   

    <v-network-graph
      ref="graphRef"
      :nodes="nodes"
      :edges="edges"
      :layouts="layouts"
      :configs="configs"
      :event-handlers="eventHandlers"
          v-model:zoom-level="zoomLevel"

    >
      <template
        #override-node-label="{
          nodeId, scale, text, x, y, config, textAnchor, dominantBaseline
        }"
      >
        <text
          x="0"
          y="0"
          :font-size="9 * scale"
          text-anchor="middle"
          dominant-baseline="central"
          fill="#ffffff" 
        >
          {{ nodes[nodeId]?.name || nodeId }}
        </text>
        <!-- <text
          x="0"
          y="0"
          :font-size="config.fontSize * scale"
          :text-anchor="textAnchor"
          :dominant-baseline="dominantBaseline"
          :fill="config.color"
          :transform="`translate(${x} ${y})`"
        >{{ text }}</text> -->
      </template>
    </v-network-graph>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { VNetworkGraph } from 'v-network-graph'
import 'v-network-graph/lib/style.css'
import { useNuxtApp } from '#app'

const { $api } = useNuxtApp()
const props = defineProps({ personId: Number, data: Object })
const emit = defineEmits(['node-selected'])

const nodes = ref({})
const edges = ref([])
const layouts = ref({ nodes: {} })
const graphRef = ref(null)

const zoomLevel = ref(1)


const eventHandlers = {
  'node:click': ({ node }) => {
    const clickedNode = nodes.value[node]
    if (clickedNode?.isUnion) return
    emit('node-selected', { id: node, ...clickedNode })
  },
}

const configs = {
  node: {
    normal: {
      type: 'rect',
      radius: node => (node.isUnion ? 6 : 20),
      width: node => (node.isUnion ? 10 : Math.max(30, (node.name || '').length * 6)),
      height: node => (node.isUnion ? 10 : 32),
      color: node => (node.isUnion ? '#10b981' : '#4f46e5'),
      strokeWidth: 2,
      strokeColor: '#c7d2fe',
    },
    label: {
      visible: node => !node.isUnion,
      fontSize: 12,
      color: '#111827',
    },
  },
  edge: {
    type: 'curve',
    normal: {
      width: 3,
      color: edge => edge.type === 'spouse' ? '#ec4899' : edge.type === 'union' ? '#10b981' : '#9ca3af',
      dasharray: edge => edge.type === 'spouse' ? '6,4' : '0',
      marker: edge => edge.type === 'parent' ? 'arrow' : null,
    },
    gap: 40,
    marker: {
      target: {
        type: 'angle',
        width: 4,
        height: 4,
        margin: -10,
      },
    },
  },
}

const buildGraph = (data, y = 0, x = 0, visited = new Set()) => {
  if (!data || visited.has(data.id)) return
  visited.add(data.id)

  nodes.value[data.id] = { name: data.name }
  layouts.value.nodes[data.id] = { x, y }

  if (data.spouse && !visited.has(data.spouse.id)) {
    visited.add(data.spouse.id)
    nodes.value[data.spouse.id] = { name: data.spouse.name }
    layouts.value.nodes[data.spouse.id] = { x: x - 150, y }

    edges.value.push({ source: data.id, target: data.spouse.id, type: 'spouse' })
  }

  let unionId = null
  if (data.parents?.length === 2 && data.parents.every(p => p?.id)) {
    const [father, mother] = data.parents
    unionId = `union_${father.id}_${mother.id}`

    if (!nodes.value[unionId]) {
      nodes.value[unionId] = { name: '', isUnion: true }
      layouts.value.nodes[unionId] = { x, y: y - 50 }

      edges.value.push({ source: father.id, target: unionId, type: 'union' })
      edges.value.push({ source: mother.id, target: unionId, type: 'union' })
    }
    edges.value.push({ source: unionId, target: data.id, type: 'parent' })
  } else if (data.parents?.length) {
    data.parents.forEach(parent => {
      if (parent && !visited.has(parent.id)) buildGraph(parent, y - 200, x, visited)
      if (parent) edges.value.push({ source: parent.id, target: data.id, type: 'parent' })
    })
  }

  if (data.parents?.length) {
    data.parents.forEach((parent, index) => {
      if (parent && !visited.has(parent.id)) {
        buildGraph(parent, y - 200, x + index * 200 - 50, visited)
      }
    })
  }

  let selfUnionId = null
  if (data.spouse) {
    selfUnionId = `union_${data.id}_${data.spouse.id}`
    if (!nodes.value[selfUnionId]) {
      nodes.value[selfUnionId] = { name: '', isUnion: true }
      layouts.value.nodes[selfUnionId] = { x: x - 75, y: y + 100 }
      edges.value.push({ source: data.id, target: selfUnionId, type: 'union' })
      edges.value.push({ source: data.spouse.id, target: selfUnionId, type: 'union' })
    }
  }

  if (data.children?.length) {
    const spacing = 200
    data.children.forEach((child, index) => {
      const childX = x + index * spacing - ((data.children.length - 1) * spacing) / 2
      buildGraph(child, y + 200, childX, visited)
      if (selfUnionId) {
        edges.value.push({ source: selfUnionId, target: child.id, type: 'parent' })
      } else {
        edges.value.push({ source: data.id, target: child.id, type: 'parent' })
      }
    })
  }

  if (data.siblings?.length && unionId) {
    data.siblings.forEach((sibling, index) => {
      if (!visited.has(sibling.id)) {
        visited.add(sibling.id)
        nodes.value[sibling.id] = { name: sibling.name }
        const siblingX = x + (index + 1) * 200
        layouts.value.nodes[sibling.id] = { x: siblingX, y }
        edges.value.push({ source: unionId, target: sibling.id, type: 'parent' })
      }
    })
  }
}

const loadPersonTree = async () => {
  nodes.value = {}
  edges.value = []
  layouts.value = { nodes: {} }
  buildGraph(props.data || {}, 0, 0)
}

const centerGraph = () => {
  graphRef.value?.reset()
}

onMounted(() => {
  if (props.data) loadPersonTree()
})

watch(() => props.data, (newData) => {
  if (newData) loadPersonTree()
})
</script>
