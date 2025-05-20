import { defineStore } from 'pinia'

type LoginResponse = {
  key: string
}

export const useUserStore = defineStore('user', {
  state: () => ({
    token: null as string | null,
    user: null as any,
  }),
  actions: {
    async login(username: string, password: string) {
      const config = useRuntimeConfig()
      const response = await $fetch<LoginResponse>('/auth/dj-rest-auth/login', {
        baseURL: config.public.apiBase,
        method: 'POST',
        body: { username, password },
      })

      this.token = response.key
      // Optionally fetch user info here
    },

    logout() {
      this.token = null
      this.user = null
    },
  },
})