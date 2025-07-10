<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useNuxtApp } from '#app'
import { VNetworkGraph } from 'v-network-graph'
import 'v-network-graph/lib/style.css'

const route = useRoute()
const { $axios } = useNuxtApp()

const personId = route.params.id
const loaded = ref(false)

const nodes = ref({})
const edges = ref({})
const layouts = ref({})

let marriageCounter = 1
let nextX = 0
const spacingX = 200
const spacingY = 180

function processTree(person, level = 0) {
  if (!person || !person.id) return
  const id = String(person.id)

  // Position X
  const currentX = nextX++
  const x = currentX * spacingX
  const y = level * spacingY

  nodes.value[id] = {
    name: `${person.first_name} ${person.hnam_hming || ''}`.trim(),
    photo: person.photo || null
  }
  layouts.value[id] = { x, y }

  let spouseId = null
  let marriageNodeId = null

  if (person.spouse) {
    const spouse = person.spouse
    spouseId = String(spouse.id)

    nodes.value[spouseId] = {
      name: `${spouse.first_name} ${spouse.hnam_hming || ''}`.trim(),
      photo: spouse.photo || null
    }

    layouts.value[spouseId] = { x: x + 100, y }

    // Link spouses
    const spouseEdgeId = `${id}-${spouseId}`
    edges.value[spouseEdgeId] = {
      source: id,
      target: spouseId,
      type: 'spouse'
    }

    // Create marriage node
    marriageNodeId = `m-${marriageCounter++}`
    nodes.value[marriageNodeId] = { name: '', isMarriageNode: true }
    layouts.value[marriageNodeId] = { x: x + 50, y: y + 30 }

    // Link both spouses to marriage node
    edges.value[`${id}-m-${marriageNodeId}`] = {
      source: id,
      target: marriageNodeId,
      type: 'parent'
    }
    edges.value[`${spouseId}-m-${marriageNodeId}`] = {
      source: spouseId,
      target: marriageNodeId,
      type: 'parent'
    }
  }

  // Recurse into children
  if (Array.isArray(person.children)) {
    for (const child of person.children) {
      processTree(child, level + 1)

      const childId = String(child.id)

      if (marriageNodeId) {
        edges.value[`${marriageNodeId}-${childId}`] = {
          source: marriageNodeId,
          target: childId,
          type: 'parent'
        }
      } else {
        edges.value[`${id}-${childId}`] = {
          source: id,
          target: childId,
          type: 'parent'
        }
      }
    }
  }
}

onMounted(async () => {
  try {
    const res = await $axios.get(`/family-tree/${personId}/deep-family-tree/`)
    const tree = res.data
    nextX = 0  // Reset before rendering
    processTree(tree, 0)
    loaded.value = true
  } catch (err) {
    console.error('Failed to load family tree:', err)
  }
})
</script>


<template>
  <div v-if="loaded" class="w-full h-screen overflow-auto">
    <v-network-graph
      :nodes="nodes"
      :edges="edges"
      :layouts="layouts"
      :configs="{
        node: {
          normal: {
            radius: (node) => node.isMarriageNode ? 5 : 24,
            color: (node) => node.isMarriageNode ? '#666' : '#ddd',
            strokeWidth: 1,
          },
          label: {
            visible: (node) => !node.isMarriageNode
          }
        },
        edge: {
          normal: {
            color: '#999',
            width: 2
          },
          types: {
            spouse: {
              color: '#cc6699',
              width: 2,
              dashed: true
            },
            parent: {
              color: '#3366cc',
              width: 2
            }
          }
        }
      }"
    />
  </div>
  <div v-else class="text-center p-4">Loading family tree...</div>
</template>
