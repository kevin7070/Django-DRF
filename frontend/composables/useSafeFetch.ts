export async function useSafeFetch<T>(url: string, options: any = {}) {
  const baseURL = useRuntimeConfig().public.apiBase;
  const userStore = useUserStore();

  try {
    return await $fetch<T>(url, {
      baseURL,
      credentials: 'include',
      ...options,
    });
  } catch (err: any) {
    const status = err.response?.status;

    // Check if the error is a CSRF error 
    const isCsrfError = status === 403 &&
      err.response?.data?.detail?.toLowerCase().includes('csrf');

    // If it is a CSRF error, try to refresh the CSRF token
    if (isCsrfError) {
      try {
        console.warn('CSRF failed — attempting to refresh CSRF token...');
        await $fetch('/auth/nuxt/csrf/', {
          baseURL,
          credentials: 'include',
        });
        // Retry original request
        return await $fetch<T>(url, {
          baseURL,
          credentials: 'include',
          ...options,
        });
      } catch (err) {
        console.error("Failed to refresh CSRF")
        await userStore.logout();
        throw err;
      }
    }

    // Check if the error is an authentication error
    if (status === 401) {
      try {
        await $fetch("/auth/nuxt/refresh/", {
          method: "POST",
          baseURL,
          credentials: "include", // 帶 refresh token cookie
        });
        console.log("Token refreshed. Retrying original request...");
        // Retry original request
        return await $fetch<T>(url, {
          baseURL,
          credentials: 'include',
          ...options,
        });
      } catch (err) {
        console.error("Failed to refresh token. Logging out...");
        await userStore.logout();
        throw err;
      }
    }
    throw err;
  }
}