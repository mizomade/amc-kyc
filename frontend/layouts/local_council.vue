<template>
  <div>
    <header>
      <nav>
        <ul>
          <li><NuxtLink to="/">Home</NuxtLink></li>
          <li><NuxtLink to="/local_council">Local Council Dashboard</NuxtLink></li>
        </ul>
      </nav>
    </header>
    <main>
      <h1>Local Council Layout</h1>
      <slot />
    </main>
    <footer>
      <p>&copy; 2023 Local Council Panel</p>
    </footer>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'local_council',
  middleware: 'auth',
  roles: ['local_council'],
});

</script>
<style scoped>
header {
  background-color: #e0e0ff;
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
  background-color: #e0e0ff;
  padding: 1rem;
  text-align: center;
}
</style>