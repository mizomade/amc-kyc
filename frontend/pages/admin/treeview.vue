<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <h1 class="text-3xl font-bold text-gray-900 mb-6">Family Tree View</h1>

    <div class="bg-white rounded-lg shadow-md p-6">
      <h2 class="text-xl font-semibold text-gray-900 mb-4">Hierarchical Data Display</h2>

      <div class="overflow-x-auto py-4">
        <div class="flex justify-center items-start">
          <div class="tree-container">
            <TreeNode :node="treeData" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// Define a simple recursive component for tree nodes
const TreeNode = {
  props: {
    node: Object,
  },
  template: `
    <div class="tree-node flex flex-col items-center">
      <div class="node-content bg-blue-500 text-white px-4 py-2 rounded-lg shadow-md cursor-pointer hover:bg-blue-600 transition duration-300">
        {{ node.name }}
      </div>
      <div v-if="node.children && node.children.length" class="node-children flex mt-4">
        <div v-for="child in node.children" :key="child.id" class="flex flex-col items-center mx-4 relative">
          <div class="line-vertical"></div>
          <div class="line-horizontal"></div>
          <TreeNode :node="child" />
        </div>
      </div>
    </div>
  `,
};

// Sample tree data
const treeData = ref({
  id: 1,
  name: 'Grandparent A',
  children: [
    {
      id: 2,
      name: 'Parent B',
      children: [
        { id: 4, name: 'Child D' },
        { id: 5, name: 'Child E' },
      ],
    },
    {
      id: 3,
      name: 'Parent C',
      children: [
        { id: 6, name: 'Child F' },
      ],
    },
  ],
});

definePageMeta({
  layout: 'admin',
  middleware: 'auth',
//   roles: ['admin'],
});
</script>

<style scoped>
.tree-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 20px;
}

.tree-node {
  position: relative;
}

.node-children {
  position: relative;
  justify-content: center;
}

.node-children > div {
  position: relative;
}

.line-vertical {
  position: absolute;
  top: -20px;
  left: 50%;
  width: 2px;
  height: 20px;
  background-color: #ccc;
  transform: translateX(-50%);
}

.line-horizontal {
  position: absolute;
  top: -20px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #ccc;
}

.node-children > div:first-child .line-horizontal {
  left: 50%;
  width: 50%;
}

.node-children > div:last-child .line-horizontal {
  width: 50%;
}

.node-children > div:only-child .line-horizontal {
  width: 0;
}
</style>
