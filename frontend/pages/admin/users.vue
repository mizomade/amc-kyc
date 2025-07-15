<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900">User Management</h1>
      <button @click="showCreateModal = true" class="bg-blue-600 text-white py-2 px-4 rounded-md shadow-md hover:bg-blue-700 transition duration-300">
        Add New User
      </button>
    </div>

    <div class="bg-white rounded-lg shadow-md p-6">
      <h2 class="text-xl font-semibold text-gray-900 mb-4">All Users</h2>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Username</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="user in users" :key="user.id">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ user.username }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ user.email }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ user.role }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <a href="#" @click.prevent="openEditModal(user)" class="text-blue-600 hover:text-blue-900 mr-4">Edit</a>
                <a href="#" @click.prevent="openDeleteModal(user)" class="text-red-600 hover:text-red-900">Delete</a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create User Modal -->
    <Modal :show="showCreateModal" title="Add New User" @close="showCreateModal = false">
      <form @submit.prevent="createUser">
        <div class="mb-4">
          <label for="newUsername" class="block text-sm font-medium text-gray-700">Username</label>
          <input type="text" id="newUsername" v-model="newUser.username" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" required>
        </div>
        <div class="mb-4">
          <label for="newEmail" class="block text-sm font-medium text-gray-700">Email</label>
          <input type="email" id="newEmail" v-model="newUser.email" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" required>
        </div>
        <div class="mb-4">
          <label for="newPassword" class="block text-sm font-medium text-gray-700">Password</label>
          <input type="password" id="newPassword" v-model="newUser.password" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" required>
        </div>
        <div class="mb-4">
          <label for="newRole" class="block text-sm font-medium text-gray-700">Role</label>
          <select id="newRole" v-model="newUser.role" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2">
            <option value="">Select a role</option>
            <option v-for="group in groups" :key="group.name" :value="group.name">{{ group.name }}</option>
          </select>
        </div>
        <div class="flex justify-end">
          <button type="button" @click="showCreateModal = false" class="bg-gray-300 text-gray-800 py-2 px-4 rounded-md mr-2">Cancel</button>
          <button type="submit" class="bg-blue-600 text-white py-2 px-4 rounded-md">Add User</button>
        </div>
      </form>
    </Modal>

    <!-- Edit User Modal -->
    <Modal :show="showEditModal" title="Edit User" @close="showEditModal = false">
      <form @submit.prevent="editUser">
        <div class="mb-4">
          <label for="editUsername" class="block text-sm font-medium text-gray-700">Username</label>
          <input type="text" id="editUsername" v-model="editingUser.username" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" required>
        </div>
        <div class="mb-4">
          <label for="editEmail" class="block text-sm font-medium text-gray-700">Email</label>
          <input type="email" id="editEmail" v-model="editingUser.email" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" required>
        </div>
        <div class="mb-4">
          <label for="editRole" class="block text-sm font-medium text-gray-700">Role</label>
          <select id="editRole" v-model="editingUser.role" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2">
            <option value="">Select a role</option>
            <option v-for="group in groups" :key="group.name" :value="group.name">{{ group.name }}</option>
          </select>
        </div>
        <div class="flex justify-end">
          <button type="button" @click="showEditModal = false" class="bg-gray-300 text-gray-800 py-2 px-4 rounded-md mr-2">Cancel</button>
          <button type="submit" class="bg-blue-600 text-white py-2 px-4 rounded-md">Save Changes</button>
        </div>
      </form>
    </Modal>

    <!-- Delete User Modal -->
    <Modal :show="showDeleteModal" title="Delete User" @close="showDeleteModal = false">
      <p class="text-gray-700 mb-4">Are you sure you want to delete user <span class="font-semibold">{{ deletingUser.username }}</span>?</p>
      <div class="flex justify-end">
        <button type="button" @click="showDeleteModal = false" class="bg-gray-300 text-gray-800 py-2 px-4 rounded-md mr-2">Cancel</button>
        <button type="button" @click="deleteUser" class="bg-red-600 text-white py-2 px-4 rounded-md">Delete</button>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useNuxtApp } from '#app';
import Modal from '~/components/Modal.vue';

const users = ref([]);
const groups = ref([]); // New ref for groups
const { $api } = useNuxtApp();

const showCreateModal = ref(false);
const showEditModal = ref(false);
const showDeleteModal = ref(false);

const newUser = ref({
  username: '',
  email: '',
  password: '',
  role: '',
});

const editingUser = ref({});
const deletingUser = ref({});

const fetchUsers = async () => {
  try {
    const response = await $api.get('/user/');
    users.value = response.data.map(user => ({
      ...user,
      role: user.groups.map(g => g.name).join(', ')
    }));
  } catch (error) {
    console.error('Failed to fetch users:', error);
  }
};

const fetchGroups = async () => {
  try {
    const response = await $api.get('/user/getch/groups/');
    groups.value = response.data;
  } catch (error) {
    console.error('Failed to fetch groups:', error);
  }
};

const openEditModal = (user) => {
  editingUser.value = { ...user };
  // Pre-select the role in the dropdown
  editingUser.value.role = user.groups.length > 0 ? user.groups[0].name : '';
  showEditModal.value = true;
};

const openDeleteModal = (user) => {
  deletingUser.value = { ...user };
  showDeleteModal.value = true;
};

const createUser = async () => {
  try {
    await $api.post('/user/', newUser.value);
    showCreateModal.value = false;
    await fetchUsers(); // Refresh user list
    newUser.value = { username: '', email: '', password: '', role: '' }; // Clear form
  } catch (error) {
    console.error('Failed to create user:', error);
  }
};

const editUser = async () => {
  try {
    await $api.put(`/user/${editingUser.value.id}/`, editingUser.value);
    showEditModal.value = false;
    await fetchUsers(); // Refresh user list
  } catch (error) {
    console.error('Failed to edit user:', error);
  }
};

const deleteUser = async () => {
  try {
    await $api.delete(`/user/${deletingUser.value.id}/`);
    showDeleteModal.value = false;
    await fetchUsers(); // Refresh user list
  } catch (error) {
    console.error('Failed to delete user:', error);
  }
};

onMounted(() => {
  fetchUsers();
  fetchGroups(); // Fetch groups on component mount
});

definePageMeta({
  layout: 'admin',
  middleware: 'auth',
  // roles: ['admin'],
});
</script>

<style scoped>
/* Tailwind CSS handles most styling, no custom styles needed here */
</style>
