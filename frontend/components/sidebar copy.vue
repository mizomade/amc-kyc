<template>
    <div
      :class="[
        'flex flex-col h-screen bg-white p-4 text-gray-700 shadow-xl transition-all duration-300 fixed top-0 left-0 z-50',
        isOpen ? 'w-64 max-w-[16rem]' : 'w-20 max-w-[5rem]'
      ]"
    >
      <!-- Toggle button -->
      <button
        @click="toggle"
        class="absolute top-4 right-4 p-2 rounded hover:bg-gray-200 transition"
      >
        <Icon
          :name="isOpen ? 'mdi:arrow-left' : 'mdi:arrow-right'"
          class="w-6 h-6"
        />
      </button>
  
      <div class="p-4 mb-4">
        <h5
          v-if="isOpen"
          class="text-xl font-semibold text-blue-gray-900"
        >
          Admin Panel
        </h5>
        <!-- <Icon
          v-else
          name="mdi:view-dashboard"
          class="w-8 h-8"
        /> -->
      </div>
  
      <nav class="flex flex-col gap-1 p-2 text-base font-normal text-blue-gray-700 overflow-y-auto">
        <button
          v-for="item in sidebarItems"
          :key="item.label"
          @click="handleClick(item)"
          :class="[
            'flex items-center w-full p-3 rounded-lg text-start outline-none transition',
            router.currentRoute.value.path === item.path ? 'bg-blue-100 text-blue-800 font-semibold' : 'hover:bg-blue-50 hover:text-blue-900'
          ]"
        >
          <div class="grid place-items-center mr-4">
            <Icon :name="item.icon" class="w-5 h-5" />
          </div>
          <span v-if="isOpen">{{ item.label }}</span>
        </button>
      </nav>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '~/stores/auth'
  
  const isOpen = ref(true)
  
  const toggle = () => {
    isOpen.value = !isOpen.value
  }
  
  const router = useRouter()
  const auth = useAuthStore()
  
  const sidebarItems = [
    { label: 'Dashboard', path: '/admin/', icon: 'material-symbols:dashboard' },
    { label: 'Citizen List', path: '/admin/citizenlist', icon: 'mdi:account-group' },
    { label: 'Reports', path: '/admin/reports', icon: 'mdi:file-chart' },
    { label: 'Family Tree', path: '/admin/treeview', icon: 'mdi:family-tree' },
    { label: 'Issued Certificates', path: '/admin/certificates', icon: 'mdi:certificate' },


    { label: 'User Management', path: '/admin/users', icon: 'mdi:account-cog' },
    // { label: 'Account', path: '/admin/account', icon: 'mdi:account' },
    // { label: 'Settings', path: '/admin/settings', icon: 'mdi:cog' },

    { label: 'Log Out', path: 'logout', icon: 'mdi:logout' },
  ]
  
  const handleClick = async (item) => {
    if (item.path === 'logout') {
      await auth.logout()
      router.push('/login')
    } else {
      router.push(item.path)
    }
  }

  defineExpose({ isOpen });
  </script>
  