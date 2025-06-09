type User = {
  pk: number
  username: string
  email: string
}

type LoginResponse = {
  detail: string
  user: User
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

    if (response.user) {
      user.value = response.user
    }
  }

  const logout = async () => {
    try {
      await $fetch('/auth/nuxt/logout/', {
        method: 'POST',
        baseURL: useRuntimeConfig().public.apiBase,
        credentials: 'include',
      })
      user.value = null
    } catch (e) {
      console.error(e)
    }
  }

  return {
    user,
    login,
    logout,
  }
}, {
  persist: true, // store in cookies
})