<template>
  <div class="w-full h-[90vh] bg-white rounded-xl shadow p-4 overflow-auto">
    <v-network-graph
      :nodes="nodes"
      :edges="edges"
      :layouts="layouts"
      :configs="configs"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { VNetworkGraph } from 'v-network-graph'
import 'v-network-graph/lib/style.css'
import { useNuxtApp } from '#app'

const { $api } = useNuxtApp()

const nodes = ref({})
const edges = ref([])
const layouts = ref({ nodes: {} })

const configs = {
  node: {
    normal: {
      radius: node => (node.isUnion ? 6 : 20),
      color: node => (node.isUnion ? '#10b981' : '#4f46e5'),
      strokeWidth: 2,
      strokeColor: '#c7d2fe'
    },
    label: {
      visible: node => !node.isUnion,
      fontSize: 12,
      color: '#111827',
    }
  },
  edge: {
    normal: {
      width: 3,
      color: edge => {
        if (edge.type === 'spouse') return '#ec4899'
        if (edge.type === 'union') return '#10b981'
        return '#9ca3af'
      },
      dasharray: edge => {
        if (edge.type === 'spouse') return '6,4'
        return '0'
      }
    }
  }
}

// Recursive Graph Builder
function buildGraph(data, y = 0, x = 0, visited = new Set()) {
  if (!data || visited.has(data.id)) return
  visited.add(data.id)

  nodes.value[data.id] = { name: data.name }
  layouts.value.nodes[data.id] = { x, y }

  // Spouse
  if (data.spouse && !visited.has(data.spouse.id)) {
    visited.add(data.spouse.id)
    nodes.value[data.spouse.id] = { name: data.spouse.name }
    layouts.value.nodes[data.spouse.id] = { x: x + 80, y }

    edges.value.push({
      source: data.id,
      target: data.spouse.id,
      type: 'spouse'
    })
  }

  // Union node for parents
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

    edges.value.push({ source: unionId, target: data.id })
  } else if (data.parents?.length) {
    data.parents.forEach(parent => {
      if (parent && !visited.has(parent.id)) {
        buildGraph(parent, y - 200, x, visited)
      }
      if (parent) {
        edges.value.push({ source: parent.id, target: data.id, type: 'parent' })
      }
    })
  }

  // Recursively build parents
  if (data.parents?.length) {
    data.parents.forEach((parent, index) => {
      if (parent && !visited.has(parent.id)) {
        buildGraph(parent, y - 200, x + index * 100 - 50, visited)
      }
    })
  }

  // Union node for children
  let selfUnionId = null
  if (data.spouse) {
    selfUnionId = `union_${data.id}_${data.spouse.id}`
    if (!nodes.value[selfUnionId]) {
      nodes.value[selfUnionId] = { name: '', isUnion: true }
      layouts.value.nodes[selfUnionId] = { x: x + 40, y: y + 100 }
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
        edges.value.push({ source: selfUnionId, target: child.id })
      } else {
        edges.value.push({ source: data.id, target: child.id })
      }
    })
  }

  // Siblings
  if (data.siblings?.length && unionId) {
    data.siblings.forEach((sibling, index) => {
      if (!visited.has(sibling.id)) {
        visited.add(sibling.id)
        nodes.value[sibling.id] = { name: sibling.name }
        const siblingX = x + (index + 1) * 150
        layouts.value.nodes[sibling.id] = { x: siblingX, y }

        edges.value.push({ source: unionId, target: sibling.id })
      }
    })
  }
}

const personId = 7

onMounted(async () => {
  const res = await $api.get(`/family-tree-v3/tree/${personId}`)
  buildGraph(res.data)
})
</script>
