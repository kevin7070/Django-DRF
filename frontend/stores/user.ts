type LoginResponse = {
  detail: string
}
type User = {
  pk: number
  username: string
  email: string
  phone: string
}

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)

  const login = async (username: string, password: string) => {
    const { csrfToken } = await $fetch<{ csrfToken: string }>('/auth/nuxt/csrf/', {
      method: 'GET',
      baseURL: useRuntimeConfig().public.apiBase,
      credentials: 'include',
    })

    // Debug
    console.log("Fetched CSRF token", csrfToken)

    const response = await $fetch<LoginResponse>('/auth/nuxt/login/', {
      method: 'POST',
      baseURL: useRuntimeConfig().public.apiBase,
      body: { username, password },
      credentials: 'include',
      headers: {
        'X-CSRFToken': csrfToken,
      },
    })

    if (response) {
      const userInfo = await $fetch<User>('/auth/nuxt/user/', {
        baseURL: useRuntimeConfig().public.apiBase,
        credentials: 'include',
      })
      user.value = userInfo
    }
  }

  const logout = async () => {
    await $fetch('/auth/nuxt/logout/', {
      method: 'POST',
      baseURL: useRuntimeConfig().public.apiBase,
      credentials: 'include',
    })
    user.value = null
  }

  return {
    user,
    login,
    logout,
  }
}, {
  persist: true, // store in cookies
})