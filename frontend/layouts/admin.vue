<template>
  <div>
    <header>
      <nav>
        <ul>
          <li><NuxtLink to="/">Home</NuxtLink></li>
          <li><NuxtLink to="/admin">Admin Dashboard</NuxtLink></li>
          <li><NuxtLink to="/admin/users">Manage Users</NuxtLink></li>
        </ul>
      </nav>
    </header>
    <main>
      <h1>Admin Layout</h1>
      <slot />
    </main>
    <footer>
      <p>&copy; 2023 Admin Panel</p>
    </footer>
  </div>
</template>
<script setup>
definePageMeta({
  layout: 'admin',
  middleware: 'auth',
  roles: ['admin'],
});
</script>

<style scoped>
header {
  background-color: #e0ffe0;
  padding: 1rem;
}

nav ul {
  list-style: none;
  padding: 0;
  display: flex;
  gap: 1rem;
}

main {
  padding: 1rem;
}

footer {
  background-color: #e0ffe0;
  padding: 1rem;
  text-align: center;
}
</style>