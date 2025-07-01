<template>
  <div>
    <header>
      <nav>
        <ul>
          <li><NuxtLink to="/">Home</NuxtLink></li>
          <li><NuxtLink to="/operator">Operator Dashboard</NuxtLink></li>
        </ul>
      </nav>
    </header>
    <main>
      <h1>Operator Layout</h1>
      <slot />
    </main>
    <footer>
      <p>&copy; 2023 Operator Panel</p>
    </footer>
  </div>
</template>
<script setup>
definePageMeta({
  layout: 'operator',
  middleware: 'auth',
  roles: ['operator'],
});
</script>

<style scoped>
header {
  background-color: #ffe0e0;
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
  background-color: #ffe0e0;
  padding: 1rem;
  text-align: center;
}
</style>