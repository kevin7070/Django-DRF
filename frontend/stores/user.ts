type LoginResponse = {
  key: string
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
    await $fetch('/auth/nuxt/csrf', {
      method: 'GET',
      baseURL: useRuntimeConfig().public.apiBase,
      credentials: 'include',
    })

    const csrftoken = useCookie('csrftoken').value

    const res = await $fetch<LoginResponse>('/auth/nuxt/login', {
      method: 'POST',
      baseURL: useRuntimeConfig().public.apiBase,
      credentials: 'include',
      headers: {
        'X-CSRFToken': csrftoken || '',
      },
      body: {
        username,
        password,
      },
    })

    if (res) {
      const userInfo = await $fetch<User>('/auth/nuxt/user', {
        method: 'GET',
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

  return { user, login, logout }
}, {
  persist: true,
}
)