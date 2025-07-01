import { useAuthStore } from '~/stores/auth';

export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();

  // Check if the user is authenticated
  if (!authStore.token) {
    // If not authenticated, redirect to the login page
    return navigateTo('/login');
  }

  // Role-based access control
  if (to.meta.roles) {
    // Assuming authStore.user and authStore.user.role are populated after successful login
    if (!authStore.user || !authStore.user.role || !to.meta.roles.includes(authStore.user.role)) {
      return navigateTo('/unauthorized');
    }
  }
});
