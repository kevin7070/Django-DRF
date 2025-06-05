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
    await $fetch('/auth/nuxt/csrf/', {
      method: 'GET',
      baseURL: useRuntimeConfig().public.apiBase,
      credentials: 'include',
    })

    const response = await $fetch<LoginResponse>('/auth/nuxt/login/', {
      method: 'POST',
      baseURL: useRuntimeConfig().public.apiBase,
      body: { username, password },
      credentials: 'include',
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