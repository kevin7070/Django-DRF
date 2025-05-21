import tailwindcss from "@tailwindcss/vite";
// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2025-05-15",
  devtools: { enabled: true },
  css: ["~/assets/css/main.css"],

  runtimeConfig: {
    public: {
      apiBase: "https://api.wowd.cc/api/v1",
    },
  },

  modules: ["@pinia/nuxt"],

  vite: {
    plugins: [tailwindcss()],
  },
});
