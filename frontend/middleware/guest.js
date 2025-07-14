import { useAuthStore } from '~/stores/auth';

export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();

  if (authStore.isAuthenticated) {
    if (authStore.user && authStore.user.role) {
      const role = authStore.user.role.name.toLowerCase();
      if (role === 'admin') {
        return navigateTo('/admin');
      } else if (role === 'local_council') {
        return navigateTo('/local-council');
      } else if (role === 'operator') {
        return navigateTo('/operator');
      }
    }
    // If the user is authenticated but has no specific role, 
    // or the role doesn't match a dashboard, redirect to a generic authenticated page.
    return navigateTo('/'); 
  }
});
