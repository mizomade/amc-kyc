<template>
  <div>
    <header>
      <nav>
        <ul>
          <li><NuxtLink to="/">Citizen Management System</NuxtLink></li>
          <!-- <li><NuxtLink to="/login">Login</NuxtLink></li>
          <li><NuxtLink to="/admin">Admin Dashboard (Example)</NuxtLink></li>
          <li><NuxtLink to="/local_council">Local Council Dashboard (Example)</NuxtLink></li>
          <li><NuxtLink to="/operator">Operator Dashboard (Example)</NuxtLink></li> -->
        </ul>
      </nav>
    </header>
    <main>
      <slot />
    </main>
    <footer>
      <p>&copy; 2023 My App</p>
    </footer>
  </div>
</template>

<style scoped>
header {
  background-color: #f0f0f0;
  padding: 1rem;
}

nav ul {
  list-style: none;
  padding: 0;
  display: flex;
  gap: 1rem;
}

/* main {
  padding: 1rem;
} */

footer {
  background-color: #f0f0f0;
  padding: 1rem;
  text-align: center;
}
</style>